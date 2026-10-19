"""Opciones de consola para guardar y consultar el historial en la base de datos.

Es una vista: no ejecuta SQL ni calcula nada. Pide los datos, llama al
HistorialPensionController y muestra el resultado. Los errores se dejan
subir: los captura el menú principal (console.py).
La conexión se abre la primera vez que se necesita, para que el programa
funcione aunque la base de datos no esté disponible.
"""

from typing import Optional, Tuple


import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from controller.historial_controller import ErrorHistorial, HistorialPensionController
from model.conexion import ConfiguracionFaltante, ErrorConexion, obtener_conexion
from model.logica_pension import DatosPension

ERRORES_HISTORIAL = (ConfiguracionFaltante, ErrorConexion, ErrorHistorial)

def solicitar_cedula() -> str:
    """Solicita la cédula (solo dígitos); reintenta hasta obtenerla."""
    while True:
        cedula = input("Cédula (solo dígitos): ").strip()
        if cedula.isascii() and cedula.isdigit():
            return cedula
        print("  >> Entrada no válida: ingrese solo dígitos, sin puntos ni espacios.")

def solicitar_nombre() -> str:
    """Solicita el nombre; reintenta si se deja vacío."""
    while True:
        nombre = input("Nombre completo: ").strip()
        if nombre:
            return nombre
        print("  >> El nombre no puede estar vacío. Intente de nuevo.")

def solicitar_persona() -> Tuple[str, str]:
    """Pide la cédula y el nombre de la persona a la que se guarda el cálculo."""
    print("\nDatos de la persona:\n")
    return solicitar_cedula(), solicitar_nombre()

class HistorialConsola:
    """Opciones de consola que usan la base de datos."""

    def __init__(self) -> None:
        self._controlador: Optional[HistorialPensionController] = None

    def _obtener_controlador(self) -> HistorialPensionController:
        """Abre la conexión la primera vez (o si se cerró) y la reutiliza."""
        if self._controlador is None or self._controlador.conexion.closed:
            self._controlador = HistorialPensionController(conexion=obtener_conexion())
        return self._controlador

    def guardar_calculo(self, cedula: str, nombre: str, datos: DatosPension) -> None:
        """Insertar: calcula la pensión y guarda el cálculo en la base de datos."""
        calculo = self._obtener_controlador().calcular_y_guardar(
            cedula=cedula, nombre=nombre, datos=datos
        )
        print("\nCálculo guardado:")
        print(HistorialPensionController.formatear_calculo(calculo))

    def buscar_por_cedula(self) -> None:
        """Buscar: muestra el historial de cálculos de una cédula."""
        cedula = solicitar_cedula()
        calculos = self._obtener_controlador().buscar_por_cedula(cedula=cedula)

        if not calculos:
            print("\nNo hay cálculos guardados para esa cédula.")
            return

        print(f"\nHistorial ({len(calculos)} cálculos):")
        for calculo in calculos:
            print(HistorialPensionController.formatear_calculo(calculo))

    def crear_tablas(self) -> None:
        """Crea las tablas si no existen (necesario la primera vez)."""
        self._obtener_controlador().crear_tablas()
        print("\nTablas persona y calculopension listas.")

    def borrar_tablas(self) -> None:
        """Borra las tablas y todos sus datos, pidiendo confirmación."""
        confirmacion = input("Esto borra TODAS las tablas y sus datos. Escriba 'SI' para continuar: ")
        if confirmacion.strip().upper() != "SI":
            print("\nOperación cancelada.")
            return
        self._obtener_controlador().borrar_tablas()
        print("\nTablas borradas.")