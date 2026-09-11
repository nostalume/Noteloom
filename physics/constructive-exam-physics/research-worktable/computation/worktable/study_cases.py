"""Matched numerical variants of six source-bound A617 route structures."""

from __future__ import annotations

from sympy import Matrix, Rational, simplify, sqrt, symbols

from occ.cost import (
    COST_AXES,
    construct_admission_boundary,
)
from occ.study import (
    MatchedVariantPair,
    StudyVariant,
    build_two_sequence_schedule,
)

from .route_cases import build_route_benchmark


epsilon_0, h, m_n, k_B = symbols("epsilon_0 h m_n k_B", positive=True)


def _crossing(variant_id: str, energy_mev, distance_years) -> StudyVariant:
    gamma = Rational(energy_mev) / Rational(1, 2)
    proper_days = simplify(Rational(distance_years) * 360 / sqrt(gamma**2 - 1))
    return StudyVariant(
        variant_id,
        (
            f"An electron of total energy {energy_mev} MeV crosses a region "
            f"{distance_years} light-years wide. Its rest energy is 0.5 MeV. "
            "Using 360 days per year, find the elapsed proper time in days."
        ),
        "special relativity; positive future-directed speed",
        (("proper_days", proper_days),),
    )


def _capacitor(variant_id: str, area, gap, slab, voltage) -> StudyVariant:
    work = simplify(epsilon_0 * area * voltage**2 * slab / (2 * (gap - slab) ** 2))
    return StudyVariant(
        variant_id,
        (
            "A parallel-plate air capacitor has plate area "
            f"{area} m^2 and separation {gap} m. A metal slab of thickness "
            f"{slab} m fills the plate area without touching either plate. "
            f"It is charged to {voltage} V, disconnected, and the slab is "
            "removed quasistatically. Find the required external work in joules."
        ),
        "0 < slab thickness < gap; source disconnected so charge is fixed",
        (("work_joule", work),),
    )


def _parallel_acceleration(variant_id: str, beta, force, mass) -> StudyVariant:
    acceleration = simplify(Rational(force, mass) * (1 - beta**2) ** Rational(3, 2))
    return StudyVariant(
        variant_id,
        (
            f"A particle of mass {mass} kg moves at v={beta}c. A force of "
            f"{force} N is applied parallel to its velocity. Find its laboratory "
            "acceleration in m/s^2."
        ),
        "special relativity; force parallel to velocity",
        (("acceleration_m_s2", acceleration),),
    )


def _neutron(variant_id: str, temperature) -> StudyVariant:
    wavelength = simplify(h / sqrt(3 * m_n * k_B * temperature))
    return StudyVariant(
        variant_id,
        (
            f"Thermal neutrons are in equilibrium at {temperature} K and have "
            "mean kinetic energy 3 k_B T/2. Find their de Broglie wavelength "
            "in metres using neutron mass m_n and Planck constant h."
        ),
        "nonrelativistic thermal neutron; positive momentum and wavelength",
        (("wavelength_m", wavelength),),
    )


def _water_jet(
    variant_id: str, speed, area, density, alpha, mass, gravity
) -> StudyVariant:
    impact_speed = simplify(mass * gravity / ((2 - alpha) * density * area * speed))
    height = simplify((speed**2 - impact_speed**2) / (2 * gravity))
    return StudyVariant(
        variant_id,
        (
            f"A vertical jet leaves an opening of area {area} m^2 at {speed} m/s "
            f"with density {density} kg/m^3 and supports an inverted cylinder of "
            f"mass {mass} kg. A fraction alpha={alpha} sticks and comes nearly to "
            "rest; the rest rebounds vertically downward at the impact speed. "
            f"Take g={gravity} m/s^2 and neglect drag and spreading. Find the "
            "stationary height above the opening."
        ),
        "steady incompressible jet; nonnegative impact speed and height",
        (("height_m", height),),
    )


