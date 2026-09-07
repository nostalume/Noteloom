# Computation workbench

This directory is the executable bench for bilateral construction between
group/representation data and differential operators. It is intentionally
constructive: a route must expose what it builds, what observable it preserves,
what residuals certify it, what it costs, and where it refuses.

## Public flow

```text
path
  -> one ProblemDocument(path, decoded JSON object)
  -> schema registry
  -> route-specific construction
  -> reduction-decision/v1
  -> full certificate or compact summary + semantic exit code
```

`reduction_workbench.py` also exposes three direct backends under the common
`reduction-witness/v1` envelope: `cyclic`, `factor-centralizer`, and
`stratified-orbit`. Omit `--summary` to retain all route evidence.

Outcomes `exact`, `controlled`, and `formal` exit 0; `obstructed` exits 2;
`unresolved` exits 3. Refusal is evidence, not an exception hidden from the
result.

From this directory:

```powershell
uv sync --locked --dev
uv run python reduction_workbench.py discover examples/quadratic-survival-compressed.json --summary
uv run python reduction_workbench.py discover examples/matrix-pde-inverse-sl3.json --summary
uv run python reduction_workbench.py discover examples/matrix-symbol-covariance-sl3.json --summary
uv run python reduction_workbench.py discover examples/matrix-adjoint-semigroup-sl3.json --summary
```

The project follows the latest stable CPython 3.14 line. The current lock resolves
CPython 3.14-compatible NumPy, SciPy, and Ruff versions exactly; update deliberately
with `uv lock --upgrade`, rerun the complete suite, and inspect numerical
tolerances before accepting a new lock.

## Ownership

| Owner | Responsibility |
| --- | --- |
| `problem_input.py` | read/decode a source-backed ProblemSpec once |
| `problem_router.py` | schema-to-constructor registry |
| `linear_defect_compiler.py` | exact residual-kernel intersection, rank ledger, and bounded refusal shared across typed seed adapters |
| `tensor_seed_compression.py` | exact metric-kernel candidates, recursive symmetric-power quotients, audit orbits, tensor defects, brackets, and span certificates |
| `natural_relation_planner.py` | lazy relation planning, symbolic admission, selected-route materialization, and explicit audit |
| `natural_tensor_input.py` | natural-tensor JSON grammar and construction-backed relation certificates |
| `natural_tensor_stabilizer.py` | selected-route execution, optional raw audit, and elasticity use witness |
| `exact_gaussian_matrix.py` | exact Hermitian/skew-Hermitian matrix operations and canonical `u(S)` basis |
| `coupled_covariance_core.py` | reusable linked-carrier covariance defects, ineffective commutant quotient, closure, and exact symbol projectors |
| `coupled_relation_input.py` | shared coupled metric/link admission, capability validation, and exact budgets |
| `coupled_relation_stabilizer.py` | coupled-relation orchestration and public witness projection |
| `coupled_operator_input.py` | typed coupled-operator, domain-contract, optional-observable, and budget admission |
| `full_operator_covariance.py` | curvature, first-order, and zeroth-order defect blocks on a generated coupled action |
| `rational_polynomial.py` | bounded exact rational splitting with explicit field and search refusals |
| `exact_rational_linear.py` | shared exact rational nullspaces, ranks, independent bases, and coordinates |
| `semisimple_coefficient_algebra.py` | commuting Hermitian minimal polynomials, joint idempotents, multiplicities, and polynomial synthesis |
| `represented_star_algebra.py` | Hermitian commutant/bicommutant construction, central sectors, and double-centralizer multiplicities |
| `exact_gaussian_linear.py` | exact Gaussian-rational rank, coordinates, and determinant |
| `simple_block_pde.py` | primitive commutant slices, irreducible actions, quadratic-symbol use, and cost ledger |
| `mode_bundle_jet.py` | exact transported projector/frame jets, connection, leakage, and second-order synthesis |
| `gap_aware_leakage.py` | exact leakage-channel norm, gapped two-channel transition witness, bounds, and refusals |
| `finite_window_propagation.py` | exact full leakage arrow, preparation-specific finite-window bounds, and residual-bearing propagation |
| `coefficient_projector_jet.py` | coefficient-derived spectral projectors, first/second Sylvester jets, gaps, and rigid G11 adaptation |
| `coefficient_algebra.py` | exact involutive two-sector algebra, restricted roots, minimal polynomial, and coefficient-derived projectors |
| `pauli_operator_channels.py` | optional curvature grading, axial coefficient reconstruction, and Pauli channel consumer |
| `coupled_operator_router.py` | generic operator-covariance orchestration, partial-evidence preservation, and public witness projection |
| `adjoint_algebra.py` | immutable rational matrices, Lie/Jordan operations, exact closure, coordinates, and pairing |
| `quadratic_route_router.py` | independent factor/cyclic probes and observable-relative selection |
| `pauli_bilateral_router.py` | local Clifford/PDE construction and coincidence |
| `pauli_global_router.py` | flux, domain, direct-integral, and heat promotion |
| `su_adjoint_multiplicity_router.py` | F3 natural adjoint channels and F4 PDE lift |
| `matrix_pde_inverse_router.py` | F5 PDE-first coefficient-algebra recovery |
| `matrix_symbol_covariance_router.py` | F6 generated derivations, invariant pairing, and Casimir action |
| `matrix_adjoint_global_router.py` | F7 compact real form, quotient, domain, and semigroup promotion |
| remaining scientific modules | cyclic, centralizer, Coulomb, singular, boundary, and quotient-PDE certificates |

