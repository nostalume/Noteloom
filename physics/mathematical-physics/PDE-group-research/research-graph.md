# Compact research graph

## Spine invariant

The graph preserves one semantic object: the requested observable of an operator
problem with its carrier, preparation, domain/boundary, accuracy, and resource
bound. It is organized by construction, not by special function, coordinates, or
group name.

```text
                         representation/action
                                 |
                                 v
S0 request semantics --> S2 realization -----------+
        |                                           |
        v                                           v
G0 seed--defect layer --> S1 constructors -------> S3 witness calculus
                                                     |
                                                     v
                                              S4 executable tool
                                                     |
                                                     v
                                              S5 bounded verdict
```

`S1` and `S2` are bilateral directions, not inverses. They coincide only when
they construct equivalent witnesses for the same observable.

## Node contract

```text
question -> typed input -> construction -> witness/check -> compact output
         -> validity/failure boundary -> named downstream edge
```

Detailed construction lives in [nodes](nodes/README.md); evidence lives in
[benchmarks](benchmarks/README.md); executable certificates live in
[computation](computation/README.md). This graph owns only dependency and current
disposition.

## S0 — Typed problem and inverse semantics (`supported`)

- **Input:** operator or representation, carrier, preparation, domain/boundary,
  observable, tolerance, and resource bound.
- **Construction:** distinguish point symmetry, dynamical algebra, monodromy,
  differential-Galois data, and integration of a represented Lie algebra; retain
  non-unique inverse fibers.
- **Output:** `ReductionRequest`; a group name is optional output in the PDE-first
  direction.
- **Boundary:** a bare PDE and a bare group do not determine each other.
- **Edge:** shared types and observable to `S1`, `S2`, and `S3`.

## S1 — Operator-to-structure discovery (`supported bounded`)

- **Input:** symbols and lower coefficients, coefficient grammar, domain/boundary
  strata, search order, and budget.
- **Construction:** factor symbols; compute bounded filtered centralizers and
  operator-domain stabilizers; construct cyclic carriers; classify exact closure.
- **Output:** represented algebra, factor/commutant, quotient, complex, mode
  bundle, cyclic object, or typed obstruction.
- **Boundary:** completeness is relative to the grammar, order, domain, and budget.
- **Edge:** candidate plus exact residual certificates to `S3`; finite certified
  Lie closure may enter `S2`.

## S2 — Structure-to-differential realization (`supported contract`)

- **Input:** represented algebra/group action, carrier or bundle type, dynamics,
  and observable.
- **Construction:** derived actions, matrix coefficients, branching/multiplicity
  maps, enveloping-algebra operations, homogeneous complexes, and
  Clifford/projector-bundle extensions.
- **Output:** differential realization, selection graph, multiplicity block,
  recurrence, or bundle-valued reduced operator.
- **Boundary:** representation constrains channels but does not supply dynamics;
  analytic domains and global integration are separate obligations.
- **Edge:** realized candidate to `S3`.

## S3 — Witness and decision calculus (`supported`)

- **Construction:** construct analysis `A`, synthesis `S`, reduced dynamics
  `D_red`, visible projector `Q_vis`, and residuals

  ```text
  AD - D_red A,   DS - S D_red,   SA - Q_vis,   O - O_red A.
  ```

- **Output:** `exact`, `controlled`, `formal`, `obstructed`, or
  `unresolved within budget`, plus route decision and limitations.
- **Decision law:** compare construction, solution, and recovery costs only for
  the same observable and accuracy.
- **Boundary:** formal closure is neither analytic completeness nor a cost gain.
- **Edge:** certified witness to `S4` and bounded disposition to `S5`.

## S4 — Executable workbench (`supported bounded router`)

- **Input:** an admitted `ProblemDocument` or named direct backend.
- **Construction:** decode once, route by schema, preserve route-specific detail,
  project to `reduction-witness/v1` or `reduction-decision/v1`.
- **Direct backends:** cyclic, factor/centralizer, and stratified orbit reduction.
- **Generated families:** quadratic Schrödinger, local/global Pauli, adjoint
  transition/PDE/inverse/covariance/semigroup, natural tensors, coupled carriers,
  and coupled full operators.
- **Checks:** exact coincidence, controlled error, domain/isotropy refusal, schema
  contract, and legacy regression.
