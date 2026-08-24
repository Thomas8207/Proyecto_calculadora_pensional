import logica_pension

def main():
    print("=" * 50)
    print("       CALCULADORA PENSIONAL")
    print("=" * 50)

    try:
        print("\nIngrese los siguientes datos:\n")

        ibc_ultimos_10 = float(input("IBC de los últimos 10 años: "))

        ibc_toda_vida = float(input("IBC de toda la vida laboral: "))

        salario_minimo_legal = int(input("Salario mínimo legal vigente: "))

        semanas = int(input("Semanas cotizadas: "))

        edad = int(input("Edad: "))

        sexo = input("Sexo (M/F): ").upper()

        # Calcular pensión
        pension = logica_pension.calcular_pension(ibc_ultimos_10,ibc_toda_vida,salario_minimo_legal,semanas,edad,sexo)

        # Mostrar resultados
        ingreso_base_liquidacion = logica_pension.calcular_ibl(ibc_ultimos_10,ibc_toda_vida)

        relacion_ibl_smlmv = logica_pension.calcular_relacion_ibl_smlmv(ingreso_base_liquidacion,salario_minimo_legal)

        tasa_reemplazo_base = logica_pension.calcular_r_base_55(relacion_ibl_smlmv)

        semanas_adicionales = logica_pension.semanas_adicionales_test(semanas)

        incremento = logica_pension.incremento_porcentual(semanas_adicionales)

        r_total = logica_pension.calcular_r_total(tasa_reemplazo_base,incremento)

        print("\n" + "=" * 50)
        print("             RESULTADOS")
        print("=" * 50)

        print(f"IBL calculado: ${ingreso_base_liquidacion:,.2f}")
        print(f"Salarios mínimos (S): {relacion_ibl_smlmv:.2f}")
        print(f"Porcentaje base: {tasa_reemplazo_base:.2f}%")
        print(f"Semanas adicionales: {semanas_adicionales}")
        print(f"Incremento: {incremento:.2f}%")
        print(f"Porcentaje total: {r_total:.2f}%")
        print(f"PENSIÓN ESTIMADA: ${pension:,.2f}")
        print("=" * 50)

    except logica_pension.SemanasInsuficientes as e:
        print(f"\nERROR: {e}")

    except logica_pension.IblCero as e:
        print(f"\nERROR: {e}")

    except logica_pension.IblNegativo as e:
        print(f"\nERROR: {e}")

    except logica_pension.SalarioMinimoNoValido as e:
        print(f"\nERROR: {e}")

    except logica_pension.SemanasNegativas as e:
        print(f"\nERROR: {e}")

    except logica_pension.EdadInsuficiente as e:
        print(f"\nERROR: {e}")

    except ValueError:
        print("\nERROR: Debe ingresar valores numéricos válidos.")

if __name__ == "__main__":
    main()