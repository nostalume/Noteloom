import math
from collections.abc import Sequence

from ._parameterized_contracts import (
    Certificate,
    CompilationResult,
    Obstruction,
    ParameterizedHeader,
    RouteStep,
    refused,
    solved,
)


_ADAPTER = "condensed_matter.phonon_count"
_OBJECTS = {"bravais_lattice", "basis", "harmonic_displacements"}
_OBSERVABLE = "phonon_mode_count"
_SPECTRUM = "phonon_frequency_measure"
_COUNT = "phonon_mode_count"
_ENSEMBLE = "bosonic_thermal_ensemble"
_HEAT_CAPACITY = "constant_volume_heat_capacity"
_COUNT_ROUTE = (
    RouteStep(
        operation="construct_displacement_fiber",
        witness="d displacement coordinates for each of p basis atoms give dimension d*p.",
    ),
    RouteStep(
        operation="construct_acoustic_translation_subspace",
        witness="Stable uniform translations contribute d acoustic directions at k=0.",
    ),
    RouteStep(
        operation="take_optical_complement",
        witness="The complementary branch count is d*p-d=d*(p-1).",
    ),
    RouteStep(
        operation="recover_total_mode_count",
        witness="Branch fibers over primitive-cell momenta recover all displacement degrees of freedom.",
    ),
)
_HEAT_ROUTE = (
    RouteStep(
        operation="admit_frequency_measure_port",
        witness="Each frequency is paired with a positive integer spectral weight.",
    ),
    RouteStep(
        operation="nondimensionalize_mode_energies",
        witness="The thermal coordinate is x=hbar*omega/(k_B*T).",
    ),
    RouteStep(
        operation="differentiate_bose_energy",
        witness="Each oscillator contributes k_B*x^2*exp(x)/(exp(x)-1)^2.",
    ),
    RouteStep(
        operation="integrate_weighted_spectrum",
        witness="The discrete frequency measure supplies the mode degeneracies.",
    ),
)


def admit(header: ParameterizedHeader) -> ParameterizedHeader | None:
    if header.observable == _OBSERVABLE and _OBJECTS.issubset(header.objects):
        return header
    if header.observable == _HEAT_CAPACITY:
        objects = header.objects
        if _ENSEMBLE in objects and (_SPECTRUM in objects or _COUNT in objects):
            return header
    return None


def _refuse(code: str, message: str, *fields: str) -> CompilationResult:
    return refused(
        _ADAPTER,
        Obstruction(code=code, message=message, fields=tuple(fields)),
    )


def _solve_count(request: ParameterizedHeader) -> CompilationResult:
    parameters = request.parameters
    if "population_kind" not in parameters:
        return _refuse(
            "ambiguous_count",
            "Population count must be typed as atoms or primitive cells.",
            "population_kind",
        )
    required = (
        "spatial_dimension",
        "basis_atom_count",
        "population_count",
        "stable_translation_modes",
    )
    missing = tuple(field for field in required if field not in parameters)
    if missing:
        return _refuse(
            "missing_field",
            "The lattice displacement count is underdetermined.",
            *missing,
        )
    dimension = parameters["spatial_dimension"]
    basis_atoms = parameters["basis_atom_count"]
    population = parameters["population_count"]
    population_kind = parameters["population_kind"]
    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for value in (dimension, basis_atoms, population)
    ):
        return _refuse(
            "invalid_field",
            "Dimension, basis size, and population must be integers.",
        )
    if dimension <= 0 or basis_atoms <= 0 or population <= 0:
        return _refuse(
            "invalid_field",
            "Dimension, basis size, and population must be positive.",
        )
    if parameters["stable_translation_modes"] is not True:
        return _refuse(
            "unsupported_regime",
            "The acoustic-branch constructor requires stable translational zero modes.",
            "stable_translation_modes",
        )
    if population_kind not in {"atoms", "primitive_cells"}:
        return _refuse(
            "invalid_field",
            "Population kind must be 'atoms' or 'primitive_cells'.",
            "population_kind",
        )
    if population_kind == "atoms" and population % basis_atoms != 0:
        return _refuse(
            "incompatible_count",
            "An integer number of primitive cells is required for this finite count.",
            "population_count",
            "basis_atom_count",
        )

    total_branches = dimension * basis_atoms
    acoustic_branches = dimension
    optical_branches = dimension * (basis_atoms - 1)
    if population_kind == "atoms":
        primitive_cells = population // basis_atoms
        total_modes = dimension * population
    else:
        primitive_cells = population
        total_modes = total_branches * population
    fiber_count = total_branches * primitive_cells

    certificates = (
        Certificate(
            name="branch_partition",
            passed=acoustic_branches + optical_branches == total_branches,
            witness="Acoustic and optical fibers partition the d*p displacement fiber.",
        ),
        Certificate(
            name="degree_of_freedom_recovery",
            passed=fiber_count == total_modes,
            witness=f"branches*cells={fiber_count} and total displacement modes={total_modes}.",
        ),
    )
    return solved(
        _ADAPTER,
        {
            "total_branches": total_branches,
            "acoustic_branches": acoustic_branches,
            "optical_branches": optical_branches,
            "total_modes": total_modes,
            "population_kind": population_kind,
        },
        _COUNT_ROUTE,
        certificates,
    )


