from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

from ._parameterized_contracts import Certificate


Vector = tuple[Fraction, ...]
Matrix = tuple[Vector, ...]


@dataclass(frozen=True)
class ExamCost:
    full_unknowns: int
    reduced_unknowns: int
    law_actions: int


@dataclass(frozen=True)
class ClosureObstruction:
    code: str
    message: str
    required_dimension_at_least: Optional[int] = None
    next_observable: Optional[Vector] = None


@dataclass(frozen=True)
class ClosureResult:
    status: str
    full_dimension: int
    closure_dimension: int
    basis: tuple[Vector, ...] = ()
    reduced_second_order_operator: Matrix = ()
    certificates: tuple[Certificate, ...] = ()
    cost: Optional[ExamCost] = None
    obstruction: Optional[ClosureObstruction] = None

    def project(self, state: Vector) -> Vector:
        if self.status != "closed":
            raise ValueError("A refused construction has no projection.")
        if len(state) != self.full_dimension:
            raise ValueError("State dimension does not match the full model.")
        return tuple(
            sum((weight * value for weight, value in zip(row, state)), Fraction(0))
            for row in self.basis
        )
