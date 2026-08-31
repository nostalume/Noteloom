# N4l — Half-Integer Support-Preserving Faithfulness

Status: the paired shell map is faithful for every separate finite half-integer spin on four-dimensional Minkowski spacetime  
Consumes: [N4b screen exactness](04b-half-integer-potential.md), [N4j causal quotient](04j-half-integer-causal-quotient.md), [N4k paired positive-shell map](04k-half-integer-positive-frequency.md), and [support-faithfulness contracts](../sources/support-faithfulness-contracts.md)  
Produces: `ker W_n^pair=0`, removing N4k's provisional spectral null quotient

## Research contract

- **Question:** if both particle and antiparticle screen amplitudes vanish, can
  their momentumwise gauge representatives be assembled into one
  spacelike-compact gamma-traceless gauge parameter?
- **Presumptions:** one fixed finite `n>=1`; complex symmetric spinor-tensors on
  Minkowski spacetime; N4j's spacelike-compact solution class; both nonzero null
  shell components retained by N4k.
- **Output:** the implication

  ```text
  W_n^pair[J]=0
    => S_n Delta_n M_n^(-1)J=R_n epsilon,
       epsilon in Gamma_sc(G_n)
    => [J]=0.
  ```

- **Boundary:** the proof uses flat finite-type compatibility and
  `H_c^1(R^3)=0`. It does not prove density, nontrivial topology, curved
  backgrounds, or a countable-spin theorem. N4z closes CAR normalization
  downstream.

Spin `1/2` was already faithful in N4k because it has no gauge image. This node
handles every gauge rank `n>=1`.

## 1. Shellwise division is not the required computation

For a compact admissible source set

```text
K=M_n^(-1)J,
X(p)=S_n(p)K_hat(p),
psi=S_n Delta_n K.
```

N4k proves that `X(p) in ker S_n(p)` on the null shell. If
`W_n^pair[J]=0`, both energy signs have zero physical screen class. N4b's exact
sequence therefore constructs, separately at every nonzero shell momentum,

```text
X(p)=R_n(p)epsilon_p.
```

The family `epsilon_p` is not yet a spacelike-compact gauge parameter. Dividing
by a momentum component can destroy inverse-Fourier support. The missing
construction must detect the gauge image before solving for a representative.

## 2. The gamma-traceless gauge equation is finite type

The gauge operator is

```text
R_n:G_n->F_n,
R_n epsilon=Sym(partial epsilon),

G_n=ker Gamma in Sym^(n-1)(V^*) tensor Delta,
F_n=ker Gamma^3 in Sym^n(V^*) tensor Delta.
```

First forget the algebraic gamma trace. In a constant spinor basis,
`R_nepsilon=0` is one rank-`n-1` Killing-tensor equation for each spinor
coefficient. Commuting flat derivatives and prolonging moves derivative indices
into Young symmetries incompatible with full symmetrization. After an order
bounded by `n`, no free symbol remains; the solution is determined by a finite jet.

Now restore `Gamma epsilon=0`. Gamma contraction is a constant Lorentz-equivariant
algebraic map and commutes with flat differentiation. Its kernel is therefore a
constant-rank invariant subbundle at every prolongation order. Restricting to it
does not recreate an unrestricted symbol. Hence the constrained `R_n` remains a
regular finite-type operator.

The finite-type compatibility theorem constructs, algorithmically,

```text
G_n --R_n--> F_n --K_(n,1)--> C_(n,2) --> ...,

K_(n,1)R_n=0,

K_(n,1)phi=0 locally
  iff phi=R_n epsilon locally.
```

`K_(n,1)` is the complete observable needed here. An unconstrained
higher-spin curvature would kill the larger unconstrained gradient image and
would not by itself detect the smaller gamma-traceless image.

At `n=1`, the parameter is a spinor and `R_1epsilon=partial epsilon`; the first
compatibility operator is the exterior curl with a spinor coefficient. Higher
ranks are its finite-prolongation generalization, not a component curvature
expansion.

## 3. Zero paired amplitude kills the complete observable

