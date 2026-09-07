# Finite split coefficient algebra

## Frozen contract `C_G8_v1`

### Why this is the next general step

G7 used one involution to obtain two transport sectors. Its useful primitive was
not the Pauli matrix or a special polynomial: it was an exact coefficient algebra
with projectors and a reconstruction map. G8 removes the supplied involution and
allows several commuting Hermitian coefficients to generate more than two joint
sectors.

Let `C_1,...,C_g` be exact Hermitian `q x q` matrices over the declared
Gaussian-rational carrier. The admitted branch requires

```text
[C_i,C_j]=0                                                    (1)
```

and asks for primitive idempotents of the generated commutative algebra, not for
eigenvectors of its matrices.

### Internal construction

For each generator, the machine constructs the first exact Krylov dependence

```text
C_i^m = a_0 I + a_1 C_i + ... + a_(m-1) C_i^(m-1),
m_i(x)=x^m-sum_(j<m) a_j x^j.                                (2)
```

Thus `m_i` is derived by exact matrix-power dependence. It is not supplied as
spectral metadata. The admitted coefficient field is `Q`; each `m_i` must split
into distinct rational linear factors within the factor-search budget:

```text
m_i(x)=product_(lambda in R_i)(x-lambda).                     (3)
```

Linear and quadratic factors are resolved directly, including exact rational
discriminant checks. Higher degrees use bounded rational-root search. A factor
outside `Q` returns `CoefficientFieldExtensionRequired`; the constructor never
silently changes fields.

For every root, polynomial functional calculus constructs

```text
Q_(i,lambda) = product_(mu in R_i, mu != lambda)
               (C_i-mu I)/(lambda-mu).                       (4)
```

Starting from `I`, the machine successively retains the nonzero intersections

```text
P_s = product_i Q_(i,lambda_(s,i)).                           (5)
```

Commutation makes these products order-independent. Exact checks certify that the
final `P_s` are Hermitian, pairwise orthogonal, idempotent, and resolve identity.
They give the joint characters and reconstruction law

```text
chi_s(C_i)=lambda_(s,i),
C_i=sum_s chi_s(C_i) P_s,
A=Q[C_1,...,C_g] congruent to direct-sum_s Q P_s.             (6)
```

The carrier multiplicity `tr(P_s)` remains explicit. A repeated eigenspace of one
generator is not a failure: another generator may refine it. A final multiplicity
greater than one means the commutative algebra does not resolve the internal
carrier, not that the algebra construction failed.

### Algebra-to-operator synthesis

For a polynomial operator expression

```text
p(C_1,...,C_g)=sum_alpha c_alpha product_i C_i^alpha_i,       (7)
```

the public operation computes

```text
p(C_1,...,C_g)=sum_s p(chi_s(C_1),...,chi_s(C_g)) P_s.       (8)
```

It evaluates both sides exactly and returns only after they agree. Equation (8)
is the reusable bridge back to a reduced PDE block, spectral coefficient,
propagator, or other polynomial function of the admitted coefficients.

## Frozen discriminators

1. `A=diag(0,1,1)` and `B=diag(0,0,1)` must construct three characters
   `(0,0)`, `(1,0)`, `(1,1)` although each generator is individually degenerate.
2. The refinement ledger must read `1 -> 2 -> 3`; all final multiplicities are
   one, and both minimal polynomials are `x(x-1)`.
3. `I+2A+3B+5AB` must have sector values `1,3,11`, and projector synthesis must
   equal direct matrix evaluation.
4. Rational orthogonal conjugation must retain the characters while rotating the
   concrete projectors.
5. Reversing generator order must produce the same set of primitive projectors.
6. Noncommuting generators, an irrational quadratic factor, exhausted rational
   factor search, and malformed polynomial powers must have distinct refusals.
7. The G7 two-sector consumer must delegate to this owner without changing its
   scalar or matrix transport witnesses.

The claim is falsified if roots/projectors enter the input, a component eigenbasis
is materialized, repeated eigenspaces are discarded, generator order changes the
projector set, field extension is implicit, or (8) lacks an exact recovery check.

## Evidence ledger

The G8 closure gate runs 159 unit tests and 20 computational checks. Ruff lint and
format checks pass across 68 Python files, all 69 JSON fixtures parse, Python
compilation succeeds, and 251 local Markdown links resolve.

### `E-G8-01` — joint refinement and use

The positive three-dimensional carrier derives `m_A=m_B=x^2-x`. No rational-root
candidate search is required because the quadratic discriminants are exact. The
first generator produces ranks `1,2`; the second refines the rank-two projector,
giving three rank-one sectors. Direct and synthesized values of (7) agree.

### `E-G8-02` — invariant transfer

Conjugation by the rational orthogonal matrix with upper block
`[[3/5,-4/5],[4/5,3/5]]` makes the first coefficient non-diagonal. The unchanged
constructor returns the same joint characters and a different concrete projector
set. Reversing generator order also returns the same projector set.

### `E-G8-03` — typed boundaries and downstream regression

A noncommuting Hermitian pair returns `NoncommutingCoefficientAlgebra`. The matrix
`[[0,1],[1,1]]` derives `x^2-x-1` and returns
`CoefficientFieldExtensionRequired`. A degree-three split example with zero
factor budget returns `FactorizationBudgetExceeded`; budget 32 constructs its
three rational sectors and records nonzero search work. Nonintegral powers return
`InvalidCoefficientPolynomial`. The existing G7 tests pass through the general
owner and retain the public coupled-operator result.

## Complexity and human computability

The current dense exact implementation constructs at most `q` Krylov powers per
generator. Repeated rational elimination and projector products give a conservative
`O(g q^5 + Bq)` arithmetic bound and `O(q^3)` storage, where `B` is the admitted
rational-factor search. Final sector output has size `s <= q`; polynomial
evaluation is output-sensitive in its term count and exponentiation depth.

This is not a runtime-dominance result. Its human gain is that equations (2), (4),
(5), and (8) replace coordinate-specific simultaneous diagonalizations and an
enumeration of special-function channels. The factor budget exposes rather than
hides the remaining symbolic search.

## Disposition and next obstruction

Disposition: **supported bounded** for finite commuting Hermitian matrix families
whose internally constructed minimal polynomials split over `Q` within budget.
Primitive means primitive in the generated algebra; carrier multiplicity is
reported separately.

Noncommutative coefficient algebras, irreducible field extensions, radicals,
variable matrices, domains, and analytic completion remain outside `C_G8_v1`.
The next consequential bridge is representation-theoretic: construct the center
and commutant of a finite noncommutative star-algebra, use the present calculus on
its center, and recover isotypic blocks plus multiplicity spaces without knowing a
group in advance.
