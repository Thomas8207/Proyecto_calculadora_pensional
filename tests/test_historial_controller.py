"""Pruebas del controlador del historial (psycopg2 + PostgreSQL).

Necesitan src/secret_config.py con una base PostgreSQL accesible; si no
está disponible, las pruebas se omiten en vez de fallar.

Para NO tocar las tablas reales, cada prueba trabaja en un esquema
temporal llamado ``pruebas``: el fixture setUp lo crea junto con las
tablas, y tearDown lo elimina por completo.
"""

import sys
import unittest

sys.path.append("src")

from controller.historial_controller import (
    CedulaInvalida,
    ErrorBaseDeDatos,
    HistorialPensionController,
    NombreInvalido,
)
from model import logica_pension
from model.conexion import ConfiguracionFaltante, ErrorConexion, obtener_conexion

ESQUEMA_PRUEBAS = "pruebas"


def _datos(**cambios) -> logica_pension.DatosPension:
    base = dict(
        ibc_ultimos_10=9_800_000,
        ibc_toda_vida=10_000_000,
        salario_minimo_legal=2_000_000,
        semanas_cotizadas=1300,
        edad=65,
        sexo="M",
    )
    base.update(cambios)
    return logica_pension.DatosPension(**base)


class BaseHistorial(unittest.TestCase):
    """Test fixture: esquema temporal con las tablas creadas."""

    def setUp(self):
        try:
            self.conexion = obtener_conexion(esquema=ESQUEMA_PRUEBAS)
        except (ConfiguracionFaltante, ErrorConexion) as error:
            raise unittest.SkipTest(f"Base de datos no disponible: {error}")
        self.controlador = HistorialPensionController(self.conexion)
        self.controlador.crear_tablas()

    def tearDown(self):
        self.conexion.rollback()
        with self.conexion.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA IF EXISTS {ESQUEMA_PRUEBAS} CASCADE")
        self.conexion.commit()
        self.conexion.close()

    def _tablas(self) -> set:
        with self.conexion.cursor() as cursor:
            cursor.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = %s",
                (ESQUEMA_PRUEBAS,),
            )
            return {fila[0] for fila in cursor.fetchall()}

    def _contar(self, tabla: str) -> int:
        with self.conexion.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            return cursor.fetchone()[0]


class TestCrearYBorrarTablas(BaseHistorial):

    def test_crear_tablas_normal(self):
        self.assertEqual(self._tablas(), {"persona", "calculopension"})

    def test_crear_tablas_dos_veces_no_falla(self):
        self.controlador.crear_tablas()  # ya existían
        self.assertEqual(self._tablas(), {"persona", "calculopension"})

    def test_borrar_tablas_normal(self):
        self.controlador.borrar_tablas()
        self.assertEqual(self._tablas(), set())

    def test_error_consultar_sin_tablas(self):
        self.controlador.borrar_tablas()
        with self.assertRaises(ErrorBaseDeDatos):
            self.controlador.listar_todos()


class TestInsertar(BaseHistorial):

    def test_insertar_normal_guarda_pension_calculada(self):
        calculo = self.controlador.calcular_y_guardar("123", "Ana", _datos())
        self.assertIsNotNone(calculo.id)
        self.assertAlmostEqual(calculo.pension, 6_300_000.00, 2)
        self.assertEqual(self._contar("calculopension"), 1)

    def test_insertar_misma_cedula_no_duplica_persona(self):
        self.controlador.calcular_y_guardar("123", "Ana", _datos())
        self.controlador.calcular_y_guardar("123", "Ana", _datos(edad=66))
        self.assertEqual(self._contar("persona"), 1)
        self.assertEqual(self._contar("calculopension"), 2)

    def test_insertar_limpia_espacios_de_la_cedula(self):
        calculo = self.controlador.calcular_y_guardar(" 123 ", "Ana", _datos())
        self.assertEqual(calculo.persona.cedula, "123")

    def test_error_insertar_cedula_no_numerica(self):
        with self.assertRaises(CedulaInvalida):
            self.controlador.calcular_y_guardar("abc", "Ana", _datos())
        self.assertEqual(self._contar("calculopension"), 0)

    def test_error_insertar_nombre_vacio(self):
        with self.assertRaises(NombreInvalido):
            self.controlador.calcular_y_guardar("123", "   ", _datos())

    def test_error_insertar_datos_de_negocio_invalidos_no_guarda(self):
        with self.assertRaises(logica_pension.SemanasInsuficientes):
            self.controlador.calcular_y_guardar(
                "123", "Ana", _datos(semanas_cotizadas=1200)
            )
        self.assertEqual(self._contar("persona"), 0)
        self.assertEqual(self._contar("calculopension"), 0)


class TestBuscar(BaseHistorial):

    def setUp(self):
        super().setUp()
        self.controlador.calcular_y_guardar("111", "Ana", _datos())
        self.controlador.calcular_y_guardar("111", "Ana", _datos(edad=66))
        self.controlador.calcular_y_guardar("222", "Luis", _datos(sexo="M"))

    def test_buscar_por_cedula_normal(self):
        calculos = self.controlador.buscar_por_cedula("111")
        self.assertEqual(len(calculos), 2)
        self.assertTrue(all(c.persona.nombre == "Ana" for c in calculos))

    def test_buscar_devuelve_el_mas_reciente_primero(self):
        calculos = self.controlador.buscar_por_cedula("111")
        self.assertEqual(calculos[0].edad, 66)

    def test_buscar_cedula_inexistente_devuelve_lista_vacia(self):
        self.assertEqual(self.controlador.buscar_por_cedula("999"), [])

    def test_listar_todos_normal(self):
        self.assertEqual(len(self.controlador.listar_todos()), 3)

    def test_error_buscar_cedula_invalida(self):
        with self.assertRaises(CedulaInvalida):
            self.controlador.buscar_por_cedula("")

    def test_formatear_calculo_contiene_nombre_y_pension(self):
        texto = self.controlador.formatear_calculo(
            self.controlador.buscar_por_cedula("222")[0]
        )
        self.assertIn("Luis", texto)
        self.assertIn("Pensión", texto)


if __name__ == "__main__":
    unittest.main()