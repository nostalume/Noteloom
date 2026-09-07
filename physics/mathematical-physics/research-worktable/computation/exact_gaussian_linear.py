"""Exact Gaussian-rational elimination for finite carrier realization."""

from __future__ import annotations

import exact_gaussian_matrix as gaussian

Vector = tuple[gaussian.Gaussian, ...]


def _reduced(
    rows: list[list[gaussian.Gaussian]], columns: int
) -> tuple[list[list[gaussian.Gaussian]], list[int]]:
    if columns < 0 or any(len(row) != columns for row in rows):
        raise ValueError("Gaussian row dimensions differ")
    result = [list(row) for row in rows]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(columns):
        selected = next(
            (row for row in range(pivot_row, len(result)) if result[row][column] != gaussian.ZERO),
            None,
        )
        if selected is None:
            continue
        result[pivot_row], result[selected] = result[selected], result[pivot_row]
        pivot = result[pivot_row][column]
        result[pivot_row] = [entry / pivot for entry in result[pivot_row]]
        for row in range(len(result)):
            if row == pivot_row or result[row][column] == gaussian.ZERO:
                continue
            factor = result[row][column]
            result[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(result[row], result[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(result):
            break
    return result, pivots


def rank(vectors: tuple[Vector, ...]) -> int:
    if not vectors:
        return 0
    width = len(vectors[0])
    return len(_reduced([list(vector) for vector in vectors], width)[1])


def coordinates(target: Vector, basis: tuple[Vector, ...]) -> Vector | None:
    if not basis:
        return () if all(entry == gaussian.ZERO for entry in target) else None
    if any(len(vector) != len(target) for vector in basis):
        raise ValueError("Gaussian vector dimensions differ")
    rows = [[*(vector[index] for vector in basis), target[index]] for index in range(len(target))]
    reduced, pivots = _reduced(rows, len(basis) + 1)
    if len(basis) in pivots:
        return None
    if len([pivot for pivot in pivots if pivot < len(basis)]) != len(basis):
        raise ValueError("Gaussian coordinate basis is dependent")
    result = [gaussian.ZERO for _ in basis]
    for row, pivot in enumerate(pivots):
        if pivot < len(basis):
            result[pivot] = reduced[row][-1]
    return tuple(result)


def determinant(value: gaussian.ComplexMatrix) -> gaussian.Gaussian:
    dimension = len(value)
    if not dimension or any(len(row) != dimension for row in value):
        raise ValueError("determinant requires a nonempty square matrix")
    rows = [list(row) for row in value]
    result = gaussian.ONE
    for column in range(dimension):
        selected = next(
            (row for row in range(column, dimension) if rows[row][column] != gaussian.ZERO),
            None,
        )
        if selected is None:
            return gaussian.ZERO
        if selected != column:
            rows[column], rows[selected] = rows[selected], rows[column]
            result = -result
        pivot = rows[column][column]
        result = result * pivot
        for row in range(column + 1, dimension):
            if rows[row][column] == gaussian.ZERO:
                continue
            factor = rows[row][column] / pivot
            rows[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[column], strict=True)
            ]
    return result
