"""Domain adapters for the bounded repeated-Pauli route family."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

import exact_gaussian_matrix as gaussian
from coefficient_projector_jet import CoefficientJet, ProjectorJetBudget
from complete_route_leverage import CoefficientRouteProblem
from exact_gaussian_linear import matrix_vector
from finite_window_propagation import FinitePropagationWindow
from represented_star_algebra import StarAlgebraBudget, StarGenerator, construct
from simple_block_pde import RealizationBudget, construct_irreducible_model


def _outer(left, right):
    return tuple(
        tuple(left[row] * right[column].conjugate() for column in range(len(right)))
        for row in range(len(left))
    )


def _standard_vector(dimension: int, selected: int):
    return tuple(gaussian.ONE if index == selected else gaussian.ZERO for index in range(dimension))


def repeated_pauli_problem(multiplicity: int, window_size: int) -> CoefficientRouteProblem:
    dimension = 2 * multiplicity
    identity = np.eye(multiplicity, dtype=int)
    generators = (
        StarGenerator(
            "X",
            gaussian.matrix(np.kron(np.array([[0, 1], [1, 0]], dtype=int), identity).tolist(), "X"),
        ),
        StarGenerator(
            "Z",
            gaussian.matrix(
                np.kron(np.array([[1, 0], [0, -1]], dtype=int), identity).tolist(), "Z"
            ),
        ),
    )
    algebra = construct(generators, StarAlgebraBudget(dimension, 2, dimension * dimension, 128))
    model = construct_irreducible_model(algebra, 0, RealizationBudget(dimension * dimension, 128))
    projector = model.selected_projector
    complement = gaussian.add(gaussian.identity(dimension), gaussian.scale(projector, -1))
    retained = model.embedding_columns[0]
    outside = None
    for index in range(dimension):
        candidate = matrix_vector(complement, _standard_vector(dimension, index))
        if any(entry != gaussian.ZERO for entry in candidate):
            outside = candidate
            break
    if outside is None:
        raise ValueError("the repeated carrier must have a complement")
    crossing = _outer(outside, retained)
    transport = gaussian.add(crossing, gaussian.scale(gaussian.dagger(crossing), -1))
    value = gaussian.add(gaussian.scale(projector, 2), gaussian.scale(complement, 5))
    first = gaussian.bracket(transport, value)
    acceleration = gaussian.add(crossing, gaussian.dagger(crossing))
    second = gaussian.add(gaussian.bracket(transport, first), acceleration)
    momenta = tuple(Fraction(index + 1, 2) for index in range(window_size))
    window = FinitePropagationWindow(
        momenta,
        (Fraction(3),) * window_size,
        Fraction(1, 5),
        Fraction(1),
        ((gaussian.ONE, gaussian.ONE),) * window_size,
    )
    return CoefficientRouteProblem(
        model,
        CoefficientJet(value, first, second, Fraction(2)),
        ProjectorJetBudget(dimension, 128),
        window,
    )
