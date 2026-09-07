"""Word-native Gaussian evaluation of retained Anderson functional insertions."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import math

import numpy as np

from .car_words import factor_car_insertion
from .graded_return import FunctionalPortRefusal, FunctionalRestrictionPacket
from .impurity import AndersonSystem, car_annihilator
from .numeric import ordered_simplex


@dataclass(frozen=True)
class LinearCarAction:
    creation: bool
    coefficients: tuple[complex, ...]
    time: float


@dataclass(frozen=True)
class WickReceipt:
    value: complex
    kernel_entries: int
    pfaffian_updates: int


@dataclass(frozen=True)
class WordNativeFunctionalReceipt:
    word_occurrences: int
    distinct_word_count: int
    combined_word_terms: int
    reconstructed_bath_matrices: int
    quadrature_cells: int
    event_cells: int
    wick_evaluations: int
    pfaffian_updates: int
    local_contractions: int
    cache_hits: int
    counts_by_quadrature: tuple[int, int]
    quadrature_discrepancy: float
    estimated_operations: int
    endpoint_baseline_operations: int


def _numeric_pfaffian(matrix: np.ndarray) -> tuple[complex, int]:
    size = matrix.shape[0]
    if size % 2:
        return 0j, 0
    if size == 0:
        return 1.0 + 0j, 0
    work = np.asarray(matrix, dtype=complex).copy()
    value = 1.0 + 0j
    updates = 0
    for left in range(0, size, 2):
        pivot_column = left + 1 + int(np.argmax(abs(work[left, left + 1:])))
        if abs(work[left, pivot_column]) <= 1e-15:
            return 0j, updates
        if pivot_column != left + 1:
            work[[left + 1, pivot_column], :] = work[[pivot_column, left + 1], :]
            work[:, [left + 1, pivot_column]] = work[:, [pivot_column, left + 1]]
            value = -value
        pivot = work[left, left + 1]
        value *= pivot
        for row in range(left + 2, size):
            for column in range(row + 1, size):
                work[row, column] -= (
                    work[left, row] * work[left + 1, column]
                    - work[left, column] * work[left + 1, row]
                ) / pivot
                work[column, row] = -work[row, column]
                updates += 1
    return complex(value), updates


def thermal_wick_expectation(
    actions: tuple[LinearCarAction, ...],
    energies: tuple[float, ...],
    beta: float,
) -> WickReceipt:
    """Evaluate an ordered free-thermal CAR word through its generated Pfaffian."""
    mode_count = len(energies)
    if beta <= 0 or not math.isfinite(beta):
        raise ValueError("inverse temperature must be finite and positive")
    if any(len(action.coefficients) != mode_count for action in actions):
        raise ValueError("linear CAR action has the wrong mode count")
    if len(actions) % 2:
        return WickReceipt(0j, 0, 0)

    energy_array = np.asarray(energies, dtype=float)
    occupations = 1.0 / (np.exp(beta * energy_array) + 1.0)
    evolved = tuple(
        np.asarray(action.coefficients, dtype=complex)
        * np.exp((1 if action.creation else -1) * energy_array * action.time)
        for action in actions
    )
    size = len(actions)
    kernel = np.zeros((size, size), dtype=complex)
    entries = 0
    for left in range(size):
        for right in range(left + 1, size):
            first = actions[left]
            second = actions[right]
            if first.creation == second.creation:
                continue
            occupation = occupations if first.creation else 1.0 - occupations
            kernel[left, right] = np.sum(
                evolved[left] * evolved[right] * occupation,
            )
            kernel[right, left] = -kernel[left, right]
            entries += 1
    value, updates = _numeric_pfaffian(kernel)
    return WickReceipt(value, entries, updates)


def _local_data(system: AndersonSystem):
    annihilators = tuple(car_annihilator(mode, 2) for mode in range(2))
    numbers = tuple(action.conj().T @ action for action in annihilators)
    hamiltonian = (
        system.request.impurity_energy * (numbers[0] + numbers[1])
        + system.request.interaction * numbers[0] @ numbers[1]
    )
    energies = np.diag(hamiltonian).real
    parity = np.diag([(-1) ** state.bit_count() for state in range(4)])
    factors = {
        (spin, True): parity @ annihilators[spin]
        for spin in range(2)
    } | {
        (spin, False): annihilators[spin].conj().T @ parity
        for spin in range(2)
    }
    return energies, factors


def _evolve_local(operator: np.ndarray, energies: np.ndarray, time: float):
    return np.exp(time * (energies[:, None] - energies[None, :])) * operator


def _event_action(system: AndersonSystem, event, time: float) -> LinearCarAction:
    spin, creation = event
    coefficients = []
    for coupling in system.request.hybridizations:
        for bath_spin in range(2):
            coefficient = 0j
            if spin == bath_spin:
                coefficient = coupling if creation else complex(coupling).conjugate()
            coefficients.append(coefficient)
    return LinearCarAction(creation, tuple(coefficients), time)


def _word_actions(label, mode_count: int) -> tuple[LinearCarAction, ...]:
    creation_mask, annihilation_mask = label
    actions = []
    for mode in range(mode_count):
        if creation_mask & (1 << mode):
            coefficients = tuple(
                1.0 if index == mode else 0.0
                for index in range(mode_count)
            )
            actions.append(LinearCarAction(True, coefficients, 0.0))
    for mode in reversed(range(mode_count)):
        if annihilation_mask & (1 << mode):
            coefficients = tuple(
                1.0 if index == mode else 0.0
                for index in range(mode_count)
            )
            actions.append(LinearCarAction(False, coefficients, 0.0))
    return tuple(actions)


def anderson_word_native_functional(
    system: AndersonSystem,
    valuations: tuple[int, ...],
    local_dimension: int,
    quadrature_order: int,
    resource_budget: int,
    word_budget: int,
):
    """Construct a reduced thermal functional from CAR words, never bath matrices."""
    def evaluate(operators: tuple[np.ndarray, ...]) -> FunctionalRestrictionPacket:
        if quadrature_order < 3:
            raise FunctionalPortRefusal(
                "word-native quadrature order must be at least three",
            )
        if local_dimension != 4:
            raise FunctionalPortRefusal("word-native v1 requires a four-state local sector")
        if len(operators) != len(valuations):
            raise FunctionalPortRefusal("valuation count does not match graded basis")

        creation = system.impurity_annihilator.conj().T
        decompositions = tuple(
            factor_car_insertion(
                operator @ creation + creation @ operator,
                local_dimension=local_dimension,
                tolerance=1e-10,
            )
            for operator in operators
        )
        grouped: dict[tuple[int, int], dict[int, np.ndarray]] = {}
        occurrence_count = 0
        for operator_index, decomposition in enumerate(decompositions):
            if decomposition.residual > 2e-9:
                raise FunctionalPortRefusal("word-native insertion reconstruction failed")
            for term in decomposition.terms:
                for label, coefficient in zip(
                    term.bath_words.labels,
                    term.bath_words.coefficients,
                    strict=True,
                ):
                    occurrence_count += 1
                    by_operator = grouped.setdefault(label, {})
                    contribution = coefficient * term.local_operator
                    by_operator[operator_index] = (
                        by_operator.get(operator_index, np.zeros_like(contribution))
                        + contribution
                    )
        if occurrence_count > word_budget:
            raise FunctionalPortRefusal("word-native CAR word budget exceeded")

        order = system.request.coefficient_order
        sizes = (quadrature_order - 1, quadrature_order)
        maximum_pfaffian_updates = 22
        event_estimate = sum(
            (4 * size) ** degree
            for size in sizes
            for degree in range(order + 1)
        )
        estimate = (
            sum(
                degree * local_dimension**3 * (4 * size) ** degree
                for size in sizes
                for degree in range(order + 1)
            )
            + event_estimate * (
                occurrence_count * local_dimension**2
                + (len(grouped) + 1) * maximum_pfaffian_updates
            )
        )
        if estimate > resource_budget:
            raise FunctionalPortRefusal("word-native functional budget exceeded")

        local_energies, local_factors = _local_data(system)
        local_thermal = np.diag(np.exp(-system.request.beta * local_energies))
        bath_energies = tuple(
            energy
            for energy in system.request.bath_energies
            for _ in range(2)
        )
        bath_partition = math.prod(
            1.0 + math.exp(-system.request.beta * energy)
            for energy in bath_energies
        )
        event_types = tuple(
            (spin, creation)
            for spin in range(2)
            for creation in (False, True)
        )
        word_action_map = {
            label: _word_actions(label, len(bath_energies))
            for label in grouped
        }

        def integrate(size: int):
            partitions = np.zeros(order + 1, dtype=complex)
            restrictions = np.zeros((order + 1, len(operators)), dtype=complex)
            quadrature_cells = event_cells = wick_evaluations = 0
            pfaffian_updates = local_contractions = requests = endpoint_wicks = 0
            local_chain_operations = 0
            for degree in range(order + 1):
                sign = (-1) ** degree
                for times, weight in ordered_simplex(system.request.beta, degree, size):
                    quadrature_cells += 1
                    for events in product(event_types, repeat=degree):
                        event_cells += 1
                        local_chain = np.eye(local_dimension, dtype=complex)
                        for event, time in zip(events, times, strict=True):
                            local_chain @= _evolve_local(
                                local_factors[event], local_energies, time,
                            )
                            local_chain_operations += local_dimension**3
                        event_actions = tuple(
                            _event_action(system, event, time)
                            for event, time in zip(events, times, strict=True)
                        )
                        event_charge = sum(1 if event[1] else -1 for event in events)
                        if event_charge == 0:
                            wick = thermal_wick_expectation(
                                event_actions, bath_energies, system.request.beta,
                            )
                            partitions[degree] += (
                                sign * weight * bath_partition * wick.value
                                * np.trace(local_thermal @ local_chain)
                            )
                            wick_evaluations += 1
                            pfaffian_updates += wick.pfaffian_updates

                        for label, by_operator in grouped.items():
                            word_charge = label[0].bit_count() - label[1].bit_count()
                            word_degree = label[0].bit_count() + label[1].bit_count()
                            if event_charge + word_charge or (degree + word_degree) % 2:
                                continue
                            local_values = tuple(
                                (operator_index, np.trace(
                                    local_thermal @ local_chain @ local_operator,
                                ))
                                for operator_index, local_operator in by_operator.items()
                            )
                            local_contractions += len(local_values)
                            active = tuple(
                                value for value in local_values if abs(value[1]) > 1e-14
                            )
                            if not active:
                                continue
                            wick = thermal_wick_expectation(
                                event_actions + word_action_map[label],
                                bath_energies,
                                system.request.beta,
                            )
                            wick_evaluations += 1
                            endpoint_wicks += 1
                            pfaffian_updates += wick.pfaffian_updates
                            requests += len(active)
                            common = sign * weight * bath_partition * wick.value
                            for operator_index, local_value in active:
                                restrictions[degree, operator_index] += common * local_value
            operations = (
                local_chain_operations
                + local_dimension**2 * local_contractions
                + pfaffian_updates
            )
            return (
                partitions,
                restrictions,
                quadrature_cells,
                event_cells,
                wick_evaluations,
                pfaffian_updates,
                local_contractions,
                requests,
                endpoint_wicks,
                operations,
            )

        low = integrate(quadrature_order - 1)
        high = integrate(quadrature_order)
        discrepancy = float(max(
            np.max(abs(high[0] - low[0])),
            np.max(abs(high[1] - low[1])),
        ))
        rank = len(operators)
        dimension = system.free_hamiltonian.shape[0]
        receipt = WordNativeFunctionalReceipt(
            word_occurrences=occurrence_count,
            distinct_word_count=len(grouped),
            combined_word_terms=sum(len(by_operator) for by_operator in grouped.values()),
            reconstructed_bath_matrices=0,
            quadrature_cells=low[2] + high[2],
            event_cells=low[3] + high[3],
            wick_evaluations=low[4] + high[4],
            pfaffian_updates=low[5] + high[5],
            local_contractions=low[6] + high[6],
            cache_hits=(low[7] + high[7]) - (low[8] + high[8]),
            counts_by_quadrature=(low[4], high[4]),
            quadrature_discrepancy=discrepancy,
            estimated_operations=low[9] + high[9],
            endpoint_baseline_operations=(
                (order + 1) * dimension**3
                + (order + 1) * rank * dimension**2
            ),
        )
        if receipt.estimated_operations > resource_budget:
            raise FunctionalPortRefusal("word-native functional budget exceeded")
        return FunctionalRestrictionPacket(
            partition_coefficients=tuple(complex(value) for value in high[0]),
            restrictions=tuple(
                tuple(complex(value) for value in row)
                for row in high[1]
            ),
            kind="word-native Gaussian functional",
            error=discrepancy,
            cells=low[3] + high[3],
            materialized_endpoint_matrices=0,
            metadata=receipt,
        )

    return evaluate
