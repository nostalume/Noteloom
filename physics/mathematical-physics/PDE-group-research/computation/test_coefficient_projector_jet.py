"""Public laws for coefficient-derived spectral-projector jets."""

from __future__ import annotations

import unittest
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from coefficient_projector_jet import (
    CoefficientJet,
    ProjectorJetBudget,
    ProjectorJetError,
    construct_projector_jet,
    construct_rigid_mode_jet,
)
from finite_window_propagation import FinitePropagationWindow, construct_window_propagation
from mode_bundle_jet import construct_mode_jet
from represented_star_algebra import StarAlgebraBudget, StarGenerator, construct
from simple_block_pde import RealizationBudget, construct_irreducible_model


class CoefficientProjectorJetTests(unittest.TestCase):
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
        self.coefficients = CoefficientJet(value, first, second, Fraction(2))
        self.budget = ProjectorJetBudget(4, 64)

    def test_transported_coefficient_constructs_projector_jet_and_downstream_use(self) -> None:
        witness = construct_projector_jet(self.coefficients, self.budget)
        expected = construct_mode_jet(self.model, self.transport)

        self.assertEqual(witness.spectrum, (Fraction(2), Fraction(5)))
        self.assertEqual(witness.spectral_gap, Fraction(3))
        self.assertEqual(witness.cluster_multiplicity, 2)
        self.assertEqual(witness.projector, self.model.selected_projector)
        self.assertEqual(witness.projector_first_derivative, expected.projector_derivative)
        self.assertEqual(
            witness.projector_second_derivative,
            gaussian.bracket(self.transport, expected.projector_derivative),
        )
        self.assertEqual(witness.canonical_transport_generator, self.transport)
        self.assertTrue(witness.rigid_transport)
        self.assertTrue(all(witness.checks.values()))

        jet = construct_rigid_mode_jet(self.model, witness)
        window = FinitePropagationWindow(
            (Fraction(1, 2), Fraction(1)),
            (witness.spectral_gap, witness.spectral_gap),
            Fraction(1, 5),
            Fraction(1),
            ((gaussian.ONE, gaussian.ONE),) * 2,
        )
        propagation = construct_window_propagation(jet, window)
        self.assertGreater(propagation.full_transition_probability, 0)
        self.assertLessEqual(
            propagation.observable_error,
            float(propagation.probability_bound) + propagation.numerical_tolerance,
        )

    def test_rational_carrier_conjugation_preserves_constructed_jet(self) -> None:
        rotation = gaussian.matrix(
            [["3/5", "-4/5", 0, 0], ["4/5", "3/5", 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            "rotation",
        )

        def rotate(value: gaussian.ComplexMatrix) -> gaussian.ComplexMatrix:
            return gaussian.multiply(gaussian.multiply(rotation, value), gaussian.dagger(rotation))

        original = construct_projector_jet(self.coefficients, self.budget)
        transformed = construct_projector_jet(
            CoefficientJet(
                rotate(self.coefficients.value),
                rotate(self.coefficients.first_derivative),
                rotate(self.coefficients.second_derivative),
                self.coefficients.selected_eigenvalue,
            ),
            self.budget,
        )

        self.assertEqual(transformed.projector, rotate(original.projector))
        self.assertEqual(
            transformed.projector_first_derivative,
            rotate(original.projector_first_derivative),
        )
        self.assertEqual(
            transformed.projector_second_derivative,
            rotate(original.projector_second_derivative),
        )
        self.assertEqual(transformed.spectral_gap, original.spectral_gap)

    def test_degenerate_cluster_is_retained_without_eigenvectors(self) -> None:
        value = gaussian.matrix([[0, 0, 0], [0, 0, 0], [0, 0, 2]], "value")
        first = gaussian.matrix([[0, 0, 1], [0, 0, 1], [1, 1, 0]], "first")
        second = gaussian.zero(3)

        witness = construct_projector_jet(
            CoefficientJet(value, first, second, Fraction(0)),
            ProjectorJetBudget(3, 32),
        )

        self.assertEqual(witness.cluster_multiplicity, 2)
        self.assertEqual(
            witness.projector,
            gaussian.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]], "projector"),
        )
        self.assertTrue(all(witness.checks.values()))

    def test_closed_absent_and_nonrigid_cases_refuse_distinctly(self) -> None:
        with self.assertRaises(ProjectorJetError) as caught:
            construct_projector_jet(
                CoefficientJet(gaussian.identity(2), gaussian.zero(2), gaussian.zero(2), 1),
                ProjectorJetBudget(2, 16),
            )
        self.assertEqual(caught.exception.kind, "SpectralGapClosed")

        with self.assertRaises(ProjectorJetError) as caught:
            construct_projector_jet(
                CoefficientJet(
                    self.coefficients.value,
                    self.coefficients.first_derivative,
                    self.coefficients.second_derivative,
                    7,
                ),
                self.budget,
            )
        self.assertEqual(caught.exception.kind, "SelectedClusterAbsent")

        nonhermitian = gaussian.matrix(
            [[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "nonhermitian derivative",
        )
        with self.assertRaises(ProjectorJetError) as caught:
            construct_projector_jet(
                CoefficientJet(
                    self.coefficients.value,
                    nonhermitian,
                    self.coefficients.second_derivative,
                    2,
                ),
                self.budget,
            )
        self.assertEqual(caught.exception.kind, "NonHermitianCoefficientJet")

        perturbation = gaussian.matrix(
            [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "second perturbation",
        )
        nonrigid = construct_projector_jet(
            CoefficientJet(
                self.coefficients.value,
                self.coefficients.first_derivative,
                gaussian.add(self.coefficients.second_derivative, perturbation),
                2,
            ),
            self.budget,
        )
        self.assertFalse(nonrigid.rigid_transport)
        with self.assertRaises(ProjectorJetError) as caught:
            construct_rigid_mode_jet(self.model, nonrigid)
        self.assertEqual(caught.exception.kind, "NonRigidProjectorJet")


if __name__ == "__main__":
    unittest.main()