- **Boundary:** finite structured grammars and dense exact low-rank carriers; no
  generic stabilizer, arbitrary jet, nonlinear closure, or automatic global
  integration.
- **Owner:** [computation workbench](computation/README.md).

## S5 — Bounded capability verdict (`supported conditional`)

- **Supported:** within declared structured classes, algebraic, representation,
  cyclic, and quotient constructions remove invisible sectors, replace component
  catalogues by generators/recurrences, and select or refuse routes reproducibly.
- **Human leverage:** kernels, projectors, quotient sectors, relative polynomial
  recurrences, and pulled-back effects are retained instead of exhaustive
  component expansion.
- **Negative:** no universal group discovery, solvability, nonlinear closure,
  analytical completeness, or route dominance follows.
- **Boundary:** every leverage claim is indexed by model, preparation, observable,
  accuracy, construction cost, recovery cost, and reuse count.

## Resolved bilateral bridges

| Bridge | Construction and bounded disposition | Owners/evidence |
| --- | --- | --- |
| F1 bundle-valued transfer | homogeneous-bundle multiplicities replace scalar-only realization | [bundle calculus](nodes/homogeneous-bundle-calculus.md), [p-form bench](benchmarks/p-form-sphere.md) |
| F2 analytical completion | domain/topology/measure data promote selected formal channels only | [Pauli global bench](benchmarks/pauli-global-analytic.md), [source contracts](sources.md) |
| F3 non-Abelian multiplicity | bracket/Jordan maps construct two visible SU(3) channels and one SU(2) control | [SU tensor bench](benchmarks/tensor-operator-su3.md) |
| F4 multiplicity-valued PDE | adjoint intertwiners lift to one exact compact order-two block | [adjoint PDE bench](benchmarks/su-adjoint-multiplicity-pde.md) |
| F5 PDE-first reconstruction | unlabeled coefficient seeds close to effective `sl_2/sl_3` or refuse | [matrix inverse bench](benchmarks/pde-first-matrix-lie-reconstruction.md) |
| F6 symbol to covariance | invariant pairing generates derivations and the Casimir action | [symbol bench](benchmarks/matrix-symbol-covariance-casimir.md) |
| F7 observable-relative globality | compact real form and domain promote one visible heat block, retaining center ambiguity | [semigroup bench](benchmarks/matrix-adjoint-semigroup-global.md) |

## Generative construction ledger

The G-series is a dependency chain, not an invitation to append examples. Each
resolved row links its semantic owner; benchmark and executable detail stay there.

| ID | Constructed bridge | Disposition / decisive boundary | Owner |
| --- | --- | --- | --- |
| G0 | seed -> defect kernel -> ineffective quotient -> closure | exact on admitted finite modules; seed origin still privileged | [seed--defect](nodes/defect-kernel-construction.md) |
| G1 | natural candidate compression before elimination | exact span preserved; proxy `1638 -> 117` | [structured seeds](nodes/structured-seed-compression.md) |
| G2 | capability-derived relation plan | typed missing/ambiguous relation refusal; audit exposes orbit scan | [relation planner](nodes/typed-relation-planner.md) |
| G3 | lazy nested symmetric-power quotient | 21 direct emits; selected proxy 138; raw scan only for audit | [lazy quotients](nodes/lazy-compositional-tensor-quotients.md) |
| G4 | coupled base/fiber covariance without group input | closed effective actions and exact linked-symbol projectors | [coupled covariance](nodes/coupled-carrier-covariance.md) |
| G5 | generated action lifted through full operator | curvature/lower-term defects reduce `3 -> 1`; domain and bad-term refusals | [operator lift](nodes/full-operator-covariance-lift.md) |
| G6 | nonzero scalar first-order transport | aligned/rotated channels exact; transverse transport kills action | [first-order transport](nodes/nonzero-first-order-transport.md) |
| G7 | two-sector matrix coefficient algebra | traces/minimal polynomial construct projectors; noncommutation refuses | [matrix transport](nodes/matrix-valued-transport-algebra.md) |
| G8 | finite commuting semisimple algebra | exact joint idempotents, multiplicities, and polynomial synthesis | [finite coefficient algebra](nodes/finite-semisimple-coefficient-algebra.md) |
| G9 | finite noncommutative represented star algebra | center and double centralizer separate irreducible size/multiplicity | [represented star algebra](nodes/finite-represented-star-algebra.md) |
| G10 | primitive simple-block realization | determinant recovers with multiplicity; proxy breaks even after 62 queries | [simple-block reduction](nodes/simple-block-pde-reduction.md) |
| G11 | moving-frame projector differential jet | connection and first/second leakage reconstruct product rule | [variable projector](nodes/variable-projector-differential-jet.md) |
| G12 | one-channel analytic leakage promotion | exact transition plus time/gap bound; closing gap refuses | [gap-aware bound](nodes/gap-aware-leakage-bound.md) |
| G13 | coherent full off-block propagation | frame-invariant finite-window map and bright/dark observable | [full-block propagation](nodes/full-block-finite-window-propagation.md) |
| G14 | coefficient-derived isolated projector jet | `P,P',P''`, gap, and horizontal transport without eigenvector matching | [coefficient jet](nodes/coefficient-derived-projector-jet.md) |
| G15 | common invariant off-block differential arrows | frame and coefficient routes meet at `QP'P, QP''P` | [projector-native route](nodes/projector-native-propagation.md) |
| G16 | same-observable complete-route adjudication | exact route has less semantic depth but loses sampled runtime comparison | [route leverage](nodes/complete-route-leverage.md) |
| G17 | preparation-reachable active carrier | all tested blocks reduce to 3; one-shot loses, 64-time reuse wins | [active subspace](nodes/prepared-observable-active-subspace.md) |
| G18 | coefficient-family reachable module | exact common closure and specialization; four-point construction wins, one-point loses | [family module](nodes/coefficient-family-reachable-module.md) |

