"""Same-observable comparison of exact and sampled local projector routes."""

from __future__ import annotations

import math
import platform
import sys
from dataclasses import dataclass
from importlib.metadata import version
from statistics import median
from time import perf_counter

from coefficient_projector_jet import CoefficientJet, ProjectorJetBudget, construct_projector_jet
from finite_window_propagation import FinitePropagationWindow
from projector_native_propagation import construct_projector_window_propagation
from sampled_projector_baseline import SampledProjectorError, construct_sampled_route
from simple_block_pde import IrreducibleModel


class RouteComparisonError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class CoefficientRouteProblem:
    model: IrreducibleModel
    coefficient_jet: CoefficientJet
    projector_budget: ProjectorJetBudget
    window: FinitePropagationWindow


@dataclass(frozen=True)
class ComparisonBudget:
    maximum_carrier_dimension: int
    finite_difference_step: float
    cluster_tolerance: float
    observable_tolerance: float
    timing_repetitions: int


@dataclass(frozen=True)
class RouteContract:
    input_domain: str
    observable: str
    recovery: str
    observable_tolerance: float


@dataclass(frozen=True)
class SemanticCost:
    transformations: tuple[str, ...]
    independent_objects: int
    numerical_policy_choices: int
    theorem_contracts: int

    @property
    def transformation_count(self) -> int:
        return len(self.transformations)


@dataclass(frozen=True)
class RouteWork:
    coefficient_samples: int
    exact_factor_candidate_checks: int
    exact_sylvester_blocks: int
    numerical_eigendecompositions: int
    analysis_coordinate_solves: int
    coupling_matrix_entries: int
    matrix_exponentials: int
    propagated_blocks: int
    block_dimension: int


@dataclass(frozen=True)
class RouteObservation:
    route: str
    probability: float
    runtime_samples_seconds: tuple[float, ...]
    median_runtime_seconds: float
    work: RouteWork
    semantic: SemanticCost


@dataclass(frozen=True)
class TimingContext:
    python_version: str
    numpy_version: str
    scipy_version: str
    platform: str
    timer: str
    repetitions: int


@dataclass(frozen=True)
class CompleteRouteComparison:
    contract: RouteContract
    exact: RouteObservation
    sampled: RouteObservation
    timing_context: TimingContext
    observable_error: float
    runtime_ratio_exact_over_sampled: float
    runtime_observation: str
    proxy_disposition: str
    human_disposition: str
    shared_stages: tuple[str, ...]
    unpaid_stages: tuple[str, ...]
    checks: dict[str, bool]


@dataclass(frozen=True)
class _UntimedObservation:
    probability: float
    work: RouteWork
    semantic: SemanticCost


def _admit(problem: CoefficientRouteProblem, budget: ComparisonBudget) -> int:
    dimension = len(problem.model.selected_projector)
    finite_values = (
        budget.finite_difference_step,
        budget.cluster_tolerance,
        budget.observable_tolerance,
    )
    if (
        budget.maximum_carrier_dimension <= 0
        or budget.timing_repetitions <= 0
        or any(not math.isfinite(value) or value <= 0 for value in finite_values)
    ):
        raise RouteComparisonError(
            "InvalidComparisonBudget", "comparison bounds and repetitions must be positive"
        )
    if dimension > budget.maximum_carrier_dimension:
        raise RouteComparisonError(
            "ComparisonBudgetExceeded", "carrier dimension exceeds the comparison budget"
        )
    if not problem.window.momenta:
        raise RouteComparisonError("EmptyComparisonWindow", "comparison window must be nonempty")
    return dimension


def _exact_route(problem: CoefficientRouteProblem) -> _UntimedObservation:
    projector = construct_projector_jet(problem.coefficient_jet, problem.projector_budget)
    propagation = construct_projector_window_propagation(problem.model, projector, problem.window)
    work = RouteWork(
        coefficient_samples=0,
        exact_factor_candidate_checks=projector.cost.factor_candidate_checks,
        exact_sylvester_blocks=2 * projector.cost.complement_sylvester_blocks,
        numerical_eigendecompositions=0,
        analysis_coordinate_solves=propagation.cost.analysis_coordinate_solves,
        coupling_matrix_entries=propagation.cost.coupling_matrix_entries,
        matrix_exponentials=propagation.cost.propagated_blocks,
        propagated_blocks=propagation.cost.propagated_blocks,
        block_dimension=propagation.cost.propagated_block_dimension,
    )
    semantic = SemanticCost(
        transformations=(
            "split exact coefficient algebra",
            "solve first and second projector Sylvester laws",
            "admit invariant off-block differential jet",
            "assemble finite carrier Hamiltonians",
            "propagate finite blocks",
            "recover and certify complement probability",
        ),
        independent_objects=4,
        numerical_policy_choices=0,
        theorem_contracts=2,
    )
    return _UntimedObservation(propagation.full_transition_probability, work, semantic)


