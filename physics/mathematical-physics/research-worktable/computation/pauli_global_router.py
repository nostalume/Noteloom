"""Analytic/topological promotion of the bilateral constant-field Pauli witness."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

from pauli_bilateral_router import discover_payload as discover_local_pauli
from problem_input import ProblemDocument, ProblemInputError, load_problem


class GlobalPauliObstruction(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def _fraction(value: object) -> Fraction:
    if isinstance(value, (bool, float)):
        raise GlobalPauliObstruction(
            "InvalidExactInput", "use integers or rational strings, not floats"
        )
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, str)):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as error:
            raise GlobalPauliObstruction(
                "InvalidExactInput", f"invalid rational value {value!r}"
            ) from error
    raise GlobalPauliObstruction("InvalidExactInput", f"invalid rational value {value!r}")


def _text(value: Fraction) -> str:
    return (
        str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    )


def _negative_exponential_upper(exponent: Fraction, terms: int = 8) -> Fraction:
    """Return a rational upper bound for exp(-exponent), exponent > 0."""

    partial = Fraction(1)
    term = Fraction(1)
    for order in range(1, terms + 1):
        term *= exponent / order
        partial += term
    return 1 / partial


def _inverse_sqrt_pi_beta_upper(beta: Fraction, scale: int = 10**6) -> Fraction:
    """Bound 1/(2 sqrt(pi beta)) above using pi > 3 and exact integer sqrt."""

    scaled_square = 3 * beta.numerator * scale * scale // beta.denominator
    lower_numerator = math.isqrt(scaled_square)
    if lower_numerator == 0:
        raise GlobalPauliObstruction(
            "ObservableScaleOutsideBudget",
            "inverse temperature is too small for the rational bound scale",
        )
    lower_sqrt = Fraction(lower_numerator, scale)
    return 1 / (2 * lower_sqrt)


def _load_local_problem(
    payload: dict[str, object], path: Path, maximum_level: int
) -> dict[str, object]:
    filename = payload.get("local_problem_file")
    if not isinstance(filename, str) or not filename:
        raise GlobalPauliObstruction(
            "MissingLocalBridge", "local_problem_file must name a bilateral Pauli ProblemSpec"
        )
    if Path(filename).name != filename:
        raise GlobalPauliObstruction(
            "InvalidLocalBridgePath", "local_problem_file must stay in the global input directory"
        )
    parent = path.resolve().parent
    local_path = (parent / filename).resolve()
    if local_path.parent != parent:
        raise GlobalPauliObstruction(
            "InvalidLocalBridgePath", "local_problem_file escaped the global input directory"
        )
    try:
        local_payload = json.loads(local_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise GlobalPauliObstruction("MissingLocalBridge", str(error)) from error
    if not isinstance(local_payload, dict):
        raise GlobalPauliObstruction(
            "MissingLocalBridge", "local Pauli ProblemSpec must be an object"
        )
    local_payload = dict(local_payload)
    local_payload["observable"] = {
        "kind": "spin_resolved_transverse_energy_channels",
        "maximum_orbital_level": maximum_level,
    }
    return local_payload


def _global_inputs(
    payload: dict[str, object],
) -> tuple[dict[str, object], dict[str, object], dict[str, object], int]:
    geometry = payload.get("global_geometry")
    domain = payload.get("domain_contract")
    observable = payload.get("observable")
    budget = payload.get("resource_budget")
    if not all(isinstance(value, dict) for value in (geometry, domain, observable, budget)):
        raise GlobalPauliObstruction(
            "InvalidGlobalProblem",
            "global_geometry, domain_contract, observable, and resource_budget must be objects",
        )
    assert isinstance(geometry, dict)
    assert isinstance(domain, dict)
    assert isinstance(observable, dict)
    assert isinstance(budget, dict)
    maximum_level = budget.get("maximum_landau_level")
    if (
        isinstance(maximum_level, bool)
        or not isinstance(maximum_level, int)
        or not 0 <= maximum_level <= 10000
    ):
        raise GlobalPauliObstruction(
            "InvalidBudget", "maximum_landau_level must be an integer from 0 through 10000"
        )
    return geometry, domain, observable, maximum_level


def _local_invariants(local_result: dict[str, object]) -> tuple[Fraction, int]:
    if local_result.get("outcome") != "exact":
        obstruction = local_result.get("obstruction", {})
        reason = (
            obstruction.get("reason", "the local bilateral bridge is not exact")
            if isinstance(obstruction, dict)
            else "the local bilateral bridge is not exact"
        )
        raise GlobalPauliObstruction("LocalBridgeObstruction", str(reason))
    candidates = local_result.get("candidates")
    decision = local_result.get("decision")
    if not isinstance(candidates, list) or not candidates or not isinstance(decision, dict):
        raise GlobalPauliObstruction(
            "LocalBridgeObstruction", "local bridge omitted its witness data"
        )
    first = candidates[0]
    if not isinstance(first, dict):
        raise GlobalPauliObstruction(
            "LocalBridgeObstruction", "local bridge candidate is malformed"
        )
    witness = first.get("witness")
    if not isinstance(witness, dict) or not isinstance(witness.get("reduced_object"), dict):
        raise GlobalPauliObstruction("LocalBridgeObstruction", "local reduced object is malformed")
    reduced = witness["reduced_object"]
    assert isinstance(reduced, dict)
    magnitude = _fraction(reduced.get("field_magnitude"))
    sign = decision.get("charge_sign")
    if sign not in (-1, 1):
        raise GlobalPauliObstruction(
            "LocalBridgeObstruction", "local charge orientation is missing"
        )
    assert isinstance(sign, int)
    return magnitude, sign


def _validate_geometry(geometry: dict[str, object]) -> Fraction:
    transverse = geometry.get("transverse")
    longitudinal = geometry.get("longitudinal")
    if not isinstance(transverse, dict) or not isinstance(longitudinal, dict):
        raise GlobalPauliObstruction(
            "UnsupportedGlobalGeometry", "transverse and longitudinal geometry must be objects"
        )
    if not (
        transverse.get("type") == "flat_torus"
        and transverse.get("bundle") == "hermitian_line_bundle_from_constant_curvature"
        and longitudinal.get("type") == "real_line"
        and longitudinal.get("fourier_convention") == "unnormalized_forward"
        and longitudinal.get("measure") == "dk/(2*pi)"
        and geometry.get("boundary") == "none"
    ):
        raise GlobalPauliObstruction(
            "UnsupportedGlobalGeometry",
            "the analytic bench requires a boundaryless magnetic flat torus times R with measure dk/(2*pi)",
        )
    area_over_2pi = _fraction(transverse.get("area_over_2pi"))
    if area_over_2pi <= 0:
        raise GlobalPauliObstruction("InvalidTorusArea", "area_over_2pi must be positive")
    return area_over_2pi


def _validate_domain(domain: dict[str, object]) -> None:
    expected = {
        "transverse": "bochner_friedrichs_on_smooth_bundle_sections",
        "longitudinal": "H2(R)",
        "tensor_sum": "self_adjoint_strongly_commuting_tensor_sum",
    }
    if any(domain.get(key) != value for key, value in expected.items()):
        raise GlobalPauliObstruction(
            "DomainContractObstruction",
            "the admitted self-adjoint realization is the Bochner/Friedrichs torus operator tensor H2(R)",
        )


def _observable_inputs(observable: dict[str, object]) -> tuple[Fraction, Fraction]:
    if observable.get("kind") != "heat_trace_per_unit_longitudinal_length":
        raise GlobalPauliObstruction(
            "UnsupportedObservable",
            "the global Pauli bench preserves heat trace per unit longitudinal length",
        )
    inverse_temperature = _fraction(observable.get("inverse_temperature"))
    tolerance = _fraction(observable.get("absolute_tolerance"))
    if inverse_temperature <= 0 or tolerance <= 0:
        raise GlobalPauliObstruction(
            "InvalidObservableScale", "inverse_temperature and absolute_tolerance must be positive"
        )
    return inverse_temperature, tolerance


def _analytic_witness(
    local_result: dict[str, object],
    field_magnitude: Fraction,
    charge_sign: int,
    area_over_2pi: Fraction,
    inverse_temperature: Fraction,
    tolerance: Fraction,
    maximum_level: int,
) -> dict[str, object]:
    chern = charge_sign * field_magnitude * area_over_2pi
    if chern.denominator != 1:
        raise GlobalPauliObstruction(
            "FluxQuantizationObstruction",
            f"charged flux b*s*Area/(2*pi)={_text(chern)} is not an integer Chern number",
        )
    chern_number = chern.numerator
    if chern_number == 0:
        raise GlobalPauliObstruction(
            "ZeroChernClass", "nonzero local curvature produced zero global flux"
        )
    multiplicity = abs(chern_number)

    beta = float(inverse_temperature)
    b_value = float(field_magnitude)
    q = math.exp(-2.0 * b_value * beta)
    longitudinal_density = 1.0 / (2.0 * math.sqrt(math.pi * beta))
    spin_sum = (1.0 + q) / (1.0 - q)
    numeric_value = multiplicity * longitudinal_density * spin_sum
    partial_sum = (
        multiplicity
        * longitudinal_density
        * (1.0 + q)
        * (1.0 - q ** (maximum_level + 1))
        / (1.0 - q)
    )
    exact_tail = (
        multiplicity * longitudinal_density * (1.0 + q) * q ** (maximum_level + 1) / (1.0 - q)
    )
    tolerance_value = float(tolerance)
    q_upper = _negative_exponential_upper(2 * field_magnitude * inverse_temperature)
    longitudinal_upper = _inverse_sqrt_pi_beta_upper(inverse_temperature)
    rigorous_tail_bound = (
        multiplicity
        * longitudinal_upper
        * (1 + q_upper)
        * q_upper ** (maximum_level + 1)
        / (1 - q_upper)
    )
    if rigorous_tail_bound > tolerance:
        raise GlobalPauliObstruction(
            "HeatTailBudgetExceeded",
            f"level budget gives rigorous tail bound {_text(rigorous_tail_bound)}, above tolerance {_text(tolerance)}",
        )

    local_coincidence = local_result.get("coincidence")
    local_passed = (
        isinstance(local_coincidence, dict) and local_coincidence.get("all_passed") is True
    )
    checks = {
        "local_bilateral_witness_exact": local_result.get("outcome") == "exact",
        "local_bilateral_coincidence": local_passed,
        "charged_flux_is_integral": chern.denominator == 1,
        "line_bundle_multiplicity_is_positive": multiplicity > 0,
        "magnetic_translation_irrep_has_chern_dimension": multiplicity == abs(chern_number),
        "fourier_measure_matches_declared_convention": True,
        "self_adjoint_tensor_domain_contract_admitted": True,
        "finite_level_audit_closes_heat_series": abs(numeric_value - partial_sum - exact_tail)
        < 1e-14,
        "heat_tail_within_requested_tolerance": rigorous_tail_bound <= tolerance,
    }
    return {
        "preserved_object": "heat trace per unit longitudinal length",
        "construction": "local bilateral witness -> integral Chern class -> magnetic-translation multiplicity -> Landau/Fourier direct integral",
        "topology": {
            "base": "T^2 x R",
            "charged_flux_over_2pi": _text(chern),
            "chern_number": chern_number,
            "landau_multiplicity": multiplicity,
            "charge_reversal": "complex-conjugates the line bundle and reverses c1",
        },
        "magnetic_translation_representation": {
            "group": f"finite Heisenberg central extension at level {multiplicity}",
            "dimension": multiplicity,
            "relations": [
                f"T1^{multiplicity}=T2^{multiplicity}=I",
                f"T1*T2=exp(2*pi*i/{chern_number})*T2*T1",
            ],
            "role": "multiplicity carrier, not an extra energy quantum number",
        },
        "direct_integral": {
            "carrier": f"integral_R^oplus direct_sum_n>=0 [(C^{multiplicity} tensor S_+)+(C^{multiplicity} tensor S_-)] dk/(2*pi)",
            "measure": "dk/(2*pi)",
            "reduced_operator": "multiplication by k^2+2bn on S_+ and k^2+2b(n+1) on S_-",
            "analysis": "torus Landau spectral projectors tensor unnormalized longitudinal Fourier transform",
            "synthesis": "sum Landau/spin multiplicities and integrate exp(ikz) dk/(2*pi)",
        },
        "domain": {
            "Hilbert_space": f"L2(T^2,L^(c1={chern_number})) tensor L2(R) tensor C^2",
            "core": "C_c^infinity(R; C^infinity(T^2,L^c1) tensor C^2)",
            "realization": "self-adjoint strongly commuting tensor sum of compact Bochner/Friedrichs and free longitudinal Laplacians",
            "boundary": "none",
        },
        "observable": {
            "inverse_temperature": _text(inverse_temperature),
            "exact_formula": f"{multiplicity}*coth({_text(field_magnitude)}*t)/(2*sqrt(pi*t))",
            "numeric_value": numeric_value,
            "finite_level_audit": {
                "maximum_landau_level": maximum_level,
                "partial_sum": partial_sum,
                "exact_tail": exact_tail,
                "tail_bound": float(rigorous_tail_bound),
                "tail_bound_proof": {
                    "exp_positive_Taylor_terms": 8,
                    "pi_strict_lower_bound": 3,
                    "sqrt_rational_scale": 1000000,
                    "arithmetic": "exact Fraction until final decimal rendering",
                },
                "requested_tolerance": tolerance_value,
            },
        },
        "maps": {
            "analysis_isometry": "Parseval on torus eigenspaces and Fourier-Plancherel on R",
            "synthesis_recovery": "orthogonal Landau sum followed by Fourier inversion",
        },
        "residuals": {"all_passed": all(checks.values()), "checks": checks},
        "error": {
            "exact_symbolic_observable": True,
            "finite_audit_absolute_error_bound": float(rigorous_tail_bound),
            "finite_audit_bound_arithmetic": "admission compares exact rationals; rendered decimal is informational",
        },
        "cost": {
            "topological_checks": 1,
            "generative_relations": 3,
            "finite_audit_channels": 2 * (maximum_level + 1),
            "closed_form_evaluation": "O(1)",
            "coordinate_eigenfunctions_constructed": 0,
            "baseline_3d_PDE_solve": "not executed; no runtime-dominance claim",
        },
        "theorem_contracts": {
            "torus": "self-adjoint Bochner Landau operator; |c1|-dimensional ground space; ladder spectrum and finite Heisenberg action",
            "longitudinal": "Fourier-Plancherel and inversion on L2(R)",
            "tensor_sum": "spectral theorem for strongly commuting self-adjoint tensor factors",
        },
    }


def _failure(
    payload: object,
    local_result: dict[str, object] | None,
    error: GlobalPauliObstruction,
) -> dict[str, object]:
    local_probes = local_result.get("probes", []) if isinstance(local_result, dict) else []
    local_candidates = local_result.get("candidates", []) if isinstance(local_result, dict) else []
    return {
        "schema": "reduction-decision/v1",
        "outcome": "unresolved" if error.kind == "HeatTailBudgetExceeded" else "obstructed",
        "request": {
            "problem_type": payload.get("schema", "unknown")
            if isinstance(payload, dict)
            else "unknown",
            "observable": "heat_trace_per_unit_longitudinal_length",
        },
        "probes": [
            *local_probes,
            {
                "route": "global-analytic-promotion",
                "applicable": False,
                "first_residual": error.kind,
                "reason": str(error),
            },
        ],
        "candidates": list(local_candidates),
        "coincidence": local_result.get("coincidence") if isinstance(local_result, dict) else None,
        "decision": {"selected_route": None, "reason": str(error)},
        "analytic_witness": None,
        "obstruction": {"kind": error.kind, "reason": str(error)},
        "human_card": {
            "result": "local reduction retained; global analytic promotion refused",
            "first_global_residual": error.kind,
            "reentry": "supply integral charged flux, the admitted self-adjoint domain, and sufficient observable budget",
        },
    }


def discover_document(document: ProblemDocument) -> dict[str, object]:
    payload: object = document.payload
    local_result: dict[str, object] | None = None
    try:
        input_path = document.path
        if not isinstance(payload, dict) or payload.get("schema") != "pauli-landau-global/v1":
            raise GlobalPauliObstruction(
                "UnsupportedProblemType", "expected pauli-landau-global/v1"
            )
        geometry, domain, observable, maximum_level = _global_inputs(payload)
        local_payload = _load_local_problem(payload, input_path, maximum_level)
        local_result = discover_local_pauli(local_payload)
        field_magnitude, charge_sign = _local_invariants(local_result)
        area_over_2pi = _validate_geometry(geometry)
        chern = charge_sign * field_magnitude * area_over_2pi
        if chern.denominator != 1:
            raise GlobalPauliObstruction(
                "FluxQuantizationObstruction",
                f"charged flux b*s*Area/(2*pi)={_text(chern)} is not an integer Chern number",
            )
        _validate_domain(domain)
        inverse_temperature, tolerance = _observable_inputs(observable)
        analytic = _analytic_witness(
            local_result,
            field_magnitude,
            charge_sign,
            area_over_2pi,
            inverse_temperature,
            tolerance,
            maximum_level,
        )
        local_probes = local_result["probes"]
        local_candidates = local_result["candidates"]
        assert isinstance(local_probes, list) and isinstance(local_candidates, list)
        return {
            "schema": "reduction-decision/v1",
            "outcome": "exact",
            "request": {
                "problem_type": payload["schema"],
                "observable": observable["kind"],
                "supplied_group_name": False,
                "supplied_gauge_potential": False,
            },
            "probes": [
                *local_probes,
                {
                    "route": "global-analytic-promotion",
                    "applicable": True,
                    "trigger": "integral charged flux, admitted tensor domain, and Fourier measure",
                    "first_residual": None,
                },
            ],
            "candidates": [
                *local_candidates,
                {"route": "global-landau-fourier", "outcome": "exact", "witness": analytic},
            ],
            "coincidence": {
                "status": "local_bilateral_then_global_exact",
                "all_passed": analytic["residuals"]["all_passed"],
                "local": local_result["coincidence"],
                "global_checks": analytic["residuals"]["checks"],
            },
            "decision": {
                "selected_route": "global-landau-fourier",
                "reason": "topology and domain promote the local channel algebra to a unitary direct integral",
            },
            "analytic_witness": analytic,
            "human_card": {
                "result": "exact theorem-backed analytic promotion",
                "primitive_global_datum": "integer charged flux (Chern number)",
                "constructed_multiplicity": analytic["topology"]["landau_multiplicity"],
                "measure": "dk/(2*pi)",
                "observable": analytic["observable"]["exact_formula"],
                "boundary": "flat magnetic T^2 times R, constant curvature, no boundary",
            },
            "not_certified": [
                "variable curvature, a physical boundary, or noncompact transverse geometry",
                "a runtime advantage over a specific discretized baseline",
                "automatic proof of the imported self-adjointness and completeness theorems",
                "interacting or nonlinear spinor systems",
            ],
        }
    except GlobalPauliObstruction as error:
        return _failure(payload, local_result, error)


def discover_problem(path: Path) -> dict[str, object]:
    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _failure(
            {},
            None,
            GlobalPauliObstruction("InvalidProblemSpec", str(error)),
        )
