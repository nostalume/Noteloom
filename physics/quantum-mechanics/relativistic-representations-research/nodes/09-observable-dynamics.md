# N9 — Observable Dynamics: Descent, Memory, and Asymptotic Closure

Status: observable factorization and autonomous-descent criteria proved for linear
evolution; exact projection-memory and resolvent identities constructed; N4r,
N4s, N8, N8c, and N8d classified; unbounded-domain generalization and quantitative
model-local memory bounds remain theorem-dependent  
Consumes: [N4q semantic computability](04q-semantic-computability.md),
[N4r field/mechanics projection](04r-field-mechanics-stability.md),
[N4s field-to-particle extraction](04s-field-particle-extraction.md),
[N8 collective diffusion](08-collective-diffusion-response.md),
[N8c dephased quantum chain](08c-dephased-quantum-ssep.md),
[N8d two-time quantum charge](08d-two-time-quantum-charge.md), and
[observable-dynamics contracts](../sources/observable-dynamics-contracts.md)  
Produces: a common dynamical criterion for exact particle, memory-bearing
mechanical, and asymptotically Markov collective reductions; an exact memory/
self-energy bridge; and a whole-route obstruction to treating every quotient as
computational compression

## Research contract

- **Question:** after an observable or preparation selects less information from a
  field dynamics, when does that retained information possess autonomous dynamics,
  and what exact object replaces autonomy when it does not?
- **Presumptions:** the internally proved core uses a vector space `X`, a linear
  semigroup `T_t:X->X`, linear observables, and surjective linear reductions. The
  projection-memory derivation first assumes a bounded generator `L` and bounded
  complementary projections. Applications to unbounded Hamiltonians consume the
  declared source contracts rather than inheriting the finite proof silently.
- **Output:** separate criteria for future-observable sufficiency and autonomous
  state descent; the minimal future-output quotient and its computational
  circularity; an exact memory equation, Markov-error obligations, and resolvent
  self-energy; and a classification of the existing global branches.
- **Boundary:** the node does not invent a useful selector, prove decay of a memory
  kernel, locate a particle shell, or make an eliminated resolvent cheap. Those are
  model-local constructions.

## 1. The missing question after selecting an observable

N4q constructed a prediction as

```text
input -> full physical evolution -> named observable.
```

N4r, N4s, and N8 then selected less information for bounded mechanics, particles,
and collective response. But an instantaneous quotient does not yet answer a
dynamical question. Two full states can agree on the retained data now and become
distinguishable later because discarded variables feed back.

The needed capability is therefore not “write a quotient,” but decide which of
the following has actually been constructed:

```text
one future observable factors through retained data;

all retained data evolve autonomously;

discarded data return through an exact memory;

memory becomes local only in a controlled scaling limit.
```

This distinction is the common bridge that the previous global view lacked.

## 2. Construct future-observable sufficiency

Let `X` be the full physical state or response space after its gauge and domain
identifications, and let

```text
T_t:X->X
```

be its evolution. A preparation or named family of measurements constructs a
surjective retained-data map

```text
q:X->Y.
```

Let `O:X->Z` be one requested output. At time `t`, the full prediction is
`O T_t`. We ask whether there is a map `R_t:Y->Z` such that

```text
O T_t=R_t q.                                      (2.1)
```

This is well-defined exactly when

```text
ker q subset ker(O T_t).                          (2.2)
```

Both directions are computed on the same input. If (2.1) holds and `qx=0`, then

```text
O T_t x=R_t qx=0,
```

which gives (2.2). Conversely, assume (2.2) and define

```text
R_t(qx)=O T_t x.
```

If `qx=qx'`, then `x-x'` lies in `ker q`; (2.2) gives
`O T_t x=O T_t x'`. Hence `R_t` is independent of the representative and the
definition computes (2.1).

This criterion is observable-relative. It can hold for a particular `O` even
when the retained state `q x` has no autonomous evolution.

