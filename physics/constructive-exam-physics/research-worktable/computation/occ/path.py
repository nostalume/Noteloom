from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from sympy import (
    Integral,
    Symbol,
    diff,
    integrate,
    simplify,
    sqrt,
    sympify,
    together,
    trigsimp,
)
from sympy.core.expr import Expr

from .records import Certificate


@dataclass(frozen=True)
class PathObstruction:
    code: str
    message: str


@dataclass(frozen=True)
class PlanarVectorField:
    name: str
    coordinates: tuple[Symbol, Symbol]
    components: tuple[Expr, Expr]
    parameters: tuple[Symbol, ...]
    provenance: str
    scalar_potential: Optional[Expr] = None

    def __init__(
        self,
        name: str,
        coordinates: tuple[Symbol, Symbol],
        components: tuple[Any, Any],
        parameters: tuple[Symbol, ...],
        provenance: str,
        scalar_potential: Any = None,
    ) -> None:
        field_name = name.strip()
        source = provenance.strip()
        coordinates = tuple(coordinates)
        parameters = tuple(parameters)
        if not field_name or not source:
            raise ValueError("A planar field requires a name and provenance.")
        if len(coordinates) != 2 or any(
            not isinstance(value, Symbol) for value in coordinates
        ):
            raise TypeError("A planar field requires exactly two coordinate symbols.")
        if len(set(coordinates)) != 2:
            raise ValueError("Planar field coordinates must be distinct.")
        if any(not isinstance(value, Symbol) for value in parameters):
            raise TypeError("Field parameters must be SymPy Symbol objects.")
        if len(set(parameters)) != len(parameters):
            raise ValueError("Field parameters contain a duplicate symbol.")
        if set(coordinates) & set(parameters):
            raise ValueError("Field coordinates and parameters must be disjoint.")
        expressions = tuple(sympify(value) for value in components)
        if len(expressions) != 2:
            raise ValueError("A planar field requires exactly two components.")
        potential = None if scalar_potential is None else sympify(scalar_potential)
        declared = set(coordinates) | set(parameters)
        if any(not expression.free_symbols <= declared for expression in expressions):
            raise ValueError("A field component contains an undeclared symbol.")
        if potential is not None and not potential.free_symbols <= declared:
            raise ValueError("The scalar potential contains an undeclared symbol.")
        object.__setattr__(self, "name", field_name)
        object.__setattr__(self, "coordinates", coordinates)
        object.__setattr__(self, "components", expressions)
        object.__setattr__(self, "parameters", parameters)
        object.__setattr__(self, "provenance", source)
        object.__setattr__(self, "scalar_potential", potential)


@dataclass(frozen=True)
class ParameterizedPath:
    name: str
    parameter: Symbol
    lower: Expr
    upper: Expr
    position: tuple[Expr, Expr]
    provenance: str

    def __init__(
        self,
        name: str,
        parameter: Symbol,
        lower: Any,
        upper: Any,
        position: tuple[Any, Any],
        provenance: str,
    ) -> None:
        path_name = name.strip()
        source = provenance.strip()
        if not path_name or not source:
            raise ValueError("A path requires a name and provenance.")
        if not isinstance(parameter, Symbol):
            raise TypeError("A path parameter must be a SymPy Symbol.")
        lower_expr = sympify(lower)
        upper_expr = sympify(upper)
        if lower_expr.free_symbols or upper_expr.free_symbols:
            raise ValueError("Path bounds must be exact constants.")
        if simplify(lower_expr - upper_expr) == 0:
            raise ValueError("A path interval must be nondegenerate.")
        coordinates = tuple(sympify(value) for value in position)
        if len(coordinates) != 2:
            raise ValueError("A planar path requires two coordinate expressions.")
        object.__setattr__(self, "name", path_name)
        object.__setattr__(self, "parameter", parameter)
        object.__setattr__(self, "lower", lower_expr)
        object.__setattr__(self, "upper", upper_expr)
        object.__setattr__(self, "position", coordinates)
        object.__setattr__(self, "provenance", source)

    def reversed(self, name: Optional[str] = None) -> ParameterizedPath:
        reflected = self.lower + self.upper - self.parameter
        return ParameterizedPath(
            name or f"reverse {self.name}",
            self.parameter,
            self.lower,
            self.upper,
            tuple(
                simplify(component.subs(self.parameter, reflected))
                for component in self.position
            ),
            f"orientation reversal of {self.provenance}",
        )


