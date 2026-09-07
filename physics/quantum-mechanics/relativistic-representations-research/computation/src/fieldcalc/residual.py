"""Exact obstruction-driven repair and bounded route-cost certificates."""

from dataclasses import dataclass

from sympy import Matrix, Rational, simplify

from .rewrite import Polynomial, Refusal


@dataclass(frozen=True)
class ResidualRequest:
    channels: tuple[object, ...]
    correction_columns: tuple[tuple[object, ...], ...]
    names: tuple[str, ...]
    provenance: str = ""


@dataclass(frozen=True)
class ResidualSolution:
    coefficients: tuple = ()
    remaining: tuple = ()
    names: tuple[str, ...] = ()
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def resolve_residual(request: ResidualRequest) -> ResidualSolution:
    residual = Matrix(request.channels)
    if len(request.names) != len(request.correction_columns):
        raise ValueError("every correction column needs one semantic name")
    if not request.correction_columns:
        return ResidualSolution(
            remaining=tuple(residual),
            refusal=Refusal("no correction operations", tuple(residual), request.provenance),
        )
    columns = [Matrix(column) for column in request.correction_columns]
    if any(column.rows != residual.rows for column in columns):
        raise ValueError("correction and residual channels must have the same codomain")
    correction = Matrix.hstack(*columns)
    target = -residual
    if correction.row_join(target).rank() > correction.rank():
        return ResidualSolution(
            remaining=tuple(residual),
            names=request.names,
            refusal=Refusal(
                "residual outside correction span", tuple(residual), request.provenance
            ),
        )
    solution, parameters = correction.gauss_jordan_solve(target)
    substitutions = {symbol: 0 for symbol in parameters.free_symbols}
    coefficients = tuple(simplify(value.subs(substitutions)) for value in solution)
    remaining = tuple(simplify(value) for value in residual + correction * Matrix(coefficients))
    return ResidualSolution(coefficients, remaining, request.names)


@dataclass(frozen=True)
class WardLiftRequest:
    internal_channels: tuple[str, ...]
    external_generators: tuple[str, ...]
    primary_internal: tuple[object, ...]
    primary_external: tuple[object, ...]
    correction_internal: tuple[tuple[object, ...], ...]
    correction_external: tuple[tuple[object, ...], ...]
    correction_names: tuple[str, ...]
    budget: int
    provenance: str = ""


@dataclass(frozen=True)
class WardLiftResult:
    weights: tuple[object, ...]
    remaining_internal: tuple[object, ...]
    external_generators: tuple[str, ...]
    external_coefficients: tuple[object, ...]
    correction_names: tuple[str, ...]
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def lift_ward_packet(request: WardLiftRequest) -> WardLiftResult:
    """Lift algebraic Ward residuals into the smallest admitted packet repair."""
    internal_size = len(request.internal_channels)
    external_size = len(request.external_generators)
    if len(request.primary_internal) != internal_size:
        raise ValueError("primary internal residual must match its named channels")
    if len(request.primary_external) != external_size:
        raise ValueError("primary external residual must match its ideal generators")
    if not (
        len(request.correction_internal)
        == len(request.correction_external)
        == len(request.correction_names)
    ):
        raise ValueError("every Ward repair needs internal, external, and name data")
    if any(len(column) != internal_size for column in request.correction_internal):
        raise ValueError("Ward repairs must share the internal residual codomain")
    if any(len(column) != external_size for column in request.correction_external):
        raise ValueError("Ward repairs must share the external ideal basis")

    if request.budget < len(request.correction_internal):
        refusal = Refusal(
            "Ward repair budget exceeded",
            tuple(request.primary_internal),
            request.provenance,
        )
        return WardLiftResult(
            (1,),
            tuple(request.primary_internal),
            request.external_generators,
            tuple(request.primary_external),
            request.correction_names,
            refusal,
        )

    solution = resolve_residual(
        ResidualRequest(
            request.primary_internal,
            request.correction_internal,
            request.correction_names,
            request.provenance,
        )
    )
    if not solution.accepted:
        return WardLiftResult(
            (1,),
            solution.remaining,
            request.external_generators,
            tuple(request.primary_external),
            request.correction_names,
            solution.refusal,
        )

    external = Matrix(request.primary_external)
    for weight, column in zip(solution.coefficients, request.correction_external):
        external += weight * Matrix(column)
    return WardLiftResult(
        (1, *solution.coefficients),
        solution.remaining,
        request.external_generators,
        tuple(simplify(value) for value in external),
        request.correction_names,
    )


