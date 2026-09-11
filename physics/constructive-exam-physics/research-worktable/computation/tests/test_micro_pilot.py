from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from occ.micro_study import (
    MicroToolObservation,
    RouteRecognitionObservation,
    build_recognition_schedules,
)
from occ.pilot import (
    ROUTE_KEY_REVIEW_COLUMNS,
    ROUTE_KEY_REVIEWER_COLUMNS,
    RouteKeyAudit,
    RouteKeyReviewer,
    audit_route_key,
    construct_micro_pilot_diagnostics,
    evaluate_route_key_preflight,
    load_route_key_review_tsv,
    load_route_key_reviewer_tsv,
    summarize_micro_pilot,
)
from worktable.micro_study_cases import (
    build_micro_tool_pairs,
    build_route_recognition_tasks,
)


TEMPLATE = (
    Path(__file__).parents[2] / "observations" / "d4-route-key-review-template.tsv"
)
REVIEWER_TEMPLATE = TEMPLATE.with_name("d4-route-key-reviewer-template.tsv")
REVIEWER_PACKET = TEMPLATE.with_name("d4-route-key-reviewer-packet.md")


class MicroPilotTests(unittest.TestCase):
    def test_empty_key_review_is_unobserved_not_agreement(self):
        tasks = build_route_recognition_tasks()
        reviews = load_route_key_review_tsv(TEMPLATE, tasks)
        reviewers = load_route_key_reviewer_tsv(
            REVIEWER_TEMPLATE, build_recognition_schedules(tasks)
        )

        audits = audit_route_key(tasks, reviews, reviewers)

        self.assertEqual(reviews, ())
        self.assertEqual(reviewers, ())
        self.assertEqual({audit.status for audit in audits}, {"unreviewed"})

    def test_key_audit_distinguishes_agreement_ambiguity_and_dispute(self):
        tasks = build_route_recognition_tasks()
        rows = (
            self._row("1", "expert-a", "R01", "direct"),
            self._row("2", "expert-b", "R01", "direct"),
            self._row("3", "expert-a", "R02", "direct"),
            self._row("4", "expert-b", "R02", "slice"),
            self._row("5", "expert-a", "R03", "direct"),
            self._row("6", "expert-b", "R03", "direct"),
            self._row("7", "expert-a", "R04", "projection"),
        )
        reviews = self._load(rows, tasks)

        audits = {
            audit.task_id: audit
            for audit in audit_route_key(tasks, reviews, self._reviewers())
        }

        self.assertEqual(audits["R01"].status, "agreed")
        self.assertEqual(audits["R02"].status, "ambiguous")
        self.assertEqual(audits["R03"].status, "key_disputed")
        self.assertEqual(audits["R04"].status, "insufficient_review")
        self.assertEqual(audits["R05"].status, "unreviewed")

    def test_unblinded_review_is_retained_but_not_admitted(self):
        tasks = build_route_recognition_tasks()
        reviews = self._load((self._row("1", "expert-a", "R01", "direct"),), tasks)
        reviewer = self._load_reviewers(
            (
                {
                    "reviewer_id": "expert-a",
                    "sequence_id": "R1",
                    "expertise_domain": "introductory mechanics",
                    "authored_key_blinded": "false",
                    "peer_reviews_blinded": "true",
                    "provenance": "preflight fixture",
                },
            ),
            tasks,
        )[0]

        audit = audit_route_key(tasks, reviews, (reviewer,))[0]

        self.assertEqual(audit.status, "protocol_invalid")
        self.assertEqual(audit.reviewer_count, 0)
        self.assertEqual(audit.excluded_review_count, 1)

    def test_blinded_reviewer_packet_contains_prompts_without_key_mapping(self):
        text = REVIEWER_PACKET.read_text(encoding="utf-8")
        for task in build_route_recognition_tasks():
            self.assertIn(task.prompt, text)
            self.assertNotIn(f"| {task.task_id} | `{task.expected_route}`", text)

    def test_preflight_kernel_freezes_review_and_revision_consequences(self):
        tasks = build_route_recognition_tasks()
        agreed = tuple(self._audit(task, "agreed") for task in tasks)

        ready = evaluate_route_key_preflight(tasks, agreed)

        self.assertEqual(ready.status, "ready_for_learner_pilot")
        self.assertEqual(ready.admitted_task_ids, tuple(task.task_id for task in tasks))
        self.assertEqual(ready.needs_review_task_ids, ())
        self.assertEqual(ready.revision_task_ids, ())

        mixed = list(agreed)
        mixed[0] = self._audit(tasks[0], "ambiguous")
        mixed[1] = self._audit(tasks[1], "insufficient_review")
        blocked = evaluate_route_key_preflight(tasks, tuple(mixed))

        self.assertEqual(blocked.status, "contract_revision_required")
        self.assertEqual(blocked.revision_task_ids, ("R01",))
        self.assertEqual(blocked.needs_review_task_ids, ("R02",))

    def test_preflight_does_not_treat_absent_review_as_ready(self):
        tasks = build_route_recognition_tasks()
        reviews = load_route_key_review_tsv(TEMPLATE, tasks)
        reviewers = load_route_key_reviewer_tsv(
            REVIEWER_TEMPLATE, build_recognition_schedules(tasks)
        )

        preflight = evaluate_route_key_preflight(
            tasks, audit_route_key(tasks, reviews, reviewers)
        )

        self.assertEqual(preflight.status, "additional_review_required")
        self.assertEqual(len(preflight.needs_review_task_ids), 12)
        self.assertEqual(preflight.admitted_task_ids, ())

    def test_key_loader_refuses_duplicate_reviewer_task(self):
        tasks = build_route_recognition_tasks()
        duplicate = (
            self._row("1", "expert-a", "R01", "direct"),
            self._row("2", "expert-a", "R01", "direct"),
        )

        with self.assertRaisesRegex(ValueError, "reviewer task"):
            self._load(duplicate, tasks)

    def test_summary_is_descriptive_and_scores_only_agreed_keys(self):
        tasks = build_route_recognition_tasks()
        reviews = self._load(
            (
                self._row("1", "expert-a", "R01", "direct"),
                self._row("2", "expert-b", "R01", "direct"),
            ),
            tasks,
        )
        key_audits = audit_route_key(tasks, reviews, self._reviewers())
        recognition = (
            RouteRecognitionObservation(
                "recognition-1",
                "recognizer-1",
                "r-session",
                "R1",
                1,
                "R01",
                "direct",
                "direct",
                Fraction(8),
                "synthetic analysis fixture",
            ),
        )
        execution = (
            self._execution("execution-1", "direct", Fraction(100)),
            self._execution("execution-2", "slice", Fraction(85)),
        )

        summary = summarize_micro_pilot(
            tasks,
            key_audits,
            recognition,
            execution,
            build_micro_tool_pairs(),
        )

        self.assertEqual(summary.status, "descriptive_only")
        self.assertEqual(summary.route_key_agreed_tasks, 1)
        self.assertEqual(summary.recognition_scored_rows, 1)
        self.assertEqual(summary.recognition_correct_rows, 1)
        self.assertEqual(summary.execution_rows, 2)
        self.assertEqual(summary.eligible_pairs, 1)
        self.assertEqual(summary.operator_faster_pairs, 1)
        self.assertEqual(summary.speed_disposition, "not_evaluated")

    def test_pilot_diagnostics_cluster_timing_by_participant_and_phase(self):
        pairs = build_micro_tool_pairs()
        observations = self._complete_diagnostic_fixture(pairs)

        diagnostics = construct_micro_pilot_diagnostics(observations, pairs)

        self.assertEqual(diagnostics.status, "design_inputs_observed")
        self.assertEqual(len(diagnostics.phases), 3)
        for phase in diagnostics.phases:
            self.assertEqual(phase.participant_count, 2)
            self.assertEqual(phase.observed_rows, 16)
            self.assertEqual(phase.direct_attempts, 8)
            self.assertEqual(phase.operator_attempts, 8)
            self.assertEqual(phase.direct_correct, 8)
            self.assertEqual(phase.operator_correct, 8)
            self.assertEqual(phase.expected_pair_slots, 8)
            self.assertEqual(phase.eligible_pairs, 8)
            self.assertEqual(phase.ineligible_pairs, 0)
            self.assertEqual(phase.missing_pairs, 0)
            self.assertEqual(phase.complete_timing_clusters, 2)
            self.assertEqual(phase.mean_cluster_time_delta, Fraction(-5))
            self.assertEqual(phase.sample_variance_cluster_time_delta, Fraction(800))
            self.assertEqual(phase.reliable_phase_clusters, 2)
            self.assertEqual(
                phase.mean_cluster_phase_deltas,
                (Fraction(0), Fraction(0), Fraction(-5), Fraction(0)),
            )
            self.assertEqual(phase.maximum_variant_route_imbalance, 0)
            self.assertEqual(phase.unobserved_variants, 0)

    def test_pilot_diagnostics_do_not_invent_variance_without_data(self):
        diagnostics = construct_micro_pilot_diagnostics((), build_micro_tool_pairs())

        self.assertEqual(diagnostics.status, "unobserved")
        for phase in diagnostics.phases:
            self.assertEqual(phase.complete_timing_clusters, 0)
            self.assertIsNone(phase.mean_cluster_time_delta)
            self.assertIsNone(phase.sample_variance_cluster_time_delta)
            self.assertIsNone(phase.mean_cluster_phase_deltas)

    def test_pilot_diagnostics_retain_failure_but_exclude_its_timing_cluster(self):
        pairs = build_micro_tool_pairs()
        observations = list(self._complete_diagnostic_fixture(pairs))
        index = next(
            index
            for index, item in enumerate(observations)
            if item.observation_id == "executor-1-assisted-jet-operator"
        )
        observations[index] = replace(
            observations[index], correct=False, error_codes=("algebra",)
        )

        diagnostics = construct_micro_pilot_diagnostics(tuple(observations), pairs)
        assisted = diagnostics.phases[0]

        self.assertEqual(diagnostics.status, "design_inputs_incomplete")
        self.assertEqual(assisted.operator_attempts, 8)
        self.assertEqual(assisted.operator_correct, 7)
        self.assertEqual(assisted.eligible_pairs, 7)
        self.assertEqual(assisted.ineligible_pairs, 1)
        self.assertEqual(assisted.complete_timing_clusters, 1)
        self.assertEqual(assisted.mean_cluster_time_delta, Fraction(15))
        self.assertIsNone(assisted.sample_variance_cluster_time_delta)

    def test_pilot_diagnostics_refuse_nonunique_variant_identity(self):
        pairs = list(build_micro_tool_pairs())
        pairs[1] = replace(pairs[1], variant_a=pairs[0].variant_a)

        with self.assertRaisesRegex(ValueError, "variant ids must be unique"):
            construct_micro_pilot_diagnostics((), tuple(pairs))

    def _row(self, review_id, reviewer_id, task_id, selected_route):
        return {
            "review_id": review_id,
            "reviewer_id": reviewer_id,
            "task_id": task_id,
            "selected_route": selected_route,
            "rationale": "independent route judgment",
            "provenance": "closed-book expert preflight",
        }

    def _audit(self, task, status):
        return RouteKeyAudit(
            task_id=task.task_id,
            expected_route=task.expected_route,
            status=status,
            reviewer_count=2,
            excluded_review_count=0,
            selected_routes=(task.expected_route,),
        )

    def _reviewers(self):
        return (
            RouteKeyReviewer(
                "expert-a", "R1", "introductory physics", True, True, "fixture"
            ),
            RouteKeyReviewer(
                "expert-b", "R2", "introductory physics", True, True, "fixture"
            ),
        )

    def _execution(self, observation_id, route, total):
        return MicroToolObservation(
            observation_id=observation_id,
            participant_id="executor-1",
            session_id="e-session",
            sequence_id="M1",
            trial_order=1 if route == "direct" else 5,
            phase="assisted",
            pair_id="assisted-jet",
            variant_id="D3-A-J1" if route == "direct" else "D3-A-J2",
            assigned_route=route,
            card_available=route != "direct",
            hours_since_assisted=Fraction(0),
            interpretation_seconds=Fraction(0),
            setup_seconds=Fraction(0),
            computation_seconds=Fraction(0),
            return_seconds=Fraction(0),
            independent_total_seconds=total,
            phase_timing_reliable=False,
            completion="complete",
            correct=True,
            error_codes=(),
            route_adherent=True,
            prior_familiarity="same_structure_seen",
            provenance="synthetic analysis fixture",
        )

    def _complete_diagnostic_fixture(self, pairs):
        deltas = {
            "executor-1": (-10, -20, -30, -40),
            "executor-2": (0, 10, 20, 30),
        }
        observations = []
        for phase_index, phase in enumerate(
            ("assisted", "internalized", "delayed_unseen")
        ):
            phase_pairs = tuple(pair for pair in pairs if pair.phase == phase)
            for participant_index, (participant_id, participant_deltas) in enumerate(
                deltas.items()
            ):
                for family_index, (pair, delta) in enumerate(
                    zip(phase_pairs, participant_deltas, strict=True)
                ):
                    direct_variant, operator_variant = (
                        (pair.variant_a.variant_id, pair.variant_b.variant_id)
                        if participant_index == 0
                        else (pair.variant_b.variant_id, pair.variant_a.variant_id)
                    )
                    common = {
                        "participant_id": participant_id,
                        "session_id": f"{participant_id}-{phase}",
                        "sequence_id": f"M{participant_index + 1}",
                        "phase": phase,
                        "pair_id": pair.pair_id,
                        "hours_since_assisted": Fraction((0, 1, 24)[phase_index]),
                        "phase_timing_reliable": True,
                        "completion": "complete",
                        "correct": True,
                        "error_codes": (),
                        "route_adherent": True,
                        "prior_familiarity": "same_structure_seen",
                        "provenance": "synthetic clustered diagnostic fixture",
                    }
                    observations.extend(
                        (
                            MicroToolObservation(
                                observation_id=(
                                    f"{participant_id}-{pair.pair_id}-direct"
                                ),
                                trial_order=2 * family_index + 1,
                                variant_id=direct_variant,
                                assigned_route="direct",
                                card_available=False,
                                interpretation_seconds=Fraction(10),
                                setup_seconds=Fraction(20),
                                computation_seconds=Fraction(60),
                                return_seconds=Fraction(10),
                                independent_total_seconds=Fraction(100),
                                **common,
                            ),
                            MicroToolObservation(
                                observation_id=(
                                    f"{participant_id}-{pair.pair_id}-operator"
                                ),
                                trial_order=2 * family_index + 2,
                                variant_id=operator_variant,
                                assigned_route=pair.operator_route,
                                card_available=phase == "assisted",
                                interpretation_seconds=Fraction(10),
                                setup_seconds=Fraction(20),
                                computation_seconds=Fraction(60 + delta),
                                return_seconds=Fraction(10),
                                independent_total_seconds=Fraction(100 + delta),
                                **common,
                            ),
                        )
                    )
        return tuple(observations)

    def _load(self, rows, tasks):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "route-key.tsv"
            lines = ["\t".join(ROUTE_KEY_REVIEW_COLUMNS)]
            lines.extend(
                "\t".join(row[column] for column in ROUTE_KEY_REVIEW_COLUMNS)
                for row in rows
            )
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return load_route_key_review_tsv(path, tasks)

    def _load_reviewers(self, rows, tasks):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "reviewers.tsv"
            lines = ["\t".join(ROUTE_KEY_REVIEWER_COLUMNS)]
            lines.extend(
                "\t".join(row[column] for column in ROUTE_KEY_REVIEWER_COLUMNS)
                for row in rows
            )
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return load_route_key_reviewer_tsv(path, build_recognition_schedules(tasks))


if __name__ == "__main__":
    unittest.main()
