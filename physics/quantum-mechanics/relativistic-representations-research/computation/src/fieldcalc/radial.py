"""Positive radial channels compiled into finite departures and transforms."""

from dataclasses import dataclass
import math
from typing import Callable

from .departure import (
    DepartureRequest,
    FockState,
    MatterBosonVertex,
    compile_departure,
)
from .numeric import Quadrature, integrate
from .rewrite import Refusal


@dataclass(frozen=True)
class RadialData:
    amplitude: Callable[[float], complex | float]
    energy: Callable[[float], float]
    threshold: float
    level_gap: float
    support: tuple[float, float]
    provenance: str
    mass_operation: Callable[[float, float], Quadrature] | None = None
    monotone_energy: bool = True

    def weight(self, radius: float) -> float:
        return 4.0 * math.pi * radius**2 * abs(self.amplitude(radius)) ** 2

    def mass(self, left: float, right: float, tolerance: float) -> Quadrature:
        if self.mass_operation is not None:
            return self.mass_operation(left, right)
        return integrate(self.weight, (left, right), tolerance)

    def measure_request(self):
        from .measures import MeasureRequest

        return MeasureRequest(
            self.weight, self.energy, self.support, self.provenance,
            monotone=self.monotone_energy,
        )


@dataclass(frozen=True)
class RadialDepartureRequest:
    data: RadialData
    radial_cutoff: float
    cell_count: int
    provenance: str
    resource_budget: int
    absolute_tolerance: float = 1e-13


@dataclass(frozen=True)
class RadialTransform:
    value: float
    error_bound: float
    variation_bound: float
    moment_bound: float
    tail_bound: float
    measure_id: str
    operation: str


@dataclass(frozen=True)
class RadialDepartureCompilation:
    radial: "FiniteRadialDeparture | None" = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


class FiniteRadialDeparture:
    def __init__(
        self, request, departure_compilation, cell_edges, cell_masses,
        cell_energies, mass_error_bound, tail_mass, tail_mass_bound,
        energy_variation, centering_error_bound,
        centered_second_moment_bound, moment_evaluations,
        continuum_measure_id,
    ):
        self.request = request
        self.departure_compilation = departure_compilation
        self.departure = departure_compilation.departure
        self.cell_edges = cell_edges
        self.cell_masses = cell_masses
        self.cell_energies = cell_energies
        self.mass_error_bound = mass_error_bound
        self.tail_mass = tail_mass
        self.tail_mass_bound = tail_mass_bound
        self.truncated_mass = sum(cell_masses)
        self.energy_variation = energy_variation
        self.centering_error_bound = centering_error_bound
        self.centered_second_moment_bound = centered_second_moment_bound
        self.moment_evaluations = moment_evaluations
        self.query_evaluations = len(cell_masses)
        self.continuum_measure_id = continuum_measure_id

    def resolvent(self, spectral_parameter: float) -> RadialTransform:
        threshold = self.request.data.threshold
        if spectral_parameter >= threshold:
            raise ValueError("radial resolvent parameter must lie below threshold")
        distance = threshold - spectral_parameter
        value = sum(
            mass / (spectral_parameter - energy)
            for mass, energy in zip(self.cell_masses, self.cell_energies)
        )
        variation_bound = (
            self.mass_error_bound / distance
            + self.energy_variation / distance**2
        )
        moment_bound = (
            self.mass_error_bound / distance
            + self.centering_error_bound / distance**2
            + self.centered_second_moment_bound / distance**3
        )
        tail_bound = self.tail_mass_bound / distance
        return RadialTransform(
            value, moment_bound + tail_bound, variation_bound,
            moment_bound, tail_bound, self.continuum_measure_id,
            "radial-resolvent",
        )

    def open_event(self, time: float) -> RadialTransform:
        if time < 0:
            raise ValueError("time must be nonnegative")
        gap = self.request.data.level_gap

        def kernel(energy):
            delta = energy - gap
            if abs(delta) < 1e-12:
                return time**2
            return 4.0 * math.sin(0.5 * time * delta) ** 2 / delta**2

        value = sum(
            mass * kernel(energy)
            for mass, energy in zip(self.cell_masses, self.cell_energies)
        )
        variation_bound = (
            time**2 * self.mass_error_bound
            + time**3 * self.energy_variation
        )
        moment_bound = (
            time**2 * self.mass_error_bound
            + time**3 * self.centering_error_bound
            + 7.0 * time**4 * self.centered_second_moment_bound / 12.0
        )
        tail_bound = time**2 * self.tail_mass_bound
        return RadialTransform(
            value, moment_bound + tail_bound, variation_bound,
            moment_bound, tail_bound, self.continuum_measure_id,
            "radial-open-event",
        )


