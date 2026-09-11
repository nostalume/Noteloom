"""Typed exact admission for the G19 polynomial active-module schema."""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction

import sympy as sp

from exact_polynomial_matrix import ExactPolynomialError, fraction, polynomial_array, term_count
from linear_defect_compiler import DefectBudget
from problem_input import ProblemDocument

SCHEMA = "polynomial-active-module/v1"
LIFT_CAPABILITY = "construct-local-infinitesimal-symmetry"


class PolynomialInputError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class PolynomialBudget:
    maximum_carrier_dimension: int
    maximum_active_dimension: int
    maximum_derivative_order: int
    maximum_polynomial_terms: int
    maximum_rank_refinements: int
    maximum_output_terms: int


@dataclass(frozen=True)
class OperatorTerm:
    derivative: tuple[int, ...]
    coefficient: sp.ImmutableMatrix


@dataclass(frozen=True)
class PolynomialProblem:
    coordinates: tuple[sp.Symbol, ...]
    operator_terms: tuple[OperatorTerm, ...]
    preparation: sp.ImmutableMatrix
    effect: sp.ImmutableMatrix
    base_point: tuple[Fraction, ...]
    region: tuple[tuple[Fraction, Fraction], ...]
    requested_capability: str
    budget: PolynomialBudget
    domain_contract: str


@dataclass(frozen=True)
class PolynomialLiftRequest:
    problem: PolynomialProblem
    budget: DefectBudget


def _powers(value: object, dimension: int, name: str) -> tuple[int, ...]:
    if (
        not isinstance(value, list)
        or len(value) != dimension
        or any(isinstance(item, bool) or not isinstance(item, int) or item < 0 for item in value)
    ):
        raise PolynomialInputError(
            "InvalidPolynomialPowers", f"{name} must contain {dimension} nonnegative integers"
        )
    return tuple(value)


def _array(value, coordinates, *, vector, name):
    try:
        return polynomial_array(value, coordinates, vector=vector, name=name)
    except ExactPolynomialError as error:
        raise PolynomialInputError("InvalidExactInput", str(error)) from error


def _budget(value: object) -> PolynomialBudget:
    names = (
        "maximum_carrier_dimension",
        "maximum_active_dimension",
        "maximum_derivative_order",
        "maximum_polynomial_terms",
        "maximum_rank_refinements",
        "maximum_output_terms",
    )
    if not isinstance(value, dict):
        raise PolynomialInputError("MissingResourceBudget", "resource_budget must be an object")
    values = tuple(value.get(name) for name in names)
    if any(isinstance(item, bool) or not isinstance(item, int) or item <= 0 for item in values):
        raise PolynomialInputError(
            "InvalidResourceBudget", "all six resource bounds must be positive integers"
        )
    return PolynomialBudget(*values)


def _lift_budget(value: object) -> DefectBudget:
    if not isinstance(value, dict):
        raise PolynomialInputError(
            "MissingResidualLieBudget", "resource_budget.residual_lie must be an object"
        )
    candidate = value.get("maximum_candidate_dimension")
    residual = value.get("maximum_residual_coordinates")
    if any(
        isinstance(item, bool) or not isinstance(item, int) or item <= 0
        for item in (candidate, residual)
    ):
        raise PolynomialInputError(
            "InvalidResidualLieBudget", "residual Lie bounds must be positive integers"
        )
    return DefectBudget(candidate, residual)


