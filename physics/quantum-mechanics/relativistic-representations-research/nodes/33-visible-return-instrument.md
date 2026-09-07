# Observable-indexed visible return

Status: `V_instrument-1` supports the finite exact visible instrument, while
action-generated composition, continuum transfer, and cost leverage remain open

Consumes: node 32's supported same-measure bound/open bridge, its multichannel
re-entry condition, and `V_open-1`'s detector-valued event output.

Produces: an obstruction-generated completely positive visible map, its inclusive
measure and channel effects, and a frozen contract for a post-distinction bench.

## Intent and constructed tension

Node 32 shows that one scalar visible measure is sufficient for a single elastic
channel. The global bridge asks for more: a graph/action compiler should retain
enough information for bound returns and for a selected open detector without
carrying the complete unresolved state space.

The tension is not merely “multichannel scattering is harder.” For a preparation
space `P` and unresolved space `Q`, the bound return uses

```text
M_B(Delta)=B^dagger E_Q(Delta)B.                (33.1)
```

This contracts the unresolved channel index. A channel-resolved open observable
may depend on the orientation and relative phase of `B` inside an energy fiber.
The exact question is whether (33.1) preserves that information.

Two alternatives are live:

1. `M_B` determines every admitted bound and open observable, so node 32's object
   can be used unchanged;
2. `M_B` determines only inclusive returns, and a detector-indexed enlargement is
   forced before an exclusive or interference-sensitive channel can be generated.

## Execute the information-loss probe

Use one retained state `P=C` and a two-dimensional degenerate channel fiber
`Q_E=C^2`. Construct two normalized departure maps

```text
B_+=(1/sqrt(2)) (1,  1)^T,
B_-=(1/sqrt(2)) (1, -1)^T.                     (33.2)
```

Both routes reach the same target in (33.1):

```text
B_+^dagger B_+=1=B_-^dagger B_-.               (33.3)
```

They therefore generate the same scalar self-energy, projected resolvent, bound
pole, and total continuum density whenever the channel Hamiltonian is proportional
to the identity on this fiber.

First test the resolved coordinate projectors

```text
Pi_1=diag(1,0), Pi_2=diag(0,1).
```

They still do not distinguish the routes:

```text
B_+^dagger Pi_a B_+=1/2=B_-^dagger Pi_a B_-,   a=1,2.            (33.4)
```

Now construct the coherent detector effect from the first departure ray,

```text
F_+=B_+B_+^dagger=(1/2)((1,1),(1,1)).           (33.5)
```

Direct multiplication gives the distinguishing output

```text
B_+^dagger F_+ B_+=1,
B_-^dagger F_+ B_-=0.                           (33.6)
```

The two interactions have identical `M_B` and identical coordinate-channel
probabilities but different interference-sensitive open observables. Alternative
1 is rejected. More samples of the scalar measure cannot repair the lost channel
orientation.

The same loss appears in the on-shell channel kernel. If `R_P(E)` is the retained
resolvent, the open matrix contains

```text
K_open(E)=B(E) R_P(E) B(E)^dagger.              (33.7)
```

Equations (33.2)--(33.3) leave `B B^dagger` undetermined, so `M_B` cannot reconstruct
(33.7). This is an information obstruction, not a failure of numerical accuracy.

## Let the obstruction generate the common object

Do not append channel labels to `M_B` by hand. Retain the operation that was
contracted too early. For the declared unresolved observable algebra `A_Q`, define

```text
Phi_B:A_Q -> End(P),
Phi_B(A)=B^dagger A B.                           (33.8)
```

Its positivity is computed rather than asserted. For every `A=C^dagger C`,

```text
Phi_B(A)=B^dagger C^dagger C B=(CB)^dagger(CB)>=0.               (33.9)
```

The old visible measure is a restriction, not a competing object:

```text
M_B(Delta)=Phi_B(E_Q(Delta)),
Sigma(z)=Phi_B((z-H_Q)^(-1)).                   (33.10)
```

If channel effects `F_a` commute with the spectral projections and form a detector
partition `sum_a F_a=I_Q`, then

```text
M_(B,a)(Delta)=Phi_B(E_Q(Delta)F_a)>=0,
sum_a M_(B,a)(Delta)=M_B(Delta).                (33.11)
```

Thus the bound return consumes the inclusive restriction, while the open detector
consumes the same map at a finer observable. Coherent channel effects such as
(33.5) retain interference; restricting `A_Q` to diagonal effects deliberately
forgets it.

