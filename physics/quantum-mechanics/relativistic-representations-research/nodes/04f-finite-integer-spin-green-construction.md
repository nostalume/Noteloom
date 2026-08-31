# N4f — Causal Green Construction for Every Finite Integer Spin

Status: classical retarded/advanced response, causal source-to-solution quotient, and helicity-shell coincidence supported for every finite symmetric integer spin on four-dimensional Minkowski spacetime  
Consumes: [N4a bosonic potential complex](04a-polynomial-complex-details.md), [N4c variational completion](04c-action-completion-audit.md), [N4d computation interface](04d-computation-interface.md), [N4e Maxwell Green construction](04e-maxwell-green-construction.md), [Maxwell Green contracts](../sources/maxwell-green-contracts.md), and [finite-spin Green contracts](../sources/finite-spin-green-contracts.md)  
Produces: the spin-two Green bridge requested at the frontier and its internally proved extension to every separate finite symmetric integer-spin carrier

Readable synthesis: [N4m finite integer-spin field machine](04m-finite-integer-spin-field-machine.md). This file retains the causal proof rather than serving as the front-door explanation.

## Research contract

- **Question/capability:** does the spin-two Fronsdal/Einstein complex admit a
  genuinely normally hyperbolic completion whose causal quotient recovers helicity
  `+2 direct-sum -2`, and which part of that construction survives for general
  integer spin?
- **Presumptions:** oriented and time-oriented Minkowski spacetime; one fixed finite
  integer `s>=1`; N4a's double-traceless field and traceless gauge-parameter
  carriers; N4c's invariant pairing and trace reversal; compactly supported sources;
  classical free theory.
- **Material bindings:** N4a supplies `R_s,C_s,D_s` and null-shell cohomology; N4c
  supplies `M_s,E_s` and formal self-adjointness; N4e supplies the causal exact-
  sequence method; FG-01 independently checks the spin-two specialization; FG-02
  bounds the abstract gauge theorem.
- **Output:** retarded/advanced sourced solutions, a proved causal isomorphism
  between source and solution quotients, a presymplectic response, Poincare
  covariance, and shell recovery of `Sym_0^s(Q_k tensor C)^*`.
- **Boundary:** each `s` is finite and separate. No half-integer completion,
  countable direct sum, positive-frequency state, Feynman inverse, curved
  background, interaction, or nonlinear gravity is claimed.

No component or polarization calculation is needed. The entire construction uses
the four natural maps `R,C,M,D`, two scalar wave operators on constrained bundles,
and their causal exact sequences.

## 1. Spin two constructs the hyperbolic completion

For `s=2`, the double-trace condition on the symmetric field and the trace condition
on its vector gauge parameter are automatic. Use N4a's maps

```text
R=P,
C=A-(1/2)P T,
D=H_2-R C,
H_2=q identity_(F_2).
```

Here `q=p^2` is the wave symbol. Acting on the same vector gauge parameter
`epsilon`, the commutators `[A,P]=q` and `[T,P]=2A` compute

```text
C R epsilon
 =(A-(1/2)P T)P epsilon
 =P A epsilon+q epsilon-P A epsilon
 =q epsilon
 =H_1 epsilon.
```

Therefore the gauge-degenerate equation and its completion are

```text
D=H_2-R C,
D+R C=H_2=q identity_(F_2).
```

This is the semantic reason de Donder gauge works: `C` measures precisely the
direction on which `D` fails to be the wave operator, and `C R=H_1` makes that
direction executable by a vector wave equation. No coordinate condition has been
added from outside the complex.

N4c's spin-two trace reversal is

```text
M=identity-(1/4)U T,
M^2=identity,
E=M D.
```

The Euler equation is `E phi=J`, while the normally hyperbolic equation will act on
the trace-reversed source `M J`. Keeping these two target meanings distinct avoids
calling `E` itself a scalar wave operator.

## 2. The spin-two identities expose a uniform finite-spin mechanism

For every finite integer `s>=1`, N4a constructs

```text
G_s=ker T in Sym^(s-1)(V_C^*),
F_s=ker T^2 in Sym^s(V_C^*),

R_s=P:G_s->F_s,
C_s=A-(1/2)P T:F_s->G_s,
D_s=H_(F,s)-R_s C_s,

H_(G,s)=q identity_(G_s),
H_(F,s)=q identity_(F_s).
```

