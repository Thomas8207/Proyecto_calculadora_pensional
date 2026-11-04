import os
from flask import Blueprint, render_template, request

from src.controller.pension_controller import CalculadoraPensionController
from src.controller.historial_controller import HistorialPensionController

blueprint = Blueprint('pension', __name__)

controlador_pension = CalculadoraPensionController()
controlador_historial = HistorialPensionController()


@blueprint.route('/')
def index():
    """Menú principal."""
    return render_template('menu_principal_calculadora.html')


@blueprint.route('/crear_tablas', methods=['GET', 'POST'])
def crear_tablas():
    """Inicializa las tablas en la base de datos."""
    try:
        controlador_historial.crear_tablas()
        mensaje = "Tablas creadas con éxito en la base de datos."
    except Exception as e:
        mensaje = f"Error al crear las tablas: {str(e)}"

    return render_template('menu_principal_calculadora.html', mensaje=mensaje)


@blueprint.route('/insertar', methods=['GET', 'POST'])
def insertar():
    """Calcula la pensión y guarda el registro."""
    if request.method == 'POST':
        try:
            cedula = request.form['cedula'].strip()
            nombre = request.form['nombre'].strip()
            edad = int(request.form['edad'])
            semanas = int(request.form['semanas'])
            salario = float(request.form['salario'])
            genero = request.form['genero'].strip()

            # Llama al método real de HistorialPensionController
            resultado = controlador_historial.calcular_y_guardar(
                cedula=cedula,
                nombre=nombre,
                edad=edad,
                semanas=semanas,
                salario=salario,
                genero=genero
            )
            return render_template('resultados_pension.html', resultado=resultado)
        except ValueError as e:
            return render_template('formulario_nuevo_calculo.html', error=f"Datos numéricos inválidos: {str(e)}")
        except Exception as e:
            return render_template('formulario_nuevo_calculo.html', error=f"Error en el proceso: {str(e)}")

    return render_template('formulario_nuevo_calculo.html')


@blueprint.route('/buscar', methods=['GET', 'POST'])
def buscar():
    """Busca el historial de cálculos por cédula."""
    if request.method == 'POST':
        try:
            cedula = request.form['cedula'].strip()
            registros = controlador_historial.buscar_por_cedula(cedula)
            return render_template('resultados_pension.html', registros=registros, cedula_buscada=cedula)
        except Exception as e:
            return render_template('formulario_buscar_historial.html', error=f"Error en la búsqueda: {str(e)}")

    return render_template('formulario_buscar_historial.html')