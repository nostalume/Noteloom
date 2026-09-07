"""Public laws for gap-aware finite-dimensional leakage calibration."""

from __future__ import annotations

import unittest
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from gap_aware_leakage import LeakageBoundError, LeakageWindow, construct_leakage_bound
from mode_bundle_jet import change_constant_frame, construct_mode_jet
from represented_star_algebra import StarAlgebraBudget, StarGenerator, construct
from simple_block_pde import RealizationBudget, construct_irreducible_model


class GapAwareLeakageTests(unittest.TestCase):
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
            [[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "transport",
        )

    def test_moving_jet_constructs_exact_formula_and_gap_bound(self) -> None:
        jet = construct_mode_jet(self.model, self.transport)
        window = LeakageWindow(
            momentum=Fraction(1, 2),
            slow_scale=Fraction(20, 101),
            gap=Fraction(198, 101),
            time=Fraction(2),
            prepared_column=0,
        )

        witness = construct_leakage_bound(jet, window)

        self.assertEqual(witness.coupling, Fraction(20, 101))
        self.assertEqual(witness.frequency, Fraction(1))
        self.assertEqual(witness.transition_coefficient, Fraction(400, 10201))
        self.assertEqual(witness.phase, Fraction(2))
        self.assertEqual(witness.probability_bound, Fraction(400, 9801))
        self.assertEqual(witness.domain_contract, "finite-dimensional bounded two-channel carrier")
        self.assertIn("transition probability", witness.observable)
        self.assertLessEqual(witness.observed_probability, float(witness.probability_bound))
        self.assertTrue(all(witness.checks.values()))

    def test_constant_frame_transfer_preserves_carrier_preparation(self) -> None:
        original = construct_mode_jet(self.model, self.transport)
        gauge = gaussian.matrix([[0, 1], [1, 0]], "gauge")
        changed = construct_mode_jet(change_constant_frame(self.model, gauge), self.transport)
        common = dict(
            momentum=Fraction(1, 2),
            slow_scale=Fraction(20, 101),
            gap=Fraction(198, 101),
            time=Fraction(2),
        )

        left = construct_leakage_bound(original, LeakageWindow(**common, prepared_column=0))
        right = construct_leakage_bound(changed, LeakageWindow(**common, prepared_column=1))

        self.assertEqual(right.off_block_vector, left.off_block_vector)
        self.assertEqual(right.probability_bound, left.probability_bound)
        self.assertEqual(right.observed_probability, left.observed_probability)

    def test_exact_decoupling_recovers_zero_observable_error(self) -> None:
        jet = construct_mode_jet(self.model, gaussian.zero(4))
        window = LeakageWindow(Fraction(1), Fraction(1), Fraction(2), Fraction(2), 0)

        witness = construct_leakage_bound(jet, window)

        self.assertEqual(witness.coupling, 0)
        self.assertEqual(witness.observed_probability, 0.0)
        self.assertEqual(witness.probability_bound, 0)

    def test_closing_gap_and_unsupported_exact_frequency_refuse(self) -> None:
        jet = construct_mode_jet(self.model, self.transport)
        with self.assertRaises(LeakageBoundError) as caught:
            construct_leakage_bound(
                jet, LeakageWindow(Fraction(1, 2), Fraction(1), Fraction(0), Fraction(1), 0)
            )
        self.assertEqual(caught.exception.kind, "ClosingGapObstruction")

        with self.assertRaises(LeakageBoundError) as caught:
            construct_leakage_bound(
                jet, LeakageWindow(Fraction(1, 2), Fraction(1), Fraction(1), Fraction(1), 0)
            )
        self.assertEqual(caught.exception.kind, "ExactFrequencyFieldExtensionRequired")


if __name__ == "__main__":
    unittest.main()
