# N4m — The Finite Integer-Spin Field Machine

Status: supported synthesis for each separate massless symmetric integer spin on four-dimensional Minkowski spacetime  
Read this before the technical proofs in N4a/N4c/N4e/N4f/N4g/N4h  
Consumes: [N2a physical helicity fiber](02a-spin-and-helicity.md), [N3 realization criterion](03-realization-bridge.md), [N4a screen complex](04a-polynomial-complex-details.md), [N4c action data](04c-action-completion-audit.md), [N4f causal construction](04f-finite-integer-spin-green-construction.md), [N4g positive-frequency construction](04g-positive-frequency-completion.md), and [N4h support faithfulness](04h-support-faithfulness.md)  
Produces: one readable constructor from a spin label to its field equation, causal response, and candidate one-particle amplitude

## Read this node as one machine

The input is one integer `s>=1`. The desired output is not merely a tensor
equation. It is a complete free-field route whose physical null-shell fiber is

```text
helicity +s direct-sum helicity -s.
```

The same five pieces of data generate that route for every finite `s`:

```text
FieldSystem_s=(G_s,F_s,R_s,C_s,M_s).
```

They have direct meanings:

| Object | Capability |
| --- | --- |
| `G_s` | stores gauge parameters |
| `F_s` | stores potential fields |
| `R_s` | turns a parameter into a gauge change |
| `C_s` | measures the part preventing wave propagation |
| `M_s` | converts the field pairing into the correct source pairing |

The equation, Green response, and particle amplitude are derived from these five
objects. They are not additional guesses.

## 1. Symmetric fields construct four natural operations

A symmetric rank-`s` covariant tensor can be evaluated repeatedly on one auxiliary
vector `u`. This identifies it with a homogeneous polynomial `phi(u)` of degree
`s`; no component information is lost. Given momentum `p`, the metric constructs

```text
P_p = multiplication by p.u,       degree +1,
A_p = contraction with p,          degree -1,
T   = trace,                       degree -2,
U   = metric insertion,            degree +2,
q(p)=p^2.
```

The important point is not the notation but the invariant operations: gradient,
divergence, trace, and metric insertion. Acting on the same polynomial verifies

```text
[A_p,P_p]=q(p),
[T,P_p]=2A_p,
[A_p,U]=2P_p.
```

These three commutators replace every component expansion used below.

Gauge invariance forces the parameter and field carriers

```text
G_s=ker T in Sym^(s-1)(V_C^*),
F_s=ker T^2 in Sym^s(V_C^*).
```

For `s=1`, the unavailable traces are simply zero. For `s>=2`, the restrictions
remove precisely the traces that would obstruct the uniform identities; they are
structural inputs of this constrained potential realization, not consequences of
Poincare symmetry alone.

## 2. Five objects generate the equation

On these carriers define

```text
R_s(p)=P_p,
C_s(p)=A_p-(1/2)P_p T,
M_s=identity-(1/4)U T.
```

`R_s` is the gauge change. `C_s` is constructed by asking for a divergence whose
composite with a gauge change becomes the scalar wave symbol. Let
`epsilon in G_s`. Using the two commutators above on that same input gives

```text
C_s R_s epsilon
 =A_pP_p epsilon-(1/2)P_pTP_p epsilon
 =P_pA_p epsilon+q epsilon
   -(1/2)P_p(P_pT epsilon+2A_p epsilon)
 =q epsilon,
```

because `T epsilon=0`. Thus

```text
C_sR_s=q identity_(G_s).
```

The local gauge equation is now derived as the defect of the scalar wave operator
along the gauge direction:

```text
D_s(p)=q(p)identity_(F_s)-R_s(p)C_s(p).
```

Applying it to a gauge change computes

```text
D_sR_s
 =qR_s-R_sC_sR_s
 =qR_s-R_sq
 =0.
```

Hence the equation is gauge invariant. The same definition also exposes its
normally hyperbolic completion:

