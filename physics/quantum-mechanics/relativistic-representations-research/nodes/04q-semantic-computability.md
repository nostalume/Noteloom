# N4q — Semantic Computability as Observable Compression

Status: supported global synthesis and obstruction theorem; problem-local
compression constructions remain open  
Consumes: [N3 realization bridge](03-realization-bridge.md), [N4d computation
interface](04d-computation-interface.md), [N4m finite integer-spin field
machine](04m-finite-integer-spin-field-machine.md), [N4n adaptive reduction
audit](04n-algebraic-spectrum-bridge.md), [N4o Dirac--Coulomb graph](04o-dirac-coulomb-local-graph.md),
[N4p angular-block obstruction](04p-dirac-angular-reduction.md), and [global
computability source contracts](../sources/global-computability-contracts.md)  
Produces: an observable-relative definition of computation, a hierarchy separating
equivalence from compression, a symmetry-insufficiency theorem, and one global
view of free response, bound spectra, scattering, and field-sector elimination

## Research contract

- **Question:** what must a field or operator construction do before it counts as
  computation rather than a coordinate change, component suppression, or transfer
  of work to an unnamed inverse?
- **Capability sought:** judge proposed reductions by a same-observable equality or
  error witness and expose the additional structure that makes prediction possible.
- **Presumptions:** a physical quotient and domain have been declared; the input
  class and target observable are fixed; cost includes construction, verification,
  and recovery rather than only the final formula.
- **Boundary:** this node is not an algorithm for inventing reductions. It supplies
  a falsifiable contract and global theory view for evaluating them.

## 1. An equation is a presentation; a prediction is a composite

Let `I` be admissible input data, `P` the physical solution or state object after
gauge/domain identifications, and `Z` the output space of one named observable.
A selected well-posed response and observable are typed as

```text
Sol_D:I -> P,
O:P -> Z.
```

The actual prediction is the composite

```text
F_(D,O)=O circle Sol_D:I -> Z.
```

This construction separates three questions that an equation alone conflates:

```text
D                 presents the dynamics,
Sol_D             selects and solves the physical response,
O circle Sol_D    is the requested prediction.
```

A field redefinition, Fourier transform, angular basis, or gamma-matrix basis can
change the presentation without changing this composite. Suppose `T:P->P'` is an
isomorphism. Define

```text
Sol_D'=T circle Sol_D,
O'=O circle T^(-1).
```

Evaluate both predictions on the same `i in I`:

```text
O'(Sol_D'(i))
 =O(T^(-1)(T(Sol_D(i))))
 =O(Sol_D(i)).
```

The equality proves semantic invariance. It does **not** prove reduced computation:
`T`, the transformed solve, and `T^(-1)` may contain exactly the old work.

## 2. Constructing a genuine observable compression

A candidate reduction supplies three new maps

```text
q:I -> I_red,
C:I_red -> Y,
r:Y -> Z.
```

It is an exact observable compression only when a same-input computation proves

```text
r circle C circle q = O circle Sol_D.
```

For a controlled approximation `C_epsilon`, the corresponding witness is

```text
d_Z(r(C_epsilon(q(i))),O(Sol_D(i))) <= epsilon
```

on the declared input class. The construction earns the name *compression* only
if all of the following are visible:

1. `C` does not call `Sol_D` or an equivalent unnamed inverse as a subroutine.
2. `Y` retains only information sufficient for `O`, or its dynamics has a smaller
   denominator, rank, sector count, graph class, or controlled approximation scale.
3. Recovery `r` returns the named observable without reconstructing every discarded
   degree of freedom.
4. Construction, verification, computation, and recovery cost less than the direct
   route, or produce a reusable theorem whose stated benefit justifies that cost.

This yields four distinct claims:

| Claim | Required witness | What it does not imply |
| --- | --- | --- |
| presentation equivalence | invertible `T` and the same-input equality above | smaller computation |
| structural decomposition | exact direct sum, integral, or block recovery | simpler residual blocks |
| semantic compression | observable factorization plus reduced whole route | recovery of the full state |
| certified approximation | observable error/bound and convergence domain | exact solvability |

The observable quotient

```text
p equivalent_O p' iff O(p)=O(p')
```

describes the least information the requested output can distinguish. It is a
semantic lower target, not automatically an algorithm: forming its class may still
require solving the original problem.

## 3. Why manifest symmetry usually stops at degeneracy

Let a compact manifest symmetry `G` act unitarily on the physical Hilbert space.
Its isotypic decomposition has the form

```text
H ~= Hilbert-direct-sum_lambda V_lambda tensor M_lambda,
```

where `V_lambda` is irreducible and `M_lambda` is its multiplicity space. If a
self-adjoint `H_dyn` commutes with `G`, every bounded spectral projector
`E_Hdyn(B)` also commutes with `G`.

