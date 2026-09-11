"""Authored matched variants for the selective micro-tool study."""

from __future__ import annotations

from pathlib import Path

from sympy import I, Rational, simplify, sqrt, sympify

from occ.micro_study import (
    MicroToolPair,
    RouteRecognitionTask,
    build_micro_tool_schedules,
    build_recognition_schedules,
    load_micro_tool_observation_tsv,
    load_route_recognition_observation_tsv,
    validate_disjoint_micro_tool_cohorts,
)
from occ.pilot import (
    audit_route_key,
    construct_micro_pilot_diagnostics,
    evaluate_route_key_preflight,
    load_route_key_review_tsv,
    load_route_key_reviewer_tsv,
    summarize_micro_pilot,
)
from occ.study import StudyVariant


def _jet(variant_id: str, speed, mass_flow, alpha, mass, gravity=10) -> StudyVariant:
    speed, mass_flow, alpha, mass, gravity = map(
        sympify, (speed, mass_flow, alpha, mass, gravity)
    )
    impact_speed = simplify(mass * gravity / ((2 - alpha) * mass_flow))
    height = simplify((speed**2 - impact_speed**2) / (2 * gravity))
    return StudyVariant(
        variant_id,
        (
            f"A vertical jet leaves at {speed} m/s with mass flow {mass_flow} kg/s. "
            f"A fraction {alpha} sticks while the remainder rebounds downward at "
            f"the impact speed. It supports a {mass} kg body. Take g={gravity} "
            "m/s^2. Find the impact speed and stationary height."
        ),
        "steady vertical stream; nonnegative impact speed and height",
        (("impact_speed", impact_speed), ("height", height)),
    )


def _impact(variant_id: str, normal, tangent, restitution, friction) -> StudyVariant:
    normal, tangent, restitution, friction = map(
        sympify, (normal, tangent, restitution, friction)
    )
    capacity = simplify(friction * (1 + restitution) * normal)
    outgoing_tangent = simplify(max(Rational(0), tangent - capacity))
    outgoing_normal = simplify(restitution * normal)
    speed = simplify(sqrt(outgoing_normal**2 + outgoing_tangent**2))
    angle_tangent = simplify(outgoing_tangent / outgoing_normal)
    return StudyVariant(
        variant_id,
        (
            "A nonrotating point particle strikes a rough fixed wall with normal "
            f"speed {normal} m/s and tangential speed {tangent} m/s. Restitution is "
            f"{restitution} and friction is {friction}. Find the impact regime, "
            "outgoing components, speed, and tangent of the angle from the normal."
        ),
        "fixed wall; nonrotating point particle; maximum-dissipation impact",
        (
            ("outgoing_normal", outgoing_normal),
            ("outgoing_tangent", outgoing_tangent),
            ("speed", speed),
            ("angle_tangent", angle_tangent),
        ),
    )


def _path(variant_id: str, curl_scale, width, height) -> StudyVariant:
    curl_scale, width, height = map(sympify, (curl_scale, width, height))
    broken_work = simplify(curl_scale * width * height / 2)
    return StudyVariant(
        variant_id,
        (
            f"For k={curl_scale} and E=(-k y/2,k x/2), compare oriented work "
            f"from (0,0) to ({width},{height}) along the straight segment and "
            "along the positive-x then positive-y broken path."
        ),
        "exact planar field; common oriented endpoints",
        (("straight_work", Rational(0)), ("broken_work", broken_work)),
    )


def _product(variant_id: str, amplitude_a, amplitude_b, phase_cos, phase_sin):
    amplitude_a, amplitude_b, phase_cos, phase_sin = map(
        sympify, (amplitude_a, amplitude_b, phase_cos, phase_sin)
    )
    scale = simplify(amplitude_a * amplitude_b / 2)
    mean = simplify(scale * phase_cos)
    ripple = simplify(scale * (phase_cos + I * phase_sin))
    return StudyVariant(
        variant_id,
        (
            f"Let x(t)={amplitude_a} cos(omega t) and y(t)={amplitude_b}["
            f"{phase_cos} cos(omega t)-{phase_sin} sin(omega t)]. Find the mean "
            "of xy and its complete 2 omega phasor."
        ),
        "two real same-frequency signals; positive omega",
        (
            ("mean", mean),
            ("ripple_real", simplify(ripple.as_real_imag()[0])),
            ("ripple_imag", simplify(ripple.as_real_imag()[1])),
        ),
    )


