"""Transfer laws for prepared-observable reduction on G15 windows."""

from __future__ import annotations

import unittest

from active_window_propagation import (
    construct_prepared_active_window,
    construct_projector_active_window_propagation,
    evaluate_active_window_at_time,
)
from coefficient_projector_jet import construct_projector_jet
from complete_route_bench import repeated_pauli_problem
from finite_window_propagation import construct_off_block_prepared_window, propagate_prepared_window
from gaussian_active_subspace import ActiveSubspaceBudget
from off_block_differential import construct_off_block_differential
from projector_native_propagation import construct_projector_window_propagation


class ActiveWindowPropagationTests(unittest.TestCase):
    def construct(self, multiplicity: int, window_size: int):
        problem = repeated_pauli_problem(multiplicity, window_size)
        projector = construct_projector_jet(problem.coefficient_jet, problem.projector_budget)
        differential = construct_off_block_differential(
            problem.model,
            projector.projector,
            projector.first_off_block_operator,
            projector.second_off_block_operator,
            "G14 coefficient-derived projector jet",
        )
        prepared = construct_off_block_prepared_window(problem.model, differential, problem.window)
        full = propagate_prepared_window(prepared)
        active = construct_prepared_active_window(
            prepared,
            ActiveSubspaceBudget(2 * multiplicity, 2 * multiplicity),
            reference_expectations=tuple(
                block.observed_transition_probability for block in full.blocks
            ),
        )
        return full, active

    def test_repeated_pauli_window_removes_unreachable_multiplicity(self) -> None:
        full, active = self.construct(2, 2)

        self.assertEqual(active.ambient_dimensions, (4, 4))
        self.assertEqual(active.active_dimensions, (3, 3))
        self.assertLessEqual(active.observable_error, active.numerical_tolerance)
        self.assertAlmostEqual(active.active_probability, full.full_transition_probability)
        self.assertEqual(active.cost.full_exponential_cubic_proxy, 2 * 4**3)
        self.assertEqual(active.cost.active_exponential_cubic_proxy, 2 * 3**3)
        self.assertTrue(all(active.checks.values()))

    def test_multiplicity_three_and_larger_window_transfer_unchanged(self) -> None:
        _, active = self.construct(3, 4)

        self.assertEqual(active.ambient_dimensions, (6,) * 4)
        self.assertEqual(active.active_dimensions, (3,) * 4)
        self.assertEqual(active.cost.full_exponential_cubic_proxy, 4 * 6**3)
        self.assertEqual(active.cost.active_exponential_cubic_proxy, 4 * 3**3)
        self.assertEqual(active.cost.full_reference_exponentials_evaluated, 0)
        self.assertTrue(all(active.checks.values()))

    def test_standalone_route_does_not_evaluate_full_exponential(self) -> None:
        problem = repeated_pauli_problem(2, 2)
        projector = construct_projector_jet(problem.coefficient_jet, problem.projector_budget)
        full = construct_projector_window_propagation(problem.model, projector, problem.window)

        active = construct_projector_active_window_propagation(
            problem.model,
            projector,
            problem.window,
            ActiveSubspaceBudget(4, 4),
        )

        self.assertIsNone(active.reference_probability)
        self.assertIsNone(active.observable_error)
        self.assertAlmostEqual(active.active_probability, full.full_transition_probability)
        self.assertEqual(active.cost.full_reference_exponentials_evaluated, 0)
        self.assertGreaterEqual(evaluate_active_window_at_time(active, 0), 0)


if __name__ == "__main__":
    unittest.main()
