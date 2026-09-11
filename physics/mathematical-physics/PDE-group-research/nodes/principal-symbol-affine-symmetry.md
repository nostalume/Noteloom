# Principal-symbol affine symmetry compiler

## Missing bridge

G20 constructs one direction from a preparation-relative leakage residual, while
G21 closes several already known lift pairs. Neither operation supplies all seeds
from the PDE itself. For a common second-order class, the principal symbol removes
that privilege before any group name or vector-field ansatz is introduced.

### Frozen exploratory contract `C_G22_v0`

Input is an exact polynomial matrix differential operator on a common
compact-supported smooth core whose second-order part has the form

```text
D_2=-G^(ij) partial_i partial_j I_n,
```

where `G` is constant, real, rational, symmetric, and nondegenerate. Candidate
generators are restricted to first-order base actions with affine real vector
fields and constant internal `u(n)` lifts. A candidate, residual-coordinate, and
bracket-check budget is mandatory.

Output is the exact kernel algebra, its zero-base internal ideal, visible quotient
and structure table, or a typed refusal distinguishing variable, nonscalar,
degenerate, higher-order, nonrational, and resource-bounded cases. A refusal means
this constructor is inapplicable; it does not mean the PDE has no symmetry.

## Internal construction

The order-two part of `[D,L_v-J]=0` is the flat Killing equation

```text
partial_i v_j+partial_j v_i=0.                              (1)
```

Differentiating cyclic permutations of (1) shows every second derivative of `v`
vanishes. Thus the complete base candidate space in this contract is

```text
v(x)=a+A x,                 A^T G^(-1)+G^(-1) A=0.           (2)
```

It is constructed without solving a polynomial ansatz:

```text
translations:  a=e_i,
linear fields: A=G S_ab,   S_ab^T=-S_ab.                    (3)
```

Equations (2)--(3) give `d(d+1)/2` base candidates. Adding the canonical real
basis of `u(n)` produces one finite intrinsic candidate algebra of dimension

```text
N=d(d+1)/2+n^2.                                             (4)
```

Lower-order terms do not generate new candidates. They filter this space through
the universal defect map

```text
Psi_D : iso(G) direct-sum u(n) -> Diff_<=2(C^n),
Psi_D(v,J)=[D,L_v-J].                                      (5)
```

The exact kernel of (5) is closed under
`[(v,J),(w,H)]=([v,w],-[J,H])` by Jacobi. The common defect compiler certifies
kernel closure, the zero-base ideal, and the quotient bracket table. Polynomial
coefficient coordinates are only the execution substrate for (5); they are not
the conceptual search space.

## Bilateral meaning

This is a direct PDE-to-representation-algebra construction:

```text
principal symbol -> affine isometry candidate algebra
full coefficients -> represented symmetry subalgebra -> visible quotient.
```

The reverse direction already exists in the worktable: a represented algebra and
carrier action are realized as differential operators and then checked against
the same full-operator witness. The two directions are not assumed inverse. On
the public polynomial fixture, the principal-symbol route and the independent
preparation-residual route select the same one-dimensional visible direction.

## Complexity and human computability

The construction replaces arbitrary polynomial-vector-field enumeration and
open-ended bracket growth by `N` generated candidates and one exact kernel. A
human can read (3), the surviving kernel combinations, and the quotient table
without inspecting monomial components. Execution still pays for lowering the
full commutator to `R` residual coordinates and for exact elimination; the generic
closure certificate currently has a cubic-in-`N` check bound. Polynomial swell,
`n^2` internal growth, and observable recovery are not removed.

## Boundary and disposition

The exact probe supports `C_G22_v0` for constant nondegenerate scalar symbols,
including a non-diagonal metric, and transfers across free scalar, anisotropic
scalar, and coupled radial matrix operators. It also agrees with G20 on the same
operator and refuses a degenerate symbol.

Disposition: **promote the bounded principal-symbol constructor and its refusal
boundary as an exact exploratory bridge**. It does not yet own a public schema.
Variable or matrix-valued symbols require a finite-type symbol-stabilizer or
prolongation certificate; variable internal lifts require a connection-aware
candidate module. Domain preservation, integration, group uniqueness, spectral
decomposition, and same-observable cost remain later gates.
