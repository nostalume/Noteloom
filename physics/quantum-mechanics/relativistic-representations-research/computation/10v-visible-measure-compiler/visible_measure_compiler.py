"""N10v: one visible-measure compiler, two inequivalent spectral regimes.

The compiler receives factor maps for the orbit measure, observable shell action,
preparation, and energy.  It multiplies them and pushes the radial measure through
the energy map.  It never receives an expected density or threshold exponent.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math
from pathlib import Path
import sys
from typing import Callable


ANGULAR_MODULE = Path(__file__).resolve().parents[1] / "10u-curvature-detector-measure"
sys.path.insert(0, str(ANGULAR_MODULE))

from angular_response import (  # noqa: E402
    ConstructionRefusal,
    DetectorContraction,
    ScalarDetectorContraction,
    compile_angular_response,
    compile_scalar_angular_response,
)


ScalarMap = Callable[[float], float]


def simpson(function, left: float, right: float, intervals: int = 100_000):
    if intervals <= 0 or intervals % 2:
        raise ValueError("Simpson interval count must be positive and even")
    step = (right - left) / intervals
    total = function(left) + function(right)
    total += 4.0 * sum(function(left + step * index) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(left + step * index) for index in range(2, intervals, 2))
    return total * step / 3.0


@dataclass(frozen=True)
class RadialChannel:
    name: str
    threshold: float
    radius_limit: float
    energy: ScalarMap
    energy_derivative: ScalarMap
    orbit_jacobian: ScalarMap
    observable_weight: ScalarMap
    preparation_weight: ScalarMap
    provenance: tuple[str, ...]


@dataclass(frozen=True)
class VisibleMeasure:
    channel: RadialChannel
    monotonicity_margin: float

    def radial_density(self, radius: float) -> float:
        if radius < 0.0:
            return 0.0
        return (
            self.channel.orbit_jacobian(radius)
            * self.channel.observable_weight(radius)
            * self.channel.preparation_weight(radius)
        )

    def radius_from_energy(self, energy: float) -> float:
        if energy < self.channel.threshold:
            raise ValueError("energy lies below the channel threshold")
        maximum_energy = self.channel.energy(self.channel.radius_limit)
        if energy > maximum_energy:
            raise ValueError("energy lies beyond the compiled radial window")
        if energy == self.channel.threshold:
            return 0.0

        left = 0.0
        right = self.channel.radius_limit
        for _ in range(100):
            middle = 0.5 * (left + right)
            if self.channel.energy(middle) < energy:
                left = middle
            else:
                right = middle
        return 0.5 * (left + right)

    def energy_density(self, energy: float) -> float:
        if energy <= self.channel.threshold:
            return 0.0
        radius = self.radius_from_energy(energy)
        derivative = self.channel.energy_derivative(radius)
        if derivative <= 0.0:
            raise ConstructionRefusal(
                "the energy pushforward is not locally one-to-one at the requested point"
            )
        return self.radial_density(radius) / derivative

    def integrate(self, function, intervals: int = 100_000):
        return simpson(
            lambda radius: self.radial_density(radius)
            * function(self.channel.energy(radius)),
            0.0,
            self.channel.radius_limit,
            intervals,
        )

    def stieltjes(self, spectral_parameter: complex) -> complex:
        return self.integrate(
            lambda energy: 1.0 / (spectral_parameter - energy)
        )

    def memory(self, time: float) -> complex:
        return self.integrate(lambda energy: cmath.exp(-1j * energy * time))


def compile_visible_measure(channel: RadialChannel) -> VisibleMeasure:
    if channel.radius_limit <= 0.0:
        raise ConstructionRefusal("a positive radial construction window is required")
    if abs(channel.energy(0.0) - channel.threshold) > 1e-12:
        raise ConstructionRefusal("the declared threshold does not equal energy(0)")
    if min(
        channel.orbit_jacobian(0.0),
        channel.observable_weight(0.0),
        channel.preparation_weight(0.0),
    ) < 0.0:
        raise ConstructionRefusal("visible-measure factors must be nonnegative")

    positive_derivatives = []
    previous_energy = channel.energy(0.0)
    for index in range(1, 257):
        radius = channel.radius_limit * index / 256.0
        energy = channel.energy(radius)
        derivative = channel.energy_derivative(radius)
        if energy <= previous_energy or derivative <= 0.0:
            raise ConstructionRefusal(
                "energy is not strictly increasing on the radial window; provide "
                "monotone branches before requesting a scalar pushforward"
            )
        if min(
            channel.orbit_jacobian(radius),
            channel.observable_weight(radius),
            channel.preparation_weight(radius),
        ) < 0.0:
            raise ConstructionRefusal("visible-measure factors must be nonnegative")
        positive_derivatives.append(derivative)
        previous_energy = energy

    return VisibleMeasure(channel, min(positive_derivatives))


def massless_curvature_channel(
    spin: int,
    cutoff: float,
    coupling: float,
    detector: DetectorContraction,
) -> RadialChannel:
    angular = compile_angular_response(spin, detector)
    return RadialChannel(
        name=f"massless-curvature-spin-{spin}",
        threshold=0.0,
        radius_limit=8.0 * cutoff,
        energy=lambda radius: radius,
        energy_derivative=lambda radius: 1.0,
        orbit_jacobian=lambda radius: 0.5 * radius,
        observable_weight=lambda radius: angular.response * radius ** (2 * spin),
        preparation_weight=lambda radius: coupling**2
        * math.exp(-(radius / cutoff) ** 2),
        provenance=(
            "future-null orbit d^3p/(2|p|)",
            f"generated curvature degree {spin}",
            "rotation-averaged physical helicity projectors",
            "detector coupling and isotropic Gaussian preparation",
        ),
    )


def massless_scalar_channel(
    cutoff: float,
    coupling: float,
    detector: ScalarDetectorContraction,
) -> RadialChannel:
    angular = compile_scalar_angular_response(detector)
    return RadialChannel(
        name="massless-scalar-spin-0",
        threshold=0.0,
        radius_limit=8.0 * cutoff,
        energy=lambda radius: radius,
        energy_derivative=lambda radius: 1.0,
        orbit_jacobian=lambda radius: 0.5 * radius,
        observable_weight=lambda radius: angular.response,
        preparation_weight=lambda radius: coupling**2
        * math.exp(-(radius / cutoff) ** 2),
        provenance=(
            "future-null orbit d^3p/(2|p|)",
            "rank-zero identity readout",
            "one-dimensional scalar physical fiber",
            "detector coupling and isotropic Gaussian preparation",
        ),
    )


def massive_recoil_channel(
    particle_mass: float,
    boson_mass: float,
    cutoff: float,
    coupling: float,
) -> RadialChannel:
    def dispersion(radius: float) -> float:
        return math.sqrt(radius * radius + boson_mass * boson_mass)

    return RadialChannel(
        name="massive-scalar-recoil",
        threshold=boson_mass,
        radius_limit=8.0 * cutoff,
        energy=lambda radius: dispersion(radius)
        + radius * radius / (2.0 * particle_mass),
        energy_derivative=lambda radius: radius
        * (1.0 / dispersion(radius) + 1.0 / particle_mass),
        orbit_jacobian=lambda radius: 4.0 * math.pi * radius**2,
        observable_weight=lambda radius: 1.0,
        preparation_weight=lambda radius: coupling**2
        * math.exp(-(radius / cutoff) ** 2),
        provenance=(
            "N9c vacuum one-boson L2(d^3k) shell",
            "scalar creation observable",
            "Gaussian departure form factor",
            "free boson plus recoil energy",
        ),
    )


def main() -> None:
    detector = DetectorContraction(plus_norm_squared=0.6, minus_norm_squared=0.4)
    spin = 2
    detector_coupling = 0.005
    detector_cutoff = 2.0
    angular = compile_angular_response(spin, detector)
    massless = compile_visible_measure(
        massless_curvature_channel(
            spin, detector_cutoff, detector_coupling, detector
        )
    )

    scalar_detector = ScalarDetectorContraction(norm_squared=1.0)
    scalar_angular = compile_scalar_angular_response(scalar_detector)
    massless_ladder = {
        0: compile_visible_measure(
            massless_scalar_channel(
                detector_cutoff, detector_coupling, scalar_detector
            )
        ),
        1: compile_visible_measure(
            massless_curvature_channel(
                1, detector_cutoff, detector_coupling, detector
            )
        ),
        2: massless,
    }

    particle_mass = 2.0
    boson_mass = 1.0
    scalar_cutoff = 1.0
    scalar_coupling = 0.2
    massive = compile_visible_measure(
        massive_recoil_channel(
            particle_mass, boson_mass, scalar_cutoff, scalar_coupling
        )
    )

    print("visible-measure compiler: cross-regime transfer")
    print("\nmassless curvature channel")
    massless_factor_errors = []
    for frequency in (0.2, 0.7, 1.2, 2.5):
        generated = massless.energy_density(frequency)
        expected = (
            0.5
            * angular.response
            * detector_coupling**2
            * frequency ** (2 * spin + 1)
            * math.exp(-(frequency / detector_cutoff) ** 2)
        )
        massless_factor_errors.append(abs(generated - expected))
    massless_mass = massless.integrate(lambda energy: 1.0)
    massless_mass_exact = (
        detector_coupling**2
        * angular.response
        * detector_cutoff ** (2 * spin + 2)
        * math.factorial(spin)
        / 4.0
    )
    detector_gap = 1.2
    massless_bound_shift = -massless.integrate(
        lambda energy: 1.0 / (detector_gap + energy)
    )
    massless_rate = 2.0 * math.pi * massless.energy_density(detector_gap)
    print(f"generated angular response       = {angular.response:.15f}")
    print(f"generated radial density power   = {2 * spin + 1}")
    print(f"factor-route maximum error       = {max(massless_factor_errors):.3e}")
    print(f"measure mass                     = {massless_mass:.15e}")
    print(f"analytic mass                    = {massless_mass_exact:.15e}")
    print(f"bound ground shift               = {massless_bound_shift:.15e}")
    print(f"open boundary rate               = {massless_rate:.15e}")

    print("\nmassless low-spin ladder")
    ladder_factor_errors = []
    ladder_angular = {
        0: scalar_angular,
        1: compile_angular_response(1, detector),
        2: angular,
    }
    for ladder_spin, measure in massless_ladder.items():
        frequency = 0.7
        expected = (
            0.5
            * ladder_angular[ladder_spin].response
            * detector_coupling**2
            * frequency ** (2 * ladder_spin + 1)
            * math.exp(-(frequency / detector_cutoff) ** 2)
        )
        error = abs(measure.energy_density(frequency) - expected)
        ladder_factor_errors.append(error)
        print(
            f"spin {ladder_spin}: generated density power = "
            f"{2 * ladder_spin + 1}, factor error = {error:.3e}"
        )

    print("\nmassive recoil channel")
    massive_mass = massive.integrate(lambda energy: 1.0)
    massive_mass_exact = (
        scalar_coupling**2 * math.pi ** 1.5 * scalar_cutoff**3
    )
    probe_energy = 1.5
    generated_probe_density = massive.energy_density(probe_energy)
    radius = massive.radius_from_energy(probe_energy)
    omega = math.sqrt(radius * radius + boson_mass * boson_mass)
    legacy_probe_density = (
        4.0
        * math.pi
        * scalar_coupling**2
        * radius**2
        * math.exp(-(radius / scalar_cutoff) ** 2)
        / (radius * (1.0 / omega + 1.0 / particle_mass))
    )
    massive_bound_shift = massive.stieltjes(0.0).real
    massive_boundary = 2.0 * math.pi * generated_probe_density

    threshold_a = 0.5 * (1.0 / boson_mass + 1.0 / particle_mass)
    threshold_coefficient = (
        2.0 * math.pi * scalar_coupling**2 / threshold_a ** 1.5
    )
    threshold_ratio = massive.energy_density(boson_mass + 1e-6) / 1e-3
    print(f"measure mass                     = {massive_mass:.15e}")
    print(f"analytic mass                    = {massive_mass_exact:.15e}")
    print(f"density at E=1.5                = {generated_probe_density:.15e}")
    print(f"N9c independent density         = {legacy_probe_density:.15e}")
    print(f"bound self-energy at z=0        = {massive_bound_shift:.15e}")
    print(f"open boundary loss              = {massive_boundary:.15e}")
    print(f"threshold ratio                 = {threshold_ratio:.15e}")
    print(f"threshold coefficient           = {threshold_coefficient:.15e}")

    nonmonotone_refusal = None
    try:
        compile_visible_measure(
            RadialChannel(
                name="nonmonotone-probe",
                threshold=0.0,
                radius_limit=2.0,
                energy=lambda radius: radius * (2.0 - radius),
                energy_derivative=lambda radius: 2.0 - 2.0 * radius,
                orbit_jacobian=lambda radius: radius**2,
                observable_weight=lambda radius: 1.0,
                preparation_weight=lambda radius: math.exp(-radius**2),
                provenance=("refusal regression",),
            )
        )
    except ConstructionRefusal as error:
        nonmonotone_refusal = str(error)

    assert max(massless_factor_errors) < 1e-14
    assert max(ladder_factor_errors) < 1e-14
    assert abs(massless_mass - massless_mass_exact) < 1e-12
    assert massless_bound_shift < 0.0
    assert massless_rate > 0.0
    assert abs(massive_mass - massive_mass_exact) < 2e-12
    assert abs(generated_probe_density - legacy_probe_density) < 1e-13
    assert massive_bound_shift < 0.0
    assert massive_boundary > 0.0
    assert abs(threshold_ratio - threshold_coefficient) < 5e-5
    assert nonmonotone_refusal is not None

    print("\nrefusal certificate")
    print(f"nonmonotone pushforward          = {nonmonotone_refusal}")
    print("\nall visible-measure transfer checks passed")


if __name__ == "__main__":
    main()
