"""Opciones de consola para guardar y consultar el historial.

Es una vista: no ejecuta SQL, no conoce la conexión a la base de datos y
no calcula nada. Pide los datos, llama al HistorialPensionController y
muestra el resultado con su propio formato. Los errores se dejan subir:
los captura el menú principal (console.py).
"""

import os
import sys
from typing import Optional, Tuple

# Permite ejecutar el archivo directamente sin configurar Sources Root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from controller.historial_controller import ErrorHistorial, HistorialPensionController
from model.calculo_pension import CalculoPension
from model.logica_pension import DatosPension

# Errores del historial (datos inválidos, conexión o base de datos) que
# el menú principal muestra al usuario.
ERRORES_HISTORIAL = (ErrorHistorial,)


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


def formatear_calculo(calculo: CalculoPension) -> str:
    """Una línea de texto legible para mostrar un cálculo guardado."""
    return (
        f"#{calculo.id} | {calculo.fecha:%Y-%m-%d %H:%M} | "
        f"{calculo.persona.nombre} (CC {calculo.persona.cedula}) | "
        f"{calculo.semanas_cotizadas} sem, {calculo.edad} años ({calculo.sexo}) | "
        f"IBL ${calculo.ibl:,.2f} | Tasa {calculo.tasa_total:.1f}% | "
        f"Pensión ${calculo.pension:,.2f}"
    )


class HistorialConsola:
    """Opciones de consola que usan el historial."""

    def __init__(self, controlador: Optional[HistorialPensionController] = None):
        # Crear el controlador no abre la conexión: eso ocurre al primer uso.
        self._controlador = controlador or HistorialPensionController()

    def guardar_calculo(self, cedula: str, nombre: str, datos: DatosPension) -> None:
        """Insertar: calcula la pensión y guarda el cálculo."""
        calculo = self._controlador.calcular_y_guardar(
            cedula=cedula, nombre=nombre, datos=datos
        )
        print("\nCálculo guardado:")
        print(formatear_calculo(calculo))

    def buscar_por_cedula(self) -> None:
        """Buscar: muestra el historial de cálculos de una cédula."""
        cedula = solicitar_cedula()
        calculos = self._controlador.buscar_por_cedula(cedula=cedula)

        if not calculos:
            print("\nNo hay cálculos guardados para esa cédula.")
            return

        print(f"\nHistorial ({len(calculos)} cálculos):")
        for calculo in calculos:
            print(formatear_calculo(calculo))

    def crear_tablas(self) -> None:
        """Crea las tablas si no existen (necesario la primera vez)."""
        self._controlador.crear_tablas()
        print("\nTablas persona y calculopension listas.")

    def borrar_tablas(self) -> None:
        """Borra las tablas y todos sus datos, pidiendo confirmación."""
        confirmacion = input(
            "Esto borra TODAS las tablas y sus datos. Escriba 'SI' para continuar: "
        )
        if confirmacion.strip().upper() != "SI":
            print("\nOperación cancelada.")
            return
        self._controlador.borrar_tablas()
        print("\nTablas borradas.")