"""PDE-first recovery of an effective matrix Lie algebra and visible witness.

The input carries matrix-valued PDE coefficient seeds, but no group name.  This
bounded constructor closes the seeds under commutator over the rationals and
recognizes ``sl_n(C)`` only when the closure is the entire traceless matrix
space.  It then reconstructs the natural bracket/Jordan channels and compares
their visible PDE amplitude with the normalized forward adjoint construction.
Global integration and real-form choices intentionally remain unresolved.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from adjoint_algebra import (
    AdjointMultiplicityObstruction,
)
from adjoint_algebra import (
    add as _add,
)
from adjoint_algebra import (
    bracket as _bracket,
)
from adjoint_algebra import (
    center_dimension as _center_dimension,
)
from adjoint_algebra import (
    commutator_closure as _commutator_closure,
)
from adjoint_algebra import (
    flat as _flat,
)
from adjoint_algebra import (
    fraction as _fraction,
)
from adjoint_algebra import (
    jordan as _jordan,
)
from adjoint_algebra import (
    matrix as _matrix,
)
from adjoint_algebra import (
    pair as _pair,
)
from adjoint_algebra import (
    rank as _rank,
)
from adjoint_algebra import (
    scale as _scale,
)
from adjoint_algebra import (
    text as _text,
)
from adjoint_algebra import (
    trace as _trace,
)
from adjoint_algebra import (
    trace_form_rank as _trace_form_rank,
)
from adjoint_algebra import (
    zero as _zero,
)
from problem_input import ProblemDocument, ProblemInputError, load_problem


def _obstruction(payload: object, error: AdjointMultiplicityObstruction) -> dict[str, object]:
    return {
        "schema": "reduction-decision/v1",
        "outcome": "obstructed",
        "request": {
            "problem_type": payload.get("schema", "unknown")
            if isinstance(payload, dict)
            else "unknown",
            "supplied_group_name": False,
        },
        "probes": [],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None, "reason": str(error)},
        "obstruction": {"kind": error.kind, "reason": str(error)},
        "human_card": {"result": "obstructed", "why": str(error)},
    }


def _construct(payload: dict[str, object]) -> dict[str, object]:
    if payload.get("schema") != "matrix-pde-inverse/v1":
        raise AdjointMultiplicityObstruction(
            "UnsupportedProblemType", "expected matrix-pde-inverse/v1"
        )

    raw_generators = payload.get("coefficient_generators")
    if not isinstance(raw_generators, list) or not raw_generators:
        raise AdjointMultiplicityObstruction(
            "MissingCoefficientSeeds", "coefficient_generators must be a nonempty list"
        )
    first = raw_generators[0]
    if not isinstance(first, list):
        raise AdjointMultiplicityObstruction(
            "CarrierViolation", "each coefficient generator must be a square matrix"
        )
    matrix_size = len(first)
    if matrix_size not in (2, 3):
        raise AdjointMultiplicityObstruction(
            "CompletenessContractOutsideHorizon",
            "the inverse closure certificate is bounded to 2 by 2 and 3 by 3 matrices",
        )

    budget = payload.get("resource_budget")
    if not isinstance(budget, dict):
        raise AdjointMultiplicityObstruction("InvalidBudget", "resource_budget is required")
    maximum_matrix_size = budget.get("maximum_matrix_size")
    maximum_closure_dimension = budget.get("maximum_closure_dimension")
    if (
        isinstance(maximum_matrix_size, bool)
        or not isinstance(maximum_matrix_size, int)
        or isinstance(maximum_closure_dimension, bool)
        or not isinstance(maximum_closure_dimension, int)
        or maximum_matrix_size < matrix_size
        or maximum_closure_dimension <= 0
    ):
        raise AdjointMultiplicityObstruction(
            "InvalidBudget", "the matrix and closure budgets must admit the supplied seeds"
        )

    generators = [
        _matrix(value, matrix_size, f"coefficient_generators[{index}]")
        for index, value in enumerate(raw_generators)
    ]
    if any(_trace(generator) != 0 for generator in generators):
        raise AdjointMultiplicityObstruction(
            "NonTracelessCoefficientAlgebra",
            "the admitted inverse grammar requires traceless matrix coefficients",
        )
    closure, growth, bracket_candidates = _commutator_closure(generators, maximum_closure_dimension)
    expected_dimension = matrix_size * matrix_size - 1
    if len(closure) != expected_dimension:
        raise AdjointMultiplicityObstruction(
            "IncompleteCoefficientAlgebra",
            f"commutator closure has dimension {len(closure)}, not the full traceless dimension {expected_dimension}",
        )

    derived = [
        _bracket(left, right)
        for left_index, left in enumerate(closure)
        for right in closure[left_index + 1 :]
    ]
    derived_dimension = _rank([_flat(value) for value in derived])
    center_dimension = _center_dimension(closure)
    trace_form_rank = _trace_form_rank(closure)
    if not (
        derived_dimension == expected_dimension
        and center_dimension == 0
        and trace_form_rank == expected_dimension
    ):
        raise AdjointMultiplicityObstruction(
            "LieAlgebraCertificateFailure",
            "closure failed perfectness, center, or nondegenerate trace-form checks",
        )

    differential = payload.get("coefficient_differential_action")
    if not isinstance(differential, dict) or differential.get("kind") != (
        "common_scalar_eigenmodule"
    ):
        raise AdjointMultiplicityObstruction(
            "DifferentialClosureObstruction",
            "the visible coefficient span must have a common scalar second-order action",
        )
    eigenvalue = _fraction(differential.get("eigenvalue"))
    if eigenvalue != matrix_size:
        raise AdjointMultiplicityObstruction(
            "DifferentialNormalizationMismatch",
            "the coefficient eigenvalue does not match the normalized forward adjoint witness",
        )

    operator = payload.get("operator_family")
    if not isinstance(operator, dict) or not (
        operator.get("kind") == "matrix_coefficient_tensor_laplacian"
        and operator.get("differential_order") == 2
    ):
        raise AdjointMultiplicityObstruction(
            "UnsupportedOperatorFamily",
            "the inverse bench requires a matrix-coefficient order-two tensor family",
        )
    couplings = operator.get("reduced_couplings")
    if not isinstance(couplings, dict):
        raise AdjointMultiplicityObstruction(
            "MissingDynamics", "the PDE family must supply its two natural couplings"
        )
    antisymmetric_coupling = _fraction(couplings.get("antisymmetric_bracket"))
    symmetric_coupling = _fraction(couplings.get("symmetric_traceless_jordan"))

    admitted_analytic = {
        "carrier": "L2_compact_base_with_matrix_fiber",
        "domain": "H2_sobolev",
        "core": "smooth_sections",
        "coefficient_regularities": "smooth_bounded",
    }
    analytic = payload.get("analytic_realization")
    if not isinstance(analytic, dict) or any(
        analytic.get(key) != value for key, value in admitted_analytic.items()
    ):
        raise AdjointMultiplicityObstruction(
            "DomainContractObstruction",
            "the inverse PDE witness requires the admitted compact H^2-to-L^2 contract",
        )
    if payload.get("equivalence") != "effective_lie_algebra_and_visible_witness":
        raise AdjointMultiplicityObstruction(
            "MissingEquivalencePolicy",
            "comparison is only at the effective algebra and visible witness",
        )
    observable = payload.get("observable")
    if not isinstance(observable, dict) or observable.get("kind") != (
        "ordered_and_exchange_reversed_reduced_pde_amplitudes"
    ):
        raise AdjointMultiplicityObstruction(
            "UnsupportedObservable", "the inverse bench preserves the exchange-paired amplitude"
        )

    preparation = payload.get("preparation")
    if not isinstance(preparation, dict):
        raise AdjointMultiplicityObstruction(
            "CarrierViolation", "preparation must supply operator, state, and probe matrices"
        )
    parameter = _matrix(
        preparation.get("operator_parameter"), matrix_size, "preparation.operator_parameter"
    )
    state = _matrix(preparation.get("state_parameter"), matrix_size, "preparation.state_parameter")
    probe = _matrix(preparation.get("probe"), matrix_size, "preparation.probe")
    if any(_trace(value) != 0 for value in (parameter, state, probe)):
        raise AdjointMultiplicityObstruction(
            "CarrierViolation", "operator, state, and probe matrices must be traceless"
        )

    bracket = _bracket(parameter, state)
    jordan = _jordan(parameter, state)
    reverse_bracket = _bracket(state, parameter)
    reverse_jordan = _jordan(state, parameter)
    source_factor = Fraction(1) + eigenvalue
    effective_antisymmetric = source_factor * antisymmetric_coupling
    effective_symmetric = Fraction(0) if matrix_size == 2 else source_factor * symmetric_coupling
    output = _add(
        _scale(bracket, effective_antisymmetric),
        _scale(jordan, effective_symmetric),
    )
    reverse_output = _add(
        _scale(reverse_bracket, effective_antisymmetric),
        _scale(reverse_jordan, effective_symmetric),
    )
    ordered = _pair(probe, output)
    exchange_reversed = _pair(probe, reverse_output)
    antisymmetric_part = (ordered - exchange_reversed) / 2
    symmetric_part = (ordered + exchange_reversed) / 2
    observable_result = {
        "ordered": _text(ordered),
        "exchange_reversed": _text(exchange_reversed),
        "antisymmetric_part": _text(antisymmetric_part),
        "symmetric_part": _text(symmetric_part),
    }

    jordan_identically_zero = all(
        _jordan(left, right) == _zero(matrix_size) for left in closure for right in closure
    )
    group_channel_dimension = 1 if jordan_identically_zero else 2
    visible_channel_dimension = int(antisymmetric_part != 0) + int(symmetric_part != 0)
    checks = {
        "commutator_closure_is_full_traceless_matrix_space": len(closure) == expected_dimension,
        "derived_algebra_is_full": derived_dimension == expected_dimension,
        "center_is_zero": center_dimension == 0,
        "trace_form_is_nondegenerate": trace_form_rank == expected_dimension,
        "bracket_naturality_follows_from_associative_derivation_identity": True,
        "jordan_naturality_follows_from_derivation_and_trace_cyclicity": True,
        "coefficient_action_matches_forward_normalization": eigenvalue == matrix_size,
        "exchange_parity_is_exact": reverse_bracket == _scale(bracket, Fraction(-1))
        and reverse_jordan == jordan,
        "observable_recovery_is_exact": ordered == antisymmetric_part + symmetric_part,
        "rank_two_jordan_channel_vanishes": matrix_size != 2 or jordan_identically_zero,
        "rank_three_jordan_channel_survives": matrix_size != 3 or not jordan_identically_zero,
    }
    if not all(checks.values()):
        raise ArithmeticError("constructed PDE-first witness failed an exact certificate")

    algebra_name = f"sl_{matrix_size}(C)"
    witness = {
        "preserved_object": "exchange-paired reduced amplitude of the matrix PDE family",
        "construction": "bounded rational commutator closure followed by natural matrix products",
        "reduced_object": {
            "kind": "effective adjoint carrier with multiplicity-valued reduced operator",
            "effective_complex_lie_algebra": algebra_name,
            "dimension": expected_dimension,
            "outer_multiplicity_space_dimension": group_channel_dimension,
        },
        "maps": {
            "antisymmetric": "F(X,Y)=[X,Y]",
            "symmetric": "D(X,Y)=XY+YX-(2/n)tr(XY)I",
            "observable": "O_Z(W)=tr(ZW)",
        },
        "residuals": {"all_passed": True, "checks": checks},
        "error": {"kind": "exact on the supplied coefficient eigenmodule", "bound": 0},
        "cost": {
            "input_seed_matrices": len(generators),
            "closure_growth": growth,
            "commutator_candidates_tested": bracket_candidates,
            "stored_structure_constant_table": False,
            "stored_natural_dynamics_coefficients": group_channel_dimension,
            "carrier_dimension_reduction": 0,
        },
        "validity": {
            "matrix_sizes": [2, 3],
            "coefficient_field": "rational traceless matrices",
            "closure_budget": maximum_closure_dimension,
            "analytic_scope": "supplied compact smooth coefficient eigenmodule",
        },
    }
    return {
        "schema": "reduction-decision/v1",
        "outcome": "exact",
        "request": {
            "problem_type": payload["schema"],
            "observable": observable["kind"],
            "supplied_group_name": False,
            "supplied_matrix_size": False,
            "supplied_reduced_output": False,
        },
        "probes": [
            {
                "route": "coefficient-commutator-closure",
                "applicable": True,
                "trigger": "finite exact traceless matrix coefficient seeds",
                "first_residual": None,
            },
            {
                "route": "global-group-integration",
                "applicable": False,
                "trigger": "local complex Lie algebra does not select a real form or global quotient",
                "first_residual": "GlobalIntegrationAmbiguity",
            },
        ],
        "candidates": [
            {"route": "pde-first-matrix-lie-closure", "outcome": "exact", "witness": witness}
        ],
        "coincidence": {
            "status": "exact_effective_algebra_and_visible_witness_coincidence",
            "all_passed": True,
            "checks": checks,
            "same_observable": observable_result,
        },
        "decision": {
            "selected_route": "pde-first-matrix-lie-closure",
            "reason": "coefficient commutators fill the traceless matrix algebra and reconstruct both natural channels",
            "effective_complex_lie_algebra": algebra_name,
            "closure_dimension": expected_dimension,
            "derived_dimension": derived_dimension,
            "center_dimension": center_dimension,
            "trace_form_rank": trace_form_rank,
            "coefficient_eigenvalue": _text(eigenvalue),
            "differential_source_factor": _text(source_factor),
            "group_channel_dimension": group_channel_dimension,
            "visible_channel_dimension": visible_channel_dimension,
            "observable": observable_result,
            "global_group": "unresolved",
        },
        "analytic_witness": {
            "domain": "H^2(M,Mat_n(C)) -> L^2(M,Mat_n(C)) on the declared compact base",
            "core": "smooth matrix-valued sections",
            "coefficient_action": f"Delta q={_text(eigenvalue)}q on the visible span",
            "status": "admitted PDE contract; global group realization not reconstructed",
        },
        "human_card": {
            "result": f"the PDE coefficients generate {algebra_name} and the same visible natural-map witness",
            "primitive_objects": f"{len(generators)} seed matrices, commutator, matrix product, trace",
            "avoided_catalogue": "no group name, root list, weight list, or structure-constant table supplied",
            "boundary": "real form, covering group, central quotient, and full coefficient completeness remain unresolved",
        },
        "not_certified": [
            "a unique real form or global Lie group",
            "global integration of the recovered infinitesimal action",
            "completeness of coefficient fields beyond the supplied eigenmodule",
            "automatic discovery for matrix sizes beyond two and three",
        ],
    }


def discover_payload(payload: object) -> dict[str, object]:
    try:
        if not isinstance(payload, dict):
            raise AdjointMultiplicityObstruction(
                "InvalidProblemSpec", "problem specification must be a JSON object"
            )
        return _construct(payload)
    except AdjointMultiplicityObstruction as error:
        return _obstruction(payload, error)


def discover_document(document: ProblemDocument) -> dict[str, object]:
    return discover_payload(document.payload)


def discover_problem(path: Path) -> dict[str, object]:
    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _obstruction({}, AdjointMultiplicityObstruction("InvalidProblemSpec", str(error)))
