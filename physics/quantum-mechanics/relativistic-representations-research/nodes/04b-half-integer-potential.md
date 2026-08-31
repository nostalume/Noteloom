# N4b — Half-Integer Spinor-Tensor Potential Complex

Status: uniform free parity-paired half-integer potential family supported on the nonzero null orbit  
Parent criterion: [N4a polynomial complexes](04a-polynomial-complex-details.md)  
Consumes: [N2a physical helicity fibers](02a-spin-and-helicity.md), [N2b Lorentz spinors](02b-lorentz-carriers.md), and [N3 realization bridge](03-realization-bridge.md)  
Produces: a local gauge-potential realization of helicities `+h direct-sum -h` for every `h=n+1/2`
Source contract: [PG-04](../sources/polynomial-gauge-contracts.md)

## Research contract

- **Question:** can the symmetric bosonic screen proof be reconstructed for every
  half-integer helicity without a vector-spinor component elimination?
- **Presumptions:** four-dimensional complexified Minkowski space; the proper
  connected spin cover; a free, constant-coefficient, parity-paired field; a
  finite rank `n`; the positive-energy nonzero null orbit is selected after the
  polynomial characteristic set is computed.
- **Output:** Lorentz carriers, a degree-one gauge map and degree-one equation
  symbol, their polynomial identity, the standard-momentum cohomology as a
  `K_k`-module, and all characteristic strata.
- **Boundary:** no action, Majorana reality condition, interaction, mixed-symmetry
  carrier, or completed infinite tower is inferred.

The tensor rank is `n>=0`; the represented helicity magnitude is

```text
h=n+1/2.
```

`n=0` is the Dirac equation without gauge symmetry, and `n=1` is the
vector-spinor potential branch.

## 1. The vector-spinor bridge constructs Clifford multiplication

N2b constructs the two Weyl spinors and the equivariant vector identification
`V_C~=S tensor bar S`. Their alternating forms turn a vector into maps between
the two chiral spinors. On the direct sum

```text
Delta=S direct-sum bar S,
```

put the two maps off diagonal and call the resulting operator `gamma(v)`. Polarizing
the determinant identity used by N2b computes, on the same spinor pair,

```text
gamma(v)gamma(w)+gamma(w)gamma(v)=2 eta(v,w) identity_Delta.
```

Thus the need to contract a vector index of a spinor-tensor constructs the Clifford
action; gamma matrices are optional coordinate representatives of this map.

Represent a symmetric rank-`n` spinor-tensor by a homogeneous `Delta`-valued
polynomial `psi(u)` of degree `n`. For momentum `p`, construct

```text
P_p psi(u)=(p.u)psi(u),
A_p psi(u)=d/dt psi(u+t p)|_(t=0),
Slash_p=gamma(p),
Gamma psi=gamma dot partial_u psi.
```

The Clifford identity and evaluation on the same polynomial give

```text
Slash_p^2=p^2,
[A_p,P_p]=p^2,
[Gamma,P_p]=Slash_p,
Gamma Slash_p+Slash_p Gamma=2A_p,
Gamma^2=T.
```

`T` is the ordinary Lorentz trace. These five relations replace all subsequent
gamma-matrix and tensor-component expansions.

## 2. The constraints and gauge identity construct the complex

For `n>=1`, construct the gauge and field carriers

```text
G_n={epsilon in Sym^(n-1)(V_C^*) tensor Delta | Gamma epsilon=0},

F_n={psi in Sym^n(V_C^*) tensor Delta | Gamma^3 psi=0}.
```

The field constraint is empty whenever degree makes the third gamma trace
automatic. Define

```text
R_n(p)=P_p:G_n->F_n,
S_n(p)=Slash_p-P_p Gamma:F_n->Sym^n(V_C^*) tensor Delta.
```

First verify the type of `R_n`. For `Gamma epsilon=0`, repeated application of
`Gamma P_p=P_p Gamma+Slash_p` computes

