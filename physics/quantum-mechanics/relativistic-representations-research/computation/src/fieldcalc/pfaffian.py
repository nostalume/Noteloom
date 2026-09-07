"""Small skew-elimination kernel with an explicit symbolic-cost receipt."""

from sympy import Matrix, simplify, sympify


def pfaffian_elimination(matrix):
    """Return value, update count, and nonzero pivots needing continuation."""
    work = Matrix(matrix)
    value = sympify(1)
    updates = 0
    conditions = []
    for left in range(0, work.rows, 2):
        pivot_column = next(
            (column for column in range(left + 1, work.cols)
             if simplify(work[left, column]) != 0),
            None,
        )
        if pivot_column is None:
            return sympify(0), updates, tuple(conditions)
        if pivot_column != left + 1:
            work.row_swap(left + 1, pivot_column)
            work.col_swap(left + 1, pivot_column)
            value = -value
        pivot = simplify(work[left, left + 1])
        if pivot.is_zero is not False:
            conditions.append(pivot)
        value *= pivot
        for row in range(left + 2, work.rows):
            for column in range(row + 1, work.cols):
                correction = (
                    work[left, row] * work[left + 1, column]
                    - work[left, column] * work[left + 1, row]
                ) / pivot
                work[row, column] = simplify(work[row, column] - correction)
                work[column, row] = -work[row, column]
                updates += 1
    return simplify(value), updates, tuple(dict.fromkeys(conditions))