## 3. Autonomous dynamics is a stronger invariant-kernel condition

Autonomous descent asks for maps `C_t:Y->Y` satisfying

```text
q T_t=C_t q.                                      (3.1)
```

Apply the preceding construction with `O=q`. The result is

```text
C_t exists
  iff ker q subset ker(q T_t)
  iff T_t(ker q) subset ker q.                    (3.2)
```

When this holds, the only possible definition is

```text
C_t(qx)=qT_t x.
```

It also inherits the semigroup law. On the common input `qx`,

```text
C_s C_t(qx)
  =C_s(qT_t x)
  =qT_sT_t x
  =qT_(s+t)x
  =C_(s+t)(qx).
```

Thus autonomous reduced dynamics is constructed by preservation of operational
indistinguishability, not inferred from the small dimension of `Y`.

For a bounded generator `L`, let `T_t=exp(tL)` and let `P` be a projection onto
the retained space, with `Q=I-P`. Here `q=P` and `ker P=QX`. Generator invariance
becomes

```text
P L Q=0.                                          (3.3)
```

Indeed, (3.3) makes `L(QX)` a subset of `QX`, hence every power of `L` and its
exponential preserve `QX`. Conversely, differentiating `P T_t Q=0` at `t=0`
gives `PLQ=0`. For unbounded generators, domain invariance and semigroup
hypotheses must be supplied separately.

## 4. The exact minimal quotient exists but can be computationally empty

The named observable and full evolution themselves define the dynamically
invisible subspace

```text
K_(O,T)=intersection_(t>=0) ker(O T_t).
```

It is invariant. If `x` belongs to `K_(O,T)`, then for any `s,t>=0`,

```text
O T_t(T_sx)=O T_(t+s)x=0,
```

so `T_sx` belongs to the same subspace. Therefore the quotient

```text
Y_*=X/K_(O,T)
```

always carries exact descended dynamics and exactly determines every future value
of `O`. Equivalently, construct the output-history map

```text
q_*x : t |-> O T_t x.
```

If `S_s` shifts a history by `(S_s f)(t)=f(t+s)`, then

```text
(q_* T_s x)(t)
  =O T_tT_sx
  =O T_(t+s)x
  =(S_s q_*x)(t).
```

Hence

```text
q_* T_s=S_s q_*.
```

This is the maximal semantic quotient for the requested future observation: any
other linear `q` satisfying (2.1) for every `t` has `ker q subset K_(O,T)` and
therefore retains at least as much information.

But constructing `q_*x` already evaluates the whole requested trajectory. It is
an exact reduction with no computational gain. This provides the global negative
baseline:

```text
existence of an exact predictive quotient
  does not imply a cheaper construction of that quotient.
```

## 5. Failure of descent constructs memory rather than an approximation

Now assume `T_t=exp(tL)` with bounded `L` and choose complementary projections
`P,Q`. For one full solution `x(t)`, construct

```text
p(t)=Px(t),
u(t)=Qx(t).
```

Applying the two projections to `dot x=Lx` gives

```text
dot p=PLP p+PLQ u,
dot u=QLP p+QLQ u.                                (5.1)
```

Solve the second equation on its own typed space `QX`:

```text
u(t)
  =exp(tQLQ)u(0)
   +integral_0^t exp((t-s)QLQ)QLP p(s) ds.         (5.2)
```

Substituting this same `u(t)` into the first equation computes

```text
dot p(t)
  =PLP p(t)
   +F(t)
   +integral_0^t K(t-s)p(s) ds,                   (5.3)

F(t)=PLQ exp(tQLQ)u(0),
K(t)=PLQ exp(tQLQ)QLP.                            (5.4)
```

The three added objects have direct meanings:

- `PLP` is instantaneous retained evolution;
- `F(t)` is dependence on discarded initial data;
- `K(t)` is information that leaves the retained sector, evolves in `QX`, and
  returns later.

