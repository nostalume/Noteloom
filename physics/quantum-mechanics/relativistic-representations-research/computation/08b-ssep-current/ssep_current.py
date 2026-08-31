"""Numerical checks for the equilibrium SSEP current large-deviation node."""

from __future__ import annotations

import math


K_MAX = 8.0
SIMPSON_PANELS = 4096


def composite_simpson(function, left, right, panels=SIMPSON_PANELS):
    """Integrate a smooth scalar function on a fixed, reproducible grid."""

    if panels % 2:
        raise ValueError("Simpson quadrature requires an even panel count")
    step = (right - left) / panels
    total = function(left) + function(right)
    total += 4.0 * sum(
        function(left + index * step) for index in range(1, panels, 2)
    )
    total += 2.0 * sum(
        function(left + index * step) for index in range(2, panels, 2)
    )
    return step * total / 3.0


def susceptibility(rho):
    return rho * (1.0 - rho)


def omega(rho, tilt):
    return 2.0 * susceptibility(rho) * (math.cosh(tilt) - 1.0)


def f_integral(argument, panels=SIMPSON_PANELS):
    integrand = lambda k: math.log1p(argument * math.exp(-k * k))
    return (2.0 / math.pi) * composite_simpson(
        integrand, 0.0, K_MAX, panels=panels
    )


def f_prime_integral(argument, panels=SIMPSON_PANELS):
    def integrand(k):
        gaussian = math.exp(-k * k)
        return gaussian / (1.0 + argument * gaussian)

    return (2.0 / math.pi) * composite_simpson(
        integrand, 0.0, K_MAX, panels=panels
    )


def f_series(argument, terms=400):
    total = 0.0
    power = argument
    sign = 1.0
    for n in range(1, terms + 1):
        total += sign * power / (n ** 1.5)
        power *= argument
        sign *= -1.0
    return total / math.sqrt(math.pi)


def scaled_cgf(rho, tilt):
    return f_integral(omega(rho, tilt))


def scaled_cgf_prime(rho, tilt):
    chi = susceptibility(rho)
    return (
        2.0
        * chi
        * math.sinh(tilt)
        * f_prime_integral(omega(rho, tilt))
    )


def optimizing_tilt(rho, current, tolerance=1.0e-12):
    if current < 0.0:
        return -optimizing_tilt(rho, -current, tolerance)
    if current == 0.0:
        return 0.0

    lower = 0.0
    upper = 1.0
    while scaled_cgf_prime(rho, upper) < current:
        upper *= 2.0
        if upper > 128.0:
            raise RuntimeError("failed to bracket the Legendre optimizer")

    while upper - lower > tolerance:
        midpoint = (lower + upper) / 2.0
        if scaled_cgf_prime(rho, midpoint) < current:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2.0


def rate_function(rho, current):
    tilt = optimizing_tilt(rho, current)
    rate = tilt * current - scaled_cgf(rho, tilt)
    residual = scaled_cgf_prime(rho, tilt) - current
    return tilt, rate, residual


def main():
    rho = 0.5
    chi = susceptibility(rho)
    cumulant_2 = 2.0 * chi / math.sqrt(math.pi)
    cumulant_4 = (
        2.0 * chi - 6.0 * math.sqrt(2.0) * chi * chi
    ) / math.sqrt(math.pi)

    print(f"rho={rho:.6f} chi={chi:.6f}")
    print(f"scaled kappa_2={cumulant_2:.12f}")
    print(f"scaled kappa_4={cumulant_4:.12f}")

    derivative_step = 0.05
    mu_minus_2 = scaled_cgf(rho, -2.0 * derivative_step)
    mu_minus_1 = scaled_cgf(rho, -derivative_step)
    mu_zero = scaled_cgf(rho, 0.0)
    mu_plus_1 = scaled_cgf(rho, derivative_step)
    mu_plus_2 = scaled_cgf(rho, 2.0 * derivative_step)
    finite_kappa_2 = (
        mu_plus_1 - 2.0 * mu_zero + mu_minus_1
    ) / derivative_step**2
    finite_kappa_4 = (
        mu_minus_2
        - 4.0 * mu_minus_1
        + 6.0 * mu_zero
        - 4.0 * mu_plus_1
        + mu_plus_2
    ) / derivative_step**4
    cumulant_2_error = abs(finite_kappa_2 - cumulant_2)
    cumulant_4_error = abs(finite_kappa_4 - cumulant_4)
    print(
        f"finite-difference kappa_2={finite_kappa_2:.12f} "
        f"error={cumulant_2_error:.3e}"
    )
    print(
        f"finite-difference kappa_4={finite_kappa_4:.12f} "
        f"error={cumulant_4_error:.3e}"
    )

    print("\nintegral/series checks")
    max_series_error = 0.0
    for tilt in (0.1, 0.5, 1.0):
        argument = omega(rho, tilt)
        integral_value = f_integral(argument)
        series_value = f_series(argument)
        error = abs(integral_value - series_value)
        max_series_error = max(max_series_error, error)
        print(
            f"lambda={tilt:3.1f} omega={argument:.9f} "
            f"mu={integral_value:.12f} series_error={error:.3e}"
        )

    print("\nquadrature refinement checks")
    max_refinement_error = 0.0
    for tilt in (1.0, 4.0, 12.0):
        argument = omega(rho, tilt)
        coarse = f_integral(argument, panels=SIMPSON_PANELS // 2)
        fine = f_integral(argument, panels=SIMPSON_PANELS)
        error = abs(fine - coarse)
        max_refinement_error = max(max_refinement_error, error)
        print(
            f"lambda={tilt:4.1f} omega={argument:.6e} "
            f"mu={fine:.12f} refinement_error={error:.3e}"
        )

    derivative_grid = [scaled_cgf_prime(rho, n / 20.0) for n in range(81)]
    minimum_increment = min(
        right - left for left, right in zip(derivative_grid, derivative_grid[1:])
    )
    print(f"\nminimum mu' grid increment={minimum_increment:.3e}")

    print("\nLegendre checks")
    max_stationarity_residual = 0.0
    minimum_rate = math.inf
    for current in (0.0, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0):
        tilt, rate, residual = rate_function(rho, current)
        gaussian = math.sqrt(math.pi) * current * current / (4.0 * chi)
        max_stationarity_residual = max(
            max_stationarity_residual, abs(residual)
        )
        minimum_rate = min(minimum_rate, rate)
        ratio = rate / gaussian if gaussian else 1.0
        print(
            f"q={current:4.2f} lambda*={tilt:.10f} Phi={rate:.12f} "
            f"stationarity={residual:.3e} Phi/Phi_gauss={ratio:.8f}"
        )

    if max_series_error >= 1.0e-10:
        raise AssertionError("integral and convergent series disagree")
    if max_refinement_error >= 1.0e-10:
        raise AssertionError("quadrature refinement changed the integral")
    if max(cumulant_2_error, cumulant_4_error) >= 5.0e-6:
        raise AssertionError("finite-difference cumulants disagree")
    if minimum_increment < -1.0e-10:
        raise AssertionError("scaled CGF derivative is not monotone on the grid")
    if max_stationarity_residual >= 1.0e-9:
        raise AssertionError("Legendre stationarity residual is too large")
    if minimum_rate < -1.0e-10:
        raise AssertionError("computed rate function is negative")

    print("\nall acceptance criteria passed")


if __name__ == "__main__":
    main()
