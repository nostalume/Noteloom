import csv
import tempfile
import unittest
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

from occ.network_study import (
    NETWORK_STUDY_COLUMNS,
    NETWORK_STUDY_PHASES,
    NetworkStudyReview,
    build_network_study_schedules,
    solve_network_study_variant,
)
from occ.network_study_analysis import (
    audit_network_study_key,
    construct_network_study_diagnostics,
)
from occ.network_study_io import (
    load_network_study_observation_tsv,
    load_network_study_review_tsv,
)
from worktable.network_study_cases import build_network_study_pairs


ROOT = Path(__file__).parents[2]
OBSERVATION_TEMPLATE = ROOT / "observations" / "n1-network-study-template.tsv"
REVIEW_TEMPLATE = ROOT / "observations" / "n1-network-key-review-template.tsv"
BOOKLET = ROOT / "observations" / "n1-network-study-booklet.md"
ANSWER_KEY = ROOT / "observations" / "n1-network-study-answer-key.md"


class NetworkStudyTests(unittest.TestCase):
    def test_frozen_bench_separates_retention_from_unseen_transfer(self):
        pairs = build_network_study_pairs()

        self.assertEqual(len(pairs), 6)
        self.assertEqual(
            Counter(pair.phase for pair in pairs),
            Counter(
                {
                    "immediate_assisted": 2,
                    "delayed_same_topology": 2,
                    "unseen_topology": 2,
                }
            ),
        )
        immediate = {
            pair.topology_family for pair in pairs if pair.phase == "immediate_assisted"
        }
        delayed = {
            pair.topology_family
            for pair in pairs
            if pair.phase == "delayed_same_topology"
        }
        unseen = {
            pair.topology_family for pair in pairs if pair.phase == "unseen_topology"
        }
        self.assertEqual(immediate, delayed)
        self.assertTrue(unseen.isdisjoint(immediate))

    def test_every_variant_has_an_exact_route_independent_answer_key(self):
        pairs = build_network_study_pairs()
        answers = []

        for pair in pairs:
            for variant in (pair.variant_a, pair.variant_b):
                answer = solve_network_study_variant(variant)
                self.assertEqual(answer.status, "constructed")
                self.assertEqual(answer.structural_disposition, "conditional")
                self.assertTrue(all(item.passed for item in answer.certificates))
                self.assertEqual(
                    answer.declared_plan.condensed_matrix,
                    answer.sparse_plan.condensed_matrix,
                )
                self.assertEqual(
                    answer.declared_plan.condensed_source,
                    answer.sparse_plan.condensed_source,
                )
                answers.append(answer.target_value)

        self.assertEqual(len(answers), 12)
        self.assertEqual(answers[0], Fraction(2, 3))

    def test_two_schedules_counterbalance_route_variant_inside_each_phase(self):
        pairs = build_network_study_pairs()
        schedules = build_network_study_schedules(pairs)

        self.assertEqual({item.sequence_id for item in schedules}, {"N1", "N2"})
        for schedule in schedules:
            self.assertEqual(len(schedule.trials), 12)
            for phase in NETWORK_STUDY_PHASES:
                trials = [item for item in schedule.trials if item.phase == phase]
                self.assertEqual(
                    Counter(item.assigned_route for item in trials),
                    {
                        "direct": 2,
                        "sparse": 2,
                    },
                )
            for pair in pairs:
                trials = [
                    item for item in schedule.trials if item.pair_id == pair.pair_id
                ]
                self.assertEqual(
                    {item.variant_id for item in trials},
                    {
                        pair.variant_a.variant_id,
                        pair.variant_b.variant_id,
                    },
                )
                self.assertEqual(
                    {item.assigned_route for item in trials},
                    {
                        "direct",
                        "sparse",
                    },
                )

        assignment = {
            (schedule.sequence_id, trial.variant_id): trial.assigned_route
            for schedule in schedules
            for trial in schedule.trials
        }
        for pair in pairs:
            for variant in (pair.variant_a, pair.variant_b):
                self.assertNotEqual(
                    assignment[("N1", variant.variant_id)],
                    assignment[("N2", variant.variant_id)],
                )

    def test_empty_templates_preserve_unobserved_and_unreviewed_boundaries(self):
        pairs = build_network_study_pairs()
        schedules = build_network_study_schedules(pairs)

        observations = load_network_study_observation_tsv(
            OBSERVATION_TEMPLATE, pairs, schedules
        )
        reviews = load_network_study_review_tsv(REVIEW_TEMPLATE, pairs)
        diagnostics = construct_network_study_diagnostics(observations, pairs)
        audit = audit_network_study_key(reviews, pairs)

        self.assertEqual(observations, ())
        self.assertEqual(reviews, ())
        self.assertEqual(diagnostics.status, "unobserved")
        self.assertEqual(diagnostics.speed_disposition, "not_evaluated")
        self.assertEqual(diagnostics.retention_disposition, "not_evaluated")
        self.assertEqual(diagnostics.transfer_disposition, "not_evaluated")
        self.assertEqual(audit.status, "additional_review_required")
        self.assertEqual(audit.reviewed_variants, 0)

    def test_loader_restores_schedule_and_scores_against_exact_key(self):
        pairs = build_network_study_pairs()
        schedules = build_network_study_schedules(pairs)
        trial = schedules[0].trials[0]
        variant = self._variant(pairs, trial.variant_id)
        answer = solve_network_study_variant(variant)
        row = self._valid_row(schedules[0].sequence_id, trial, answer.target_value)

        observations = self._load_rows((row,), pairs, schedules)

        self.assertEqual(len(observations), 1)
        self.assertTrue(observations[0].correct)
        self.assertEqual(observations[0].total_seconds, 100)
        self.assertIn(variant.provenance, observations[0].provenance)

        wrong = dict(row, submitted_answer="999")
        self.assertFalse(self._load_rows((wrong,), pairs, schedules)[0].correct)
        tampered = dict(
            row,
            assigned_route="sparse" if trial.assigned_route == "direct" else "direct",
        )
        with self.assertRaisesRegex(ValueError, "frozen schedule"):
            self._load_rows((tampered,), pairs, schedules)

    def test_delay_card_and_timing_consistency_are_enforced(self):
        pairs = build_network_study_pairs()
        schedules = build_network_study_schedules(pairs)
        schedule = schedules[0]
        delayed = next(
            item for item in schedule.trials if item.phase == "delayed_same_topology"
        )
        answer = solve_network_study_variant(self._variant(pairs, delayed.variant_id))
        row = self._valid_row(schedule.sequence_id, delayed, answer.target_value)

        with self.assertRaisesRegex(ValueError, "positive delay"):
            self._load_rows((dict(row, hours_since_immediate="0"),), pairs, schedules)
        with self.assertRaisesRegex(ValueError, "card visibility"):
            self._load_rows((dict(row, strip_available="true"),), pairs, schedules)
        with self.assertRaisesRegex(ValueError, "phase times"):
            self._load_rows((dict(row, computation_seconds="71"),), pairs, schedules)

    def test_timing_requires_complete_correct_adherent_participant_clusters(self):
        pairs = build_network_study_pairs()
        observations = []
        for participant_index, participant_id in enumerate(("p1", "p2")):
            schedule = build_network_study_schedules(pairs)[participant_index]
            for trial in schedule.trials:
                variant = self._variant(pairs, trial.variant_id)
                answer = solve_network_study_variant(variant)
                total = 90 if trial.assigned_route == "sparse" else 100
                observations.append(
                    self._observation(
                        participant_id,
                        schedule.sequence_id,
                        trial,
                        answer.target_value,
                        total,
                    )
                )

        diagnostics = construct_network_study_diagnostics(tuple(observations), pairs)

        self.assertEqual(diagnostics.status, "design_inputs_observed")
        for phase in diagnostics.phases:
            self.assertEqual(phase.complete_participant_clusters, 2)
            self.assertEqual(phase.mean_cluster_time_delta, -10)
            self.assertEqual(phase.sample_variance_cluster_time_delta, 0)
        self.assertEqual(diagnostics.speed_disposition, "not_evaluated")

        observations[0] = replace(observations[0], submitted_answer=999)
        degraded = construct_network_study_diagnostics(tuple(observations), pairs)
        self.assertEqual(degraded.phases[0].complete_participant_clusters, 1)
        self.assertIsNone(degraded.phases[0].sample_variance_cluster_time_delta)

    def test_two_blinded_independent_reviews_are_required_per_variant(self):
        pairs = build_network_study_pairs()
        variants = [
            variant for pair in pairs for variant in (pair.variant_a, pair.variant_b)
        ]
        reviews = tuple(
            NetworkStudyReview(
                review_id=f"{reviewer}-{variant.variant_id}",
                reviewer_id=reviewer,
                variant_id=variant.variant_id,
                declared_expertise="graduate classical physics instruction",
                independently_solved=True,
                blinded_to_authored_routes=True,
                blinded_to_peer_reviews=True,
                exact_answer_agrees=True,
                direct_route_valid=True,
                sparse_route_valid=True,
                baseline_competent=True,
                notes="independent reconstruction",
                provenance="synthetic schema fixture, not expert evidence",
            )
            for reviewer in ("r1", "r2")
            for variant in variants
        )

        self.assertEqual(
            audit_network_study_key(reviews, pairs).status, "ready_for_pilot"
        )
        disputed = replace(reviews[0], baseline_competent=False)
        self.assertEqual(
            audit_network_study_key((disputed, *reviews[1:]), pairs).status,
            "revision_required",
        )
        unidentified = replace(reviews[0], reviewer_id="")
        self.assertEqual(
            audit_network_study_key((unidentified, *reviews[1:]), pairs).status,
            "additional_review_required",
        )

    def test_booklet_exposes_schedules_but_not_answer_values(self):
        pairs = build_network_study_pairs()
        schedules = build_network_study_schedules(pairs)
        booklet = BOOKLET.read_text(encoding="utf-8")
        key = ANSWER_KEY.read_text(encoding="utf-8")

        for schedule in schedules:
            self.assertIn(f"## Sequence {schedule.sequence_id}", booklet)
            for trial in schedule.trials:
                self.assertIn(
                    f"| {trial.order} | {trial.phase} | {trial.variant_id} | "
                    f"{trial.assigned_route} |",
                    booklet,
                )
        self.assertNotIn("Exact answer:", booklet)
        self.assertEqual(key.count("Exact answer:"), 12)
        for pair in pairs:
            for variant in (pair.variant_a, pair.variant_b):
                answer = solve_network_study_variant(variant)
                self.assertIn(f"Exact answer: `{answer.target_value}", key)

    @staticmethod
    def _variant(pairs, variant_id):
        return next(
            variant
            for pair in pairs
            for variant in (pair.variant_a, pair.variant_b)
            if variant.variant_id == variant_id
        )

    def _valid_row(self, sequence_id, trial, answer):
        strip = trial.phase == "immediate_assisted" and trial.assigned_route == "sparse"
        return {
            "observation_id": f"obs-{sequence_id}-{trial.order}",
            "participant_id": "p1",
            "session_id": f"p1-{trial.phase}",
            "sequence_id": sequence_id,
            "trial_order": str(trial.order),
            "phase": trial.phase,
            "pair_id": trial.pair_id,
            "variant_id": trial.variant_id,
            "assigned_route": trial.assigned_route,
            "strip_available": str(strip).lower(),
            "hours_since_immediate": "0"
            if trial.phase == "immediate_assisted"
            else "24",
            "interpretation_seconds": "10",
            "setup_seconds": "20",
            "computation_seconds": "60",
            "return_seconds": "10",
            "independent_total_seconds": "100",
            "phase_timing_reliable": "true",
            "completion": "complete",
            "submitted_answer": str(answer),
            "error_codes": "",
            "route_adherent": "true",
            "prior_familiarity": "unseen",
            "provenance": "synthetic loader fixture",
        }

    def _load_rows(self, rows, pairs, schedules):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.tsv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=NETWORK_STUDY_COLUMNS, delimiter="\t"
                )
                writer.writeheader()
                writer.writerows(rows)
            return load_network_study_observation_tsv(path, pairs, schedules)

    def _observation(self, participant_id, sequence_id, trial, answer, total):
        from occ.network_study import NetworkStudyObservation

        return NetworkStudyObservation(
            observation_id=f"{participant_id}-{trial.order}",
            participant_id=participant_id,
            session_id=f"{participant_id}-{trial.phase}",
            sequence_id=sequence_id,
            trial_order=trial.order,
            phase=trial.phase,
            pair_id=trial.pair_id,
            variant_id=trial.variant_id,
            assigned_route=trial.assigned_route,
            strip_available=trial.phase == "immediate_assisted"
            and trial.assigned_route == "sparse",
            hours_since_immediate=Fraction(
                0 if trial.phase == "immediate_assisted" else 24
            ),
            interpretation_seconds=Fraction(10),
            setup_seconds=Fraction(20),
            computation_seconds=Fraction(total - 40),
            return_seconds=Fraction(10),
            independent_total_seconds=Fraction(total),
            phase_timing_reliable=True,
            completion="complete",
            submitted_answer=answer,
            expected_answer=answer,
            error_codes=(),
            route_adherent=True,
            prior_familiarity="unseen",
            provenance="synthetic clustered fixture",
        )


if __name__ == "__main__":
    unittest.main()
