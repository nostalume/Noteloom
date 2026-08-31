"""N9d regression: one field Hamiltonian, bound and emitted-boson observables.

The calculation retains the complete coefficient through order g^2.  It does
not exponentiate the excited-state loss or claim a finite-coupling resonance.
"""

from __future__ import annotations

import cmath
import math


PARTICLE_MASS = 2.0
BOSON_MASS = 1.0
CUTOFF = 1.0
LEVEL_GAP = 1.5
COUPLING = 0.01
RADIAL_LIMIT = 8.0


def simpson(function, left: float, right: float, intervals: int):
    if intervals % 2:
        raise ValueError("Simpson interval count must be even")
    step = (right - left) / intervals
    total = function(left) + function(right)
    total += 4.0 * sum(function(left + step * index) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(left + step * index) for index in range(2, intervals, 2))
    return total * step / 3.0


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


def radial_measure_integral(function, intervals: int = 50000):
    prefactor = 4.0 * math.pi * COUPLING**2
    return prefactor * simpson(
        lambda radius: radius**2
        * form_factor_squared(radius)
        * function(channel_energy(radius), radius),
        0.0,
        RADIAL_LIMIT,
        intervals,
    )


def density_measure_integral(function, intervals: int = 100000):
    maximum_energy = channel_energy(RADIAL_LIMIT)
    maximum_root = math.sqrt(maximum_energy - BOSON_MASS)
    return simpson(
        lambda root: 2.0
        * root
        * spectral_density(BOSON_MASS + root * root)
        * function(BOSON_MASS + root * root),
        0.0,
        maximum_root,
        intervals,
    )


def transition_kernel(detuning: float, time: float) -> float:
    argument = 0.5 * detuning * time
    if abs(argument) < 1e-7:
        # 4 sin^2(detuning*t/2)/detuning^2 = t^2 sinc(argument)^2.
        sinc = 1.0 - argument**2 / 6.0 + argument**4 / 120.0
        return time * time * sinc * sinc
    return 4.0 * math.sin(argument) ** 2 / detuning**2


def emitted_probability_radial(time: float) -> float:
    intervals = max(60000, int(2000 * max(1.0, time)))
    if intervals % 2:
        intervals += 1
    return radial_measure_integral(
        lambda energy, radius: transition_kernel(LEVEL_GAP - energy, time),
        intervals=intervals,
    )


def emitted_probability_density(time: float) -> float:
    intervals = max(100000, int(2500 * max(1.0, time)))
    if intervals % 2:
        intervals += 1
    return density_measure_integral(
        lambda energy: transition_kernel(LEVEL_GAP - energy, time),
        intervals=intervals,
    )


def memory(time: float) -> complex:
    return radial_measure_integral(
        lambda energy, radius: cmath.exp(-1j * energy * time),
        intervals=max(60000, 2000 * math.ceil(max(1.0, time) / 2.0)),
    )


def principal_value_excited_shift() -> float:
    """PV integral m(x)/(Delta-x) dx after x=mu+y^2."""

    maximum_energy = channel_energy(RADIAL_LIMIT)
    maximum_root = math.sqrt(maximum_energy - BOSON_MASS)
    pole_root = math.sqrt(LEVEL_GAP - BOSON_MASS)

    def transformed(root: float) -> float:
        energy = BOSON_MASS + root * root
        return 2.0 * root * spectral_density(energy)

    pole_value = transformed(pole_root)
    derivative_step = 1e-5
    pole_derivative = (
        transformed(pole_root + derivative_step)
        - transformed(pole_root - derivative_step)
    ) / (2.0 * derivative_step)

    def regularized(root: float) -> float:
        denominator = pole_root * pole_root - root * root
        if abs(root - pole_root) < 1e-8:
            return -pole_derivative / (2.0 * pole_root)
        return (transformed(root) - pole_value) / denominator

    regular_part = simpson(regularized, 0.0, maximum_root, 160000)
    singular_part = pole_value / (2.0 * pole_root) * math.log(
        abs((pole_root + maximum_root) / (pole_root - maximum_root))
    )
    return regular_part + singular_part


def five_point_second_derivative(function, point: float, step: float) -> float:
    return (
        -function(point + 2.0 * step)
        + 16.0 * function(point + step)
        - 30.0 * function(point)
        + 16.0 * function(point - step)
        - function(point - 2.0 * step)
    ) / (12.0 * step * step)


