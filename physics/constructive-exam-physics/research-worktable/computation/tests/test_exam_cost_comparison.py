from collections import Counter
import unittest

from fractions import Fraction

from occ.cost import (
    COST_AXES,
    CostProfile,
    ExamAction,
    HandwrittenRoute,
    compare_exam_routes,
    construct_admission_boundary,
    evaluate_route_admission,
)
from worktable.route_cases import (
    build_route_benchmark,
    run_route_admission,
    run_route_benchmark,
)


class ExamCostComparisonTests(unittest.TestCase):
    def test_route_cost_is_derived_from_an_inspectable_action_ledger(self):
        route = HandwrittenRoute(
            problem_id="fixture",
            target="observable",
            hidden_quantities=("field", "multiplier"),
            actions=(
                ExamAction("relation", "write balance", live_relations=1),
                ExamAction("relation", "write response", live_relations=2),
                ExamAction(
                    "symbolic",
                    "eliminate field and multiplier",
                    live_relations=2,
                    symbolic_subjects=("field", "multiplier"),
                ),
                ExamAction("branch", "choose positive root", live_relations=1),
                ExamAction("representation", "lower to polynomial relation"),
                ExamAction("return", "substitute in original laws"),
            ),
        )

        self.assertEqual(
            route.cost.as_tuple(),
            (2, 2, 2, 2, 1, 1, 1),
        )

    def test_symbolic_cost_is_derived_from_atomic_subjects(self):
        action = ExamAction(
            "symbolic",
            "eliminate three hidden quantities",
            live_relations=4,
            symbolic_subjects=("charge", "initial energy", "final energy"),
        )

        self.assertEqual(action.atomic_units, 3)

    def test_symbolic_action_cannot_hide_an_unidentified_work_unit(self):
        with self.assertRaisesRegex(ValueError, "symbolic_subjects"):
            ExamAction("symbolic", "eliminate several quantities", 3)

    def test_route_comparison_rejects_mixed_execution_substrates(self):
        handwritten = HandwrittenRoute(
            "fixture",
            "observable",
            (),
            (ExamAction("relation", "write direct law", 1),),
            execution_substrate="handwritten",
        )
        tool_assisted = HandwrittenRoute(
            "fixture",
            "observable",
            (),
            (ExamAction("relation", "enter direct law", 1),),
            execution_substrate="tool_assisted",
        )

        with self.assertRaisesRegex(ValueError, "execution substrate"):
            compare_exam_routes(handwritten, tool_assisted)

    def test_comparison_uses_pareto_order_not_an_arbitrary_weighted_score(self):
        baseline = HandwrittenRoute(
            "fixture",
            "observable",
            (),
            (ExamAction("relation", "direct law", 1),),
        )
        proposed = HandwrittenRoute(
            "fixture",
            "observable",
            (),
            (
                ExamAction("relation", "direct law", 1),
                ExamAction("representation", "encode relation", 1),
            ),
        )

        result = compare_exam_routes(baseline, proposed)

        self.assertEqual(result.status, "baseline_win")
        self.assertEqual(result.proposed_worse, ("representation_changes",))

    def test_tradeoff_is_not_promoted_to_a_computational_win(self):
        baseline = HandwrittenRoute(
            "fixture",
            "observable",
            ("x",),
            (
                ExamAction("relation", "law one", 1),
                ExamAction("symbolic", "long substitution", 1, ("x",)),
                ExamAction("symbolic", "finish", 1, ("observable",)),
            ),
        )
        proposed = HandwrittenRoute(
            "fixture",
            "observable",
            (),
            (
                ExamAction("relation", "law one", 1),
                ExamAction("representation", "encode relation", 1),
                ExamAction("symbolic", "eliminate", 1, ("observable",)),
            ),
        )

        result = compare_exam_routes(baseline, proposed)

        self.assertEqual(result.status, "tradeoff")
        self.assertEqual(
            result.proposed_better, ("hidden_quantities", "symbolic_actions")
        )
        self.assertEqual(result.proposed_worse, ("representation_changes",))

    def test_locked_route_benchmark_is_source_bound_and_cross_domain(self):
        cases = build_route_benchmark()

        self.assertEqual(len(cases), 6)
        self.assertEqual(
            {(case.problem_id, case.pdf_page) for case in cases},
            {
                ("A25-03", 4),
                ("A24-09-3", 7),
                ("A22-03-1", 10),
                ("A15-08", 26),
                ("A13-02", 29),
                ("A11-03", 33),
            },
        )
        self.assertEqual(
            {case.area for case in cases},
            {"relativity", "electromagnetism", "thermal-quantum", "fluid-mechanics"},
        )
        self.assertTrue(
            all(case.baseline.target == case.proposed.target for case in cases)
        )

    def test_route_benchmark_does_not_claim_exam_leverage_without_evidence(self):
        result = run_route_benchmark()

        self.assertEqual(
            Counter(comparison.status for comparison in result.comparisons),
            {"baseline_win": 5, "tradeoff": 1},
        )
        self.assertEqual(result.verdict, "exam_leverage_not_established")
        self.assertEqual(result.proposed_wins, 0)

    def test_invalid_action_kind_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "action kind"):
            ExamAction("timing", "invented elapsed time")

    def test_break_even_boundary_is_derived_without_fixed_weights(self):
        case = next(
            case for case in build_route_benchmark() if case.problem_id == "A13-02"
        )

        boundary = construct_admission_boundary(case.baseline, case.proposed)

        self.assertEqual(boundary.classification, "conditional")
        self.assertEqual(boundary.delta, (0, -1, 0, -1, 0, 1, 0))
        self.assertEqual(
            boundary.proposed_cheaper_when,
            "w_representation_changes < w_hidden_quantities + w_symbolic_actions",
        )

    def test_dominated_route_cannot_be_rescued_by_positive_weights(self):
        case = next(
            case for case in build_route_benchmark() if case.problem_id == "A25-03"
        )
        boundary = construct_admission_boundary(case.baseline, case.proposed)
        profile = CostProfile(
            name="positive probe",
            weights=(Fraction(1),) * len(COST_AXES),
            provenance="hypothetical positive weights for a dominance law test",
        )

        decision = evaluate_route_admission(boundary, profile)

        self.assertEqual(boundary.classification, "always_direct")
        self.assertEqual(decision.status, "use_direct")
        self.assertGreater(decision.weighted_delta, 0)

    def test_conditional_boundary_changes_decision_with_declared_profile(self):
        case = next(
            case for case in build_route_benchmark() if case.problem_id == "A13-02"
        )
        boundary = construct_admission_boundary(case.baseline, case.proposed)
        uniform = CostProfile(
            name="unit actions",
            weights=(Fraction(1),) * len(COST_AXES),
            provenance="hypothetical unit-action sensitivity probe",
        )
        expensive_setup = CostProfile(
            name="expensive representation",
            weights=(
                Fraction(1),
                Fraction(1),
                Fraction(1),
                Fraction(1),
                Fraction(1),
                Fraction(3),
                Fraction(1),
            ),
            provenance="hypothetical setup-sensitive probe",
        )

        self.assertEqual(
            evaluate_route_admission(boundary, uniform).status,
            "use_proposed",
        )
        self.assertEqual(
            evaluate_route_admission(boundary, expensive_setup).status,
            "use_direct",
        )

    def test_peak_relation_budget_overrides_a_weighted_gain(self):
        case = next(
            case for case in build_route_benchmark() if case.problem_id == "A13-02"
        )
        boundary = construct_admission_boundary(case.baseline, case.proposed)
        algebra_expensive = CostProfile(
            name="algebra-expensive",
            weights=(
                Fraction(1),
                Fraction(1),
                Fraction(1),
                Fraction(3),
                Fraction(1),
                Fraction(1),
                Fraction(1),
            ),
            provenance="hypothetical high-symbolic-cost probe",
            max_peak_live_relations=1,
        )

        decision = evaluate_route_admission(boundary, algebra_expensive)

        self.assertEqual(decision.status, "use_direct")
        self.assertEqual(decision.reason, "proposed_exceeds_peak_budget")

    def test_route_admission_exposes_regions_without_empirical_claim(self):
        result = run_route_admission()

        self.assertEqual(
            Counter(item.boundary.classification for item in result.cases),
            {"always_direct": 5, "conditional": 1},
        )
        self.assertEqual(
            Counter(item.unit_probe.status for item in result.cases),
            {"use_direct": 5, "use_proposed": 1},
        )
        self.assertEqual(result.conditionally_admitted_problem_ids, ("A13-02",))
        self.assertEqual(
            result.verdict, "conditional_admission_constructed_weights_unmeasured"
        )

    def test_cost_profile_rejects_zero_or_unproven_dimensions(self):
        with self.assertRaisesRegex(ValueError, "strictly positive"):
            CostProfile(
                name="invalid",
                weights=(Fraction(1),) * (len(COST_AXES) - 1) + (Fraction(0),),
                provenance="test",
            )


if __name__ == "__main__":
    unittest.main()
