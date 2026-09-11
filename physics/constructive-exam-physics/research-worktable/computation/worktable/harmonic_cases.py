"""Source-bound harmonic-response cases from A617 pages 5 and 12."""

from __future__ import annotations

from dataclasses import dataclass

from sympy import Expr, I, Rational, Symbol, exp, pi, simplify, symbols

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
from occ.harmonic_pattern import (
    SpatialHarmonicRequest,
    SpatialHarmonicResult,
    construct_spatial_harmonic_pattern,
)


@dataclass(frozen=True)
class A21WaveResult:
    amplitude: Symbol
    coordinate: Symbol
    angular_frequency: Symbol
    time: Symbol
    reflected_phasor: Expr
    response: HarmonicResponseResult
    pattern: SpatialHarmonicResult
    q_signal: Expr


@dataclass(frozen=True)
class A25RlcResult:
    impedance: Expr
    response: HarmonicResponseResult
    admission: AdmissionBoundary


def _a21_symbols() -> tuple[Symbol, Symbol, Symbol, Symbol, Symbol]:
    return (
        symbols("A", positive=True, real=True),
        symbols("theta", real=True),
        symbols("omega", positive=True, real=True),
        symbols("t", real=True),
        symbols("B_r"),
    )


def build_a21_wave_request() -> HarmonicResponseRequest:
    amplitude, coordinate, angular_frequency, time, reflected_amplitude = _a21_symbols()
    boundary = Rational(11, 2) * pi
    incident = I * amplitude * exp(-I * coordinate)
    reflected = reflected_amplitude * exp(I * coordinate)
    fixed_boundary_law = simplify((incident + reflected).subs(coordinate, boundary))
    return HarmonicResponseRequest(
        problem_id="A21-03",
        laws=(fixed_boundary_law,),
        unknowns=(reflected_amplitude,),
        observables=(
            HarmonicObservable("total displacement amplitude", incident + reflected),
        ),
        angular_frequency=angular_frequency,
        time=time,
    )


def run_a21_wave() -> A21WaveResult:
    request = build_a21_wave_request()
    response = construct_harmonic_response(request)
    if response.status != "constructed":
        raise RuntimeError("The source-bound A21-03 harmonic construction failed.")
    amplitude, coordinate, _, _, _ = _a21_symbols()
    reflected_phasor = response.solution[0][1]
    pattern = construct_spatial_harmonic_pattern(
        SpatialHarmonicRequest(
            response.observables[0].phasor,
            coordinate,
            0,
            Rational(11, 2) * pi,
        )
    )
    q_phasor = simplify(response.observables[0].phasor.subs(coordinate, 4 * pi))
    q_signal = phasor_to_real_signal(
        q_phasor,
        request.angular_frequency,
        request.time,
    )
    return A21WaveResult(
        amplitude=amplitude,
        coordinate=coordinate,
        angular_frequency=request.angular_frequency,
        time=request.time,
        reflected_phasor=reflected_phasor,
        response=response,
        pattern=pattern,
        q_signal=q_signal,
    )


def build_a25_rlc_request() -> HarmonicResponseRequest:
    current = symbols("I_response")
    time = symbols("t", real=True)
    resistance = 30
    inductance = Rational(45, 1000)
    capacitance = Rational(35, 1_000_000)
    angular_frequency = 100
    impedance = resistance + I * (
        angular_frequency * inductance - 1 / (angular_frequency * capacitance)
    )
    return HarmonicResponseRequest(
        problem_id="A25-06",
        laws=(impedance * current - 200,),
        unknowns=(current,),
        observables=(HarmonicObservable("series current", current, reference=200),),
        angular_frequency=angular_frequency,
        time=time,
    )


def _action(
    kind: str,
    description: str,
    live: int = 0,
    subjects: tuple[str, ...] = (),
) -> ExamAction:
    return ExamAction(kind, description, live, subjects)


def build_a25_handwritten_routes() -> tuple[HandwrittenRoute, HandwrittenRoute]:
    target = "complex impedance, current amplitude, and power factor"
    shared_symbolic_actions = (
        _action(
            "symbolic",
            "evaluate two reactances and combine the series impedance",
            1,
            ("inductive reactance", "capacitive reactance", "series impedance"),
        ),
        _action(
            "symbolic",
            "divide the voltage phasor and calculate its modulus",
            1,
            ("current phasor", "current amplitude"),
        ),
        _action(
            "symbolic",
            "calculate the in-phase fraction",
            1,
            ("power factor",),
        ),
        _action("return", "state that the capacitive current leads the source", 1),
    )
    baseline = HandwrittenRoute(
        problem_id="A25-06",
        target=target,
        hidden_quantities=(),
        actions=(
            _action("relation", "write the standard series-impedance relation", 1),
            *shared_symbolic_actions,
        ),
    )
    proposed = HandwrittenRoute(
        problem_id="A25-06",
        target=target,
        hidden_quantities=(),
        actions=(
            _action("relation", "bind the same series phasor law", 1),
            _action(
                "representation",
                "encode the law and observables as a harmonic response request",
                1,
            ),
            *shared_symbolic_actions,
        ),
    )
    return baseline, proposed


def run_a25_rlc() -> A25RlcResult:
    request = build_a25_rlc_request()
    response = construct_harmonic_response(request)
    if response.status != "constructed":
        raise RuntimeError("The source-bound A25-06 harmonic construction failed.")
    current = request.unknowns[0]
    impedance = simplify(200 / dict(response.solution)[current])
    routes = build_a25_handwritten_routes()
    return A25RlcResult(
        impedance=impedance,
        response=response,
        admission=construct_admission_boundary(*routes),
    )


def command_harmonic_transfer() -> None:
    wave = run_a21_wave()
    rlc = run_a25_rlc()
    current = rlc.response.observables[0]
    print("problem\toperation\tresult")
    print(f"A21-03\treflected_phasor\t{wave.reflected_phasor}")
    print(f"A21-03\ttotal_phasor\t{wave.response.observables[0].phasor}")
    print(f"A21-03\tnodes\t{wave.pattern.nodes}")
    print(f"A21-03\tantinodes\t{wave.pattern.antinodes}")
    print(f"A21-03\tQ_signal\t{wave.q_signal}")
    print(f"A25-06\timpedance\t{rlc.impedance}")
    print(f"A25-06\tcurrent_phasor\t{current.phasor}")
    print(f"A25-06\tcurrent_magnitude_squared\t{current.magnitude_squared}")
    print(f"A25-06\tpower_factor\t{current.reference_phase_cosine}")
    print(f"A25-06\tadmission\t{rlc.admission.classification}")
    print("summary\t2_source_problems\tphase_preserved")