def build_micro_tool_pairs() -> tuple[MicroToolPair, ...]:
    """Build four direct/operator pairs in each independent study phase."""

    specifications = (
        (
            "assisted",
            "jet",
            "card-1",
            "slice",
            _jet("D3-A-J1", 10, 10, Rational(1, 2), 9),
            _jet("D3-A-J2", 8, 8, Rational(1, 2), 6),
        ),
        (
            "assisted",
            "impact",
            "card-3",
            "projection",
            _impact("D3-A-I1", 4, 2, Rational(1, 2), Rational(1, 2)),
            _impact("D3-A-I2", 5, 2, Rational(1, 5), Rational(1, 2)),
        ),
        (
            "assisted",
            "path",
            "card-4",
            "path",
            _path("D3-A-P1", 1, 1, 1),
            _path("D3-A-P2", 2, 2, 1),
        ),
        (
            "assisted",
            "product",
            "card-6",
            "product",
            _product("D3-A-H1", 2, 5, Rational(3, 5), Rational(4, 5)),
            _product("D3-A-H2", 3, 10, Rational(4, 5), Rational(3, 5)),
        ),
        (
            "internalized",
            "jet",
            "card-1",
            "slice",
            _jet("D3-I-J1", 12, 12, Rational(1, 2), 9),
            _jet("D3-I-J2", 10, 10, 0, 8),
        ),
        (
            "internalized",
            "impact",
            "card-3",
            "projection",
            _impact("D3-I-I1", 6, 3, Rational(1, 2), Rational(1, 3)),
            _impact("D3-I-I2", 3, 1, 1, Rational(1, 4)),
        ),
        (
            "internalized",
            "path",
            "card-4",
            "path",
            _path("D3-I-P1", 3, 2, 2),
            _path("D3-I-P2", Rational(1, 2), 4, 3),
        ),
        (
            "internalized",
            "product",
            "card-6",
            "product",
            _product("D3-I-H1", 4, 5, Rational(5, 13), Rational(12, 13)),
            _product("D3-I-H2", 6, 5, Rational(12, 13), Rational(5, 13)),
        ),
        (
            "delayed_unseen",
            "jet",
            "card-1",
            "slice",
            _jet("D3-D-J1", 12, 15, 1, 9),
            _jet("D3-D-J2", 10, 12, Rational(1, 2), 9),
        ),
        (
            "delayed_unseen",
            "impact",
            "card-3",
            "projection",
            _impact("D3-D-I1", 8, 2, Rational(1, 4), Rational(1, 4)),
            _impact("D3-D-I2", 5, 1, Rational(3, 5), Rational(1, 4)),
        ),
        (
            "delayed_unseen",
            "path",
            "card-4",
            "path",
            _path("D3-D-P1", Rational(3, 2), 2, 4),
            _path("D3-D-P2", 4, Rational(3, 2), 2),
        ),
        (
            "delayed_unseen",
            "product",
            "card-6",
            "product",
            _product("D3-D-H1", 5, 2, -Rational(3, 5), Rational(4, 5)),
            _product("D3-D-H2", 8, 5, Rational(7, 25), Rational(24, 25)),
        ),
    )
    return tuple(
        MicroToolPair(
            pair_id=f"{phase}-{family}",
            family_id=family,
            phase=phase,
            card_id=card_id,
            operator_route=route,
            variant_a=variant_a,
            variant_b=variant_b,
            provenance=(
                "Authored D3 micro-tool matched variant; derived from "
                f"review/{card_id}; phase={phase}; family={family}."
            ),
        )
        for phase, family, card_id, route, variant_a, variant_b in specifications
    )


