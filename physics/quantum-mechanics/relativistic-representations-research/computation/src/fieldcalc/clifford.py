"""Generate abstract Clifford words and representation-free traces."""

from dataclasses import dataclass
from math import comb, prod

from sympy import ImmutableMatrix, Matrix, conjugate, simplify, sympify

from .pfaffian import pfaffian_elimination


@dataclass(frozen=True)
class CliffordOperator:
    terms: tuple[tuple[object, tuple[ImmutableMatrix, ...]], ...]

    def __add__(self, other):
        return _operator(self.terms + other.terms)

    def __mul__(self, other):
        return _operator(
            (left * right, left_word + right_word)
            for left, left_word in self.terms
            for right, right_word in other.terms
        )

    def __rmul__(self, coefficient):
        return _operator(
            (sympify(coefficient) * value, word) for value, word in self.terms
        )

    def adjoint(self):
        return _operator(
            (conjugate(value), tuple(reversed(word)))
            for value, word in self.terms
        )


@dataclass(frozen=True)
class CliffordTrace:
    value: object
    word_terms: int
    pairing_terms: int
    recurrence_updates: int = 0
    pfaffian_update_bound: int = 0
    elimination_updates: int = 0
    pivot_conditions: tuple[object, ...] = ()
    normal_form_terms: int = 0
    contraction_updates: int = 0
    normal_form_residual: object | None = None


def _operator(items) -> CliffordOperator:
    merged = {}
    for coefficient, word in items:
        word = tuple(ImmutableMatrix(vector) for vector in word)
        merged[word] = simplify(merged.get(word, 0) + coefficient)
    return CliffordOperator(tuple(
        (coefficient, word)
        for word, coefficient in merged.items()
        if coefficient != 0
    ))


def clifford_scalar(value) -> CliffordOperator:
    return _operator(((sympify(value), ()),))


def clifford_vector(vector) -> CliffordOperator:
    return _operator(((sympify(1), (ImmutableMatrix(vector),)),))


def clifford_trace(operator: CliffordOperator, metric) -> CliffordTrace:
    """Evaluate the parity-even normalized trace from {C(v),C(w)}=-2<v,w>."""
    metric = ImmutableMatrix(metric)
    cache = {(): sympify(1)}
    updates = 0

    def word_trace(word):
        nonlocal updates
        if len(word) % 2:
            return sympify(0)
        if word in cache:
            return cache[word]
        first = word[0]
        value = 0
        for index in range(1, len(word)):
            updates += 1
            remainder = word[1:index] + word[index + 1:]
            pairing = -(first.T * metric * word[index])[0]
            value += (-1) ** (index + 1) * pairing * word_trace(remainder)
        cache[word] = simplify(value)
        return cache[word]

    value = 0
    words = 0
    pairings = 0
    pfaffian_bound = 0
    for coefficient, word in operator.terms:
        if len(word) % 2 == 0:
            value += coefficient * word_trace(word)
            words += 1
            pairings += prod(range(len(word) - 1, 0, -2)) if word else 1
            pfaffian_bound += sum(
                comb(size, 2) for size in range(len(word) - 2, 0, -2)
            )
    return CliffordTrace(
        simplify(value), words, pairings, recurrence_updates=updates,
        pfaffian_update_bound=pfaffian_bound,
    )


def clifford_trace_pfaffian(operator: CliffordOperator, metric) -> CliffordTrace:
    """Compile each even Clifford word to one invariant Pfaffian."""
    metric = ImmutableMatrix(metric)
    value = 0
    words = 0
    pairings = 0
    updates = 0
    conditions = []
    for coefficient, word in operator.terms:
        if len(word) % 2:
            continue
        size = len(word)
        pairing_matrix = Matrix.zeros(size)
        for row in range(size):
            for column in range(row + 1, size):
                pairing = simplify(-(word[row].T * metric * word[column])[0])
                pairing_matrix[row, column] = pairing
                pairing_matrix[column, row] = -pairing
        pfaffian, word_updates, word_conditions = pfaffian_elimination(
            pairing_matrix
        )
        value += coefficient * pfaffian
        words += 1
        pairings += prod(range(size - 1, 0, -2)) if word else 1
        updates += word_updates
        conditions.extend(word_conditions)
    return CliffordTrace(
        simplify(value), words, pairings,
        pfaffian_update_bound=updates,
        elimination_updates=updates,
        pivot_conditions=tuple(dict.fromkeys(conditions)),
    )
