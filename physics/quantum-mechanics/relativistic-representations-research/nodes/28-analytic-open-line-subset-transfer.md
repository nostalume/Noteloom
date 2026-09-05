# Analytic open-line subset transfer

Status: exact use-level leverage is supported for the generic Euclidean four-photon
scalar-line bench; the compiler reduces 66 ordered histories to 16 shared states
while preserving the dressed propagator and its Ward endpoint law

## Capability and spine binding

Node 27 compresses scalar-line insertion histories into a matching kernel, but
leaves open whether proper-time integration recreates every ordering chamber. This
node tests that possible failure rather than generalizing the formalism.

- **Upstream anchor:** node 27's matching strata and node 26's action-generated
  current/contact operations.
- **Bridge question:** can the stratified proper-time object be integrated and
  summed without reopening all ordered graph histories?
- **Invariant target:** the exact untruncated scalar propagator dressed by four
  labelled photons at one generic Euclidean off-shell input.
- **Downstream effect:** decide whether the algebra--graph handoff has use-level
  computational value or stops at integrand organization.
- **Special resources:** one open tree line, exact rational invariant pairings,
  nonzero Euclidean kinetic denominators, and no loop momentum.
- **Rejoin edge:** a subset-transfer evaluator, exact recovery certificate, Ward
  certificate, and deterministic operation-count comparison.

The horizon is the full summed four-photon line, not its individual graph terms or
a cross section. Coupling powers and common phase factors are removed identically
from both routes.

## Integrate one chamber by its propagation segments

Take an ordered history with `r` local events `B_1,...,B_r`, where each block has
one or two photon labels. Let

```text
q_0=p,
q_a=p+sum_(b<=a) sum_(i in B_b) k_i,
D_a=m^2+<q_a,q_a>.                               (28.1)
```

The Euclidean presumption `D_a>0` places this bench away from every characteristic
denominator. For ordered insertion times

```text
0<tau_1<...<tau_r<T,
```

construct the durations for which each intermediate momentum propagates:

```text
s_0=tau_1,
s_a=tau_(a+1)-tau_a       (1<=a<r),
s_r=T-tau_r.                                      (28.2)
```

The transformation is triangular with unit Jacobian and maps the ordered chamber
bijectively to `s_a>0`. Evaluating the proper-time exponent on the same history
gives `-sum_a D_a s_a`; therefore

```text
integral_(ordered chamber) dT d^r tau
  exp[-sum_(a=0)^r D_a s_a]

=product_(a=0)^r integral_0^infinity ds_a exp(-D_a s_a)
=product_(a=0)^r D_a^(-1).                       (28.3)
```

This calculation, rather than an analogy with diagrams, turns every chamber into
the scalar propagator chain for its accumulated momenta. The remaining question is
whether those chains share enough intermediate results to avoid enumeration.

## Generate vertices from kinetic transport and its Ward obstruction

Define the reusable scalar propagator

```text
G(q)=D(q)^(-1),       D(q)=m^2+<q,q>.             (28.4)
```

The polarized current generated in node 26 evaluates on a transition `q->q+k_i`
as

```text
V_i(q)=<2q+k_i,epsilon_i>.                        (28.5)
```

Its pure-gauge evaluation is already a kinetic difference:

```text
V_i(q)|_(epsilon_i=k_i)
 =2<q,k_i>+<k_i,k_i>
 =D(q+k_i)-D(q).                                  (28.6)
```

Now inspect what happens when another photon `j` is inserted on opposite sides of
that kinetic cancellation:

```text
V_j(q+k_i)-V_j(q)
 =<2(q+k_i)+k_j,epsilon_j>-<2q+k_j,epsilon_j>
 =2<k_i,epsilon_j>.                               (28.7)
```

Without a local pair operation, (28.7) is the interior Ward residual. Requiring
the pure-gauge insertion to move to the endpoints forces

```text
C_(ij)|_(epsilon_i=k_i)
 =-[V_j(q+k_i)-V_j(q)]
 =-2<k_i,epsilon_j>,

C_(ij)=-2<epsilon_i,epsilon_j>.                   (28.8)
```

