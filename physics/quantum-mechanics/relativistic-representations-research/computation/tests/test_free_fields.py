import unittest

from sympy import Matrix, Rational

from fieldcalc.grammar import factor_first_order
from fieldcalc.residual import projected_raise_coefficient


class FreeFieldTests(unittest.TestCase):
    def test_abstract_first_order_factorization_avoids_gamma_components(self):
        grammar = factor_first_order("Q")
        certificate = grammar.relation_certificate(("G", "G"))
        self.assertEqual(certificate.normal_form.terms, {("Q",): 1})
        self.assertEqual(certificate.origin, "polarized first-order factorization")

    def test_projected_raise_is_forced_by_trace_obstruction(self):
        self.assertEqual(projected_raise_coefficient(rank=2, dimension=4), Rational(-1, 6))
        self.assertEqual(projected_raise_coefficient(rank=3, dimension=4), Rational(-1, 8))

    def test_quotient_dimension_is_rank_minus_gauge_rank(self):
        equation = Matrix([[1, 0, 0], [0, 1, 0]])
        gauge = Matrix([[0], [0], [1]])
        self.assertEqual(len(equation.nullspace()) - gauge.rank(), 0)


if __name__ == "__main__":
    unittest.main()
