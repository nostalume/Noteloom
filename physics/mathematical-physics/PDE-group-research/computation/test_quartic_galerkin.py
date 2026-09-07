import unittest
from fractions import Fraction

from cyclic_reduce import reduce_symmetric_matrix
from quartic_galerkin import build_even_quartic_galerkin


class QuarticGalerkinTests(unittest.TestCase):
    def test_x_fourth_action_is_generated_in_the_hermite_parity_carrier(self):
        matrix, metric = build_even_quartic_galerkin(3, Fraction(1, 10))

        self.assertEqual(matrix[0][0], Fraction(43, 40))
        self.assertEqual(matrix[1][0], Fraction(3, 40))
        self.assertEqual(matrix[2][0], Fraction(1, 160))
        self.assertEqual(metric[0][0], Fraction(1))
        self.assertEqual(metric[1][1], Fraction(8))
        self.assertEqual(metric[2][2], Fraction(384))

    def test_quartic_ground_preparation_reaches_the_full_even_block(self):
        matrix, metric = build_even_quartic_galerkin(6, Fraction(1, 10))
        result = reduce_symmetric_matrix(matrix, [1, 0, 0, 0, 0, 0], metric=metric)

        self.assertEqual(result.status, "ExactCyclicReduction")
        self.assertEqual(result.carrier_dimension, 6)
        self.assertTrue(result.no_dimension_gain)

    def test_zero_coupling_recovers_the_harmonic_ground_eigenspace(self):
        matrix, metric = build_even_quartic_galerkin(6, Fraction(0))
        result = reduce_symmetric_matrix(matrix, [1, 0, 0, 0, 0, 0], metric=metric)

        self.assertEqual(result.carrier_dimension, 1)
        self.assertEqual(result.minimal_polynomial, (Fraction(-1), Fraction(1)))

    def test_early_quartic_stop_is_truncation_not_invisibility(self):
        matrix, metric = build_even_quartic_galerkin(6, Fraction(1, 10))
        result = reduce_symmetric_matrix(
            matrix,
            [1, 0, 0, 0, 0, 0],
            metric=metric,
            budget=2,
        )

        self.assertEqual(result.status, "FormalTruncation")
        self.assertEqual(result.dimension_verdict, "budget_truncation_not_invisibility")


if __name__ == "__main__":
    unittest.main()
