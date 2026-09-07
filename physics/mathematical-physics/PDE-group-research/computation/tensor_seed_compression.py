"""Exact candidate and residual compression for finite covariant tensors."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement, product

from linear_defect_compiler import CandidateBracket, DefectBlock, LinearMap

Index = tuple[int, ...]
Matrix = tuple[tuple[Fraction, ...], ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class SlotQuotient:
    pass


@dataclass(frozen=True)
class SymmetricPowerQuotient:
    child: TensorQuotient
    degree: int


TensorQuotient = SlotQuotient | SymmetricPowerQuotient


@dataclass(frozen=True)
class CovariantTensor:
    name: str
    dimension: int
    rank: int
    components: tuple[Fraction, ...]
    permutation_generators: tuple[Permutation, ...] = ()
    capabilities: frozenset[str] = frozenset()
    relation_certificate: str | None = None
    quotient: TensorQuotient | None = None

    def value(self, index: Index) -> Fraction:
        offset = 0
        for coordinate in index:
            offset = offset * self.dimension + coordinate
        return self.components[offset]


def add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row))
        for left_row, right_row in zip(left, right)
    )


def scale(matrix: Matrix, scalar: Fraction) -> Matrix:
    return tuple(tuple(scalar * value for value in row) for row in matrix)


def multiply(left: Matrix, right: Matrix) -> Matrix:
    dimension = len(left)
    return tuple(
        tuple(
            sum(
                (left[row][index] * right[index][column] for index in range(dimension)),
                Fraction(0),
            )
            for column in range(dimension)
        )
        for row in range(dimension)
    )


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[column][row] for column in range(len(matrix))) for row in range(len(matrix))
    )


def _subtract(left: Matrix, right: Matrix) -> Matrix:
    return add(left, scale(right, Fraction(-1)))


def _inverse(matrix: Matrix) -> Matrix:
    dimension = len(matrix)
    work = [
        [*matrix[row], *(Fraction(row == column) for column in range(dimension))]
        for row in range(dimension)
    ]
    for column in range(dimension):
        selected = next((row for row in range(column, dimension) if work[row][column]), None)
        if selected is None:
            raise ValueError("metric must be nondegenerate")
        work[column], work[selected] = work[selected], work[column]
        pivot = work[column][column]
        work[column] = [value / pivot for value in work[column]]
        for row in range(dimension):
            if row == column or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value for value, pivot_value in zip(work[row], work[column])
            ]
    return tuple(tuple(work[row][dimension:]) for row in range(dimension))


def endomorphism_candidate_labels(dimension: int) -> tuple[str, ...]:
    return tuple(f"E[{row},{column}]" for row in range(dimension) for column in range(dimension))


def endomorphism_candidates(dimension: int) -> tuple[Matrix, ...]:
    return tuple(
        tuple(
            tuple(
                Fraction(target_row == row and target_column == column)
                for target_column in range(dimension)
            )
            for target_row in range(dimension)
        )
        for row in range(dimension)
        for column in range(dimension)
    )


def metric_candidates(metric: Matrix) -> tuple[tuple[str, ...], tuple[Matrix, ...]]:
    dimension = len(metric)
    inverse = _inverse(metric)
    labels: list[str] = []
    candidates: list[Matrix] = []
    for row in range(dimension):
        for column in range(row + 1, dimension):
            alternating = tuple(
                tuple(
                    Fraction(
                        (target_row == row and target_column == column)
                        - (target_row == column and target_column == row)
                    )
                    for target_column in range(dimension)
                )
                for target_row in range(dimension)
            )
            candidate = multiply(inverse, alternating)
            metric_defect = add(
                multiply(_transpose(candidate), metric), multiply(metric, candidate)
            )
            if any(value for defect_row in metric_defect for value in defect_row):
                raise ArithmeticError("metric-seed certificate failed")
            labels.append(f"g^-1 omega[{row},{column}]")
            candidates.append(candidate)
    return tuple(labels), tuple(candidates)


def raw_targets(tensor: CovariantTensor) -> tuple[Index, ...]:
    return tuple(product(range(tensor.dimension), repeat=tensor.rank))


def quotient_rank(quotient: TensorQuotient) -> int:
    if isinstance(quotient, SlotQuotient):
        return 1
    return quotient.degree * quotient_rank(quotient.child)


def quotient_dimension(quotient: TensorQuotient, dimension: int) -> int:
    if isinstance(quotient, SlotQuotient):
        return dimension
    child_dimension = quotient_dimension(quotient.child, dimension)
    return math.comb(child_dimension + quotient.degree - 1, quotient.degree)


def quotient_coordinates(quotient: TensorQuotient, dimension: int) -> tuple[Index, ...]:
    if isinstance(quotient, SlotQuotient):
        return tuple((index,) for index in range(dimension))
    child = quotient_coordinates(quotient.child, dimension)
    return tuple(
        tuple(value for coordinate in combination for value in coordinate)
        for combination in combinations_with_replacement(child, quotient.degree)
    )


def _compose_permutations(left: Permutation, right: Permutation) -> Permutation:
    return tuple(right[left[index]] for index in range(len(left)))


def permutation_group(rank: int, generators: tuple[Permutation, ...]) -> tuple[Permutation, ...]:
    identity = tuple(range(rank))
    for generator in generators:
        if len(generator) != rank or tuple(sorted(generator)) != identity:
            raise ValueError("slot permutation generators must permute every tensor slot")
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            composite = _compose_permutations(current, generator)
            if composite not in group:
                group.add(composite)
                frontier.append(composite)
    return tuple(sorted(group))


def structured_targets(tensor: CovariantTensor) -> tuple[Index, ...]:
    if not tensor.permutation_generators or tensor.relation_certificate is None:
        raise ValueError("structured targets require certified permutation generators")
    group = permutation_group(tensor.rank, tensor.permutation_generators)
    representatives = {
        min(tuple(index[slot] for slot in permutation) for permutation in group)
        for index in product(range(tensor.dimension), repeat=tensor.rank)
    }
    return tuple(sorted(representatives))


def tensor_defect(
    tensor: CovariantTensor,
    candidates: tuple[Matrix, ...],
    target_indices: tuple[Index, ...],
) -> DefectBlock:
    columns: list[tuple[Fraction, ...]] = []
    for candidate in candidates:
        residual: list[Fraction] = []
        for target in target_indices:
            value = Fraction(0)
            for slot in range(tensor.rank):
                for source_coordinate in range(tensor.dimension):
                    source = (*target[:slot], source_coordinate, *target[slot + 1 :])
                    value += candidate[source_coordinate][target[slot]] * tensor.value(source)
            residual.append(value)
        columns.append(tuple(residual))
    return DefectBlock(
        name=f"preserve-{tensor.name}",
        target_labels=tuple(str(index) for index in target_indices),
        columns=tuple(columns),
    )


def endomorphism_bracket(dimension: int) -> CandidateBracket:
    candidate_dimension = dimension**2
    table: list[tuple[tuple[Fraction, ...], ...]] = []
    for a in range(dimension):
        for b in range(dimension):
            row: list[tuple[Fraction, ...]] = []
            for c in range(dimension):
                for d in range(dimension):
                    value = [Fraction(0) for _ in range(candidate_dimension)]
                    if b == c:
                        value[a * dimension + d] += 1
                    if d == a:
                        value[c * dimension + b] -= 1
                    row.append(tuple(value))
            table.append(tuple(row))
    return CandidateBracket(name="endomorphism-commutator", table=tuple(table))


def metric_bracket(metric: Matrix, candidates: tuple[Matrix, ...]) -> CandidateBracket:
    dimension = len(metric)
    table: list[tuple[tuple[Fraction, ...], ...]] = []
    for left in candidates:
        row: list[tuple[Fraction, ...]] = []
        for right in candidates:
            commutator = _subtract(multiply(left, right), multiply(right, left))
            alternating = multiply(metric, commutator)
            row.append(
                tuple(
                    alternating[first][second]
                    for first in range(dimension)
                    for second in range(first + 1, dimension)
                )
            )
        table.append(tuple(row))
    return CandidateBracket(name="metric-skew-commutator", table=tuple(table))


def standard_action(candidates: tuple[Matrix, ...]) -> LinearMap:
    dimension = len(candidates[0])
    return LinearMap(
        name="standard-vector-action",
        target_labels=tuple(
            f"{row},{column}" for row in range(dimension) for column in range(dimension)
        ),
        columns=tuple(
            tuple(value for row in candidate for value in row) for candidate in candidates
        ),
    )


def basis_matrices_json(
    basis: tuple[tuple[Fraction, ...], ...], candidates: tuple[Matrix, ...]
) -> list[list[list[str]]]:
    dimension = len(candidates[0])
    return [
        [
            [
                str(
                    sum(
                        (
                            coefficient * candidate[row][column]
                            for coefficient, candidate in zip(vector, candidates)
                        ),
                        Fraction(0),
                    )
                )
                for column in range(dimension)
            ]
            for row in range(dimension)
        ]
        for vector in basis
    ]


def generated_vectors(
    basis: tuple[tuple[Fraction, ...], ...], candidates: tuple[Matrix, ...]
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(
            sum(
                (
                    coefficient * candidate[row][column]
                    for coefficient, candidate in zip(vector, candidates)
                ),
                Fraction(0),
            )
            for row in range(len(candidates[0]))
            for column in range(len(candidates[0]))
        )
        for vector in basis
    )


def _rank(vectors: tuple[tuple[Fraction, ...], ...]) -> int:
    if not vectors:
        return 0
    work = [list(vector) for vector in vectors]
    pivot_row = 0
    for column in range(len(work[0])):
        selected = next((row for row in range(pivot_row, len(work)) if work[row][column]), None)
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [value / pivot for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def same_span(
    left: tuple[tuple[Fraction, ...], ...], right: tuple[tuple[Fraction, ...], ...]
) -> bool:
    return _rank(left) == _rank(right) == _rank((*left, *right))


def matrix_json(matrix: Matrix) -> list[list[str]]:
    return [[str(value) for value in row] for row in matrix]
