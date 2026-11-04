from flask import Blueprint, render_template, request, url_for
from controller.pension_controller import PensionController
from controller.historial_controller import HistorialController

# Definición del Blueprint con el nombre 'blueprint' como lo usa tu profesor
blueprint = Blueprint('pension', __name__)

controlador_pension = PensionController()
controlador_historial = HistorialController()

# Ruta para el menú principal
@blueprint.route('/')
def index():
    return render_template('menu_principal_calculadora.html')

# Ruta para crear las tablas en la BD vacía
@blueprint.route('/crear_tablas')
def crear_tablas():
    controlador_historial.crear_tablas()
    return render_template('menu_principal_calculadora.html', mensaje="Tablas creadas con éxito.")

# Ruta para calcular e insertar la pensión
@blueprint.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        edad = int(request.form['edad'])
        semanas = int(request.form['semanas'])
        salario = float(request.form['salario'])
        genero = request.form['genero']
        
        # Llama a tu método existente de pension_controller
        resultado = controlador_pension.calcular_y_guardar(cedula, nombre, edad, semanas, salario, genero)
        return render_template('pantalla_resultados_pension.html', resultado=resultado)
    
    return render_template('formulario_nuevo_calculo.html')

# Ruta para buscar el historial por cédula
@blueprint.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        cedula = request.form['cedula']
        
        # Llama a tu método existente de historial_controller
        registros = controlador_historial.buscar_por_cedula(cedula)
        return render_template('pantalla_resultados_pension.html', registros=registros)
    
    return render_template('formulario_buscar_historial.html')