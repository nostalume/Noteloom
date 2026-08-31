# Massive Spin-One Realization Bridge

Status: supported free massive construction  
Parent node: [N3](03-realization-bridge.md)  
Physical fiber: [N2a spin and helicity](02a-spin-and-helicity.md)  
Scope: proper orthochronous Poincare group, `m>0`, metric `diag(+---)`

## Semantic input

The physical datum constructed in `N2a` is the positive mass shell

```text
O_m^+ = { p | p^2=m^2, p^0>0 }
```

with the spin-one irreducible representation of the little group at
`k=(m,0,0,0)`. Its carrier `V_1=C^3` is the `SU(2)` highest-weight representation
with weights `1,0,-1`, equivalently the ordinary rotation action on `k^perp_C`.

Choose the covariant Lorentz vector carrier `V_vec=C^4`. This is a realization
choice, not an output of the classification.

## Fiber construction

Embed the rest-frame spin fiber by

```text
iota: C^3 -> C^4,
iota(v) = (0,v).
```

Choose standard boosts `B(p)` satisfying `B(p)k=p` and define the polarization
intertwiner

```text
u(p) = B(p) compose iota: C^3 -> p^perp.
```

The codomain follows rather than being assumed. At rest,

```text
k.A = m A^0,
```

so `k^perp` consists exactly of vectors `(0,v)`. Lorentz invariance of the metric
then gives

```text
p.[B(p)iota(v)] = [B(p)k].[B(p)iota(v)] = k.iota(v) = 0.
```

Since `B(p)` is invertible and both spaces have dimension three, it maps `k^perp`
onto `p^perp`.

For `q=Lambda^(-1)p`, the Wigner rotation is

```text
W(Lambda,p) = B(p)^(-1) Lambda B(q).
```

Since `W(Lambda,p)` stabilizes `k`, it acts on `iota(C^3)` as the spin-one
little-group representation. Therefore

```text
Lambda u(q) = u(p) sigma_1(W(Lambda,p)).
```

This is the required particle-to-carrier intertwining identity. Changing standard
boosts conjugates it by a momentum-dependent little-group basis change and does not
change the realized Poincare representation.

## Global particle-to-field map

For `psi in H_(m,1)=L2(O_m^+,dmu;C^3)`, define the momentum-space vector field

```text
[W_vec psi](p) = u(p) psi(p),  p in O_m^+.
```

Combining the preceding identity with the induced state action constructed in `N2`
gives

```text
W_vec U_(m,1)(g) = T_vec(g) W_vec.
```

The Lorentz part is exactly `Lambda u(q)=u(p)sigma_1(W)`; the translation part is
the common Fourier phase `exp(i p.a)`. Thus `W_vec` is a Poincare intertwiner, not
only a fiberwise vector-space map.

Viewed as a spacetime distribution after Fourier transformation, its support and
fiber obey

```text
p^2=m^2,
p.A(p)=0.
```

Conversely, every positive-energy mass-shell vector distribution satisfying
`p.A=0` is recovered by

```text
psi(p) = iota^(-1) B(p)^(-1) A(p).
```

Thus `W_vec` is an isomorphism between the induced physical representation and the
positive-energy transverse solution space. The physical fiber metric is

```text
<A_1,A_2>_phys = -eta(conj(A_1),A_2) on p^perp,
```

which pulls back to the positive Euclidean metric on `C^3`.

## Local covariant equation

The equation is constructed from the physical fiber rather than recognized after a
component calculation. Require:

1. a linear equation on the Lorentz vector carrier;
2. Lorentz covariance;
3. locality with at most two derivatives, so its momentum symbol is polynomial of
   degree at most two;
4. every transverse vector at `p^2=m^2` is a solution;
5. the longitudinal sector has no additional characteristic surface at any real
   momentum.

Using only `eta` and `p`, a parity-even rank-one operator with these properties has
the form

```text
K(p) = alpha(p^2) identity + beta(p^2) p tensor p_flat.
```