def parse(payload: object) -> PolynomialProblem | PolynomialLiftRequest:
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise PolynomialInputError("UnsupportedProblemType", f"expected {SCHEMA}")
    raw_names = payload.get("coordinates")
    if (
        not isinstance(raw_names, list)
        or not raw_names
        or any(
            not isinstance(name, str) or re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name) is None
            for name in raw_names
        )
        or len(set(raw_names)) != len(raw_names)
    ):
        raise PolynomialInputError(
            "InvalidCoordinates", "coordinates must be unique identifier strings"
        )
    coordinates = tuple(sp.Symbol(name, real=True) for name in raw_names)
    raw_budget = payload.get("resource_budget")
    budget = _budget(raw_budget)
    raw_terms = payload.get("operator_terms")
    if not isinstance(raw_terms, list) or not raw_terms:
        raise PolynomialInputError("MissingOperator", "operator_terms must be a nonempty list")
    combined: dict[tuple[int, ...], sp.Matrix] = {}
    for index, raw in enumerate(raw_terms):
        if not isinstance(raw, dict):
            raise PolynomialInputError(
                "InvalidOperator", f"operator_terms[{index}] must be an object"
            )
        derivative = _powers(
            raw.get("derivative"), len(coordinates), f"operator_terms[{index}].derivative"
        )
        if sum(derivative) > budget.maximum_derivative_order:
            raise PolynomialInputError(
                "DerivativeOrderBudgetExceeded", "operator derivative order exceeds budget"
            )
        coefficient = _array(
            raw.get("coefficient"),
            coordinates,
            vector=False,
            name=f"operator_terms[{index}].coefficient",
        )
        combined[derivative] = combined.get(derivative, sp.zeros(*coefficient.shape)) + coefficient
    operator_terms = tuple(
        OperatorTerm(alpha, sp.ImmutableMatrix(matrix.applyfunc(sp.expand)))
        for alpha, matrix in sorted(combined.items())
        if any(entry != 0 for entry in matrix)
    )
    if not operator_terms or any(
        term.coefficient.rows != term.coefficient.cols for term in operator_terms
    ):
        raise PolynomialInputError(
            "InvalidOperatorShape", "operator coefficients must be nonzero square matrices"
        )
    carrier = operator_terms[0].coefficient.rows
    if carrier > budget.maximum_carrier_dimension or any(
        term.coefficient.rows != carrier for term in operator_terms
    ):
        raise PolynomialInputError(
            "CarrierBudgetExceeded", "operator carrier dimensions differ or exceed budget"
        )
    preparation = _array(payload.get("preparation"), coordinates, vector=True, name="preparation")
    effect = _array(payload.get("effect"), coordinates, vector=False, name="effect")
    if preparation.shape != (carrier, 1) or effect.shape != (carrier, carrier):
        raise PolynomialInputError(
            "CarrierDimensionMismatch", "preparation/effect must match the operator carrier"
        )
    if any(
        sp.expand(effect[row, column] - sp.conjugate(effect[column, row])) != 0
        for row in range(carrier)
        for column in range(carrier)
    ):
        raise PolynomialInputError(
            "NonHermitianEffect", "effect must be Hermitian as a polynomial matrix"
        )
    base_raw, region_raw = payload.get("base_point"), payload.get("region")
    if (
        not isinstance(base_raw, list)
        or len(base_raw) != len(coordinates)
        or not isinstance(region_raw, list)
        or len(region_raw) != len(coordinates)
    ):
        raise PolynomialInputError(
            "InvalidRegion", "base_point and region must match coordinate arity"
        )
    try:
        base_point = tuple(
            fraction(value, f"base_point[{index}]") for index, value in enumerate(base_raw)
        )
    except ExactPolynomialError as error:
        raise PolynomialInputError("InvalidExactInput", str(error)) from error
    region: list[tuple[Fraction, Fraction]] = []
    for index, value in enumerate(region_raw):
        if not isinstance(value, list) or len(value) != 2:
            raise PolynomialInputError("InvalidRegion", f"region[{index}] must be [lower, upper]")
        try:
            lower, upper = (fraction(item, f"region[{index}]") for item in value)
        except ExactPolynomialError as error:
            raise PolynomialInputError("InvalidExactInput", str(error)) from error
        if lower >= upper or not lower <= base_point[index] <= upper:
            raise PolynomialInputError(
                "InvalidRegion", "region must be nondegenerate and contain the base point"
            )
        region.append((lower, upper))
    domain = payload.get("domain")
    if (
        not isinstance(domain, dict)
        or domain.get("core") != "compact-supported-smooth"
        or domain.get("boundary") != "none"
    ):
        raise PolynomialInputError(
            "DomainContractMismatch",
            "v1 admits only compact-supported smooth sections without boundary trace",
        )
    capability = payload.get("requested_capability")
    if capability not in {
        "decompose-with-residual",
        "exact-closed-reduction",
        LIFT_CAPABILITY,
    }:
        raise PolynomialInputError("UnsupportedCapability", "unsupported reduction capability")
    terms = sum(term_count(term.coefficient, coordinates) for term in operator_terms)
    terms += term_count(preparation, coordinates) + term_count(effect, coordinates)
    if terms > budget.maximum_polynomial_terms:
        raise PolynomialInputError(
            "PolynomialTermBudgetExceeded", "canonical input terms exceed budget"
        )
    substitutions = dict(zip(coordinates, base_point, strict=True))
    if all(entry.subs(substitutions) == 0 for entry in preparation):
        raise PolynomialInputError(
            "ZeroPreparation", "preparation must be nonzero at the base point"
        )
    problem = PolynomialProblem(
        coordinates,
        operator_terms,
        preparation,
        effect,
        base_point,
        tuple(region),
        capability,
        budget,
        "C_c^infinity(region; C^n), boundary none",
    )
    if capability == LIFT_CAPABILITY:
        assert isinstance(raw_budget, dict)
        return PolynomialLiftRequest(problem, _lift_budget(raw_budget.get("residual_lie")))
    return problem


def admit_document(document: ProblemDocument) -> PolynomialProblem | PolynomialLiftRequest:
    return parse(document.payload)
