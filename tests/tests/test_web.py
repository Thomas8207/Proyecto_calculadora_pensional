import pytest
from src.view.web.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_menu_principal_carga_ok(client):
    """Verifica que el menú principal responda HTTP 200."""
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert b"Calculadora Pensional" in respuesta.data

def test_formulario_nuevo_calculo_carga_ok(client):
    """Verifica que el formulario de cálculo responda HTTP 200."""
    respuesta = client.get("/insertar")
    assert respuesta.status_code == 200

def test_formulario_buscar_carga_ok(client):
    """Verifica que la vista de búsqueda responda HTTP 200."""
    respuesta = client.get("/buscar")
    assert respuesta.status_code == 200