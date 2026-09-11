from collections import Counter
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from sympy import Matrix, Rational, simplify, sqrt, symbols

from occ.cost import COST_AXES
from occ.study import (
    build_two_sequence_schedule,
    load_paired_observation_tsv,
)
from worktable.study_cases import build_matched_variant_pairs


TEMPLATE = Path(__file__).parents[2] / "observations" / "d1-observation-template.tsv"


class MatchedVariantStudyTests(unittest.TestCase):
    def test_six_source_bound_pairs_have_twelve_distinct_variants(self):
        pairs = build_matched_variant_pairs()

        self.assertEqual(len(pairs), 6)
        self.assertEqual(
            {(pair.source_problem_id, pair.pdf_page) for pair in pairs},
            {
                ("A25-03", 4),
                ("A24-09-3", 7),
                ("A22-03-1", 10),
                ("A15-08", 26),
                ("A13-02", 29),
                ("A11-03", 33),
            },
        )
        variant_ids = [
            variant.variant_id
            for pair in pairs
            for variant in (pair.variant_a, pair.variant_b)
        ]
        self.assertEqual(len(variant_ids), len(set(variant_ids)))
        self.assertTrue(all(pair.provenance for pair in pairs))

    def test_variant_answer_keys_preserve_each_physical_relation(self):
        pairs = {pair.source_problem_id: pair for pair in build_matched_variant_pairs()}
        epsilon_0, h, m_n, k_B = symbols("epsilon_0 h m_n k_B", positive=True)

        self.assertEqual(pairs["A25-03"].variant_a.answer("proper_days"), 2 * sqrt(11))
        self.assertEqual(pairs["A25-03"].variant_b.answer("proper_days"), 6 * sqrt(2))
        self.assertEqual(
            pairs["A24-09-3"].variant_a.answer("work_joule"),
            100000 * epsilon_0,
        )
        self.assertEqual(
            pairs["A24-09-3"].variant_b.answer("work_joule"),
            75000 * epsilon_0,
        )
        self.assertEqual(pairs["A22-03-1"].variant_a.answer("acceleration_m_s2"), 64)
        self.assertEqual(pairs["A22-03-1"].variant_b.answer("acceleration_m_s2"), 27)
        wavelength_a = pairs["A15-08"].variant_a.answer("wavelength_m")
        wavelength_b = pairs["A15-08"].variant_b.answer("wavelength_m")
        self.assertEqual(simplify(wavelength_b / wavelength_a), Rational(2, 3))
        self.assertTrue(wavelength_a.has(h, m_n, k_B))
        self.assertEqual(pairs["A13-02"].variant_a.answer("height_m"), Rational(16, 5))
        self.assertEqual(pairs["A13-02"].variant_b.answer("height_m"), Rational(39, 20))
        self.assertEqual(pairs["A11-03"].variant_a.answer("distance_m"), 450)
        self.assertEqual(
            pairs["A11-03"].variant_a.answer("time_microseconds"), Rational(3, 2)
        )
        self.assertEqual(pairs["A11-03"].variant_b.answer("distance_m"), 250)
        self.assertEqual(
            pairs["A11-03"].variant_b.answer("time_microseconds"), Rational(5, 6)
        )

    def test_calibration_split_has_rank_four_and_holdout_uses_no_new_axis(self):
        pairs = build_matched_variant_pairs()
        calibration = tuple(pair for pair in pairs if pair.study_role == "calibration")
        holdout = tuple(pair for pair in pairs if pair.study_role == "holdout")
        active_indices = tuple(
            index
            for index, axis in enumerate(COST_AXES)
            if axis
            in {
                "hidden_quantities",
                "peak_live_relations",
                "symbolic_actions",
                "representation_changes",
            }
        )
        design = Matrix(
            [
                [pair.boundary.delta[index] for index in active_indices]
                for pair in calibration
            ]
        )

        self.assertEqual(len(calibration), 4)
        self.assertEqual(len(holdout), 2)
        self.assertEqual(design.rank(), 4)
        self.assertTrue(
            all(
                pair.boundary.delta[index] == 0
                for pair in holdout
                for index in range(len(COST_AXES))
                if index not in active_indices
            )
        )

    def test_two_sequences_counterbalance_route_variant_assignment(self):
        pairs = build_matched_variant_pairs()
        schedules = build_two_sequence_schedule(pairs)

        self.assertEqual({schedule.sequence_id for schedule in schedules}, {"S1", "S2"})
        for schedule in schedules:
            self.assertEqual(
                tuple(trial.order for trial in schedule.trials),
                tuple(range(1, 13)),
            )
            self.assertEqual(
                Counter(trial.route for trial in schedule.trials[:6]),
                {"direct": 3, "proposed": 3},
            )
            self.assertEqual(
                Counter(trial.route for trial in schedule.trials[6:]),
                {"direct": 3, "proposed": 3},
            )
            for pair in pairs:
                trials = [
                    trial for trial in schedule.trials if trial.pair_id == pair.pair_id
                ]
                self.assertEqual(
                    Counter(trial.route for trial in trials),
                    {"direct": 1, "proposed": 1},
                )
                self.assertEqual(abs(trials[0].order - trials[1].order), 6)
                self.assertEqual(
                    {trial.variant_id for trial in trials},
                    {pair.variant_a.variant_id, pair.variant_b.variant_id},
                )

        for pair in pairs:
            assignments = Counter(
                (trial.route, trial.variant_id)
                for schedule in schedules
                for trial in schedule.trials
                if trial.pair_id == pair.pair_id
            )
            self.assertEqual(
                assignments,
                {
                    ("direct", pair.variant_a.variant_id): 1,
                    ("direct", pair.variant_b.variant_id): 1,
                    ("proposed", pair.variant_a.variant_id): 1,
                    ("proposed", pair.variant_b.variant_id): 1,
                },
            )

    def test_header_only_observation_template_preserves_zero_empirical_rows(self):
        observations = load_paired_observation_tsv(
            TEMPLATE,
            build_matched_variant_pairs(),
        )

        self.assertEqual(observations, ())

    def test_completed_tsv_row_becomes_a_provenance_bearing_observation(self):
        pair = next(
            pair
            for pair in build_matched_variant_pairs()
            if pair.source_problem_id == "A13-02"
        )
        header = TEMPLATE.read_text(encoding="utf-8").splitlines()[0]
        row = "\t".join(
            (
                "pilot-001",
                "learner-001",
                "session-001",
                pair.source_problem_id,
                pair.variant_a.variant_id,
                pair.variant_b.variant_id,
                "120",
                "95",
                "true",
                "true",
                "direct_then_proposed",
                "timed in a closed-book paper session",
            )
        )
        with TemporaryDirectory() as directory:
            path = Path(directory) / "observations.tsv"
            path.write_text(f"{header}\n{row}\n", encoding="utf-8")

            observations = load_paired_observation_tsv(
                path,
                build_matched_variant_pairs(),
            )

        self.assertEqual(len(observations), 1)
        observation = observations[0]
        self.assertEqual(observation.boundary, pair.boundary)
        self.assertEqual(observation.direct_seconds, Fraction(120))
        self.assertEqual(observation.proposed_seconds, Fraction(95))
        self.assertIn("learner-001", observation.provenance)
        self.assertEqual(observation.order_control, "direct_then_proposed")
        self.assertEqual(observation.participant_id, "learner-001")
        self.assertEqual(observation.session_id, "session-001")


if __name__ == "__main__":
    unittest.main()
