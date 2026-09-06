# Coupled-carrier covariance construction

## Frozen contract `C_G4_v1`

### Spine bridge

G0 constructs finite stabilizers from linear defects, but G1--G3 exercise one
real tensor carrier. A spinor-valued symbol instead contains a typed link

```text
gamma : V -> End(S)
```

between a real metric carrier `(V,g)` and a Hermitian complex carrier `S`. The
missing bridge is not another Pauli formula. It is construction of the joint
infinitesimal action from the link itself, without a group name, stabilizer basis,
or expected dimension.

`C_G4_v1` admits finite exact data over the Gaussian rationals:

```text
CoupledRelationProblem = (
  rational nondegenerate symmetric metric g on V,
  Hermitian Gaussian-rational matrices gamma_i = gamma(e_i),
  requested link capabilities,
  optional covector and preparation for symbol use,
  candidate/residual/bracket resource budget
).
```

The candidate seed is intrinsic but plural:

```text
End_R(V) direct-sum u(S).
```

No universal seed claim is made. `End_R(V)` is forced by an unknown base action;
`u(S)` is forced by preservation of the supplied Hermitian structure.

### Construction

For every candidate pair `(A,B)`, form two linear defects:

```text
R_g(A,B)       = A^T g + g A,
R_gamma,i(A,B) = [B,gamma_i] - sum_j A_(j,i) gamma_j.      (1)
```

The common G0 compiler intersects their kernels. Pairwise commutators in
`End_R(V) direct-sum u(S)` supply the candidate bracket. The visible action is
the base action `A`; therefore pairs with `A=0` form the ineffective fiber
commutant and must be proved to be an ideal before quotienting.

When the requested capability is `metric-clifford-link`, admission also checks

```text
gamma_i gamma_j + gamma_j gamma_i = 2 g_(i,j) I.          (2)
```

Equation (2) is an input-relation certificate, not the inferred Lie algebra.

For an optional covector `k`, the use stage constructs

```text
c(k) = sum_i k_i gamma_i,
q(k) = k^T g^(-1) k,
P_+/- = (I +/- c(k)/sqrt(q(k)))/2,                        (3)
```

provided `q(k)` is a nonzero rational square. It verifies the Clifford square,
projector, synthesis, and symbol-intertwining identities exactly. A nonsquare
norm refuses this exact projector realization rather than introducing floating
arithmetic.

### Frozen discriminators

1. One unchanged constructor handles both a two-dimensional and a
   three-dimensional base Clifford link.
2. The rank-three input begins with `9+4=13` candidates. The simultaneous kernel
   has dimension four; one fiber phase is ineffective; the effective quotient has
   dimension three and is closed.
3. The rank-two transfer begins with `4+4=8` candidates and returns kernel/effective
   dimensions two/one after the same ineffective phase quotient.
4. Inputs contain matrices, relations, observable, and budgets, but no group name,
   preferred generators, structure constants, or expected dimensions.
5. A violated requested Clifford relation returns
   `CliffordRelationViolation`. A candidate budget below the symbolic dimension
   returns `CandidateBudgetExceeded` before candidate or defect materialization.
6. For `k=(1,2,2)` in the rank-three Euclidean input, (3) gives two exact
   projectors and exact symbol reconstruction without an eigensolver.

The candidate is falsified if it chooses a Pauli basis as the answer, hides a
complex numerical nullspace, fails to quotient the scalar phase, amends rules for
rank two, or promotes covariance closure to global spin-group integration.

### Bench family and promotion

- **Regression:** rank-three irreducible Clifford link and exact projectors.
- **Structural transfer:** rank-two link through the unchanged constructor.
- **Adversarial:** one broken Clifford anticommutator.
- **Resource refusal:** rank-three input below candidate budget.
- **Use:** exact characteristic projectors for the named linked symbol.

Promotion requires all five. Passing supports only construction of the effective
finite covariance algebra and exact symbol channels in this grammar. It does not
support runtime leverage, arbitrary Clifford dimension, global integration,
curved or bounded spin geometry, variable coefficients, analytic spectral
completion, or nonlinear systems.

## Pseudocode and code boundary

```text
plan(g, gamma, budget):
    n_candidates <- dim(V)^2 + dim(S)^2
    n_residuals <- dim Sym^2(V*) + dim(V) dim Herm(S)
    refuse before materialization when either bound fails

construct(g, gamma):
    candidates <- canonical End(V) and u(S) matrix units
    defects <- metric_defect + link_covariance_defect
    bracket <- componentwise commutator
    visible <- flattened base actions
    return compile_defects(candidates, defects, visible, bracket)

use(gamma, k):
    construct c(k), q(k), P_plus, P_minus
    certify square, resolution, orthogonality, and intertwining
```

The exact complex-matrix substrate should remain below roughly 220 source lines;
the coupled mathematical core below roughly 360; the public adapter below roughly
320; and its public tests below roughly 220.

## Evidence ledger

### `E-G4-01` — rank-three construction

The generic candidate is `End(R^3) direct-sum u(2)`, of dimension 13. Metric
preservation has rank six and leaves dimension seven. Link covariance has three
additional independent defects and leaves a four-dimensional joint kernel. The
visible-base quotient discovers one ineffective fiber phase and returns a closed
three-dimensional effective algebra. The witness retains the three generated
base/fiber pairs and the ineffective pair; no expected dimension or preferred
basis occurs in the fixture.

### `E-G4-02` — structural transfer

The unchanged constructor receives two link matrices over `R^2`. Its symbolic
plan changes to 8 candidates and 11 residual coordinates. Metric and covariance
defects have ranks three and three; the kernel has dimension two, the ineffective
phase has dimension one, and the effective quotient has dimension one. No
rank-specific construction rule was added.

### `E-G4-03` — refusal and laziness

A broken anticommutator returns `CliffordRelationViolation` with zero
materialization. Reducing the rank-three candidate budget from 13 to 12 returns
`CandidateBudgetExceeded`, also with zero materialization. The symbolic bracket
upper bounds are 2873 and 768 for the rank-three and rank-two plans.

### `E-G4-04` — symbol use

For `k=(1,2,2)` the rank-three constructor derives norm three; for the rank-two
transfer `k=(3,4)` gives norm five. In both cases all seven exact laws pass:
Clifford square, two idempotences, orthogonality, synthesis, and the two symbol
intertwining identities. No component eigensolver is used.

Observed implementation sizes are 190 lines for the Gaussian-rational substrate,
303 for the reusable covariance core, 293 for the public adapter, and 66 for its
focused tests. The public and common-dispatch focused suite executes eight tests.
Fresh closure of the computation workbench reports 137 unit tests and 20 numerical
checks passing, Ruff lint and format passing over 57 files, successful bytecode
compilation, and zero broken local Markdown links. This evidence is bound to the
G0--G4 stage commit containing this packet; its commit hash is the external
revision identifier.

Disposition: **supported bounded** for finite exact local metric/Hermitian links,
their observable-effective covariance algebra, and rational-norm principal-symbol
projectors. This is cross-family transfer for the G0 defect compiler, not yet a
full spinor PDE decomposition. Lower-order coefficients, differential domains,
global spin integration, arbitrary Clifford size, runtime leverage, and analytic
spectral completion remain open.
