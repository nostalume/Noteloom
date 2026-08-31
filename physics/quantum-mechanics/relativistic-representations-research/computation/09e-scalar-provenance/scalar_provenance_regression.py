"""N9e regression: source-shell normalization and N9d measure recovery."""

from __future__ import annotations

import math


PARTICLE_MASS = 2.0
BOSON_MASS = 1.0
CUTOFF = 1.0
COUPLING = 0.01
RADIAL_LIMIT = 8.0


def dispersion(radius: float) -> float:
    return math.sqrt(radius * radius + BOSON_MASS * BOSON_MASS)


def shell_amplitude(radius: float) -> float:
    return math.exp(-0.5 * (radius / CUTOFF) ** 2)


def source_fourier(radius: float) -> float:
    return math.sqrt(2.0 * dispersion(radius)) * shell_amplitude(radius)


def recovered_shell_amplitude(radius: float) -> float:
    return source_fourier(radius) / math.sqrt(2.0 * dispersion(radius))


def channel_energy(radius: float) -> float:
    return dispersion(radius) + radius * radius / (2.0 * PARTICLE_MASS)


def radial_from_energy(energy: float) -> float:
    omega = -PARTICLE_MASS + math.sqrt(
        PARTICLE_MASS**2 + BOSON_MASS**2 + 2.0 * PARTICLE_MASS * energy
    )
    return math.sqrt(max(0.0, omega * omega - BOSON_MASS**2))


def spectral_density(energy: float) -> float:
    if energy <= BOSON_MASS:
        return 0.0
    radius = radial_from_energy(energy)
    derivative = radius * (1.0 / dispersion(radius) + 1.0 / PARTICLE_MASS)
    return (
        4.0
        * math.pi
        * COUPLING**2
        * radius**2
        * shell_amplitude(radius) ** 2
        / derivative
    )


def simpson(function, left: float, right: float, intervals: int = 40000) -> float:
    if intervals % 2:
        raise ValueError("Simpson interval count must be even")
    step = (right - left) / intervals
    total = function(left) + function(right)
    total += 4.0 * sum(function(left + step * i) for i in range(1, intervals, 2))
    total += 2.0 * sum(function(left + step * i) for i in range(2, intervals, 2))
    return total * step / 3.0


def radial_integral(function) -> float:
    return 4.0 * math.pi * simpson(
        lambda radius: radius**2 * function(radius), 0.0, RADIAL_LIMIT
    )


def main() -> None:
    sample_radii = [index * 0.01 for index in range(801)]
    recovery_error = max(
        abs(recovered_shell_amplitude(radius) - shell_amplitude(radius))
        for radius in sample_radii
    )

    h_norm_squared = radial_integral(lambda radius: shell_amplitude(radius) ** 2)
    energy_norm_squared = radial_integral(
        lambda radius: shell_amplitude(radius) ** 2 / dispersion(radius)
    )
    expected_h_norm_squared = math.pi**1.5 * CUTOFF**3

    measure_mass = COUPLING**2 * h_norm_squared
    expected_measure_mass = COUPLING**2 * expected_h_norm_squared
    probe_energy = 1.5
    probe_density = spectral_density(probe_energy)
    boundary_rate = 2.0 * math.pi * probe_density

    print("source-shell identity")
    print(f"maximum sampled recovery error = {recovery_error:.3e}")
    print(f"||h||^2 radial                = {h_norm_squared:.15f}")
    print(f"||h||^2 analytic              = {expected_h_norm_squared:.15f}")
    print(f"||h/sqrt(omega)||^2           = {energy_norm_squared:.15f}")

    print("\nN9d measure recovery")
    print(f"measure mass                  = {measure_mass:.15f}")
    print(f"density m(1.5)                = {probe_density:.15f}")
    print(f"boundary rate 2*pi*m(1.5)     = {boundary_rate:.15f}")

    assert recovery_error < 1e-15
    assert abs(h_norm_squared - expected_h_norm_squared) < 2e-12
    assert math.isfinite(energy_norm_squared) and energy_norm_squared > 0.0
    assert abs(measure_mass - expected_measure_mass) < 2e-16
    assert abs(probe_density - 0.000410346265971) < 5e-16
    assert abs(boundary_rate - 0.002578281629203) < 5e-15
    print("\nall scalar-provenance acceptance checks passed")


if __name__ == "__main__":
    main()
