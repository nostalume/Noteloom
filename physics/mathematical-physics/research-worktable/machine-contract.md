# Machine contract

## 1. Typed objects

The machine operates on packages, not isolated formulas.

```text
AnalyticProblem = (
  base M, bundle E -> M, coefficient field K,
  operator family D_a, parameter space A,
  Hilbert/Banach realization H,
  common dense core C, closed domains Dom(D_a),
  boundary/regularity data B,
  preparation P, observable O,
  allowed equivalences Eq, resource budget R
)

RepresentationProblem = (
  group/cover G, Lie algebra g,
  subgroup K and fiber type tau when a homogeneous bundle is present,
  carrier V, representation pi and derived action dpi,
  chosen u in U(g), commuting labels Z,
  analytic realization J: V -> H,
  preparation P, observable O,
  globality/unitarity data A, resource budget R
)

OperatorDecompositionProblem = (
  compact group G and actions U_E,U_F,
  bundles E,F over M,
  differential operator D: Gamma(E) -> Gamma(F), order bound r,
  common G-stable smooth core C,
  invariant connections or an allowed splitting policy,
  state-sector decompositions and tensor/branching oracle,
  bandwidth or tail policy,
  preparation P, observable O, resource budget R
)

InverseLadderProblem = (
  linear order-two operator pencil L_a with no supplied group,
  common core, domains, boundary data, adjoint pairing,
  allowed parameter shifts and intermediate bundles,
  arrow-order and coefficient-class bounds,
  observable O, zero policy, resource budget R
)

PDEDecompositionProblem = (
  jet-bundle map d_D: J^r E -> F and analytic realization D,
  symbol rank/characteristic regularity data,
  allowed coordinate, frame, and gauge equivalences,
  domain, boundary, preparation, observable,
  allowed intermediate bundles and local/global policy,
  closure, approximation, and resource bounds
)

OrbitReductionProblem = (
  PDEDecompositionProblem plus a bounded infinitesimal-automorphism grammar,
  joint interior/domain/boundary stabilizer policy,
  allowed compact/local group integrations and orbit-type policy,
  source/preparation/observable or spectral-window sector policy,
  quotient discretization, error target, baseline, and recovery demand
)

AdiabaticModeProblem = (
  slow base or phase space Z, fast Hilbert fiber K,
  full operator/symbol H_epsilon and leading fast family h_0(z),
  isolated spectral cluster and uniform gap gamma,
  common domains and symbol regularity order,
  energy/momentum validity region,
  preparation, observable, requested error order and time scale,
  allowed bundle trivializations and resource bound
)
```

`P` and `O` are included because a decomposition is useful only relative to what
is prepared and measured.  They may be omitted for a pure classification result,
but then no computational-leverage claim is available.

The common semantic output is first a representation calculus:

```text
RepresentationCalculus = (
  generators and relations,
  modules and distinguished vectors/covectors,
  central characters and commuting algebra,
  branching/tensor/intertwiner operations,
  differential-symbol layers and operator conjugation types,
  selection graph and reduced multiplicity maps,
  homogeneous-bundle multiplicity spaces and graded arrows,
  matrix-coefficient constructor,
  multiplicity or cyclic reduction,
  analysis/synthesis and observable recovery,
  construction, execution, and human-compression certificates
)
```

An analytic realization of that calculus is packaged as:

```text
BridgePackage = (
  algebraic carrier V,
  analytic carrier H and core C,
  differential realization rho: U(g) -> Diff(E)|C,
  represented operator rho(u),
  comparison W: rho(u) ~ D_a under Eq,
  sector decomposition V ~ integral/sum V_lambda,
  analysis/synthesis intertwiners A, S,
  recovery map Rec for O,
  chart/frame/gauge gluing intertwiners when local,
  mode projector, connection, curvature, effective operator, and leakage residual
    when approximate,
  certificates Cert,
  validity boundary Bound
)
```

`~` must be tagged as exact equality, unitary equivalence, gauge equivalence,
coordinate conjugacy, restriction to a sector, or controlled approximation.

Every mechanism must also expose the common operational interface:

