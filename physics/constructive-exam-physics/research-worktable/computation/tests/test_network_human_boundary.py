import unittest
from fractions import Fraction

from sympy import symbols

from occ.cost import (
    COST_AXES,
    CostProfile,
    evaluate_route_admission,
)
from occ.network import (
    LinearNetworkRequest,
    NetworkVariable,
)
from occ.network_human import construct_network_human_boundary


def sparse_request():
    left, right, center, leaf_one, leaf_two = symbols("x_L x_R x_C x_1 x_2")
    variables = tuple(
        NetworkVariable(symbol, name, "voltage")
        for symbol, name in (
            (left, "left boundary"),
            (right, "right boundary"),
            (center, "central junction"),
            (leaf_one, "first grounded branch"),
            (leaf_two, "second grounded branch"),
        )
    )
    return LinearNetworkRequest(
        area="electricity",
        variables=variables,
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
        provenance="matched sparse human-boundary fixture",
    )


class NetworkHumanBoundaryTests(unittest.TestCase):
    def test_constructs_atomic_route_ledgers_and_exact_break_even_region(self):
        result = construct_network_human_boundary(
            sparse_request(), problem_id="N-H1", target="terminal response"
        )

        self.assertEqual(result.status, "constructed")
        self.assertEqual(result.declared_route.cost.as_tuple(), (1, 3, 5, 19, 0, 0, 1))
        self.assertEqual(result.sparse_route.cost.as_tuple(), (1, 3, 5, 5, 0, 3, 1))
        self.assertEqual(result.admission_boundary.classification, "conditional")
        self.assertEqual(result.admission_boundary.delta, (0, 0, 0, -14, 0, 3, 0))
        self.assertEqual(
            result.admission_boundary.proposed_cheaper_when,
            "3*w_representation_changes < 14*w_symbolic_actions",
        )
        self.assertEqual(result.fill_delta, -5)
        self.assertTrue(all(item.passed for item in result.certificates))

    def test_hypothetical_profiles_can_fall_on_opposite_sides(self):
        result = construct_network_human_boundary(
            sparse_request(), problem_id="N-H1", target="terminal response"
        )
        uniform = CostProfile(
            "uniform probe",
            (Fraction(1),) * len(COST_AXES),
            "hypothetical sensitivity analysis only",
        )
        recognition_expensive = CostProfile(
            "recognition-expensive probe",
            (
                Fraction(1),
                Fraction(1),
                Fraction(1),
                Fraction(1),
                Fraction(1),
                Fraction(6),
                Fraction(1),
            ),
            "hypothetical sensitivity analysis only",
        )

        self.assertEqual(
            evaluate_route_admission(result.admission_boundary, uniform).status,
            "use_proposed",
        )
        self.assertEqual(
            evaluate_route_admission(
                result.admission_boundary, recognition_expensive
            ).status,
            "use_direct",
        )

    def test_deduction_does_not_promote_unobserved_human_claims(self):
        result = construct_network_human_boundary(
            sparse_request(), problem_id="N-H1", target="terminal response"
        )

        self.assertEqual(result.speed_disposition, "conditional_weights_unmeasured")
        self.assertEqual(result.learnability_disposition, "human_observations_required")
        self.assertEqual(
            result.required_evidence,
            (
                "independent_route_key_review",
                "matched_correct_execution",
                "participant_clustered_timing",
                "delayed_retention",
                "unseen_topology_transfer",
            ),
        )

    def test_same_order_exposes_recognition_overhead_and_selects_direct(self):
        left, right, hidden = symbols("x_L x_R x_h")
        request = LinearNetworkRequest(
            area="electricity",
            variables=(
                NetworkVariable(left, "left terminal", "voltage"),
                NetworkVariable(right, "right terminal", "voltage"),
                NetworkVariable(hidden, "junction", "voltage"),
            ),
            boundary_symbols=(left, right),
            internal_symbols=(hidden,),
            response_matrix=((1, 0, -1), (0, 1, -1), (-1, -1, 2)),
            source_vector=(0, 0, 0),
            provenance="single-hidden direct-gate fixture",
        )

        result = construct_network_human_boundary(
            request, problem_id="N-H3", target="terminal response"
        )

        self.assertEqual(result.status, "constructed")
        self.assertEqual(result.admission_boundary.classification, "always_direct")
        self.assertEqual(result.speed_disposition, "structural_model_favors_declared")
        self.assertEqual(result.learnability_disposition, "human_observations_required")

    def test_scalar_planning_obstruction_prevents_a_cost_claim(self):
        boundary, hidden_one, hidden_two = symbols("x_B x_1 x_2")
        request = LinearNetworkRequest(
            area="reciprocal response",
            variables=(
                NetworkVariable(boundary, "boundary", "potential"),
                NetworkVariable(hidden_one, "first hidden", "potential"),
                NetworkVariable(hidden_two, "second hidden", "potential"),
            ),
            boundary_symbols=(boundary,),
            internal_symbols=(hidden_one, hidden_two),
            response_matrix=((1, 0, 0), (0, 0, 1), (0, 1, 0)),
            source_vector=(0, 0, 0),
            provenance="scalar-pivot refusal fixture",
        )

        result = construct_network_human_boundary(
            request, problem_id="N-H2", target="boundary response"
        )

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "no_provable_scalar_pivot")
        self.assertIsNone(result.admission_boundary)

    def test_identity_fields_are_required_before_comparison(self):
        with self.assertRaisesRegex(ValueError, "problem_id"):
            construct_network_human_boundary(
                sparse_request(), problem_id="", target="terminal response"
            )


if __name__ == "__main__":
    unittest.main()
