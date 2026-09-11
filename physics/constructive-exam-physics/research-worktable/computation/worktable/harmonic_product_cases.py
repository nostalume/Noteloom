"""Source-bound harmonic-product cases from A617 pages 9 and 34."""

from __future__ import annotations

from dataclasses import dataclass

from sympy import Expr, I, Symbol, pi, simplify, symbols

from occ.cost import (
    AdmissionBoundary,
    ExamAction,
    HandwrittenRoute,
    construct_admission_boundary,
)
from occ.harmonic import (
    HarmonicObservable,
    HarmonicResponseRequest,
    HarmonicResponseResult,
    construct_harmonic_response,
    phasor_to_real_signal,
)
from occ.harmonic_product import (
    HarmonicProductRequest,
    HarmonicProductResult,
    construct_harmonic_product,
)


@dataclass(frozen=True)
class A23CoilResult:
    flux_scale: Expr
    resistance: Symbol
    inductance: Symbol
    angular_frequency: Symbol
    time: Symbol
    emf_phasor: Expr
    emf_signal: Expr
    response: HarmonicResponseResult
    torque: HarmonicProductResult
    average_power_balance_residual: Expr
    admission: AdmissionBoundary


@dataclass(frozen=True)
class A11CoilResult:
    flux_scale: Expr
    resistance: Symbol
    angular_frequency: Symbol
    time: Symbol
    response: HarmonicResponseResult
    torque: HarmonicProductResult


@dataclass(frozen=True)
class SourceCoilCase:
    problem_id: str
    pdf_page: int
    provenance: str
    flux_scale: Expr
    resistance: Expr
    inductance: Expr
    angular_frequency: Symbol
    time: Symbol
    request: HarmonicResponseRequest


def _build_coil_case(
    problem_id: str,
    pdf_page: int,
    provenance: str,
    flux_scale: Expr,
    resistance: Expr,
    inductance: Expr,
    angular_frequency: Symbol,
    time: Symbol,
) -> SourceCoilCase:
    current = symbols(f"I_{problem_id.replace('-', '_')}")
    emf_phasor = -I * flux_scale * angular_frequency
    impedance = resistance + I * angular_frequency * inductance
    return SourceCoilCase(
        problem_id=problem_id,
        pdf_page=pdf_page,
        provenance=provenance,
        flux_scale=flux_scale,
        resistance=resistance,
        inductance=inductance,
        angular_frequency=angular_frequency,
        time=time,
        request=HarmonicResponseRequest(
            problem_id=problem_id,
            laws=(impedance * current - emf_phasor,),
            unknowns=(current,),
            observables=(HarmonicObservable("induced current", current),),
            angular_frequency=angular_frequency,
            time=time,
        ),
    )


def build_a23_coil_case() -> SourceCoilCase:
    turns = symbols("N", positive=True, integer=True)
    field, side, resistance, inductance, omega, time = symbols(
        "B a R L omega t", positive=True, real=True
    )
    return _build_coil_case(
        "A23-05",
        9,
        "A617 PDF page 9; rotating square R-L coil",
        turns * field * side**2,
        resistance,
        inductance,
        omega,
        time,
    )


def build_a11_coil_case() -> SourceCoilCase:
    side, outer_radius, resistance, large_current, permeability, omega, time = symbols(
        "a b R I mu_0 omega t", positive=True, real=True
    )
    field_at_center = permeability * large_current / (2 * outer_radius)
    return _build_coil_case(
        "A11-06",
        34,
        "A617 PDF page 34; b>>a large-loop field and negligible self-inductance",
        field_at_center * pi * side**2,
        resistance,
        0,
        omega,
        time,
    )


