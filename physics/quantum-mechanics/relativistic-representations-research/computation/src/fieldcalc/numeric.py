"""Bounded numerical integration shared by research constructions."""

from dataclasses import dataclass
from itertools import product
import math

import numpy as np
from scipy.integrate import quad


@dataclass(frozen=True)
class Quadrature:
    value: float
    error: float
    evaluations: int


def integrate(function, support, absolute_tolerance: float) -> Quadrature:
    if not math.isfinite(absolute_tolerance) or absolute_tolerance <= 0:
        raise ValueError("absolute tolerance must be finite and positive")
    output = quad(
        function, *support, epsabs=absolute_tolerance,
        epsrel=absolute_tolerance, limit=300, full_output=1,
    )
    return Quadrature(output[0], output[1], output[2]["neval"])


def ordered_simplex(beta: float, dimension: int, quadrature_order: int):
    """Generate product-Gauss cells mapped to an ordered time simplex."""
    if dimension < 0:
        raise ValueError("simplex dimension must be nonnegative")
    raw_nodes, raw_weights = np.polynomial.legendre.leggauss(quadrature_order)
    nodes = 0.5 * (raw_nodes + 1.0)
    weights = 0.5 * raw_weights
    for indices in product(range(quadrature_order), repeat=dimension):
        fractions = [nodes[index] for index in indices]
        times = []
        current = beta
        for fraction in fractions:
            current *= fraction
            times.append(current)
        jacobian = beta**dimension
        for index, fraction in enumerate(fractions[:-1]):
            jacobian *= fraction ** (dimension - index - 1)
        yield tuple(times), jacobian * math.prod(weights[index] for index in indices)
