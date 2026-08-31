# N4g — Positive-Frequency Completion of the Causal Quotient

Status: invariant and faithful future-shell pre-Hilbert map supported for every separate finite integer spin; equality with the full N3 Hilbert space remains the PF-04(b) density theorem  
Consumes: [N2 orbit measure](02-three-representation-spaces.md), [N2a helicity fiber](02a-spin-and-helicity.md), [N3 realization bridge](03-realization-bridge.md), [N4a screen complex](04a-polynomial-complex-details.md), [N4f causal quotient](04f-finite-integer-spin-green-construction.md), and [positive-frequency contracts](../sources/positive-frequency-contracts.md)  
Produces: a positive-energy shell map, positive norm, compatible complex structure, and an explicit comparison with the N3 induced representation

Readable synthesis: [N4m finite integer-spin field machine](04m-finite-integer-spin-field-machine.md). This file owns only the spectral construction and its analytic boundary.
Support proof: [N4h support-preserving faithfulness](04h-support-faithfulness.md).

## Research contract

- **Question:** how does N4f's real causal solution quotient, which contains both
  energy signs, become a positive-energy one-particle representation?
- **Presumptions:** oriented and time-oriented Minkowski spacetime; one fixed
  finite integer `s>=1`; real compact smooth admissible sources; the Fourier
  convention

  ```text
  f(x)=integral exp(-i p.x) f_hat(p) d4p,
  i partial_mu |-> p_mu;
  ```

  N4f's source/solution isomorphism; and N2's positive null-orbit measure.
- **Output:** an injective real-linear future-shell map from the causal source
  quotient, its positive pre-Hilbert norm and Hilbert completion, the induced
  proper-orthochronous Poincare action, and its relation to the causal form.
- **Boundary:** N4h discharges support-preserving faithfulness on Minkowski
  spacetime. Density in the entire N3 `L2` space remains a separate analytic
  contract. No Fock space, vacuum uniqueness, Feynman inverse,
  half-integer completion, countable-spin topology, or interaction is claimed.

The construction is one semantic chain:

```text
real compact observable source class
  -> trace-reversed Fourier source
  -> future null-shell cohomology class
  -> positive screen norm
  -> Hilbert completion
  -> positive-energy induced Poincare representation.
```

The first arrow is local and compactly supported. Selecting one connected shell is
necessarily spectral and nonlocal in spacetime; this is precisely the additional
structure that a one-particle state requires.

## 1. Why the causal quotient is not yet a particle Hilbert space

N4f constructs the real source quotient

```text
O_s^R
 =ker(R_s^dagger:F_(s,c)^R->G_(s,c)^R)/E_s(F_(s,c)^R)
```

and the causal solution class

```text
I_s([J])=[Delta_(F,s) M_s^(-1)J].
```

The Fourier support of `Delta_(F,s)` is the whole nonzero null shell. It therefore
contains two Poincare orbits:

```text
O_+={p | p^2=0, p^0>0},
O_-=-O_+.
```

Reality ties them together but does not turn either one into a Hilbert norm. Three
new operations are required and must not be conflated:

1. restrict the causal datum to `O_+`;
2. use the positive screen metric to measure that datum;
3. complete the finite-norm source classes.

Positive frequency selects the energy orbit. It does **not** select a helicity.
The symmetric potential still carries `+s direct-sum -s` on `O_+`.

## 2. The positive orbit already carries the required measure

N2 constructs the Lorentz-invariant measure by restricting four-volume:

```text
dmu_0(p)=d4p delta(p^2) theta(p^0)
         =d3p/(2|p|),
```

up to one overall constant. The origin is removed because it is a different orbit;
it also has zero `dmu_0` measure. No equal-time coordinates enter the definition.

For every `p in O_+`, N2a constructs the Euclidean screen

```text
Q_p=p^perp/span(p),
<[x],[y]>_Q=-eta(x,y).
```

Functoriality gives the positive Hermitian fiber

```text
H_s(p)=Sym_0^s(Q_p tensor C)^*.
```

N4a has already computed its little-group representation:

```text
H_s(p) ~= C_(+s) direct-sum C_(-s).
```

Thus both the integration rule and the positive fiber metric are constructed before
the source map. They are not inferred from a component polarization sum.

## 3. A compact source constructs its future-shell amplitude

Let `J` be a real admissible source and define its trace-reversed Fourier datum

```text
S_J(p)=M_s^(-1) J_hat(p).
```

Source admissibility and N4f's constrained-adjoint identity compute, at every
momentum,

```text
C_s(p)S_J(p)
 =R_s(p)^dagger M_s M_s^(-1)J_hat(p)
 =R_s(p)^dagger J_hat(p)
 =0.
```

At `p in O_+`, `D_s(p)=p^2-R_s(p)C_s(p)` therefore also kills `S_J(p)`. N4a's
screen restriction can be applied without choosing a polarization:

```text
w_s[J](p)=res_p(S_J(p)) in H_s(p).
```

