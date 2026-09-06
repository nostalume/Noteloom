# Coordinate-free decomposition of linear PDE systems

## 1. Why PDE is not merely a larger ODE

An ODE has one cotangent direction, so a scalar quadratic principal symbol is
locally factorable after choosing a square root.  A PDE has an entire cotangent
fiber at every point.  Its symbol can change rank, have several characteristic
branches, fail to factor through scalar first-order operators, or carry gauge
null directions.  A general PDE decomposition must therefore begin with bundles,
jets, and symbols—not with a preferred coordinate separation.

The revised common object is

```text
jet-level differential operator
  -> symbol geometry and characteristic/mode data
  -> compatible factor, commutant, complex, or microlocal arrows
  -> represented operator algebra/algebroid
  -> analytic direct sum/integral or obstruction.                       (1)
```

Group representations enter when the constructed arrows close globally to a Lie
action.  They are one branch of (1), not its prerequisite.

## 2. Coordinate-independent input

Let `E,F -> M` be vector bundles.  A linear differential operator of order at most
`r` is encoded by a bundle map

```text
d_D : J^r E -> F,             D = d_D o j^r.             (2)
```

Here `J^r E` is the jet bundle and `j^r s` records the value of a section and its
derivatives through order `r` without choosing a chart.  A change of coordinates
or bundle frame acts functorially on both sides of (2).  It changes the array of
coefficients but not `d_D`.

For an order-two operator, the induced filtration produces

```text
sigma_2(D)(x,xi) : E_x -> F_x,     xi in T_x^*M,         (3)
```

together with connection-dependent first- and zero-order representatives.  The
top symbol (3) is intrinsic.  The machine records any connection used to split the
lower layers and verifies recombination to `D`.

Coordinate changes and physical symmetries are therefore different types:

```text
coordinate/frame change = equivalent presentation of (2),
symmetry/intertwiner     = an automorphism or arrow preserving specified operator
                            and domain data.
```

Confusing these two creates spurious “symmetry groups.”

## 3. First decomposition: the symbol geometry

Before searching for a group, compute the following intrinsic objects from (3):

1. **rank strata:** where `rank sigma_2(D)(x,xi)` changes;
2. **characteristic variety:** covectors where the symbol is noninvertible;
3. **factorization type:** whether the symbol factors through an intermediate
   bundle;
4. **spectral projectors/eigenbundles:** when the matrix-valued symbol is
   diagonalisable with separated eigenvalues;
5. **null complex:** gauge or constraint directions invisible to the principal
   equation;
6. **symbol automorphisms:** vector fields and fiber maps preserving the symbol or
   transforming it within a finite module.

This produces a bounded sequence of geometric diagnostics even when no global
separation or Lie group exists; carrying them out can still be analytically hard.
Projectors are used only on constant-rank, spectrally separated regions;
eigenvalue crossings are retained as gluing or mode-conversion loci.

The group-free symmetry candidate is obtained by a stabilizer descent:

```text
Aut(symbol strata)
  contains Aut(symbol + connection/lower layers)
  contains Aut(D + domain + boundary + observable).                    (4)
```

At one fiber the first stabilizer is finite-dimensional linear algebra; global
compatibility can reduce it to a Lie group, a bundle of groups, a pseudogroup, or
nothing nontrivial.  This descent constructs symmetry from the PDE data instead of
testing a list of named groups.

For a boundary condition `B Gamma_r u=0`, the last descent is executable through

```text
R_boundary(Q)=(B Gamma_r Q)|ker(B Gamma_r).             (4a)
```

It is not optional bookkeeping. A formal arrow with `[D,Q]=0` but
`R_boundary(Q)!=0` does not act on the realized spectral problem. In the
[quadratic-boundary probe](benchmarks/boundary-domain-symmetry-complexity.md),
`-Delta` retains all three `e(2)` generators as an expression, the disk retains
only rotation, and a noncircular ellipse retains no connected Euclidean generator.
The orbit/character coordinates are constructed after this test.

## 4. Four decomposition mechanisms

The constructor should select among four mechanisms rather than demand one
universal kind of separation.

### 4.1 First-order symbol factorization

Seek a bundle `W` and linear symbols

```text
a(x,xi):E_x -> W_x,      b(x,xi):W_x -> F_x
```

such that

```text
sigma_2(D)(x,xi) = b(x,xi)a(x,xi).                      (5)
```

