from src.model import logica_pension


def main():
    print("=" * 50)
    print("       CALCULADORA PENSIONAL")
    print("=" * 50)

    try:
        print("\nIngrese los siguientes datos:\n")

        ibc_ultimos_10 = float(input("IBC de los últimos 10 años: "))

        ibc_toda_vida = float(input("IBC de toda la vida laboral: "))

        smlmv = float(input("Salario mínimo legal vigente: "))

        semanas = int(input("Semanas cotizadas: "))

        edad = int(input("Edad: "))

        sexo = input("Sexo (M/F): ").upper()

        # Calcular pensión
        pension = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

        # Mostrar resultados
        ibl = logica_pension.calcular_ibl(ibc_ultimos_10, ibc_toda_vida)

<<<<<<<< HEAD:src/view/console/Main.py
        s = logica_pension.calcular_s(ibl, smlmv)
========
        s = logica_pension.calcular_relacion_ibl_smlmv(ibl,smlmv)
>>>>>>>> eafabaa (Arreglado 7 issues del proyecto 1, 2, 4, 6, 7, 8, 9, 14):main.py

        r_base = logica_pension.calcular_r_base_55(s)

        semanas_adi = logica_pension.semanas_adicionales_test(semanas)

        incremento = logica_pension.incremento_porcentual(semanas_adi)

        r_total = logica_pension.calcular_r_total(r_base, incremento)

        print("\n" + "=" * 50)
        print("             RESULTADOS")
        print("=" * 50)

        print(f"IBL calculado: ${ibl:,.2f}")
        print(f"Salarios mínimos (S): {s:.2f}")
        print(f"Porcentaje base: {r_base:.2f}%")
        print(f"Semanas adicionales: {semanas_adi}")
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

    except logica_pension.SalariominimolegalvigenteCero as e:
        print(f"\nERROR: {e}")

    except logica_pension.SemanasNegativas as e:
        print(f"\nERROR: {e}")

    except logica_pension.EdadInsuficiente as e:
        print(f"\nERROR: {e}")

    except ValueError:
        print("\nERROR: Debe ingresar valores numéricos válidos.")

if __name__ == "__main__":
    main()