The first uniform computation is the spin-two calculation with only one extra
input, `T epsilon=0`:

```text
C_s R_s epsilon
 =A P epsilon-(1/2)P T P epsilon
 =P A epsilon+q epsilon
   -(1/2)P(P T epsilon+2A epsilon)
 =q epsilon
 =H_(G,s)epsilon.
```

Because `q` acts only on spacetime dependence, it preserves both algebraic kernels
`ker T` and `ker T^2`. Thus `H_(G,s)` and `H_(F,s)` are normally hyperbolic wave
operators on finite-rank constrained bundles. They also intertwine the complex:

```text
H_(F,s)R_s=R_s H_(G,s),
C_s H_(F,s)=H_(G,s)C_s.
```

The extension from spin two is therefore not a guessed propagator pattern. The
same evaluated composite constructs it for every fixed finite `s`.

## 3. Trace reversal converts source conservation into gauge condition

N4c constructs on `F_s`

```text
M_s=identity-(1/4)U T,
E_s=M_s D_s.
```

For `s>=2`, `M_s` is an automorphism with

```text
M_s^(-1)=identity-(1/(4(s-1)))U T;
```

for `s=1`, `M_1=identity`. The missing bridge is the constrained adjoint of the
gauge map. Let `epsilon in G_s` and `phi in F_s`. Using `R_s=P`, `P^dagger=A`,
and `[A,U]=2P`, evaluate both sides in the same Fischer pairing:

```text
<R_s epsilon,M_s phi>
 =<epsilon,A M_s phi>,

A M_s phi
 =A phi-(1/4)(U A+2P)T phi
 =C_s phi-(1/4)U A T phi.
```

The last term is pure trace. Since `T epsilon=0`,

```text
<epsilon,U A T phi>=<T epsilon,A T phi>=0.
```

Nondegeneracy on `G_s` therefore constructs the constrained adjoint identity

```text
R_s^dagger M_s=C_s.
```

An admissible source is now typed by gauge invariance:

```text
J in F_(s,c),
R_s^dagger J=0.
```

Set `S=M_s^(-1)J`. Substitution into the constructed adjoint identity gives

```text
C_s S
 =R_s^dagger M_s M_s^(-1)J
 =R_s^dagger J
 =0.
```

For spin two, `R_2^dagger=A`, so this is ordinary stress-tensor conservation and
`S=MJ`. For higher spin, it is exactly the projected divergence condition dictated
by the traceless gauge-parameter carrier.

## 4. Retarded and advanced Green maps solve the Euler equation

MG-01 supplies unique retarded and advanced Green operators

```text
G_(F,s)^+/-: F_(s,c) -> F_(s,sc),
G_(G,s)^+/-: G_(s,c) -> G_(s,sc)
```

for the two normally hyperbolic operators. The intertwining identities and causal
uniqueness compute

```text
G_(F,s)^+/- R_s=R_s G_(G,s)^+/-,
C_s G_(F,s)^+/-=G_(G,s)^+/- C_s.
```

For an admissible source define

```text
phi_J^+/-=G_(F,s)^+/- M_s^(-1)J.
```

Its gauge condition is not imposed afterward:

```text
C_s phi_J^+/-
 =G_(G,s)^+/- C_s M_s^(-1)J
 =0.
```

The same field then solves the original Euler equation:

```text
D_s phi_J^+/-
 =(H_(F,s)-R_s C_s)phi_J^+/-
 =M_s^(-1)J,

E_s phi_J^+/-
 =M_s D_s phi_J^+/-
 =J.
```

Its support lies in the causal future or past of `supp J`. This establishes the
retarded/advanced classical response for every separate finite integer spin.

## 5. The causal map descends to the physical quotient

Let

```text
Delta_(F,s)=G_(F,s)^+-G_(F,s)^-,
Delta_(G,s)=G_(G,s)^+-G_(G,s)^-.
```

Define the compact observable-source quotient and spacelike-compact solution
quotient by

```text
O_s=ker(R_s^dagger:F_(s,c)->G_(s,c))/E_s(F_(s,c)),

S_s={phi in F_(s,sc) | E_s phi=0}/R_s(G_(s,sc)).
```

The denominator of `O_s` really lies in its numerator. Formal self-adjointness and
gauge invariance evaluate, for every compact parameter `epsilon`,

