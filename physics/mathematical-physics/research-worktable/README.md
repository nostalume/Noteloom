# Bilateral reduction worktable

## Aim

Construct reductions in both directions without presupposing a group:

```text
representation/action + dynamics  -> differential realization -> reduction witness
differential operator + domain    -> candidate structure       -> reduction witness or obstruction
```

This is not a bijection and not a universal PDE solver. A group alone does not
determine dynamics, and a PDE alone need not determine a unique group. The bounded
machine preserves a named observable and returns one of five outcomes:

```text
exact | controlled | formal | obstructed | unresolved within budget
```

## Spine

The common middle language is a represented filtered operator algebra acting on a
carrier with analytic data. A Lie group is integrated only when finite Lie closure
and global hypotheses are certified.

```text
ReductionRequest
  = operator/representation + carrier + domain/boundary
    + observable + accuracy + resource bound

Candidate constructors
  = factor | centralizer | representation branching | orbit quotient
    | differential complex | mode bundle | observable-cyclic space

ReductionWitness
  = reduced object + analysis/synthesis + residual/error
    + validity domain + construction/recovery cost
```

The capability claim concerns the complete route to the same observable, not a
smaller formula or carrier by itself.

## Start here

- [Research graph](research-graph.md) — six spine nodes, evidence lanes, open
  bridges, and the mapping from retired fine-grained node IDs.
- [Machine contract](machine-contract.md) — full mathematical type and residual
  laws.
- [Computation](computation/README.md) — one executable witness envelope over the
  currently integrated backends.
- [Spine evaluation](spine-evaluation.md) — feasibility and limits of the program.
- [Complexity audit](complexity-reduction-audit.md) — whole-route comparison rules
  and measured benches.
- [Sources](sources.md) and [material audit](material-audit.md) — external theorem
  contracts and local provenance.

## Calculus library

The library is organized by semantic operation rather than by special function or
group name.

| Operation | Owner | Output |
| --- | --- | --- |
| infer structure from an operator | [operator-algebra inverse](operator-algebra-inverse.md) | factors, ladders, closure type, obstructions |
| select finite infinitesimal structures from typed defects | [seed--defect construction](defect-kernel-construction.md) | kernels, effective quotients, closure, and first obstruction |
| compress natural tensor searches before elimination | [structured seed compression](structured-seed-compression.md) | metric-derived candidates, symmetry-orbit residuals, and exact span comparison |
| construct linked-carrier covariance algebras | [coupled-carrier covariance](coupled-carrier-covariance.md) | joint actions, ineffective commutant quotient, and linked-symbol projectors |
| lift symbol centralizers | [filtered centralizer calculus](filtered-centralizer-calculus.md) | commuting differential operators |
| generate bounded quadratic candidates | [quadratic centralizer generator](quadratic-centralizer-generator.md) | complete rank-two modules and kernels |
| realize representations differentially | [representation calculus](representation-calculus.md) | matrix coefficients and spectral channels |
| decompose typed operators | [operator decomposition calculus](operator-decomposition-calculus.md) | selection graphs and reduced maps |
| reduce PDEs geometrically | [PDE decomposition calculus](pde-decomposition-calculus.md) | quotient, complex, spectral, or microlocal routes |
| descend domains and strata | [orbit-space calculus](orbit-space-reduction-calculus.md) | quotient PDEs and isotropy conditions |
| reduce bundle-valued fields | [homogeneous-bundle calculus](homogeneous-bundle-calculus.md) | finite multiplicity complexes |
| follow variable modes | [adiabatic mode-bundle calculus](adiabatic-mode-bundle-calculus.md) | effective connection and leakage residual |
| retain only observable-visible states | [observable-cyclic calculus](observable-cyclic-calculus.md) | Jacobi recurrence and recovery map |
| type nonlinear closure | [polynomial-algebra bridge](polynomial-algebra-bridge.md) | polynomial/Lie distinction and positivity duties |
| select among valid routes | [decision engine](decomposition-decision-engine.md) | comparable witnesses and route decision |

The Euclidean rank-two implementation details remain in
[the radial extension](radial-centralizer-extension.md) and
[the complete `E^3` construction](e3-quadratic-centralizer.md); they are supporting
backends rather than separate spine branches.

## Evidence lanes

Benchmarks are tests of a spine bridge, not nodes that automatically generate more
examples.

