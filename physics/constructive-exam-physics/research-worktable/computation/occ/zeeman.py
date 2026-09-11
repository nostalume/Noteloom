from collections.abc import Mapping
from fractions import Fraction
from typing import Any

from ._parameterized_contracts import (
    Certificate,
    CompilationResult,
    Obstruction,
    ParameterizedHeader,
    RouteStep,
    refused,
    solved,
)


_ADAPTER = "atomic.weak_field_zeeman"
_OBJECTS = {"ls_term", "electric_dipole_transition", "weak_magnetic_field"}
_OBSERVABLE = "zeeman_line_shifts"
_FIELDS = ("upper", "lower", "zeeman_to_fine_ratio", "weak_ratio_max")
_DIPOLE_DELTAS = frozenset((-1, 0, 1))
_VALIDATE_STEP = RouteStep(
    operation="validate_ls_and_e1_contracts",
    witness="Triangle, Delta S, Delta L, Delta J, zero-to-zero, and parity rules pass.",
)
_SUBLEVEL_STEP = RouteStep(
    operation="construct_magnetic_sublevels",
    witness="Each J carrier contributes m=-J,-J+1,...,J.",
)
_SELECTION_STEP = RouteStep(
    operation="construct_selection_graph",
    witness="Edges are generated exactly when Delta m is 0 or +/-1.",
)
_RECOVERY_STEP = RouteStep(
    operation="recover_distinct_line_shifts",
    witness="Each edge is evaluated by g_upper*m_upper-g_lower*m_lower.",
)


def admit(header: ParameterizedHeader) -> ParameterizedHeader | None:
    if not _OBJECTS.issubset(header.objects) or header.observable != _OBSERVABLE:
        return None
    return header


def _as_fraction(value: Any) -> Fraction:
    if isinstance(value, float):
        return Fraction(str(value))
    return Fraction(value)


def _term(
    data: Mapping[str, Any], label: str
) -> tuple[int, Fraction, Fraction, str] | CompilationResult:
    missing = tuple(field for field in ("L", "S", "J", "parity") if field not in data)
    if missing:
        return refused(
            _ADAPTER,
            Obstruction(
                code="missing_field",
                message=f"The {label} LS term is incomplete.",
                fields=tuple(f"{label}.{field}" for field in missing),
            ),
        )
    try:
        orbital = int(data["L"])
        spin = _as_fraction(data["S"])
        total = _as_fraction(data["J"])
    except (TypeError, ValueError, ZeroDivisionError):
        return refused(
            _ADAPTER,
            Obstruction(
                code="invalid_quantum_number",
                message=f"The {label} term has invalid L, S, or J.",
            ),
        )
    parity = data["parity"]
    if orbital < 0 or spin < 0 or total < 0 or parity not in {"even", "odd"}:
        return refused(
            _ADAPTER,
            Obstruction(
                code="invalid_quantum_number",
                message=f"The {label} term lies outside the admitted LS-term types.",
            ),
        )
    if (2 * spin).denominator != 1 or (2 * total).denominator != 1:
        return refused(
            _ADAPTER,
            Obstruction(
                code="invalid_quantum_number",
                message="S and J must be integer or half-integer values.",
            ),
        )
    if not abs(Fraction(orbital) - spin) <= total <= Fraction(orbital) + spin:
        return refused(
            _ADAPTER,
            Obstruction(
                code="incompatible_quantum_numbers",
                message=f"The {label} J is not contained in the coupling of L and S.",
            ),
        )
    return orbital, spin, total, parity


def _lande(orbital: int, spin: Fraction, total: Fraction) -> Fraction:
    if total == 0:
        return Fraction(0)
    return 1 + (total * (total + 1) + spin * (spin + 1) - orbital * (orbital + 1)) / (
        2 * total * (total + 1)
    )


def _magnetic_values(total: Fraction) -> tuple[Fraction, ...]:
    count = int(2 * total) + 1
    return tuple(-total + index for index in range(count))


