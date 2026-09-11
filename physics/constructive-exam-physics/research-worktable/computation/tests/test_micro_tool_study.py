from collections import Counter
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from occ.micro_study import (
    MICRO_OBSERVATION_COLUMNS,
    RECOGNITION_OBSERVATION_COLUMNS,
    build_micro_tool_schedules,
    build_recognition_schedules,
    construct_micro_tool_outcomes,
    load_micro_tool_observation_tsv,
    load_route_recognition_observation_tsv,
    validate_disjoint_micro_tool_cohorts,
)
from worktable.micro_study_cases import (
    build_micro_tool_pairs,
    build_route_recognition_tasks,
)


TEMPLATE = (
    Path(__file__).parents[2]
    / "observations"
    / "d3-micro-tool-observation-template.tsv"
)
RECOGNITION_TEMPLATE = (
    Path(__file__).parents[2]
    / "observations"
    / "d3-route-recognition-observation-template.tsv"
)
EXECUTION_BOOKLET = TEMPLATE.with_name("d3-micro-tool-booklet.md")
RECOGNITION_BOOKLET = TEMPLATE.with_name("d3-route-recognition-booklet.md")


class MicroToolStudyTests(unittest.TestCase):
    def test_twelve_pairs_cover_four_families_and_three_phases(self):
        pairs = build_micro_tool_pairs()

        self.assertEqual(len(pairs), 12)
        self.assertEqual(
            Counter(pair.phase for pair in pairs),
            {"assisted": 4, "internalized": 4, "delayed_unseen": 4},
        )
        self.assertEqual(
            {pair.operator_route for pair in pairs},
            {"slice", "projection", "path", "product"},
        )
        variant_ids = [
            variant.variant_id
            for pair in pairs
            for variant in (pair.variant_a, pair.variant_b)
        ]
        self.assertEqual(len(variant_ids), 24)
        self.assertEqual(len(variant_ids), len(set(variant_ids)))
        self.assertTrue(all(pair.provenance for pair in pairs))

    def test_authored_variants_have_exact_expected_returns(self):
        pairs = {pair.pair_id: pair for pair in build_micro_tool_pairs()}

        jet = pairs["assisted-jet"]
        self.assertEqual(jet.variant_a.answer("impact_speed"), 6)
        self.assertEqual(jet.variant_a.answer("height"), Fraction(16, 5))
        impact = pairs["assisted-impact"]
        self.assertEqual(impact.variant_a.answer("outgoing_normal"), 2)
        self.assertEqual(impact.variant_a.answer("outgoing_tangent"), 0)
        path = pairs["assisted-path"]
        self.assertEqual(path.variant_a.answer("straight_work"), 0)
        self.assertEqual(path.variant_a.answer("broken_work"), Fraction(1, 2))
        product = pairs["assisted-product"]
        self.assertEqual(product.variant_a.answer("mean"), 3)
        self.assertEqual(product.variant_a.answer("ripple_real"), 3)
        self.assertEqual(product.variant_a.answer("ripple_imag"), 4)

    def test_two_schedules_counterbalance_each_phase_and_variant(self):
        pairs = build_micro_tool_pairs()
        schedules = build_micro_tool_schedules(pairs)

        self.assertEqual({schedule.sequence_id for schedule in schedules}, {"M1", "M2"})
        for schedule in schedules:
            self.assertEqual(len(schedule.trials), 24)
            for phase in ("assisted", "internalized", "delayed_unseen"):
                trials = [trial for trial in schedule.trials if trial.phase == phase]
                self.assertEqual(len(trials), 8)
                self.assertEqual(
                    Counter(trial.assigned_route for trial in trials),
                    {"direct": 4, "slice": 1, "projection": 1, "path": 1, "product": 1},
                )
            for pair in pairs:
                trials = [
                    trial for trial in schedule.trials if trial.pair_id == pair.pair_id
                ]
                self.assertEqual(
                    Counter(trial.assigned_route for trial in trials),
                    {"direct": 1, pair.operator_route: 1},
                )
                self.assertEqual(abs(trials[0].order - trials[1].order), 4)

        for pair in pairs:
            assignments = Counter(
                (trial.assigned_route, trial.variant_id)
                for schedule in schedules
                for trial in schedule.trials
                if trial.pair_id == pair.pair_id
            )
            self.assertEqual(
                assignments,
                {
                    ("direct", pair.variant_a.variant_id): 1,
                    ("direct", pair.variant_b.variant_id): 1,
                    (pair.operator_route, pair.variant_a.variant_id): 1,
                    (pair.operator_route, pair.variant_b.variant_id): 1,
                },
            )

    def test_empty_template_preserves_zero_empirical_rows(self):
        observations = load_micro_tool_observation_tsv(
            TEMPLATE,
            build_micro_tool_pairs(),
            build_micro_tool_schedules(build_micro_tool_pairs()),
        )

        self.assertEqual(observations, ())

    def test_valid_execution_row_restores_schedule_without_diagnosis_priming(self):
        pairs = build_micro_tool_pairs()
        schedules = build_micro_tool_schedules(pairs)
        schedule = schedules[0]
        trial = schedule.trials[0]
        pair = next(pair for pair in pairs if pair.pair_id == trial.pair_id)
        row = self._valid_row(schedule.sequence_id, trial)

        observations = self._load_rows((row,), pairs, schedules)

        self.assertEqual(len(observations), 1)
        observation = observations[0]
        self.assertEqual(observation.total_seconds, Fraction(100))
        self.assertEqual(observation.hours_since_assisted, Fraction(0))
        self.assertTrue(observation.phase_timing_reliable)
        self.assertEqual(observation.phase, trial.phase)
        self.assertEqual(observation.assigned_route, trial.assigned_route)
        self.assertIn(pair.provenance, observation.provenance)

    def test_loader_rejects_assignment_tampering_and_unresolved_correct_error(self):
        pairs = build_micro_tool_pairs()
        schedules = build_micro_tool_schedules(pairs)
        schedule = schedules[0]
        trial = schedule.trials[0]
        tampered = self._valid_row(schedule.sequence_id, trial)
        tampered["assigned_route"] = "path"
        with self.assertRaisesRegex(ValueError, "frozen schedule"):
            self._load_rows((tampered,), pairs, schedules)

        invalid_error = self._valid_row(schedule.sequence_id, trial)
        invalid_error["error_codes"] = "sign"
        with self.assertRaisesRegex(ValueError, "correct attempt"):
            self._load_rows((invalid_error,), pairs, schedules)

    def test_independent_total_and_delay_are_observed_not_reconstructed(self):
        pairs = build_micro_tool_pairs()
        schedules = build_micro_tool_schedules(pairs)
        schedule = schedules[0]
        assisted = next(trial for trial in schedule.trials if trial.phase == "assisted")
        delayed = next(
            trial for trial in schedule.trials if trial.phase == "delayed_unseen"
        )

        mismatched = self._valid_row(schedule.sequence_id, assisted)
        mismatched["independent_total_seconds"] = "101"
        with self.assertRaisesRegex(ValueError, "independent total"):
            self._load_rows((mismatched,), pairs, schedules)

        unreliable = mismatched.copy()
        unreliable["phase_timing_reliable"] = "false"
        observation = self._load_rows((unreliable,), pairs, schedules)[0]
        self.assertEqual(observation.total_seconds, Fraction(101))
        self.assertFalse(observation.phase_timing_reliable)

        zero_delay = self._valid_row(schedule.sequence_id, delayed)
        zero_delay["hours_since_assisted"] = "0"
        with self.assertRaisesRegex(ValueError, "delayed-unseen"):
            self._load_rows((zero_delay,), pairs, schedules)

    def test_card_is_visible_only_on_assisted_operator_trials(self):
        pairs = build_micro_tool_pairs()
        schedules = build_micro_tool_schedules(pairs)
        schedule = schedules[0]
        operator_trial = next(
            trial
            for trial in schedule.trials
            if trial.phase == "assisted" and trial.assigned_route != "direct"
        )
        valid = self._valid_row(schedule.sequence_id, operator_trial)
        self.assertEqual(
            len(self._load_rows((valid,), pairs, schedules)),
            1,
        )

        invalid = valid.copy()
        invalid["card_available"] = "false"
        with self.assertRaisesRegex(ValueError, "card visibility"):
            self._load_rows((invalid,), pairs, schedules)

    def test_phase_session_and_delay_metadata_are_relationally_consistent(self):
        pairs = build_micro_tool_pairs()
        schedules = build_micro_tool_schedules(pairs)
        schedule = schedules[0]
        assisted = [trial for trial in schedule.trials if trial.phase == "assisted"]
        internalized = [
            trial for trial in schedule.trials if trial.phase == "internalized"
        ]
        delayed = next(
            trial for trial in schedule.trials if trial.phase == "delayed_unseen"
        )

        split_session = [
            self._valid_row(schedule.sequence_id, assisted[0]),
            self._valid_row(schedule.sequence_id, assisted[1]),
        ]
        split_session[1]["session_id"] = "another-assisted-session"
        with self.assertRaisesRegex(ValueError, "one session per phase"):
            self._load_rows(tuple(split_session), pairs, schedules)

        mixed_delay = [
            self._valid_row(schedule.sequence_id, internalized[0]),
            self._valid_row(schedule.sequence_id, internalized[1]),
        ]
        mixed_delay[1]["hours_since_assisted"] = "2"
        with self.assertRaisesRegex(ValueError, "one delay per phase"):
            self._load_rows(tuple(mixed_delay), pairs, schedules)

        reversed_time = [
            self._valid_row(schedule.sequence_id, internalized[0]),
            self._valid_row(schedule.sequence_id, delayed),
        ]
        reversed_time[0]["hours_since_assisted"] = "200"
        with self.assertRaisesRegex(ValueError, "later than internalized"):
            self._load_rows(tuple(reversed_time), pairs, schedules)

    def test_pair_outcome_requires_two_correct_adherent_routes(self):
        pairs = build_micro_tool_pairs()
        schedules = build_micro_tool_schedules(pairs)
        schedule = schedules[0]
        pair = next(pair for pair in pairs if pair.pair_id == "assisted-jet")
        trials = [trial for trial in schedule.trials if trial.pair_id == pair.pair_id]
        rows = tuple(self._valid_row(schedule.sequence_id, trial) for trial in trials)
        operator_row = next(row for row in rows if row["assigned_route"] != "direct")
        operator_row["computation_seconds"] = "30"
        operator_row["independent_total_seconds"] = "85"
        observations = self._load_rows(rows, pairs, schedules)

        outcomes = construct_micro_tool_outcomes(observations, pairs)

        self.assertEqual(len(outcomes), 1)
        self.assertEqual(outcomes[0].status, "eligible")
        self.assertEqual(outcomes[0].time_delta, Fraction(-15))

        incorrect_rows = tuple(row.copy() for row in rows)
        next(row for row in incorrect_rows if row["assigned_route"] != "direct")[
            "correct"
        ] = "false"
        ineligible = construct_micro_tool_outcomes(
            self._load_rows(incorrect_rows, pairs, schedules),
            pairs,
        )
        self.assertEqual(ineligible[0].status, "ineligible")
        self.assertEqual(ineligible[0].reason, "incorrect_or_incomplete")

    def test_recognition_instrument_includes_direct_and_refusal_decoys(self):
        tasks = build_route_recognition_tasks()
        schedules = build_recognition_schedules(tasks)

        self.assertEqual(len(tasks), 12)
        routes = {task.expected_route for task in tasks}
        self.assertIn("direct", routes)
        self.assertIn("refuse-card", routes)
        self.assertEqual({schedule.sequence_id for schedule in schedules}, {"R1", "R2"})
        self.assertTrue(all(len(schedule.task_ids) == 12 for schedule in schedules))
        self.assertEqual(
            load_route_recognition_observation_tsv(
                RECOGNITION_TEMPLATE,
                tasks,
                schedules,
            ),
            (),
        )

    def test_recognition_row_derives_correctness_from_frozen_task(self):
        tasks = build_route_recognition_tasks()
        schedules = build_recognition_schedules(tasks)
        task_by_id = {task.task_id: task for task in tasks}
        schedule = schedules[0]
        task_id = schedule.task_ids[0]
        task = task_by_id[task_id]
        row = {
            "observation_id": "recognition-001",
            "participant_id": "learner-001",
            "session_id": "recognition-session",
            "sequence_id": schedule.sequence_id,
            "task_order": "1",
            "task_id": task_id,
            "selected_route": task.expected_route,
            "decision_seconds": "12",
            "provenance": "closed-book recognition fixture",
        }
        with TemporaryDirectory() as directory:
            path = Path(directory) / "recognition.tsv"
            path.write_text(
                "\t".join(RECOGNITION_OBSERVATION_COLUMNS)
                + "\n"
                + "\t".join(row[column] for column in RECOGNITION_OBSERVATION_COLUMNS)
                + "\n",
                encoding="utf-8",
            )
            observations = load_route_recognition_observation_tsv(
                path,
                tasks,
                schedules,
            )

        self.assertEqual(len(observations), 1)
        self.assertTrue(observations[0].correct)
        self.assertEqual(observations[0].decision_seconds, Fraction(12))

        pairs = build_micro_tool_pairs()
        execution_schedules = build_micro_tool_schedules(pairs)
        execution = self._load_rows(
            (
                self._valid_row(
                    execution_schedules[0].sequence_id,
                    execution_schedules[0].trials[0],
                ),
            ),
            pairs,
            execution_schedules,
        )
        with self.assertRaisesRegex(ValueError, "disjoint cohorts"):
            validate_disjoint_micro_tool_cohorts(observations, execution)

    def test_participant_booklets_match_executable_tasks_and_schedules(self):
        pairs = build_micro_tool_pairs()
        execution_text = EXECUTION_BOOKLET.read_text(encoding="utf-8")
        m1_text = execution_text.split("## Sequence M1", 1)[1].split(
            "## Sequence M2", 1
        )[0]
        m2_text = execution_text.split("## Sequence M2", 1)[1].split(
            "## Jet variants", 1
        )[0]
        sections = {"M1": m1_text, "M2": m2_text}
        for schedule in build_micro_tool_schedules(pairs):
            for trial in schedule.trials:
                expected_row = (
                    f"| {trial.order} | {trial.phase.replace('_', ' ')} | "
                    f"{trial.variant_id} | {trial.assigned_route} |"
                )
                self.assertIn(expected_row, sections[schedule.sequence_id])

        recognition_text = RECOGNITION_BOOKLET.read_text(encoding="utf-8")
        for task in build_route_recognition_tasks():
            self.assertIn(f"| {task.task_id} | {task.prompt} | |", recognition_text)

    def _valid_row(self, sequence_id, trial):
        card_available = trial.phase == "assisted" and trial.assigned_route != "direct"
        return {
            "observation_id": f"obs-{sequence_id}-{trial.order}",
            "participant_id": "learner-001",
            "session_id": f"session-{trial.phase}",
            "sequence_id": sequence_id,
            "trial_order": str(trial.order),
            "phase": trial.phase,
            "pair_id": trial.pair_id,
            "variant_id": trial.variant_id,
            "assigned_route": trial.assigned_route,
            "card_available": str(card_available).lower(),
            "hours_since_assisted": {
                "assisted": "0",
                "internalized": "1",
                "delayed_unseen": "168",
            }[trial.phase],
            "interpretation_seconds": "20",
            "setup_seconds": "25",
            "computation_seconds": "45",
            "return_seconds": "10",
            "independent_total_seconds": "100",
            "phase_timing_reliable": "true",
            "completion": "complete",
            "correct": "true",
            "error_codes": "",
            "route_adherent": "true",
            "prior_familiarity": "same_structure_seen",
            "provenance": "closed-book paper pilot fixture",
        }

    def _load_rows(self, rows, pairs, schedules):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "micro.tsv"
            lines = ["\t".join(MICRO_OBSERVATION_COLUMNS)]
            lines.extend(
                "\t".join(row[column] for column in MICRO_OBSERVATION_COLUMNS)
                for row in rows
            )
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return load_micro_tool_observation_tsv(path, pairs, schedules)


if __name__ == "__main__":
    unittest.main()
