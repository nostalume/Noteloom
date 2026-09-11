# Retained compiler baseline

## Disposition

This record preserves the first typed-problem-compiler experiment. It is a
historical, provisional baseline, not the active research spine. The active
[observable-relation graph](../research-graph.md) owns current claims and the
[framework](../framework.md) owns the current construction contract.

The baseline established a useful software boundary: different physics areas can
provide different laws and reductions while returning uniform solution,
certificate, transfer, and refusal records. It did not establish automatic prose
interpretation, blind transfer, a new universal physics formalism, reduced
whole-route cost, or improved human performance.

## Provisional spine and stop rule

```text
source audit -> locked questions -> typed ProblemModel
typed ProblemModel -> adapter activation -> obstruction/reduction
obstruction/reduction -> certificates or refusal -> executable slice
executable slice -> regression/transfer/cost comparison -> bounded claim
bounded claim -> review projection
```

Every arrow consumes an inspectable result. The branch must stop or reconstruct
when it cannot represent a selected family without answer-specific fields, when a
reduction changes the requested observable, when transfer needs undeclared
physics, or when organization merely moves rather than removes work.

## Input, admission, and output contract

```text
ProblemModel {
  system, state, domain, scales,
  admissible_laws, symmetry_evidence,
  boundary_and_initial_data,
  observable, unknowns, conventions,
  representation, resource_budget, provenance
}

compile(model) {
  require a defined observable and recoverable answer convention
  collect adapter activation evidence; keywords alone are insufficient
  complete domain-owned laws or return the earliest typed obstruction
  generate only reductions whose hypotheses have witnesses
  reject routes that cannot recover the same observable
  choose by construction + solve + recovery cost
  return Solution(answer, route, certificates, boundary)
      or Refusal(obstruction, smallest_repair, boundary)
}
```

The structured record, not unrestricted prose, is the input boundary. A valid
route carries `(typed input, operation, common target, witness, assumptions,
failure boundary)`. Missing dimensional, sign/orientation, boundary/initial,
conservation/symmetry, limiting-case, residual, approximation, or provenance
certificates remain explicit obligations.

## Stable kernel and domain adapters

```text
DomainAdapter {
  primitive_types
  law_contracts
  activation_evidence(model) -> SupportClaim
  complete(model) -> DomainModel | Obstruction
  construct_routes(domain_model, observable, budget) -> ReductionWitness[]
  recover(route, observable) -> AnswerRepresentation
  certify(route, answer) -> CertificateSet
  mutate(domain_model, typed_change) -> DomainModel | RegimeChange | Refusal
}
```

The kernel preserves the observable, tracks dependencies, checks compositions,
ranks complete routes, and retains equality/error/refusal records. Adapters own
physical primitives, admissible laws, validity regimes, reductions, checks, and
the meaning of a typed mutation.

| Adapter | Owned construction | Decisive refusals |
| --- | --- | --- |
| mechanics | frame forces, balance, constraints, conserved quantities, normal modes | unspecified frame, force, data, or orientation |
| electromagnetism | Maxwell/constitutive bundles, surface reduction, phasor and interface response | missing material/boundary law, gauge-dependent target, invalid scale |
| quantum/atomic | operator domains, coupling hierarchy, spectral blocks and selection graphs | incompatible labels, missing regime, unspecified degeneracy |
| statistical | ensemble/measure, generating function, response derivative and closure | non-normalizable measure, incompatible constraints, absent scale separation |
| condensed matter | lattice/basis, dynamical matrix, Bloch blocks and state counting | cell/atom ambiguity, nonprimitive convention, invalid wavelength regime |

A new adapter is admitted only with independent primitives and laws, a genuine
obstruction, a reusable constructor, direct/transfer/refusal cases, independent
same-observable recovery, and explicit scope and resource bounds.

Adapters compose through typed physical ports rather than importing one another's
internals. A port match requires equal domain, units, orientation, convention,
and approximation regime. The retained executable composition is
`lattice frequencies -> spectral measure -> thermal heat capacity`; a bare mode
count is correctly refused as insufficient.

## SPPC-Bench-17

These identifiers are frozen so later evidence can be compared without silently
changing the question.

