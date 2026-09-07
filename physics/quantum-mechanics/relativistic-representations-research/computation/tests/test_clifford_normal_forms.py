import unittest

from sympy import Matrix, Rational, diag, symbols

from fieldcalc.clifford import (
    clifford_trace,
    clifford_trace_pfaffian,
    clifford_vector,
)
from fieldcalc.exterior import compile_exterior_normal_form


class CliffordNormalFormTests(unittest.TestCase):
    def test_trace_is_generated_only_from_invariant_pairings(self):
        metric = diag(-1, 1)
        vectors = tuple(Matrix(vector) for vector in (
            (1, 0), (2, 1), (0, 1), (1, -1),
        ))
        operator = clifford_vector(vectors[0])
        for vector in vectors[1:]:
            operator *= clifford_vector(vector)
        trace = clifford_trace(operator, metric)

        def pairing(left, right):
            return -(left.T * metric * right)[0]

        a, b, c, d = vectors
        expected = (
            pairing(a, b) * pairing(c, d)
            - pairing(a, c) * pairing(b, d)
            + pairing(a, d) * pairing(b, c)
        )
        self.assertEqual(trace.value, expected)
        self.assertEqual(trace.pairing_terms, 3)

    def test_pfaffian_exposes_when_structural_reduction_moves_cost(self):
        metric = diag(-1, 1)
        vector = Matrix((1, 0))
        operator = clifford_vector(vector)
        for _ in range(7):
            operator *= clifford_vector(vector)
        recursive = clifford_trace(operator, metric)
        compiled = clifford_trace_pfaffian(operator, metric)

        self.assertEqual(compiled.value, recursive.value)
        self.assertEqual(compiled.pairing_terms, 105)
        self.assertEqual(compiled.elimination_updates, 22)
        self.assertEqual(recursive.recurrence_updates, 16)
        self.assertLess(
            recursive.recurrence_updates, compiled.elimination_updates
        )

        distinct = []
        for index in range(8):
            coordinates = [1] + [0] * 8
            coordinates[index + 1] = 1
            distinct.append(Matrix(coordinates))
        distinct_operator = clifford_vector(distinct[0])
        for item in distinct[1:]:
            distinct_operator *= clifford_vector(item)
        distinct_recursive = clifford_trace(distinct_operator, diag(*([1] * 9)))
        distinct_pfaffian = clifford_trace_pfaffian(
            distinct_operator, diag(*([1] * 9))
        )
        self.assertEqual(distinct_pfaffian.value, distinct_recursive.value)
        self.assertLess(
            distinct_pfaffian.elimination_updates,
            distinct_recursive.recurrence_updates,
        )

        uncertain = symbols("x", real=True)
        conditional = clifford_trace_pfaffian(
            clifford_vector(Matrix((uncertain, 0)))
            * clifford_vector(vector),
            metric,
        )
        self.assertEqual(conditional.value, uncertain)
        self.assertEqual(conditional.pivot_conditions, (uncertain,))

    def test_exterior_normal_form_is_covariant_and_bounded(self):
        metric = diag(-1, 1, 1)
        vectors = tuple(Matrix(vector) for vector in (
            (1, 0, 1), (2, 1, 0), (0, 1, -1), (1, -1, 2),
        ))
        operator = clifford_vector(vectors[0])
        for vector in vectors[1:]:
            operator *= clifford_vector(vector)
        normal = compile_exterior_normal_form(operator, metric)

        self.assertTrue(normal.accepted)
        self.assertLessEqual(normal.operator.term_count, 8)
        self.assertEqual(
            normal.operator.scalar_part,
            clifford_trace(operator, metric).value,
        )
        self.assertEqual(normal.relation_residual, 0)

        boost = Matrix((
            (Rational(5, 4), Rational(3, 4), 0),
            (Rational(3, 4), Rational(5, 4), 0),
            (0, 0, 1),
        ))
        self.assertEqual(boost.T * metric * boost, metric)
        transformed = clifford_vector(boost * vectors[0])
        for vector in vectors[1:]:
            transformed *= clifford_vector(boost * vector)
        transformed_normal = compile_exterior_normal_form(transformed, metric)
        self.assertEqual(
            transformed_normal.operator.scalar_part,
            normal.operator.scalar_part,
        )

        nonorthogonal = compile_exterior_normal_form(
            operator, Matrix(((-1, 1, 0), (1, 1, 0), (0, 0, 1)))
        )
        self.assertFalse(nonorthogonal.accepted)
        self.assertEqual(
            nonorthogonal.refusal.reason,
            "exterior backend requires an admitted orthogonal frame",
        )

        mismatched = compile_exterior_normal_form(
            clifford_vector(Matrix((1, 0))), metric
        )
        self.assertFalse(mismatched.accepted)
        self.assertEqual(
            mismatched.refusal.reason,
            "Clifford vector dimension does not match the frame",
        )


if __name__ == "__main__":
    unittest.main()
