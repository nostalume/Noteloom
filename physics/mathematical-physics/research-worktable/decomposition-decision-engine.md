# Observable-preserving decomposition decision engine

## 1. Capability and obstruction

The worktable has several successful reduction mechanisms: representation blocks,
operator ladders, differential complexes, and gapped mode bundles. Their local
mathematics differs, but leaving them as a catalogue does not answer the global
question:

```text
Given a differential problem without a known group, which decomposition object
should be constructed, and what common test says that it preserves the requested
physics?
```

The obstruction to selecting by vocabulary is immediate. The oscillator is
exactly ladder-reducible, the Hodge system is naturally a complex, and a variable
spin texture has only an approximate moving-mode reduction. Requiring all three
to return a Lie group either discards valid structure or invents symmetry.

The smallest common object is therefore a **reduction witness**, not a group.

## 2. Universal reduction witness

First allow a general differential arrow `D:H_E->H_F`. A candidate reduction
supplies reduced carriers `K_E,K_F`, a reduced arrow `D_red:K_E->K_F`, and
analysis/synthesis maps

```text
A_E:H_E -> K_E,     S_E:K_E -> H_E,
A_F:H_F -> K_F,     S_F:K_F -> H_F.                                 (1)
```

Also supply a projector or chosen representative `Q_E,Q_F` for each visible
sector. For a source observable `O:H_E->Y`, also supply `O_red:K_E->Y`.

The engine computes the following residuals on the declared cores:

```text
R_an    = A_F D-D_red A_E,                                           (2a)
R_syn   = D S_E-S_F D_red,                                           (2b)
R_rec,E = S_E A_E-Q_E,       R_rec,F = S_F A_F-Q_F,                  (2c)
R_obs   = O-O_red A_E.                                               (2d)
```

These equations have one common semantic target:

- (2a) asks whether analysis transports the same operator;
- (2b) asks whether synthesis transports the reduced operator back;
- (2c) asks whether synthesis recovers the same visible state or equivalence
  class;
- (2d) asks whether the same observable is computed after reduction.

For dynamics, specialize to `H_E=H_F=H`, `K_E=K_F=K`, and the same analysis map
on both sides. Then the two operator residuals become

```text
R_A = A D-D_red A,          R_S = D S-S D_red.                       (2e)
```

An exact decomposition has all applicable residuals zero. A controlled
decomposition attaches norms, domains, time/energy windows, and a tolerance.
Formal block notation without (2) is not yet a reduction.

When a boundary trace condition `B Gamma_r u=0` is present, admission also requires

```text
R_boundary(Q)=(B Gamma_r Q)|ker(B Gamma_r)=0.           (2f)
```

The interior relation `[D,Q]=0` cannot substitute for (2f). The
[disk/ellipse complexity probe](benchmarks/boundary-domain-symmetry-complexity.md)
uses this rule to remove translations, retain disk rotations, and refuse a false
continuous group on the ellipse before any spectral blocks are formed.

Several earlier constructions are instances of (1)--(2):

| Mechanism | Analysis | Reduced carrier | Meaning of `R_an`/`R_syn` |
| --- | --- | --- | --- |
| group harmonic analysis | Fourier/Peter--Weyl transform | direct sum/integral of multiplicity blocks | failed intertwining or domain compatibility |
| oscillator modes | normal-mode/Fock analysis | occupation-number channels | ladder reconstruction residual |
| differential complex | quotient or Hodge projection | cohomology/exact/coexact blocks | failure of differential arrows to descend |
| tensor-operator graph | carrier decomposition | graph of reduced multiplicity maps | missing or incorrectly reconstructed edge |
| mode bundle | spectral projector/bundle analysis | sections of `Ran(P)` | off-diagonal mode coupling `[D,P]` |
| observable-cyclic reduction | cyclic spectral transform | scalar or block spectral measure | failure of cyclic invariance |

Thus the exact and approximate branches share a contract even when their internal
constructors remain different.

## 3. Why the dynamic residual controls use

Assume for this calculation that `D` and `D_red` generate unitary propagators
`U(t)` and `V(t)` and that (2e) is bounded on invariant sectors. Evaluate the
two dynamics on the same analyzed state by differentiating `V(t-s) A U(s)`:

```text
d/ds [V(t-s) A U(s)]
  = -i V(t-s) (A D-D_red A) U(s)
  = -i V(t-s) R_A U(s).
```

Integrating from `0` to `t` constructs the coincidence defect

