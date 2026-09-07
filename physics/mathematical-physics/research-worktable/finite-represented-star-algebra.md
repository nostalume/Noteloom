# Finite represented star-algebra decomposition

## Frozen contract `C_G9_v1`

### The obstruction carried forward from G8

G8 constructs primitive sectors only for commuting Hermitian coefficients. For a
noncommuting family, an eigenspace of one coefficient is generally moved by
another. Its rank therefore confounds two different quantities:

```text
dimension of an irreducible carrier x number of repeated copies.             (1)
```

Supplying a group name, irreducible labels, or a preferred tensor basis would
answer the inverse question in the input. G9 instead starts with exact Hermitian
matrices surviving from a PDE coefficient or covariance construction.

Let `C_1,...,C_g` be `q x q` matrices over `Q(i)`. The admitted presentation
requires `C_i=C_i^dagger`; hence it generates a unital complex star-algebra

```text
A = alg*(I,C_1,...,C_g) subset End(C^q).                                    (2)
```

The matrices need not commute. Roots, blocks, multiplicities, matrix units, and
group labels are absent from the input.

### Two invariant kernel constructions

The real vector space `Herm(q)` has dimension `q^2`. The machine constructs its
canonical rational basis but exposes only invariant matrix spaces. It first solves

```text
A'_sa = {X in Herm(q) : [X,C_i]=0 for every i}.                             (3)
```

It then uses the constructed basis of (3) as new constraints and solves

```text
A''_sa = {Y in Herm(q) : [Y,X]=0 for every X in A'_sa}.                     (4)
```

Equations (3)--(4) are exact rational nullspaces of commutator maps. No group
elements, algebra words, eigenvectors, or coordinate block candidates are
enumerated.

G9 admits the finite-dimensional double-commutant theorem as a theorem contract:
for a unital complex star-subalgebra of `End(C^q)`, `A''=A`. Consequently (4) is
the Hermitian part of the generated algebra, not merely a formal centralizer. The
Hermitian center is then constructed by exact intersection:

```text
Z(A)_sa = A''_sa intersect A'_sa.                                           (5)
```

Because all constraint coefficients are rational, rational elimination produces a
basis of the rational solution space and preserves its real dimension. If the
center's primitive idempotents require a field extension, the next step refuses;
the implementation does not promote rational solvability silently.

### Center first, multiplicity second

The basis constructed in (5) is a commuting Hermitian family. G8 derives its
minimal polynomials, performs bounded rational splitting, and returns primitive
central projectors `P_r`. Thus

```text
sum_r P_r=I,       P_r P_s=delta_rs P_r,       [P_r,C_i]=0.                 (6)
```

For each projector, G9 compresses the two constructed matrix spaces and computes
their exact rational dimensions:

```text
a_r = dim_R(P_r A_sa P_r),
c_r = dim_R(P_r A'_sa P_r),
q_r = tr(P_r).                                                              (7)
```

The finite-dimensional Wedderburn/double-centralizer form is the second theorem
contract:

```text
P_r C^q ~= C^(d_r) tensor C^(m_r),
P_r A P_r ~= M_(d_r)(C) tensor I_(m_r),
P_r A' P_r ~= I_(d_r) tensor M_(m_r)(C).                                   (8)
```

Hermitian `n x n` matrices have real dimension `n^2`, so (8) forces the fully
checkable integer relations

```text
a_r=d_r^2,       c_r=m_r^2,       q_r=d_r m_r.                             (9)
```

The machine takes exact integer square roots and refuses if any equality fails.
Multiplicity is therefore inferred neither from one eigenvalue degeneracy nor
from a supplied label: it is certified by the independently constructed
commutant.

### Reusable return to a differential operator

For a constant-coefficient matrix differential operator

```text
L = sum_alpha D_alpha tensor K_alpha,                                      (10)
```

apply the public coefficient decomposition to every `K_alpha` that respects the
constructed center. It computes

```text
K_(alpha,r)=P_r K_alpha P_r,
K_alpha=sum_r K_(alpha,r),
L=sum_r P_r L P_r.                                                         (11)
```

The implementation compares the two sides of (11) exactly. A coefficient with an
off-diagonal central block returns `CoefficientMixesIsotypicBlocks`. The result's
`m_r` is the representation multiplicity for spectral weights and traces; G9 does
not yet choose matrix units or an explicit `d_r`-dimensional model inside a block.

