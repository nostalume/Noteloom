"""Immutable exact matrix and Lie-algebra constructions for adjoint routes."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

Matrix = tuple[tuple[Fraction, ...], ...]


class AdjointMultiplicityObstruction(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def fraction(value: object) -> Fraction:
    if isinstance(value, (bool, float)):
        raise AdjointMultiplicityObstruction(
            "InvalidExactInput", "use integers or rational strings, not floats"
        )
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, str)):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as error:
            raise AdjointMultiplicityObstruction(
                "InvalidExactInput", f"invalid rational value {value!r}"
            ) from error
    raise AdjointMultiplicityObstruction("InvalidExactInput", f"invalid rational value {value!r}")


def text(value: Fraction) -> str:
    return (
        str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    )


def matrix(value: object, dimension: int, name: str) -> Matrix:
    if (
        not isinstance(value, list)
        or len(value) != dimension
        or any(not isinstance(row, list) or len(row) != dimension for row in value)
    ):
        raise AdjointMultiplicityObstruction(
            "CarrierViolation", f"{name} must be an exact {dimension} by {dimension} matrix"
        )
    return tuple(tuple(fraction(entry) for entry in row) for row in value)


def zero(dimension: int) -> Matrix:
    return tuple(tuple(Fraction(0) for _ in range(dimension)) for _ in range(dimension))


def identity(dimension: int) -> Matrix:
    return tuple(
        tuple(Fraction(row == column) for column in range(dimension)) for row in range(dimension)
    )


def add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(len(left)))
        for row in range(len(left))
    )


def scale(value: Matrix, scalar: Fraction) -> Matrix:
    return tuple(tuple(scalar * entry for entry in row) for row in value)


def multiply(left: Matrix, right: Matrix) -> Matrix:
    dimension = len(left)
    return tuple(
        tuple(
            sum(
                (left[row][inner] * right[inner][column] for inner in range(dimension)),
                Fraction(0),
            )
            for column in range(dimension)
        )
        for row in range(dimension)
    )


def transpose(value: Matrix) -> Matrix:
    return tuple(
        tuple(value[column][row] for column in range(len(value))) for row in range(len(value))
    )


def trace(value: Matrix) -> Fraction:
    return sum((value[index][index] for index in range(len(value))), Fraction(0))


def pair(left: Matrix, right: Matrix) -> Fraction:
    """Return tr(left @ right) without materializing the full product."""

    dimension = len(left)
    return sum(
        (
            left[row][column] * right[column][row]
            for row in range(dimension)
            for column in range(dimension)
        ),
        Fraction(0),
    )


def bracket(left: Matrix, right: Matrix) -> Matrix:
    return add(multiply(left, right), scale(multiply(right, left), Fraction(-1)))


def jordan(left: Matrix, right: Matrix) -> Matrix:
    dimension = len(left)
    product = multiply(left, right)
    reverse = multiply(right, left)
    scalar_part = Fraction(2, dimension) * trace(product)
    return add(add(product, reverse), scale(identity(dimension), -scalar_part))


def conjugator(dimension: int) -> tuple[Matrix, Matrix]:
    if dimension == 2:
        group_element: Matrix = (
            (Fraction(0), Fraction(1)),
            (Fraction(-1), Fraction(0)),
        )
    else:
        group_element = (
            (Fraction(0), Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(1)),
            (Fraction(1), Fraction(0), Fraction(0)),
        )
    return group_element, transpose(group_element)


def conjugate(group_element: Matrix, inverse_value: Matrix, value: Matrix) -> Matrix:
    return multiply(multiply(group_element, value), inverse_value)


def flat(value: Matrix) -> tuple[Fraction, ...]:
    return tuple(entry for row in value for entry in row)


def rank(rows: list[tuple[Fraction, ...]]) -> int:
    if not rows:
        return 0
    work = [list(row) for row in rows]
    row_count, column_count = len(work), len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next((row for row in range(pivot_row, row_count) if work[row][column] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][index] - factor * work[pivot_row][index] for index in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def independent(basis: list[Matrix], candidate: Matrix) -> bool:
    vectors = [flat(value) for value in basis]
    return rank([*vectors, flat(candidate)]) > len(basis)


def commutator_closure(
    seeds: list[Matrix], maximum_dimension: int
) -> tuple[list[Matrix], list[int], int]:
    basis: list[Matrix] = []
    for seed in seeds:
        if seed != zero(len(seed)) and independent(basis, seed):
            basis.append(seed)
    growth = [len(basis)]
    bracket_candidates = 0
    while True:
        snapshot = tuple(basis)
        additions = 0
        for left_index in range(len(snapshot)):
            for right_index in range(left_index + 1, len(snapshot)):
                bracket_candidates += 1
                candidate = bracket(snapshot[left_index], snapshot[right_index])
                if candidate != zero(len(candidate)) and independent(basis, candidate):
                    basis.append(candidate)
                    additions += 1
                    if len(basis) > maximum_dimension:
                        raise AdjointMultiplicityObstruction(
                            "ResourceBudgetExceeded",
                            "commutator closure exceeded maximum_closure_dimension",
                        )
        if additions == 0:
            return basis, growth, bracket_candidates
        growth.append(len(basis))


def center_dimension(basis: list[Matrix]) -> int:
    equations: list[tuple[Fraction, ...]] = []
    dimension = len(basis[0])
    for right in basis:
        brackets = [bracket(left, right) for left in basis]
        for row in range(dimension):
            for column in range(dimension):
                equations.append(tuple(value[row][column] for value in brackets))
    return len(basis) - rank(equations)


def trace_form_rank(basis: list[Matrix]) -> int:
    return rank([tuple(pair(left, right) for right in basis) for left in basis])


def inverse(value: Matrix) -> Matrix:
    dimension = len(value)
    work = [
        [*value[row], *(Fraction(row == column) for column in range(dimension))]
        for row in range(dimension)
    ]
    for column in range(dimension):
        pivot = next((row for row in range(column, dimension) if work[row][column] != 0), None)
        if pivot is None:
            raise AdjointMultiplicityObstruction(
                "DegeneratePrincipalPairing",
                "the principal-symbol pairing is degenerate on the generated closure",
            )
        work[column], work[pivot] = work[pivot], work[column]
        pivot_value = work[column][column]
        work[column] = [entry / pivot_value for entry in work[column]]
        for row in range(dimension):
            if row == column or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][index] - factor * work[column][index] for index in range(2 * dimension)
            ]
    return tuple(tuple(work[row][dimension:]) for row in range(dimension))


def coordinates(
    basis: list[Matrix], trace_gram_inverse: Matrix, value: Matrix
) -> tuple[Fraction, ...]:
    pairings = tuple(pair(left, value) for left in basis)
    return tuple(
        sum(
            (trace_gram_inverse[row][column] * pairings[column] for column in range(len(basis))),
            Fraction(0),
        )
        for row in range(len(basis))
    )


def adjoint_matrices(basis: list[Matrix], trace_gram_inverse: Matrix) -> list[Matrix]:
    dimension = len(basis)
    actions: list[Matrix] = []
    for generator in basis:
        columns = [
            coordinates(basis, trace_gram_inverse, bracket(generator, value)) for value in basis
        ]
        actions.append(
            tuple(
                tuple(columns[column][row] for column in range(dimension))
                for row in range(dimension)
            )
        )
    return actions


def matrix_sum(values: list[Matrix], dimension: int) -> Matrix:
    result = zero(dimension)
    for value in values:
        result = add(result, value)
    return result


def scalar_identity_value(value: Matrix) -> Fraction | None:
    scalar = value[0][0]
    for row in range(len(value)):
        for column in range(len(value)):
            expected = scalar if row == column else Fraction(0)
            if value[row][column] != expected:
                return None
    return scalar


@dataclass(frozen=True)
class AdjointClosure:
    matrix_size: int
    basis: tuple[Matrix, ...]
    growth: tuple[int, ...]
    bracket_candidates: int
    trace_gram: Matrix
    trace_gram_inverse: Matrix


def build_closure(seeds: list[Matrix], maximum_dimension: int) -> AdjointClosure:
    basis, growth, candidates = commutator_closure(seeds, maximum_dimension)
    gram: Matrix = tuple(tuple(pair(left, right) for right in basis) for left in basis)
    return AdjointClosure(
        len(seeds[0]), tuple(basis), tuple(growth), candidates, gram, inverse(gram)
    )