```text
A U(t)-V(t)A
  = -i integral_0^t V(t-s) R_A U(s) ds,                              (3)

||A U(t)-V(t)A|| <= |t| ||R_A||.                                    (4)
```

Using (2d), both observable routes land in `Y` and satisfy

```text
||O U(t)psi-O_red V(t)A psi||
 <= ||R_obs U(t)psi||
    +|t| ||O_red|| ||R_A|| ||psi||.                                 (5)
```

For state reconstruction, differentiating `U(t-s)S V(s)` instead gives

```text
U(t)S-SV(t)
 = -i integral_0^t U(t-s) R_S V(s) ds.
```

Consequently, if `R_rec=SA-Q_vis` on the prepared sector,

```text
||U(t)Q_vis psi-SV(t)A psi||
 <= ||R_rec psi||+|t| ||R_S|| ||A psi||.                            (5b)
```

For nonunitary semigroups, the corresponding propagator norms remain inside the
integral. For unbounded operators, core invariance and localized bounds are
theorem obligations. Equation (5) nevertheless identifies the residual the
machine must control; it prevents “smaller blocks” from substituting for
same-observable recovery.

## 4. Candidate generation without a prior group

The engine does not run one universal symbolic solver. It constructs a bounded
portfolio from intrinsic features of the supplied operator. Candidate generation
has six semantic probes:

The [seed--defect construction calculus](defect-kernel-construction.md) now factors
the linearized centralizer, boundary-stabilizer, and covariance portions into two
stages: a typed natural seed module followed by one defect/kernel/quotient/closure
compiler. The retrospective probe supports the second stage but shows that the
seed origins remain genuinely different. Therefore the following list is still a
portfolio; the common witness and defect compiler must not be misreported as a
universal generator.

1. **Constraint/complex probe.** Symbol nullity and identities such as
   `sigma(d_1)sigma(d_0)=0` generate a quotient, gauge complex, or cohomological
   carrier before physical modes are counted.
2. **Factor probe.** A principal-symbol factorization generates intermediate
   bundles and first-order arrows; lower-order residual descent decides whether
   the factorization survives for `D`.
3. **Filtered-centralizer/orbit probe.** The
   [filtered centralizer calculus](filtered-centralizer-calculus.md) solves
   principal-symbol Poisson-centralizer equations inside intrinsic covariance
   modules of any declared order.  Residual descent lifts surviving symbols or
   returns obstruction classes; corrected operator brackets determine joint
   spectral, orbit, Lie, polynomial, or unresolved closure.
4. **Spectral-projector probe.** A separated matrix/operator-valued symbol
   generates Riesz projectors, mode bundles, connections, and the off-diagonal
   residual. A closing gap generates a coupled cluster or crossing obstruction.
5. **Observable-cyclic probe.** Using the
   [cyclic calculus](observable-cyclic-calculus.md), construct from prepared
   vectors/covectors the
   smallest closed `D`-invariant cyclic carrier needed by `O`. A finite or
   generative recurrence gives a reduced spectral measure without first finding a
   spatial symmetry.
6. **Supplied-action probe.** If a group action is actually given, decompose the
   carriers and `D` under conjugation, producing selection graphs and reduced
   multiplicity maps. This probe is optional, not the default inverse.

Each probe returns a candidate `(A,S,D_red)` or its first residual. Candidate
generation may run in any order justified by the symbol and observable; the list
is a portfolio, not a claim that one mechanism dominates the others.

## 5. Decision rule

For every candidate, lift its symbol-level data through the lower differential
orders and compute (2). Then apply the following rule:

```text
if domains/closures needed by the candidate are absent:
    FormalCandidate or AnalyticObstruction

else if all applicable analysis, synthesis, recovery, and observable residuals vanish:
    ExactReduction

else if an error theorem turns the residuals into error <= requested tolerance:
    ControlledReduction(validity window, error certificate)

else if finer sectors fail but their sum is separated and controlled:
    CoupledReduction(enlarged block)

else if required input is absent or several inequivalent candidates remain:
    Underdetermined(missing data, ambiguity groupoid)

else:
    NoCandidateWithinBudget(first residual, re-entry condition).
```

Validity precedes cost. Among candidates meeting the same observable tolerance,
rank with the whole-route cost vector

```text
C_total = (C_discover, C_construct, C_lift, C_close, C_decompose,
           C_analytic, C_solve, C_recover, C_certify,
           semantic_depth).                                         (6)
```

