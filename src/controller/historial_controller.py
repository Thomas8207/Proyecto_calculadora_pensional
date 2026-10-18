"""Controlador del historial: crear/borrar tablas, insertar y consultar.

Recibe una conexión psycopg2 y ejecuta el SQL. Reutiliza
CalculadoraPensionController para el cálculo de negocio.
"""

from typing import List

import psycopg2

from controller.pension_controller import CalculadoraPensionController
from model.logica_pension import DatosPension
from pathlib import Path

from model.calculo_pension import CalculoPension

CARPETA_SQL = Path(__file__).resolve().parents[2] / "sql"


def _leer_sql(nombre_archivo: str) -> str:
    """Lee un script de la carpeta sql/ del proyecto."""
    return (CARPETA_SQL / nombre_archivo).read_text(encoding="utf-8")

class ErrorHistorial(Exception):
    """Excepción base de los errores del historial."""


class CedulaInvalida(ErrorHistorial):
    """La cédula está vacía o no es numérica."""

    def __init__(self, cedula: str = None):
        super().__init__(
            f"La cédula no es válida (recibido: '{cedula}'). "
            "Solución: ingrese solo dígitos, sin puntos ni espacios."
        )


class NombreInvalido(ErrorHistorial):
    """El nombre está vacío."""

    def __init__(self):
        super().__init__("El nombre no puede estar vacío. Solución: ingréselo.")


class ErrorBaseDeDatos(ErrorHistorial):
    """Falla de la base de datos (tablas inexistentes, conexión, etc.)."""

    def __init__(self, causa: Exception):
        super().__init__(
            f"Error de base de datos: {str(causa).strip()}. Solución: verifique "
            "la conexión y que las tablas estén creadas (opción 'Crear tablas')."
        )


class HistorialPensionController:
    """Casos de uso de persistencia del historial de cálculos."""

    def __init__(self, conexion, calculadora: CalculadoraPensionController = None):
        self.conexion = conexion
        self.calculadora = calculadora or CalculadoraPensionController()

    def _ejecutar(self, sentencia: str, parametros: tuple = None) -> list:
        """Ejecuta una sentencia con commit/rollback y retorna sus filas.

        Si algo falla se hace rollback (psycopg2 deja la transacción
        inutilizable si no) y se lanza ErrorBaseDeDatos.
        """
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(sentencia, parametros)
                filas = cursor.fetchall() if cursor.description else []
            self.conexion.commit()
            return filas
        except psycopg2.Error as error:
            self.conexion.rollback()
            raise ErrorBaseDeDatos(error) from error

    # --- Crear y borrar tablas ------------------------------------------
    def crear_tablas(self) -> None:
        """CREATE TABLE: crea las tablas si no existen."""
        self._ejecutar(_leer_sql("crear_tablas.sql"))

    def borrar_tablas(self) -> None:
        """DROP TABLE: borra las tablas y TODOS sus datos."""
        self._ejecutar(_leer_sql("borrar_tablas.sql"))

    # --- Insertar -------------------------------------------------------
    def calcular_y_guardar(
        self, cedula: str, nombre: str, datos: DatosPension
    ) -> CalculoPension:
        """Calcula la pensión y guarda el cálculo (INSERT INTO).

        Si los datos violan una regla de negocio, ErrorCalculoPension se
        propaga y NO se guarda nada. Si la persona ya existe (misma
        cédula) se reutiliza en vez de duplicarla.
        """
        cedula = self._validar_cedula(cedula)
        nombre = self._validar_nombre(nombre)
        resultado = self.calculadora.calcular(datos)

        try:
            with self.conexion.cursor() as cursor:
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
            self.conexion.commit()
        except psycopg2.Error as error:
            self.conexion.rollback()
            raise ErrorBaseDeDatos(error) from error

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

    # --- Presentación y validación ---------------------------------------
    @staticmethod
    def formatear_calculo(calculo: CalculoPension) -> str:
        """Una línea de texto legible para mostrar un cálculo guardado."""
        return (
            f"#{calculo.id} | {calculo.fecha:%Y-%m-%d %H:%M} | "
            f"{calculo.persona.nombre} (CC {calculo.persona.cedula}) | "
            f"{calculo.semanas_cotizadas} sem, {calculo.edad} años ({calculo.sexo}) | "
            f"IBL ${calculo.ibl:,.2f} | Tasa {calculo.tasa_total:.1f}% | "
            f"Pensión ${calculo.pension:,.2f}"
        )

    @staticmethod
    def _validar_cedula(cedula: str) -> str:
        limpia = (cedula or "").strip()
        if not limpia.isdigit():
            raise CedulaInvalida(cedula=cedula)
        return limpia

    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        limpio = (nombre or "").strip()
        if not limpio:
            raise NombreInvalido()
        return limpio