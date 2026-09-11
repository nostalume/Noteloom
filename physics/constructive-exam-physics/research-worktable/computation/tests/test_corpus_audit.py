from pathlib import Path
import unittest

from occ.corpus import load_corpus_index, summarize_corpus


CORPUS_PATH = Path(__file__).parents[2] / "sources" / "a617-corpus-index.tsv"


class CorpusAuditTests(unittest.TestCase):
    def test_complete_top_level_inventory_has_expected_year_counts(self):
        entries = load_corpus_index(CORPUS_PATH)
        summary = summarize_corpus(entries)

        self.assertEqual(summary.total, 126)
        self.assertEqual(len(summary.years), 15)
        self.assertNotIn(2017, summary.years)
        self.assertEqual(summary.by_year[2025], 8)
        self.assertEqual(summary.by_year[2019], 9)
        self.assertEqual(summary.by_year[2010], 8)
        self.assertEqual(len({entry.problem_id for entry in entries}), 126)

    def test_evidence_levels_do_not_confuse_execution_with_static_triage(self):
        entries = load_corpus_index(CORPUS_PATH)
        by_id = {entry.problem_id: entry for entry in entries}
        summary = summarize_corpus(entries)

        self.assertEqual(by_id["A25-02"].evidence, "executed-full")
        self.assertEqual(by_id["A25-05"].evidence, "executed-shape-only")
        self.assertEqual(by_id["A24-05"].evidence, "executed-shape-only")
        self.assertEqual(by_id["A23-05"].evidence, "executed-full")
        self.assertEqual(by_id["A23-05"].next_operator, "harmonic-product-operator")
        self.assertEqual(by_id["A15-01"].evidence, "executed-full")
        self.assertEqual(by_id["A15-01"].next_operator, "event-branch-compiler")
        self.assertEqual(by_id["A15-02"].evidence, "executed-full")
        self.assertEqual(by_id["A15-02"].next_operator, "impact-projection-operator")
        self.assertEqual(by_id["A14-06"].evidence, "executed-full")
        self.assertEqual(by_id["A10-06"].evidence, "executed-full")
        self.assertEqual(by_id["A14-06"].next_operator, "path-functional-operator")
        self.assertEqual(by_id["A10-06"].next_operator, "path-functional-operator")
        self.assertEqual(by_id["A21-03"].evidence, "executed-full")
        self.assertEqual(by_id["A25-06"].evidence, "executed-full")
        self.assertEqual(by_id["A21-03"].next_operator, "harmonic-response-operator")
        self.assertEqual(by_id["A25-06"].next_operator, "harmonic-response-operator")
        self.assertEqual(by_id["A11-06"].evidence, "executed-full")
        self.assertEqual(by_id["A11-06"].next_operator, "harmonic-product-operator")
        self.assertEqual(summary.by_evidence["executed-full"], 25)
        self.assertEqual(summary.by_evidence["executed-partial"], 3)
        self.assertEqual(summary.by_evidence["executed-shape-only"], 2)
        self.assertEqual(summary.by_evidence["candidate-unexecuted"], 18)
        self.assertEqual(summary.by_evidence["outside-current-grammar"], 74)
        self.assertEqual(
            summary.total,
            sum(summary.by_evidence.values()),
        )

    def test_every_row_names_the_missing_or_used_operation(self):
        entries = load_corpus_index(CORPUS_PATH)

        self.assertTrue(all(entry.next_operator.strip() for entry in entries))
        self.assertTrue(all(entry.family.strip() for entry in entries))
        self.assertTrue(all(entry.synopsis.strip() for entry in entries))


if __name__ == "__main__":
    unittest.main()
