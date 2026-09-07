# Compact research graph

## Spine invariant

The graph preserves one semantic object: the requested observable of an operator
problem with its carrier, domain, boundary data, accuracy, and resource bound.

The program is not organized by special function, coordinate system, or group
name. Its durable output is a `ReductionWitness` or an obstruction.

```text
                    representation/action
                            |
                            v
S0 request semantics --> S2 realization -----------+
        |                                           |
        v                                           v
G0 seed--defect layer --> S1 typed constructors --> S3 witness calculus
                                                    |
                                                    v
                                              S4 executable tool
                                                    |
                                                    v
                                              S5 capability verdict
```

`S1` and `S2` are the two bilateral directions. They need not invert one another.
They coincide only when their outputs produce equivalent witnesses for the same
observable.

## Node contract

Every active node records:

```text
question -> typed input -> construction -> witness/check -> compact output
         -> validity/failure boundary -> named downstream edge
```

A benchmark is evidence for a node, not a node merely because it is another
example. Detailed derivations remain in their calculus or benchmark owners.

## S0 — Typed problem and inverse semantics (`supported`)

- **Question:** What data make either direction meaningful?
- **Input:** operator or representation, carrier, domain/boundary, preparation,
  observable, tolerance, and resource bound.
- **Construction:** distinguish point symmetry, dynamical algebra, monodromy,
  differential Galois data, and integration of a represented Lie algebra. Treat
  inverse fibers as non-unique.
- **Output:** `ReductionRequest`; a group name is optional output, never presumed
  input in the PDE-first direction.
- **Evidence:** [material audit](material-audit.md), [source map](sources.md), and
  the inverse diagnosis in the [machine contract](machine-contract.md).
- **Boundary:** a bare PDE and a bare group do not determine each other.
- **Edges:** `S0 -> S1,S2,S3` supplies the shared types and observable.

## S1 — Operator-to-structure discovery (`supported bounded contract`)

- **Question:** What algebraic or geometric structure can be generated from the
  operator without guessing a group?
- **Input:** symbols and lower coefficients, domain/boundary strata, coefficient
  grammar, and search order/budget.
- **Construction:** factor symbols; compute bounded filtered centralizers; discover
  joint operator-domain stabilizers; generate cyclic carriers; classify exact
  closure as Lie, graded, polynomial, parameter-shift, or unresolved.
- **Output:** candidate represented algebra, factor/commutant, orbit quotient,
  complex, mode bundle, cyclic object, or obstruction class.
- **Owners:** [operator-algebra inverse](operator-algebra-inverse.md),
  [filtered centralizers](filtered-centralizer-calculus.md),
  [PDE decomposition](pde-decomposition-calculus.md),
  [orbit-space reduction](orbit-space-reduction-calculus.md), and
  [observable-cyclic reduction](observable-cyclic-calculus.md).
- **Checks:** exact commutators, order-lowering residuals, stabilizer equations,
  recurrence termination, isotropy compatibility, and transfer/refusal cases.
- **Boundary:** completeness is relative to the declared coefficient grammar,
  order, domain, and budget; generic structure discovery is not promised.
- **Edges:** `S1 -> S3`; finite certified Lie closure may additionally enter `S2`.

## S2 — Structure-to-differential realization (`supported contract`)

- **Question:** How do representation data generate differential systems and
  finite reduced channels without component enumeration?
- **Input:** represented algebra/group action, carrier or bundle type, dynamics,
  and observable.
- **Construction:** derived representation and matrix coefficients; branching and
  reduced multiplicity maps; enveloping-algebra operations; homogeneous bundles
  and finite differential complexes; Clifford or projector-bundle extensions.
- **Output:** differential realization, selection graph, multiplicity block,
  spectral recurrence, or bundle-valued reduced operator.
- **Owners:** [representation calculus](representation-calculus.md),
  [operator decomposition](operator-decomposition-calculus.md),
  [homogeneous bundles](homogeneous-bundle-calculus.md), and
  [adiabatic mode bundles](adiabatic-mode-bundle-calculus.md).
- **Checks:** intertwining, branching multiplicity, differential-complex laws,
  matrix-coefficient equations, and recovery of scalar limits.
- **Boundary:** representation data constrain channels but do not supply dynamics;
  analytic domains and global group integration remain separate obligations.
- **Edges:** `S2 -> S3`; comparison with `S1` is made only through a common witness.

## S3 — Reduction witness and decision calculus (`supported`)

- **Question:** When do heterogeneous constructions represent the same useful
  reduction, and how should a route be selected?
- **Input:** candidates from `S1` or `S2` plus the `S0` request.
- **Construction:** build analysis `A`, synthesis `S`, reduced dynamics `D_red`,
  visible projector `Q_vis`, and residuals

  ```text
  AD - D_red A,   DS - S D_red,   SA - Q_vis,   O - O_red A.
  ```

  Compose witnesses and propagate residuals. Compare complete construction,
  solution, and recovery costs for the same observable and accuracy.
- **Output:** `exact`, `controlled`, `formal`, `obstructed`, or
  `unresolved within budget`, with route decision and limitations.
- **Owners:** [machine contract](machine-contract.md),
  [decision engine](decomposition-decision-engine.md), and
  [complexity audit](complexity-reduction-audit.md).
- **Checks:** round-trip/observable coincidence, Duhamel error bounds, cross-route
  equality, dominance or Pareto incomparability, and honest refusal.
- **Boundary:** formal closure is not analytic completeness or computational gain.
- **Edges:** `S3 -> S4,S5`.

## S4 — Executable reduction workbench (`supported bounded router`)