```text
<epsilon,R_s^dagger E_s a>
 =<R_s epsilon,E_s a>
 =<E_s R_s epsilon,a>
 =0.
```

Nondegeneracy gives `R_s^dagger E_s a=0`.

The proposed causal bridge is

```text
I_s:O_s->S_s,
I_s([J])=[Delta_(F,s) M_s^(-1)J].
```

It is well-defined under an equation-source shift. Since
`M_s^(-1)E_s=D_s`, the same compact `a` gives

```text
Delta_(F,s) M_s^(-1)E_s a
 =Delta_(F,s)(H_(F,s)-R_s C_s)a
 =-R_s Delta_(G,s)C_s a.
```

The change is gauge. For `S=M_s^(-1)J`, compute the image on the same source:

```text
C_s Delta_(F,s)S=Delta_(G,s)C_sS=0,

D_s Delta_(F,s)S
 =(H_(F,s)-R_sC_s)Delta_(F,s)S
 =0.
```

Multiplication by `M_s` then gives `E_s Delta_(F,s)S=0`, so the image lies in
the declared solution quotient.

### 5.1 Surjectivity is a gauge-fixing and exact-sequence computation

Take `phi in F_(s,sc)` with `E_s phi=0`; invertibility of `M_s` gives
`D_s phi=0`. The causal exact sequence makes `H_(G,s)` surjective on
spacelike-compact sections, so choose `epsilon in G_(s,sc)` satisfying

```text
H_(G,s)epsilon=-C_s phi.
```

Then

```text
phi'=phi+R_s epsilon,
C_s phi'=C_s phi+H_(G,s)epsilon=0,

D_s phi'
 =D_s phi+(H_(F,s)R_s-R_sH_(G,s))epsilon
 =0,

H_(F,s)phi'=D_s phi'+R_s C_s phi'=0.
```

The field exact sequence supplies `a in F_(s,c)` with
`Delta_(F,s)a=phi'`. Applying `C_s` gives

```text
0=C_s phi'=Delta_(G,s)C_s a.
```

Exactness on the compact parameter carrier constructs `b in G_(s,c)` with

```text
C_s a=H_(G,s)b.
```

Set `a'=a-R_s b`. Then

```text
C_s a'=0,
Delta_(F,s)a'=phi'-R_s Delta_(G,s)b.
```

The second field differs from `phi` only by gauge. Finally set `J=M_s a'`.
The adjoint identity computes `R_s^dagger J=C_s a'=0`, and

```text
I_s([J])=[Delta_(F,s)a']=[phi].
```

### 5.2 Injectivity returns a zero solution to an equation source

Suppose `I_s([J])=0`. Put `S=M_s^(-1)J`; then `C_sS=0` and there is
`chi in G_(s,sc)` with

```text
Delta_(F,s)S=R_s chi.
```

Applying `C_s` computes `H_(G,s)chi=0`. The parameter exact sequence supplies
`b in G_(s,c)` with `chi=Delta_(G,s)b`. Therefore

```text
Delta_(F,s)(S-R_s b)=0,
```

and field exactness constructs `a in F_(s,c)` satisfying

```text
S-R_s b=H_(F,s)a.
```

Apply `C_s` to this same equality:

```text
-H_(G,s)b=H_(G,s)C_s a,
H_(G,s)(b+C_s a)=0.
```

The wave operator has no nonzero compactly supported homogeneous section, hence
`b=-C_s a`. Substitution returns

```text
S=H_(F,s)a-R_s C_s a=D_s a,
J=M_s S=M_s D_s a=E_s a.
```

Thus `[J]=0` in `O_s`, proving that `I_s` is injective. Together with the previous
construction,

```text
O_s ~= S_s
```

for every fixed finite integer `s>=1`.

## 6. The causal response is invariant and antisymmetric

The boundary-selected and causal source responses are

```text
Response_s^+/-([J],[J'])
 =<J,G_(F,s)^+/- M_s^(-1)J'>,

tau_s([J],[J'])
 =<J,Delta_(F,s)M_s^(-1)J'>.
```

Changing `J'` by `E_s a` changes the propagated field by
`-R_s Delta_(G,s)C_s a`, whose pairing with `J` is

```text
<J,R_s xi>=<R_s^dagger J,xi>=0.
```

The wave causal propagator is formally skew-adjoint. Since the algebraic,
self-adjoint `M_s^(-1)` commutes with it,

