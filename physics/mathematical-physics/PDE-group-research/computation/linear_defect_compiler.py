"""Exact kernel compiler for finite typed linear defect blocks.

Problem adapters own the semantic construction of candidate arrows and residual
coordinates. This module owns only their common intersection-of-kernels operation,
its incremental rank ledger, and bounded refusal.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

Vector = tuple[Fraction, ...]


@dataclass(frozen=True)
class DefectBlock:
    """Residual coordinates for every candidate basis arrow.

    ``columns[j][i]`` is coordinate ``i`` of the residual produced by candidate
    ``j``. Target labels retain the semantic meaning of those coordinates.
    """

    name: str
    target_labels: tuple[str, ...]
    columns: tuple[tuple[Fraction | int, ...], ...]


@dataclass(frozen=True)
class LinearMap:
    """A typed linear map represented by candidate-major exact columns."""

    name: str
    target_labels: tuple[str, ...]
    columns: tuple[tuple[Fraction | int, ...], ...]


@dataclass(frozen=True)
class CandidateBracket:
    """Candidate-coordinate bracket table before defect selection."""

    name: str
    table: tuple[tuple[tuple[Fraction | int, ...], ...], ...]


@dataclass(frozen=True)
class DefectBudget:
    maximum_candidate_dimension: int
    maximum_residual_coordinates: int
    maximum_bracket_checks: int = 0


@dataclass(frozen=True)
class DefectLedgerEntry:
    name: str
    target_dimension: int
    residual_rank: int
    rank_drop: int
    kernel_dimension: int
    first_nonzero_candidate: str | None


@dataclass(frozen=True)
class DefectCompilation:
    outcome: str
    candidate_labels: tuple[str, ...]
    kernel_basis: tuple[Vector, ...]
    ledger: tuple[DefectLedgerEntry, ...]
    obstruction_kind: str | None = None
    obstruction_reason: str | None = None
    ineffective_basis: tuple[Vector, ...] = ()
    effective_representatives: tuple[Vector, ...] = ()
    closure_status: str = "not-supplied"
    quotient_bracket_table: tuple[tuple[Vector, ...], ...] = ()
    bracket_checks: int = 0

    @property
    def candidate_dimension(self) -> int:
        return len(self.candidate_labels)

    @property
    def kernel_dimension(self) -> int:
        return len(self.kernel_basis)

    @property
    def effective_dimension(self) -> int:
        return len(self.effective_representatives)


def _nullspace(rows: list[list[Fraction]], columns: int) -> tuple[Vector, ...]:
    reduced = [list(row) for row in rows if any(row)]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(columns):
        selected = next(
            (row for row in range(pivot_row, len(reduced)) if reduced[row][column]), None
        )
        if selected is None:
            continue
        reduced[pivot_row], reduced[selected] = reduced[selected], reduced[pivot_row]
        pivot = reduced[pivot_row][column]
        reduced[pivot_row] = [value / pivot for value in reduced[pivot_row]]
        for row in range(len(reduced)):
            if row == pivot_row or not reduced[row][column]:
                continue
            factor = reduced[row][column]
            reduced[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(reduced[row], reduced[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(reduced):
            break

    free_columns = [column for column in range(columns) if column not in pivot_columns]
    basis: list[Vector] = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -reduced[row][free]
        basis.append(tuple(vector))
    return tuple(basis)


def _unresolved(candidate_labels: tuple[str, ...], kind: str, reason: str) -> DefectCompilation:
    return DefectCompilation(
        outcome="unresolved",
        candidate_labels=candidate_labels,
        kernel_basis=(),
        ledger=(),
        obstruction_kind=kind,
        obstruction_reason=reason,
    )


def _rank(vectors: list[Vector], ambient_dimension: int) -> int:
    if not vectors:
        return 0
    return ambient_dimension - len(
        _nullspace([list(vector) for vector in vectors], ambient_dimension)
    )


def _linear_combination(coefficients: Vector, basis: tuple[Vector, ...]) -> Vector:
    if not basis:
        return ()
    return tuple(
        sum(
            (coefficient * vector[index] for coefficient, vector in zip(coefficients, basis)),
            Fraction(0),
        )
        for index in range(len(basis[0]))
    )


def _in_span(vector: Vector, basis: tuple[Vector, ...]) -> bool:
    if not basis:
        return not any(vector)
    ambient_dimension = len(vector)
    return _rank([*basis, vector], ambient_dimension) == len(basis)


def _coordinates(vector: Vector, basis: tuple[Vector, ...]) -> Vector:
    if not basis:
        if any(vector):
            raise ValueError("a nonzero vector is not in the empty span")
        return ()
    unknowns = len(basis)
    augmented = [
        [*(basis[column][row] for column in range(unknowns)), vector[row]]
        for row in range(len(vector))
    ]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(unknowns):
        selected = next(
            (row for row in range(pivot_row, len(augmented)) if augmented[row][column]), None
        )
        if selected is None:
            continue
        augmented[pivot_row], augmented[selected] = augmented[selected], augmented[pivot_row]
        pivot = augmented[pivot_row][column]
        augmented[pivot_row] = [value / pivot for value in augmented[pivot_row]]
        for row in range(len(augmented)):
            if row == pivot_row or not augmented[row][column]:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
    if len(pivots) != unknowns or any(not any(row[:-1]) and row[-1] for row in augmented):
        raise ValueError("vector is not uniquely represented in the supplied basis")
    result = [Fraction(0) for _ in range(unknowns)]
    for row, pivot in enumerate(pivots):
        result[pivot] = augmented[row][-1]
    return tuple(result)


def _exact_map(mapping: LinearMap, candidate_dimension: int) -> tuple[tuple[Fraction, ...], ...]:
    if not mapping.name:
        raise ValueError("linear map names must be nonempty")
    if len(mapping.columns) != candidate_dimension:
        raise ValueError(
            f"linear map {mapping.name!r} has {len(mapping.columns)} candidate columns; "
            f"expected {candidate_dimension}"
        )
    target_dimension = len(mapping.target_labels)
    if len(set(mapping.target_labels)) != target_dimension:
        raise ValueError(f"linear map {mapping.name!r} target labels must be unique")
    if any(len(column) != target_dimension for column in mapping.columns):
        raise ValueError(f"linear map {mapping.name!r} has an inconsistent target dimension")
    return tuple(tuple(Fraction(value) for value in column) for column in mapping.columns)


def _restricted_kernel(
    mapping: tuple[tuple[Fraction, ...], ...], kernel_basis: tuple[Vector, ...]
) -> tuple[Vector, ...]:
    if not kernel_basis:
        return ()
    target_dimension = len(mapping[0]) if mapping else 0
    restricted_columns = tuple(
        tuple(
            sum(
                (coefficient * mapping[index][target] for index, coefficient in enumerate(vector)),
                Fraction(0),
            )
            for target in range(target_dimension)
        )
        for vector in kernel_basis
    )
    rows = [
        [restricted_columns[column][target] for column in range(len(kernel_basis))]
        for target in range(target_dimension)
    ]
    coefficients = _nullspace(rows, len(kernel_basis))
    return tuple(_linear_combination(vector, kernel_basis) for vector in coefficients)


def _complement(subspace: tuple[Vector, ...], space: tuple[Vector, ...]) -> tuple[Vector, ...]:
    if not space:
        return ()
    ambient_dimension = len(space[0])
    spanning = list(subspace)
    current_rank = _rank(spanning, ambient_dimension)
    representatives: list[Vector] = []
    for vector in space:
        candidate_rank = _rank([*spanning, vector], ambient_dimension)
        if candidate_rank > current_rank:
            representatives.append(vector)
            spanning.append(vector)
            current_rank = candidate_rank
    return tuple(representatives)


def _exact_bracket(
    bracket: CandidateBracket, candidate_dimension: int
) -> tuple[tuple[Vector, ...], ...]:
    if not bracket.name:
        raise ValueError("candidate bracket names must be nonempty")
    if len(bracket.table) != candidate_dimension or any(
        len(row) != candidate_dimension for row in bracket.table
    ):
        raise ValueError("candidate bracket table must be square in the candidate basis")
    if any(len(value) != candidate_dimension for row in bracket.table for value in row):
        raise ValueError("candidate bracket values must use candidate coordinates")
    return tuple(
        tuple(tuple(Fraction(coefficient) for coefficient in value) for value in row)
        for row in bracket.table
    )


def _bracket_vectors(left: Vector, right: Vector, table: tuple[tuple[Vector, ...], ...]) -> Vector:
    dimension = len(left)
    return tuple(
        sum(
            (
                left[i] * right[j] * table[i][j][target]
                for i in range(dimension)
                for j in range(dimension)
            ),
            Fraction(0),
        )
        for target in range(dimension)
    )


def _obstructed(
    base: DefectCompilation,
    kind: str,
    reason: str,
    *,
    ineffective_basis: tuple[Vector, ...] = (),
    effective_representatives: tuple[Vector, ...] = (),
    bracket_checks: int = 0,
) -> DefectCompilation:
    return DefectCompilation(
        outcome="obstructed",
        candidate_labels=base.candidate_labels,
        kernel_basis=base.kernel_basis,
        ledger=base.ledger,
        obstruction_kind=kind,
        obstruction_reason=reason,
        ineffective_basis=ineffective_basis,
        effective_representatives=effective_representatives,
        closure_status="obstructed",
        bracket_checks=bracket_checks,
    )


def compile_defects(
    *,
    candidate_labels: tuple[str, ...],
    blocks: tuple[DefectBlock, ...],
    budget: DefectBudget,
    visible_action: LinearMap | None = None,
    bracket: CandidateBracket | None = None,
) -> DefectCompilation:
    """Intersect exact residual kernels and retain the rank change of each block."""

    if not candidate_labels:
        raise ValueError("candidate_labels must be nonempty")
    if len(set(candidate_labels)) != len(candidate_labels):
        raise ValueError("candidate_labels must be unique")
    if (
        budget.maximum_candidate_dimension <= 0
        or budget.maximum_residual_coordinates < 0
        or budget.maximum_bracket_checks < 0
    ):
        raise ValueError("defect budgets must be positive or zero as appropriate")

    candidate_dimension = len(candidate_labels)
    if candidate_dimension > budget.maximum_candidate_dimension:
        return _unresolved(
            candidate_labels,
            "CandidateBudgetExceeded",
            f"candidate dimension {candidate_dimension} exceeds "
            f"budget {budget.maximum_candidate_dimension}",
        )

    total_target_dimension = sum(len(block.target_labels) for block in blocks)
    if total_target_dimension > budget.maximum_residual_coordinates:
        return _unresolved(
            candidate_labels,
            "ResidualBudgetExceeded",
            f"residual dimension {total_target_dimension} exceeds "
            f"budget {budget.maximum_residual_coordinates}",
        )

    rows: list[list[Fraction]] = []
    ledger: list[DefectLedgerEntry] = []
    previous_kernel_dimension = candidate_dimension
    previous_rank = 0

    for block in blocks:
        if not block.name:
            raise ValueError("defect block names must be nonempty")
        if len(block.columns) != candidate_dimension:
            raise ValueError(
                f"defect block {block.name!r} has {len(block.columns)} candidate columns; "
                f"expected {candidate_dimension}"
            )
        target_dimension = len(block.target_labels)
        if len(set(block.target_labels)) != target_dimension:
            raise ValueError(f"defect block {block.name!r} target labels must be unique")
        if any(len(column) != target_dimension for column in block.columns):
            raise ValueError(f"defect block {block.name!r} has an inconsistent target dimension")

        exact_columns = tuple(
            tuple(Fraction(value) for value in column) for column in block.columns
        )
        block_rows = [
            [exact_columns[column][target] for column in range(candidate_dimension)]
            for target in range(target_dimension)
        ]
        rows.extend(block_rows)
        kernel = _nullspace(rows, candidate_dimension)
        current_rank = candidate_dimension - len(kernel)
        first_nonzero = next(
            (candidate_labels[index] for index, column in enumerate(exact_columns) if any(column)),
            None,
        )
        ledger.append(
            DefectLedgerEntry(
                name=block.name,
                target_dimension=target_dimension,
                residual_rank=current_rank - previous_rank,
                rank_drop=previous_kernel_dimension - len(kernel),
                kernel_dimension=len(kernel),
                first_nonzero_candidate=first_nonzero,
            )
        )
        previous_kernel_dimension = len(kernel)
        previous_rank = current_rank

    kernel_basis = _nullspace(rows, candidate_dimension)
    base = DefectCompilation(
        outcome="exact",
        candidate_labels=candidate_labels,
        kernel_basis=kernel_basis,
        ledger=tuple(ledger),
        effective_representatives=kernel_basis,
    )

    ineffective_basis: tuple[Vector, ...] = ()
    if visible_action is not None:
        exact_visible_action = _exact_map(visible_action, candidate_dimension)
        ineffective_basis = _restricted_kernel(exact_visible_action, kernel_basis)
    effective_representatives = _complement(ineffective_basis, kernel_basis)

    if bracket is None:
        if ineffective_basis:
            return DefectCompilation(
                outcome="unresolved",
                candidate_labels=candidate_labels,
                kernel_basis=kernel_basis,
                ledger=tuple(ledger),
                obstruction_kind="IdealCertificateMissing",
                obstruction_reason="a nonzero ineffective subspace requires a supplied bracket",
                ineffective_basis=ineffective_basis,
                effective_representatives=effective_representatives,
            )
        return DefectCompilation(
            outcome="exact",
            candidate_labels=candidate_labels,
            kernel_basis=kernel_basis,
            ledger=tuple(ledger),
            ineffective_basis=ineffective_basis,
            effective_representatives=effective_representatives,
        )

    table = _exact_bracket(bracket, candidate_dimension)
    maximum_checks = (
        candidate_dimension**2
        + candidate_dimension**3
        + len(kernel_basis) ** 2
        + len(kernel_basis) * len(ineffective_basis)
        + len(effective_representatives) ** 2
    )
    if maximum_checks > budget.maximum_bracket_checks:
        return DefectCompilation(
            outcome="unresolved",
            candidate_labels=candidate_labels,
            kernel_basis=kernel_basis,
            ledger=tuple(ledger),
            obstruction_kind="BracketBudgetExceeded",
            obstruction_reason=(
                f"bracket certification needs {maximum_checks} checks; "
                f"budget is {budget.maximum_bracket_checks}"
            ),
            ineffective_basis=ineffective_basis,
            effective_representatives=effective_representatives,
        )

    checks = 0
    zero = tuple(Fraction(0) for _ in range(candidate_dimension))
    for left in range(candidate_dimension):
        for right in range(candidate_dimension):
            checks += 1
            if (
                tuple(
                    table[left][right][index] + table[right][left][index]
                    for index in range(candidate_dimension)
                )
                != zero
            ):
                return _obstructed(
                    base,
                    "InvalidCandidateBracket",
                    f"{bracket.name} is not antisymmetric on candidates {left},{right}",
                    ineffective_basis=ineffective_basis,
                    effective_representatives=effective_representatives,
                    bracket_checks=checks,
                )
    for left in range(candidate_dimension):
        for middle in range(candidate_dimension):
            for right in range(candidate_dimension):
                checks += 1
                jacobi = tuple(
                    sum(
                        (
                            table[middle][right][index] * table[left][index][target]
                            + table[right][left][index] * table[middle][index][target]
                            + table[left][middle][index] * table[right][index][target]
                            for index in range(candidate_dimension)
                        ),
                        Fraction(0),
                    )
                    for target in range(candidate_dimension)
                )
                if jacobi != zero:
                    return _obstructed(
                        base,
                        "InvalidCandidateBracket",
                        f"{bracket.name} fails the Jacobi identity",
                        ineffective_basis=ineffective_basis,
                        effective_representatives=effective_representatives,
                        bracket_checks=checks,
                    )

    for left in kernel_basis:
        for right in kernel_basis:
            checks += 1
            value = _bracket_vectors(left, right, table)
            if not _in_span(value, kernel_basis):
                return _obstructed(
                    base,
                    "KernelClosureObstruction",
                    f"the {bracket.name} bracket leaves the simultaneous defect kernel",
                    ineffective_basis=ineffective_basis,
                    effective_representatives=effective_representatives,
                    bracket_checks=checks,
                )

    for left in kernel_basis:
        for ineffective in ineffective_basis:
            checks += 1
            value = _bracket_vectors(left, ineffective, table)
            if not _in_span(value, ineffective_basis):
                return _obstructed(
                    base,
                    "IneffectiveSubspaceNotIdeal",
                    "the visible-action kernel is not an ideal in the admissible algebra",
                    ineffective_basis=ineffective_basis,
                    effective_representatives=effective_representatives,
                    bracket_checks=checks,
                )

    combined_basis = (*ineffective_basis, *effective_representatives)
    quotient_table: list[tuple[Vector, ...]] = []
    for left in effective_representatives:
        row: list[Vector] = []
        for right in effective_representatives:
            checks += 1
            coordinates = _coordinates(_bracket_vectors(left, right, table), combined_basis)
            row.append(coordinates[len(ineffective_basis) :])
        quotient_table.append(tuple(row))

    return DefectCompilation(
        outcome="exact",
        candidate_labels=candidate_labels,
        kernel_basis=kernel_basis,
        ledger=tuple(ledger),
        ineffective_basis=ineffective_basis,
        effective_representatives=effective_representatives,
        closure_status="closed",
        quotient_bracket_table=tuple(quotient_table),
        bracket_checks=checks,
    )
