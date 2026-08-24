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

class SalarioMinimoNoValido(Exception):
    pass

class SemanasNegativas(Exception):
    pass

class IblNegativo(Exception):
    pass

class EdadInsuficiente(Exception):
    pass


def calcular_ibl(ibc_ultimos_10: float, ibc_toda_vida: float) -> float:
    ibl = max(ibc_ultimos_10, ibc_toda_vida)
    return ibl

def calcular_relacion_ibl_smlmv(ingreso_base_liquidacion: float, salario_minimo_legal: int) -> float:
    relacion_ibl_smlmv = ingreso_base_liquidacion / salario_minimo_legal
    return relacion_ibl_smlmv

def calcular_r_base_55(relacion_ibl_smlmv: float) -> float:
    r_base = max(TASA_REEMPLAZO_INICIAL - relacion_ibl_smlmv * FACTOR_REDUCCION_POR_SALARIO, TASA_REEMPLAZO_MINIMA)
    return r_base


def semanas_adicionales_test(semanas_cotizadas: int) -> int:
    semanas_adicionales = max(semanas_cotizadas - SEMANAS_MINIMAS, 0)
    return semanas_adicionales


def incremento_porcentual(semanas_adicionales : int) -> float:
    incremento = int(semanas_adicionales / SEMANAS_POR_INCREMENTO) * INCREMENTO_PORCENTUAL
    return incremento


def calcular_r_total(r_base: float, incremento: float) -> float:
    r_total = min(r_base + incremento, TASA_REEMPLAZO_MAXIMA)
    return r_total


def cumple_requisitos(semanas_cotizadas: int, edad: int, sexo: str) -> bool:
    return (semanas_cotizadas >= SEMANAS_MINIMAS and((sexo == "F" and edad >= EDAD_MINIMA_MUJER) or
            (sexo == "M" and edad >= EDAD_MINIMA_HOMBRE)))


def calcular_pension(ibc_ultimos_10: float, ibc_toda_vida: float, smlmv: float, semanas_cotizadas: int, edad: int, sexo: str) -> float:

    ibl = calcular_ibl(ibc_ultimos_10, ibc_toda_vida)

    if semanas_cotizadas < SEMANAS_MINIMAS:
        raise SemanasNegativas("Las semanas cotizadas no pueden ser negativas")

    if ibl < 0:
        raise IblNegativo("El ibl no puede ser negativo")

    if ibl == 0:
        raise IblCero("El ibl no puede ser cero")

    if smlmv == 0:
        raise SalarioMinimoNoValido("El salario minimo mensual legal vigente no puede ser 0")

    if semanas_cotizadas < SEMANAS_MINIMAS :
        raise SemanasInsuficientes("semanas_cotizadas menores a las minimas necesarias")

    if (
        (sexo == "F" and edad < EDAD_MINIMA_MUJER)
        or
        (sexo == "M" and edad < EDAD_MINIMA_HOMBRE)):
        raise EdadInsuficiente("La edad que tiene es menor a la requerida para acceder a pension")

    relacion_ibl_smlmv = calcular_relacion_ibl_smlmv(ibl, smlmv)
    r_base = calcular_r_base_55(relacion_ibl_smlmv)
    semanas_adicionales = semanas_adicionales_test(semanas_cotizadas)
    incremento = incremento_porcentual(semanas_adicionales)
    r_total = calcular_r_total(r_base, incremento)


    if cumple_requisitos(semanas_cotizadas, edad, sexo):
        pension = round(max(ibl * r_total / 100, smlmv), 2)
        return pension
    else:
        raise EdadInsuficiente()