```text
(Delta_(F,s)M_s^(-1))^dagger
 =-Delta_(F,s)M_s^(-1).
```

Therefore `tau_s` is an antisymmetric, gauge-independent presymplectic response on
`O_s`. Possible global degeneracy outside Minkowski spacetime remains a topology
and support question rather than a local spin equation.

## 7. The causal shell recovers helicity `+s direct-sum -s`

Translation invariance makes the causal wave distribution shell-supported at
`p^2=0`. At a nonzero null momentum `k`, an admissible source gives

```text
S(k)=M_s^(-1)J(k),
C_s(k)S(k)=0,
D_s(k)S(k)=-R_s(k)C_s(k)S(k)=0.
```

Thus the numerator lands directly in N4a's field cohomology. N4a's exact screen
sequence then computes

```text
[S(k)] in ker D_s(k)/im R_s(k)
       ~=Sym_0^s(Q_k tensor C)^*
       ~=C_(+s) direct-sum C_(-s).
```

For `s=2`, `M_2^(-1)=M_2`. On the two-dimensional screen its induced action is

```text
j |-> j-(1/2)metric_Q trace_Q(j),
```

which removes the pure trace and retains the two circular trace-free lines. This is
the promised spin-two path:

```text
conserved compact stress source
  -> trace-reversed causal solution
  -> de Donder solution class
  -> trace-free screen class
  -> helicity +2 direct-sum -2.
```

For general finite `s`, the same conclusion comes from the exact screen map rather
than a component numerator or polarization sum.

The causal propagator still contains both energy signs. [N4g](04g-positive-frequency-completion.md)
now constructs the additional future-shell map, positive norm, and spectral complex
structure. [N4h](04h-support-faithfulness.md) proves that this norm is faithful on
the present spacelike-compact causal quotient. Equality of the completion with the
whole N3 Hilbert space is the remaining support-completion contract PF-04(b).

## 8. Covariance, checks, and open boundary

Every carrier, constraint, and map is constructed from the Minkowski metric,
symmetrization, trace, and derivative. A proper orthochronous Poincare
transformation therefore intertwines `R_s,C_s,M_s,H_(F,s),H_(G,s)`. It also
preserves retarded and advanced support. Uniqueness of the Green operators then
computes covariance of `G^+/-`, `Delta`, `I_s`, and `tau_s`. Time reversal exchanges
the two boundary prescriptions.

| N4d obligation | Supported finite-integer-spin result | Boundary |
| --- | --- | --- |
| inverse modulo gauge | `G_(F,s)^+/-M_s^(-1)` solves `E_s phi=J` | projected-conserved compact sources |
| typed complex identities | `D_s+R_sC_s=q identity` and the two causal exact sequences | one fixed finite `s` |
| covariance | proper orthochronous Poincare covariance by naturality and uniqueness | time reversal exchanges `+/-` |
| gauge independence | `I_s` and source response descend through `E_s(F_c)` | classical exact gauge complex |
| residue/cohomology | shell numerator lands in `Sym_0^s(Q_k tensor C)^*` | nonzero null momentum |
| analytic validity | finite-rank bundles, compact/sc domains, causal support, and boundary prescription stated | no wavefront products or state selection |

Independent checks are supplied by FG-01 for spin two and by N4a's existing
finite-rank computation packet for low spins. The proof above remains invariant and
uniform in the label; the finite-rank script is not its logical basis.

The result does **not** complete a countable tower. Passing from all separate finite
labels to a single infinite carrier requires a topology, common dense domain,
continuity of `M_s^(-1)`, and Green estimates uniform in `s`. N4i now completes the
half-integer pairing, self-adjoint Euler operator, wave reduction, and admissible
response, while N4j completes its causal quotient theorem. Curved backgrounds add
curvature terms and topology; interactions change
the gauge complex itself.

## Edges

- `N4a/N4c -> N4f`: the polynomial complex, constrained pairing, trace reversal,
  and Euler operator construct the finite-spin Green data.
- `N4e -> N4f`: the Maxwell causal exact-sequence method is generalized after its
  spin-two test succeeds.
- `N4f -> N7`: source/solution equivalence and causal response are now available
  for comparison across every finite symmetric integer spin.
- `N4f -> N4g`: the real causal quotient and its two-sign shell are the input to
  positive-frequency completion.
- `N4f -> N4m`: the uniform causal theorem is condensed into the readable field
  constructor; its proof remains here.
