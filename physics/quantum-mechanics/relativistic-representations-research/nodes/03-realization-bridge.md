# N3 — When a Field Represents the Same Particle

Status: universal orbitwise bridge supported  
Consumes: the representation spaces from [N2](02-three-representation-spaces.md), the physical fibers from [N2a](02a-spin-and-helicity.md), and the explicit restricted-carrier intertwiners from [N2b](02b-lorentz-carriers.md)  
Produces: the criterion consumed by [N4](04-local-symbol-extension.md)  
Technical details: [N3c](03c-realization-details.md)

## Read this node as one question

The physical state and the covariant field live in different representation
spaces. What exact map proves that they describe the same particle?

```text
physical states H_(O,sigma)
  -> field solutions or field cohomology over O
  -> optional scalar coefficient packaging on the Poincare group.
```

The last arrow is not needed for physical equivalence.

## 1. The spaces have different jobs

| Space | Job | Important property |
| --- | --- | --- |
| `H_(O,sigma)` | physical one-particle states | unitary, on shell |
| `Gamma_F'` | distributions valued in a Lorentz carrier `F` | covariant, generally off shell and nonunitary before constraints |
| `F_(rho,lambda)` | scalar functions that encode components of `Gamma_F'` | algebraic packaging, not the physical Hilbert space |
| `L2(G)` | regular unitary representation on the full Poincare group | larger and analytically different from the finite coefficient sector |

Therefore the primary bridge is `H_(O,sigma) -> Gamma_F'`. Group functions can
encode its output but do not automatically construct it.

## 2. Ordinary fields: one fiber map determines the bridge

At standard momentum `k`, the physical internal space is `V_sigma`, carrying the
little-group action `sigma`. Choose a Lorentz carrier `rho:L_spin->GL(F)`.

A candidate embedding at `k` is

```text
j:V_sigma->F.
```

For the finite carriers constructed in N2b, this is not an existential placeholder:
the massive maps are the invariant inclusions `I_r`, and the direct massless map
is the inclusion of the null extremal line.

It preserves the physical meaning of a residual frame change exactly when

```text
j sigma(r)=rho(r)j,       r in K_k.
```

This single identity constructs a map over the whole momentum orbit. For the
associated-bundle representative `[A,v]`, set

```text
J_j[A,v]=(A k,rho(A)j(v)).
```

The quotient identifies `(A r,v)` with `(A,sigma(r)v)`. Applying `J_j` to both
representatives gives

```text
J_j[A r,v]
  =(A k,rho(A)rho(r)j(v))
  =(A k,rho(A)j sigma(r)v)
  =J_j[A,sigma(r)v].
```

Thus the map is well defined. Conversely, an equivariant orbit map is fixed by its
value over `k`, and that value must obey the same identity. Hence

```text
ordinary orbit realizations
  <-> Hom_(K_k)(V_sigma,F restricted to K_k).
```

This statement is independent of the value of spin or helicity.

## 3. The fiber map gives the Poincare intertwiner

Choose `B(p)k=p` only to write the map in coordinates:

```text
[W_j psi](p)=rho(B(p))j psi(p).
```

If `B'(p)=B(p)r(p)`, the same state has coordinates
`psi'(p)=sigma(r(p))^(-1)psi(p)`. Then

```text
rho(B')j psi'
  =rho(B)rho(r)j sigma(r)^(-1)psi
  =rho(B)j psi.
```

So the field does not depend on the arbitrary standard boost. For a Lorentz
transformation `A`, let `q=A^(-1)p` and

```text
w(A,p)=B(p)^(-1)A B(q) in K_k.
```

Acting on the same wavefunction computes

```text
rho(A)[W_j psi](q)
  =rho(B(p))rho(w(A,p))j psi(q)
  =rho(B(p))j sigma(w(A,p))psi(q).
```

The right side is `W_j` applied to the induced state action. Translations give the
same Fourier phase on both sides. Therefore

```text
W_j U_(O,sigma)(g)=T_rho(g)W_j.
```

If `j` is injective, this is a faithful physical realization. The physical inner
product is transported through `W_j`; it need not equal a momentum-independent
positive form on the finite Lorentz carrier.

## 4. Gauge fields: the physical fiber is a quotient

For a potential, the physical helicity may not occur as a literal subspace of
`F`. Construct at `k`

```text
G --R_k--> F --D_k--> E,
D_k R_k=0.
```

`K_k` equivariance preserves both `ker D_k` and `im R_k`, so it acts on

```text
H_k=ker D_k/im R_k.
```

