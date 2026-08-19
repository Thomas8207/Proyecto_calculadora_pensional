class  SemanasInsuficientes(Exception):
    pass

class IblCero(Exception):
    pass

class SalariominimolegalvigenteCero(Exception):
    pass

class SemanasNegativas(Exception):
    pass

class IblNegativo(Exception):
    pass

class EdadInsuficiente(Exception):
    pass


def calcular_ibl(ibc_ultimos_10, ibc_toda_vida):
    ibl = max(ibc_ultimos_10, ibc_toda_vida)
    return ibl

def calcular_s(ibl, smlmv):
    s = ibl / smlmv
    return s

def calcular_r_base_55(s):
    r_base = max(65.5 - s * 0.5, 55)
    return r_base


def semanas_adicionales(semanas_cotizadas):
    sema_adi = max(semanas_cotizadas - 1300, 0)
    return sema_adi


def incremento_porcentual(sema_adi):
    incremento = int(sema_adi / 50) * 1.5
    return incremento


def calcular_r_total(r_base, incremento):
    r_total = min(r_base + incremento, 80)
    return r_total


def cumple_requisitos(semanas_cotizadas, edad, sexo):
    return (semanas_cotizadas >= 1300 and((sexo == "F" and edad >= 57) or
            (sexo == "M" and edad >= 62)))


def calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas_cotizadas, edad, sexo):

    ibl = calcular_ibl(ibc_ultimos_10, ibc_toda_vida)

    if semanas_cotizadas < 0:
        raise SemanasNegativas("Las semanas cotizadas no pueden ser negativas")

    if ibl < 0:
        raise IblNegativo("El ibl no puede ser negativo")

    if ibl == 0:
        raise IblCero("El ibl no puede ser cero")

    if smlmv == 0:
        raise SalariominimolegalvigenteCero("El salario minimo mensual legal vigente no puede ser 0")

    if semanas_cotizadas < 1300 :
        raise SemanasInsuficientes("semanas_cotizadas menores a las minimas necesarias")

    if sexo == "F" and edad < 57 or sexo == "M" and edad <62:
        raise EdadInsuficiente("La edad que tiene es menor a la requerida para acceder a pension")

    s = calcular_s(ibl, smlmv)
    r_base = calcular_r_base_55(s)
    sema_adi = semanas_adicionales(semanas_cotizadas)
    incremento = incremento_porcentual(sema_adi)
    r_total = calcular_r_total(r_base, incremento)


    if cumple_requisitos(semanas_cotizadas, edad, sexo):
        pension = round(max(ibl * r_total / 100, smlmv), 2)
        return pension
    else:
        return ""