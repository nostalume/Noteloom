"""N9f: explicit error certificates for N9d's two order-g^2 observables."""

from __future__ import annotations

import math


PARTICLE_MASS = 2.0
BOSON_MASS = 1.0
CUTOFF = 1.0
LEVEL_GAP = 1.5
COUPLING = 0.01
RADIAL_LIMIT = 8.0


def simpson(function, left: float, right: float, intervals: int = 50000) -> float:
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


def radial_integral(function, intervals: int = 50000) -> float:
    return 4.0 * math.pi * simpson(
        lambda radius: radius**2 * form_factor_squared(radius) * function(radius),
        0.0,
        RADIAL_LIMIT,
        intervals,
    )


def transition_kernel(detuning: float, time: float) -> float:
    argument = 0.5 * detuning * time
    if abs(argument) < 1e-7:
        sinc = 1.0 - argument**2 / 6.0 + argument**4 / 120.0
        return time * time * sinc * sinc
    return 4.0 * math.sin(argument) ** 2 / detuning**2


def emission_coefficient(time: float) -> float:
    intervals = max(50000, int(1500 * max(1.0, time)))
    if intervals % 2:
        intervals += 1
    return radial_integral(
        lambda radius: transition_kernel(
            LEVEL_GAP - channel_energy(radius), time
        ),
        intervals=intervals,
    )


def field_form_constant(alpha: float, beta: float, gap: float) -> float:
    return 2.0 * alpha / math.sqrt(gap) + beta / gap


def emission_certificate(time: float, beta: float) -> tuple[float, float, float]:
    leading_probability = COUPLING**2 * emission_coefficient(time)
    three_vertex_constant = (
        math.sqrt(3.0) * (math.sqrt(2.0) + math.sqrt(3.0)) * beta**3
    )
    amplitude_remainder = (
        abs(COUPLING) ** 3 * time**3 * three_vertex_constant / 6.0
    )
    probability_remainder = (
        2.0 * math.sqrt(leading_probability) * amplitude_remainder
        + amplitude_remainder**2
    )
    return leading_probability, amplitude_remainder, probability_remainder


def relative_emission_bound(time: float, beta: float) -> float:
    leading, _, remainder = emission_certificate(time, beta)
    return remainder / leading


def uniform_probability_remainder(time: float, beta: float) -> float:
    """Monotone bound valid simultaneously for every 0 <= s <= time."""

    three_vertex_constant = (
        math.sqrt(3.0) * (math.sqrt(2.0) + math.sqrt(3.0)) * beta**3
    )
    amplitude_remainder = (
        abs(COUPLING) ** 3 * time**3 * three_vertex_constant / 6.0
    )
    first_amplitude_bound = abs(COUPLING) * beta * time
    return (
        2.0 * first_amplitude_bound * amplitude_remainder
        + amplitude_remainder**2
    )


def bisect_horizon(beta: float, target: float, left: float, right: float) -> float:
    f_left = relative_emission_bound(left, beta) - target
    f_right = relative_emission_bound(right, beta) - target
    if f_left * f_right > 0.0:
        raise ValueError("requested horizon is not bracketed")
    for _ in range(45):
        middle = 0.5 * (left + right)
        f_middle = relative_emission_bound(middle, beta) - target
        if f_left * f_middle <= 0.0:
            right = middle
        else:
            left, f_left = middle, f_middle
    return 0.5 * (left + right)


def bisect_uniform_horizon(
    beta: float, tolerance: float, left: float, right: float
) -> float:
    if uniform_probability_remainder(left, beta) > tolerance:
        raise ValueError("left endpoint already exceeds the tolerance")
    if uniform_probability_remainder(right, beta) < tolerance:
        raise ValueError("right endpoint does not reach the tolerance")
    for _ in range(45):
        middle = 0.5 * (left + right)
        if uniform_probability_remainder(middle, beta) <= tolerance:
            left = middle
        else:
            right = middle
    return 0.5 * (left + right)