- **Question:** Is the common witness a real interface rather than shared prose?
- **Input:** either one named backend for direct execution or an admitted physical
  `ProblemSpec` without a backend/group name.
- **Construction:** normalize independent backends; for
  `quadratic-schrodinger/v1`, run full-mode and observable-cyclic applicability
  probes independently; for `pauli-landau-bilateral/v1`, independently construct
  representation-to-PDE and PDE-to-representation candidates; for
  `pauli-landau-global/v1`, compose their common local witness with topology,
  domain, magnetic multiplicity, and Fourier measure; for
  `su-adjoint-transition/v1`, construct natural adjoint intertwiners and select the
  observable-visible outer-multiplicity quotient; for `su-adjoint-pde/v1`, lift
  those maps through the compact adjoint Casimir to an order-two differential
  witness on a smooth matrix-coefficient core; for `matrix-pde-inverse/v1`, close
  unlabeled matrix coefficient seeds under exact commutators and reconstruct the
  effective algebra and natural maps; for `matrix-symbol-covariance/v1`, generate
  inner-derivation vector fields, verify the principal pairing, and construct its
  scalar second-order action; for `matrix-adjoint-semigroup/v1`, use involution,
  positivity, normalized Haar measure, and an `H^2` domain contract to promote the
  visible coefficient block to a compact heat-semigroup witness. Compare only at
  the common observable witness. For `natural-tensor-stabilizer/v1`, plan lazy
  tensor quotient defects; for `coupled-carrier-covariance/v1`, construct joint
  base/fiber actions from a metric and link relation and quotient their ineffective
  commutant; for `coupled-operator-covariance/v1`, lift that action through ordered
  lower terms and optionally consume its two-sector coefficient algebra.
- **Output:** executable `reduction-witness/v1` envelope or
  `reduction-decision/v1` with probes, candidates, coincidence, decision, and a
  compact human card.
- **Owner:** [computation workbench](computation/README.md) and
  `computation/reduction_workbench.py`.
- **Integrated backends:** exact factor/centralizer cross-probe, exact/controlled
  observable-cyclic recurrence, and stratified orbit-space PDE reduction.
- **Backend-free bench:** [quadratic route discovery](benchmarks/backend-independent-quadratic-router.md)
  changes selection from cyclic at `r=1` to full modes at `r=3`; an irrational
  factor spectrum obstructs only that probe while exact cyclic reduction survives.
- **Bundle-valued bench:** the [bilateral Pauli router](benchmarks/bilateral-pauli-router.md)
  constructs equal Clifford--Heisenberg channel witnesses for both charge signs;
  a broken matrix lower term obstructs only the PDE-first probe. The
  [global promotion](benchmarks/pauli-global-analytic.md) constructs the unitary
  direct-integral contract and heat density, or refuses nonintegral flux/domain.
- **Non-Abelian bench:** the [`SU(3)` multiplicity router](benchmarks/tensor-operator-su3.md)
  constructs bracket/Jordan intertwiners without weights, proves that two reduced
  channels are visible to an exchange-paired amplitude, transfers to the one-copy
  `SU(2)` control, and refuses invalid carrier data.
- **Multiplicity-valued PDE bench:** the [adjoint PDE lift](benchmarks/su-adjoint-multiplicity-pde.md)
  constructs a left-covariant order-two operator on `L^2(SU(n),sl_n)`, reduces it
  exactly on one smooth adjoint coefficient copy, transfers from `n=3` to `n=2`,
  and refuses an inadequate domain.
- **PDE-first non-Abelian bench:** the [matrix coefficient closure](benchmarks/pde-first-matrix-lie-reconstruction.md)
  reconstructs `sl_3(C)` or `sl_2(C)` from unlabeled coefficient seeds, recovers
  the forward exchange-paired witness, refuses a proper subalgebra, and leaves the
  global group unresolved.
- **Symbol-covariance bench:** the [pairing-dual construction](benchmarks/matrix-symbol-covariance-casimir.md)
  generates covariance vector fields and the coefficient eigenvalue instead of
  accepting them, transfers from rank three to rank two, and refuses a
  noninvariant principal pairing.
- **Adjoint-semigroup bench:** the [compact analytic promotion](benchmarks/matrix-adjoint-semigroup-global.md)
  constructs the compact real form, identifies the observable-effective carrier
  `PSU(n)`, and evaluates one adjoint heat block; incompatible involution and
  inadequate domain data refuse only this promotion.
- **Relation-construction benches:** the [natural-tensor chain](structured-seed-compression.md)
  constructs lazy quotient stabilizers, while the [coupled-carrier transfer](coupled-carrier-covariance.md)
  constructs metric/link covariance actions and exact principal-symbol projectors
  in ranks two and three. Its full-operator continuation derives scalar and
  two-sector transport without changing the defect compiler; the general finite
  commuting algebra is additionally exposed as a direct bounded operation.
- **Checks:** common-schema tests, exact coincidence, controlled truncation,
  isotropy refusal, retained route-specific detail, and legacy regression suite.
- **Boundary:** automatic probing is limited to a three-dimensional positive
  quadratic family, a constant-field Pauli family on Euclidean space or magnetic
  `T^2 x R`, the `SU(2)/SU(3)` complexified-adjoint transition grammar, finite
  natural tensors, and finite exact metric/Hermitian links. Other problem grammars
  still require a backend name; variable bundle fields, full
  regular-representation synthesis, arbitrary polynomial-jet stabilizers, and
  analytic promotion beyond the one adjoint-visible coefficient block are not
  integrated.
