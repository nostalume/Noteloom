"""Visible radial measures and same-object bound/open transforms."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import TYPE_CHECKING, Callable

from sympy import Abs, lambdify, simplify, sympify

from .numeric import integrate
from .rewrite import Refusal

if TYPE_CHECKING:
    from .amplitude import CharacteristicScalarAmplitude


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
    evaluations: int = 0


@dataclass(frozen=True)
class MeasureCompilation:
    measure: "VisibleMeasure | None" = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


@dataclass(frozen=True)
class EventEffectCost:
    baseline_operations: int
    compiled_operations: int
    readout_operations: int = 2

    @property
    def advantage(self) -> bool:
        return self.compiled_operations < self.baseline_operations


@dataclass(frozen=True)
class PreparedEventEffect:
    value: object | None = None
    amplitude_value: object | None = None
    detector_weight: object | None = None
    gauge_residuals: tuple[object, ...] = ()
    cost: EventEffectCost | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


@dataclass(frozen=True)
class PreparedEventMeasureRequest:
    effect: PreparedEventEffect
    parameter: object
    phase_space_density: object
    support: tuple[float, float]
    provenance: str


@dataclass(frozen=True)
class PreparedEventMeasureCompilation:
    measure: "PreparedEventMeasure | None" = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


class PreparedEventMeasure:
    def __init__(self, request: PreparedEventMeasureRequest, density):
        self.request = request
        self.density = density
        identity = f"{request.provenance}|{request.support}|{density}".encode()
        self.measure_id = hashlib.sha256(identity).hexdigest()[:16]
        self._density = lambdify(request.parameter, density, "math")

    def _bounds(self, aperture):
        bounds = self.request.support if aperture is None else aperture
        left, right = bounds
        support_left, support_right = self.request.support
        if left < support_left or right > support_right or right <= left:
            raise ValueError("aperture lies outside the event-measure support")
        return bounds

    def _integrate(self, operation: str, aperture=None) -> TransformResult:
        left, right = self._bounds(aperture)
        result = integrate(self._density, (left, right), 1e-12)
        return TransformResult(
            result.value, result.error, self.measure_id,
            operation, result.evaluations,
        )

    def total_mass(self) -> TransformResult:
        return self._integrate("event-mass")

    def aperture(self, support) -> TransformResult:
        return self._integrate("detector-aperture", support)

    def fraction(self, support) -> TransformResult:
        part = self.aperture(support)
        total = self.total_mass()
        if total.value <= total.error:
            raise ValueError("event measure has no certified positive mass")
        value = part.value / total.value
        error = part.error / total.value + abs(part.value) * total.error / total.value**2
        evaluations = part.evaluations + total.evaluations
        return TransformResult(value, error, self.measure_id, "normalized-aperture", evaluations)


class VisibleMeasure:
    def __init__(self, request: MeasureRequest):
        self.request = request
        identity = f"{request.provenance}|{request.support}".encode()
        self.measure_id = hashlib.sha256(identity).hexdigest()[:16]

    def _integrate(
        self, operation: str, integrand: Callable[[float], float],
        absolute_tolerance: float = 1e-11,
    ) -> TransformResult:
        result = integrate(integrand, self.request.support, absolute_tolerance)
        return TransformResult(
            result.value, result.error, self.measure_id,
            operation, result.evaluations,
        )

    def total_mass(self) -> TransformResult:
        return self._integrate("mass", self.request.weight)

    def resolvent(
        self, spectral_parameter: float, absolute_tolerance: float = 1e-11,
    ) -> TransformResult:
        def integrand(radius: float) -> float:
            denominator = spectral_parameter - self.request.energy(radius)
            if denominator == 0:
                raise ValueError("resolvent parameter lies on the visible spectrum")
            return self.request.weight(radius) / denominator

        return self._integrate("resolvent", integrand, absolute_tolerance)

    def open_event(
        self, time: float, gap: float, absolute_tolerance: float = 1e-11,
    ) -> TransformResult:
        if time < 0:
            raise ValueError("time must be nonnegative")

        def integrand(radius: float) -> float:
            delta = self.request.energy(radius) - gap
            kernel = time * time if abs(delta) < 1e-12 else 4.0 * math.sin(0.5 * time * delta) ** 2 / delta**2
            return self.request.weight(radius) * kernel

        return self._integrate("open-event", integrand, absolute_tolerance)


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


def compile_prepared_event_effect(
    amplitude: "CharacteristicScalarAmplitude",
    detector_weight,
) -> PreparedEventEffect:
    """Construct a positive event weight from an admitted characteristic class."""
    if not amplitude.accepted:
        return PreparedEventEffect(refusal=Refusal(
            "characteristic amplitude is unavailable",
            provenance="prepared scalar-QED event effect",
        ))

    def residual(values):
        return tuple(simplify(value) for value in values)

    endpoints = residual(amplitude.endpoint_generators)
    photons = residual(amplitude.photon_generators)
    transverse = residual(amplitude.transversality_residuals)
    ward = residual(item.residual for item in amplitude.ward_certificates)
    contractions = residual(item.contraction for item in amplitude.ward_certificates)
    checks = (
        (endpoints, "scalar endpoints are not characteristic"),
        (photons, "photon momenta are not characteristic"),
        (transverse, "prepared polarizations are not transverse"),
        (ward + contractions, "amplitude does not descend to the gauge quotient"),
    )
    failed = next(
        ((values, reason) for values, reason in checks
         if any(value != 0 for value in values)),
        None,
    )
    if failed is not None:
        values, reason = failed
        return PreparedEventEffect(
            amplitude_value=amplitude.value,
            gauge_residuals=contractions,
            refusal=Refusal(
                reason,
                residual=values,
                provenance="prepared scalar-QED event effect",
            ),
        )

    detector_weight = sympify(detector_weight)
    if detector_weight.is_nonnegative is not True:
        return PreparedEventEffect(
            amplitude_value=amplitude.value,
            detector_weight=detector_weight,
            gauge_residuals=contractions,
            refusal=Refusal(
                "detector weight must be provably nonnegative",
                residual=(detector_weight,),
                provenance="prepared scalar-QED event effect",
            ),
        )

    readout_operations = 2
    cost = EventEffectCost(
        baseline_operations=amplitude.cost.history_event_terms + readout_operations,
        compiled_operations=amplitude.cost.complete_transition_terms + readout_operations,
        readout_operations=readout_operations,
    )
    return PreparedEventEffect(
        value=simplify(detector_weight * Abs(amplitude.value) ** 2),
        amplitude_value=amplitude.value,
        detector_weight=detector_weight,
        gauge_residuals=contractions,
        cost=cost,
    )


def compile_prepared_event_measure(
    request: PreparedEventMeasureRequest,
) -> PreparedEventMeasureCompilation:
    """Push an admitted event-effect family through a positive shell density."""
    def refuse(reason, residual=()):
        return PreparedEventMeasureCompilation(refusal=Refusal(
            reason, residual=tuple(residual), provenance=request.provenance,
        ))

    if not request.effect.accepted:
        return refuse("prepared event effect is unavailable")
    parameter = request.parameter
    if getattr(parameter, "is_Symbol", False) is not True or parameter.is_real is not True:
        return refuse("event parameter must be one real symbol")
    left, right = request.support
    if not math.isfinite(left) or right <= left:
        return refuse("invalid event-measure support", request.support)
    phase_density = simplify(sympify(request.phase_space_density))
    if phase_density.free_symbols - {parameter}:
        return refuse("phase-space density has unbound symbols", phase_density.free_symbols)
    if phase_density.is_nonnegative is not True:
        return refuse("phase-space density must be provably nonnegative", (phase_density,))
    density = simplify(request.effect.value * phase_density)
    if density.free_symbols - {parameter}:
        return refuse("event effect has unbound symbols", density.free_symbols)
    if density.is_nonnegative is not True:
        return refuse("visible density must be provably nonnegative", (density,))
    return PreparedEventMeasureCompilation(measure=PreparedEventMeasure(request, density))


def curvature_threshold_power(spatial_dimension: int, spin: int) -> int:
    if spatial_dimension < 2 or spin < 0:
        raise ValueError("threshold power requires d>=2 and nonnegative spin")
    return spatial_dimension - 2 + 2 * spin
