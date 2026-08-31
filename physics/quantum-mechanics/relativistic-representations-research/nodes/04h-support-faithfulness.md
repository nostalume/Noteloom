# N4h — Support-Preserving Faithfulness of the Future-Shell Map

Status: PF-04(a) supported for every separate finite symmetric integer spin on four-dimensional Minkowski spacetime  
Consumes: [N4a screen exactness](04a-polynomial-complex-details.md), [N4f causal quotient](04f-finite-integer-spin-green-construction.md), [N4g future-shell map](04g-positive-frequency-completion.md), and [support-faithfulness contracts](../sources/support-faithfulness-contracts.md)  
Produces: `ker W_s=0` on N4f's real causal source quotient

## Research contract

- **Question:** if a real causal solution has zero physical amplitude on the future
  null shell, can the shellwise gauge representatives be assembled into one
  spacelike-compact gauge parameter?
- **Presumptions:** one fixed finite integer `s>=1`; flat, oriented and
  time-oriented four-dimensional Minkowski spacetime; N4f's smooth
  spacelike-compact causal solutions; N4g's real source quotient and Fourier
  convention.
- **Output:** a support-preserving computation

  ```text
  W_s[J]=0
    => Delta_(F,s)M_s^(-1)J=R_s chi,  chi in G_(s,sc)
    => [J]=0.
  ```

- **Boundary:** the proof uses flat finite-type compatibility and
  `H_c^1(R^3)=0`. It does not extend automatically to nontrivial Cauchy topology,
  curved backgrounds, countable spin, or the PF-04(b) density claim.

## 1. Why pointwise screen division was insufficient

Put

```text
S=M_s^(-1)J,
phi=Delta_(F,s)S.
```

N4a proves at every nonzero null momentum `p` that

```text
ker D_s(p)/im R_s(p)
  ~=Sym_0^s(Q_p tensor C)^*.
```

Thus `W_s[J](p)=0` constructs some `epsilon_p` with

```text
S_hat(p)=R_s(p)epsilon_p.
```

Choosing `epsilon_p` independently does not control its inverse Fourier support.
Division by `p.t` may turn a spacelike-compact field into a non-spacelike-compact
parameter. The missing object must therefore remember gauge compatibility in
spacetime before solving for a parameter.

## 2. Gauge compatibility constructs a finite complex

The gauge operator is

```text
R_s: G_s->F_s,
R_s epsilon=Sym(partial epsilon),

G_s=ker T in Sym^(s-1)(V^*),
F_s=ker T^2 in Sym^s(V^*).
```

A complete gauge observable is a differential operator `K_(s,1)` satisfying

```text
K_(s,1)R_s=0,

K_(s,1)phi=0 locally
  iff phi=R_s epsilon locally.
```

The second line is the required capability: its kernel is not merely a set of
quantities invariant under gauge; it detects the whole constrained gauge image.

### 2.1 Finite prolongation constructs `K_(s,1)`

The homogeneous equation `R_s epsilon=0` is the traceless rank-`s-1` Killing
tensor equation. On flat spacetime, commute derivatives and prolong it. Each
prolongation moves one derivative index into a Young symmetry incompatible with
complete symmetrization. After finitely many steps, at an order bounded in terms
of `s`, the prolonged symbol vanishes. Equivalently, a solution is fixed by a
finite jet and is polynomial of bounded degree.

Trace commutes with the flat derivative, so imposing `T epsilon=0` selects an
invariant constant-rank subbundle throughout this prolongation. Therefore `R_s`
is a regular finite-type operator.

SF-01 supplies the following exact theorem contract:

```text
regular finite-type R_s
  -> finite prolonged bundle Z_s with a connection nabla^(s)
  -> R_s epsilon=0 iff j^r epsilon is nabla^(s)-parallel
  -> a full compatibility complex

G_s --R_s--> F_s --K_(s,1)--> C_(s,2) --> ... .
```

On Minkowski spacetime the coefficients and prolongation relations are constant,
so `nabla^(s)` is flat and the transferred compatibility operators may be chosen
with constant coefficients. This constructs `K_(s,1)` algorithmically without a
tensor-component curvature expansion.

For orientation:

```text
s=1: K_(1,1)=d,                         Maxwell curvature;
s=2: K_(2,1)=linearized Riemann,        Calabi complex;
s>=3: complete constrained compatibility operator.
```

The last line need not equal the unconstrained de Wit--Freedman curvature alone.
That curvature kills a larger gradient image; completeness for the traceless
parameter is the reason for using the finite-type construction.

## 3. Zero screen amplitude kills the complete gauge observable

N4g gives the Fourier form of the causal solution, up to one nonzero convention
constant:

```text
phi_hat(p)
 =c_Delta sign(p^0)delta(p^2)S_hat(p).
```

