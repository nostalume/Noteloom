# Orbit-space reduction calculus for PDEs

## 1. The principle as a typed construction

Orbit reduction applies only after a joint symmetry of the realized PDE has been
constructed. Its input is

```text
OrbitReductionProblem = (
  manifold M and bundle E -> M,
  differential realization D with domain and boundary B,
  preparation/source P and observable O,
  bounded infinitesimal-automorphism grammar,
  analytic and computational resource bounds
).                                                               (1)
```

The output is not “new coordinates.” It is

```text
OrbitReduction = (
  effective action G on (M,E,Dom D),
  orbit-type quotient Q=M/G,
  representation labels pi and multiplicity bundles M_pi -> Q,
  reduced differential operators D_pi on Q,
  analysis A_pi and synthesis S_pi,
  descended boundary/interface conditions B_pi,
  sector-selection certificate,
  residuals, observable recovery, and cost verdict
).                                                               (2)
```

Coordinates may trivialize (2), but they do not define it.

## 2. Bilateral entry: construct the action from the PDE

Begin with the stabilizer descent

```text
Aut(principal symbol)
  contains Aut(full coefficient layers)
  contains Aut(D,Omega,B,Dom D,P,O).                               (3)
```

For a candidate infinitesimal bundle automorphism `X`, compute

```text
R_int(X)=[D,X],
R_boundary(X)=(B Gamma_r X)|ker(B Gamma_r),
R_obs(X)=O X - X_O O.                                             (4)
```

Only candidates satisfying the residual policy act on the requested problem.
Close their brackets, determine kernels and ineffective directions, and integrate
only when the required domain/globality conditions hold. Thus `G` is an output of
the joint stabilizer, not a group guessed from the shape of one formula.

This branch finds geometric first-order symmetry. A higher-order commutant such as
Runge--Lenz need not act by orbits on `M`; it belongs to the separate operator-
module branch.

## 3. Quotient geometry is generally stratified

For `x in M`, let `G_x` be its isotropy subgroup. Points with conjugate isotropy
form an orbit-type stratum. The quotient is therefore

```text
Q=M/G = union_[H] M_[H]/G,                                      (5)
```

not necessarily a smooth manifold. On the principal stratum,

```text
q=dim Q=dim M-dim(G.x).                                         (6)
```

Exceptional or fixed orbits become quotient boundaries, corners, or singular
strata. Regularity there is part of the reduced domain. For axial rotation, an
axis-containing domain has fixed points and requires a weight-dependent axis
condition; an annulus avoids that obligation but cannot certify it.

## 4. Representation decomposition along the orbits

For a compact action, analyze a section along each orbit into irreducibles. On a
principal orbit `G/H`, the remaining fiber for type `pi` is

```text
M_pi(q)=Hom_H(V_pi,E_q).                                        (7)
```

The scalar free-action case reduces (7) to character or representation
multiplicity. Spinors, tensors, gauge fields, and nontrivial isotropy make it a
finite vector bundle over `Q`; its connection and holonomy cannot be discarded.

The analysis/synthesis maps have the schematic form

```text
A: Gamma(E) -> direct-sum/integral_pi Gamma(M_pi),
S: direct-sum/integral_pi Gamma(M_pi) -> Gamma(E).               (8)
```

An equivariant operator descends when

```text
A_pi D = D_pi A_pi,
D S_pi = S_pi D_pi.                                             (9)
```

Equation (9), together with visible-state recovery, is the semantic witness that
the sector PDEs are the same problem rather than a heuristic separation.

## 5. Differential order and quotient dimension

Orbit reduction removes orbit variables but normally preserves differential order
on the quotient. An order-two PDE on an `n`-manifold with generic `d`-dimensional
orbits becomes a family of order-two PDEs on a `q=n-d` dimensional quotient:

```text
D -> {D_pi on Q},       q=n-d.                                  (10)
```

Only `q=1` produces ODEs. A transitive action has `q=0` and yields finite algebra;
an axial action in three dimensions has `q=2` and leaves 2D PDEs. This is why
orbit reduction is more general than Cartesian or radial separation.

## 6. Boundary descent

An invariant physical boundary decomposes into orbit types. The analysis map must
carry its trace kernel to sector trace kernels:

```text
A_pi ker(B Gamma_r) = ker(B_pi Gamma_r^Q),                       (11)
```

and the reduced Green boundary form must agree with the restriction of the full
one. If the group moves the boundary, mixes prescribed and free trace components,
or fails at a corner/interface, (11) is obstructed even if the interior commutator
vanishes.

On singular quotient strata, regularity can act like an additional boundary
condition. It must be generated from isotropy and finite-energy behavior, not
copied from a scalar radial table.

## 7. Sector selection is capability-dependent

There is no single correct set of sectors. The selection rule comes from the
requested capability:

1. **Source/preparation support:** for `D u=f`, equivariance preserves the
   representation support of `f`; only those sectors are needed for `u`.
2. **Spectral window:** generate irreducibles until a coercive lower bound such as
   `lambda_min(pi)>=a C_2(pi)+b` excludes every unseen type below the window.
3. **Observable visibility:** quotient sectors annihilated by both preparation and
   observable, using a cyclic/selection-graph certificate.
4. **Full resolvent or propagator:** generally requires every sector or a controlled
   tail estimate; finite source support cannot justify truncating this object.

These policies prevent representation theory from turning into a new exhaustive
enumeration.

## 8. Whole-route complexity

Let `h` be quotient mesh scale, `F` the selected sector set, and `b_pi` the finite
real/multiplicity fiber size. The spatial carrier scales schematically as

```text
N_full(h)=Theta(h^(-n)),
N_red(h)=sum_(pi in F) b_pi Theta(h^(-q)).                        (12)
```

This is only the carrier law. A valid cost comparison also includes

```text
stabilizer discovery + orbit stratification + representation analysis
+ reduced assembly/solution + synthesis/observable recovery + certification.   (13)
```

If a complete field is requested, synthesis itself costs at least the number of
output samples. If only a sector coefficient or invariant observable is requested,
that recovery cost can disappear. Sparse fill, iterations, conditioning, sector
count, and error constants decide whether (12) becomes a runtime gain.

## 9. Human computability

The human-facing output is a small grammar:

```text
one generated action,
orbit invariants describing Q,
one parameterized operator template D_pi,
one boundary/stratum rule,
one sector-selection certificate,
one synthesis formula.                                         (14)
```

It replaces separate coordinate derivations and component tables. A long list of
irreducibles, special polynomials, or sampled field values is machine evidence,
not the human calculus.

## 10. First quotient-PDE execution and boundary

The [axial nonseparable benchmark](benchmarks/axial-nonseparable-quotient-pde.md)
executes (1)--(14) in a bounded scalar grammar. It discovers the surviving axial
rotation, turns one 3D elliptic problem into three source-visible 2D PDEs, proves
discrete analysis/synthesis equality, and compares continuum error and whole-route
cost with the full sparse solve.

The [warped-axis benchmark](benchmarks/warped-axis-stratified-quotient-pde.md)
now pays the first two debts. The fixed axis becomes a singular quotient boundary;
isotropy generates `partial_r u_0=0` and `u_m=O(r^|m|)`, while the warped physical
wall descends independently. A uniform axis policy is refused, and the accepted
sector solutions synthesize the full warped-domain discretization.

Bundle-valued fields and spectral-window tails remain open. For spinors or tensors,
the axis rule must be computed from `Hom_H(V_pi,E_x)` rather than copied from the
scalar condition; this is now the strongest re-entry condition.
