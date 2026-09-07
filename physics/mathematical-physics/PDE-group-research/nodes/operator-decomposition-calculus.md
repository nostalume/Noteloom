# Group-typed differential-operator calculus

## 1. Change of spine

The primary object is a differential operator, not an eigenfunction and not an
already invariant Hamiltonian.  Let a compact Lie group `G` act smoothly on a
manifold `M` and equivariantly on bundles `E,F -> M`.  Write `U_E,U_F` for the
induced actions on smooth sections.  For

```text
D : Gamma(E) -> Gamma(F),      order(D) <= r,
```

the group acts on the operator itself by conjugation:

```text
(g . D) = U_F(g) D U_E(g)^(-1).                         (1)
```

This is the missing generalization of the earlier homogeneous-bundle compiler.
An invariant operator is only the trivial representation inside (1).  A general
operator decomposes into tensor-operator types and therefore becomes
**block-banded**, rather than block diagonal, on representation sectors.

The supported horizon is compact `G`, smooth finite-order operators, and a common
`G`-stable smooth core.  Noncompact groups require direct-integral and
distributional versions of every projection below and are not silently included.

## 2. Two simultaneous decompositions

There are two distinct but compatible decompositions.

### 2.1 Decompose the carriers

On the compact Hilbert realization,

```text
H_E = direct-sum_lambda V_lambda tensor M^E_lambda,
H_F = direct-sum_mu     V_mu     tensor M^F_mu.          (2)
```

`V_lambda` contains the universal group dependence; `M_lambda` contains
multiplicity, boundary, geometry, and any internal degrees of freedom.  The
earlier invariant compiler stopped here: if `[D,U(g)]=0`, Schur reduction gives

```text
D = direct-sum_lambda I_(V_lambda) tensor D_lambda.      (3)
```

### 2.2 Decompose the operator

For an irreducible representation `sigma` with character `chi_sigma` and
dimension `d_sigma`, its central isotypic projection in the operator module is

```text
P_sigma D
  = d_sigma integral_G conjugate(chi_sigma(g)) (g . D) dg.   (4)
```

Haar measure is normalized to one.  Equation (4) preserves differential order.
It is an exact, coordinate-free constructor; it is not yet a finite algorithm.

More precisely, a type-`sigma` tensor operator is a `G`-map

```text
T : V_sigma -> Diff^r(E,F),
T(sigma(g)v) = U_F(g) T(v) U_E(g)^(-1).                 (5)
```

Currying (5) produces one intertwiner

```text
T_tilde : V_sigma tensor Gamma(E) -> Gamma(F).          (6)
```

An arbitrary isotypic component can contain several independent copies of
`V_sigma`; the operator-multiplicity space must be retained.  A single “reduced
matrix element” is valid only when all relevant outer and carrier multiplicities
are one.

For a smooth operator on a compact `G`-manifold, the Peter--Weyl sum over `sigma`
is generally infinite (with convergence understood in the smooth coefficient
topology after a differential-symbol splitting).  The machine therefore returns
one of:

```text
FiniteBandwidth(types = finite set),
ControlledTail(types <= cutoff, error on named observable <= epsilon),
InfiniteFormal(types and convergence topology),
Unresolved(no proved convergence or error policy).
```

Calling every such decomposition a reduction would be false.  The first two
cases support block-sparse execution or a controlled finite truncation; neither
by itself proves that an infinite-dimensional spectral problem has become finite.

## 3. Basis-free Wigner--Eckart factorization

Restrict (6) to a source sector `lambda` and target sector `mu`.  The whole
channel factors as

```text
Hom_G(V_sigma tensor (V_lambda tensor M^E_lambda),
      V_mu tensor M^F_mu)

  = Hom_G(V_sigma tensor V_lambda, V_mu)
      tensor Hom(M^E_lambda, M^F_mu).                   (7)
```

Thus the group calculation and the analytic calculation separate:

- `C^(sigma,lambda;mu) = Hom_G(V_sigma tensor V_lambda,V_mu)` is the
  Clebsch--Gordan or outer-multiplicity space;
- the map between `M^E_lambda` and `M^F_mu` is the reduced operator;
- a channel can occur only when
  `N^(mu)_(sigma,lambda)=dim C^(sigma,lambda;mu) > 0`.

No magnetic quantum numbers and no component matrix elements are needed.  If
`sigma=1`, (7) reduces to (3).  Schur decomposition of invariant operators is
therefore the zero-bandwidth boundary of the general calculus, not a separate
method.

