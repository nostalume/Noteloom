"""Action-factored determinant expansion for a finite Anderson system."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import math

import numpy as np

from .impurity import AndersonSystem, car_annihilator
from .numeric import ordered_simplex


@dataclass(frozen=True)
class ContractionReceipt:
    expanded: complex
    determinant: complex
    graph_count: int
    kernel_entries: int


@dataclass(frozen=True)
class DeterminantCost:
    determinant_cells: int
    pairing_histories: int
    quadrature_points: int


@dataclass(frozen=True)
class DeterminantGreenCoefficients:
    values: tuple[complex, ...]
    cost: DeterminantCost


def _expanded_determinant(kernel: np.ndarray) -> complex:
    width = kernel.shape[0]
    if width == 0:
        return 1.0 + 0.0j
    return sum(
        (-1) ** column
        * kernel[0, column]
        * _expanded_determinant(np.delete(kernel[1:], column, axis=1))
        for column in range(width)
    )


def compress_fermion_contractions(kernel) -> ContractionReceipt:
    """Generate the signed pairing sum and its determinant quotient."""
    matrix = np.asarray(kernel, dtype=complex)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("fermion contraction kernel must be square")
    if matrix.shape[0] > 8:
        raise ValueError("expanded pairing certificate is limited to grade eight")
    return ContractionReceipt(
        expanded=_expanded_determinant(matrix),
        determinant=np.linalg.det(matrix),
        graph_count=math.factorial(matrix.shape[0]),
        kernel_entries=matrix.size,
    )


def _local_data(system: AndersonSystem):
    annihilators = tuple(car_annihilator(mode, 2) for mode in range(2))
    numbers = tuple(action.conj().T @ action for action in annihilators)
    hamiltonian = (
        system.request.impurity_energy * (numbers[0] + numbers[1])
        + system.request.interaction * numbers[0] @ numbers[1]
    )
    energies = np.diag(hamiltonian).real
    parity = np.diag([(-1) ** state.bit_count() for state in range(4)])
    return annihilators, energies, parity


def _evolve_local(operator, energies, time):
    return np.exp(time * (energies[:, None] - energies[None, :])) * operator


def _balanced_events(order: int):
    event_types = tuple(
        (spin, creation)
        for spin in range(2)
        for creation in (False, True)
    )
    return tuple(
        sequence
        for sequence in product(event_types, repeat=order)
        if all(
            sum(spin == selected and creation for spin, creation in sequence)
            == sum(spin == selected and not creation for spin, creation in sequence)
            for selected in range(2)
        )
    )


def _bath_pair(system, left, right, time_difference: float) -> complex:
    left_spin, left_creation = left
    right_spin, right_creation = right
    if left_spin != right_spin or left_creation == right_creation:
        return 0j
    value = 0j
    for energy, coupling in zip(
        system.request.bath_energies,
        system.request.hybridizations,
        strict=True,
    ):
        occupation = 1.0 / (math.exp(system.request.beta * energy) + 1.0)
        weight = abs(coupling) ** 2
        if not left_creation:
            value += weight * math.exp(-energy * time_difference) * (1.0 - occupation)
        else:
            value += weight * math.exp(energy * time_difference) * occupation
    return value


def _bath_determinant(system, events, times) -> complex:
    order = len(events)
    contractions = np.zeros((order, order), dtype=complex)
    for left in range(order):
        for right in range(left + 1, order):
            contraction = _bath_pair(
                system,
                events[left],
                events[right],
                times[left] - times[right],
            )
            contractions[left, right] = contraction
            contractions[right, left] = -contraction
    annihilations = [index for index, event in enumerate(events) if not event[1]]
    creations = [index for index, event in enumerate(events) if event[1]]
    permutation = annihilations + creations
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(order)
        for right in range(left + 1, order)
    )
    half = order // 2
    grouped = contractions[np.ix_(permutation, permutation)]
    determinant = np.linalg.det(grouped[:half, half:])
    sign = (-1) ** (inversions + half * (half - 1) // 2)
    return complex(sign * determinant)


def _pairing_count(events) -> int:
    return math.prod(
        math.factorial(sum(
            spin == selected and not creation
            for spin, creation in events
        ))
        for selected in range(2)
    )


def _bath_partition(system: AndersonSystem) -> float:
    return math.prod(
        (1.0 + math.exp(-system.request.beta * energy)) ** 2
        for energy in system.request.bath_energies
    )


def determinant_green_coefficients(
    system: AndersonSystem,
    quadrature_order: int,
) -> DeterminantGreenCoefficients:
    """Evaluate the Green series after action-generated bath factorization."""
    if quadrature_order < 3:
        raise ValueError("determinant quadrature order must be at least three")
    maximum_order = system.request.coefficient_order
    estimated_cells = sum(
        len(_balanced_events(order))
        * (quadrature_order**order + (order + 1) * quadrature_order ** (order + 1))
        for order in range(2, maximum_order + 1, 2)
    )
    if estimated_cells > system.request.resource_budget:
        raise ValueError("determinant transfer budget exceeded")

    annihilators, energies, parity = _local_data(system)
    thermal = np.diag(np.exp(-system.request.beta * energies))
    bath_partition = _bath_partition(system)
    partition = np.zeros(maximum_order + 1, dtype=complex)
    numerator = np.zeros(maximum_order + 1, dtype=complex)
    partition[0] = np.trace(thermal) * bath_partition
    determinant_cells = pairing_histories = quadrature_points = 0
    local_factors = {
        (spin, True): parity @ annihilators[spin]
        for spin in range(2)
    } | {
        (spin, False): annihilators[spin].conj().T @ parity
        for spin in range(2)
    }

    for order in range(2, maximum_order + 1, 2):
        sequences = tuple(
            (events, _pairing_count(events))
            for events in _balanced_events(order)
        )
        for times, weight in ordered_simplex(
            system.request.beta, order, quadrature_order,
        ):
            quadrature_points += 1
            for events, pairing_count in sequences:
                bath = bath_partition * _bath_determinant(system, events, times)
                local = np.eye(4, dtype=complex)
                for event, time in zip(events, times, strict=True):
                    local @= _evolve_local(local_factors[event], energies, time)
                partition[order] += weight * np.trace(thermal @ local) * bath
                determinant_cells += 1
                pairing_histories += pairing_count

    external_creation = annihilators[0].conj().T
    for order in range(0, maximum_order + 1, 2):
        sequences = tuple(
            (events, _pairing_count(events))
            for events in _balanced_events(order)
        )
        for external_rank in range(order + 1):
            for ordered_times, weight in ordered_simplex(
                system.request.beta, order + 1, quadrature_order,
            ):
                quadrature_points += 1
                external_time = ordered_times[external_rank]
                event_times = ordered_times[:external_rank] + ordered_times[external_rank + 1:]
                phase = np.exp(1j * system.matsubara_frequency * external_time)
                for events, pairing_count in sequences:
                    bath = (
                        bath_partition
                        if order == 0
                        else bath_partition * _bath_determinant(system, events, event_times)
                    )
                    local = np.eye(4, dtype=complex)
                    event_index = 0
                    for rank, time in enumerate(ordered_times):
                        if rank == external_rank:
                            operator = _evolve_local(annihilators[0], energies, time)
                        else:
                            event = events[event_index]
                            event_index += 1
                            operator = _evolve_local(local_factors[event], energies, time)
                        local @= operator
                    numerator[order] -= (
                        weight * phase * np.trace(thermal @ local @ external_creation) * bath
                    )
                    if order:
                        determinant_cells += 1
                        pairing_histories += pairing_count

    values = np.zeros(maximum_order + 1, dtype=complex)
    for order in range(maximum_order + 1):
        correction = sum(
            partition[index] * values[order - index]
            for index in range(1, order + 1)
        )
        values[order] = (numerator[order] - correction) / partition[0]
    return DeterminantGreenCoefficients(
        values=tuple(complex(value) for value in values),
        cost=DeterminantCost(
            determinant_cells=determinant_cells,
            pairing_histories=pairing_histories,
            quadrature_points=quadrature_points,
        ),
    )
