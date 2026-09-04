# N10h — Carrier-Functor to Natural-Operator Grammar

Status: the natural operations and relations are internally derived for symmetric
tensor and symmetric Dirac-spinor-tensor potential functors in four dimensions,
and their packet adapters are consumed by N10c/N10g; the executable dispatches two
handwritten packets rather than synthesizing a grammar from a general carrier  
Consumes: [N2b Lorentz carriers](02b-lorentz-carriers.md),
[N3 realization bridge](03-realization-bridge.md),
[N4a polynomial-complex criterion](04a-polynomial-complex-details.md), and
[N10c retained residual constructor](10c-generative-residual-constructor.md), plus
[N10g Clifford transfer](10g-clifford-source-euler-transfer.md) as the downstream
consumer interfaces  
Computation: [carrier-to-grammar generator](../computation/10h-carrier-to-grammar/README.md)  
Produces: a typed two-family carrier-grammar adapter, three resource refusals, and
an end-to-end provenance witness through the bosonic and Clifford field systems  
Construction-origin correction: [audit](../results/07-construction-origin-audit.md)

## Research contract

- **Upstream anchor:** N2b constructs finite Lorentz carriers and N3 constructs
  their orbitwise relation to a physical fiber. N10c previously received its
  natural-operator grammar manually.
- **Bridge question:** which part of the operator grammar follows from carrier
  data, and which part is an additional presentation choice that representation
  theory cannot select?
- **Invariant target:** the same symmetric tensor and symmetric spinor-tensor
  fields, with the same rank shifts, local equations, constraints, source
  adapters, and physical cohomology as N10c--N10g.
- **Downstream effect:** the derivation removes unexplained operator vocabulary from
  the mathematical argument and the adapter makes its provenance consumable;
  executable grammar synthesis remains the next obstruction. Refusal narrows the
  paper's claim by proving that a particle representation alone does not choose an
  off-shell field presentation.
- **Special resources:** a chosen symmetric-power carrier functor, invariant
  nondegenerate Lorentz metric, and—only for the spinor branch—the Clifford action
  constructed in N4b from N2b's Weyl-spinor bridge.
- **Internal benchmark:** refuse label-only and missing-resource inputs; derive both
  local and adjoint grammars without coordinates; adapt them into N10c/N10g; recover
  their supported outputs with grammar provenance intact. This bench does not test
  relation synthesis from an unregistered carrier.
- **Horizon:** arbitrary Schur functors, mixed symmetry, auxiliary complexes,
  automatic carrier selection, invariant-theory basis enumeration, and predictive
  cost reduction are outside this node.

## 1. A representation label does not contain an operator grammar

N2b passes a finite Lorentz module and a little-group intertwiner. N3 proves that
this is sufficient for an orbitwise realization. A local operator needs more:

```text
physical fiber sigma
  -> choose an off-shell carrier presentation F
  -> construct natural maps on F
  -> solve locality and gauge obstructions.             (1.1)
```

The first arrow is not determined by `sigma`. The same helicity can be represented
by a direct chiral curvature, a gauge potential, or a larger auxiliary complex.
These presentations have different ranks, derivative orders, adjoints, and source
interfaces. Therefore the constructor deliberately refuses input containing only
a helicity or Lorentz highest-weight label:

```text
phase: carrier-presentation,
missing: off-shell carrier functor.                     (1.2)
```

This refusal is a result about the representation-to-field-equation spine, not an
implementation limitation: symmetry constrains admissible presentations but does
not uniquely choose their physical capability.

## 2. The symmetric functor generates multiplication and contraction

Choose the off-shell presentation

```text
F_r=Sym^r(V_C^*) tensor C,                             (2.1)
```

where `C` is initially the scalar coefficient module. The symmetric algebra
constructs two universal operations before momentum or coordinates are chosen:

```text
m_alpha:Sym^r(V^*)->Sym^(r+1)(V^*),
i_v:Sym^r(V^*)->Sym^(r-1)(V^*).                       (2.2)
```

Evaluate both composites on the same symmetric polynomial `f`. The derivation
rule gives

```text
i_v m_alpha f
 =alpha(v)f+m_alpha i_v f.                            (2.3)
```

The invariant nondegenerate metric turns momentum `p` into `p sharp` and therefore
constructs

```text
P=m_p,
A=i_(p sharp),
Q=eta^(-1)(p,p).                                      (2.4)
```

Substituting `(v,alpha)=(p sharp,p)` into (2.3) computes

```text
A P=P A+Q.                                            (2.5)
```

The same metric constructs double contraction `T=i_(eta^(-1))`. When `T` acts on
`p symmetric-product f`, either of its two contraction slots can hit the new
factor. Hence, on that same `f`,

```text
T P f=P T f+2A f,
T A f=A T f.                                          (2.6)
```

Thus the local scalar grammar is derived as

```text
{Q,P,A,T},
AP=PA+Q,
TP=PT+2A,
TA=AT.                                                (2.7)
```

The Fischer pairing does not add an arbitrary operator. It turns the same
multiplication/contraction construction around:

```text
P^dagger=A,
T^dagger=U,                                           (2.8)
```

where `U=m_eta` is symmetric metric insertion. This derives the adjoint extension
`{Q,P,A,T,U}` consumed by the source/Euler branch.

Without the nondegenerate metric, neither `p sharp`, `Q`, `T`, nor the Fischer
adjoints exist. The adapter therefore returns a separate `invariant-duality`
refusal rather than silently importing index raising.