def _run_coil_pipeline(
    case: SourceCoilCase,
) -> tuple[Expr, HarmonicResponseResult, HarmonicProductResult]:
    emf_phasor = -I * case.flux_scale * case.angular_frequency
    response = construct_harmonic_response(case.request)
    if response.status != "constructed":
        raise RuntimeError(f"The source-bound {case.problem_id} response failed.")
    torque = construct_harmonic_product(
        HarmonicProductRequest(
            problem_id=case.problem_id,
            product_name="applied torque along the rotation direction",
            left_phasor=response.observables[0].phasor,
            right_phasor=-I,
            angular_frequency=case.angular_frequency,
            time=case.time,
            scale=case.flux_scale,
        )
    )
    if torque.status != "constructed":
        raise RuntimeError(f"The source-bound {case.problem_id} torque return failed.")
    return emf_phasor, response, torque


def _action(
    kind: str,
    description: str,
    live: int = 0,
    subjects: tuple[str, ...] = (),
) -> ExamAction:
    return ExamAction(kind, description, live, subjects)


def build_a23_handwritten_routes() -> tuple[HandwrittenRoute, HandwrittenRoute]:
    target = "induced emf, steady current, and applied torque"
    physical_relations = (
        _action("relation", "write flux and Faraday induction", 1),
        _action("relation", "write the steady series R-L response", 1),
        _action(
            "relation", "write applied torque as flux scale times current and sine", 1
        ),
    )
    symbolic_work = (
        _action("symbolic", "differentiate flux", 1, ("induced emf",)),
        _action("symbolic", "solve the R-L response", 1, ("steady current",)),
        _action("symbolic", "combine the two harmonic factors", 1, ("applied torque",)),
        _action("return", "restore sign and average-power checks", 1),
    )
    baseline = HandwrittenRoute(
        "A23-05", target, (), physical_relations + symbolic_work
    )
    proposed = HandwrittenRoute(
        "A23-05",
        target,
        (),
        physical_relations
        + (
            _action(
                "representation",
                "encode the response and product as two composable requests",
                1,
            ),
        )
        + symbolic_work,
    )
    return baseline, proposed


def run_a23_coil() -> A23CoilResult:
    case = build_a23_coil_case()
    emf_phasor, response, torque = _run_coil_pipeline(case)
    average_power_balance = simplify(
        case.angular_frequency * torque.dc_component
        - case.resistance * response.observables[0].magnitude_squared / 2
    )
    return A23CoilResult(
        flux_scale=case.flux_scale,
        resistance=case.resistance,
        inductance=case.inductance,
        angular_frequency=case.angular_frequency,
        time=case.time,
        emf_phasor=emf_phasor,
        emf_signal=phasor_to_real_signal(emf_phasor, case.angular_frequency, case.time),
        response=response,
        torque=torque,
        average_power_balance_residual=average_power_balance,
        admission=construct_admission_boundary(*build_a23_handwritten_routes()),
    )


def run_a11_coil() -> A11CoilResult:
    case = build_a11_coil_case()
    _, response, torque = _run_coil_pipeline(case)
    return A11CoilResult(
        flux_scale=case.flux_scale,
        resistance=case.resistance,
        angular_frequency=case.angular_frequency,
        time=case.time,
        response=response,
        torque=torque,
    )


def command_harmonic_product() -> None:
    source = run_a23_coil()
    transfer = run_a11_coil()
    print("problem\toperation\tresult")
    print(f"A23-05\temf\t{source.emf_signal}")
    print(f"A23-05\tcurrent\t{source.response.observables[0].time_signal}")
    print(f"A23-05\ttorque_dc\t{source.torque.dc_component}")
    print(f"A23-05\ttorque_2omega\t{source.torque.second_harmonic_phasor}")
    print(f"A23-05\tpower_balance_residual\t{source.average_power_balance_residual}")
    print(f"A23-05\tadmission\t{source.admission.classification}")
    print(f"A11-06\tcurrent\t{transfer.response.observables[0].time_signal}")
    print(f"A11-06\ttorque_dc\t{transfer.torque.dc_component}")
    print(f"A11-06\ttorque_2omega\t{transfer.torque.second_harmonic_phasor}")
    print("summary\t2_source_problems\tdc_and_second_harmonic_certified")
