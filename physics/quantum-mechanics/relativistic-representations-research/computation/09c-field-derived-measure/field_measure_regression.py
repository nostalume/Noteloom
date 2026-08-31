"""N9c regression: one field-derived measure, four computational routes.

The fixed-total-momentum scalar field fiber is evaluated at P=0. Units are
chosen so that the boson mass and Gaussian cutoff scale are one.
"""

from __future__ import annotations

import cmath
import math


PARTICLE_MASS = 2.0
BOSON_MASS = 1.0
CUTOFF = 1.0
COUPLING = 0.2
RADIAL_LIMIT = 8.0


def dispersion(radius: float) -> float:
    return math.sqrt(radius * radius + BOSON_MASS * BOSON_MASS)


def channel_energy(radius: float) -> float:
    return dispersion(radius) + radius * radius / (2.0 * PARTICLE_MASS)


def form_factor_squared(radius: float) -> float:
    return math.exp(-(radius / CUTOFF) ** 2)


def radial_from_energy(energy: float) -> float:
    if energy < BOSON_MASS:
        raise ValueError("energy lies below the one-boson threshold")
    omega = -PARTICLE_MASS + math.sqrt(
        PARTICLE_MASS**2 + BOSON_MASS**2 + 2.0 * PARTICLE_MASS * energy
    )
    return math.sqrt(max(0.0, omega * omega - BOSON_MASS**2))


def spectral_density(energy: float) -> float:
    if energy <= BOSON_MASS:
        return 0.0
    radius = radial_from_energy(energy)
    omega = dispersion(radius)
    derivative = radius * (1.0 / omega + 1.0 / PARTICLE_MASS)
    return (
        4.0
        * math.pi
        * COUPLING**2
        * radius**2
        * form_factor_squared(radius)
        / derivative
    )


def simpson(function, left: float, right: float, intervals: int):
    if intervals % 2:
        raise ValueError("Simpson interval count must be even")
    step = (right - left) / intervals
    total = function(left) + function(right)
    total += 4.0 * sum(function(left + step * index) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(left + step * index) for index in range(2, intervals, 2))
    return total * step / 3.0


def radial_measure_integral(function, intervals: int = 40000):
    prefactor = 4.0 * math.pi * COUPLING**2
    return prefactor * simpson(
        lambda radius: radius**2 * form_factor_squared(radius) * function(channel_energy(radius)),
        0.0,
        RADIAL_LIMIT,
        intervals,
    )


def density_measure_integral(function, intervals: int = 120000):
    maximum_energy = channel_energy(RADIAL_LIMIT)
    # Resolve the square-root threshold by energy = mu + y^2.  Integrating
    # directly in energy makes composite Simpson convergence needlessly slow.
    maximum_root = math.sqrt(maximum_energy - BOSON_MASS)
    return simpson(
        lambda root: (
            2.0
            * root
            * spectral_density(BOSON_MASS + root * root)
            * function(BOSON_MASS + root * root)
        ),
        0.0,
        maximum_root,
        intervals,
    )


def self_energy(z: complex) -> complex:
    return radial_measure_integral(lambda energy: 1.0 / (z - energy))


def self_energy_derivative_below(energy: float) -> float:
    return -radial_measure_integral(lambda channel: 1.0 / (energy - channel) ** 2).real


def memory_radial(time: float) -> complex:
    intervals = max(60000, int(2500 * max(1.0, time)))
    if intervals % 2:
        intervals += 1
    return radial_measure_integral(
        lambda energy: cmath.exp(-1j * energy * time), intervals=intervals
    )


def memory_density(time: float) -> complex:
    intervals = max(120000, int(4000 * max(1.0, time)))
    if intervals % 2:
        intervals += 1
    return density_measure_integral(
        lambda energy: cmath.exp(-1j * energy * time), intervals=intervals
    )


