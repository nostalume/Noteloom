# N4i — Half-Integer Adjoint and Hyperbolic Completion

Status: invariant pairing, invertible Euler representative, hyperbolic reduction, and admissible retarded/advanced response supported for every separate finite half-integer spin on four-dimensional Minkowski spacetime; causal quotient bijectivity is completed in N4j  
Consumes: [N4b spinor-tensor complex](04b-half-integer-potential.md), [N4c action audit](04c-action-completion-audit.md), and [fermionic Green contracts](../sources/fermionic-green-contracts.md)  
Produces: a component-free bridge from the half-integer symbol complex to a formally Hermitian Euler operator and causal sourced solutions

## Research contract

- **Question:** can the half-integer Fang--Fronsdal complex support sourced causal
  computation without choosing gamma matrices or deriving a propagator separately
  at every rank?
- **Presumptions:** one fixed finite tensor rank `n>=0`; helicity magnitude
  `h=n+1/2`; complex Dirac spinors on four-dimensional Minkowski spacetime; the
  triple-gamma-traceless field carrier and gamma-traceless gauge carrier of N4b;
  compact sources; constant coefficients.
- **Output:** an invariant Dirac--Fischer pairing, an executable inverse for the
  fermionic trace reversal, formal self-adjointness of its Euler operator, a
  normally hyperbolic reduction, and retarded/advanced response for admissible
  sources.
- **Boundary:** a Majorana real form, positive shell-map faithfulness, curved
  backgrounds, interactions, and a countable tower are not claimed.

The construction uses only the natural operators already built in N4b:

```text
P: multiplication by p.u,       A: contraction with p,
Y: multiplication by gamma(u),  Gamma: gamma trace,
Slash: Clifford multiplication by p,
q=p^2,                          T=Gamma^2, U=Y^2.
```

No matrix representative of the Clifford action enters the proof.

## 1. The field duality is constructed before the inverse

Let `beta` be the invariant Dirac sesquilinear form on the parity-paired spinor
carrier `Delta`. It is characterized, for real `v`, by

```text
beta(gamma(v)z,w)=beta(z,gamma(v)w).
```

Complete Lorentz contraction of the symmetric tensor slots with `beta` on the
spinor slot constructs the Dirac--Fischer pairing

```text
<psi,chi>_n
 =[beta(psi(partial_u),chi(u))]_(u=0).
```

Evaluating multiplication and contraction on the same two polynomials gives

```text
P^dagger=A,    Y^dagger=Gamma,    Slash^dagger=Slash.
```

After spacetime integration, compact support makes `p=i partial` formally
self-adjoint. This pairing is Lorentz invariant and nondegenerate, not positive
definite. A real Grassmann action still requires a declared Majorana or other
reality convention.

## 2. Three gamma layers make trace reversal executable

Put

```text
H_r=ker(Gamma:Sym^r(V_C^*) tensor Delta
                 ->Sym^(r-1)(V_C^*) tensor Delta).
```

The Clifford relation evaluated on a homogeneous rank-`r` polynomial is

```text
Gamma Y+Y Gamma=2r+4.
```

For `psi in F_n=ker Gamma^3`, construct its three layers rather than invoking an
unresolved projection. For `n>=2`, set

```text
h_2=(1/(4n))Gamma^2 psi;
```

for `n<2`, set `h_2=0`. Because `Gamma^3psi=0`, `h_2` is gamma-traceless. Now put

```text
r=psi-Y^2h_2,
h_1=(1/(2n+2))Gamma r,
h_0=r-Yh_1.
```

Direct substitution uses

```text
Gamma(Y h_1)=(2n+2)h_1,
Gamma^2(Y^2h_2)=4n h_2
```

and computes

```text
psi=h_0+Yh_1+Y^2h_2,
h_j in H_(n-j).
```

Thus, with unavailable negative-degree layers omitted,

```text
F_n=H_n direct-sum YH_(n-1) direct-sum Y^2H_(n-2).
```

The action-side trace reversal proposed in N4c is

```text
M_n=I-(1/2)Y Gamma-(1/4)Y^2Gamma^2.
```

Evaluating it on the three constructed layers gives

