"""Compile Clifford words into a finite exterior-grade normal form."""

from dataclasses import dataclass
from functools import lru_cache

from sympy import ImmutableMatrix, cancel, conjugate, sympify

from .rewrite import Refusal


@dataclass(frozen=True)
class ExteriorOperator:
    terms: tuple[tuple[int, object], ...]
    diagonal: tuple[object, ...]

    @property
    def term_count(self) -> int:
        return len(self.terms)

    @property
    def scalar_part(self):
        return dict(self.terms).get(0, sympify(0))

    def adjoint(self):
        items = (
            (
                mask,
                (-1) ** (mask.bit_count() * (mask.bit_count() - 1) // 2)
                * conjugate(value),
            )
            for mask, value in self.terms
        )
        return _operator(items, diagonal=self.diagonal)


@dataclass(frozen=True)
class ExteriorProduct:
    operator: ExteriorOperator
    product_updates: int


@dataclass(frozen=True)
class ExteriorCompilation:
    operator: ExteriorOperator | None = None
    product_updates: int = 0
    relation_residual: object | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def _operator(items, *, diagonal) -> ExteriorOperator:
    merged = {}
    for mask, value in items:
        merged[mask] = merged.get(mask, 0) + value
    canonical = ((mask, cancel(value)) for mask, value in sorted(merged.items()))
    return ExteriorOperator(
        tuple((mask, value) for mask, value in canonical if value != 0),
        tuple(diagonal),
    )


def exterior_product(left: ExteriorOperator, right: ExteriorOperator):
    if left.diagonal != right.diagonal:
        raise ValueError("exterior products require one admitted frame")
    diagonal = left.diagonal
    terms = []
    for left_mask, left_value in left.terms:
        for right_mask, right_value in right.terms:
            swaps = sum(
                (right_mask & ((1 << index) - 1)).bit_count()
                for index in range(len(diagonal))
                if left_mask & (1 << index)
            )
            overlap = left_mask & right_mask
            coefficient = (-1) ** swaps * left_value * right_value
            for index, square in enumerate(diagonal):
                if overlap & (1 << index):
                    coefficient *= square
            terms.append((left_mask ^ right_mask, coefficient))
    return ExteriorProduct(
        _operator(terms, diagonal=diagonal), len(left.terms) * len(right.terms)
    )


def _scalar(value, diagonal):
    return _operator(((0, sympify(value)),), diagonal=diagonal)


def _vector(vector, diagonal):
    vector = ImmutableMatrix(vector)
    return _operator(
        ((1 << index, value) for index, value in enumerate(vector)),
        diagonal=diagonal,
    )


@lru_cache(maxsize=None)
def _relation_residual(diagonal):
    basis = tuple(
        _operator(((1 << index, 1),), diagonal=diagonal)
        for index in range(len(diagonal))
    )
    for row, left in enumerate(basis):
        for column, right in enumerate(basis):
            forward = exterior_product(left, right).operator
            reverse = exterior_product(right, left).operator
            target = 2 * diagonal[row] if row == column else 0
            residual = _operator(
                (*forward.terms, *reverse.terms, (0, -target)),
                diagonal=diagonal,
            )
            if residual.terms:
                return residual.terms
    return sympify(0)


def exterior_sum(*operators):
    diagonal = operators[0].diagonal
    if any(operator.diagonal != diagonal for operator in operators):
        raise ValueError("exterior sums require one admitted frame")
    return _operator(
        (term for operator in operators for term in operator.terms),
        diagonal=diagonal,
    )


def exterior_scale(value, operator):
    return _operator(
        ((mask, value * coefficient) for mask, coefficient in operator.terms),
        diagonal=operator.diagonal,
    )


def compile_exterior_normal_form(operator, metric) -> ExteriorCompilation:
    """Quotient word syntax by the Clifford relation in an orthogonal frame."""
    metric = ImmutableMatrix(metric)
    provenance = "exterior-grade Clifford quotient"
    if metric.rows != metric.cols:
        return ExteriorCompilation(refusal=Refusal(
            "Clifford metric must be square", provenance=provenance,
        ))
    if any(metric[row, column] != 0 for row in range(metric.rows)
           for column in range(metric.cols) if row != column):
        return ExteriorCompilation(refusal=Refusal(
            "exterior backend requires an admitted orthogonal frame",
            provenance=provenance,
        ))
    if any(
        ImmutableMatrix(vector).shape != (metric.rows, 1)
        for _, word in operator.terms for vector in word
    ):
        return ExteriorCompilation(refusal=Refusal(
            "Clifford vector dimension does not match the frame",
            provenance=provenance,
        ))
    diagonal = tuple(-metric[index, index] for index in range(metric.rows))
    result = _scalar(0, diagonal)
    updates = 0
    for coefficient, word in operator.terms:
        lowered = _scalar(coefficient, diagonal)
        for vector in word:
            product = exterior_product(lowered, _vector(vector, diagonal))
            lowered = product.operator
            updates += product.product_updates
        result = exterior_sum(result, lowered)
    return ExteriorCompilation(result, updates, _relation_residual(diagonal))
