"""Exact spectral-projector derivatives constructed from Hermitian coefficient jets."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from mode_bundle_jet import ModeBundleJet, construct_mode_jet
from semisimple_coefficient_algebra import (
    AlgebraBudget,
    AlgebraError,
    Generator,
)
from semisimple_coefficient_algebra import (
    construct as construct_coefficient_algebra,
)
from simple_block_pde import IrreducibleModel


class ProjectorJetError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class CoefficientJet:
    value: gaussian.ComplexMatrix
    first_derivative: gaussian.ComplexMatrix
    second_derivative: gaussian.ComplexMatrix
    selected_eigenvalue: Fraction


@dataclass(frozen=True)
class ProjectorJetBudget:
    maximum_carrier_dimension: int
    maximum_factor_candidates: int


@dataclass(frozen=True)
class ProjectorJetCost:
    carrier_dimension: int
    spectral_sectors: int
    factor_candidate_checks: int
    complement_sylvester_blocks: int


@dataclass(frozen=True)
class SpectralProjectorJet:
    coefficient_jet: CoefficientJet
    spectrum: tuple[Fraction, ...]
    spectral_gap: Fraction
    cluster_multiplicity: int
    projector: gaussian.ComplexMatrix
    projector_first_derivative: gaussian.ComplexMatrix
    projector_second_derivative: gaussian.ComplexMatrix
    first_off_block_operator: gaussian.ComplexMatrix
    second_off_block_operator: gaussian.ComplexMatrix
    canonical_transport_generator: gaussian.ComplexMatrix
    rigid_transport: bool
    cost: ProjectorJetCost
    checks: dict[str, bool]


def _sum(values: tuple[gaussian.ComplexMatrix, ...], dimension: int) -> gaussian.ComplexMatrix:
    result = gaussian.zero(dimension)
    for value in values:
        result = gaussian.add(result, value)
    return result


def _sandwich(
    left: gaussian.ComplexMatrix,
    middle: gaussian.ComplexMatrix,
    right: gaussian.ComplexMatrix,
) -> gaussian.ComplexMatrix:
    return gaussian.multiply(gaussian.multiply(left, middle), right)


def _validate_jet(jet: CoefficientJet, budget: ProjectorJetBudget) -> tuple[int, Fraction]:
    if budget.maximum_carrier_dimension <= 0 or budget.maximum_factor_candidates < 0:
        raise ProjectorJetError("InvalidProjectorJetBudget", "projector-jet budget is invalid")
    dimension = len(jet.value)
    values = (jet.value, jet.first_derivative, jet.second_derivative)
    if not dimension or any(
        len(value) != dimension or any(len(row) != dimension for row in value) for value in values
    ):
        raise ProjectorJetError(
            "CoefficientJetDimensionMismatch", "coefficient jets must be square"
        )
    if dimension > budget.maximum_carrier_dimension:
        raise ProjectorJetError(
            "ProjectorJetBudgetExceeded", "carrier dimension exceeds the declared budget"
        )
    if any(not gaussian.is_hermitian(value) for value in values):
        raise ProjectorJetError(
            "NonHermitianCoefficientJet", "coefficient value and derivatives must be Hermitian"
        )
    try:
        selected = gaussian.rational(jet.selected_eigenvalue)
    except ValueError as error:
        raise ProjectorJetError("InexactSelectedEigenvalue", str(error)) from error
    return dimension, selected


def construct_projector_jet(
    jet: CoefficientJet, budget: ProjectorJetBudget
) -> SpectralProjectorJet:
    dimension, selected_value = _validate_jet(jet, budget)
    try:
        algebra = construct_coefficient_algebra(
            (Generator("coefficient", jet.value),),
            AlgebraBudget(
                budget.maximum_carrier_dimension,
                1,
                budget.maximum_factor_candidates,
            ),
        )
    except AlgebraError as error:
        raise ProjectorJetError(error.kind, str(error)) from error
    selected = next(
        (sector for sector in algebra.sectors if sector.character == (selected_value,)), None
    )
    if selected is None:
        raise ProjectorJetError(
            "SelectedClusterAbsent", "selected eigenvalue is absent from the exact spectrum"
        )
    others = tuple(sector for sector in algebra.sectors if sector is not selected)
    if not others:
        raise ProjectorJetError(
            "SpectralGapClosed", "selected cluster has no spectrally separated complement"
        )
    spectrum = tuple(sector.character[0] for sector in algebra.sectors)
    gap = min(abs(value - selected_value) for value in spectrum if value != selected_value)
    projector = selected.projector
    complement = gaussian.add(gaussian.identity(dimension), gaussian.scale(projector, -1))

    first_crossings = tuple(
        gaussian.scale(
            _sandwich(sector.projector, jet.first_derivative, projector),
            Fraction(1, 1) / (selected_value - sector.character[0]),
        )
        for sector in others
    )
    first_lower = _sum(first_crossings, dimension)
    first = gaussian.add(first_lower, gaussian.dagger(first_lower))

    source = gaussian.add(
        gaussian.scale(gaussian.bracket(jet.first_derivative, first), 2),
        gaussian.bracket(jet.second_derivative, projector),
    )
    second_crossings = tuple(
        gaussian.scale(
            _sandwich(sector.projector, source, projector),
            Fraction(1, 1) / (selected_value - sector.character[0]),
        )
        for sector in others
    )
    second_lower = _sum(second_crossings, dimension)
    first_squared = gaussian.multiply(first, first)
    second_diagonal = gaussian.add(
        gaussian.scale(_sandwich(projector, first_squared, projector), -2),
        gaussian.scale(_sandwich(complement, first_squared, complement), 2),
    )
    second = gaussian.add(
        gaussian.add(second_lower, gaussian.dagger(second_lower)), second_diagonal
    )
    canonical_transport = gaussian.bracket(first, projector)
    first_off_block = _sandwich(complement, first, projector)
    second_off_block = _sandwich(complement, second, projector)
    zero = gaussian.zero(dimension)
    checks = {
        "projector_is_hermitian": gaussian.is_hermitian(projector),
        "projector_is_idempotent": gaussian.multiply(projector, projector) == projector,
        "first_derivative_is_hermitian": gaussian.is_hermitian(first),
        "first_projector_law": first
        == gaussian.add(gaussian.multiply(first, projector), gaussian.multiply(projector, first)),
        "first_commutator_law": gaussian.add(
            gaussian.bracket(jet.value, first),
            gaussian.bracket(jet.first_derivative, projector),
        )
        == zero,
        "second_derivative_is_hermitian": gaussian.is_hermitian(second),
        "second_projector_law": second
        == gaussian.add(
            gaussian.add(
                gaussian.multiply(second, projector), gaussian.multiply(projector, second)
            ),
            gaussian.scale(first_squared, 2),
        ),
        "second_commutator_law": gaussian.add(gaussian.bracket(jet.value, second), source) == zero,
        "canonical_transport_is_skew": gaussian.dagger(canonical_transport)
        == gaussian.scale(canonical_transport, -1),
        "canonical_transport_recovers_first_jet": gaussian.bracket(canonical_transport, projector)
        == first,
        "first_arrow_is_off_block": gaussian.multiply(projector, first_off_block) == zero,
        "second_arrow_is_off_block": gaussian.multiply(projector, second_off_block) == zero,
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise ProjectorJetError("ProjectorJetResidual", f"construction fails at {failed}")
    admitted_jet = CoefficientJet(
        jet.value, jet.first_derivative, jet.second_derivative, selected_value
    )
    return SpectralProjectorJet(
        coefficient_jet=admitted_jet,
        spectrum=spectrum,
        spectral_gap=gap,
        cluster_multiplicity=selected.multiplicity,
        projector=projector,
        projector_first_derivative=first,
        projector_second_derivative=second,
        first_off_block_operator=first_off_block,
        second_off_block_operator=second_off_block,
        canonical_transport_generator=canonical_transport,
        rigid_transport=second == gaussian.bracket(canonical_transport, first),
        cost=ProjectorJetCost(
            carrier_dimension=dimension,
            spectral_sectors=len(algebra.sectors),
            factor_candidate_checks=algebra.factor_candidate_checks,
            complement_sylvester_blocks=len(others),
        ),
        checks=checks,
    )


def construct_rigid_mode_jet(
    model: IrreducibleModel, projector_jet: SpectralProjectorJet
) -> ModeBundleJet:
    if model.selected_projector != projector_jet.projector:
        raise ProjectorJetError(
            "ProjectorModelMismatch", "coefficient cluster differs from the selected G10 block"
        )
    if not projector_jet.rigid_transport:
        raise ProjectorJetError(
            "NonRigidProjectorJet",
            "second projector derivative is not constant-generator transport",
        )
    result = construct_mode_jet(model, projector_jet.canonical_transport_generator)
    if (
        result.projector_derivative != projector_jet.projector_first_derivative
        or gaussian.bracket(
            projector_jet.canonical_transport_generator, result.projector_derivative
        )
        != projector_jet.projector_second_derivative
    ):
        raise ProjectorJetError(
            "RigidModeJetResidual",
            "constructed G11 jet does not recover coefficient projector jets",
        )
    return result