```text
D_s+R_sC_s=q identity_(F_s).
```

Finally, the Euler operator is not guessed independently:

```text
E_s=M_sD_s.
```

For `s>=2`, trace algebra on `ker T^2` gives the executable inverse

```text
M_s^(-1)=identity-[1/(4(s-1))]U T;
```

for `s=1`, `M_1=identity`.

## 3. One adjoint identity constructs admissible sources

Use the invariant Fischer pairing on symmetric tensors. It makes

```text
P_p^dagger=A_p,
U^dagger=T.
```

For the same `epsilon in G_s` and `phi in F_s`, evaluate

```text
<R_s epsilon,M_s phi>
 =<epsilon,A_pM_s phi>,

A_pM_s phi
 =C_s phi-(1/4)U A_pT phi.
```

The last term pairs to zero because

```text
<epsilon,U A_pT phi>=<T epsilon,A_pT phi>=0.
```

Therefore the constrained adjoint is

```text
R_s^dagger M_s=C_s.
```

A source is observable only when a gauge change does not alter its pairing. This
constructs the source condition

```text
R_s^dagger J=0.
```

Set `S=M_s^(-1)J`. The adjoint identity then computes

```text
C_sS
 =R_s^dagger M_sM_s^(-1)J
 =R_s^dagger J
 =0.
```

Thus source conservation and the wave gauge condition are the same statement after
the explicit pairing conversion `M_s^(-1)`.

## 4. The null shell returns the helicity fiber

Let `k` be nonzero and null. Then `q(k)=0`, so

```text
D_s(k)phi=-P_kC_s(k)phi.
```

Multiplication by the nonzero linear polynomial `P_k` is injective; consequently

```text
D_s(k)phi=0 iff C_s(k)phi=0.
```

Restrict such a polynomial to `k^perp`. The equation says it is constant along the
radical `span(k)`, so it descends to the Euclidean screen

```text
Q_k=k^perp/span(k).
```

Call the descended trace-free polynomial `res_k(phi)`. Its kernel is exactly gauge:

```text
res_k(phi)=0
  => phi=P_k psi
  => 0=C_s(k)phi=-(1/2)P_k^2T psi
  => T psi=0
  => phi=R_s(k)psi.
```

Conversely, a trace-free screen polynomial can be extended constantly along one
chosen null complement; that lift satisfies `C_s(k)phi=0`. The choice changes the
lift only by the gauge kernel just computed. Hence

```text
ker D_s(k)/im R_s(k)
  ~=Sym_0^s(Q_k tensor C)^*
  ~=C_(+s) direct-sum C_(-s).
```

This quotient is the N3 realization criterion. Spin is recovered from the field
equation rather than inferred from its tensor rank.

## 5. The same machine generates causal response

Replace `q` by the scalar wave operator on the two finite-rank constrained bundles.
Let `G_(F,s)^+/-` be its retarded/advanced Green maps on `F_s`. For an admissible
compact source define

```text
phi_J^+/-=G_(F,s)^+/- M_s^(-1)J.
```

The previous source computation already gave `C_sM_s^(-1)J=0`. Commutation with
the scalar Green map therefore yields

```text
C_s phi_J^+/-=0,

E_s phi_J^+/-
 =M_s(q-R_sC_s)G_(F,s)^+/-M_s^(-1)J
 =J.
```

Thus retarded and advanced response are consequences of the same five objects.
Their difference `Delta_(F,s)` produces the causal map

```text
[J]
  |-> [Delta_(F,s)M_s^(-1)J]
```

from compact conserved sources modulo equation sources to spacelike-compact
solutions modulo gauge. N4f proves this map is bijective by the two scalar-wave
exact sequences; this synthesis does not repeat that support proof.

## 6. The same source produces a particle amplitude

Fourier transform the trace-reversed source and restrict it to the future null
orbit:

```text
W_s[J](p)=res_p(M_s^(-1)J_hat(p)),
p^2=0,
p^0>0.
```

Changing `J` by `E_sa` changes the shell datum by

