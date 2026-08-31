"""Compare several reconstructions of N9a's coupling spectral measure.

The exact normalized density is lambda*exp(-lambda). Its two-site Jacobi
truncation is the Gaussian quadrature determined by the first four moments.
"""

from __future__ import annotations

import cmath
import math


G = 0.16
E0 = 0.10
EULER_GAMMA = 0.5772156649015329


def ei_negative(x: float, tolerance: float = 2e-16) -> float:
    if x >= 0.0:
        raise ValueError("this regression needs Ei only below zero")
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


def exact_sigma(energy: float) -> float:
    if energy >= 0.0:
        raise ValueError("ordinary self-energy is used only below threshold")
    return G * (energy * math.exp(-energy) * ei_negative(energy) - 1.0)


SQRT3 = math.sqrt(3.0)
NODES = (3.0 - SQRT3, 3.0 + SQRT3)
WEIGHTS = (0.5 * (1.0 + 1.0 / SQRT3), 0.5 * (1.0 - 1.0 / SQRT3))


def chain_sigma(energy: float) -> float:
    return G * sum(weight / (energy - node) for node, weight in zip(NODES, WEIGHTS))


def exact_memory(time: float) -> complex:
    return G / complex(1.0, time) ** 2


def chain_memory(time: float) -> complex:
    return G * sum(
        weight * cmath.exp(-1j * node * time)
        for node, weight in zip(NODES, WEIGHTS)
    )


def exact_euclidean(time: float) -> float:
    return G / (1.0 + time) ** 2


def chain_euclidean(time: float) -> float:
    return G * sum(
        weight * math.exp(-node * time)
        for node, weight in zip(NODES, WEIGHTS)
    )


def bisect(function, left: float, right: float, tolerance: float = 1e-14) -> float:
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


def main() -> None:
    exact_moments = [G * math.factorial(order + 1) for order in range(7)]
    chain_moments = [
        G * sum(weight * node**order for node, weight in zip(NODES, WEIGHTS))
        for order in range(7)
    ]

    exact_bound = bisect(lambda energy: energy - E0 - exact_sigma(energy), -2.0, -1e-14)
    chain_bound = bisect(lambda energy: energy - E0 - chain_sigma(energy), -2.0, -1e-14)

    print("two-site Jacobi realization")
    print("J_2 = [[2, sqrt(2)], [sqrt(2), 4]]")
    print(f"nodes                          = {NODES}")
    print(f"normalized weights             = {WEIGHTS}")
    print("\nmoment comparison")
    for order, (exact, chain) in enumerate(zip(exact_moments, chain_moments)):
        print(
            f"mu_{order}: exact={exact:12.6f} chain={chain:12.6f} "
            f"error={abs(exact-chain):.3e}"
        )

    print("\nreal-time memory")
    for time in (0.1, 0.5, 2.0, 10.0):
        exact = exact_memory(time)
        chain = chain_memory(time)
        print(
            f"t={time:4.1f}: exact={exact!s:>30} chain={chain!s:>30} "
            f"error={abs(exact-chain):.6e}"
        )

    print("\nEuclidean correlation")
    for time in (0.1, 0.5, 2.0, 10.0):
        exact = exact_euclidean(time)
        chain = chain_euclidean(time)
        print(
            f"tau={time:4.1f}: exact={exact:.12e} chain={chain:.12e} "
            f"error={abs(exact-chain):.6e}"
        )

    print("\nresolvent and threshold")
    for energy in (-0.25, -1.0, -5.0):
        exact = exact_sigma(energy)
        chain = chain_sigma(energy)
        print(
            f"z={energy:5.2f}: exact={exact:.12f} chain={chain:.12f} "
            f"error={abs(exact-chain):.6e}"
        )
    exact_threshold = -G
    chain_threshold = chain_sigma(-1e-14)
    print(f"Sigma(0-): exact={exact_threshold:.12f} chain={chain_threshold:.12f}")
    print(f"bound pole: exact={exact_bound:.12f} chain={chain_bound:.12f}")

    epsilon = 1e-8
    hidden_energy = 1000.0
    euclidean_differences = []
    for time in (1.0, 2.0, 4.0):
        altered = (1.0 - epsilon) * exact_euclidean(time) + (
            G * epsilon * math.exp(-hidden_energy * time)
        )
        euclidean_differences.append(abs(altered - exact_euclidean(time)))
    original_fourth = exact_moments[4]
    altered_fourth = (1.0 - epsilon) * original_fourth + G * epsilon * hidden_energy**4
    print("\nEuclidean finite-precision discriminator")
    print(f"max |Delta C_E| for tau=1,2,4 = {max(euclidean_differences):.12e}")
    print(f"original mu_4                   = {original_fourth:.12f}")
    print(f"altered mu_4                    = {altered_fourth:.12f}")

    for order in range(4):
        assert abs(exact_moments[order] - chain_moments[order]) < 1e-12
    assert abs(exact_moments[4] - chain_moments[4]) > 1.0
    assert abs(chain_memory(10.0)) > 50.0 * abs(exact_memory(10.0))
    assert abs(chain_bound - exact_bound) > 0.02
    assert max(euclidean_differences) < 5e-10
    assert altered_fourth > 50.0 * original_fourth
    print("\nall route-discrimination checks passed")


if __name__ == "__main__":
    main()
