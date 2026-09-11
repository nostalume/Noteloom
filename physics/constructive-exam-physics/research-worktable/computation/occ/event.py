from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from sympy import S, Symbol, simplify, solve_poly_system, sympify
from sympy.core.expr import Expr
from sympy.polys.polyerrors import CoercionFailed, ComputationFailed, PolynomialError

from .problem import PhysicalLaw
from .records import Certificate
from .relation import (
    PolynomialEliminationResult,
    RelationObstruction,
    eliminate_polynomial_relations,
)


def _decide(statement: Any) -> Optional[bool]:
    value = simplify(statement)
    if value is S.true:
        return True
    if value is S.false:
        return False
    return None


@dataclass(frozen=True)
class EventPredicate:
    name: str
    relation: Expr
    provenance: str

    def __init__(self, name: str, relation: Any, provenance: str) -> None:
        object.__setattr__(self, "name", name.strip())
        object.__setattr__(self, "relation", sympify(relation))
        object.__setattr__(self, "provenance", provenance.strip())
        if not self.name or not self.provenance:
            raise ValueError("An event predicate requires a name and provenance.")


@dataclass(frozen=True)
class VariableInterval:
    symbol: Symbol
    lower: Optional[Expr] = None
    upper: Optional[Expr] = None
    meaning: str = ""

    def __init__(
        self,
        symbol: Symbol,
        *,
        lower: Any = None,
        upper: Any = None,
        meaning: str = "",
    ) -> None:
        if not isinstance(symbol, Symbol):
            raise TypeError("An interval variable must be a SymPy Symbol.")
        lower_expr = None if lower is None else sympify(lower)
        upper_expr = None if upper is None else sympify(upper)
        if lower_expr is None and upper_expr is None:
            raise ValueError("An interval requires at least one bound.")
        for bound in (lower_expr, upper_expr):
            if bound is not None and (bound.free_symbols or bound.is_real is not True):
                raise ValueError("Event-domain bounds must be exact real constants.")
        if lower_expr is not None and upper_expr is not None:
            ordered = _decide(lower_expr <= upper_expr)
            if ordered is not True:
                raise ValueError("Event-domain bounds must have a decidable order.")
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "lower", lower_expr)
        object.__setattr__(self, "upper", upper_expr)
        object.__setattr__(self, "meaning", meaning.strip())

    def contains(self, value: Expr) -> Optional[bool]:
        checks = []
        if self.lower is not None:
            checks.append(_decide(self.lower <= value))
        if self.upper is not None:
            checks.append(_decide(value <= self.upper))
        if any(check is False for check in checks):
            return False
        if any(check is None for check in checks):
            return None
        return True


@dataclass(frozen=True)
class EventProblem:
    problem_id: str
    pdf_page: int
    state_laws: tuple[PhysicalLaw, ...]
    event: EventPredicate
    unknowns: tuple[Symbol, ...]
    event_coordinate: Symbol
    domains: tuple[VariableInterval, ...] = ()
    max_variables: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.problem_id.strip():
            raise ValueError("An event problem requires an id.")
        if self.pdf_page < 1:
            raise ValueError("An event problem requires a positive PDF page.")
        if not self.state_laws:
            raise ValueError("An event problem requires at least one state law.")
        if not self.unknowns or any(
            not isinstance(symbol, Symbol) for symbol in self.unknowns
        ):
            raise TypeError("Event unknowns must be SymPy Symbol objects.")
        if len(self.unknowns) != len(set(self.unknowns)):
            raise ValueError("Event unknowns contain a duplicate symbol.")
        if self.event_coordinate not in self.unknowns:
            raise ValueError("The event coordinate must be one of the unknowns.")
        law_names = tuple(law.name for law in self.state_laws)
        if len(law_names) != len(set(law_names)):
            raise ValueError("Each state-law name must be unique.")
        domain_symbols = tuple(domain.symbol for domain in self.domains)
        if len(domain_symbols) != len(set(domain_symbols)):
            raise ValueError("Each event-domain symbol may appear only once.")
        if not set(domain_symbols) <= set(self.unknowns):
            raise ValueError("Every event-domain symbol must be an unknown.")
        declared = set(self.unknowns)
        relations = tuple(law.relation for law in self.state_laws) + (
            self.event.relation,
        )
        if any(not relation.free_symbols <= declared for relation in relations):
            raise ValueError("An event relation contains an undeclared symbol.")


@dataclass(frozen=True)
class EventBranch:
    variables: tuple[Symbol, ...]
    values: tuple[Expr, ...]

    def value(self, symbol: Symbol) -> Expr:
        try:
            return self.values[self.variables.index(symbol)]
        except ValueError as error:
            raise KeyError(symbol) from error

    def substitution(self) -> dict[Symbol, Expr]:
        return dict(zip(self.variables, self.values))


@dataclass(frozen=True)
class EventConstructionResult:
    status: str
    request: EventProblem
    projection: Optional[PolynomialEliminationResult] = None
    algebraic_branches: tuple[EventBranch, ...] = ()
    admissible_branches: tuple[EventBranch, ...] = ()
    selected: Optional[EventBranch] = None
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[RelationObstruction] = None


