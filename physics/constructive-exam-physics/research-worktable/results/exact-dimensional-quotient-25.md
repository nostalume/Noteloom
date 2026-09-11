# Result 25: exact dimensional-quotient constructor

## Tension

The semantic layer already retained dimensions, but used them only to reject an
invalid return. The proposed area unification requires a generative reduction:
remove arbitrary base-unit scale while preserving physical comparisons. Merely
naming Buckingham groups would supply a formalism, not an internally constructed
operation.

## Obstruction and construction `C-dim-v1`

For quantities `x_1,...,x_n`, place their mass, length, time, and current exponent
vectors in the columns of an exact integer matrix `D`. A monomial

```text
Pi(a) = product_i x_i^a_i
```

changes under a base-unit rescaling by the dimension vector `D a`. It is invariant
exactly when

```text
D a=0.
```

Thus unit-rescaling failure constructs the reduction space `kernel(D)`. The
executable operation computes an exact rational nullspace, clears denominators,
divides the integer gcd, and fixes the first nonzero exponent positive. The result
is a deterministic ordered set of primitive integer representatives. Certificates
check rank-nullity, zero dimension, and primitive scaling.

The constructor returns `irreducible` when nullity is zero. If nullity exceeds the
declared group budget, it returns `group_budget_exceeded` without presenting a
partial basis as complete. Duplicate symbols, missing semantic names, and invalid
quantity types are rejected before computation.

## Frozen distinguishing bench

| Packet | Constructed group | Downstream meaning |
| --- | --- | --- |
| pendulum `T,L,g` | `T^2 g/L` | the supplied small-angle law returns `4 pi^2` |
| fluid `rho,v,L,mu` | `rho v L/mu` | Reynolds regime coordinate |
| circuit `t,R,C` | `t/(RC)` | the supplied one-time-constant state returns `1` |
| independent `m,L` | none | dimensionally irreducible |

All three successful packets use the same constructor. The first supplies
regression plus downstream consumption; fluid and circuit are structurally
different transfers. A separate three-dimensionless-input fixture verifies that a
two-group budget refuses the full three-dimensional nullspace.

## Disposition

`C-dim-v1` is **supported-bounded as an exact reduction constructor** over the
current four-base `Dimension` type. It generates dimensionless coordinates without
hard-coding the expected groups and returns inspectable certificates and
refusals.

It does not generate a pendulum equation, a drag law, an RC response, numerical
constants, or empirical regime thresholds. A nullspace basis is nonunique; input
order fixes one deterministic basis but not the cognitively cheapest basis.
Temperature, amount, luminous intensity, affine units, uncertainty, non-rational
scaling weights, and automated extraction from prose are outside the contract.
No learner data establish that this candidate card saves exam time.

The next internal discriminator on this branch is whether target-aware basis
selection can reduce complete handwritten work without encoding the desired group.
The next independent reduction family remains network condensation by boundary
observable, not another dimensional example.
