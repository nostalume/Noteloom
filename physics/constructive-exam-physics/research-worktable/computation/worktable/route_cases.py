"""Locked structural-action comparison for six source-bound A617 problems.

The ledgers count atomic symbolic subjects and explicit semantic operations on the
handwritten substrate, not elapsed time or cognitive load. They are an auditable
first feasibility gate, not learner-performance data.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction

from occ.cost import (
    COST_AXES,
    AdmissionBoundary,
    AdmissionDecision,
    CostProfile,
    ExamAction,
    HandwrittenRoute,
    RouteComparison,
    compare_exam_routes,
    construct_admission_boundary,
    evaluate_route_admission,
)
from occ.calibration import calibrate_paired_route_costs


@dataclass(frozen=True)
class RouteBenchmarkCase:
    problem_id: str
    pdf_page: int
    area: str
    source_scope: str
    baseline: HandwrittenRoute
    proposed: HandwrittenRoute


@dataclass(frozen=True)
class RouteBenchmarkResult:
    comparisons: tuple[RouteComparison, ...]
    verdict: str

    @property
    def proposed_wins(self) -> int:
        return sum(item.status == "proposed_win" for item in self.comparisons)


def _a(
    kind: str,
    description: str,
    live: int = 0,
    symbolic_subjects: tuple[str, ...] = (),
) -> ExamAction:
    return ExamAction(kind, description, live, symbolic_subjects)


def _route(
    problem_id: str,
    target: str,
    hidden: tuple[str, ...],
    actions: tuple[ExamAction, ...],
) -> HandwrittenRoute:
    return HandwrittenRoute(problem_id, target, hidden, actions)


def _a25_03() -> RouteBenchmarkCase:
    problem_id = "A25-03"
    target = "electron proper crossing time in days"
    baseline = _route(
        problem_id,
        target,
        ("gamma", "beta"),
        (
            _a("relation", "gamma = electron energy / rest energy", 1),
            _a("relation", "gamma^2(1-beta^2)=1", 2),
            _a("relation", "proper days * gamma * beta = 36,000,000", 3),
            _a("symbolic", "substitute the energy ratio", 3, ("gamma",)),
            _a(
                "symbolic", "solve the positive proper-time branch", 1, ("proper time",)
            ),
            _a("branch", "require beta>0 and elapsed time>0", 1),
            _a("return", "recover light-year/year/day units", 1),
        ),
    )
    proposed = _route(
        problem_id,
        target,
        ("gamma", "beta"),
        (
            _a("relation", "bind the relativistic energy ratio", 1),
            _a("relation", "bind the Lorentz speed relation", 2),
            _a("relation", "bind the proper crossing relation", 3),
            _a("representation", "encode the physical packet as polynomials", 3),
            _a("symbolic", "eliminate gamma and beta", 3, ("gamma", "beta")),
            _a("symbolic", "solve the retained time relation", 1, ("proper time",)),
            _a("branch", "select beta>0 and elapsed time>0", 1),
            _a("return", "restore the proper-time and day convention", 1),
        ),
    )
    return RouteBenchmarkCase(
        problem_id, 4, "relativity", "2025 problem 3", baseline, proposed
    )


def _a24_09_3() -> RouteBenchmarkCase:
    problem_id = "A24-09-3"
    target = "work required to remove the metal slab"
    baseline = _route(
        problem_id,
        target,
        ("C_m", "C_0", "Q", "U_i", "U_f"),
        (
            _a("relation", "C_m = epsilon S/(d-l)", 1),
            _a("relation", "Q = C_m U_0 after disconnection", 2),
            _a("symbolic", "substitute C_m into Q", 1, ("Q",)),
            _a("relation", "U_i = Q^2/(2 C_m)", 2),
            _a("symbolic", "substitute charge and C_m into U_i", 1, ("U_i",)),
            _a("relation", "C_0 = epsilon S/d", 2),
            _a("relation", "U_f = Q^2/(2 C_0)", 3),
            _a("symbolic", "substitute charge and C_0 into U_f", 1, ("U_f",)),
            _a("relation", "W = U_f-U_i", 2),
            _a("symbolic", "substitute both energies", 2, ("W",)),
            _a("symbolic", "factor the retained work expression", 1, ("W",)),
            _a("branch", "require 0<l<d and positive capacitances", 1),
            _a("return", "check fixed charge after source disconnection", 1),
        ),
    )
    proposed = _route(
        problem_id,
        target,
        ("C_m", "C_0", "Q", "U_i", "U_f"),
        (
            _a("relation", "bind the metal-slab capacitance", 1),
            _a("relation", "bind isolated charge", 2),
            _a("relation", "bind initial capacitor energy", 3),
            _a("relation", "bind vacuum capacitance", 4),
            _a("relation", "bind final capacitor energy", 5),
            _a("relation", "bind quasistatic work balance", 6),
            _a("representation", "encode the six-law packet", 6),
            _a(
                "symbolic",
                "eliminate five hidden quantities",
                6,
                ("C_m", "C_0", "Q", "U_i", "U_f"),
            ),
            _a("symbolic", "factor the retained work relation", 1, ("W",)),
            _a("branch", "require 0<l<d and positive capacitances", 1),
            _a("return", "restore fixed-charge process semantics", 1),
        ),
    )
    return RouteBenchmarkCase(
        problem_id,
        7,
        "electromagnetism",
        "2024 problem 9, subpart 3",
        baseline,
        proposed,
    )


def _a22_03_1() -> RouteBenchmarkCase:
    problem_id = "A22-03-1"
    target = "acceleration parallel to relativistic velocity"
    baseline = _route(
        problem_id,
        target,
        ("gamma",),
        (
            _a("relation", "gamma^2(1-beta^2)=1", 1),
            _a("relation", "a_parallel gamma^3 = F/m", 2),
            _a("symbolic", "substitute gamma(beta)", 2, ("a_parallel",)),
            _a("symbolic", "solve for the signed acceleration", 1, ("a_parallel",)),
            _a("branch", "take gamma>0 and the force-component sign", 1),
            _a("return", "recover the laboratory parallel component", 1),
        ),
    )
    proposed = _route(
        problem_id,
        target,
        ("gamma",),
        (
            _a("relation", "bind the Lorentz-factor relation", 1),
            _a("relation", "bind parallel relativistic dynamics", 2),
            _a("representation", "encode both relations as polynomials", 2),
            _a("symbolic", "eliminate gamma", 2, ("gamma",)),
            _a(
                "symbolic", "recover the signed acceleration branch", 1, ("a_parallel",)
            ),
            _a("branch", "take gamma>0 and the force-component sign", 1),
            _a("return", "restore the laboratory component meaning", 1),
        ),
    )
    return RouteBenchmarkCase(
        problem_id, 10, "relativity", "2022 problem 3, subpart 1", baseline, proposed
    )


def _a15_08() -> RouteBenchmarkCase:
    problem_id = "A15-08"
    target = "thermal neutron de Broglie wavelength"
    baseline = _route(
        problem_id,
        target,
        ("momentum",),
        (
            _a("relation", "p^2/(2m)=3kT/2", 1),
            _a("relation", "lambda p = h", 2),
            _a("symbolic", "solve for positive thermal momentum", 2, ("momentum",)),
            _a(
                "symbolic",
                "substitute momentum into de Broglie relation",
                1,
                ("wavelength",),
            ),
            _a("branch", "require p>0 and lambda>0", 1),
            _a("return", "convert the wavelength to the requested unit", 1),
        ),
    )
    proposed = _route(
        problem_id,
        target,
        ("momentum",),
        (
            _a("relation", "bind the thermal momentum relation", 1),
            _a("relation", "bind the de Broglie relation", 2),
            _a("representation", "encode the two polynomial relations", 2),
            _a("symbolic", "eliminate momentum", 2, ("momentum",)),
            _a("symbolic", "select the positive wavelength", 1, ("wavelength",)),
            _a("branch", "require p>0 and lambda>0", 1),
            _a("return", "restore the wavelength unit", 1),
        ),
    )
    return RouteBenchmarkCase(
        problem_id,
        26,
        "thermal-quantum",
        "2015 problem 8",
        baseline,
        proposed,
    )


def _a13_02() -> RouteBenchmarkCase:
    problem_id = "A13-02"
    target = "water-supported cylinder height"
    baseline = _route(
        problem_id,
        target,
        ("impact speed", "mass flow rate"),
        (
            _a("relation", "v_i^2=v_0^2-2gH", 1),
            _a("relation", "mass flow rate = rho S v_0", 2),
            _a(
                "symbolic",
                "substitute mass flow into momentum rate",
                1,
                ("momentum rate",),
            ),
            _a("relation", "(2-alpha) mass_flow v_i = mg", 2),
            _a(
                "symbolic",
                "solve momentum balance for impact speed",
                2,
                ("impact speed",),
            ),
            _a("symbolic", "substitute into the ballistic relation", 1, ("height",)),
            _a("branch", "require impact speed>=0", 1),
            _a("branch", "require H>=0 below the free-jet apex", 1),
            _a("return", "check force direction and detached-water convention", 1),
        ),
    )
    proposed = _route(
        problem_id,
        target,
        ("impact speed",),
        (
            _a("relation", "construct mass flux rho S v_0", 1),
            _a("relation", "bind momentum flux using that flux", 2),
            _a("relation", "bind the ballistic speed relation", 2),
            _a("representation", "encode the target-connected packet", 2),
            _a("symbolic", "eliminate impact speed", 2, ("impact speed",)),
            _a("symbolic", "solve the retained height relation", 1, ("height",)),
            _a("branch", "require impact speed>=0", 1),
            _a("branch", "require H>=0 below the free-jet apex", 1),
            _a("return", "restore momentum direction and water fractions", 1),
        ),
    )
    return RouteBenchmarkCase(
        problem_id,
        29,
        "fluid-mechanics",
        "2013 problem 2",
        baseline,
        proposed,
    )


def _a11_03() -> RouteBenchmarkCase:
    problem_id = "A11-03"
    target = "ground-frame light/ship meeting distance and time"
    baseline = _route(
        problem_id,
        target,
        ("contracted ship length",),
        (
            _a("relation", "L=L_0/gamma at v=0.8c", 1),
            _a(
                "symbolic",
                "evaluate the contracted length",
                1,
                ("contracted ship length",),
            ),
            _a("relation", "ship head: x=L+vt", 2),
            _a("relation", "light: x=ct", 2),
            _a(
                "symbolic", "equate the worldlines and solve time", 2, ("meeting time",)
            ),
            _a(
                "symbolic",
                "substitute time to recover distance",
                1,
                ("meeting distance",),
            ),
            _a("branch", "require the future meeting t>0", 1),
            _a("return", "report both observables in the ground frame", 1),
        ),
    )
    proposed = _route(
        problem_id,
        target,
        ("contracted ship length",),
        (
            _a("relation", "bind length contraction", 1),
            _a("relation", "bind the ship-head worldline", 2),
            _a("relation", "bind the light worldline", 3),
            _a("representation", "encode the joint relation packet", 3),
            _a(
                "symbolic",
                "eliminate contracted length",
                3,
                ("contracted ship length",),
            ),
            _a(
                "symbolic",
                "recover meeting time and distance",
                2,
                ("meeting time", "meeting distance"),
            ),
            _a("branch", "require the future meeting t>0", 1),
            _a("return", "restore both ground-frame observables", 1),
        ),
    )
    return RouteBenchmarkCase(
        problem_id, 33, "relativity", "2011 problem 3", baseline, proposed
    )


def build_route_benchmark() -> tuple[RouteBenchmarkCase, ...]:
    return (
        _a25_03(),
        _a24_09_3(),
        _a22_03_1(),
        _a15_08(),
        _a13_02(),
        _a11_03(),
    )


def run_route_benchmark() -> RouteBenchmarkResult:
    comparisons = tuple(
        compare_exam_routes(case.baseline, case.proposed)
        for case in build_route_benchmark()
    )
    counts = Counter(item.status for item in comparisons)
    if counts["proposed_win"] == len(comparisons):
        verdict = "structural_exam_leverage_supported_on_locked_bench"
    elif counts["proposed_win"] == 0:
        verdict = "exam_leverage_not_established"
    else:
        verdict = "mixed_inconclusive"
    return RouteBenchmarkResult(comparisons=comparisons, verdict=verdict)


def command_route_benchmark() -> None:
    cases = build_route_benchmark()
    result = run_route_benchmark()
    print("problem\tstatus\tbaseline\tproposed\tbetter\tworse")
    for case, comparison in zip(cases, result.comparisons):
        print(
            f"{case.problem_id}\t{comparison.status}\t"
            f"{comparison.baseline.cost.as_tuple()}\t"
            f"{comparison.proposed.cost.as_tuple()}\t"
            f"{','.join(comparison.proposed_better) or '-'}\t"
            f"{','.join(comparison.proposed_worse) or '-'}"
        )
    print(f"verdict\t{result.verdict}")


@dataclass(frozen=True)
class RouteAdmissionCase:
    source: RouteBenchmarkCase
    boundary: AdmissionBoundary
    unit_probe: AdmissionDecision


@dataclass(frozen=True)
class RouteAdmissionResult:
    cases: tuple[RouteAdmissionCase, ...]
    conditionally_admitted_problem_ids: tuple[str, ...]
    verdict: str


def unit_action_probe() -> CostProfile:
    return CostProfile(
        name="unit-action sensitivity probe",
        weights=(Fraction(1),) * len(COST_AXES),
        provenance=(
            "Hypothetical equal written-action costs; a sensitivity probe only, "
            "not learner or timing evidence."
        ),
    )


def run_route_admission() -> RouteAdmissionResult:
    profile = unit_action_probe()
    cases = tuple(
        RouteAdmissionCase(
            source=case,
            boundary=(
                boundary := construct_admission_boundary(case.baseline, case.proposed)
            ),
            unit_probe=evaluate_route_admission(boundary, profile),
        )
        for case in build_route_benchmark()
    )
    admitted = tuple(
        case.source.problem_id
        for case in cases
        if case.boundary.classification == "conditional"
        and case.unit_probe.status == "use_proposed"
    )
    return RouteAdmissionResult(
        cases=cases,
        conditionally_admitted_problem_ids=admitted,
        verdict="conditional_admission_constructed_weights_unmeasured",
    )


def command_route_admission() -> None:
    result = run_route_admission()
    print("problem\tclass\tproposed cheaper when\tunit probe")
    for item in result.cases:
        print(
            f"{item.source.problem_id}\t{item.boundary.classification}\t"
            f"{item.boundary.proposed_cheaper_when}\t{item.unit_probe.status}"
        )
    print(f"verdict\t{result.verdict}")


def command_calibration_probe() -> None:
    result = calibrate_paired_route_costs("unobserved learner", ())
    print("empirical_observations\t0")
    print(f"status\t{result.status}")
    print(f"obstruction\t{result.obstruction.kind}")
    print(f"message\t{result.obstruction.message}")
