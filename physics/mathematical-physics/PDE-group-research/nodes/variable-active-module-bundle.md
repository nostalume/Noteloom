# Variable active-module bundle

## Contract `C_G19_v1`

For an exact Gaussian-rational polynomial matrix PDE

```text
D=sum_alpha C_alpha(x) partial^alpha
```

on a rational box, the constructor receives polynomial preparation/effect, a
rational base point, the compact-supported smooth core without boundary trace,
and explicit closure, polynomial, rank, and output budgets. It receives no frame,
projector, reduced operator, separation coordinates, or group label.

## Construction

At the base point, exact breadth-first closure generates the smallest module from
the preparation under all `C_alpha(x_0)`. Its proof object records only `Seed` and
admitted `Apply(parent,coefficient)` nodes. Replaying this finite DAG over the
whole polynomials constructs `B(x)`; rejected dependent words never re-enter.

Exact elimination selects pivot rows and one constant normalization at the base
point. For `mu=det B_I`, bounded rational Horner intervals certify
`conjugate(mu)mu>0` on the first successful nested box. Exhaustion returns
`RankRegionUnresolved`, not a guessed rank jump.

For every derivative multi-index `beta`, the constructor forms

```text
K_beta=sum_(alpha>=beta) binom(alpha,beta)
       C_alpha partial^(alpha-beta) B,
G=B^dagger B,  A_B=G^-1 B^dagger,  P=B A_B,
D_B=sum_beta A_B K_beta partial^beta,
R_B=sum_beta (I-P) K_beta partial^beta.
```

All rational-function identities are checked after denominator clearing:
`D S_B=S_B D_B+R_B`, `A_B R_B=0`, projector idempotency, preparation recovery,
and effect pullback. Polynomial growth and serialization are budgeted and counted.

## Executable dispositions

- `exact`: every residual coefficient vanishes on the certified chart.
- `formal`: reconstruction is exact but leakage is nonzero and has no error bound.
- `obstructed`: exact closure was requested but coefficient/derivative escape is
  nonzero, or admission/core data are unsupported.
- `unresolved`: rank or exact polynomial/output budgets are exhausted.

The [coefficient-generated benchmark](../benchmarks/coefficient-generated-variable-module.md)
contains constant, non-Pauli variable, coefficient-escape, and rank-refinement
fixtures through the common workbench route.

## Boundary and next bridge

This node constructs a local PDE decomposition, not a group. Residual
factorization may next propose base vector fields; those candidates still require
coefficient-defect, bracket, integration, and domain-flow tests. Controlled
leakage, observable propagation, finite jets with remainders, boundary descent,
and global bundle gluing remain open.