- **Edges:** `S4 -> S5` supplies reproducible evidence that several different
  calculi share the same capability-bearing result type.

## S5 — Bounded capability verdict (`supported conditional verdict`)

- **Question:** Does the program provide computational and human leverage beyond
  ordinary component-wise analysis?
- **Input:** `S3` comparison law and `S4` executable evidence.
- **Construction:** compare whole routes on fixed observables; separate eliminated
  work, compressed work, relocated work, and unpaid analytic debt.
- **Supported verdict:** within bounded structured classes, algebraic,
  representation, cyclic, and orbit constructions can remove invisible sectors,
  replace large component systems by generative recurrences or quotient PDEs, and
  select or refuse routes reproducibly.
- **Negative verdict:** no universal group discovery, exact solvability, nonlinear
  closure, or model-independent route dominance follows.
- **Evidence:** oscillator and interbasis cross-probes, cyclic no-gain/control,
  Coulomb closure, fixed-accuracy boundary comparison, axial/warped quotient PDEs,
  backend-free quadratic selection, the bilateral Pauli channel bridge and its
  topology/domain/heat-density promotion, and the `SU(3)` exchange-paired
  multiplicity decision together with its PDE-first effective-algebra recovery;
  finite split coefficient algebras add exact joint projectors and polynomial
  synthesis without eigenvectors.
- **Boundary:** analytical completion is still local to particular theorem
  contracts; the strongest open debts are noncommutative isotypic/multiplicity
  construction, arbitrary jets, variable bundles, and cross-route human-cost
  normalization.

## Evidence ledger

The former fine-grained node IDs are retired as graph vertices. They remain aliases
for provenance so older notes and benchmark discussions can be interpreted.

| Retired IDs | New owner | Role/status retained |
| --- | --- | --- |
| `M0,Q0` | `S0` | supported material and inverse semantics |
| `L0,P0,Z0,K0` | `S1` | supported operator, symbol, PDE, and cyclic contracts |
| `R0,O0,R1,H0,J0,I0` | `S2` | representation/bundle contracts; rank-one developing and family inverse specified |
| `D0,C1,X0` | `S3` | witness/complexity contract; bounded refusal absorbed into every backend |
| `L1,B0,O1,H1,P1` | `S4` evidence | supported regressions, not spine nodes |
| `O2` | `S2/S4/S5` evidence | executable `SU(3)` outer-multiplicity transition and `SU(2)` control |
| `O3` | `S2/S3/S4` evidence | exact multiplicity-valued order-two PDE action on an adjoint coefficient core |
| `O4` | `S1/S3/S4` evidence | unlabeled matrix coefficients reconstruct the effective `sl_2/sl_3` algebra and visible witness |
| `O5` | `S1/S3/S4` evidence | invariant principal pairing generates covariance derivations and the adjoint-linear second-order eigenvalue |
| `O6` | `S1/S3/S4/S5` evidence | compact real form and domain contracts promote one adjoint-visible coefficient block to a heat-semigroup witness, modulo the center |
| `P2,P3` | `S2` evidence/frontier | mode-bundle contract supported; spin-texture analytic contract open |
| `Z1,Z2,Z3,Z4` | `S1/S4` evidence | supported bounded centralizer and Coulomb constructions |
| `K1,D1,D2` | `S4` evidence | executable cyclic tool, conditional gain, and finite-model boundary |
| `D3,D4,D5` | `S4/S5` evidence | exact route selection, polynomial closure, and interbasis equality |
| `D6,D7,D8,D9` | `S4/S5` evidence | boundary, accuracy, quotient-PDE, and stratified-domain use |
| `P4` | `S1/S2/S4` evidence | executable bilateral Pauli channel bridge |
| `P5` | `S3/S4/S5` evidence | torus topology, direct-integral measure, degeneracy, heat density, and global refusals |
| `C0` | `S5` | replaced by the bounded conditional verdict above |

This consolidation removes automatic edges from one successful example to another.
A new benchmark rejoins the graph only by changing a node contract, capability
verdict, or failure boundary.

## Resolved bridges

### F1 — Bundle-valued executable transfer

- **Upstream:** `S2` spinor/projector-bundle contract and `S4` envelope.
- **Question:** Can a spinor or tensor reduction expose fiber isotropy, matrix-valued
  reduced dynamics, recovery, residuals, and cost through `reduction-witness/v1`?
- **Invariant target:** one spin-resolved spectral or propagation observable.
- **Success:** transfer plus refusal through the same public interface, without
  scalarizing the fiber.
- **Downstream effect:** tests whether the current witness is genuinely general or
  must be reconstructed.
- **Verdict:** passed for the constant-curvature Pauli channel observable. The
  common witness retained the matrix grading, fiber isotropy, projectors, odd
  Clifford factor, graded closure, analysis/synthesis grammar, exact residuals,
  cost, charge-sign transfer, and refusal. This does not cover variable bundles or
  global analytic completeness.

### F2 — Analytical completion

- **Upstream:** formal/exact algebraic witnesses from `S1`--`S3`.
- **Question:** Which domain, self-adjointness, completeness, convergence, and
  continuum-error theorem contracts promote them to controlled analytic tools?
- **Success:** one nontrivial backend gains a checked analytic error/completeness
  contract reusable by `S5`.
- **Verdict:** passed for the Pauli heat trace per unit length on magnetic
  `T^2 x R`. Integral flux constructs the line bundle, finite Heisenberg
  multiplicity, unitary Landau/Fourier carrier, and exact heat formula; nonintegral
  flux and the wrong domain refuse only the global promotion. The completeness and
  self-adjointness facts remain explicit imported theorem contracts.