@dataclass(frozen=True)
class PathFunctionalRequest:
    field: PlanarVectorField
    paths: tuple[ParameterizedPath, ...]
    max_paths: Optional[int] = None

    def __post_init__(self) -> None:
        paths = tuple(self.paths)
        object.__setattr__(self, "paths", paths)
        if not paths:
            raise ValueError("A path-functional request requires at least one path.")
        names = tuple(path.name for path in paths)
        if len(names) != len(set(names)):
            raise ValueError("Path names must be unique within a request.")
        if self.max_paths is not None and (
            not isinstance(self.max_paths, int)
            or isinstance(self.max_paths, bool)
            or self.max_paths < 1
        ):
            raise ValueError("max_paths must be a positive integer or None.")
        allowed_parameters = set(self.field.parameters)
        for path in paths:
            if path.parameter in set(self.field.coordinates) | allowed_parameters:
                raise ValueError("A path parameter must be local to its path.")
            allowed = allowed_parameters | {path.parameter}
            if any(
                not component.free_symbols <= allowed for component in path.position
            ):
                raise ValueError("A path position contains an undeclared symbol.")


@dataclass(frozen=True)
class PathEvaluation:
    name: str
    start: tuple[Expr, Expr]
    end: tuple[Expr, Expr]
    line_work: Expr
    length: Expr
    signed_area_contribution: Expr


@dataclass(frozen=True)
class PathFunctionalResult:
    status: str
    request: PathFunctionalRequest
    paths: tuple[PathEvaluation, ...] = ()
    curl: Optional[Expr] = None
    scalar_potential_difference: Optional[Expr] = None
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[PathObstruction] = None

    def path(self, name: str) -> PathEvaluation:
        for path in self.paths:
            if path.name == name:
                return path
        raise KeyError(name)

    def work_difference(self, first: str, second: str) -> Expr:
        return simplify(self.path(first).line_work - self.path(second).line_work)

    def signed_area_difference(self, first: str, second: str) -> Expr:
        return simplify(
            self.path(first).signed_area_contribution
            - self.path(second).signed_area_contribution
        )


@dataclass(frozen=True)
class EndpointValueResult:
    status: str
    value: Optional[Expr] = None
    path_name: Optional[str] = None
    obstruction: Optional[PathObstruction] = None


@dataclass(frozen=True)
class TwoPathCircuitResult:
    status: str
    first_path: str
    second_path: str
    terminal_voltage: Optional[Expr] = None
    first_current: Optional[Expr] = None
    second_current: Optional[Expr] = None
    first_resistance: Optional[Expr] = None
    second_resistance: Optional[Expr] = None
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[PathObstruction] = None


def _refused(
    request: PathFunctionalRequest,
    code: str,
    message: str,
) -> PathFunctionalResult:
    return PathFunctionalResult(
        status="refused",
        request=request,
        obstruction=PathObstruction(code, message),
    )


def _same_point(left: tuple[Expr, Expr], right: tuple[Expr, Expr]) -> bool:
    return all(simplify(a - b) == 0 for a, b in zip(left, right))