```text
Gamma(P_p epsilon)=Slash_p epsilon,
Gamma^2(P_p epsilon)=2A_p epsilon,
Gamma^3(P_p epsilon)=2A_p Gamma epsilon=0.
```

The equation-gauge composite then reduces to one gamma trace:

```text
S_n(p)P_p
 =Slash_p P_p-P_p(Gamma P_p)
 =-P_p^2 Gamma.
```

It vanishes on `G_n`. Therefore

```text
G_n --R_n(p)--> F_n --S_n(p)--> Sym^n(V_C^*) tensor Delta
```

is a Lorentz-equivariant polynomial complex with first-order gauge and equation
symbols. Gauge invariance has been computed rather than appended to a named
spinor-tensor equation.

For `n=0`, take `F_0=Delta`, omit `G_0`, and use `S_0(p)=Slash_p`.

## 3. Null momentum constructs the spinor-screen fiber

Fix a nonzero null momentum `k` and abbreviate

```text
P=P_k,
A=A_k,
Slash=Slash_k,
S=Slash-P Gamma.
```

If `S psi=0`, applying `Slash` gives

```text
0=Slash(S psi)=Slash^2 psi-P Slash Gamma psi=-P Slash Gamma psi.
```

Multiplication by the nonzero linear polynomial `P` is injective, so

```text
Slash Gamma psi=0.
```

Applying `Gamma` to the original equation and using the same input computes

```text
0=Gamma(S psi)
 =2A psi-2Slash Gamma psi-P Gamma^2 psi,

2A psi=P Gamma^2 psi.
```

On the hyperplane `P(u)=0`, which is `k^perp`, this gives `A psi=0`. The
restriction is therefore constant under `u |->u+t k` and descends through the
radical to the screen quotient `Q_k`.

The spinor value also descends to

```text
W_k=ker(Slash:Delta->Delta),
```

because the equation restricted to `P=0` gives `Slash psi=0`.

It remains to construct the screen gamma-trace condition. Choose one null witness
`a` with `k.a=1`, write `B_a` for differentiation along `a`, and set
`N=gamma(a)`. The Clifford contraction decomposes relative to this witness as

```text
Gamma=N A+Slash B_a+Gamma_Q.
```

Differentiate `S psi=0` with `B_a` and restrict to `P=0`:

```text
0=B_a(S psi)|_(P=0)
 =Slash B_a psi-Gamma psi
 =-Gamma_Q res_k(psi).
```

The last equality uses `A psi|_(P=0)=0`. Hence the equation constructs the map

```text
res_k:ker S_n(k)->H_n(Q_k,W_k),

H_n(Q_k,W_k)
 ={r in Sym^n(Q_k tensor C)^* tensor W_k | Gamma_Q r=0}.
```

Although `a` verifies the displayed decomposition, the restriction, quotient, and
screen Clifford contraction are intrinsic.

## 4. Screen restriction has exactly the gauge kernel

A gauge amplitude restricts to zero because it contains the factor `P`. Section 2
already proves that it lies in `F_n` and in `ker S_n(k)`.

Conversely, let `psi in ker S_n(k)` satisfy `res_k(psi)=0`. It vanishes on the
hyperplane `P=0`, so polynomial division by this linear factor constructs a unique
`epsilon` with

```text
psi=P epsilon.
```

The equation-gauge composite acts on this same `epsilon`:

```text
0=S psi=-P^2 Gamma epsilon.
```

The polynomial ring has no zero divisors, hence `Gamma epsilon=0`; therefore
`epsilon in G_n` and `psi` is gauge.

Surjectivity is constructive. Given `r in H_n(Q_k,W_k)`, choose one witness `a`,
identify the screen with `{k,a}^perp`, and extend `r` constantly along `k` and `a`.
For this extension,

```text
A psi=B_a psi=0,
Slash psi=0,
Gamma psi=Gamma_Q r=0.
```