def _bose_heat_capacity_factor(x: float) -> float:
    if x == 0.0:
        return 1.0
    if x > 50.0:
        decay = math.exp(-x)
        return x * x * decay / ((1.0 - decay) ** 2)
    population_denominator = math.expm1(x)
    return x * x * math.exp(x) / (population_denominator**2)


def _solve_heat_capacity(request: ParameterizedHeader) -> CompilationResult:
    adapter = "composition.phonon_heat_capacity"

    def reject(code: str, message: str, *fields: str) -> CompilationResult:
        return refused(
            adapter,
            Obstruction(code=code, message=message, fields=tuple(fields)),
        )

    if _SPECTRUM not in request.objects:
        return reject(
            "insufficient_port",
            "A total mode count does not determine thermal occupation by frequency.",
            "frequencies_rad_s",
            "degeneracies",
        )

    parameters = request.parameters
    required = (
        "frequencies_rad_s",
        "degeneracies",
        "temperature_k",
        "hbar_j_s",
        "boltzmann_j_k",
    )
    missing = tuple(field for field in required if field not in parameters)
    if missing:
        return reject(
            "missing_field",
            "The frequency measure and thermal scale are incomplete.",
            *missing,
        )

    frequencies = parameters["frequencies_rad_s"]
    degeneracies = parameters["degeneracies"]
    if (
        not isinstance(frequencies, Sequence)
        or isinstance(frequencies, (str, bytes))
        or not isinstance(degeneracies, Sequence)
        or isinstance(degeneracies, (str, bytes))
        or not frequencies
        or len(frequencies) != len(degeneracies)
    ):
        return reject(
            "invalid_measure",
            "Frequencies and degeneracies must be nonempty lists of equal length.",
        )

    try:
        omega = [float(value) for value in frequencies]
        temperature = float(parameters["temperature_k"])
        hbar = float(parameters["hbar_j_s"])
        boltzmann = float(parameters["boltzmann_j_k"])
    except (TypeError, ValueError):
        return reject("invalid_field", "Thermal parameters must be real scalars.")

    if not all(math.isfinite(value) and value >= 0.0 for value in omega) or not all(
        math.isfinite(value) and value > 0.0 for value in (temperature, hbar, boltzmann)
    ):
        return reject(
            "invalid_field",
            "Frequencies must be finite and nonnegative; thermal scales must be positive.",
        )
    if not all(
        isinstance(value, int) and not isinstance(value, bool) and value > 0
        for value in degeneracies
    ):
        return reject(
            "invalid_measure",
            "Every frequency weight must be a positive integer degeneracy.",
        )

    energies = [hbar * frequency / (boltzmann * temperature) for frequency in omega]
    factors = [_bose_heat_capacity_factor(x) for x in energies]
    represented_modes = sum(degeneracies)
    heat_capacity = boltzmann * sum(
        degeneracy * factor
        for degeneracy, factor in zip(degeneracies, factors, strict=True)
    )
    upper_bound = boltzmann * represented_modes
    certificates = (
        Certificate(
            name="frequency_measure_cardinality",
            passed=len(omega) == len(degeneracies),
            witness=f"The port contains {len(omega)} frequency-weight pairs.",
        ),
        Certificate(
            name="classical_mode_bound",
            passed=0.0 <= heat_capacity <= upper_bound * (1.0 + 1e-14),
            witness=(f"0 <= C_V={heat_capacity!r} <= k_B*mode_count={upper_bound!r}."),
        ),
    )
    value = {
        "heat_capacity_j_k": heat_capacity,
        "represented_modes": represented_modes,
        "dimensionless_energies": tuple(energies),
    }
    return solved(adapter, value, _HEAT_ROUTE, certificates)


def solve(request: ParameterizedHeader) -> CompilationResult:
    if request.observable == _OBSERVABLE:
        return _solve_count(request)
    return _solve_heat_capacity(request)
