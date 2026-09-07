# Filtered centralizer calculus: PDE to hidden operator algebra

## 1. Why this replaces blind symmetry search

The inverse problem is not initially “which group acts?”  Given a differential
operator `D`, the first intrinsic object is its represented centralizer or
normalizer:

```text
C(D) = {Q : [D,Q]=0},
N(D) = {Q : [D,Q] lies in the declared equation ideal}.
```

These objects exist before a group name, coordinate separation, or polynomial
basis is chosen.  Their finite presentations, cyclic modules, and obstruction
classes are the possible computational output.  A Lie group is considered only
after a finite Lie subalgebra has been constructed and analytically integrated.

The capability sought here is narrower than a universal symmetry solver:

> construct nontrivial commuting or intertwining operators by solving invariant
> symbol equations and a finite order-lowering lift, while reporting the first
> obstruction and the exact completeness horizon.

## 2. Filtration and the first necessary equation

Let `D` have order `r` and scalar principal symbol `p=sigma_r(D)`.  Filter
differential operators by order, `F_m Diff(E)`.  If `Q` has order `m`, then

```text
sigma_(r+m-1)([D,Q]) = (hbar/i) {p,q},                (1)
q = sigma_m(Q),
```

up to the stated quantization convention.  Hence a commuting lift must start in
the Poisson centralizer

```text
Z_p^m = ker(delta_p : S^m(TM) -> S^(m+r-1)(TM)),
delta_p(q) = {p,q}.                                   (2)
```

For bundle-valued symbols, (1) also contains the leading fiber commutator.  The
scalar formula must not be reused silently for spinors or systems.

Equation (2) is a geometric determining equation, not an enumeration of all
coordinate differential expressions.  Killing vectors/tensors, moment maps,
Clifford symbols, and separation tensors are different structured solution
classes of this one symbol-level problem.  Eastwood's Laplacian result is an
important complete special case: higher symmetries form a filtered algebra tied
to conformal Killing tensors and an enveloping-algebra quotient.  It is evidence
for the architecture, not a completeness theorem for arbitrary `D`.

## 3. Order-lowering lift

Take a constructed `q_m in Z_p^m` and choose a declared quantization
`Op(q_m)`.  Compute, do not infer, the residual

```text
R_(r+m-2) = [D,Op(q_m)].                              (3)
```

If its highest surviving symbol is `rho_(r+m-2)`, seek a correction `q_(m-1)`
whose commutator cancels it:

```text
delta_p(q_(m-1)) = -rho_(r+m-2),                      (4)
Q_(m-1) = Op(q_m)+Op(q_(m-1)).
```

Repeat through lower orders.  At each stage there are exactly three outcomes:

- a correction exists;
- an obstruction class remains in `coker(delta_p)`;
- the deciding equation is unresolved in the declared coefficient class.

Corrections are not unique: two differ by a lower-order element of `ker(delta_p)`.
The output therefore retains an affine family modulo already constructed
symmetries rather than selecting a convenient representative and forgetting the
ambiguity.  For an order-`r` operator and an order-`m` candidate, differential
order descends finitely, although solving any one geometric equation can still be
hard or infinite-dimensional.

Subprincipal symbols, connections, curvature, potentials, bundle endomorphisms,
and boundary conditions enter precisely in this lift.  This is where a classical
integral can fail to quantize, acquire an ordering correction, or cease to
preserve the physical domain.

## 4. Candidate generation without component explosion

The constructor does not begin with every coefficient of a generic tensor.  It
uses the smallest intrinsic module selected by the operator and requested
observable:

1. extract canonical geometric data from `p`—metric, characteristic cone,
   eigenspaces, moment maps, or Clifford action;
2. decompose candidate symbols by stabilizer/covariance type;
3. solve `delta_p q=0` inside one type at a time;
4. lift only surviving symbols through (3)--(4);
5. close only the generated operators needed by the observable.