def _valid(packet: Quadrature, *, positive: bool | None) -> bool:
    values = (packet.value, packet.error, packet.evaluations)
    if not all(math.isfinite(value) for value in values) or packet.error < 0:
        return False
    if positive is None:
        return True
    return packet.value > packet.error if positive else packet.value >= 0


def _cell_moments(data, left, right, mass, tolerance):
    first = integrate(
        lambda radius: data.energy(radius) * data.weight(radius),
        (left, right), tolerance,
    )
    energy = first.value / mass.value
    second = integrate(
        lambda radius: (data.energy(radius) - energy) ** 2 * data.weight(radius),
        (left, right), tolerance,
    )
    valid = _valid(first, positive=None) and _valid(second, positive=False)
    centering = first.error + abs(energy) * mass.error
    second_bound = max(second.value, 0.0) + second.error
    evaluations = mass.evaluations + first.evaluations + second.evaluations
    return energy, centering, second_bound, evaluations, valid


def compile_radial_departure(
    request: RadialDepartureRequest,
) -> RadialDepartureCompilation:
    data = request.data

    def refuse(reason):
        return RadialDepartureCompilation(refusal=Refusal(
            reason, provenance=request.provenance,
        ))

    left_support, right_support = data.support
    if (
        not math.isfinite(left_support) or math.isnan(right_support)
        or left_support < 0 or right_support <= left_support
        or not math.isfinite(data.threshold) or not math.isfinite(data.level_gap)
    ):
        return refuse("invalid radial channel domain")
    if not data.monotone_energy:
        return refuse("radial energy must be declared monotone")
    try:
        threshold_energy = data.energy(left_support)
    except Exception:
        return refuse("radial threshold does not bound channel energy")
    if (
        not math.isfinite(threshold_energy)
        or threshold_energy < data.threshold
    ):
        return refuse("radial threshold does not bound channel energy")
    if (
        not math.isfinite(request.radial_cutoff)
        or not left_support < request.radial_cutoff <= right_support
    ):
        return refuse("radial cutoff must be finite and inside support")
    if (
        not isinstance(request.cell_count, int)
        or isinstance(request.cell_count, bool)
        or request.cell_count <= 0
    ):
        return refuse("radial cell count must be a positive integer")
    if (
        not math.isfinite(request.absolute_tolerance)
        or request.absolute_tolerance <= 0
    ):
        return refuse("radial tolerance must be finite and positive")

    count = request.cell_count
    width = (request.radial_cutoff - left_support) / count
    edges = tuple(left_support + width * index for index in range(count + 1))
    masses = tuple(
        data.mass(left, right, request.absolute_tolerance)
        for left, right in zip(edges, edges[1:])
    )
    if any(not _valid(mass, positive=True) for mass in masses):
        return refuse("radial cell mass is numerically unresolved")
    tail = data.mass(
        request.radial_cutoff, right_support, request.absolute_tolerance
    )
    if not _valid(tail, positive=False):
        return refuse("radial tail mass is numerically unresolved")

    moments = tuple(
        _cell_moments(data, left, right, mass, request.absolute_tolerance)
        for mass, left, right in zip(masses, edges, edges[1:])
    )
    if any(not moment[4] for moment in moments):
        return refuse("radial energy moment is numerically unresolved")
    cell_masses = tuple(mass.value for mass in masses)
    energies = tuple(moment[0] for moment in moments)
    mass_error = sum(mass.error for mass in masses)
    centering_error = sum(moment[1] for moment in moments)
    centered_second_moment = sum(moment[2] for moment in moments)
    energy_variation = sum(
        (mass.value + mass.error) * max(
            abs(data.energy(left) - energy),
            abs(data.energy(right) - energy),
        )
        for mass, left, right, energy
        in zip(masses, edges, edges[1:], energies)
    )
    evaluations = tail.evaluations + sum(moment[3] for moment in moments)

    vacuum = (0,) * count
    preparations = (FockState("excited", vacuum),)
    channels = tuple(
        FockState("ground", tuple(1 if i == mode else 0 for i in range(count)))
        for mode in range(count)
    )
    vertices = tuple(
        MatterBosonVertex(
            "excited", "ground", mode, "create", math.sqrt(mass),
            f"radial-cell:{mode}",
        )
        for mode, mass in enumerate(cell_masses)
    )
    departure = compile_departure(DepartureRequest(
        preparations, channels, vertices, request.provenance,
        request.resource_budget,
    ))
    if not departure.accepted:
        return RadialDepartureCompilation(refusal=departure.refusal)

    from .measures import compile_visible_measure

    continuum = compile_visible_measure(data.measure_request())
    if not continuum.accepted:
        return RadialDepartureCompilation(refusal=continuum.refusal)
    return RadialDepartureCompilation(radial=FiniteRadialDeparture(
        request, departure, edges, cell_masses, energies, mass_error,
        tail.value, tail.value + tail.error, energy_variation,
        centering_error, centered_second_moment, evaluations,
        continuum.measure.measure_id,
    ))
