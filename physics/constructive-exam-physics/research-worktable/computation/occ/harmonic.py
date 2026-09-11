"""Exact finite linear phasor construction with physical-signal return."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sympy import (
    EmptySet,
    Expr,
    Symbol,
    conjugate,
    cos,
    expand_complex,
    linear_eq_to_matrix,
    linsolve,
    simplify,
    sin,
    sqrt,
    sympify,
)
from sympy.solvers.solveset import NonlinearError

from .records import Certificate


@dataclass(frozen=True)
class HarmonicObservable:
    """One requested complex amplitude and an optional phase reference."""

    name: str
    expression: Expr
    reference: Optional[Expr] = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("A harmonic observable requires a name.")
        object.__setattr__(self, "expression", sympify(self.expression))
        if self.reference is not None:
            object.__setattr__(self, "reference", sympify(self.reference))


@dataclass(frozen=True)
class HarmonicResponseRequest:
    """Exact phasor laws under the convention Re(z exp(i omega t))."""

    problem_id: str
    laws: tuple[Expr, ...]
    unknowns: tuple[Symbol, ...]
    observables: tuple[HarmonicObservable, ...]
    angular_frequency: Expr
    time: Symbol
    max_unknowns: int = 8

    def __post_init__(self) -> None:
        if not self.problem_id.strip():
            raise ValueError("A harmonic response requires a problem id.")
        laws = tuple(sympify(law) for law in self.laws)
        unknowns = tuple(self.unknowns)
        observables = tuple(self.observables)
        omega = sympify(self.angular_frequency)
        if not laws:
            raise ValueError("At least one phasor law is required.")
        if not unknowns or any(not isinstance(item, Symbol) for item in unknowns):
            raise TypeError("Harmonic unknowns must be a nonempty tuple of symbols.")
        if len(unknowns) != len(set(unknowns)):
            raise ValueError("Harmonic unknowns must be unique.")
        if not observables or any(
            not isinstance(item, HarmonicObservable) for item in observables
        ):
            raise TypeError("At least one HarmonicObservable is required.")
        if not isinstance(self.time, Symbol) or self.time.is_real is not True:
            raise TypeError("The time coordinate must be a real symbol.")
        if omega.is_real is not True:
            raise ValueError("The angular frequency must be explicitly real.")
        expressions = (
            laws
            + tuple(item.expression for item in observables)
            + tuple(
                item.reference for item in observables if item.reference is not None
            )
        )
        if any(self.time in expression.free_symbols for expression in expressions):
            raise ValueError("Phasor laws and observables must be time independent.")
        if (
            not isinstance(self.max_unknowns, int)
            or isinstance(self.max_unknowns, bool)
            or self.max_unknowns < 1
        ):
            raise ValueError("max_unknowns must be a positive integer.")
        object.__setattr__(self, "laws", laws)
        object.__setattr__(self, "unknowns", unknowns)
        object.__setattr__(self, "observables", observables)
        object.__setattr__(self, "angular_frequency", omega)


@dataclass(frozen=True)
class HarmonicObservableResult:
    name: str
    phasor: Expr
    magnitude_squared: Expr
    time_signal: Expr
    reference_phase_cosine: Optional[Expr] = None


@dataclass(frozen=True)
class HarmonicObstruction:
    code: str
    message: str
    next_action: str = ""


@dataclass(frozen=True)
class HarmonicResponseResult:
    status: str
    request: HarmonicResponseRequest
    solution: tuple[tuple[Symbol, Expr], ...] = ()
    observables: tuple[HarmonicObservableResult, ...] = ()
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[HarmonicObstruction] = None


def phasor_magnitude_squared(phasor: Expr) -> Expr:
    """Return the exact squared modulus without discarding phase beforehand."""

    value = sympify(phasor)
    return simplify(expand_complex(value * conjugate(value)))


def phasor_to_real_signal(phasor: Expr, angular_frequency: Expr, time: Symbol) -> Expr:
    """Reconstruct Re(z exp(i omega t)) from an exact phasor."""

    real_part, imaginary_part = expand_complex(sympify(phasor)).as_real_imag()
    phase = sympify(angular_frequency) * time
    return simplify(real_part * cos(phase) - imaginary_part * sin(phase))


def relative_phase_cosine(reference: Expr, response: Expr) -> Expr:
    """Return the exact cosine of the response-reference phase difference."""

    reference = sympify(reference)
    response = sympify(response)
    numerator = expand_complex(reference * conjugate(response)).as_real_imag()[0]
    denominator = sqrt(
        phasor_magnitude_squared(reference) * phasor_magnitude_squared(response)
    )
    if denominator == 0:
        raise ValueError("Relative phase is undefined for a zero phasor.")
    return simplify(numerator / denominator)


def _refused(
    request: HarmonicResponseRequest,
    code: str,
    message: str,
    next_action: str,
) -> HarmonicResponseResult:
    return HarmonicResponseResult(
        status="refused",
        request=request,
        obstruction=HarmonicObstruction(code, message, next_action),
    )


def construct_harmonic_response(
    request: HarmonicResponseRequest,
) -> HarmonicResponseResult:
    """Solve a bounded exact linear phasor system and return physical observables."""

    if len(request.unknowns) > request.max_unknowns:
        return _refused(
            request,
            "harmonic_unknown_budget_exceeded",
            "The phasor system exceeds the declared unknown budget.",
            "Raise max_unknowns or reduce the admitted response model.",
        )
    try:
        matrix, right_hand_side = linear_eq_to_matrix(request.laws, request.unknowns)
    except (NonlinearError, ValueError) as error:
        return _refused(
            request,
            "nonlinear_phasor_law",
            f"The admitted harmonic laws are not linear in the phasor unknowns: {error}",
            "Supply a finite linear response law or use a nonlinear harmonic solver.",
        )
    solutions = linsolve((matrix, right_hand_side), request.unknowns)
    if solutions == EmptySet:
        return _refused(
            request,
            "inconsistent_phasor_laws",
            "The admitted phasor laws have no common response.",
            "Inspect source conventions and incompatible boundary or circuit laws.",
        )
    values = tuple(solutions)
    if len(values) != 1 or any(
        value.free_symbols & set(request.unknowns) for value in values[0]
    ):
        return _refused(
            request,
            "underdetermined_phasor_response",
            "The admitted phasor laws do not determine every declared unknown.",
            "Add an independent physical or boundary law.",
        )
    solution = tuple(zip(request.unknowns, values[0]))
    substitution = dict(solution)
    results = []
    for observable in request.observables:
        phasor = simplify(observable.expression.subs(substitution))
        phase_cosine = None
        if observable.reference is not None:
            try:
                phase_cosine = relative_phase_cosine(
                    observable.reference.subs(substitution),
                    phasor,
                )
            except ValueError as error:
                return _refused(
                    request,
                    "undefined_phase_reference",
                    str(error),
                    "Use a certified nonzero reference or omit relative phase.",
                )
        results.append(
            HarmonicObservableResult(
                name=observable.name,
                phasor=phasor,
                magnitude_squared=phasor_magnitude_squared(phasor),
                time_signal=phasor_to_real_signal(
                    phasor, request.angular_frequency, request.time
                ),
                reference_phase_cosine=phase_cosine,
            )
        )
    residuals = tuple(
        simplify(expand_complex(law.subs(substitution))) for law in request.laws
    )
    unknown_free = all(
        result.phasor.free_symbols.isdisjoint(request.unknowns) for result in results
    )
    real_returns = all(
        simplify(conjugate(result.time_signal) - result.time_signal) == 0
        for result in results
    )
    certificates = (
        Certificate(
            "phasor_law_recovery",
            all(residual == 0 for residual in residuals),
            f"Exact substituted law residuals: {residuals}.",
        ),
        Certificate(
            "phasor_unknowns_eliminated",
            unknown_free,
            "Every requested phasor is free of declared response unknowns.",
        ),
        Certificate(
            "real_signal_return",
            real_returns,
            "Each returned signal equals its complex conjugate under declared real data.",
        ),
    )
    if not all(certificate.passed for certificate in certificates):
        return HarmonicResponseResult(
            status="refused",
            request=request,
            solution=solution,
            observables=tuple(results),
            certificates=certificates,
            obstruction=HarmonicObstruction(
                "harmonic_recovery_failed",
                "The exact response failed a required recovery certificate.",
                "Inspect parameter reality, source conventions, and target expressions.",
            ),
        )
    return HarmonicResponseResult(
        status="constructed",
        request=request,
        solution=solution,
        observables=tuple(results),
        certificates=certificates,
    )
