"""Public laws for one active carrier shared by a coefficient family."""

from __future__ import annotations

import unittest
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from gaussian_active_subspace import (
    ActiveSubspaceBudget,
    ActiveSubspaceError,
    construct_active_subspace,
    construct_coefficient_family_active_subspace,
    evaluate_family_expectation,
    specialize_active_hamiltonian,
)


class CoefficientFamilyActiveSubspaceTests(unittest.TestCase):
    def test_common_module_specializes_exactly_and_recovers_effect(self) -> None:
        coefficients = (
            gaussian.matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]], "H0"),
            gaussian.matrix([[1, 0, 0], [0, 2, 0], [0, 0, 7]], "H1"),
        )
        preparation = (gaussian.ONE, gaussian.ZERO, gaussian.ZERO)
        effect = gaussian.matrix([[0, 0, 0], [0, 1, 1], [0, 1, 0]], "effect")

        result = construct_coefficient_family_active_subspace(
            coefficients,
            preparation,
            effect,
            ActiveSubspaceBudget(3, 3),
        )

        self.assertEqual(result.status, "ExactCoefficientFamilyReduction")
        self.assertEqual(result.active_dimension, 2)
        self.assertFalse(result.no_dimension_gain)
        self.assertEqual(result.coefficient_count, 2)
        self.assertTrue(all(result.checks.values()))

        weights = (Fraction(2), Fraction(3))
        reduced = specialize_active_hamiltonian(result, weights)
        full = gaussian.add(gaussian.scale(coefficients[0], 2), gaussian.scale(coefficients[1], 3))
        pointwise = construct_active_subspace(
            full,
            preparation,
            effect,
            Fraction(1, 3),
            ActiveSubspaceBudget(3, 3),
        )
        self.assertEqual(len(reduced), 2)
        self.assertAlmostEqual(
            evaluate_family_expectation(result, weights, Fraction(1, 3)),
            pointwise.reference_expectation,
        )

    def test_generator_closure_cannot_be_inferred_from_one_cancelled_sample(self) -> None:
        coefficients = (
            gaussian.matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]], "H0"),
            gaussian.matrix([[0, -1, 0], [-1, 0, 1], [0, 1, 0]], "H1"),
        )
        preparation = (gaussian.ONE, gaussian.ZERO, gaussian.ZERO)
        effect = gaussian.identity(3)

        family = construct_coefficient_family_active_subspace(
            coefficients, preparation, effect, ActiveSubspaceBudget(3, 3)
        )
        cancelled = gaussian.add(coefficients[0], coefficients[1])
        pointwise = construct_active_subspace(
            cancelled,
            preparation,
            effect,
            Fraction(1),
            ActiveSubspaceBudget(3, 3),
        )

        self.assertEqual(family.active_dimension, 3)
        self.assertTrue(family.no_dimension_gain)
        self.assertEqual(pointwise.active_dimension, 1)

    def test_family_domain_and_specialization_refusals_are_distinct(self) -> None:
        good = gaussian.matrix([[0, 1], [1, 0]], "good")
        preparation = (gaussian.ONE, gaussian.ZERO)

        with self.assertRaises(ActiveSubspaceError) as caught:
            construct_coefficient_family_active_subspace(
                (), preparation, gaussian.identity(2), ActiveSubspaceBudget(2, 2)
            )
        self.assertEqual(caught.exception.kind, "EmptyCoefficientFamily")

        with self.assertRaises(ActiveSubspaceError) as caught:
            construct_coefficient_family_active_subspace(
                (good,), preparation, gaussian.identity(2), ActiveSubspaceBudget(2, 1)
            )
        self.assertEqual(caught.exception.kind, "ActiveSubspaceBudgetExceeded")

        with self.assertRaises(ActiveSubspaceError) as caught:
            construct_coefficient_family_active_subspace(
                (gaussian.matrix([[0, 1], [0, 0]], "bad"),),
                preparation,
                gaussian.identity(2),
                ActiveSubspaceBudget(2, 2),
            )
        self.assertEqual(caught.exception.kind, "NonHermitianCoefficient")

        family = construct_coefficient_family_active_subspace(
            (good,), preparation, gaussian.identity(2), ActiveSubspaceBudget(2, 2)
        )
        with self.assertRaises(ActiveSubspaceError) as caught:
            specialize_active_hamiltonian(family, (Fraction(1), Fraction(2)))
        self.assertEqual(caught.exception.kind, "CoefficientWeightLengthMismatch")


if __name__ == "__main__":
    unittest.main()
