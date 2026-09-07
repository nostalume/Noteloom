"""Admit invariant first/second off-block differential operators exactly."""

from __future__ import annotations

from dataclasses import dataclass

import exact_gaussian_matrix as gaussian
from simple_block_pde import IrreducibleModel


class OffBlockDifferentialError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class OffBlockDifferentialJet:
    projector: gaussian.ComplexMatrix
    first_operator: gaussian.ComplexMatrix
    second_operator: gaussian.ComplexMatrix
    source: str
    checks: dict[str, bool]


def construct_off_block_differential(
    model: IrreducibleModel,
    projector: gaussian.ComplexMatrix,
    first_operator: gaussian.ComplexMatrix,
    second_operator: gaussian.ComplexMatrix,
    source: str,
) -> OffBlockDifferentialJet:
    ambient_dimension = len(model.selected_projector)
    matrices = (projector, first_operator, second_operator)
    if any(
        len(value) != ambient_dimension or any(len(row) != ambient_dimension for row in value)
        for value in matrices
    ):
        raise OffBlockDifferentialError(
            "OffBlockJetDimensionMismatch",
            "projector and off-block arrows must have the selected carrier dimension",
        )
    if projector != model.selected_projector:
        raise OffBlockDifferentialError(
            "ProjectorModelMismatch",
            "off-block projector differs from the selected G10 block",
        )
    zero = gaussian.zero(ambient_dimension)
    checks = {
        "projector_matches_model": projector == model.selected_projector,
        "projector_is_hermitian": gaussian.is_hermitian(projector),
        "projector_is_idempotent": gaussian.multiply(projector, projector) == projector,
        "first_arrow_is_off_block": gaussian.multiply(projector, first_operator) == zero
        and gaussian.multiply(first_operator, projector) == first_operator,
        "second_arrow_is_off_block": gaussian.multiply(projector, second_operator) == zero
        and gaussian.multiply(second_operator, projector) == second_operator,
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise OffBlockDifferentialError(
            "OffBlockDifferentialResidual", f"off-block differential fails at {failed}"
        )
    if not source:
        raise OffBlockDifferentialError(
            "MissingDifferentialProvenance", "off-block differential source must be named"
        )
    return OffBlockDifferentialJet(projector, first_operator, second_operator, source, checks)