Equation (5.3) is exact. If `PLQ=0`, both `F` and `K` vanish and it reduces to the
autonomous criterion (3.3). If only the prepared inputs satisfy `u(0)=0`, the
initial term vanishes but the memory generally remains; closure on one prepared
input class is weaker than a quotient of all states.

## 6. Markov closure requires a computed memory scale

Suppose `QLQ` is exponentially stable on the relevant complement and invertible.
Then the integrated memory is constructed without expanding components:

```text
M=integral_0^infinity K(s)ds
  =-PLQ(QLQ)^(-1)QLP.                             (6.1)
```

The equality follows by applying `QLQ` to the semigroup integral:

```text
QLQ integral_0^infinity exp(sQLQ)ds
  =[exp(sQLQ)]_0^infinity
  =-I_(QX).
```

Replacing the memory convolution by `M p(t)` is not licensed by (6.1) alone. The
exact difference is

```text
integral_0^t K(s)p(t-s)ds-Mp(t)
  =integral_0^t K(s)[p(t-s)-p(t)]ds
   -integral_t^infinity K(s)p(t)ds.               (6.2)
```

For differentiable `p`, the norm is bounded by

```text
sup_(0<=r<=t)||dot p(r)|| integral_0^t s||K(s)||ds
  +||p(t)|| integral_t^infinity ||K(s)||ds.       (6.3)
```

Thus an honest Markov reduction needs both a short memory moment and a slow
retained variable. The candidate local generator is

```text
L_eff=PLP-PLQ(QLQ)^(-1)QLP,                       (6.4)
```

but convergence and its error must come from model-local scale estimates.

## 7. The same eliminated dynamics produces the resolvent self-energy

The time-memory and bound-state constructions are two transforms of the same
`Q` evolution. For `f in PX`, solve

```text
(z-L)(p+u)=f,
p in PX,
u in QX.
```

The `Q` equation gives, whenever the inverse exists,

```text
u=(z-QLQ)^(-1)QLP p.                              (7.1)
```

Insert this same `u` into the `P` equation:

```text
[z-PLP-Sigma(z)]p=f,

Sigma(z)=PLQ(z-QLQ)^(-1)QLP.                     (7.2)
```

Consequently, on `PX`,

```text
P(z-L)^(-1)P
  =[z-PLP-Sigma(z)]^(-1),                         (7.3)
```

and (7.1) recovers the discarded component. Equations (5.4) and (7.2) contain the
same departure, complementary evolution, and return maps. Memory in time and
self-energy in spectral response are not parallel analogies; they are constructed
from the same block composites.

For unbounded field Hamiltonians, OD-03 owns the domain and invertibility
conditions. At a continuum threshold, the ordinary inverse may cease to exist;
boundary values, resonances, or asymptotic constructions then replace the gapped
formula.

## 8. Existing branches are three different descent mechanisms

### 8.1 N4r: prepared mechanics is generally memory-bearing

N4r constructs a preparation isometry `J:M->H` and `P=JJ^dagger`. The prepared
subspace is not presumed invariant under the field Hamiltonian `mathbb H`; emission,
virtual radiation, and pair sectors supply nonzero cross maps. With `L` replaced by
`mathbb H`, (7.2) becomes exactly N4r's

```text
Sigma(z)
  =J^dagger mathbb H Q
    (z-Q mathbb H Q)^(-1)
    Q mathbb H J.
```

Thus mechanical dynamics is not obtained by deleting the field. It is an exact
prepared response with energy-dependent memory and a recovery map for its dressing.

An exact bound spectral projection would commute with `mathbb H` and therefore
give autonomous unitary evolution on its range. But locating that projection can
require the full spectral problem. Exact invariance can therefore be semantically
stronger yet computationally more expensive than the simple preparation.

### 8.2 N4s: a stable particle shell is exactly invariant

