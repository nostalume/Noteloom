from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Optional

from sympy import Poly, QQ, Symbol, groebner, solve, sympify
from sympy.core.expr import Expr
from sympy.polys.polytools import GroebnerBasis

from .records import Certificate


@dataclass(frozen=True)
class RelationObstruction:
    code: str
    message: str


@dataclass(frozen=True)
class PolynomialEliminationResult:
    status: str
    eliminated: tuple[Symbol, ...]
    retained: tuple[Symbol, ...]
    target: Symbol
    projected_relations: tuple[Expr, ...] = ()
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[RelationObstruction] = None
    _basis: Optional[GroebnerBasis] = field(default=None, repr=False, compare=False)

    def implies(self, relation: Any) -> bool:
        """Return whether a polynomial relation belongs to the supplied law ideal."""
        if self._basis is None:
            raise ValueError("A refused elimination has no relation ideal.")
        expression = sympify(relation)
        declared = set(self.eliminated) | set(self.retained)
        if not expression.free_symbols <= declared:
            raise ValueError("The queried relation contains an undeclared symbol.")
        _, remainder = self._basis.reduce(expression)
        return remainder == 0

    def target_candidates(self) -> tuple[Expr, ...]:
        """Solve the projected target relations without selecting a physical branch."""
        target_relations = tuple(
            relation
            for relation in self.projected_relations
            if self.target in relation.free_symbols
        )
        if not target_relations:
            return ()
        candidates = solve(target_relations, self.target, dict=False)
        if isinstance(candidates, dict):
            value = candidates.get(self.target)
            return () if value is None else (value,)
        return tuple(
            candidate[0]
            if isinstance(candidate, tuple) and len(candidate) == 1
            else candidate
            for candidate in candidates
        )


def _symbols(
    values: Sequence[Symbol],
    name: str,
    *,
    allow_empty: bool = False,
) -> tuple[Symbol, ...]:
    result = tuple(values)
    if not result and not allow_empty:
        raise ValueError(f"{name} must contain at least one symbol.")
    if any(not isinstance(value, Symbol) for value in result):
        raise TypeError(f"{name} accepts SymPy Symbol objects only.")
    if len(set(result)) != len(result):
        raise ValueError(f"{name} contains a duplicate symbol.")
    return result


def eliminate_polynomial_relations(
    relations: Sequence[Any],
    *,
    eliminate: Sequence[Symbol],
    retain: Sequence[Symbol],
    target: Symbol,
    max_variables: Optional[int] = None,
) -> PolynomialEliminationResult:
    """Compute retained consequences of an exact rational polynomial law system.

    Lexicographic elimination removes ``eliminate`` variables. The returned
    relations are the elimination-ideal basis on ``retain``. A target relation can
    have several roots; physical branch selection remains an explicit obligation.
    """
    eliminated = _symbols(eliminate, "eliminate", allow_empty=True)
    retained = _symbols(retain, "retain")
    if set(eliminated) & set(retained):
        raise ValueError("Eliminated and retained symbols must be disjoint.")
    if not isinstance(target, Symbol) or target not in retained:
        raise ValueError("target must be one of the retained symbols.")
    if max_variables is not None and (
        not isinstance(max_variables, int)
        or isinstance(max_variables, bool)
        or max_variables < 1
    ):
        raise ValueError("max_variables must be a positive integer or None.")

    variable_order = eliminated + retained
    if max_variables is not None and len(variable_order) > max_variables:
        return PolynomialEliminationResult(
            status="refused",
            eliminated=eliminated,
            retained=retained,
            target=target,
            obstruction=RelationObstruction(
                code="variable_budget_exceeded",
                message=(
                    "The declared relation system exceeds the variable budget "
                    "before elimination."
                ),
            ),
        )

    expressions = tuple(sympify(relation) for relation in relations)
    if not expressions:
        raise ValueError("At least one physical relation is required.")
    declared = set(variable_order)
    undeclared = (
        set().union(*(expression.free_symbols for expression in expressions)) - declared
    )
    if undeclared:
        raise ValueError("A physical relation contains an undeclared symbol.")

    # Poly construction is the admission check: only exact polynomials over QQ
    # enter this bounded kernel. Parameters are declared as retained variables.
    polynomials = tuple(
        Poly(expression, *variable_order, domain=QQ) for expression in expressions
    )
    basis = groebner(polynomials, *variable_order, order="lex", domain=QQ)
    eliminated_set = set(eliminated)
    projected = tuple(
        polynomial.monic().as_expr()
        for polynomial in basis.polys
        if polynomial.as_expr().free_symbols.isdisjoint(eliminated_set)
    )

    if any(not relation.free_symbols and relation != 0 for relation in projected):
        status = "inconsistent"
        obstruction = RelationObstruction(
            code="inconsistent_relations",
            message="The supplied physical relations have no common state.",
        )
    elif any(target in relation.free_symbols for relation in projected):
        status = "constrained"
        obstruction = None
    else:
        status = "underdetermined"
        obstruction = RelationObstruction(
            code="target_not_constrained",
            message=(
                "After hidden quantities were eliminated, no retained relation "
                "constrains the requested target."
            ),
        )

    certificates = (
        Certificate(
            name="hidden_symbols_eliminated",
            passed=all(
                relation.free_symbols.isdisjoint(eliminated_set)
                for relation in projected
            ),
            witness=(
                "Every projected relation is expressed only in retained quantities."
            ),
        ),
        Certificate(
            name="elimination_ideal_constructed",
            passed=True,
            witness=(
                "A lexicographic Groebner basis over QQ supplies the exact "
                "elimination-ideal intersection with the retained polynomial ring."
            ),
        ),
    )
    return PolynomialEliminationResult(
        status=status,
        eliminated=eliminated,
        retained=retained,
        target=target,
        projected_relations=projected,
        certificates=certificates,
        obstruction=obstruction,
        _basis=basis,
    )
