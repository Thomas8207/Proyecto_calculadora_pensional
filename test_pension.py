import unittest
import logica_pension



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
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10,ibc_toda_vida,smlmv,semanas,edad,sexo)

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
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10,ibc_toda_vida,smlmv,semanas,edad,sexo)

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
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10,ibc_toda_vida,smlmv,semanas,edad,sexo)

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
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10,ibc_toda_vida,smlmv,semanas,edad,sexo)

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
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10,ibc_toda_vida,smlmv,semanas,edad,sexo)

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
        pension_calculada = logica_pension.calcular_pension(ibc_ultimos_10,ibc_toda_vida,smlmv,semanas,edad,sexo)

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

        with self.assertRaises(logica_pension.SalariominimolegalvigenteCero):
            logica_pension.calcular_pension(ibc_ultimos_10, ibc_toda_vida, smlmv, semanas, edad, sexo)