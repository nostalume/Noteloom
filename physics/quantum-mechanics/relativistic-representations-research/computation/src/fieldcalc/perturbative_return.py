"""Perturbative Green coefficients from one endpoint correlation functional."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .impurity import AndersonSystem
from .rewrite import Refusal


@dataclass(frozen=True)
class PerturbativeReturnCost:
    block_dimension: int
    endpoint_exponential_actions: int
    moment_generator_actions: int
    resolvent_actions_per_query: int
    retained_operators: int
    retained_moment_scalars: int
    estimated_setup_operations: int
    baseline_time_nodes: int
    baseline_exponential_actions: int


@dataclass(frozen=True)
class PerturbativeReturnModel:
    system: AndersonSystem
    coefficient_order: int
    thermal_coefficients: tuple[np.ndarray, ...]
    source_duals: tuple[np.ndarray, ...]
    partition_coefficients: tuple[complex, ...]
    moments: tuple[tuple[complex, ...], ...]
    free_energies: np.ndarray
    free_vectors: np.ndarray
    cost: PerturbativeReturnCost

    def _free_resolvent(self, z: complex, value: np.ndarray) -> np.ndarray:
        vectors = self.free_vectors
        transformed = vectors.conj().T @ value @ vectors
        differences = self.free_energies[None, :] - self.free_energies[:, None]
        solved = transformed / (z - differences)
        return vectors @ solved @ vectors.conj().T

    def green_coefficients(self, z: complex) -> tuple[complex, ...]:
        z = complex(z)
        if not math.isfinite(z.real) or not math.isfinite(z.imag):
            raise ValueError("spectral parameter must be finite")
        if z.imag == 0:
            raise ValueError("perturbative return requires an off-axis query")

        interaction = self.system.hybridization_action
        source = self.system.impurity_annihilator
        resolvent_coefficients = [self._free_resolvent(z, source)]
        for _ in range(self.coefficient_order):
            previous = resolvent_coefficients[-1]
            forcing = previous @ interaction - interaction @ previous
            resolvent_coefficients.append(self._free_resolvent(z, forcing))

        numerator = tuple(
            sum(
                np.vdot(self.source_duals[left], resolvent_coefficients[order - left])
                for left in range(order + 1)
            )
            for order in range(self.coefficient_order + 1)
        )
        return _series_divide(numerator, self.partition_coefficients)

    def moment_green_coefficients(
        self,
        z: complex,
        count: int,
    ) -> tuple[complex, ...]:
        z = complex(z)
        if z.imag == 0:
            raise ValueError("moment return requires an off-axis query")
        if count < 1 or count > len(self.moments):
            raise ValueError("moment count lies outside the generated packet")
        return tuple(
            sum(
                self.moments[moment][order] / z ** (moment + 1)
                for moment in range(count)
            )
            for order in range(self.coefficient_order + 1)
        )

    def zeroth_hankel_rank(self, depth: int, tolerance: float = 1e-10) -> int:
        if depth < 1 or 2 * depth - 1 > len(self.moments):
            raise ValueError("Hankel depth lies outside the generated moments")
        hankel = np.asarray([
            [self.moments[left + right][0] for right in range(depth)]
            for left in range(depth)
        ], dtype=complex)
        singular_values = np.linalg.svd(hankel, compute_uv=False)
        scale = max(1.0, float(singular_values[0]))
        return int(np.count_nonzero(singular_values > tolerance * scale))


@dataclass(frozen=True)
class PerturbativeReturnCompilation:
    model: PerturbativeReturnModel | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def _series_divide(
    numerator: tuple[complex, ...],
    denominator: tuple[complex, ...],
) -> tuple[complex, ...]:
    if abs(denominator[0]) <= 1e-14:
        raise ValueError("correlation functional has zero normalization")
    quotient: list[complex] = []
    for order, value in enumerate(numerator):
        correction = sum(
            denominator[index] * quotient[order - index]
            for index in range(1, order + 1)
        )
        quotient.append(complex((value - correction) / denominator[0]))
    return tuple(quotient)


def _refuse(system: AndersonSystem, reason: str) -> PerturbativeReturnCompilation:
    return PerturbativeReturnCompilation(
        refusal=Refusal(reason, provenance=system.request.provenance),
    )


def compile_perturbative_return(
    system: AndersonSystem,
    moment_order: int,
    resource_budget: int,
    coefficient_order: int | None = None,
) -> PerturbativeReturnCompilation:
    order = system.request.coefficient_order if coefficient_order is None else coefficient_order
    if order < 0 or order > 6:
        return _refuse(
            system,
            "coefficient order lies outside the perturbative return boundary",
        )
    if order != system.request.coefficient_order:
        return _refuse(system, "coefficient order differs from the generated system")
    if moment_order < 1:
        return _refuse(system, "moment order must be positive")

    dimension = system.free_hamiltonian.shape[0]
    nonzero_free = int(np.count_nonzero(abs(system.free_hamiltonian) > 1e-14))
    nonzero_interaction = int(np.count_nonzero(abs(system.hybridization_action) > 1e-14))
    endpoint_cost = (order + 1) * dimension**3
    generator_cost = (
        moment_order
        * (order + 1)
        * 2
        * (nonzero_free + nonzero_interaction)
        * dimension
    )
    correlation_cost = (moment_order + 1) * (order + 1) ** 2 * dimension**2
    setup_operations = endpoint_cost + generator_cost + correlation_cost
    if setup_operations > resource_budget:
        return _refuse(system, "perturbative return budget exceeded")

    thermal = system.thermal_coefficients(system.request.beta)
    source = system.impurity_annihilator
    duals = tuple(value @ source + source @ value for value in thermal)
    partition = tuple(complex(np.trace(value)) for value in thermal)

    free = system.free_hamiltonian
    interaction = system.hybridization_action
    operator_coefficients = [
        source.copy() if index == 0 else np.zeros_like(source)
        for index in range(order + 1)
    ]
    moments: list[tuple[complex, ...]] = []
    for _ in range(moment_order + 1):
        numerator = tuple(
            sum(
                np.vdot(duals[left], operator_coefficients[degree - left])
                for left in range(degree + 1)
            )
            for degree in range(order + 1)
        )
        moments.append(_series_divide(numerator, partition))
        next_coefficients = []
        for degree, value in enumerate(operator_coefficients):
            generated = value @ free - free @ value
            if degree:
                previous = operator_coefficients[degree - 1]
                generated += previous @ interaction - interaction @ previous
            next_coefficients.append(generated)
        operator_coefficients = next_coefficients

    energies, vectors = np.linalg.eigh(free)
    return PerturbativeReturnCompilation(PerturbativeReturnModel(
        system=system,
        coefficient_order=order,
        thermal_coefficients=tuple(thermal),
        source_duals=duals,
        partition_coefficients=partition,
        moments=tuple(moments),
        free_energies=energies,
        free_vectors=vectors,
        cost=PerturbativeReturnCost(
            block_dimension=(order + 1) * dimension,
            endpoint_exponential_actions=1,
            moment_generator_actions=moment_order * (order + 1),
            resolvent_actions_per_query=order + 1,
            retained_operators=2 * (order + 1),
            retained_moment_scalars=(moment_order + 1) * (order + 1),
            estimated_setup_operations=setup_operations,
            baseline_time_nodes=system.request.quadrature_order,
            baseline_exponential_actions=2 * system.request.quadrature_order + 1,
        ),
    ))
