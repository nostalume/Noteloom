"""Explicit parameters and factors for retained observable benchmarks."""

from dataclasses import dataclass
import math


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


def scalar_departure_request(model: ScalarModel):
    from .measures import MeasureRequest

    def weight(radius: float) -> float:
        amplitude = model.coupling * model.form_factor(radius)
        return 4.0 * math.pi * radius * radius * amplitude * amplitude

    return MeasureRequest(
        weight=weight,
        energy=model.energy,
        support=(0.0, math.inf),
        provenance=(
            f"scalar:M={model.particle_mass}:mu={model.boson_mass}:"
            f"cutoff={model.cutoff}:g={model.coupling}"
        ),
        monotone=True,
    )
