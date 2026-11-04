import sys
import os
from flask import Flask

# 1. Calculamos la ruta raíz (dos carpetas hacia atrás desde view/web/)
directorio_actual = os.path.dirname(os.path.abspath(__file__))
raiz_proyecto = os.path.abspath(os.path.join(directorio_actual, "..", ".."))

# 2. Agregamos la raíz y src al path del sistema para que Python encuentre tus módulos
sys.path.append(raiz_proyecto)
sys.path.append(os.path.join(raiz_proyecto, "src"))

# Importamos el blueprint
from view.web import vista_pension

# 3. Le indicamos explícitamente a Flask dónde está la carpeta templates
ruta_templates = os.path.join(raiz_proyecto, "templates")
app = Flask(__name__, template_folder=ruta_templates)

# Registramos el blueprint
app.register_blueprint(vista_pension.blueprint)

if __name__ == '__main__':
    app.run(debug=True)