The Fourier transform of N4j's causal solution is, up to a nonzero convention
constant,

```text
psi_hat(p)
 =c_Delta sign(p^0)delta(p^2)X(p).
```

For each nonzero shell momentum, evaluate the compatibility symbol on the same
`X(p)`:

```text
K_(n,1)(p)X(p)
 =K_(n,1)(p)R_n(p)epsilon_p
 =0.
```

The multiplier is polynomial and the compact-source amplitude is smooth. Its
value extends continuously to the cone origin, while the causal distribution
contains `delta(p^2)` and no derivative of that delta. Therefore

```text
Fourier(K_(n,1)psi)
 =c_Delta sign(p^0)delta(p^2)K_(n,1)(p)X(p)
 =0,

K_(n,1)psi=0.
```

Both shell signs were required in the first equality. Unlike the integer-spin
argument, no reality condition is needed to reconstruct the unobserved shell.

## 4. Support cohomology constructs one global gauge parameter

Local exactness makes the compatibility complex a resolution of the sheaf
`KillSpin_n` of gamma-traceless Killing spinor-tensors. On spacelike-compact
sections, the exact obstruction is

```text
H_sc^1(M;KillSpin_n)
 =ker K_(n,1)|_(Gamma_sc(F_n))
   /R_n Gamma_sc(G_n).
```

Finite prolongation identifies `KillSpin_n` with parallel sections of a
finite-rank prolonged bundle `Z_n`. All coefficients are constant on Minkowski
spacetime, so the prolonged connection is flat. Since Minkowski spacetime is
simply connected, `Z_n` is a constant finite-dimensional complex local system.

The causally restricted support theorem then gives

```text
H_sc^1(M;KillSpin_n)
 ~=H_c^1(R^3;Z_n).
```

Compact-support Poincare duality evaluates the right side:

```text
H_c^r(R^3;Z_n)=0 for r!=3,

H_sc^1(M;KillSpin_n)=0.
```

Apply this vanishing to the already constructed `psi`. It produces one

```text
epsilon in Gamma_sc(G_n)
```

with

```text
psi=R_n epsilon.
```

The support property is part of the cohomology computation; it is not recovered
after an uncontrolled momentum division.

## 5. N4j converts gauge triviality into source faithfulness

N4j's causal isomorphism sends

```text
[J] |-> [S_n Delta_n M_n^(-1)J]=[psi].
```

The constructed equality `psi=R_nepsilon` makes the solution class zero.
Injectivity of that same map computes

```text
W_n^pair[J]=0
  => [psi]=0
  => [J]=0.
```

Thus

```text
ker W_n^pair=0
```

for every separate finite `n>=1`; together with N4k's `n=0` argument, this covers
all finite half-integer spins. N4k's positive form is therefore a norm on the
original realification of `O_n^C`, not merely on a spectral quotient.

## 6. Computability and boundary

The rank dependence is isolated in one finite prolongation. The semantic route is

```text
zero two-shell screen class
  -> complete compatibility observable vanishes
  -> flat finite local system
  -> H_c^1(R^3;Z_n)=0
  -> one spacelike-compact gauge parameter.
```

No polarization basis, gamma-matrix expansion, or momentum denominator enters the
proof. A program can construct `K_(n,1)` rank by rank through finite jet linear
algebra, but a minimal closed formula is not required for faithfulness.

Still open:

- density of the compact-source particle and antiparticle images in the full
  induced Hilbert spaces;
- an explicit minimal compatibility operator and its complexity growth with `n`;
- Majorana or charge-conjugation choices (Euler/CAR normalization is closed in
  N4z);
- nontrivial Cauchy topology, curved backgrounds, interactions, and uniform
  countable-spin estimates.

## Edges

- `N4k -> N4l`: zero paired shell amplitude supplies the shellwise gauge datum.
- `N4l -> N6`: the finite half-integer positive norm is now faithful; only density
  and uniform countable completion remain.
- `N4l -> N7`: support topology becomes an explicit distinction between shellwise
  and causal gauge equivalence.