def _evaluate_path(
    field: PlanarVectorField, path: ParameterizedPath
) -> Optional[PathEvaluation]:
    substitution = dict(zip(field.coordinates, path.position))
    velocity = tuple(diff(component, path.parameter) for component in path.position)
    field_on_path = tuple(
        component.subs(substitution) for component in field.components
    )
    work_integrand = trigsimp(
        simplify(
            sum(component * rate for component, rate in zip(field_on_path, velocity))
        )
    )
    speed_squared = trigsimp(simplify(sum(rate**2 for rate in velocity)))
    line_work = simplify(
        integrate(work_integrand, (path.parameter, path.lower, path.upper))
    )
    length = simplify(
        integrate(sqrt(speed_squared), (path.parameter, path.lower, path.upper))
    )
    signed_area_integrand = simplify(
        (path.position[0] * velocity[1] - path.position[1] * velocity[0]) / 2
    )
    signed_area_contribution = simplify(
        integrate(
            signed_area_integrand,
            (path.parameter, path.lower, path.upper),
        )
    )
    if any(
        value.has(Integral) for value in (line_work, length, signed_area_contribution)
    ):
        return None
    start = tuple(
        simplify(component.subs(path.parameter, path.lower))
        for component in path.position
    )
    end = tuple(
        simplify(component.subs(path.parameter, path.upper))
        for component in path.position
    )
    return PathEvaluation(
        path.name,
        start,
        end,
        line_work,
        length,
        signed_area_contribution,
    )


def construct_path_functionals(
    request: PathFunctionalRequest,
) -> PathFunctionalResult:
    """Integrate one planar field along same-endpoint oriented paths exactly."""

    if request.max_paths is not None and len(request.paths) > request.max_paths:
        return _refused(
            request,
            "path_budget_exceeded",
            "The request exceeds its path budget before integration.",
        )

    evaluations = []
    for path in request.paths:
        evaluation = _evaluate_path(request.field, path)
        if evaluation is None:
            return _refused(
                request,
                "unevaluated_path_integral",
                f"The exact backend did not evaluate path {path.name!r} completely.",
            )
        evaluations.append(evaluation)

    first = evaluations[0]
    if any(
        not _same_point(first.start, path.start) or not _same_point(first.end, path.end)
        for path in evaluations[1:]
    ):
        return _refused(
            request,
            "endpoint_mismatch",
            "All paths in one request must have the same oriented endpoints.",
        )

    curl = simplify(
        diff(request.field.components[1], request.field.coordinates[0])
        - diff(request.field.components[0], request.field.coordinates[1])
    )
    certificates = (
        Certificate(
            "common_oriented_endpoints",
            True,
            "Every declared path starts and ends at the same symbolic points.",
        ),
        Certificate(
            "path_integrals_evaluated",
            True,
            "Every line-work and arc-length integral evaluated without a residual Integral.",
        ),
    )
    if len(evaluations) >= 2 and not (
        curl.free_symbols & set(request.field.coordinates)
    ):
        reference = evaluations[0]
        constant_curl_recovery = all(
            simplify(
                path.line_work
                - reference.line_work
                - curl
                * (path.signed_area_contribution - reference.signed_area_contribution)
            )
            == 0
            for path in evaluations[1:]
        )
        if not constant_curl_recovery:
            return _refused(
                request,
                "constant_curl_recovery_failed",
                "A path difference failed exact constant-curl recovery.",
            )
        certificates += (
            Certificate(
                "constant_curl_path_difference",
                True,
                "Every same-endpoint work difference equals curl times the signed area between the two paths.",
            ),
        )
    potential_difference = None
    potential = request.field.scalar_potential
    if potential is not None:
        is_gradient = all(
            simplify(component + diff(potential, coordinate)) == 0
            for component, coordinate in zip(
                request.field.components, request.field.coordinates
            )
        )
        if not is_gradient:
            return _refused(
                request,
                "scalar_potential_mismatch",
                "The supplied scalar potential does not generate the declared field.",
            )
        start_substitution = dict(zip(request.field.coordinates, first.start))
        end_substitution = dict(zip(request.field.coordinates, first.end))
        potential_difference = simplify(
            potential.subs(end_substitution) - potential.subs(start_substitution)
        )
        recovers = all(
            simplify(path.line_work + potential_difference) == 0 for path in evaluations
        )
        if not recovers:
            return _refused(
                request,
                "scalar_potential_recovery_failed",
                "A path integral failed to recover the supplied endpoint potential.",
            )
        certificates += (
            Certificate(
                "scalar_potential_recovered",
                True,
                "Every declared path work equals minus the same endpoint potential difference.",
            ),
        )

    return PathFunctionalResult(
        status="constructed",
        request=request,
        paths=tuple(evaluations),
        curl=curl,
        scalar_potential_difference=potential_difference,
        certificates=certificates,
    )


