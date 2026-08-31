# Massless Helicity-One Realization Bridge

Status: supported free complexified construction  
Parent node: [N3](03-realization-bridge.md)  
Consumes: the typed orbit, bundle, and induced action constructed in
[N2](02-three-representation-spaces.md), and the physical character constructed in
[N2a](02a-spin-and-helicity.md)  
Scope: proper orthochronous spin-cover Poincare group, nonzero positive-energy
null orbit, metric `diag(+---)`

## Development contract

- **Question:** how does a finite-helicity particle representation become a local
  covariant electromagnetic potential or curvature without identifying gauge
  redundancy with a physical state?
- **Presumptions:** one free linear field on Minkowski spacetime; finite helicity,
  not continuous spin; polynomial local symbols of Maxwell order; complex fields
  until a reality or parity condition is added.
- **Semantic input:** the physical state is a unitary induced representation on the
  positive null orbit. A covariant vector or two-form is additional realization
  data.
- **Output:** the null little group, its helicity quotient, the Maxwell symbol
  complex, particle-to-potential and particle-to-curvature intertwiners, physical
  norm, locality, and group-function boundary.
- **Failure boundary:** interactions, nontrivial spacetime topology, zero momentum,
  continuous spin, Fock quantization, and global gauge fixing are not derived.

No heavy computation packet is required. Every decisive operation reduces to a
four-dimensional invariant identity or a two-dimensional transverse quotient.

## 1. Fixing a null momentum constructs its transverse plane

Choose a nonzero future null momentum `k` and another null vector `n` such that

```text
k^2 = n^2 = 0,
k.n = 1.
```

Their common orthogonal complement

```text
E = { x | x.k=0 and x.n=0 }
```

is two-dimensional, and `-eta` is positive definite on it. Choose an oriented
orthonormal basis `e_1,e_2` of `E`, so

```text
e_i.e_j = -delta_(ij).
```

The hyperplane orthogonal to `k` decomposes as

```text
k^perp = span(k) direct-sum E.
```

This decomposition depends on `n`, but the quotient

```text
Q_k = k^perp / span(k)
```

does not. The Minkowski form has radical `span(k)` on `k^perp`: if an element of
`k^perp` is orthogonal to all of `k^perp`, it belongs to
`(k^perp)^perp=span(k)`. Therefore

```text
< [u],[v] >_Q = -eta(conj(u),v)
```

is a well-defined positive-definite Hermitian form on `Q_k`. The quotient is the
intrinsic transverse plane; the chosen `E` is only a representative of it.

## 2. Consume the intrinsic null-stabilizer sequence

N2a constructs the screen space and the exact sequence

```text
Q_k=k^perp/span(k),

1 -> (Q_k,+) --N--> K_k -> Spin(Q_k) -> 1.
```

For `q=[xi]`, the translation-like element is the representative-independent map

```text
N_q(v)
 =v+(k.v)xi-[xi.v+(xi^2/2)(k.v)]k.
```

N2a verifies metric preservation, `N_qN_r=N_(q+r)`, and the conjugation law.
The screen `E={k,n}^perp` chosen in Section 1 is now only a local reading of this
intrinsic result. For `x in E`,

```text
N_q x=x-(xi.x)k.
```

This bounded formula is retained because the potential quotient below consumes
the displayed gauge direction; it is not used to construct the group.

## 3. Consume the physical helicity character

N2a also computes the finite-spectrum obstruction. A finite-dimensional unitary
little-group fiber has only finitely many joint characters of `Q_k`, whereas
every nonzero character has a full circular orbit under `Spin(Q_k)`. Therefore
the translation spectrum is `{0}` and

```text
sigma_h(N_q)=1,
sigma_h(theta)=exp(i h theta),
h in (1/2)Z.
```

For electromagnetism, the two possible direct characters are `h=+1` and `h=-1`.
Each is irreducible under the proper connected group. A real or parity-complete
field contains both only after adding that extra presumption.

## 4. The potential carrier constructs gauge equivalence

Let `V_C` be complexified Minkowski vector space. At `k`, the condition needed for
a transverse potential is

```text
P_k = { a in V_C | k.a=0 } = k^perp_C.
```

The little group preserves `P_k`, but its null translations do not act as physical
helicity rotations. For `x in E_C`, the calculation from Section 2 gives

```text
N_q x = x-(xi.x)k,  q=[xi].
```

The change is proportional to `k` and vanishes only after quotienting. This
constructs the gauge line

```text
G_k = span_C(k)
```

and the physical potential fiber

```text
H_A(k) = P_k/G_k
       = k^perp_C/span_C(k)
       = Q_k tensor C.
```

The null translations now act trivially because

```text
[N_q x] = [x-(xi.x)k] = [x].
```

For circular transverse vectors