```text
ReductionWitness = (
  original carriers H_E,H_F, operator D:H_E->H_F,
  preparation Prep and observable O:H_E->Y,
  reduced carriers K_E,K_F and operator D_red:K_E->K_F,
  analysis A_E,A_F and synthesis S_E,S_F,
  visible-sector representatives Q_E,Q_F and reduced observable O_red,
  R_an = A_F D-D_red A_E,
  R_syn = D S_E-S_F D_red,
  R_rec,E = S_E A_E-Q_E and R_rec,F = S_F A_F-Q_F,
  R_obs = O-O_red A_E,
  exact/controlled/formal tag, certificates, validity boundary
)
```

Group blocks, cyclic measures, complex quotients, and mode bundles are different
constructors for this same output.  Their witnesses compose; for two consecutive
endomorphic dynamics reductions the analysis residual is `R_A=AD-D_red A` and
the synthesis residual is `R_S=DS-SD_red`.  Consecutive analysis residuals compose
as `A_2 R_1+R_2 A_1`, while synthesis residuals compose as
`R_1 S_2+S_1 R_2`.  These formulas propagate approximation error without
reanalyzing the unreduced PDE.

### 1.1 Executable projection

The public computation boundary serializes this mathematical object as
`reduction-witness/v1`:

```text
schema, backend, outcome, request,
witness = {
  preserved_object, construction, reduced_object,
  maps, residuals, error, cost, validity
},
decision, limitations | obstruction, detail.
```

The five outcomes are `exact`, `controlled`, `formal`, `obstructed`, and
`unresolved`.  `detail` retains the backend-native certificate, including objects
too structured to flatten into the comparison fields.  Consequently this envelope
is a common capability and ranking interface, not a claim that every mathematical
witness has the same internal coordinates.

The direct executable registry covers factor/centralizer, observable-cyclic, and
stratified-orbit constructors. Its implementation and admission rule are in the
[computation workbench](computation/README.md). Bundle-valued Pauli construction,
its bounded global analytic promotion, `SU(2)/SU(3)` adjoint outer-multiplicity
selection, and an exact order-two lift on one adjoint matrix-coefficient core now
pass through the discovery boundary. A bounded PDE-first matrix closure also
recovers the effective `sl_2/sl_3` algebra and visible witness without a group
label. Its symbol-fiber continuation also constructs the inner covariance
derivations and pairing-dual second-order action without a supplied eigenvalue.
The coupled-operator continuation now applies generated base/fiber actions to
curvature and ordered lower terms before an optional Pauli observable consumer.
Full regular-representation synthesis, arbitrary polynomial-jet stabilizers, and
analytic promotion outside declared theorem contracts remain contract-level.

For bounded backend-independent discovery, the executable projection is
`reduction-decision/v1`:

```text
ProblemSpec
  -> applicability probes with first residuals
  -> candidate reduction-witness/v1 objects
  -> same-observable coincidence
  -> selected route or obstruction
  -> compact human decision card.
```

The admitted `quadratic-schrodinger/v1` problem runs full-mode and
observable-cyclic probes without a backend or group name. The
`pauli-landau-bilateral/v1` problem independently runs representation-to-PDE and
PDE-to-representation probes, retaining the matrix fiber and comparing their
spin/Fock channel witnesses. `pauli-landau-global/v1` composes that result with an
integral Chern class, finite magnetic-translation multiplicity, self-adjoint tensor
domain, Fourier measure, and heat-density observable. `su-adjoint-transition/v1`
constructs exchange-odd bracket and exchange-even traceless-Jordan intertwiners,
then selects the smallest quotient preserving an ordered/exchange-reversed
amplitude. `su-adjoint-pde/v1` composes those maps with the compact adjoint Casimir
and constructs an exact `H^2 -> L^2` order-two witness on one smooth coefficient
copy. These are evidence for the decision shape, not completeness of the candidate
portfolio. `matrix-pde-inverse/v1` instead closes unlabeled traceless coefficient
seeds under commutator, recognizes the full `sl_2/sl_3` matrix algebra, reconstructs
the natural maps, and leaves real-form and global-integration choices unresolved.
`matrix-symbol-covariance/v1` adds a principal pairing, generates inner derivation
vector fields on `Sym(L^*)`, verifies their symbol covariance, and derives the
coefficient eigenvalue from their pairing-dual square.
`matrix-adjoint-semigroup/v1` adds an involution, normalized compact carrier, and
`H^2` domain, constructs the `SU(n)` integration and observable-effective
`PSU(n)` quotient, and evaluates one closed heat-semigroup matrix element.
`natural-tensor-stabilizer/v1` constructs a finite tensor stabilizer from typed
relations, while `coupled-carrier-covariance/v1` constructs joint base/fiber
actions from metric and link covariance, quotients the ineffective fiber
commutant, and returns exact linked-symbol projectors.
`coupled-operator-covariance/v1` consumes that generated quotient, intersects the
curvature, first-order, and zeroth-order covariance kernels, and returns the
surviving full-operator action. Pauli grading and channels are an optional
observable consumer; the accepted domain record is a matched common-core theorem
contract rather than an internally proved self-adjoint completion. For Euclidean
rank-three scalar transport, that consumer derives the curvature axis, verifies
exact alignment, and returns both the longitudinal momentum polynomial and its
completed square. For a matrix-valued axial coefficient, it constructs the exact
two-sector algebra relative to the curvature grading, checks scalar sector action,
and derives roots, a minimal polynomial, primitive projectors, and sector momentum
polynomials. Noncommutation or unresolved within-sector action refuses observable
recovery while retaining the already certified generic operator candidate. None
of these finite schemas by itself performs global group integration.

