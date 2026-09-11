"""Source-bound frictional-impact construction from A617 page 25."""

from __future__ import annotations

from dataclasses import dataclass

from sympy import Expr, Piecewise, Symbol, atan, cos, simplify, sin, symbols, tan

from occ.cost import (
    AdmissionBoundary,
    ExamAction,
    HandwrittenRoute,
    construct_admission_boundary,
)
from occ.impact import (
    FrictionalImpactRequest,
    FrictionalImpactResult,
    construct_frictional_impact,
)


TARGET = "reflected speed and angle"


@dataclass(frozen=True)
class SourceImpactCase:
    problem_id: str
    pdf_page: int
    provenance: str
    mass: Symbol
    incident_speed: Symbol
    incidence_angle: Symbol
    friction_coefficient: Symbol
    restitution_coefficient: Symbol
    normal_component: Symbol
    tangential_component: Symbol
    request: FrictionalImpactRequest


@dataclass(frozen=True)
class A15ImpactResult:
    incident_speed: Symbol
    incidence_angle: Symbol
    friction_coefficient: Symbol
    restitution_coefficient: Symbol
    construction: FrictionalImpactResult
    sticking_condition: Expr
    sticking_speed: Expr
    sticking_angle: Expr
    sliding_condition: Expr
    sliding_speed: Expr
    sliding_angle: Expr
    reflected_speed: Expr
    reflected_angle: Expr
    admission: AdmissionBoundary


def build_a15_impact_case() -> SourceImpactCase:
    mass, speed, angle, friction, restitution = symbols(
        "m v_1 theta mu e", positive=True, real=True
    )
    normal, tangent_speed = symbols("u_n u_t", positive=True, real=True)
    return SourceImpactCase(
        problem_id="A15-02",
        pdf_page=25,
        provenance=(
            "A617 PDF page 25; nonrotating point-particle interpretation and "
            "maximum-dissipation Coulomb impact contract"
        ),
        mass=mass,
        incident_speed=speed,
        incidence_angle=angle,
        friction_coefficient=friction,
        restitution_coefficient=restitution,
        normal_component=normal,
        tangential_component=tangent_speed,
        request=FrictionalImpactRequest(
            "A15-02", mass, normal, tangent_speed, friction, restitution
        ),
    )


def _action(
    kind: str,
    description: str,
    live: int = 0,
    subjects: tuple[str, ...] = (),
) -> ExamAction:
    return ExamAction(kind, description, live, subjects)


def build_a15_impact_routes() -> tuple[HandwrittenRoute, HandwrittenRoute]:
    common = (
        _action("relation", "resolve velocity into wall-normal and tangent parts", 2),
        _action("relation", "apply Newton restitution to the normal component", 2),
        _action("relation", "bound the tangent impulse by Coulomb friction", 3),
        _action(
            "symbolic",
            "derive impulses and outgoing components",
            3,
            ("normal impulse", "tangent impulse", "normal speed", "tangent speed"),
        ),
        _action("branch", "separate feasible sticking from saturated sliding", 2),
        _action(
            "symbolic",
            "assemble the requested polar return",
            2,
            ("reflected speed", "reflection angle"),
        ),
        _action("return", "restore the reflected direction and limiting cases", 1),
    )
    baseline = HandwrittenRoute("A15-02", TARGET, (), common)
    proposed = HandwrittenRoute(
        "A15-02",
        TARGET,
        (),
        common[:3]
        + (
            _action(
                "representation", "encode tangent impulse as interval projection", 3
            ),
        )
        + common[3:],
    )
    return baseline, proposed


def run_a15_impact() -> A15ImpactResult:
    case = build_a15_impact_case()
    construction = construct_frictional_impact(case.request)
    substitutions = {
        case.normal_component: case.incident_speed * cos(case.incidence_angle),
        case.tangential_component: case.incident_speed * sin(case.incidence_angle),
    }
    boundary = case.friction_coefficient * (1 + case.restitution_coefficient)
    sticking_condition = tan(case.incidence_angle) <= boundary
    sliding_condition = tan(case.incidence_angle) > boundary
    sticking_speed = simplify(construction.sticking.outgoing_speed.subs(substitutions))
    sliding_speed = simplify(construction.sliding.outgoing_speed.subs(substitutions))
    sliding_ratio = simplify(
        construction.sliding.reflection_tangent.subs(substitutions)
    )
    sticking_angle = 0
    sliding_angle = atan(sliding_ratio)
    return A15ImpactResult(
        incident_speed=case.incident_speed,
        incidence_angle=case.incidence_angle,
        friction_coefficient=case.friction_coefficient,
        restitution_coefficient=case.restitution_coefficient,
        construction=construction,
        sticking_condition=sticking_condition,
        sticking_speed=sticking_speed,
        sticking_angle=sticking_angle,
        sliding_condition=sliding_condition,
        sliding_speed=sliding_speed,
        sliding_angle=sliding_angle,
        reflected_speed=Piecewise(
            (sticking_speed, sticking_condition), (sliding_speed, True)
        ),
        reflected_angle=Piecewise(
            (sticking_angle, sticking_condition), (sliding_angle, True)
        ),
        admission=construct_admission_boundary(*build_a15_impact_routes()),
    )


def command_impact_transfer() -> None:
    result = run_a15_impact()
    print("problem\tregime\tcondition\treflected_speed\treflection_angle")
    print(
        f"A15-02\tsticking\t{result.sticking_condition}\t"
        f"{result.sticking_speed}\t{result.sticking_angle}"
    )
    print(
        f"A15-02\tsliding\t{result.sliding_condition}\t"
        f"{result.sliding_speed}\t{result.sliding_angle}"
    )
    print("admission\t" + result.admission.classification)
    print("summary\t1_source_problem\t2_physical_regimes\timpulse_projection_certified")
