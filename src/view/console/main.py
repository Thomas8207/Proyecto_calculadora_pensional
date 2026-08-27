import sys

sys.path.append("src")

from model import logica_pension

def solicitar_datos():

    ibc_ultimos_10 = float(input("IBC de los últimos 10 años: "))

    ibc_toda_vida = float(input("IBC de toda la vida laboral: "))

    salario_minimo_legal = int(input("Salario mínimo legal vigente: "))

    semanas_cotizadas = int(input("Semanas cotizadas: "))

    edad = int(input("Edad: "))

    sexo = input("Sexo (M/F): ").upper()

    return logica_pension.DatosPension(
        ibc_ultimos_10=ibc_ultimos_10,
        ibc_toda_vida=ibc_toda_vida,
        salario_minimo_legal=salario_minimo_legal,
        semanas_cotizadas=semanas_cotizadas,
        edad=edad,
        sexo=sexo
    )

def calcular_resultado(datos):
    return logica_pension.calcular_pension(datos)


def mostrar_resultados(resultado):
    print("\n" + "=" * 50)
    print("             RESULTADOS")
    print("=" * 50)

    print(f"IBL calculado: ${resultado['ibl']:,.2f}")
    print(f"Salarios mínimos (S): {resultado['relacion']:.2f}")
    print(f"Porcentaje base: {resultado['tasa_base']:.2f}%")
    print(f"Semanas adicionales: {resultado['semanas_adicionales']}")
    print(f"Incremento: {resultado['incremento']:.2f}%")
    print(f"Porcentaje total: {resultado['tasa_total']:.2f}%")
    print(f"PENSIÓN ESTIMADA: ${resultado['pension']:,.2f}")

    print("=" * 50)


def manejar_error(error):
    print(f"\nERROR: {error}")


def manejar_error_valor():
    print("\nERROR: Debe ingresar valores numéricos válidos.")


def main():
    print("=" * 50)
    print("       CALCULADORA PENSIONAL")
    print("=" * 50)

    try:
        print("\nIngrese los siguientes datos:\n")

        datos = solicitar_datos()
        resultado = calcular_resultado(*datos)
        mostrar_resultados(resultado)

    except (
        logica_pension.SemanasInsuficientes,
        logica_pension.IblCero,
        logica_pension.IblNegativo,
        logica_pension.SalarioMinimoLegalVigenteCero,
        logica_pension.SalarioMinimoNegativo,
        logica_pension.SemanasNegativas,
        logica_pension.EdadInsuficiente
    ) as e:
        manejar_error(e)

    except ValueError:
        manejar_error_valor()


if __name__ == "__main__":
    main()