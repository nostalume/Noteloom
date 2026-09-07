"""Public laws for exact variable-projector differential jets."""

from __future__ import annotations

import unittest
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from mode_bundle_jet import (
    ModeJetError,
    change_constant_frame,
    construct_mode_jet,
    evaluate_section_second_derivative,
)
from represented_star_algebra import StarAlgebraBudget, StarGenerator, construct
from simple_block_pde import RealizationBudget, construct_irreducible_model


class ModeBundleJetTests(unittest.TestCase):
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

    def test_constant_projector_recovers_exact_g10_decoupling(self) -> None:
        jet = construct_mode_jet(self.model, gaussian.zero(4))

        self.assertTrue(jet.exact_decoupling)
        self.assertEqual(jet.projector_derivative, gaussian.zero(4))
        self.assertTrue(all(jet.checks.values()))

    def test_moving_projector_constructs_nonzero_leakage_and_exact_product_rule(self) -> None:
        transport = gaussian.matrix(
            [[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "transport",
        )

        jet = construct_mode_jet(self.model, transport)
        witness = evaluate_section_second_derivative(
            jet,
            (gaussian.ONE, gaussian.ZERO),
            (gaussian.ONE, gaussian.ZERO),
            (gaussian.ONE, gaussian.ONE),
        )

        self.assertFalse(jet.exact_decoupling)
        self.assertNotEqual(jet.projector_derivative, gaussian.zero(4))
        self.assertNotEqual(witness.leakage, (gaussian.ZERO,) * 4)
        self.assertEqual(witness.direct_second_derivative, witness.synthesis)

    def test_constant_frame_change_preserves_carrier_second_derivative(self) -> None:
        transport = gaussian.matrix(
            [[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "transport",
        )
        gauge = gaussian.matrix([[0, 1], [1, 0]], "gauge")
        original = construct_mode_jet(self.model, transport)
        changed = construct_mode_jet(change_constant_frame(self.model, gauge), transport)
        amplitude = (gaussian.Gaussian(Fraction(2)), gaussian.ONE)
        derivative = (gaussian.ONE, gaussian.Gaussian(Fraction(3)))
        second = (gaussian.Gaussian(Fraction(4)), gaussian.Gaussian(Fraction(5)))
        swapped = lambda value: (value[1], value[0])  # noqa: E731

        original_witness = evaluate_section_second_derivative(
            original, amplitude, derivative, second
        )
        changed_witness = evaluate_section_second_derivative(
            changed, swapped(amplitude), swapped(derivative), swapped(second)
        )

        self.assertEqual(
            changed_witness.direct_second_derivative, original_witness.direct_second_derivative
        )
        self.assertEqual(changed_witness.synthesis, original_witness.synthesis)

    def test_non_skew_transport_and_wrong_gauge_dimension_refuse(self) -> None:
        with self.assertRaises(ModeJetError) as caught:
            construct_mode_jet(self.model, gaussian.identity(4))
        self.assertEqual(caught.exception.kind, "NonSkewTransportGenerator")

        with self.assertRaises(ModeJetError) as caught:
            change_constant_frame(self.model, gaussian.identity(3))
        self.assertEqual(caught.exception.kind, "GaugeDimensionMismatch")
