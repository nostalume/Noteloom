import unittest
from fractions import Fraction

from coulomb_e3_closure import build_certificate


class CoulombE3ClosureTests(unittest.TestCase):
    def test_generated_centralizer_closes_to_so4_and_satisfies_casimirs(self):
        result = build_certificate()

        self.assertEqual(result["status"], "Passed")
        self.assertEqual(result["generated_module_dimension"], 20)
        self.assertEqual(result["generated_kernel_dimension"], 10)
        self.assertEqual(result["generated_first_order_dimension"], 3)
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(result["energy_shell_output"]["degeneracy"], "n^2")

    def test_coupling_is_symbolic_rational_not_hard_coded(self):
        result = build_certificate(Fraction(3, 2))

        self.assertEqual(result["status"], "Passed")
        self.assertTrue(all(result["checks"].values()))

    def test_nonpositive_coupling_is_refused(self):
        self.assertEqual(build_certificate(Fraction(0))["status"], "Refused")


if __name__ == "__main__":
    unittest.main()
