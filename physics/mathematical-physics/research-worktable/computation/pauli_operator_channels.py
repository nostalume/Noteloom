"""Exact Pauli channel use stage from invariant full-operator data."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

import exact_gaussian_matrix as gaussian
from adjoint_algebra import Matrix as RealMatrix


class PauliChannelError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def _square_root(value: Fraction) -> Fraction:
    if value <= 0:
        raise PauliChannelError("CurvatureRankObstruction", "curvature norm must be positive")
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator**2 != value.numerator or denominator**2 != value.denominator:
        raise PauliChannelError(
            "CurvatureNormObstruction", "the exact curvature norm is not rational"
        )
    return Fraction(numerator, denominator)


def _channels(magnitude: Fraction, maximum_level: int) -> list[dict[str, object]]:
    channels: list[dict[str, object]] = []
    for level in range(maximum_level + 1):
        for spin, offset in (
            ("curvature-aligned", 2 * magnitude * level),
            ("curvature-antialigned", 2 * magnitude * (level + 1)),
        ):
            text = gaussian.rational_text(offset)
            channels.append(
                {
                    "orbital_level": level,
                    "spin": spin,
                    "energy": f"k^2+{text}",
                    "energy_offset": text,
                }
            )
    return channels


def construct(
    metric: RealMatrix,
    links: tuple[gaussian.ComplexMatrix, ...],
    curvature: RealMatrix,
    first_order: tuple[gaussian.ComplexMatrix, ...],
    zero_order: gaussian.ComplexMatrix,
    maximum_level: int,
) -> dict[str, object]:
    identity_metric = tuple(
        tuple(Fraction(row == column) for column in range(3)) for row in range(3)
    )
    if len(metric) != 3 or metric != identity_metric or len(links) != 3:
        raise PauliChannelError(
            "PauliUseOutsideDomain", "the channel use stage currently requires Euclidean rank three"
        )
    if any(value != gaussian.zero(len(zero_order)) for value in first_order):
        raise PauliChannelError(
            "UnsupportedChannelLowerOrder",
            "nonzero first-order matrices require a different reduced channel rule",
        )
    axial = (curvature[1][2], curvature[2][0], curvature[0][1])
    magnitude = _square_root(sum((entry * entry for entry in axial), Fraction(0)))
    clifford_curvature = gaussian.zero(len(zero_order))
    for left in range(3):
        for right in range(left + 1, 3):
            clifford_curvature = gaussian.add(
                clifford_curvature,
                gaussian.scale(
                    gaussian.multiply(links[left], links[right]), curvature[left][right]
                ),
            )
    grading = gaussian.scale(
        clifford_curvature,
        gaussian.Gaussian(Fraction(0), Fraction(-1, 1) / magnitude),
    )
    unit = gaussian.identity(len(zero_order))
    plus = gaussian.scale(gaussian.add(unit, grading), Fraction(1, 2))
    minus = gaussian.scale(
        gaussian.add(unit, gaussian.scale(grading, Fraction(-1))), Fraction(1, 2)
    )
    checks = {
        "curvature_grading_hermitian": gaussian.is_hermitian(grading),
        "curvature_grading_involutive": gaussian.multiply(grading, grading) == unit,
        "zeroth_order_pauli_factorization": zero_order == gaussian.scale(grading, -magnitude),
        "aligned_projector_idempotent": gaussian.multiply(plus, plus) == plus,
        "antialigned_projector_idempotent": gaussian.multiply(minus, minus) == minus,
        "projectors_orthogonal": gaussian.multiply(plus, minus) == gaussian.zero(len(unit)),
        "projectors_resolve_identity": gaussian.add(plus, minus) == unit,
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise PauliChannelError(
            "PauliFactorizationResidual", f"full operator use fails at {failed}"
        )
    return {
        "kind": "spin-resolved-transverse-energy-channels",
        "field_magnitude": gaussian.rational_text(magnitude),
        "parallel_axis": [gaussian.rational_text(entry / magnitude) for entry in axial],
        "projectors": {
            "curvature_aligned": gaussian.serialize(plus),
            "curvature_antialigned": gaussian.serialize(minus),
        },
        "channels": _channels(magnitude, maximum_level),
        "checks": checks,
    }
