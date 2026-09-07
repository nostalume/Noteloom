"""Public laws for invariant full-block finite-window propagation."""

from __future__ import annotations

import unittest
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from finite_window_propagation import (
    FinitePropagationWindow,
    WindowPropagationError,
    construct_window_propagation,
)
from mode_bundle_jet import change_constant_frame, construct_mode_jet
from represented_star_algebra import StarAlgebraBudget, StarGenerator, construct
from simple_block_pde import RealizationBudget, construct_irreducible_model


class FiniteWindowPropagationTests(unittest.TestCase):
    def setUp(self) -> None:
        generators = (
            StarGenerator(
                "X",
                gaussian.matrix(
                    [[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]],
                    "X",
                ),
            ),
            StarGenerator(
                "Z",
                gaussian.matrix(
                    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]],
                    "Z",
                ),
            ),
        )
        algebra = construct(generators, StarAlgebraBudget(4, 2, 16, 64))
        self.model = construct_irreducible_model(algebra, 0, RealizationBudget(4, 64))
        self.transport = gaussian.matrix(
            [[0, -1, 0, -1], [1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]],
            "rank-one transport",
        )
        self.jet = construct_mode_jet(self.model, self.transport)

    def window(self, preparation: tuple[gaussian.Gaussian, ...]) -> FinitePropagationWindow:
        return FinitePropagationWindow(
            momenta=(Fraction(1, 2), Fraction(1)),
            gaps=(Fraction(2), Fraction(3)),
            slow_scale=Fraction(1, 5),
            time=Fraction(1),
            preparations=(preparation, preparation),
        )

    def test_full_map_propagates_bright_state_on_two_momentum_window(self) -> None:
        witness = construct_window_propagation(self.jet, self.window((gaussian.ONE, gaussian.ONE)))

        self.assertEqual(len(witness.blocks), 2)
        self.assertTrue(all(block.coupling_rank == 1 for block in witness.blocks))
        self.assertEqual(
            tuple(block.frobenius_upper_squared for block in witness.blocks),
            (Fraction(2, 25), Fraction(8, 25)),
        )
        self.assertEqual(witness.short_time_bound, Fraction(1, 5))
        self.assertEqual(witness.gap_bound, Fraction(1, 9))
        self.assertEqual(witness.probability_bound, Fraction(1, 9))
        self.assertEqual(witness.cost.analysis_coordinate_solves, 4)
        self.assertEqual(witness.cost.propagated_blocks, 2)
        self.assertGreater(witness.full_transition_probability, 0.0)
        self.assertEqual(witness.reduced_transition_probability, 0.0)
        self.assertLessEqual(
            witness.observable_error,
            float(witness.probability_bound) + witness.numerical_tolerance,
        )
        self.assertTrue(all(witness.checks.values()))

    def test_coherent_dark_state_is_removed_by_full_map_not_column_sum(self) -> None:
        witness = construct_window_propagation(
            self.jet, self.window((gaussian.ONE, gaussian.Gaussian(Fraction(-1))))
        )

        self.assertTrue(all(block.preparation_coupling_squared == 0 for block in witness.blocks))
        self.assertEqual(witness.probability_bound, 0)
        self.assertLessEqual(witness.observable_error, witness.numerical_tolerance)

    def test_constant_frame_change_preserves_operator_state_and_observable(self) -> None:
        gauge = gaussian.matrix([[0, 1], [1, 0]], "gauge")
        changed = construct_mode_jet(change_constant_frame(self.model, gauge), self.transport)
        original = self.window((gaussian.ONE, gaussian.Gaussian(Fraction(2))))
        transformed = self.window((gaussian.Gaussian(Fraction(2)), gaussian.ONE))

        left = construct_window_propagation(self.jet, original)
        right = construct_window_propagation(changed, transformed)

        self.assertEqual(
            tuple(block.coupling_operator for block in right.blocks),
            tuple(block.coupling_operator for block in left.blocks),
        )
        self.assertEqual(right.probability_bound, left.probability_bound)
        self.assertAlmostEqual(right.observable_error, left.observable_error, places=14)

    def test_constant_jet_recovers_zero_and_bad_windows_refuse(self) -> None:
        constant = construct_mode_jet(self.model, gaussian.zero(4))
        witness = construct_window_propagation(constant, self.window((gaussian.ONE, gaussian.ONE)))
        self.assertEqual(witness.probability_bound, 0)
        self.assertLessEqual(witness.observable_error, witness.numerical_tolerance)

        with self.assertRaises(WindowPropagationError) as caught:
            construct_window_propagation(
                self.jet,
                FinitePropagationWindow(
                    (Fraction(0),),
                    (Fraction(0),),
                    Fraction(1),
                    Fraction(1),
                    ((gaussian.ONE, gaussian.ONE),),
                ),
            )
        self.assertEqual(caught.exception.kind, "ClosingGapObstruction")

        with self.assertRaises(WindowPropagationError) as caught:
            construct_window_propagation(
                self.jet,
                FinitePropagationWindow(
                    (Fraction(0), Fraction(1)),
                    (Fraction(1),),
                    Fraction(1),
                    Fraction(1),
                    ((gaussian.ONE, gaussian.ONE),),
                ),
            )
        self.assertEqual(caught.exception.kind, "WindowLengthMismatch")


if __name__ == "__main__":
    unittest.main()
