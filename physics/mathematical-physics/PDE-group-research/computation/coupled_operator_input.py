"""Typed admission for the bounded coupled Pauli full-operator schema."""

from __future__ import annotations

from dataclasses import dataclass

import exact_gaussian_matrix as gaussian
from adjoint_algebra import Matrix as RealMatrix
from adjoint_algebra import scale as real_scale
from adjoint_algebra import transpose as real_transpose
from coupled_relation_input import (
    CoupledRelationObstruction,
    parse_real_matrix,
    parse_relation_input,
)
from linear_defect_compiler import DefectBudget

SCHEMA = "coupled-operator-covariance/v1"


class OperatorInputError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class CoupledOperatorInput:
    metric: RealMatrix
    links: tuple[gaussian.ComplexMatrix, ...]
    capabilities: tuple[str, ...]
    curvature: RealMatrix
    first_order: tuple[gaussian.ComplexMatrix, ...]
    zero_order: gaussian.ComplexMatrix
    relation_budget: DefectBudget
    operator_budget: DefectBudget
    domain_witness: dict[str, object]
    maximum_level: int | None


def _budget(value: object, name: str) -> DefectBudget:
    if not isinstance(value, dict):
        raise OperatorInputError("MissingResourceBudget", f"{name} budget must be an object")
    try:
        return DefectBudget(
            int(value["maximum_candidate_dimension"]),
            int(value["maximum_residual_coordinates"]),
            int(value["maximum_bracket_checks"]),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise OperatorInputError(
            "InvalidResourceBudget", f"{name} budget requires three integer bounds"
        ) from error


def _matrix(value: object, name: str) -> gaussian.ComplexMatrix:
    try:
        return gaussian.matrix(value, name)
    except (ValueError, ZeroDivisionError) as error:
        raise OperatorInputError("InvalidExactInput", str(error)) from error


def _domain(
    payload: dict[str, object], base_dimension: int, fiber_dimension: int
) -> dict[str, object]:
    value = payload.get("domain_contract")
    expected = {
        "kind": "boundaryless-gauge-covariant-schwartz",
        "core": f"Schwartz(R^{base_dimension},C^{fiber_dimension})",
        "boundary": "none",
    }
    if not isinstance(value, dict) or any(value.get(key) != item for key, item in expected.items()):
        raise OperatorInputError(
            "DomainContractMismatch",
            "G5 admits only the boundaryless gauge-covariant Schwartz common core",
        )
    return {
        "kind": "matched-theorem-contract",
        "core": expected["core"],
        "scope": "common-core covariance; not self-adjoint completion",
        "checks": {
            "boundaryless": True,
            "linear_base_actions_preserve_schwartz": True,
            "constant_fiber_actions_preserve_schwartz": True,
            "curvature_stabilizer_has_gauge_covariant_lift": True,
        },
    }


def _maximum_level(payload: dict[str, object]) -> int | None:
    value = payload.get("observable")
    if value is None:
        return None
    maximum = value.get("maximum_orbital_level") if isinstance(value, dict) else None
    if (
        not isinstance(value, dict)
        or value.get("kind") != "spin_resolved_transverse_energy_channels"
        or isinstance(maximum, bool)
        or not isinstance(maximum, int)
        or not 0 <= maximum <= 32
    ):
        raise OperatorInputError(
            "UnsupportedObservable",
            "observable must request spin-resolved channels through a level from 0 to 32",
        )
    return maximum


def _operator(
    payload: dict[str, object], base_dimension: int, fiber_dimension: int
) -> tuple[RealMatrix, tuple[gaussian.ComplexMatrix, ...], gaussian.ComplexMatrix]:
    raw = payload.get("operator")
    if (
        not isinstance(raw, dict)
        or raw.get("kind") != "constant-curvature-covariant-laplacian"
        or raw.get("order") != 2
    ):
        raise OperatorInputError(
            "UnsupportedOperator",
            "operator must be an order-two constant-curvature covariant Laplacian",
        )
    try:
        curvature = parse_real_matrix(raw.get("curvature_two_form"), "curvature_two_form")
    except CoupledRelationObstruction as error:
        raise OperatorInputError(error.kind, str(error)) from error
    if len(curvature) != base_dimension or real_transpose(curvature) != real_scale(curvature, -1):
        raise OperatorInputError(
            "CurvatureRelationViolation",
            "curvature_two_form must be skew and match the base dimension",
        )
    if not any(entry for row in curvature for entry in row):
        raise OperatorInputError("ZeroCurvature", "curvature_two_form must be nonzero")
    raw_first = raw.get("first_order_matrices")
    if not isinstance(raw_first, list) or len(raw_first) != base_dimension:
        raise OperatorInputError(
            "InvalidOperatorCoefficients",
            "first_order_matrices must contain one matrix per base dimension",
        )
    first_order = tuple(
        _matrix(value, f"first_order_matrices[{index}]") for index, value in enumerate(raw_first)
    )
    zero_order = _matrix(raw.get("zero_order_matrix"), "zero_order_matrix")
    if any(len(value) != fiber_dimension for value in (*first_order, zero_order)):
        raise OperatorInputError(
            "InvalidOperatorCoefficients", "all lower-order matrices must match the fiber"
        )
    if any(not gaussian.is_hermitian(value) for value in (*first_order, zero_order)):
        raise OperatorInputError(
            "HermitianRelationViolation", "all lower-order coefficient matrices must be Hermitian"
        )
    return curvature, first_order, zero_order


def parse(payload: object) -> CoupledOperatorInput:
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise OperatorInputError("UnsupportedProblemType", f"expected {SCHEMA}")
    budgets = payload.get("resource_budget")
    if not isinstance(budgets, dict):
        raise OperatorInputError("MissingResourceBudget", "resource_budget must be an object")
    relation_payload = dict(payload)
    relation_payload["resource_budget"] = budgets.get("relation")
    try:
        metric, links, capabilities, relation_budget = parse_relation_input(relation_payload)
    except CoupledRelationObstruction as error:
        raise OperatorInputError(error.kind, str(error)) from error
    curvature, first_order, zero_order = _operator(payload, len(metric), len(links[0]))
    return CoupledOperatorInput(
        metric=metric,
        links=links,
        capabilities=capabilities,
        curvature=curvature,
        first_order=first_order,
        zero_order=zero_order,
        relation_budget=relation_budget,
        operator_budget=_budget(budgets.get("operator"), "operator"),
        domain_witness=_domain(payload, len(metric), len(links[0])),
        maximum_level=_maximum_level(payload),
    )
