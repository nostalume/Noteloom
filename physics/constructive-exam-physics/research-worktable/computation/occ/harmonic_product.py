"""Exact product of two same-frequency real harmonic signals."""

from dataclasses import dataclass
from typing import Optional

from sympy import (
    Expr,
    Symbol,
    conjugate,
    expand_complex,
    expand_trig,
    simplify,
    sympify,
    trigsimp,
)

from .harmonic import phasor_to_real_signal
from .records import Certificate


@dataclass(frozen=True)
class HarmonicProductRequest:
    """Two phasors whose real signals share one positive angular frequency."""

    problem_id: str
    product_name: str
    left_phasor: Expr
    right_phasor: Expr
    angular_frequency: Expr
    time: Symbol
    scale: Expr = sympify(1)

    def __post_init__(self) -> None:
        if not self.problem_id.strip() or not self.product_name.strip():
            raise ValueError("A harmonic product requires problem and product names.")
        left = sympify(self.left_phasor)
        right = sympify(self.right_phasor)
        omega = sympify(self.angular_frequency)
        scale = sympify(self.scale)
        if not isinstance(self.time, Symbol) or self.time.is_real is not True:
            raise TypeError("The time coordinate must be a real symbol.")
        if omega.is_positive is not True:
            raise ValueError(
                "The shared angular frequency must be explicitly positive."
            )
        if scale.is_real is not True:
            raise ValueError("The physical product scale must be explicitly real.")
        if self.time in (left.free_symbols | right.free_symbols | scale.free_symbols):
            raise ValueError("Phasors and scale must be time independent.")
        object.__setattr__(self, "left_phasor", left)
        object.__setattr__(self, "right_phasor", right)
        object.__setattr__(self, "angular_frequency", omega)
        object.__setattr__(self, "scale", scale)


@dataclass(frozen=True)
class HarmonicProductObstruction:
    code: str
    message: str
    next_action: str = ""


@dataclass(frozen=True)
class HarmonicProductResult:
    status: str
    request: HarmonicProductRequest
    dc_component: Optional[Expr] = None
    second_harmonic_phasor: Optional[Expr] = None
    time_signal: Optional[Expr] = None
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[HarmonicProductObstruction] = None


def _zero_trigonometric_residual(expression: Expr) -> Expr:
    return simplify(trigsimp(expand_trig(expression)))


def construct_harmonic_product(
    request: HarmonicProductRequest,
) -> HarmonicProductResult:
    """Construct the DC and second-harmonic channels of a real-signal product."""

    cross = expand_complex(request.left_phasor * conjugate(request.right_phasor))
    dc_component = simplify(request.scale * cross.as_real_imag()[0] / 2)
    second_harmonic = simplify(
        expand_complex(request.scale * request.left_phasor * request.right_phasor / 2)
    )
    time_signal = simplify(
        dc_component
        + phasor_to_real_signal(
            second_harmonic,
            2 * request.angular_frequency,
            request.time,
        )
    )
    direct_product = simplify(
        request.scale
        * phasor_to_real_signal(
            request.left_phasor, request.angular_frequency, request.time
        )
        * phasor_to_real_signal(
            request.right_phasor, request.angular_frequency, request.time
        )
    )
    residual = _zero_trigonometric_residual(direct_product - time_signal)
    real_residual = simplify(conjugate(time_signal) - time_signal)
    certificates = (
        Certificate(
            "harmonic_product_recovery",
            residual == 0,
            f"Direct real-signal product minus DC-plus-second-harmonic return: {residual}.",
        ),
        Certificate(
            "real_product_return",
            real_residual == 0,
            f"Returned product minus its complex conjugate: {-real_residual}.",
        ),
    )
    if not all(certificate.passed for certificate in certificates):
        return HarmonicProductResult(
            status="refused",
            request=request,
            dc_component=dc_component,
            second_harmonic_phasor=second_harmonic,
            time_signal=time_signal,
            certificates=certificates,
            obstruction=HarmonicProductObstruction(
                "harmonic_product_recovery_failed",
                "The generated channels did not reconstruct the admitted product.",
                "Inspect parameter reality and phasor convention.",
            ),
        )
    return HarmonicProductResult(
        status="constructed",
        request=request,
        dc_component=dc_component,
        second_harmonic_phasor=second_harmonic,
        time_signal=time_signal,
        certificates=certificates,
    )