def _spaceship(variant_id: str, proper_length, beta) -> StudyVariant:
    gamma = simplify(1 / sqrt(1 - beta**2))
    contracted_length = simplify(proper_length / gamma)
    distance = simplify(contracted_length / (1 - beta))
    time_microseconds = simplify(distance / 300)
    return StudyVariant(
        variant_id,
        (
            f"A spaceship of proper length {proper_length} m moves at v={beta}c. "
            "When its tail passes a ground station, the station emits a forward "
            "light pulse. In the ground frame, find the ship-head distance from "
            "the station and the elapsed time when the pulse reaches the head. "
            "Use c=3.00e8 m/s."
        ),
        "ground frame; future light/ship-head meeting",
        (("distance_m", distance), ("time_microseconds", time_microseconds)),
    )


def build_matched_variant_pairs() -> tuple[MatchedVariantPair, ...]:
    cases = {case.problem_id: case for case in build_route_benchmark()}
    specifications = (
        (
            "A25-03",
            "calibration",
            _crossing("A25-03-A", 5, Rational(11, 60)),
            _crossing("A25-03-B", Rational(17, 2), Rational(2, 5)),
        ),
        (
            "A24-09-3",
            "holdout",
            _capacitor(
                "A24-09-3-A", Rational(1, 50), Rational(1, 250), Rational(1, 1000), 300
            ),
            _capacitor(
                "A24-09-3-B", Rational(3, 100), Rational(3, 500), Rational(1, 500), 200
            ),
        ),
        (
            "A22-03-1",
            "holdout",
            _parallel_acceleration("A22-03-1-A", Rational(3, 5), 125, 1),
            _parallel_acceleration("A22-03-1-B", Rational(4, 5), 250, 2),
        ),
        (
            "A15-08",
            "calibration",
            _neutron("A15-08-A", 300),
            _neutron("A15-08-B", 675),
        ),
        (
            "A13-02",
            "calibration",
            _water_jet("A13-02-A", 10, Rational(1, 1000), 1000, Rational(1, 2), 9, 10),
            _water_jet("A13-02-B", 8, Rational(1, 1000), 1000, Rational(1, 2), 6, 10),
        ),
        (
            "A11-03",
            "calibration",
            _spaceship("A11-03-A", 150, Rational(4, 5)),
            _spaceship("A11-03-B", 125, Rational(3, 5)),
        ),
    )
    return tuple(
        MatchedVariantPair(
            pair_id=f"{problem_id}-pair",
            source_problem_id=problem_id,
            pdf_page=cases[problem_id].pdf_page,
            study_role=role,
            variant_a=variant_a,
            variant_b=variant_b,
            boundary=construct_admission_boundary(
                cases[problem_id].baseline,
                cases[problem_id].proposed,
            ),
            provenance=(
                f"Authored matched variants of A617 PDF page {cases[problem_id].pdf_page}, "
                f"{cases[problem_id].source_scope}; physical structure visually rechecked."
            ),
        )
        for problem_id, role, variant_a, variant_b in specifications
    )


def command_study_audit() -> None:
    pairs = build_matched_variant_pairs()
    calibration = tuple(pair for pair in pairs if pair.study_role == "calibration")
    active = tuple(
        index
        for index in range(len(COST_AXES))
        if any(pair.boundary.delta[index] != 0 for pair in calibration)
    )
    design = Matrix(
        [[pair.boundary.delta[index] for index in active] for pair in calibration]
    )
    print(f"pairs\t{len(pairs)}")
    print(f"variants\t{2 * len(pairs)}")
    print(f"calibration_axes\t{','.join(COST_AXES[index] for index in active)}")
    print(f"calibration_rank\t{design.rank()}")
    print("empirical_rows\t0")
    for schedule in build_two_sequence_schedule(pairs):
        print(f"schedule\t{schedule.sequence_id}")
        for trial in schedule.trials:
            print(
                f"{trial.order}\t{trial.source_problem_id}\t"
                f"{trial.variant_id}\t{trial.route}"
            )
