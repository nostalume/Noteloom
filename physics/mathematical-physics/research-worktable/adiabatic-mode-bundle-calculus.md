# Adiabatic mode-bundle calculus for variable-coefficient PDEs

## 1. Why this layer is needed

Constant coefficients can turn a differential operator into a fixed Lie algebra:
the Pauli--Landau bench has one curvature-selected spin splitting and one exact
Heisenberg ladder at every point.  With variable coefficients, the local mode
spaces themselves move.  A fixed global ladder generally ceases to exist.

The replacement is not a component expansion.  It is a finite semantic package:

```text
isolated spectral cluster
  -> spectral projector bundle
  -> intrinsic connection + off-diagonal transition arrow
  -> projected effective PDE + computable defect
  -> observable error bound or crossing obstruction.                 (1)
```

This is the approximate counterpart of exact representation decomposition.  Its
organizing resource is a spectral gap rather than a globally known group.

## 2. Admission data

Let `z` denote slow position or phase-space variables and let `h_0(z)` be a
self-adjoint family on a fixed fast Hilbert space `K`.  Assume a spectral cluster
`Sigma_*(z)` is separated from the rest of the spectrum by

```text
dist(Sigma_*(z), spec(h_0(z)) \ Sigma_*(z)) >= gamma > 0.             (2)
```

The cluster may have multiplicity `m`; no eigenvector or scalar band is chosen.
For a contour `Gamma` enclosing only this cluster, construct the Riesz projector

```text
P_0(z) = (1/(2 pi i)) integral_Gamma
           (lambda-h_0(z))^(-1) d lambda.                            (3)
```

The input must also specify:

- the full slow-fast operator or operator-valued symbol `H_epsilon`;
- its common domain and the phase-space/energy region under study;
- a regularity order for `P_0` and the symbol calculus being used;
- preparation and observable;
- the requested approximation order and time scale.

Small derivatives without (2) do not admit the branch.  A gap without derivative
control constructs a bundle but not a useful decoupling estimate.

## 3. The mode bundle and its intrinsic arrows

The ranges of (3) form the rank-`m` mode bundle

```text
E_* = Ran(P_0) -> Z.                                                  (4)
```

Its Grassmann connection and off-diagonal second fundamental form are

```text
nabla^(E_*) = P_0 d,
K       = (I-P_0) dP_0 P_0.                                         (5)
```

Equation (5) is the variable-coefficient version of the lowering/raising data.
`K` sends a retained mode toward discarded modes; `K^*` returns it.  In a local
orthonormal frame these become matrices of derivative couplings, but the
projector formula is the construction and does not enumerate components.

The connection curvature is

```text
F_* = P_0 (dP_0 wedge dP_0) P_0.                                    (6)
```

For `m>1`, (5)--(6) are non-Abelian.  On overlaps, local frames transform by
`U(m)` and the connection transforms with its inhomogeneous gauge term.  Holonomy
and (6), not the chosen matrices, are the invariant data.  A nontrivial bundle
may have no global eigenbasis even though the projector is globally smooth.

Differentiating the spectral equation shows why the gap matters.  The
off-diagonal part of `dP_0` is obtained by a reduced resolvent, or more generally
by the Sylvester inverse of `ad_(h_0)` on off-diagonal blocks.  Schematically,

```text
K = - (h_Q-h_*)^(-1) Q(dh_0)P_0,       Q=I-P_0,                     (7)
```

with (7) literal for a simple eigenvalue and interpreted blockwise for a cluster.
Thus its size is controlled by `||dh_0||/gamma`.  At `gamma=0`, this inverse is
undefined: the failure is structural, not a weakness of symbolic simplification.

## 4. Exact decomposition defect

For any candidate projector `P`, define

```text
Def(P) = ([H_epsilon,P], P^2-P).                                    (8)
```

The off-diagonal operator

```text
R_P = (I-P) H_epsilon P                                             (9)
```

is the first uncancelled mode-conversion arrow.  An exact invariant
decomposition has `R_P=0`.  An adiabatic decomposition retains (9), its norm on a
declared energy/momentum window, and the scale on which it controls the requested
observable.

The effective operator is intrinsically