@dataclass(frozen=True)
class ObservableDescentRequest:
    external_generators: tuple[str, ...]
    primary_on_ideal: tuple[object, ...]
    correction_on_ideal: tuple[tuple[object, ...], ...]
    correction_names: tuple[str, ...]
    budget: int
    provenance: str = ""


@dataclass(frozen=True)
class ObservableDescentResult:
    weights: tuple[object, ...]
    remaining: tuple[object, ...]
    external_generators: tuple[str, ...]
    correction_names: tuple[str, ...]
    kind: str
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def _descent_result(request, remaining, kind, weights=(1,), refusal=None):
    return ObservableDescentResult(
        weights, tuple(remaining), request.external_generators,
        request.correction_names, kind, refusal,
    )


def descend_observable(
    request: ObservableDescentRequest,
) -> ObservableDescentResult:
    """Admit an observable only when it factors through the external quotient."""
    size = len(request.external_generators)
    if len(request.primary_on_ideal) != size:
        raise ValueError("observable residual must match the external ideal basis")
    if len(request.correction_on_ideal) != len(request.correction_names):
        raise ValueError("every observable repair needs one semantic name")
    if any(len(column) != size for column in request.correction_on_ideal):
        raise ValueError("observable repairs must share the external ideal basis")

    residual = tuple(simplify(value) for value in request.primary_on_ideal)
    if not any(residual):
        return _descent_result(request, residual, "direct quotient")
    if request.budget < len(request.correction_on_ideal):
        return _descent_result(
            request,
            residual,
            "refused",
            refusal=Refusal(
                "observable repair budget exceeded", residual, request.provenance,
            ),
        )
    if not request.correction_on_ideal:
        return _descent_result(
            request,
            residual,
            "refused",
            refusal=Refusal(
                "observable does not annihilate external ideal",
                residual, request.provenance,
            ),
        )

    solution = resolve_residual(ResidualRequest(
        residual, request.correction_on_ideal,
        request.correction_names, request.provenance,
    ))
    if not solution.accepted:
        return _descent_result(
            request,
            solution.remaining,
            "refused",
            refusal=solution.refusal,
        )
    return _descent_result(
        request,
        solution.remaining,
        "compensated quotient",
        weights=(1, *solution.coefficients),
    )


def projected_raise_coefficient(rank: int, dimension: int):
    denominator = 2 * rank + dimension - 2
    if rank < 1 or denominator == 0:
        raise ValueError("projected raise requires positive rank and nonzero denominator")
    return Rational(-1, denominator)


@dataclass(frozen=True)
class SourceAdapterInverse:
    spin: int
    adapter_coefficient: object
    coefficient: object
    operation: Polynomial
    residual: tuple
    provenance: str


def source_adapter_inverse(spin: int, adapter_coefficient: object) -> SourceAdapterInverse:
    """Invert ``I + a UT`` using ``(UT)^2 = 4s UT`` on the trace cell."""
    if spin < 2:
        raise ValueError("source adapter requires a traceful spin cell")
    adapter_coefficient = Rational(adapter_coefficient)
    correction_channel = 1 + 4 * spin * adapter_coefficient
    if correction_channel == 0:
        raise ValueError("source adapter is singular on the trace cell")
    provenance = f"spin-{spin} source-adapter inverse"
    solution = resolve_residual(
        ResidualRequest(
            channels=(adapter_coefficient,),
            correction_columns=((correction_channel,),),
            names=("UT",),
            provenance=provenance,
        )
    )
    if not solution.accepted or any(solution.remaining):
        raise ArithmeticError("source-adapter inverse residual did not vanish")
    coefficient = solution.coefficients[0]
    return SourceAdapterInverse(
        spin=spin,
        adapter_coefficient=adapter_coefficient,
        coefficient=coefficient,
        operation=Polynomial({(): 1, ("U", "T"): coefficient}),
        residual=solution.remaining,
        provenance=provenance,
    )


@dataclass(frozen=True)
class CostVerdict:
    preferred: str
    direct_load: int
    compensated_load: int
    active_direct_solves: int
    active_compensated_solves: int


def compare_carrier_costs(spin: int, active_layers: int | None = None) -> CostVerdict:
    if spin < 2:
        raise ValueError("comparison bench starts at spin two")
    direct = (spin + 1) ** 3
    compensated = 2 * spin * spin + 2
    if active_layers == 1:
        return CostVerdict("tie", direct, compensated, 1, 1)
    preferred = "direct" if direct < compensated else "compensated" if direct > compensated else "tie"
    return CostVerdict(preferred, direct, compensated, spin + 1, 1)