def _sampled_route(
    problem: CoefficientRouteProblem, budget: ComparisonBudget
) -> _UntimedObservation:
    try:
        witness = construct_sampled_route(
            problem.model,
            problem.coefficient_jet,
            problem.window,
            budget.finite_difference_step,
            budget.cluster_tolerance,
        )
    except SampledProjectorError as error:
        raise RouteComparisonError(error.kind, str(error)) from error
    if witness.projector_residual > 1e-10 or witness.maximum_unitarity_residual > 1e-10:
        raise RouteComparisonError(
            "SampledNumericalResidual", "sampled projector or propagator residual is too large"
        )
    count = len(problem.window.momenta)
    dimension = len(problem.model.selected_projector)
    work = RouteWork(
        coefficient_samples=3,
        exact_factor_candidate_checks=0,
        exact_sylvester_blocks=0,
        numerical_eigendecompositions=3,
        analysis_coordinate_solves=0,
        coupling_matrix_entries=count * dimension * dimension,
        matrix_exponentials=count,
        propagated_blocks=count,
        block_dimension=dimension,
    )
    semantic = SemanticCost(
        transformations=(
            "choose sampling and cluster policies",
            "sample the quadratic coefficient jet three times",
            "diagonalize and select three spectral clusters",
            "finite-difference first and second projectors",
            "extract off-block differential arrows",
            "assemble finite carrier Hamiltonians",
            "propagate finite blocks",
            "recover and compare complement probability",
        ),
        independent_objects=6,
        numerical_policy_choices=2,
        theorem_contracts=1,
    )
    return _UntimedObservation(witness.probability, work, semantic)


def compare_complete_routes(
    problem: CoefficientRouteProblem, budget: ComparisonBudget
) -> CompleteRouteComparison:
    dimension = _admit(problem, budget)
    exact = _exact_route(problem)
    sampled = _sampled_route(problem, budget)
    error = abs(exact.probability - sampled.probability)
    if error > budget.observable_tolerance:
        raise RouteComparisonError(
            "ObservableAccuracyUnmet",
            f"route observable error {error} exceeds {budget.observable_tolerance}",
        )
    exact_times = []
    sampled_times = []
    for index in range(budget.timing_repetitions):
        order = ("exact", "sampled") if index % 2 == 0 else ("sampled", "exact")
        for route in order:
            started = perf_counter()
            (_exact_route(problem) if route == "exact" else _sampled_route(problem, budget))
            (exact_times if route == "exact" else sampled_times).append(perf_counter() - started)
    exact_times = tuple(exact_times)
    sampled_times = tuple(sampled_times)
    exact_median = median(exact_times)
    sampled_median = median(sampled_times)
    lower_exact_depth = (
        exact.semantic.transformation_count < sampled.semantic.transformation_count
        and exact.semantic.independent_objects < sampled.semantic.independent_objects
        and exact.semantic.numerical_policy_choices < sampled.semantic.numerical_policy_choices
    )
    exact_observation = RouteObservation(
        "G14--G15 exact projector route",
        exact.probability,
        tuple(exact_times),
        exact_median,
        exact.work,
        exact.semantic,
    )
    sampled_observation = RouteObservation(
        "three-sample dense eigensolver route",
        sampled.probability,
        tuple(sampled_times),
        sampled_median,
        sampled.work,
        sampled.semantic,
    )
    timing_context = TimingContext(
        sys.version.split()[0],
        version("numpy"),
        version("scipy"),
        platform.platform(),
        "time.perf_counter",
        budget.timing_repetitions,
    )
    contract = RouteContract(
        "fixed G10 model and exact local Hermitian coefficient jet",
        "finite-window selected-complement transition probability",
        "norm-weighted sum over the supplied momentum preparations",
        budget.observable_tolerance,
    )
    shared = ("G9/G10 model realization",)
    unpaid = (
        "original unbounded PDE propagation",
        "continuous-window and operator-domain certification",
        "standalone sampled-projector truncation certificate",
    )
    checks = {
        "same_input_contract": dimension
        == exact.work.block_dimension
        == sampled.work.block_dimension,
        "same_observable_within_accuracy": error <= budget.observable_tolerance,
        "same_propagation_work_shape": exact.work.coupling_matrix_entries
        == sampled.work.coupling_matrix_entries
        and exact.work.matrix_exponentials == sampled.work.matrix_exponentials,
        "paired_local_stage_coverage": bool(exact.work.propagated_blocks)
        and bool(sampled.work.propagated_blocks),
        "original_pde_stage_remains_unpaid": "original unbounded PDE propagation" in unpaid,
        "timings_are_finite_positive": all(
            math.isfinite(value) and value > 0 for value in (*exact_times, *sampled_times)
        ),
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise RouteComparisonError("ComparisonResidual", f"comparison fails at {failed}")
    return CompleteRouteComparison(
        contract,
        exact_observation,
        sampled_observation,
        timing_context,
        error,
        exact_median / sampled_median,
        (
            "exact-route-faster-in-this-run"
            if exact_median < sampled_median
            else "sampled-route-faster-in-this-run"
        ),
        "heterogeneous-no-scalar-dominance",
        (
            "lower-declared-exact-depth-with-more-theorem-debt"
            if lower_exact_depth
            else "declared-human-cost-incomparable"
        ),
        shared,
        unpaid,
        checks,
    )