This is the promised realization bridge. Every operation has an executable
meaning:

```text
J_hat(p)
  --M_s^(-1)--> source datum satisfying the gauge constraint
  --restrict to p^perp--> polynomial constant along span(p)
  --descend--> trace-free polynomial on Q_p.
```

Because `J` is smooth and compactly supported, `J_hat` decreases rapidly on real
momentum after multiplying by any polynomial. The finite algebraic map `M_s^(-1)`
and screen descent introduce no momentum pole. Hence `w_s[J]` is square-integrable
on `O_+`.

## 4. The amplitude depends only on the source class

Take another representative `J'=J+E_s a` with compact `a`. N4f gives

```text
M_s^(-1)E_s a=D_s a.
```

On the null shell, the homotopy identity becomes

```text
D_s(p)a_hat(p)=-R_s(p)C_s(p)a_hat(p).
```

N4a proves that `res_p` has exactly `im R_s(p)` as its kernel. Applying it to the
same difference computes

```text
w_s[J'](p)-w_s[J](p)
 =res_p(D_s(p)a_hat(p))
 =-res_p(R_s(p)C_s(p)a_hat(p))
 =0.
```

Therefore the map descends:

```text
W_s:O_s^R -> L2(O_+,dmu_0;H_s),
W_s[J]=w_s[J].
```

This quotient computation is the reason for using source classes. Restricting an
arbitrary potential representative to the shell would leave a gauge-dependent
answer.

## 5. Reality and support cohomology prove faithfulness

For a real source, Fourier conjugation gives

```text
J_hat(-p)=overline(J_hat(p)).
```

All maps `M_s,R_s,C_s` and screen descent are real. Under the canonical
identification `Q_(-p)=Q_p`, the past-shell amplitude is therefore the complex
conjugate of the future-shell amplitude. The future datum determines the entire
real causal shell.

Suppose `W_s[J]=0`. Reality makes the past-shell datum zero as well. PF-01 supplies
the retarded/advanced Green operators. In Minkowski momentum space their scalar
parts are the two boundary values of `1/p^2`; applying
`1/(x+i0)-1/(x-i0)=-2 pi i delta(x)` at the two signs of `p^0` computes, for one
nonzero convention constant `c_Delta`,

```text
Fourier(Delta_(F,s)S_J)
 =c_Delta sign(p^0)delta(p^2)S_J(p).
```

Its physical screen class vanishes on both shell components. N4a's exact screen
sequence constructs a gauge amplitude at every shell momentum. The missing support
step is now supplied by N4h: the complete compatibility complex of `R_s` has
degree-one spacelike-compact cohomology

```text
H_sc^1(M;Kill_s)
 ~=H_c^1(R^3;Z_s)
 =0.
```

Consequently the shellwise gauge amplitude assembles into one
`chi in G_(s,sc)`. N4f's injective causal map then computes

```text
W_s[J]=0
  => Delta_(F,s)M_s^(-1)J=R_s chi
  => I_s([J])=0
  => [J]=0.
```

Thus `W_s` is faithful. For arbitrary complex solutions the first reduction would
still fail: a nonzero negative-frequency solution can have zero future restriction.
The real form must be selected before positive completion.

## 6. The screen metric constructs the one-particle norm

Let `h_(s,p)` be the Hermitian metric on `H_s(p)` induced functorially from the
Euclidean metric of `Q_p`. Define

```text
z_s([J],[K])
 =integral_(O_+) h_(s,p)(W_s[J](p),W_s[K](p)) dmu_0(p),

mu_s([J],[K])=Re z_s([J],[K]),
||[J]||_+^2=mu_s([J],[J]).
```

The integrand is nonnegative, and N4h proves its null space is zero:

```text
||[J]||_+=0
  iff W_s[J]=0
  iff [J]=0.
```

Consequently `O_s^R` itself is a positive real pre-Hilbert space. Its complex
one-particle completion is

```text
H_(src,s)=closure_C(W_s(O_s^R))
  subseteq L2(O_+,dmu_0;H_s).
```

This definition no longer needs an extra spectral null quotient. It does not
presume density: it records exactly what the compact causal sources generate.

## 7. Covariance computes the induced action

Let `g=(a,A)` belong to the proper orthochronous Poincare group and put
`q=A^(-1)p`. Naturality of `M_s` and of the screen quotient gives a fiber isometry

```text
A_Q:H_s(q)->H_s(p).
```

Fourier transformation of the covariant source action then computes

```text
W_s(g.J)(p)
 =exp(i p.a) A_Q W_s(J)(A^(-1)p).
```

The orbit measure is invariant and `A_Q` preserves the screen metric, so direct
substitution gives

```text
||W_s(g.J)||_+^2=||W_s(J)||_+^2.
```

To compare with N2/N3, choose standard transports `B(p)k=p` only as fiber
coordinates. Then `A_Q` at the standard fiber becomes the Wigner transformation

