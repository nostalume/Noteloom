"""Group-to-PDE covariance and Casimir construction from exact matrix seeds."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from adjoint_algebra import (
    AdjointMultiplicityObstruction,
    Matrix,
)
from adjoint_algebra import (
    add as _add,
)
from adjoint_algebra import (
    adjoint_matrices as _adjoint_matrices,
)
from adjoint_algebra import (
    bracket as _bracket,
)
from adjoint_algebra import (
    commutator_closure as _commutator_closure,
)
from adjoint_algebra import (
    coordinates as _coordinates,
)
from adjoint_algebra import (
    fraction as _fraction,
)
from adjoint_algebra import (
    identity as _identity,
)
from adjoint_algebra import (
    inverse as _inverse,
)
from adjoint_algebra import (
    jordan as _jordan,
)
from adjoint_algebra import (
    matrix as _matrix,
)
from adjoint_algebra import (
    matrix_sum as _matrix_sum,
)
from adjoint_algebra import (
    multiply as _multiply,
)
from adjoint_algebra import (
    pair as _pair,
)
from adjoint_algebra import (
    scalar_identity_value as _scalar_identity_value,
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
    transpose as _transpose,
)
from adjoint_algebra import (
    zero as _zero,
)
from linear_defect_compiler import (
    CandidateBracket,
    DefectBlock,
    DefectBudget,
    LinearMap,
    compile_defects,
)
from problem_input import ProblemDocument, ProblemInputError, load_problem


def _construct_symbol_covariance(payload: dict[str, object]) -> dict[str, object]:
    """Generate covariance derivations and their second-order scalar action."""

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
            "the symbol-covariance constructor is bounded to matrix sizes two and three",
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
        or matrix_size > maximum_matrix_size
        or maximum_closure_dimension <= 0
    ):
        raise AdjointMultiplicityObstruction(
            "InvalidBudget", "the matrix and closure budgets must admit the supplied seeds"
        )
    generators = [
        _matrix(value, matrix_size, f"coefficient_generators[{index}]")
        for index, value in enumerate(raw_generators)
    ]
    if any(_trace(value) != 0 for value in generators):
        raise AdjointMultiplicityObstruction(
            "NonTracelessCoefficientAlgebra",
            "the admitted symbol grammar requires traceless coefficient matrices",
        )
    closure, growth, bracket_candidates = _commutator_closure(generators, maximum_closure_dimension)
    closure_dimension = len(closure)
    expected_dimension = matrix_size * matrix_size - 1
    if closure_dimension != expected_dimension:
        raise AdjointMultiplicityObstruction(
            "IncompleteCoefficientAlgebra",
            f"commutator closure has dimension {closure_dimension}, not {expected_dimension}",
        )

    trace_gram: Matrix = tuple(tuple(_pair(left, right) for right in closure) for left in closure)
    trace_gram_inverse = _inverse(trace_gram)
    adjoint_actions = _adjoint_matrices(closure, trace_gram_inverse)
    bracket_table = tuple(
        tuple(_coordinates(closure, trace_gram_inverse, _bracket(left, right)) for right in closure)
        for left in closure
    )

    jet = payload.get("differential_jet")
    if not isinstance(jet, dict) or not (
        jet.get("kind") == "pairing_dual_square_of_generated_derivations"
        and jet.get("core") == "symmetric_algebra_of_coefficient_dual"
    ):
        raise AdjointMultiplicityObstruction(
            "UnsupportedDifferentialJet",
            "the bounded jet must square the pairing-dual generated derivations on the polynomial core",
        )
    pairing = jet.get("covariant_pairing")
    if not isinstance(pairing, dict):
        raise AdjointMultiplicityObstruction(
            "MissingPrincipalPairing", "the differential jet requires a covariant pairing"
        )
    pairing_scale = _fraction(pairing.get("scale"))
    if pairing_scale == 0:
        raise AdjointMultiplicityObstruction(
            "DegeneratePrincipalPairing", "the principal pairing scale must be nonzero"
        )
    if pairing.get("kind") == "matrix_trace":
        principal_pairing = _scale(trace_gram, pairing_scale)
    elif pairing.get("kind") == "coordinate_identity":
        principal_pairing = _scale(_identity(closure_dimension), pairing_scale)
    else:
        raise AdjointMultiplicityObstruction(
            "UnsupportedPrincipalPairing",
            "supported pairings are matrix_trace and coordinate_identity",
        )

    zero_on_closure = _zero(closure_dimension)
    pairing_residuals = [
        _add(
            _multiply(_transpose(action), principal_pairing),
            _multiply(principal_pairing, action),
        )
        for action in adjoint_actions
    ]
    pairing_defect = compile_defects(
        candidate_labels=tuple(f"ad-{index}" for index in range(closure_dimension)),
        blocks=(
            DefectBlock(
                name="principal-pairing-covariance",
                target_labels=tuple(
                    f"{row},{column}"
                    for row in range(closure_dimension)
                    for column in range(closure_dimension)
                ),
                columns=tuple(
                    tuple(value for row in residual for value in row)
                    for residual in pairing_residuals
                ),
            ),
        ),
        visible_action=LinearMap(
            name="adjoint-action-on-linear-coefficients",
            target_labels=tuple(
                f"{row},{column}"
                for row in range(closure_dimension)
                for column in range(closure_dimension)
            ),
            columns=tuple(
                tuple(value for row in action for value in row) for action in adjoint_actions
            ),
        ),
        bracket=CandidateBracket(name="generated-coefficient-bracket", table=bracket_table),
        budget=DefectBudget(
            closure_dimension,
            closure_dimension**2,
            maximum_bracket_checks=closure_dimension**3 + 4 * closure_dimension**2,
        ),
    )
    first_pairing_residual = next(
        (index for index, residual in enumerate(pairing_residuals) if residual != zero_on_closure),
        None,
    )
    if pairing_defect.kernel_dimension != closure_dimension:
        raise AdjointMultiplicityObstruction(
            "PrincipalSymbolCovarianceObstruction",
            "the supplied principal pairing is not invariant under generated derivation "
            f"{first_pairing_residual}",
        )
    if pairing_defect.outcome != "exact":
        raise AdjointMultiplicityObstruction(
            "CovarianceClosureObstruction",
            pairing_defect.obstruction_reason or "the covariance closure certificate failed",
        )

    representation_checks: list[bool] = []
    for left_index, left in enumerate(closure):
        for right_index, right in enumerate(closure):
            represented_bracket = _matrix_sum(
                [
                    _scale(action, coefficient)
                    for coefficient, action in zip(
                        bracket_table[left_index][right_index], adjoint_actions
                    )
                ],
                closure_dimension,
            )
            representation_checks.append(
                _bracket(adjoint_actions[left_index], adjoint_actions[right_index])
                == represented_bracket
            )
    if not all(representation_checks):
        raise AdjointMultiplicityObstruction(
            "CovarianceClosureObstruction",
            "the generated inner derivations failed the Lie representation law",
        )

    principal_pairing_inverse = _inverse(principal_pairing)
    casimir_terms = [
        _scale(
            _multiply(adjoint_actions[left], adjoint_actions[right]),
            principal_pairing_inverse[left][right],
        )
        for left in range(closure_dimension)
        for right in range(closure_dimension)
        if principal_pairing_inverse[left][right] != 0
    ]
    coefficient_action = _matrix_sum(casimir_terms, closure_dimension)
    derived_eigenvalue = _scalar_identity_value(coefficient_action)
    if derived_eigenvalue is None:
        raise AdjointMultiplicityObstruction(
            "CoefficientEigenmoduleObstruction",
            "the pairing-dual second-order action is not scalar on linear coefficients",
        )
    if derived_eigenvalue != matrix_size:
        raise AdjointMultiplicityObstruction(
            "DifferentialNormalizationMismatch",
            "the derived coefficient action does not match the forward normalized witness",
        )

    operator = payload.get("operator_family")
    if not isinstance(operator, dict) or not (
        operator.get("kind") == "natural_tensor_after_generated_second_order_operator"
        and operator.get("differential_order") == 2
    ):
        raise AdjointMultiplicityObstruction(
            "UnsupportedOperatorFamily",
            "the symbol bench requires the natural tensor family after the generated order-two action",
        )
    couplings = operator.get("reduced_couplings")
    if not isinstance(couplings, dict):
        raise AdjointMultiplicityObstruction(
            "MissingDynamics", "the operator family must supply its natural couplings"
        )
    antisymmetric_coupling = _fraction(couplings.get("antisymmetric_bracket"))
    symmetric_coupling = _fraction(couplings.get("symmetric_traceless_jordan"))
    observable = payload.get("observable")
    if not isinstance(observable, dict) or observable.get("kind") != (
        "ordered_and_exchange_reversed_reduced_pde_amplitudes"
    ):
        raise AdjointMultiplicityObstruction(
            "UnsupportedObservable", "the symbol bench preserves the exchange-paired amplitude"
        )
    if payload.get("equivalence") != "effective_lie_algebra_and_visible_witness":
        raise AdjointMultiplicityObstruction(
            "MissingEquivalencePolicy",
            "comparison is only at the effective algebra and visible witness",
        )
    preparation = payload.get("preparation")
    if not isinstance(preparation, dict):
        raise AdjointMultiplicityObstruction(
            "CarrierViolation", "preparation must supply operator, state, and probe matrices"
        )
    parameter = _matrix(
        preparation.get("operator_parameter"),
        matrix_size,
        "preparation.operator_parameter",
    )
    state = _matrix(
        preparation.get("state_parameter"),
        matrix_size,
        "preparation.state_parameter",
    )
    probe = _matrix(preparation.get("probe"), matrix_size, "preparation.probe")
    if any(_trace(value) != 0 for value in (parameter, state, probe)):
        raise AdjointMultiplicityObstruction(
            "CarrierViolation", "operator, state, and probe matrices must be traceless"
        )

    bracket = _bracket(parameter, state)
    jordan = _jordan(parameter, state)
    reverse_bracket = _bracket(state, parameter)
    reverse_jordan = _jordan(state, parameter)
    source_factor = Fraction(1) + derived_eigenvalue
    effective_antisymmetric = source_factor * antisymmetric_coupling
    jordan_identically_zero = all(
        _jordan(left, right) == _zero(matrix_size) for left in closure for right in closure
    )
    effective_symmetric = (
        Fraction(0) if jordan_identically_zero else source_factor * symmetric_coupling
    )
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
    group_channel_dimension = 1 if jordan_identically_zero else 2
    visible_channel_dimension = int(antisymmetric_part != 0) + int(symmetric_part != 0)
    checks = {
        "coefficient_closure_is_full_traceless_space": closure_dimension == expected_dimension,
        "generated_derivations_form_a_lie_representation": all(representation_checks),
        "principal_pairing_is_covariant": first_pairing_residual is None,
        "pairing_dual_square_is_scalar_on_linear_coefficients": derived_eigenvalue is not None,
        "coefficient_eigenvalue_is_internally_derived": "coefficient_differential_action"
        not in payload,
        "forward_normalization_coincides": derived_eigenvalue == matrix_size,
        "exchange_parity_is_exact": reverse_bracket == _scale(bracket, Fraction(-1))
        and reverse_jordan == jordan,
        "observable_recovery_is_exact": ordered == antisymmetric_part + symmetric_part,
    }
    if not all(checks.values()):
        raise ArithmeticError("constructed symbol-covariance witness failed an exact certificate")

    algebra_name = f"sl_{matrix_size}(C)"
    witness = {
        "preserved_object": "exchange-paired reduced amplitude of the generated polynomial-core PDE",
        "construction": "matrix coefficient closure -> inner derivations -> invariant pairing-dual square",
        "reduced_object": {
            "kind": "adjoint-linear coefficient eigenmodule with natural reduced operator",
            "effective_complex_lie_algebra": algebra_name,
            "dimension": closure_dimension,
            "outer_multiplicity_space_dimension": group_channel_dimension,
        },
        "maps": {
            "covariance": "A -> X_A, X_A f(x)=d f_x([A,x])",
            "synthesis": "S(Y)=ell_Y with ell_Y(x)=g(Y,x)",
            "analysis": "A(ell_Y)=Y by nondegeneracy of g",
            "differential": "Delta_g=sum g^(ij) X_(B_i) X_(B_j)",
            "observable": "O_Z(W)=tr(ZW)",
        },
        "residuals": {"all_passed": True, "checks": checks},
        "error": {
            "kind": "exact on the polynomial linear-coefficient core",
            "bound": 0,
        },
        "cost": {
            "input_seed_matrices": len(generators),
            "closure_growth": growth,
            "commutator_candidates_tested": bracket_candidates,
            "generated_covariance_derivations": closure_dimension,
            "defect_kernel_dimension": pairing_defect.kernel_dimension,
            "defect_residual_rank": pairing_defect.ledger[0].residual_rank,
            "defect_closure_status": pairing_defect.closure_status,
            "effective_derivation_dimension": pairing_defect.effective_dimension,
            "defect_bracket_checks": pairing_defect.bracket_checks,
            "lie_representation_residuals_tested": closure_dimension**2,
            "stored_structure_constant_table": False,
            "coordinate_chart_expansion": False,
            "carrier_dimension_reduction": 0,
        },
        "validity": {
            "matrix_sizes": [2, 3],
            "coefficient_domain": "exact rational traceless matrices",
            "core": "symmetric algebra of the generated coefficient dual",
            "analytic_completion": "not supplied",
        },
    }
    return {
        "schema": "reduction-decision/v1",
        "outcome": "exact",
        "request": {
            "problem_type": payload["schema"],
            "observable": observable["kind"],
            "supplied_group_name": False,
            "supplied_lie_algebra_name": False,
            "supplied_covariance_generators": False,
            "supplied_coefficient_eigenvalue": False,
            "supplied_reduced_output": False,
        },
        "probes": [
            {
                "route": "symbol-fiber-to-covariance",
                "applicable": True,
                "trigger": "exact matrix product and nondegenerate invariant principal pairing",
                "first_residual": None,
            },
            {
                "route": "analytic-global-promotion",
                "applicable": False,
                "trigger": "the polynomial core supplies no Hilbert completion or global group",
                "first_residual": "AnalyticCompletionUnresolved",
            },
        ],
        "candidates": [
            {
                "route": "generated-symbol-covariance",
                "outcome": "exact",
                "witness": witness,
            }
        ],
        "coincidence": {
            "status": "exact_symbol_covariance_and_visible_witness_coincidence",
            "all_passed": True,
            "checks": checks,
            "same_observable": observable_result,
        },
        "decision": {
            "selected_route": "generated-symbol-covariance",
            "reason": "the invariant principal pairing turns generated inner derivations into a scalar second-order action",
            "effective_complex_lie_algebra": algebra_name,
            "covariance_generator_dimension": closure_dimension,
            "derived_coefficient_eigenvalue": _text(derived_eigenvalue),
            "differential_source_factor": _text(source_factor),
            "group_channel_dimension": group_channel_dimension,
            "visible_channel_dimension": visible_channel_dimension,
            "observable": observable_result,
            "global_group": "unresolved",
        },
        "analytic_witness": {
            "carrier": f"Sym({algebra_name}^*)",
            "core": "polynomial functions on the effective coefficient space",
            "operator_order": 2,
            "coefficient_action": f"Delta_g ell_Y={_text(derived_eigenvalue)} ell_Y",
            "status": "exact algebraic differential core; no closed Hilbert realization claimed",
        },
        "human_card": {
            "result": f"the symbol fiber generates {closure_dimension} covariance derivations and eigenvalue {_text(derived_eigenvalue)}",
            "primitive_objects": "seed matrices, commutator, trace pairing, pairing-dual square",
            "avoided_catalogue": "no group, roots, weights, covariance generators, Casimir label, or eigenvalue supplied",
            "boundary": "matrix sizes two/three and polynomial core; analytic/global promotion unresolved",
        },
        "not_certified": [
            "a closed self-adjoint Hilbert-space realization",
            "a compact real form or global group action",
            "arbitrary polynomial coefficient jets",
            "outer derivations or non-semisimple coefficient algebras",
        ],
    }


def _obstruction(payload: object, error: AdjointMultiplicityObstruction) -> dict[str, object]:
    return {
        "schema": "reduction-decision/v1",
        "outcome": "obstructed",
        "request": {
            "problem_type": payload.get("schema", "unknown")
            if isinstance(payload, dict)
            else "unknown"
        },
        "probes": [],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None, "reason": str(error)},
        "obstruction": {"kind": error.kind, "reason": str(error)},
        "human_card": {"result": "obstructed", "why": str(error)},
    }


def discover_payload(payload: object) -> dict[str, object]:
    try:
        if not isinstance(payload, dict):
            raise AdjointMultiplicityObstruction(
                "InvalidProblemSpec", "problem specification must be a JSON object"
            )
        return _construct_symbol_covariance(payload)
    except AdjointMultiplicityObstruction as error:
        return _obstruction(payload, error)


def discover_document(document: ProblemDocument) -> dict[str, object]:
    return discover_payload(document.payload)


def discover_problem(path: Path) -> dict[str, object]:
    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _obstruction({}, AdjointMultiplicityObstruction("InvalidProblemSpec", str(error)))
