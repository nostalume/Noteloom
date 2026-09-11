"""Frozen route-admission tasks for the network recognition instrument."""

from __future__ import annotations

from pathlib import Path

from sympy import symbols

from occ.network import (
    LinearNetworkRequest,
    NetworkVariable,
)
from occ.network_admission import (
    NetworkAdmissionTask,
    build_network_admission_schedules,
    construct_network_admission_key,
)
from occ.network_admission_analysis import (
    audit_network_admission_key,
    construct_network_admission_diagnostics,
)
from occ.network_admission_io import (
    load_network_admission_observation_tsv,
    load_network_admission_review_tsv,
)

from .network_study_cases import build_network_study_pairs


def _request(task_id, matrix, *, state_kind="voltage", area="electricity"):
    size = len(matrix)
    names = ("left terminal", "right terminal", "junction", "second junction")[:size]
    states = symbols(
        " ".join(f"a_{task_id.replace('-', '_')}_{index}" for index in range(size))
    )
    return LinearNetworkRequest(
        area=area,
        variables=tuple(
            NetworkVariable(symbol, name, state_kind)
            for symbol, name in zip(states, names, strict=True)
        ),
        boundary_symbols=tuple(states[:2]),
        internal_symbols=tuple(states[2:]),
        response_matrix=matrix,
        source_vector=(0,) * size,
        provenance=f"{task_id} authored adaptive-admission fixture",
    )


def _single_hidden(task_id, link):
    return _request(
        task_id,
        (
            (link, 0, -link),
            (0, link, -link),
            (-link, -link, 2 * link),
        ),
    )


def _nonreciprocal(task_id, scale):
    return _request(
        task_id,
        (
            (scale, 0, -scale),
            (0, scale, -2 * scale),
            (-3 * scale, -scale, 4 * scale),
        ),
        state_kind="response potential",
        area="nonreciprocal linear response",
    )


def _task(task_id, phase, topology, prompt, request):
    return NetworkAdmissionTask(
        task_id,
        phase,
        topology,
        prompt,
        request,
        "C-network-human-v1; authored adaptive-admission task; not learner evidence",
    )


def build_network_admission_tasks() -> tuple[NetworkAdmissionTask, ...]:
    """Return balanced direct-gate, conditional, and refusal tasks in three phases."""

    execution_pairs = build_network_study_pairs()
    immediate_candidate = execution_pairs[0].variant_a
    delayed_candidate = execution_pairs[2].variant_a
    unseen_candidate = execution_pairs[4].variant_a
    two_path = _request(
        "N2-U-G",
        (
            (1, 0, -1, 0),
            (0, 1, 0, -1),
            (-1, 0, 2, -1),
            (0, -1, -1, 2),
        ),
    )
    zero_pivot = LinearNetworkRequest(
        area="reciprocal coupled-mode response",
        variables=tuple(
            NetworkVariable(symbol, name, "mode amplitude")
            for symbol, name in zip(
                symbols("a_N2_U_R_B a_N2_U_R_1 a_N2_U_R_2"),
                ("boundary mode", "first hidden mode", "second hidden mode"),
                strict=True,
            )
        ),
        boundary_symbols=(symbols("a_N2_U_R_B"),),
        internal_symbols=symbols("a_N2_U_R_1 a_N2_U_R_2"),
        response_matrix=((1, 0, 0), (0, 0, 1), (0, 1, 0)),
        source_vector=(0, 0, 0),
        provenance="N2-U-R authored zero-scalar-pivot fixture",
    )
    return (
        _task(
            "N2-I-C",
            "immediate_unassisted",
            "two_leaf_star",
            immediate_candidate.prompt,
            immediate_candidate.request,
        ),
        _task(
            "N2-I-G",
            "immediate_unassisted",
            "single_hidden_chain",
            "A reciprocal two-terminal network has one hidden junction joined equally to L and R. Decide the warranted route status before solving its terminal response.",
            _single_hidden("N2-I-G", 1),
        ),
        _task(
            "N2-I-R",
            "immediate_unassisted",
            "nonreciprocal_junction",
            "A directed linear-response network has K=[[1,0,-1],[0,1,-2],[-3,-1,4]]. Decide whether the reciprocal scalar strip is admitted before solving.",
            _nonreciprocal("N2-I-R", 1),
        ),
        _task(
            "N2-D-C",
            "delayed_same_topology",
            "two_leaf_star",
            delayed_candidate.prompt,
            delayed_candidate.request,
        ),
        _task(
            "N2-D-G",
            "delayed_same_topology",
            "single_hidden_chain",
            "A reciprocal two-terminal network has one hidden junction and both link conductances are 3. Decide the warranted route status before solving its terminal response.",
            _single_hidden("N2-D-G", 3),
        ),
        _task(
            "N2-D-R",
            "delayed_same_topology",
            "nonreciprocal_junction",
            "A directed linear-response network has K=2[[1,0,-1],[0,1,-2],[-3,-1,4]]. Decide whether the reciprocal scalar strip is admitted before solving.",
            _nonreciprocal("N2-D-R", 2),
        ),
        _task(
            "N2-U-C",
            "unseen_topology",
            "split_hub",
            unseen_candidate.prompt,
            unseen_candidate.request,
        ),
        _task(
            "N2-U-G",
            "unseen_topology",
            "two_hidden_path",
            "A reciprocal path L-A-B-R has unit conductance on every link and no other link. Decide the warranted route status before solving the terminal response.",
            two_path,
        ),
        _task(
            "N2-U-R",
            "unseen_topology",
            "zero_scalar_pivot",
            "A reciprocal coupled-mode packet has one boundary and hidden block [[0,1],[1,0]]. Decide whether scalar elimination is admitted before solving.",
            zero_pivot,
        ),
    )


def command_network_admission_audit() -> None:
    tasks = build_network_admission_tasks()
    schedules = build_network_admission_schedules(tasks)
    root = Path(__file__).parents[2]
    observations = load_network_admission_observation_tsv(
        root / "observations" / "n2-network-admission-template.tsv",
        tasks,
        schedules,
    )
    reviews = load_network_admission_review_tsv(
        root / "observations" / "n2-network-admission-review-template.tsv",
        tasks,
    )
    keys = tuple(construct_network_admission_key(task) for task in tasks)
    diagnostics = construct_network_admission_diagnostics(observations, tasks)
    audit = audit_network_admission_key(reviews, tasks)

    print("contract\tC-network-admission-v1")
    print(f"tasks\t{len(tasks)}\tsequences\t{len(schedules)}")
    counts = {
        decision: sum(key.expected_decision == decision for key in keys)
        for decision in ("direct_gate", "conditional_candidate", "refuse")
    }
    print(
        f"decisions\tdirect_gate:{counts['direct_gate']}"
        f"\tconditional_candidate:{counts['conditional_candidate']}"
        f"\trefuse:{counts['refuse']}"
    )
    print(f"key_preflight\t{audit.status}\tlearner_data\t{diagnostics.status}")
    print(
        f"recognition\t{diagnostics.recognition_disposition}"
        f"\tretention\t{diagnostics.retention_disposition}"
        f"\ttransfer\t{diagnostics.transfer_disposition}"
    )
    print("verdict\texpert_review_and_disjoint_recognition_cohort_required")