The field describes the particle exactly when there is a little-group
intertwining isomorphism

```text
V_sigma ~= H_k.
```

Assume `G,F,E` are restrictions of Lorentz carriers with actions
`rho_G,rho_F,rho_E`. Transport the two maps explicitly:

```text
R_p = rho_F(B(p)) R_k rho_G(B(p))^(-1),
D_p = rho_E(B(p)) D_k rho_F(B(p))^(-1).
```

If `B'(p)=B(p)r` with `r in K_k`, equivariance computes

```text
rho_F(B r) R_k rho_G(B r)^(-1)
 =rho_F(B)[rho_F(r)R_k rho_G(r)^(-1)]rho_G(B)^(-1)
 =R_p,
```

and identically for `D_p`. Thus the transported maps, their kernels, their
images, and their quotient do not depend on the chosen standard boost. Moreover,

```text
D_p R_p
 =rho_E(B(p))[D_k R_k]rho_G(B(p))^(-1)
 =0.
```

Transporting the little-group isomorphism `V_sigma~=H_k` now uses the same
associated-bundle computation as Section 2. It gives an orbit bundle isomorphism
before any analytic completion. Consequently

```text
H_(O,sigma)
  ~= positive-energy sections of the transported field cohomology.
```

The passage from smooth orbit sections to a completed Hilbert or distribution
space is an analytic theorem contract: it requires the invariant orbit measure,
measurable transport, and the chosen positive-energy completion from N2.

An ordinary field is the special case with no gauge image. Auxiliary fields are
physically harmless only when their added complex is exact.

## 5. What N3 proves—and what N4 must add

N3 is orbitwise and representation-theoretic:

```text
V_sigma appears as a carrier subspace or field-complex subquotient
  -> the field realizes the same Poincare representation.
```

This does not yet ensure a local spacetime equation. Local finite-order equations
require the transported maps to extend polynomially away from the orbit. The exact
next obligation is

```text
input:
  Lorentz carriers G,F,E,
  standard-fiber maps R_k,D_k,
  j_bar:V_sigma ~= ker D_k/im R_k,
  desired polynomial degree/locality bound;

output:
  equivariant polynomial maps R(p),D(p),
  D(p)R(p)=0,
  ker D(k)/im R(k) ~= V_sigma,
  declared characteristic set and failure boundary.
```

Existence of the fiber intertwiner does not imply existence of this extension.
[N4](04-local-symbol-extension.md) constructs one direct chiral extension for every
finite spin and helicity. [N4a](04a-polynomial-complex-details.md) retains the
general polynomial-complex and characteristic-set obligations for potential or
auxiliary-field alternatives.

## 6. Where group functions enter

For a cyclic covector `lambda in F^*`, encode a covariant field by

```text
[C_(rho,lambda)Phi](x,B)
  =lambda(rho(B^(-1))Phi(x)).
```

This map is injective on the finite carrier and intertwines the left Poincare
action. It points from fields to coefficient functions:

```text
H_(O,sigma) --W--> Sol(D)/Gauge inside Gamma_F'
                                   |
                                   | C_(rho,lambda)
                                   v
                         finite coefficient functions.
```

It does not identify the result with the regular Hilbert space `L2(G)`, and it
does not reduce computation unless an equation or observable can be constructed
more cheaply in the coefficient representation. The analytic proof and economy
criteria are retained in [N3c](03c-realization-details.md).

## Output and open boundary

Supported:

- ordinary realizations are classified orbitwise by little-group intertwiners;
- gauge realizations are classified by the little-group cohomology of the fiber
  complex;
- either construction produces an explicit Poincare intertwiner;
- group-function coefficients are optional downstream packaging.

Still open outside this node:

- classification of every alternative Lorentz carrier containing a given fiber;
- polynomial potential resolutions and their extra characteristic branches;
- parity, reality, action, interaction, and countable-tower completion.

[N10h](10h-carrier-to-grammar.md) sharpens the first two boundaries: once a
symmetric off-shell carrier functor is declared, its invariant operator grammar can
be generated and consumed by the residual solver; the physical fiber or Lorentz
label alone is correctly refused because it does not choose that presentation.

## Downstream interacting reversal

[N4s](04s-field-particle-extraction.md) reverses this node's question for an
interacting field theory. It constructs candidate particle spaces from the
translation spectral measure and interpolating field operations, then asks when
the resulting quotient is stable and asymptotic. N3 and N4s are inverse only when
the field-generated shell image is complete and carries the same induced
representation constructed here.