### F3 — Non-Abelian multiplicity execution

- **Upstream:** `S2` outer-multiplicity calculus.
- **Question:** Can multiplicity-valued reduced maps be constructed and used without
  weight-by-weight enumeration?
- **Success:** one executable non-Abelian transfer changes an observable or route
  decision, rather than merely reproducing branching labels.
- **Verdict:** passed on the complexified adjoint. Matrix multiplication constructs
  the exchange-odd bracket and exchange-even traceless Jordan maps. The `SU(3)`
  exchange-paired observable sees both channels and rejects either scalarized
  route; polarized Cayley--Hamilton reduces the unchanged `SU(2)` control to one.
  Completeness still consumes the bounded tensor-product theorem contract.

### F4 — Multiplicity-valued PDE execution

- **Upstream:** `S2` operator filtration, the F3 natural-intertwiner constructor,
  and the `S3/S4` witness interface.
- **Question:** Can the two outer-multiplicity channels be reconstructed as reduced
  maps of an actual order-two differential operator, with core/domain and
  analysis/synthesis rather than only a finite transition block?
- **Invariant target:** one resolvent, transition, or heat observable for
  `T_ell=M_(f_ell)(1+Delta_G)` on a declared finite Peter--Weyl window or a
  controlled tail.
- **Success:** equality on the smooth core, observable recovery, and a whole-route
  cost comparison against a component realization.
- **Verdict:** passed on one adjoint matrix-coefficient copy using the
  bundle-valued natural operator `T_X u=a[q_X,(1+Delta)u]+b{q_X,(1+Delta)u}_0`.
  The Casimir contract gives `Delta q_Y=n q_Y`, forcing `A T_X S=R_X` exactly on
  the smooth core. `SU(3)` retains two observable-visible channels, `SU(2)` one,
  and an `L^2`-only domain is refused. Full Peter--Weyl synthesis remains outside
  this bounded verdict.

### F5 — PDE-first non-Abelian reconstruction

- **Upstream:** the F4 differential family and the bounded covariance/closure
  inverse in `S1`.
- **Question:** without an `SU(n)` label, can the matrix PDE coefficients generate
  the effective conjugation algebra, its adjoint carrier, and the same multiplicity
  maps?
- **Invariant target:** the exchange-paired PDE amplitude already recovered in F4.
- **Success:** an independent PDE-first probe reconstructs the effective
  `sl_2/sl_3` Lie algebra and visible reduced witness, coincides with the
  representation-first result, and retains center/global-integration ambiguity.
- **Verdict:** passed inside the rational rank-two/rank-three matrix-coefficient
  grammar. Four unlabeled rank-three seeds close from dimension four to eight,
  certify the full traceless algebra, and recover the forward `(5,1)` observable;
  the rank-two transfer recovers one channel, and a nonspanning family is refused.
  The result determines only the effective complex infinitesimal algebra. The
  common scalar second-order action on the coefficient span remains supplied.

### F6 — Symbol-fiber-to-covariance reconstruction

- **Upstream:** the bounded `S1` symbol/stabilizer search and the F5 matrix closure.
- **Question:** can invariant matrix-symbol data construct the first-order
  covariance generators and common coefficient eigenmodule that F5 accepts as
  input, without expanding a coordinate jet array?
- **Invariant target:** the same exchange-paired PDE amplitude, with the F5
  effective-algebra result used only as an independent comparison target.
- **Success:** a bounded symbol input with no group, algebra, generator, or
  coefficient-eigenvalue label produces covariance arrows and a scalar
  pairing-dual square, then composes with F5; a broken pairing gives its first
  nonzero covariance residual.
- **Verdict:** passed on the exact polynomial core `Sym(sl_n^*)`, for `n=2,3`.
  Inner derivations are generated from coefficient closure, their Lie law and
  trace-pairing covariance are certified, and the pairing-dual square derives
  eigenvalue three or two. The unchanged observables coincide with F4/F5. A
  coordinate-identity pairing is refused at its first covariance residual. No
  Hilbert closure or arbitrary polynomial-jet stabilizer is claimed.

### F7 — Observable-relative analytic and global promotion

- **Upstream:** the F6 polynomial differential core and the F4 compact analytic
  realization.
- **Question:** can involution, positivity, and domain data select a compact real
  realization of the generated algebra and promote its visible coefficient module
  to a closed `L^2` semigroup witness?
- **Invariant target:** the adjoint-coefficient semigroup matrix element
  `O_Z(exp(-t Delta)q_Y)`, together with the exchange-paired tensor amplitude.
- **Success:** construct the compact real form and normalized measure/domain up to
  the unavoidable central quotient, prove the visible semigroup formula from the
  generated eigenvalue, and show that `SU(n)` versus `PSU(n)` ambiguity is invisible
  to the named adjoint observable; refuse nonpositive or incompatible involution
  data.
- **Verdict:** passed for the adjoint-visible coefficient block in ranks two and
  three. Conjugate transpose selects `su(n)` with positive form
  `-2 tr(XY)`; normalized Haar measure and the imported compact elliptic theorem
  contract give the `H^2` self-adjoint realization, and F6's generated eigenvalue
  yields `exp(-t Delta)q_Y=exp(-nt)q_Y`. Because `q_Y(zg)=q_Y(g)`, the observable
  identifies the effective carrier as `PSU(n)` and cannot distinguish it from
  `SU(n)`. Wrong involution or an `L^2`-only domain is refused while the local F6
  result remains valid. No full heat trace, full spectrum, non-adjoint
  representation, or unique global integration is claimed.

