# N4e — Causal Green Construction for the Maxwell Complex

Status: classical retarded/advanced Maxwell response and causal source-to-solution quotient supported on four-dimensional Minkowski spacetime; finite symmetric integer-spin generalization completed in N4f  
Consumes: [N3b massless helicity one](03b-massless-helicity-one.md), [N4c variational completion](04c-action-completion-audit.md), [N4d algebraic computation interface](04d-computation-interface.md), and [Maxwell Green contracts](../sources/maxwell-green-contracts.md)  
Produces: a typed Green completion of the free Maxwell potential complex, an intrinsic causal observable quotient, and the exact obstruction list for finite-spin generalization

## Research contract

- **Question/capability:** can the representation-correct Maxwell complex compute a
  causal sourced field and an on-shell observable without choosing polarization
  components or treating a rational pole as a Green distribution?
- **Presumptions:** oriented and time-oriented Minkowski spacetime `M`; metric
  convention inherited from N3b; smooth real or complex differential forms;
  compactly supported sources; exact gauge transformations; classical linear
  theory.
- **Material bindings:** N3b supplies the null physical quotient; N4c supplies the
  pairing, formal adjoint, and source meaning; N4d supplies the six compatibility
  obligations; MG-01--MG-03 delimit the analytic theorem contracts.
- **Output:** retarded and advanced Maxwell response, causal propagator, source and
  solution quotients, presymplectic response, Poincare covariance, and an explicit
  Fourier-fiber map back to `Q_p=p^perp/span(p)`.
- **Boundary:** no Feynman inverse, positive-frequency state, quantization,
  interacting response, curved-background topology, or arbitrary-spin Green
  theorem is claimed.

No heavy computation packet is needed. Every supported identity is an operation on
the de Rham complex, a support/uniqueness argument, or a one-shell quotient.

## 1. Gauge degeneracy constructs the hyperbolic completion

Let `Omega_c^r(M)` denote compactly supported smooth `r`-forms and
`Omega_sc^r(M)` smooth forms with spacelike-compact support. The exterior
differential and its formal adjoint are typed as

```text
d:     Omega^r(M) -> Omega^(r+1)(M),
delta: Omega^r(M) -> Omega^(r-1)(M).
```

Their nilpotence is

```text
d d=0,
delta delta=0.
```

The potential equation constructed in N3b is

```text
K=delta d: Omega^1(M) -> Omega^1(M).
```

It cannot possess a two-sided Green inverse on the whole potential carrier. On
the same compact scalar `alpha`, direct evaluation gives

```text
K(d alpha)=delta d d alpha=0.
```

Thus `im d` is a nonzero kernel before any characteristic or boundary issue is
considered. The needed operation is not inversion of `K`, but completion by the
adjoint gauge direction:

```text
P_r=d delta+delta d: Omega^r(M) -> Omega^r(M).
```

For `r=1`, the added term is inactive on the Lorenz subspace `ker delta`, while it
supplies an equation along `im d`. On flat Minkowski spacetime `P_r` is the
normally hyperbolic de Rham wave operator. MG-01 therefore supplies unique maps

```text
G_r^+/-: Omega_c^r(M) -> Omega_sc^r(M)
```

such that

```text
P_r G_r^+/- f=f,
G_r^+/- P_r f=f,
supp(G_r^+ f) subset J^+(supp f),
supp(G_r^- f) subset J^-(supp f).
```

Here `+` means retarded and `-` advanced. Causal support is additional analytic
data; it is not encoded by the polynomial symbol of `P_r`.

## 2. Commutation with the complex is computed by uniqueness

Nilpotence first computes the operator identities on an arbitrary form:

```text
P_(r+1)d
 =(d delta+delta d)d
 =d delta d
 =d(d delta+delta d)
 =d P_r,

P_(r-1)delta
 =(d delta+delta d)delta
 =delta d delta
 =delta(d delta+delta d)
 =delta P_r.
```

Now take `f in Omega_c^r(M)`. Both `d G_r^+ f` and `G_(r+1)^+ d f`
have support in `J^+(supp f)`, and evaluation by the same target operator gives

```text
P_(r+1)d G_r^+ f=d f,
P_(r+1)G_(r+1)^+ d f=d f.
```

Uniqueness of the retarded solution supplies their semantic coincidence. The same
calculation applies to the advanced prescription and to `delta`, producing

```text
d G_r^+/-=G_(r+1)^+/- d,
delta G_r^+/-=G_(r-1)^+/- delta.
```

The equations are therefore consequences of one common sourced problem with one
common support condition, not formal movement of symbols past each other.

## 3. A conserved source constructs the causal Maxwell response

An admissible current is

```text
J in Omega_c^1(M),
delta J=0.
```

Define the boundary-selected potentials and their curvatures by

```text
A^+/-=G_1^+/- J,
F^+/-=d A^+/-.
```

The commutation result computes the Lorenz condition:

```text
delta A^+/-
 =delta G_1^+/- J
 =G_0^+/- delta J
 =0.
```

Consequently the completed equation reduces to the Maxwell equation on the same
field:

```text
delta d A^+/-
 =(P_1-d delta)A^+/-
 =J.
```

Applying `d` and `delta` to the constructed curvature yields

```text
d F^+/-=d d A^+/-=0,
delta F^+/-=delta d A^+/-=J.
```

This is the first predictive output: a compact conserved current produces the
unique retarded or advanced Lorenz representative, and `F^+/-` is independent of
any later replacement `A^+/- -> A^+/-+d chi`.

A second conserved test current `J'` also removes the representative at the
observable:

```text
<J',A+d chi>-<J',A>
 =<J',d chi>
 =<delta J',chi>
 =0.
```

The equality uses compact overlap to remove the boundary term. Gauge independence
is computed at the field strength and source response, not asserted for the
potential representative.

## 4. The inverse and the on-shell propagator are different maps

Construct the causal propagator by subtracting the two boundary solutions:

```text
E_r=G_r^+-G_r^-: Omega_c^r(M) -> Omega_sc^r(M).
```

Evaluation shows that it is not another sourced inverse:

```text
P_r E_r f=f-f=0,
E_r P_r f=f-f=0.
```

It sends a source to the difference of its retarded and advanced responses, hence
to a homogeneous radiative solution.

The retarded and advanced maps separately contract the compactly supported de
Rham complex. Define

```text
h_r^+/-=delta G_r^+/-: Omega_c^r(M) -> Omega^(r-1)(M).
```

Then commutation computes

```text
d h_r^+/-+h_(r+1)^+/- d
 =d delta G_r^+/-+delta G_(r+1)^+/- d
 =(d delta+delta d)G_r^+/-
 =identity.
```

By contrast, their difference obeys

```text
d(delta E_r)+(delta E_(r+1))d=P_r E_r=0.
```

This corrects the provisional N4d picture. The sourced homotopy has right-hand
side `identity`; the causal map has right-hand side zero. A shell projector is a
third object and requires a spectral splitting not needed here.

MG-01 supplies the exact sequence

```text
0 -> Omega_c^r --P_r--> Omega_c^r --E_r--> Omega_sc^r
  --P_r--> Omega_sc^r -> 0.
```

Its semantic content is precise: `ker E_r=im P_r`, and every spacelike-compact
homogeneous wave is represented by a compact source modulo `P_r`.

## 5. Source quotient and solution quotient coincide

Gauge invariance first constructs the compact source space

```text
J_c=ker(delta:Omega_c^1 -> Omega_c^0).
```

Two such sources define the same on-shell linear observable when they differ by
the formally self-adjoint field equation:

```text
O_Max=J_c/(delta d Omega_c^1).
```

The denominator lies in `J_c` because `delta delta=0`. On the solution side use

```text
S_Max,sc={A in Omega_sc^1 | delta d A=0}/d Omega_sc^0.
```

The causal map proposes

```text
I: O_Max -> S_Max,sc,
I([J])=[E_1 J].
```

It is well-defined by a direct computation. For `a in Omega_c^1`, use
`delta d=P_1-d delta`, the exact-sequence identity `E_1 P_1=0`, and commutation:

```text
E_1(delta d a)
 =E_1(P_1-d delta)a
 =-d E_0(delta a).
```

The change is exact and therefore zero in `S_Max,sc`. Also

```text
delta(E_1 J)=E_0(delta J)=0,
delta d(E_1 J)=(P_1-d delta)E_1 J=0,
```

so the image is a Lorenz representative of a Maxwell gauge class.

MG-02 supplies the remaining global theorem contract: on a globally hyperbolic
spacetime with these exact-gauge and support conventions, the causal exact sequence
and existence of Lorenz representatives make `I` an isomorphism. N4e internally
constructs its well-definedness and specializes the result to Minkowski spacetime;
it does not silently transfer the claim to other gauge notions or topologies.

## 6. The causal response is an observable pairing

Define

```text
tau([J],[J'])=<J,E_1 J'>.
```

Changing the second source by `delta d a` gives

```text
<J,E_1 delta d a>
 =-<J,d E_0 delta a>
 =-<delta J,E_0 delta a>
 =0.
```

The same holds in the first slot. Formal self-adjointness of `P_1` makes the
retarded and advanced operators adjoint to one another, so

```text
E_1^dagger=(G_1^+)^dagger-(G_1^-)^dagger
           =G_1^--G_1^+
           =-E_1.
```

Therefore

```text
tau([J],[J'])=-tau([J'],[J]).
```

This presymplectic response is the global, causal version of N4d's conserved-source
pairing. Nondegeneracy on a broader spacetime is a support-cohomology question,
not a consequence of the local Maxwell symbol; MG-03 owns that boundary.

