# Singular oscillator: group-free polynomial-closure transfer

## 1. Spine binding and horizon

- **Upstream anchor:** the complete `E^2` rank-two centralizer and closure
  classification promised by the operator-algebra inverse.
- **Bridge question:** can PDE coefficients generate a non-Lie finite algebra
  without a supplied group, and does that algebra shorten the route to the same
  energy observable?
- **Invariant target:** the bound-state energy family and multiplicity on the
  positive quadrant.
- **Special resources:** flat two-dimensional space, scalar order-two
  superintegrability, exact finite Laurent coefficients, isotropic confinement,
  and inverse-square couplings in the limit-point regime.
- **Rejoin edge:** an exact polynomial presentation, an anisotropic rank-drop
  control, and a whole-route spectral verdict.
- **Stop condition:** classify the closure and decide the energy route.  Do not
  enumerate separated eigenfunctions or import a named polynomial family.

The primary theorem contracts and their limitations are recorded as sources
[39--41](../sources.md): they establish the known quadratic-algebra and
representation setting, while the coefficient-to-closure computation below is
internal to this bench.

## 2. PDE and analytic contract

In `hbar=mu=omega=1` units use

```text
H=-1/2(partial_x^2+partial_y^2)
  +1/2(x^2+y^2)+1/x^2+3/y^2,             x>0, y>0.       (1)
```

This is the input `g_x=2`, `g_y=6` in the convention
`g_i/(2x_i^2)`.  Both couplings exceed `3/4`, so the half-line endpoints are in
the limit-point regime and no boundary-extension parameter is needed.  Formal
operator equalities are checked on compactly supported smooth functions in the
open quadrant; the spectral baseline uses the corresponding self-adjoint
singular-oscillator theorem contract.

## 3. Construction from coefficients

The metric supplies the three Euclidean Killing vectors.  Their symmetric square
is the complete six-dimensional rank-two module.  The exact Laurent
Bertrand--Darboux map

```text
B_V(K)=d(K dV)                                           (2)
```

has rank three on (1), hence kernel dimension three.  After distinguishing the
metric line, the two generated hidden operators are

```text
A=-1/2 (x partial_y-y partial_x)^2+y^2/x^2+3x^2/y^2,
B=-1/2 partial_x^2+x^2/2+1/x^2.                         (3)
```

The program obtains their tensors and lower terms from (2); equations (3) only
name the compact promoted result.  Full Leibniz composition verifies

```text
[H,A]=[H,B]=0.                                           (4)
```

No coordinate separation, special function, group, or known integral is an
input.

## 4. Exact nonlinear closure

Set `R=[A,B]`.  Exact membership in the linear word space
`span{1,H,A,B}` fails.  Membership in the degree-two space succeeds and gives

```text
[A,R]=-6H+28B-4HA+4{A,B},
[B,R]=-1-4A+4HB-4B^2.                                  (5)
```

Here `{A,B}=AB+BA`.  The first commutator `R` has differential order three; the
right sides in (5) reconstruct both higher commutators exactly as differential
operators.  Nonzero `HA`, `HB`, `{A,B}`, and `B^2` terms prove that these
generators do not form a Lie algebra with constant structure coefficients.
Fixing `H=E` does not remove `{A,B}` or `B^2`, so unlike the Coulomb example this
algebra does not become linear merely by passing to one energy shell.

The correct inverse output is therefore `PolynomialAlgebra`.  A parent
enveloping-algebra realization may exist, but is neither unique nor required by
the coefficient-to-closure construction.  Group integration is not applied.

## 5. Transfer control

Change only the `y` oscillator frequency from `1` to `2`.  The same complete
module and Laurent engine then return

```text
quadratic kernel: 3 -> 2,
hidden quotient:  2 -> 1.                               (6)
```

Only the Cartesian separated integral remains besides `H`; there are not two
hidden generators from which to form the nonabelian quadratic algebra.  This
rank drop shows that (5) is selected by isotropic superintegrability, not inserted
by the closure classifier.

## 6. Positive representation generated from closure