N4s constructs the stable one-particle space from a sharp joint translation-
spectral shell `Sigma`. Its spectral projector `E(Sigma)` commutes with translations
and their time subgroup. On the same full state `x`, time-translation covariance
computes

```text
E(Sigma)T_t x=T_tE(Sigma)x.
```

With `P=E(Sigma)` and `Q=I-P`, this gives

```text
P T_t Qx=T_t P Qx=0,
Q T_t Px=Q P T_t x=0.
```

Hence its `P/Q` cross maps vanish and the restricted translation action is
autonomous. The field-created state

```text
E(Sigma)A Omega
```

is the recovery of the same shell amplitude, not a coordinate representative of
the original field carrier.

Scattering uses a different exact construction. When a wave operator exists, its
intertwining relation transports autonomous asymptotic dynamics into the full
theory. A resonance or infraparticle lacks the corresponding sharp invariant shell,
so it must not be forced into the same quotient.

### 8.3 N8/N8c: collective dynamics is asymptotically autonomous

In N8c, `X` is the operator space and `P` is occupation pinching. Write the
Liouvillian as

```text
L_gamma=D_gamma+V.
```

N8c computes

```text
D_gamma P=0,
P D_gamma=0,
P V P=0,
Q V P nonzero,
P V Q nonzero
```

on an allowed one-hop occupation event. In particular,

```text
P L_gamma Q=P V Q nonzero.
```

The invariant-kernel criterion therefore rejects autonomous population dynamics at
finite `gamma`. Its exact population memory is

```text
K_gamma(t)
  =P V Q exp(t QL_gamma Q)Q V P.                 (8.1)
```

Strong dephasing makes the relevant complementary coherence decay on the fast
scale. OD-01 supplies the exact memory baseline, while QD-01 supplies the
model-local slow-process limit. Equation (6.1) constructs its leading generator:

```text
L_slow
  =-P V(D_gamma|_Q)^(-1)V P,
```

which N8c evaluates as SSEP. Collective classical dynamics is therefore not a
lower quantization level. It is a Markov limit of an exact memory-bearing quantum
quotient.

N8's hydrodynamic density has the same logical type but a different scale: the
discarded microscopic modes become locally representable only in the long-time,
long-wavelength response limit. Its conductivity and any remainder estimate play
the role of model-local data that must justify that closure; N8 does not derive an
exact projection kernel for a generic quantum field theory.

### 8.4 N8d is a recovery regression, not a fourth mechanism

N8d constructs one endpoint observable `O`, the two-time right-charge difference,
and verifies that its finite distribution approaches the SSEP output. In the
language of section 2, it tests approximate factorization of `O T_t` through the
slow population process. It does not make `P L_gamma Q` vanish and therefore does
not establish autonomous finite-`gamma` classical dynamics.

N8d remains valuable as a same-observable check, but it is downstream evidence for
N8c's asymptotic closure, not a new global branch.

## 9. The reconstructed global view

The research spine now has a dynamical discriminator after the observable selector:

```text
symmetry representation
  -> admissible state content and covariance
  -> local field realization/equation
  -> algebra + state + full dynamics
  -> operational preparation or observable constructs q
  -> test how q interacts with full evolution
       |-> invariant kernel: exact autonomous particle/bound sector
       |-> noninvariant kernel: exact memory/self-energy mechanics
       |-> fast/slow or hydrodynamic limit: collective Markov closure
       `-> asymptotic intertwiner: scattering output
  -> recover the same named observable
  -> audit construction, memory, and recovery cost.