## Generative construction disposition

### G0 — Seed--defect construction layer (`supported bounded`)

- **Upstream:** `S0` typed semantics, the bounded stabilizer operations in `S1`,
  and the F6/F7 covariance witnesses.
- **Tension:** heterogeneous routes share a `ReductionWitness`, but the executable
  router still selects prewritten schemas and therefore does not generate a route
  from common primitives.
- **Alternatives tested:** one universal defect generator versus plural natural
  seed functors followed by one defect compiler.
- **Probe result:** [the retrospective construction probe](defect-kernel-construction.md)
  factors centralizer, boundary, and covariance routes through common residual,
  kernel, quotient, closure, and refusal operations. It also shows that their
  Killing, affine-isometry, and inner-derivation candidate modules have different
  origins. The universal-seed alternative is rejected for this evidence domain;
  the two-stage alternative is frozen as `C_G0_v1`.
- **Invariant target:** a constructed effective infinitesimal action that composes
  with the existing observable witness.
- **Current evidence:** `E-G0-02` implements one exact kernel-selection compiler
  unchanged across the quadratic-centralizer, boundary, and covariance
  regressions, with rank ledgers and bounded refusal. This is regression evidence,
  not held-out transfer. `E-G0-03` adds exact ineffective-ideal quotient, induced
  bracket, closure, and non-ideal/non-closed refusal when the seed supplies a
  finite ambient bracket.
- **Transfer disposition:** `E-G0-04` passes the separately frozen
  [isotropic-elasticity natural-tensor transfer](benchmarks/isotropic-elasticity-natural-tensor.md)
  without changing `C_G0_v1`. Nine canonical endomorphisms reduce to a closed
  three-generator stabilizer; an axis tensor reduces it to one; a small budget
  returns unresolved. Two exact projectors recover the propagator observable to
  `4.996e-16` against a dense eigensolve.
- **Leverage disposition:** conditional under the declared arithmetic proxy, with
  break-even at 103 wave-vector queries; runtime dominance is unresolved.
- **Boundary:** exact finite linearized grammars. Factorization, cyclic closure,
  arbitrary jets, nonlinear symmetries, and analytic integration are not claimed
  as instances.

Former `F8` is resolved as the held-out transfer under `C_G0_v1`; its bounded
result is evidence for G0, not a permanent elasticity branch or permission for
case-by-case router growth.

### G1 — Structured seed compression before raw tensor enumeration (`supported bounded`)

- **Upstream:** the bounded G0 disposition and its elasticity cost audit.
- **Tension:** `End(V)` is canonical and answer-independent, but has dimension
  `d^2`; raw rank-four tensor defects expose up to `d^4` target coordinates before
  symmetry is used. The compiler is general in semantics but not yet scalable in
  candidate origin.
- **Question:** can tensor permutation type, contractions, grading, and natural
  operations construct smaller complete candidate and residual modules before
  row reduction, without supplying the expected stabilizer?
- **Invariant target:** the same stabilizer action and observable witness produced
  by G0.
- **Falsifier:** compression requires the expected algebra/basis, loses an admitted
  stabilizer direction, or relocates enumeration into an opaque decomposition
  oracle.
- **Probe result:** [the frozen G1 construction](structured-seed-compression.md)
  shows that metric-kernel seed compression and permutation-orbit codomain
  compression are complementary and compose. In dimension three they lower the
  candidate/residual dimensions from `9/(9+81)` to `3/21` while preserving the
  exact generated stabilizer span. The axis control still lowers dimension
  `3 -> 1`, and a non-orthonormal metric passes.
- **Leverage disposition:** the one-time arithmetic proxy falls `1638 -> 117` and
  repeated-query break-even `103 -> 8`; the observable and its `4.996e-16` error
  are unchanged. This is conditional proxy evidence, not measured runtime.
- **Boundary:** finite exact natural tensors. Arbitrary jets, nonlinear symmetry,
  indefinite metrics, general symmetry parsing, analytic integration, and
  universal tractability remain outside the bridge.

### G2 — Typed relation planner for seed and codomain construction (`supported bounded`)

- **Upstream:** the G0 defect compiler and bounded G1 structured functors.
- **Tension:** G1 removes component growth, but the adapter still chooses the
  metric-first seed and assigns known tensor symmetry tags. The computation is
  constructive inside each rule but route assembly is not yet generated.
- **Question:** can a finite typed relation graph derive all admitted exact seed
  and codomain reductions, their prerequisites, completeness certificates, and
  estimated costs, then select an order without a physics-kind case table?
- **Invariant target:** the same G1 stabilizer span, bracket, refusal semantics, and
  elasticity observable; no new physical example may modify the planner.
- **Alternatives:** a declarative natural-operation planner versus keeping plural
  hand-selected adapters behind the common defect compiler.
- **Falsifier:** the planner needs an expected algebra/basis, silently assumes a
  tensor identity not present in the input, or merely relocates exhaustive route
  enumeration into an opaque registry.
- **Probe result:** [the typed relation planner](typed-relation-planner.md) replaces
  adapter route assembly by a deterministic five-rule dependency chain. Anonymous
  tensors reproduce the 21-coordinate quotient; missing, ambiguous, and
  uncertified relations produce typed route rejection. All G1 outputs remain
  unchanged.
- **Cost disposition:** semantic/internal and human construction are supported.
  Computational leverage is restricted: the compiler proxy remains 117, but the
  generic orbit constructor performs an upper-bound 648 permutation checks, giving
  an expanded structured proxy 765 versus raw 1872 and break-even 48 rather than 8.
