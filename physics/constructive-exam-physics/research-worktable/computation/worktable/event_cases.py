"""Source-bound event construction and handwritten route audit for A15-01."""

from __future__ import annotations

from dataclasses import dataclass

from sympy import Rational, acos, sqrt, symbols

from occ.cost import (
    AdmissionBoundary,
    ExamAction,
    HandwrittenRoute,
    RouteComparison,
    compare_exam_routes,
    construct_admission_boundary,
)
from occ.event import (
    EventConstructionResult,
    EventPredicate,
    EventProblem,
    VariableInterval,
    construct_event,
)
from occ.problem import PhysicalLaw


@dataclass(frozen=True)
class EventTransferResult:
    event: EventConstructionResult
    angle: object
    handwritten_comparison: RouteComparison
    admission: AdmissionBoundary


def build_a15_event_problem() -> EventProblem:
    cosine, speed_squared, vertical_acceleration = symbols(
        "cosine speed_squared vertical_acceleration"
    )
    return EventProblem(
        problem_id="A15-01",
        pdf_page=25,
        state_laws=(
            PhysicalLaw(
                "energy evolution",
                speed_squared - 2 * (cosine - Rational(1, 10)),
                "A617 PDF page 25 and mechanical-energy conservation; "
                "speed_squared=v^2/(g*l)",
            ),
            PhysicalLaw(
                "vertical acceleration observable",
                vertical_acceleration - 1 + cosine**2 + speed_squared * cosine,
                "vertical projection of radial and tangential acceleration; "
                "vertical_acceleration=a_y/g with downward positive",
            ),
        ),
        event=EventPredicate(
            "horizontal resultant",
            vertical_acceleration,
            "horizontal net force iff its vertical component is zero",
        ),
        unknowns=(speed_squared, vertical_acceleration, cosine),
        event_coordinate=cosine,
        domains=(
            VariableInterval(
                cosine,
                lower=Rational(1, 10),
                upper=1,
                meaning="released descent from theta to the bottom",
            ),
        ),
        max_variables=3,
    )


def _action(
    kind: str,
    description: str,
    live: int = 0,
    symbolic_subjects: tuple[str, ...] = (),
) -> ExamAction:
    return ExamAction(kind, description, live, symbolic_subjects)


def build_a15_handwritten_routes() -> tuple[HandwrittenRoute, HandwrittenRoute]:
    baseline = HandwrittenRoute(
        problem_id="A15-01",
        target="pendulum angle at horizontal resultant",
        hidden_quantities=("scaled speed squared",),
        actions=(
            _action("relation", "write energy evolution for scaled speed", 1),
            _action(
                "relation",
                "set the vertical acceleration expression to zero",
                2,
            ),
            _action(
                "symbolic",
                "substitute energy into the event equation",
                2,
                ("scaled speed squared",),
            ),
            _action(
                "symbolic",
                "solve the quadratic for cosine",
                1,
                ("cosine",),
            ),
            _action("branch", "require 1/10 <= cosine <= 1", 1),
            _action("return", "convert the selected cosine to the angle", 1),
        ),
    )
    proposed = HandwrittenRoute(
        problem_id="A15-01",
        target="pendulum angle at horizontal resultant",
        hidden_quantities=("scaled speed squared", "vertical acceleration"),
        actions=(
            _action("relation", "bind energy evolution", 1),
            _action("relation", "bind the vertical acceleration observable", 2),
            _action("relation", "bind the zero vertical-component event", 3),
            _action(
                "representation",
                "encode the nondimensional event packet and physical interval",
                3,
            ),
            _action(
                "symbolic",
                "eliminate the speed and acceleration coordinates",
                3,
                ("scaled speed squared", "vertical acceleration"),
            ),
            _action(
                "symbolic",
                "solve the generated event polynomial",
                1,
                ("cosine",),
            ),
            _action("branch", "filter full-state lifts by 1/10 <= cosine <= 1", 1),
            _action("return", "convert the selected cosine to the angle", 1),
        ),
    )
    return baseline, proposed


def run_event_transfer() -> EventTransferResult:
    event = construct_event(build_a15_event_problem())
    if event.status != "constructed" or event.selected is None:
        raise RuntimeError("The locked A15-01 event transfer did not construct.")
    cosine = event.request.event_coordinate
    angle = acos(event.selected.value(cosine))
    baseline, proposed = build_a15_handwritten_routes()
    return EventTransferResult(
        event=event,
        angle=angle,
        handwritten_comparison=compare_exam_routes(baseline, proposed),
        admission=construct_admission_boundary(baseline, proposed),
    )


def command_event_transfer() -> None:
    result = run_event_transfer()
    cosine = result.event.request.event_coordinate
    selected_cosine = result.event.selected.value(cosine)
    print(f"problem\t{result.event.request.problem_id}")
    print(f"status\t{result.event.status}")
    print(f"projected\t{result.event.projection.projected_relations}")
    print(f"algebraic_branches\t{len(result.event.algebraic_branches)}")
    print(f"admissible_branches\t{len(result.event.admissible_branches)}")
    print(f"selected_cosine\t{selected_cosine}")
    print(f"expected_identity\t{selected_cosine == (1 + sqrt(301)) / 30}")
    print(f"angle_radians\t{result.angle.evalf(10)}")
    print(f"direct_cost\t{result.handwritten_comparison.baseline.cost.as_tuple()}")
    print(f"event_card_cost\t{result.handwritten_comparison.proposed.cost.as_tuple()}")
    print(f"handwritten_verdict\t{result.handwritten_comparison.status}")
    print(f"admission\t{result.admission.classification}")
