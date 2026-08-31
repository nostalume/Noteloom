# N2b — Constructing Lorentz Carriers by Invariant Splitting

Status: supported for finite complex carriers, massive restriction maps, and direct massless extremal lines  
Consumes: the oriented, time-oriented Lorentz space and spin cover constructed in [N2](02-three-representation-spaces.md)  
Joins: the physical fibers constructed independently in [N2a](02a-spin-and-helicity.md)  
Produces: explicit little-group intertwiners consumed by [N3](03-realization-bridge.md)  
Source contracts: [Lorentz-carrier contracts](../sources/lorentz-carrier-contracts.md)

## Research contract

**Question.** Why are finite Lorentz carriers indexed by two half-integers, and
which explicit maps place a massive spin or massless helicity fiber inside one?

**Constructed input.** A real oriented, time-oriented four-space `(V,eta)`, its
connected Lorentz group `L=SO^+(V,eta)`, and the chosen spin cover
`pi:L_spin->L`.

**Output.** For nonnegative integers `m,n`, construct

```text
F_(m,n)=Sym^m(S) tensor Sym^n(bar S),
(j_L,j_R)=(m/2,n/2),
```

and pass N3 an actual little-group intertwiner, not merely an allowed label.

```text
Lorentz motions
  -> Hodge eigenspaces of the same motions
  -> two commuting chiral actions
  -> finite carrier functors
  -> restriction along the constructed little group
  -> explicit intertwiner.
```

No coordinate generator is passed downstream.

## 1. Infinitesimal motions are metric bivectors

The capability “change a vector while preserving its metric pairing to first
order” constructs

```text
g={X in End(V) | eta(Xu,v)+eta(u,Xv)=0 for all u,v}.
```

The metric maps a decomposable bivector to such a motion:

```text
M(u wedge v)x=eta(v,x)u-eta(u,x)v.
```

Substitution verifies the defining identity. Nondegeneracy of `eta` makes
`M:wedge^2 V->g` injective; both spaces have dimension six, so it is an
isomorphism. For `A in L`,

```text
A M(u wedge v) A^(-1)=M(Au wedge Av).
```

Thus adjoint motion and transformed bivector are two representations of the same
operation.

## 2. Hodge spectra split the same motion

The induced metric on `wedge^2 V` and the oriented volume form construct `star`
by

```text
beta wedge star(alpha)=<beta,alpha>_eta vol.
```

For a metric with three negative directions, the defining equation gives

```text
star^2 on wedge^r V = (-1)^[r(4-r)+3] identity.
```

At `r=2` this is `star^2=-identity`. A check on one oriented orthonormal pair
of complementary two-planes fixes the same sign; naturality makes it basis
independent. After complexification, construct

```text
P_+=(identity-i star)/2,
P_-=(identity+i star)/2.
```

Direct calculation from `star^2=-identity` gives

```text
P_+^2=P_+,     P_-^2=P_-,
P_+P_-=0,      P_++P_-=identity.
```

Therefore

```text
g_C=g_+ direct-sum g_-,
g_+=M(im P_+),    g_-=M(im P_-).
```

No degree of freedom has been added: each motion has merely been recovered from
its two spectral parts.

## 3. Naturality makes the parts commute

Every `A in L` preserves `eta` and `vol`. Applying the definition of `star`
to transformed bivectors computes

```text
star(wedge^2 A alpha)=wedge^2 A star(alpha).
```

Hence the projectors commute with the Lorentz action. Differentiation shows that
`g_+` and `g_-` are ideals. Because they are complementary,

```text
[g_+,g_-] subset g_+ intersection g_-=0.
```

This is the invariant reason the two chiral actions commute.

The remaining classification is an exact theorem contract:

> **Four-dimensional complex Lorentz contract.** The complex Lorentz algebra is
> semisimple; its two three-dimensional Hodge ideals are simple; and every
> three-dimensional complex simple Lie algebra is isomorphic to `sl(2,C)`.
> Consequently `g_+~=sl(S)` and `g_-~=sl(bar S)` for two-dimensional
> fundamental modules exchanged by real conjugation.

