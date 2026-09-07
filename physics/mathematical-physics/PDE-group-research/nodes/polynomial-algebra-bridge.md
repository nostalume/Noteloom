# Polynomial symmetry algebra as the non-Lie middle language

## 1. The distinction that matters

“Polynomial” occurs in three different places and they must not be conflated:

1. coefficients of a PDE may be polynomial or Laurent;
2. a representation may preserve a polynomial function space;
3. an operator algebra is polynomial when brackets require products of its
   generators.

Only the third meaning changes the bilateral spine.  For generators `Q_i`, a Lie
algebra has

```text
[Q_i,Q_j]=sum_k c_ij^k Q_k                              (1)
```

with constant structure coefficients.  A polynomial algebra instead requires

```text
[Q_i,Q_j]=P_ij(H,Q_1,...,Q_r),                          (2)
```

where `H` and any other Casimirs are central and some `P_ij` has degree greater
than one.  Equation (2) is an exact finite presentation, but in general there is
no Lie algebra to integrate into a group.

## 2. Relation to Lie algebras

There are three relations, none of them an equivalence.

- **Enveloping origin.** Products of represented Lie generators lie in
  `U(g)`.  A polynomial symmetry algebra may be a subalgebra or quotient built
  from such composite operators.  This does not make its own commutator law
  linear or recover a unique `g`.
- **Central quotient.** A bracket such as
  `[A_i,A_j]=-2H epsilon_ijk L_k` becomes linear after imposing `H=E`.  This is a
  Lie shadow on one energy shell, not an off-shell Lie algebra.  Other polynomial
  algebras remain nonlinear even after fixing all central characters.
- **Contraction.** Limits of Lie algebras may induce limits of quadratic algebras
  and their representations.  This organizes families, but it does not license
  naming a group before the PDE-generated brackets have been classified.

Thus the inverse machine uses the typed route

```text
PDE coefficients and domain
  -> complete filtered centralizer within a declared module
  -> exact operator brackets
  -> Lie | super | polynomial | shift | infinite | unresolved
  -> group integration only on the Lie branch.                  (3)
```

## 3. Bounded closure constructor

Given central `H` and generated integrals `A,B`, construct `R=[A,B]`.  Test the
two new brackets first in the linear word space

```text
W_1=span{1,H,A,B},                                      (4)
```

then, only if needed, in the Hermitian degree-two word space

```text
W_2=W_1+span{H^2,HA,HB,A^2,{A,B},B^2}.                 (5)
```

Every membership test is exact differential-operator equality, not a fit to
sampled eigenvalues.  If both `[A,R]` and `[B,R]` miss `W_1` but lie in `W_2`
with a nonzero degree-two coefficient, the output is `PolynomialAlgebra` within
this word budget.  Failure to lie in `W_2` is `UnresolvedWithinBudget`, not an
infinite-algebra theorem.

The reusable output is

```text
PolynomialPresentation(
  central characters,
  star operation,
  generators and differential realization,
  oriented bracket relations,
  word filtration and exact recovery certificates,
  analytic-domain and representation obligations
).                                                       (6)
```

This is human-computable because later work uses the short presentation rather
than re-expanding third- and fourth-order differential operators.

## 4. From presentation to representation

A polynomial presentation is not yet a spectral solution.  On a central quotient
`H=E`, one still needs a positive `*`-representation.  A typical adapter seeks

```text
[N,b^+]=b^+,       [N,b^-]=-b^-,
b^+b^-=Phi_E(N),   b^-b^+=Phi_E(N+1),                  (7)
```

and derives `Phi_E` from the generated relations and Casimir, rather than looking
it up.  A finite unitary module requires endpoint and positivity conditions

```text
Phi_E(0)=0,  Phi_E(p+1)=0,  Phi_E(n)>0 for 1<=n<=p.     (8)
```

Equations (7)--(8) can quantize `E`, give multiplicity `p+1`, and generate a
three-term interbasis recurrence.  The familiar orthogonal polynomial is then a
coordinate realization of this recurrence, not an item selected from a special-
function catalogue.

The singular-oscillator bench constructs one bounded instance of (7)--(8): the
closure forces a Jacobi recurrence, endpoint termination quantizes the energy,
and positivity selects the physical branch. This is a regression/transfer for one
quadratic presentation, not yet a general compiler from every relation set to a
deformed oscillator. Spectral leverage is still judged per observable; on this
bench direct factorization remains shorter for energy alone.

## 5. Boundary

The present constructor is complete only for scalar even order-two integrals on
flat `E^2` and finite Laurent coefficients.  Higher-order integrals require a new
symbol module and larger word filtration.  Matrix potentials require graded or
Clifford-valued words.  Strong commutation, self-adjoint extensions, and
completeness of joint eigenfunctions are analytic contracts, not consequences of
formal closure.
