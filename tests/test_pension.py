import sys
sys.path.append("src")
import unittest
from model import logica_pension


class TestPension(unittest.TestCase):

    def test_normal_1(self):
        ibc_ultimos_10 = 9_800_000
        ibc_toda_vida = 10_000_000
        smlmv = 2_000_000
        semanas = 1300
        edad = 65
        sexo = "M"

        # definir las variables de salida esperadas
        pension_esperada = 6_300_000.00

        # Invocar la funcionalidad que resuelve el problema
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

        # verificamos el resultado
        self.assertAlmostEqual(pension_esperada,pension_calculada,2)

    def test_normal_2(self):
        ibc_ultimos_10 = 1_950_000
        ibc_toda_vida = 2_000_000
        smlmv = 2_000_000
        semanas = 1300
        edad = 60
        sexo = "F"

        # definir las variables de salida esperadas
        pension_esperada = 2_000_000.00

        # Invocar la funcionalidad que resuelve el problema
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

        # verificamos el resultado
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)

    def test_normal_3(self):
        ibc_ultimos_10 = 3_700_000
        ibc_toda_vida = 3_900_000
        smlmv = 2_000_000
        semanas = 1500
        edad = 63
        sexo = "M"

        # definir las variables de salida esperadas
        pension_esperada = 2_750_475.00

        # Invocar la funcionalidad que resuelve el problema
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

        # verificamos el resultado
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)

    def test_normal_4(self):
        ibc_ultimos_10 = 15_200_000
        ibc_toda_vida = 15_600_000
        smlmv = 2_000_000
        semanas = 1800
        edad = 64
        sexo = "M"

        # definir las variables de salida esperadas
        pension_esperada = 11_949_600.00

        # Invocar la funcionalidad que resuelve el problema
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

        # verificamos el resultado
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)

    def test_normal_5(self):
        ibc_ultimos_10 = 2_500_000
        ibc_toda_vida = 2_600_000
        smlmv = 2_000_000
        semanas = 2500
        edad = 65
        sexo = "F"

        # definir las variables de salida esperadas
        pension_esperada = 2_080_000.00

        # Invocar la funcionalidad que resuelve el problema
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

        # verificamos el resultado
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)

    def test_normal_6(self):
        ibc_ultimos_10 = 25_000_000
        ibc_toda_vida = 26_000_000
        smlmv = 2_000_000
        semanas = 1300
        edad = 62
        sexo = "M"

        # definir las variables de salida esperadas
        pension_esperada = 15_340_000.00

        # Invocar la funcionalidad que resuelve el problema
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

        # verificamos el resultado
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)

    def test_semanas_insuficientes(self):
        ibc_ultimos_10 = 4_800_000
        ibc_toda_vida = 5_000_000
        smlmv = 2_000_000
        semanas = 1200
        edad = 65
        sexo = "M"

        with self.assertRaises(logica_pension.SemanasInsuficientes):
            logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

    def test_ibl_0(self):
        ibc_ultimos_10 = 0
        ibc_toda_vida = 0
        smlmv = 2_000_000
        semanas = 1300
        edad = 60
        sexo = "F"

        with self.assertRaises(logica_pension.IblCero):
            logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

    def test_smlmv_0(self):
        ibc_ultimos_10 = 4_800_000
        ibc_toda_vida = 5_000_000
        smlmv = 0
        semanas = 1300
        edad = 62
        sexo = "M"

        with self.assertRaises(logica_pension.SalarioMinimoLegalVigenteCero):
            logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

    def test_semanas_negativas(self):
        ibc_ultimos_10 = 4_800_000
        ibc_toda_vida = 5_000_000
        smlmv = 2_000_000
        semanas = -100
        edad = 65
        sexo = "M"

        with self.assertRaises(logica_pension.SemanasNegativas):
            logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

    def test_ibl_negativo(self):
        ibc_ultimos_10 = -2_900_000
        ibc_toda_vida = -3_000_000
        smlmv = 2_000_000
        semanas = 1300
        edad = 60
        sexo = "F"

        with self.assertRaises(logica_pension.IblNegativo):
            logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

    def test_edad_insuficiente(self):
        ibc_ultimos_10 = 4_800_000
        ibc_toda_vida = 5_000_000
        smlmv = 2_000_000
        semanas = 1300
        edad = 45
        sexo = "F"

        with self.assertRaises(logica_pension.EdadInsuficiente):
            logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)

    # =========================
    # CASOS EXCEPCIONALES
    # =========================

    def test_excepcional_edad_limite_mujer(self):
        ibc_ultimos_10 = 1_950_000
        ibc_toda_vida = 2_000_000
        smlmv = 2_000_000
        semanas = 1300
        edad = 57
        sexo = "F"

        pension_esperada = 2_000_000.00

        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)

    def test_excepcional_edad_limite_hombre(self):
        ibc_ultimos_10 = 1_950_000
        ibc_toda_vida = 2_000_000
        smlmv = 2_000_000
        semanas = 1300
        edad = 62
        sexo = "M"

        pension_esperada = 2_000_000.00

        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)

    def test_excepcional_r_base_bajo_piso_55(self):
        ibc_ultimos_10 = 32_000_000
        ibc_toda_vida = 32_500_000
        smlmv = 2_000_000
        semanas = 1300
        edad = 65
        sexo = "M"

        pension_esperada = 18_646_875.00

        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)

    def test_excepcional_r_total_llega_tope_80(self):
        ibc_ultimos_10 = 1_250_000
        ibc_toda_vida = 1_300_000
        smlmv = 2_000_000
        semanas = 1800
        edad = 60
        sexo = "F"

        pension_esperada = 2_000_000.00

        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)

    def test_excepcional_49_semanas_no_alcanza_incremento(self):
        ibc_ultimos_10 = 1_250_000
        ibc_toda_vida = 1_300_000
        smlmv = 2_000_000
        semanas = 1349
        edad = 63
        sexo = "M"

        pension_esperada = 2_000_000.00

        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)
        self.assertAlmostEqual(pension_esperada, pension_calculada, 2)


if __name__ == "__main__":
    unittest.main()
