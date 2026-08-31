"""Standard-library regression for N9a's rank-one Friedrichs model.

Units: continuum threshold and cutoff scale are both normalized to 0 and 1.
The coupling density is m(lambda)=G*lambda*exp(-lambda).
"""

from __future__ import annotations

import cmath
import math


G = 0.16
BOUND_E0 = 0.10
OPEN_E0 = 0.60
EULER_GAMMA = 0.5772156649015329


def ei_series(x: float, tolerance: float = 2e-16) -> float:
    """Real Ei(x) from its convergent series, for the range used here."""
    if x == 0.0:
        return -math.inf
    term = x
    total = term
    for k in range(2, 10000):
        term *= x / k
        addition = term / k
        total += addition
        if abs(addition) <= tolerance * max(1.0, abs(total)):
            break
    else:
        raise RuntimeError("Ei series did not converge")
    return EULER_GAMMA + math.log(abs(x)) + total


def scaled_ei_positive(x: float) -> float:
    """Return exp(-x) Ei(x) without overflow on the integration tail."""
    if x < 30.0:
        return math.exp(-x) * ei_series(x)
    inverse = 1.0 / x
    term = inverse
    total = term
    previous = abs(term)
    for k in range(1, 10000):
        term *= k * inverse
        if abs(term) > previous:
            break
        total += term
        previous = abs(term)
    return total


def coupling_density(energy: float) -> float:
    return G * energy * math.exp(-energy) if energy >= 0.0 else 0.0


def delta(energy: float) -> float:
    """Principal-value real self-energy Delta(E)."""
    if energy == 0.0:
        return -G
    scaled_ei = (
        math.exp(-energy) * ei_series(energy)
        if energy < 0.0
        else scaled_ei_positive(energy)
    )
    return G * (energy * scaled_ei - 1.0)


def sigma_derivative_below(energy: float) -> float:
    if energy >= 0.0:
        raise ValueError("ordinary derivative is used only below threshold")
    scaled_ei = math.exp(-energy) * ei_series(energy)
    return G * ((1.0 - energy) * scaled_ei + 1.0)


def denominator_real(energy: float, bare_energy: float) -> float:
    return energy - bare_energy - delta(energy)


def bisect(function, left: float, right: float, tolerance: float = 1e-14) -> float:
    f_left = function(left)
    f_right = function(right)
    if f_left == 0.0:
        return left
    if f_right == 0.0:
        return right
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


def simpson(function, left: float, right: float) -> float:
    middle = 0.5 * (left + right)
    return (right - left) * (function(left) + 4.0 * function(middle) + function(right)) / 6.0


def adaptive_simpson(
    function, left: float, right: float, tolerance: float = 1e-11, depth: int = 24
) -> float:
    whole = simpson(function, left, right)

    def refine(a: float, b: float, estimate: float, tol: float, remaining: int) -> float:
        middle = 0.5 * (a + b)
        left_estimate = simpson(function, a, middle)
        right_estimate = simpson(function, middle, b)
        correction = left_estimate + right_estimate - estimate
        if remaining == 0 or abs(correction) <= 15.0 * tol:
            return left_estimate + right_estimate + correction / 15.0
        return refine(a, middle, left_estimate, tol / 2.0, remaining - 1) + refine(
            middle, b, right_estimate, tol / 2.0, remaining - 1
        )

    return refine(left, right, whole, tolerance, depth)


def prepared_continuum_density(energy: float, bare_energy: float) -> float:
    if energy == 0.0:
        return 0.0
    m = coupling_density(energy)
    a = denominator_real(energy, bare_energy)
    return m / (a * a + (math.pi * m) ** 2)


def continuum_weight(bare_energy: float, cutoff: float) -> float:
    density = lambda energy: prepared_continuum_density(energy, bare_energy)
    # Splitting at 1 resolves the threshold and any resonance peak separately.
    return adaptive_simpson(density, 0.0, 1.0) + adaptive_simpson(density, 1.0, cutoff)