## 4. The operator selection graph

The semantic normal form is a labeled graph:

```text
vertex lambda
  carrier V_lambda, multiplicity space M_lambda,
  invariant diagonal block if present

edge lambda --sigma,alpha--> mu
  alpha in a basis-free outer-multiplicity space,
  reduced map R^(sigma,alpha)_(mu,lambda): M^E_lambda -> M^F_mu.
```

The graph is constructed from fusion/branching rules before any analytic matrix
is assembled.  It provides three kinds of compression:

1. forbidden blocks are proved zero by `N^(mu)_(sigma,lambda)=0`;
2. all dependence on internal representation coordinates is delegated to the
   reusable intertwiner space `C^(sigma,lambda;mu)`;
3. only reduced multiplicity maps remain problem-specific.

The selection rule is necessary, not sufficient.  A permitted reduced map can
vanish because of parity, bundle geometry, a differential identity, or the
chosen operator.  Those zeros are certificates, not corrections to the fusion
rule.

For a Hamiltonian

```text
H = H_invariant + sum_(sigma in S) T_sigma,
```

a finite set `S` gives a sparse transition graph.  Spectrum computation can then
use graph components, conserved gradings, and reduced blocks.  No speedup is
claimed until their construction and observable-recovery cost is compared with a
baseline.

## 5. Differential order without coordinate expansion

Tensor-operator decomposition alone forgets what makes `D` differential.  Retain
the order filtration

```text
Diff^0(E,F) subset ... subset Diff^r(E,F)
```

and the `G`-equivariant principal-symbol sequence

```text
0 -> Diff^(q-1)(E,F) -> Diff^q(E,F)
  --sym_q--> Gamma(Sym^q(TM) tensor Hom(E,F)) -> 0.      (8)
```

Because `G` is compact, connections on `TM`, `E`, and `F` can be averaged to
`G`-invariant connections.  Such a choice splits (8): a symbol coefficient `a_q`
is lifted by contraction with the symmetrized covariant derivative,

```text
Q_nabla(a_q)s = <a_q, nabla^(q)s>.                      (9)
```

This gives the finite-depth constructor:

```text
R_r := D
for q = r,...,0:
  a_q := sym_q(R_q)
  decompose a_q into G-types by (4)
  retain its type multiplicities and admissible state-sector edges
  R_(q-1) := R_q - Q_nabla(a_q)
```

`R_(q-1)` has order at most `q-1`, so termination is structural rather than an
exhaustive coefficient search.  The principal symbol and its `G`-type are
intrinsic.  The division of lower-order terms depends on the invariant connection;
the package records that choice and verifies that recombination returns `D`.

This is the main human-computability gain: the filtration has at most `r+1`
semantic layers, each described by irreducible types and reduced maps rather than
all chart components or all matrix entries.  Actual compression additionally
requires those types to have finite or generative descriptions; differential
order alone does not provide that.

## 6. Homogeneous-space compiler

Let `M=G/K`, choose a reductive tangent module `p = g/k`, and let

```text
E_tau = G x_K W_tau,       F_eta = G x_K W_eta.
```

At the base point, the order-`q` symbol fiber is the finite-dimensional `K`-module

```text
S_q(tau,eta)
  = Sym^q(p_C) tensor Hom(W_tau,W_eta).                 (10)
```

Frobenius reciprocity gives an admissibility test for a global operator type
`sigma`:

```text
Hom_K(V_sigma restricted to K, S_q(tau,eta)) != 0.      (11)
```

Equations (7), (10), and (11) form a two-stage compiler:

```text
isotropy branching at one fiber
  -> allowed global operator types by differential order
  -> fusion with state representations
  -> reduced multiplicity-space differential blocks.
```

This replaces a field of coordinate coefficients by finite representation data at
one point.  `G`-invariant differential operators are obtained by taking the
trivial type in (11); their standard enveloping/relative-enveloping realization is
a compatible implementation, not the definition of a general operator.

## 7. Bilateral direction

### Group and operator data to PDE decomposition

Given `(G action, E, F, D)`:

1. verify the common smooth core and conjugation action (1);
2. recurse through the order filtration (8)--(9);
3. project each symbol layer into operator types;
4. compute (11) on a homogeneous space and (7) on state sectors;
5. return the labeled graph and reduced maps;
6. attach domain, convergence/tail, and observable-recovery certificates.

This direction is constructive.  The group does not choose `D`; it compresses a
supplied `D`.

### PDE family to group data

Given only `D`, there is no canonical `G` with which to form (1).  The inverse
therefore constructs arrows before operator types:

