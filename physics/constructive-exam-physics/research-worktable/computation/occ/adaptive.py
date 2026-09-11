"""Obstruction-guided construction of a target relation from supplied laws.

This module selects laws; it does not infer physics from prose.  Its admissible
input is an unordered finite bag of provenance-bearing theorem contracts.  It
searches that bag by increasing packet size and asks the exact relation backend
whether eliminating the packet's hidden quantities constrains the requested
target.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Optional

from sympy import Symbol, count_ops
from sympy.polys.polyerrors import CoercionFailed, PolynomialError

from .problem import PhysicalLaw
from .relation import PolynomialEliminationResult, eliminate_polynomial_relations


@dataclass(frozen=True)
class AdaptiveRelationRequest:
    """A target and resource budget, independent of any expected answer."""

    problem_id: str
    laws: tuple[PhysicalLaw, ...]
    givens: tuple[Symbol, ...]
    target: Symbol
    max_selected_laws: int = 6
    max_attempts: int = 128
    max_variables: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.problem_id.strip():
            raise ValueError("An adaptive request requires a problem id.")
        if not self.laws:
            raise ValueError("An adaptive request requires at least one law.")
        if any(not isinstance(law, PhysicalLaw) for law in self.laws):
            raise TypeError("laws accepts PhysicalLaw objects only.")
        names = tuple(law.name for law in self.laws)
        if len(names) != len(set(names)):
            raise ValueError("Each supplied physical law name must be unique.")
        if any(not isinstance(given, Symbol) for given in self.givens):
            raise TypeError("givens accepts SymPy Symbol objects only.")
        if len(self.givens) != len(set(self.givens)):
            raise ValueError("givens contains a duplicate symbol.")
        if not isinstance(self.target, Symbol):
            raise TypeError("target must be a SymPy Symbol.")
        if self.target in self.givens:
            raise ValueError("The target cannot also be a supplied given.")
        for name, value in (
            ("max_selected_laws", self.max_selected_laws),
            ("max_attempts", self.max_attempts),
        ):
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ValueError(f"{name} must be a positive integer.")
        if self.max_variables is not None and (
            not isinstance(self.max_variables, int)
            or isinstance(self.max_variables, bool)
            or self.max_variables < 1
        ):
            raise ValueError("max_variables must be a positive integer or None.")


@dataclass(frozen=True)
class AdaptiveObstruction:
    code: str
    message: str
    next_action: str
    witness: str = ""


@dataclass(frozen=True)
class AdaptiveConstructionResult:
    status: str
    request: AdaptiveRelationRequest
    selected_laws: tuple[PhysicalLaw, ...] = ()
    candidate_packets: tuple[tuple[str, ...], ...] = ()
    elimination: Optional[PolynomialEliminationResult] = None
    attempted_subsets: int = 0
    obstruction: Optional[AdaptiveObstruction] = None


@dataclass(frozen=True)
class _Candidate:
    laws: tuple[PhysicalLaw, ...]
    elimination: PolynomialEliminationResult

    @property
    def packet(self) -> tuple[str, ...]:
        return tuple(law.name for law in self.laws)

    @property
    def signature(self) -> tuple[str, ...]:
        # Reduced lexicographic Groebner bases over QQ are canonical for a fixed
        # variable order.  All attempts use the same retained order.
        return tuple(str(relation) for relation in self.elimination.projected_relations)

    @property
    def cost(self) -> tuple[int, tuple[str, ...]]:
        return (
            sum(int(count_ops(law.relation)) for law in self.laws),
            self.packet,
        )


def _target_component(
    laws: tuple[PhysicalLaw, ...], target: Symbol
) -> tuple[PhysicalLaw, ...]:
    """Return the law component connected to the target by shared quantities."""

    reached_symbols = {target}
    reached_laws: set[int] = set()
    changed = True
    while changed:
        changed = False
        for index, law in enumerate(laws):
            if index in reached_laws:
                continue
            if law.relation.free_symbols & reached_symbols:
                reached_laws.add(index)
                reached_symbols.update(law.relation.free_symbols)
                changed = True
    return tuple(law for index, law in enumerate(laws) if index in reached_laws)


def _refusal(
    request: AdaptiveRelationRequest,
    *,
    attempted: int,
    code: str,
    message: str,
    next_action: str,
    witness: str = "",
    packets: tuple[tuple[str, ...], ...] = (),
) -> AdaptiveConstructionResult:
    return AdaptiveConstructionResult(
        status="refused",
        request=request,
        candidate_packets=packets,
        attempted_subsets=attempted,
        obstruction=AdaptiveObstruction(
            code=code,
            message=message,
            next_action=next_action,
            witness=witness,
        ),
    )


def construct_target_relation(
    request: AdaptiveRelationRequest,
) -> AdaptiveConstructionResult:
    """Find a smallest supplied-law packet that constrains ``request.target``.

    Search is exhaustive only inside the declared law-count, attempt, variable,
    polynomial, and supplied-law boundaries.  The first successful packet size is
    therefore certified minimal within those boundaries.  Distinct projected
    ideals at that size are returned as ambiguity rather than silently ranked.
    """

    component = _target_component(request.laws, request.target)
    if not component:
        return _refusal(
            request,
            attempted=0,
            code="no_target_path",
            message="No supplied physical law mentions the requested target.",
            next_action=(
                "Construct or supply a provenance-bearing law that connects the "
                "target to measurable or given quantities."
            ),
        )

    retain = request.givens + (request.target,)
    max_size = min(request.max_selected_laws, len(component))
    attempted = 0
    unsupported_packets: list[tuple[str, ...]] = []
    variable_budget_packets: list[tuple[str, ...]] = []

    for size in range(1, max_size + 1):
        candidates: list[_Candidate] = []
        for selected in combinations(component, size):
            free = set().union(*(law.relation.free_symbols for law in selected))
            if request.target not in free:
                continue
            if attempted >= request.max_attempts:
                return _refusal(
                    request,
                    attempted=attempted,
                    code="search_budget_exceeded",
                    message=(
                        "The attempt budget ended before all packets at the current "
                        "minimality level were checked."
                    ),
                    next_action="Raise max_attempts or prune the supplied law bag.",
                    witness=f"stopped while checking packets of {size} laws",
                    packets=tuple(candidate.packet for candidate in candidates),
                )

            attempted += 1
            hidden = tuple(sorted(free - set(retain), key=lambda symbol: symbol.name))
            packet = tuple(law.name for law in selected)
            try:
                elimination = eliminate_polynomial_relations(
                    tuple(law.relation for law in selected),
                    eliminate=hidden,
                    retain=retain,
                    target=request.target,
                    max_variables=request.max_variables,
                )
            except (CoercionFailed, PolynomialError):
                unsupported_packets.append(packet)
                continue

            if elimination.status == "constrained":
                candidates.append(_Candidate(selected, elimination))
            elif (
                elimination.status == "refused"
                and elimination.obstruction is not None
                and elimination.obstruction.code == "variable_budget_exceeded"
            ):
                variable_budget_packets.append(packet)

        if candidates:
            by_signature: dict[tuple[str, ...], list[_Candidate]] = {}
            for candidate in candidates:
                by_signature.setdefault(candidate.signature, []).append(candidate)
            packets = tuple(candidate.packet for candidate in candidates)
            if len(by_signature) > 1:
                return _refusal(
                    request,
                    attempted=attempted,
                    code="ambiguous_minimal_packets",
                    message=(
                        "Different smallest supplied-law packets imply different "
                        "retained relations for the target."
                    ),
                    next_action=(
                        "Use regime, sign, dimensional, or provenance evidence to "
                        "reject at least one competing packet."
                    ),
                    witness="; ".join(" + ".join(packet) for packet in packets),
                    packets=packets,
                )

            chosen = min(candidates, key=lambda candidate: candidate.cost)
            return AdaptiveConstructionResult(
                status="constructed",
                request=request,
                selected_laws=chosen.laws,
                candidate_packets=packets,
                elimination=chosen.elimination,
                attempted_subsets=attempted,
            )

    if max_size < len(component) or variable_budget_packets:
        reasons = []
        if max_size < len(component):
            reasons.append(
                f"law-count cap {request.max_selected_laws} is below the "
                f"{len(component)}-law target component"
            )
        if variable_budget_packets:
            reasons.append(
                f"{len(variable_budget_packets)} packet(s) exceeded max_variables"
            )
        return _refusal(
            request,
            attempted=attempted,
            code="search_budget_exceeded",
            message="No target constraint was certified inside the resource budget.",
            next_action=(
                "Raise the named budget or reduce the law bag using independently "
                "justified regime information."
            ),
            witness="; ".join(reasons),
        )

    if unsupported_packets:
        return _refusal(
            request,
            attempted=attempted,
            code="unsupported_relation_shape",
            message=(
                "No target constraint was certified, and at least one necessary "
                "candidate lies outside exact rational-polynomial elimination."
            ),
            next_action=(
                "Route transcendental, inequality, differential, integral, or "
                "piecewise laws to a matching typed backend."
            ),
            witness="; ".join(" + ".join(packet) for packet in unsupported_packets),
        )

    component_symbols = set().union(*(law.relation.free_symbols for law in component))
    if request.givens and component_symbols.isdisjoint(request.givens):
        return _refusal(
            request,
            attempted=attempted,
            code="disconnected_target",
            message=(
                "The target-connected law component contains none of the supplied "
                "givens and does not constrain the target by itself."
            ),
            next_action=(
                "Supply a bridge law or initial/boundary datum connecting this "
                "component to the measured input."
            ),
            witness=("target component: " + ", ".join(law.name for law in component)),
        )

    return _refusal(
        request,
        attempted=attempted,
        code="target_not_constrained",
        message=(
            "Every admissible target-connected packet was checked, but hidden "
            "quantities remain free after exact elimination."
        ),
        next_action=(
            "Supply one more independent physical relation, an initial/boundary "
            "condition, or weaken the requested observable."
        ),
        witness=f"exhausted {attempted} target-containing packet(s)",
    )