This sign is for the untruncated Euclidean line after stripping its common coupling
and phase. Node 26 uses an amputated Minkowski normalization in which the exchange
propagator contributes the relative minus sign instead. The two conventions encode
the same Ward cancellation; mixing them would produce the defect caught by the
executable endpoint test.

## Fold chamber integrals by accumulated photon subset

For a label subset `S`, construct

```text
q_S=p+sum_(i in S) k_i,
G_S=G(q_S).                                       (28.9)
```

Let `A_S(p)` be the sum of all integrated histories that start at `p` and consume
exactly `S`. Every nonempty history has a unique last event. Partitioning by that
event and attaching the last propagator from (28.3) constructs

```text
A_empty(p)=G_empty,

A_S(p)=G_S [
  sum_(i in S) V_i(q_(S-{i})) A_(S-{i})(p)
 +sum_({i,j} subset S) C_(ij) A_(S-{i,j})(p)
].                                                (28.10)
```

No expected amplitude is present in the input. The function
`evaluate_scalar_line_amplitude` receives the invariant pairing, initial momentum,
photon momenta and polarizations, mass, and a state budget. It constructs every
`q_S`, denominator, current, contact, and recurrence value.

The equality with explicit histories follows inductively. For `S=empty`, both
routes return the initial propagator. If they agree for all smaller subsets, the
first sum appends every possible singleton last event once, while the second
appends every possible pair last event once. Because every ordered singleton/pair
partition has exactly one last block, their images are disjoint and exhaustive.
Multiplication by `G_S` gives the same final chamber integral (28.3). Thus

```text
A_S^subset(p)=sum_(histories h on S) A_h(p).       (28.11)
```

The proof certifies the retained recurrence; it does not replace it.

## Calculate the endpoint Ward law

For two photons, abbreviate `G_S=G(q_S)` and
`V_i(S)=V_i(q_S)`. Contract photon one. Substitution of (28.6)--(28.8) into
(28.10) gives

```text
W_1 A_{1,2}(p)
=G_12 [
  (D_12-D_2) G_2 V_2(empty)G_empty
 +V_2({1}) G_1(D_1-D_empty)G_empty
 -[V_2({1})-V_2(empty)]G_empty
].                                                (28.12)
```

Using only `D_S G_S=1`, calculate the three contributions:

```text
first
 =A_{2}(p)-G_12 V_2(empty)G_empty,

second
 =G_12 V_2({1})G_empty-G_12 V_2({1})G_1,

third
 =-G_12 V_2({1})G_empty+G_12 V_2(empty)G_empty.   (28.13)
```

The four interior terms cancel on their common scalar-line target, leaving

```text
W_1 A_{1,2}(p)
 =A_{2}(p)-A_{2}(p+k_1).                          (28.14)
```

This is precisely the difference between attaching the pure-gauge photon at the
two endpoints. It vanishes after the corresponding on-shell amputation, while the
off-shell line retains its endpoint charge. The computation also explains why the
contact sign in (28.8) is forced.

## Exact four-photon use certificate

The certificate uses a nine-dimensional formal invariant span for

```text
(p,k_1,k_2,k_3,k_4,epsilon_1,epsilon_2,epsilon_3,epsilon_4).
```

Its Gram form has diagonal entries `20` and off-diagonal entry
`1/(2+i+j)` for basis labels `i!=j`; `m^2=3`. The form is symmetric and strictly
diagonally dominant with positive diagonal, so the Euclidean denominators are
positive. These are pairings of semantic vectors, not a spacetime component
expansion.

Two independent constructions run on that same input:

```text
baseline
  -> recursively enumerate every ordered singleton/pair partition
  -> evaluate its vertices and propagator chain
  -> sum 66 exact rational values;

subset transfer
  -> construct 16 accumulated momenta and denominators
  -> evaluate recurrence (28.10)
  -> return one exact rational value.                             (28.15)
```

The computed residual is exactly zero:

