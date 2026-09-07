"""One-channel field return shared by bound and open observables."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Callable

from scipy.integrate import quad
from scipy.linalg import solve
from scipy.optimize import brentq

from .rewrite import Refusal


@dataclass(frozen=True)
class FieldReturnRequest:
    bare_energy: float
    coupling: float
    form_factor_squared: Callable[[float], float]
    band: tuple[float, float]
    provenance: str
    mode_budget: int = 256


@dataclass(frozen=True)
class BoundStateResult:
    energy: float | None = None
    residue: float | None = None
    equation_residual: float | None = None
    measure_id: str = ""
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


@dataclass(frozen=True)
class OpenChannelResult:
    energy: float
    transition: complex
    scattering: complex
    unitarity_residual: float
    measure_id: str


@dataclass(frozen=True)
class FiniteModeComparison:
    projected_direct: complex | None = None
    projected_reduced: complex | None = None
    projected_continuum: complex | None = None
    residual: float | None = None
    continuum_error: float | None = None
    reduced_operations: int = 0
    expert_operations: int = 0
    direct_operations: int = 0
    observable: str = "projected-resolvent"
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None

    @property
    def advantage_over_expert(self) -> bool:
        return self.accepted and self.reduced_operations < self.expert_operations


@dataclass(frozen=True)
class FieldReturnCompilation:
    return_: "SingleChannelFieldReturn | None" = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


class SingleChannelFieldReturn:
    def __init__(self, request: FieldReturnRequest):
        self.request = request
        identity = f"{request.provenance}|{request.band}|{request.coupling}".encode()
        self.measure_id = hashlib.sha256(identity).hexdigest()[:16]

    def visible_density(self, energy: float) -> float:
        left, right = self.request.band
        if energy < left or energy > right:
            return 0.0
        return self.request.coupling**2 * self.request.form_factor_squared(energy)

    def self_energy(self, spectral_parameter: complex) -> complex:
        z = complex(spectral_parameter)
        left, right = self.request.band
        if z.imag == 0.0 and left <= z.real <= right:
            raise ValueError("use the continuum boundary on the visible band")

        def integrand(energy: float) -> complex:
            return self.visible_density(energy) / (z - energy)

        real = quad(lambda energy: integrand(energy).real, left, right,
                    epsabs=1e-12, epsrel=1e-12, limit=300)[0]
        imag = quad(lambda energy: integrand(energy).imag, left, right,
                    epsabs=1e-12, epsrel=1e-12, limit=300)[0]
        return complex(real, imag)

    def continuum_boundary(self, energy: float) -> complex:
        left, right = self.request.band
        if not left < energy < right:
            raise ValueError("open energy must lie inside the continuum band")
        principal_value = -quad(
            self.visible_density,
            left,
            right,
            weight="cauchy",
            wvar=energy,
            epsabs=1e-12,
            epsrel=1e-12,
            limit=300,
        )[0]
        return complex(principal_value, -math.pi * self.visible_density(energy))

    def projected_resolvent(self, spectral_parameter: complex) -> complex:
        z = complex(spectral_parameter)
        return 1.0 / (z - self.request.bare_energy - self.self_energy(z))

    def bound_state(self, bracket: tuple[float, float]) -> BoundStateResult:
        left_band, _ = self.request.band
        left, right = bracket
        if not left < right < left_band:
            return BoundStateResult(refusal=Refusal(
                "bound bracket must lie below the continuum",
                residual=bracket,
                provenance=self.request.provenance,
            ))

        def denominator(energy: float) -> float:
            return energy - self.request.bare_energy - self.self_energy(energy).real

        if denominator(left) * denominator(right) > 0:
            return BoundStateResult(refusal=Refusal(
                "bound pole is not bracketed",
                residual=(denominator(left), denominator(right)),
                provenance=self.request.provenance,
            ))

        energy = brentq(denominator, left, right, xtol=1e-13, rtol=1e-13)
        derivative = -quad(
            lambda value: self.visible_density(value) / (energy - value) ** 2,
            *self.request.band,
            epsabs=1e-12,
            epsrel=1e-12,
            limit=300,
        )[0]
        return BoundStateResult(
            energy=energy,
            residue=1.0 / (1.0 - derivative),
            equation_residual=abs(denominator(energy)),
            measure_id=self.measure_id,
        )

    def open_channel(self, energy: float) -> OpenChannelResult:
        sigma = self.continuum_boundary(energy)
        density = self.visible_density(energy)
        transition = density / (energy - self.request.bare_energy - sigma)
        scattering = 1.0 - 2j * math.pi * transition
        return OpenChannelResult(
            energy=energy,
            transition=transition,
            scattering=scattering,
            unitarity_residual=abs(abs(scattering) ** 2 - 1.0),
            measure_id=self.measure_id,
        )

    def compare_finite_modes(
        self,
        spectral_parameter: complex,
        mode_count: int,
    ) -> FiniteModeComparison:
        if mode_count < 1 or mode_count > self.request.mode_budget:
            return FiniteModeComparison(refusal=Refusal(
                "finite-mode budget exceeded",
                residual=(mode_count, self.request.mode_budget),
                provenance=self.request.provenance,
            ))

        z = complex(spectral_parameter)
        left, right = self.request.band
        width = (right - left) / mode_count
        nodes = [left + (index + 0.5) * width for index in range(mode_count)]
        masses = [self.visible_density(node) * width for node in nodes]
        couplings = [math.sqrt(mass) for mass in masses]

        size = mode_count + 1
        matrix = [[0j for _ in range(size)] for _ in range(size)]
        matrix[0][0] = z - self.request.bare_energy
        for index, (node, coupling) in enumerate(zip(nodes, couplings), start=1):
            matrix[index][index] = z - node
            matrix[0][index] = matrix[index][0] = -coupling
        right_hand_side = [1.0] + [0.0] * mode_count
        direct = complex(solve(matrix, right_hand_side)[0])

        finite_sigma = sum(mass / (z - node) for node, mass in zip(nodes, masses))
        reduced = 1.0 / (z - self.request.bare_energy - finite_sigma)
        continuum = self.projected_resolvent(z)
        reduced_operations = 3 * mode_count + 2
        return FiniteModeComparison(
            projected_direct=direct,
            projected_reduced=reduced,
            projected_continuum=continuum,
            residual=abs(direct - reduced),
            continuum_error=abs(reduced - continuum),
            reduced_operations=reduced_operations,
            expert_operations=reduced_operations,
            direct_operations=size**3 + 3 * mode_count,
        )


def compile_field_return(request: FieldReturnRequest) -> FieldReturnCompilation:
    left, right = request.band
    if not math.isfinite(left) or not math.isfinite(right) or right <= left:
        return FieldReturnCompilation(refusal=Refusal(
            "continuum band must be finite and ordered", provenance=request.provenance,
        ))
    if request.coupling < 0:
        return FieldReturnCompilation(refusal=Refusal(
            "coupling must be nonnegative", provenance=request.provenance,
        ))
    if request.mode_budget < 1:
        return FieldReturnCompilation(refusal=Refusal(
            "mode budget must be positive", provenance=request.provenance,
        ))
    samples = [left + (right - left) * index / 8 for index in range(9)]
    if any(request.form_factor_squared(value) < 0 for value in samples):
        return FieldReturnCompilation(refusal=Refusal(
            "form-factor square must be nonnegative", provenance=request.provenance,
        ))
    return FieldReturnCompilation(return_=SingleChannelFieldReturn(request))