```text
M_s^(-1)E_sa=D_sa=-R_sC_sa
```

on `p^2=0`; `res_p` kills this gauge image. Therefore `W_s` depends only on the
source class. The positive screen metric and invariant orbit measure construct

```text
||[J]||_+^2
 =integral_(O_+) ||W_s[J](p)||_(Q_p)^2 dmu_0(p).
```

N4h proves `ker W_s=0` on N4f's real causal quotient by a support-preserving
compatibility-complex argument. Thus this formula is already a norm on that
quotient; no extra spectral quotient is required. Completing it gives a closed
Poincare-invariant subrepresentation with helicity fiber `+s direct-sum -s`.
N4g owns the analytic details. Only density in the whole induced `L2` space
remains open.

## 7. Maxwell and spin two are evaluations, not separate derivations

| Input | Evaluated machine | Physical output |
| --- | --- | --- |
| `s=1` | `G_1=C`, `F_1=V_C^*`, `R=P`, `C=A`, `M=identity`, `D=q-PA` | Maxwell potential, screen `Q_k`, helicities `+1 direct-sum -1` |
| `s=2` | `G_2=V_C^*`, `F_2=Sym^2(V_C^*)`, `M=identity-(1/4)UT`, `D=q-RC` | metric potential, trace-reversed conserved source, helicities `+2 direct-sum -2` |

The higher-spin continuation changes only the symmetric degree and trace
constraints. It does not add a new component numerator or polarization formula.

## 8. Computability and semantic cost

For a fixed finite `s`, the constructor is executable in this order:

| Input | Operation | Checkable output |
| --- | --- | --- |
| spin label `s` | symmetric functors plus `ker T`, `ker T^2` | typed carriers `G_s,F_s` |
| `p` and the metric | build `P,A,T,U` | natural maps without a basis |
| carriers | evaluate `CR=q` and `D=q-RC` | gauge-invariant local equation |
| pairing | evaluate `R^dagger M=C` | admissible source and Euler operator |
| null `p` | restrict and divide by `im R` | two helicity lines |
| compact source | apply scalar Green map | retarded/advanced and causal response |
| future shell | apply `res_p` and screen norm | candidate one-particle amplitude |

Carrier dimensions grow with `s`, but the semantic proof depth does not. Optional
finite-rank scripts check low-degree ranks; they do not generate the theorem. This
is the computational reduction: four natural operations and four identities replace
an expanding family of component calculations.

## 9. Scope and proof ownership

This machine covers separate finite, massless, symmetric, parity-paired integer
spins on flat spacetime. It does not cover:

- the shorter chiral single-helicity curvature family constructed in N4;
- the separate half-integer branch beyond N4i/N4j/N4k/N4l: density and CAR
  normalization of its now-faithful positive particle/antiparticle completion;
- massive potentials, mixed symmetry, curved backgrounds, or interactions;
- a countable-spin Hilbert topology;
- the PF-04(b) density theorem left open by N4g.

Technical ownership is deliberately one-way:

| Proof packet | What it proves for this machine |
| --- | --- |
| [N4a](04a-polynomial-complex-details.md) | carrier preservation, polynomial complex, screen exactness |
| [N4c](04c-action-completion-audit.md) | pairing, trace reversal, formal adjoint, Euler operator |
| [N4e](04e-maxwell-green-construction.md) | first complete causal case |
| [N4f](04f-finite-integer-spin-green-construction.md) | uniform finite-spin Green and causal quotient theorem |
| [N4g](04g-positive-frequency-completion.md) | positive shell norm and exact analytic boundary |
| [N4h](04h-support-faithfulness.md) | support-preserving faithfulness of the shell norm |

The present node is the readable constructor consumed by N6/N7. N4q additionally
consumes its scalar Green reuse and gauge quotient as the positive regression case
for genuine observable compression. Those downstream nodes should not reconstruct
the technical packets unless they challenge one of the four identities or an
analytic boundary.
