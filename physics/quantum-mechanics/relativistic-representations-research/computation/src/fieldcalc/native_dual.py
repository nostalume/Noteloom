"""Native right-action closure required by an Anderson thermal functional."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .impurity import AndersonSystem
from .native_car import (
    NativeDirection,
    NativeOperator,
    NativeReachabilityModel,
    add_scaled_native,
    anderson_local_data,
    anderson_native_interaction,
    clean_native,
    multiply_native,
    native_inner_product,
    native_local_operator,
    orthogonalize_native,
    trace_native,
)
from .rewrite import Refusal


@dataclass(frozen=True)
class NativeDualDirection:
    thermal_grade: int
    terms: tuple[tuple[tuple[int, int, int, int], complex], ...]


@dataclass(frozen=True)
class NativeThermalDualModel:
    ranks_by_grade: tuple[int, ...]
    support_by_grade: tuple[int, ...]
    directions: tuple[NativeDualDirection, ...]
    free_action: np.ndarray
    interaction_action: np.ndarray
    seed_coordinates: np.ndarray
    trace_covector: np.ndarray
    total_rank: int
    retained_coefficients: int
    ambient_operator_dimension: int
    multiplication_terms: int
    normal_order_updates: int
    inner_product_work: int
    estimated_construction_operations: int
    closure_residual: float
    commutator_module_escape: float


@dataclass(frozen=True)
class NativeThermalDualBoundary:
    active_grade: int
    ranks_by_grade: tuple[int, ...]
    support_by_grade: tuple[int, ...]
    retained_coefficients: int
    resource_used: int
    commutator_module_escape: float


@dataclass(frozen=True)
class NativeThermalDualCompilation:
    model: NativeThermalDualModel | None = None
    refusal: Refusal | None = None
    boundary: NativeThermalDualBoundary | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


class _BudgetExceeded(Exception):
    pass


class _SupportExceeded(Exception):
    pass


def _direction_operator(direction: NativeDirection) -> NativeOperator:
    return dict(direction.terms)


def anderson_native_free_hamiltonian(system: AndersonSystem):
    _, local_energies, _ = anderson_local_data(system)
    result = native_local_operator(np.diag(local_energies), (0, 0))
    local_identity = np.eye(4, dtype=complex)
    mode = 0
    for energy in system.request.bath_energies:
        for _ in range(2):
            add_scaled_native(
                result,
                native_local_operator(
                    local_identity,
                    (1 << mode, 1 << mode),
                ),
                energy,
            )
            mode += 1
    return clean_native(result)


def native_functional_seeds(
    native: NativeReachabilityModel,
    system: AndersonSystem,
):
    local_annihilators, _, _ = anderson_local_data(system)
    creation = native_local_operator(
        local_annihilators[0].conj().T,
        (0, 0),
    )
    identity = native_local_operator(np.eye(4, dtype=complex), (0, 0))
    insertions = []
    updates = attempts = 0
    mode_count = 2 * len(system.request.bath_energies)
    for direction in native.directions:
        operator = _direction_operator(direction)
        forward, forward_updates, forward_attempts = multiply_native(
            operator, creation, mode_count,
        )
        reverse, reverse_updates, reverse_attempts = multiply_native(
            creation, operator, mode_count,
        )
        add_scaled_native(forward, reverse, 1.0)
        insertions.append(clean_native(forward))
        updates += forward_updates + reverse_updates
        attempts += forward_attempts + reverse_attempts
    return (identity, *insertions), updates, attempts


def native_projection_residual(operator, basis, mode_count):
    residual = dict(operator)
    work = 0
    for direction in basis:
        coefficient, cost = native_inner_product(direction, residual, mode_count)
        work += cost + len(direction) + len(residual)
        add_scaled_native(residual, direction, -coefficient)
        residual = clean_native(residual)
    squared, cost = native_inner_product(residual, residual, mode_count)
    work += cost + len(residual)
    return math.sqrt(max(0.0, squared.real)), work


def _refuse(system: AndersonSystem, reason: str, boundary=None):
    return NativeThermalDualCompilation(refusal=Refusal(
        reason,
        provenance=system.request.provenance,
    ), boundary=boundary)


def compile_native_thermal_dual(
    system: AndersonSystem,
    native: NativeReachabilityModel,
    thermal_order: int,
    tolerance: float,
    coefficient_budget: int,
    resource_budget: int,
):
    """Generate the minimal native right-action module for Gibbs coefficients."""
    if thermal_order < 0 or thermal_order > system.request.coefficient_order:
        return _refuse(system, "native thermal order lies outside the model")
    if tolerance <= 0 or not math.isfinite(tolerance):
        return _refuse(system, "native thermal tolerance must be finite and positive")

    mode_count = 2 * len(system.request.bath_energies)
    free = anderson_native_free_hamiltonian(system)
    interaction = anderson_native_interaction(system)
    seeds, normal_updates, multiplication_terms = native_functional_seeds(
        native, system,
    )
    basis_by_grade: list[list[NativeOperator]] = [
        [] for _ in range(thermal_order + 1)
    ]
    work = inner_work = 0
    active_grade = 0

    commutator_basis = tuple(
        _direction_operator(direction) for direction in native.directions
    )
    escape = 0.0
    for direction in commutator_basis:
        image, _, _ = multiply_native(direction, interaction, mode_count)
        residual, _ = native_projection_residual(
            image, commutator_basis, mode_count,
        )
        escape = max(escape, residual)

    def boundary():
        support = tuple(
            sum(len(direction) for direction in basis)
            for basis in basis_by_grade
        )
        return NativeThermalDualBoundary(
            active_grade=active_grade,
            ranks_by_grade=tuple(len(basis) for basis in basis_by_grade),
            support_by_grade=support,
            retained_coefficients=sum(support),
            resource_used=work,
            commutator_module_escape=escape,
        )

    def spend(amount: int):
        nonlocal work
        work += amount
        if work > resource_budget:
            raise _BudgetExceeded

    def admit(candidate, grade):
        nonlocal inner_work
        result = orthogonalize_native(
            candidate,
            tuple(basis_by_grade[grade]),
            mode_count,
            tolerance,
        )
        inner_work += result.inner_product_work
        spend(result.estimated_work)
        if result.operator is None:
            return None
        basis_by_grade[grade].append(result.operator)
        retained = sum(
            len(direction)
            for basis in basis_by_grade
            for direction in basis
        )
        if retained > coefficient_budget:
            raise _SupportExceeded
        return result.operator

    def close_under_free(candidates, grade):
        nonlocal normal_updates, multiplication_terms
        queue = []
        for candidate in candidates:
            admitted = admit(candidate, grade)
            if admitted is not None:
                queue.append(admitted)
        cursor = 0
        while cursor < len(queue):
            image, updates, attempts = multiply_native(
                queue[cursor], free, mode_count,
            )
            cursor += 1
            normal_updates += updates
            multiplication_terms += attempts
            spend(updates + attempts)
            admitted = admit(image, grade)
            if admitted is not None:
                queue.append(admitted)

    try:
        spend(normal_updates + multiplication_terms + len(free) + len(interaction))
        close_under_free(seeds, 0)
        for grade in range(1, thermal_order + 1):
            active_grade = grade
            generated = []
            for direction in basis_by_grade[grade - 1]:
                image, updates, attempts = multiply_native(
                    direction, interaction, mode_count,
                )
                normal_updates += updates
                multiplication_terms += attempts
                spend(updates + attempts)
                generated.append(image)
            close_under_free(generated, grade)
    except _SupportExceeded:
        return _refuse(
            system, "native thermal-dual support exceeded", boundary(),
        )
    except _BudgetExceeded:
        return _refuse(
            system, "native thermal-dual resource budget exceeded", boundary(),
        )

    offsets = []
    total_rank = 0
    for basis in basis_by_grade:
        offsets.append(total_rank)
        total_rank += len(basis)
    free_action = np.zeros((total_rank, total_rank), dtype=complex)
    interaction_action = np.zeros_like(free_action)
    closure_residual = 0.0

    for grade, basis in enumerate(basis_by_grade):
        offset = offsets[grade]
        for column, direction in enumerate(basis):
            image, updates, attempts = multiply_native(direction, free, mode_count)
            normal_updates += updates
            multiplication_terms += attempts
            reconstruction: NativeOperator = {}
            for row, target in enumerate(basis):
                coefficient, cost = native_inner_product(target, image, mode_count)
                inner_work += cost
                work += cost + len(target) + len(image)
                free_action[offset + row, offset + column] = coefficient
                add_scaled_native(reconstruction, target, coefficient)
            residual = dict(image)
            add_scaled_native(residual, reconstruction, -1.0)
            residual_norm, cost = native_projection_residual(
                residual, (), mode_count,
            )
            work += cost
            closure_residual = max(closure_residual, residual_norm)

            if grade == thermal_order:
                continue
            next_basis = basis_by_grade[grade + 1]
            next_offset = offsets[grade + 1]
            image, updates, attempts = multiply_native(
                direction, interaction, mode_count,
            )
            normal_updates += updates
            multiplication_terms += attempts
            reconstruction = {}
            for row, target in enumerate(next_basis):
                coefficient, cost = native_inner_product(target, image, mode_count)
                inner_work += cost
                work += cost + len(target) + len(image)
                interaction_action[next_offset + row, offset + column] = coefficient
                add_scaled_native(reconstruction, target, coefficient)
            residual = dict(image)
            add_scaled_native(residual, reconstruction, -1.0)
            residual_norm, cost = native_projection_residual(
                residual, (), mode_count,
            )
            work += cost
            closure_residual = max(closure_residual, residual_norm)

    grade_zero = tuple(basis_by_grade[0])
    seed_coordinates = np.zeros((total_rank, len(seeds)), dtype=complex)
    for column, seed in enumerate(seeds):
        for row, direction in enumerate(grade_zero):
            coefficient, cost = native_inner_product(
                direction, seed, mode_count,
            )
            seed_coordinates[row, column] = coefficient
            inner_work += cost
            work += cost + len(direction) + len(seed)
        residual, cost = native_projection_residual(seed, grade_zero, mode_count)
        work += cost
        closure_residual = max(closure_residual, residual)

    flattened = tuple(
        direction
        for basis in basis_by_grade
        for direction in basis
    )
    trace_covector = np.asarray([
        trace_native(direction, mode_count) for direction in flattened
    ], dtype=complex)
    support_by_grade = tuple(
        sum(len(direction) for direction in basis)
        for basis in basis_by_grade
    )
    retained = sum(support_by_grade)
    if closure_residual > 20 * tolerance:
        return _refuse(system, "native thermal-dual closure residual exceeded")
    if work > resource_budget:
        return _refuse(system, "native thermal-dual resource budget exceeded")

    return NativeThermalDualCompilation(model=NativeThermalDualModel(
        ranks_by_grade=tuple(len(basis) for basis in basis_by_grade),
        support_by_grade=support_by_grade,
        directions=tuple(
            NativeDualDirection(grade, tuple(sorted(direction.items())))
            for grade, basis in enumerate(basis_by_grade)
            for direction in basis
        ),
        free_action=free_action,
        interaction_action=interaction_action,
        seed_coordinates=seed_coordinates,
        trace_covector=trace_covector,
        total_rank=total_rank,
        retained_coefficients=retained,
        ambient_operator_dimension=system.free_hamiltonian.size,
        multiplication_terms=multiplication_terms,
        normal_order_updates=normal_updates,
        inner_product_work=inner_work,
        estimated_construction_operations=work,
        closure_residual=closure_residual,
        commutator_module_escape=escape,
    ))
