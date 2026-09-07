"""Prepared-observable Krylov reduction of assembled finite propagation blocks."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from coefficient_projector_jet import SpectralProjectorJet
from finite_window_propagation import (
    NUMERICAL_TOLERANCE,
    FinitePropagationWindow,
    PreparedPropagationWindow,
    construct_off_block_prepared_window,
)
from gaussian_active_subspace import (
    ActiveSubspaceBudget,
    ActiveSubspaceError,
    ActiveSubspaceWitness,
    CoefficientFamilyActiveSubspaceWitness,
    construct_active_subspace,
    construct_coefficient_family_active_subspace,
    evaluate_active_expectation,
    evaluate_family_expectation,
)
from off_block_differential import OffBlockDifferentialJet, construct_off_block_differential
from simple_block_pde import IrreducibleModel


class ActiveWindowError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class ActiveWindowCost:
    hamiltonian_actions: int
    exact_coordinate_solves: int
    gram_and_effect_pairings: int
    full_reference_exponentials_evaluated: int
    full_exponential_cubic_proxy: int
    active_exponential_cubic_proxy: int


@dataclass(frozen=True)
class ActiveWindowWitness:
    blocks: tuple[ActiveSubspaceWitness, ...]
    ambient_dimensions: tuple[int, ...]
    active_dimensions: tuple[int, ...]
    active_probability: float
    reference_probability: float | None
    observable_error: float | None
    numerical_tolerance: float
    any_dimension_gain: bool
    observable: str
    recovery: str
    domain_contract: str
    cost: ActiveWindowCost
    checks: dict[str, bool]


@dataclass(frozen=True)
class CoefficientFamilyWindowCost:
    coefficient_actions: int
    exact_coordinate_solves: int
    gram_and_effect_pairings: int
    specialized_blocks: int
    full_exponential_cubic_proxy: int
    active_exponential_cubic_proxy: int


@dataclass(frozen=True)
class CoefficientFamilyActiveWindowWitness:
    family: CoefficientFamilyActiveSubspaceWitness
    coefficient_names: tuple[str, ...]
    coefficient_matrices: tuple[gaussian.ComplexMatrix, ...]
    specialization_weights: tuple[tuple[Fraction, ...], ...]
    exact_specializations: tuple[bool, ...]
    ambient_dimension: int
    active_dimension: int
    active_probability: float
    numerical_tolerance: float
    any_dimension_gain: bool
    observable: str
    recovery: str
    domain_contract: str
    cost: CoefficientFamilyWindowCost
    checks: dict[str, bool]


def evaluate_active_window_at_time(witness: ActiveWindowWitness, time: object) -> float:
    """Reuse every constructed block carrier for another common time."""
    norms = tuple(block.gram[0][0].real for block in witness.blocks)
    return sum(
        evaluate_active_expectation(block, time) * float(norm)
        for block, norm in zip(witness.blocks, norms, strict=True)
    ) / float(sum(norms, Fraction(0)))


def construct_prepared_active_window(
    prepared: PreparedPropagationWindow,
    budget: ActiveSubspaceBudget,
    *,
    reference_expectations: tuple[float, ...] | None = None,
    numerical_tolerance: float = NUMERICAL_TOLERANCE,
) -> ActiveWindowWitness:
    """Compress already assembled blocks; a full numerical reference is optional."""
    if not prepared.blocks:
        raise ActiveWindowError(
            "ActiveWindowLengthMismatch", "prepared window must contain at least one block"
        )
    if reference_expectations is not None and len(reference_expectations) != len(prepared.blocks):
        raise ActiveWindowError(
            "ActiveReferenceLengthMismatch", "references and prepared blocks must have equal length"
        )
    reductions = []
    for index, block in enumerate(prepared.blocks):
        reference = None if reference_expectations is None else reference_expectations[index]
        try:
            reduction = construct_active_subspace(
                block.full_hamiltonian,
                block.carrier_preparation,
                block.effect,
                prepared.window.time,
                budget,
                reference_expectation=reference,
                evaluate_full_reference=False,
                numerical_tolerance=numerical_tolerance,
            )
        except (ActiveSubspaceError, ValueError) as error:
            kind = getattr(error, "kind", "ActiveWindowPreparationMismatch")
            raise ActiveWindowError(kind, str(error)) from error
        reductions.append(reduction)
    blocks = tuple(reductions)
    total_norm = float(prepared.total_norm_squared)
    active_probability = (
        sum(
            reduction.active_expectation * float(block.preparation_norm_squared)
            for reduction, block in zip(blocks, prepared.blocks, strict=True)
        )
        / total_norm
    )
    reference_probability = (
        None
        if reference_expectations is None
        else sum(
            reference * float(block.preparation_norm_squared)
            for reference, block in zip(reference_expectations, prepared.blocks, strict=True)
        )
        / total_norm
    )
    observable_error = (
        None if reference_probability is None else abs(active_probability - reference_probability)
    )
    checks = {
        "all_active_block_laws_hold": all(all(block.checks.values()) for block in blocks),
        "same_block_references_or_exact_recovery_only": all(
            block.observable_error is None or block.observable_error <= numerical_tolerance
            for block in blocks
        ),
        "same_window_observable_or_exact_recovery_only": observable_error is None
        or observable_error <= numerical_tolerance,
        "active_observable_obeys_original_bound": -numerical_tolerance
        <= active_probability
        <= float(prepared.probability_bound) + numerical_tolerance,
        "full_reference_not_recomputed": not any(
            block.cost.full_reference_exponential_evaluated for block in blocks
        ),
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise ActiveWindowError("ActiveWindowResidual", f"construction fails at {failed}")
    costs = tuple(block.cost for block in blocks)
    return ActiveWindowWitness(
        blocks,
        tuple(block.ambient_dimension for block in blocks),
        tuple(block.active_dimension for block in blocks),
        active_probability,
        reference_probability,
        observable_error,
        numerical_tolerance,
        any(not block.no_dimension_gain for block in blocks),
        "probability in the selected projector complement",
        "norm-weighted sum of compressed-effect expectations",
        "assembled finite exact Hermitian blocks; full references are optional evidence",
        ActiveWindowCost(
            sum(cost.hamiltonian_actions for cost in costs),
            sum(cost.exact_coordinate_solves for cost in costs),
            sum(cost.gram_pairings + cost.effect_pairings for cost in costs),
            sum(cost.full_reference_exponential_evaluated for cost in costs),
            sum(cost.full_exponential_cubic_proxy for cost in costs),
            sum(cost.active_exponential_cubic_proxy for cost in costs),
        ),
        checks,
    )


def _specialize_full_hamiltonian(
    coefficients: tuple[gaussian.ComplexMatrix, ...], weights: tuple[Fraction, ...]
) -> gaussian.ComplexMatrix:
    result = gaussian.zero(len(coefficients[0]))
    for coefficient, weight in zip(coefficients, weights, strict=True):
        result = gaussian.add(result, gaussian.scale(coefficient, weight))
    return result


def construct_coefficient_family_active_window(
    model: IrreducibleModel,
    differential: OffBlockDifferentialJet,
    window: FinitePropagationWindow,
    budget: ActiveSubspaceBudget,
    *,
    numerical_tolerance: float = NUMERICAL_TOLERANCE,
) -> CoefficientFamilyActiveWindowWitness:
    """Construct one unsampled active module for an entire G15 window."""
    prepared = construct_off_block_prepared_window(model, differential, window)
    return construct_prepared_coefficient_family_active_window(
        prepared, differential, budget, numerical_tolerance=numerical_tolerance
    )


def construct_prepared_coefficient_family_active_window(
    prepared: PreparedPropagationWindow,
    differential: OffBlockDifferentialJet,
    budget: ActiveSubspaceBudget,
    *,
    numerical_tolerance: float = NUMERICAL_TOLERANCE,
) -> CoefficientFamilyActiveWindowWitness:
    """Compress one already assembled window using its unsampled G15 family."""
    preparations = tuple(block.carrier_preparation for block in prepared.blocks)
    effects = tuple(block.effect for block in prepared.blocks)
    if any(value != preparations[0] for value in preparations[1:]):
        raise ActiveWindowError(
            "VariablePreparationFamily",
            "one coefficient-family carrier requires a fixed preparation",
        )
    if any(value != effects[0] for value in effects[1:]):
        raise ActiveWindowError(
            "VariableEffectFamily", "one coefficient-family carrier requires a fixed effect"
        )

    dimension = len(differential.projector)
    signed_projector = gaussian.add(
        gaussian.identity(dimension), gaussian.scale(differential.projector, -2)
    )
    first_hermitian = gaussian.add(
        differential.first_operator, gaussian.dagger(differential.first_operator)
    )
    second_hermitian = gaussian.add(
        differential.second_operator, gaussian.dagger(differential.second_operator)
    )
    coefficients = (
        gaussian.scale(signed_projector, Fraction(1, 2)),
        gaussian.scale(first_hermitian, 2 * prepared.window.slow_scale),
        gaussian.scale(second_hermitian, prepared.window.slow_scale),
    )
    weights = tuple((block.gap, block.momentum, Fraction(1)) for block in prepared.blocks)
    exact_specializations = tuple(
        _specialize_full_hamiltonian(coefficients, weight) == block.full_hamiltonian
        for weight, block in zip(weights, prepared.blocks, strict=True)
    )
    if not all(exact_specializations):
        raise ActiveWindowError(
            "CoefficientFamilySpecializationResidual",
            "derived coefficient family does not recover every assembled block",
        )
    try:
        family = construct_coefficient_family_active_subspace(
            coefficients,
            preparations[0],
            effects[0],
            budget,
            numerical_tolerance=numerical_tolerance,
        )
        expectations = tuple(
            evaluate_family_expectation(family, weight, prepared.window.time) for weight in weights
        )
    except (ActiveSubspaceError, ValueError) as error:
        kind = getattr(error, "kind", "CoefficientFamilyPreparationMismatch")
        raise ActiveWindowError(kind, str(error)) from error
    active_probability = sum(
        expectation * float(block.preparation_norm_squared)
        for expectation, block in zip(expectations, prepared.blocks, strict=True)
    ) / float(prepared.total_norm_squared)
    checks = {
        **prepared.checks,
        "derived_coefficients_are_hermitian": all(
            gaussian.is_hermitian(coefficient) for coefficient in coefficients
        ),
        "every_block_is_exact_specialization": all(exact_specializations),
        "all_family_laws_hold": all(family.checks.values()),
        "active_observable_obeys_original_bound": -numerical_tolerance
        <= active_probability
        <= float(prepared.probability_bound) + numerical_tolerance,
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise ActiveWindowError(
            "CoefficientFamilyWindowResidual", f"construction fails at {failed}"
        )
    family_cost = family.cost
    block_count = len(prepared.blocks)
    return CoefficientFamilyActiveWindowWitness(
        family,
        ("gap", "momentum", "constant"),
        coefficients,
        weights,
        exact_specializations,
        family.ambient_dimension,
        family.active_dimension,
        active_probability,
        numerical_tolerance,
        not family.no_dimension_gain,
        "probability in the selected projector complement",
        "norm-weighted specialization of one coefficient-family module",
        "G15 finite exact jet with fixed preparation/effect across the window",
        CoefficientFamilyWindowCost(
            family_cost.coefficient_actions,
            family_cost.exact_coordinate_solves,
            family_cost.gram_pairings + family_cost.effect_pairings,
            block_count,
            block_count * family.ambient_dimension**3,
            block_count * family.active_dimension**3,
        ),
        checks,
    )


def construct_projector_active_window_propagation(
    model: IrreducibleModel,
    projector_jet: SpectralProjectorJet,
    window: FinitePropagationWindow,
    budget: ActiveSubspaceBudget,
    *,
    numerical_tolerance: float = NUMERICAL_TOLERANCE,
) -> ActiveWindowWitness:
    """Run G14--G17 without evaluating an ambient-carrier exponential."""
    differential = construct_off_block_differential(
        model,
        projector_jet.projector,
        projector_jet.first_off_block_operator,
        projector_jet.second_off_block_operator,
        "G14 coefficient-derived projector jet",
    )
    prepared = construct_off_block_prepared_window(model, differential, window)
    return construct_prepared_active_window(
        prepared, budget, numerical_tolerance=numerical_tolerance
    )
