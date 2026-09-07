"""Exact Pauli channel use stage from invariant full-operator data."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

import exact_gaussian_matrix as gaussian
from adjoint_algebra import Matrix as RealMatrix
from coefficient_algebra import CoefficientAlgebraError
from coefficient_algebra import construct as construct_coefficient_algebra
from coefficient_algebra import witness as coefficient_algebra_witness


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


Channel = tuple[int, str, Fraction]


def _channel_data(magnitude: Fraction, maximum_level: int) -> list[Channel]:
    return [
        (level, spin, offset)
        for level in range(maximum_level + 1)
        for spin, offset in (
            ("curvature-aligned", 2 * magnitude * level),
            ("curvature-antialigned", 2 * magnitude * (level + 1)),
        )
    ]


def _channels(data: list[Channel]) -> list[dict[str, object]]:
    channels = []
    for level, spin, offset in data:
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


def _axial_coefficient(
    first_order: tuple[gaussian.ComplexMatrix, ...],
    axial: tuple[Fraction, ...],
    magnitude: Fraction,
) -> gaussian.ComplexMatrix:
    axis = tuple(direction / magnitude for direction in axial)
    coefficient = gaussian.linear_combination(axis, first_order)
    if any(
        value != gaussian.scale(coefficient, direction)
        for value, direction in zip(first_order, axis, strict=True)
    ):
        raise PauliChannelError(
            "UnsupportedChannelLowerOrder",
            "first-order transport must be parallel to the curvature-derived axis",
        )
    return coefficient


def _energy_text(linear: Fraction, constant: Fraction) -> str:
    if linear == 0:
        return f"k^2+{gaussian.rational_text(constant)}"
    coefficient = gaussian.rational_text(linear)
    sign = "+" if linear > 0 else ""
    return f"k^2{sign}{coefficient}*k+{gaussian.rational_text(constant)}"


def _transport_channels(
    data: list[Channel], linears: dict[str, Fraction]
) -> list[dict[str, object]]:
    result = []
    for level, spin, constant in data:
        linear = linears[spin]
        momentum_shift = linear / 2
        result.append(
            {
                "orbital_level": level,
                "spin": spin,
                "energy": _energy_text(linear, constant),
                "energy_polynomial": {
                    "quadratic": "1",
                    "linear": gaussian.rational_text(linear),
                    "constant": gaussian.rational_text(constant),
                },
                "completed_square_constant": gaussian.rational_text(constant - momentum_shift**2),
            }
        )
    return result


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
    axial = (curvature[1][2], curvature[2][0], curvature[0][1])
    magnitude = _square_root(sum((entry * entry for entry in axial), Fraction(0)))
    longitudinal = _axial_coefficient(first_order, axial, magnitude)
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
    try:
        algebra = construct_coefficient_algebra(grading, longitudinal)
    except CoefficientAlgebraError as error:
        raise PauliChannelError(error.kind, str(error)) from error
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
    channel_data = _channel_data(magnitude, maximum_level)
    channels = _channels(channel_data)
    aligned, antialigned = algebra.eigenvalues
    linears = {
        "curvature-aligned": aligned,
        "curvature-antialigned": antialigned,
    }
    if aligned == antialigned:
        momentum_shift = aligned / 2
        transport = {
            "linear_coefficient": gaussian.rational_text(aligned),
            "momentum_shift": gaussian.rational_text(momentum_shift),
            "energy_shift": gaussian.rational_text(-(momentum_shift**2)),
        }
    else:
        transport = {
            "sector_linear_coefficients": {
                "curvature_aligned": gaussian.rational_text(aligned),
                "curvature_antialigned": gaussian.rational_text(antialigned),
            }
        }
    return {
        "kind": "spin-resolved-transverse-energy-channels",
        "field_magnitude": gaussian.rational_text(magnitude),
        "parallel_axis": [gaussian.rational_text(entry / magnitude) for entry in axial],
        "projectors": {
            "curvature_aligned": gaussian.serialize(plus),
            "curvature_antialigned": gaussian.serialize(minus),
        },
        "channels": channels,
        "coefficient_algebra": coefficient_algebra_witness(algebra),
        "longitudinal_transport": transport,
        "transport_channels": _transport_channels(channel_data, linears),
        "checks": checks,
    }
