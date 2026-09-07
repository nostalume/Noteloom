"""Exact laws for the shared adjoint-algebra kernel."""

from __future__ import annotations

import unittest
from fractions import Fraction

from adjoint_algebra import (
    add,
    bracket,
    identity,
    inverse,
    jordan,
    matrix,
    multiply,
    pair,
    rank,
    scale,
    trace,
    transpose,
    zero,
)


class AdjointAlgebraTests(unittest.TestCase):
    def setUp(self):
        self.left = matrix([["1/2", 2], [-1, 3]], 2, "left")
        self.right = matrix([[4, -2], [5, "1/3"]], 2, "right")

    def test_exact_matrix_ring_operations(self):
        self.assertEqual(add(self.left, zero(2)), self.left)
        self.assertEqual(multiply(self.left, identity(2)), self.left)
        self.assertEqual(multiply(self.left, inverse(self.left)), identity(2))
        self.assertEqual(transpose(transpose(self.left)), self.left)
        self.assertEqual(trace(scale(self.left, Fraction(2))), 2 * trace(self.left))
        self.assertEqual(rank([self.left[0], self.left[1]]), 2)

    def test_lie_and_jordan_laws(self):
        third = matrix([[0, 1], [1, 0]], 2, "third")
        self.assertEqual(bracket(self.left, self.right), scale(bracket(self.right, self.left), -1))
        jacobi = add(
            add(
                bracket(self.left, bracket(self.right, third)),
                bracket(self.right, bracket(third, self.left)),
            ),
            bracket(third, bracket(self.left, self.right)),
        )
        self.assertEqual(jacobi, zero(2))
        self.assertEqual(jordan(self.left, self.right), jordan(self.right, self.left))
        self.assertEqual(trace(jordan(self.left, self.right)), 0)

    def test_trace_pair_uses_crossed_indices(self):
        expected = trace(multiply(self.left, self.right))
        same_index = sum(
            (
                self.left[row][column] * self.right[row][column]
                for row in range(2)
                for column in range(2)
            ),
            Fraction(0),
        )
        self.assertNotEqual(same_index, expected)
        self.assertEqual(pair(self.left, self.right), expected)
        self.assertEqual(pair(self.left, self.right), pair(self.right, self.left))


if __name__ == "__main__":
    unittest.main()