def solve(request: ParameterizedHeader) -> CompilationResult:
    parameters = request.parameters
    missing = tuple(field for field in _FIELDS if field not in parameters)
    if missing:
        return refused(
            _ADAPTER,
            Obstruction(
                code="missing_field",
                message="Weak-field Zeeman compilation requires an explicit hierarchy and both terms.",
                fields=missing,
            ),
        )

    try:
        ratio = float(parameters["zeeman_to_fine_ratio"])
        weak_max = float(parameters["weak_ratio_max"])
    except (TypeError, ValueError):
        return refused(
            _ADAPTER,
            Obstruction(
                code="invalid_field",
                message="The weak-field hierarchy must be numeric.",
                fields=("zeeman_to_fine_ratio", "weak_ratio_max"),
            ),
        )
    if ratio < 0 or weak_max <= 0 or ratio > weak_max:
        return refused(
            _ADAPTER,
            Obstruction(
                code="unsupported_regime",
                message="The supplied energy hierarchy does not justify the weak-field LS basis.",
                fields=("zeeman_to_fine_ratio", "weak_ratio_max"),
            ),
        )

    upper = _term(parameters["upper"], "upper")
    if isinstance(upper, CompilationResult):
        return upper
    lower = _term(parameters["lower"], "lower")
    if isinstance(lower, CompilationResult):
        return lower
    upper_l, upper_s, upper_j, upper_parity = upper
    lower_l, lower_s, lower_j, lower_parity = lower

    e1_allowed = (
        upper_s == lower_s
        and abs(upper_l - lower_l) <= 1
        and not (upper_l == 0 and lower_l == 0)
        and abs(upper_j - lower_j) <= 1
        and not (upper_j == 0 and lower_j == 0)
        and upper_parity != lower_parity
    )
    if not e1_allowed:
        return refused(
            _ADAPTER,
            Obstruction(
                code="forbidden_transition",
                message="The supplied LS terms do not satisfy the admitted electric-dipole rules.",
            ),
        )

    upper_g = _lande(upper_l, upper_s, upper_j)
    lower_g = _lande(lower_l, lower_s, lower_j)
    edges: list[tuple[Fraction, Fraction, Fraction, str]] = []
    shift_values: set[Fraction] = set()
    pi_count = 0
    for upper_m in _magnetic_values(upper_j):
        for lower_m in _magnetic_values(lower_j):
            delta_m = upper_m - lower_m
            if delta_m in _DIPOLE_DELTAS:
                shift = upper_g * upper_m - lower_g * lower_m
                polarization = "pi" if delta_m == 0 else "sigma"
                edges.append((upper_m, lower_m, shift, polarization))
                shift_values.add(shift)
                pi_count += delta_m == 0

    shifts = sorted(shift_values)
    polarization_counts = {"pi": pi_count, "sigma": len(edges) - pi_count}
    centered = all(-shift in shift_values for shift in shift_values)
    route = (
        _VALIDATE_STEP,
        RouteStep(
            operation="construct_lande_factors",
            witness=f"g_upper={upper_g}, g_lower={lower_g} from the LS term data.",
        ),
        _SUBLEVEL_STEP,
        _SELECTION_STEP,
        _RECOVERY_STEP,
    )
    certificates = (
        Certificate(
            name="weak_field_hierarchy",
            passed=ratio <= weak_max,
            witness=f"zeeman/fine={ratio!r} <= admitted maximum {weak_max!r}",
        ),
        Certificate(
            name="selection_graph",
            passed=all(abs(edge[0] - edge[1]) <= 1 for edge in edges),
            witness=f"{len(edges)} edges satisfy Delta m in {{-1,0,1}}.",
        ),
        Certificate(
            name="spectral_center_symmetry",
            passed=centered,
            witness="The distinct dimensionless shifts are closed under sign reversal.",
        ),
    )
    return solved(
        adapter=_ADAPTER,
        value={
            "g_factors": {"upper": upper_g, "lower": lower_g},
            "transition_count": len(edges),
            "distinct_line_count": len(shifts),
            "shift_coefficients": shifts,
            "polarization_counts": polarization_counts,
            "edges": tuple(edges),
        },
        route=route,
        certificates=certificates,
    )