| Lane | Representative evidence | Supported conclusion |
| --- | --- | --- |
| regression | [Legendre/`SO(3)`](benchmarks/legendre-so3.md), [rank-one spaces](benchmarks/rank-one-symmetric-spaces.md) | representation data can generate familiar differential spectra; no uniqueness of the inverse |
| non-scalar representation | [`p`-forms](benchmarks/p-form-sphere.md), [`SO(3)` tensors](benchmarks/tensor-operator-so3.md), [`SU(3)` multiplicity](benchmarks/tensor-operator-su3.md), [multiplicity-valued PDE](benchmarks/su-adjoint-multiplicity-pde.md) | fiber type and outer multiplicity must remain explicit and can become reduced differential blocks |
| group-free inverse | [quadratic oscillator](benchmarks/inverse-quadratic-oscillator.md), [Coulomb](benchmarks/coulomb-hidden-so4.md), [matrix PDE Lie closure](benchmarks/pde-first-matrix-lie-reconstruction.md), [symbol covariance/Casimir](benchmarks/matrix-symbol-covariance-casimir.md), [adjoint semigroup promotion](benchmarks/matrix-adjoint-semigroup-global.md), [natural-tensor stabilizer](benchmarks/isotropic-elasticity-natural-tensor.md) | coefficients, pairings, and tensor relations can construct effective algebras and differential modules; structured seeds reduce search before elimination, while global promotion remains observable-relative |
| observable-relative | [cyclic quadratic](benchmarks/observable-cyclic-quadratic.md), [quartic control](benchmarks/quartic-cyclic-transfer.md) | invisible sectors can be removed; no-gain and truncation are valid outcomes |
| route equality and discovery | [oscillator cross-probe](benchmarks/oscillator-cross-probe.md), [backend-independent router](benchmarks/backend-independent-quadratic-router.md), [interbasis cross-probe](benchmarks/singular-interbasis-cross-probe.md) | distinct constructions can be generated and compared on one witness and observable |
| boundary/orbit PDE | [boundary accuracy](benchmarks/boundary-fixed-accuracy-comparison.md), [axial quotient](benchmarks/axial-nonseparable-quotient-pde.md), [warped axis](benchmarks/warped-axis-stratified-quotient-pde.md) | reduction can end in lower-dimensional PDEs and must descend boundary strata |
| spinor/mode bundle | [Pauli--Landau](benchmarks/spinor-pauli-landau.md), [bilateral Pauli router](benchmarks/bilateral-pauli-router.md), [global Pauli promotion](benchmarks/pauli-global-analytic.md), [spin texture](benchmarks/spin-texture-adiabatic.md) | Clifford/projector data replace scalar ladders; on `T^2 x R`, topology constructs multiplicity and promotes the channels to an analytic heat-density witness |
| refusal | [bounded refusal](benchmarks/refusal-probe.md) | failure must identify the violated contract, not invent a group |

## Supported boundary

Supported:

- a typed, non-unique bilateral correspondence;
- bounded symbolic construction for several factor, centralizer, orbit, cyclic, and
  representation routes;
- exact or controlled analysis/synthesis witnesses in representative models;
- same-observable route comparisons including construction and recovery cost;
- explicit refusal for broken symmetry, incompatible domains, insufficient budget,
  or missing analytic hypotheses.

Not supported:

- automatic discovery of a useful group for every PDE;
- exact solvability from formal closure alone;
- analytical completeness for all constructed representations;
- generic nonlinear sector closure;
- route dominance independent of observable, accuracy, and model class.

## Active horizon

The witness and bounded route integrations are retained, but new schema growth is
frozen. A retrospective probe found that centralizer, boundary-stabilizer, and
matrix-covariance routes share a defect/kernel/quotient/closure compiler while
still depending on different, privileged candidate-module origins. The active
contract is therefore [the seed--defect construction calculus](defect-kernel-construction.md).
Its exact kernel, ineffective-ideal quotient, and closure slices are executable
across the admitted regressions. The held-out isotropic-elasticity transfer now
constructs a closed three-generator stabilizer, reduces an axis control to one,
and recovers a longitudinal/transverse propagator observable. G1 then constructs
the metric-kernel seed and permutation-orbit residuals before elimination: exact
span equality is preserved while the one-time proxy falls `1638 -> 117` and the
  break-even `103 -> 8` queries. G2 derives the five-operation route from typed
capabilities and permutation generators, with explicit missing/ambiguous relation
refusals. Its expanded cost audit also exposes 648 orbit-canonicalization checks;
  the selected planning-plus-compiler proxy is 765 with break-even 48. G3 now
  replaces that orbit scan by 21 direct nested-symmetric-power emits, admits
  budgets before materialization, and executes only the selected route. Its
  complete selected proxy is 138 with conditional break-even 9; raw comparison is
  an explicit audit. G4 then constructs linked vector/spinor actions from metric
  and commutator-covariance relations without a group or preferred generators. It
  passes rank-two/rank-three construction, ineffective-phase quotient, refusal,
  and exact principal-symbol projector tests. The active frontier is now lifting
  that generated action through a full order-two operator, lower terms, and domain
  to the same Pauli observable.

Further scalar axial examples, additional polynomial catalogues, arbitrary higher
dimension, and nonlinear generalization are parked until a named downstream claim
requires them.