The routers consume public algebra operations; they do not import private helpers
from one another. Path-based `discover_problem(path)` functions remain
compatibility entry points. A global route may decode one contained local bridge
file, and it retains a successful local certificate when analytic promotion
fails.

## Admitted discovery families

| Schema | Bilateral construction |
| --- | --- |
| `quadratic-schrodinger/v1` | PDE stiffness/action to factor or observable-cyclic spectral measure |
| `pauli-landau-bilateral/v1` | Clifford/curvature data and matrix PDE to the same spin/Fock channels |
| `pauli-landau-global/v1` | local channels to flux multiplicity, Fourier carrier, and heat observable |
| `su-adjoint-transition/v1` | SU(2)/SU(3) adjoint data to bracket/Jordan intertwiners |
| `su-adjoint-pde/v1` | adjoint channels to a compact Sobolev/Casimir differential block |
| `matrix-pde-inverse/v1` | matrix PDE seeds to effective sl(2)/sl(3) and visible channels |
| `matrix-symbol-covariance/v1` | generated algebra to covariant differential action and Casimir |
| `matrix-adjoint-semigroup/v1` | local symbol block to compact quotient and one heat-semigroup matrix element |
| `natural-tensor-stabilizer/v1` | supplied natural tensors to an effective stabilizer and optional elasticity plane-wave witness |
| `coupled-carrier-covariance/v1` | metric and link relations to an effective coupled action and exact linked-symbol projectors |
| `coupled-operator-covariance/v1` | generated coupled action to ordered full-operator covariance, with optional Pauli and scalar longitudinal channel recovery |

Detailed mathematical contracts live in the neighboring
[benchmarks](../benchmarks/). In particular, see the
[quadratic router](../benchmarks/backend-independent-quadratic-router.md),
[bilateral Pauli construction](../benchmarks/bilateral-pauli-router.md),
[adjoint PDE lift](../benchmarks/su-adjoint-multiplicity-pde.md),
[PDE-first matrix reconstruction](../benchmarks/pde-first-matrix-lie-reconstruction.md),
[symbol covariance](../benchmarks/matrix-symbol-covariance-casimir.md), and
[global adjoint semigroup](../benchmarks/matrix-adjoint-semigroup-global.md). The
[full-operator lift](../full-operator-covariance-lift.md) owns the current coupled
operator contract; [nonzero first-order transport](../nonzero-first-order-transport.md)
owns its scalar longitudinal continuation, and the
[matrix transport algebra](../matrix-valued-transport-algebra.md) owns the
two-sector coefficient-algebra consumer. The
[finite split algebra](../finite-semisimple-coefficient-algebra.md) owns its
multi-generator generalization and exact polynomial synthesis.

## Reproducible verification

Run after every code or dependency change:

