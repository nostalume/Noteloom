"""Public laws for complete local coefficient-route comparison."""

from __future__ import annotations

import unittest
from fractions import Fraction

import numpy as np

import exact_gaussian_matrix as gaussian
from coefficient_projector_jet import CoefficientJet, ProjectorJetBudget, construct_projector_jet
from complete_route_leverage import (
    CoefficientRouteProblem,
    ComparisonBudget,
    RouteComparisonError,
    compare_complete_routes,
)
from exact_gaussian_linear import matrix_vector
from finite_window_propagation import FinitePropagationWindow
from represented_star_algebra import StarAlgebraBudget, StarGenerator, construct
from simple_block_pde import RealizationBudget, construct_irreducible_model


def _outer(left, right):
    return tuple(
        tuple(left[row] * right[column].conjugate() for column in range(len(right)))
        for row in range(len(left))
    )


def _standard_vector(dimension: int, selected: int):
    return tuple(gaussian.ONE if index == selected else gaussian.ZERO for index in range(dimension))


def repeated_pauli_problem(multiplicity: int, window_size: int) -> CoefficientRouteProblem:
    dimension = 2 * multiplicity
    identity = np.eye(multiplicity, dtype=int)
    generators = (
        StarGenerator(
            "X",
            gaussian.matrix(np.kron(np.array([[0, 1], [1, 0]], dtype=int), identity).tolist(), "X"),
        ),
        StarGenerator(
            "Z",
            gaussian.matrix(
                np.kron(np.array([[1, 0], [0, -1]], dtype=int), identity).tolist(), "Z"
            ),
        ),
    )
    algebra = construct(generators, StarAlgebraBudget(dimension, 2, dimension * dimension, 128))
    model = construct_irreducible_model(algebra, 0, RealizationBudget(dimension * dimension, 128))
    projector = model.selected_projector
    complement = gaussian.add(gaussian.identity(dimension), gaussian.scale(projector, -1))
    retained = model.embedding_columns[0]
    outside = None
    for index in range(dimension):
        candidate = matrix_vector(complement, _standard_vector(dimension, index))
        if any(entry != gaussian.ZERO for entry in candidate):
            outside = candidate
            break
    if outside is None:
        raise AssertionError("the repeated carrier must have a complement")
    crossing = _outer(outside, retained)
    transport = gaussian.add(crossing, gaussian.scale(gaussian.dagger(crossing), -1))
    value = gaussian.add(gaussian.scale(projector, 2), gaussian.scale(complement, 5))
    first = gaussian.bracket(transport, value)
    acceleration = gaussian.add(crossing, gaussian.dagger(crossing))
    second = gaussian.add(gaussian.bracket(transport, first), acceleration)
    momenta = tuple(Fraction(index + 1, 2) for index in range(window_size))
    window = FinitePropagationWindow(
        momenta,
        (Fraction(3),) * window_size,
        Fraction(1, 5),
        Fraction(1),
        ((gaussian.ONE, gaussian.ONE),) * window_size,
    )
    return CoefficientRouteProblem(
        model,
        CoefficientJet(value, first, second, Fraction(2)),
        ProjectorJetBudget(dimension, 128),
        window,
    )


def budget(
    dimension: int,
    step: float = 1e-3,
    observable_tolerance: float = 1e-5,
    cluster_tolerance: float = 1e-8,
    repetitions: int = 1,
) -> ComparisonBudget:
    return ComparisonBudget(
        maximum_carrier_dimension=dimension,
        finite_difference_step=step,
        cluster_tolerance=cluster_tolerance,
        observable_tolerance=observable_tolerance,
        timing_repetitions=repetitions,
    )


class CompleteRouteLeverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.multiplicity_two = repeated_pauli_problem(2, 2)

    def test_same_observable_comparison_keeps_cost_kinds_separate(self) -> None:
        result = compare_complete_routes(self.multiplicity_two, budget(4, repetitions=2))
        projector = construct_projector_jet(
            self.multiplicity_two.coefficient_jet,
            self.multiplicity_two.projector_budget,
        )

        self.assertFalse(projector.rigid_transport)
        self.assertLessEqual(result.observable_error, result.contract.observable_tolerance)
        self.assertTrue(all(result.checks.values()))
        self.assertEqual(result.exact.work.numerical_eigendecompositions, 0)
        self.assertEqual(result.sampled.work.numerical_eigendecompositions, 3)
        self.assertEqual(result.exact.work.coefficient_samples, 0)
        self.assertEqual(result.sampled.work.coefficient_samples, 3)
        self.assertGreater(result.exact.work.exact_sylvester_blocks, 0)
        self.assertEqual(result.exact.work.propagated_blocks, 2)
        self.assertEqual(result.sampled.work.propagated_blocks, 2)
        self.assertEqual(result.proxy_disposition, "heterogeneous-no-scalar-dominance")
        self.assertGreater(result.exact.median_runtime_seconds, 0)
        self.assertGreater(result.sampled.median_runtime_seconds, 0)
        self.assertEqual(result.timing_context.repetitions, 2)
        self.assertTrue(result.timing_context.python_version)

    def test_multiplicity_three_and_larger_window_transfer_unchanged(self) -> None:
        problem = repeated_pauli_problem(3, 3)
        result = compare_complete_routes(problem, budget(6, observable_tolerance=2e-5))

        self.assertLessEqual(result.observable_error, result.contract.observable_tolerance)
        self.assertEqual(result.exact.work.block_dimension, 6)
        self.assertEqual(result.exact.work.propagated_blocks, 3)
        self.assertEqual(result.exact.work.analysis_coordinate_solves, 0)
        self.assertEqual(result.shared_stages, ("G9/G10 model realization",))
        self.assertIn("original unbounded PDE propagation", result.unpaid_stages)
        self.assertIn("standalone sampled-projector truncation certificate", result.unpaid_stages)

    def test_sampled_projector_converges_under_step_refinement(self) -> None:
        coarse = compare_complete_routes(
            self.multiplicity_two, budget(4, step=5e-2, observable_tolerance=2e-2)
        )
        fine = compare_complete_routes(
            self.multiplicity_two, budget(4, step=1e-2, observable_tolerance=2e-2)
        )

        self.assertLess(fine.observable_error, coarse.observable_error)
        self.assertEqual(fine.sampled.semantic.numerical_policy_choices, 2)
        self.assertLess(
            fine.exact.semantic.transformation_count,
            fine.sampled.semantic.transformation_count,
        )
        self.assertLess(
            fine.exact.semantic.independent_objects,
            fine.sampled.semantic.independent_objects,
        )
        self.assertEqual(
            fine.human_disposition, "lower-declared-exact-depth-with-more-theorem-debt"
        )

    def test_invalid_budget_ambiguous_cluster_and_unmet_accuracy_refuse(self) -> None:
        with self.assertRaises(RouteComparisonError) as caught:
            compare_complete_routes(self.multiplicity_two, budget(3))
        self.assertEqual(caught.exception.kind, "ComparisonBudgetExceeded")

        with self.assertRaises(RouteComparisonError) as caught:
            compare_complete_routes(
                self.multiplicity_two, budget(4, cluster_tolerance=10, observable_tolerance=1)
            )
        self.assertEqual(caught.exception.kind, "SampledClusterUnseparated")

        with self.assertRaises(RouteComparisonError) as caught:
            compare_complete_routes(
                self.multiplicity_two, budget(4, step=1e-1, observable_tolerance=1e-14)
            )
        self.assertEqual(caught.exception.kind, "ObservableAccuracyUnmet")


if __name__ == "__main__":
    unittest.main()
