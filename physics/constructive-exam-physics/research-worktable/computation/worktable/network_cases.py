"""Cross-area witnesses for exact boundary-network condensation."""

from __future__ import annotations

from sympy import symbols

from occ.network import (
    LinearNetworkRequest,
    NetworkVariable,
    condense_linear_network,
)


def _variable(symbol, name, state_kind):
    return NetworkVariable(symbol, name, state_kind)


def _chain(problem, area, state_kind, internal_source=0):
    left, right, hidden = symbols(f"{problem}_L {problem}_R {problem}_h")
    first, second = symbols(f"{problem}_1 {problem}_2", positive=True)
    return LinearNetworkRequest(
        area=area,
        variables=(
            _variable(left, "left boundary state", state_kind),
            _variable(right, "right boundary state", state_kind),
            _variable(hidden, "hidden junction state", state_kind),
        ),
        boundary_symbols=(left, right),
        internal_symbols=(hidden,),
        response_matrix=(
            (first, 0, -first),
            (0, second, -second),
            (-first, -second, first + second),
        ),
        source_vector=(0, 0, internal_source),
        provenance=f"{area} cross-area condensation bench",
    )


def _singular_request():
    boundary, hidden = symbols("singular_B singular_h")
    return LinearNetworkRequest(
        area="mechanics",
        variables=(
            _variable(boundary, "boundary displacement", "displacement"),
            _variable(hidden, "free hidden displacement", "displacement"),
        ),
        boundary_symbols=(boundary,),
        internal_symbols=(hidden,),
        response_matrix=((1, 0), (0, 0)),
        source_vector=(0, 0),
        provenance="singular free-mode bench",
    )


def _undetermined_request():
    boundary, hidden, coefficient = symbols("symbolic_B symbolic_h symbolic_c")
    return LinearNetworkRequest(
        area="generic linear response",
        variables=(
            _variable(boundary, "boundary state", "potential"),
            _variable(hidden, "hidden state", "potential"),
        ),
        boundary_symbols=(boundary,),
        internal_symbols=(hidden,),
        response_matrix=((1, 0), (0, coefficient)),
        source_vector=(0, 0),
        provenance="undetermined symbolic block bench",
    )


def command_network_condensation() -> None:
    heat = symbols("Q")
    cases = (
        ("resistor-chain", _chain("g", "electricity", "voltage")),
        ("spring-chain", _chain("k", "mechanics", "displacement")),
        ("thermal-chain", _chain("h", "thermal physics", "temperature", heat)),
        ("free-mode", _singular_request()),
        ("unknown-block", _undetermined_request()),
    )

    print("problem\tarea\tstatus\tboundary\tinternal\tresponse\treconstruction")
    constructed = 0
    refused = 0
    all_certified = True
    for problem, request in cases:
        result = condense_linear_network(request)
        response = str(result.condensed_matrix) if result.condensed_matrix else "-"
        reconstruction = (
            str(result.reconstruction_matrix) if result.reconstruction_matrix else "-"
        )
        print(
            f"{problem}\t{result.area}\t{result.status}"
            f"\t{len(result.boundary_symbols)}\t{len(result.internal_symbols)}"
            f"\t{response}\t{reconstruction}"
        )
        constructed += result.status == "constructed"
        refused += result.status == "refused"
        if result.status == "constructed":
            all_certified &= all(item.passed for item in result.certificates)
    certificate_status = (
        "all_constructed_cases_certified" if all_certified else "certificate_failed"
    )
    print(
        f"summary\t{constructed}_cross_area_condensations\t{refused}_refusals"
        f"\t{certificate_status}"
    )