```text
factorization/intertwiner search:
  descend from the principal-symbol factorization obstruction and cancel the
  lower-order residuals;

stabilizer search:
  find first-order X with [rho(X),D]=0;

covariance-closure search:
  find a finite family D_a for which
  [rho(X),D_a] = sum_b c(X)_a^b D_b modulo a declared residual.
```

These arrows generate a represented operator algebra.  Exact closure classifies it
as Lie, super, polynomial, parameter-shift, infinite, or unresolved; only the Lie
case proceeds to possible group integration.  Principal-symbol equations are
solved first, followed only by lower-order corrections forced by the residual.
The detailed constructor and its Riccati non-leverage test are specified in the
[operator-algebra inverse](operator-algebra-inverse.md).

The resulting selection graph does not uniquely determine a group.  Recovering a
group from representation data requires enough tensor objects, products, duals,
coherence maps, and a faithful fiber functor; a finite fragment of fusion rules
can only return an effective tensor-category candidate with ambiguity.  This is
the precise stopping point of the bilateral machine.

## 8. Constructibility and verification contract

For each result, retain the following witnesses:

```text
ActionWitness      (1) defines a representation on Diff^r;
OrderWitness       conjugation and P_sigma preserve order;
ProjectionWitness  P_sigma P_tau = delta_(sigma,tau) P_sigma by character relations;
SymbolWitness      recombination of all lifted layers equals D;
FusionWitness      every graph edge has N > 0;
ZeroWitness        every removed allowed edge has a stated extra reason;
DomainWitness      all unbounded maps share the declared invariant core;
BandwidthWitness   finite support, or a tail bound for the named observable;
RecoveryWitness    analysis -> reduced graph -> synthesis preserves that observable.
```

The machine should refuse the following upgrades:

- `operator decomposed` does not imply `spectrum solved`;
- `fusion-allowed` does not imply `nonzero coupling`;
- `compact projection formula` does not apply unchanged to a noncompact group;
- `finite differential order` does not imply finitely many group types in the
  smooth coefficient functions;
- `commutator closure` does not identify a unique global group;
- `fewer matrix entries` does not prove lower total computational cost.

## 9. Why this is more general than polynomial or spherical methods

No polynomial flag, radial variable, special-function family, or multiplicity-one
assumption appears in the constructor.  Its primitives are:

```text
group action on bundles,
operator conjugation,
differential-order symbols,
isotropy branching,
tensor-product intertwiners,
reduced multiplicity maps,
analysis/synthesis on a named observable.
```

Polynomial modules, spherical functions, Hodge complexes, spin systems, and
symmetry-breaking potentials are special consumers.  Generality is obtained not
by accepting arbitrary opaque input, but by preserving the semantic structures
that permit finite construction and honest refusal.

## 10. Current transfer and next decisive experiment

The tests use a compact non-invariant operator family: an invariant
Laplacian composed with one finite tensor type.  The compiler must predict every
possible representation-sector transition, expose additional geometric zeros,
and reconstruct the action from reduced maps.  The
[`SO(3)` tensor-operator bench](../benchmarks/tensor-operator-so3.md) is the
multiplicity-free regression.  The
[`SU(3)` outer-multiplicity bench](../benchmarks/tensor-operator-su3.md) removes both
the spherical and multiplicity-free assumptions. Its finite-sector executable
constructs the two natural intertwiners and proves that a named exchange-paired
observable requires both. The
[adjoint PDE continuation](../benchmarks/su-adjoint-multiplicity-pde.md) constructs an
actual order-two tensor family and exact analysis/synthesis on one smooth
matrix-coefficient copy. The
[PDE-first matrix closure](../benchmarks/pde-first-matrix-lie-reconstruction.md)
recovers the effective `sl_2/sl_3` algebra and the same visible witness without a
group label. The [symbol-covariance continuation](../benchmarks/matrix-symbol-covariance-casimir.md)
then generates the inner-derivation vector fields and derives the common
coefficient eigenvalue from an invariant principal pairing. Its realization is
only the algebraic polynomial core, so the next decisive experiment is analytical
and global promotion—or an explicit obstruction to it. The
[adjoint semigroup promotion](../benchmarks/matrix-adjoint-semigroup-global.md) now
constructs that visible compact block and proves that its observable sees `PSU(n)`
rather than the central cover. The next decisive experiment must replace the
full-matrix inner-derivation assumption by a bounded natural-tensor stabilizer;
none of these instances owns the general claim.