def resolve_open_wire_voltage(
    result: PathFunctionalResult, path_name: str
) -> EndpointValueResult:
    """Return V(end)-V(start) induced on one open conducting path."""

    if result.status != "constructed":
        return EndpointValueResult(
            status="refused",
            obstruction=PathObstruction(
                "path_construction_failed",
                "An open-wire voltage requires a constructed path functional.",
            ),
        )
    path = result.path(path_name)
    return EndpointValueResult(
        status="constructed", value=path.line_work, path_name=path_name
    )


def resolve_free_space_potential_difference(
    result: PathFunctionalResult,
) -> EndpointValueResult:
    """Return a path-independent endpoint value only with a verified potential."""

    if result.status != "constructed":
        return EndpointValueResult(
            status="refused",
            obstruction=PathObstruction(
                "path_construction_failed",
                "Endpoint recovery requires constructed path functionals.",
            ),
        )
    if result.scalar_potential_difference is None:
        return EndpointValueResult(
            status="refused",
            obstruction=PathObstruction(
                "no_scalar_potential_certificate",
                "Endpoints alone do not define a voltage without a verified scalar potential or measurement path.",
            ),
        )
    return EndpointValueResult(
        status="constructed", value=result.scalar_potential_difference
    )


def construct_two_path_circuit(
    result: PathFunctionalResult,
    first_path: str,
    second_path: str,
    resistance_per_length: Any,
) -> TwoPathCircuitResult:
    """Close two conducting paths into a loop and solve terminal voltage/current."""

    if result.status != "constructed":
        return TwoPathCircuitResult(
            status="refused",
            first_path=first_path,
            second_path=second_path,
            obstruction=PathObstruction(
                "path_construction_failed",
                "Circuit construction requires exact path functionals.",
            ),
        )
    if first_path == second_path:
        raise ValueError("A two-path circuit requires two distinct paths.")
    first = result.path(first_path)
    second = result.path(second_path)
    density = sympify(resistance_per_length)
    if density.is_positive is not True:
        return TwoPathCircuitResult(
            status="refused",
            first_path=first_path,
            second_path=second_path,
            obstruction=PathObstruction(
                "nonpositive_resistance_density",
                "Resistance per unit length must be declared strictly positive.",
            ),
        )
    first_resistance = simplify(density * first.length)
    second_resistance = simplify(density * second.length)
    denominator = simplify(first_resistance + second_resistance)
    terminal_voltage = together(
        (first.line_work * second_resistance + second.line_work * first_resistance)
        / denominator
    )
    first_current = together((first.line_work - second.line_work) / denominator)
    second_current = -first_current
    certificates = (
        Certificate(
            "node_current_conserved",
            simplify(first_current + second_current) == 0,
            "The two oriented branch currents sum to zero at each isolated terminal.",
        ),
        Certificate(
            "first_branch_voltage_recovered",
            simplify(
                first.line_work - first_current * first_resistance - terminal_voltage
            )
            == 0,
            "The first branch recovers the common terminal voltage.",
        ),
        Certificate(
            "second_branch_voltage_recovered",
            simplify(
                second.line_work - second_current * second_resistance - terminal_voltage
            )
            == 0,
            "The second branch recovers the common terminal voltage.",
        ),
    )
    return TwoPathCircuitResult(
        status="constructed",
        first_path=first_path,
        second_path=second_path,
        terminal_voltage=terminal_voltage,
        first_current=first_current,
        second_current=second_current,
        first_resistance=first_resistance,
        second_resistance=second_resistance,
        certificates=certificates,
    )
