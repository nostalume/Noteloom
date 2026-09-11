"""Frozen matched variants for the network acquisition instrument."""

from __future__ import annotations

from pathlib import Path

from sympy import symbols

from occ.network import (
    LinearNetworkRequest,
    NetworkVariable,
)
from occ.network_study import (
    NetworkStudyPair,
    NetworkStudyVariant,
    build_network_study_schedules,
    solve_network_study_variant,
)
from occ.network_study_analysis import (
    audit_network_study_key,
    construct_network_study_diagnostics,
)
from occ.network_study_io import (
    load_network_study_observation_tsv,
    load_network_study_review_tsv,
)


def _variant(
    variant_id,
    topology_family,
    node_names,
    edges,
    grounds,
    boundary_values,
):
    states = symbols(
        " ".join(f"v_{variant_id.replace('-', '_')}_{name}" for name in node_names)
    )
    matrix = [[0 for _ in states] for _ in states]
    edge_text = []
    for first, second, conductance in edges:
        i, j = node_names.index(first), node_names.index(second)
        matrix[i][i] += conductance
        matrix[j][j] += conductance
        matrix[i][j] -= conductance
        matrix[j][i] -= conductance
        edge_text.append(f"{first}-{second}:{conductance}")
    for node, conductance in grounds:
        matrix[node_names.index(node)][node_names.index(node)] += conductance
        edge_text.append(f"{node}-ground:{conductance}")
    prompt = (
        "A reciprocal conductance network has links "
        + ", ".join(edge_text)
        + f". Fix L={boundary_values[0]} V and R={boundary_values[1]} V. "
        "Find the current injected at L; include one boundary-law check."
    )
    request = LinearNetworkRequest(
        area="electricity",
        variables=tuple(
            NetworkVariable(symbol, f"node {name}", "voltage")
            for symbol, name in zip(states, node_names, strict=True)
        ),
        boundary_symbols=(states[0], states[1]),
        internal_symbols=tuple(states[2:]),
        response_matrix=tuple(tuple(row) for row in matrix),
        source_vector=(0,) * len(states),
        provenance=f"N1 authored {topology_family} exact-network fixture",
    )
    return NetworkStudyVariant(
        variant_id,
        topology_family,
        prompt,
        request,
        boundary_values,
        "C-network-v1/C-order-v1/C-network-human-v1; authored acquisition variant",
    )


def _star(variant_id, topology, leaves, link, ground, boundary_values):
    leaf_names = ("A", "B", "D")[:leaves]
    nodes = ("L", "R", "C", *leaf_names)
    edges = (
        ("L", "C", link),
        ("R", "C", link),
        *(("C", leaf, link) for leaf in leaf_names),
    )
    grounds = tuple((leaf, ground) for leaf in leaf_names)
    return _variant(variant_id, topology, nodes, edges, grounds, boundary_values)


def build_network_study_pairs() -> tuple[NetworkStudyPair, ...]:
    """Return two trained, two delayed, and two unseen matched pairs."""

    common = "authored network acquisition bench; not learner evidence"
    return (
        NetworkStudyPair(
            "N1-I-two-leaf",
            "immediate_assisted",
            "two_leaf_star",
            _star("N1-I2-A", "two_leaf_star", 2, 1, 1, (1, 0)),
            _star("N1-I2-B", "two_leaf_star", 2, 2, 1, (1, 0)),
            common,
        ),
        NetworkStudyPair(
            "N1-I-three-leaf",
            "immediate_assisted",
            "three_leaf_star",
            _star("N1-I3-A", "three_leaf_star", 3, 1, 1, (1, 0)),
            _star("N1-I3-B", "three_leaf_star", 3, 2, 1, (1, 0)),
            common,
        ),
        NetworkStudyPair(
            "N1-D-two-leaf",
            "delayed_same_topology",
            "two_leaf_star",
            _star("N1-D2-A", "two_leaf_star", 2, 1, 2, (2, 0)),
            _star("N1-D2-B", "two_leaf_star", 2, 3, 1, (1, -1)),
            common,
        ),
        NetworkStudyPair(
            "N1-D-three-leaf",
            "delayed_same_topology",
            "three_leaf_star",
            _star("N1-D3-A", "three_leaf_star", 3, 1, 2, (2, 0)),
            _star("N1-D3-B", "three_leaf_star", 3, 2, 3, (1, -1)),
            common,
        ),
        NetworkStudyPair(
            "N1-U-split-hub",
            "unseen_topology",
            "split_hub",
            _variant(
                "N1-US-A",
                "split_hub",
                ("L", "R", "C", "D", "A", "B"),
                (
                    ("L", "C", 1),
                    ("C", "D", 1),
                    ("D", "R", 1),
                    ("C", "A", 1),
                    ("D", "B", 1),
                ),
                (("A", 1), ("B", 1)),
                (1, 0),
            ),
            _variant(
                "N1-US-B",
                "split_hub",
                ("L", "R", "C", "D", "A", "B"),
                (
                    ("L", "C", 2),
                    ("C", "D", 1),
                    ("D", "R", 2),
                    ("C", "A", 1),
                    ("D", "B", 1),
                ),
                (("A", 2), ("B", 2)),
                (1, -1),
            ),
            common,
        ),
        NetworkStudyPair(
            "N1-U-branch-chain",
            "unseen_topology",
            "branch_chain",
            _variant(
                "N1-UC-A",
                "branch_chain",
                ("L", "R", "C", "A", "B", "D"),
                (
                    ("L", "C", 1),
                    ("R", "C", 1),
                    ("C", "A", 1),
                    ("A", "B", 1),
                    ("C", "D", 1),
                ),
                (("B", 1), ("D", 1)),
                (1, 0),
            ),
            _variant(
                "N1-UC-B",
                "branch_chain",
                ("L", "R", "C", "A", "B", "D"),
                (
                    ("L", "C", 2),
                    ("R", "C", 2),
                    ("C", "A", 1),
                    ("A", "B", 2),
                    ("C", "D", 1),
                ),
                (("B", 1), ("D", 2)),
                (2, 0),
            ),
            common,
        ),
    )


def command_network_study_audit() -> None:
    pairs = build_network_study_pairs()
    schedules = build_network_study_schedules(pairs)
    root = Path(__file__).parents[2]
    observations = load_network_study_observation_tsv(
        root / "observations" / "n1-network-study-template.tsv", pairs, schedules
    )
    reviews = load_network_study_review_tsv(
        root / "observations" / "n1-network-key-review-template.tsv", pairs
    )
    answers = tuple(
        solve_network_study_variant(variant)
        for pair in pairs
        for variant in (pair.variant_a, pair.variant_b)
    )
    diagnostics = construct_network_study_diagnostics(observations, pairs)
    key_audit = audit_network_study_key(reviews, pairs)

    print("contract\tC-network-study-v1")
    print(f"pairs\t{len(pairs)}\tvariants\t{len(answers)}\tsequences\t{len(schedules)}")
    print(
        "phases\t"
        + ",".join(
            f"{phase}:2_pairs"
            for phase in (
                "immediate_assisted",
                "delayed_same_topology",
                "unseen_topology",
            )
        )
    )
    print(
        f"exact_keys\t{sum(item.status == 'constructed' for item in answers)}"
        f"\tkey_preflight\t{key_audit.status}"
    )
    print(
        f"learner_data\t{diagnostics.status}\tspeed\t{diagnostics.speed_disposition}"
        f"\tretention\t{diagnostics.retention_disposition}"
        f"\ttransfer\t{diagnostics.transfer_disposition}"
    )
    print("verdict\texpert_review_and_learner_execution_required")
