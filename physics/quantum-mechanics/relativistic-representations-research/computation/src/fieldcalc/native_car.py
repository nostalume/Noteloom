"""Local-matrix/CAR-word graded reachability without ambient operator matrices."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math

import numpy as np

from .impurity import AndersonSystem, car_annihilator
from .rewrite import Refusal


WordLabel = tuple[int, int]
NativeKey = tuple[int, int, int, int]
NativeOperator = dict[NativeKey, complex]


@dataclass(frozen=True)
class CarWordProduct:
    terms: tuple[tuple[WordLabel, complex], ...]
    updates: int


@dataclass(frozen=True)
class NativeOrthogonalization:
    operator: NativeOperator | None
    original_norm: float
    residual_norm: float
    inner_product_work: int
    estimated_work: int


@dataclass(frozen=True)
class NativeDirection:
    valuation: int
    free_gap: float
    terms: tuple[tuple[NativeKey, complex], ...]


@dataclass(frozen=True)
class NativeReachabilityModel:
    filtration_ranks: tuple[int, ...]
    support_by_grade: tuple[int, ...]
    directions: tuple[NativeDirection, ...]
    free_generator: np.ndarray
    interaction_generator: np.ndarray
    reduced_source: np.ndarray
    retained_coefficients: int
    matrix_retained_coefficients: int
    estimated_construction_operations: int
    normal_order_updates: int
    inner_product_terms: int
    multiplication_terms: int
    orthogonalization_candidates: int
    native_closure_residual: float
    free_recovery_residual: float
    interaction_recovery_residual: float


@dataclass(frozen=True)
class NativeReachabilityCompilation:
    model: NativeReachabilityModel | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


class _BudgetExceeded(Exception):
    pass


def _token_key(token: tuple[bool, int]):
    creation, mode = token
    return (0, mode) if creation else (1, -mode)


def _merge_word_terms(*collections):
    merged: dict[WordLabel, complex] = {}
    for collection, scale in collections:
        for label, coefficient in collection:
            merged[label] = merged.get(label, 0j) + scale * coefficient
    return tuple(
        (label, complex(coefficient))
        for label, coefficient in sorted(merged.items())
        if abs(coefficient) > 1e-14
    )


@lru_cache(maxsize=None)
def _normal_order(tokens: tuple[tuple[bool, int], ...]):
    for index in range(len(tokens) - 1):
        left = tokens[index]
        right = tokens[index + 1]
        if left == right:
            return (), 1
        if _token_key(left) <= _token_key(right):
            continue
        swapped = tokens[:index] + (right, left) + tokens[index + 2:]
        exchange, exchange_updates = _normal_order(swapped)
        if not left[0] and right[0] and left[1] == right[1]:
            contracted = tokens[:index] + tokens[index + 2:]
            contraction, contraction_updates = _normal_order(contracted)
            return (
                _merge_word_terms(
                    (contraction, 1.0),
                    (exchange, -1.0),
                ),
                1 + exchange_updates + contraction_updates,
            )
        return (
            _merge_word_terms((exchange, -1.0)),
            1 + exchange_updates,
        )

    creation_mask = annihilation_mask = 0
    for creation, mode in tokens:
        if creation:
            creation_mask |= 1 << mode
        else:
            annihilation_mask |= 1 << mode
    return (((creation_mask, annihilation_mask), 1.0 + 0j),), 0


def _word_tokens(label: WordLabel, mode_count: int):
    creation_mask, annihilation_mask = label
    tokens = [
        (True, mode)
        for mode in range(mode_count)
        if creation_mask & (1 << mode)
    ]
    tokens.extend(
        (False, mode)
        for mode in reversed(range(mode_count))
        if annihilation_mask & (1 << mode)
    )
    return tuple(tokens)


def multiply_car_words(
    left: WordLabel,
    right: WordLabel,
    mode_count: int,
    update_budget: int,
) -> CarWordProduct:
    """Generate the normal polynomial for a product of two canonical CAR words."""
    limit = 1 << mode_count
    if any(mask < 0 or mask >= limit for label in (left, right) for mask in label):
        raise ValueError("CAR word mask lies outside the admitted mode count")
    terms, updates = _normal_order(
        _word_tokens(left, mode_count) + _word_tokens(right, mode_count),
    )
    if updates > update_budget:
        raise ValueError("CAR normal-order budget exceeded")
    return CarWordProduct(terms, updates)


@lru_cache(maxsize=None)
def _word_adjoint(label: WordLabel, mode_count: int):
    tokens = tuple(
        (not creation, mode)
        for creation, mode in reversed(_word_tokens(label, mode_count))
    )
    return _normal_order(tokens)[0]


@lru_cache(maxsize=None)
def _word_inner(left: WordLabel, right: WordLabel, mode_count: int):
    value = 0j
    work = 0
    for adjoint_label, adjoint_coefficient in _word_adjoint(left, mode_count):
        product = multiply_car_words(
            adjoint_label,
            right,
            mode_count,
            update_budget=1_000_000,
        )
        work += len(product.terms) + product.updates
        for label, coefficient in product.terms:
            creation, annihilation = label
            if creation == annihilation:
                value += (
                    adjoint_coefficient
                    * coefficient
                    * 2 ** (mode_count - creation.bit_count())
                )
    return complex(value), work


def clean_native(operator: NativeOperator, tolerance: float = 1e-13):
    scale = max((abs(value) for value in operator.values()), default=0.0)
    threshold = tolerance * max(1.0, scale)
    return {
        key: complex(value)
        for key, value in operator.items()
        if abs(value) > threshold
    }


def add_scaled_native(target: NativeOperator, source: NativeOperator, scale: complex):
    for key, value in source.items():
        target[key] = target.get(key, 0j) + scale * value


def multiply_native(left, right, mode_count: int):
    result: NativeOperator = {}
    updates = attempts = 0
    for (left_row, left_column, left_creation, left_annihilation), left_value in left.items():
        for (
            right_row,
            right_column,
            right_creation,
            right_annihilation,
        ), right_value in right.items():
            attempts += 1
            if left_column != right_row:
                continue
            word_product = multiply_car_words(
                (left_creation, left_annihilation),
                (right_creation, right_annihilation),
                mode_count,
                update_budget=1_000_000,
            )
            updates += word_product.updates
            for (creation, annihilation), coefficient in word_product.terms:
                key = (left_row, right_column, creation, annihilation)
                result[key] = result.get(key, 0j) + (
                    left_value * right_value * coefficient
                )
    return clean_native(result), updates, attempts


def native_inner_product(left, right, mode_count: int):
    value = 0j
    work = 0
    right_by_local: dict[tuple[int, int], list[tuple[WordLabel, complex]]] = {}
    for (row, column, creation, annihilation), coefficient in right.items():
        right_by_local.setdefault((row, column), []).append(
            ((creation, annihilation), coefficient),
        )
    for (row, column, creation, annihilation), coefficient in left.items():
        for right_label, right_coefficient in right_by_local.get((row, column), ()):
            word_value, word_work = _word_inner(
                (creation, annihilation), right_label, mode_count,
            )
            value += complex(coefficient).conjugate() * right_coefficient * word_value
            work += word_work
    return complex(value), work


def orthogonalize_native(
    candidate: NativeOperator,
    basis: tuple[NativeOperator, ...],
    mode_count: int,
    tolerance: float,
) -> NativeOrthogonalization:
    """Reorthogonalize one native operator in the generated trace metric."""
    residual = dict(candidate)
    original_squared, cost = native_inner_product(
        residual, residual, mode_count,
    )
    inner_work = cost
    estimated_work = cost + len(residual)
    original_norm = math.sqrt(max(0.0, original_squared.real))
    if original_norm == 0:
        return NativeOrthogonalization(None, 0.0, 0.0, inner_work, estimated_work)
    for _ in range(2):
        for existing in basis:
            overlap, cost = native_inner_product(existing, residual, mode_count)
            inner_work += cost
            estimated_work += cost + len(existing) + len(residual)
            add_scaled_native(residual, existing, -overlap)
            residual = clean_native(residual)
    squared, cost = native_inner_product(residual, residual, mode_count)
    inner_work += cost
    estimated_work += cost + len(residual)
    norm = math.sqrt(max(0.0, squared.real))
    if norm <= tolerance * max(1.0, original_norm):
        return NativeOrthogonalization(
            None, original_norm, norm, inner_work, estimated_work,
        )
    return NativeOrthogonalization(
        {key: value / norm for key, value in residual.items()},
        original_norm,
        norm,
        inner_work,
        estimated_work,
    )


def trace_native(operator: NativeOperator, mode_count: int) -> complex:
    """Evaluate the unnormalized finite-Fock trace from native labels."""
    value = 0j
    for (row, column, creation, annihilation), coefficient in operator.items():
        if row == column and creation == annihilation:
            value += coefficient * 2 ** (mode_count - creation.bit_count())
    return complex(value)


def anderson_local_data(system: AndersonSystem):
    annihilators = tuple(car_annihilator(mode, 2) for mode in range(2))
    numbers = tuple(action.conj().T @ action for action in annihilators)
    hamiltonian = (
        system.request.impurity_energy * (numbers[0] + numbers[1])
        + system.request.interaction * numbers[0] @ numbers[1]
    )
    parity = np.diag([(-1) ** state.bit_count() for state in range(4)])
    return annihilators, np.diag(hamiltonian).real, parity


def native_local_operator(operator: np.ndarray, word: WordLabel):
    return {
        (row, column, word[0], word[1]): complex(operator[row, column])
        for row in range(operator.shape[0])
        for column in range(operator.shape[1])
        if abs(operator[row, column]) > 1e-14
    }


def anderson_native_interaction(system: AndersonSystem):
    annihilators, _, parity = anderson_local_data(system)
    result: NativeOperator = {}
    for bath, coupling in enumerate(system.request.hybridizations):
        for spin in range(2):
            mode = 2 * bath + spin
            creation_local = parity @ annihilators[spin]
            annihilation_local = annihilators[spin].conj().T @ parity
            add_scaled_native(
                result,
                native_local_operator(creation_local, (1 << mode, 0)),
                coupling,
            )
            add_scaled_native(
                result,
                native_local_operator(annihilation_local, (0, 1 << mode)),
                complex(coupling).conjugate(),
            )
    return clean_native(result)


def _gap(key: NativeKey, local_energies, bath_energies):
    row, column, creation, annihilation = key
    value = local_energies[column] - local_energies[row]
    value += sum(
        energy
        for mode, energy in enumerate(bath_energies)
        if annihilation & (1 << mode)
    )
    value -= sum(
        energy
        for mode, energy in enumerate(bath_energies)
        if creation & (1 << mode)
    )
    return float(value)


def _spectral_parts(operator, local_energies, bath_energies, tolerance):
    groups: list[tuple[float, NativeOperator]] = []
    for key, coefficient in operator.items():
        value = _gap(key, local_energies, bath_energies)
        target = next(
            (group for group in groups if abs(group[0] - value) <= tolerance),
            None,
        )
        if target is None:
            target = (value, {})
            groups.append(target)
        target[1][key] = coefficient
    return tuple((gap, clean_native(part)) for gap, part in groups)


@lru_cache(maxsize=None)
def _word_matrix(label: WordLabel, mode_count: int):
    annihilators = tuple(
        car_annihilator(mode, mode_count) for mode in range(mode_count)
    )
    value = np.eye(1 << mode_count, dtype=complex)
    for creation, mode in _word_tokens(label, mode_count):
        value @= annihilators[mode].conj().T if creation else annihilators[mode]
    return value


def native_to_matrix(operator: NativeOperator, mode_count: int):
    dimension = 4 * (1 << mode_count)
    result = np.zeros((dimension, dimension), dtype=complex)
    for (row, column, creation, annihilation), coefficient in operator.items():
        local = np.zeros((4, 4), dtype=complex)
        local[row, column] = 1.0
        result += coefficient * np.kron(
            _word_matrix((creation, annihilation), mode_count),
            local,
        )
    return result


def _refuse(system: AndersonSystem, reason: str):
    return NativeReachabilityCompilation(refusal=Refusal(
        reason,
        provenance=system.request.provenance,
    ))


def compile_native_graded_reachability(
    system: AndersonSystem,
    coefficient_order: int,
    tolerance: float,
    resource_budget: int,
):
    """Generate the graded cyclic module in a native CAR-word representation."""
    if coefficient_order < 0 or coefficient_order > system.request.coefficient_order:
        return _refuse(system, "native CAR coefficient order lies outside the model")
    if tolerance <= 0 or not math.isfinite(tolerance):
        return _refuse(system, "native CAR tolerance must be finite and positive")

    mode_count = 2 * len(system.request.bath_energies)
    bath_energies = tuple(
        energy for energy in system.request.bath_energies for _ in range(2)
    )
    local_annihilators, local_energies, _ = anderson_local_data(system)
    source = native_local_operator(local_annihilators[0], (0, 0))
    interaction = anderson_native_interaction(system)

    basis: list[NativeOperator] = []
    gaps: list[float] = []
    valuations: list[int] = []
    interaction_images: dict[int, NativeOperator] = {}
    normal_updates = inner_work = multiplication_terms = candidates = work = 0

    def spend(amount: int):
        nonlocal work
        work += amount
        if work > resource_budget:
            raise _BudgetExceeded

    def admit(candidate, grade, gap):
        nonlocal inner_work, candidates
        candidates += 1
        existing = tuple(
            operator
            for operator, existing_gap in zip(basis, gaps, strict=True)
            if abs(existing_gap - gap) <= tolerance
        )
        result = orthogonalize_native(
            candidate, existing, mode_count, tolerance,
        )
        inner_work += result.inner_product_work
        spend(result.estimated_work)
        if result.operator is None:
            return None
        basis.append(result.operator)
        gaps.append(gap)
        valuations.append(grade)
        return len(basis) - 1

    def spectral_close(operator, grade):
        for gap, part in _spectral_parts(
            operator, local_energies, bath_energies, tolerance,
        ):
            spend(len(part))
            admit(part, grade, gap)

    try:
        spend(len(source) + len(interaction))
        spectral_close(source, 0)
        filtration = [len(basis)]
        for grade in range(1, coefficient_order + 1):
            previous = tuple(
                (index, operator)
                for index, (operator, valuation) in enumerate(
                    zip(basis, valuations, strict=True),
                )
                if valuation == grade - 1
            )
            for index, operator in previous:
                forward, forward_updates, forward_attempts = multiply_native(
                    operator, interaction, mode_count,
                )
                reverse, reverse_updates, reverse_attempts = multiply_native(
                    interaction, operator, mode_count,
                )
                normal_updates += forward_updates + reverse_updates
                multiplication_terms += forward_attempts + reverse_attempts
                spend(
                    forward_updates + reverse_updates
                    + forward_attempts + reverse_attempts
                )
                commutator = dict(forward)
                add_scaled_native(commutator, reverse, -1.0)
                commutator = clean_native(commutator)
                interaction_images[index] = commutator
                spectral_close(commutator, grade)
            filtration.append(len(basis))

        rank = len(basis)
        reduced_source = np.zeros(rank, dtype=complex)
        reduced_interaction = np.zeros((rank, rank), dtype=complex)
        native_closure_residual = 0.0
        for row, direction in enumerate(basis):
            value, cost = native_inner_product(direction, source, mode_count)
            reduced_source[row] = value
            inner_work += cost
            spend(cost + len(direction) + len(source))
        source_reconstruction: NativeOperator = {}
        for coefficient, direction in zip(
            reduced_source, basis, strict=True,
        ):
            add_scaled_native(source_reconstruction, direction, coefficient)
        source_difference = dict(source)
        add_scaled_native(source_difference, source_reconstruction, -1.0)
        value, cost = native_inner_product(
            clean_native(source_difference), clean_native(source_difference), mode_count,
        )
        inner_work += cost
        spend(cost + len(source_difference))
        native_closure_residual = math.sqrt(max(0.0, value.real))

        for column, grade in enumerate(valuations):
            if grade >= coefficient_order:
                continue
            image = interaction_images[column]
            reconstruction: NativeOperator = {}
            for row, direction in enumerate(basis):
                coefficient, cost = native_inner_product(
                    direction, image, mode_count,
                )
                reduced_interaction[row, column] = coefficient
                inner_work += cost
                spend(cost + len(direction) + len(image))
                add_scaled_native(reconstruction, direction, coefficient)
            difference = dict(image)
            add_scaled_native(difference, reconstruction, -1.0)
            difference = clean_native(difference)
            value, cost = native_inner_product(
                difference, difference, mode_count,
            )
            inner_work += cost
            spend(cost + len(difference))
            native_closure_residual = max(
                native_closure_residual,
                math.sqrt(max(0.0, value.real)),
            )
    except _BudgetExceeded:
        return _refuse(system, "native CAR reachability budget exceeded")

    free_residual = interaction_residual = 0.0
    for index, (operator, gap, grade) in enumerate(
        zip(basis, gaps, valuations, strict=True),
    ):
        matrix = native_to_matrix(operator, mode_count)
        free_residual = max(
            free_residual,
            float(np.linalg.norm(
                matrix @ system.free_hamiltonian
                - system.free_hamiltonian @ matrix
                - gap * matrix
            )),
        )
        if grade < coefficient_order:
            generated = native_to_matrix(interaction_images[index], mode_count)
            interaction_residual = max(
                interaction_residual,
                float(np.linalg.norm(
                    generated
                    - matrix @ system.hybridization_action
                    + system.hybridization_action @ matrix
                )),
            )

    support_by_grade = tuple(
        sum(
            len(operator)
            for operator, valuation in zip(basis, valuations, strict=True)
            if valuation == grade
        )
        for grade in range(coefficient_order + 1)
    )
    retained = sum(support_by_grade)
    return NativeReachabilityCompilation(model=NativeReachabilityModel(
        filtration_ranks=tuple(filtration),
        support_by_grade=support_by_grade,
        directions=tuple(
            NativeDirection(
                valuation=valuation,
                free_gap=gap,
                terms=tuple(sorted(operator.items())),
            )
            for operator, valuation, gap in zip(
                basis, valuations, gaps, strict=True,
            )
        ),
        free_generator=np.diag(gaps),
        interaction_generator=reduced_interaction,
        reduced_source=reduced_source,
        retained_coefficients=retained,
        matrix_retained_coefficients=len(basis) * system.free_hamiltonian.size,
        estimated_construction_operations=work,
        normal_order_updates=normal_updates,
        inner_product_terms=inner_work,
        multiplication_terms=multiplication_terms,
        orthogonalization_candidates=candidates,
        native_closure_residual=native_closure_residual,
        free_recovery_residual=free_residual,
        interaction_recovery_residual=interaction_residual,
    ))
