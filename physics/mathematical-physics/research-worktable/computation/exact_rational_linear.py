"""Small exact rational linear-algebra operations shared by symbolic constructors."""

from __future__ import annotations

from fractions import Fraction

Vector = tuple[Fraction, ...]


def _reduced_rows(
    rows: list[list[Fraction]], columns: int
) -> tuple[list[list[Fraction]], list[int]]:
    if columns < 0 or any(len(row) != columns for row in rows):
        raise ValueError("rational row dimensions differ")
    reduced = [list(row) for row in rows]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(columns):
        selected = next(
            (row for row in range(pivot_row, len(reduced)) if reduced[row][column]),
            None,
        )
        if selected is None:
            continue
        reduced[pivot_row], reduced[selected] = reduced[selected], reduced[pivot_row]
        pivot = reduced[pivot_row][column]
        reduced[pivot_row] = [entry / pivot for entry in reduced[pivot_row]]
        for row in range(len(reduced)):
            if row == pivot_row or not reduced[row][column]:
                continue
            factor = reduced[row][column]
            reduced[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(reduced[row], reduced[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(reduced):
            break
    return reduced, pivots


def nullspace(rows: list[list[Fraction]], columns: int) -> tuple[Vector, ...]:
    """Return a canonical exact basis for the kernel of a row matrix."""
    reduced, pivots = _reduced_rows(rows, columns)
    free_columns = [column for column in range(columns) if column not in pivots]
    basis: list[Vector] = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        basis.append(tuple(vector))
    return tuple(basis)


def rank(vectors: tuple[Vector, ...]) -> int:
    """Return the exact dimension of the span of equally sized row vectors."""
    if not vectors:
        return 0
    width = len(vectors[0])
    if any(len(vector) != width for vector in vectors):
        raise ValueError("rational vector dimensions differ")
    return len(_reduced_rows([list(vector) for vector in vectors], width)[1])


def independent_basis(vectors: tuple[Vector, ...]) -> tuple[Vector, ...]:
    """Retain the first exact independent vectors, preserving input order."""
    basis: list[Vector] = []
    for vector in vectors:
        candidate = (*basis, vector)
        if rank(candidate) > len(basis):
            basis.append(vector)
    return tuple(basis)


def coordinates(target: Vector, basis: tuple[Vector, ...]) -> Vector | None:
    """Solve for target coordinates in an independent basis, or return None."""
    if not basis:
        return () if not any(target) else None
    if any(len(vector) != len(target) for vector in basis):
        raise ValueError("rational vector dimensions differ")
    rows = [[*(vector[index] for vector in basis), target[index]] for index in range(len(target))]
    reduced, pivots = _reduced_rows(rows, len(basis) + 1)
    if len(basis) in pivots:
        return None
    basis_pivots = [pivot for pivot in pivots if pivot < len(basis)]
    if len(basis_pivots) != len(basis):
        raise ValueError("coordinate basis is linearly dependent")
    result = [Fraction(0) for _ in basis]
    for row, pivot in enumerate(pivots):
        if pivot < len(basis):
            result[pivot] = reduced[row][-1]
    return tuple(result)
