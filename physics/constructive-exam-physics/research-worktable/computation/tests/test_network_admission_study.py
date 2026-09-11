import csv
import tempfile
import unittest
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

from occ.network_admission import (
    NETWORK_ADMISSION_COLUMNS,
    NETWORK_ADMISSION_PHASES,
    NetworkAdmissionReview,
    build_network_admission_schedules,
    construct_network_admission_key,
)
from occ.network_admission_analysis import (
    audit_network_admission_key,
    construct_network_admission_diagnostics,
    validate_disjoint_network_cohorts,
)
from occ.network_admission_io import (
    load_network_admission_observation_tsv,
    load_network_admission_review_tsv,
)
from worktable.network_admission_cases import build_network_admission_tasks


ROOT = Path(__file__).parents[2]
OBSERVATION_TEMPLATE = ROOT / "observations" / "n2-network-admission-template.tsv"
REVIEW_TEMPLATE = ROOT / "observations" / "n2-network-admission-review-template.tsv"
BOOKLET = ROOT / "observations" / "n2-network-admission-booklet.md"
ANSWER_KEY = ROOT / "observations" / "n2-network-admission-answer-key.md"


class NetworkAdmissionStudyTests(unittest.TestCase):
    def test_three_phases_each_balance_gate_candidate_and_refusal(self):
        tasks = build_network_admission_tasks()

        self.assertEqual(len(tasks), 9)
        self.assertEqual(
            Counter(task.phase for task in tasks),
            {
                "immediate_unassisted": 3,
                "delayed_same_topology": 3,
                "unseen_topology": 3,
            },
        )
        for phase in NETWORK_ADMISSION_PHASES:
            keys = [
                construct_network_admission_key(task).expected_decision
                for task in tasks
                if task.phase == phase
            ]
            self.assertEqual(
                Counter(keys),
                {
                    "direct_gate": 1,
                    "conditional_candidate": 1,
                    "refuse": 1,
                },
            )

    def test_key_is_constructed_from_cost_boundary_or_typed_obstruction(self):
        keys = tuple(
            construct_network_admission_key(task)
            for task in build_network_admission_tasks()
        )

        self.assertTrue(all(item.status == "constructed" for item in keys))
        self.assertEqual(
            Counter(item.expected_decision for item in keys),
            {
                "direct_gate": 3,
                "conditional_candidate": 3,
                "refuse": 3,
            },
        )
        for item in keys:
            self.assertTrue(
                all(certificate.passed for certificate in item.certificates)
            )
            if item.expected_decision == "conditional_candidate":
                self.assertIn("w_representation_changes", item.decision_witness)
            if item.expected_decision == "refuse":
                self.assertTrue(item.obstruction_code)

    def test_two_sequences_reverse_order_inside_every_phase(self):
        tasks = build_network_admission_tasks()
        schedules = build_network_admission_schedules(tasks)

        self.assertEqual({item.sequence_id for item in schedules}, {"A1", "A2"})
        for schedule in schedules:
            self.assertEqual(len(schedule.trials), 9)
            for phase in NETWORK_ADMISSION_PHASES:
                self.assertEqual(
                    sum(item.phase == phase for item in schedule.trials), 3
                )
        for phase in NETWORK_ADMISSION_PHASES:
            first = [
                item.task_id for item in schedules[0].trials if item.phase == phase
            ]
            second = [
                item.task_id for item in schedules[1].trials if item.phase == phase
            ]
            self.assertEqual(second, list(reversed(first)))

    def test_empty_templates_preserve_external_evidence_boundary(self):
        tasks = build_network_admission_tasks()
        schedules = build_network_admission_schedules(tasks)
        observations = load_network_admission_observation_tsv(
            OBSERVATION_TEMPLATE, tasks, schedules
        )
        reviews = load_network_admission_review_tsv(REVIEW_TEMPLATE, tasks)

        diagnostics = construct_network_admission_diagnostics(observations, tasks)
        audit = audit_network_admission_key(reviews, tasks)

        self.assertEqual(observations, ())
        self.assertEqual(reviews, ())
        self.assertEqual(diagnostics.status, "unobserved")
        self.assertEqual(diagnostics.recognition_disposition, "not_evaluated")
        self.assertEqual(diagnostics.retention_disposition, "not_evaluated")
        self.assertEqual(diagnostics.transfer_disposition, "not_evaluated")
        self.assertEqual(audit.status, "additional_review_required")

    def test_loader_restores_task_key_and_refuses_assignment_tampering(self):
        tasks = build_network_admission_tasks()
        schedules = build_network_admission_schedules(tasks)
        trial = schedules[0].trials[0]
        key = construct_network_admission_key(self._task(tasks, trial.task_id))
        row = self._valid_row(schedules[0].sequence_id, trial, key.expected_decision)

        observation = self._load_rows((row,), tasks, schedules)[0]

        self.assertTrue(observation.correct)
        self.assertEqual(observation.expected_decision, key.expected_decision)
        self.assertEqual(observation.decision_seconds, 12)
        wrong = dict(
            row,
            selected_decision="refuse"
            if key.expected_decision != "refuse"
            else "direct_gate",
        )
        self.assertFalse(self._load_rows((wrong,), tasks, schedules)[0].correct)
        with self.assertRaisesRegex(ValueError, "frozen schedule"):
            self._load_rows((dict(row, task_id="not-the-task"),), tasks, schedules)

    def test_delay_session_and_choice_vocabulary_are_enforced(self):
        tasks = build_network_admission_tasks()
        schedules = build_network_admission_schedules(tasks)
        delayed = next(
            item
            for item in schedules[0].trials
            if item.phase == "delayed_same_topology"
        )
        key = construct_network_admission_key(self._task(tasks, delayed.task_id))
        row = self._valid_row("A1", delayed, key.expected_decision)

        with self.assertRaisesRegex(ValueError, "positive delay"):
            self._load_rows((dict(row, hours_since_training="0"),), tasks, schedules)
        with self.assertRaisesRegex(ValueError, "selected decision"):
            self._load_rows(
                (dict(row, selected_decision="always_sparse"),), tasks, schedules
            )

    def test_diagnostics_cluster_complete_three_class_sets_by_participant(self):
        tasks = build_network_admission_tasks()
        schedules = build_network_admission_schedules(tasks)
        observations = []
        for participant_index, participant_id in enumerate(("p1", "p2")):
            schedule = schedules[participant_index]
            for trial in schedule.trials:
                key = construct_network_admission_key(self._task(tasks, trial.task_id))
                observations.append(
                    self._observation(
                        participant_id,
                        schedule.sequence_id,
                        trial,
                        key.expected_decision,
                    )
                )

        diagnostics = construct_network_admission_diagnostics(
            tuple(observations), tasks
        )

        self.assertEqual(diagnostics.status, "design_inputs_observed")
        for phase in diagnostics.phases:
            self.assertEqual(phase.complete_participant_clusters, 2)
            self.assertEqual(phase.mean_participant_accuracy, 1)
            self.assertEqual(phase.mean_participant_decision_seconds, 12)
        self.assertEqual(diagnostics.recognition_disposition, "not_evaluated")

        observations[0] = replace(observations[0], selected_decision="refuse")
        degraded = construct_network_admission_diagnostics(tuple(observations), tasks)
        self.assertEqual(degraded.phases[0].mean_participant_accuracy, Fraction(5, 6))

    def test_two_blinded_reviews_are_required_and_disputes_take_precedence(self):
        tasks = build_network_admission_tasks()
        reviews = tuple(
            NetworkAdmissionReview(
                review_id=f"{reviewer}-{task.task_id}",
                reviewer_id=reviewer,
                task_id=task.task_id,
                declared_expertise="graduate classical physics instruction",
                independently_classified=True,
                blinded_to_authored_key=True,
                blinded_to_peer_reviews=True,
                expected_decision_agrees=True,
                prompt_unambiguous=True,
                notes="independent fixture",
                provenance="synthetic schema fixture, not expert evidence",
            )
            for reviewer in ("r1", "r2")
            for task in tasks
        )

        self.assertEqual(
            audit_network_admission_key(reviews, tasks).status, "ready_for_pilot"
        )
        disputed = replace(reviews[0], prompt_unambiguous=False)
        self.assertEqual(
            audit_network_admission_key((disputed, *reviews[1:]), tasks).status,
            "revision_required",
        )
        unidentified = replace(reviews[0], reviewer_id="")
        self.assertEqual(
            audit_network_admission_key((unidentified, *reviews[1:]), tasks).status,
            "additional_review_required",
        )

    def test_recognition_and_execution_cohorts_must_be_disjoint(self):
        tasks = build_network_admission_tasks()
        schedule = build_network_admission_schedules(tasks)[0]
        trial = schedule.trials[0]
        key = construct_network_admission_key(self._task(tasks, trial.task_id))
        recognition = (self._observation("shared", "A1", trial, key.expected_decision),)

        with self.assertRaisesRegex(ValueError, "disjoint"):
            validate_disjoint_network_cohorts(
                recognition, (SimpleNamespace(participant_id="shared"),)
            )

    def test_booklet_contains_tasks_without_expected_decision_mapping(self):
        tasks = build_network_admission_tasks()
        booklet = BOOKLET.read_text(encoding="utf-8")
        key = ANSWER_KEY.read_text(encoding="utf-8")

        for task in tasks:
            self.assertIn(f"### {task.task_id}", booklet)
            self.assertIn(f"### {task.task_id}", key)
        self.assertNotIn("Expected decision:", booklet)
        self.assertEqual(key.count("Expected decision:"), 9)

    @staticmethod
    def _task(tasks, task_id):
        return next(item for item in tasks if item.task_id == task_id)

    def _valid_row(self, sequence_id, trial, selected):
        delay = {
            "immediate_unassisted": 0,
            "delayed_same_topology": 24,
            "unseen_topology": 48,
        }[trial.phase]
        return {
            "observation_id": f"obs-{sequence_id}-{trial.order}",
            "participant_id": "p1",
            "session_id": f"p1-{trial.phase}",
            "sequence_id": sequence_id,
            "trial_order": str(trial.order),
            "phase": trial.phase,
            "task_id": trial.task_id,
            "selected_decision": selected,
            "decision_seconds": "12",
            "hours_since_training": str(delay),
            "completion": "complete",
            "justification": "active-neighbor and pivot check",
            "provenance": "synthetic loader fixture",
        }

    def _load_rows(self, rows, tasks, schedules):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.tsv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=NETWORK_ADMISSION_COLUMNS, delimiter="\t"
                )
                writer.writeheader()
                writer.writerows(rows)
            return load_network_admission_observation_tsv(path, tasks, schedules)

    @staticmethod
    def _observation(participant_id, sequence_id, trial, selected):
        from occ.network_admission import NetworkAdmissionObservation

        expected = construct_network_admission_key(
            NetworkAdmissionStudyTests._task(
                build_network_admission_tasks(), trial.task_id
            )
        ).expected_decision
        delay = {
            "immediate_unassisted": 0,
            "delayed_same_topology": 24,
            "unseen_topology": 48,
        }[trial.phase]
        return NetworkAdmissionObservation(
            observation_id=f"{participant_id}-{trial.order}",
            participant_id=participant_id,
            session_id=f"{participant_id}-{trial.phase}",
            sequence_id=sequence_id,
            trial_order=trial.order,
            phase=trial.phase,
            task_id=trial.task_id,
            selected_decision=selected,
            expected_decision=expected,
            decision_seconds=Fraction(12),
            hours_since_training=Fraction(delay),
            completion="complete",
            justification="active-neighbor and pivot check",
            provenance="synthetic clustered fixture",
        )


if __name__ == "__main__":
    unittest.main()