## 3. The coefficient module decides whether gamma operations exist

Now choose

```text
F_r^Delta=Sym^r(V_C^*) tensor Delta.                  (3.1)
```

Calling `Delta` a Dirac carrier is not yet enough. N4b constructs an equivariant
map

```text
gamma:V_C->End(Delta),
gamma(v)gamma(w)+gamma(w)gamma(v)
 =2eta(v,w)I.                                         (3.2)
```

Only this operation permits the derivation to add

```text
L=gamma(p),
G=gamma dot partial_u,
Y=gamma(u).                                           (3.3)
```

If (3.2) is absent, the request returns a `coefficient-action` refusal. The Dirac
label is not treated as a hidden gamma matrix.

The relations are again evaluations of common composites. Gamma contraction can
act either on the old field or on the newly inserted momentum:

```text
G(P psi)=P(G psi)+L psi.                              (3.4)
```

Clifford polarization applied after tensor-slot contraction gives

```text
G L+L G=2A,
L^2=Q.                                                (3.5)
```

Operations on distinct tensor and coefficient slots commute. Together with (2.5),
this derives N10c's complete bounded local rewrite packet

```text
{Q,L,P,A,G}.                                          (3.6)
```

Dirac--Fischer duality constructs

```text
P^dagger=A,
G^dagger=Y,
L^dagger=L,                                           (3.7)
```

and evaluating `LY`, `AY`, and the local relations in the dual canonical order
derives the extended packet used by N10g. No component gamma matrix appears in
the packet adapter or its exact checks.

## 4. The derived packets are consumed, not compared afterward

The retained interface is

```text
CarrierGrammarAdapter(
  chosen symmetric-power presentation,
  coefficient module,
  invariant resources)
 -> primitives,
    typed degrees and rank shifts,
    rewrite rules,
    adjoints,
    provenance,
    refusal record.                                   (4.1)
```

N10c now accepts this packet instead of necessarily using its legacy built-in
grammar. With the scalar packet it regenerates

```text
D=Q-PA+(1/2)P^2T,
T epsilon=0,
T^2phi=0.                                             (4.2)
```

With the Dirac packet it regenerates

```text
S=L-PG,
G epsilon=0,
G^3psi=0.                                             (4.3)
```

N10g consumes the generated duality rewrite packet and independently returns

```text
M=I-(1/2)YG-(1/4)Y^2G^2.                             (4.4)
```

The executable check requires the provenance string from (4.1) to remain attached
through all three downstream outputs. Therefore (4.2)--(4.4) are not comparisons
with a generated list; they are calculations performed by the existing residual
and Euler constructors using that list.

## 5. Supported closure and global limitation

The bridge now has the more precise form

```text
physical representation
  -> chosen off-shell carrier functor                 [not determined]
  -> derived invariant operator grammar                [supported mathematically]
  -> two-family executable packet adapter              [supported here]
  -> obstruction-generated equation and constraints  [N10c]
  -> generated source/Euler response                  [N10e--N10g]. (5.1)
```

This makes the two active grammars internally readable and their presumptions
inspectable. It does not remove their relation tables from the executable: the
current constructor validates `symmetric-power`, dispatches on `scalar` or `dirac`,
and returns a handwritten packet justified by Sections 2--3. It therefore does not
show that Lorentz symmetry alone determines field equations or that an arbitrary
carrier yields an operator grammar. The remaining presentation choice is physical
and capability-relative: potential access, locality order, parity, source coupling,
action data, auxiliary freedom, and cost can select different nondominated routes.

The construction improves generative provenance and repeated reuse. It does not
make one free-field observable cheaper: the invariant structures and carrier
presentation were already known in the hand route, and the generator adds a small
symbolic construction cost.

N10i subsequently supplied the bounded capability-relative selector proposed by
the original version of this node, but only over three registered routes. The
construction-origin audit now exposes the earlier missing bridge one level lower:

```text
(carrier expression, invariant resources, degree/rank bounds)
  -> generated natural operations and computed relations
  -> normal-form grammar or refusal
  -> residual constructor use.                         (5.2)
```

[N10m](10m-natural-operation-compiler.md) now passes that discriminator: it removes
packet-specific dispatch from its trusted input, regenerates the symmetric packets,
transfers the carrier law to exterior power, and supplies the generated grammar to
a downstream residual constructor. N10h remains the derivation and legacy adapter;
N10m is the executable compiler front edge. Another rank or named equation within
the same power laws changes no spine claim. The next benchmark is complete bounded
operation enumeration for a projected or mixed-symmetry carrier.

## Edges

- `N2b/N4b -> N10h`: pass the vector metric, symmetric functor, Dirac coefficient
  module, and internally constructed Clifford action.
- `N3 -> N10h`: pass the representation/presentation distinction and the locality
  obligation; a fiber intertwiner alone triggers refusal.
- `N10c/N10g -> N10h`: pass the residual and Euler consumer interfaces; N10h binds
  its generated packets to them and returns one composite carrier-to-response
  operation. This is a revision edge, not a conceptual cycle.
- `N10h -> N10i`: pass the exact supported generation boundary and the label-only
  refusal; N10i adds capability and budget data rather than pretending to infer a
  presentation from the label.
- `N10h -> N10m`: pass the carrier-law derivation and expose the handwritten packet
  boundary that N10m replaces with executable law-driven compilation.