Assume `W_s[J]=0`. Reality makes the physical screen class zero on both connected
shell components. N4a's exact sequence then computes, for every nonzero shell
momentum,

```text
S_hat(p) in im R_s(p).
```

The compatibility identity acts on the same datum:

```text
K_(s,1)(p)S_hat(p)
 =K_(s,1)(p)R_s(p)epsilon_p
 =0.
```

The multiplier is smooth and polynomial. It also vanishes at the cone origin by
continuity; the causal distribution contains `delta(p^2)`, not derivatives of that
delta distribution. Multiplication therefore gives

```text
Fourier(K_(s,1)phi)
 =c_Delta sign(p^0)delta(p^2)
   K_(s,1)(p)S_hat(p)
 =0.
```

Hence

```text
K_(s,1)phi=0
```

as a spacetime distribution, and therefore as a smooth field because N4f's causal
map sends compact smooth sources to smooth spacelike-compact solutions.

## 4. The support obstruction is a degree-one cohomology class

The complete compatibility complex is locally exact, so it resolves the sheaf
`Kill_s` of traceless Killing tensors. Restricting the first two maps to
spacelike-compact sections gives

```text
H_sc^1(M;Kill_s)
 =ker(K_(s,1):F_(s,sc)->C_(s,2,sc))
   /R_s(G_(s,sc)).
```

This equality types the obstruction. `K_(s,1)phi=0` constructs a local gauge
parameter; its class in `H_sc^1` measures whether those local parameters can be
assembled with the required support.

The finite prolongation identifies `Kill_s` with parallel sections of the flat
finite-rank bundle `Z_s`. Minkowski spacetime is simply connected, so a parallel
section is determined by one element of a fixed finite-dimensional vector space,
also denoted `Z_s`. The sheaf is therefore constant.

SF-02's support construction, applied to this flat local system, gives

```text
H_sc^1(M;Kill_s)
 ~=H_c^1(Sigma;Z_s).
```

For Minkowski spacetime choose `Sigma=R^3`. Compact-support Poincare duality
computes

```text
H_c^r(R^3;Z_s)
 =0,  r!=3,

H_c^3(R^3;Z_s)
 ~=Z_s.
```

In particular,

```text
H_sc^1(M;Kill_s)=0.
```

Applying this vanishing to the same `phi` constructs one
`chi in G_(s,sc)` with

```text
phi=R_s chi.
```

Unlike shell division, this conclusion includes the support property because the
cohomology was computed on the spacelike-compact complex itself.

## 5. Return through N4f proves faithfulness

N4f's causal isomorphism is

```text
I_s([J])=[Delta_(F,s)M_s^(-1)J]=[phi].
```

The constructed equality `phi=R_schi` makes its solution class zero. Injectivity
of `I_s` then evaluates

```text
W_s[J]=0
  => I_s([J])=0
  => [J]=0.
```

Therefore

```text
ker W_s=0
```

on N4g's real causal source quotient for every separate finite integer `s>=1`.
The spectral null quotient introduced provisionally in N4g is unnecessary on this
Minkowski support class.

## 6. Low-spin checks and general boundary

| Spin | Compatibility complex | Degree-one support result |
| --- | --- | --- |
| `1` | de Rham: scalar `--d-->` one-form `--d-->` two-form | `H_sc^1(M)~=H_c^1(R^3)=0` |
| `2` | Calabi: vector `--Killing-->` symmetric tensor `--Riemann_lin-->` curvature | Killing-sheaf `H_sc^1=0` on Minkowski |
| finite `s>=3` | finite-type traceless Killing compatibility complex | flat prolonged local system gives the same `H_c^1(R^3;Z_s)=0` |

No component calculation grows with `s`. The executable route is

```text
prolong R_s finitely
  -> flat jet connection
  -> twisted de Rham resolution
  -> compact Cauchy-surface cohomology
  -> support-preserving gauge parameter.
```

What remains open is different:

- PF-04(b): whether compact admissible sources have dense image in the entire N3
  induced `L2` helicity-pair space;
- explicit minimal formulas and semantic cost for `K_(s,1)` at `s>=3`;
- nontrivial Cauchy topology, where `H_c^1(Sigma;Z_s)` need not vanish;
- curved backgrounds, where prolongation may define a nonflat local system or
  change rank;
- half-integer and countable-spin completions.

## Edges

- `N4a/N4f/N4g -> N4h`: shell exactness and the causal future-shell map identify
  the pointwise gauge datum whose support must be repaired.
- `N4h -> N4m`: faithfulness removes N4m's provisional spectral null quotient on
  Minkowski spacetime.
- `N4h -> N7`: topology-sensitive compatibility cohomology becomes a precise
  stronger-equivalence test.
