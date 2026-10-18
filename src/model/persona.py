"""Clase de Model de la tabla persona."""

from dataclasses import dataclass


@dataclass
class Persona:
    """Una fila de la tabla persona."""

    id: int
    cedula: str
    nombre: str