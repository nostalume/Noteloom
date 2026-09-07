# `SU(3)` outer-multiplicity execution bench

## Spine binding

- **Upstream:** the group-typed differential-operator calculus predicts the
  reduced channel `Hom_G(A tensor V_lambda,V_mu)`.
- **Bridge question:** can a channel of dimension greater than one be constructed
  and used without weights or Clebsch--Gordan component tables?
- **Invariant target:** ordered and exchange-reversed adjoint transition
  amplitudes on one source/target sector.
- **Downstream effect:** decide whether one reduced scalar is sufficient.
- **Special resource:** the adjoint of `SU(3)` is the traceless matrix algebra and
  inherits two natural products.
- **Rejoin edge:** an exact `reduction-decision/v1` witness with a two-channel
  route, an `SU(2)` one-channel control, and a typed carrier refusal.

The horizon is one finite Peter--Weyl source/target block. Full synthesis on
`L^2(SU(3))`, unbounded-operator domains, and group-general invariant discovery
are not claimed here.

## Differential-operator setting

Let `G=SU(3)` act on `H=L^2(G)` by left translation, let `Delta_G` be a positive
bi-invariant Laplacian, and let `A` be the adjoint representation. For fixed
`v_0 in A` and `ell in A^*`, define

```text
f_ell(g)=ell(Ad_g v_0),
T_ell=M_(f_ell)(1+Delta_G).                              (1)
```

The Laplacian is invariant and `ell -> T_ell` is an order-two tensor operator of
type `A`. Peter--Weyl and Wigner--Eckart reduce its source `lambda` to target `mu`
channel to

```text
Hom_G(A tensor V_lambda,V_mu)
  tensor Hom(M_lambda,M_mu).                            (2)
```

On the adjoint source and target, the standard tensor-product theorem contract is

```text
8 tensor 8 = 1 + 8_S + 8_A + 10 + conjugate(10) + 27,
dim Hom_G(8 tensor 8,8)=2.                              (3)
```

Equation (3) supplies completeness only. It is not used as a table from which the
two intertwiners are copied.

## Construction from natural operations

Realize the complexified adjoint as `A=sl_3(C)`, with simultaneous conjugation.
The associative matrix product forces two traceless covariant bilinear maps:

```text
F(X,Y)=[X,Y],
D(X,Y)=XY+YX-(2/3)tr(XY)I.                              (4)
```

They are constructed in constant semantic depth: product, exchange, trace
removal. For `g in SU(3)`, associativity and cyclicity of trace give

```text
F(gXg^-1,gYg^-1)=gF(X,Y)g^-1,
D(gXg^-1,gYg^-1)=gD(X,Y)g^-1.                          (5)
```

Moreover, `F(Y,X)=-F(X,Y)` and `D(Y,X)=D(X,Y)`. Since both maps are nonzero,
their opposite exchange parities prove linear independence. Combined with (3),
this proves that `(F,D)` is a complete basis of the outer-multiplicity space. No
weight, root string, magnetic label, or component `f_abc,d_abc` table is needed.

Representation theory supplies the two allowed channels; the differential
operator supplies their reduced couplings. If `kappa` is the scalar action of the
invariant order-two factor on the chosen source block, write

```text
R_(a,b)(X,Y)=kappa[a F(X,Y)+b D(X,Y)].                  (6)
```

This separation prevents the false claim that `SU(3)` determines the dynamics.

## Use-level observable and route decision

For a traceless probe `Z`, retain the ordered pair

```text
A_forward = tr[Z R_(a,b)(X,Y)],
A_reverse = tr[Z R_(a,b)(Y,X)].                        (7)
```

Exchange is the analysis map:

```text
(A_forward-A_reverse)/2 = kappa a tr(ZF(X,Y)),
(A_forward+A_reverse)/2 = kappa b tr(ZD(X,Y)).         (8)
```

The exact fixture chooses

```text
X=E_12,  Y=E_23,  Z=E_31,
kappa=4, a=1/2, b=3/4.
```

Both natural products equal `E_13` on this preparation, and the trace pairing is
one. The executable result is therefore

```text
A_forward=5, A_reverse=1,
antisymmetric part=2, symmetric part=3.                (9)
```

A bracket-only route leaves residual `3`; a Jordan-only route leaves residual
`2`. Consequently the same observable cannot factor through one chosen octet
copy. The router selects `two-channel-outer-multiplicity`.

## Transfer control and refusal

The unchanged interface is applied to `SU(2)`. For traceless two-by-two matrices,
polarized Cayley--Hamilton gives

```text
XY+YX=tr(XY)I,
```

so the traceless Jordan channel vanishes identically. The control fixture returns
ordered amplitudes `(4,-4)` and selects `single-antisymmetric-channel`. Thus the
route change is constructed from the carrier algebra rather than supplied as an
expected multiplicity label.

A nontraceless preparation returns `CarrierViolation` before any transition
calculation. Dimensions beyond two and three return
`CompletenessContractOutsideHorizon`; the tool does not infer a complete
intertwiner basis from two natural operations for arbitrary groups.

## Complexity and human-computability certificate

For `SU(3)`, an uncompressed bilinear map on an eight-dimensional adjoint carrier
has `8^3=512` possible coefficients. The retained dynamics has two scalars. One
preparation uses two defining `3 by 3` matrix products and trace removal, with an
upper bound of 63 rational multiplications in the present accounting. This is
structural compression from the adjoint component carrier to the defining matrix
algebra; it is not a claim of runtime dominance over a precomputed sparse
Clebsch--Gordan table for a single query.

The human replay consists of four operations and two parity identities. The full
weight decomposition is retained only as a theorem contract proving completeness.

## Reproducible artifacts and verdict

- Constructor: `../computation/su_adjoint_multiplicity_router.py`
- `SU(3)` use fixture: `../computation/examples/su-adjoint-transition-su3.json`
- `SU(2)` transfer control: `../computation/examples/su-adjoint-transition-su2.json`
- Refusal: `../computation/examples/su-adjoint-transition-nontraceless.json`
- Public tests: `../computation/test_reduction_workbench.py`

The bounded F3 bridge is supported: outer multiplicity now changes a named
observable and route decision without component enumeration. The stronger
PDE realization now continues in the
[multiplicity-valued adjoint PDE bench](su-adjoint-multiplicity-pde.md). The scalar
operator (1) still requires a full product-coefficient Peter--Weyl projector and
remains parked at that boundary.