```text
M_n h_0=h_0,
M_n(Yh_1)=-n Yh_1,
M_n(Y^2h_2)=-n Y^2h_2.
```

Hence `M_0=I`, while for every `n>=1` it is invertible on `F_n`. Its inverse is
not a black box:

```text
M_n^(-1)psi=h_0-(1/n)(Yh_1+Y^2h_2).
```

The same orthogonal-layer calculation proves that the Dirac--Fischer pairing
restricted to `F_n` is nondegenerate.

## 3. The Euler operator is formally self-adjoint

Recall N4b's equation symbol

```text
S_n=Slash-P Gamma
```

and define

```text
E_n=M_nS_n:F_n->F_n.
```

First, `S_n` preserves the field constraint. Acting on the same
`psi in ker Gamma^3`, the Clifford relations compute

```text
Gamma^3 Slash psi=2A Gamma^2psi,
Gamma^3 P Gamma psi=2A Gamma^2psi,
Gamma^3 S_n psi=0.
```

The adjoints from Section 1 give

```text
S_n^dagger=Slash-YA,
M_n^dagger=M_n.
```

Normal-order both composites using only

```text
Gamma Slash+Slash Gamma=2A,
Slash Y+Y Slash=2P,
[A,Y]=Slash,
[A,Y^2]=2P.
```

Their difference on the full rank-`n` carrier is

```text
M_nS_n-(M_nS_n)^dagger
 =(1/4)(Y^2P Gamma^3-Y^3A Gamma^2).
```

For `phi,psi in F_n`, the first term vanishes because `Gamma^3psi=0`; the second
vanishes after moving `Y^3` through the pairing because `Gamma^3phi=0`. Therefore

```text
<phi,E_npsi>_n=<E_nphi,psi>_n.
```

Since `M_n` is invertible, its Euler equation has exactly N4b's vacuum solutions:

```text
E_npsi=0 iff S_npsi=0.
```

This closes N4c's complex formal-adjoint obligation. It does not yet select a real
fermionic action or a positive inner product.

## 4. The Bianchi operator constructs both gauge fixing and wave reduction

The capability now needed is not a component propagator. We need one operator that
detects the gauge direction and reduces the equation to the scalar wave operator.
Define

```text
B_n=A-(1/2)P Gamma^2-(1/2)Slash Gamma:F_n->G_n.
```

This paragraph applies to `n>=1`. At `n=0` there is no gauge carrier, `R_0` and
`B_0` are omitted, and the completion below reduces to `S_0^2=qI`.

Its type is computed on one arbitrary field:

```text
Gamma B_n
 =Gamma A-(1/2)Gamma P Gamma^2-(1/2)Gamma Slash Gamma
 =-(1/2)P Gamma^3.
```

Thus `Gamma^3psi=0` implies `Gamma(B_npsi)=0`, so `B_npsi` is an admissible gauge
parameter. N4c's Bianchi calculation is

```text
B_nS_n=(1/2)P^2Gamma^3,
```

hence `B_nS_n=0` on `F_n`.

For `epsilon in G_n=ker Gamma`, evaluate the gauge composite:

```text
B_nR_nepsilon
 =[A-(1/2)P Gamma^2-(1/2)Slash Gamma]P epsilon
 =(1/2)q epsilon.
```

The same operator algebra, now on an arbitrary rank-`n` spinor-tensor, computes

```text
S_n^2
 =qI-2PA+P^2Gamma^2+P Slash Gamma,

2R_nB_n
 =2PA-P^2Gamma^2-P Slash Gamma.
```

Adding the two composites with their common domain and target gives the uniform
hyperbolic reduction

```text
S_n^2+2R_nB_n=qI_(F_n).
```

This is the half-integer analogue of `D_s+R_sC_s=qI`, but the first-order field
equation must be composed once with itself. The computational depth is independent
of `n`.

## 5. The constrained adjoint constructs admissible sources

Using `P^dagger=A`, compute

```text
A M_n
 =B_n-(1/2)Y A Gamma-(1/4)Y^2A Gamma^2.
```

If `epsilon in G_n`, the last two terms pair to zero because moving `Y` or `Y^2`
to the first slot produces `Gamma epsilon` or `Gamma^2epsilon`. Consequently

