"""Controlador del historial: crear/borrar tablas, insertar y consultar.

Es la única capa que habla con la base de datos: ejecuta el SQL y maneja
la conexión (se abre la primera vez que se necesita y se reabre si se
cerró). Las vistas y las pruebas solo llaman a sus métodos: no conocen la
conexión ni escriben SQL. Reutiliza CalculadoraPensionController para el
cálculo de negocio.
"""

from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import Callable, Iterator, List, Optional

import psycopg2
from psycopg2.extensions import connection as Conexion
from psycopg2.extensions import cursor as Cursor

from controller.pension_controller import CalculadoraPensionController
from model.calculo_pension import CalculoPension
from model.conexion import ConfiguracionFaltante, ErrorConexion, obtener_conexion
from model.logica_pension import DatosPension

# Los scripts SQL viven en la carpeta sql/ de la raíz del proyecto.
CARPETA_SQL = Path(__file__).resolve().parents[2] / "sql"

LONGITUD_MAXIMA_CEDULA = 20   # Debe coincidir con VARCHAR(20) de persona.cedula.
LONGITUD_MAXIMA_NOMBRE = 100  # Debe coincidir con VARCHAR(100) de persona.nombre.


class ErrorHistorial(Exception):
    """Excepción base de los errores del historial."""


class CedulaInvalida(ErrorHistorial):
    """La cédula está vacía, no es numérica o es demasiado larga."""

    def __init__(self, cedula: Optional[str] = None):
        super().__init__(
            f"La cédula no es válida (recibido: '{cedula}'). "
            f"Solución: ingrese solo dígitos (máximo {LONGITUD_MAXIMA_CEDULA}), "
            "sin puntos ni espacios."
        )


class NombreInvalido(ErrorHistorial):
    """El nombre está vacío o es demasiado largo."""

    def __init__(self):
        super().__init__(
            "El nombre no es válido: no puede estar vacío ni superar "
            f"{LONGITUD_MAXIMA_NOMBRE} caracteres. Solución: ingréselo de nuevo."
        )


class ErrorConexionHistorial(ErrorHistorial):
    """No fue posible abrir la conexión (falta configuración o falla de red)."""

    def __init__(self, causa: Exception):
        super().__init__(str(causa))


class ErrorBaseDeDatos(ErrorHistorial):
    """Falla de la base de datos (tablas inexistentes, SQL inválido, etc.)."""

    def __init__(self, causa: Exception):
        super().__init__(
            f"Error de base de datos: {str(causa).strip()}. Solución: verifique "
            "la conexión y que las tablas estén creadas (opción 'Crear tablas')."
        )


def _leer_sql(nombre_archivo: str) -> str:
    """Lee un script de la carpeta sql/ del proyecto."""
    return (CARPETA_SQL / nombre_archivo).read_text(encoding="utf-8")