The [whole-route audit](complexity-reduction-audit.md) classifies each stage as
eliminated, compressed, relocated, or unpaid and separates one-time from per-query
cost.  No universal scalar weighting is imposed. The user may prioritize human proof
depth, symbolic expression growth, numerical conditioning, memory, or reuse.
Smaller `dim(K)` wins only when the omitted costs in (6) do not reverse the result.

## 6. Composition is the global simplification law

The useful decomposition of a physical PDE is often a chain: quotient constraints,
decompose a group action, reduce multiplicities, and finally take a cyclic sector.
The witness calculus composes without reopening components.

Let the first reduction have `(A_1,S_1,D_1)` and analysis residual `R_1`, and the
second have `(A_2,S_2,D_2)` and analysis residual `R_2`. Both routes from the
original carrier to the twice-reduced carrier have the same type, and explicit
composition gives

```text
(A_2 A_1)D_0-D_2(A_2 A_1)
 = A_2(A_1D_0-D_1A_1)+(A_2D_1-D_2A_2)A_1
 = A_2 R_1+R_2 A_1.                                                  (7)
```

If `O_0-O_1A_1=E_1` and `O_1-O_2A_2=E_2`, then evaluation on the same original
state gives

```text
O_0-O_2A_2A_1 = E_1+E_2A_1.                                        (8)
```

If the intermediate visible projector acts identically on `Ran(A_1)`, the state
recovery defect similarly becomes

```text
R_rec,composite = R_rec,1 + S_1 R_rec,2 A_1.                         (9)
```

The synthesis-intertwining defect obeys the dual composition law

```text
R_syn,composite = R_syn,1 S_2+S_1 R_syn,2.                           (10)
```

Equations (7)--(10) are the central human-computability gain: reductions can be
designed and checked locally, while their errors and observable recovery propagate
by short map algebra. One does not re-expand the original PDE after every layer.

## 7. Bilateral group--PDE relation

The two directions now have a common codomain:

```text
(group action, representation, supplied D)
  -> construct A,S,D_red by branching/intertwining
  -> ReductionWitness

(PDE D, domain, Prep, O; no group)
  -> construct candidates by the six probes
  -> ReductionWitness
  -> classify generated arrows
  -> integrate a group only if Lie closure and analytic integration are certified.
```

Round-trip equivalence means equality of the witnesses on the declared sector,
including observable and analytic data. It does not mean that a PDE uniquely
recovers a group. Different groups, covers, algebras, or mode bundles may induce
equivalent witnesses for one observable; the ambiguity remains part of the output.

The first executable bundle-valued cross-probe is the
[constant-curvature Pauli bridge](benchmarks/bilateral-pauli-router.md). From
Clifford/curvature data it constructs the Pauli square; from the matrix PDE it
normalizes the subprincipal term to a grading, reconstructs a Clifford-frame
groupoid, and generates the Heisenberg ladder. Both routes meet at the same
spin/Fock channel witness. The recovered object is a graded represented operator
algebra; a unique global magnetic-translation or spin group is intentionally not
claimed.

## 8. Human-facing decision card

A researcher can operate the machine with seven questions:

1. What state or observable must survive?
2. What is the physical carrier after constraints, domains, and boundaries?
3. What does the principal symbol construct: factors, null complex, commutants,
   separated modes, or none of these?
4. Which lower-order residual prevents that symbol decomposition from lifting?
5. Do the corrected arrows close exactly, approximately, only as a block, or not
   within the declared budget?
6. What are the analysis/synthesis maps and `D_red`, and what are the residuals
   (2)?
7. Does the complete route through (5)--(6) improve the named calculation or only
   organize it?

This card is simpler than enumerating special functions or candidate groups. It
retains every failure point required by the machine implementation.

## 9. Supported boundary

Supported here:

- the reduction-witness type and its exact residual tests in both arrow
  directions;
- the propagation/observable identity (3)--(5b) under the stated bounded/unitary
  contract;
- the composition laws (7)--(10);
- the classification of existing worktable outputs by one interface.

Still open:

- completeness of the six probes for any broad PDE class; the filtered-centralizer
  probe is complete only relative to its stated order/covariance/coefficient
  modules;
