import unittest

from sympy import cos, simplify, sqrt, symbols

from occ.event import (
    EventPredicate,
    EventProblem,
    VariableInterval,
    construct_event,
)
from occ.problem import PhysicalLaw
from worktable.event_cases import build_a15_event_problem, run_event_transfer


class EventConstructorTests(unittest.TestCase):
    def test_source_transfer_keeps_machine_construction_and_hand_route_distinct(self):
        result = run_event_transfer()

        self.assertEqual(result.event.status, "constructed")
        self.assertEqual(result.handwritten_comparison.status, "baseline_win")
        self.assertEqual(result.admission.classification, "always_direct")

    def test_a15_pendulum_constructs_event_equation_and_unique_physical_branch(self):
        request = build_a15_event_problem()
        speed_squared, vertical_acceleration, cosine = request.unknowns

        result = construct_event(request)

        expected_cosine = (1 + sqrt(301)) / 30
        self.assertEqual(result.status, "constructed")
        self.assertTrue(result.projection.implies(15 * cosine**2 - cosine - 5))
        self.assertEqual(len(result.algebraic_branches), 2)
        self.assertEqual(len(result.admissible_branches), 1)
        self.assertEqual(
            simplify(result.selected.value(cosine) - expected_cosine),
            0,
        )
        self.assertEqual(result.selected.value(vertical_acceleration), 0)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_two_lifted_roots_inside_domain_return_ambiguity(self):
        position, marker = symbols("position marker")
        request = EventProblem(
            problem_id="ambiguous-crossing",
            pdf_page=1,
            state_laws=(PhysicalLaw("state map", marker - position**2, "fixture"),),
            event=EventPredicate("unit marker", marker - 1, "fixture"),
            unknowns=(marker, position),
            event_coordinate=position,
            domains=(VariableInterval(position, lower=-2, upper=2),),
        )

        result = construct_event(request)

        self.assertEqual(result.status, "ambiguous")
        self.assertEqual(result.obstruction.code, "ambiguous_event_branches")
        self.assertEqual(
            {branch.value(position) for branch in result.admissible_branches},
            {-1, 1},
        )
        self.assertIsNone(result.selected)

    def test_event_with_no_branch_in_physical_domain_is_reported(self):
        position, marker = symbols("position marker")
        request = EventProblem(
            problem_id="unreached-crossing",
            pdf_page=1,
            state_laws=(PhysicalLaw("state map", marker - position**2, "fixture"),),
            event=EventPredicate("unit marker", marker - 1, "fixture"),
            unknowns=(marker, position),
            event_coordinate=position,
            domains=(VariableInterval(position, lower=2, upper=3),),
        )

        result = construct_event(request)

        self.assertEqual(result.status, "no_event")
        self.assertEqual(result.obstruction.code, "no_admissible_event")
        self.assertEqual(result.admissible_branches, ())
        self.assertIsNone(result.selected)

    def test_nonpolynomial_event_is_refused_at_the_backend_boundary(self):
        angle, marker = symbols("angle marker")
        request = EventProblem(
            problem_id="transcendental-event",
            pdf_page=1,
            state_laws=(PhysicalLaw("state map", marker - cos(angle), "fixture"),),
            event=EventPredicate("zero marker", marker, "fixture"),
            unknowns=(marker, angle),
            event_coordinate=angle,
        )

        result = construct_event(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "unsupported_relation_shape")

    def test_variable_budget_refuses_before_branch_solving(self):
        x, y = symbols("x y")
        request = EventProblem(
            problem_id="budgeted-event",
            pdf_page=1,
            state_laws=(PhysicalLaw("state map", y - x, "fixture"),),
            event=EventPredicate("origin", y, "fixture"),
            unknowns=(y, x),
            event_coordinate=x,
            max_variables=1,
        )

        result = construct_event(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "variable_budget_exceeded")


if __name__ == "__main__":
    unittest.main()
