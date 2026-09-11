# Bilateral PDE/group reduction worktable

## Aim

Construct useful reductions in either direction without presupposing a group:

```text
representation/action + dynamics -> differential realization -> witness
differential operator + domain   -> candidate structure       -> witness or obstruction
```

The correspondence is typed and non-unique. A group does not determine dynamics,
and a PDE need not determine a unique group. The machine returns `exact`,
`controlled`, `formal`, `obstructed`, or `unresolved within budget` for a
named preparation, observable, accuracy, domain, and resource bound.

## Common spine

The common middle object is a represented filtered operator algebra with analytic
data. A Lie group is integrated only after finite Lie closure and the required
global hypotheses are certified.

```text
ReductionRequest
  -> candidate construction
     (factor | centralizer | branching | quotient | complex | mode bundle | cyclic)
  -> ReductionWitness
     (analysis, synthesis, reduced dynamics, recovery, residual/error, domain, cost)
  -> same-observable route decision or typed refusal
```

This is a bounded reduction compiler, not a universal PDE solver. Computational
gain is claimed only for the complete route, including construction and observable
recovery.

## Navigation

- [Research graph](research-graph.md): current six-node spine, compact evidence
  disposition, active G22 symbol-construction frontier, and parked branches.
- [Research nodes](nodes/README.md): the 37 semantic construction owners, grouped
  by capability.
- [Benchmark index](benchmarks/README.md): regression, transfer, refusal, analytic,
  and cost evidence.
- [Computation workbench](computation/README.md): executable schemas, owners,
  commands, and extension boundary.
- [Machine contract](machine-contract.md): mathematical types, residual laws,
  inverse targets, and certificate envelope.
- [Spine evaluation](spine-evaluation.md): bounded feasibility verdict and weakest
  open bridge.
- [Complexity audit](complexity-reduction-audit.md): complete-route comparison law
  and result ledger.
- [Sources](sources.md) and [material audit](material-audit.md): theorem contracts
  and local provenance.

## Construction families

| Family | Constructed object | Principal boundary |
| --- | --- | --- |
| bilateral/reduction calculi | factors, represented actions, quotient PDEs, complexes, cyclic carriers, comparable witnesses | grammar, domain, and observable must be declared |
| candidate construction | exact defect kernels, compressed seeds, relation plans, centralizers, effective quotients | completeness is budget- and candidate-module-relative |
| finite represented algebras | covariance actions, coefficient algebras, isotypic blocks, primitive carriers | finite exact matrix setting; global integration is separate |
| variable-block propagation | projector jets, invariant leakage arrows, finite-window propagation, active carriers | isolated gaps, finite windows, and declared preparation/effect |

The detailed owner and current disposition of every operation are listed in
[nodes/README.md](nodes/README.md). Euclidean rank-two and `E^3` centralizers are
supporting backends, not separate spine branches.

## Evidence summary

The admitted benches establish, within their stated domains:

- representation-first differential realization beyond scalar polynomials,
  including bundles, spinors, and outer multiplicity;
- PDE-first factor, centralizer, coefficient-algebra, and covariance construction
  without supplying the expected group label;
- quotient PDE reduction with boundary and singular-stratum descent;
- observable-relative cyclic and active-carrier compression;
- exact or controlled coincidence of independent routes in selected quadratic,
  Pauli, and adjoint models;
- explicit refusal when covariance, domain, gap, grammar, or budget fails.

They do not establish a useful group for every PDE, exact solvability from formal
closure, generic nonlinear sector closure, analytical completeness, or
model-independent route dominance.

## Active frontier

G19 constructs a local variable frame and full product-rule leakage from
base-point reachability provenance. G20 now consumes that leakage publicly:
first-order function-field rank one yields a real projective derivation line, and
one exact full-operator commutator kernel decides whether it has a visible
skew-Hermitian lift. The route distinguishes lift, same-line/no-lift, rank-two,
coefficient-only, complex-real-form, higher-order, and budget outcomes while
retaining G19 evidence. Multi-line Lie closure, controlled recovery, global
integration, bundle gluing, and boundary descent remain open.

G21 closes several exact local lifts over constant real scalars and quotients pure
internal ambiguity, while its degenerate-symbol control proves that generic
polynomial closure can be infinite. G22 now removes the remaining seed privilege
for a common class: a constant nondegenerate scalar principal symbol constructs
all `d(d+1)/2` affine Killing candidates, a canonical `u(n)` seed supplies the
constant internal lifts, and one exact full-operator kernel returns the visible
local Lie algebra. Free, anisotropic, nonorthogonal-coordinate, and radial matrix
tests discriminate the unchanged constructor; an independent G20 route agrees on
the public fixture.

The next structural frontier is not another potential or named group. It is a
finite-type symbol-stabilizer/prolongation certificate for variable or
matrix-valued principal symbols, with an explicit refusal when no bounded
candidate module is justified. Global integration, domain flow, spectral use, and
complete-route leverage remain separate gates.

More scalar examples, polynomial catalogues, arbitrary dimension, and nonlinear
systems remain parked until they change a current contract, witness, or boundary.