```text
e_+ = (e_1+i e_2)/sqrt(2),
e_- = (e_1-i e_2)/sqrt(2),
```

a transverse rotation acts by opposite phases. With the chosen orientation,

```text
S_theta [e_+] = exp(-i theta)[e_+],
S_theta [e_-] = exp(+i theta)[e_-].
```

Thus `H_A(k)` is the direct sum of helicities `-1` and `+1` under this convention.
The quotient proves the representation, not merely its dimension. It also explains
why a covariant potential changes by a gauge term under the translation-like part
of the massless little group.

## 5. The local Maxwell complex constructs the same quotient

For any nonzero momentum `p`, use `eta` to identify it with a vector when taking
contractions. Construct the gauge, curvature, and equation symbols by

```text
R(p): C -> V_C,             R(p)alpha = p alpha,
d(p): V_C -> wedge^2 V_C,  d(p)a = p wedge a,
delta(p): wedge^2 V_C -> V_C,  delta(p)F = i_p F.
```

The first semantic coincidence is nilpotence:

```text
d(p)R(p)alpha
  = p wedge (p alpha)
  = 0.
```

Thus curvature forgets exactly the candidate gauge direction. The potential
equation symbol is the constructed composite

```text
K_Max(p) = delta(p)d(p),

K_Max(p)a
  = i_p(p wedge a)
  = p^2 a-p(p.a).
```

It annihilates every gauge vector at every momentum:

```text
K_Max(p)R(p)alpha
  = p^2 p alpha-p(p^2 alpha)
  = 0.
```

At a nonzero null momentum `k`, evaluation gives

```text
K_Max(k)a = -k(k.a),

ker K_Max(k) = k^perp_C,
im R(k) = span_C(k).
```

Therefore the physical cohomology of the symbol complex is

```text
H_Max(k)
  = ker K_Max(k) / im R(k)
  = k^perp_C/span_C(k)
  = H_A(k).
```

The null orbit is also constructed as the only non-gauge characteristic. If
`p^2!=0` and `K_Max(p)a=0`, then

```text
a = p (p.a)/p^2,
```

which lies in `im R(p)` and has zero curvature. Hence the physical quotient is zero
off the null cone; non-gauge plane-wave solutions occur only at `p^2=0`.

In position space, with an inessential Fourier-sign choice, the same complex is

```text
alpha |-> A+d alpha,
F=dA,
delta F=0.
```

The operator is local: `R` and `d` are first order and `K_Max` is second order.
Gauge invariance is the exact identity `K_Max R=0`, not an additional verbal
symmetry attached after the equation.

## 6. Curvature is the gauge-free realization

The curvature map descends to the quotient because `d(p)R(p)=0`:

```text
d_bar(p): H_Max(p) -> wedge^2 V_C,
d_bar(p)[a] = p wedge a.
```

At nonzero null `p`, it is injective. Indeed,

```text
p wedge a=0
  => a in span_C(p)
  => [a]=0.
```

Its image can be constructed without a component expansion. Let `F` satisfy

```text
p wedge F=0,
i_p F=0.
```

Choose `n` with `n.p=1`. Contracting the first equation gives

```text
0 = i_n(p wedge F)
  = F-p wedge (i_n F),

F = p wedge a,  a=i_n F.
```

The second equation then reads

```text
0 = i_p F = i_p(p wedge a) = K_Max(p)a.
```

Thus `d_bar(p)` is onto the closed and coclosed curvature fiber. We have constructed
the isomorphism

```text
H_Max(p)
  ~= { F in wedge^2 V_C | p wedge F=0 and i_p F=0 }.
```

In four Lorentzian dimensions, `star^2=-1` on complex two-forms. The projectors

```text
F^(+) = (F-i star F)/2,
F^(-) = (F+i star F)/2
```

split the curvature fiber into its two one-dimensional circular sectors. Their
rotation characters are the two helicities above; which sign is called `+1`
depends on the orientation and Fourier convention. A single complex helicity may
therefore be represented by one duality sector, while a real curvature relates the
two sectors by complex conjugation.

## 7. Particle-to-field intertwining

Choose standard transports `B(p)` on the positive null orbit and define transverse
polarization representatives

```text
epsilon_h(p) = B(p)e_h,  h in {+1,-1}.
```

For a Lorentz transformation `A`, put `q=A^(-1) dot p`. The Wigner element
constructed in `N2` satisfies

```text
Lambda(A)B(q) = B(p)W(A,p).
```

Every `W(A,p)` is a transverse rotation followed by a null translation. Section 2
computes its action on a circular representative as

```text
W(A,p)e_h
  = exp(i h theta(A,p))e_h + c_h(A,p)k
```

for a convention-dependent scalar `c_h`. Applying `B(p)` gives

