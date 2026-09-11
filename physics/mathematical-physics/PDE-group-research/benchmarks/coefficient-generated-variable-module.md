# Coefficient-generated variable module

## Frozen question

`E_G19_probe_2` tests the first constructor-level transfer in the
[G19 inquiry](../research-graph.md#resolved-bridge-ledger-g19-variable-active-module-bundle):
can G18 basis provenance, rather than a supplied frame or projector, generate a
constant-rank variable module and expose the precise failure of full PDE closure?

The outcomes were frozen as: a constant module, a variable module with reported
connection/leakage, or refusal at a rank/domain obstruction. The input contains no
group label, separation coordinates, projector, eigenvector, or expected reduced
operator.

## Polynomial coupled-channel input

On

```text
Omega=(1/2,3/2) x (-1,1),       x_0=(1,0),
v=(1,x,y)^T,                    H(x,y)=v v^T,
D=-Delta I_3+H(x,y),            psi=e_1,       Q=psi psi^dagger,              (1)
```

use polynomial coefficient jets through order two and the common core
`C_c^infinity(Omega;C^3)`. This is a two-dimensional, three-channel matrix
Schrodinger PDE, not a Pauli specialization.

## Provenance lift and rank certificate

At `x_0`, G18 closure admits only the expression nodes `psi` and `H psi`:

```text
H_0 psi=(1,1,0)^T,       H_0(H_0 psi)=2 H_0 psi.                            (2)
```

Continue those two expressions as polynomials, without emitting another
coefficient word. One constant column operation gives

```text
B_raw=[psi,H psi],       B=B_raw [[1,-1],[0,1]]=[e_1,q],
q=(0,x,y)^T.                                                               (3)
```

Writing `rho^2=x^2+y^2`,

```text
G=B^dagger B=diag(1,rho^2),       det G=rho^2 >= 1/4 on closure(Omega).       (4)
```

Thus (3) is a certified rank-two frame on the admitted region. At the origin its
rank falls to one, so continuation to a region containing the origin is refused
unless the base is stratified. By contrast, the constant matrices obtained by
expanding the polynomial `H` generate `e_1,e_2,e_3` from `psi`; the G18 common
constant module is ambient. The variable construction therefore retains a local
rank-two object that constant coefficient-family closure cannot retain.

## Exact differential witness

The analysis, projector, and potential action are

```text
A_B=G^(-1)B^dagger
   =[[1,0,0],[0,x/rho^2,y/rho^2]],       P=B A_B,

H B=B A_H,       A_H=[[1,rho^2],[1,rho^2]].                                (5)
```

Since `B_x=[0,e_2]`, `B_y=[0,e_3]`, and `Delta B=0`, the induced connection is

```text
Gamma_x=A_B B_x=diag(0,x/rho^2),
Gamma_y=A_B B_y=diag(0,y/rho^2).                                            (6)
```

For reduced amplitudes `f=(f_1,f_2)^T`, the exact witness shell returns

```text
D_B=A_B D S_B
   =-Delta I_2-2 Gamma_x partial_x-2 Gamma_y partial_y+A_H,

R_B f=(I-P)D(Bf)
     =-2 t/rho^2 (-y partial_x+x partial_y) f_2,
t=(0,-y,x)^T,                                                               (7)

D S_B=S_B D_B+R_B,       A_B R_B=0.                                        (8)
```

The kinetic part of `D_B` also has the compact metric form
`-G^(-1) div(G grad f)`. Its in-bundle curvature is zero, but `R_B` is generally
nonzero. Flat connection is therefore insufficient for differential-operator
invariance: the extrinsic frame motion remains visible.

## Residual-to-generator construction

Factoring the two first-order leakage coefficients in (7), rather than guessing a
group, constructs the base vector field

```text
L=-y partial_x+x partial_y.                                                  (9)
```

Solving the resulting constant skew coefficient-covariance defect gives

```text
J=[[0,0,0],[0,0,-1],[0,1,0]],       L(H)=[J,H],       L(B)=J B.              (10)
```

Because the Laplacian commutes with `L`, the combined infinitesimal action
`K=L-J` satisfies `[D,K]=0` as a differential expression. This is a bounded
PDE-to-Lie construction: the leakage determines the orbit direction, and the
coefficient defect then determines its represented internal action. On a
rotation-invariant annulus, `K` integrates to the diagonal `SO(2)` action. The
rectangular `Omega` in (1) is not preserved by that flow, so a global domain
symmetry is explicitly refused here.

Equation (7) also gives the two obstruction-driven repairs without changing the
constructor: restrict to `L f_2=0`, which closes the rank-two differential
expression, or adjoin the missing tangential column `t`, which regrows the carrier
to dimension three.

## Observable, cost, and boundary

The preparation and effect descend algebraically:

```text
alpha=A_B psi=(1,0)^T,       F=B^dagger Q B=diag(1,0),
(Bf)^dagger Q(Bf)=f^dagger Ff.                                               (11)
```

For a compactly supported scalar envelope, synthesis preserves the stated common
core. But (11) is not an exact evolution reduction for unrestricted amplitudes,
because (7) drives the state off the module. No runtime or complete-route gain is
claimed until that leakage is eliminated, bounded, or propagated and the same
observable is recovered.

The human construction retains two provenance expressions, one Gram determinant,
one product-rule witness, and one residual factorization. It does not enumerate
polynomial monomials, angular modes, or representation components. This is a
semantic compression result, not yet a scaling result.

## Frozen-interface regression and adversarial controls

`E_G19_probe_3` tests the subsequently frozen `C_G19_v1` contract without adding
rules from this successful transfer.

**Constant regression.** If all coefficient fields and the preparation are
constant, every positive-order provenance jet vanishes. In the multi-index
product rule, only the term `alpha=beta` remains, so

```text
K_beta=C_beta B,       D_B=sum_beta A_B C_beta B partial^beta,       R_B=0,  (12)
```

whenever G18 closure certifies `C_beta B` lies in `range(B)`. The selected pivot
minor is constant. Thus the same interface recovers the G18 constant
differential-operator lift exactly; no separate constant-frame rule is required.

**Finite-jet rank no-go.** Fix any derivative order `m`, nonzero rational
`epsilon`, preparation `e_1`, and

```text
b_0(x)=1,                    b_epsilon(x)=1-(x/epsilon)^(m+1),
H_b(x)=[[0,b(x)],[b(x),0]].                                               (13)
```

The two matrix fields have identical `m`-jets at zero. Base-point closure admits
the same expressions `e_1,H_b e_1`, but their continued frame determinants are
respectively `1` and `b_epsilon`; the latter vanishes at `x=epsilon`. Therefore
no operation receiving only the finite jet can certify constant rank on a
neighborhood containing `epsilon`. Whole bounded-degree polynomial data or a
verified remainder enclosure is logically necessary.

**Coefficient escape.** Take

```text
H(x)=[[0,1,0],[1,0,x],[0,x,0]],       psi=e_1,       x_0=0.                (14)
```

Base-point closure admits `B=[e_1,H psi]=[e_1,e_2]`, which continues as a constant
rank-two frame. Nevertheless

```text
A_B H B=[[0,1],[1,0]],
(I-P)H B=[[0,0],[0,0],[0,x]].                                             (15)
```

The unchanged contract reports (15) as exact zero-order leakage. It does not add
the rejected word `H^2 psi` away from the base point. This prevents adaptive word
enumeration from being hidden inside “continuation.”

## Reproduction and disposition

The identities (3)--(11) were independently checked coefficient-by-coefficient
under CPython 3.14.6 and SymPy 1.14.0, invoked transiently through the existing
`uv` workbench. Base revision:
`c9b2717f3cd2d5a715f8d537f7adf5b2011817ae`. Checker SHA-256:
`581CE36A0E1FDE36D6702BFE1D1E884B3C2C13D809E7DE421E9CAFCBAA911398`;
canonical result SHA-256:
`a03dbfbfcfcced4d2ba0db6cad035fdb6ae5ca5aba43ad217466eaba7af52763`.
The exact calculation is retained here; scratch source and raw output are not a
second computation project or a production G19 route.

Equations (12)--(15) were separately replayed in the same environment at base
revision `ae1208f11dfd3255544d7528d2afd5a6df9d77ed`. Control-checker SHA-256:
`877B29EBD5687BF188FA83F1E8603D645929D98028519AB07E895A8E97A76B5C`;
canonical control-result SHA-256:
`e22c37adfbd2b75965ea6e1ada69d0c0d4d919c7fbcfa39a9b08b6893a7934c6`.
The run instantiated (13) at `m=2, epsilon=1/4`; the displayed arbitrary-`m`
identity is the exact polynomial argument, not an extrapolation from that run.

Disposition: **exact bounded support for the frozen polynomial provenance
calculus** at the deduction, constant-regression, one non-Pauli transfer, and
adversarial-refusal levels. It exactly rejects the implications “coefficient
invariance implies PDE invariance,” “flat connection implies no leakage,” “local
Lie covariance implies domain symmetry,” and “a finite jet certifies a
neighborhood.” The maintained route described below now establishes the bounded
local executable slice, but not complete rank certification on a prescribed large
region, controlled leakage, global integration, or computational leverage.

## Executable vertical slice

The public `polynomial-active-module/v1` route now replays this contract from
sparse exact input. The maintained fixtures are:

```powershell
uv run python reduction_workbench.py discover examples/polynomial-active-constant.json --summary
uv run python reduction_workbench.py discover examples/polynomial-active-variable.json --summary
uv run python reduction_workbench.py discover examples/polynomial-active-escape.json --summary
uv run python reduction_workbench.py discover examples/polynomial-active-rank-unresolved.json --summary
```

They return `exact`, `formal`, `obstructed/CoefficientOrDerivativeEscape`, and
`unresolved/RankRegionUnresolved`, respectively. The variable fixture constructs
the two provenance nodes `psi,H psi`, the normalized frame (3), a certified
rational subbox, and every coefficient of (7)-(8). The constructor retains the
nonzero residual rather than adding a third word. Exact Horner interval failure is
reported with attempted boxes; it is not promoted to a rank-jump assertion.

This upgrades the disposition to an **executable bounded local construction**.
It still makes no controlled-error, observable-propagation, boundary-descent,
residual-factorization, Lie-closure, or global-group claim.
