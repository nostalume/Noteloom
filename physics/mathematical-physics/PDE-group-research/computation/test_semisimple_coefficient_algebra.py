"""Public laws for finite split Hermitian coefficient algebras."""

from __future__ import annotations

import unittest
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from semisimple_coefficient_algebra import (
    AlgebraBudget,
    AlgebraError,
    Generator,
    PolynomialTerm,
    construct,
    decompose_polynomial,
)


class SemisimpleCoefficientAlgebraTests(unittest.TestCase):
    def setUp(self) -> None:
        self.first = Generator("A", gaussian.matrix([[0, 0, 0], [0, 1, 0], [0, 0, 1]], "A"))
        self.second = Generator("B", gaussian.matrix([[0, 0, 0], [0, 0, 0], [0, 0, 1]], "B"))
        self.budget = AlgebraBudget(3, 2, 64)

    def test_joint_refinement_constructs_three_primitive_sectors_and_polynomial_use(self) -> None:
        algebra = construct((self.first, self.second), self.budget)

        self.assertEqual(algebra.dimension, 3)
        self.assertEqual(
            [sector.character for sector in algebra.sectors],
            [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)), (Fraction(1), Fraction(1))],
        )
        self.assertEqual([sector.multiplicity for sector in algebra.sectors], [1, 1, 1])
        self.assertTrue(algebra.separates_carrier)
        self.assertEqual(
            algebra.minimal_polynomials,
            ((Fraction(0), Fraction(-1), Fraction(1)),) * 2,
        )
        self.assertEqual(
            [(step.input_sectors, step.output_sectors) for step in algebra.refinement],
            [(1, 2), (2, 3)],
        )
        self.assertEqual(algebra.factor_candidate_checks, 0)
        self.assertTrue(all(algebra.checks.values()))

        decomposition = decompose_polynomial(
            algebra,
            (
                PolynomialTerm(Fraction(1), (0, 0)),
                PolynomialTerm(Fraction(2), (1, 0)),
                PolynomialTerm(Fraction(3), (0, 1)),
                PolynomialTerm(Fraction(5), (1, 1)),
            ),
        )
        self.assertEqual(decomposition.sector_values, (Fraction(1), Fraction(3), Fraction(11)))
        self.assertEqual(decomposition.direct_value, decomposition.projector_synthesis)

    def test_repeated_eigenspace_is_reported_when_not_jointly_refined(self) -> None:
        algebra = construct((self.first,), AlgebraBudget(3, 1, 32))

        self.assertEqual([sector.multiplicity for sector in algebra.sectors], [1, 2])
        self.assertFalse(algebra.separates_carrier)

    def test_rational_orthogonal_conjugation_preserves_characters(self) -> None:
        rotation = gaussian.matrix([["3/5", "-4/5", 0], ["4/5", "3/5", 0], [0, 0, 1]], "rotation")

        def rotate(generator: Generator) -> Generator:
            return Generator(
                generator.label,
                gaussian.multiply(
                    gaussian.multiply(rotation, generator.value), gaussian.dagger(rotation)
                ),
            )

        original = construct((self.first, self.second), self.budget)
        rotated = construct((rotate(self.first), rotate(self.second)), self.budget)

        self.assertEqual(
            [sector.character for sector in rotated.sectors],
            [sector.character for sector in original.sectors],
        )
        self.assertNotEqual(
            [sector.projector for sector in rotated.sectors],
            [sector.projector for sector in original.sectors],
        )

    def test_primitive_projectors_do_not_depend_on_generator_order(self) -> None:
        forward = construct((self.first, self.second), self.budget)
        reverse = construct((self.second, self.first), self.budget)

        self.assertEqual(
            {repr(gaussian.serialize(sector.projector)) for sector in forward.sectors},
            {repr(gaussian.serialize(sector.projector)) for sector in reverse.sectors},
        )

    def test_noncommuting_generators_are_refused(self) -> None:
        mixing = Generator("X", gaussian.matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]], "X"))

        with self.assertRaises(AlgebraError) as caught:
            construct((self.first, mixing), self.budget)

        self.assertEqual(caught.exception.kind, "NoncommutingCoefficientAlgebra")

    def test_unsplit_minimal_polynomial_requires_a_field_extension(self) -> None:
        golden = Generator("G", gaussian.matrix([[0, 1], [1, 1]], "G"))

        with self.assertRaises(AlgebraError) as caught:
            construct((golden,), AlgebraBudget(2, 1, 32))

        self.assertEqual(caught.exception.kind, "CoefficientFieldExtensionRequired")

    def test_factorization_budget_is_checked_before_candidate_evaluation(self) -> None:
        distinct = Generator("D", gaussian.matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]], "D"))

        with self.assertRaises(AlgebraError) as caught:
            construct((distinct,), AlgebraBudget(3, 1, 0))

        self.assertEqual(caught.exception.kind, "FactorizationBudgetExceeded")

    def test_bounded_rational_search_splits_a_cubic_minimal_polynomial(self) -> None:
        distinct = Generator("D", gaussian.matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]], "D"))

        algebra = construct((distinct,), AlgebraBudget(3, 1, 32))

        self.assertEqual(
            algebra.minimal_polynomials[0],
            (Fraction(-6), Fraction(11), Fraction(-6), Fraction(1)),
        )
        self.assertEqual([sector.character for sector in algebra.sectors], [(1,), (2,), (3,)])
        self.assertGreater(algebra.factor_candidate_checks, 0)

    def test_nonintegral_polynomial_power_is_refused_by_the_public_operation(self) -> None:
        algebra = construct((self.first,), AlgebraBudget(3, 1, 32))

        with self.assertRaises(AlgebraError) as caught:
            decompose_polynomial(
                algebra,
                (PolynomialTerm(Fraction(1), (Fraction(1, 2),)),),  # type: ignore[arg-type]
            )

        self.assertEqual(caught.exception.kind, "InvalidCoefficientPolynomial")


if __name__ == "__main__":
    unittest.main()
