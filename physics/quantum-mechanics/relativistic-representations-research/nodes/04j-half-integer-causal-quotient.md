# N4j — Half-Integer Causal Quotient Theorem

Status: causal source-to-solution quotient isomorphism supported for every separate finite half-integer spin on four-dimensional Minkowski spacetime  
Consumes: [N4i adjoint and hyperbolic completion](04i-half-integer-green-construction.md) and [fermionic Green contracts](../sources/fermionic-green-contracts.md)  
Produces: a bijective causal map from compact admissible sources modulo Euler sources to spacelike-compact Fang--Fronsdal solutions modulo spacelike-compact gauge

## Research contract

- **Question:** does N4i's causal response represent every spacelike-compact
  physical solution exactly once, after source and gauge equivalence are imposed?
- **Presumptions:** one fixed finite `n>=0`; four-dimensional Minkowski spacetime;
  N4i's constrained finite-rank bundles and complex Dirac--Fischer pairing; compact
  sources; spacelike-compact solutions and gauge parameters; the scalar wave
  retarded/advanced exact sequence, including its past/future-compact extensions.
- **Output:** an explicitly constructed isomorphism

  ```text
  O_n ~= Sol_(sc,n)/R_n Gamma_sc(G_n).
  ```

- **Boundary:** the quotient uses spacelike-compact gauge parameters. It does not
  identify larger gauge relations, construct a Majorana real form, prove
  positivity, select particle/antiparticle sectors, or cover curved backgrounds;
  [N4k](04k-half-integer-positive-frequency.md) owns the downstream positive
  construction.

No new tensor or Clifford calculation is required. The theorem is a support
computation using the four N4i identities

```text
B_nS_n=0,
B_nR_n=(1/2)qI,
S_n^2+2R_nB_n=qI,
R_n^dagger M_n=B_n.
```

For `n=0`, omit `R_n,B_n`; then `S_0^2=qI`. The ordinary Dirac causal exact
sequence is also reconstructed below rather than left as an imported special case.

## 1. Trace reversal exposes the exact quotient

The original compact source space is

```text
O_n
 ={J in Gamma_c(F_n) | R_n^dagger J=0}
   /E_n Gamma_c(F_n),

E_n=M_nS_n.
```

Use N4i's executable inverse and set `K=M_n^(-1)J`. Evaluate both source
conditions on the same `J`:

```text
R_n^dagger J
 =R_n^dagger M_nK
 =B_nK,

J=E_na=M_nS_na
 iff K=S_na.
```

Thus `M_n^(-1)` constructs an isomorphism

```text
O_n
 ~=O_tilde_n
  ={K in Gamma_c(F_n) | B_nK=0}
    /S_n Gamma_c(F_n).
```

This is not only shorter notation. In `O_tilde_n`, admissibility is precisely the
condition that eliminates the gauge term in the wave reduction.

Let `Delta_n=g_n^+-g_n^-` be the scalar-wave causal propagator on `F_n`. The map
to be proved bijective is

```text
I_tilde_n:[K] |-> [S_nDelta_nK]

from O_tilde_n to

Sol_(sc,n)/R_n Gamma_sc(G_n),

Sol_(sc,n)={psi in Gamma_sc(F_n) | S_npsi=0}.
```

N4i already proves that it is well typed and independent of the source
representative.

## 2. Injectivity is a compact-support computation

Take `K in Gamma_c(F_n)` with `B_nK=0` and suppose its causal solution is gauge:

```text
S_nDelta_nK=R_nepsilon,
epsilon in Gamma_sc(G_n).
```

Apply `B_n` to this same equality. The left side vanishes by `B_nS_n=0`; the right
side is `(1/2)qepsilon`. Hence

```text
qepsilon=0.
```

The scalar-wave exact sequence on `G_n` constructs a compact `b` with

```text
epsilon=Delta_nb.
```

Constant coefficients let `S_n` and `R_n` commute with `Delta_n`, so the assumed
gauge equality becomes

```text
Delta_n(S_nK-R_nb)=0.
```

Exactness at compact sections now constructs `c in Gamma_c(F_n)` such that

```text
S_nK-R_nb=qc.
```

Apply `B_n` to this equality:

```text
0-(1/2)qb=qB_nc,

q(b+2B_nc)=0.
```

A normally hyperbolic equation has no nonzero compactly supported homogeneous
solution, so

```text
b=-2B_nc.
```

Substitute this constructed value into the preceding compact equality:

```text
S_nK+2R_nB_nc=qc
             =S_n^2c+2R_nB_nc.
```

Therefore `S_n(K-S_nc)=0`. Its Bianchi condition is also zero:

```text
B_n(K-S_nc)=B_nK-B_nS_nc=0.
```

The hyperbolic identity acts on this same compact field `d=K-S_nc`:

```text
qd=S_n^2d+2R_nB_nd=0.
```

Again compact wave uniqueness gives `d=0`, hence

```text
K=S_nc.
```

So `[K]=0` in `O_tilde_n`. This proves injectivity without choosing a momentum or
dividing a symbol.

