"""Clase de Model de la tabla calculopension."""

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, Tuple

from model.persona import Persona


@dataclass
class CalculoPension:
    """Una fila de calculopension junto con su persona."""

    id: int
    persona: Persona
    ibc_ultimos_10: float
    ibc_toda_vida: float
    salario_minimo_legal: int
    semanas_cotizadas: int
    edad: int
    sexo: str
    ibl: float
    tasa_total: float
    pension: float
    fecha: datetime

    # El orden de columnas debe coincidir con desde_fila().
    # El controller agrega después el WHERE / ORDER BY.
    SQL_SELECT: ClassVar[str] = """
        SELECT c.id, p.id, p.cedula, p.nombre,
               c.ibc_ultimos_10, c.ibc_toda_vida, c.salario_minimo_legal,
               c.semanas_cotizadas, c.edad, c.sexo,
               c.ibl, c.tasa_total, c.pension, c.fecha
        FROM calculopension c
        JOIN persona p ON p.id = c.persona_id
    """

    @classmethod
    def desde_fila(cls, fila: Tuple) -> "CalculoPension":
        """Construye un CalculoPension a partir de una fila de SQL_SELECT."""
        (
            calculo_id, persona_id, cedula, nombre,
            ibc_ultimos_10, ibc_toda_vida, salario_minimo_legal,
            semanas_cotizadas, edad, sexo,
            ibl, tasa_total, pension, fecha,
        ) = fila

        return cls(
            id=calculo_id,
            persona=Persona(id=persona_id, cedula=cedula, nombre=nombre),
            ibc_ultimos_10=ibc_ultimos_10,
            ibc_toda_vida=ibc_toda_vida,
            salario_minimo_legal=salario_minimo_legal,
            semanas_cotizadas=semanas_cotizadas,
            edad=edad,
            sexo=sexo,
            ibl=ibl,
            tasa_total=tasa_total,
            pension=pension,
            fecha=fecha,
        )