It therefore lies in `F_n`, solves `S psi=0`, and restricts to `r`. A different
witness changes the lift by an element already proved to be gauge. Multiplication
by `P` is injective, so the complete result is the exact `K_k`-sequence

```text
0 -> G_n --R_n(k)--> ker S_n(k)
  --res_k--> H_n(Q_k,W_k) -> 0.
```

Every map is natural under the stabilizer. Consequently

```text
ker S_n(k)/im R_n(k) ~= H_n(Q_k,W_k)
```

as a little-group representation.

## 5. Screen Clifford reduction computes helicity `n+1/2`

The null Clifford operator satisfies `Slash^2=0`. The witness `N=gamma(a)` obeys
`Slash N+N Slash=2`, so for every `w in ker Slash`,

```text
w=(1/2)Slash N w.
```

Thus `ker Slash=im Slash`; on the four-dimensional Dirac carrier, `W_k` is
two-dimensional. N2b's chiral null lines identify it as

```text
W_k~=C_(+1/2) direct-sum C_(-1/2),
```

and its null translations act trivially.

Use the metric and orientation of `Q_k` to split its complexification into
isotropic rotation lines `L_+ direct-sum L_-`. Choose nonzero
`q_+ in L_+`, `q_- in L_-` with `eta_Q(q_+,q_-)=1`, and let `z_+,z_-` be the
corresponding polynomial coordinates of rotation weights `+1,-1`. Clifford
multiplication preserves `W_k`, because for `q in k^perp` and `w in W_k`,

```text
Slash gamma(q)w=-gamma(q)Slash w=0.
```

The operation depends only on the screen class. Replacing a lift by `q+beta k`
acts on the same `w` as

```text
gamma(q+beta k)w=gamma(q)w+beta Slash w=gamma(q)w.
```

Write `c_+=gamma(q_+)|_(W_k)` and `c_-=gamma(q_-)|_(W_k)`. Evaluating the
Clifford relation on this two-dimensional space gives

```text
c_+^2=c_-^2=0,
c_+c_-+c_-c_+=2I.
```

Neither map can vanish because their anticommutator is invertible. A nonzero
square-zero endomorphism of the two-dimensional `W_k` has rank one and
one-dimensional kernel. Their kernels are distinct: a common kernel vector would
be killed by the displayed anticommutator. Thus they construct the two lines

```text
W_+=ker c_+,
W_-=ker c_-.
```

N2b already identifies the only two rotation characters in `W_k` as `+1/2` and
`-1/2`. Equivariance of `c_+`, whose weight is `+1`, makes its nonzero part map
the `-1/2` line to the `+1/2` line; hence `W_+` has weight `+1/2`. Similarly
`W_-` has weight `-1/2`. Choose nonzero `w_+ in W_+`, `w_- in W_-`.

Raising the polynomial derivative index with the screen metric gives the intrinsic
operator in these eigenlines:

```text
Gamma_Q=c_+ partial_(z_+)+c_- partial_(z_-).
```

For

```text
r=f_+(z_+,z_-)w_+ + f_-(z_+,z_-)w_-,
```

the two summands of `Gamma_Q r` land in the distinct lines `W_+` and `W_-`.
Evaluating them on the same polynomial computes

```text
Gamma_Q r
 =(partial_(z_-)f_+)c_-w_+
  +(partial_(z_+)f_-)c_+w_-,

partial_(z_-)f_+=0,
partial_(z_+)f_-=0.
```

Homogeneity of degree `n` then gives

```text
r=alpha_+ z_+^n w_+ + alpha_- z_-^n w_-.
```

The two lines have rotation weights `+(n+1/2)` and `-(n+1/2)`, up to the declared
sign convention. Null translations act trivially on both `Q_k` and `W_k`. Hence

```text
H_n(Q_k,W_k)
 ~=C_(+(n+1/2)) direct-sum C_(-(n+1/2)).
```