| ID | Case | Required output |
| --- | --- | --- |
| M-R | rotating-channel Coriolis tilt | signed height difference with frame and limit checks |
| M-I | changed channel orientation | vector surface gradient projected across the channel |
| M-T | add/remove a justified non-inertial term | rebuilt balance and recovery of the original limit |
| M-X | missing latitude, frame, or orientation | typed symbolic result or precise refusal |
| E-R | conduction/displacement-current ratio | `sigma/(omega epsilon)` with phase and unit checks |
| E-I | loss tangent or crossover recast | equivalent observable from the constitutive pair |
| E-T | tensor response with field direction | directional/vector response without scalar cancellation |
| E-X | tensors without direction or norm | set-valued result or precise refusal |
| Q-R | weak-field `6 ^2 P_(3/2) -> 6 ^2 S_(1/2)` | six shifts and polarization classes |
| Q-I | held-out `LS` transition | generated edges and shifts without a transition template |
| Q-T | explicit strong-field hierarchy | `m_L,m_S` reconstruction and weak-field boundary |
| Q-X | missing hierarchy or incompatible labels | required discriminator, alternatives, or refusal |
| C-R | diamond phonon branches and modes | `3+3` branches and convention-sensitive total count |
| C-I | `p`-atom cell in `d` dimensions | `dp`, `d`, and `d(p-1)` counts |
| C-T | commensurate supercell | invariant total states with changed branch presentation |
| C-X | `N` ambiguous between atoms and cells | two typed results, never a guessed count |
| X-C | lattice modes to thermal response | `D(k)->omega->g->U->C_V`, or an insufficient-port refusal |

`R`, `I`, `T`, and `X` denote regression, isomorphic transfer,
regime/representation transfer, and refusal; `X-C` is cross-area composition.
Each locked case records source/revision, statement/diagram, conventions, laws,
observable, accuracy target, independent route, hidden output, allowed inputs,
compiled model, activation trace, route, answer, certificates/refusal, and
complete-route cost. Expected outputs must be inaccessible to adapter activation,
completion, and route construction.

The broad baseline would pass only if all four regressions recover the reference
observable, at least three isomorphic transfers need no new problem-specific
rule, all regime transfers reconstruct or expose the precise boundary, all four
refusals reject and then accept repaired input, the cross-area port preserves its
types and regime, and two areas reduce a declared whole-route cost. Correctness
without cost makes this a verification/review system, not a new computation
method.

## Four manual constructions

### Mechanics: oriented free-surface balance

For northward velocity `v e_y` in the Earth-fixed frame,

```text
a_C = -2 Omega x v = 2 Omega v sin(lambda) e_x,
h'(x) = a_C/g,
h_east - h_west = 2 Omega v b sin(lambda)/g.
```

Dimensions, the equator limit, and orientation reversal certify the route.
Missing latitude or orientation yields a symbolic/unsigned result or refusal.

### Electromagnetism: common constitutive target

```text
J_cond = sigma E,
J_disp = i omega epsilon E,
|J_cond|/|J_disp| = sigma/(omega epsilon).
```

The shared current-density target licenses cancellation. Tensor coefficients do
not define one scalar ratio without a direction and norm, so the scalar route is
refused rather than extrapolated.

### Atomic physics: selection graph

For the weak-field `6 ^2 P_(3/2) -> 6 ^2 S_(1/2)` transition, the Landé factors
are `4/3` and `2`. Constructing all magnetic sublevels and retaining
`Delta m in {-1,0,1}` gives six edges with photon-shift coefficients

```text
{-5/3, -1, -1/3, 1/3, 1, 5/3} mu_B B.
```

The graph count, sign symmetry, and zero-field limit certify the result. When the
weak-field hierarchy fails, `J,m_J` labels are invalidated and the route must be
rebuilt in `m_L,m_S` variables.

### Condensed matter: typed mode counting

For `p` atoms per primitive cell in `d` dimensions, the displacement fiber has
`dp` branches: `d` acoustic and `d(p-1)` optical. Diamond has `p=2,d=3`, hence
three acoustic and three optical branches. The total is `3N` when `N` counts
atoms and `6N` when it counts primitive cells; an untyped `N` produces both
possibilities, not a guess.

## Executable evidence and source boundary

The baseline implementations were absorbed into the direct `occ` owners. The
[first vertical slice](vertical-slice-01.md) binds mechanics and atomic behavior;
the [expanded vertical slice](vertical-slice-02.md) binds electromagnetic,
lattice, and spectral-to-thermal behavior. Their executable specification is
[`test_vertical_slices.py`](../computation/tests/test_vertical_slices.py).

The 18 public-development tests support a bounded common interface, generated
routes for four structured domains, typed refusal, and one physical-port
composition. They are not hidden tests: expected behavior was visible during
development. The cases are transcript/synthetic-bound under
[`materials.md`](../materials.md), not page-verified A617 regressions. Therefore
they do not establish the SPPC-Bench-17 source, transfer, regime, or cost gates.

## Retained lesson

The common construction is deliberately small:

```text
typed model -> justified law bundle -> obstruction or reduction
            -> requested observable -> replayable witness
            -> one typed mutation and reconstruction
```

The physics remains domain-owned. This separation is retained as architecture
and refusal evidence; current research must earn any stronger claim through the
active benchmark and graph.
