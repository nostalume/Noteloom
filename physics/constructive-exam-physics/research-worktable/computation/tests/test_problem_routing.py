import unittest

from sympy import symbols

from occ.adaptive import AdaptiveRelationRequest
from occ.problem import PhysicalLaw
from occ.routing import (
    ProblemCard,
    compile_problem_card,
)
from worktable.routing_cases import build_routing_benchmark, run_routing_benchmark


class ProblemRoutingTests(unittest.TestCase):
    def test_one_law_without_hidden_quantities_routes_directly(self):
        given, target = symbols("given target")
        request = AdaptiveRelationRequest(
            problem_id="direct-fixture",
            laws=(PhysicalLaw("direct law", target - 2 * given, "fixture"),),
            givens=(given,),
            target=target,
        )

        result = compile_problem_card(
            ProblemCard(
                problem_id="direct-fixture",
                observable="target",
                provenance="routing RED fixture",
                request=request,
            )
        )

        self.assertEqual(result.status, "constructed")
        self.assertEqual(result.operator, "direct_relation")
        self.assertEqual(result.source_status, "constructed")
        self.assertTrue(result.certificates)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_frozen_bench_selects_existing_owners_or_exact_refusals(self):
        results = {result.card.problem_id: result for result in run_routing_benchmark()}

        expected = {
            "A24-09": ("direct_relation", "constructed", None),
            "A13-02": ("polynomial_relation", "constructed", None),
            "functional-transfer": ("source_functional", "constructed", None),
            "linear-closure": ("linear_closure", "constructed", None),
            "A15-01": ("event_relation", "constructed", None),
            "A15-02": ("frictional_impact", "constructed", None),
            "A14-06": ("path_functional", "constructed", None),
            "A10-06": ("path_functional", "constructed", None),
            "A21-03": ("harmonic_response", "constructed", None),
            "A25-06": ("harmonic_response", "constructed", None),
            "adversarial-ambiguous": (
                "relation_projection",
                "ambiguous",
                "ambiguous_minimal_packets",
            ),
            "adversarial-transcendental": (
                "relation_projection",
                "refused",
                "unsupported_relation_shape",
            ),
        }
        self.assertEqual(set(results), set(expected))
        for problem_id, (operator, status, obstruction) in expected.items():
            with self.subTest(problem_id=problem_id):
                result = results[problem_id]
                self.assertEqual(result.operator, operator)
                self.assertEqual(result.status, status)
                code = None if result.obstruction is None else result.obstruction.code
                self.assertEqual(code, obstruction)

    def test_every_constructed_bench_result_preserves_passing_certificates(self):
        constructed = [
            result
            for result in run_routing_benchmark()
            if result.status == "constructed"
        ]

        self.assertEqual(len(constructed), 10)
        for result in constructed:
            with self.subTest(problem_id=result.card.problem_id):
                self.assertTrue(result.certificates)
                self.assertTrue(
                    all(certificate.passed for certificate in result.certificates)
                )

    def test_event_construction_rejoins_the_existing_cost_boundary(self):
        result = next(
            result
            for result in run_routing_benchmark()
            if result.card.problem_id == "A15-01"
        )

        self.assertEqual(result.admission.classification, "always_direct")
        self.assertEqual(result.admission.baseline.target, result.card.observable)

    def test_problem_identity_does_not_choose_the_relation_operator(self):
        first_given, first_target = symbols("first_given first_target")
        second_given, second_target = symbols("second_given second_target")
        first = compile_problem_card(
            ProblemCard(
                "first-id",
                "answer",
                "first fixture",
                AdaptiveRelationRequest(
                    "first-id",
                    (PhysicalLaw("law", first_target - first_given, "fixture"),),
                    (first_given,),
                    first_target,
                ),
            )
        )
        second = compile_problem_card(
            ProblemCard(
                "unrelated-name",
                "answer",
                "second fixture",
                AdaptiveRelationRequest(
                    "unrelated-name",
                    (PhysicalLaw("law", second_target - second_given, "fixture"),),
                    (second_given,),
                    second_target,
                ),
            )
        )

        self.assertEqual(first.operator, "direct_relation")
        self.assertEqual(second.operator, first.operator)

    def test_card_admission_rejects_unknown_request_or_mismatched_identity(self):
        with self.assertRaisesRegex(TypeError, "unsupported request type"):
            ProblemCard("bad", "target", "fixture", object())

        given, target = symbols("given target")
        request = AdaptiveRelationRequest(
            "inner",
            (PhysicalLaw("law", target - given, "fixture"),),
            (given,),
            target,
        )
        with self.assertRaisesRegex(ValueError, "problem ids must match"):
            ProblemCard("outer", "target", "fixture", request)

    def test_frozen_cards_contain_no_expected_answer_field(self):
        for card in build_routing_benchmark():
            self.assertFalse(hasattr(card, "expected_answer"))


if __name__ == "__main__":
    unittest.main()
