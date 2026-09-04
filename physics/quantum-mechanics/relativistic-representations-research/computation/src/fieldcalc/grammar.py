"""Generate bounded operation grammars from carrier laws and resources."""

from dataclasses import dataclass

from .rewrite import Polynomial, Refusal, Rejected, RewriteSystem, Rule


@dataclass(frozen=True)
class CarrierLaw:
    kind: str
    power: int

    def __post_init__(self):
        if self.kind not in {"symmetric", "exterior"}:
            raise ValueError(f"unsupported free-power law: {self.kind}")
        if self.power < 0:
            raise ValueError("power must be nonnegative")


def compile_grammar(
    law: CarrierLaw, resources: set[str], budget: int = 3
) -> RewriteSystem | Rejected:
    if law.kind == "symmetric" and "metric" not in resources:
        return Rejected(Refusal("missing metric resource", provenance="symmetric free power"))

    if law.kind == "symmetric":
        rules = (
            Rule(("A", "P"), Polynomial({("P", "A"): 1, ("Q",): 1}), "symmetric derivation law"),
            Rule(("T", "P"), Polynomial({("P", "T"): 1, ("A",): 2}), "metric trace law"),
        )
    else:
        rules = (
            Rule(("A", "P"), Polynomial({("P", "A"): -1, ("Q",): 1}), "exterior derivation law"),
            Rule(("P", "P"), Polynomial(), "exterior nilpotence"),
            Rule(("A", "A"), Polynomial(), "exterior nilpotence"),
        )
    return RewriteSystem(rules, budget=budget, provenance=f"{law.kind} power {law.power}")


def factor_first_order(wave_token: str, budget: int = 3) -> RewriteSystem:
    return RewriteSystem(
        (
            Rule(
                ("G", "G"),
                Polynomial.word(wave_token),
                "polarized first-order factorization",
            ),
        ),
        budget=budget,
        provenance="first-order factorization",
    )
