# Residual-derived infinitesimal lift

## Frozen question and alternatives

`E_G20_probe_1` asks whether G19's exact leakage constructs an infinitesimal PDE
symmetry without a supplied group or generator. Before calculation, the outcomes
were frozen as:

1. no first-order directional data;
2. one common projective direction which lifts through the whole operator;
3. one common direction whose full-operator lift fails; or
4. first-order tensor rank greater than one, where the single-direction contract
   must refuse.

The probe reuses the exact G19 polynomial witness and the contract in the
[G20 node](../nodes/residual-direction-lie-lift.md). It does not alter G19 after
seeing an outcome.

## Rank-one direction in the non-Pauli PDE

For the coefficient-generated frame

```text
B=[e_1,(0,x,y)^T],       D=-Delta I_3+H,       H=(1,x,y)^T(1,x,y),
rho^2=x^2+y^2,
```

G19 returns first-order residual numerators, flattened by ambient/active entry,

```text
        partial_x    partial_y
A_R = [[0,            0],
       [0,            0],
       [0,            0],
       [-2y^2,        2xy],
       [0,            0],
       [2xy,         -2x^2]],                 denominator=rho^2.             (1)
```

Every `2 x 2` minor vanishes and `x` is nonzero on the certified chart, so
`rank_K(A_R)=1`. Clearing polynomial content gives

```text
Lambda_R=span_K{(y,-x)},       L_v=y partial_x-x partial_y.                 (2)
```

This is the line of the angular derivation, with orientation deliberately not
chosen by a group convention.

Write a general real skew internal endomorphism as

```text
J(a,b,c)=[[0,-a,-b],[a,0,-c],[b,c,0]].                                     (3)
```

Coefficientwise expansion of
`[D,lambda L_v-J(a,b,c)]` gives a linear defect matrix of rank three with

```text
ker(Phi)=span{(-1,0,0,1)}       in coordinates (lambda,a,b,c).              (4)
```

Thus the visible representative is

```text
L=-y partial_x+x partial_y,
J=[[0,0,0],[0,0,-1],[0,1,0]],       [D,L-J]=0.                              (5)
```

No rotation label entered (1)--(4). It may be recognized as the local `so(2)`
action only after the operator identity is constructed. For the rectangular G19
region, its flow does not preserve the domain, so (5) is not promoted to a global
operator symmetry there.

## Same direction, failed operator lift

Add the scalar polynomial `xI_3` to the potential. The base-point provenance frame
changes to

```text
B'=[e_1,(x-1,x,y)^T],
```

but it has the same pointwise range and the first-order residual still has rank
one with the line (2). The full defect now contains

```text
lambda L_v(xI_3)=lambda y I_3.
```

Taking trace in the zeroth-order equation gives `3 lambda y=0`; an internal
commutator has zero trace. Hence every lift has `lambda=0`. Exact elimination in
the canonical real skew seed returns an empty kernel for this coefficient family.
This control rejects the false implication

```text
common residual direction => PDE symmetry.                                 (6)
```

## Rank-two and coefficient-only refusals

For the free vector Laplacian with the rank-one preparation

```text
D=-Delta I_3,       B=(1,x,y)^T,
```

the first-order residual has common denominator `1+x^2+y^2` and flattened
numerator

```text
A_R=[[2x,             2y],
     [-2(y^2+1),      2xy],
     [2xy,       -2(x^2+1)]].                                               (7)
```

The last two rows have determinant `4(1+x^2+y^2)`, so `rank_K(A_R)=2`.
`C_G20_v1` returns `ResidualNotLineGenerated`; choosing `partial_x` or `partial_y`
would be a coordinate-basis guess. The free PDE does have translation and rotation
symmetries, which makes (7) a strong boundary test: this route is a
preparation-relative direction constructor, not a complete symmetry classifier.

The G19 coefficient-escape fixture has only the nonzero zeroth-order residual

```text
R_0=[[0,0],[0,0],[0,x]].                                                    (8)
```

Its first-order flattening has rank zero, so the output is
`NoDirectionalLeakage`, not an invented vector field.

## Gauge check, cost, and reproduction

For the successful fixture, the variable reduced gauge

```text
U(x)=[[1,x],[0,1]]
```

sends each first-order coefficient to `R_i U`. Exact row reduction before and
after this transformation is identical. This checks that the constructed object
is the derivation line, not a preferred active-frame basis.

The public constructor performs one `(nr) x d` exact rank, one polynomial
primitive-content normalization, and one linear kernel in the canonical
`1+dim u(3)=10` real unknowns. It enumerates no
special functions, group catalogue, angular modes, or representation components.
No runtime or complete-route leverage claim is made.

From `computation/`:

```powershell
uv run python -m unittest check_residual_direction_lift.py
uv run python -m unittest test_polynomial_residual_lie.py test_polynomial_active_module_router.py
uv run python reduction_workbench.py discover examples/polynomial-lie-lift.json --summary
```

Under CPython 3.14 and SymPy 1.14, the independent five-check certificate and the
public contract suite pass. Four additive fixtures cover success,
same-line/no-lift, rank-two, and coefficient-only refusal; a bounded candidate
control exits unresolved. The four older G19 public outputs retain their canonical
SHA-256 digests after the shared coefficient-iterator refactor.

Final stage receipt: 232 unit tests and 25 independent check tests pass; Ruff,
format, compileall, and all 77 JSON examples pass. Nonblank LOC are 339 for the new
math owner, 118 for the shared polynomial owner, 237 for admission, 300 for the
router, 202 for the new tests, and the retained checker remains 149. The new owner
plus net production growth elsewhere is 500 lines, below the frozen 700-line cap.

## Evidence disposition

```text
id: E-G20-01
target: C_G20_v1 direction and lift distinctions
kind: deductive laws plus maintained exact computation
operation: filter residual order; flatten first-order coefficients; compute rank
           and primitive line; compile the full polynomial commutator kernel
result: rank-one/lift success; same-line/no-lift control; rank-two refusal;
        coefficient-only rank-zero refusal; variable-gauge invariance
permitted consequence: freeze the exact-polynomial local constructor contract
boundary: no multi-direction completeness, Lie closure, global integration,
          domain promotion, or leverage result
```

Disposition: **implemented support for the frozen local distinction**. The next
semantic question is closure of several independently visible lines modulo their
internal ambiguity, not another fitted one-line example.