```

This locates “first” and “second” quantization upstream: they construct algebras and
states. They do not determine which downstream selector closes. Bounded mechanics,
particles, scattering, and collective response differ by how their operationally
selected information interacts with the same full evolution, not by successive
quantization ranks.

The common mathematical object is also now more precise than a generic quotient:

```text
observable sufficiency: ker q subset ker(O T_t),
autonomous descent:      T_t ker q subset ker q,
failure of descent:      complementary propagator and return memory,
computational gain:      cheaper construction of the retained law and recovery.
```

## 10. Computability audit and next discriminator

The node produces a theorem, not a universal solver:

- the future-output quotient always exists, but constructing it can equal the
  original prediction;
- an invariant spectral projector gives exact autonomy, but finding it can equal
  the original spectral problem;
- the exact memory equation preserves semantics, but `exp(tQLQ)` can retain the
  full discarded complexity;
- a Markov generator is cheaper only after decay and scale estimates control
  (6.3);
- an asymptotic intertwiner is predictive only when its limit and observable
  recovery can be constructed.

The next global discriminator returns to the field/mechanics boundary in
[N9a](09a-threshold-spectral-measure.md). N4r's self-energy has the form (7.2).
N9a constructs its same `Q`-spectral object on both sides of a channel threshold:

```text
below threshold
  -> analytic self-energy and a prepared bound pole;

at/above threshold
  -> boundary value, long memory, decay or scattering output.
```

The result is not another formal Schur complement. One rank-one coupling measure
computes a bound pole and dressing weight below threshold, a continuum density and
scattering boundary above it, and an exact `t^-2` memory. Its divergent first
memory moment also shows that cheap spectral root finding does not imply the
simple time-local Markov estimate. The remaining frontier is to construct the
coupling measure from one regulated field model rather than prescribing it.

## Verification ledger

| Obligation | Same-input witness | Verdict |
| --- | --- | --- |
| future observable factors through `q` | representative-independence iff `ker q subset ker(O T_t)` | exact linear theorem |
| retained state is autonomous | `C_t(qx)=qT_t x` iff `T_t ker q subset ker q` | exact linear theorem |
| descended maps form a semigroup | compute both composites on `qx` | exact |
| bounded projection generator criterion | differentiate/exponentiate `P T_t Q=0` and `PLQ=0` | exact |
| minimal future-output quotient | invariant intersection of future-output kernels and shift intertwiner | exact but computationally circular |
| nonautonomous retained evolution | solve the `Q` equation and substitute into the `P` equation | exact bounded linear identity |
| local-memory coefficient | integrate the stable `Q` semigroup | exact under stated stability/invertibility |
| Markov error obligations | identity (6.2) and norm bound (6.3) | exact; model estimates still required |
| spectral self-energy | solve the same `Q` block in the resolvent equation | exact under OD-03 hypotheses |
| N4r classification | its prepared Feshbach self-energy is (7.2) | exact semantic coincidence |
| N4s classification | sharp spectral projector commutes with translations | exact under stable-shell contract |
| N8c classification | N8c's one-hop calculation gives both departure and return maps | finite-`gamma` autonomy rejected; Zeno closure supported |
| N8d placement | tests one recovered output, not kernel invariance | regression leaf |
| unbounded/nonlinear generality | not proved by the bounded internal derivation | theorem-contract boundary |
| whole-route computational gain | depends on shell, complementary propagator, or memory estimates | open/model-local |

## Edges

- `N4q -> N9`: pass the same-observable compression equation and whole-route cost
  test; N9 adds the missing dynamical descent criterion.
- `N4r -> N9`: pass the prepared projection, self-energy, and dressing recovery as
  the exact noninvariant/memory-bearing case.
- `N4s -> N9`: pass the stable spectral shell and asymptotic intertwiner as exact
  invariant and scattering cases.
- `N8/N8c -> N9`: pass hydrodynamic scale separation and occupation pinching as
  asymptotically autonomous collective cases.
- `N8d -> N9`: pass one finite same-observable recovery check; retain it as
  downstream evidence rather than a new mechanism.
- `N9 -> N9a`: pass the common `Q` propagator, self-energy, Markov-error
  obligations, and bound/scattering discriminator for explicit evaluation.
- `N9 -> N7/manuscript synthesis`: pass the constructed global relation among
  field dynamics, bounded mechanics, particles, scattering, and collective
  response without a quantization hierarchy.