```text
<R_nepsilon,M_npsi>_n=<epsilon,B_npsi>_(n-1).
```

This is the constrained-adjoint identity

```text
R_n^dagger M_n=B_n.
```

For `n>=1`, an admissible compact source `J` is therefore characterized by

```text
R_n^dagger J=0.
```

After the explicit trace reversal

```text
K=M_n^(-1)J,
```

the same condition becomes the gauge-fixing equation

```text
B_nK=0.
```

Source conservation and hyperbolic compatibility are thus the same semantic
condition in two dual presentations. At `n=0`, every compact Dirac source is
admissible because there is no gauge map.

## 6. Scalar wave Green maps construct fermionic response

Let `g_n^+/-` be the retarded/advanced Green maps of `qI` on `F_n`. They preserve
the algebraic gamma-trace constraint and commute with the constant-coefficient
operators. For an admissible compact source define

```text
psi_J^+/-=S_n g_n^+/- M_n^(-1)J.
```

Set `K=M_n^(-1)J`. The hyperbolic identity and `B_nK=0` compute

```text
S_npsi_J^+/-
 =S_n^2g_n^+/-K
 =(qI-2R_nB_n)g_n^+/-K
 =K,

E_npsi_J^+/-=M_nK=J.
```

The Bianchi identity simultaneously gives

```text
B_npsi_J^+/-=B_nS_ng_n^+/-K=0.
```

Therefore the response has retarded/advanced support, solves the sourced Euler
equation, and is already in the constructed gauge. No rank-dependent numerator
has been inverted.

Let `Delta_n=g_n^+-g_n^-`. The causal map is

```text
[J] |-> [S_nDelta_nM_n^(-1)J].
```

It is well defined on compact source classes modulo `E_na`. Indeed, for compact
`a in F_n`, the change is

```text
S_nDelta_nM_n^(-1)E_na
 =S_nDelta_nS_na
 =(qI-2R_nB_n)Delta_na
 =-2R_nDelta_nB_na,
```

which is a spacelike-compact gauge transformation. The output solves the
homogeneous equation because `qDelta_n=0` and `B_nM_n^(-1)J=0`.

This proves response and quotient independence.
[N4j](04j-half-integer-causal-quotient.md) now supplies the all-rank
support/exact-sequence theorem and proves that this map is injective and
surjective.

## 7. Checks and supported boundary

| Rank | Meaning | Check |
| --- | --- | --- |
| `n=0` | Dirac field, no gauge | `M_0=I`, `S_0^2=qI`; ordinary Dirac causal propagator |
| `n=1` | Rarita--Schwinger field | trace reversal invertible; field and parameter completions agree with the Dirac/wave pattern of FH-03 |
| finite `n>=2` | higher Fang--Fronsdal potentials | the same five operators and identities; no new component formula |

The existing bounded computation now checks ranks `n=0,1,2,3` at null and non-null
momenta. It verifies preservation of `F_n`, invertibility of `M_n`, formal
self-adjointness of `E_n` in the Dirac--Fischer Gram form, `B_nS_n=0`,
`B_nR_n=(1/2)q`, and `S_n^2+2R_nB_n=qI`. Its largest residual is at floating-point
roundoff; the script remains independent evidence rather than the proof.

Supported here:

- a nondegenerate invariant complex pairing on the constrained field carrier;
- invertible fermionic trace reversal and formal self-adjoint Euler operator;
- a uniform normally hyperbolic reduction for every separate finite `n`;
- retarded/advanced response for admissible compact sources;
- quotient independence of the causal response.

Still open:

- support-preserving faithfulness for gamma-traceless gauge parameters and density
  of [N4k's positive particle/antiparticle image](04k-half-integer-positive-frequency.md);
- Majorana reality and positivity choices;
- curved backgrounds, interactions, and estimates uniform in `n`.

## Edges

- `N4b/N4c -> N4i`: the spinor-tensor complex and Bianchi candidate supply the
  carriers and operators whose adjoint and hyperbolic identities are completed.
- `N4i -> N4j`: the four operator identities and admissible response supply the
  input for the causal quotient theorem.