Lift `a,b` to first-order differential operators and cancel lower-order residuals
as in the [operator-algebra inverse](operator-algebra-inverse.md).  Scalar
factorization is not required: Dirac and gauge systems naturally need a larger
intermediate bundle.

### 4.2 Joint commutant decomposition

Construct operators `Q_1,...,Q_k` from the symbol Poisson equations and forced
lower-order corrections.  Formal commutation is checked on a common core:

```text
[D,Q_i]=0,             [Q_i,Q_j]=0.                     (6)
```

If their closed realizations strongly commute, the joint spectral theorem gives

```text
H = integral^oplus H_lambda dmu(lambda),
D = integral^oplus D_lambda dmu(lambda).                (7)
```

Equation (7) is the actual PDE decomposition.  It may yield ODEs, lower-dimensional
PDEs, finite blocks, or scalar multiplication.  Formal commutators alone do not
justify the direct integral.

When the principal symbols `q_i` are independent and Poisson commute, their
Hamiltonian distributions are involutive.  Frobenius then produces adapted local
coordinates; action-angle coordinates require the additional Liouville
integrability, regularity, and compactness hypotheses.  Coordinates enter *after*
the commuting geometry is constructed; they do not generate it.

### 4.3 Noncommuting symmetry/orbit decomposition

If discovered first-order arrows close to a Lie algebra, decompose along its
orbits and irreducible modules.  Orbit variables are treated representation-wise;
the quotient variables retain a reduced PDE.  Only when the quotient is
one-dimensional does the result become an ODE.  This is the honest generalization
of radial reduction.

The executable specialization is now stated in the
[orbit-space reduction calculus](orbit-space-reduction-calculus.md). It adds
orbit-type strata, isotropy multiplicity bundles, descended boundary traces,
source/spectral/observable sector policies, analysis/synthesis residuals, and the
cohomogeneity cost law. The
[axial quotient-PDE benchmark](benchmarks/axial-nonseparable-quotient-pde.md)
constructs `SO(2)` from a 3D operator/domain pair and stops at coupled 2D sector
PDEs, proving that this branch does not depend on complete separation into ODEs.

### 4.4 Differential-complex and microlocal decomposition

For gauge-degenerate symbols, construct a complex

```text
Gamma(E_0) --d_0--> Gamma(E_1) --d_1--> ...,
d_(i+1)d_i=0,                                               (8)
```

and place physical modes in cohomology or in a gauge-fixed elliptic/hyperbolic
realization.  For variable coefficients without global algebraic closure, use
local spectral projectors and Hamiltonian propagation of the characteristic
branches.  The output is then a microlocal mode decomposition with transition
data, not a global group representation.

## 5. Coordinate comparison and global gluing

Suppose two charts produce reductions `R_alpha` and `R_beta`.  They describe the
same decomposition only when the transition map on the overlap intertwines:

```text
T_(alpha beta) R_beta(D) = R_alpha(D) T_(alpha beta),    (9)
```

and transports domains, boundary conditions, preparation, and observable.  Local
mode bundles are glued by these intertwiners.  Nontrivial cocycles can produce
holonomy, Berry phases, spin structures, or an obstruction to a global basis.

Consequently, “try Cartesian, spherical, parabolic, ...” is not the general
algorithm.  The algorithm constructs distributions/projectors first and regards a
named coordinate system as one possible trivialization.

## 6. Spinors force a richer factorization object

Let `(M,g)` admit a spin or `Spin^c` structure, with spinor bundle `S` and Clifford
action

```text
c(xi)c(eta)+c(eta)c(xi) = -2 g^(-1)(xi,eta) I.         (10)
```

Conversely, suppose a first-order PDE supplies a symbol `c(xi)` whose
anticommutator is scalar.  If `N=rank(S)`, the symbol reconstructs the inverse
metric by

```text
g^(-1)(xi,eta)
  = -(1/(2N)) trace[c(xi)c(eta)+c(eta)c(xi)].           (11)
```

The automorphisms preserving this symbol construct the orthogonal action and its
possible spinorial lift; the spin group is not required as a prior name.  Failure
of the local lifts to glue is the global spin obstruction.

The relation (10) constructs a matrix factorization of the metric quadratic form.
With a compatible spin connection,

```text
Dirac = c o nabla^S,       sigma_1(Dirac)(xi)=c(xi),   (12)
```

where the conventional factor of `i` is absorbed into the symbol convention.

Squaring (12), using (10) and connection compatibility, yields a Laplace-type
operator plus curvature.  In the untwisted
Riemannian convention the Lichnerowicz formula is