- a general executable portfolio router. The bounded dispatcher now accepts
  `quadratic-schrodinger/v1`, runs full-mode and cyclic probes independently, and
  changes its decision with preparation visibility. Its
  [executable benchmark](benchmarks/backend-independent-quadratic-router.md) also
  retains the cyclic witness when exact rational factor splitting fails. It also
  accepts `pauli-landau-bilateral/v1`; representation and PDE probes coincide for
  both charge signs, while a bad matrix lower term obstructs only the inverse. The
  `pauli-landau-global/v1` continuation composes that witness with Chern
  integrality, magnetic-translation multiplicity, the Fourier measure, and a heat
  observable; nonintegral flux or the wrong domain blocks only global promotion.
  `su-adjoint-transition/v1` constructs bracket/Jordan intertwiners without a
  Clebsch--Gordan component table, selects two copies for an exchange-paired
  `SU(3)` observable, and one for the `SU(2)` control. Its `su-adjoint-pde/v1`
  continuation realizes those maps on a smooth order-two PDE core. Conversely,
  `matrix-pde-inverse/v1` starts from unlabeled matrix coefficient seeds, closes
  them to `sl_2/sl_3`, and recovers the same visible amplitude while refusing an
  incomplete seed algebra and retaining global-group ambiguity. Its
  `matrix-symbol-covariance/v1` continuation constructs the covariance action and
  Casimir eigenvalue from the principal pairing; `matrix-adjoint-semigroup/v1`
  then promotes one visible block through compact real-form, normalized-Haar, and
  `H^2` contracts while preserving the invisible `SU(n)/PSU(n)` quotient.
  Beyond these problem grammars, two probes have independent exact backends: finite
  observable-cyclic reduction and the relative-complete
  [quadratic centralizers](quadratic-centralizer-generator.md), including the
  nontrivial [three-dimensional quotient](e3-quadratic-centralizer.md). The
  [oscillator cross-probe](benchmarks/oscillator-cross-probe.md) joins factor and
  centralizer witnesses for one exact class, but is not yet a general router;
- automated analytic-domain certification beyond the explicit theorem contracts
  admitted by individual grammars;
- a continuum-certified nonquadratic transfer where an approximate cyclic witness
  competes with exact commutant information. The
  [quartic finite-model probe](benchmarks/quartic-cyclic-transfer.md) now performs
  this comparison inside one Galerkin model but does not certify its PDE limit.

Therefore this is a supported semantic decision engine, not a universal PDE
solver.  The [Coulomb bench](benchmarks/coulomb-hidden-so4.md) supplies its first
hidden-symmetry full-route spectral regression: the PDE constructs a sectorwise
Lie algebra that computes all bound energies and degeneracies, while the domain
and completeness theorem remains imported.  Its first restricted
observable-cyclic leverage result is the
[observable-cyclic quadratic bench](benchmarks/observable-cyclic-quadratic.md);
the quartic probe adds a reproducible no-gain/refusal verdict beyond quadratic
closure, while continuum generality remains open.

The [Euclidean-plane transfer](benchmarks/quadratic-centralizer-e2.md) separately
supports relative-complete Step-B discovery: the metric generates the candidate
module, the potential selects its kernel, and exact operator composition certifies
the quantum lift.  Its [radial extension](radial-centralizer-extension.md) now
rediscovers the complete two-dimensional Coulomb hidden algebra and distinguishes
it from a rotation-preserving perturbation. The
[complete `E^3` transfer](e3-quadratic-centralizer.md) now constructs its
rank-two redundancy quotient and the `so(4)` spectrum route without a selected
Runge--Lenz module. Dimension-/metric-parametric generation, higher orders,
bundles, and analytic strong commutation remain open.

The [oscillator cross-probe](benchmarks/oscillator-cross-probe.md) supplies the
first executable use of the ranking rule between two independently valid PDE-first
constructors. It proves equality at the primitive-projector, reduction-witness,
representation, and observable levels, then selects factorization while retaining
the centralizer's distinct completeness certificate.

The [singular-oscillator transfer](benchmarks/singular-oscillator-polynomial.md)
now makes closure classification executable beyond the Lie branch: the same
PDE-first probe returns an exact degree-two polynomial presentation and refuses
group integration. Its bounded adapter then generates positive finite Jacobi
modules and recovers the energy family and multiplicity. The recurrence is a
completed interbasis reduction witness for phase-insensitive probabilities: the
[cross-probe](benchmarks/singular-interbasis-cross-probe.md) independently builds
the factor `su(1,1)` coproduct Casimir and proves exact primitive, spectrum, and
probability equality. Its `ParetoRetainBoth` verdict keeps the shorter known-split
route and the group-free relative-completeness route as distinct capabilities.
