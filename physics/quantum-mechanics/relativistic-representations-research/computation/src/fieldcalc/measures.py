"""Visible radial measures and same-object bound/open transforms."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Callable

from scipy.integrate import quad

from .rewrite import Refusal


@dataclass(frozen=True)
class MeasureRequest:
    weight: Callable[[float], float]
    energy: Callable[[float], float]
    support: tuple[float, float]
    provenance: str
    monotone: bool | None = None


@dataclass(frozen=True)
class TransformResult:
    value: float
    error: float
    measure_id: str
    operation: str


@dataclass(frozen=True)
class MeasureCompilation:
    measure: "VisibleMeasure | None" = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


class VisibleMeasure:
    def __init__(self, request: MeasureRequest):
        self.request = request
        identity = f"{request.provenance}|{request.support}".encode()
        self.measure_id = hashlib.sha256(identity).hexdigest()[:16]

    def _integrate(self, operation: str, integrand: Callable[[float], float]) -> TransformResult:
        value, error = quad(
            integrand,
            self.request.support[0],
            self.request.support[1],
            epsabs=1e-11,
            epsrel=1e-11,
            limit=300,
        )
        return TransformResult(value, error, self.measure_id, operation)

    def total_mass(self) -> TransformResult:
        return self._integrate("mass", self.request.weight)

    def resolvent(self, spectral_parameter: float) -> TransformResult:
        def integrand(radius: float) -> float:
            denominator = spectral_parameter - self.request.energy(radius)
            if denominator == 0:
                raise ValueError("resolvent parameter lies on the visible spectrum")
            return self.request.weight(radius) / denominator

        return self._integrate("resolvent", integrand)

    def open_event(self, time: float, gap: float) -> TransformResult:
        if time < 0:
            raise ValueError("time must be nonnegative")

        def integrand(radius: float) -> float:
            delta = self.request.energy(radius) - gap
            kernel = time * time if abs(delta) < 1e-12 else 4.0 * math.sin(0.5 * time * delta) ** 2 / delta**2
            return self.request.weight(radius) * kernel

        return self._integrate("open-event", integrand)


def _is_monotone(request: MeasureRequest, samples: int = 65) -> bool:
    if request.monotone is not None:
        return request.monotone
    left, right = request.support
    if not math.isfinite(left) or not math.isfinite(right) or right <= left:
        return False
    values = [request.energy(left + (right - left) * index / (samples - 1)) for index in range(samples)]
    differences = [right_value - left_value for left_value, right_value in zip(values, values[1:])]
    return all(value >= 0 for value in differences) or all(value <= 0 for value in differences)


def compile_visible_measure(request: MeasureRequest) -> MeasureCompilation:
    left, right = request.support
    if left < 0 or right <= left:
        return MeasureCompilation(refusal=Refusal("invalid radial support", provenance=request.provenance))
    if not _is_monotone(request):
        return MeasureCompilation(refusal=Refusal("energy map is not monotone", provenance=request.provenance))
    return MeasureCompilation(measure=VisibleMeasure(request))


def curvature_threshold_power(spatial_dimension: int, spin: int) -> int:
    if spatial_dimension < 2 or spin < 0:
        raise ValueError("threshold power requires d>=2 and nonnegative spin")
    return spatial_dimension - 2 + 2 * spin