- **Boundary:** finite linear exact relations. Search optimality, arbitrary Young
  symmetries, jets, nonlinear closure, and analytic integration are not claimed.

### G3 — Lazy compositional tensor quotients without raw orbit scans (`supported bounded`)

- **Upstream:** G2's typed relation DAG and explicit orbit-planning cost.
- **Tension:** the planner removes physics-kind branching but discovers orbit
  representatives by scanning `d^r` indices. Generality has relocated part of the
  exhaustive computation rather than eliminating it. Its certification mode also
  materializes raw and structured routes before budgeted selection.
- **Question:** can symmetric-slot, antisymmetric-slot, block-exchange, and trace
  relations compose into canonical quotient-coordinate constructors whose work is
  proportional to retained coordinates rather than the raw tensor space, with
  symbolic budget admission before any defect block is materialized?
- **Invariant target:** the same 6-coordinate dyad and 21-coordinate elasticity
  targets, exact stabilizer span, bracket, refusal, and observable.
- **Alternatives:** arbitrary permutation-group canonicalization versus a typed
  quotient-expression calculus with compositional completeness certificates.
- **Falsifier:** a constructor embeds elasticity or another expected answer,
  enumerates all raw indices internally, or cannot reproduce the generic orbit
  route exactly on the frozen relation signatures.
- **Probe result:** [the G3 constructor](lazy-compositional-tensor-quotients.md)
  emits the 6/21 coordinates from nested symmetric powers, admits budgets before
  materialization, and executes only the selected route unless an audit is
  requested. The explicit audit exactly matches the G2 orbit set and raw
  stabilizer span.
- **Cost disposition:** operational planning falls `648 -> 21`; selected
  planning-plus-compiler cost is 138 and the conditional break-even is 9 queries.
  The 648 orbit comparisons remain an audit cost, not an operational cost.
- **Boundary:** finite tensor quotient expressions. Mixed variance, arbitrary
  Young-projector optimization, spinors, jets, and nonlinear closure remain open.

### G4 — Coupled-carrier covariance without a supplied group (`supported bounded`)

- **Upstream:** G0's defect/quotient/closure compiler and G3's admission-before-
  materialization policy.
- **Tension:** natural tensors construct an action on one carrier, whereas spinor
  PDE symbols couple a vector carrier to a noncommutative fiber. The current Pauli
  route constructs channels but does not test whether the common defect compiler
  can generate the coupled infinitesimal action itself.
- **Question:** from a metric `g` and a certified link
  `gamma:V -> End(S)`, can the machine construct pairs `(A,B)` satisfying
  `A^T g+gA=0` and `[B,gamma(v)]=gamma(Av)`, quotient ineffective fiber phases,
  certify bracket closure, and use the result to decompose the linked PDE symbol?
- **Alternatives:** plural relation-specific seed functors feeding the common
  compiler versus a new case-specific spin router. A universal seed enumerator is
  not revived.
- **Falsifier:** the expected rotation/spin algebra or a preferred generator basis
  enters the input; covariance is checked only after a supplied answer; the
  ineffective commutant is not quotiented; or a broken link is promoted.
- **Probe result:** [the coupled-carrier constructor](coupled-carrier-covariance.md)
  uses one generic metric/link relation schema in ranks two and three. It constructs
  effective dimensions one and three, discovers and quotients one ineffective
  fiber phase, certifies closure, refuses a broken Clifford relation and an
  insufficient budget before materialization, and returns exact symbol projectors.
- **Boundary:** finite exact real base carriers and Gaussian-rational Hermitian
  fibers and principal symbols. This is G0 cross-family transfer, not yet full
  differential-operator covariance. Global spin integration, curved domains,
  variable coefficients, continuous spectra, and nonlinear systems remain open.

### G5 — Promote constructed symbol covariance to a full PDE witness (`supported bounded`)

- **Upstream:** G4's generated effective base/fiber action and the existing
  bilateral Pauli lower-term/domain witness.
- **Tension:** principal-symbol projectors are exact, but a symmetry of the symbol
  need not preserve subprincipal terms, curvature, the operator domain, boundary
  traces, or the named time/heat observable.
- **Question:** can the generated G4 action, without replacement by a named spin
  group, be lifted through every lower-order defect of a second-order spinor PDE
  and produce analysis/synthesis maps for the same Pauli channel observable?
- **Alternatives:** descend the generated action through ordered symbol layers and
  domain defects versus retain G4 as a symbol-only classification result.
- **Falsifier:** the lift imports the Pauli grading or rotation generators that it
  is meant to derive, skips a lower-order/domain residual, or compares a different
  observable from the existing bilateral bench.
- **Probe result:** [the full-operator lift](full-operator-covariance-lift.md)
  applies curvature, first-order, and zeroth-order defect blocks to the generated
  G4 quotient. The unchanged Pauli input contracts `3 -> 1` at curvature and no
  further, remains closed, derives its grading from curvature and the Clifford
  link, and exactly matches the independent bilateral projector and channel list.
  The generic schema also returns the operator action without a Pauli observable.
  Charge reversal transfers; a transverse zeroth-order term kills the last
  generator; an unmatched half-space domain refuses promotion.
- **Boundary:** constant exact coupled Laplace-type coefficient packages on a
  dimension-matched boundaryless Schwartz common-core theorem contract; observable
  recovery is tested only for Euclidean rank-three Pauli data. The successful
  first-order coefficients are zero. Global integration, self-adjoint completion,
  nonzero transport, and analytic completeness remain separate.

### G6 — Nonzero first-order transport without a case-specific symmetry rule (`supported bounded`)

