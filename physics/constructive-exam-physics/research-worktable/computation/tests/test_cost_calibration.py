from dataclasses import replace
from fractions import Fraction
import unittest

from occ.cost import (
    COST_AXES,
    ExamAction,
    HandwrittenRoute,
    construct_admission_boundary,
)
from occ.calibration import (
    PairedRouteObservation,
    calibrate_paired_route_costs,
    evaluate_held_out_route,
)
from worktable.route_cases import build_route_benchmark


ACTIVE_WEIGHTS = {
    "hidden_quantities": Fraction(2),
    "peak_live_relations": Fraction(3),
    "symbolic_actions": Fraction(5),
    "representation_changes": Fraction(11),
}


def _synthetic_observations():
    observations = []
    for index, case in enumerate(build_route_benchmark(), start=1):
        boundary = construct_admission_boundary(case.baseline, case.proposed)
        time_delta = sum(
            ACTIVE_WEIGHTS.get(axis, Fraction(0)) * coefficient
            for axis, coefficient in zip(COST_AXES, boundary.delta)
        )
        observations.append(
            PairedRouteObservation(
                sample_id=f"synthetic-{index}",
                problem_id=case.problem_id,
                boundary=boundary,
                direct_seconds=Fraction(100),
                proposed_seconds=Fraction(100) + time_delta,
                direct_correct=True,
                proposed_correct=True,
                provenance="synthetic exact-recovery fixture; not learner evidence",
                order_control="synthetic counterbalanced order",
            )
        )
    return tuple(observations)


def _held_out_boundary(problem_id="held-out"):
    direct = HandwrittenRoute(
        problem_id,
        "observable",
        ("intermediate",),
        (ExamAction("relation", "write direct relation", 1),),
    )
    proposed = HandwrittenRoute(
        problem_id,
        "observable",
        (),
        (
            ExamAction("relation", "write direct relation", 1),
            ExamAction("representation", "enter relation view", 1),
        ),
    )
    return construct_admission_boundary(direct, proposed)