```text
Lambda(A)epsilon_h(q)
  = exp(i h theta(A,p))epsilon_h(p)+c_h(A,p)p.
```

The second term is exactly in `im R(p)`. Therefore

```text
[Lambda(A)epsilon_h(q)]
  = exp(i h theta(A,p))[epsilon_h(p)]
```

in `H_Max(p)`. This is the little-group intertwiner required by `N3`.

For a helicity wavefunction `psi_h(p)`, define

```text
[W_A psi_h](p) = [epsilon_h(p)psi_h(p)],

[W_F psi_h](p) = p wedge epsilon_h(p) psi_h(p).
```

The first map intertwines into the potential quotient; it does not intertwine into
unquotiented vectors because of the displayed gauge term. The second map is an
ordinary covariant intertwiner because wedging with `p` kills that term:

```text
p wedge [c_h(A,p)p] = 0.
```

Translations multiply all three realizations by the same character `exp(i p.a)`.
Hence `W_A` and `W_F` intertwine the full proper orthochronous Poincare action.

The positive fiber form from Section 1 makes the quotient unitary:

```text
||[a]||_phys^2 = -eta(conj(a),a).
```

It is independent of the representative because `k` is the radical of `k^perp`.
With normalized `e_h`, its orbit integral is exactly the induced one-particle norm
up to the chosen overall normalization of the polarization and orbit measure.

## 8. Group-function packaging and semantic economy

The vector coefficient map from `N2` packages a potential as

```text
C_A(A_field)(x,B)
  = lambda(D_vec(B^(-1))A_field(x)).
```

It does not descend unchanged to the physical quotient. A gauge shift computes

```text
C_A(A_field+d alpha)-C_A(A_field)
  = lambda(D_vec(B^(-1))d alpha),
```

which is generally nonzero. One must either quotient the coefficient image by the
packaged gauge image or package the curvature instead:

```text
C_F(F)(x,B)
  = lambda_2(D_(wedge^2)(B^(-1))F(x)).
```

The curvature route is gauge invariant because `F` itself is unchanged by
`A -> A+d alpha`. Both coefficient sectors remain finite nonunitary Lorentz
sectors, not the regular Hilbert space `L2(G)`.

| Route | Semantic path | Extra burden | Supported result |
| --- | --- | --- | --- |
| potential quotient | helicity fiber -> polarization class -> Maxwell cohomology | representative and gauge quotient | shortest local potential bridge |
| curvature | helicity fiber -> `p wedge epsilon_h` -> closed/coclosed two-form | larger carrier, Bianchi identity | gauge-free single-helicity split available |
| group-function potential | potential route -> orientation coefficients -> coefficient gauge quotient | non-`L2` sector and two quotients | no reduction at fixed helicity |
| group-function curvature | curvature route -> orientation coefficients | non-`L2` sector and coefficient reconstruction | valid packaging, no economy yet shown |

For fixed helicity one, the group-function route adds a representation change and
does not reduce the construction or verification cost. Its possible economy remains
a general-spin reuse question, not a conclusion from this example.

## Checks and source bindings

- the exact sequence, `N_qN_r=N_(q+r)`, and rotation conjugation construct the
  null little group without making a screen choice part of the result.
- The action on `k^perp/span(k)` proves trivial null translations and helicities
  `+/-1`, rather than relying on a dimension count.
- `K_Max R=0`, `ker K_Max(k)=k^perp`, and `im R(k)=span(k)` compute the physical
  quotient.
- The contraction with `n` proves that closed curvature is exact at nonzero fixed
  momentum; no global topological claim is made.
- [Bekaert--Boulanger](https://arxiv.org/abs/hep-th/0611263), Sections 3.2 and 5.3.1,
  independently verify the `ISO(2)` helicity/continuous-spin boundary and the
  closed-coclosed Maxwell curvature formulation.
- [Weinberg 1964](https://doi.org/10.1103/PhysRev.134.B882) is the primary check for
  the gauge term produced when a massless finite-helicity state is realized by a
  covariant potential.

The sources validate theorem boundaries and conventions. The quotient and every
intertwining identity used here were constructed explicitly.

## Supported output and open boundary

The massless helicity-one realization is now supported as

```text
H_(0,+1) direct-sum H_(0,-1)
  ~= positive-energy Maxwell solutions / gauge
  ~= positive-energy closed-coclosed curvature solutions.
```

For one complex helicity, restrict the curvature to one duality sector. For a real
electromagnetic field, impose the conjugation relation pairing the two sectors.

Still open:

- whether a scalar operator on the Poincare group reproduces this complex with
  fewer semantic transformations across a family of spins;
- how the free quotient changes under interactions or on topologically nontrivial
  spacetime;
- the `N4` construction problem of extending standard-momentum cohomology to a
  Lorentz-equivariant polynomial complex with no unexplained characteristic modes.