The orbit constructor specializes the witness through

```text
OrbitReduction = (
  constructed effective action G and quotient strata Q=M/G,
  multiplicity bundles M_pi=Hom_H(V_pi,E|Q),
  reduced PDEs D_pi and descended trace domains,
  sector origin: source support, spectral frontier, or observable visibility,
  analysis/synthesis residuals and whole-route cost
).
```

It may return lower-dimensional PDEs. An ODE is obtained only when the quotient
dimension is one. The detailed construction and refusal boundaries are in the
[orbit-space reduction calculus](orbit-space-reduction-calculus.md).

## 2. Why the correspondence is not a bijection

Write the forward construction schematically as

```text
F: RepresentationProblem -> BridgePackage + Obstruction.
```

The inverse has type

```text
I: AnalyticProblem
   -> finite set/groupoid of InverseCandidate + Ambiguity + Obstruction.
```

Two round trips have weaker laws than inverse functions:

```text
AnalyticProblem --I--> candidate --F--> AnalyticProblem'
```

must produce a witness `AnalyticProblem' ~ AnalyticProblem` in the explicitly
allowed equivalence class, including domain and boundary data.

```text
RepresentationProblem --F--> bridge --I--> candidates
```

can at most require that one candidate recover the effective image of `G` acting
on the selected sector.  A kernel, covering group, central extension, inactive
factor, or larger commuting algebra may prevent recovery of the original `G`.

This asymmetry is information-theoretic, not an implementation defect.

### 2.1 The boundary-domain stabilizer

The inverse never assigns a symmetry from the differential expression alone. For
a boundary-value problem it descends through the joint stabilizer

```text
Aut(symbol)
  contains Aut(differential expression)
  contains Aut(expression, Omega, boundary trace subspace, observable).
```

If `Gamma_r` is the required boundary-jet trace and the boundary condition is
`B Gamma_r u=0`, a candidate arrow `Q` has domain defect

```text
R_boundary(Q)=(B Gamma_r Q)|ker(B Gamma_r).             (2.1)
```

Exact spectral decomposition requires this residual to vanish in addition to the
interior commutator. For a first-order geometric generator on a Dirichlet domain,
normal boundary motion appears directly in (2.1); tangency removes it. The
[disk/ellipse probe](benchmarks/boundary-domain-symmetry-complexity.md) implements
this descent for affine Euclidean Killing fields and centered quadratic boundaries.

## 3. Tagged inverse targets

An `InverseCandidate` must have exactly one primary tag:

```text
GeometricSymmetry
  generator prolongations preserve an equation submanifold in jet space;

CommutingSymmetry
  operators Q satisfy [Q,D] = 0 (or preserve ker D);

LadderOrDynamicalAlgebra
  intertwiners map ker(D_a-lambda) to ker(D_a'-lambda');

MonodromyOrDifferentialGalois
  a group acts on analytic continuations or a Picard-Vessiot solution space;

LocalizationRepresentation
  a module over differential operators is related to a Lie-algebra module.
```

A candidate may have proven comparison maps to other tags, but sharing a Lie
algebra name is not such a proof.

## 4. Forward constructor

Given a `RepresentationProblem`:

1. **Select the visible coefficient.** Construct
   `MC(ell,v)(g)=ell(pi(g)v)` from the preparation/observable or a distinguished
   subgroup-fixed vector. Do not construct every matrix entry when the observable
   consumes only one channel.