The contract supplies the classification name. The preceding computation supplies
why the two factors exist. This Hodge mechanism is special to four dimensions,
where bivectors are mapped to bivectors; algebra decompositions in general are not.

## 4. Construct the spin covering and its vector bridge

Choose `epsilon in wedge^2 S^*`, `epsilon!=0`, and set

```text
SL(S)={A in GL(S) | A preserves epsilon}.
```

Let `Herm(S)` be the real Hermitian fixed part of `S tensor bar(S)`. The form
`epsilon tensor bar(epsilon)` constructs `q(P)=det(P)), and `SL(S)` acts by

```text
lambda(A)P=(A tensor bar A)P.
```

Functoriality gives the group law; preservation of `epsilon` gives
`q(lambda(A)P)=q(P)`. In one `epsilon`-normalized basis, the bounded local check

```text
P(t,x,y,z)=((t+z,x-i y),(x+i y,t-z)),
det P=t^2-x^2-y^2-z^2
```

fixes the signature and positive cone. The matrix is a check, not the construction.

If `lambda(A)` fixes every Hermitian element, it fixes every rank-one ray
`s tensor bar(s)`. Therefore `A` preserves every line in `S), hence
`A=c identity`; `det A=1` gives `c=+1` or `-1). Thus

```text
ker lambda={+identity,-identity}.
```

The derivative is injective. Domain and target are connected real
six-dimensional groups, so the image is open and therefore equals the connected
target:

```text
lambda:SL(S)->SO^+(Herm(S),q)
```

is a double cover.

Choose an orientation- and time-orientation-preserving isometry
`iota:V->Herm(S)`. Transporting `lambda` through `iota` produces a connected
double cover of `L). Uniqueness of the connected spin cover supplies
`c:L_spin->SL(S)` satisfying

```text
iota(pi(g)v)=lambda(c(g))iota(v).
```

This commuting equation is the semantic-coincidence witness missing from the old
node: both sides are the same transformed vector. `iota` is a spin-frame choice;
changing it conjugates the construction without changing multiplicities.

For future-null `k`, `q(iota(k))=0` and positivity place `iota(k)` on the
rank-one boundary:

```text
iota(k)=lambda_0 tensor bar(lambda_0).
```

The resulting line `ell=span(lambda_0)` is phase independent.

## 5. Finite carriers are functorial

Construct

```text
F_(m,n)=Sym^m(S) tensor Sym^n(bar S).
```

The commuting ideals act on their respective factors, so this is a representation
without generator expansion.

> **Finite-carrier contract.** Every finite-dimensional irreducible complex
> representation of `Spin^+(1,3)` is isomorphic to one `F_(m,n)). This is the
> finite highest-weight theorem applied after the internally constructed split.

This contract excludes infinite-dimensional unitary carriers, real structures,
and discrete parity/time reversal.

## 6. Massive restriction constructs the inclusion maps

For a future timelike rest momentum, normalize
`P_0=iota(k)/sqrt(q(iota(k)))`. Its stabilizer is

```text
K_k={A | lambda(A)P_0=P_0}=SU(S,P_0)~=SU(2).
```

The inverse of positive `P_0` is an invariant Hermitian form; it maps
`bar S->S^*`. Composing with `epsilon^(-1):S^*->S` gives a
`K_k`-equivariant identification `bar S~=S`. Calling the fundamental
restricted module `W`,

```text
Res_(K_k)F_(m,n)=Sym^m(W) tensor Sym^n(W).
```

Let `Omega=epsilon^(-1) in wedge^2 W`, and let

```text
Delta_(a,b):Sym^(a+b)(W)->Sym^a(W) tensor Sym^b(W)
```

be the bidegree `(a,b)` part of the symmetric-algebra coproduct. For
`0<=r<=min(m,n)), define

```text
I_r:Sym^(m+n-2r)(W)->Sym^m(W) tensor Sym^n(W),
I_r(f)=Omega^r dot Delta_(m-r,n-r)(f).
```

Coproduct, multiplication, and `Omega` are invariant, so `I_r` is an
intertwiner. It is nonzero, as one verifies on a pure symmetric power paired with
a vector of nonzero `epsilon` pairing.

