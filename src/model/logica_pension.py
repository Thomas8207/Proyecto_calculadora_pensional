SEMANAS_MINIMAS = 1300
SEMANAS_POR_INCREMENTO = 50
INCREMENTO_PORCENTUAL = 1.5

TASA_REEMPLAZO_INICIAL = 65.5
FACTOR_REDUCCION_POR_SALARIO = 0.5
TASA_REEMPLAZO_MINIMA = 55
TASA_REEMPLAZO_MAXIMA = 80

EDAD_MINIMA_MUJER = 57
EDAD_MINIMA_HOMBRE = 62
class  SemanasInsuficientes(Exception):
    pass

class IblCero(Exception):
    pass

class SalarioMinimoLegalVigenteCero(Exception):
    pass

class SemanasNegativas(Exception):
    pass

class IblNegativo(Exception):
    pass

class EdadInsuficiente(Exception):
    pass


def calcular_ibl(ibc_ultimos_10: float, ibc_toda_vida: float) -> float:
    ingreso_base_liquidacion = max(ibc_ultimos_10, ibc_toda_vida)
    return ingreso_base_liquidacion

def calcular_relacion_ibl_smlmv(ingreso_base_liquidacion: float, salario_minimo_legal: int) -> float:
    relacion_ibl_smlmv = ingreso_base_liquidacion / salario_minimo_legal
    return relacion_ibl_smlmv

def calcular_r_base_55(relacion_ibl_smlmv: float) -> float:
    tasa_reemplazo_base = max(TASA_REEMPLAZO_INICIAL - relacion_ibl_smlmv * FACTOR_REDUCCION_POR_SALARIO, TASA_REEMPLAZO_MINIMA)
    return tasa_reemplazo_base


def semanas_adicionales_test(semanas_cotizadas: int) -> int:
    semanas_adicionales = max(semanas_cotizadas - SEMANAS_MINIMAS, 0)
    return semanas_adicionales


def incremento_porcentual(semanas_adicionales : int) -> float:
    incremento = int(semanas_adicionales / SEMANAS_POR_INCREMENTO) * INCREMENTO_PORCENTUAL
    return incremento


def calcular_r_total(tasa_reemplazo_base: float, incremento: float) -> float:
    tasa_reemplazo_total = min(tasa_reemplazo_base + incremento, TASA_REEMPLAZO_MAXIMA)
    return tasa_reemplazo_total


def cumple_requisitos(semanas_cotizadas: int, edad: int, sexo: str) -> bool:
    return (semanas_cotizadas >= SEMANAS_MINIMAS and((sexo == "F" and edad >= EDAD_MINIMA_MUJER) or
            (sexo == "M" and edad >= EDAD_MINIMA_HOMBRE)))

def validar_datos(ingreso_base_liquidacion: float,salario_minimo_legal: int,semanas_cotizadas: int,edad: int,sexo: str) -> None:
    if semanas_cotizadas < 0:
        raise SemanasNegativas("Las semanas cotizadas no pueden ser negativas")

    if ingreso_base_liquidacion < 0:
        raise IblNegativo("El ibl no puede ser negativo")

    if ingreso_base_liquidacion == 0:
        raise IblCero("El ibl no puede ser cero")

    if salario_minimo_legal == 0:
        raise SalarioMinimoLegalVigenteCero("El salario minimo mensual legal vigente no puede ser 0")

    if semanas_cotizadas < SEMANAS_MINIMAS:
        raise SemanasInsuficientes("semanas_cotizadas menores a las minimas necesarias")

    if (sexo == "F" and edad < EDAD_MINIMA_MUJER)or(sexo == "M" and edad < EDAD_MINIMA_HOMBRE):
        raise EdadInsuficiente("La edad que tiene es menor a la requerida para acceder a pension")

def calcular_pension(ibc_ultimos_10: float,ibc_toda_vida: float,salario_minimo_legal: int,semanas_cotizadas: int,edad: int,sexo: str) -> float:

    ingreso_base_liquidacion = calcular_ibl(ibc_ultimos_10,ibc_toda_vida)

    validar_datos(ingreso_base_liquidacion,salario_minimo_legal,semanas_cotizadas,edad,sexo)

    relacion_ibl_smlmv = calcular_relacion_ibl_smlmv(ingreso_base_liquidacion,salario_minimo_legal)

    tasa_reemplazo_base = calcular_r_base_55(relacion_ibl_smlmv)

    semanas_adicionales = semanas_adicionales_test(semanas_cotizadas)

    incremento = incremento_porcentual(semanas_adicionales)

    tasa_reemplazo_total = calcular_r_total(tasa_reemplazo_base,incremento)

    pension = round( max(ingreso_base_liquidacion * tasa_reemplazo_total / 100,salario_minimo_legal), 2)
    return pension