def scattering_factor(energy: float, bare_energy: float) -> complex:
    a = denominator_real(energy, bare_energy)
    imaginary = math.pi * coupling_density(energy)
    return complex(a, -imaginary) / complex(a, imaginary)


def memory(time: float) -> complex:
    return G / complex(1.0, time) ** 2


def main() -> None:
    bound_energy = bisect(
        lambda energy: denominator_real(energy, BOUND_E0), -2.0, -1e-15
    )
    derivative = sigma_derivative_below(bound_energy)
    bound_weight = 1.0 / (1.0 - derivative)
    bound_continuum_30 = continuum_weight(BOUND_E0, 30.0)
    bound_continuum_40 = continuum_weight(BOUND_E0, 40.0)

    resonance_center = bisect(
        lambda energy: denominator_real(energy, OPEN_E0), 1e-15, 2.0
    )
    resonance_m = coupling_density(resonance_center)
    width_scale = 2.0 * math.pi * resonance_m
    open_continuum_30 = continuum_weight(OPEN_E0, 30.0)
    open_continuum_40 = continuum_weight(OPEN_E0, 40.0)

    sample_energies = (0.01, 0.1, resonance_center, 1.0, 4.0)
    maximum_unitarity_error = max(
        abs(abs(scattering_factor(energy, OPEN_E0)) - 1.0)
        for energy in sample_energies
    )

    print(f"coupling mass                 = {G:.15f}")
    print(f"K(2)                          = {memory(2.0)}")
    print(f"|K(100)| * 100^2              = {abs(memory(100.0)) * 100.0**2:.15f}")
    for horizon in (10.0, 100.0, 1000.0):
        first_moment = 0.5 * G * math.log1p(horizon * horizon)
        print(f"memory first moment T={horizon:6.0f} = {first_moment:.15f}")

    print("\nbound case")
    print(f"bare energy                   = {BOUND_E0:.15f}")
    print(f"bound energy                  = {bound_energy:.15f}")
    print(f"pole residual                 = {abs(denominator_real(bound_energy, BOUND_E0)):.3e}")
    print(f"Sigma'(bound energy)          = {derivative:.15f}")
    print(f"bound prepared weight Z       = {bound_weight:.15f}")
    print(f"continuum weight, cutoff 30   = {bound_continuum_30:.15f}")
    print(f"continuum weight, cutoff 40   = {bound_continuum_40:.15f}")
    print(f"normalization residual        = {abs(bound_weight + bound_continuum_40 - 1.0):.3e}")

    print("\nopen case")
    print(f"bare energy                   = {OPEN_E0:.15f}")
    print(f"threshold denominator D(0-)   = {G - OPEN_E0:.15f}")
    print(f"on-shell center A(E*)=0       = {resonance_center:.15f}")
    print(f"coupling density m(E*)        = {resonance_m:.15f}")
    print(f"width scale 2*pi*m(E*)        = {width_scale:.15f}")
    print(f"continuum weight, cutoff 30   = {open_continuum_30:.15f}")
    print(f"continuum weight, cutoff 40   = {open_continuum_40:.15f}")
    print(f"normalization residual        = {abs(open_continuum_40 - 1.0):.3e}")
    print(f"max sampled |S|-1 error       = {maximum_unitarity_error:.3e}")

    assert abs(denominator_real(bound_energy, BOUND_E0)) < 1e-12
    assert derivative < 0.0
    assert abs(bound_weight + bound_continuum_40 - 1.0) < 2e-8
    assert abs(open_continuum_40 - 1.0) < 2e-8
    assert abs(bound_continuum_40 - bound_continuum_30) < 2e-10
    assert abs(open_continuum_40 - open_continuum_30) < 2e-10
    assert maximum_unitarity_error < 1e-12
    print("\nall acceptance checks passed")


if __name__ == "__main__":
    main()
