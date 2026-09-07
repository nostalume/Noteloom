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
  disposition, active G19 frontier, and parked branches.
- [Research nodes](nodes/README.md): the 33 semantic construction owners, grouped
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

G18 now constructs one exact cyclic module for an entire coefficient family,
proves specialization invariance, and conditionally beats repeated pointwise
closure on a four-point window while honestly losing for one point. The next
discriminating bridge is G19: lift that internal certificate to
`D=sum_alpha L_alpha tensor H_alpha` before momentum sampling, and prove that an
invertible change of the scalar differential basis preserves the internal module,
PDE intertwiner, and requested observable. Domain descent remains an explicit
obligation rather than a formal consequence.

More scalar examples, polynomial catalogues, arbitrary dimension, and nonlinear
systems remain parked until they change a current contract, witness, or boundary.