At `n=0`, the same computation shortens. If `S_0Delta_0K=0`, wave exactness
constructs compact `c` with `S_0K=qc`. Hence `S_0(K-S_0c)=0`, while
`q(K-S_0c)=S_0^2(K-S_0c)=0`; compact wave uniqueness gives `K=S_0c`. Thus the
Dirac source class also vanishes.

## 3. A temporal cutoff constructs every solution class

Let `psi in Sol_(sc,n)`. Choose a smooth temporal cutoff `chi` that is zero before
one Cauchy surface and one after a later Cauchy surface. Define

```text
a_+=chi psi,
a_-=-(1-chi)psi.
```

Because `psi` is spacelike compact and the derivative of `chi` lies between two
Cauchy surfaces,

```text
K=S_na_+=S_na_-=[S_n,chi]psi
```

is compact. The Bianchi identity computes

```text
B_nK=B_nS_na_+=0,
```

so `K` is an admissible trace-reversed source.

The two cutoff fields solve `S_na_+/-=K`, but they need not satisfy `B_na_+/-=0`.
Repair this rather than assuming it. Extend the wave Green maps to past-compact
and future-compact sections and construct

```text
epsilon_+=-2g_(G,n)^+ B_na_+,
epsilon_-=-2g_(G,n)^- B_na_-,

a'_+=a_+ +R_nepsilon_+,
a'_- =a_- +R_nepsilon_-.
```

The gauge composite verifies on each sign separately

```text
B_na'_+/-
 =B_na_+/- +(1/2)qepsilon_+/-
 =0.
```

Gauge invariance preserves the source equation:

```text
S_na'_+/-=K.
```

Now compute the wave equation of these same corrected fields:

```text
qa'_+/-
 =(S_n^2+2R_nB_n)a'_+/-
 =S_nK.
```

They have respectively retarded and advanced support. N4i's response fields

```text
u_+/-=S_ng_n^+/-K
```

obey the same wave equation and the same support condition:

```text
qu_+/-=S_nK.
```

Uniqueness of the retarded/advanced wave problem therefore gives

```text
u_+/-=a'_+/-.
```

Taking their causal difference computes

```text
S_nDelta_nK
 =a'_+-a'_-
 =a_+-a_-+R_n(epsilon_+-epsilon_-)
 =psi+R_n(epsilon_+-epsilon_-).
```

Thus `I_tilde_n[K]=[psi]`. Every spacelike-compact solution class is reached, so
the causal map is surjective.

The constructed gauge parameter is admissible for the stated quotient. A
spacelike-compact field that vanishes before one Cauchy surface has support in
`J^+(C_+)` for a compact cut `C_+`; the time-reversed statement gives compact
`C_-` for the field that vanishes after a Cauchy surface. Thus `B_na_+/-` has the
same respective support type, and causal support of `g^+/-` gives

```text
supp(epsilon_+) subset J^+(C_+),
supp(epsilon_-) subset J^-(C_-).
```

Each set is spacelike compact, so `epsilon_+-epsilon_-` is spacelike compact.

For `n=0`, skip the gauge-repair lines: `q a_+/-=S_0K` already follows from
`S_0^2=qI`. Retarded/advanced uniqueness gives
`S_0g_0^+/-K=a_+/-`, and their difference is exactly `psi`. This proves the
spin-`1/2` surjectivity internally as well.

## 4. Return to the original source variables

Combining Sections 1--3 constructs the isomorphism

```text
I_n:O_n -> Sol_(sc,n)/R_n Gamma_sc(G_n),

I_n[J]=[S_nDelta_nM_n^(-1)J].
```

Its inverse is constructive up to the declared quotient:

```text
solution psi
 -> temporal cutoff chi
 -> compact K=[S_n,chi]psi
 -> compact admissible J=M_nK.
```

Changing `chi` changes `J` by an Euler source because injectivity has already been
proved. The semantic object preserved across both directions is the same
spacelike-compact physical solution class.

## 5. Computability and boundaries

The proof adds no rank-dependent algebra. For every finite `n`, its operations are

```text
one trace reversal,
one scalar wave exact sequence,
one temporal cutoff,
two scalar wave Green applications,
one gauge correction per support sign.
```

The transformation depth is therefore uniform in spin. The theorem does not hide
an explicit tensor numerator, a component gauge elimination, or an arbitrary
choice of polarization.

Supported here:

- injectivity of the compact-source causal map modulo Euler sources;
- surjectivity onto all spacelike-compact solutions modulo spacelike-compact gauge;
- an executable inverse using a temporal cutoff;
- equality of source-response and classical solution equivalence for every
  separate finite half-integer spin on Minkowski spacetime.

Still open:

- gauge-rank faithfulness and density of
  [N4k's particle/antiparticle shell map](04k-half-integer-positive-frequency.md);
- a Majorana real-form comparison and positivity;
- larger gauge relations, nontrivial topology, curved backgrounds, interactions,
  and a countable-spin topology.

## Edges

- `N4i -> N4j`: the adjoint, Bianchi, and wave-reduction identities become a
  support-sensitive causal quotient theorem.
- `N4j -> N4k`: the complex causal quotient and its two shell signs become the
  input for the positive particle/antiparticle construction.