```powershell
uv sync --locked --dev
uv run ruff check .
uv run ruff format --check .
uv run python -m unittest test_adjoint_algebra.py test_workbench_contract.py
uv run python -m unittest discover -s . -p "test_*.py"
uv run python -m unittest discover -s . -p "check_*.py"
uv run python -m compileall -q .
```

The exact trace pairing uses
`tr(AB) = sum(A[i,j] * B[j,i])` without materializing `AB`. On Windows with
CPython 3.14.6 and the rank-three global fixture, seven warmed in-process runs
moved from a 207.20 ms median to 205.02 ms. A separate 15-run CLI confirmation
measured 307.37 ms median against the earlier 333.26 ms sample. These are local
regression observations, not portable speed claims; exact output equality is the
primary gate.

## Boundary and extension rule

The current inverse machinery is deliberately bounded to dense exact 2x2 and 3x3
matrix carriers. It does not infer a unique global group from a Lie algebra,
construct arbitrary real forms, prove imported elliptic/domain theorems, enumerate
a full Peter-Weyl spectrum, or solve nonlinear PDEs by relabeling them as linear
representations.

Admit a new route only when it provides:

1. input independent of the expected answer;
2. a reusable constructed object, not a component catalogue;
3. analysis/synthesis maps or an explicit obstruction;
4. exact residuals or a controlled error contract;
5. whole-route cost for a named observable;
6. transfer and refusal tests; and
7. a route-specific certificate preserved by the common envelope.

New case-specific schema growth remains frozen. The generic coupled-operator schema
is one composition boundary whose covariance result remains available without its
optional Pauli consumer. The
[seed--defect compiler](../defect-kernel-construction.md) passes its held-out
isotropic-elasticity transfer, and [G1](../structured-seed-compression.md) now
constructs `g^-1 Lambda^2(V*)` candidates and symmetry-orbit residuals before
elimination. The selected route exactly matches the raw stabilizer span with 3
candidates and 21 residual coordinates rather than 9 and 90. The
[G2 planner](../typed-relation-planner.md) now derives this route from certified
capabilities and permutation generators. Its transparent cost audit finds that
generic orbit canonicalization scans the 81-coordinate input. G3 now replaces it
operationally with recursive quotient-coordinate emission, checks budgets before
materialization, and confines the raw/orbit route to explicit audit. G4 then uses
the common defect compiler on a metric/Hermitian link, constructs its effective
coupled action in ranks two and three, and returns exact principal-symbol
projectors. G5 applies that generated action to curvature and ordered lower-term
defects, returning a closed `3 -> 1` operator action before optional Pauli
recovery. G6 passes nonzero curvature-aligned scalar transport through the
unchanged compiler, derives the axis from curvature, and returns exact shifted
longitudinal polynomials. A transverse coefficient kills the action. G7 now
consumes an axial matrix coefficient through the separate two-sector algebra
owner: exact restricted traces construct its roots, a minimal polynomial recovers
its projectors, and rotated data yields the same channel polynomials without a
preferred spin basis. G8 passes the multi-sector discriminator directly and
through the delegated G7 consumer: exact Krylov dependence and bounded rational
splitting construct three joint sectors from two degenerate generators. G9 now
constructs the noncommutative boundary: Hermitian commutator kernels recover the
represented star-algebra and commutant, G8 splits their center, and exact block
dimensions certify irreducible size and multiplicity. G10 constructs a primitive
commutant slice, solves exact intertwiner coordinates for a minimal carrier, and
verifies a multiplicity-weighted quadratic-symbol determinant. G11 then constructs
the connection and leakage terms of an exact transported projector jet and
reconstructs a second-order section derivative in any tested constant reduced
frame. G12 now promotes one selected momentum-sector leakage column through a
supplied gap and time to an exact
two-channel transition formula and bound. Uniform energy-window and multichannel
PDE propagation remained open at that stage. G13 now constructs the complete
frame-invariant leakage operator at finitely many momenta and compares full and
reduced complement probabilities. Derivation of projector transport and gap data
from variable PDE coefficients remained open at that stage. G14 now constructs
those data exactly for isolated rational Hermitian clusters and passes its rigid
transport subclass through G11 into G13. Projector-native propagation for general
non-rigid second jets remains open.
