import os
import sys

# Asegurar que la raíz del proyecto esté en el path de Python
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask
from src.view.web.vista_pension import blueprint

# Carpeta templates ubicada en la raíz
template_folder_path = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=template_folder_path)
app.secret_key = "clave_secreta_pension"

app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True, port=5000)