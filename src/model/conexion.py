"""Conexión a PostgreSQL para el historial de cálculos.

Lee los datos de acceso desde ``secret_config.py`` (archivo local que NO
se sube al repositorio; ver ``secret_config_sample.py``) y entrega una
conexión psycopg2 lista para usar.
"""

import importlib
from typing import Dict, Optional

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection

NOMBRES_CONFIGURACION = (
    "DB_NOMBRE",
    "DB_USUARIO",
    "DB_CLAVE",
    "DB_HOST",
    "DB_PUERTO",
    "DB_SSLMODE",
)
SEGUNDOS_MAXIMOS_DE_ESPERA = 10


class ConfiguracionFaltante(Exception):
    """No existe secret_config.py o le faltan datos."""

    def __init__(self, detalle: str):
        super().__init__(
            f"Falta la configuración de la base de datos: {detalle} "
            "Solución: copie src/secret_config_sample.py como "
            "src/secret_config.py y complete sus datos."
        )


class ErrorConexion(Exception):
    """No fue posible conectarse a la base de datos."""

    def __init__(self, causa: Exception):
        super().__init__(
            f"No fue posible conectarse a la base de datos: {str(causa).strip()}. "
            "Solución: verifique los datos de secret_config.py y su "
            "conexión a internet."
        )


def _cargar_configuracion() -> Dict[str, object]:
    """Lee secret_config.py y verifica que defina todos los datos."""
    try:
        configuracion = importlib.import_module("secret_config")
    except ImportError as error:
        raise ConfiguracionFaltante("no se encontró src/secret_config.py.") from error

    faltantes = [n for n in NOMBRES_CONFIGURACION if not hasattr(configuracion, n)]
    if faltantes:
        raise ConfiguracionFaltante(
            f"secret_config.py no define: {', '.join(faltantes)}."
        )
    return {n: getattr(configuracion, n) for n in NOMBRES_CONFIGURACION}


def _usar_esquema(conexion: connection, esquema: str) -> None:
    """Crea el esquema si no existe y hace que la sesión trabaje solo en él.

    Se usa en las pruebas para no tocar las tablas reales.
    """
    with conexion.cursor() as cursor:
        cursor.execute(
            sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(esquema))
        )
        cursor.execute(
            sql.SQL("SET search_path TO {}").format(sql.Identifier(esquema))
        )
    conexion.commit()


def obtener_conexion(esquema: Optional[str] = None) -> connection:
    """Abre una conexión a PostgreSQL con los datos de secret_config.py.

    Si se indica ``esquema``, la conexión trabaja únicamente en ese esquema.
    """
    configuracion = _cargar_configuracion()

    try:
        conexion = psycopg2.connect(
            dbname=configuracion["DB_NOMBRE"],
            user=configuracion["DB_USUARIO"],
            password=configuracion["DB_CLAVE"],
            host=configuracion["DB_HOST"],
            port=configuracion["DB_PUERTO"],
            sslmode=configuracion["DB_SSLMODE"],
            connect_timeout=SEGUNDOS_MAXIMOS_DE_ESPERA,
        )
    except psycopg2.Error as error:
        raise ErrorConexion(error) from error

    if esquema:
        try:
            _usar_esquema(conexion=conexion, esquema=esquema)
        except psycopg2.Error as error:
            conexion.close()
            raise ErrorConexion(error) from error

    return conexion