def bisect(function, left: float, right: float, tolerance: float = 2e-14) -> float:
    f_left = function(left)
    f_right = function(right)
    if f_left * f_right > 0.0:
        raise ValueError("root is not bracketed")
    while right - left > tolerance:
        middle = 0.5 * (left + right)
        f_middle = function(middle)
        if f_left * f_middle <= 0.0:
            right, f_right = middle, f_middle
        else:
            left, f_left = middle, f_middle
    return 0.5 * (left + right)


def two_site_chain(moments: list[float]):
    mu0, mu1, mu2, mu3 = moments[:4]
    b0 = mu1 / mu0
    a1_squared = mu2 / mu0 - b0 * b0
    a1 = math.sqrt(a1_squared)
    norm1 = mu0 * a1_squared
    b1 = (mu3 - 2.0 * b0 * mu2 + b0 * b0 * mu1) / norm1
    discriminant = math.sqrt((b0 - b1) ** 2 + 4.0 * a1_squared)
    lower = 0.5 * (b0 + b1 - discriminant)
    upper = 0.5 * (b0 + b1 + discriminant)
    lower_weight = (b1 - lower) / (upper - lower)
    upper_weight = 1.0 - lower_weight
    return b0, a1, b1, (lower, upper), (lower_weight, upper_weight)