## Evidence alias ledger

Retired fine-grained IDs remain provenance aliases, not live graph vertices.

| Retired IDs | Current owner | Retained role |
| --- | --- | --- |
| `M0,Q0` | S0 | material and inverse semantics |
| `L0,P0,Z0,K0` | S1 | operator, symbol, PDE, and cyclic contracts |
| `R0,O0,R1,H0,J0,I0` | S2 | representation and bundle contracts |
| `D0,C1,X0` | S3 | witness, cost, and refusal contract |
| `L1,B0,O1,H1,P1,O2--O6` | S4 evidence | scalar, bundle, multiplicity, inverse, covariance, and global regressions |
| `P2--P5,Z1--Z4,K1,D1--D9` | S4/S5 evidence | mode, centralizer, cyclic, route, quotient, and Pauli evidence |
| `C0` | S5 | superseded by the bounded verdict |

## Active open bridge: G19 differential-operator module lift

- **Upstream:** G18 constructs an internal module for all finite symbol
  specializations but evaluates only finite momentum blocks.
- **Question:** for `D=sum_alpha L_alpha tensor H_alpha`, does a common invariant
  module of the matrix coefficients construct an invariant function/bundle
  module before Fourier sampling or coordinate separation?
- **Required output:** PDE-level analysis/synthesis intertwiner, coefficient-basis
  covariance, same-observable recovery, domain obligation, and cost ledger.
- **Alternatives:** a coordinate-independent tensor-module lift versus a hidden
  reliance on one scalar differential basis or Fourier window.
- **Falsifier:** coordinate mixing changes the internal carrier, lower-order
  coefficients escape it, domain/boundary data fail to descend, or the lifted
  observable differs.
- **Next probe:** exact order-two two-coordinate operator with mixed derivative
  basis, transformed by an invertible rational coordinate change, using the same
  spinor-compatible coefficient module on both presentations.
- **Boundary:** finite exact internal carriers and declared scalar differential
  operators; unbounded-domain closure and nonlinear coefficients remain separate.

## Parked branches and re-entry

- Scalar axial domains: only for a new stratum or boundary law that breaks the
  current quotient witness.
- Polynomial families: only when a second nonlinear closure changes route choice
  or positivity duties.
- Higher dimension: only for a dimension-dependent constructor obstruction.
- Microlocal decomposition: when the observable is phase-space local and global
  reduction fails.
- Nonlinear PDE: a separate program requiring invariant manifolds, fusion/normal
  forms, or controlled closure error.
- Unique inverse-group recovery: parked unless global family, topology, and
  integration data are supplied.

## Stop rule

Stop when evidence supports or rejects the bridge, further detail changes no
observable or verdict, or work crosses the declared model class. Promote only the
compact witness, assumptions, cost, and failure boundary; leave derivations and raw
computation with their owners.
