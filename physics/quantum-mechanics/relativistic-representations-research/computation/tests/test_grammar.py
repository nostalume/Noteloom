import unittest

from fieldcalc.grammar import CarrierLaw, compile_grammar, factor_first_order
from fieldcalc.rewrite import Polynomial


class GrammarTests(unittest.TestCase):
    def test_symmetric_and_exterior_exchange_are_generated_from_law(self):
        symmetric = compile_grammar(CarrierLaw("symmetric", power=3), {"metric"})
        exterior = compile_grammar(CarrierLaw("exterior", power=2), set())

        self.assertEqual(
            symmetric.normalize(Polynomial.word("A", "P")),
            Polynomial({("P", "A"): 1, ("Q",): 1}),
        )
        self.assertEqual(
            exterior.normalize(Polynomial.word("A", "P")),
            Polynomial({("P", "A"): -1, ("Q",): 1}),
        )
        self.assertEqual(exterior.normalize(Polynomial.word("P", "P")), Polynomial())

    def test_missing_resource_returns_a_typed_refusal(self):
        result = compile_grammar(CarrierLaw("symmetric", power=2), set())
        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "missing metric resource")

    def test_first_order_factorization_generates_clifford_reduction(self):
        grammar = factor_first_order("Q")
        self.assertEqual(
            grammar.normalize(Polynomial.word("G", "G")),
            Polynomial.word("Q"),
        )

    def test_word_budget_is_a_semantic_refusal(self):
        grammar = compile_grammar(CarrierLaw("exterior", power=2), set(), budget=1)
        result = grammar.try_normalize(Polynomial.word("A", "P"))
        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "word budget exceeded")


if __name__ == "__main__":
    unittest.main()