class CostCalibrationTests(unittest.TestCase):
    def test_exact_paired_differences_recover_identified_axis_weights(self):
        result = calibrate_paired_route_costs(
            "synthetic recovery",
            _synthetic_observations(),
        )

        self.assertEqual(result.status, "calibrated")
        self.assertIsNotNone(result.profile)
        self.assertEqual(result.profile.identified_axes, tuple(ACTIVE_WEIGHTS))
        self.assertEqual(result.profile.axis_weights, ACTIVE_WEIGHTS)
        self.assertEqual(result.profile.residual_sum_squares, 0)
        self.assertIn("synthetic", result.profile.provenance)

    def test_rank_deficiency_returns_the_unidentified_axes(self):
        result = calibrate_paired_route_costs(
            "rank-deficient",
            _synthetic_observations()[:2],
        )

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.kind, "insufficient_rank")
        self.assertTrue(result.obstruction.unidentified_axes)

    def test_incorrect_pairs_are_excluded_and_cannot_create_a_profile(self):
        observation = _synthetic_observations()[0]
        incorrect = PairedRouteObservation(
            sample_id=observation.sample_id,
            problem_id=observation.problem_id,
            boundary=observation.boundary,
            direct_seconds=observation.direct_seconds,
            proposed_seconds=observation.proposed_seconds,
            direct_correct=True,
            proposed_correct=False,
            provenance=observation.provenance,
            order_control=observation.order_control,
        )

        result = calibrate_paired_route_costs("no correct pairs", (incorrect,))

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.kind, "no_correct_pairs")
        self.assertEqual(result.excluded_sample_ids, (incorrect.sample_id,))

    def test_nonpositive_seconds_per_unit_fit_is_rejected(self):
        direct = HandwrittenRoute(
            "negative-fit",
            "observable",
            (),
            (ExamAction("relation", "write direct relation", 1),),
        )
        proposed = HandwrittenRoute(
            "negative-fit",
            "observable",
            (),
            (
                ExamAction("relation", "write direct relation", 1),
                ExamAction("representation", "enter relation view", 1),
            ),
        )
        boundary = construct_admission_boundary(direct, proposed)
        observation = PairedRouteObservation(
            sample_id="negative-fit-1",
            problem_id="negative-fit",
            boundary=boundary,
            direct_seconds=Fraction(20),
            proposed_seconds=Fraction(10),
            direct_correct=True,
            proposed_correct=True,
            provenance="synthetic contradiction fixture",
            order_control="synthetic counterbalanced order",
        )

        result = calibrate_paired_route_costs("negative fit", (observation,))

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.kind, "nonpositive_fit")

    def test_held_out_prediction_uses_only_identified_axes(self):
        profile = calibrate_paired_route_costs(
            "synthetic recovery",
            _synthetic_observations(),
        ).profile
        observation = PairedRouteObservation(
            sample_id="held-out-1",
            problem_id="held-out",
            boundary=_held_out_boundary(),
            direct_seconds=Fraction(20),
            proposed_seconds=Fraction(29),
            direct_correct=True,
            proposed_correct=True,
            provenance="synthetic held-out fixture",
            order_control="synthetic counterbalanced order",
        )

        evaluation = evaluate_held_out_route(profile, observation)

        self.assertEqual(evaluation.status, "matched")
        self.assertEqual(evaluation.predicted_route, "direct")
        self.assertEqual(evaluation.observed_best_route, "direct")
        self.assertEqual(evaluation.predicted_time_delta, 9)

    def test_holdout_refuses_training_leakage(self):
        observations = _synthetic_observations()
        profile = calibrate_paired_route_costs(
            "synthetic recovery",
            observations,
        ).profile

        evaluation = evaluate_held_out_route(profile, observations[0])

        self.assertEqual(evaluation.status, "refused")
        self.assertEqual(evaluation.reason, "training_problem_leakage")

    def test_holdout_refuses_an_axis_not_identified_by_training(self):
        profile = calibrate_paired_route_costs(
            "synthetic recovery",
            _synthetic_observations(),
        ).profile
        direct = HandwrittenRoute(
            "new-axis",
            "observable",
            (),
            (ExamAction("relation", "one relation", 1),),
        )
        proposed = HandwrittenRoute(
            "new-axis",
            "observable",
            (),
            (
                ExamAction("relation", "one relation", 1),
                ExamAction("relation", "second relation", 2),
            ),
        )
        observation = PairedRouteObservation(
            sample_id="new-axis-1",
            problem_id="new-axis",
            boundary=construct_admission_boundary(direct, proposed),
            direct_seconds=Fraction(10),
            proposed_seconds=Fraction(12),
            direct_correct=True,
            proposed_correct=True,
            provenance="synthetic unseen-axis fixture",
            order_control="synthetic counterbalanced order",
        )

        evaluation = evaluate_held_out_route(profile, observation)

        self.assertEqual(evaluation.status, "refused")
        self.assertEqual(evaluation.reason, "unidentified_prediction_axis")
        self.assertEqual(evaluation.unidentified_axes, ("relations_selected",))

    def test_personal_profile_refuses_mixed_participant_training_rows(self):
        observations = _synthetic_observations()
        mixed = (
            replace(observations[0], participant_id="learner-a"),
            replace(observations[1], participant_id="learner-b"),
        )

        with self.assertRaisesRegex(ValueError, "one participant"):
            calibrate_paired_route_costs("mixed learner", mixed)

    def test_holdout_refuses_a_different_participant(self):
        observations = tuple(
            replace(item, participant_id="learner-a")
            for item in _synthetic_observations()
        )
        profile = calibrate_paired_route_costs("learner a", observations).profile
        held_out = PairedRouteObservation(
            sample_id="other-learner-held-out",
            problem_id="held-out",
            boundary=_held_out_boundary(),
            direct_seconds=Fraction(20),
            proposed_seconds=Fraction(29),
            direct_correct=True,
            proposed_correct=True,
            provenance="synthetic other-learner fixture",
            order_control="synthetic counterbalanced order",
            participant_id="learner-b",
            session_id="session-b",
        )

        evaluation = evaluate_held_out_route(profile, held_out)

        self.assertEqual(evaluation.status, "refused")
        self.assertEqual(evaluation.reason, "participant_mismatch")


if __name__ == "__main__":
    unittest.main()