```text
Dirac^2 = (nabla^S)^* nabla^S + Scal/4.                (13)
```

Twisting by a gauge bundle adds Clifford action of its curvature.  Hence a spinor
PDE decomposition must retain:

- the Clifford module, not just the scalar principal polynomial;
- the spin/`Spin^c` topology and double cover of frame rotations;
- connection and gauge curvature;
- chirality, charge conjugation, and grading when present;
- supercommutators when odd Dirac-type arrows square to even Hamiltonians.

A scalar Laplace-type operator admits a local metric symbol, but it has a global
Dirac square root only when the required Clifford module and topology exist and
the lower-order curvature/potential terms match.  Failure to factor is meaningful
geometric information.

If a symmetry action is eventually found, it must lift to the spinor bundle.  The
effective group may be a double cover such as `Spin(n)` rather than `SO(n)`, and
the central sign cannot be discarded when half-integer representations are
physical.

## 7. A generalized PDE decomposition package

The reusable output is

```text
PDEDecomposition = (
  jet operator and allowed equivalences,
  symbol rank/characteristic strata,
  factor or eigenbundle/complex data,
  generated commutant, ladder algebra, Lie algebroid, or local mode system,
  base/orbit/quotient dimensional split,
  direct-sum/integral or cohomological analysis map,
  synthesis and observable recovery,
  chart/frame/gauge gluing cocycle,
  domain and boundary realization,
  obstruction and validity region
).                                                      (14)
```

This package includes but does not privilege separation into ODEs.

## 8. Cases the earlier group picture misses

The symbol-first classifier exposes several general regimes:

| Symbol/analytic feature | Correct decomposition object |
| --- | --- |
| elliptic scalar, finite commutant | joint spectral blocks |
| real characteristic branches | microlocal propagation/scattering channels |
| matrix symbol with a spectral gap | mode eigenbundles and Berry connection |
| gauge-null symbol | differential complex and cohomology |
| first-order Clifford factor | spinor module and superalgebra |
| only local symmetry closure | Lie algebroid or pseudogroup |
| non-self-adjoint realization | generalized eigenspaces, resonances, pseudospectral bounds |
| boundary/interface | boundary operator and transmission graph |
| singular/variable-rank symbol | stratified local decompositions with gluing |

These are not peripheral exceptions.  They show that “find the hidden Lie group”
is too narrow as a universal inverse request.  The broader invariant is the
operator/module/complex structure that preserves the chosen observable.

## 9. Refusal and success criteria

The machine succeeds only if it returns an analysis map and reconstruction of the
same solution or observable.  It refuses stronger claims when:

- symbol factors do not lift through lower-order residuals;
- commuting operators fail strong/domain commutation;
- adapted coordinates exist only locally and gluing has nontrivial holonomy;
- a spin or `Spin^c` lift is absent;
- eigenbundles collide and no controlled mode-conversion theory is supplied;
- boundary conditions destroy the constructed arrows;
- the generated operator algebra grows without finite or controlled closure.

The immediate spinor regression is the
[uniform-field Pauli decomposition](benchmarks/spinor-pauli-landau.md).  It uses
curvature rather than a gauge potential to construct the preferred direction,
Clifford factorization, transverse ladder algebra, spin projectors, and the final
direct-integral decomposition.  Its variable-coefficient continuation is the
[adiabatic mode-bundle calculus](adiabatic-mode-bundle-calculus.md), tested first
on the [spin-texture PDE](benchmarks/spin-texture-adiabatic.md).  There a fixed
ladder is replaced by the projector connection and its off-diagonal second
fundamental form, with `[H,P]` retained as the observable-level defect.

## 10. Outer horizon beyond linear local PDE

For a nonlinear equation, the intrinsic object is a submanifold or differential
ideal in a jet space rather than a linear bundle map.  Its linearization at a
solution produces a family of operators to which the present machine applies, but
that yields tangent stability/mode information, not a decomposition of the full
nonlinear solution space.  A genuine nonlinear extension would need to construct
and verify structures such as multilinear intertwiners, recursion operators,
zero-curvature/Lax data, or a symmetry algebroid directly on the equation
manifold.

Nonlocal and pseudodifferential equations replace polynomial symbols by symbol
classes and Fourier-integral propagation; time-dependent systems may require
cocycles or Floquet objects; random coefficients require measurable rather than
smooth decompositions.  These are re-entry branches when a named observable needs
them.  They are not consequences of the present linear finite-order contract.
