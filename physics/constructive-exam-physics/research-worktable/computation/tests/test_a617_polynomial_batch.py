from collections import Counter
from pathlib import Path
import unittest

from occ.corpus import load_corpus_index
from worktable.polynomial_cases import (
    build_polynomial_batch,
    run_polynomial_batch,
)


CORPUS_PATH = Path(__file__).parents[2] / "sources" / "a617-corpus-index.tsv"


class A617PolynomialBatchTests(unittest.TestCase):
    def test_locked_batch_is_exactly_the_corpus_polynomial_queue(self):
        queued = {
            entry.problem_id
            for entry in load_corpus_index(CORPUS_PATH)
            if entry.next_operator == "finite-polynomial-elimination"
        }
        cases = build_polynomial_batch()

        self.assertEqual(len(cases), 19)
        self.assertEqual({case.packet.problem_id for case in cases}, queued)

    def test_every_expected_relation_is_certified_by_the_source_packet(self):
        checked = run_polynomial_batch()

        self.assertTrue(all(item.certificates_passed for item in checked))
        self.assertEqual(
            Counter(item.result.status for item in checked),
            {"complete": 16, "partial": 3},
        )

    def test_partial_results_expose_only_the_declared_semantic_gap(self):
        checked = run_polynomial_batch()
        target_statuses = Counter(
            target.elimination.status
            for item in checked
            for target in item.result.targets
        )

        self.assertEqual(sum(target_statuses.values()), 44)
        self.assertEqual(target_statuses, {"constrained": 41, "underdetermined": 3})
        self.assertEqual(
            {
                item.case.packet.problem_id
                for item in checked
                if item.result.status == "partial"
            },
            {"A16-04", "A14-08", "A11-07"},
        )


if __name__ == "__main__":
    unittest.main()