```text
W(A,p)=B(p)^(-1)A B(A^(-1)p),
```

and the preceding source action reads

```text
[U_s(a,A)psi](p)
 =exp(i p.a) sigma_(+s direct-sum -s)(W(A,p))
  psi(A^(-1)p).
```

This is exactly N2's induced action. Hence `H_(src,s)` is a closed invariant
subrepresentation of N3's positive-energy helicity-pair Hilbert representation.
No new component calculation is needed to identify it.

## 8. The causal form is the imaginary part of the positive norm

On the realification of the completed future-shell image, define the spectral
complex structure by

```text
J_s: future amplitude |-> +i times future amplitude,
     past amplitude   |-> -i times past amplitude.
```

The negative shell is reconstructed by conjugation. Direct application twice gives

```text
J_s^2=-identity.
```

The boundary-value computation places opposite signs on the two shell components.
Substituting the reality relation into N4f's causal response therefore reduces its
two shell integrals to one:

```text
tau_s([J],[K])
 =kappa_s 2 Im z_s([J],[K]),
```

where `kappa_s` is a nonzero real constant fixed by the Fourier convention, the
choice `Delta=G^+-G^-`, the overall action normalization, and the rank-`s` sign of
the Lorentz Fischer pairing on the spacelike screen. No momentum-dependent or
helicity-dependent factor remains.

Multiplying the free action by the constant sign of `kappa_s` changes no equation
or gauge quotient and gives the compatible normalization

```text
omega_s(u,v)=2 Im <u,v>_+,
mu_s(u,v)=omega_s(u,J_s v)=2 Re <u,v>_+.
```

Here `<.,.>_+` denotes the continuous extension of `z_s` to `H_(src,s)`.

Thus positivity is not obtained from an indefinite Lorentz-carrier norm. It is
constructed only after equation cohomology has reduced the carrier to the Euclidean
screen and positive energy has selected one orbit.

## 9. Exact supported result and remaining theorem

For every separate finite integer `s>=1`, the work above proves:

```text
O_s^R
  --injective isometric positive-energy intertwiner W_s-->
L2(O_+,dmu_0;C_(+s) direct-sum C_(-s)),
```

and its completion is the closed invariant image `H_(src,s)`. N4h proves
PF-04(a), so there is no extra null quotient. PF-04(b) alone remains: replace
“closed invariant image” by the whole N3 Hilbert space,

```text
closure(W_s(O_s^R))
 =L2(O_+,dmu_0;H_s).
```

The remaining statement is a density theorem, not another representation
calculation.
Lledo's arbitrary-discrete-helicity construction independently supports the
test-function-to-Wigner-Hilbert route, but it does not silently prove density for
the projected-conserved symmetric-potential sources used here.

Several nearby claims are also excluded:

- positive energy does not choose between helicities `+s` and `-s`;
- a single helicity requires N4's chiral curvature projection;
- time reversal exchanges `O_+` and `O_-` and anticommutes with `J_s`;
- generic spacelike-compact solutions need not have finite `||.||_+` norm;
- the zero orbit, infrared completion, and a countable sum over `s` need separate
  topology;
- the one-particle completion does not yet construct a Fock representation or an
  interacting theory.

## Verification ledger

| Obligation | Equality witness | Boundary |
| --- | --- | --- |
| source quotient | `M_s^(-1)E_s=D_s`, and null-shell `D_s=-R_sC_s` | compact smooth sources |
| physical fiber | `ker D_s(p)/im R_s(p) ~= Sym_0^s(Q_p tensor C)^*` | `p!=0`, `p^2=0` |
| positivity | Euclidean screen metric and N4h's `ker W_s=0` | real causal quotient |
| covariance | natural screen transport gives N2's Wigner cocycle | proper orthochronous group |
| causal compatibility | opposite shell signs reduce `tau_s` to `2 Im` up to one constant | free normalization retained |
| causal-quotient faithfulness | N4h's compatibility cohomology gives `H_sc^1=0` | Minkowski Cauchy surface `R^3` |
| full N3 equality | PF-04(b) density theorem | not yet discharged |

## Edges

- `N2/N2a/N3 -> N4g`: the positive orbit, measure, helicity fiber, and induced
  action type the target rather than being rediscovered from a propagator.
- `N4a/N4f -> N4g`: screen cohomology and the causal source quotient construct the
  future-shell map and prove its quotient independence.
- `N4g -> N4h`: the future-shell map supplies the zero-amplitude condition whose
  support-preserving gauge lift N4h proves.
- `N4g/N4h -> N4y`: pass the faithful free bosonic source-to-shell quotient,
  positive inner product, and causal symplectic form; N4y constructs the CCR field
  and proves its vacuum one-particle vector equals the same shell amplitude.
- `N4g/N4h -> N4s`: pass the faithful free bosonic source-to-shell quotient as a
  regression case for the reverse interacting extractor; compact-source density
  in the whole N3 space remains separate.
