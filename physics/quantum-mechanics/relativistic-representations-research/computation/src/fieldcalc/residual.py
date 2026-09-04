"""Exact obstruction-driven repair and bounded route-cost certificates."""

from dataclasses import dataclass

from sympy import Matrix, Rational, simplify

from .rewrite import Refusal


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


def projected_raise_coefficient(rank: int, dimension: int):
    denominator = 2 * rank + dimension - 2
    if rank < 1 or denominator == 0:
        raise ValueError("projected raise requires positive rank and nonzero denominator")
    return Rational(-1, denominator)


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