For `p.A=0`, this reduces to `alpha(p^2)A`. Condition 4 requires
`alpha(m^2)=0`; minimal differential degree and overall normalization give

```text
alpha(p^2)=m^2-p^2.
```

On a longitudinal vector `A=p`, the eigenvalue is
`alpha(p^2)+beta(p^2)p^2`. At minimal degree `beta` is constant. With
`alpha=m^2-p^2`, any real constant `beta != 1` creates an additional longitudinal
root `p^2=m^2/(1-beta)`; `beta=1` instead leaves the constant eigenvalue `m^2`.
Condition 5 therefore selects `beta=1`. Hence the minimal symbol is

```text
K_Proca(p) A = (m^2-p^2) A + p (p.A)
```

This choice is not claimed unique without the minimal-degree and no-extra-
characteristic conditions. Multiplication by a nowhere-vanishing scalar symbol or
addition of auxiliary fields produces other equations with the same free physical
fiber. Contracting the selected symbol with `p` gives

```text
p.K_Proca(p)A = m^2 (p.A),
```

so `m>0` forces transversality. The remaining equation forces `p^2=m^2` for a
nonzero field. At a standard on-shell momentum,

```text
ker K_Proca(k) = k^perp = iota(C^3),
```

and the stabilizer action on this kernel is exactly `sigma_1`, not merely a
three-dimensional vector space. There is no gauge image in the massive system.

This is a second-order local equation. The first-order field-strength formulation
would be another realization and must not be declared equivalent without its own
explicit maps.

With Fourier convention `partial_mu |-> -i p_mu`, the symbol is the transform of

```text
partial_mu F^(mu nu) + m^2 A^nu = 0,
F_(mu nu) = partial_mu A_nu - partial_nu A_mu.
```

Indeed, transforming the left side gives
`(m^2-p^2)A^nu+p^nu(p.A)`. Thus the familiar Proca equation is the position-space
form of the kernel constructed above, not an independent imported formula.

## Group-function coefficient realization

For a cyclic covector `lambda in (C^4)^*`, package the vector field as

```text
f_A(x,B) = lambda(B^(-1) A(x)).
```

`N2` proves this is a left-Poincare intertwiner. Reconstruction requires choosing a
dual frame in the orbit of `lambda` (equivalently extracting coefficients in a
chosen polynomial/orientation basis). Closing under the right Lorentz action varies
that covector and supplies realization multiplicity; it does not change the
physical little-group fiber.

The finite coefficient function is not an element of the unitary regular
`L2(G)` space in the Lorentz variable. Consequently, this packaging does not supply
the physical Hilbert norm for free.

## Computation decision

No substantial component computation is justified for this case. Orbit reduction
turns every decisive question into an invariant identity:

- equivariance follows from `Lambda B(q)=B(p)W(Lambda,p)`;
- the equation kernel is `p^perp`;
- the little-group action is the defining rotation action on `k^perp`;
- positivity is `-eta` restricted to `p^perp`;
- locality is read from the quadratic polynomial symbol.

A matrix program could recheck these statements in a chosen boost basis, but it
would add transformations without producing new semantic information.

## Economy result for massive spin one

| Route | Semantic path | Extra burden | Result |
| --- | --- | --- | --- |
| direct covariant | little-group fiber -> `u(p)` -> transverse vector -> Proca symbol | choice of standard boosts | complete physical bridge |
| group-function | direct route -> coefficient packaging in `B` -> coefficient reconstruction | non-`L2` orientation sector, right-type multiplicity, basis/frame extraction | same physical bridge, no reduction shown |

For fixed massive spin one, the group-function route is therefore a valid generating
realization but is not computationally preferable to the direct covariant route.
Its possible value must be tested as reusable structure across many carriers or
spins, not inferred from this example.

## Failure boundary

- The result uses `m>0`; the massless limit changes the little group and introduces
  gauge redundancy.
- It treats positive-energy free solutions only.
- It proves no interacting equivalence and introduces no action.
- It does not establish that a chosen scalar group-function equation is simpler
  than Proca; such an equation would require a separate operator-level bridge.
