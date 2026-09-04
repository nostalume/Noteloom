"""Bounded noncommutative words with explicit semantic rewrite policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from sympy import Rational

Word = tuple[str, ...]


@dataclass(frozen=True)
class Refusal:
    reason: str
    residual: tuple = ()
    provenance: str = ""


@dataclass(frozen=True)
class Rejected:
    refusal: Refusal
    accepted: bool = False


class Polynomial:
    """A small exact linear combination of semantic operation words."""

    def __init__(self, terms: Mapping[Word, object] | None = None):
        merged: dict[Word, Rational] = {}
        for word, coefficient in (terms or {}).items():
            value = Rational(coefficient)
            if value:
                merged[tuple(word)] = merged.get(tuple(word), Rational(0)) + value
        self.terms = {word: value for word, value in merged.items() if value}

    @classmethod
    def word(cls, *tokens: str) -> "Polynomial":
        return cls({tuple(tokens): 1})

    def __add__(self, other: "Polynomial") -> "Polynomial":
        terms = dict(self.terms)
        for word, coefficient in other.terms.items():
            terms[word] = terms.get(word, Rational(0)) + coefficient
        return Polynomial(terms)

    def scale(self, coefficient: object) -> "Polynomial":
        return Polynomial({word: Rational(coefficient) * value for word, value in self.terms.items()})

    def surround(self, prefix: Word, suffix: Word) -> "Polynomial":
        return Polynomial({prefix + word + suffix: value for word, value in self.terms.items()})

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Polynomial) and self.terms == other.terms

    def __repr__(self) -> str:
        return f"Polynomial({self.terms!r})"


@dataclass(frozen=True)
class Rule:
    pattern: Word
    replacement: Polynomial
    origin: str


@dataclass(frozen=True)
class Normalization:
    normal_form: Polynomial
    origin: str
    accepted: bool = True


class RewriteSystem:
    def __init__(self, rules: Iterable[Rule], budget: int = 3, provenance: str = ""):
        self.rules = tuple(rules)
        self.budget = budget
        self.provenance = provenance
        self.accepted = True
        self.refusal = None

    def _rewrite_once(self, polynomial: Polynomial) -> tuple[Polynomial, str | None]:
        output = Polynomial()
        applied_origin = None
        changed = False
        for word, coefficient in polynomial.terms.items():
            replaced = False
            for rule in self.rules:
                width = len(rule.pattern)
                for index in range(len(word) - width + 1):
                    if word[index : index + width] == rule.pattern:
                        term = rule.replacement.surround(word[:index], word[index + width :])
                        output = output + term.scale(coefficient)
                        applied_origin = rule.origin
                        replaced = changed = True
                        break
                if replaced:
                    break
            if not replaced:
                output = output + Polynomial({word: coefficient})
        return output, applied_origin if changed else None

    def try_normalize(self, polynomial: Polynomial) -> Normalization | Rejected:
        if any(len(word) > self.budget for word in polynomial.terms):
            return Rejected(Refusal("word budget exceeded", provenance=self.provenance))
        current = polynomial
        origins: list[str] = []
        for _ in range(max(1, self.budget * max(1, len(self.rules)) * 4)):
            updated, origin = self._rewrite_once(current)
            if origin is None:
                return Normalization(updated, "; ".join(dict.fromkeys(origins)))
            origins.append(origin)
            current = updated
        return Rejected(Refusal("rewrite budget exhausted", tuple(current.terms), self.provenance))

    def normalize(self, polynomial: Polynomial) -> Polynomial:
        result = self.try_normalize(polynomial)
        if not result.accepted:
            raise ValueError(result.refusal.reason)
        return result.normal_form

    def relation_certificate(self, word: Word) -> Normalization | Rejected:
        return self.try_normalize(Polynomial.word(*word))