- **Upstream:** G5's ordered coefficient compiler and exact Pauli channel witness.
- **Tension:** G5 materializes and checks a twelve-coordinate first-order defect
  block, but its successful Pauli fixtures have `C_i=0`; this does not test whether
  a nonzero lower-order covector can survive the generated action or be consumed
  without component diagonalization.
- **Question:** can a nonzero scalar Hermitian coefficient aligned with the
  curvature-derived kernel be selected by the unchanged defect compiler and
  carried to an exact shifted longitudinal channel rule?
- **Alternatives:** extend only the observable use grammar after the generic
  compiler selects the coefficient, versus require a new route-specific symmetry
  construction.
- **Falsifier:** the fixture supplies the curvature axis, surviving generator,
  grading, or shifted spectrum; the compiler is amended with an axial special
  case; a transverse coefficient is silently discarded; or recovery omits the
  original longitudinal momentum observable.
- **Probe result:** [the nonzero transport continuation](nonzero-first-order-transport.md)
  leaves the generic defect compiler unchanged. With `F_12=3` and `C_3=2I`, it
  retains the G5 `3 -> 1` action, derives the axis and `mu=2`, and returns exact
  polynomial and completed-square channels. Rotating the curvature plane and
  coefficient transfers unchanged. A transverse scalar coefficient kills the
  action at `first-order-covariance`. An axial matrix coefficient preserves the
  generic action but refuses scalar recovery without erasing that partial witness.
- **Boundary:** constant scalar longitudinal drift parallel to a rational-norm
  curvature axis in Euclidean rank three. Matrix-valued transport, variable
  connections, boundaries, and curved geometry remain outside this disposition.

### G7 — Observable-relative coefficient algebra for matrix-valued transport (`supported bounded`)

- **Upstream:** G6's matrix-valued axial fixture, whose generated operator action
  is exact while the scalar observable consumer refuses.
- **Tension:** operator covariance alone does not decompose a matrix-valued
  longitudinal polynomial, but adding a Pauli-component diagonalizer would return
  to case-specific enumeration.
- **Question:** can the machine construct the finite star-algebra generated by the
  curvature grading, zeroth-order term, and surviving longitudinal coefficient,
  then derive common projectors or a noncommutation obstruction and recover the
  visible channel polynomial?
- **Alternatives:** an observable-relative coefficient-algebra/minimal-polynomial
  constructor versus separate spin-matrix formulas in each PDE adapter.
- **Falsifier:** the input supplies eigenvectors, a preferred spin component, or
  the expected channel roots; the constructor exhaustively enumerates matrix
  entries instead of using the generated algebra; noncommuting coefficients are
  silently diagonalized; or recovery omits the original momentum polynomial.
- **Probe result:** [the matrix transport algebra](matrix-valued-transport-algebra.md)
  reconstructs the axial coefficient, constructs the two-dimensional star-algebra
  `span{I,Sigma_F}`, obtains its sector roots from restricted traces, derives the
  minimal polynomial and primitive idempotents, and synthesizes the visible
  momentum polynomials. Rotation preserves the abstract result while rotating its
  concrete projectors. Equal roots regress to G6; noncommutation refuses.
- **Boundary:** one exact Hermitian involution with two nonzero sectors and a
  Hermitian coefficient scalar on each sector, over Gaussian rationals. This is
  not yet a constructor for arbitrary finite coefficient algebras or unresolved
  sector multiplicity.

### G8 — Primitive idempotents for finite semisimple coefficient algebras (`supported bounded`)

- **Upstream:** G7 proves that the useful reduction object is the coefficient
  algebra and its idempotents, not a catalogue of Pauli components.
- **Tension:** G7 obtains completeness from a supplied two-sector involution.
  General bundle-valued PDEs may expose several commuting coefficients, more than
  two sectors, and multiplicities not resolved by one grading.
- **Question:** can the machine close a finite commutative Hermitian coefficient
  algebra from surviving PDE coefficients, construct minimal polynomials and
  primitive idempotents by exact polynomial arithmetic, and synthesize channel
  blocks without enumerating eigenvectors or presupposing a group?
- **Alternatives:** square-free factorization plus Chinese-remainder idempotents
  over the declared exact field versus a generic simultaneous eigensolver; only
  the former preserves symbolic and human auditability.
- **Falsifier:** the constructor assumes sector roots, silently extends the exact
  field, expands a full component eigenbasis, claims primitive sectors when the
  algebra leaves multiplicity unresolved, or drops the reconstruction map.
- **Probe result:** [the finite split algebra](finite-semisimple-coefficient-algebra.md)
  derives minimal polynomials from exact Krylov dependence, constructs Lagrange
  root projectors, and intersects them into joint sectors. Two individually
  degenerate generators yield three primitive algebra sectors and exact polynomial
  synthesis. Rational rotation and generator reversal preserve the result;
  noncommutation, field extension, budget, and malformed-polynomial failures are
  distinct. G7 now consumes this general owner.
- **Boundary:** finite-dimensional constant coefficient algebras over a declared
  exact field whose generator minimal polynomials split rationally within budget.
  Repeated eigenspaces are retained with carrier multiplicity. Field extensions,
  noncommutative algebras, radicals, variable connections, path ordering, domains,
  and analytic completeness remain parked.

### G9 — Noncommutative coefficient algebras and representation multiplicity (`supported bounded`)

- **Upstream:** G8 constructs primitive projectors only after all coefficient
  generators commute. Its explicit carrier multiplicities show exactly where a
  commutative sector calculus stops.
