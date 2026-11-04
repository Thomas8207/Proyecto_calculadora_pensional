from flask import Blueprint, render_template, request

from src.controller.historial_controller import HistorialPensionController
from src.controller.pension_controller import CalculadoraPensionController
# Si tu archivo se llama diferente, ajusta la ruta del import de DatosPension
try:
    from src.model.logica_pension import DatosPension
except ImportError:
    try:
        from src.model.calculo_pension import DatosPension
    except ImportError:
        from logica_pension import DatosPension

blueprint = Blueprint('pension', __name__)

controlador_pension = CalculadoraPensionController()
controlador_historial = HistorialPensionController()


@blueprint.route('/')
def index():
    """Menú principal unificado con búsqueda e inserción."""
    return render_template('menu_principal_calculadora.html')


@blueprint.route('/crear_tablas', methods=['GET', 'POST'])
def crear_tablas():
    """Inicializa las tablas en la base de datos PostgreSQL."""
    try:
        controlador_historial.crear_tablas()
        mensaje = "Tablas creadas con éxito en la base de datos."
    except Exception as e:
        mensaje = f"Error al crear las tablas: {str(e)}"

    return render_template('menu_principal_calculadora.html', mensaje=mensaje)


@blueprint.route('/insertar', methods=['GET', 'POST'])
def insertar():
    """Calcula la pensión y almacena el registro en la base de datos."""
    if request.method == 'POST':
        try:
            cedula = request.form['cedula'].strip()
            nombre = request.form['nombre'].strip()
            edad = int(request.form['edad'])
            sexo = request.form['sexo'].strip()
            semanas_cotizadas = int(request.form['semanas_cotizadas'])
            ibc_ultimos_10 = float(request.form['ibc_ultimos_10'])
            ibc_toda_vida = float(request.form['ibc_toda_vida'])
            salario_minimo_legal = float(request.form['salario_minimo_legal'])

            datos = DatosPension(
                ibc_ultimos_10=ibc_ultimos_10,
                ibc_toda_vida=ibc_toda_vida,
                salario_minimo_legal=salario_minimo_legal,
                semanas_cotizadas=semanas_cotizadas,
                edad=edad,
                sexo=sexo,
            )

            resultado = controlador_historial.calcular_y_guardar(
                cedula=cedula,
                nombre=nombre,
                datos=datos,
            )
            return render_template('resultados_pension.html', resultado=resultado)
        except Exception as e:
            return render_template(
                'menu_principal_calculadora.html',
                error=f"Error al calcular: {str(e)}",
            )

    return render_template('menu_principal_calculadora.html')


@blueprint.route('/buscar', methods=['GET', 'POST'])
def buscar():
    """Busca el historial de cálculos guardados por cédula."""
    if request.method == 'POST':
        try:
            cedula = request.form['cedula'].strip()
            registros = controlador_historial.buscar_por_cedula(cedula)
            return render_template(
                'resultados_pension.html',
                registros=registros,
                cedula_buscada=cedula,
            )
        except Exception as e:
            return render_template(
                'menu_principal_calculadora.html',
                error=f"Error en la búsqueda: {str(e)}",
            )

    return render_template('menu_principal_calculadora.html')