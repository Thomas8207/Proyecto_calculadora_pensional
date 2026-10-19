"""Interfaz de consola (CLI) de la calculadora pensional.

Uso:
    python src/view/console/console.py

Ofrece un menú para calcular la pensión y, además, guardar cálculos en
la base de datos y consultar el historial por cédula.
"""

import sys
import os
from typing import Callable

# Permite ejecutar el archivo directamente sin configurar Sources Root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

# La vista solo importa el controlador (y los tipos del modelo que
# necesita para anotar variables); nunca calcula nada por sí misma.
from controller.pension_controller import (
    CalculadoraPensionController,
    MENSAJE_ENTRADA_INVALIDA,
)
from model.logica_pension import DatosPension, ErrorCalculoPension, ResultadoPension
from view.console.historial_console import (
    ERRORES_HISTORIAL,
    HistorialConsola,
    solicitar_persona,
)

MENU = """
Seleccione una opción:
  1. Calcular pensión
  2. Calcular y guardar en la base de datos
  3. Buscar historial por cédula
  4. Crear tablas (primera vez)
  5. Borrar tablas
  0. Salir
"""


def solicitar_numero(mensaje: str) -> float:
    """Solicita un número al usuario; reintenta hasta obtenerlo.

    No lanza excepciones hacia arriba: los errores de formato (campo
    vacío o texto no numérico) se resuelven aquí mismo, volviendo a
    pedir el dato, para que el usuario nunca vea un traceback por un
    simple error de tecleo.
    """
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            print("  >> El campo no puede estar vacío. Intente de nuevo.")
            continue
        try:
            return float(entrada)
        except ValueError:
            print("  >> Entrada no válida: ingrese un valor numérico.")


def solicitar_entero(mensaje: str) -> int:
    """Solicita un entero al usuario; reintenta hasta obtenerlo.

    Reutiliza solicitar_numero() y solo agrega la validación de que el
    valor no tenga parte decimal (por ejemplo, rechaza 1300.5 pero
    acepta 1300.0), en vez de truncar el número en silencio.
    """
    while True:
        valor = solicitar_numero(mensaje=mensaje)
        if valor == int(valor):
            return int(valor)
        print("  >> Entrada no válida: ingrese un número entero.")


def solicitar_sexo() -> str:
    """Solicita el sexo (M/F); reintenta hasta obtenerlo."""
    while True:
        sexo = input("Sexo (M/F): ").strip().upper()
        if sexo in ("M", "F"):
            return sexo
        print("  >> Entrada no válida: ingrese 'M' para hombre o 'F' para mujer.")


def solicitar_datos(controlador: CalculadoraPensionController) -> DatosPension:
    """Pide al usuario todos los datos y construye el objeto DatosPension.

    Cada dato se solicita con su propia función de reintento, así que al
    llegar aquí abajo ya se tienen valores con el formato correcto; el
    controlador se encarga de las validaciones de negocio (semanas
    mínimas, edad mínima, etc.), no esta vista.
    """
    print("\nIngrese los siguientes datos:\n")

    ibc_ultimos_10 = solicitar_numero(mensaje="IBC de los últimos 10 años: ")
    ibc_toda_vida = solicitar_numero(mensaje="IBC de toda la vida laboral: ")
    salario_minimo_legal = solicitar_entero(mensaje="Salario mínimo legal vigente: ")
    semanas_cotizadas = solicitar_entero(mensaje="Semanas cotizadas: ")
    edad = solicitar_entero(mensaje="Edad: ")
    sexo = solicitar_sexo()

    return controlador.construir_datos(
        ibc_ultimos_10=ibc_ultimos_10,
        ibc_toda_vida=ibc_toda_vida,
        salario_minimo_legal=salario_minimo_legal,
        semanas_cotizadas=semanas_cotizadas,
        edad=edad,
        sexo=sexo,
    )


def mostrar_resultados(
    controlador: CalculadoraPensionController, resultado: ResultadoPension
) -> None:
    """Imprime en consola las líneas de resultado formateadas.

    El formateo del contenido (qué texto va en cada línea) lo hace el
    controlador; esta función solo se encarga del encabezado y el
    "marco" visual de asteriscos alrededor del resultado.
    """
    print("\n" + "=" * 50)
    print("             RESULTADOS")
    print("=" * 50)
    for linea in controlador.formatear_resultado(resultado=resultado):
        print(linea)
    print("=" * 50)


def calcular_pension(controlador: CalculadoraPensionController) -> None:
    """Opción 1: pide los datos, calcula y muestra el resultado."""
    datos = solicitar_datos(controlador=controlador)
    resultado = controlador.calcular(datos=datos)
    mostrar_resultados(controlador=controlador, resultado=resultado)


def calcular_y_guardar(
    controlador: CalculadoraPensionController, historial: HistorialConsola
) -> None:
    """Opción 2: pide la persona y los datos, y guarda el cálculo."""
    cedula, nombre = solicitar_persona()
    datos = solicitar_datos(controlador=controlador)
    historial.guardar_calculo(cedula=cedula, nombre=nombre, datos=datos)


def ejecutar_accion(
    accion: Callable[[], None], controlador: CalculadoraPensionController
) -> None:
    """Ejecuta una opción del menú y convierte cualquier error en un mensaje.

    Errores de formato, de negocio, de base de datos o inesperados se
    capturan aquí para que el programa siempre muestre un mensaje claro
    en vez de un traceback.
    """
    try:
        accion()
    except ValueError:
        print("\nERROR: " + MENSAJE_ENTRADA_INVALIDA)
    except ErrorCalculoPension as error:
        # Errores de negocio ya conocidos: se traducen a un mensaje amigable.
        print("\nERROR: " + controlador.mensaje_de_error(error))
    except ERRORES_HISTORIAL as error:
        # Cédula/nombre inválidos, falta de configuración o fallas de la base de datos.
        print("\nERROR: " + str(error))
    except Exception as error:
        # Último recurso de resiliencia: cualquier falla no prevista no debe
        # tumbar la consola (requisito de la actividad), pero sí queda
        # reportada de forma clara al usuario.
        print("\nERROR INESPERADO: " + controlador.mensaje_de_error(error))


def main() -> None:
    controlador = CalculadoraPensionController()
    historial = HistorialConsola()

    acciones = {
        "1": lambda: calcular_pension(controlador=controlador),
        "2": lambda: calcular_y_guardar(controlador=controlador, historial=historial),
        "3": historial.buscar_por_cedula,
        "4": historial.crear_tablas,
        "5": historial.borrar_tablas,
    }

    print("=" * 50)
    print("       CALCULADORA PENSIONAL")
    print("=" * 50)

    while True:
        print(MENU)
        opcion = input("Opción: ").strip()

        if opcion == "0":
            print("\nHasta pronto.")
            return

        accion = acciones.get(opcion)
        if accion is None:
            print("  >> Opción no válida: elija un número del menú.")
            continue

        ejecutar_accion(accion=accion, controlador=controlador)


if __name__ == "__main__":
    main()