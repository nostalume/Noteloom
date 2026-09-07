# Graded return and functional port

Status: coupling valuation generates an exact rank-30 multi-frequency return and
a genuine scalar functional port; the raw closed-path evaluator is semantically
valid but computationally rejected

Consumes: node 43's coefficient-valued endpoint functional and rank-changing
Hankel obstruction, plus node 13's action grammar.

Produces: a graded reduced action `(J_0,J_1,b)`, a scalar restriction port, and the
matrix-exposure obstruction consumed by [node 49](49-native-car-return.md).

## Construct grade instead of regularizing rank

Let

```text
L_0(A)=AH_0-H_0A,
L_1(A)=AV-VA,
Close_0(S)=span{L_0^k(A):A in S,k>=0}.                  (47.1)
```

Starting from the observable `d`, construct

```text
F_0=Close_0({d}),
F_s=Close_0(F_(s-1) union L_1(F_(s-1))), 1<=s<=4.       (47.2)
```

The valuation of a direction is the least grade containing it. This directly
computes

```text
L_0(F_s) subset F_s,
L_1(F_s) subset F_(s+1),                                (47.3)
```

without forcing positive-grade directions into the singular grade-zero metric.
Free spectral projectors realize `Close_0` because

```text
L_0 Pi_omega=omega Pi_omega,
Close_0(S)=direct-sum_omega span(Pi_omega S).            (47.4)
```

Only vectors sharing one free gap require rank reduction.

For an orthonormal serialization `Q` of `F_4`, construct

```text
J_0=Q^dagger L_0Q,   J_1=Q^dagger L_1Q,
b=Q^dagger d,        ell_s=Q^dagger D_s.                (47.5)
```

The returned multi-frequency operation is

```text
(z-J_0)y_0=b,
(z-J_0)y_s=J_1y_(s-1).                                  (47.6)
```

Equations (47.3) imply `Qy_s=X_s` grade by grade; node 43's scalar convolution and
partition division then recover the Green coefficients.

## Remove endpoint matrices from the interface

The state side needs only `ell_(s,j)=Omega_s(q_j)`. Trace cyclicity constructs

```text
Tr[(W_s d+d W_s)^dagger A]
 =Tr[W_s(A d^dagger+d^dagger A)]
 =Phi_s(A).                                              (47.7)
```

Therefore the evaluator port is

```text
Port({q_j}) -> (Z_s,Phi_s(q_j)), 0<=s<=4,               (47.8)
```

not `W_s`, a density matrix, or transition coordinates. An independent evaluator
may insert the ordered expansion of `W_s` into (47.7), contract each closed path,
and return only these scalars.

## Evidence and cost

- `E47-graded-return-v1`: filtration ranks are `(2,6,12,22,30)` with newly admitted
  counts `(2,4,6,10,8)`. Free closure residual is zero and interaction closure
  residual is `3.40e-16`. The reduced recurrence matches three frequency families
  within `8.46e-16`.
- The rank-30 packet retains 1,985 complex scalars instead of 41,025. Construction
  costs `7,794,688`; full/reduced query costs are `147,456/35,550`, giving a
  70-query break-even. Single/few-query leverage is rejected.
- `E48-functional-port-v1`: an ordered closed-path evaluator returns (47.8) with no
  endpoint matrices and reproduces the same Green families within `1.11e-12`, well
  inside its `1.03e-5` paired-quadrature estimate.
- That evaluator visits 3,582 path cells and performs 111,042 contractions; its
  local runtime was `75.3 s` versus about `0.045 s` for endpoint construction.
  Evaluator transfer is supported, but its computational leverage is rejected.

## Disposition and edge

The graded module is a reusable semantic and conditionally amortized computation.
The scalar port is a genuine producer-independent interface, but an interface does
not compress its evaluator. The surviving obstruction is representational: the
30 generated `q_j` remain opaque matrices, whereas a determinant or cumulant route
needs local factors and normal-ordered CAR words. Node 49 constructs that exposure
without changing (47.6)--(47.8). The domain remains the finite order-four Anderson
response at off-axis queries; graph/QFT transfer and continuum leverage remain
unresolved.
