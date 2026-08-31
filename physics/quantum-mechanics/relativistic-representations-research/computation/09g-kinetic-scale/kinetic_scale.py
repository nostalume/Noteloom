"""N9g: evaluate the same-measure kinetic generator and its scale audit."""

from __future__ import annotations

import math


PARTICLE_MASS = 2.0
BOSON_MASS = 1.0
CUTOFF = 1.0
LEVEL_GAP = 1.5
COUPLING = 0.01
RADIAL_LIMIT = 8.0


def simpson(function, left: float, right: float, intervals: int) -> float:
    if intervals % 2:
        raise ValueError("Simpson interval count must be even")
    step = (right - left) / intervals
    total = function(left) + function(right)
    total += 4.0 * sum(function(left + step * i) for i in range(1, intervals, 2))
    total += 2.0 * sum(function(left + step * i) for i in range(2, intervals, 2))
    return total * step / 3.0


def dispersion(radius: float) -> float:
    return math.sqrt(radius * radius + BOSON_MASS * BOSON_MASS)


def channel_energy(radius: float) -> float:
    return dispersion(radius) + radius * radius / (2.0 * PARTICLE_MASS)


def form_factor_squared(radius: float) -> float:
    return math.exp(-(radius / CUTOFF) ** 2)


def radial_from_energy(energy: float) -> float:
    omega = -PARTICLE_MASS + math.sqrt(
        PARTICLE_MASS**2
        + BOSON_MASS**2
        + 2.0 * PARTICLE_MASS * energy
    )
    return math.sqrt(max(0.0, omega * omega - BOSON_MASS**2))


def density_without_coupling(energy: float) -> float:
    if energy <= BOSON_MASS:
        return 0.0
    radius = radial_from_energy(energy)
    omega = dispersion(radius)
    derivative = radius * (1.0 / omega + 1.0 / PARTICLE_MASS)
    return (
        4.0
        * math.pi
        * radius**2
        * form_factor_squared(radius)
        / derivative
    )


def principal_value_shift_without_coupling() -> float:
    """PV integral m_0(x)/(Delta-x) dx after x=mu+y^2."""

    maximum_energy = channel_energy(RADIAL_LIMIT)
    maximum_root = math.sqrt(maximum_energy - BOSON_MASS)
    pole_root = math.sqrt(LEVEL_GAP - BOSON_MASS)

    def transformed(root: float) -> float:
        energy = BOSON_MASS + root * root
        return 2.0 * root * density_without_coupling(energy)

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


def n9f_amplitude_remainder(time: float) -> float:
    beta_squared = math.pi**1.5 * CUTOFF**3
    beta = math.sqrt(beta_squared)
    three_vertex_constant = (
        math.sqrt(3.0) * (math.sqrt(2.0) + math.sqrt(3.0)) * beta**3
    )
    return abs(COUPLING) ** 3 * time**3 * three_vertex_constant / 6.0


def main() -> None:
    on_shell_density = density_without_coupling(LEVEL_GAP)
    gamma_0 = 2.0 * math.pi * on_shell_density
    delta_0 = principal_value_shift_without_coupling()
    kinetic_lifetime = 1.0 / gamma_0
    physical_lifetime = kinetic_lifetime / COUPLING**2
    finite_g_rate = COUPLING**2 * gamma_0

    print("same-measure kinetic generator")
    print(f"m_0(Delta)                       = {on_shell_density:.15f}")
    print(f"gamma_0=2*pi*m_0(Delta)          = {gamma_0:.15f}")
    print(f"delta_0=PV integral              = {delta_0:.15f}")
    print(f"kinetic lifetime 1/gamma_0       = {kinetic_lifetime:.15f}")
    print(f"physical lifetime at g=0.01      = {physical_lifetime:.15f}")
    print(f"finite-g boundary rate Gamma     = {finite_g_rate:.15f}")

    print("\nbounded kinetic law versus secular tangent")
    for lifetime_units in (0.1, 0.25, 0.5, 1.0, 2.0):
        tau = lifetime_units / gamma_0
        physical_time = tau / COUPLING**2
        emitted = 1.0 - math.exp(-lifetime_units)
        linear = lifetime_units
        phase = delta_0 * tau
        print(
            f"Gamma*t={lifetime_units:4.2f}: tau={tau:.12f} "
            f"t={physical_time:10.6f} exp-event={emitted:.12f} "
            f"linear={linear:.12f} phase={phase:.12f}"
        )

    probe_time = 80.0
    probe_tau = COUPLING**2 * probe_time
    probe_exponent = gamma_0 * probe_tau
    probe_event = 1.0 - math.exp(-probe_exponent)
    probe_remainder = n9f_amplitude_remainder(probe_time)
    lifetime_remainder = n9f_amplitude_remainder(physical_lifetime)
    print("\nN9d/N9f bridge audit")
    print(f"t=80 kinetic exponent Gamma*t    = {probe_exponent:.15f}")
    print(f"t=80 exponential comparator      = {probe_event:.15f}")
    print(f"t=80 secular tangent              = {probe_exponent:.15f}")
    print(f"t=80 tangent curvature difference = {probe_exponent-probe_event:.15f}")
    print(f"N9f amplitude bound at t=80       = {probe_remainder:.15f}")
    print(f"N9f bound at one kinetic lifetime = {lifetime_remainder:.15f}")

    assert abs(finite_g_rate - 0.002578281629203) < 2e-15
    assert abs(COUPLING**2 * delta_0 - (-0.000207454527144)) < 2e-15
    assert 387.0 < physical_lifetime < 389.0
    assert 0.18 < probe_event < 0.19
    assert probe_remainder > 1.0
    assert lifetime_remainder > probe_remainder
    print("\nall kinetic-scale acceptance checks passed")


if __name__ == "__main__":
    main()
