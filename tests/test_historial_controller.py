"""Pruebas del controlador del historial (psycopg2 + PostgreSQL).

Estas pruebas solo usan los métodos públicos del controlador: no escriben
SQL, no abren cursores y no conocen la conexión. Necesitan src/secret_config.py
con una base PostgreSQL accesible; si no está disponible, se omiten en vez
de fallar.

Para NO tocar las tablas reales, cada prueba trabaja en un esquema aparte
llamado ``pruebas``: el fixture setUp deja las tablas limpias y tearDown
las borra.
"""

import sys
import unittest

sys.path.append("src")

from controller.historial_controller import (
    CedulaInvalida,
    ErrorBaseDeDatos,
    ErrorConexionHistorial,
    HistorialPensionController,
    NombreInvalido,
)
from model import logica_pension

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
    """Test fixture: controlador con las tablas creadas y vacías."""

    def setUp(self):
        self.controlador = HistorialPensionController.en_esquema(ESQUEMA_PRUEBAS)
        try:
            self.controlador.borrar_tablas()  # limpia restos de una corrida anterior
            self.controlador.crear_tablas()
        except ErrorConexionHistorial as error:
            raise unittest.SkipTest(f"Base de datos no disponible: {error}")

    def tearDown(self):
        self.controlador.borrar_tablas()
        self.controlador.cerrar()


class TestCrearYBorrarTablas(BaseHistorial):

    def test_crear_tablas_normal(self):
        self.assertEqual(self.controlador.listar_todos(), [])

    def test_crear_tablas_dos_veces_no_borra_los_datos(self):
        self.controlador.calcular_y_guardar("123", "Ana", _datos())
        self.controlador.crear_tablas()  # ya existían
        self.assertEqual(len(self.controlador.listar_todos()), 1)

    def test_borrar_tablas_normal(self):
        self.controlador.borrar_tablas()
        with self.assertRaises(ErrorBaseDeDatos):
            self.controlador.listar_todos()

    def test_borrar_tablas_dos_veces_no_falla(self):
        self.controlador.borrar_tablas()
        self.controlador.borrar_tablas()  # DROP ... IF EXISTS


class TestInsertar(BaseHistorial):

    def test_insertar_normal_guarda_pension_calculada(self):
        calculo = self.controlador.calcular_y_guardar("123", "Ana", _datos())
        self.assertIsNotNone(calculo.id)
        self.assertAlmostEqual(calculo.pension, 6_300_000.00, 2)
        self.assertEqual(len(self.controlador.listar_todos()), 1)

    def test_insertar_misma_cedula_no_duplica_persona(self):
        self.controlador.calcular_y_guardar("123", "Ana", _datos())
        self.controlador.calcular_y_guardar("123", "Ana", _datos(edad=66))
        calculos = self.controlador.listar_todos()
        self.assertEqual(len(calculos), 2)
        self.assertEqual(len({calculo.persona.id for calculo in calculos}), 1)

    def test_insertar_limpia_espacios_de_la_cedula(self):
        calculo = self.controlador.calcular_y_guardar(" 123 ", "Ana", _datos())
        self.assertEqual(calculo.persona.cedula, "123")

    def test_error_insertar_cedula_no_numerica(self):
        with self.assertRaises(CedulaInvalida):
            self.controlador.calcular_y_guardar("abc", "Ana", _datos())
        self.assertEqual(self.controlador.listar_todos(), [])

    def test_error_insertar_nombre_vacio(self):
        with self.assertRaises(NombreInvalido):
            self.controlador.calcular_y_guardar("123", "   ", _datos())
        self.assertEqual(self.controlador.listar_todos(), [])

    def test_error_insertar_datos_de_negocio_invalidos_no_guarda(self):
        with self.assertRaises(logica_pension.SemanasInsuficientes):
            self.controlador.calcular_y_guardar(
                "123", "Ana", _datos(semanas_cotizadas=1200)
            )
        self.assertEqual(self.controlador.listar_todos(), [])


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

    def test_buscar_ignora_espacios_de_la_cedula(self):
        self.assertEqual(len(self.controlador.buscar_por_cedula(" 111 ")), 2)

    def test_buscar_cedula_inexistente_devuelve_lista_vacia(self):
        self.assertEqual(self.controlador.buscar_por_cedula("999"), [])

    def test_listar_todos_normal(self):
        self.assertEqual(len(self.controlador.listar_todos()), 3)

    def test_error_buscar_cedula_invalida(self):
        with self.assertRaises(CedulaInvalida):
            self.controlador.buscar_por_cedula("")


if __name__ == "__main__":
    unittest.main()
