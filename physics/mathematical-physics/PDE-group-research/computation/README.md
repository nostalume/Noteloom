# Computation workbench

This directory executes bounded bilateral constructions between
group/representation data and differential operators. A route must expose what it
constructs, the observable it preserves, residual/error, cost, provenance, and
refusal boundary.

## Public flow

```text
path
  -> ProblemDocument(path, decoded JSON object)
  -> schema registry
  -> route-specific construction
  -> reduction-decision/v1
  -> full certificate or compact summary + semantic exit code
```

`reduction_workbench.py` also exposes direct `cyclic`,
`factor-centralizer`, and `stratified-orbit` backends under
`reduction-witness/v1`. Omit `--summary` to retain full route evidence.
`exact`, `controlled`, and `formal` exit 0; `obstructed` exits 2;
`unresolved` exits 3.

## Quick start

From this directory:

```powershell
uv sync --locked --dev
uv run python reduction_workbench.py discover examples/quadratic-survival-compressed.json --summary
uv run python reduction_workbench.py discover examples/matrix-pde-inverse-sl3.json --summary
uv run python reduction_workbench.py discover examples/matrix-symbol-covariance-sl3.json --summary
uv run python reduction_workbench.py discover examples/matrix-adjoint-semigroup-sl3.json --summary
uv run python reduction_workbench.py discover examples/polynomial-active-variable.json --summary
uv run python reduction_workbench.py discover examples/polynomial-lie-lift.json --summary
uv run python -m unittest check_residual_direction_lift.py
```

The project targets the current stable CPython 3.14 line and pins compatible
NumPy, SciPy, SymPy, and Ruff versions in `uv.lock`. Upgrade deliberately with
`uv lock --upgrade`, then rerun all checks and inspect numerical tolerances.

## Ownership

| Owner group | Modules | Responsibility |
| --- | --- | --- |
| admission/routing | `problem_input.py`, `problem_router.py`, route input modules | decode once into typed schemas and select one constructor |
| exact linear algebra | `exact_rational_linear.py`, `exact_gaussian_linear.py`, `exact_gaussian_matrix.py`, `exact_polynomial_matrix.py`, `rational_polynomial.py` | ranks, kernels, multivariate polynomial matrices, coordinates, splitting, and bounded refusal |
| seed/relation construction | `linear_defect_compiler.py`, `tensor_seed_compression.py`, `natural_relation_planner.py`, `natural_tensor_stabilizer.py` | structured candidates, lazy quotient relations, defect kernels, closure, and audit |
| coupled covariance | `coupled_covariance_core.py`, coupled input/router modules, `full_operator_covariance.py` | linked base/fiber actions and ordered full-operator lift |
| finite represented algebras | `coefficient_algebra.py`, `semisimple_coefficient_algebra.py`, `represented_star_algebra.py`, `simple_block_pde.py` | projectors, center, multiplicity, primitive carriers, and PDE use |
| moving blocks | `mode_bundle_jet.py`, `coefficient_projector_jet.py`, `off_block_differential.py`, `projector_native_propagation.py` | exact projector/frame jets and common invariant arrows |
| propagation/cost | `gap_aware_leakage.py`, `finite_window_propagation.py`, `gaussian_active_subspace.py`, `active_window_propagation.py`, benchmark modules | analytic promotion, observable recovery, and whole-route comparison |
| bilateral physics routers | quadratic, Pauli, adjoint, matrix-inverse/covariance/semigroup router modules | independent constructions projected to the common witness |
| scientific backends | remaining cyclic, centralizer, Coulomb, singular, boundary, and quotient modules | route-local mathematical certificates |

Routers consume public algebra operations and do not import another router's
private helpers. A global route may consume one contained local bridge and must
retain that successful certificate if analytic promotion fails.

## Admitted schemas

| Family | Schemas / construction |
| --- | --- |
| quadratic and orbit | `quadratic-schrodinger/v1` plus the three direct backends |
| Pauli | `pauli-landau-bilateral/v1`, `pauli-landau-global/v1` |
| adjoint | `su-adjoint-transition/v1`, `su-adjoint-pde/v1`, `matrix-pde-inverse/v1`, `matrix-symbol-covariance/v1`, `matrix-adjoint-semigroup/v1` |
| relation-derived covariance | `natural-tensor-stabilizer/v1`, `coupled-carrier-covariance/v1`, `coupled-operator-covariance/v1` |
| variable PDE modules | `polynomial-active-module/v1`: provenance-derived local frame, exact rank chart, leakage, and optional residual-derived local infinitesimal lift |

These schemas are bounded scientific grammars, not a catalogue to extend for each
new example. Mathematical contracts are indexed in
[benchmarks](../benchmarks/README.md), with construction ownership in
[nodes](../nodes/README.md).

## Canonical verification

```powershell
uv sync --locked --dev
uv run ruff check .
uv run ruff format --check .
uv run python -m unittest test_adjoint_algebra.py test_workbench_contract.py
uv run python -m unittest discover -s . -p "test_*.py"
uv run python -m unittest discover -s . -p "check_*.py"
uv run python -m compileall -q .
```

JSON fixtures must also parse as JSON. Exact output equality is the primary gate;
wall-clock measurements are local observations tied to their benchmark,
environment, repetitions, and noise limits.

## Extension boundary

The current inverse machinery is bounded to dense exact 2x2 and 3x3 matrix
carriers and declared finite grammars. It does not infer a unique global group,
construct arbitrary real forms, import missing domain theorems, enumerate a full
Peter--Weyl spectrum, or solve nonlinear PDEs.

Admit a new route only when it provides:

1. input independent of the expected answer;
2. a reusable constructed object rather than a component catalogue;
3. analysis/synthesis or an explicit obstruction;
4. exact residuals or controlled error;
5. whole-route cost for one observable;
6. transfer and refusal evidence; and
7. route-specific detail preserved by the common envelope.

G18 constructs one preparation-reachable module for a finite Hermitian coefficient
family. G19's `polynomial-active-module/v1` route now evaluates a general exact
polynomial coefficient family at a base point, retains only the admitted
reachable-expression DAG, continues that DAG polynomially, certifies one local
rank chart by bounded rational Horner intervals, and returns the exact product-rule
reduced operator and leakage. `formal` means the reconstruction identity is exact
but leakage is nonzero and unbounded; requesting exact closure instead returns
`CoefficientOrDerivativeEscape`. Exhausted chart search returns
`RankRegionUnresolved`, never a guessed rank jump. V1 admits only
compact-supported smooth sections without boundary trace and does not construct a
global group. See the [G19 node](../nodes/variable-active-module-bundle.md).

The additive `construct-local-infinitesimal-symmetry` capability first completes
G19, then filters residual order, computes the exact first-order function-field
rank, normalizes a real projective direction, and compiles
`[D,lambda L_v-J]` over the canonical `u(n)` seed. A visible kernel vector returns
the local lift and internal-centralizer ambiguity. Rank zero/two, absent real
form, higher-order leakage, absent visible lift, and resource exhaustion are typed
separately; every downstream refusal retains the G19 witness. The maintained
`check_residual_direction_lift.py` remains an independent certificate. See the
[G20 node](../nodes/residual-direction-lie-lift.md). This route proves a local
common-core identity, not Lie closure, group integration, or domain preservation.
