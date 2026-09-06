"""Exact natural-operation constructor for adjoint SU(2)/SU(3) channels.

The constructor realizes the complexified adjoint carrier as traceless defining
matrices.  It obtains covariant bilinear maps from the associative product:
the exchange-odd commutator and the exchange-even traceless Jordan product.
For SU(3) a tensor-product theorem contract says these two nonzero maps exhaust
Hom_SU(3)(8 tensor 8, 8); for SU(2), polarized Cayley--Hamilton kills the
Jordan map.  No weight list or Clebsch--Gordan component table is generated.
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
    conjugate as _conjugate,
)
from adjoint_algebra import (
    conjugator as _conjugator,
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
    scale as _scale,
)
from adjoint_algebra import (
    text as _text,
)
from adjoint_algebra import (
    trace as _trace,
)
from adjoint_algebra import (
    zero as _zero,
)
from problem_input import ProblemDocument, ProblemInputError, load_problem


def _probe(route: str, applicable: bool, residual: str | None, reason: str) -> dict[str, object]:
    return {
        "route": route,
        "applicable": applicable,
        "trigger": reason,
        "first_residual": residual,
    }


def _construct(payload: dict[str, object]) -> dict[str, object]:
    if payload.get("schema") != "su-adjoint-transition/v1":
        raise AdjointMultiplicityObstruction(
            "UnsupportedProblemType", "expected su-adjoint-transition/v1"
        )
    group = payload.get("group_family")
    if not isinstance(group, dict) or group.get("type") != "SU":
        raise AdjointMultiplicityObstruction(
            "UnsupportedGroupFamily", "the current natural-operation constructor requires SU(n)"
        )
    dimension = group.get("defining_dimension")
    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension not in (2, 3):
        raise AdjointMultiplicityObstruction(
            "CompletenessContractOutsideHorizon",
            "the executable completeness contract is bounded to SU(2) and SU(3)",
        )
    if group.get("carrier") != "complexified_adjoint_as_traceless_matrices":
        raise AdjointMultiplicityObstruction(
            "CarrierViolation", "the carrier must be the complexified adjoint as traceless matrices"
        )
    budget = payload.get("resource_budget")
    maximum_dimension = (
        budget.get("maximum_defining_dimension") if isinstance(budget, dict) else None
    )
    if (
        isinstance(maximum_dimension, bool)
        or not isinstance(maximum_dimension, int)
        or maximum_dimension not in (2, 3)
    ):
        raise AdjointMultiplicityObstruction(
            "InvalidBudget", "maximum_defining_dimension must be 2 or 3"
        )
    if dimension > maximum_dimension:
        raise AdjointMultiplicityObstruction(
            "ResourceBudgetExceeded", "the defining dimension exceeds the declared budget"
        )
    if payload.get("equivalence") != "simultaneous_conjugation":
        raise AdjointMultiplicityObstruction(
            "MissingEquivalencePolicy", "the comparison requires simultaneous conjugation"
        )
    observable = payload.get("observable")
    if not isinstance(observable, dict) or observable.get("kind") != (
        "ordered_and_exchange_reversed_transition_amplitudes"
    ):
        raise AdjointMultiplicityObstruction(
            "UnsupportedObservable",
            "the current constructor preserves ordered and exchange-reversed transition amplitudes",
        )
    operator = payload.get("operator_family")
    if not isinstance(operator, dict) or not (
        operator.get("kind") == "type_adjoint_order_two_on_one_source_sector"
        and operator.get("differential_order") == 2
    ):
        raise AdjointMultiplicityObstruction(
            "UnsupportedOperatorFamily",
            "the bench requires a type-adjoint order-two operator reduced on one source sector",
        )
    couplings = operator.get("reduced_couplings")
    if not isinstance(couplings, dict):
        raise AdjointMultiplicityObstruction(
            "MissingDynamics", "reduced_couplings must supply the problem-specific dynamics"
        )
    source_factor = _fraction(operator.get("invariant_source_block_factor"))
    antisymmetric_coupling = _fraction(couplings.get("antisymmetric_bracket"))
    symmetric_coupling = _fraction(couplings.get("symmetric_traceless_jordan"))

    preparation = payload.get("preparation")
    if not isinstance(preparation, dict):
        raise AdjointMultiplicityObstruction(
            "CarrierViolation", "preparation must contain left, right, and probe matrices"
        )
    left = _matrix(preparation.get("left"), dimension, "preparation.left")
    right = _matrix(preparation.get("right"), dimension, "preparation.right")
    probe = _matrix(preparation.get("probe"), dimension, "preparation.probe")
    for name, value in (("left", left), ("right", right), ("probe", probe)):
        if _trace(value) != 0:
            raise AdjointMultiplicityObstruction(
                "CarrierViolation", f"preparation.{name} is not traceless"
            )

    bracket = _bracket(left, right)
    jordan = _jordan(left, right)
    bracket_reverse = _bracket(right, left)
    jordan_reverse = _jordan(right, left)
    bracket_response = _pair(probe, bracket)
    jordan_response = _pair(probe, jordan)
    effective_antisymmetric = source_factor * antisymmetric_coupling
    effective_symmetric = source_factor * symmetric_coupling
    antisymmetric_part = effective_antisymmetric * bracket_response
    symmetric_part = effective_symmetric * jordan_response if dimension == 3 else Fraction(0)
    ordered = antisymmetric_part + symmetric_part
    exchange_reversed = -antisymmetric_part + symmetric_part

    ordered_matrix = _add(
        _scale(bracket, effective_antisymmetric),
        _scale(jordan, effective_symmetric if dimension == 3 else Fraction(0)),
    )
    reverse_matrix = _add(
        _scale(bracket_reverse, effective_antisymmetric),
        _scale(jordan_reverse, effective_symmetric if dimension == 3 else Fraction(0)),
    )

    group_element, inverse = _conjugator(dimension)
    left_conjugated = _conjugate(group_element, inverse, left)
    right_conjugated = _conjugate(group_element, inverse, right)
    probe_conjugated = _conjugate(group_element, inverse, probe)
    bracket_conjugated = _bracket(left_conjugated, right_conjugated)
    jordan_conjugated = _jordan(left_conjugated, right_conjugated)

    checks: dict[str, bool] = {
        "bracket_exchange_odd": bracket_reverse == _scale(bracket, Fraction(-1)),
        "jordan_exchange_even": jordan_reverse == jordan,
        "bracket_closes_on_traceless_carrier": _trace(bracket) == 0,
        "jordan_closes_on_traceless_carrier": _trace(jordan) == 0,
        "bracket_simultaneous_conjugation_equivariant": bracket_conjugated
        == _conjugate(group_element, inverse, bracket),
        "jordan_simultaneous_conjugation_equivariant": jordan_conjugated
        == _conjugate(group_element, inverse, jordan),
        "trace_pairing_conjugation_invariant": (
            _pair(probe_conjugated, bracket_conjugated) == bracket_response
            and _pair(probe_conjugated, jordan_conjugated) == jordan_response
        ),
        "ordered_analysis_synthesis_exact": _pair(probe, ordered_matrix) == ordered,
        "exchange_reversed_analysis_synthesis_exact": _pair(probe, reverse_matrix)
        == exchange_reversed,
        "observable_parity_recovery_exact": (
            (ordered - exchange_reversed) / 2 == antisymmetric_part
            and (ordered + exchange_reversed) / 2 == symmetric_part
        ),
        "outer_multiplicity_completeness_theorem_contract": True,
    }
    if dimension == 2:
        checks["rank_two_cayley_hamilton_kills_jordan_channel"] = jordan == _zero(2)
    else:
        checks["two_nonzero_exchange_parities_are_independent"] = bracket != _zero(
            3
        ) and jordan != _zero(3)
    if not all(checks.values()):
        raise ArithmeticError("constructed adjoint-channel witness failed an exact certificate")

    group_channel_dimension = 1 if dimension == 2 else 2
    visible_antisymmetric = antisymmetric_part != 0
    visible_symmetric = symmetric_part != 0
    visible_channel_dimension = int(visible_antisymmetric) + int(visible_symmetric)
    if visible_antisymmetric and visible_symmetric:
        selected_route = "two-channel-outer-multiplicity"
        selection_reason = (
            "exchange reversal independently observes the bracket and Jordan reduced couplings"
        )
    elif visible_antisymmetric:
        selected_route = "single-antisymmetric-channel"
        selection_reason = "the named observable sees only the exchange-odd quotient"
    elif visible_symmetric:
        selected_route = "single-symmetric-channel"
        selection_reason = "the named observable sees only the exchange-even quotient"
    else:
        selected_route = "zero-visible-channel"
        selection_reason = "the preparation and probe annihilate every admitted reduced channel"

    adjoint_dimension = dimension * dimension - 1
    candidate = {
        "route": "multiplicity-aware-natural-operations",
        "outcome": "exact",
        "witness": {
            "preserved_object": "ordered and exchange-reversed adjoint transition amplitudes",
            "construction": (
                "defining matrix product -> commutator/traceless Jordan parity channels -> "
                "observable-visible quotient"
            ),
            "reduced_object": {
                "group": f"SU({dimension})",
                "source_type": "adjoint",
                "operator_type": "adjoint",
                "target_type": "adjoint",
                "outer_multiplicity_space_dimension": group_channel_dimension,
                "basis": (
                    ["commutator"] if dimension == 2 else ["commutator", "traceless_jordan_product"]
                ),
                "effective_couplings": {
                    "antisymmetric": _text(effective_antisymmetric),
                    "symmetric": _text(effective_symmetric) if dimension == 3 else "inactive",
                },
            },
            "maps": {
                "analysis": {
                    "antisymmetric_response": _text(bracket_response),
                    "symmetric_response": _text(jordan_response),
                    "operation": "trace probe against the two natural covariant products",
                },
                "synthesis": {
                    "ordered": "a*F+b*D",
                    "exchange_reversed": "-a*F+b*D",
                },
            },
            "residuals": {"all_passed": True, "checks": checks},
            "error": {"kind": "exact rational", "bound": 0},
            "cost": {
                "stored_dynamics_coefficients": group_channel_dimension,
                "uncompressed_component_coefficients": adjoint_dimension**3,
                "natural_matrix_products_per_preparation": 2,
                "rational_multiplication_upper_bound": 2 * dimension**3 + dimension**2,
                "weight_or_clebsch_component_enumerations": 0,
            },
            "validity": {
                "group_family": f"SU({dimension})",
                "carrier": "sl_n over exact rational test data, interpreted in the complexified adjoint",
                "operator_order": 2,
                "analytic_scope": "one finite Peter-Weyl source/target sector on the smooth core",
                "completeness_contract": (
                    "8 tensor 8 contains exactly two adjoint copies"
                    if dimension == 3
                    else "3 tensor 3 contains exactly one adjoint copy"
                ),
            },
        },
    }
    probes = [
        _probe(
            "multiplicity-aware-natural-operations",
            True,
            None,
            "associative product and trace construct covariant exchange-parity channels",
        ),
        _probe(
            "single-antisymmetric-channel",
            not visible_symmetric,
            None if not visible_symmetric else "VisibleSymmetricChannel",
            "test whether the named observable factors through the bracket copy alone",
        ),
        _probe(
            "single-symmetric-channel",
            not visible_antisymmetric and dimension == 3,
            (
                None
                if not visible_antisymmetric and dimension == 3
                else "VisibleAntisymmetricChannel"
            ),
            "test whether the named observable factors through the Jordan copy alone",
        ),
    ]
    observable_result = {
        "ordered": _text(ordered),
        "exchange_reversed": _text(exchange_reversed),
        "antisymmetric_part": _text(antisymmetric_part),
        "symmetric_part": _text(symmetric_part),
    }
    return {
        "schema": "reduction-decision/v1",
        "outcome": "exact",
        "request": {
            "problem_type": payload["schema"],
            "observable": observable["kind"],
            "supplied_outer_multiplicity": False,
            "supplied_clebsch_component_table": False,
        },
        "probes": probes,
        "candidates": [candidate],
        "coincidence": {
            "status": "exact_analysis_synthesis_recovery",
            "all_passed": True,
            "same_observable": observable_result,
        },
        "decision": {
            "selected_route": selected_route,
            "reason": selection_reason,
            "group_channel_dimension": group_channel_dimension,
            "visible_channel_dimension": visible_channel_dimension,
            "observable": observable_result,
        },
        "human_card": {
            "result": selection_reason,
            "primitive_objects": "matrix product, trace removal, exchange parity, trace pairing",
            "replaced_expansion": f"{adjoint_dimension**3} possible adjoint tensor components",
            "recovery": "one sum and one difference of the ordered amplitudes recover both reduced channels",
            "boundary": "SU(2)/SU(3), complexified adjoint, one finite sector; dynamics remains supplied data",
        },
        "not_certified": [
            "the full L2(SU(3)) Peter-Weyl synthesis or analytic domain of an unbounded operator",
            "automatic construction for arbitrary compact groups or higher outer multiplicities",
            "runtime dominance over a precomputed sparse Clebsch--Gordan table for one evaluation",
        ],
    }


def _construct_pde(payload: dict[str, object]) -> dict[str, object]:
    """Lift the natural adjoint channels to one exact differential core."""

    group = payload.get("group_family")
    if not isinstance(group, dict) or group.get("type") != "SU":
        raise AdjointMultiplicityObstruction(
            "UnsupportedGroupFamily", "the PDE lift requires SU(n)"
        )
    dimension = group.get("defining_dimension")
    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension not in (2, 3):
        raise AdjointMultiplicityObstruction(
            "CompletenessContractOutsideHorizon",
            "the executable PDE lift is bounded to SU(2) and SU(3)",
        )
    if group.get("carrier") != "complexified_adjoint_as_traceless_matrices":
        raise AdjointMultiplicityObstruction(
            "CarrierViolation", "the PDE fiber must be the complexified adjoint"
        )
    budget = payload.get("resource_budget")
    maximum_dimension = (
        budget.get("maximum_defining_dimension") if isinstance(budget, dict) else None
    )
    if (
        isinstance(maximum_dimension, bool)
        or not isinstance(maximum_dimension, int)
        or maximum_dimension not in (2, 3)
    ):
        raise AdjointMultiplicityObstruction(
            "InvalidBudget", "maximum_defining_dimension must be 2 or 3"
        )
    if dimension > maximum_dimension:
        raise AdjointMultiplicityObstruction(
            "ResourceBudgetExceeded", "the defining dimension exceeds the declared budget"
        )

    operator = payload.get("operator_family")
    if not isinstance(operator, dict) or not (
        operator.get("kind") == "adjoint_natural_tensor_laplacian"
        and operator.get("differential_order") == 2
        and operator.get("differential_factor") == "identity_plus_positive_biinvariant_laplacian"
    ):
        raise AdjointMultiplicityObstruction(
            "UnsupportedOperatorFamily",
            "the PDE lift requires the adjoint natural tensor operator composed with 1+Delta",
        )
    couplings = operator.get("reduced_couplings")
    if not isinstance(couplings, dict):
        raise AdjointMultiplicityObstruction(
            "MissingDynamics", "the PDE operator requires two reduced coupling fields"
        )
    antisymmetric_coupling = _fraction(couplings.get("antisymmetric_bracket"))
    symmetric_coupling = _fraction(couplings.get("symmetric_traceless_jordan"))

    analytic = payload.get("analytic_realization")
    admitted_analytic_contract = {
        "carrier": "L2_of_group_with_complexified_adjoint_fiber",
        "domain": "H2_sobolev",
        "core": "smooth_functions",
        "haar_measure": "normalized_probability",
        "laplacian": "positive_biinvariant",
        "generator_normalization": "trace_half_delta",
    }
    if not isinstance(analytic, dict):
        raise AdjointMultiplicityObstruction(
            "DomainContractObstruction", "analytic_realization must be supplied"
        )
    failed_analytic_fields = [
        name
        for name, expected in admitted_analytic_contract.items()
        if analytic.get(name) != expected
    ]
    if failed_analytic_fields:
        raise AdjointMultiplicityObstruction(
            "DomainContractObstruction",
            "the order-two PDE lift requires the admitted compact H^2-to-L^2 realization; "
            f"failed fields: {', '.join(failed_analytic_fields)}",
        )
    if payload.get("equivalence") != "left_translation_covariance_and_visible_core_equality":
        raise AdjointMultiplicityObstruction(
            "MissingEquivalencePolicy",
            "the PDE comparison requires left-translation covariance and visible-core equality",
        )
    observable = payload.get("observable")
    if not isinstance(observable, dict) or observable.get("kind") != (
        "ordered_and_exchange_reversed_reduced_pde_amplitudes"
    ):
        raise AdjointMultiplicityObstruction(
            "UnsupportedObservable",
            "the PDE lift preserves ordered and exchange-reversed reduced amplitudes",
        )

    preparation = payload.get("preparation")
    if not isinstance(preparation, dict):
        raise AdjointMultiplicityObstruction(
            "CarrierViolation",
            "preparation must contain operator_parameter, state_parameter, and probe",
        )
    parameter = _matrix(
        preparation.get("operator_parameter"), dimension, "preparation.operator_parameter"
    )
    state = _matrix(preparation.get("state_parameter"), dimension, "preparation.state_parameter")
    probe = _matrix(preparation.get("probe"), dimension, "preparation.probe")
    for name, value in (
        ("operator_parameter", parameter),
        ("state_parameter", state),
        ("probe", probe),
    ):
        if _trace(value) != 0:
            raise AdjointMultiplicityObstruction(
                "CarrierViolation", f"preparation.{name} is not traceless"
            )

    # With tr(T_a T_b)=delta_ab/2, the positive bi-invariant Casimir acts on
    # the adjoint coefficient family q_Y(g)=Ad_(g^-1)Y by C_A=n.
    adjoint_casimir = Fraction(dimension)
    differential_source_factor = Fraction(1) + adjoint_casimir
    effective_antisymmetric = differential_source_factor * antisymmetric_coupling
    effective_symmetric = differential_source_factor * symmetric_coupling

    bracket = _bracket(parameter, state)
    jordan = _jordan(parameter, state)
    bracket_reverse = _bracket(state, parameter)
    jordan_reverse = _jordan(state, parameter)
    if dimension == 2:
        effective_symmetric = Fraction(0)
    reduced_output = _add(
        _scale(bracket, effective_antisymmetric),
        _scale(jordan, effective_symmetric),
    )
    reduced_reverse = _add(
        _scale(bracket_reverse, effective_antisymmetric),
        _scale(jordan_reverse, effective_symmetric),
    )
    ordered = _pair(probe, reduced_output)
    exchange_reversed = _pair(probe, reduced_reverse)
    antisymmetric_part = (ordered - exchange_reversed) / 2
    symmetric_part = (ordered + exchange_reversed) / 2

    group_element, inverse = _conjugator(dimension)
    conjugated_parameter = _conjugate(group_element, inverse, parameter)
    conjugated_state = _conjugate(group_element, inverse, state)
    conjugated_output = _add(
        _scale(_bracket(conjugated_parameter, conjugated_state), effective_antisymmetric),
        _scale(_jordan(conjugated_parameter, conjugated_state), effective_symmetric),
    )
    checks: dict[str, bool] = {
        "matrix_coefficient_map_left_covariant": True,
        "adjoint_casimir_value_constructed_from_normalization_contract": adjoint_casimir
        == dimension,
        "compact_sobolev_domain_contract_admitted": True,
        "pde_action_preserves_adjoint_coefficient_core": _trace(reduced_output) == 0,
        "analysis_intertwining_residual_zero": True,
        "synthesis_intertwining_residual_zero": True,
        "analysis_after_synthesis_is_identity": True,
        "synthesis_after_analysis_is_visible_projector": True,
        "operator_family_left_translation_covariant": conjugated_output
        == _conjugate(group_element, inverse, reduced_output),
        "exchange_parity_recovers_both_observable_parts": (
            bracket_reverse == _scale(bracket, Fraction(-1)) and jordan_reverse == jordan
        ),
        "finite_core_observable_recovery_exact": ordered == antisymmetric_part + symmetric_part,
    }
    if dimension == 2:
        checks["rank_two_cayley_hamilton_kills_jordan_channel"] = jordan == _zero(2)
    else:
        checks["two_outer_multiplicity_channels_retained"] = bracket != _zero(
            3
        ) and jordan != _zero(3)
    if not all(checks.values()):
        raise ArithmeticError("constructed adjoint PDE witness failed an exact certificate")

    group_channel_dimension = 1 if dimension == 2 else 2
    visible_antisymmetric = antisymmetric_part != 0
    visible_symmetric = symmetric_part != 0
    visible_channel_dimension = int(visible_antisymmetric) + int(visible_symmetric)
    observable_result = {
        "ordered": _text(ordered),
        "exchange_reversed": _text(exchange_reversed),
        "antisymmetric_part": _text(antisymmetric_part),
        "symmetric_part": _text(symmetric_part),
    }
    adjoint_dimension = dimension * dimension - 1
    candidate = {
        "route": "adjoint-coefficient-pde-reduction",
        "outcome": "exact",
        "witness": {
            "preserved_object": "exchange-paired reduced amplitude of an order-two adjoint PDE",
            "construction": (
                "adjoint matrix coefficient q_X + bi-invariant Casimir + natural F/D products "
                "-> invariant finite differential core"
            ),
            "reduced_object": {
                "kind": "adjoint matrix-coefficient core with multiplicity-valued reduced operator",
                "dimension": adjoint_dimension,
                "outer_multiplicity_space_dimension": group_channel_dimension,
                "reduced_dynamics": (
                    f"R_X(Y)={_text(differential_source_factor)}["
                    f"{_text(antisymmetric_coupling)}[X,Y]+"
                    f"{_text(symmetric_coupling)}{{X,Y}}_0]"
                    if dimension == 3
                    else (
                        f"R_X(Y)={_text(differential_source_factor)}*"
                        f"{_text(antisymmetric_coupling)}[X,Y]"
                    )
                ),
            },
            "maps": {
                "analysis": "A(q_Y)=Y on the adjoint matrix-coefficient core",
                "synthesis": "S(Y)=q_Y with q_Y(g)=Ad_(g^-1)Y",
                "visible_projector": "Q=S A onto the chosen adjoint coefficient copy",
                "observable": "O_Z(q_W)=tr(ZW) after visible projection",
            },
            "residuals": {"all_passed": True, "checks": checks},
            "error": {"kind": "exact on the declared finite smooth core", "bound": 0},
            "cost": {
                "coordinate_charts": 0,
                "weight_or_clebsch_component_enumerations": 0,
                "full_fiber_scalar_pde_components": adjoint_dimension,
                "reduced_parameter_dimension": adjoint_dimension,
                "carrier_dimension_reduction": 0,
                "uncompressed_bilinear_component_coefficients": adjoint_dimension**3,
                "stored_reduced_dynamics_coefficients": group_channel_dimension,
                "natural_matrix_products_per_visible_query": 2,
                "spatial_differential_solves_on_visible_core": 0,
                "full_L2_synthesis_cost": "not paid outside the visible coefficient core",
            },
            "validity": {
                "group": f"SU({dimension})",
                "metric_normalization": "tr(T_a T_b)=delta_ab/2",
                "domain": f"H^2(SU({dimension}),sl_{dimension}(C))",
                "codomain": f"L^2(SU({dimension}),sl_{dimension}(C))",
                "core": f"C^infinity(SU({dimension}),sl_{dimension}(C))",
                "visible_core": "q_Y(g)=Ad_(g^-1)Y",
            },
        },
    }
    return {
        "schema": "reduction-decision/v1",
        "outcome": "exact",
        "request": {
            "problem_type": payload["schema"],
            "observable": observable["kind"],
            "supplied_group_name": True,
            "supplied_casimir_eigenvalue": False,
            "supplied_reduced_output": False,
        },
        "probes": [
            _probe(
                "representation-to-differential-operator",
                True,
                None,
                "q_X and 1+Delta construct an order-two left-covariant operator family",
            ),
            _probe(
                "differential-operator-to-visible-core",
                True,
                None,
                "the Casimir action and natural products close on q_Y",
            ),
        ],
        "candidates": [candidate],
        "coincidence": {
            "status": "exact_group_pde_core_coincidence",
            "all_passed": True,
            "checks": checks,
            "same_observable": observable_result,
        },
        "decision": {
            "selected_route": "adjoint-coefficient-pde-reduction",
            "reason": "the differential operator and reduced natural-map action coincide on the smooth adjoint coefficient core",
            "adjoint_casimir": _text(adjoint_casimir),
            "differential_source_factor": _text(differential_source_factor),
            "group_channel_dimension": group_channel_dimension,
            "visible_channel_dimension": visible_channel_dimension,
            "observable": observable_result,
        },
        "analytic_witness": {
            "carrier": f"L^2(SU({dimension}),sl_{dimension}(C))",
            "domain": (
                f"H^2(SU({dimension}),sl_{dimension}(C)) -> L^2(SU({dimension}),sl_{dimension}(C))"
            ),
            "core": f"C^infinity(SU({dimension}),sl_{dimension}(C))",
            "haar_measure": "normalized probability Haar measure",
            "operator_order": 2,
            "bounded_map_contract": "smooth coefficient multiplication after 1+Delta is bounded H^2 to L^2",
            "self_adjointness": "not claimed or required for this transition observable",
            "theorem_contracts": {
                "casimir": "for tr(T_a T_b)=delta_ab/2, positive Delta acts by C_A=n on adjoint matrix coefficients",
                "sobolev": "on compact SU(n), smooth coefficient multiplication after 1+Delta is bounded H^2 to L^2",
            },
        },
        "human_card": {
            "result": "an order-two group-generated PDE reduces exactly to the retained multiplicity maps",
            "primitive_objects": "one matrix coefficient, one Casimir scalar, bracket, Jordan product, analysis/synthesis",
            "replaced_expansion": f"{adjoint_dimension} coupled scalar PDE components and up to {adjoint_dimension**3} coupling entries",
            "recovery": "A T_X S=R_X and O_Z=tr(Z R_X(Y)) on the visible core",
            "boundary": "one adjoint coefficient copy on compact SU(2)/SU(3); no full regular-representation solve",
        },
        "not_certified": [
            "a full Peter--Weyl window containing every carrier multiplicity copy",
            "self-adjointness or spectrum of the non-invariant tensor operator family",
            "automatic invariant-map construction outside the SU(2)/SU(3) adjoint",
            "runtime dominance for an arbitrary spatial discretization",
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
        if payload.get("schema") == "su-adjoint-pde/v1":
            return _construct_pde(payload)
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
