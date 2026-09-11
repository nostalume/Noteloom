from dataclasses import dataclass
from typing import Any, Optional

from sympy import Symbol, sympify
from sympy.core.expr import Expr

from .relation import PolynomialEliminationResult, eliminate_polynomial_relations


@dataclass(frozen=True)
class PhysicalLaw:
    name: str
    relation: Expr
    provenance: str

    def __init__(self, name: str, relation: Any, provenance: str) -> None:
        object.__setattr__(self, "name", name.strip())
        object.__setattr__(self, "relation", sympify(relation))
        object.__setattr__(self, "provenance", provenance.strip())
        if not self.name or not self.provenance:
            raise ValueError("A physical law requires a name and provenance.")


@dataclass(frozen=True)
class TargetRequest:
    name: str
    target: Symbol
    eliminate: tuple[Symbol, ...]
    retain: tuple[Symbol, ...]
    law_names: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("A target request requires a name.")
        if self.target not in self.retain:
            raise ValueError("A target request must retain its target symbol.")
        if len(self.law_names) != len(set(self.law_names)):
            raise ValueError("A target request contains a duplicate law name.")


@dataclass(frozen=True)
class PolynomialProblemPacket:
    problem_id: str
    pdf_page: int
    laws: tuple[PhysicalLaw, ...]
    targets: tuple[TargetRequest, ...]
    regime: tuple[str, ...]
    branch_obligations: tuple[str, ...]
    max_variables: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.problem_id.strip():
            raise ValueError("A problem packet requires an id.")
        if self.pdf_page < 1:
            raise ValueError("A problem packet requires a positive PDF page.")
        if not self.laws or not self.targets:
            raise ValueError("A problem packet requires laws and targets.")
        law_names = tuple(law.name for law in self.laws)
        if len(law_names) != len(set(law_names)):
            raise ValueError("Each physical law name must be unique within a packet.")
        names = tuple(request.name for request in self.targets)
        if len(names) != len(set(names)):
            raise ValueError("Each target name must be unique within a problem packet.")
        available = set(law_names)
        for request in self.targets:
            missing = set(request.law_names) - available
            if missing:
                raise ValueError(
                    f"Target {request.name} selects unknown laws: {sorted(missing)}."
                )


@dataclass(frozen=True)
class NamedTargetResult:
    name: str
    elimination: PolynomialEliminationResult


@dataclass(frozen=True)
class PolynomialProblemResult:
    status: str
    packet: PolynomialProblemPacket
    targets: tuple[NamedTargetResult, ...]

    def target(self, name: str) -> PolynomialEliminationResult:
        for result in self.targets:
            if result.name == name:
                return result.elimination
        raise KeyError(name)


def compile_polynomial_problem(
    packet: PolynomialProblemPacket,
) -> PolynomialProblemResult:
    """Project every declared target while preserving the physical-law packet."""

    laws_by_name = {law.name: law for law in packet.laws}
    targets = tuple(
        NamedTargetResult(
            name=request.name,
            elimination=eliminate_polynomial_relations(
                tuple(laws_by_name[name].relation for name in request.law_names)
                if request.law_names
                else tuple(law.relation for law in packet.laws),
                eliminate=request.eliminate,
                retain=request.retain,
                target=request.target,
                max_variables=packet.max_variables,
            ),
        )
        for request in packet.targets
    )
    constrained = sum(result.elimination.status == "constrained" for result in targets)
    if constrained == len(targets):
        status = "complete"
    elif constrained:
        status = "partial"
    else:
        status = "refused"
    return PolynomialProblemResult(status=status, packet=packet, targets=targets)
