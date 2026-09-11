"""Exact Coulomb-impulse projection for a planar point-particle impact."""

from dataclasses import dataclass
from typing import Optional

from sympy import Expr, Piecewise, S, simplify, sqrt, sympify
from sympy.logic.boolalg import Boolean

from .records import Certificate


@dataclass(frozen=True)
class FrictionalImpactRequest:
    problem_id: str
    mass: Expr
    incoming_normal_speed: Expr
    incoming_tangential_speed: Expr
    friction_coefficient: Expr
    restitution_coefficient: Expr

    def __post_init__(self) -> None:
        if not self.problem_id.strip():
            raise ValueError("An impact request requires a problem id.")
        values = tuple(
            sympify(value)
            for value in (
                self.mass,
                self.incoming_normal_speed,
                self.incoming_tangential_speed,
                self.friction_coefficient,
                self.restitution_coefficient,
            )
        )
        mass, normal, tangent, friction, restitution = values
        if mass.is_positive is not True:
            raise ValueError("Impact mass must be positive.")
        if normal.is_positive is not True:
            raise ValueError("Incoming normal speed must be positive.")
        if tangent.is_nonnegative is not True:
            raise ValueError("Incoming tangential speed must be nonnegative.")
        if friction.is_nonnegative is not True:
            raise ValueError("The friction coefficient must be nonnegative.")
        if restitution.is_positive is not True:
            raise ValueError("The restitution coefficient must be positive.")
        for name, value in zip(
            (
                "mass",
                "incoming_normal_speed",
                "incoming_tangential_speed",
                "friction_coefficient",
                "restitution_coefficient",
            ),
            values,
        ):
            object.__setattr__(self, name, value)


@dataclass(frozen=True)
class ImpactRegime:
    name: str
    condition: Boolean
    tangential_impulse: Expr
    outgoing_tangential_speed: Expr
    outgoing_speed: Expr
    reflection_tangent: Expr


@dataclass(frozen=True)
class FrictionalImpactResult:
    status: str
    request: FrictionalImpactRequest
    normal_impulse: Expr
    friction_impulse_limit: Expr
    outgoing_normal_speed: Expr
    sticking: ImpactRegime
    sliding: ImpactRegime
    outgoing_tangential_speed: Expr
    outgoing_speed: Expr
    reflection_tangent: Expr
    selected_regime: Optional[str]
    certificates: tuple[Certificate, ...]
    obstruction: None = None


def _certificate(name: str, residual: Expr, witness: str) -> Certificate:
    return Certificate(name, simplify(residual) == 0, witness)


def construct_frictional_impact(
    request: FrictionalImpactRequest,
) -> FrictionalImpactResult:
    """Project the no-slip impulse onto the Coulomb interval."""

    mass = request.mass
    normal = request.incoming_normal_speed
    tangent = request.incoming_tangential_speed
    friction = request.friction_coefficient
    restitution = request.restitution_coefficient

    normal_impulse = mass * (1 + restitution) * normal
    impulse_limit = friction * normal_impulse
    threshold = simplify(impulse_limit / mass)
    outgoing_normal = restitution * normal
    sticking_condition = tangent <= threshold
    sliding_condition = tangent > threshold

    sticking_impulse = -mass * tangent
    sliding_impulse = -impulse_limit
    sliding_tangent = simplify(tangent + sliding_impulse / mass)
    sticking_speed = outgoing_normal
    sliding_speed = sqrt(outgoing_normal**2 + sliding_tangent**2)
    sliding_reflection_tangent = simplify(sliding_tangent / outgoing_normal)

    sticking = ImpactRegime(
        "sticking",
        sticking_condition,
        sticking_impulse,
        S.Zero,
        sticking_speed,
        S.Zero,
    )
    sliding = ImpactRegime(
        "sliding",
        sliding_condition,
        sliding_impulse,
        sliding_tangent,
        sliding_speed,
        sliding_reflection_tangent,
    )
    outgoing_tangent = Piecewise(
        (sticking.outgoing_tangential_speed, sticking_condition),
        (sliding.outgoing_tangential_speed, True),
    )
    outgoing_speed = Piecewise(
        (sticking.outgoing_speed, sticking_condition),
        (sliding.outgoing_speed, True),
    )
    reflection_tangent = Piecewise(
        (sticking.reflection_tangent, sticking_condition),
        (sliding.reflection_tangent, True),
    )
    selected = (
        "sticking"
        if sticking_condition is S.true
        else "sliding"
        if sticking_condition is S.false
        else None
    )
    certificates = (
        _certificate(
            "normal_impulse_balance",
            normal_impulse - mass * (outgoing_normal + normal),
            "Normal momentum change equals the restitution impulse.",
        ),
        _certificate(
            "sticking_tangential_balance",
            sticking_impulse - mass * (S.Zero - tangent),
            "The feasible no-slip impulse cancels tangential speed.",
        ),
        _certificate(
            "sliding_tangential_balance",
            sliding_impulse - mass * (sliding_tangent - tangent),
            "The saturated friction impulse returns the sliding speed.",
        ),
        _certificate(
            "sliding_cone_saturation",
            -sliding_impulse - impulse_limit,
            "The sliding impulse lies on the Coulomb bound.",
        ),
        _certificate(
            "sliding_speed_return",
            sliding_speed**2 - outgoing_normal**2 - sliding_tangent**2,
            "The returned speed reconstructs its normal and tangent components.",
        ),
    )
    return FrictionalImpactResult(
        status="constructed",
        request=request,
        normal_impulse=normal_impulse,
        friction_impulse_limit=impulse_limit,
        outgoing_normal_speed=outgoing_normal,
        sticking=sticking,
        sliding=sliding,
        outgoing_tangential_speed=outgoing_tangent,
        outgoing_speed=outgoing_speed,
        reflection_tangent=reflection_tangent,
        selected_regime=selected,
        certificates=certificates,
    )
