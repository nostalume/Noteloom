# Multiplicity-valued `SU(3)` differential-operator bench

## Why the finite transition bench was insufficient

The [outer-multiplicity constructor](tensor-operator-su3.md) generated the two
maps in `Hom_SU(3)(8 tensor 8,8)` and proved that an exchange-paired observable
needs both. It did not yet make those maps the reduced action of a differential
operator.

The earlier scalar candidate `M_(f_ell)(1+Delta)` presents a specific obstruction:
its two octet copies become distinguishable only after constructing a full
Peter--Weyl projection of a product of scalar matrix coefficients. Declaring that
projection as an input would relocate the component problem into a black box.

The smallest constructive repair is to retain the adjoint fiber on which the two
natural products already act. This bench asks whether that repair produces an
actual order-two PDE witness with domain, core, analysis, synthesis, and observable
recovery.

## Typed analytic problem

Let `G=SU(n)`, for `n=2` or `3`, and let `V=sl_n(C)`. Use normalized Haar measure
and the positive bi-invariant Laplacian whose generators satisfy

```text
tr(T_a T_b)=delta_ab/2.                                 (1)
```

The analytic carrier and operator domain are

```text
H=L^2(G,V),
Dom(T_X)=H^2(G,V),
C=C^infinity(G,V).                                     (2)
```

For `X in V`, construct the adjoint matrix coefficient

```text
q_X(g)=Ad_(g^-1)X.                                     (3)
```

Pointwise multiplication by `q_X` is smooth and bounded on compact `G`. Therefore
the following natural-map family is a bounded map `H^2 -> L^2` and a differential
operator of order at most two:

```text
T_X^(a,b) u
  = a [q_X,(1+Delta)u]
    + b {q_X,(1+Delta)u}_0.                            (4)
```

Here `{A,B}_0=AB+BA-(2/n)tr(AB)I`. Equation (4) is a supplied dynamics family;
the group constrains its two channels but does not determine `a,b`.

## Covariance is computed before decomposition

Let left translation be `(L_h u)(g)=u(h^-1 g)`. Applying it to (3) gives

```text
(L_h q_X)(g)
  = Ad_(g^-1 h)X
  = Ad_(g^-1)(Ad_h X)
  = q_(Ad_h X)(g).                                     (5)
```

The Laplacian commutes with `L_h`, and the bracket, traceless Jordan product, and
trace are conjugation-natural. Applying both sides of the conjugated operator to
the same `u` therefore gives

```text
L_h T_X L_h^-1 = T_(Ad_h X).                           (6)
```

Thus `X -> T_X` is an adjoint-type differential-operator family. No coordinate
chart or component-valued coefficient table was introduced.

## The visible Peter--Weyl core

Let `S:V -> H` be `S(Y)=q_Y`. Equation (5) shows that its image `Q(V)` is one
adjoint matrix-coefficient copy in the smooth Peter--Weyl core. Define analysis
only on this visible copy by

```text
A(q_Y)=Y,
A S=I_V,
S A=Q.                                                 (7)
```

The Casimir theorem contract associated with normalization (1) supplies

```text
Delta q_Y=C_A q_Y,   C_A=n.                            (8)
```

Now apply (4) to the constructed input `S(Y)`. Naturality of (3) and (8) produce
the uninterrupted equality

```text
T_X S(Y)
  =(n+1)[a[q_X,q_Y]+b{q_X,q_Y}_0]
  =q_((n+1)[a[X,Y]+b{X,Y}_0])
  =S R_X(Y),                                           (9)

R_X(Y)=(n+1)[a[X,Y]+b{X,Y}_0].                         (10)
```

Consequently

```text
A T_X S=R_X,   T_X S-S R_X=0.                         (11)
```

Equations (9)--(11), not a matching spectrum label, are the bilateral coincidence
on this finite core.

## Observable use and transfer

For a probe `Z in V`, define the visible observable by

```text
O_Z(q_W)=tr(ZW).                                       (12)
```

The `SU(3)` fixture uses `X=E_12`, `Y=E_23`, `Z=E_31`, `a=1/2`, and `b=3/4`.
Since `C_A=3`, equations (10)--(12) give

```text
O_Z(T_X q_Y)=5,
O_Z(T_Y q_X)=1,
odd contribution=2,
even contribution=3.                                  (13)
```

The same PDE schema transfers to `SU(2)`. There `C_A=2` and polarized
Cayley--Hamilton kills the traceless Jordan map. With `a=2/3`, the fixture returns
`(4,-4)` and one visible channel. An `L^2`-only input domain is refused with
`DomainContractObstruction`, because `(1+Delta)u` is not defined there as the
declared `L^2` output.

## Whole-route cost and meaning

For `SU(3)`, the component presentation is eight coupled scalar fields with up to
`8^3=512` bilinear coupling entries. The natural route still has eight fiber
degrees of freedom; it does not win by relabeling the carrier as one matrix. Its
gain is that, on the admitted Casimir eigenmodule, the spatial differential solve
is replaced by one scalar while the coupling table is replaced by two couplings,
two natural matrix products, and one trace pairing. No coordinates, weights, or
Clebsch--Gordan components occur.

This is exact semantic and human compression, plus reduced per-query algebra on
the declared core. It is not a full `L^2(G,V)` solver: constructing every
Peter--Weyl multiplicity copy, the spectrum of the non-invariant family, and a
discretized runtime baseline remain unpaid. Self-adjointness is neither asserted
nor required for the transition observable.

## Artifacts and bounded verdict

- Router: `../computation/su_adjoint_multiplicity_router.py`
- `SU(3)` fixture: `../computation/examples/su-adjoint-pde-su3.json`
- `SU(2)` transfer: `../computation/examples/su-adjoint-pde-su2.json`
- Domain refusal: `../computation/examples/su-adjoint-pde-wrong-domain.json`
- Public tests: `../computation/test_reduction_workbench.py`

F4 passes on one adjoint coefficient copy: the multiplicity-valued reduced map is
now the exact action of a domain-typed order-two PDE. The scalar-product projection
problem is parked, not silently solved. The next bilateral bridge must remove the
supplied group label and reconstruct the effective non-Abelian algebra from the
matrix PDE family.