The exact sequence has therefore recovered the required parity-paired physical
fiber, not only two unnamed degrees of freedom.

## 6. Non-null and zero momentum strata

Let `p^2!=0` and suppose `S_n(p)psi=0`, so

```text
Slash_p psi=P_p Gamma psi.
```

Apply `Gamma^2` to both sides. Since `Gamma^2` commutes with `Slash_p`, while
`Gamma^2P_p=P_pGamma^2+2A_p`, the triple gamma-trace constraint computes

```text
Slash_p Gamma^2 psi=2A_p Gamma psi.
```

Construct

```text
epsilon=(1/p^2)Slash_p Gamma psi.
```

Its gamma trace vanishes by semantic coincidence of the preceding identity:

```text
Gamma epsilon
 =(1/p^2)(2A_p Gamma psi-Slash_p Gamma^2 psi)
 =0.
```

Multiplying the field equation by `Slash_p` now gives

```text
p^2 psi=P_p Slash_p Gamma psi=p^2 P_p epsilon,
```

so every solution is gauge. The converse is the gauge identity from Section 2.
Therefore

```text
p^2!=0 => ker S_n(p)/im R_n(p)=0.
```

At nonzero null `p`, Sections 3--5 give helicities
`+(n+1/2) direct-sum -(n+1/2)`. At `p=0`, both symbols vanish and the cohomology is
the full constrained carrier `F_n`. Thus the real characteristic set is the null
cone: future-null and past-null orbits plus the exceptional origin. Positive energy
selects the future orbit after the local equation is constructed.

## 7. Spacetime equation and supported boundary

Fourier substitution turns the same polynomial complex into

```text
Gamma^3 Psi=0,
Gamma Epsilon=0,

[gamma(i partial)-P_(i partial)Gamma]Psi=0,
Psi -> Psi+P_(i partial)Epsilon.
```

The exact screen sequence proves that its gauge-inequivalent positive-energy plane
waves carry helicities `+(n+1/2) direct-sum -(n+1/2)`. At `n=1`, this is the
massless vector-spinor potential with physical helicities `+3/2` and `-3/2`; no
separate vector-spinor component count is required.

Supported internally:

- the Clifford operator algebra and polynomial gauge identity;
- the field and parameter constraint compatibility;
- the intrinsic null-screen exact sequence;
- the two little-group characters;
- vanishing cohomology for every non-null momentum;
- explicit future/past/origin characteristic strata.

Still separate:

- the formally self-adjoint Euler representative and admissible causal response
  are now constructed in [N4i](04i-half-integer-green-construction.md), while
  [N4j](04j-half-integer-causal-quotient.md) proves causal quotient bijectivity and
  [N4k](04k-half-integer-positive-frequency.md) constructs the positive
  particle/antiparticle completion; [N4l](04l-half-integer-support-faithfulness.md)
  proves its gauge-rank faithfulness, while density remains open;
- Majorana or other reality conditions;
- massive spinor-tensor alternatives;
- mixed-symmetry fermionic fields, interactions, and tower completion.

## Computation decision

The all-rank proof closes through Clifford identities, restriction, and polynomial
division. A separate bounded
[fiber-rank check](../computation/04b-half-integer-potential/README.md) constructs a
realification of the Dirac operators and verifies tensor ranks `0` through `3` at
null, non-null, and zero momentum. The calculation is independent evidence, not a
replacement for the exact sequence.

## Source boundary

- J. Fang and C. Fronsdal,
  [Massless fields with half-integral spin](https://doi.org/10.1103/PhysRevD.18.3630),
  is the primary source for the symmetric spinor-tensor potential, triple
  gamma-trace field constraint, gamma-traceless gauge parameter, and arbitrary
  finite half-integer scope.
- The source validates the historical equation family. The Clifford identities,
  polynomial lift, screen exact sequence, little-group action, and characteristic
  calculation used here are constructed inside this node.
