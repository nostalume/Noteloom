"""Sparse-order witnesses for reciprocal network condensation."""

from __future__ import annotations

from sympy import symbols

from occ.network import (
    LinearNetworkRequest,
    NetworkVariable,
)
from occ.network_order import plan_network_elimination


def build_sparse_branch_request(area, state_kind):
    left, right, center, leaf_one, leaf_two = symbols("x_L x_R x_C x_1 x_2")
    return LinearNetworkRequest(
        area=area,
        variables=tuple(
            NetworkVariable(symbol, name, state_kind)
            for symbol, name in (
                (left, "left boundary"),
                (right, "right boundary"),
                (center, "central junction"),
                (leaf_one, "first grounded branch"),
                (leaf_two, "second grounded branch"),
            )
        ),
        boundary_symbols=(left, right),
        internal_symbols=(center, leaf_one, leaf_two),
        response_matrix=(
            (1, 0, -1, 0, 0),
            (0, 1, -1, 0, 0),
            (-1, -1, 4, -1, -1),
            (0, 0, -1, 2, 0),
            (0, 0, -1, 0, 2),
        ),
        source_vector=(0, 0, 0, 0, 0),
        provenance=f"{area} sparse-branch ordering bench",
    )


def command_network_ordering() -> None:
    request = build_sparse_branch_request("electricity", "voltage")
    declared = plan_network_elimination(request, strategy="declared")
    minimum = plan_network_elimination(request, strategy="min_fill")
    elastic = plan_network_elimination(
        build_sparse_branch_request("mechanics", "displacement"), strategy="min_fill"
    )
    plans = (declared, minimum, elastic)

    print("strategy\tarea\torder\tfill_edges\talgebraic_updates\tcertificates")
    for plan in plans:
        order = ",".join(str(symbol) for symbol in plan.elimination_order)
        certificates = (
            "pass" if all(item.passed for item in plan.certificates) else "fail"
        )
        print(
            f"{plan.strategy}\t{plan.area}\t{order}\t{plan.total_fill_edges}"
            f"\t{plan.total_algebraic_updates}\t{certificates}"
        )
    print(
        f"summary\tfill_{declared.total_fill_edges}_to_{minimum.total_fill_edges}"
        f"\tupdates_{declared.total_algebraic_updates}_to_"
        f"{minimum.total_algebraic_updates}\tstructural_savings_only"
    )
