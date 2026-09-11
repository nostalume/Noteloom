"""Path-functional construction on A14-06 and unchanged transfer to A10-06."""

from __future__ import annotations

from dataclasses import dataclass

from sympy import cos, pi, sin, sqrt, symbols

from occ.path import (
    EndpointValueResult,
    ParameterizedPath,
    PathFunctionalRequest,
    PathFunctionalResult,
    PlanarVectorField,
    TwoPathCircuitResult,
    construct_path_functionals,
    construct_two_path_circuit,
    resolve_free_space_potential_difference,
)


@dataclass(frozen=True)
class SourcePathCase:
    problem_id: str
    pdf_page: int
    request: PathFunctionalRequest
    parameters: dict[str, object]


@dataclass(frozen=True)
class PathTransferResult:
    construction: PathFunctionalResult
    circuit: TwoPathCircuitResult
    transfer: PathFunctionalResult
    free_space_voltage: EndpointValueResult


def build_a14_case() -> SourcePathCase:
    x, y, t = symbols("x y t", real=True)
    a, kappa, rho = symbols("a kappa rho", positive=True)
    field = PlanarVectorField(
        "uniform-flux induced field",
        coordinates=(x, y),
        components=(kappa * y, -kappa * x),
        parameters=(a, kappa),
        provenance=("A617 PDF page 28; symmetric Faraday field with kappa=(dB_z/dt)/2"),
    )
    radius = sqrt(2) * a
    paths = (
        ParameterizedPath(
            "minor arc",
            t,
            0,
            1,
            (
                radius * cos(3 * pi / 4 - pi * t / 2),
                radius * sin(3 * pi / 4 - pi * t / 2),
            ),
            "clockwise minor circular conductor from P=(-a,a) to Q=(a,a)",
        ),
        ParameterizedPath(
            "straight chord",
            t,
            0,
            1,
            (-a + 2 * a * t, a),
            "straight conductor from P=(-a,a) to Q=(a,a)",
        ),
    )
    return SourcePathCase(
        "A14-06",
        28,
        PathFunctionalRequest(field, paths, max_paths=2),
        {"a": a, "kappa": kappa, "rho": rho},
    )


def build_a10_case() -> SourcePathCase:
    x, y, t = symbols("x y t", real=True)
    radius = symbols("radius", positive=True)
    kappa = symbols("kappa", real=True)
    field = PlanarVectorField(
        "uniform-flux induced field",
        coordinates=(x, y),
        components=(kappa * y, -kappa * x),
        parameters=(radius, kappa),
        provenance=(
            "A617 PDF page 36; signed kappa=(dB_z/dt)/2 for the circular field"
        ),
    )
    paths = (
        ParameterizedPath(
            "short arc",
            t,
            0,
            1,
            (
                radius * cos(pi * t / 2),
                radius * sin(pi * t / 2),
            ),
            "first-quadrant arc from a=(r,0) to b=(0,r)",
        ),
        ParameterizedPath(
            "long arc",
            t,
            0,
            1,
            (
                radius * cos(-3 * pi * t / 2),
                radius * sin(-3 * pi * t / 2),
            ),
            "clockwise arc through quadrants IV, III, II from a to b",
        ),
    )
    return SourcePathCase(
        "A10-06",
        36,
        PathFunctionalRequest(field, paths, max_paths=2),
        {"radius": radius, "kappa": kappa},
    )


def run_path_transfer() -> PathTransferResult:
    a14 = build_a14_case()
    construction = construct_path_functionals(a14.request)
    circuit = construct_two_path_circuit(
        construction,
        "minor arc",
        "straight chord",
        a14.parameters["rho"],
    )
    transfer = construct_path_functionals(build_a10_case().request)
    free_space_voltage = resolve_free_space_potential_difference(transfer)
    return PathTransferResult(
        construction=construction,
        circuit=circuit,
        transfer=transfer,
        free_space_voltage=free_space_voltage,
    )


def command_path_transfer() -> None:
    result = run_path_transfer()
    print(f"construction\t{result.construction.status}")
    for path in result.construction.paths:
        print(f"A14-06\t{path.name}\twork={path.line_work}\tlength={path.length}")
    print(f"A14-06\tcurl\t{result.construction.curl}")
    print(
        "A14-06\tarea_difference\t"
        f"{result.construction.signed_area_difference('minor arc', 'straight chord')}"
    )
    print(f"A14-06\tterminal_voltage\t{result.circuit.terminal_voltage}")
    print(f"A14-06\tloop_current\t{result.circuit.first_current}")
    print(f"transfer\t{result.transfer.status}")
    for path in result.transfer.paths:
        print(f"A10-06\t{path.name}\twork={path.line_work}\tlength={path.length}")
    print(f"A10-06\tfree_space_voltage\t{result.free_space_voltage.status}")
    print(f"A10-06\tobstruction\t{result.free_space_voltage.obstruction.code}")