```text
A_{1,2,3,4}^subset-A_{1,2,3,4}^66-histories=0.    (28.16)
```

The independent history generator confirms the sector decomposition from node 27:

```text
24 four-current histories
+36 one-contact histories
+ 6 two-contact histories
=66.                                               (28.17)
```

The Ward certificate independently replaces one polarization by its momentum and
checks (28.14). This catches a relative contact sign that the same-value comparison
would miss if both routes shared the same mistaken convention.

## Deterministic cost comparison

For `N` photons, recurrence (28.10) has `2^N` states. Its transition contributions
are

```text
E_N=sum_(S subset [N]) [|S|+binom(|S|,2)]
   =N 2^(N-1)+binom(N,2)2^(N-2).                  (28.18)
```

For `N=4`, the evaluator visits 16 states and combines 56 transition terms. Explicit
history evaluation performs

```text
L_4=sum_r h_(4,r)(4-r)
   =24(4)+36(3)+6(2)
   =216                                               (28.19)
```

event applications across 66 separately materialized histories. Both routes build
the same invariant pairings and return the same exact value; there is no accuracy
trade. Optional recovery of every individual graph still costs at least 66 outputs,
but that cost is absent when the requested object is their full dressed-line sum.

This supports computational leverage for the scoped Green-function building block:
shared accumulated-momentum states prevent analytic chamber integration from
recreating the history count. It does not yet establish predictive leverage for a
cross section, a loop amplitude, or a bound-state observable.

## Global verdict and next discriminator

The path from representation-derived field data to graph computation is now
generative on the scalar open-line class:

```text
local U(1) transport
  -> current and Ward-forced contact
  -> matching quotient
  -> proper-time chamber factorization
  -> subset transfer
  -> exact dressed scalar line with endpoint certificate.        (28.20)
```

The special resource is important: scalar transport is commutative and its free
worldline measure is Gaussian. Loop topology, renormalization, and spin transport
are not compressed by this result.

The next global discriminator is therefore the half-integer branch, not another
scalar multiplicity and not tropical integration. A fermionic open line introduces
ordered spin transport. The candidate reconstruction is a Grassmann/exterior
worldline operation whose finite coefficient is generated as a Pfaffian or matching
recurrence, never by selecting explicit gamma matrices. It must recover the scalar
subset interface after forgetting spin, preserve the Ward endpoint law, and either
retain comparable shared-state complexity or issue a precise noncommutative-ordering
obstruction. If it merely hides gamma-matrix expansion inside a spin factor, reject
the extension and keep the scalar result bounded.

## Supported frontier and open boundary

Supported:

- every ordered chamber factors exactly into its scalar propagator chain;
- action-generated singleton and Ward-forced pair vertices produce a reusable
  subset recurrence;
- the generic rational `N=4` value equals the independent 66-history sum exactly;
- the evaluator reduces 216 repeated event applications to 56 shared transition
  contributions on 16 states; and
- the two-photon Ward contraction equals the difference of endpoint lines.

Open:

- half-integer spin transport without explicit Clifford components;
- a physical on-shell multiphoton observable and its recovery cost;
- loop sewing, causal continuation, singular thresholds, and renormalization;
- stability and scaling for floating-point high-multiplicity input; and
- graph-moduli/tropical leverage once nontrivial loop topology exists.

Stop the scalar open-tree multiplicity branch here. Re-enter only for a physical
observable that consumes this exact recurrence or for a failure discovered by the
fermionic/loop extensions.

## Materials and edges

- Node 26 supplies the current/contact Ward obstruction.
- Node 27 supplies the matching quotient and its unresolved analytic boundary.
- `fieldcalc.worldline.evaluate_scalar_line_amplitude` owns the retained subset
  evaluator and cost certificate.
- `computation/tests/test_scalar_line_transfer.py` owns the independent 66-history,
  invariant Gram, budget, characteristic, and endpoint-Ward checks.

```text
26 local U(1) operations -> 27 matching quotient
  -> 28 analytic subset transfer
  -> fermionic exterior/spin-transport discriminator.
```
