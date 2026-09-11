"""Page-bound exact-relation batch for the 19 A617 polynomial candidates.

The physical laws are supplied theorem contracts.  The computation under test is
target-conditioned law selection followed by exact elimination.  Expected
relations are independent certificates; they are not compiler inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from sympy import Expr, Rational, Symbol, symbols

from occ.problem import (
    PhysicalLaw,
    PolynomialProblemPacket,
    PolynomialProblemResult,
    TargetRequest,
    compile_polynomial_problem,
)
from occ.corpus import (
    load_corpus_index,
    summarize_corpus,
)


CORPUS = Path(__file__).parents[2] / "sources" / "a617-corpus-index.tsv"


@dataclass(frozen=True)
class TargetExpectation:
    name: str
    relation: Optional[Expr]


@dataclass(frozen=True)
class BatchCase:
    packet: PolynomialProblemPacket
    expected_status: str
    expectations: tuple[TargetExpectation, ...]
    source_scope: str


@dataclass(frozen=True)
class CheckedBatchCase:
    case: BatchCase
    result: PolynomialProblemResult
    certificates_passed: bool


def _law(name: str, relation: Expr, provenance: str) -> PhysicalLaw:
    return PhysicalLaw(name, relation, provenance)


def _request(
    name: str,
    target: Symbol,
    laws: tuple[PhysicalLaw, ...],
    law_names: tuple[str, ...],
    retain: tuple[Symbol, ...],
) -> TargetRequest:
    selected = tuple(law for law in laws if law.name in law_names)
    free = set().union(*(law.relation.free_symbols for law in selected)) | {target}
    retained = tuple(dict.fromkeys(retain + (target,)))
    eliminated = tuple(sorted(free - set(retained), key=lambda value: value.name))
    return TargetRequest(
        name=name,
        target=target,
        eliminate=eliminated,
        retain=retained,
        law_names=law_names,
    )


def _packet(
    problem_id: str,
    page: int,
    laws: tuple[PhysicalLaw, ...],
    request_specs: tuple[tuple[str, Symbol, tuple[str, ...], tuple[Symbol, ...]], ...],
    *,
    regime: tuple[str, ...],
    branches: tuple[str, ...],
) -> PolynomialProblemPacket:
    return PolynomialProblemPacket(
        problem_id=problem_id,
        pdf_page=page,
        laws=laws,
        targets=tuple(
            _request(name, target, laws, law_names, retain)
            for name, target, law_names, retain in request_specs
        ),
        regime=regime,
        branch_obligations=branches,
    )


def _a25_03() -> BatchCase:
    gamma, beta, days = symbols("gamma beta days")
    laws = (
        _law("energy ratio", gamma - 120000, "60 GeV / 0.5 MeV"),
        _law("Lorentz speed", gamma**2 * (1 - beta**2) - 1, "special relativity"),
        _law("proper crossing", days * gamma * beta - 36000000, "proper time"),
    )
    packet = _packet(
        "A25-03",
        4,
        laws,
        (("proper days", days, tuple(law.name for law in laws), (days,)),),
        regime=("electron energy interpreted as total relativistic energy",),
        branches=("days > 0 and beta > 0",),
    )
    expected = days**2 * (120000**2 - 1) - 36000000**2
    return BatchCase(
        packet,
        "complete",
        (TargetExpectation("proper days", expected),),
        "all requested output",
    )


def _a24_09() -> BatchCase:
    eps, area, gap, thickness, voltage, er = symbols(
        "eps area gap thickness voltage er"
    )
    c0, cm, charge, initial_energy, final_energy, work, cd, inverse_scale = symbols(
        "c0 cm charge initial_energy final_energy work cd inverse_scale"
    )
    laws = (
        _law("vacuum capacitance", c0 * gap - eps * area, "parallel-plate theorem"),
        _law(
            "metal capacitance",
            cm * (gap - thickness) - eps * area,
            "zero field in conductor",
        ),
        _law(
            "isolated charge",
            charge - cm * voltage,
            "charge conservation after disconnect",
        ),
        _law("initial energy", 2 * initial_energy * cm - charge**2, "capacitor energy"),
        _law("final energy", 2 * final_energy * c0 - charge**2, "capacitor energy"),
        _law(
            "mechanical work",
            work - final_energy + initial_energy,
            "quasistatic energy balance",
        ),
        _law(
            "positive plate scale",
            eps * area * inverse_scale - 1,
            "positive permittivity and plate area",
        ),
        _law(
            "dielectric capacitance",
            cd * (er * (gap - thickness) + thickness) - eps * er * area,
            "series dielectric layers",
        ),
    )
    specs = (
        ("vacuum capacitance", c0, ("vacuum capacitance",), (eps, area, gap)),
        ("metal capacitance", cm, ("metal capacitance",), (eps, area, gap, thickness)),
        (
            "extraction work",
            work,
            tuple(law.name for law in laws[:7]),
            (eps, area, gap, thickness, voltage),
        ),
        (
            "dielectric capacitance",
            cd,
            ("dielectric capacitance",),
            (eps, area, gap, thickness, er),
        ),
    )
    packet = _packet(
        "A24-09",
        7,
        laws,
        specs,
        regime=("edge effects neglected", "inserted slabs span the plate area"),
        branches=("0 < thickness < gap", "eps > 0 and er > 0"),
    )
    expectations = (
        TargetExpectation("vacuum capacitance", c0 * gap - eps * area),
        TargetExpectation("metal capacitance", cm * (gap - thickness) - eps * area),
        TargetExpectation(
            "extraction work",
            2 * work * (gap - thickness) ** 2 - eps * area * voltage**2 * thickness,
        ),
        TargetExpectation(
            "dielectric capacitance",
            cd * (er * (gap - thickness) + thickness) - eps * er * area,
        ),
    )
    return BatchCase(packet, "complete", expectations, "all four subparts")


def _a22_03() -> BatchCase:
    beta, gamma, force_per_mass, parallel, perpendicular = symbols(
        "beta gamma force_per_mass parallel perpendicular"
    )
    laws = (
        _law("Lorentz factor", gamma**2 * (1 - beta**2) - 1, "special relativity"),
        _law(
            "parallel dynamics",
            parallel * gamma**3 - force_per_mass,
            "F parallel to velocity",
        ),
        _law(
            "perpendicular dynamics",
            perpendicular * gamma - force_per_mass,
            "F perpendicular to velocity",
        ),
    )
    packet = _packet(
        "A22-03",
        10,
        laws,
        (
            (
                "parallel acceleration",
                parallel,
                ("Lorentz factor", "parallel dynamics"),
                (beta, force_per_mass),
            ),
            (
                "perpendicular acceleration",
                perpendicular,
                ("Lorentz factor", "perpendicular dynamics"),
                (beta, force_per_mass),
            ),
        ),
        regime=("instantaneous force decomposition in the laboratory frame",),
        branches=("gamma > 0", "acceleration component has the force-component sign"),
    )
    expectations = (
        TargetExpectation(
            "parallel acceleration",
            parallel**2 - force_per_mass**2 * (1 - beta**2) ** 3,
        ),
        TargetExpectation(
            "perpendicular acceleration",
            perpendicular**2 - force_per_mass**2 * (1 - beta**2),
        ),
    )
    return BatchCase(packet, "complete", expectations, "both requested orientations")


def _a20_03() -> BatchCase:
    root2, acceleration1, acceleration2, ratio = symbols(
        "root2 acceleration1 acceleration2 ratio"
    )
    laws = (
        _law("geometry radical", root2**2 - 2, "initial 45-degree geometry"),
        _law(
            "rod AB equation",
            16 * acceleration1 - 9 * root2,
            "initial Lagrange equation",
        ),
        _law(
            "rod BC equation",
            4 * acceleration2 - 3 * root2,
            "initial Lagrange equation",
        ),
        _law(
            "ratio definition",
            ratio * acceleration2 - acceleration1,
            "requested magnitude ratio",
        ),
    )
    packet = _packet(
        "A20-03",
        15,
        laws,
        (
            (
                "angular-acceleration ratio",
                ratio,
                tuple(law.name for law in laws),
                (ratio,),
            ),
        ),
        regime=("uniform identical rods released from rest",),
        branches=("root2 > 0; both initial angular accelerations have the same sign",),
    )
    return BatchCase(
        packet,
        "complete",
        (TargetExpectation("angular-acceleration ratio", 4 * ratio - 3),),
        "requested ratio",
    )


def _a19_07() -> BatchCase:
    ell, energy, angular, magnetic = symbols("ell energy angular magnetic")
    laws = (
        _law("ground orbital state", ell, "hydrogen 1s has l=0"),
        _law("ground energy", 5 * energy + 68, "hydrogenic spectrum in eV"),
        _law("orbital angular momentum", angular - ell, "units chosen as hbar for l=0"),
        _law(
            "orbital magnetic moment",
            magnetic - ell,
            "units chosen as Bohr magneton for l=0",
        ),
    )
    packet = _packet(
        "A19-07",
        19,
        laws,
        (
            ("energy eV", energy, ("ground orbital state", "ground energy"), (energy,)),
            (
                "orbital angular momentum",
                angular,
                ("ground orbital state", "orbital angular momentum"),
                (angular,),
            ),
            (
                "orbital magnetic moment",
                magnetic,
                ("ground orbital state", "orbital magnetic moment"),
                (magnetic,),
            ),
        ),
        regime=("nonrelativistic hydrogen ground state", "orbital moment only"),
        branches=(),
    )
    expectations = (
        TargetExpectation("energy eV", 5 * energy + 68),
        TargetExpectation("orbital angular momentum", angular),
        TargetExpectation("orbital magnetic moment", magnetic),
    )
    return BatchCase(packet, "complete", expectations, "all three requested quantities")


def _a18_04() -> BatchCase:
    charge, radius, coulomb = symbols("charge radius coulomb")
    inner, shell_inner, outer = symbols("inner shell_inner outer")
    field_gap, field_out = symbols("field_gap field_out")
    potential_inverse, potential_constant, shell_potential = symbols(
        "potential_inverse potential_constant shell_potential"
    )
    energy, capacitance = symbols("energy capacitance")
    laws = (
        _law(
            "ground condition",
            5 * inner + 2 * charge,
            "zero potential on the grounded inner sphere",
        ),
        _law("inner shell charge", shell_inner + inner, "zero field in the conductor"),
        _law("outer shell charge", outer - charge - inner, "outer-shell net charge"),
        _law(
            "gap field coefficient",
            field_gap - coulomb * inner,
            "Gauss-law radial field",
        ),
        _law(
            "outer field coefficient",
            field_out - coulomb * (charge + inner),
            "Gauss-law exterior field",
        ),
        _law(
            "gap inverse potential", potential_inverse - field_gap, "radial integration"
        ),
        _law(
            "gap constant potential",
            6 * radius * potential_constant
            - 3 * coulomb * shell_inner
            - 2 * coulomb * outer,
            "shell potentials inside each shell",
        ),
        _law(
            "shell potential",
            3 * radius * shell_potential - coulomb * outer,
            "outer-surface potential",
        ),
        _law(
            "gap energy",
            4 * radius * energy - coulomb * inner**2,
            "field energy between radii a and 2a",
        ),
        _law(
            "capacitance",
            capacitance * coulomb - 2 * radius,
            "concentric-sphere capacitance",
        ),
    )
    common = (charge, radius, coulomb)
    specs = tuple(
        (name, target, law_names, common)
        for name, target, law_names in (
            ("inner charge", inner, ("ground condition",)),
            (
                "shell inner charge",
                shell_inner,
                ("ground condition", "inner shell charge"),
            ),
            ("outer charge", outer, ("ground condition", "outer shell charge")),
            ("gap field", field_gap, ("ground condition", "gap field coefficient")),
            ("outer field", field_out, ("ground condition", "outer field coefficient")),
            (
                "gap inverse potential",
                potential_inverse,
                ("ground condition", "gap field coefficient", "gap inverse potential"),
            ),
            (
                "gap constant potential",
                potential_constant,
                (
                    "ground condition",
                    "inner shell charge",
                    "outer shell charge",
                    "gap constant potential",
                ),
            ),
            (
                "shell potential",
                shell_potential,
                ("ground condition", "outer shell charge", "shell potential"),
            ),
            ("gap energy", energy, ("ground condition", "gap energy")),
            ("capacitance", capacitance, ("capacitance", "ground condition")),
        )
    )
    packet = _packet(
        "A18-04",
        21,
        laws,
        specs,
        regime=(
            "spherical symmetry",
            "field and potential returned as coefficients on declared radial regions",
        ),
        branches=("radius > 0 and capacitance > 0",),
    )
    expectations = (
        TargetExpectation("inner charge", 5 * inner + 2 * charge),
        TargetExpectation("shell inner charge", 5 * shell_inner - 2 * charge),
        TargetExpectation("outer charge", 5 * outer - 3 * charge),
        TargetExpectation("gap field", 5 * field_gap + 2 * coulomb * charge),
        TargetExpectation("outer field", 5 * field_out - 3 * coulomb * charge),
        TargetExpectation(
            "gap inverse potential", 5 * potential_inverse + 2 * coulomb * charge
        ),
        TargetExpectation(
            "gap constant potential",
            5 * radius * potential_constant - 2 * coulomb * charge,
        ),
        TargetExpectation(
            "shell potential", 5 * radius * shell_potential - coulomb * charge
        ),
        TargetExpectation("gap energy", 25 * radius * energy - coulomb * charge**2),
        TargetExpectation("capacitance", capacitance * coulomb - 2 * radius),
    )
    return BatchCase(
        packet,
        "complete",
        expectations,
        "all four subparts via radial-region coefficients",
    )


def _a16_03() -> BatchCase:
    given_velocity, bottom_velocity, opposite_velocity, momentum, mass, inverse_mass = (
        symbols(
            "given_velocity bottom_velocity opposite_velocity momentum mass inverse_mass"
        )
    )
    laws = (
        _law(
            "given rod velocity",
            bottom_velocity - given_velocity,
            "rod 1 centre velocity",
        ),
        _law("mass nonzero", mass * inverse_mass - 1, "positive rod mass"),
        _law(
            "unforced coordinate momentum",
            momentum,
            "zero impulse conjugate to opposite-edge motion",
        ),
        _law(
            "symmetric kinetic metric",
            3 * momentum - mass * (-bottom_velocity + 10 * opposite_velocity),
            "uniform-rod kinetic energy on the symmetric linkage constraint",
        ),
    )
    packet = _packet(
        "A16-03",
        23,
        laws,
        (
            (
                "opposite rod velocity",
                opposite_velocity,
                tuple(law.name for law in laws),
                (given_velocity, opposite_velocity),
            ),
        ),
        regime=(
            "infinitesimal impulse",
            "mirror-symmetric response of the regular hexagon",
        ),
        branches=(),
    )
    return BatchCase(
        packet,
        "complete",
        (
            TargetExpectation(
                "opposite rod velocity", 10 * opposite_velocity - given_velocity
            ),
        ),
        "requested rod-4 velocity",
    )


def _a16_04() -> BatchCase:
    charge, radius, coulomb = symbols("charge radius coulomb")
    macro_ed, field_e0, assignment, context = symbols(
        "macro_ed field_e0 assignment context"
    )
    laws = (
        _law(
            "ED convention",
            8 * radius * macro_ed - 19 * coulomb * charge**2,
            "integral of E dot D over two radial regions",
        ),
        _law(
            "epsilon0 convention",
            16 * radius * field_e0 - 37 * coulomb * charge**2,
            "integral of epsilon0 E squared over two radial regions",
        ),
        _law("source context", context - charge, "source charge anchor only"),
    )
    packet = _packet(
        "A16-04",
        24,
        laws,
        (
            (
                "ED energy",
                macro_ed,
                ("ED convention", "source context"),
                (charge, radius, coulomb, macro_ed),
            ),
            (
                "epsilon0 field energy",
                field_e0,
                ("epsilon0 convention", "source context"),
                (charge, radius, coulomb, field_e0),
            ),
            (
                "source-term assignment",
                assignment,
                ("source context",),
                (charge, assignment),
            ),
        ),
        regime=(
            "thin concentric shells",
            "dielectric permittivity 2 epsilon0 only between shells",
        ),
        branches=(
            "the compilation does not define which convention its two energy labels denote",
        ),
    )
    expectations = (
        TargetExpectation(
            "ED energy", 8 * radius * macro_ed - 19 * coulomb * charge**2
        ),
        TargetExpectation(
            "epsilon0 field energy", 16 * radius * field_e0 - 37 * coulomb * charge**2
        ),
        TargetExpectation("source-term assignment", None),
    )
    return BatchCase(
        packet,
        "partial",
        expectations,
        "both candidate values but unresolved label semantics",
    )


def _a15_07() -> BatchCase:
    first, second, total = symbols("first second total")
    laws = (
        _law("first ionization", 5 * first - 123, "given 24.6 eV"),
        _law("He plus ionization", 5 * second - 272, "hydrogenic Z=2 ion"),
        _law(
            "total ionization",
            total - first - second,
            "successive ionization energy sum",
        ),
    )
    packet = _packet(
        "A15-07",
        26,
        laws,
        (("total eV", total, tuple(law.name for law in laws), (total,)),),
        regime=("nonrelativistic hydrogenic He+",),
        branches=(),
    )
    return BatchCase(
        packet,
        "complete",
        (TargetExpectation("total eV", total - 79),),
        "requested total",
    )


def _a15_08() -> BatchCase:
    mass, boltzmann, temperature, planck, momentum, wavelength = symbols(
        "mass boltzmann temperature planck momentum wavelength"
    )
    laws = (
        _law(
            "thermal momentum",
            momentum**2 - 3 * mass * boltzmann * temperature,
            "mean kinetic energy 3 k T / 2",
        ),
        _law("de Broglie", wavelength * momentum - planck, "de Broglie relation"),
    )
    packet = _packet(
        "A15-08",
        26,
        laws,
        (
            (
                "wavelength",
                wavelength,
                tuple(law.name for law in laws),
                (mass, boltzmann, temperature, planck, wavelength),
            ),
        ),
        regime=("nonrelativistic thermal neutron",),
        branches=("momentum > 0 and wavelength > 0",),
    )
    expected = 3 * mass * boltzmann * temperature * wavelength**2 - planck**2
    return BatchCase(
        packet,
        "complete",
        (TargetExpectation("wavelength", expected),),
        "requested wavelength",
    )


def _a14_08() -> BatchCase:
    lambda_h, lambda_t, separation, spectral_label, context = symbols(
        "lambda_h lambda_t separation spectral_label context"
    )
    numerator = 1836 * 5509
    denominator = 1837 * 5508
    laws = (
        _law(
            "reduced-mass wavelength",
            denominator * lambda_t - numerator * lambda_h,
            "hydrogen versus tritium reduced mass",
        ),
        _law(
            "line separation",
            separation - lambda_h + lambda_t,
            "positive H-minus-tritium wavelength separation",
        ),
        _law("pattern context", context - lambda_h, "shared Balmer pattern anchor"),
    )
    packet = _packet(
        "A14-08",
        28,
        laws,
        (
            (
                "Balmer separation",
                separation,
                ("reduced-mass wavelength", "line separation"),
                (lambda_h, separation),
            ),
            (
                "unmeasured isotope label",
                spectral_label,
                ("pattern context",),
                (lambda_h, spectral_label),
            ),
        ),
        regime=("proton and neutron masses each 1836 electron masses",),
        branches=(
            "the first subpart is an identifiability statement rather than a polynomial observable",
        ),
    )
    expected = denominator * separation - (denominator - numerator) * lambda_h
    return BatchCase(
        packet,
        "partial",
        (
            TargetExpectation("Balmer separation", expected),
            TargetExpectation("unmeasured isotope label", None),
        ),
        "numeric isotope shift only",
    )


def _a13_01() -> BatchCase:
    gravity, omega, speed, width, sine_latitude, coriolis, height = symbols(
        "gravity omega speed width sine_latitude coriolis height"
    )
    laws = (
        _law(
            "Coriolis acceleration",
            coriolis - 2 * omega * speed * sine_latitude,
            "rotating-Earth frame",
        ),
        _law(
            "free-surface balance",
            gravity * height - coriolis * width,
            "hydrostatic effective-gravity slope",
        ),
    )
    packet = _packet(
        "A13-01",
        29,
        laws,
        (
            (
                "east-west height",
                height,
                tuple(law.name for law in laws),
                (gravity, omega, speed, width, sine_latitude, height),
            ),
        ),
        regime=("steady northward flow", "small surface slope"),
        branches=("east bank is higher for positive northern latitude",),
    )
    expected = gravity * height - 2 * omega * speed * width * sine_latitude
    return BatchCase(
        packet,
        "complete",
        (TargetExpectation("east-west height", expected),),
        "requested height difference",
    )


def _a13_02() -> BatchCase:
    impact_speed, launch_speed, gravity, height, alpha, density, area, mass = symbols(
        "impact_speed launch_speed gravity height alpha density area mass"
    )
    laws = (
        _law(
            "ballistic speed",
            impact_speed**2 - launch_speed**2 + 2 * gravity * height,
            "energy along the rising jet",
        ),
        _law(
            "momentum flux",
            (2 - alpha) * density * area * launch_speed * impact_speed - mass * gravity,
            "absorbed plus reflected water momentum",
        ),
    )
    packet = _packet(
        "A13-02",
        29,
        laws,
        (
            (
                "support height",
                height,
                tuple(law.name for law in laws),
                (launch_speed, gravity, alpha, density, area, mass, height),
            ),
        ),
        regime=(
            "steady non-dispersing jet",
            "attached fraction leaves with negligible speed",
        ),
        branches=("impact_speed >= 0 and height >= 0",),
    )
    expected = (2 - alpha) ** 2 * density**2 * area**2 * launch_speed**2 * (
        launch_speed**2 - 2 * gravity * height
    ) - mass**2 * gravity**2
    return BatchCase(
        packet,
        "complete",
        (TargetExpectation("support height", expected),),
        "requested height",
    )


def _a13_06() -> BatchCase:
    conductivity, permittivity, omega, field, inverse_field = symbols(
        "conductivity permittivity omega field inverse_field"
    )
    conduction, displacement, ratio = symbols("conduction displacement ratio")
    laws = (
        _law(
            "nonzero field",
            field * inverse_field - 1,
            "nonzero AC amplitude for a defined ratio",
        ),
        _law("Ohmic current", conduction - conductivity * field, "Jc = sigma E"),
        _law(
            "displacement current",
            displacement - permittivity * omega * field,
            "sinusoidal Jd amplitude",
        ),
        _law(
            "ratio definition", ratio * displacement - conduction, "requested RMS ratio"
        ),
    )
    packet = _packet(
        "A13-06",
        30,
        laws,
        (
            (
                "current-density ratio",
                ratio,
                tuple(law.name for law in laws),
                (conductivity, permittivity, omega, ratio),
            ),
        ),
        regime=("linear isotropic conductor", "single-frequency steady state"),
        branches=(),
    )
    expected = permittivity * omega * ratio - conductivity
    return BatchCase(
        packet,
        "complete",
        (TargetExpectation("current-density ratio", expected),),
        "requested ratio",
    )


def _a13_09() -> BatchCase:
    lambda_one, lambda_two, hc, magneton, splitting, field = symbols(
        "lambda_one lambda_two hc magneton splitting field"
    )
    l1 = Rational(589593, 1000)
    l2 = Rational(588996, 1000)
    laws = (
        _law("D1 wavelength", lambda_one - l1, "589.593 nm"),
        _law("D2 wavelength", lambda_two - l2, "588.996 nm"),
        _law(
            "fine splitting",
            splitting * lambda_one * lambda_two - hc * (lambda_one - lambda_two),
            "photon-energy difference",
        ),
        _law(
            "level crossing",
            7 * magneton * field - 3 * splitting,
            "g(P3/2)=4/3 and g(P1/2)=2/3",
        ),
    )
    packet = _packet(
        "A13-09",
        30,
        laws,
        (
            (
                "crossing field",
                field,
                tuple(law.name for law in laws),
                (hc, magneton, field),
            ),
        ),
        regime=("weak-field Zeeman effect",),
        branches=("field > 0",),
    )
    expected = 7 * magneton * field * l1 * l2 - 3 * hc * (l1 - l2)
    return BatchCase(
        packet,
        "complete",
        (TargetExpectation("crossing field", expected),),
        "requested magnetic field",
    )


def _a11_03() -> BatchCase:
    rest_length, lab_length, light_speed, time, position = symbols(
        "rest_length lab_length light_speed time position"
    )
    laws = (
        _law("given rest length", rest_length - 90, "source value in metres"),
        _law(
            "length contraction", 5 * lab_length - 3 * rest_length, "gamma=5/3 at 0.8c"
        ),
        _law(
            "ship head worldline",
            5 * position - 5 * lab_length - 4 * light_speed * time,
            "head moves at 0.8c",
        ),
        _law(
            "light worldline",
            position - light_speed * time,
            "light signal from the station",
        ),
        _law("light speed value", light_speed - 300000000, "3e8 m/s"),
    )
    packet = _packet(
        "A11-03",
        33,
        laws,
        (
            (
                "meeting distance metres",
                position,
                tuple(law.name for law in laws),
                (position,),
            ),
            ("meeting time seconds", time, tuple(law.name for law in laws), (time,)),
        ),
        regime=("ground inertial frame",),
        branches=("time > 0",),
    )
    expectations = (
        TargetExpectation("meeting distance metres", position - 270),
        TargetExpectation("meeting time seconds", 10000000 * time - 9),
    )
    return BatchCase(packet, "complete", expectations, "both requested outputs")


def _a11_07() -> BatchCase:
    reduced_mass, energy, muon_radius, electron_radius = symbols(
        "reduced_mass energy muon_radius electron_radius"
    )
    radial_shape, context = symbols("radial_shape context")
    laws = (
        _law(
            "reduced mass",
            7507 * reduced_mass - 207 * 7300,
            "muon and helium-nucleus reduced mass in electron-mass units",
        ),
        _law(
            "muonic energy",
            5 * energy - 272 * reduced_mass,
            "hydrogenic Z=2 binding magnitude in eV",
        ),
        _law(
            "muonic radius",
            2 * reduced_mass * muon_radius - 1,
            "Bohr radius in units of a0",
        ),
        _law(
            "screened electron radius",
            electron_radius - 1,
            "compact muon screens one nuclear charge",
        ),
        _law("shape context", context - reduced_mass, "mass-scale anchor only"),
    )
    packet = _packet(
        "A11-07",
        34,
        laws,
        (
            (
                "binding magnitude eV",
                energy,
                ("reduced mass", "muonic energy"),
                (energy,),
            ),
            (
                "muon radius over a0",
                muon_radius,
                ("reduced mass", "muonic radius"),
                (muon_radius,),
            ),
            (
                "electron radius over a0",
                electron_radius,
                ("reduced mass", "screened electron radius"),
                (electron_radius,),
            ),
            (
                "radial probability curve",
                radial_shape,
                ("shape context",),
                (radial_shape,),
            ),
        ),
        regime=(
            "nonrelativistic hydrogenic approximation",
            "muon orbit much smaller than electron orbit",
        ),
        branches=(
            "energy is reported as positive binding magnitude",
            "probability-curve and chemical-analogy returns are not polynomial targets",
        ),
    )
    expectations = (
        TargetExpectation("binding magnitude eV", 7507 * 5 * energy - 272 * 207 * 7300),
        TargetExpectation("muon radius over a0", 2 * 207 * 7300 * muon_radius - 7507),
        TargetExpectation("electron radius over a0", electron_radius - 1),
        TargetExpectation("radial probability curve", None),
    )
    return BatchCase(
        packet,
        "partial",
        expectations,
        "three scalar subparts; curve and analogy remain semantic",
    )


def _a10_01() -> BatchCase:
    mass1, mass2, gravity, relative = symbols("mass1 mass2 gravity relative")
    mass1_x, mass1_y, mass2_y = symbols("mass1_x mass1_y mass2_y")
    laws = (
        _law(
            "cabin Atwood acceleration",
            2 * (mass1 + mass2) * relative - 3 * mass2 * gravity,
            "effective gravity 3g/2 in the cabin",
        ),
        _law("mass1 horizontal", mass1_x - relative, "rope constraint in cabin"),
        _law("mass1 vertical", 2 * mass1_y - gravity, "elevator translation"),
        _law(
            "mass2 ground vertical",
            2 * mass2_y - gravity + 2 * relative,
            "elevator acceleration minus downward relative acceleration",
        ),
    )
    common = (mass1, mass2, gravity)
    packet = _packet(
        "A10-01",
        35,
        laws,
        (
            (
                "cabin relative magnitude",
                relative,
                ("cabin Atwood acceleration", "mass1 horizontal"),
                common,
            ),
            (
                "mass1 ground horizontal",
                mass1_x,
                ("cabin Atwood acceleration", "mass1 horizontal"),
                common,
            ),
            (
                "mass1 ground vertical",
                mass1_y,
                ("cabin Atwood acceleration", "mass1 vertical"),
                common,
            ),
            (
                "mass2 ground vertical",
                mass2_y,
                ("cabin Atwood acceleration", "mass2 ground vertical"),
                common,
            ),
        ),
        regime=(
            "massless rope and pulley",
            "frictionless support",
            "upward ground direction positive",
        ),
        branches=("relative is the downward magnitude for mass2",),
    )
    expectations = (
        TargetExpectation(
            "cabin relative magnitude",
            2 * (mass1 + mass2) * relative - 3 * mass2 * gravity,
        ),
        TargetExpectation(
            "mass1 ground horizontal",
            2 * (mass1 + mass2) * mass1_x - 3 * mass2 * gravity,
        ),
        TargetExpectation("mass1 ground vertical", 2 * mass1_y - gravity),
        TargetExpectation(
            "mass2 ground vertical",
            2 * (mass1 + mass2) * mass2_y - gravity * (mass1 - 2 * mass2),
        ),
    )
    return BatchCase(
        packet,
        "complete",
        expectations,
        "cabin and ground-frame acceleration components",
    )


def _a10_03() -> BatchCase:
    single_beta, relative_beta, gamma, proper_length, measured_length = symbols(
        "single_beta relative_beta gamma proper_length measured_length"
    )
    laws = (
        _law("single speed", 5 * single_beta - 3, "each ruler has speed 0.6c in K"),
        _law(
            "relative velocity",
            relative_beta * (1 + single_beta**2) - 2 * single_beta,
            "relativistic velocity addition",
        ),
        _law(
            "relative Lorentz factor",
            gamma**2 * (1 - relative_beta**2) - 1,
            "special relativity",
        ),
        _law(
            "length contraction",
            measured_length * gamma - proper_length,
            "moving-ruler length",
        ),
    )
    packet = _packet(
        "A10-03",
        35,
        laws,
        (
            (
                "measured length",
                measured_length,
                tuple(law.name for law in laws),
                (proper_length, measured_length),
            ),
        ),
        regime=("parallel inertial rulers",),
        branches=("gamma > 0 and measured_length > 0",),
    )
    expected = 289 * measured_length**2 - 64 * proper_length**2
    return BatchCase(
        packet,
        "complete",
        (TargetExpectation("measured length", expected),),
        "reciprocal measured length",
    )


def build_polynomial_batch() -> tuple[BatchCase, ...]:
    return (
        _a25_03(),
        _a24_09(),
        _a22_03(),
        _a20_03(),
        _a19_07(),
        _a18_04(),
        _a16_03(),
        _a16_04(),
        _a15_07(),
        _a15_08(),
        _a14_08(),
        _a13_01(),
        _a13_02(),
        _a13_06(),
        _a13_09(),
        _a11_03(),
        _a11_07(),
        _a10_01(),
        _a10_03(),
    )


def run_polynomial_batch() -> tuple[CheckedBatchCase, ...]:
    checked = []
    for case in build_polynomial_batch():
        result = compile_polynomial_problem(case.packet)
        passed = result.status == case.expected_status
        for expectation in case.expectations:
            target_result = result.target(expectation.name)
            if expectation.relation is None:
                passed = passed and target_result.status == "underdetermined"
            else:
                passed = passed and target_result.status == "constrained"
                passed = passed and target_result.implies(expectation.relation)
        checked.append(CheckedBatchCase(case, result, passed))
    return tuple(checked)


def _print_counts(title: str, counts: dict[object, int]) -> None:
    print(title)
    for key, count in counts.items():
        print(f"  {key}: {count}")


def command_corpus_audit() -> None:
    result = summarize_corpus(load_corpus_index(CORPUS))
    print(f"total: {result.total}")
    print(
        f"years: {len(result.years)} "
        f"({min(result.years)}-{max(result.years)}; 2017 absent)"
    )
    _print_counts("by area", result.by_area)
    _print_counts("by family", result.by_family)
    _print_counts("by evidence", result.by_evidence)
    _print_counts("by next operator", result.by_next_operator)


def command_polynomial_batch() -> None:
    results = run_polynomial_batch()
    for checked in results:
        print(
            f"{checked.case.packet.problem_id}\t{checked.result.status}\t"
            f"{len(checked.result.targets)} targets\t"
            f"certificate={'pass' if checked.certificates_passed else 'FAIL'}"
        )
    print(
        f"batch: {sum(item.certificates_passed for item in results)}/{len(results)} passed"
    )