- **Tension:** matrix-valued PDEs and represented symmetry algebras commonly
  generate noncommutative blocks. Diagonalizing one coefficient cannot distinguish
  irreducible type from repeated copies, while a supplied group label would defeat
  the PDE-first direction.
- **Question:** can the machine close a finite exact star-algebra, construct its
  center and commutant, apply G8 to primitive central idempotents, and recover
  isotypic blocks and multiplicity spaces by a double-centralizer certificate?
- **Alternatives:** center/commutant kernels and Wedderburn-type block witnesses
  versus component decomposition after guessing a representation or group.
- **Falsifier:** the input supplies irreducible labels or a preferred block basis;
  central projectors fail exact reconstruction; algebra and commutant dimensions
  violate the double-centralizer relation; or multiplicity is inferred from
  eigenvalue degeneracy alone.
- **Probe result:** [the finite represented star algebra](finite-represented-star-algebra.md)
  constructs Hermitian commutant and bicommutant kernels, intersects them for the
  center, and delegates primitive central splitting to G8. Repeated `M_2` gives
  algebra/commutant dimensions `4,4` and multiplicity two. A scalar direct summand
  yields two isotypic blocks; rational conjugation preserves their signatures, and
  a complex Pauli pair verifies the Gaussian-rational spinor branch.
- **Boundary:** finite Gaussian-rational Hermitian generator presentations with a
  rationally split center and explicit dense-elimination budget. Recognition of
  global groups, explicit simple-block models, infinite-dimensional
  representations, variable bundles, domains, and analytic spectral completeness
  remain separate.

### G10 — Minimal simple-block realization and PDE leverage (`supported bounded`)

- **Upstream:** G9 certifies `P_r C^q ~= C^(d_r) tensor C^(m_r)` and constructs the
  isotypic projectors, but its matrices remain `q x q`.
- **Tension:** a multiplicity integer is representation-theoretic compression, yet
  it does not reduce a differential computation until an exact analysis/synthesis
  route removes the repeated factor.
- **Question:** can the machine construct a primitive left ideal, matrix units, or
  an equivalent basis-free `d_r`-dimensional action from each simple algebra block,
  then reduce and reconstruct a matrix PDE observable at lower whole-route cost?
- **Alternatives:** exact primitive-idempotent/left-ideal construction versus a
  multiplication-table spectral calculus that never chooses carrier coordinates.
- **Falsifier:** a preferred tensor basis or irreducible label enters the input;
  construction costs exceed the unreduced route for the declared family; the
  reduced action fails exact synthesis; or only dimensions, not a reusable PDE
  operation, are returned.
- **Probe result:** [the simple-block PDE reduction](simple-block-pde-reduction.md)
  constructs a primitive commutant projector, derives an exact rank-two embedding,
  and solves generator intertwining equations. The quadratic symbol reduces
  `4 -> 2`; its determinant reconstructs as the square of the reduced determinant
  before and after rational conjugation. The declared proxy breaks even at 62
  queries, so only amortized—not single-query or runtime—leverage is supported.
- **Boundary:** one full finite rationally split isotypic block, a rational
  commutant splitter within budget, and constant compatible Hermitian differential
  coefficients. Field extensions, variable connections, domains, and analytic
  completeness remain parked.

## Active open bridge

### G11 — Variable coefficient star-algebra bundles and derivative coupling

- **Upstream:** G10 proves exact reduction when the algebra, primitive commutant
  projector, and embedding are constant over the differential base.
- **Tension:** for `B=B(x)`, differentiation gives
  `partial(B psi)=B partial(psi)+(partial B)psi`; algebraic block invariance alone
  therefore does not imply PDE decoupling.
- **Question:** can pointwise G9/G10 data construct the induced connection and a
  basis-independent leakage residual, composing with the existing mode-bundle
  calculus to distinguish exact from controlled adiabatic reduction?
- **Alternatives:** projector connection `P dP` with off-block leakage versus local
  diagonalization followed by untracked derivative terms.
- **Falsifier:** derivative coupling is omitted; gauge/frame changes alter the
  reported observable; an adiabatic estimate is presented as exact; or the
  construction loses the G10 constant-projector limit.
- **Next probe:** use a rationally parameterized rotating repeated-Pauli carrier.
  Construct `P(x)`, its connection, and `(I-P)dP`; recover zero leakage for constant
  rotation and nonzero controlled coupling for a varying rotation without changing
  the pointwise algebra constructor.
- **Boundary:** smooth finite-rank coefficient bundles with declared derivative and
  gap information. Singular crossings, domains, topology beyond one chart, and
  nonlinear feedback remain separate.

## Parked branches and re-entry conditions

- **More scalar axial domains:** re-enter only if a new stratum or boundary law
  breaks the current orbit witness.
- **Additional polynomial families:** re-enter only if a second nonlinear closure
  changes route choice or positivity requirements.
- **Arbitrary higher dimension:** re-enter when a dimension-dependent obstruction
  affects a current constructor.
- **Microlocal decomposition:** re-enter when the target observable is local in
  phase space and global reduction fails.
- **Nonlinear PDEs:** a separate program requiring invariant manifolds, fusion
  rules, normal forms, or controlled closure error; linear sector decomposition
  alone is insufficient.
- **Unique inverse-group recovery:** parked permanently unless additional global
  family, topology, and integration data are supplied.

## Stop rule

Stop a branch when its benchmark supports or rejects its bridge, when further
detail changes no observable or verdict, or when progress requires a new model
class. Promote only the compact witness, assumptions, costs, and failure boundary;
leave derivations and raw computation with their material owners.
