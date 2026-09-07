"""Charge-adapted normal-ordered CAR words for retained bath insertions."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np

from .graded_return import FunctionalPortRefusal, FunctionalRestrictionPacket
from .impurity import car_annihilator
from .perturbative_return import PerturbativeReturnModel


@dataclass(frozen=True)
class CarWordDecomposition:
    charge: int
    labels: tuple[tuple[int, int], ...]
    coefficients: tuple[complex, ...]
    reconstructed: np.ndarray
    residual: float


@dataclass(frozen=True)
class GaussianCarReceipt:
    schmidt_factor_count: int
    total_word_occurrences: int
    distinct_word_count: int
    dense_word_bound: int
    maximum_word_degree: int
    occurrences_by_valuation: tuple[int, ...]
    counts_by_tolerance: tuple[int, ...]
    maximum_recovery_residual: float
    count_stable: bool


@dataclass(frozen=True)
class CarFactorTerm:
    local_operator: np.ndarray
    bath_words: CarWordDecomposition


@dataclass(frozen=True)
class CarInsertionDecomposition:
    terms: tuple[CarFactorTerm, ...]
    reconstructed: np.ndarray
    residual: float


@lru_cache(maxsize=None)
def _word_sector(mode_count: int, charge: int):
    annihilators = tuple(
        car_annihilator(mode, mode_count)
        for mode in range(mode_count)
    )
    dimension = 1 << mode_count
    labels = []
    words = []
    for creation_mask in range(1 << mode_count):
        for annihilation_mask in range(1 << mode_count):
            if creation_mask.bit_count() - annihilation_mask.bit_count() != charge:
                continue
            word = np.eye(dimension, dtype=complex)
            for mode in range(mode_count):
                if creation_mask & (1 << mode):
                    word = word @ annihilators[mode].conj().T
            for mode in reversed(range(mode_count)):
                if annihilation_mask & (1 << mode):
                    word = word @ annihilators[mode]
            labels.append((creation_mask, annihilation_mask))
            words.append(word)
    design = np.column_stack([word.reshape(-1) for word in words])
    return tuple(labels), tuple(words), design


def decompose_charge_homogeneous(
    operator: np.ndarray,
    mode_count: int,
    tolerance: float,
) -> CarWordDecomposition:
    dimension = 1 << mode_count
    value = np.asarray(operator, dtype=complex)
    if value.shape != (dimension, dimension):
        raise FunctionalPortRefusal("bath factor dimension does not match mode count")
    number = sum(
        car_annihilator(mode, mode_count).conj().T
        @ car_annihilator(mode, mode_count)
        for mode in range(mode_count)
    )
    commutator = number @ value - value @ number
    scale = max(1.0, float(np.linalg.norm(value)))
    candidates = tuple(
        (charge, float(np.linalg.norm(commutator - charge * value)))
        for charge in range(-mode_count, mode_count + 1)
    )
    charge, charge_residual = min(candidates, key=lambda item: item[1])
    if charge_residual > tolerance * scale:
        raise FunctionalPortRefusal("bath factor has mixed charge")

    labels, words, design = _word_sector(mode_count, charge)
    coefficients, _, _, _ = np.linalg.lstsq(design, value.reshape(-1), rcond=None)
    coefficient_scale = max(1.0, float(np.max(abs(coefficients))))
    retained = tuple(
        index
        for index, coefficient in enumerate(coefficients)
        if abs(coefficient) > tolerance * coefficient_scale
    )
    reconstructed = sum(
        (coefficients[index] * words[index] for index in retained),
        start=np.zeros_like(value),
    )
    residual = float(np.linalg.norm(value - reconstructed))
    if residual > 20 * tolerance * scale:
        raise FunctionalPortRefusal("Gaussian CAR reconstruction failed")
    return CarWordDecomposition(
        charge=charge,
        labels=tuple(labels[index] for index in retained),
        coefficients=tuple(complex(coefficients[index]) for index in retained),
        reconstructed=reconstructed,
        residual=residual,
    )


def factor_car_insertion(
    insertion: np.ndarray,
    local_dimension: int,
    tolerance: float,
) -> CarInsertionDecomposition:
    dimension = insertion.shape[0]
    bath_dimension = dimension // local_dimension
    bath_modes = bath_dimension.bit_length() - 1
    coefficient_map = insertion.reshape(
        bath_dimension,
        local_dimension,
        bath_dimension,
        local_dimension,
    ).transpose(1, 3, 0, 2).reshape(local_dimension**2, bath_dimension**2)
    local_numbers = tuple(state.bit_count() for state in range(local_dimension))
    terms = []
    for local_charge in range(-bath_modes, bath_modes + 1):
        rows = tuple(
            left * local_dimension + right
            for left in range(local_dimension)
            for right in range(local_dimension)
            if local_numbers[left] - local_numbers[right] == local_charge
        )
        if not rows:
            continue
        block = coefficient_map[np.asarray(rows)]
        left, singular_values, right = np.linalg.svd(block, full_matrices=False)
        scale = max(1.0, float(singular_values[0]))
        rank = int(np.count_nonzero(singular_values > tolerance * scale))
        for index in range(rank):
            local = np.zeros(local_dimension**2, dtype=complex)
            local[np.asarray(rows)] = left[:, index] * singular_values[index]
            bath = right[index].reshape(bath_dimension, bath_dimension)
            words = decompose_charge_homogeneous(
                bath,
                mode_count=bath_modes,
                tolerance=tolerance,
            )
            terms.append(CarFactorTerm(
                local_operator=local.reshape(local_dimension, local_dimension),
                bath_words=words,
            ))

    reconstructed = np.zeros_like(insertion)
    for term in terms:
        tensor = np.einsum(
            "ij,kl->kilj",
            term.local_operator,
            term.bath_words.reconstructed,
        )
        reconstructed += tensor.reshape(dimension, dimension)
    residual = float(np.linalg.norm(insertion - reconstructed))
    return CarInsertionDecomposition(tuple(terms), reconstructed, residual)


def car_audited_endpoint_functional(
    source: PerturbativeReturnModel,
    valuations: tuple[int, ...],
    local_dimension: int,
    word_budget: int,
):
    """Audit Gaussian word consumability, then evaluate recomposed insertions."""
    def evaluate(operators: tuple[np.ndarray, ...]) -> FunctionalRestrictionPacket:
        dimension = source.system.free_hamiltonian.shape[0]
        if dimension % local_dimension:
            raise FunctionalPortRefusal(
                "local dimension does not divide the Hilbert dimension",
            )
        if len(valuations) != len(operators):
            raise FunctionalPortRefusal("valuation count does not match graded basis")
        creation = source.system.impurity_annihilator.conj().T
        insertions = tuple(
            operator @ creation + creation @ operator
            for operator in operators
        )

        tolerance_counts = []
        retained_terms = ()
        reconstructed = ()
        maximum_residual = 0.0
        for tolerance in (1e-8, 1e-10, 1e-12):
            results = tuple(
                factor_car_insertion(insertion, local_dimension, tolerance)
                for insertion in insertions
            )
            count = sum(
                len(term.bath_words.labels)
                for result in results
                for term in result.terms
            )
            tolerance_counts.append(count)
            if tolerance == 1e-10:
                retained_terms = tuple(result.terms for result in results)
                reconstructed = tuple(result.reconstructed for result in results)
                maximum_residual = max(
                    result.residual for result in results
                )

        occurrences = tuple(
            sum(len(term.bath_words.labels) for term in terms)
            for terms in retained_terms
        )
        total_occurrences = sum(occurrences)
        if total_occurrences > word_budget:
            raise FunctionalPortRefusal("Gaussian CAR word budget exceeded")
        labels = {
            label
            for terms in retained_terms
            for term in terms
            for label in term.bath_words.labels
        }
        maximum_degree = max(
            creation.bit_count() + annihilation.bit_count()
            for creation, annihilation in labels
        )
        by_valuation = tuple(
            sum(
                occurrence
                for occurrence, valuation in zip(occurrences, valuations, strict=True)
                if valuation == grade
            )
            for grade in range(source.coefficient_order + 1)
        )
        restrictions = tuple(
            tuple(
                complex(np.trace(thermal @ insertion))
                for insertion in reconstructed
            )
            for thermal in source.thermal_coefficients
        )
        receipt = GaussianCarReceipt(
            schmidt_factor_count=sum(len(terms) for terms in retained_terms),
            total_word_occurrences=total_occurrences,
            distinct_word_count=len(labels),
            dense_word_bound=sum(len(terms) for terms in retained_terms) * 256,
            maximum_word_degree=maximum_degree,
            occurrences_by_valuation=by_valuation,
            counts_by_tolerance=tuple(tolerance_counts),
            maximum_recovery_residual=maximum_residual,
            count_stable=len(set(tolerance_counts)) == 1,
        )
        return FunctionalRestrictionPacket(
            partition_coefficients=source.partition_coefficients,
            restrictions=restrictions,
            kind="Gaussian-CAR-audited endpoint",
            error=maximum_residual,
            cells=0,
            materialized_endpoint_matrices=2 * len(source.thermal_coefficients),
            metadata=receipt,
        )

    return evaluate
