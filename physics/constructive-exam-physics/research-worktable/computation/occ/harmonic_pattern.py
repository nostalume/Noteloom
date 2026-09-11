"""Exact bounded spatial patterns derived from a harmonic response."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sympy import (
    Expr,
    FiniteSet,
    Interval,
    Max,
    Symbol,
    default_sort_key,
    diff,
    simplify,
    solveset,
    sympify,
)

from .harmonic import phasor_magnitude_squared
from .records import Certificate


@dataclass(frozen=True)
class SpatialHarmonicRequest:
    """A generated phasor and a bounded real coordinate interval."""

    phasor: Expr
    coordinate: Symbol
    lower: Expr
    upper: Expr
    max_points: int = 64

    def __post_init__(self) -> None:
        phasor = sympify(self.phasor)
        lower = sympify(self.lower)
        upper = sympify(self.upper)
        if (
            not isinstance(self.coordinate, Symbol)
            or self.coordinate.is_real is not True
        ):
            raise TypeError("The spatial coordinate must be a real symbol.")
        if self.coordinate not in phasor.free_symbols:
            raise ValueError("The spatial phasor must depend on its coordinate.")
        if lower.is_real is not True or upper.is_real is not True:
            raise ValueError("Spatial bounds must be explicitly real.")
        if simplify(upper - lower).is_positive is not True:
            raise ValueError("The upper spatial bound must exceed the lower bound.")
        if (
            not isinstance(self.max_points, int)
            or isinstance(self.max_points, bool)
            or self.max_points < 1
        ):
            raise ValueError("max_points must be a positive integer.")
        object.__setattr__(self, "phasor", phasor)
        object.__setattr__(self, "lower", lower)
        object.__setattr__(self, "upper", upper)


@dataclass(frozen=True)
class SpatialHarmonicObstruction:
    code: str
    message: str
    next_action: str = ""


@dataclass(frozen=True)
class SpatialHarmonicResult:
    status: str
    request: SpatialHarmonicRequest
    magnitude_squared: Optional[Expr] = None
    nodes: tuple[Expr, ...] = ()
    antinodes: tuple[Expr, ...] = ()
    maximum_magnitude_squared: Optional[Expr] = None
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[SpatialHarmonicObstruction] = None


def _refused(
    request: SpatialHarmonicRequest,
    code: str,
    message: str,
    next_action: str,
) -> SpatialHarmonicResult:
    return SpatialHarmonicResult(
        status="refused",
        request=request,
        obstruction=SpatialHarmonicObstruction(code, message, next_action),
    )


def construct_spatial_harmonic_pattern(
    request: SpatialHarmonicRequest,
) -> SpatialHarmonicResult:
    """Certify finite nodes and global antinodes on a bounded interval."""

    coordinate = request.coordinate
    magnitude_squared = phasor_magnitude_squared(request.phasor)
    domain = Interval(request.lower, request.upper)
    nodes = solveset(magnitude_squared, coordinate, domain=domain)
    stationary = solveset(
        diff(magnitude_squared, coordinate), coordinate, domain=domain
    )
    if not isinstance(nodes, FiniteSet) or not isinstance(stationary, FiniteSet):
        return _refused(
            request,
            "nonfinite_spatial_pattern",
            "Exact node or stationary-point construction did not produce a finite set.",
            "Restrict the coordinate interval or use a dedicated periodic-set result.",
        )
    candidates = set(stationary) | {request.lower, request.upper}
    if len(candidates) > request.max_points:
        return _refused(
            request,
            "spatial_point_budget_exceeded",
            "The finite spatial pattern exceeds the declared point budget.",
            "Raise max_points or shorten the admitted interval.",
        )
    values = {
        point: simplify(magnitude_squared.subs(coordinate, point))
        for point in candidates
    }
    maximum = simplify(Max(*values.values()))
    if maximum.has(Max):
        return _refused(
            request,
            "unordered_spatial_extrema",
            "The exact parameter assumptions do not order the stationary amplitudes.",
            "Declare sufficient real sign assumptions or partition the parameter domain.",
        )
    antinodes = []
    for point, value in values.items():
        comparison = simplify(value - maximum)
        equal = comparison == 0 or comparison.equals(0) is True
        if equal:
            antinodes.append(point)
        elif comparison.is_negative is not True:
            return _refused(
                request,
                "unordered_spatial_extrema",
                "A candidate amplitude cannot be ordered against the exact maximum.",
                "Declare sufficient real sign assumptions or partition the domain.",
            )
    ordered_nodes = tuple(sorted(nodes, key=default_sort_key))
    ordered_antinodes = tuple(sorted(antinodes, key=default_sort_key))
    certificates = (
        Certificate(
            "spatial_nodes_zero",
            all(
                simplify(magnitude_squared.subs(coordinate, point)) == 0
                for point in ordered_nodes
            ),
            f"Squared magnitude vanishes at {ordered_nodes}.",
        ),
        Certificate(
            "spatial_antinodes_maximal",
            all(simplify(values[point] - maximum) == 0 for point in ordered_antinodes),
            f"Squared magnitude equals {maximum} at {ordered_antinodes}.",
        ),
    )
    if not all(certificate.passed for certificate in certificates):
        return SpatialHarmonicResult(
            status="refused",
            request=request,
            magnitude_squared=magnitude_squared,
            nodes=ordered_nodes,
            antinodes=ordered_antinodes,
            maximum_magnitude_squared=maximum,
            certificates=certificates,
            obstruction=SpatialHarmonicObstruction(
                "spatial_pattern_recovery_failed",
                "The finite pattern failed a required exact certificate.",
                "Inspect coordinate assumptions and the generated phasor.",
            ),
        )
    return SpatialHarmonicResult(
        status="constructed",
        request=request,
        magnitude_squared=magnitude_squared,
        nodes=ordered_nodes,
        antinodes=ordered_antinodes,
        maximum_magnitude_squared=maximum,
        certificates=certificates,
    )