The Clebsch–Gordan theorem contract says these inequivalent images split and
exhaust the tensor product. For `m>=n`, the independent dimension witness is

```text
sum_(r=0)^n [m+n-2r+1]=(m+1)(n+1).
```

Hence

```text
Res_(K_k)F_(m,n)
 ~= direct-sum_(r=0)^min(m,n) Sym^(m+n-2r)(W).
```

Writing `s=(m+n)/2-r` yields

```text
s=|m-n|/2, |m-n|/2+1, ..., (m+n)/2,
```

once each. N3 receives the actual map

```text
j_s^(m,n)=I_r:V_s=Sym^(2s)(W)->Res_(K_k)F_(m,n).
```

For `(m,n)=(2s,0)`, this is the identity and no lower rest spin occurs.

## 7. Null restriction constructs the direct helicity line

The null line `ell` has parabolic stabilizer

```text
P_ell={A in SL(S) | A ell=ell}.
```

The exact momentum stabilizer `K_k` consists of elements whose action on `ell`
has unit modulus: if `A lambda_0=z lambda_0`, preservation of `iota(k)` computes
`|z|^2=1`.

Construct its translation-like subgroup intrinsically:

```text
N_ell={A in P_ell |
       A acts identically on ell and on S/ell}.
```

Composition identifies `N_ell` with the additive space
`Hom(S/ell,ell)~=C`.

This is the same subgroup constructed without spinors in N2a. N2a defines
`N(Q_k)` as the kernel of the action on the screen quotient. The commuting
vector–spinor equation from Section 4 sends a lifted `N_q` to an element fixing
`ell` and acting identically on `S/ell`, hence into `N_ell`. Conversely,
`N_ell` fixes the null vector and acts trivially on its screen quotient, so it
lies over `N(Q_k)`. The two kernels are therefore identified by the spin cover:

```text
c(N(Q_k))=N_ell.
```

Thus the physical branch and carrier branch refer to the same residual frame
motion. Now `N_ell` fixes the canonical line

```text
L_(m,n)=Sym^m(ell) tensor Sym^n(bar ell)
         subset Res_(K_k)F_(m,n)
```

pointwise. With `z=exp(-i theta/2)`, the residual rotation acts by

```text
z^m bar(z)^n=exp(i(n-m)theta/2).
```

Therefore the line inclusion is the intertwiner

```text
j_h^(m,n):C_h->Res_(K_k)F_(m,n),
h=(n-m)/2.
```

This constructs one direct extremal line; it does not classify all invariant
subspaces of mixed carriers. Potential realizations instead use
`ker D(k)/im R(k)` and belong to N3/N4a.

## 8. One bounded generator check

In an oriented orthonormal frame, the bivector map gives rotations `J_i` and
boosts `K_i`. Their brackets imply that closure of `J_i+cK_i` requires
`c^2=-1`. Thus, up to orientation convention,

```text
(J_i+iK_i)/2 in g_+,
(J_i-iK_i)/2 in g_-.
```

This checks the projector signs. No downstream node consumes these generators.

## Exact output consumed downstream

N2b passes

```text
(F_(m,n), Res_(K_k)F_(m,n), j_sigma),
```

where `j_sigma` is `I_r` in the massive case or the direct line inclusion in
the massless case. [N3](03-realization-bridge.md) uses that map to construct the
orbitwise field intertwiner. [N4](04-local-symbol-extension.md) must separately
construct a Lorentz-equivariant polynomial symbol with the stated standard-fiber
kernel. Carrier occurrence does not imply locality.

## Checks and boundary

Supported internally:

- the bivector map preserves the same infinitesimal motion;
- Hodge projectors are complementary and Lorentz natural;
- their images are commuting ideals;
- the spinor action has kernel `{+1,-1}`;
- the commuting equation for `iota` proves vector–spinor equivariance;
- `I_r` constructs massive intertwiners without a weight expansion;
- the null line constructs a helicity character without a triangular matrix.

Theorem contracts own semisimplicity and simple-algebra classification, finite
highest-weight completeness, Clebsch–Gordan splitting, and uniqueness of the spin
cover. Infinite carriers, continuous spin, gauge resolutions, field symbols,
actions, and interactions remain outside this node.
