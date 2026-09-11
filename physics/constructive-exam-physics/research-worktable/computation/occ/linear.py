from collections.abc import Sequence
from fractions import Fraction
from typing import Optional

from .records import (
    Certificate,
    ClosureObstruction,
    ClosureResult,
    ExamCost,
    Matrix,
    Vector,
)


def _fraction(value: object) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("Boolean values are not rational coefficients.")
    if isinstance(value, (int, Fraction)):
        return Fraction(value)
    raise TypeError("The exact constructor accepts integer or Fraction coefficients.")


def _matrix_and_target(
    restoring_map: Sequence[Sequence[object]],
    observable: Sequence[object],
) -> tuple[Matrix, Vector]:
    if isinstance(restoring_map, (str, bytes)) or not restoring_map:
        raise ValueError("The restoring map must be a nonempty square matrix.")
    matrix = tuple(tuple(_fraction(entry) for entry in row) for row in restoring_map)
    dimension = len(matrix)
    if any(len(row) != dimension for row in matrix):
        raise ValueError("The restoring map must be square.")
    target = tuple(_fraction(entry) for entry in observable)
    if len(target) != dimension:
        raise ValueError("The observable and restoring map dimensions must match.")
    return matrix, target


def _transpose_action(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(
            (matrix[row][column] * vector[row] for row in range(len(matrix))),
            Fraction(0),
        )
        for column in range(len(matrix))
    )


def _linear_combination(basis: list[Vector], coefficients: Vector) -> Vector:
    return tuple(
        sum(
            (
                coefficients[index] * basis[index][component]
                for index in range(len(basis))
            ),
            Fraction(0),
        )
        for component in range(len(basis[0]))
    )


def _coordinates(basis: list[Vector], candidate: Vector) -> Optional[Vector]:
    variable_count = len(basis)
    augmented = [
        [basis[column][row] for column in range(variable_count)] + [candidate[row]]
        for row in range(len(candidate))
    ]
    pivot_rows: list[int] = []
    next_row = 0
    for column in range(variable_count):
        pivot = next(
            (row for row in range(next_row, len(augmented)) if augmented[row][column]),
            None,
        )
        if pivot is None:
            raise RuntimeError("The maintained closure basis lost independence.")
        augmented[next_row], augmented[pivot] = augmented[pivot], augmented[next_row]
        scale = augmented[next_row][column]
        augmented[next_row] = [entry / scale for entry in augmented[next_row]]
        for row in range(len(augmented)):
            if row == next_row:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry in zip(augmented[row], augmented[next_row])
                ]
        pivot_rows.append(next_row)
        next_row += 1

    if any(
        all(row[column] == 0 for column in range(variable_count)) and row[-1] != 0
        for row in augmented
    ):
        return None
    return tuple(augmented[pivot_rows[column]][-1] for column in range(variable_count))


def _refused(
    dimension: int,
    closure_dimension: int,
    law_actions: int,
    obstruction: ClosureObstruction,
) -> ClosureResult:
    return ClosureResult(
        status="refused",
        full_dimension=dimension,
        closure_dimension=closure_dimension,
        cost=ExamCost(dimension, closure_dimension, law_actions),
        obstruction=obstruction,
    )


def construct_observable_closure(
    restoring_map: Sequence[Sequence[object]],
    observable: Sequence[object],
    *,
    max_dimension: Optional[int] = None,
) -> ClosureResult:
    """Construct the exact observable closure for x'' = -A x.

    The coefficient domain is rational. Basis rows are observable covectors; the
    returned reduced operator R satisfies y'' = -R y for y_i = q_i^T x.
    """
    matrix, target = _matrix_and_target(restoring_map, observable)
    dimension = len(matrix)
    if all(entry == 0 for entry in target):
        return _refused(
            dimension,
            0,
            0,
            ClosureObstruction(
                code="zero_observable",
                message="The zero covector does not define an exam observable.",
            ),
        )
    if max_dimension is not None and (
        not isinstance(max_dimension, int)
        or isinstance(max_dimension, bool)
        or max_dimension < 1
    ):
        raise ValueError("max_dimension must be a positive integer or None.")

    basis = [target]
    action_columns: list[Vector] = []
    law_actions = 0
    index = 0
    while index < len(basis):
        candidate = _transpose_action(matrix, basis[index])
        law_actions += 1
        coefficients = _coordinates(basis, candidate)
        if coefficients is None:
            if max_dimension is not None and len(basis) >= max_dimension:
                return _refused(
                    dimension,
                    len(basis),
                    law_actions,
                    ClosureObstruction(
                        code="closure_budget_exceeded",
                        message=(
                            "Applying the law produced an independent observable "
                            "outside the declared exam budget."
                        ),
                        required_dimension_at_least=len(basis) + 1,
                        next_observable=candidate,
                    ),
                )
            action_columns = [column + (Fraction(0),) for column in action_columns]
            basis.append(candidate)
            coefficients = (Fraction(0),) * (len(basis) - 1) + (Fraction(1),)
        action_columns.append(coefficients)
        index += 1

    reduced_operator = tuple(action_columns)
    closure_passed = all(
        _transpose_action(matrix, basis[index])
        == _linear_combination(basis, action_columns[index])
        for index in range(len(basis))
    )
    certificates = (
        Certificate(
            name="target_is_first_coordinate",
            passed=basis[0] == target,
            witness="The first reduced coordinate is the requested observable.",
        ),
        Certificate(
            name="adjoint_action_closes",
            passed=closure_passed,
            witness=(
                "Every law action on a retained observable is reconstructed "
                "exactly in the retained basis."
            ),
        ),
    )
    return ClosureResult(
        status="closed",
        full_dimension=dimension,
        closure_dimension=len(basis),
        basis=tuple(basis),
        reduced_second_order_operator=reduced_operator,
        certificates=certificates,
        cost=ExamCost(dimension, len(basis), law_actions),
    )