```text
H_eff = P H_epsilon P : Gamma(E_*) -> Gamma(E_*).                    (10)
```

Only when `E_*` is trivialized should (10) be converted into a matrix or scalar
PDE.  Projected derivatives in (10) use (5), and virtual transitions through `K`
produce geometric scalar/matrix potentials.  This distinguishes genuine
decoupling from merely diagonalizing the coefficient matrix pointwise.

For a fixed orthogonal projector whose commutator is bounded on the declared
sector, Duhamel comparison with the block-diagonal operator gives the leakage
estimate

```text
||(I-P) exp(-itH_epsilon) P psi||
  <= |t| ||[H_epsilon,P]||_sector ||psi||.                           (11)
```

For unbounded operators, (11) is a theorem contract: domain invariance and an
energy-localized commutator bound must be supplied.  The residual is nevertheless
the correct observable-level quantity; no claim is inferred from a formal
`O(epsilon)` label alone.

## 5. Superadiabatic correction without component enumeration

Space-adiabatic perturbation theory suggests the following recursive constructor.
Seek

```text
P_epsilon^(N) = P_0 + epsilon P_1 + ... + epsilon^N P_N              (12)
```

such that, in the selected symbol calculus,

```text
(P_epsilon^(N))^2-P_epsilon^(N) = O(epsilon^(N+1)),
[H_epsilon,P_epsilon^(N)]        = O(epsilon^(N+1)).                 (13)
```

At each order:

1. the idempotency residual forces the diagonal part of the next correction;
2. the commutator residual forces its off-diagonal part;
3. the gap in (2) permits the Sylvester inverse of `ad_(h_0)` on that part;
4. the new residual is recomputed rather than presumed small.

This recursion manipulates projectors, commutators, resolvents, and symbol orders.
It never needs a list of local eigenvector components.  An intertwining unitary
may identify the corrected bundle with a reference bundle, but if topology
forbids a global trivialization the effective dynamics remains bundle-valued.

The all-orders existence and long-time estimates are imported as theorem
contracts from space-adiabatic perturbation theory; this worktable currently
implements only the semantic recursion and exact first residual.

## 6. Bilateral interpretation

### PDE to representation-like structure

Starting from `H_epsilon`, the spectral cluster constructs `P_0`, hence the mode
bundle, connection, holonomy, and transition arrows.  Their generated object is
usually a connection algebra or Lie algebroid over `Z`, not one fixed Lie algebra.
If `P_0` is constant and the arrows close with constant structure constants, this
specializes back to an ordinary dynamical Lie algebra and may integrate to a
group.

### Representation to PDE

Starting from a group representation carried by the fast fiber, an equivariant
family `h_0(z)` and a selected representation cluster construct (3)--(6).
Quantizing the slow variables and projecting gives (10), including the induced
connection and geometric potential.  Thus the forward direction does not merely
attach a special function: it constructs a bundle-valued differential operator.

The two directions meet at the projector calculus, not at a guessed group name.

## 7. Output and refusal types

The constructor returns one of:

```text
AdiabaticModeBundle(P, connection, curvature, H_eff, residual, validity),
CoupledCluster(P_enlarged, internal matrix PDE, residual, validity),
CrossingObstruction(location, closing_gap, required_enlargement),
RegularityObstruction(missing_derivatives_or_symbol_control),
AnalyticObstruction(domain_or_commutator_bound).
```

When bands cross but a larger cluster remains separated from the rest, the
machine enlarges the block and preserves its internal matrix dynamics.  It does
not force a scalar decomposition.  If no controlled cluster exists, global
decoupling is refused while local or microlocal propagation may remain available.

## 8. Human-computability gain

For rank `m`, the reusable data are one projector, one connection, one curvature,
one effective operator, and one defect.  This replaces:

- repeated local diagonalization in every coordinate chart;
- phase choices for every eigenvector;
- componentwise derivative-coupling tables;
- independent perturbation derivations for each mode;
- false global bases when the mode bundle is topologically nontrivial.

The remaining hard work is exposed honestly: compute or bound a resolvent, a gap,
projector derivatives, and the residual on the observable's sector.  The
compression is semantic, not merely faster matrix arithmetic.
