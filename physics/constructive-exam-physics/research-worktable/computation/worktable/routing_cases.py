"""Frozen heterogeneous cards for the common problem-routing boundary."""

from __future__ import annotations

from fractions import Fraction

from sympy import sin, symbols

from occ.adaptive import AdaptiveRelationRequest
from occ.semantic import (
    Dimension,
    PhysicalRelationPacket,
    QuantitySemantics,
)
from occ.routing import (
    FunctionalRelationRequest,
    LinearDynamicsRequest,
    ProblemCard,
    RouteAlternatives,
    RoutedProblemResult,
    compile_problem_card,
)
from occ.problem import PhysicalLaw

from .event_cases import build_a15_event_problem, build_a15_handwritten_routes
from .harmonic_cases import (
    build_a21_wave_request,
    build_a25_handwritten_routes,
    build_a25_rlc_request,
)
from .impact_cases import build_a15_impact_case, build_a15_impact_routes
from .path_cases import build_a10_case, build_a14_case
from .polynomial_cases import build_polynomial_batch


ZERO = Dimension(0, 0, 0, 0)
VELOCITY = Dimension(0, 1, -1, 0)
POWER = Dimension(1, 2, -3, 0)


def _adaptive_from_batch(problem_id: str, target_name: str) -> AdaptiveRelationRequest:
    case = next(
        case
        for case in build_polynomial_batch()
        if case.packet.problem_id == problem_id
    )
    target = next(
        target for target in case.packet.targets if target.name == target_name
    )
    laws_by_name = {law.name: law for law in case.packet.laws}
    laws = (
        tuple(laws_by_name[name] for name in target.law_names)
        if target.law_names
        else case.packet.laws
    )
    givens = tuple(symbol for symbol in target.retain if symbol != target.target)
    return AdaptiveRelationRequest(
        problem_id=problem_id,
        laws=laws,
        givens=givens,
        target=target.target,
        max_selected_laws=len(laws),
        max_attempts=128,
        max_variables=case.packet.max_variables,
    )


def _quantity(symbol, name: str, dimension: Dimension) -> QuantitySemantics:
    return QuantitySemantics(symbol, name, dimension)


def _functional_transfer() -> FunctionalRelationRequest:
    speed, damper_1, damper_2, power = symbols("v v_1 v_2 P")
    packet = PhysicalRelationPacket(
        area="mechanics/viscous-dissipation",
        source=_quantity(speed, "driving speed", VELOCITY),
        fields=(
            _quantity(damper_1, "damper speed 1", VELOCITY),
            _quantity(damper_2, "damper speed 2", VELOCITY),
        ),
        target=_quantity(power, "dissipated power", POWER),
        relations=(
            damper_1 - 2 * speed,
            damper_2 + speed,
            power - 3 * damper_1**2 - 5 * damper_2**2,
        ),
        map_coefficient_dimension=ZERO,
        functional_weight_dimension=Dimension(1, 0, -1, 0),
        regime=("linear viscous damping",),
        conventions=("positive dissipation",),
    )
    return FunctionalRelationRequest(packet, max_fields=2)


def _linear_closure() -> LinearDynamicsRequest:
    value = Fraction
    return LinearDynamicsRequest(
        restoring_map=(
            (value(6), value(-1), value(0), value(-1)),
            (value(-1), value(6), value(-1), value(0)),
            (value(0), value(-1), value(6), value(-1)),
            (value(-1), value(0), value(-1), value(6)),
        ),
        observable=(value(1, 4),) * 4,
        max_dimension=2,
    )


def _ambiguous_relation() -> AdaptiveRelationRequest:
    given, target = symbols("ambiguous_given ambiguous_target")
    return AdaptiveRelationRequest(
        problem_id="adversarial-ambiguous",
        laws=(
            PhysicalLaw("first candidate", target - given, "adversarial fixture"),
            PhysicalLaw("second candidate", target - 2 * given, "adversarial fixture"),
        ),
        givens=(given,),
        target=target,
        max_selected_laws=2,
    )


def _unsupported_relation() -> AdaptiveRelationRequest:
    given, target = symbols("transcendental_given transcendental_target")
    return AdaptiveRelationRequest(
        problem_id="adversarial-transcendental",
        laws=(
            PhysicalLaw(
                "transcendental response",
                sin(target) - given,
                "adversarial fixture",
            ),
        ),
        givens=(given,),
        target=target,
    )


def build_routing_benchmark() -> tuple[ProblemCard, ...]:
    event_routes = RouteAlternatives(*build_a15_handwritten_routes())
    impact_routes = RouteAlternatives(*build_a15_impact_routes())
    impact = build_a15_impact_case()
    a14 = build_a14_case()
    a10 = build_a10_case()
    return (
        ProblemCard(
            "A24-09",
            "vacuum capacitance",
            "A617 PDF page 7",
            _adaptive_from_batch("A24-09", "vacuum capacitance"),
        ),
        ProblemCard(
            "A13-02",
            "support height",
            "A617 PDF page 29",
            _adaptive_from_batch("A13-02", "support height"),
        ),
        ProblemCard(
            "functional-transfer",
            "dissipated power",
            "unseen-area semantic transfer fixture",
            _functional_transfer(),
        ),
        ProblemCard(
            "linear-closure",
            "mean position",
            "finite rational closure regression",
            _linear_closure(),
        ),
        ProblemCard(
            "A15-01",
            event_routes.direct.target,
            "A617 PDF page 25",
            build_a15_event_problem(),
            event_routes,
        ),
        ProblemCard(
            impact.problem_id,
            "reflected speed and angle",
            impact.provenance,
            impact.request,
            impact_routes,
        ),
        ProblemCard(
            a14.problem_id,
            "oriented induced line work",
            f"A617 PDF page {a14.pdf_page}",
            a14.request,
        ),
        ProblemCard(
            a10.problem_id,
            "oriented induced line work",
            f"A617 PDF page {a10.pdf_page}",
            a10.request,
        ),
        ProblemCard(
            "A21-03",
            "standing-wave displacement phasor",
            "A617 PDF page 12",
            build_a21_wave_request(),
        ),
        ProblemCard(
            "A25-06",
            "complex impedance, current amplitude, and power factor",
            "A617 PDF page 5",
            build_a25_rlc_request(),
            RouteAlternatives(*build_a25_handwritten_routes()),
        ),
        ProblemCard(
            "adversarial-ambiguous",
            "ambiguous target",
            "frozen competing-packet fixture",
            _ambiguous_relation(),
        ),
        ProblemCard(
            "adversarial-transcendental",
            "transcendental target",
            "frozen unsupported-backend fixture",
            _unsupported_relation(),
        ),
    )


def run_routing_benchmark() -> tuple[RoutedProblemResult, ...]:
    return tuple(compile_problem_card(card) for card in build_routing_benchmark())


def command_routing_benchmark() -> None:
    print("problem\toperator\tstatus\tsource_status\tobstruction\tadmission")
    results = run_routing_benchmark()
    for result in results:
        obstruction = "-" if result.obstruction is None else result.obstruction.code
        admission = "-" if result.admission is None else result.admission.classification
        print(
            f"{result.card.problem_id}\t{result.operator}\t{result.status}\t"
            f"{result.source_status}\t{obstruction}\t{admission}"
        )
    constructed = sum(result.status == "constructed" for result in results)
    refused = len(results) - constructed
    print(f"summary\t{constructed}_constructed\t{refused}_bounded_non_success")
