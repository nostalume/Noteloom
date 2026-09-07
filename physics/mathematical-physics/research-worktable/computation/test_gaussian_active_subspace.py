"""Public laws for exact prepared-observable active carriers."""

from __future__ import annotations

import unittest
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from exact_gaussian_linear import coordinates, matrix_vector
from gaussian_active_subspace import (
    ActiveSubspaceBudget,
    ActiveSubspaceError,
    construct_active_subspace,
    evaluate_active_expectation,
)


def budget(carrier: int, active: int | None = None) -> ActiveSubspaceBudget:
    return ActiveSubspaceBudget(carrier, carrier if active is None else active)


class GaussianActiveSubspaceTests(unittest.TestCase):
    def test_complex_hermitian_hidden_sector_is_removed_and_effect_recovered(self) -> None:
        hamiltonian = gaussian.matrix([[0, [0, 1], 0], [[0, -1], 0, 0], [0, 0, 7]], "Hamiltonian")
        effect = gaussian.matrix([[0, 0, 0], [0, 1, 1], [0, 1, 0]], "effect")

        result = construct_active_subspace(
            hamiltonian,
            (gaussian.ONE, gaussian.ZERO, gaussian.ZERO),
            effect,
            Fraction(1, 2),
            budget(3),
        )

        self.assertEqual(result.status, "ExactPreparedObservableReduction")
        self.assertEqual(result.ambient_dimension, 3)
        self.assertEqual(result.active_dimension, 2)
        self.assertFalse(result.no_dimension_gain)
        self.assertEqual(result.reduced_hamiltonian, gaussian.matrix([[0, 1], [1, 0]], "A"))
        self.assertEqual(result.compressed_effect, gaussian.matrix([[0, 0], [0, 1]], "F"))
        self.assertTrue(
            any(
                coordinates(matrix_vector(effect, vector), result.basis) is None
                for vector in result.basis
            )
        )
        self.assertLessEqual(result.observable_error, result.numerical_tolerance)
        self.assertTrue(all(result.checks.values()))

        later = evaluate_active_expectation(result, Fraction(1, 3))
        direct_later = construct_active_subspace(
            hamiltonian,
            (gaussian.ONE, gaussian.ZERO, gaussian.ZERO),
            effect,
            Fraction(1, 3),
            budget(3),
        )
        self.assertAlmostEqual(later, direct_later.reference_expectation)

    def test_power_basis_uses_exact_gram_metric_not_orthonormalization(self) -> None:
        result = construct_active_subspace(
            gaussian.matrix([[1, 0], [0, 2]], "Hamiltonian"),
            (gaussian.ONE, gaussian.IMAGINARY_UNIT),
            gaussian.matrix([[1, 0], [0, 0]], "effect"),
            Fraction(1),
            budget(2),
        )

        self.assertEqual(result.active_dimension, 2)
        self.assertNotEqual(result.gram, gaussian.identity(2))
        self.assertTrue(result.checks["reduced_hamiltonian_is_gram_self_adjoint"])
        self.assertTrue(result.checks["compressed_effect_is_hermitian"])
        self.assertLessEqual(result.observable_error, result.numerical_tolerance)

    def test_full_cyclic_carrier_reports_no_dimension_gain(self) -> None:
        result = construct_active_subspace(
            gaussian.matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]], "Hamiltonian"),
            (gaussian.ONE, gaussian.ONE, gaussian.ONE),
            gaussian.identity(3),
            Fraction(1),
            budget(3),
        )

        self.assertEqual(result.active_dimension, 3)
        self.assertTrue(result.no_dimension_gain)
        self.assertEqual(result.cost.full_exponential_cubic_proxy, 27)
        self.assertEqual(result.cost.active_exponential_cubic_proxy, 27)

    def test_budget_and_domain_obstructions_refuse_distinctly(self) -> None:
        hamiltonian = gaussian.matrix([[0, 1], [1, 0]], "Hamiltonian")
        preparation = (gaussian.ONE, gaussian.ZERO)

        with self.assertRaises(ActiveSubspaceError) as caught:
            construct_active_subspace(
                hamiltonian,
                preparation,
                gaussian.identity(2),
                Fraction(1),
                budget(2, 1),
            )
        self.assertEqual(caught.exception.kind, "ActiveSubspaceBudgetExceeded")

        with self.assertRaises(ActiveSubspaceError) as caught:
            construct_active_subspace(
                hamiltonian,
                preparation,
                gaussian.matrix([[0, 1], [0, 0]], "bad effect"),
                Fraction(1),
                budget(2),
            )
        self.assertEqual(caught.exception.kind, "NonHermitianEffect")


if __name__ == "__main__":
    unittest.main()