2. **Differentiate the action.** Construct `dpi(X)` on the common core and verify
   `R_X MC(ell,v)=MC(ell,dpi(X)v)` before choosing coordinates.
3. **Bracket certificate.** Evaluate both composites on a generic core element and
   verify
   ` [dpi(X),dpi(Y)]f = dpi([X,Y])f `.
4. **Extend multiplicatively.** Use the universal property of `U(g)` to construct
   `rho(u)`; do not infer the dynamics from `G`.
5. **Exploit the center and commutant.** Evaluate central characters, branching,
   multiplicity spaces, or cyclic subspaces before forming coordinate operators.
6. **Analytic realization.** Check symmetry/closability or the specified closed
   realization, compute `R_boundary`, and verify domain invariance and boundary
   terms before giving the candidate a representation sector.
7. **Decompose.** Use irreducibles and a declared commuting algebra to construct
   sector projectors or an integral transform.
8. **Recover.** Push `P` and `O` through analysis and synthesis maps and exhibit
   `O(Rec(A(P))) = O(P)` or an error bound.

Failure at any step returns the failed equality, missing theorem hypothesis, or
domain obstruction.

### 4.1 General differential-operator specialization

For a supplied, not necessarily invariant, differential operator define

```text
g.D = U_F(g) D U_E(g)^(-1).
```

The compiler first decomposes `D` by differential order through the equivariant
principal-symbol sequence, then decomposes every symbol layer into irreducible
operator types `sigma`.  A type is curried to an intertwiner

```text
V_sigma tensor H_E -> H_F.
```

On state sectors `lambda -> mu`, the channel is represented by

```text
Hom_G(V_sigma tensor V_lambda,V_mu)
  tensor Hom(M^E_lambda,M^F_mu).
```

The output is an order-filtered selection graph, including outer multiplicities
and reduced maps.  It must classify its group support as finite bandwidth,
controlled tail for the named observable, infinite formal decomposition, or
unresolved.  `sigma=1` recovers invariant block diagonalization.

### 4.2 Homogeneous-bundle specialization

For `E_tau=G x_K W_tau`, the analytic carrier is the induced representation and
the visible block is

```text
M_(pi,tau)=Hom_K(V_pi restricted to K,W_tau).
```

Every `G`-equivariant differential arrow decomposes as `I_(V_pi) tensor D_pi` on
the smooth `G`-finite core.  For a graded complex, the machine returns the finite
maps between the `M_(pi,tau_p)` rather than coordinate components.  In the de Rham
case it must verify

```text
d_(pi,p+1)d_(pi,p)=0,
d_(pi,p-1)d_(pi,p-1)^* + d_(pi,p)^*d_(pi,p)
  = Delta_(pi,p).
```

For compact symmetric spaces with the declared invariant metric,
`Delta_(pi,p)=c_pi I`; for other homogeneous spaces this scalar Casimir reduction
is not assumed.

## 5. Inverse constructor family

The global selector is specified in the
[decomposition decision engine](decomposition-decision-engine.md).  It generates
a bounded candidate portfolio from constraint/complex, factor, commutant/orbit,
spectral-projector, observable-cyclic, and optional supplied-action probes.  Every
candidate is lifted through lower-order residuals and must instantiate a
`ReductionWitness` before ranking.

The observable-cyclic probe is specified in
[observable-cyclic-calculus.md](observable-cyclic-calculus.md).  Exact termination
requires a relative minimal-polynomial/zero certificate; approximate termination
requires an observable error certificate and may not be inferred from a small
floating-point recurrence coefficient.
Its current finite rational backend is
[computation/cyclic_reduce.py](computation/cyclic_reduce.py): it verifies a matrix
and physical metric exactly or consumes a matrix-free action with supplied
self-adjointness, then returns the recurrence, analysis/synthesis data, relative
minimal polynomial or boundary residual, moment-recovery checks, and an honest
no-gain flag.

Given an `AnalyticProblem`, first choose an equivalence policy.  Gauge and coordinate
normalization are transformations of the same problem only when their inverse and
their action on domains and observables are supplied.

Within resource budget `R`, run independent analyzers:

### 5.0 PDE symbol-geometry router

Represent `D` by `d_D:J^rE->F`; compute principal-symbol rank strata,
characteristic variety, factorization possibilities, separated symbol
eigenbundles, and gauge-null directions before selecting coordinates.  Route the
problem to one or more of:

