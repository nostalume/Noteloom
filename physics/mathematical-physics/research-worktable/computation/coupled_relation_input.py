"""Shared exact admission for coupled metric-carrier relation problems."""

from __future__ import annotations

import exact_gaussian_matrix as gaussian
from adjoint_algebra import Matrix as RealMatrix
from adjoint_algebra import inverse as real_inverse
from adjoint_algebra import transpose as real_transpose
from linear_defect_compiler import DefectBudget

CAPABILITY = "metric-clifford-link"


class CoupledRelationObstruction(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def parse_real_matrix(value: object, name: str) -> RealMatrix:
    if not isinstance(value, list) or not value or any(not isinstance(row, list) for row in value):
        raise CoupledRelationObstruction("InvalidRelationInput", f"{name} must be a square matrix")
    dimension = len(value)
    if any(len(row) != dimension for row in value):
        raise CoupledRelationObstruction("InvalidRelationInput", f"{name} must be a square matrix")
    try:
        return tuple(tuple(gaussian.rational(entry) for entry in row) for row in value)
    except (ValueError, ZeroDivisionError) as error:
        raise CoupledRelationObstruction("InvalidExactInput", str(error)) from error


def _budget(payload: dict[str, object]) -> DefectBudget:
    value = payload.get("resource_budget")
    if not isinstance(value, dict):
        raise CoupledRelationObstruction(
            "MissingResourceBudget", "resource_budget must be an object"
        )
    try:
        return DefectBudget(
            int(value["maximum_candidate_dimension"]),
            int(value["maximum_residual_coordinates"]),
            int(value["maximum_bracket_checks"]),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise CoupledRelationObstruction(
            "InvalidResourceBudget", "resource_budget requires three integer bounds"
        ) from error


def parse_relation_input(
    payload: dict[str, object],
) -> tuple[
    RealMatrix,
    tuple[gaussian.ComplexMatrix, ...],
    tuple[str, ...],
    DefectBudget,
]:
    metric = parse_real_matrix(payload.get("base_metric"), "base_metric")
    if metric != real_transpose(metric):
        raise CoupledRelationObstruction("MetricRelationViolation", "base_metric is not symmetric")
    try:
        real_inverse(metric)
    except ValueError as error:
        raise CoupledRelationObstruction(
            "MetricRelationViolation", "base_metric is degenerate"
        ) from error
    raw_links = payload.get("link_matrices")
    if not isinstance(raw_links, list) or len(raw_links) != len(metric):
        raise CoupledRelationObstruction(
            "InvalidRelationInput", "link_matrices must contain one matrix per base dimension"
        )
    try:
        links = tuple(
            gaussian.matrix(value, f"link_matrices[{index}]")
            for index, value in enumerate(raw_links)
        )
    except (ValueError, ZeroDivisionError) as error:
        raise CoupledRelationObstruction("InvalidExactInput", str(error)) from error
    fiber_dimension = len(links[0])
    if any(len(link) != fiber_dimension for link in links):
        raise CoupledRelationObstruction(
            "InvalidRelationInput", "all link matrices must have one common fiber dimension"
        )
    if any(not gaussian.is_hermitian(link) for link in links):
        raise CoupledRelationObstruction(
            "HermitianRelationViolation", "every link matrix must be Hermitian"
        )
    raw_capabilities = payload.get("required_capabilities", [])
    if not isinstance(raw_capabilities, list) or any(
        not isinstance(item, str) for item in raw_capabilities
    ):
        raise CoupledRelationObstruction(
            "InvalidRelationInput", "required_capabilities must be a list of strings"
        )
    capabilities = tuple(raw_capabilities)
    unsupported = tuple(item for item in capabilities if item != CAPABILITY)
    if unsupported:
        raise CoupledRelationObstruction(
            "UnsupportedRelationCapability", f"unsupported capabilities: {', '.join(unsupported)}"
        )
    return metric, links, capabilities, _budget(payload)
