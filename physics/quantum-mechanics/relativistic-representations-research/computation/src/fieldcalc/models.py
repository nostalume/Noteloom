"""Explicit parameters and factors for retained observable benchmarks."""

from dataclasses import dataclass
import math

from .numeric import Quadrature
from .radial import RadialData


@dataclass(frozen=True)
class ScalarModel:
    particle_mass: float
    boson_mass: float
    cutoff: float
    coupling: float
    level_gap: float

    def __post_init__(self):
        if min(self.particle_mass, self.boson_mass, self.cutoff) <= 0:
            raise ValueError("masses and cutoff must be positive")
        if self.coupling < 0 or self.level_gap < 0:
            raise ValueError("coupling and gap must be nonnegative")

    def dispersion(self, radius: float) -> float:
        return math.sqrt(radius * radius + self.boson_mass * self.boson_mass)

    def energy(self, radius: float) -> float:
        return self.dispersion(radius) + radius * radius / (2.0 * self.particle_mass)

    def form_factor(self, radius: float) -> float:
        return math.exp(-0.5 * (radius / self.cutoff) ** 2)


def _gaussian_tail(model: ScalarModel, radius: float) -> float:
    if math.isinf(radius):
        return 0.0
    scale = model.cutoff
    ratio = radius / scale
    coupling_squared = model.coupling**2
    return (
        coupling_squared * math.pi**1.5 * scale**3 * math.erfc(ratio)
        + 2.0 * math.pi * coupling_squared * scale**2
        * radius * math.exp(-ratio**2)
    )


def scalar_radial_data(model: ScalarModel) -> RadialData:
    provenance = (
        f"scalar:M={model.particle_mass}:mu={model.boson_mass}:"
        f"cutoff={model.cutoff}:g={model.coupling}"
    )

    def mass(left, right):
        return Quadrature(
            _gaussian_tail(model, left) - _gaussian_tail(model, right), 0.0, 0
        )

    return RadialData(
        amplitude=lambda radius: model.coupling * model.form_factor(radius),
        energy=model.energy,
        threshold=model.boson_mass,
        level_gap=model.level_gap,
        support=(0.0, math.inf),
        provenance=provenance,
        mass_operation=mass,
    )


def scalar_departure_request(model: ScalarModel):
    return scalar_radial_data(model).measure_request()