```text
first-order bundle factorization,
joint strongly commuting decomposition,
noncommuting orbit/representation reduction,
differential-complex/cohomology reduction,
local microlocal modes with gluing.
```

Adapted coordinates may be integrated only from a constructed involutive
distribution or orbit geometry.  Local outputs must carry overlap intertwiners;
failure of constant rank, spectral separation, or cocycle compatibility is an
obstruction result rather than permission to choose another chart blindly.

### 5.1 Geometric analyzer

Choose a bounded vector-field ansatz, prolong it to the required jet order, and
solve the determining equations obtained by restricting the prolonged action to
the equation manifold.  Return infinitesimal generators and local integration
conditions.  This analyzer does not claim a spectral representation.

### 5.2 Filtered-centralizer analyzer

Apply the [filtered centralizer calculus](filtered-centralizer-calculus.md).
From `p=sigma(D)`, select intrinsic covariance modules and solve
`{p,q}=0` at the declared symbol orders.  Quantize each surviving `q`, compute the
lower-order commutator residuals, and solve the forced correction equations in
descending order.  Return lifted operators, obstruction/ambiguity classes, and a
completeness tag relative to order, module types, and coefficient class.  A raw
coordinate coefficient ansatz is only a tagged fallback.  Quotient polynomials in
`D` and other declared trivial symmetries before ranking new generators.

For `H=-Delta/2+V` on the Euclidean plane with `V in Q[x,y]`, the
[quadratic centralizer generator](quadratic-centralizer-generator.md) is the first
relative-complete backend.  It generates all rank-two Killing symbols from the
metric isometry algebra, computes `ker[K -> d(K dV)]`, reconstructs scalar lower
terms, and checks the divergence-ordered quantum commutator exactly.

The [radial extension](radial-centralizer-extension.md) retains the same modules
while enlarging coefficients to a finite half-Laurent algebra in
`s=x^2+y^2`.  It returns exact first-/second-order kernels and lower-term lifts or
refuses when the declared normal form cannot reconstruct them.  The complete
`E^2` Coulomb transfer is an implemented specialization, not a new ansatz.

The [complete `E^3` backend](e3-quadratic-centralizer.md) adds the first nontrivial
module quotient. It generates 21 symmetric presentations from `e(3)`, computes
their one-dimensional relation and 20-dimensional image, and only then applies
the potential map. Coulomb selects a ten-dimensional kernel; a radial perturbation
selects seven. Exact closure reconstructs `so(4)` after, not before, this rank test.

The [singular `E^2` backend](benchmarks/singular-oscillator-polynomial.md) adds a
finite Laurent coefficient grammar and an exact word-membership closure test. It
tries `span{1,H,A,B}` before the Hermitian degree-two words
`{H^2,HA,HB,A^2,{A,B},B^2}`. Success in the latter with a required nonlinear
coefficient returns `PolynomialAlgebra`; missing that bounded word space returns
`UnresolvedWithinBudget`, never a false infinite-algebra verdict. This backend
also has one bounded closure-to-representation adapter: a central character and
one lowest weight generate a positive finite Jacobi module, endpoint energy, and
interbasis recurrence. A companion cross-probe now identifies the hidden
generator as an affine coproduct `su(1,1)` Casimir and proves exact equality of
the phase-insensitive interbasis probabilities through the certified finite
levels, including a second rational-coupling input. This adapter is not yet
general across polynomial presentations; generic parent recognition, phases,
spatial kernels, and continuous carriers remain open.

### 5.3 Symbol-first factorization/intertwiner analyzer

For a parameter family `D_a`, begin with the necessary principal-symbol equation
`sym_2(D_a)=sym_1(B_a)sym_1(A_a)` through an explicitly allowed intermediate
bundle.  If it factors, lift the symbols and cancel the order-one and order-zero
residuals in descending order.  The target equalities are

```text
D_a - lambda_a = B_a A_a,
D_s(a) - tilde_lambda_a = A_a B_a,
A_a D_a = D_s(a) A_a + (lambda_a-tilde_lambda_a)A_a.
```

The last equality must be computed from the first two on the same core rather than
asserted separately.  A one-dimensional Riccati factor obtained from a previously
known eigenfunction is tagged `FormalFactorization`, not construction leverage.

### 5.4 Operator-algebra closure and group integration

Generate the associative operator algebra from every certified factor,
intertwiner, parameter shift, and `D_a`, quotienting only identities proved on the
common core.  Compute its bracket closure and classify it as Lie, Lie-super,
polynomial, shift-groupoid/crossed-product, infinite, or unresolved within budget.

