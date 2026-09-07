"""Exact prepared-observable Krylov reduction over Gaussian rationals."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

import numpy as np
from scipy.linalg import expm

import exact_gaussian_matrix as gaussian
from exact_gaussian_linear import Vector, coordinates, linear_combination, matrix_vector

NUMERICAL_TOLERANCE = 1e-11


class ActiveSubspaceError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class ActiveSubspaceBudget:
    maximum_carrier_dimension: int
    maximum_active_dimension: int


@dataclass(frozen=True)
class ActiveSubspaceCost:
    hamiltonian_actions: int
    exact_coordinate_solves: int
    gram_pairings: int
    effect_actions: int
    effect_pairings: int
    full_reference_exponential_evaluated: bool
    full_exponential_cubic_proxy: int
    active_exponential_cubic_proxy: int


@dataclass(frozen=True)
class ActiveSubspaceWitness:
    status: str
    ambient_dimension: int
    active_dimension: int
    basis: tuple[Vector, ...]
    closure_coordinates: Vector
    reduced_hamiltonian: gaussian.ComplexMatrix
    gram: gaussian.ComplexMatrix
    compressed_effect: gaussian.ComplexMatrix
    initial_coordinates: Vector
    active_expectation: float
    reference_expectation: float | None
    observable_error: float | None
    numerical_tolerance: float
    no_dimension_gain: bool
    reference_source: str
    domain_contract: str
    cost: ActiveSubspaceCost
    checks: dict[str, bool]


@dataclass(frozen=True)
class CoefficientFamilyCost:
    coefficient_actions: int
    exact_coordinate_solves: int
    gram_pairings: int
    effect_actions: int
    effect_pairings: int


@dataclass(frozen=True)
class CoefficientFamilyActiveSubspaceWitness:
    status: str
    ambient_dimension: int
    active_dimension: int
    coefficient_count: int
    basis: tuple[Vector, ...]
    reduced_coefficients: tuple[gaussian.ComplexMatrix, ...]
    gram: gaussian.ComplexMatrix
    compressed_effect: gaussian.ComplexMatrix
    initial_coordinates: Vector
    numerical_tolerance: float
    no_dimension_gain: bool
    domain_contract: str
    cost: CoefficientFamilyCost
    checks: dict[str, bool]


def evaluate_active_expectation(witness: ActiveSubspaceWitness, time: object) -> float:
    """Reuse one exact active carrier for a new admitted propagation time."""
    try:
        admitted_time = gaussian.rational(time)
    except ValueError as error:
        raise ActiveSubspaceError("InexactTimeDatum", str(error)) from error
    if admitted_time < 0:
        raise ActiveSubspaceError("NegativePropagationTime", "time must be nonnegative")
    value, imaginary_residual = _expectation(
        witness.reduced_hamiltonian,
        witness.initial_coordinates,
        witness.compressed_effect,
        admitted_time,
        witness.gram[0][0].real,
    )
    if imaginary_residual > witness.numerical_tolerance:
        raise ActiveSubspaceError(
            "ActiveExpectationResidual", "compressed-effect expectation is not numerically real"
        )
    return value


def specialize_active_hamiltonian(
    witness: CoefficientFamilyActiveSubspaceWitness, weights: tuple[object, ...]
) -> gaussian.ComplexMatrix:
    """Specialize a common active carrier at exact real coefficient weights."""
    if not isinstance(weights, tuple) or len(weights) != witness.coefficient_count:
        raise ActiveSubspaceError(
            "CoefficientWeightLengthMismatch",
            "weights and coefficient generators must have equal length",
        )
    try:
        admitted = tuple(gaussian.rational(weight) for weight in weights)
    except ValueError as error:
        raise ActiveSubspaceError("InexactCoefficientWeight", str(error)) from error
    result = gaussian.zero(witness.active_dimension)
    for weight, coefficient in zip(admitted, witness.reduced_coefficients, strict=True):
        result = gaussian.add(result, gaussian.scale(coefficient, weight))
    return result


def evaluate_family_expectation(
    witness: CoefficientFamilyActiveSubspaceWitness,
    weights: tuple[object, ...],
    time: object,
) -> float:
    """Evaluate one specialization without reconstructing its invariant carrier."""
    try:
        admitted_time = gaussian.rational(time)
    except ValueError as error:
        raise ActiveSubspaceError("InexactTimeDatum", str(error)) from error
    if admitted_time < 0:
        raise ActiveSubspaceError("NegativePropagationTime", "time must be nonnegative")
    value, imaginary_residual = _expectation(
        specialize_active_hamiltonian(witness, weights),
        witness.initial_coordinates,
        witness.compressed_effect,
        admitted_time,
        witness.gram[0][0].real,
    )
    if imaginary_residual > witness.numerical_tolerance:
        raise ActiveSubspaceError(
            "ActiveExpectationResidual", "compressed-effect expectation is not numerically real"
        )
    return value


def _admit_matrix(value: object, name: str) -> gaussian.ComplexMatrix:
    if (
        not isinstance(value, tuple)
        or not value
        or any(not isinstance(row, tuple) for row in value)
    ):
        raise ActiveSubspaceError("InvalidMatrix", f"{name} must be a nonempty square matrix")
    dimension = len(value)
    if any(len(row) != dimension for row in value):
        raise ActiveSubspaceError("InvalidMatrix", f"{name} must be a nonempty square matrix")
    try:
        return tuple(tuple(gaussian.scalar(entry) for entry in row) for row in value)
    except ValueError as error:
        raise ActiveSubspaceError("InexactMatrixDatum", f"{name}: {error}") from error


def _admit_vector(value: object, dimension: int) -> Vector:
    if not isinstance(value, tuple) or len(value) != dimension:
        raise ActiveSubspaceError(
            "PreparationDimensionMismatch", f"preparation must have dimension {dimension}"
        )
    try:
        return tuple(gaussian.scalar(entry) for entry in value)
    except ValueError as error:
        raise ActiveSubspaceError("InexactPreparationDatum", str(error)) from error


def _inner(left: Vector, right: Vector) -> gaussian.Gaussian:
    return sum((x.conjugate() * y for x, y in zip(left, right, strict=True)), gaussian.ZERO)


def _matrix_from_columns(columns: tuple[Vector, ...]) -> gaussian.ComplexMatrix:
    return tuple(
        tuple(columns[column][row] for column in range(len(columns)))
        for row in range(len(columns[0]))
    )


def _pairing_matrix(
    left_basis: tuple[Vector, ...], right_vectors: tuple[Vector, ...]
) -> gaussian.ComplexMatrix:
    return tuple(tuple(_inner(left, right) for right in right_vectors) for left in left_basis)


def _standard_vector(dimension: int, selected: int) -> Vector:
    return tuple(gaussian.ONE if index == selected else gaussian.ZERO for index in range(dimension))


def _numpy_matrix(value: gaussian.ComplexMatrix) -> np.ndarray:
    return np.array(
        [[complex(float(entry.real), float(entry.imaginary)) for entry in row] for row in value],
        dtype=np.complex128,
    )


def _numpy_vector(value: Vector) -> np.ndarray:
    return np.array(
        [complex(float(entry.real), float(entry.imaginary)) for entry in value],
        dtype=np.complex128,
    )


def _expectation(
    hamiltonian: gaussian.ComplexMatrix,
    preparation: Vector,
    effect: gaussian.ComplexMatrix,
    time: Fraction,
    normalization: Fraction,
) -> tuple[float, float]:
    propagator = expm(-1j * float(time) * _numpy_matrix(hamiltonian))
    state = propagator @ _numpy_vector(preparation)
    value = np.vdot(state, _numpy_matrix(effect) @ state)
    norm = float(normalization)
    return float(value.real / norm), abs(float(value.imag)) / norm


def _admit(
    hamiltonian: object,
    preparation: object,
    effect: object,
    time: object,
    budget: ActiveSubspaceBudget,
    numerical_tolerance: float,
) -> tuple[gaussian.ComplexMatrix, Vector, gaussian.ComplexMatrix, Fraction]:
    admitted_hamiltonian = _admit_matrix(hamiltonian, "Hamiltonian")
    dimension = len(admitted_hamiltonian)
    admitted_effect = _admit_matrix(effect, "effect")
    if len(admitted_effect) != dimension:
        raise ActiveSubspaceError("EffectDimensionMismatch", "effect and Hamiltonian differ")
    admitted_preparation = _admit_vector(preparation, dimension)
    try:
        admitted_time = gaussian.rational(time)
    except ValueError as error:
        raise ActiveSubspaceError("InexactTimeDatum", str(error)) from error
    if not gaussian.is_hermitian(admitted_hamiltonian):
        raise ActiveSubspaceError("NonHermitianHamiltonian", "Hamiltonian must be Hermitian")
    if not gaussian.is_hermitian(admitted_effect):
        raise ActiveSubspaceError("NonHermitianEffect", "effect must be Hermitian")
    integer_bounds = (budget.maximum_carrier_dimension, budget.maximum_active_dimension)
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value <= 0
        for value in integer_bounds
    ):
        raise ActiveSubspaceError("InvalidActiveSubspaceBudget", "bounds must be positive integers")
    if dimension > budget.maximum_carrier_dimension:
        raise ActiveSubspaceError("CarrierBudgetExceeded", "carrier dimension exceeds budget")
    if admitted_time < 0:
        raise ActiveSubspaceError("NegativePropagationTime", "time must be nonnegative")
    if not math.isfinite(numerical_tolerance) or numerical_tolerance <= 0:
        raise ActiveSubspaceError("InvalidNumericalTolerance", "tolerance must be positive")
    if _inner(admitted_preparation, admitted_preparation) == gaussian.ZERO:
        raise ActiveSubspaceError("ZeroPreparation", "preparation must be nonzero")
    return admitted_hamiltonian, admitted_preparation, admitted_effect, admitted_time


def _admit_family(
    coefficients: object,
    preparation: object,
    effect: object,
    budget: ActiveSubspaceBudget,
    numerical_tolerance: float,
) -> tuple[tuple[gaussian.ComplexMatrix, ...], Vector, gaussian.ComplexMatrix]:
    if not isinstance(coefficients, tuple) or not coefficients:
        raise ActiveSubspaceError(
            "EmptyCoefficientFamily", "coefficient family must be a nonempty tuple"
        )
    admitted_coefficients = tuple(
        _admit_matrix(value, f"coefficient[{index}]") for index, value in enumerate(coefficients)
    )
    dimension = len(admitted_coefficients[0])
    if any(len(value) != dimension for value in admitted_coefficients):
        raise ActiveSubspaceError(
            "CoefficientDimensionMismatch", "coefficient generators must have equal dimensions"
        )
    if any(not gaussian.is_hermitian(value) for value in admitted_coefficients):
        raise ActiveSubspaceError(
            "NonHermitianCoefficient", "every coefficient generator must be Hermitian"
        )
    admitted_effect = _admit_matrix(effect, "effect")
    if len(admitted_effect) != dimension:
        raise ActiveSubspaceError("EffectDimensionMismatch", "effect and coefficients differ")
    if not gaussian.is_hermitian(admitted_effect):
        raise ActiveSubspaceError("NonHermitianEffect", "effect must be Hermitian")
    admitted_preparation = _admit_vector(preparation, dimension)
    integer_bounds = (budget.maximum_carrier_dimension, budget.maximum_active_dimension)
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value <= 0
        for value in integer_bounds
    ):
        raise ActiveSubspaceError("InvalidActiveSubspaceBudget", "bounds must be positive integers")
    if dimension > budget.maximum_carrier_dimension:
        raise ActiveSubspaceError("CarrierBudgetExceeded", "carrier dimension exceeds budget")
    if not math.isfinite(numerical_tolerance) or numerical_tolerance <= 0:
        raise ActiveSubspaceError("InvalidNumericalTolerance", "tolerance must be positive")
    if _inner(admitted_preparation, admitted_preparation) == gaussian.ZERO:
        raise ActiveSubspaceError("ZeroPreparation", "preparation must be nonzero")
    return admitted_coefficients, admitted_preparation, admitted_effect


def construct_coefficient_family_active_subspace(
    coefficients: tuple[gaussian.ComplexMatrix, ...],
    preparation: Vector,
    effect: gaussian.ComplexMatrix,
    budget: ActiveSubspaceBudget,
    *,
    numerical_tolerance: float = NUMERICAL_TOLERANCE,
) -> CoefficientFamilyActiveSubspaceWitness:
    """Construct the minimal common invariant carrier for all coefficients."""
    coefficients, preparation, effect = _admit_family(
        coefficients, preparation, effect, budget, numerical_tolerance
    )
    dimension = len(coefficients[0])
    basis = [preparation]
    action_records: list[list[Vector | int]] = []
    action_images: list[list[Vector]] = []
    basis_index = 0
    while basis_index < len(basis):
        records: list[Vector | int] = []
        images: list[Vector] = []
        for coefficient in coefficients:
            image = matrix_vector(coefficient, basis[basis_index])
            images.append(image)
            coordinate = coordinates(image, tuple(basis))
            if coordinate is None:
                if len(basis) >= budget.maximum_active_dimension:
                    raise ActiveSubspaceError(
                        "ActiveSubspaceBudgetExceeded",
                        "coefficient-family closure exceeds active-dimension budget",
                    )
                basis.append(image)
                records.append(len(basis) - 1)
            else:
                records.append(coordinate)
        action_records.append(records)
        action_images.append(images)
        basis_index += 1

    active_basis = tuple(basis)
    active_dimension = len(active_basis)

    def final_coordinate(record: Vector | int) -> Vector:
        if isinstance(record, int):
            return _standard_vector(active_dimension, record)
        return (*record, *(gaussian.ZERO for _ in range(active_dimension - len(record))))

    reduced_coefficients = tuple(
        _matrix_from_columns(
            tuple(
                final_coordinate(action_records[index][coefficient_index])
                for index in range(active_dimension)
            )
        )
        for coefficient_index in range(len(coefficients))
    )
    gram = _pairing_matrix(active_basis, active_basis)
    effect_images = tuple(matrix_vector(effect, vector) for vector in active_basis)
    compressed_effect = _pairing_matrix(active_basis, effect_images)
    initial_coordinates = _standard_vector(active_dimension, 0)
    checks = {
        "basis_starts_at_preparation": active_basis[0] == preparation,
        "every_coefficient_closes_on_basis": all(
            linear_combination(
                tuple(reduced[row][column] for row in range(active_dimension)), active_basis
            )
            == action_images[column][coefficient_index]
            for coefficient_index, reduced in enumerate(reduced_coefficients)
            for column in range(active_dimension)
        ),
        "every_reduced_coefficient_is_gram_self_adjoint": all(
            gaussian.multiply(gram, reduced) == gaussian.multiply(gaussian.dagger(reduced), gram)
            for reduced in reduced_coefficients
        ),
        "compressed_effect_is_hermitian": gaussian.is_hermitian(compressed_effect),
        "preparation_coordinates_recover": linear_combination(initial_coordinates, active_basis)
        == preparation,
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise ActiveSubspaceError("ActiveSubspaceResidual", f"construction fails at {failed}")
    coefficient_count = len(coefficients)
    return CoefficientFamilyActiveSubspaceWitness(
        "ExactCoefficientFamilyReduction",
        dimension,
        active_dimension,
        coefficient_count,
        active_basis,
        reduced_coefficients,
        gram,
        compressed_effect,
        initial_coordinates,
        numerical_tolerance,
        active_dimension == dimension,
        "finite exact Hermitian coefficient family with fixed preparation/effect",
        CoefficientFamilyCost(
            coefficient_count * active_dimension,
            coefficient_count * active_dimension,
            active_dimension * active_dimension,
            active_dimension,
            active_dimension * active_dimension,
        ),
        checks,
    )


def construct_active_subspace(
    hamiltonian: gaussian.ComplexMatrix,
    preparation: Vector,
    effect: gaussian.ComplexMatrix,
    time: Fraction,
    budget: ActiveSubspaceBudget,
    *,
    reference_expectation: float | None = None,
    evaluate_full_reference: bool = True,
    numerical_tolerance: float = NUMERICAL_TOLERANCE,
) -> ActiveSubspaceWitness:
    """Construct the minimal exact `H`-invariant carrier containing `preparation`."""
    hamiltonian, preparation, effect, time = _admit(
        hamiltonian, preparation, effect, time, budget, numerical_tolerance
    )
    dimension = len(hamiltonian)
    basis = [preparation]
    images: list[Vector] = []
    while True:
        image = matrix_vector(hamiltonian, basis[-1])
        images.append(image)
        closure = coordinates(image, tuple(basis))
        if closure is not None:
            break
        if len(basis) >= budget.maximum_active_dimension:
            raise ActiveSubspaceError(
                "ActiveSubspaceBudgetExceeded", "Krylov closure exceeds active-dimension budget"
            )
        basis.append(image)
    active_basis = tuple(basis)
    active_dimension = len(active_basis)
    columns = tuple(
        _standard_vector(active_dimension, index + 1) for index in range(active_dimension - 1)
    ) + (closure,)
    reduced_hamiltonian = _matrix_from_columns(columns)
    gram = _pairing_matrix(active_basis, active_basis)
    effect_images = tuple(matrix_vector(effect, vector) for vector in active_basis)
    compressed_effect = _pairing_matrix(active_basis, effect_images)
    initial_coordinates = _standard_vector(active_dimension, 0)
    preparation_norm = _inner(preparation, preparation).real
    active_expectation, active_imaginary = _expectation(
        reduced_hamiltonian,
        initial_coordinates,
        compressed_effect,
        time,
        preparation_norm,
    )
    if reference_expectation is None and evaluate_full_reference:
        reference_expectation, reference_imaginary = _expectation(
            hamiltonian, preparation, effect, time, preparation_norm
        )
        reference_source = "direct full-carrier numerical certificate"
        evaluated_reference = True
    elif reference_expectation is None:
        reference_imaginary = 0.0
        reference_source = "exact recovery law; numerical full reference not evaluated"
        evaluated_reference = False
    else:
        if not math.isfinite(reference_expectation):
            raise ActiveSubspaceError("InvalidReferenceExpectation", "reference must be finite")
        reference_imaginary = 0.0
        reference_source = "supplied same-contract reference"
        evaluated_reference = False
    observable_error = (
        None if reference_expectation is None else abs(active_expectation - reference_expectation)
    )
    checks = {
        "basis_starts_at_preparation": active_basis[0] == preparation,
        "hamiltonian_closes_on_basis": all(
            linear_combination(column, active_basis) == image
            for column, image in zip(columns, images, strict=True)
        ),
        "reduced_hamiltonian_is_gram_self_adjoint": gaussian.multiply(gram, reduced_hamiltonian)
        == gaussian.multiply(gaussian.dagger(reduced_hamiltonian), gram),
        "compressed_effect_is_hermitian": gaussian.is_hermitian(compressed_effect),
        "preparation_coordinates_recover": linear_combination(initial_coordinates, active_basis)
        == preparation,
        "observable_expectations_are_real": max(active_imaginary, reference_imaginary)
        <= numerical_tolerance,
        "same_observable_or_exact_recovery_only": observable_error is None
        or observable_error <= numerical_tolerance,
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise ActiveSubspaceError("ActiveSubspaceResidual", f"construction fails at {failed}")
    return ActiveSubspaceWitness(
        "ExactPreparedObservableReduction",
        dimension,
        active_dimension,
        active_basis,
        closure,
        reduced_hamiltonian,
        gram,
        compressed_effect,
        initial_coordinates,
        active_expectation,
        reference_expectation,
        observable_error,
        numerical_tolerance,
        active_dimension == dimension,
        reference_source,
        "finite exact Gaussian-rational Hermitian carrier with supplied preparation/effect",
        ActiveSubspaceCost(
            active_dimension,
            active_dimension,
            active_dimension * active_dimension,
            active_dimension,
            active_dimension * active_dimension,
            evaluated_reference,
            dimension**3,
            active_dimension**3,
        ),
        checks,
    )
