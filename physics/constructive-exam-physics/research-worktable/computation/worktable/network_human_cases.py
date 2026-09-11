"""Deductive speed-boundary witnesses for sparse network routes."""

from __future__ import annotations

from sympy import symbols

from occ.network import (
    LinearNetworkRequest,
    NetworkVariable,
)
from occ.network_human import construct_network_human_boundary

from .network_order_cases import build_sparse_branch_request


def _single_hidden_request():
    left, right, hidden = symbols("y_L y_R y_h")
    return LinearNetworkRequest(
        area="electricity",
        variables=(
            NetworkVariable(left, "left terminal", "voltage"),
            NetworkVariable(right, "right terminal", "voltage"),
            NetworkVariable(hidden, "junction", "voltage"),
        ),
        boundary_symbols=(left, right),
        internal_symbols=(hidden,),
        response_matrix=((1, 0, -1), (0, 1, -1), (-1, -1, 2)),
        source_vector=(0, 0, 0),
        provenance="single-hidden direct-gate bench",
    )


def command_network_human_boundary() -> None:
    cases = (
        (
            "branched",
            construct_network_human_boundary(
                build_sparse_branch_request("electricity", "voltage"),
                problem_id="N-H1",
                target="terminal response",
            ),
        ),
        (
            "single-hidden",
            construct_network_human_boundary(
                _single_hidden_request(),
                problem_id="N-H2",
                target="terminal response",
            ),
        ),
    )

    print("case\tclassification\tdelta\tcheaper_when\tspeed\tlearnability")
    classifications = []
    for name, result in cases:
        boundary = result.admission_boundary
        classifications.append(boundary.classification)
        delta = ",".join(str(value) for value in boundary.delta)
        print(
            f"{name}\t{boundary.classification}\t{delta}"
            f"\t{boundary.proposed_cheaper_when}\t{result.speed_disposition}"
            f"\t{result.learnability_disposition}"
        )
    print(
        f"summary\t{classifications.count('conditional')}_conditional"
        f"\t{classifications.count('always_direct')}_always_direct"
        "\t0_human_observations"
    )