Fix `H=E` and diagonalize `B`.  Write `B|n>=b_n|n>` and let `A` be Hermitian.
The off-diagonal matrix elements of the second relation in (5) give

```text
-(b_m-b_n)^2 A_nm=-4A_nm.                              (7)
```

Hence every connected transition has step two.  The lowest weight of the
generated one-dimensional `x` factor gives `b_0=5/2`, so `b_n=2n+5/2`; no
component wavefunctions are required. The diagonal part of the same relation
then forces

```text
a_n=<n|A|n>=E b_n-b_n^2-1/4.                           (8)
```

Let `u_(n+1)=<n|A|n+1>` with positive phase.  The diagonal part of the first
relation in (5) gives a first-order recurrence for `u_(n+1)^2`. Starting with
`u_0=0`, summing through a prospective level `N` factorizes the upper endpoint:

```text
u_(N+1)^2=0
  iff (E-(2N+1))(E-(2N+6))=0.                          (9)
```

The branch `E=2N+1` has a negative internal norm when `N>=1`; for `N=0` it
violates the complementary lower bound `H-B>=7/2`.  The unique positive branch is

```text
E_N=2N+6,
u_(n+1)^2=4(n+1)(n+5/2)(N-n)(N-n+5/2)>0               (10)
```

for `0<=n<N`, with `u_(N+1)=0`.  Thus the closure constructs a positive module of
dimension `N+1` and recovers both the energy and degeneracy.

More importantly for human computation, the same Jacobi data generates the
interbasis characteristic recurrence

```text
P_(n+1)(lambda)
  =(lambda-a_n)P_n(lambda)-u_n^2 P_(n-1)(lambda).       (11)
```

This recurrence, rather than a named orthogonal-polynomial table, is the compact
map between the `B`-adapted Cartesian basis and the `A`-adapted angular basis.
The executable constructor derives and verifies levels `N=0,...,4`; equations
(7)--(10) give the finite-arithmetic family proof.

## 7. Same-observable cost verdict

Direct factorization writes `H=h_x+h_y`.  With

```text
nu_x=sqrt(g_x+1/4)=3/2,    nu_y=sqrt(g_y+1/4)=5/2,
E_i(n_i)=2n_i+1+nu_i,                                  (12)
```

the common observable is

```text
E_N=2N+6,               multiplicity=N+1.               (13)
```

The multiplicity follows from the `N+1` nonnegative pairs satisfying
`n_x+n_y=N`.  For (8), separated factorization is shorter: the polynomial route
adds the six-column compatibility kernel, closure solve, and Jacobi construction
before reaching the same result.

This branch therefore supports two different conclusions:

- the common middle language genuinely exceeds Lie/group recognition;
- polynomial closure independently recovers the spectrum, but is not cheaper for
  the energy observable;
- it additionally generates the finite interbasis recurrence (11).

The [interbasis cross-probe](singular-interbasis-cross-probe.md) closes the
phase-insensitive same-observable comparison. It independently constructs the
two factor `su(1,1)` representations, identifies `A` as an affine coproduct
Casimir, and obtains the same Jacobi data, simple spectrum, and normalized
transition probabilities. Neither route dominates: the factor route is shorter
after a Cartesian split is known, whereas this route discovers the integrals
without a prior group and supplies relative completeness.

## 8. Reproducibility and boundary

Run

```powershell
python physics\mathematical-physics\PDE-group-research\computation\singular_polynomial_closure.py `
  physics\mathematical-physics\PDE-group-research\computation\examples\singular-isotropic-e2.json `
  --summary
```

The full JSON retains the six-column compatibility system indirectly through its
rank, the generated operators, exact closure coefficients, word budget,
certificates, and cost verdict. Persistent tests cover the positive transfer,
nonlinearity requirement, positive representation/recurrence, energy-route
decision, CLI, domain refusal, anisotropic control, and a second rational-coupling
input whose symbolic representation labels are generated rather than hardcoded.

Not certified: strong commutation of `A,B`; coordinate-dependent overlap phases
or spatial kernels; arbitrary couplings with irrational indicial exponents;
higher dimensions or higher-order integrals.
