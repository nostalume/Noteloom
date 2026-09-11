"""Public reduction-decision adapter for the G19 polynomial active module."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import sympy as sp

from exact_polynomial_matrix import (
    fraction_text,
    serialize_matrix,
    serialize_polynomial,
    term_count,
)
from gaussian_reachable_module import Apply
from polynomial_active_module import (
    IntervalAttempt,
    PolynomialReductionError,
    RationalMatrix,
    ReductionWitness,
    construct_reduction,
)
from polynomial_active_module_input import SCHEMA, PolynomialInputError, parse
from problem_input import ProblemDocument, ProblemInputError, load_problem

ROUTE = "polynomial-active-module"


def _rational_matrix(value: RationalMatrix, coordinates):
    return {
        "numerator": serialize_matrix(value.numerator, coordinates),
        "denominator": serialize_polynomial(value.denominator, coordinates),
    }


def _serialize_witness(witness: ReductionWitness, coordinates, maximum_terms):
    rational_values = (
        witness.left_inverse,
        witness.projector,
        witness.preparation_coordinates,
        *witness.reduced_coefficients.values(),
        *witness.residual_coefficients.values(),
    )
    matrices = (
        witness.raw_frame,
        witness.frame,
        witness.gram,
        witness.compressed_effect,
        *(value.numerator for value in rational_values),
        sp.Matrix([value.denominator for value in rational_values]),
        sp.Matrix([witness.rank_chart.pivot_minor, witness.rank_chart.norm_square]),
    )
    output_terms = sum(term_count(matrix, coordinates) for matrix in matrices)
    if output_terms > maximum_terms:
        raise PolynomialReductionError(
            "OutputTermBudgetExceeded",
            "serialized witness exceeds the output-term budget",
            {"observed_terms": output_terms, "maximum_terms": maximum_terms},
        )

    def coefficient_map(values):
        return {
            ",".join(map(str, alpha)): _rational_matrix(value, coordinates)
            for alpha, value in values.items()
        }

    chart = witness.rank_chart
    cost = asdict(witness.cost)
    cost["serialized_polynomial_terms"] = output_terms
    return {
        "ambient_dimension": witness.ambient_dimension,
        "active_dimension": witness.active_dimension,
        "provenance": [
            {"kind": "Seed"}
            if not isinstance(node, Apply)
            else {
                "kind": "Apply",
                "parent_index": node.parent_index,
                "coefficient_index": node.generator_index,
            }
            for node in witness.provenance
        ],
        "raw_frame": serialize_matrix(witness.raw_frame, coordinates),
        "frame": serialize_matrix(witness.frame, coordinates),
        "gram": serialize_matrix(witness.gram, coordinates),
        "left_inverse": _rational_matrix(witness.left_inverse, coordinates),
        "projector": _rational_matrix(witness.projector, coordinates),
        "reduced_coefficients": coefficient_map(witness.reduced_coefficients),
        "residual_coefficients": coefficient_map(witness.residual_coefficients),
        "preparation_coordinates": _rational_matrix(witness.preparation_coordinates, coordinates),
        "compressed_effect": serialize_matrix(witness.compressed_effect, coordinates),
        "rank_chart": {
            "pivot_rows": list(chart.pivot_rows),
            "pivot_transform": serialize_matrix(chart.pivot_transform, coordinates),
            "certified_box": [[fraction_text(a), fraction_text(b)] for a, b in chart.certified_box],
            "pivot_minor": serialize_polynomial(chart.pivot_minor, coordinates),
            "norm_square": serialize_polynomial(chart.norm_square, coordinates),
            "interval_attempts": [_attempt(value) for value in chart.attempts],
        },
        "leakage_is_zero": witness.leakage_is_zero,
        "domain_contract": witness.domain_contract,
        "cost": cost,
        "checks": witness.checks,
    }


def _attempt(value: IntervalAttempt) -> dict[str, object]:
    def text(item):
        return (
            str(item.numerator) if item.denominator == 1 else f"{item.numerator}/{item.denominator}"
        )

    return {
        "box": [[text(lower), text(upper)] for lower, upper in value.box],
        "enclosure": [text(value.enclosure[0]), text(value.enclosure[1])],
    }


def _failure(payload: object, kind: str, reason: str, details=None) -> dict[str, object]:
    unresolved = kind in {
        "RankRegionUnresolved",
        "PolynomialTermBudgetExceeded",
        "OutputTermBudgetExceeded",
    }
    outcome = "unresolved" if unresolved else "obstructed"
    bounded_details = dict(details or {})
    if "attempts" in bounded_details:
        bounded_details["attempts"] = [_attempt(value) for value in bounded_details["attempts"]]
    problem_type = payload.get("schema", "unknown") if isinstance(payload, dict) else "unknown"
    return {
        "schema": "reduction-decision/v1",
        "outcome": outcome,
        "request": {"problem_type": problem_type, "supplied_group_name": False},
        "probes": [{"route": ROUTE, "outcome": outcome, "first_residual": kind}],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None, "reason": reason},
        "obstruction": {"kind": kind, "reason": reason, "details": bounded_details},
        "human_card": {"result": outcome, "why": reason},
    }


def discover_payload(payload: object) -> dict[str, object]:
    try:
        problem = parse(payload)
        witness = construct_reduction(problem)
        serialized = _serialize_witness(
            witness, problem.coordinates, problem.budget.maximum_output_terms
        )
        if witness.leakage_is_zero:
            outcome, obstruction = "exact", None
            reason = "the provenance frame is closed under every product-rule coefficient"
        elif problem.requested_capability == "decompose-with-residual":
            outcome, obstruction = "formal", None
            reason = "the exact decomposition retains nonzero off-module leakage"
        else:
            result = _failure(
                payload,
                "CoefficientOrDerivativeEscape",
                "exact closed reduction was requested but the constructed residual is nonzero",
                {"witness": serialized},
            )
            return result
        return {
            "schema": "reduction-decision/v1",
            "outcome": outcome,
            "request": {
                "problem_type": SCHEMA,
                "supplied_group_name": False,
                "supplied_frame": False,
                "supplied_projector": False,
                "supplied_reduced_operator": False,
            },
            "probes": [{"route": ROUTE, "outcome": outcome, "first_residual": obstruction}],
            "candidates": [{"route": ROUTE, "outcome": outcome, "witness": serialized}],
            "coincidence": {
                "status": "exact_product_rule_reconstruction",
                "all_passed": all(witness.checks.values()),
                "checks": witness.checks,
            },
            "decision": {
                "selected_route": ROUTE,
                "reason": reason,
                "active_dimension": witness.active_dimension,
                "leakage_is_zero": witness.leakage_is_zero,
                "global_group": "not constructed",
            },
            "human_card": {
                "result": outcome,
                "primitive_objects": "polynomial coefficients, preparation, base point, and rational box",
                "construction": "reachable DAG -> local frame -> product-rule reduction and leakage",
                "boundary": "one exact local chart; no boundary descent or global Lie integration",
            },
        }
    except (PolynomialInputError, PolynomialReductionError) as error:
        return _failure(payload, error.kind, str(error), getattr(error, "details", None))


def discover_document(document: ProblemDocument) -> dict[str, object]:
    return discover_payload(document.payload)


def discover_problem(path: Path) -> dict[str, object]:
    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _failure({}, "InvalidProblemSpec", str(error))