class HistorialPensionController:
    """Casos de uso de persistencia del historial de cálculos."""

    def __init__(
        self,
        fabrica_conexion: Callable[[], Conexion] = obtener_conexion,
        calculadora: Optional[CalculadoraPensionController] = None,
    ):
        self._fabrica_conexion = fabrica_conexion
        self._conexion: Optional[Conexion] = None
        self.calculadora = calculadora or CalculadoraPensionController()

    @classmethod
    def en_esquema(cls, esquema: str) -> "HistorialPensionController":
        """Controlador que trabaja en un esquema aparte (para las pruebas)."""
        return cls(fabrica_conexion=partial(obtener_conexion, esquema=esquema))

    # --- Conexión ---------------------------------------------------------
    def _conexion_activa(self) -> Conexion:
        """Abre la conexión la primera vez (o si se cerró) y la reutiliza."""
        if self._conexion is None or self._conexion.closed:
            try:
                self._conexion = self._fabrica_conexion()
            except (ConfiguracionFaltante, ErrorConexion) as error:
                raise ErrorConexionHistorial(error) from error
        return self._conexion

    def cerrar(self) -> None:
        """Cierra la conexión si está abierta."""
        if self._conexion is not None and not self._conexion.closed:
            self._conexion.close()
        self._conexion = None

    @contextmanager
    def _transaccion(self) -> Iterator[Cursor]:
        """Entrega un cursor; hace commit al terminar o rollback si algo falla."""
        conexion = self._conexion_activa()
        try:
            with conexion.cursor() as cursor:
                yield cursor
            conexion.commit()
        except psycopg2.Error as error:
            conexion.rollback()
            raise ErrorBaseDeDatos(error) from error
        except Exception:
            conexion.rollback()
            raise

    def _ejecutar(self, sentencia: str, parametros: Optional[tuple] = None) -> List[tuple]:
        """Ejecuta una sentencia dentro de una transacción y retorna sus filas."""
        with self._transaccion() as cursor:
            cursor.execute(sentencia, parametros)
            return cursor.fetchall() if cursor.description else []

    # --- Crear y borrar tablas ------------------------------------------
    def crear_tablas(self) -> None:
        """CREATE TABLE: ejecuta sql/crear_tablas.sql (no borra datos existentes)."""
        self._ejecutar(_leer_sql("crear_tablas.sql"))

    def borrar_tablas(self) -> None:
        """DROP TABLE: ejecuta sql/borrar_tablas.sql (borra TODOS los datos)."""
        self._ejecutar(_leer_sql("borrar_tablas.sql"))

    # --- Insertar -------------------------------------------------------
    def calcular_y_guardar(
        self, cedula: str, nombre: str, datos: DatosPension
    ) -> CalculoPension:
        """Calcula la pensión y guarda el cálculo (INSERT INTO).

        Si los datos violan una regla de negocio, ErrorCalculoPension se
        propaga y NO se guarda nada. Si la persona ya existe (misma
        cédula) se reutiliza y se conserva su nombre original.
        """
        cedula = self._validar_cedula(cedula)
        nombre = self._validar_nombre(nombre)
        resultado = self.calculadora.calcular(datos)

        with self._transaccion() as cursor:
            cursor.execute(
                """
                INSERT INTO persona (cedula, nombre) VALUES (%s, %s)
                ON CONFLICT (cedula) DO UPDATE SET cedula = EXCLUDED.cedula
                RETURNING id
                """,
                (cedula, nombre),
            )
            persona_id = cursor.fetchone()[0]
            cursor.execute(
                """
                INSERT INTO calculopension (
                    persona_id, ibc_ultimos_10, ibc_toda_vida,
                    salario_minimo_legal, semanas_cotizadas, edad, sexo,
                    ibl, tasa_total, pension
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    persona_id,
                    datos.ibc_ultimos_10,
                    datos.ibc_toda_vida,
                    datos.salario_minimo_legal,
                    datos.semanas_cotizadas,
                    datos.edad,
                    datos.sexo,
                    resultado.ibl,
                    resultado.tasa_total,
                    resultado.pension,
                ),
            )
            calculo_id = cursor.fetchone()[0]

        return self._buscar_por_id(calculo_id)

    # --- Consultar ------------------------------------------------------
    def buscar_por_cedula(self, cedula: str) -> List[CalculoPension]:
        """SELECT: cálculos de una persona, del más reciente al más antiguo.

        Retorna lista vacía si la persona no existe o no tiene cálculos.
        """
        cedula = self._validar_cedula(cedula)
        filas = self._ejecutar(
            CalculoPension.SQL_SELECT + " WHERE p.cedula = %s ORDER BY c.id DESC",
            (cedula,),
        )
        return [CalculoPension.desde_fila(fila) for fila in filas]

    def listar_todos(self) -> List[CalculoPension]:
        """SELECT: todos los cálculos guardados."""
        filas = self._ejecutar(CalculoPension.SQL_SELECT + " ORDER BY c.id")
        return [CalculoPension.desde_fila(fila) for fila in filas]

    def _buscar_por_id(self, calculo_id: int) -> CalculoPension:
        filas = self._ejecutar(
            CalculoPension.SQL_SELECT + " WHERE c.id = %s", (calculo_id,)
        )
        return CalculoPension.desde_fila(filas[0])

    # --- Validación de los datos de la persona ---------------------------
    @staticmethod
    def _validar_cedula(cedula: Optional[str]) -> str:
        limpia = (cedula or "").strip()
        es_numerica = limpia.isascii() and limpia.isdigit()
        if not es_numerica or len(limpia) > LONGITUD_MAXIMA_CEDULA:
            raise CedulaInvalida(cedula=cedula)
        return limpia

    @staticmethod
    def _validar_nombre(nombre: Optional[str]) -> str:
        limpio = (nombre or "").strip()
        if not limpio or len(limpio) > LONGITUD_MAXIMA_NOMBRE:
            raise NombreInvalido()
        return limpio