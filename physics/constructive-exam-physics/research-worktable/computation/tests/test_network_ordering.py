import unittest
from dataclasses import replace

from sympy import symbols

from occ.network import (
    LinearNetworkRequest,
    NetworkVariable,
    condense_linear_network,
)
from occ.network_order import plan_network_elimination


def variable(symbol, name, state_kind="potential"):
    return NetworkVariable(symbol, name, state_kind)


def sparse_branch_request(area="electricity", state_kind="voltage"):
    left, right, center, leaf_one, leaf_two = symbols("x_L x_R x_C x_1 x_2")
    return LinearNetworkRequest(
        area=area,
        variables=(
            variable(left, "left boundary", state_kind),
            variable(right, "right boundary", state_kind),
            variable(center, "central junction", state_kind),
            variable(leaf_one, "first grounded branch", state_kind),
            variable(leaf_two, "second grounded branch", state_kind),
        ),
        boundary_symbols=(left, right),
        internal_symbols=(center, leaf_one, leaf_two),
        response_matrix=(
            (1, 0, -1, 0, 0),
            (0, 1, -1, 0, 0),
            (-1, -1, 4, -1, -1),
            (0, 0, -1, 2, 0),
            (0, 0, -1, 0, 2),
        ),
        source_vector=(0, 0, 0, 0, 0),
        provenance=f"{area} sparse-branch ordering bench",
    )


class NetworkOrderingTests(unittest.TestCase):
    def test_minimum_fill_order_reduces_local_work_against_declared_order(self):
        request = sparse_branch_request()
        center, leaf_one, leaf_two = request.internal_symbols

        planned = plan_network_elimination(request, strategy="min_fill")
        declared = plan_network_elimination(request, strategy="declared")

        self.assertEqual(planned.status, "constructed")
        self.assertEqual(planned.elimination_order, (leaf_one, leaf_two, center))
        self.assertEqual(declared.elimination_order, (center, leaf_one, leaf_two))
        self.assertEqual(planned.total_fill_edges, 1)
        self.assertEqual(declared.total_fill_edges, 6)
        self.assertEqual(planned.total_algebraic_updates, 5)
        self.assertEqual(declared.total_algebraic_updates, 19)

    def test_sequential_result_and_reverse_recovery_equal_block_condensation(self):
        request = sparse_branch_request()
        boundary_values = symbols("V_L V_R")

        planned = plan_network_elimination(request)
        block = condense_linear_network(request)

        self.assertEqual(planned.condensed_matrix, block.condensed_matrix)
        self.assertEqual(planned.condensed_source, block.condensed_source)
        self.assertEqual(
            planned.reconstruct_internal(boundary_values),
            block.reconstruct_internal(boundary_values),
        )
        self.assertTrue(all(item.passed for item in planned.certificates))

    def test_same_sparse_order_transfers_across_area_semantics(self):
        circuit = plan_network_elimination(sparse_branch_request())
        elastic = plan_network_elimination(
            sparse_branch_request("mechanics", "displacement")
        )

        self.assertEqual(circuit.elimination_order, elastic.elimination_order)
        self.assertEqual(circuit.condensed_matrix, elastic.condensed_matrix)
        self.assertEqual(elastic.area, "mechanics")
        self.assertEqual(elastic.state_kind, "displacement")

    def test_nonzero_source_counts_only_its_affected_neighbor_updates(self):
        request = replace(sparse_branch_request(), source_vector=(0, 0, 1, 0, 0))

        result = plan_network_elimination(request)

        self.assertEqual(result.total_algebraic_updates, 7)
        self.assertEqual(
            tuple(step.algebraic_updates for step in result.steps), (1, 1, 5)
        )

    def test_nonreciprocal_matrix_is_outside_the_human_sparse_planner(self):
        boundary, hidden = symbols("x_B x_h")
        request = LinearNetworkRequest(
            area="directed response",
            variables=(variable(boundary, "boundary"), variable(hidden, "hidden")),
            boundary_symbols=(boundary,),
            internal_symbols=(hidden,),
            response_matrix=((1, 1), (0, 1)),
            source_vector=(0, 0),
            provenance="nonreciprocal refusal bench",
        )

        result = plan_network_elimination(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "nonreciprocal_response")

    def test_invertible_block_without_scalar_pivot_is_explicitly_refused(self):
        boundary, hidden_one, hidden_two = symbols("x_B x_1 x_2")
        request = LinearNetworkRequest(
            area="reciprocal response",
            variables=(
                variable(boundary, "boundary"),
                variable(hidden_one, "first hidden"),
                variable(hidden_two, "second hidden"),
            ),
            boundary_symbols=(boundary,),
            internal_symbols=(hidden_one, hidden_two),
            response_matrix=((1, 0, 0), (0, 0, 1), (0, 1, 0)),
            source_vector=(0, 0, 0),
            provenance="two-by-two pivot boundary",
        )

        self.assertEqual(condense_linear_network(request).status, "constructed")
        result = plan_network_elimination(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "no_provable_scalar_pivot")

    def test_step_budget_refuses_before_returning_a_partial_plan(self):
        result = plan_network_elimination(sparse_branch_request(), max_steps=2)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "elimination_step_budget_exceeded")
        self.assertEqual(result.steps, ())

    def test_no_internal_state_preserves_the_original_boundary_law(self):
        boundary = symbols("x_B")
        request = LinearNetworkRequest(
            area="electricity",
            variables=(variable(boundary, "terminal voltage", "voltage"),),
            boundary_symbols=(boundary,),
            internal_symbols=(),
            response_matrix=((2,),),
            source_vector=(3,),
            provenance="already-boundary-only bench",
        )

        result = plan_network_elimination(request)

        self.assertEqual(result.status, "irreducible")
        self.assertEqual(result.condensed_matrix, ((2,),))
        self.assertEqual(result.condensed_source, (3,))

    def test_unknown_strategy_is_rejected_at_admission(self):
        with self.assertRaisesRegex(ValueError, "strategy"):
            plan_network_elimination(sparse_branch_request(), strategy="magic")


if __name__ == "__main__":
    unittest.main()
