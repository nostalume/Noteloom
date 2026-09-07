"""Public laws for irreducible simple-block PDE reduction."""

from __future__ import annotations

import unittest
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from represented_star_algebra import StarAlgebraBudget, StarGenerator, construct
from simple_block_pde import (
    QuadraticSymbol,
    RealizationBudget,
    RealizationError,
    construct_irreducible_model,
    evaluate_quadratic_symbol,
)


class SimpleBlockPdeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generators = (
            StarGenerator(
                "X",
                gaussian.matrix(
                    [[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]],
                    "X",
                ),
            ),
            StarGenerator(
                "Z",
                gaussian.matrix(
                    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]],
                    "Z",
                ),
            ),
        )
        self.algebra = construct(self.generators, StarAlgebraBudget(4, 2, 16, 64))

    def test_repeated_matrix_block_constructs_a_minimal_irreducible_carrier(self) -> None:
        model = construct_irreducible_model(self.algebra, 0, RealizationBudget(4, 64))

        self.assertEqual(model.carrier_dimension, 2)
        self.assertEqual(model.multiplicity, 2)
        self.assertEqual(len(model.embedding_columns), 2)
        self.assertEqual([item.label for item in model.reduced_generators], ["X", "Z"])
        self.assertTrue(all(model.checks.values()))

    def test_quadratic_differential_symbol_reconstructs_determinant_and_cost(self) -> None:
        model = construct_irreducible_model(self.algebra, 0, RealizationBudget(4, 64))
        symbol = QuadraticSymbol(
            gaussian.identity(4),
            self.generators[0].value,
            self.generators[1].value,
        )

        witness = evaluate_quadratic_symbol(model, symbol, Fraction(2))

        self.assertEqual(
            witness.full_determinant, witness.reduced_determinant * witness.reduced_determinant
        )
        self.assertEqual(witness.cost.baseline_per_query, 64)
        self.assertEqual(witness.cost.reduced_per_query, 8)
        self.assertGreater(witness.cost.break_even_queries, 1)
        self.assertTrue(all(witness.checks.values()))

    def test_splitter_budget_and_non_algebra_coefficient_refuse_distinctly(self) -> None:
        with self.assertRaises(RealizationError) as caught:
            construct_irreducible_model(self.algebra, 0, RealizationBudget(0, 64))
        self.assertEqual(caught.exception.kind, "MultiplicitySplitterUnavailable")

        model = construct_irreducible_model(self.algebra, 0, RealizationBudget(4, 64))
        bad = QuadraticSymbol(
            gaussian.identity(4),
            self.algebra.commutant_hermitian_basis[1],
            gaussian.identity(4),
        )
        with self.assertRaises(RealizationError) as caught:
            evaluate_quadratic_symbol(model, bad, Fraction(1))
        self.assertEqual(caught.exception.kind, "CoefficientOutsideRepresentedAlgebra")

    def test_rational_conjugation_preserves_reduced_symbol_observable(self) -> None:
        rotation = gaussian.matrix(
            [
                ["3/5", "-4/5", 0, 0],
                ["4/5", "3/5", 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            "rotation",
        )

        def rotate(value: gaussian.ComplexMatrix) -> gaussian.ComplexMatrix:
            return gaussian.multiply(gaussian.multiply(rotation, value), gaussian.dagger(rotation))

        rotated_generators = tuple(
            StarGenerator(generator.label, rotate(generator.value)) for generator in self.generators
        )
        rotated_algebra = construct(
            rotated_generators,
            StarAlgebraBudget(4, 2, 16, 64),
        )
        original_model = construct_irreducible_model(self.algebra, 0, RealizationBudget(4, 64))
        rotated_model = construct_irreducible_model(rotated_algebra, 0, RealizationBudget(4, 64))
        original = evaluate_quadratic_symbol(
            original_model,
            QuadraticSymbol(
                gaussian.identity(4), self.generators[0].value, self.generators[1].value
            ),
            Fraction(3),
        )
        rotated = evaluate_quadratic_symbol(
            rotated_model,
            QuadraticSymbol(
                gaussian.identity(4), rotated_generators[0].value, rotated_generators[1].value
            ),
            Fraction(3),
        )

        self.assertEqual(rotated.full_determinant, original.full_determinant)
        self.assertEqual(rotated.reduced_determinant, original.reduced_determinant)