def _refused(
    request: EventProblem,
    code: str,
    message: str,
    *,
    projection: Optional[PolynomialEliminationResult] = None,
) -> EventConstructionResult:
    return EventConstructionResult(
        status="refused",
        request=request,
        projection=projection,
        obstruction=RelationObstruction(code=code, message=message),
    )


def construct_event(request: EventProblem) -> EventConstructionResult:
    """Construct and physically filter a finite exact algebraic event.

    The event equation is generated by projecting supplied state laws together
    with a provenance-bearing zero predicate. Every algebraic branch must then
    lift to the full state; closed exact intervals select a unique physical branch
    or produce an explicit obstruction.
    """

    eliminated = tuple(
        symbol for symbol in request.unknowns if symbol != request.event_coordinate
    )
    relations = tuple(law.relation for law in request.state_laws) + (
        request.event.relation,
    )
    try:
        projection = eliminate_polynomial_relations(
            relations,
            eliminate=eliminated,
            retain=(request.event_coordinate,),
            target=request.event_coordinate,
            max_variables=request.max_variables,
        )
    except (CoercionFailed, ComputationFailed, PolynomialError, ValueError) as error:
        return _refused(
            request,
            "unsupported_relation_shape",
            f"The event is outside the exact rational polynomial backend: {error}",
        )

    if projection.status == "refused":
        return EventConstructionResult(
            status="refused",
            request=request,
            projection=projection,
            obstruction=projection.obstruction,
        )
    if projection.status == "inconsistent":
        return EventConstructionResult(
            status="no_event",
            request=request,
            projection=projection,
            obstruction=RelationObstruction(
                "no_algebraic_event",
                "The state laws and event predicate have no common state.",
            ),
        )
    if projection.status != "constrained":
        return _refused(
            request,
            "event_coordinate_not_constrained",
            "The supplied laws and predicate do not isolate the event coordinate.",
            projection=projection,
        )

    try:
        solved = solve_poly_system(relations, *request.unknowns)
    except (
        CoercionFailed,
        ComputationFailed,
        NotImplementedError,
        PolynomialError,
    ) as error:
        return _refused(
            request,
            "branch_solver_failed",
            f"Full algebraic branches could not be constructed: {error}",
            projection=projection,
        )
    if solved is None:
        return _refused(
            request,
            "nonfinite_event_set",
            "The event equations do not have a finite full-state solution set.",
            projection=projection,
        )

    branches = tuple(
        EventBranch(request.unknowns, tuple(sympify(value) for value in solution))
        for solution in solved
    )
    lifts_pass = all(
        all(
            simplify(relation.subs(branch.substitution())) == 0
            for relation in relations
        )
        for branch in branches
    )
    if not lifts_pass:
        return _refused(
            request,
            "branch_lift_failed",
            "At least one reported algebraic branch fails an original relation.",
            projection=projection,
        )

    admissible = []
    undecidable = False
    for branch in branches:
        if any(value.is_real is False for value in branch.values):
            continue
        if any(value.is_real is None for value in branch.values):
            undecidable = True
            continue
        checks = tuple(
            domain.contains(branch.value(domain.symbol)) for domain in request.domains
        )
        if any(check is None for check in checks):
            undecidable = True
        elif all(check is True for check in checks):
            admissible.append(branch)
    if undecidable:
        return _refused(
            request,
            "undecidable_branch_admissibility",
            "Exact reality or interval membership was undecidable for a branch.",
            projection=projection,
        )

    base_certificates = projection.certificates + (
        Certificate(
            name="full_state_branches_lift",
            passed=lifts_pass,
            witness=(
                "Every branch returned by the finite polynomial solver makes all "
                "state laws and the event predicate exactly zero."
            ),
        ),
    )
    admissible_tuple = tuple(admissible)
    if not admissible_tuple:
        return EventConstructionResult(
            status="no_event",
            request=request,
            projection=projection,
            algebraic_branches=branches,
            certificates=base_certificates,
            obstruction=RelationObstruction(
                "no_admissible_event",
                "No real lifted event branch lies in every declared physical interval.",
            ),
        )
    if len(admissible_tuple) > 1:
        return EventConstructionResult(
            status="ambiguous",
            request=request,
            projection=projection,
            algebraic_branches=branches,
            admissible_branches=admissible_tuple,
            certificates=base_certificates,
            obstruction=RelationObstruction(
                "ambiguous_event_branches",
                "Several real lifted event branches satisfy the declared intervals.",
            ),
        )

    selected = admissible_tuple[0]
    return EventConstructionResult(
        status="constructed",
        request=request,
        projection=projection,
        algebraic_branches=branches,
        admissible_branches=admissible_tuple,
        selected=selected,
        certificates=base_certificates
        + (
            Certificate(
                name="unique_admissible_event_branch",
                passed=True,
                witness=(
                    "Exactly one real full-state lift lies in every declared "
                    "physical interval."
                ),
            ),
        ),
    )