Take its block from `V_lambda tensor M_lambda` to
`V_mu tensor M_mu`. It is an intertwiner between `V_lambda` and `V_mu`. Schur's
theorem computes

```text
lambda != mu: block=0,
lambda = mu: block=I_(V_lambda) tensor e_lambda(B),
```

where `e_lambda` is otherwise an arbitrary projector-valued measure on
`M_lambda`. Conversely, every such family defines a `G`-invariant spectral
measure by the same direct sum. Therefore

```text
manifest symmetry fixes representation labels and degeneracies,
manifest symmetry does not fix multiplicity dynamics or energies.
```

This theorem places the earlier nodes correctly. Poincare representation theory
constructs free particle types and allowed covariance maps. It does not uniquely
select a local field presentation, an interaction, a domain, or the spectrum after
a background breaks Poincare symmetry. N4p's `kappa` split refines the
multiplicities, but its residual `Cl_2(C)~=M_2(C)` remains arbitrary dynamics in
the symmetry commutant.

## 4. When the free field path genuinely compresses

N4m does more than change carrier coordinates. Its field complex constructs
operators satisfying

```text
D_s+R_s C_s=q identity,
R_s^dagger M_s=C_s.
```

For an admissible source `J`, one scalar Green map `G_q` constructs the response;
the gauge image is then quotiented before the particle amplitude is recovered.
The same-input witness has the form

```text
J
 -> G_q J
 -> invariant finite carrier operations
 -> [physical response]
 -> shell observable.
```

Increasing integer spin changes only bounded algebraic carrier operations; it does
not introduce a new analytic denominator. Gauge quotienting removes directions
that every physical observable identifies. This is genuine semantic compression:
both the analytic operator and the physical information have been reduced.

The Dirac--Coulomb deformation fails at exactly this test. Squaring the covariant
first-order operator produces a spin--curvature term, so the scalar Green map no
longer factors the response. Rotations remove magnetic duplication, but `a,b`
retain the complete residual gamma algebra. The contrast is not
coordinate-free versus coordinate-based notation; it is scalar factorization
versus irreducible matrix-valued dynamics.

## 5. Bound states and scattering are two queries on one spectral object

For a closed self-adjoint dynamics construct

```text
R(z)=(z-H)^(-1),
E_H(B)=spectral projector of H on B.
```

An isolated bound energy is an atom of `E_H`, equivalently a resolvent pole whose
residue is its projector. Continuous response is obtained from boundary values of
the same resolvent. Thus bound and continuum physics do not require two dynamics.

Scattering asks for additional relational data. Given a reference `H_0`, the wave
operators, when they exist, compare the two evolutions, and

```text
S=Omega_+^dagger Omega_-
```

acts on the asymptotic continuous fibers. The practical separation is therefore

```text
bound query: spectral atoms of one H,
continuum query: boundary density of one H,
scattering query: continuum plus comparison with H_0.
```

Coordinates are not the source of this difference. Normalizability, thresholds,
and asymptotic comparison are different semantic outputs.

## 6. Mechanics and field theory meet through exact sector elimination

Let `P` select the degrees of freedom relevant to an observable and `Q=I-P`.
Applying `(E-H)psi=0` to both sectors and solving the `Q` equation where its
resolvent exists computes

```text
H_eff(E)
 =PHP+PHQ(E-QHQ)^(-1)QHP.
```

Substitution into the `P` equation proves that `E-H` is singular on the full
space exactly when the corresponding Feshbach operator is singular, subject to
the stated inverse and domain hypotheses. This is an exact semantic reduction
only when the target observable lives in `P` and the `Q` resolvent is cheaper or
can be controlled recursively. Otherwise the inverse merely hides the full field
problem.

Below an open-channel threshold, the effective operator can describe a closed
mechanical bound sector. Across a threshold, boundary values of the eliminated
resolvent acquire a discontinuity and return decay or scattering. This constructs
the field/mechanics relation without treating them as separate theories.

Perturbative QFT graphs compute coefficients in expansions of propagators,
self-energies, kernels, or this eliminated resolvent. The Connes--Kreimer Hopf
algebra genuinely compresses the combinatorics of subdivergence subtraction. It
does not by itself sum the series, construct a bound-state pole, or control the
nonperturbative inverse. Graph reduction and spectral reduction therefore answer
different obligations and must meet at the kernel/resolvent recovery map.

## 7. Known compression witnesses are evidence, not a method catalogue

The worktable and source contracts expose several different ways a route can
become shorter. They are regression examples, not a selector:

| Additional structure | Semantic gain actually witnessed | Boundary |
| --- | --- | --- |
| gauge complex and compatibility identities | quotient null directions and reuse one Green denominator | curvature or topology may obstruct it |
| dynamical algebra with `H=f(Casimirs)` | replace eigen-equation by unitary-label evaluation | constructing the algebra may be as hard as the spectrum |
| Feshbach--Schur isospectral map | remove sectors with exact kernel and eigenvector recovery | eliminated resolvent still carries their cost |
| Birman--Schwinger relation | convert an eigenvalue query into an eigenvalue of an auxiliary operator | only useful if compactness, kernel evaluation, or bounds improve |
| Mourre estimate | obtain limiting absorption and continuum control from a positive commutator | does not calculate bound energies |
| low-entanglement tensor representation | approximate named local observables with bounded bond dimension under area-law hypotheses | not a universal full-state or higher-dimensional solver |
| graph Hopf algebra | compress recursive renormalization combinatorics | does not compute graph integrals or resum nonperturbative poles |

The important commonality is not the mathematical form of the method. It is the
observable factorization and its recovery witness from Section 2.

## 8. Why no universal computability framework can finish the job

The spectral-gap undecidability result supplies a hard boundary: for a broad class
of translationally invariant local many-body Hamiltonians, no algorithm decides
the promised gapped/gapless alternative in every case. Therefore no symmetry,
algebra, graph, variational, or numerical recipe can be promoted into a universal
spectral solver.

This does not make local research arbitrary. It changes the global ambition from

```text
classify equations -> apply universal solver
```

to

```text
construct physical object and observable
 -> expose the obstruction left by manifest structure
 -> invent a problem-local semantic compression
 -> verify equality/error and whole-route gain
 -> otherwise use a controlled residual computation.
```

Computability is thus relative to a model class, input class, observable, accuracy,
and resource scale. Exact solvability is an exceptional additional structure, not
the generic consequence of symmetry.

## 9. The reconstructed global view

The research spine can now be read at four distinct levels:

```text
symmetry representation
  -> classifies states, orbits, spin/helicity and allowed covariance;

field realization
  -> presents those states locally through carriers, equations and gauge complexes;

dynamics plus domain/background/state
  -> constructs a definite response or spectral object;

observable compression
  -> turns that object into a prediction through a verified shorter route.
```

None of the arrows may be collapsed:

- symmetry does not uniquely determine dynamics;
- a covariant field equation does not select its Green function or state;
- a Green function or Hamiltonian does not specify which observable matters;
- a coordinate-free rewrite does not prove computational gain.

The current Dirac--Coulomb frontier is therefore pre-radial. The next useful probe
must begin with the full `H_nu`, its distinguished domain, and the gap spectral
measure. It should construct either

1. a full-operator relation that constrains the measure before a gamma subblock is
   chosen, or
2. an obstruction showing that a proposed relation contains the same residual
   inverse and therefore does not beat the fallback calculation.

Birman--Schwinger, Feshbach, hidden intertwining, variational, and numerical forms
are only candidate edges. None is accepted by its name. The first concrete test
should compute its same-observable diagram and whole-route cost on the
Dirac--Coulomb operator before any detailed expansion.

For the wider field-theory branch, [N4r](04r-field-mechanics-stability.md) now
constructs the abstract projected resolvent, exact field-state recovery, the
Gauss-law origin of the electrostatic mechanical representative, and a contour
stability estimate. What remains is its realization in one UV-controlled field
model: bound the eliminated-sector self-energy at an atomic pole and audit whether
that route is cheaper than direct recomputation.

## Checks and open boundary

Supported:

- presentation invariance is computed on the same input;
- exact/approximate observable compression has a typed commuting-diagram witness;
- the Schur-commutant computation proves the limit of manifest symmetry;
- N4m and N4p provide positive and negative regression cases;
- resolvent and Feshbach identities join bound, continuum, scattering, mechanics,
  and field sectors without identifying their observables;
- source contracts delimit exact elimination, continuum estimates, low-rank
  approximation, graph combinatorics, and undecidability.

Open:

- a pre-radial Dirac--Coulomb compression with positive whole-route gain;
- a controlled field-model realization of N4r's projected resolvent connecting
  atomic poles and radiative observables;
- quantitative cost models for symbolic, analytic, and numerical candidate edges;
- manuscript synthesis after at least one interacting prediction passes this
  contract.

## Edges

- `N3/N4m -> N4q`: pass representation realization, physical quotient, scalar
  factorization, and observable recovery as the positive free-field witness.
- `N4d/N4n -> N4q`: pass the observable interface, resolvent unity, sector
  elimination, and open reduction-edge audit.
- `N4o/N4p -> N4q`: pass the interacting Coulomb operator and proof that angular
  block diagonalization does not reduce its residual Clifford computation.
- `N4q -> N4r`: pass the full-operator observable compression contract and
  rejection test for field-sector elimination, background variation, bound poles,
  and continuum thresholds.
- `N4q -> N9`: pass observable factorization and whole-route cost; N9 constructs
  the additional criterion for autonomous reduced dynamics and its exact memory
  alternative.
- `N4q -> N7`: pass the distinction among representation, field, response,
  spectral, and computational equivalence.