The observable algebra also generates the strongest safe quotient. Define the
cyclic unresolved sector

```text
Q_cyc=closure span{A Bp : A in A_Q, p in P}.    (33.12)
```

Every vector orthogonal to `Q_cyc` is invisible to every declared return because
`B^dagger A q=0`. Removing that complement preserves (33.8) for all admitted
observables. This is semantic compression relative to an observable algebra; it
does not claim that evaluation of the surviving map is cheap.

## Relation to the algebra and graph compilers

The action jet supplies typed vertices and the preparation selects their departure
columns. Before endpoint squaring or channel summation, a graph compiler can in
principle generate

```text
CompileDeparture(action jet, preparation, unresolved channel grammar, budget)
 -> B + action of A_Q on generated channel states
    + provenance, Ward/factorization certificates, and refusal.                 (33.13)
```

The visible map then consumes this output once:

```text
departure compiler -> Phi_B
                         |- spectral resolvent -> bound pole/return
                         |- detector effect     -> open event/channel
                         `- graph excursions    -> perturbative refinement.
```

`C_open-v1` currently produces characteristic amplitudes and detector effects, not
the pre-contraction operator `B` or its unresolved observable action. Therefore the
present relation is a generated interface obligation, not yet a composition claim.
Adding `B` to `C_open-v1` would create `C_open-v2`; a separate upstream departure
compiler avoids silently revising the frozen result.

## Frozen candidate `C_instrument-v1`

Inputs:

```text
finite P and channel fiber Q,
action/preparation-generated departure B: P -> Q,
declared finite observable/effect family in A_Q,
optional channel partition and resource budget.
```

Retained operation:

```text
CompileVisibleInstrument(B, observable family, detector partition, budget)
 -> Phi_B evaluations + inclusive measure
    + channel cells + additivity/positivity certificates
    + open kernel B R_P B^dagger + cyclic visible support
 | refusal(shape, nonpositive effect, incomplete partition,
           unavailable departure, or budget).
```

Independent dimensions are inclusive recovery, channel discrimination, positivity
and partition recovery, open-kernel reconstruction, cyclic quotient, and complete
cost. The seed counterexample (33.2)--(33.6) motivates the candidate and cannot
serve as independent transfer evidence.

The post-freeze bench must use `dim(P)>1`, a different exact departure matrix, a
nontrivial detector partition, one coherent effect, and one rejected invalid
effect/partition. It supports the candidate only if the unchanged operation
recovers `B^dagger A B`, the partition sum, and `B R_P B^dagger` without receiving
their expected answers. Cost leverage remains open until an action-generated
departure and a fair full-route consumer are present.

## Post-freeze bench

Use `P=C^2`, `Q=C^3`, and the exact departure

```text
B=((1,0),(0,1),(1,1)).                          (33.14)
```

This is structurally distinct from the one-column seed. With
`F_L=diag(1,0,0)`, `F_R=diag(0,1,1)`, and the coherent effect projecting onto
`(1,1,0)^T/sqrt(2)`, the unchanged compiler generates

```text
Phi_B(I)=((2,1),(1,2)),
Phi_B(F_L)=((1,0),(0,0)),
Phi_B(F_R)=((1,1),(1,2)),
Phi_B(F_L)+Phi_B(F_R)=Phi_B(I),                 (33.15)

Phi_B(F_coh)=(1/2)((1,1),(1,1)).               (33.16)
```

For `R_P=((2,1),(1,3))`, the same stored departure gives

```text
B R_P B^dagger=((2,1,3),(1,3,4),(3,4,7)).      (33.17)
```

Closure of the departure columns under the declared effects has rank three, so
the generated cyclic support is all of this `Q`; the compiler does not manufacture
a false quotient. Non-Hermitian, nonpositive, above-identity, incomplete-partition,
shape, and budget failures are typed refusals. The executable certificate is
`computation/tests/test_visible_instrument.py`; the replayable domain verdict is
owned by `../results/return-compiler-dispositions.md`.

## Horizon and stop rule

The horizon is finite-dimensional exact channel fibers and observable algebras.
It establishes the information object and its algebraic certificates, not a
continuum scattering theorem, asymptotic completeness, or computational advantage.
The post-freeze matrix bench and refusals have determined the frozen dimensions, so
this branch stops. Re-enter continuum physics only through an action-generated `B`,
spectral/channel algebra, and a named bound/open consumer.
