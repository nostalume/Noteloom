"""Prepared-observable Krylov reduction of assembled finite propagation blocks."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

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
    construct_active_subspace,
    evaluate_active_expectation,
)
from off_block_differential import construct_off_block_differential
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