def main() -> None:
    exact_mass = COUPLING**2 * math.pi ** 1.5 * CUTOFF**3
    radial_mass = radial_measure_integral(lambda energy: 1.0)
    density_mass = density_measure_integral(lambda energy: 1.0)

    leading_energy_shift = self_energy(0.0).real
    pole = bisect(lambda energy: energy - self_energy(energy).real, -1.0, 0.0)
    pole_derivative = self_energy_derivative_below(pole)
    pole_residue = 1.0 / (1.0 - pole_derivative)
    leading_residue = 1.0 + self_energy_derivative_below(0.0)

    # The energy alone does not retain radius; evaluate N4u's invariant radial
    # pushforward before the energy quotient.
    mass_integral = 4.0 * math.pi * COUPLING**2 * simpson(
        lambda radius: (
            radius**4
            * form_factor_squared(radius)
            / channel_energy(radius) ** 3
        ),
        0.0,
        RADIAL_LIMIT,
        40000,
    )
    inverse_effective_mass = 1.0 / PARTICLE_MASS - (
        2.0 / (3.0 * PARTICLE_MASS**2)
    ) * mass_integral
    effective_mass_order_2 = PARTICLE_MASS + PARTICLE_MASS**2 * (
        1.0 / PARTICLE_MASS - inverse_effective_mass
    )
    reciprocal_mass_diagnostic = 1.0 / inverse_effective_mass

    probe_energy = 1.5
    probe_density = spectral_density(probe_energy)
    boundary_loss = 2.0 * math.pi * probe_density

    threshold_a = 0.5 * (1.0 / BOSON_MASS + 1.0 / PARTICLE_MASS)
    threshold_density_coefficient = (
        2.0 * math.pi * COUPLING**2 / threshold_a ** 1.5
    )
    threshold_memory_coefficient = (
        math.pi ** 1.5 * COUPLING**2 / threshold_a ** 1.5
    )
    expected_scaled_memory = threshold_memory_coefficient * cmath.exp(-3j * math.pi / 4.0)

    moments = [radial_measure_integral(lambda energy, order=order: energy**order) for order in range(7)]
    b0, a1, b1, nodes, normalized_weights = two_site_chain(moments)
    atomic_weights = tuple(radial_mass * weight for weight in normalized_weights)
    chain_moments = [
        sum(weight * node**order for weight, node in zip(atomic_weights, nodes))
        for order in range(7)
    ]
    chain_sigma_far = sum(weight / (-5.0 - node) for weight, node in zip(atomic_weights, nodes))
    exact_sigma_far = self_energy(-5.0).real

    print("field and measure")
    print(f"particle mass M                 = {PARTICLE_MASS:.12f}")
    print(f"boson mass mu                   = {BOSON_MASS:.12f}")
    print(f"coupling g                      = {COUPLING:.12f}")
    print(f"measure mass analytic           = {exact_mass:.15f}")
    print(f"measure mass radial             = {radial_mass:.15f}")
    print(f"measure mass density            = {density_mass:.15f}")

    print("\nbound observables")
    print(f"order-g^2 energy shift          = {leading_energy_shift:.15f}")
    print(f"one-boson resummed pole         = {pole:.15f}")
    print(f"order-g^2 prepared residue      = {leading_residue:.15f}")
    print(f"one-boson resummed residue      = {pole_residue:.15f}")
    print(f"order-g^2 inverse M_eff         = {inverse_effective_mass:.15f}")
    print(f"order-g^2 M_eff expansion       = {effective_mass_order_2:.15f}")
    print(f"reciprocal-mass diagnostic      = {reciprocal_mass_diagnostic:.15f}")

    print("\nopen-channel observables")
    print(f"density m(1.5)                  = {probe_density:.15f}")
    print(f"boundary loss 2*pi*m(1.5)      = {boundary_loss:.15f}")
    print(f"threshold density coefficient   = {threshold_density_coefficient:.15f}")
    for offset in (1e-2, 1e-4, 1e-6):
        ratio = spectral_density(BOSON_MASS + offset) / math.sqrt(offset)
        print(f"m(mu+{offset:.0e})/sqrt(offset) = {ratio:.15f}")

    print("\nFourier route coincidence and tail")
    for time in (0.0, 2.0, 10.0, 40.0, 80.0):
        radial = memory_radial(time)
        density = memory_density(time)
        route_error = abs(radial - density)
        if time:
            scaled = radial * cmath.exp(1j * BOSON_MASS * time) * time**1.5
            tail_error = abs(scaled - expected_scaled_memory)
            print(
                f"t={time:5.1f}: route error={route_error:.3e} "
                f"scaled={scaled!s:>34} tail error={tail_error:.3e}"
            )
        else:
            print(f"t={time:5.1f}: route error={route_error:.3e} K(0)={radial}")
    print(f"expected scaled tail            = {expected_scaled_memory}")

    print("\ntwo-site moment chain")
    print(f"J2 coefficients b0,a1,b1       = {(b0, a1, b1)}")
    print(f"nodes                           = {nodes}")
    print(f"normalized weights              = {normalized_weights}")
    for order, (exact, chain) in enumerate(zip(moments, chain_moments)):
        print(
            f"mu_{order}: exact={exact:12.6f} chain={chain:12.6f} "
            f"error={abs(exact-chain):.3e}"
        )
    print(f"Sigma(-5) exact                 = {exact_sigma_far:.15f}")
    print(f"Sigma(-5) two-site              = {chain_sigma_far:.15f}")

    assert abs(radial_mass - exact_mass) < 2e-12
    assert abs(density_mass - exact_mass) < 2e-9
    assert leading_energy_shift < 0.0
    assert 0.0 < leading_residue < 1.0
    assert effective_mass_order_2 > PARTICLE_MASS
    assert probe_density > 0.0
    assert abs(
        spectral_density(BOSON_MASS + 1e-6) / 1e-3
        - threshold_density_coefficient
    ) < 5e-5
    for order in range(4):
        assert abs(moments[order] - chain_moments[order]) < 2e-11
    assert abs(moments[4] - chain_moments[4]) > 1e-3
    assert abs(chain_sigma_far - exact_sigma_far) < 2e-5
    assert abs(memory_radial(10.0) - memory_density(10.0)) < 2e-8
    scaled_80 = memory_radial(80.0) * cmath.exp(1j * BOSON_MASS * 80.0) * 80.0**1.5
    assert abs(scaled_80 - expected_scaled_memory) < 0.02
    print("\nall field-measure acceptance checks passed")


if __name__ == "__main__":
    main()
