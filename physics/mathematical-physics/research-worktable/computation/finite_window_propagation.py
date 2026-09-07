"""Invariant full-block propagation on a finite exact momentum window."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import numpy as np
from scipy.linalg import expm

import exact_gaussian_matrix as gaussian
from exact_gaussian_linear import Vector, coordinates, linear_combination, matrix_vector, rank
from mode_bundle_jet import ModeBundleJet
from off_block_differential import OffBlockDifferentialJet, construct_off_block_differential
from simple_block_pde import IrreducibleModel

NUMERICAL_TOLERANCE = 1e-11


class WindowPropagationError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class FinitePropagationWindow:
    momenta: tuple[Fraction, ...]
    gaps: tuple[Fraction, ...]
    slow_scale: Fraction
    time: Fraction
    preparations: tuple[Vector, ...]


@dataclass(frozen=True)
class PreparedMomentumBlock:
    momentum: Fraction
    gap: Fraction
    leakage_columns: tuple[Vector, ...]
    coupling_operator: gaussian.ComplexMatrix
    baseline_hamiltonian: gaussian.ComplexMatrix
    full_hamiltonian: gaussian.ComplexMatrix
    effect: gaussian.ComplexMatrix
    carrier_preparation: Vector
    coupling_rank: int
    frobenius_upper_squared: Fraction
    preparation_norm_squared: Fraction
    preparation_coupling_squared: Fraction
    checks: dict[str, bool]


@dataclass(frozen=True)
class PreparedPropagationWindow:
    window: FinitePropagationWindow
    blocks: tuple[PreparedMomentumBlock, ...]
    total_norm_squared: Fraction
    short_time_bound: Fraction
    gap_bound: Fraction
    probability_bound: Fraction
    differential_source: str
    analysis_coordinate_solves: int
    checks: dict[str, bool]


@dataclass(frozen=True)
class MomentumBlockWitness:
    momentum: Fraction
    gap: Fraction
    leakage_columns: tuple[Vector, ...]
    coupling_operator: gaussian.ComplexMatrix
    baseline_hamiltonian: gaussian.ComplexMatrix
    full_hamiltonian: gaussian.ComplexMatrix
    coupling_rank: int
    frobenius_upper_squared: Fraction
    preparation_norm_squared: Fraction
    preparation_coupling_squared: Fraction
    observed_transition_probability: float
    unitarity_residual: float
    expectation_imaginary_residual: float
    checks: dict[str, bool]


@dataclass(frozen=True)
class WindowPropagationCost:
    analysis_coordinate_solves: int
    coupling_matrix_entries: int
    propagated_blocks: int
    propagated_block_dimension: int


@dataclass(frozen=True)
class WindowPropagationWitness:
    window: FinitePropagationWindow
    blocks: tuple[MomentumBlockWitness, ...]
    full_transition_probability: float
    reduced_transition_probability: float
    observable_error: float
    short_time_bound: Fraction
    gap_bound: Fraction
    probability_bound: Fraction
    numerical_tolerance: float
    differential_source: str
    domain_contract: str
    observable: str
    cost: WindowPropagationCost
    checks: dict[str, bool]


def _admit_rational(value: object, label: str) -> Fraction:
    try:
        return gaussian.rational(value)
    except ValueError as error:
        raise WindowPropagationError("InexactWindowDatum", f"{label}: {error}") from error


def _admit_vector(value: object, dimension: int, label: str) -> Vector:
    if not isinstance(value, tuple) or len(value) != dimension:
        raise WindowPropagationError(
            "PreparationDimensionMismatch", f"{label} must have dimension {dimension}"
        )
    try:
        return tuple(gaussian.scalar(entry) for entry in value)
    except ValueError as error:
        raise WindowPropagationError("InexactPreparationDatum", f"{label}: {error}") from error


def _norm_squared(value: Vector) -> Fraction:
    return sum(
        (entry.real * entry.real + entry.imaginary * entry.imaginary for entry in value),
        Fraction(0),
    )


def _matrix_from_columns(columns: tuple[Vector, ...]) -> gaussian.ComplexMatrix:
    return tuple(
        tuple(columns[column][row] for column in range(len(columns)))
        for row in range(len(columns[0]))
    )


def _standard_vector(dimension: int, selected: int) -> Vector:
    return tuple(gaussian.ONE if index == selected else gaussian.ZERO for index in range(dimension))


def _construct_analysis(jet: ModeBundleJet) -> tuple[tuple[Vector, ...], dict[str, bool]]:
    projector = jet.model.selected_projector
    embedding = jet.model.embedding_columns
    carrier_dimension = len(projector)
    reduced_dimension = len(embedding)
    analysis_columns: list[Vector] = []
    for index in range(carrier_dimension):
        projected = matrix_vector(projector, _standard_vector(carrier_dimension, index))
        coefficient = coordinates(projected, embedding)
        if coefficient is None:
            raise WindowPropagationError(
                "AnalysisCoordinateResidual", "projected carrier vector is outside the frame"
            )
        analysis_columns.append(coefficient)
    analysis = tuple(analysis_columns)
    synthesis_analysis = _matrix_from_columns(
        tuple(linear_combination(column, embedding) for column in analysis)
    )
    analysis_synthesis = tuple(linear_combination(vector, analysis) for vector in embedding)
    checks = {
        "analysis_synthesis_is_identity": analysis_synthesis
        == tuple(_standard_vector(reduced_dimension, index) for index in range(reduced_dimension)),
        "synthesis_analysis_is_projector": synthesis_analysis == projector,
    }
    return analysis, checks


def _carrier_arrow(
    leakage_columns: tuple[Vector, ...], analysis: tuple[Vector, ...]
) -> gaussian.ComplexMatrix:
    dimension = len(analysis)
    return tuple(
        tuple(
            sum(
                (
                    leakage_columns[index][row] * analysis[column][index]
                    for index in range(len(leakage_columns))
                ),
                gaussian.ZERO,
            )
            for column in range(dimension)
        )
        for row in range(dimension)
    )


def _frobenius_squared(value: gaussian.ComplexMatrix) -> Fraction:
    return sum(
        (
            entry.real * entry.real + entry.imaginary * entry.imaginary
            for row in value
            for entry in row
        ),
        Fraction(0),
    )


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


def _prepare_block(
    model: IrreducibleModel,
    differential: OffBlockDifferentialJet,
    momentum: Fraction,
    gap: Fraction,
    slow_scale: Fraction,
    preparation: Vector,
) -> PreparedMomentumBlock:
    projector = differential.projector
    complement = gaussian.add(gaussian.identity(len(projector)), gaussian.scale(projector, -1))
    arrow = gaussian.scale(
        gaussian.add(
            gaussian.scale(differential.first_operator, 2 * momentum),
            differential.second_operator,
        ),
        slow_scale,
    )
    leakage = tuple(matrix_vector(arrow, vector) for vector in model.embedding_columns)
    coupling = gaussian.add(arrow, gaussian.dagger(arrow))
    baseline = gaussian.scale(
        gaussian.add(gaussian.identity(len(projector)), gaussian.scale(projector, -2)), gap / 2
    )
    full = gaussian.add(baseline, coupling)
    carrier_preparation = linear_combination(preparation, model.embedding_columns)
    preparation_norm = _norm_squared(carrier_preparation)
    preparation_coupling = _norm_squared(matrix_vector(arrow, carrier_preparation))
    checks = {
        "leakage_map_is_off_block": gaussian.multiply(projector, arrow)
        == gaussian.zero(len(projector)),
        "leakage_map_has_retained_domain": gaussian.multiply(arrow, projector) == arrow,
        "coupling_is_hermitian": gaussian.is_hermitian(coupling),
        "full_hamiltonian_is_hermitian": gaussian.is_hermitian(full),
        "baseline_preserves_retained_block": gaussian.multiply(
            complement, gaussian.multiply(baseline, projector)
        )
        == gaussian.zero(len(projector)),
        "preparation_starts_retained": matrix_vector(complement, carrier_preparation)
        == tuple(gaussian.ZERO for _ in carrier_preparation),
    }
    return PreparedMomentumBlock(
        momentum=momentum,
        gap=gap,
        leakage_columns=leakage,
        coupling_operator=arrow,
        baseline_hamiltonian=baseline,
        full_hamiltonian=full,
        effect=complement,
        carrier_preparation=carrier_preparation,
        coupling_rank=rank(arrow),
        frobenius_upper_squared=_frobenius_squared(arrow),
        preparation_norm_squared=preparation_norm,
        preparation_coupling_squared=preparation_coupling,
        checks=checks,
    )


def _propagate_block(
    prepared: PreparedMomentumBlock, time: Fraction
) -> tuple[MomentumBlockWitness, float]:
    full_numeric = _numpy_matrix(prepared.full_hamiltonian)
    propagator = expm(-1j * float(time) * full_numeric)
    state = propagator @ _numpy_vector(prepared.carrier_preparation)
    observed = np.vdot(state, _numpy_matrix(prepared.effect) @ state)
    observed_probability = (
        float(observed.real / float(prepared.preparation_norm_squared))
        if prepared.preparation_norm_squared
        else 0.0
    )
    unitarity_residual = float(
        np.linalg.norm(propagator.conj().T @ propagator - np.eye(len(prepared.effect)), ord=2)
    )
    block = MomentumBlockWitness(
        momentum=prepared.momentum,
        gap=prepared.gap,
        leakage_columns=prepared.leakage_columns,
        coupling_operator=prepared.coupling_operator,
        baseline_hamiltonian=prepared.baseline_hamiltonian,
        full_hamiltonian=prepared.full_hamiltonian,
        coupling_rank=prepared.coupling_rank,
        frobenius_upper_squared=prepared.frobenius_upper_squared,
        preparation_norm_squared=prepared.preparation_norm_squared,
        preparation_coupling_squared=prepared.preparation_coupling_squared,
        observed_transition_probability=observed_probability,
        unitarity_residual=unitarity_residual,
        expectation_imaginary_residual=(
            abs(float(observed.imag)) / float(prepared.preparation_norm_squared)
            if prepared.preparation_norm_squared
            else 0.0
        ),
        checks=prepared.checks,
    )
    return block, float(observed.real)


def _prepare_off_block_window(
    model: IrreducibleModel,
    differential: OffBlockDifferentialJet,
    window: FinitePropagationWindow,
    adapter_checks: dict[str, bool],
    analysis_coordinate_solves: int,
) -> PreparedPropagationWindow:
    count = len(window.momenta)
    if not count or len(window.gaps) != count or len(window.preparations) != count:
        raise WindowPropagationError(
            "WindowLengthMismatch", "momenta, gaps, and preparations must have equal nonzero length"
        )
    momenta = tuple(
        _admit_rational(momentum, f"momentum[{index}]")
        for index, momentum in enumerate(window.momenta)
    )
    gaps = tuple(_admit_rational(gap, f"gap[{index}]") for index, gap in enumerate(window.gaps))
    slow_scale = _admit_rational(window.slow_scale, "slow_scale")
    time = _admit_rational(window.time, "time")
    if len(set(momenta)) != count:
        raise WindowPropagationError("DuplicateMomentumPoint", "momentum points must be unique")
    if any(gap <= 0 for gap in gaps):
        raise WindowPropagationError("ClosingGapObstruction", "every supplied gap must be positive")
    if slow_scale < 0:
        raise WindowPropagationError("NegativeSlowScale", "slow scale must be nonnegative")
    if time < 0:
        raise WindowPropagationError("NegativePropagationTime", "time must be nonnegative")
    dimension = model.carrier_dimension
    preparations = tuple(
        _admit_vector(value, dimension, f"preparation[{index}]")
        for index, value in enumerate(window.preparations)
    )
    blocks = tuple(
        _prepare_block(model, differential, momentum, gap, slow_scale, preparation)
        for momentum, gap, preparation in zip(momenta, gaps, preparations, strict=True)
    )
    total_norm = sum((block.preparation_norm_squared for block in blocks), Fraction(0))
    if not total_norm:
        raise WindowPropagationError("ZeroPreparation", "the window preparation must be nonzero")
    short_bound = (
        time
        * time
        * sum((block.preparation_coupling_squared for block in blocks), Fraction(0))
        / total_norm
    )
    gap_bound = (
        sum(
            (4 * block.preparation_coupling_squared / (block.gap * block.gap) for block in blocks),
            Fraction(0),
        )
        / total_norm
    )
    probability_bound = min(Fraction(1), short_bound, gap_bound)
    checks = {
        **adapter_checks,
        **differential.checks,
        "all_block_laws_hold": all(all(block.checks.values()) for block in blocks),
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise WindowPropagationError("WindowPreparationResidual", f"construction fails at {failed}")
    return PreparedPropagationWindow(
        FinitePropagationWindow(momenta, gaps, slow_scale, time, preparations),
        blocks,
        total_norm,
        short_bound,
        gap_bound,
        probability_bound,
        differential.source,
        analysis_coordinate_solves,
        checks,
    )


def propagate_prepared_window(prepared: PreparedPropagationWindow) -> WindowPropagationWitness:
    """Evaluate the dense full-carrier route from an already assembled exact window."""
    blocks_and_numerators = tuple(
        _propagate_block(block, prepared.window.time) for block in prepared.blocks
    )
    blocks = tuple(item[0] for item in blocks_and_numerators)
    full_probability = sum(item[1] for item in blocks_and_numerators) / float(
        prepared.total_norm_squared
    )
    observable_error = abs(full_probability)
    checks = {
        **prepared.checks,
        "numerical_propagators_are_unitary": all(
            block.unitarity_residual <= NUMERICAL_TOLERANCE for block in blocks
        ),
        "observable_expectations_are_real": all(
            block.expectation_imaginary_residual <= NUMERICAL_TOLERANCE for block in blocks
        ),
        "observable_obeys_constructed_bound": -NUMERICAL_TOLERANCE
        <= full_probability
        <= float(prepared.probability_bound) + NUMERICAL_TOLERANCE,
        "zero_preparation_coupling_recovers_zero_error": any(
            block.preparation_coupling_squared for block in blocks
        )
        or observable_error <= NUMERICAL_TOLERANCE,
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise WindowPropagationError("WindowPropagationResidual", f"construction fails at {failed}")
    return WindowPropagationWitness(
        window=prepared.window,
        blocks=blocks,
        full_transition_probability=full_probability,
        reduced_transition_probability=0.0,
        observable_error=observable_error,
        short_time_bound=prepared.short_time_bound,
        gap_bound=prepared.gap_bound,
        probability_bound=prepared.probability_bound,
        numerical_tolerance=NUMERICAL_TOLERANCE,
        differential_source=prepared.differential_source,
        domain_contract="finite direct sum of bounded Gaussian-rational carrier blocks",
        observable="probability in the selected projector complement",
        cost=WindowPropagationCost(
            analysis_coordinate_solves=prepared.analysis_coordinate_solves,
            coupling_matrix_entries=len(blocks) * len(blocks[0].full_hamiltonian) ** 2,
            propagated_blocks=len(blocks),
            propagated_block_dimension=len(blocks[0].full_hamiltonian),
        ),
        checks=checks,
    )


def construct_off_block_prepared_window(
    model: IrreducibleModel,
    differential: OffBlockDifferentialJet,
    window: FinitePropagationWindow,
) -> PreparedPropagationWindow:
    """Assemble exact finite Hamiltonians without evaluating a matrix exponential."""
    return _prepare_off_block_window(model, differential, window, {}, 0)


def _construct_off_block_window(
    model: IrreducibleModel,
    differential: OffBlockDifferentialJet,
    window: FinitePropagationWindow,
    adapter_checks: dict[str, bool],
    analysis_coordinate_solves: int,
) -> WindowPropagationWitness:
    return propagate_prepared_window(
        _prepare_off_block_window(
            model, differential, window, adapter_checks, analysis_coordinate_solves
        )
    )


def construct_off_block_window_propagation(
    model: IrreducibleModel,
    differential: OffBlockDifferentialJet,
    window: FinitePropagationWindow,
) -> WindowPropagationWitness:
    """Propagate one admitted invariant differential jet without frame analysis."""
    return _construct_off_block_window(model, differential, window, {}, 0)


def construct_window_propagation(
    jet: ModeBundleJet, window: FinitePropagationWindow
) -> WindowPropagationWitness:
    """Adapt a G11 frame jet to the invariant differential propagation core."""
    analysis, analysis_checks = _construct_analysis(jet)
    differential = construct_off_block_differential(
        jet.model,
        jet.model.selected_projector,
        _carrier_arrow(jet.first_leakage_columns, analysis),
        _carrier_arrow(jet.second_leakage_columns, analysis),
        "G11 frame leakage columns",
    )
    return _construct_off_block_window(
        jet.model,
        differential,
        window,
        analysis_checks,
        len(jet.model.selected_projector),
    )