For a rotationally invariant Hamiltonian, for example, angular momentum is the
canonical moment-map output.  Asking whether an additional degree-two conserved
**vector** exists selects one irreducible covariance type.  Its determining
equation may force the potential, as in the Coulomb bench; it is not a list of all
quadratic monomials.

This is still a bounded grammar.  Its advantage is that the bound is semantic
(order, covariance type, bundle type, observable), not an arbitrary coordinate
coefficient count.

## 5. Completeness ladder

Every result carries one of four completeness tags:

```text
CanonicalSeed
  generated functorially from supplied geometry, but no full-centralizer claim;

RelativeComplete(order <= m, type set T, coefficient class A)
  symbol solutions and every lift/obstruction are complete inside the stated
  filtration and covariance modules;

AlgebraComplete(generators, relations, core)
  a theorem or Hilbert-series/graded argument proves that the presented
  operators generate the relevant centralizer/normalizer;

UnresolvedWithinBudget(first undecided equation).
```

A raw polynomial ansatz without a module-completeness proof is only a fallback
under `RelativeComplete`; it never supports “the PDE has no other symmetry.”

## 6. Closure and representation output

Successful lifts are represented differential operators on a common core.  Close
them under the bracket actually justified by the problem:

```text
ordinary commutator, supercommutator, polynomial closure over the center,
or parameter-shift composition.                              (5)
```

Record a finite presentation when possible.  Central elements and Casimir
relations then decompose modules without solving for coordinate wavefunctions.
Only constant finite-dimensional Lie closure proceeds to a real form, adjoint
realization, domain preservation, and group integration.  Thus the bilateral
route is

```text
PDE -> symbol centralizer -> lifted operator algebra -> modules -> [group],
group representation -> enveloping element -> differential realization -> PDE.
```

The brackets are the bridge; the group is an optional global endpoint.

## 7. Reproducible certificate

A replayable inverse result contains:

```text
FilteredCentralizerCertificate = (
  operator/core/domain,
  filtration and covariance module,
  principal symbol p,
  symbol equations and their solution basis,
  quantization convention,
  residual at every lowering step,
  obstruction/ambiguity classes,
  verified operator relations,
  represented module and observable,
  completeness tag,
  analytic obligations,
  whole-route complexity audit
).
```

The human-facing form retains the small covariance modules, obstruction sequence,
algebra presentation, and Casimirs.  Coordinate components may occur in a replay
certificate but are not the explanation.

## 8. Boundary and extensions

- General determining equations need not admit a finite algorithm.
- A Poisson symmetry is necessary, not sufficient, for a quantum/domain symmetry.
- Singular coefficients can change self-adjoint extensions and invalidate formal
  commutators.
- Matrix symbols require simultaneous treatment of base and fiber algebras.
- Spinorial problems replace symmetric-tensor seeds by Clifford and often
  Killing--Yano data; grading changes (5).
- Nonlinear PDEs generally require recursion operators, Lax/zero-curvature data,
  or conservation-law complexes.  Linear centralizer language alone is not a
  universal extension.

The [quadratic centralizer generator](quadratic-centralizer-generator.md) removes
the module-selection ambiguity completely for scalar even quadratic integrals on
the Euclidean plane with polynomial potential.  Its
[transfer bench](../benchmarks/quadratic-centralizer-e2.md) discovers a rotated
separation operator and returns a relative no-go on a generic control.  The
[complete `E^2` Coulomb bench](../benchmarks/coulomb-e2-complete.md) now admits radial
coefficients and rediscovers both Runge--Lenz directions from the full module.  The
[three-dimensional module](e3-quadratic-centralizer.md) now computes its
`21 -> 20` redundancy quotient before Coulomb selects the ten-dimensional kernel;
the [Coulomb bench](../benchmarks/coulomb-hidden-so4.md) consumes it and closes the
generated operators to `so(4)`. The
[quartic cyclic transfer](../benchmarks/quartic-cyclic-transfer.md) is retained as a
control showing that an exact visible group need not yield useful further spectral
compression.
