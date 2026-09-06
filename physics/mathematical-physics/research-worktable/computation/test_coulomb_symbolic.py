import unittest

from coulomb_symbolic import build_certificate


class CoulombSymbolicTests(unittest.TestCase):
    def test_all_classical_hidden_algebra_relations_hold_exactly(self):
        certificate = build_certificate()

        self.assertEqual(certificate["status"], "Passed")
        self.assertEqual(len(certificate["checks"]), 35)
        self.assertTrue(all(certificate["checks"].values()))
        self.assertTrue(all(certificate["negative_control"].values()))

    def test_certificate_does_not_overclaim_quantum_or_analytic_results(self):
        certificate = build_certificate()

        self.assertIn(
            "quantum ordering and hbar^2 Casimir correction",
            certificate["not_certified"],
        )
        self.assertIn(
            "existence and completeness of bound states",
            certificate["not_certified"],
        )


if __name__ == "__main__":
    unittest.main()
