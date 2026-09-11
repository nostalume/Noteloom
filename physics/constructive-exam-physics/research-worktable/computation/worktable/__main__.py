"""Run one source-bound worktable operation."""

from __future__ import annotations

from argparse import ArgumentParser
from collections.abc import Sequence


COMMANDS = (
    "corpus-audit",
    "polynomial-batch",
    "route-benchmark",
    "route-admission",
    "calibration-probe",
    "study-audit",
    "micro-study-audit",
    "dimensional-transfer",
    "network-condensation",
    "network-ordering",
    "network-human-boundary",
    "network-study-audit",
    "network-admission-audit",
    "event-transfer",
    "impact-transfer",
    "path-transfer",
    "harmonic-transfer",
    "harmonic-product",
    "composition-benchmark",
    "routing-benchmark",
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = ArgumentParser(
        description="Run a constructive exam physics worktable operation."
    )
    parser.add_argument("command", choices=COMMANDS)
    command = parser.parse_args(argv).command

    match command:
        case "corpus-audit":
            from .polynomial_cases import command_corpus_audit

            command_corpus_audit()
        case "polynomial-batch":
            from .polynomial_cases import command_polynomial_batch

            command_polynomial_batch()
        case "route-benchmark":
            from .route_cases import command_route_benchmark

            command_route_benchmark()
        case "route-admission":
            from .route_cases import command_route_admission

            command_route_admission()
        case "calibration-probe":
            from .route_cases import command_calibration_probe

            command_calibration_probe()
        case "study-audit":
            from .study_cases import command_study_audit

            command_study_audit()
        case "micro-study-audit":
            from .micro_study_cases import command_micro_study_audit

            command_micro_study_audit()
        case "dimensional-transfer":
            from .dimensional_cases import command_dimensional_transfer

            command_dimensional_transfer()
        case "network-condensation":
            from .network_cases import command_network_condensation

            command_network_condensation()
        case "network-ordering":
            from .network_order_cases import command_network_ordering

            command_network_ordering()
        case "network-human-boundary":
            from .network_human_cases import command_network_human_boundary

            command_network_human_boundary()
        case "network-study-audit":
            from .network_study_cases import command_network_study_audit

            command_network_study_audit()
        case "network-admission-audit":
            from .network_admission_cases import command_network_admission_audit

            command_network_admission_audit()
        case "event-transfer":
            from .event_cases import command_event_transfer

            command_event_transfer()
        case "impact-transfer":
            from .impact_cases import command_impact_transfer

            command_impact_transfer()
        case "path-transfer":
            from .path_cases import command_path_transfer

            command_path_transfer()
        case "harmonic-transfer":
            from .harmonic_cases import command_harmonic_transfer

            command_harmonic_transfer()
        case "harmonic-product":
            from .harmonic_product_cases import command_harmonic_product

            command_harmonic_product()
        case "composition-benchmark":
            from .composition_cases import command_composition_benchmark

            command_composition_benchmark()
        case "routing-benchmark":
            from .routing_cases import command_routing_benchmark

            command_routing_benchmark()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
