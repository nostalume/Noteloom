"""Coupling-graded cyclic reduction for perturbative scalar returns."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import math

import numpy as np

from .perturbative_return import PerturbativeReturnModel
from .rewrite import Refusal


@dataclass(frozen=True)
class GradedReturnCost:
    ambient_operator_dimension: int
    reduced_dimension: int
    free_spectral_projections: int
    interaction_generator_actions: int
    orthogonalization_candidates: int
    estimated_construction_operations: int
    full_query_operations: int
    reduced_query_operations: int
    break_even_queries: int | None
    retained_complex_scalars: int
    source_packet_complex_scalars: int


@dataclass(frozen=True)
class GradedCyclicReturnModel:
    coefficient_order: int
    partition_coefficients: tuple[complex, ...]
    valuations: tuple[int, ...]
    filtration_ranks: tuple[int, ...]
    free_generator: np.ndarray
    interaction_generator: np.ndarray
    reduced_source: np.ndarray
    reduced_duals: tuple[np.ndarray, ...]
    free_closure_residual: float
    graded_interaction_residual: float
    functional_kind: str
    functional_error: float
    functional_cells: int
    materialized_endpoint_matrices: int
    functional_metadata: object | None
    cost: GradedReturnCost

    @property
    def rank(self) -> int:
        return self.free_generator.shape[0]

    def green_coefficients(self, z: complex) -> tuple[complex, ...]:
        z = complex(z)
        if not math.isfinite(z.real) or not math.isfinite(z.imag):
            raise ValueError("spectral parameter must be finite")
        if z.imag == 0:
            raise ValueError("graded return requires an off-axis query")

        operator = z * np.eye(self.rank) - self.free_generator
        values = [np.linalg.solve(operator, self.reduced_source)]
        for _ in range(self.coefficient_order):
            values.append(np.linalg.solve(
                operator,
                self.interaction_generator @ values[-1],
            ))

        numerator = tuple(
            sum(
                np.vdot(self.reduced_duals[left], values[order - left])
                for left in range(order + 1)
            )
            for order in range(self.coefficient_order + 1)
        )
        return _series_divide(
            numerator,
            self.partition_coefficients,
        )


@dataclass(frozen=True)
class GradedReturnCompilation:
    model: GradedCyclicReturnModel | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


class _BudgetExceeded(Exception):
    pass


class FunctionalPortRefusal(ValueError):
    pass


@dataclass(frozen=True)
class FunctionalRestrictionPacket:
    partition_coefficients: tuple[complex, ...]
    restrictions: tuple[tuple[complex, ...], ...]
    kind: str
    error: float
    cells: int
    materialized_endpoint_matrices: int
    metadata: object | None = None


FunctionalFactory = Callable[
    [tuple[np.ndarray, ...]],
    FunctionalRestrictionPacket,
]


def _series_divide(numerator, denominator) -> tuple[complex, ...]:
    quotient: list[complex] = []
    for order, value in enumerate(numerator):
        correction = sum(
            denominator[index] * quotient[order - index]
            for index in range(1, order + 1)
        )
        quotient.append(complex((value - correction) / denominator[0]))
    return tuple(quotient)


def _refuse(
    source: PerturbativeReturnModel,
    reason: str,
) -> GradedReturnCompilation:
    return GradedReturnCompilation(
        refusal=Refusal(reason, provenance=source.system.request.provenance),
    )


def compile_graded_cyclic_return(
    source: PerturbativeReturnModel,
    resource_budget: int,
    tolerance: float = 1e-10,
    functional_factory: FunctionalFactory | None = None,
) -> GradedReturnCompilation:
    if tolerance <= 0 or not math.isfinite(tolerance):
        return _refuse(source, "rank tolerance must be positive")

    system = source.system
    free = system.free_hamiltonian
    interaction = system.hybridization_action
    hermitian_residual = max(
        float(np.linalg.norm(free - free.conj().T)),
        float(np.linalg.norm(interaction - interaction.conj().T)),
    )
    if hermitian_residual > tolerance:
        return _refuse(source, "return action is not Hermitian")

    hilbert_dimension = free.shape[0]
    ambient = hilbert_dimension**2
    order = source.coefficient_order
    vectors = source.free_vectors
    energies = source.free_energies
    energy_interaction = vectors.conj().T @ interaction @ vectors
    energy_source = vectors.conj().T @ system.impurity_annihilator @ vectors
    nonzero_interaction = int(np.count_nonzero(abs(energy_interaction) > tolerance))
    interaction_action_cost = 2 * nonzero_interaction * hilbert_dimension

    basis: list[np.ndarray] = []
    valuations: list[int] = []
    gap_labels: list[float] = []
    operation_count = 0
    spectral_projections = 0
    interaction_actions = 0
    candidates = 0
    interaction_images_by_basis: dict[int, np.ndarray] = {}

    # The free eigensystem is already owned by node 46. This count covers only the
    # additional operator changes of basis retained by the reduced module.
    operation_count += 2 * (order + 2) * hilbert_dimension**3

    raw_gaps = (energies[None, :] - energies[:, None]).reshape(-1)
    sorted_indices = np.argsort(raw_gaps)
    gap_groups: list[np.ndarray] = []
    current: list[int] = []
    current_gap = 0.0
    for index in sorted_indices:
        gap = float(raw_gaps[index])
        if not current:
            current_gap = gap
        elif abs(gap - current_gap) > tolerance:
            gap_groups.append(np.asarray(current, dtype=int))
            current = []
            current_gap = gap
        current.append(int(index))
    if current:
        gap_groups.append(np.asarray(current, dtype=int))

    def spend(amount: int) -> None:
        nonlocal operation_count
        operation_count += amount
        if operation_count > resource_budget:
            raise _BudgetExceeded

    def interaction_action(vector: np.ndarray) -> np.ndarray:
        nonlocal interaction_actions
        spend(interaction_action_cost)
        interaction_actions += 1
        value = vector.reshape(hilbert_dimension, hilbert_dimension)
        return (
            value @ energy_interaction - energy_interaction @ value
        ).reshape(-1)

    def admit(vector: np.ndarray, grade: int, gap: float) -> int | None:
        nonlocal candidates
        candidates += 1
        residual = np.asarray(vector, dtype=complex).reshape(-1).copy()
        original_norm = float(np.linalg.norm(residual))
        if original_norm == 0:
            return None
        for _ in range(2):
            for existing, existing_gap in zip(basis, gap_labels, strict=True):
                if abs(existing_gap - gap) > tolerance:
                    continue
                spend(4 * ambient)
                residual -= existing * np.vdot(existing, residual)
        norm = float(np.linalg.norm(residual))
        if norm <= tolerance * max(1.0, original_norm):
            return None
        basis.append(residual / norm)
        valuations.append(grade)
        gap_labels.append(gap)
        return len(basis) - 1

    def spectral_close(vector: np.ndarray, grade: int) -> list[int]:
        nonlocal spectral_projections
        spend(ambient)
        generated = []
        for indices in gap_groups:
            component = np.zeros(ambient, dtype=complex)
            component[indices] = vector[indices]
            if np.linalg.norm(component) <= tolerance:
                continue
            spectral_projections += 1
            gap = float(raw_gaps[indices[0]])
            admitted = admit(component, grade, gap)
            if admitted is not None:
                generated.append(admitted)
        return generated

    try:
        source_indices = spectral_close(energy_source.reshape(-1), 0)
        if not source_indices:
            return _refuse(source, "return source has zero rank")
        filtration_ranks = [len(basis)]

        for grade in range(1, order + 1):
            previous = tuple(
                (index, vector)
                for index, (vector, valuation) in enumerate(
                    zip(basis, valuations, strict=True)
                )
                if valuation == grade - 1
            )
            for index, vector in previous:
                image = interaction_action(vector)
                interaction_images_by_basis[index] = image
                spectral_close(image, grade)
            filtration_ranks.append(len(basis))
    except _BudgetExceeded:
        return _refuse(source, "graded return budget exceeded")

    serialized = np.column_stack(basis)
    reduced_free = np.diag(gap_labels)
    free_images = serialized @ reduced_free
    interaction_columns = []
    for index, grade in enumerate(valuations):
        if grade < order:
            interaction_columns.append(interaction_images_by_basis[index])
        else:
            interaction_columns.append(np.zeros(ambient, dtype=complex))
    interaction_images = np.column_stack(interaction_columns)
    reduced_interaction = serialized.conj().T @ interaction_images
    free_residual = float(np.linalg.norm(
        free_images - serialized @ reduced_free,
    ))

    graded_residual = 0.0
    for index, grade in enumerate(valuations):
        if grade >= order:
            continue
        target_rank = filtration_ranks[grade + 1]
        target = serialized[:, :target_rank]
        value = interaction_images[:, index]
        residual = value - target @ (target.conj().T @ value)
        graded_residual = max(graded_residual, float(np.linalg.norm(residual)))

    reduced_source = serialized.conj().T @ energy_source.reshape(-1)
    rank = len(basis)
    if functional_factory is None:
        energy_duals = tuple(
            vectors.conj().T @ value @ vectors
            for value in source.source_duals
        )
        reduced_duals = tuple(
            serialized.conj().T @ value.reshape(-1)
            for value in energy_duals
        )
        functional = FunctionalRestrictionPacket(
            partition_coefficients=source.partition_coefficients,
            restrictions=tuple(
                tuple(complex(np.vdot(dual, vector)) for vector in basis)
                for dual in energy_duals
            ),
            kind="endpoint dual matrices",
            error=0.0,
            cells=0,
            materialized_endpoint_matrices=2 * (order + 1),
        )
    else:
        original_basis = tuple(
            vectors @ vector.reshape(hilbert_dimension, hilbert_dimension)
            @ vectors.conj().T
            for vector in basis
        )
        try:
            functional = functional_factory(original_basis)
        except FunctionalPortRefusal as error:
            return _refuse(source, str(error))
        if (
            len(functional.partition_coefficients) != order + 1
            or len(functional.restrictions) != order + 1
            or any(len(row) != rank for row in functional.restrictions)
        ):
            return _refuse(source, "functional port shape does not match graded module")
        reduced_duals = tuple(
            np.conjugate(np.asarray(row, dtype=complex))
            for row in functional.restrictions
        )

    pairings = (order + 1) * (order + 2) // 2
    full_query = (
        (order + 1) * ambient
        + order * interaction_action_cost
        + pairings * ambient
    )
    reduced_query = (
        rank**3
        + (2 * order + 1) * rank**2
        + pairings * rank
    )
    saving = full_query - reduced_query
    break_even = (
        None if saving <= 0
        else max(1, math.ceil(operation_count / saving))
    )
    retained_scalars = 2 * rank**2 + (order + 2) * rank + order + 1
    source_scalars = (
        2 * (order + 1) * ambient
        + len(source.moments) * (order + 1)
    )
    return GradedReturnCompilation(GradedCyclicReturnModel(
        coefficient_order=order,
        partition_coefficients=functional.partition_coefficients,
        valuations=tuple(valuations),
        filtration_ranks=tuple(filtration_ranks),
        free_generator=reduced_free,
        interaction_generator=reduced_interaction,
        reduced_source=reduced_source,
        reduced_duals=reduced_duals,
        free_closure_residual=free_residual,
        graded_interaction_residual=graded_residual,
        functional_kind=functional.kind,
        functional_error=functional.error,
        functional_cells=functional.cells,
        materialized_endpoint_matrices=functional.materialized_endpoint_matrices,
        functional_metadata=functional.metadata,
        cost=GradedReturnCost(
            ambient_operator_dimension=ambient,
            reduced_dimension=rank,
            free_spectral_projections=spectral_projections,
            interaction_generator_actions=interaction_actions,
            orthogonalization_candidates=candidates,
            estimated_construction_operations=operation_count,
            full_query_operations=full_query,
            reduced_query_operations=reduced_query,
            break_even_queries=break_even,
            retained_complex_scalars=retained_scalars,
            source_packet_complex_scalars=source_scalars,
        ),
    ))