Only a finite Lie closure with constant structure constants proceeds to Jacobi,
real-form, kernel, closed/skew-adjoint realization, domain-flow, and global
integration checks.  Until those pass, the output is a represented operator
algebra rather than “the group of the PDE.”

### 5.5 Analytic-continuation analyzer

For linear complex ODE systems, compute monodromy or differential-Galois data under
the hypotheses of the chosen theorem/algorithm.  Keep this result tagged; it
answers integrability and continuation questions, not automatically the geometric
or dynamical symmetry question.

## 6. Candidate ranking and ambiguity

Rank only relative to a requested capability:

1. preserves the requested domain, sector, preparation, and observable;
2. supplies exact or controlled recovery;
3. has fewer representation changes and lower whole-route cost;
4. exposes reusable intertwiners, projectors, or recurrences;
5. uses fewer unproved globality or analytic assumptions.

Equivalent candidates should be connected by an explicit intertwiner.  Otherwise
retain both.  The output is allowed to say `Underdetermined(missing=[...])`.

## 7. Certificate bundle

Every supported `BridgePackage` carries:

- algebra certificate: brackets, Jacobi identity, Casimir or enveloping relation;
- symbol certificate: rank/characteristic strata, factorization or mode projectors,
  and the first uncancelled residual when construction fails;
- differential certificate: equality/conjugacy of operators on a named core;
- witness certificate: analysis and synthesis intertwining residuals, visible-state
  recovery residual, and observable residual on their typed domains;
- analytic certificate: measure, closed/self-adjoint realization or weaker stated
  property, boundary form, and spectral scope;
- decomposition certificate: orthogonality plus completeness/resolution on the
  declared sector;
- recovery certificate: same observable after analysis and synthesis;
- round-trip certificate: equality in the allowed equivalence class;
- ambiguity certificate: kernels, covers, inactive factors, and alternative
  candidates;
- coordinate/gauge certificate: overlap intertwiners, cocycle consistency, and
  preservation of the named observable;
- spin/complex certificate when applicable: Clifford relations, spin or `Spin^c`
  lift, grading, and cohomological physical sector;
- adiabatic certificate when applicable: isolated cluster and gap, projector
  regularity, connection/gluing data, exact first residual, validity sector, time
  scale, and observable error bound;
- refusal certificate: finite ansatz, residual equations, and re-entry condition.

It also carries a **human-compression certificate**: primitive generator count,
relation count, semantic transformation depth, residual multiplicity/cyclic block
size, coordinate-expansion depth, and the instance formulas replaced by reusable
operations. Low runtime with a long opaque expansion does not pass this check.

Formal algebra without the analytic certificate is a `FormalCandidate`, not a
solution decomposition.

## 8. Computational substrate

Any executable implementation must remain beneath the human calculus:

```text
semantic request and observable
  -> carrier decomposition + differential-symbol filtration
  -> operator conjugation types + branching/fusion selection graph
  -> reduced multiplicity maps or cyclic blocks
  -> human-readable generators, relations, and recovery maps
  -> normalization/equivalence policy
  -> bounded ansatz generators
  -> exact polynomial/rational linear algebra and Gröbner elimination
  -> candidate objects + machine-checkable residuals
  -> analytic/domain checks that may require theorem contracts
```

Exact rational-function arithmetic is preferred for local certificates.
An unrestricted simplifier is not a proof step: coefficient field, assumptions,
canonical form, zero test, and degree/order bounds must be recorded.

## 9. Evaluation levels

- **Scalar family bench:** construct the rank-one spherical calculus from restricted-root
  multiplicities and central characters, then recover one fixed observable for at
  least two distinct multiplicity pairs.
- **Bundle transfer:** construct the multiplicity-space de Rham complex from a
  nontrivial isotropy type, generate exact/coexact spectra through its arrows, and
  recover a heat trace without component eigenforms.
- **General-operator regression:** decompose a finite tensor-type, non-invariant
  differential operator under conjugation; generate its state-sector selection
  graph and verify at least one extra zero not implied by fusion alone.
- **General-operator transfer:** repeat on a nontrivial homogeneous bundle or a
  group with outer tensor-product multiplicity, preserving symbol order and
  recovering one named transition or resolvent observable from reduced maps. The
  finite `SU(3)` adjoint sector passes transition recovery and changes the route
  relative to either one-copy model. Its adjoint-valued continuation now supplies
  `H^2 -> L^2` domain control and exact differential analysis/synthesis on one
  matrix-coefficient copy; the full regular representation remains open.