def build_route_recognition_tasks() -> tuple[RouteRecognitionTask, ...]:
    """Build the no-solving route set, including direct and refusal decoys."""

    specifications = (
        (
            "R01",
            "A mass is dropped through a known height; find its pre-impact speed.",
            "direct",
        ),
        (
            "R02",
            "A circuit subpart asks only for heat in one known resistor and interval.",
            "slice",
        ),
        (
            "R03",
            "Find the first instant when a pendulum string tension vanishes.",
            "event",
        ),
        (
            "R04",
            "Saturated wall friction would reverse a point particle's tangent speed.",
            "projection",
        ),
        (
            "R05",
            "Compare open-wire voltages on two paths through changing magnetic flux.",
            "path",
        ),
        (
            "R06",
            "A steady series RLC problem asks for magnitude, lead/lag, and real signal.",
            "harmonic",
        ),
        (
            "R07",
            "A rotating coil asks only for cycle-averaged torque from two phasors.",
            "product",
        ),
        (
            "R08",
            "A spinning sphere hits a rough wall; only a point-particle card is offered.",
            "refuse-card",
        ),
        (
            "R09",
            "Find a switched oscillator's full transient using only a steady phasor law.",
            "refuse-card",
        ),
        (
            "R10",
            "A verified electrostatic potential is given; find endpoint voltage.",
            "direct",
        ),
        (
            "R11",
            "A symmetric linkage has twelve components but two admissible coordinates.",
            "symmetry",
        ),
        (
            "R12",
            "Jet-supported height and momentum flux share one hidden impact speed.",
            "slice",
        ),
    )
    return tuple(
        RouteRecognitionTask(
            task_id,
            prompt,
            route,
            f"Authored D3 recognition task; review/mixed-drills Part A item {index}.",
        )
        for index, (task_id, prompt, route) in enumerate(specifications, start=1)
    )


def command_micro_study_audit() -> None:
    pairs = build_micro_tool_pairs()
    recognition_tasks = build_route_recognition_tasks()
    recognition_schedules = build_recognition_schedules(recognition_tasks)
    observations = Path(__file__).parents[2] / "observations"
    execution_rows = load_micro_tool_observation_tsv(
        observations / "d3-micro-tool-observation-template.tsv",
        pairs,
        build_micro_tool_schedules(pairs),
    )
    recognition_rows = load_route_recognition_observation_tsv(
        observations / "d3-route-recognition-observation-template.tsv",
        recognition_tasks,
        recognition_schedules,
    )
    route_key_reviews = load_route_key_review_tsv(
        observations / "d4-route-key-review-template.tsv", recognition_tasks
    )
    route_key_reviewers = load_route_key_reviewer_tsv(
        observations / "d4-route-key-reviewer-template.tsv", recognition_schedules
    )
    route_key_audits = audit_route_key(
        recognition_tasks, route_key_reviews, route_key_reviewers
    )
    route_key_preflight = evaluate_route_key_preflight(
        recognition_tasks, route_key_audits
    )
    validate_disjoint_micro_tool_cohorts(recognition_rows, execution_rows)
    summary = summarize_micro_pilot(
        recognition_tasks,
        route_key_audits,
        recognition_rows,
        execution_rows,
        pairs,
    )
    diagnostics = construct_micro_pilot_diagnostics(execution_rows, pairs)
    print("contract\tC-human-v2")
    print("key_contract\tC-key-v1")
    print("key_policy\tK-key-v1")
    print("pilot_analysis_contract\tC-pilot-time-v1")
    print(f"recognition_tasks\t{len(recognition_tasks)}")
    for schedule in recognition_schedules:
        print(
            f"recognition_schedule\t{schedule.sequence_id}\ttasks={len(schedule.task_ids)}"
        )
    print(f"route_key_reviews\t{len(route_key_reviews)}")
    print(f"route_key_reviewers\t{len(route_key_reviewers)}")
    print(
        "route_key_status\t"
        f"unreviewed={sum(audit.status == 'unreviewed' for audit in route_key_audits)}"
    )
    print(f"route_key_preflight\t{route_key_preflight.status}")
    print(f"pairs\t{len(pairs)}")
    print(f"variants\t{2 * len(pairs)}")
    for schedule in build_micro_tool_schedules(pairs):
        print(f"schedule\t{schedule.sequence_id}\ttrials={len(schedule.trials)}")
        for phase in ("assisted", "internalized", "delayed_unseen"):
            count = sum(trial.phase == phase for trial in schedule.trials)
            print(f"phase\t{phase}\ttrials={count}")
    print(f"recognition_rows\t{len(recognition_rows)}")
    print(f"execution_rows\t{len(execution_rows)}")
    print(f"empirical_rows\t{len(recognition_rows) + len(execution_rows)}")
    print(f"pilot_status\t{summary.status}")
    print(f"pilot_design_inputs\t{diagnostics.status}")
    for phase in diagnostics.phases:
        variance = (
            "observed"
            if phase.sample_variance_cluster_time_delta is not None
            else "unobserved"
        )
        print(
            f"pilot_phase\t{phase.phase}"
            f"\tparticipants={phase.participant_count}"
            f"\tcomplete_clusters={phase.complete_timing_clusters}"
            f"\tvariance={variance}"
        )
    print(f"speed_disposition\t{summary.speed_disposition}")
    print("verdict\thuman_benefit_unobserved")
