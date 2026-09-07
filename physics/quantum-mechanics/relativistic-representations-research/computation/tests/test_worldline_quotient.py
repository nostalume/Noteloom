import unittest
from math import comb

from sympy import expand, symbols

from fieldcalc.worldline import (
    compile_open_line_quotient,
    evaluate_matching_kernel,
)


class OpenLineQuotientTests(unittest.TestCase):
    def test_cells_recover_ordered_cubic_and_contact_histories(self):
        expected = {
            2: (2, 3),
            3: (4, 12),
            4: (10, 66),
            5: (26, 450),
            6: (76, 3690),
        }

        for photon_count, totals in expected.items():
            quotient = compile_open_line_quotient(photon_count)
            self.assertEqual(
                (quotient.master_monomials, quotient.ordered_histories), totals
            )
            self.assertEqual(
                quotient.ordered_histories,
                sum(cell.ordered_histories for cell in quotient.cells),
            )

    def test_counts_obey_matching_and_ordered_event_recursions(self):
        quotients = [compile_open_line_quotient(n) for n in range(9)]

        for n in range(2, len(quotients)):
            self.assertEqual(
                quotients[n].master_monomials,
                quotients[n - 1].master_monomials
                + (n - 1) * quotients[n - 2].master_monomials,
            )
            self.assertEqual(
                quotients[n].ordered_histories,
                n * quotients[n - 1].ordered_histories
                + comb(n, 2) * quotients[n - 2].ordered_histories,
            )

    def test_four_photon_cells_recover_each_contact_sector(self):
        quotient = compile_open_line_quotient(4)

        self.assertEqual(
            tuple(
                (
                    cell.pair_count,
                    cell.master_monomials,
                    cell.ordering_chambers,
                    cell.ordered_histories,
                )
                for cell in quotient.cells
            ),
            (
                (0, 1, 24, 24),
                (1, 6, 6, 36),
                (2, 3, 2, 6),
            ),
        )

    def test_matching_kernel_generates_the_three_photon_polynomial(self):
        j0, j1, j2, k01, k02, k12 = symbols("j0 j1 j2 k01 k02 k12")
        evaluation = evaluate_matching_kernel(
            (j0, j1, j2),
            (
                (0, k01, k02),
                (k01, 0, k12),
                (k02, k12, 0),
            ),
            state_budget=8,
        )

        self.assertTrue(evaluation.accepted)
        expected = j0 * j1 * j2 + k01 * j2 + k02 * j1 + k12 * j0
        self.assertEqual(expand(evaluation.value - expected), 0)

    def test_unit_weights_count_master_monomials(self):
        for n in range(7):
            evaluation = evaluate_matching_kernel(
                (1,) * n,
                tuple(tuple(0 if i == j else 1 for j in range(n)) for i in range(n)),
                state_budget=2**n,
            )
            self.assertTrue(evaluation.accepted)
            self.assertEqual(
                evaluation.value, compile_open_line_quotient(n).master_monomials
            )

    def test_evaluator_refuses_an_insufficient_subset_budget(self):
        evaluation = evaluate_matching_kernel(
            (1, 1, 1, 1),
            (
                (0, 1, 1, 1),
                (1, 0, 1, 1),
                (1, 1, 0, 1),
                (1, 1, 1, 0),
            ),
            state_budget=15,
        )

        self.assertFalse(evaluation.accepted)
        self.assertEqual(evaluation.refusal.reason, "matching state budget exceeded")

    def test_invalid_counts_and_pair_kernels_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            compile_open_line_quotient(-1)
        with self.assertRaisesRegex(ValueError, "square"):
            evaluate_matching_kernel((1, 1), ((0, 1),), state_budget=4)
        with self.assertRaisesRegex(ValueError, "symmetric"):
            evaluate_matching_kernel(
                (1, 1), ((0, 1), (2, 0)), state_budget=4
            )
if __name__ == "__main__":
    unittest.main()
