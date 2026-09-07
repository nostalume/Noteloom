"""Public laws for projector-native finite-window propagation."""

from __future__ import annotations

import unittest
from dataclasses import replace
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from coefficient_projector_jet import CoefficientJet, ProjectorJetBudget, construct_projector_jet
from finite_window_propagation import FinitePropagationWindow, construct_window_propagation
from mode_bundle_jet import change_constant_frame
from projector_native_propagation import construct_projector_window_propagation
from represented_star_algebra import StarAlgebraBudget, StarGenerator, construct
from simple_block_pde import RealizationBudget, construct_irreducible_model


class ProjectorNativePropagationTests(unittest.TestCase):
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
            "transport",
        )
        projector = self.model.selected_projector
        complement = gaussian.add(gaussian.identity(4), gaussian.scale(projector, -1))
        value = gaussian.add(gaussian.scale(projector, 2), gaussian.scale(complement, 5))
        first = gaussian.bracket(self.transport, value)
        second = gaussian.bracket(self.transport, first)
        self.rigid = construct_projector_jet(
            CoefficientJet(value, first, second, Fraction(2)),
            ProjectorJetBudget(4, 64),
        )
        perturbation = gaussian.matrix(
            [[0, 1, 0, 1], [1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]],
            "non-rigid acceleration",
        )
        self.nonrigid = construct_projector_jet(
            CoefficientJet(value, first, gaussian.add(second, perturbation), Fraction(2)),
            ProjectorJetBudget(4, 64),
        )

    def rigid_window(self, preparation: tuple[gaussian.Gaussian, ...]) -> FinitePropagationWindow:
        return FinitePropagationWindow(
            (Fraction(1, 2), Fraction(1)),
            (self.rigid.spectral_gap,) * 2,
            Fraction(1, 5),
            Fraction(1),
            (preparation,) * 2,
        )

    def acceleration_window(
        self, preparation: tuple[gaussian.Gaussian, ...]
    ) -> FinitePropagationWindow:
        return FinitePropagationWindow(
            (Fraction(0),),
            (self.nonrigid.spectral_gap,),
            Fraction(1),
            Fraction(1),
            (preparation,),
        )

    def test_rigid_projector_route_exactly_recovers_g11_route(self) -> None:
        from coefficient_projector_jet import construct_rigid_mode_jet

        window = self.rigid_window((gaussian.ONE, gaussian.Gaussian(2)))
        legacy = construct_window_propagation(
            construct_rigid_mode_jet(self.model, self.rigid), window
        )
        native = construct_projector_window_propagation(self.model, self.rigid, window)

        self.assertEqual(
            tuple(block.coupling_operator for block in native.blocks),
            tuple(block.coupling_operator for block in legacy.blocks),
        )
        self.assertEqual(native.short_time_bound, legacy.short_time_bound)
        self.assertEqual(native.gap_bound, legacy.gap_bound)
        self.assertAlmostEqual(native.observable_error, legacy.observable_error, places=14)
        self.assertEqual(native.differential_source, "G14 coefficient-derived projector jet")
        self.assertEqual(legacy.differential_source, "G11 frame leakage columns")
        self.assertEqual(native.cost.analysis_coordinate_solves, 0)
        self.assertEqual(legacy.cost.analysis_coordinate_solves, 4)

    def test_nonrigid_second_arrow_produces_bright_and_dark_observables(self) -> None:
        self.assertFalse(self.nonrigid.rigid_transport)
        bright = construct_projector_window_propagation(
            self.model,
            self.nonrigid,
            self.acceleration_window((gaussian.ONE, gaussian.ONE)),
        )
        dark = construct_projector_window_propagation(
            self.model,
            self.nonrigid,
            self.acceleration_window((gaussian.ONE, gaussian.Gaussian(-1))),
        )

        self.assertEqual(bright.blocks[0].coupling_rank, 1)
        self.assertGreater(bright.blocks[0].preparation_coupling_squared, 0)
        self.assertGreater(bright.full_transition_probability, 0)
        self.assertEqual(dark.blocks[0].preparation_coupling_squared, 0)
        self.assertEqual(dark.probability_bound, 0)
        self.assertLessEqual(dark.observable_error, dark.numerical_tolerance)

    def test_reduced_frame_change_preserves_carrier_operator_and_observable(self) -> None:
        gauge = gaussian.matrix([[0, 1], [1, 0]], "gauge")
        changed = change_constant_frame(self.model, gauge)
        left = construct_projector_window_propagation(
            self.model,
            self.nonrigid,
            self.acceleration_window((gaussian.ONE, gaussian.Gaussian(2))),
        )
        right = construct_projector_window_propagation(
            changed,
            self.nonrigid,
            self.acceleration_window((gaussian.Gaussian(2), gaussian.ONE)),
        )

        self.assertEqual(right.blocks[0].coupling_operator, left.blocks[0].coupling_operator)
        self.assertEqual(right.probability_bound, left.probability_bound)
        self.assertAlmostEqual(right.observable_error, left.observable_error, places=14)

    def test_mismatched_projector_and_malformed_arrow_refuse(self) -> None:
        with self.assertRaisesRegex(ValueError, "selected G10 block"):
            construct_projector_window_propagation(
                replace(self.model, selected_projector=gaussian.zero(4)),
                self.nonrigid,
                self.acceleration_window((gaussian.ONE, gaussian.ONE)),
            )

        with self.assertRaisesRegex(ValueError, "off-block"):
            construct_projector_window_propagation(
                self.model,
                replace(self.nonrigid, second_off_block_operator=gaussian.identity(4)),
                self.acceleration_window((gaussian.ONE, gaussian.ONE)),
            )


if __name__ == "__main__":
    unittest.main()
