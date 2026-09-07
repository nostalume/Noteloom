"""Dependency-free exact Poisson certificate for the Coulomb hidden algebra.

The expression field consists of rational sums of

    x^a p^b s^q mu^u kappa^v,  s = x.x,  q in (1/2) Z.

It is deliberately small: it verifies the classical principal-symbol relations
used by the Coulomb benchmark.  It does not certify quantum ordering, domains, or
self-adjointness.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction

Triple = tuple[int, int, int]
Key = tuple[Triple, Triple, Fraction, int, int]


def _add_triples(a: Triple, b: Triple) -> Triple:
    return tuple(a[i] + b[i] for i in range(3))  # type: ignore[return-value]


@dataclass(frozen=True)
class Expr:
    terms: dict[Key, Fraction]

    def __post_init__(self) -> None:
        clean = {key: value for key, value in self.terms.items() if value}
        object.__setattr__(self, "terms", clean)

    @staticmethod
    def constant(value: int | Fraction) -> Expr:
        coefficient = Fraction(value)
        if not coefficient:
            return Expr({})
        return Expr({((0, 0, 0), (0, 0, 0), Fraction(0), 0, 0): coefficient})

    @staticmethod
    def monomial(
        *,
        x: Triple = (0, 0, 0),
        p: Triple = (0, 0, 0),
        s: Fraction = Fraction(0),
        mu: int = 0,
        kappa: int = 0,
        coefficient: int | Fraction = 1,
    ) -> Expr:
        return Expr({(x, p, s, mu, kappa): Fraction(coefficient)})

    def __add__(self, other: Expr) -> Expr:
        result = dict(self.terms)
        for key, value in other.terms.items():
            result[key] = result.get(key, Fraction(0)) + value
        return Expr(result)

    def __neg__(self) -> Expr:
        return Expr({key: -value for key, value in self.terms.items()})

    def __sub__(self, other: Expr) -> Expr:
        return self + (-other)

    def __mul__(self, other: Expr) -> Expr:
        result: dict[Key, Fraction] = {}
        for (xa, pa, sa, mua, ka), ca in self.terms.items():
            for (xb, pb, sb, mub, kb), cb in other.terms.items():
                key = (
                    _add_triples(xa, xb),
                    _add_triples(pa, pb),
                    sa + sb,
                    mua + mub,
                    ka + kb,
                )
                result[key] = result.get(key, Fraction(0)) + ca * cb
        return Expr(result)

    def scale(self, value: int | Fraction) -> Expr:
        return self * Expr.constant(value)

    def derivative_x(self, index: int) -> Expr:
        result = Expr.constant(0)
        for (x_power, p_power, s_power, mu_power, k_power), coefficient in self.terms.items():
            if x_power[index]:
                lowered = list(x_power)
                lowered[index] -= 1
                result += Expr.monomial(
                    x=tuple(lowered),  # type: ignore[arg-type]
                    p=p_power,
                    s=s_power,
                    mu=mu_power,
                    kappa=k_power,
                    coefficient=coefficient * x_power[index],
                )
            if s_power:
                raised = list(x_power)
                raised[index] += 1
                result += Expr.monomial(
                    x=tuple(raised),  # type: ignore[arg-type]
                    p=p_power,
                    s=s_power - 1,
                    mu=mu_power,
                    kappa=k_power,
                    coefficient=2 * coefficient * s_power,
                )
        return result

    def derivative_p(self, index: int) -> Expr:
        result = Expr.constant(0)
        for (x_power, p_power, s_power, mu_power, k_power), coefficient in self.terms.items():
            if p_power[index]:
                lowered = list(p_power)
                lowered[index] -= 1
                result += Expr.monomial(
                    x=x_power,
                    p=tuple(lowered),  # type: ignore[arg-type]
                    s=s_power,
                    mu=mu_power,
                    kappa=k_power,
                    coefficient=coefficient * p_power[index],
                )
        return result

    def vanishes_mod_radius(self) -> bool:
        """Test zero after imposing s=x_0^2+x_1^2+x_2^2 exactly."""
        groups: dict[
            tuple[Triple, int, int, Fraction], list[tuple[Triple, Fraction, Fraction]]
        ] = {}
        for (x_power, p_power, s_power, mu_power, k_power), coefficient in self.terms.items():
            floor = s_power.numerator // s_power.denominator
            fractional_part = s_power - floor
            group = (p_power, mu_power, k_power, fractional_part)
            groups.setdefault(group, []).append((x_power, s_power, coefficient))

        for values in groups.values():
            base = min(s_power for _, s_power, _ in values)
            polynomial: dict[Triple, Fraction] = {}
            for x_power, s_power, coefficient in values:
                exponent = s_power - base
                if exponent.denominator != 1 or exponent < 0:
                    raise AssertionError("incompatible radius powers")
                radial_polynomial: dict[Triple, Fraction] = {(0, 0, 0): Fraction(1)}
                for _ in range(int(exponent)):
                    expanded: dict[Triple, Fraction] = {}
                    for powers, value in radial_polynomial.items():
                        for index in range(3):
                            shifted = list(powers)
                            shifted[index] += 2
                            shifted_tuple = tuple(shifted)  # type: ignore[assignment]
                            expanded[shifted_tuple] = (
                                expanded.get(shifted_tuple, Fraction(0)) + value
                            )
                    radial_polynomial = expanded
                for radial_power, value in radial_polynomial.items():
                    power = _add_triples(x_power, radial_power)
                    polynomial[power] = polynomial.get(power, Fraction(0)) + coefficient * value
            if any(polynomial.values()):
                return False
        return True


ZERO = Expr.constant(0)
ONE = Expr.constant(1)
X = tuple(Expr.monomial(x=tuple(1 if i == j else 0 for i in range(3))) for j in range(3))
P = tuple(Expr.monomial(p=tuple(1 if i == j else 0 for i in range(3))) for j in range(3))
MU_INV = Expr.monomial(mu=-1)
KAPPA = Expr.monomial(kappa=1)
R_INV = Expr.monomial(s=Fraction(-1, 2))


def dot(a: Iterable[Expr], b: Iterable[Expr]) -> Expr:
    return sum((left * right for left, right in zip(a, b)), ZERO)


def cross(a: tuple[Expr, Expr, Expr], b: tuple[Expr, Expr, Expr]) -> tuple[Expr, Expr, Expr]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def poisson(left: Expr, right: Expr) -> Expr:
    result = ZERO
    for index in range(3):
        result += left.derivative_x(index) * right.derivative_p(index)
        result -= left.derivative_p(index) * right.derivative_x(index)
    return result


def epsilon(i: int, j: int, k: int) -> int:
    if len({i, j, k}) < 3:
        return 0
    return 1 if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


def eps_vector(i: int, j: int, vector: tuple[Expr, Expr, Expr]) -> Expr:
    return sum((vector[k].scale(epsilon(i, j, k)) for k in range(3)), ZERO)


def build_certificate() -> dict[str, object]:
    angular_momentum = cross(X, P)
    runge_lenz = tuple(
        component * MU_INV - KAPPA * X[index] * R_INV
        for index, component in enumerate(cross(P, angular_momentum))
    )
    hamiltonian = dot(P, P).scale(Fraction(1, 2)) * MU_INV - KAPPA * R_INV

    checks: dict[str, bool] = {}
    for i in range(3):
        checks[f"poisson(H,L[{i}])=0"] = poisson(
            hamiltonian, angular_momentum[i]
        ).vanishes_mod_radius()
        checks[f"poisson(H,A[{i}])=0"] = poisson(hamiltonian, runge_lenz[i]).vanishes_mod_radius()
        for j in range(3):
            checks[f"LL[{i},{j}]"] = (
                poisson(angular_momentum[i], angular_momentum[j])
                - eps_vector(i, j, angular_momentum)
            ).vanishes_mod_radius()
            checks[f"LA[{i},{j}]"] = (
                poisson(angular_momentum[i], runge_lenz[j]) - eps_vector(i, j, runge_lenz)
            ).vanishes_mod_radius()
            checks[f"AA[{i},{j}]"] = (
                poisson(runge_lenz[i], runge_lenz[j])
                + hamiltonian.scale(2) * MU_INV * eps_vector(i, j, angular_momentum)
            ).vanishes_mod_radius()

    checks["L.A=0"] = dot(angular_momentum, runge_lenz).vanishes_mod_radius()
    checks["A^2=kappa^2+(2H/mu)L^2"] = (
        dot(runge_lenz, runge_lenz)
        - KAPPA * KAPPA
        - hamiltonian.scale(2) * MU_INV * dot(angular_momentum, angular_momentum)
    ).vanishes_mod_radius()

    perturbed_hamiltonian = hamiltonian + Expr.monomial(s=Fraction(1))
    negative_control = {
        "adding_r_squared_breaks_hidden_vector": all(
            not poisson(perturbed_hamiltonian, component).vanishes_mod_radius()
            for component in runge_lenz
        )
    }

    return {
        "status": "Passed" if all(checks.values()) and all(negative_control.values()) else "Failed",
        "scope": "classical principal-symbol Coulomb algebra only",
        "convention": "{f,g}=d_x f d_p g-d_p f d_x g",
        "checks": checks,
        "negative_control": negative_control,
        "not_certified": [
            "quantum ordering and hbar^2 Casimir correction",
            "operator domains and self-adjointness",
            "existence and completeness of bound states",
        ],
    }


if __name__ == "__main__":
    certificate = build_certificate()
    print(json.dumps(certificate, indent=2, sort_keys=True))
    raise SystemExit(0 if certificate["status"] == "Passed" else 1)