- **Group-free inverse regression:** from a positive quadratic Schrödinger PDE,
  construct normal modes, first-order factors, commutator closure, cyclic module,
  and spectrum without a supplied group.
- **Group-free inverse transfer:** on a second-order family whose answer is not
  supplied, return either a finite typed operator algebra with round-trip recovery
  or the first principal-symbol/lower-order/closure obstruction.
- **Cross-probe selection:** when two inverse constructors apply, build their
  reduction witnesses on the same carrier and observable, compute an explicit
  coincidence or obstruction, and retain the cheaper valid route together with
  any distinct classification capability of the unselected route. The rotated
  oscillator now supplies one exact factor-versus-centralizer instance.
- **Spinor PDE regression:** from connection curvature and Clifford multiplication,
  reconstruct the uniform-field Pauli factorization, Heisenberg ladder, spin
  projectors, and longitudinal direct integral without fixing a gauge potential.
  The [bilateral executable projection](benchmarks/bilateral-pauli-router.md)
  passes the algebraic channel, charge-sign transfer, and spin-curvature refusal
  checks through the public decision interface. The
  [group-free full-operator lift](full-operator-covariance-lift.md) independently
  constructs the coupled action, reduces it by curvature and lower-order defects,
  and recovers the same projector and channels on a matched common core. The
  [nonzero transport continuation](nonzero-first-order-transport.md) passes aligned
  and rotated scalar coefficients through the unchanged first-order defect and
  recovers exact shifted longitudinal polynomials; transverse inputs expose the
  construction boundary. The
  [matrix transport continuation](matrix-valued-transport-algebra.md) constructs
  the surviving two-sector coefficient algebra, minimal polynomial, projectors,
  and sector-dependent momentum polynomials, while noncommutation exposes its
  observable boundary. The
  [global analytic promotion](benchmarks/pauli-global-analytic.md) adds the unitary
  Landau/Fourier carrier, measure, finite Heisenberg degeneracy, self-adjoint
  domain contract, exact heat density, and topology/domain refusals on `T^2 x R`.
- **Variable-coefficient PDE transfer:** construct local symbol modes and their
  gluing/connection residuals, then either recover a named observable with an error
  bound or refuse global decoupling.  The spin-texture bench passes the exact
  projector/residual construction and states a conditional first-projector error
  bound; its sector-invariance theorem, the orbital magnetic transfer, and the
  whole-route cost audit remain open.
- **Orbit PDE-to-PDE transfer:** construct a boundary-compatible action from the
  realized operator, form its orbit-type quotient and parameterized sector PDEs,
  select sectors from the named source/spectral/observable policy, and prove
  analysis/synthesis recovery against a full PDE baseline at the same continuum
  error. The annular axial benchmark passes the source-visible scalar case with
  `3D -> 2D`. The warped-axis continuation constructs scalar fixed-stratum domain
  conditions and refuses an incompatible uniform policy; bundle multiplicities
  remain open.
- **Inverse-information bench:** verify that `(d,delta,Delta)` returns the universal
  Hodge factorization algebra and refuses a group claim unless first-order Cartan
  or equivalent symmetry arrows are supplied.
- **Regression:** recover the `SO(3)`/Legendre bridge without hard-coding its final
  coordinate operators.
- **Higher-rank transfer:** replace the single rank-one radial operator by a
  higher-rank
  commuting algebra without changing the matrix-coefficient interface.
- **Use:** consume the generated decomposition in a spectral coefficient,
  propagator, Green function, or transition-amplitude calculation and compare total
  cost with separation/factorization by hand.  The quadratic one-excitation bench
  passes this conditionally when `L` has a cheap retained action and its discovered
  cyclic degree satisfies `r<<n`; it returns no advantage at `r=n` and does not
  support a continuum nonquadratic claim. The quartic Galerkin transfer detects
  `Z_2` parity from the PDE coefficients, then returns exact cyclic no-gain in its
  tested even block and a controlled finite-model budget truncation; its
  Galerkin-to-PDE error remains open.
- **Refusal:** produce a bounded obstruction without upgrading it to a universal
  nonexistence theorem.

Use-level evidence must show both execution savings and human semantic compression
before the worktable claims general computational leverage.
