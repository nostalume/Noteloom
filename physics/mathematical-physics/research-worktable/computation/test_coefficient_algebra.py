"""Unit checks for the exact involutive coefficient algebra."""

from __future__ import annotations

import unittest
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from coefficient_algebra import CoefficientAlgebraError, construct


class CoefficientAlgebraTests(unittest.TestCase):
    def setUp(self) -> None:
        self.grading = gaussian.matrix([[1, 0], [0, -1]], "grading")

    def test_distinct_sector_roots_recover_projectors_without_an_eigensolver(self) -> None:
        coefficient = gaussian.scale(self.grading, Fraction(2))

        algebra = construct(self.grading, coefficient)

        self.assertEqual(algebra.eigenvalues, (Fraction(2), Fraction(-2)))
        self.assertEqual(algebra.coordinates, (Fraction(0), Fraction(2)))
        self.assertEqual(algebra.minimal_polynomial, (Fraction(-4), Fraction(0), Fraction(1)))
        self.assertEqual(algebra.coefficient_projectors, algebra.projectors)
        self.assertTrue(all(algebra.checks.values()))

    def test_equal_roots_collapse_the_coefficient_minimal_polynomial(self) -> None:
        coefficient = gaussian.scale(gaussian.identity(2), Fraction(2))

        algebra = construct(self.grading, coefficient)

        self.assertEqual(algebra.eigenvalues, (Fraction(2), Fraction(2)))
        self.assertEqual(algebra.minimal_polynomial, (Fraction(-2), Fraction(1)))
        self.assertIsNone(algebra.coefficient_projectors)

    def test_noncommuting_coefficient_is_refused(self) -> None:
        coefficient = gaussian.matrix([[0, 1], [1, 0]], "coefficient")

        with self.assertRaises(CoefficientAlgebraError) as caught:
            construct(self.grading, coefficient)

        self.assertEqual(caught.exception.kind, "NoncommutingCoefficientAlgebra")


if __name__ == "__main__":
    unittest.main()