def main() -> None:
    measure_mass = radial_measure_integral(lambda energy, radius: 1.0)

    ground_shift = -radial_measure_integral(
        lambda energy, radius: 1.0 / (LEVEL_GAP + energy)
    )
    ground_residue = 1.0 - radial_measure_integral(
        lambda energy, radius: 1.0 / (LEVEL_GAP + energy) ** 2
    )
    mass_response = radial_measure_integral(
        lambda energy, radius: radius**2 / (LEVEL_GAP + energy) ** 3
    )
    inverse_ground_mass = 1.0 / PARTICLE_MASS - (
        2.0 / (3.0 * PARTICLE_MASS**2)
    ) * mass_response
    ground_mass_order_2 = PARTICLE_MASS + PARTICLE_MASS**2 * (
        1.0 / PARTICLE_MASS - inverse_ground_mass
    )

    excited_shift = principal_value_excited_shift()
    boundary_density = spectral_density(LEVEL_GAP)
    golden_rate = 2.0 * math.pi * boundary_density

    print("two-level field and operator-valued departure measure")
    print(f"particle mass M                 = {PARTICLE_MASS:.12f}")
    print(f"boson mass mu                   = {BOSON_MASS:.12f}")
    print(f"level gap Delta                 = {LEVEL_GAP:.12f}")
    print(f"coupling g                      = {COUPLING:.12f}")
    print(f"base channel measure mass       = {measure_mass:.15f}")

    print("\nbound preparation |g,Omega>")
    print(f"order-g^2 ground shift          = {ground_shift:.15f}")
    print(f"order-g^2 ground residue        = {ground_residue:.15f}")
    print(f"order-g^2 inverse ground mass   = {inverse_ground_mass:.15f}")
    print(f"order-g^2 ground mass expansion = {ground_mass_order_2:.15f}")

    print("\nopen preparation |e,Omega>")
    print(f"PV excited energy shift         = {excited_shift:.15f}")
    print(f"on-shell density m(Delta)       = {boundary_density:.15f}")
    print(f"boundary/FGR rate 2*pi*m        = {golden_rate:.15f}")

    print("\nfinite-time emitted-boson event")
    route_errors = []
    for time in (1.0, 5.0, 20.0, 40.0, 80.0):
        probability = emitted_probability_radial(time)
        density_probability = emitted_probability_density(time)
        route_error = abs(probability - density_probability)
        route_errors.append(route_error)
        print(
            f"t={time:5.1f}: P_emit^(2)={probability:.12f} "
            f"P_survive^(2)={1.0-probability:.12f} "
            f"P/t={probability/time:.12f} "
            f"route error={route_error:.3e}"
        )

    witness_time = 5.0
    step = 0.002
    probability_curvature = five_point_second_derivative(
        emitted_probability_radial, witness_time, step
    )
    memory_curvature = 2.0 * (
        cmath.exp(1j * LEVEL_GAP * witness_time) * memory(witness_time)
    ).real
    curvature_error = abs(probability_curvature - memory_curvature)
    print("\nmemory/event coincidence")
    print(f"P_emit''(5) finite difference   = {probability_curvature:.15f}")
    print(f"2 Re[e^(i Delta t)K(t)]         = {memory_curvature:.15f}")
    print(f"coincidence error               = {curvature_error:.3e}")

    probability_80 = emitted_probability_radial(80.0)
    relative_rate_error = abs(probability_80 / 80.0 - golden_rate) / golden_rate
    perturbative_horizon = golden_rate * 80.0

    assert 0.0 < ground_residue < 1.0
    assert ground_shift < 0.0
    assert ground_mass_order_2 > PARTICLE_MASS
    assert boundary_density > 0.0
    assert excited_shift < 0.0
    assert max(route_errors) < 2e-12
    assert curvature_error < 2e-9
    assert relative_rate_error < 0.08
    assert perturbative_horizon < 0.25
    print(f"relative rate error at t=80     = {relative_rate_error:.3e}")
    print(f"Gamma*t perturbative horizon    = {perturbative_horizon:.3e}")
    print("\nall operational-channel acceptance checks passed")


if __name__ == "__main__":
    main()