## Frozen discriminators

1. The Hermitian matrices `X=sigma_x tensor I_2` and
   `Z=sigma_z tensor I_2` must yield algebra dimension four, commutant dimension
   four, center dimension one, and `(q,d,m)=(4,2,2)`.
2. The output must contain the commutant, bicommutant, center, central projector,
   exact block dimensions, and reconstruction checks, not only the integer two.
3. Adding a one-dimensional scalar summand must construct two central blocks with
   signatures `(4,2,2)` and `(1,1,1)` without changing the constructor.
4. A rational orthogonal conjugation mixing the displayed coordinates must retain
   both signatures while rotating the concrete central projectors.
5. The complex Hermitian pair `(sigma_x,sigma_y)` must produce one irreducible
   two-dimensional block with multiplicity one.
6. A non-Hermitian presentation and a pre-materialization ambient-space budget
   failure must have distinct refusal kinds.
7. G8's public sector and polynomial results must remain unchanged after exact
   rational elimination receives one shared owner.

The claim is falsified if a block basis or irreducible label enters the input, word
or eigenvector enumeration replaces the kernels, central projectors fail exact
reconstruction, dimensions are rounded to squares, or a non-star presentation is
silently admitted.

## Evidence ledger

### `E-G9-01` — repeated irreducible regression

Two exact noncommuting `4 x 4` generators construct a four-dimensional Hermitian
commutant. Commuting the full Hermitian ambient space with that result constructs a
four-dimensional algebra. Their intersection is one-dimensional, G8 returns `I`
as the sole central projector, and (9) gives `d=m=2`.

### `E-G9-02` — mixed-isotypic and covariance transfer

The unchanged inputs extended by one scalar coordinate construct dimensions
`dim A_sa=5`, `dim A'_sa=5`, and `dim Z(A)_sa=2`. G8 separates rank-four and
rank-one central projectors; their compressed dimensions give `(4,2,2)` and
`(1,1,1)`. Conjugation by a rational orthogonal matrix mixing the first and fifth
coordinates preserves those signatures but changes the concrete projector set.

### `E-G9-03` — complex spin and typed boundaries

`sigma_x` and the Gaussian-rational `sigma_y` construct `dim A_sa=4` and
`dim A'_sa=1`, hence `d=2,m=1`. A non-Hermitian triangular generator returns
`NonStarClosedGenerators`. A rank-five input with Hermitian-space budget 24
returns `StarAlgebraBudgetExceeded` before the 25-element ambient basis is built.

The G9 closure gate runs 165 unit tests and 20 computational checks. Ruff lint and
format checks pass across 71 Python files, all 69 JSON fixtures parse, Python
compilation succeeds, and 253 local Markdown links resolve.

## Complexity and human computability

Let `h=q^2` and `c=dim_R(A'_sa)<=q^2`. The first commutator matrix contains
`2gq^4` rational entries; the second contains `2cq^4<=2q^6`. Dense rational RREF
therefore has the conservative arithmetic bound

```text
first commutant:  O(g q^6),
bicommutant:      O(c q^6) <= O(q^8),
stored systems:   O(c q^4) <= O(q^6),
center split:     the bounded G8 factor cost.                               (12)
```

Coefficient bit growth is not hidden in (12). This is not a speed claim against a
floating-point Schur or eigensystem routine. It is an exact, bounded construction
whose output is invariant and reusable.

The human path is much smaller than the internal elimination: write the coefficient
family, form two commutator kernels, intersect them, split the center, and inspect
the three integers in (9). This replaces component-wise eigenvector matching and
case-by-case representation naming. The returned `commutator_system_entries`
makes the dense symbolic cost visible rather than confusing semantic compression
with runtime reduction.

## Disposition and next obstruction

Disposition: **supported bounded** for finite Gaussian-rational Hermitian generator
presentations whose center splits rationally within budget. G9 constructs isotypic
projectors and certifies irreducible and multiplicity dimensions without knowing a
group first.

G9 alone identifies `C^d tensor C^m` but does not construct a minimal carrier.
[G10](simple-block-pde-reduction.md) now closes that constant-coefficient gap with
a primitive commutant slice and exact quadratic-symbol reconstruction. Variable
projectors and their derivative coupling remain the active boundary.
