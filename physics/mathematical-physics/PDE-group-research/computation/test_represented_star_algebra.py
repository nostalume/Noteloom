"""Public laws for exact finite represented star-algebra decomposition."""

from __future__ import annotations

import unittest

import exact_gaussian_matrix as gaussian
from represented_star_algebra import (
    StarAlgebraBudget,
    StarAlgebraError,
    StarGenerator,
    construct,
    decompose_coefficient,
)


class RepresentedStarAlgebraTests(unittest.TestCase):
    @staticmethod
    def _mixed_generators() -> tuple[StarGenerator, StarGenerator]:
        return (
            StarGenerator(
                "X",
                gaussian.matrix(
                    [
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0],
                        [1, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                    ],
                    "X",
                ),
            ),
            StarGenerator(
                "Z",
                gaussian.matrix(
                    [
                        [1, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0],
                        [0, 0, -1, 0, 0],
                        [0, 0, 0, -1, 0],
                        [0, 0, 0, 0, 0],
                    ],
                    "Z",
                ),
            ),
        )

    def test_repeated_matrix_algebra_separates_irreducible_size_from_multiplicity(self) -> None:
        mixing = StarGenerator(
            "X",
            gaussian.matrix(
                [[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]],
                "X",
            ),
        )
        grading = StarGenerator(
            "Z",
            gaussian.matrix(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]],
                "Z",
            ),
        )

        algebra = construct(
            (mixing, grading),
            StarAlgebraBudget(4, 2, 16, 64),
        )

        self.assertEqual(algebra.algebra_dimension, 4)
        self.assertEqual(algebra.commutant_dimension, 4)
        self.assertEqual(algebra.center_dimension, 1)
        self.assertEqual(len(algebra.blocks), 1)
        block = algebra.blocks[0]
        self.assertEqual(block.carrier_dimension, 4)
        self.assertEqual(block.algebra_dimension, 4)
        self.assertEqual(block.commutant_dimension, 4)
        self.assertEqual(block.irreducible_dimension, 2)
        self.assertEqual(block.multiplicity, 2)
        self.assertEqual(algebra.commutator_system_entries, 3072)
        self.assertTrue(all(algebra.checks.values()))

    def test_mixed_isotypic_transfer_constructs_two_central_blocks(self) -> None:
        algebra = construct(
            self._mixed_generators(),
            StarAlgebraBudget(5, 2, 25, 128),
        )

        self.assertEqual(algebra.algebra_dimension, 5)
        self.assertEqual(algebra.commutant_dimension, 5)
        self.assertEqual(algebra.center_dimension, 2)
        self.assertEqual(
            sorted(
                (
                    block.carrier_dimension,
                    block.irreducible_dimension,
                    block.multiplicity,
                )
                for block in algebra.blocks
            ),
            [(1, 1, 1), (4, 2, 2)],
        )
        self.assertTrue(all(algebra.checks.values()))
        decomposition = decompose_coefficient(algebra, algebra.generators[0].value)
        self.assertEqual(decomposition.direct_value, decomposition.projector_synthesis)
        self.assertEqual(len(decomposition.block_values), 2)
        self.assertEqual(algebra.commutator_system_entries, 8750)
        cross_block = gaussian.matrix(
            [
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
            ],
            "cross_block",
        )
        with self.assertRaises(StarAlgebraError) as caught:
            decompose_coefficient(algebra, cross_block)
        self.assertEqual(caught.exception.kind, "CoefficientMixesIsotypicBlocks")

    def test_complex_spinor_coefficients_construct_an_irreducible_block(self) -> None:
        mixing = StarGenerator("X", gaussian.matrix([[0, 1], [1, 0]], "X"))
        imaginary = StarGenerator(
            "Y",
            gaussian.matrix([[0, [0, -1]], [[0, 1], 0]], "Y"),
        )

        algebra = construct(
            (mixing, imaginary),
            StarAlgebraBudget(2, 2, 4, 32),
        )

        self.assertEqual(
            (
                algebra.algebra_dimension,
                algebra.commutant_dimension,
                algebra.blocks[0].irreducible_dimension,
                algebra.blocks[0].multiplicity,
            ),
            (4, 1, 2, 1),
        )

    def test_rational_orthogonal_conjugation_preserves_block_signature(self) -> None:
        rotation = gaussian.matrix(
            [
                ["3/5", 0, 0, 0, "-4/5"],
                [0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                ["4/5", 0, 0, 0, "3/5"],
            ],
            "rotation",
        )

        def rotate(generator: StarGenerator) -> StarGenerator:
            return StarGenerator(
                generator.label,
                gaussian.multiply(
                    gaussian.multiply(rotation, generator.value),
                    gaussian.dagger(rotation),
                ),
            )

        original = construct(
            self._mixed_generators(),
            StarAlgebraBudget(5, 2, 25, 128),
        )
        rotated = construct(
            tuple(rotate(generator) for generator in self._mixed_generators()),
            StarAlgebraBudget(5, 2, 25, 128),
        )

        signature = lambda result: sorted(  # noqa: E731
            (
                block.carrier_dimension,
                block.irreducible_dimension,
                block.multiplicity,
            )
            for block in result.blocks
        )
        self.assertEqual(signature(rotated), signature(original))
        self.assertNotEqual(
            {repr(gaussian.serialize(block.projector)) for block in rotated.blocks},
            {repr(gaussian.serialize(block.projector)) for block in original.blocks},
        )

    def test_non_hermitian_generator_is_refused_as_non_star_input(self) -> None:
        non_hermitian = StarGenerator("N", gaussian.matrix([[0, 1], [0, 0]], "N"))

        with self.assertRaises(StarAlgebraError) as caught:
            construct((non_hermitian,), StarAlgebraBudget(2, 1, 4, 16))

        self.assertEqual(caught.exception.kind, "NonStarClosedGenerators")

    def test_ambient_budget_refuses_before_kernel_materialization(self) -> None:
        generators = self._mixed_generators()

        with self.assertRaises(StarAlgebraError) as caught:
            construct(generators, StarAlgebraBudget(5, 2, 24, 128))

        self.assertEqual(caught.exception.kind, "StarAlgebraBudgetExceeded")