def main() -> None:
    beta_squared_analytic = math.pi**1.5 * CUTOFF**3
    beta_squared = radial_integral(lambda radius: 1.0)
    alpha_squared = radial_integral(lambda radius: 1.0 / dispersion(radius))
    beta = math.sqrt(beta_squared_analytic)
    alpha = math.sqrt(alpha_squared)

    # Xi=Z(-1)^N.  The ground vector has Xi=-1.  After removing it, the
    # free sector begins at min(2 mu, Delta+mu), not min(mu,Delta).
    ground_complement_gap = min(2.0 * BOSON_MASS, LEVEL_GAP + BOSON_MASS)
    opposite_parity_gap = min(BOSON_MASS, LEVEL_GAP)
    ground_form_constant = field_form_constant(
        alpha, beta, ground_complement_gap
    )
    opposite_form_constant = field_form_constant(alpha, beta, opposite_parity_gap)
    ground_margin = 1.0 - abs(COUPLING) * ground_form_constant
    opposite_margin = 1.0 - abs(COUPLING) * opposite_form_constant

    ground_stieltjes_mass = radial_integral(
        lambda radius: 1.0 / (LEVEL_GAP + channel_energy(radius))
    )
    leading_ground_shift = -(COUPLING**2) * ground_stieltjes_mass
    ground_remainder = COUPLING**4 * (
        ground_stieltjes_mass * ground_form_constant**2 / ground_margin
        + ground_stieltjes_mass**2
        / (ground_margin**3 * ground_complement_gap)
    )
    ground_relative_bound = ground_remainder / abs(leading_ground_shift)

    # A theorem-level certificate using only analytic inequalities.  Since
    # omega>=mu, alpha<=beta/sqrt(mu).  The Stieltjes mass is bounded above by
    # ||h||^2/(Delta+mu), and below by retaining the ball |k|<=Lambda and using
    # the largest denominator on that ball.
    alpha_upper = beta / math.sqrt(BOSON_MASS)
    theorem_form_constant = field_form_constant(
        alpha_upper, beta, ground_complement_gap
    )
    theorem_margin = 1.0 - abs(COUPLING) * theorem_form_constant
    theorem_opposite_constant = field_form_constant(
        alpha_upper, beta, opposite_parity_gap
    )
    theorem_opposite_margin = 1.0 - abs(COUPLING) * theorem_opposite_constant
    stieltjes_upper = beta_squared_analytic / (LEVEL_GAP + BOSON_MASS)
    ball_radius = CUTOFF
    ball_mass = (
        math.pi**1.5 * CUTOFF**3 * math.erf(ball_radius / CUTOFF)
        - 2.0
        * math.pi
        * CUTOFF**2
        * ball_radius
        * math.exp(-(ball_radius / CUTOFF) ** 2)
    )
    stieltjes_lower = ball_mass / (
        LEVEL_GAP + channel_energy(ball_radius)
    )
    theorem_ground_remainder = COUPLING**4 * (
        stieltjes_upper * theorem_form_constant**2 / theorem_margin
        + stieltjes_upper**2
        / (theorem_margin**3 * ground_complement_gap)
    )
    theorem_relative_bound = theorem_ground_remainder / (
        COUPLING**2 * stieltjes_lower
    )

    print("field norms and symmetry-reduced gaps")
    print(f"beta^2=||h||^2 radial          = {beta_squared:.15f}")
    print(f"beta^2 analytic                = {beta_squared_analytic:.15f}")
    print(f"alpha^2=||h/sqrt(omega)||^2    = {alpha_squared:.15f}")
    print(f"Xi=- ground-complement gap     = {ground_complement_gap:.12f}")
    print(f"Xi=+ opposite-sector gap       = {opposite_parity_gap:.12f}")
    print(f"ground form constant C_-       = {ground_form_constant:.12f}")
    print(f"opposite form constant C_+     = {opposite_form_constant:.12f}")
    print(f"positivity margin 1-|g|C_-     = {ground_margin:.12f}")
    print(f"positivity margin 1-|g|C_+     = {opposite_margin:.12f}")

    print("\nbound observable certificate")
    print(f"Stieltjes coefficient s        = {ground_stieltjes_mass:.15f}")
    print(f"order-g^2 ground shift         = {leading_ground_shift:.15f}")
    print(f"absolute remainder bound       = {ground_remainder:.15f}")
    print(f"relative remainder bound       = {ground_relative_bound:.6%}")
    print("analytic-majorant theorem certificate")
    print(f"alpha upper bound              = {alpha_upper:.15f}")
    print(f"analytic C_- / C_+             = {(theorem_form_constant, theorem_opposite_constant)}")
    print(f"analytic margins - / +         = {(theorem_margin, theorem_opposite_margin)}")
    print(f"Stieltjes lower/upper          = {(stieltjes_lower, stieltjes_upper)}")
    print(f"absolute theorem remainder     = {theorem_ground_remainder:.15f}")
    print(f"relative theorem remainder     = {theorem_relative_bound:.6%}")

    print("\nopen observable certificate")
    for time in (1.0, 5.0, 10.0, 20.0, 40.0, 80.0):
        leading, amplitude_remainder, probability_remainder = emission_certificate(
            time, beta
        )
        relative = probability_remainder / leading
        uniform_remainder = uniform_probability_remainder(time, beta)
        verdict = "certified" if relative < 1.0 else "vacuous"
        print(
            f"t={time:5.1f}: P2={leading:.12f} "
            f"||r3||<={amplitude_remainder:.12f} "
            f"|dP|<={probability_remainder:.12f} "
            f"eval-relative<={relative:.3%} "
            f"uniform-|dP|<={uniform_remainder:.12f} {verdict}"
        )

    ten_percent_horizon = bisect_horizon(beta, 0.10, 5.0, 20.0)
    nonvacuous_horizon = bisect_horizon(beta, 1.0, 5.0, 20.0)
    uniform_millipoint_horizon = bisect_uniform_horizon(beta, 0.001, 0.0, 20.0)
    uniform_centipoint_horizon = bisect_uniform_horizon(beta, 0.01, 0.0, 20.0)
    print("\npointwise relative-bound crossings in bracket [5,20]")
    print(f"10% relative crossing          = {ten_percent_horizon:.12f}")
    print(f"100% relative crossing         = {nonvacuous_horizon:.12f}")
    print("\nuniform absolute-error windows")
    print(
        f"|dP|<=0.001 for all t<=        = {uniform_millipoint_horizon:.12f}"
    )
    print(
        f"|dP|<=0.01 for all t<=         = {uniform_centipoint_horizon:.12f}"
    )

    assert abs(beta_squared - beta_squared_analytic) < 2e-12
    assert ground_margin > 0.9
    assert opposite_margin > 0.9
    assert ground_relative_bound < 0.002
    assert theorem_margin > 0.9
    assert theorem_opposite_margin > 0.9
    assert theorem_relative_bound < 0.01
    assert relative_emission_bound(5.0, beta) < 0.04
    assert relative_emission_bound(20.0, beta) > 1.0
    assert 5.0 < ten_percent_horizon < nonvacuous_horizon < 20.0
    assert 5.0 < uniform_millipoint_horizon < uniform_centipoint_horizon < 20.0
    print("\nall certified-window acceptance checks passed")


if __name__ == "__main__":
    main()
