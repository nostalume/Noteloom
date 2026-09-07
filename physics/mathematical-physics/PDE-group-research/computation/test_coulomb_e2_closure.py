import unittest
from fractions import Fraction

from coulomb_e2_closure import build_certificate


class CoulombE2ClosureTests(unittest.TestCase):
    def test_generated_operators_close_and_satisfy_quantum_casimir(self):
        result = build_certificate()

        self.assertEqual(result["status"], "Passed")
        self.assertEqual(result["generated_kernel_dimension"], 4)
        self.assertEqual(result["generated_first_order_dimension"], 1)
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(result["energy_shell_output"]["negative_energy_real_form"], "so(3)")

    def test_coupling_is_not_hard_coded_to_one(self):
        result = build_certificate(Fraction(3, 2))

        self.assertEqual(result["status"], "Passed")
        self.assertTrue(all(result["checks"].values()))

    def test_nonpositive_coupling_is_refused(self):
        self.assertEqual(build_certificate(Fraction(0))["status"], "Refused")


if __name__ == "__main__":
    unittest.main()