## 7. Poincare covariance follows from the same uniqueness witness

Let `U_g` be the pullback action of a proper orthochronous Poincare transformation.
Metric and orientation preservation compute

```text
U_g d=d U_g,
U_g delta=delta U_g,
U_g P_r=P_r U_g.
```

Time-orientation preservation also gives

```text
U_g J^+(S)=J^+(U_g S),
U_g J^-(S)=J^-(U_g S).
```

For the same compact input `f`, both `U_g G_r^+/- f` and
`G_r^+/- U_g f` solve the transformed source equation with the same causal support.
Uniqueness therefore yields

```text
U_g G_r^+/-=G_r^+/- U_g,
U_g E_r=E_r U_g.
```

Time reversal exchanges the two support prescriptions rather than preserving each
one. The supported covariance group is therefore stated rather than inferred from
the symbol alone.

## 8. The shell quotient recovers the helicity fiber

Translation invariance permits Fourier transformation. Up to Fourier and sign
conventions, `G^+/-` are distinct boundary values of the scalar wave denominator
on each form carrier, while their difference has support on

```text
p^2=0.
```

No explicit matrix numerator is required. At a nonzero null momentum `p`, current
conservation becomes

```text
p.J(p)=0,
```

so the current value lies in `p^perp`. A source-equation shift has symbol

```text
(delta d)(p)a=p^2 a-p(p.a).
```

Restricting the same operation to `p^2=0` gives

```text
(delta d)(p)a=-p(p.a) in span(p).
```

Thus the source quotient carried by the causal shell is exactly

```text
p^perp/span(p)=Q_p.
```

The induced metric pairing is representative-independent because `span(p)` is the
radical of the metric on `p^perp`. This computes the semantic route

```text
compact conserved source class
  -> causal Maxwell solution class
  -> null-shell current class
  -> intrinsic screen quotient Q_p
  -> helicity +1 direct-sum -1 from N3b.
```

The causal propagator contains both energy signs. [N4g](04g-positive-frequency-completion.md)
now restricts it to the positive orbit and constructs the compatible screen norm
and complex structure uniformly for finite integer spin.
[N4h](04h-support-faithfulness.md) proves support-preserving faithfulness on
Minkowski spacetime. Compact-source density remains the exact boundary before
equality with the whole N3b one-particle Hilbert representation.

## 9. Compatibility audit and generalization boundary

| N4d obligation | Maxwell result | Boundary |
| --- | --- | --- |
| inverse modulo gauge | `A^+/-=G_1^+/-J` solves `delta d A=J` in Lorenz gauge | compact conserved sources |
| typed complex identities | sourced homotopy gives `identity`; causal difference gives zero | no universal shell projector |
| covariance | proper orthochronous Poincare covariance follows from uniqueness | time reversal exchanges prescriptions |
| gauge independence | curvature and conserved-source pairing remove exact changes | exact-gauge convention |
| residue/cohomology | shell source quotient is `Q_p` | nonzero null momentum |
| analytic validity | domain, range, causal support, and boundary prescription are explicit | wavefront products and Feynman/state data open |

The construction exposes the reusable finite-spin contract. A new gauge complex
can inherit this route only after it supplies:

1. a formally self-adjoint gauge completion `P` on the constrained carrier;
2. normal or Green hyperbolicity of `P` on declared support spaces;
3. commutation of `P` and its Green operators with the complex maps;
4. a source constraint that removes gauge representatives from observables;
5. a causal exact sequence inducing source/solution quotient coincidence;
6. a shell calculation identifying the quotient with the N3/N4 little-group
   cohomology.

N4f now executes this contract for the whole separate finite symmetric integer-spin
family. Its decisive new identities are `D_s+R_sC_s=q identity` on the constrained
bundles and `R_s^dagger M_s=C_s` in the constrained pairing. This promotion does
not make the half-integer family or a countable-spin sum automatic: N4i supplies
the former's pairing, adjoint, wave reduction, and admissible response, while N4j
completes its causal quotient theorem; the latter needs a common topology, dense
domain, and estimates uniform in spin.

## Edges and open boundary

- `N3b -> N4e`: the intrinsic helicity-one quotient is the shell result that the
  causal observable must recover.
- `N4c/N4d -> N4e`: pairing, adjoint, source typing, and compatibility obligations
  determine what must be computed.
- `N4e -> N7`: the causal source/solution quotient is the first stronger-than-
  representation equivalence available for comparison.
- `N4e -> N4f`: only the six-item reusable contract passes forward;
  Maxwell-specific de Rham identities do not.

N4g now supplies a faithful positive-frequency pre-Hilbert completion, with N4h
providing the support proof. Still open are its full induced-space density theorem,
Feynman and Hadamard constructions,
half-integer density beyond N4i/N4j/N4k/N4l (N4z closes CAR normalization),
countable-spin completion, topology-sensitive
sectors, and every interaction deformation.
