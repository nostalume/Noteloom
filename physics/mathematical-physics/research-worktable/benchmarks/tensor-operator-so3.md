# `SO(3)` tensor-operator regression bench

## Purpose

This bench tests the group-typed operator calculus on a non-invariant differential
operator.  It is deliberately familiar so that selection rules and extra zeros
are easy to audit.  The general construction lives in
[`operator-decomposition-calculus.md`](../operator-decomposition-calculus.md).

## Input

Let `G=SO(3)` act on scalar functions on the unit sphere and use the positive
Laplacian convention

```text
Delta Y_(ell,m) = ell(ell+1) Y_(ell,m).
```

Let `x_q`, `q=-1,0,1`, be the spherical components of the position vector and
define a rank-one family of second-order differential operators

```text
T_q = M_(x_q) (1 + Delta).                              (1)
```

Multiplication is applied after `1+Delta`.  The common core is `C^infinity(S^2)`.
The observable for this bench is transition support between Laplacian eigenspaces,
not individual magnetic matrix elements.

## Construction certificate

The Laplacian commutes with rotations, while the span of the three functions
`x_q` is the vector representation `V_1`.  Hence

```text
U(g) T_q U(g)^(-1) = sum_(q') (V_1(g))_(q',q) T_(q'),   (2)
```

so (1) is a type-`1` tensor differential operator of order two.  Its principal
symbol is `x_q` times the metric inverse, again of type `1`; its lower symbol
layers are obtained without expanding in spherical coordinates.

The scalar carrier is multiplicity-free:

```text
L^2(S^2) = direct-sum_(ell>=0) V_ell.
```

The group-only fusion rule

```text
V_1 tensor V_ell = V_(ell-1) + V_ell + V_(ell+1)        (3)
```

permits edges `ell -> ell-1,ell,ell+1`, with the negative label omitted.
Wigner--Eckart reduces the whole family on each permitted edge to one group
intertwiner and one scalar reduced coefficient.

## Extra geometric zero

The middle edge allowed by (3) vanishes.  Under the antipodal map, `x_q` is odd
and a degree-`ell` spherical harmonic has parity `(-1)^ell`.  Therefore
`x_q Y_ell` has parity `(-1)^(ell+1)`, whereas `V_ell` has parity `(-1)^ell`.
Consequently

```text
T_q : V_ell -> V_(ell-1) + V_(ell+1).                  (4)
```

This distinction is essential: fusion constructs possible channels; the reduced
operator and auxiliary geometry decide which permitted channels are actually
nonzero.

The invariant factor contributes only

```text
(1+Delta)|_(V_ell) = (1 + ell(ell+1)) I,
```

so it rescales the two reduced edges but creates no new ones.

## Generated graph

```text
V_0 <-> V_1 <-> V_2 <-> V_3 <-> ...
```

Each adjacent arrow represents the type-`1` family, and all magnetic dependence
is stored in the standard `SO(3)` intertwiner.  A perturbation

```text
H = Delta + sum_q v_q T_q
```

is block tridiagonal in `ell` before any basis inside `V_ell` is chosen.  The
direction `v` can reduce the residual symmetry further, but it does not change the
operator-family certificate (2).

## What is and is not proved

Passed by this bench:

- a non-invariant differential operator is decomposed by its group type;
- its differential order and principal symbol are retained;
- group fusion predicts sparse sector support;
- parity supplies a certified zero beyond the group-only rule;
- no component-wise spherical-harmonic matrix is enumerated.

Not proved:

- that an arbitrary smooth perturbation has finite `SO(3)` bandwidth;
- that the resulting spectral problem has a closed form;
- that block tridiagonality alone reduces total runtime;
- that the selection graph reconstructs `SO(3)` uniquely.

## Transfer criterion

The general calculus passes beyond this regression only when the same sequence

```text
symbol layer -> operator type -> fusion edge -> reduced block -> observable
```

works for a nontrivial homogeneous bundle or a compact group with tensor-product
multiplicity, without introducing magnetic indices or a coordinate ansatz.
