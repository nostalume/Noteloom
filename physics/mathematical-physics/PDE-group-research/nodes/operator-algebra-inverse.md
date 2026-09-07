# Differential operator to ladder algebra, representation, and group

## 1. Corrected bilateral spine

The group cannot be an obligatory input to the inverse direction.  The shared
middle object must instead be constructed directly from the differential problem:

```text
linear differential family
  -> factorization and intertwining arrows
  -> filtered operator algebra and cyclic modules
  -> Lie / super / polynomial / shift classification
  -> group integration only when justified
  -> representation-sector decomposition and observable recovery.       (1)
```

The forward direction reverses the supported part of this route:

```text
represented algebra + chosen enveloping element
  -> differential realization
  -> PDE/ODE + factorization + spectrum/observable.                       (2)
```

Thus the genuinely bilateral correspondence is between differential problems and
**represented operator algebras**.  A Lie group is one possible global completion,
not a presumed universal endpoint.

## 2. Input and bounded horizon

Start with no group:

```text
InverseLadderProblem = (
  linear operator pencil L_a of order <= 2 on bundle E,
  parameter space a and allowed parameter shifts s,
  common dense core C and boundary conditions,
  coefficient field and adjoint pairing,
  allowed intermediate bundle W,
  arrow order bound (initially one),
  coefficient class / geometric regularity class,
  observable O and resource bound R
).
```

The active horizon is exact first-order factorization or intertwining of a linear
second-order family.  Higher-order arrows are a bounded extension.  Arbitrary
nonlinear PDEs and an unbounded search over all smooth coefficient functions are
outside this node.

## 3. Construct arrows from residuals

Seek first-order maps

```text
A_a : Gamma(E) -> Gamma(W),
B_a : Gamma(W) -> Gamma(E)
```

and scalars `lambda_a,tilde_lambda_a` satisfying on `C`

```text
L_a - lambda_a       = B_a A_a,
L_(s(a)) - tilde_lambda_a = A_a B_a.                    (3)
```

These equations are not guessed after naming a Lie algebra.  They are constructed
by descending differential order.

### 3.1 Principal-symbol obstruction

At order two, (3) forces

```text
sym_2(L_a) = sym_1(B_a) sym_1(A_a).                     (4)
```

The product in (4) is composition through the intermediate fiber `W`.  If no such
factorization exists in the declared bundle and coefficient class, the scalar
first-order route stops immediately.  Enlarging `W` to a Clifford or Dirac-type
bundle is a new, explicitly charged assumption, not an automatic repair.

### 3.2 Forced lower-order corrections

Choose a lift of a successful symbol factorization and compute

```text
R_1 = L_a - B_a^(1) A_a^(1).
```

`R_1` has order at most one.  Add zero-order corrections to `A_a,B_a`, recompute
the residual, and solve only the equations required to cancel `sym_1(R_1)` and
then `sym_0(R_0)`.  The output is either (3) or the first nonzero residual together
with its bundle type.  This order descent is finite; solving its coefficient
equations may still be difficult.

### 3.3 Intertwining is a computed consequence

When (3) holds, evaluate both routes on the same `u in C`:

```text
A_a L_a u
  = A_a(B_a A_a + lambda_a)u
  = (A_a B_a)A_a u + lambda_a A_a u
  = L_(s(a))A_a u
      + (lambda_a-tilde_lambda_a)A_a u.                 (5)
```

So `A_a` transports an `L_a` eigenstate to an `L_(s(a))` eigenstate with the
computed shift.  The reverse relation follows from `B_a`.  Equation (5), not the
terminology “raising operator,” is the ladder certificate.

## 4. Factorization alone is not yet a construction advantage

For a one-dimensional Schrödinger operator

```text
H = -d^2/dx^2 + V(x),
A_- = d/dx + W(x),
A_+ = -d/dx + W(x),
```

the identity `H=A_+A_-+epsilon` requires

```text
W^2-W' = V-epsilon.                                    (6)
```

Equation (6) is Riccati.  With `W=-psi_0'/psi_0`, it is equivalent to
`H psi_0=epsilon psi_0`.  Therefore a factorization obtained by first solving for
`psi_0` merely repackages the original problem.

The inverse machine calls factorization constructive only if at least one of the
following generates `W` more cheaply than the original spectral problem:

- a finite coefficient class closes under the residual equations;
- a parameter shift makes (3) shape invariant;
- geometry supplies a Dirac/Clifford square root;
- a finite commutator module forces the missing coefficients;
- a controlled approximation gives an observable-level error bound.

Otherwise it returns `FormalFactorization(no_leverage_witness)`.

## 5. Discover the algebra after discovering the arrows

From every certified arrow construct the budgeted presented algebra

```text
A_R(L) = FreeAlg<L_a,A_i,B_i,S_i,I> / I_cert,                     (7)
```

where `I_cert` is generated only by identities actually verified on `C` within
resource bound `R`; unknown additional identities are not silently quotiented.
The differential realization accompanies (7), so every relation can be evaluated
again.  Here `S_i` records a genuine parameter shift when present.  Compute
commutators, anticommutators when grading is supplied, and compositions modulo
already proved relations.  Classify the output rather than forcing it into a Lie
template:

```text
LieAlgebra
  commutators close with constant structure constants;

LieSuperalgebra
  a declared Z_2 grading closes under the superbracket;

PolynomialAlgebra
  commutators close only with polynomial functions of L or central elements;

ShiftGroupoidOrCrossedProduct
  closure requires parameter-changing arrows S_i;

InfiniteOperatorAlgebra
  successive commutators generate unbounded independent types;

UnresolvedWithinBudget
  equality or independence cannot be decided under R.
```

This prevents a common category error: raising and lowering operators often form
a polynomial or parameter-shift algebra, not the Lie algebra of a unique group.

## 6. Construct representations without first naming the group

If a lowering arrow and a normalizable cyclic vector satisfy

```text
A_- psi_0 = 0,        L psi_0 = E_0 psi_0,              (8)
```

then repeated certified raising arrows construct a cyclic module.  Equation (5)
generates its spectral labels and norms are generated from the adjoint/factorization
relations.  The machine must still check:

- every generated vector belongs to the operator domains;
- zero or negative norms do not appear in a claimed unitary realization;
- the cyclic module is complete for the named observable;
- missing sectors and scattering states are reported;
- boundary conditions are transported by every arrow.

Absence of a lowest-weight vector does not refute representation structure; it
changes the requested module class to continuous, principal-series, or another
non-highest-weight realization.

## 7. The group is a certified global output

A finite-dimensional Lie algebra candidate `g_eff` is integrated only after:

1. Jacobi holds for the computed structure constants;
2. the differential representation is faithful modulo a reported kernel;
3. a real form and adjoint convention are selected;
4. the generators admit compatible closed/skew-adjoint realizations or another
   stated integration theorem applies;
5. local flows preserve the physical domain and boundary data.

The output is then an effective group or cover with kernel and topology ambiguity.
If these checks fail, the operator algebra and its module remain valid local
outputs; inventing a group name would lose information.

## 8. Symmetry and spectrum generation are parallel outputs

The same PDE can generate different useful algebras:

```text
commutant algebra:       [Q,L]=0
  -> degeneracy and block decomposition;

ladder/dynamical algebra: [L,A] != 0 but closes
  -> motion between spectral or parameter sectors;

factorization algebra:    L-lambda=BA
  -> positivity, ground sector, partner operators;

geometric symmetry:       prolonged vector fields preserve the PDE
  -> invariant variables and solution reduction.
```

They should be compared by the requested observable, not merged because their
integrated groups happen to share a name.

## 9. PDE-first discovery by filtered centralizers

First-order factorization is only one inverse channel.  For hidden symmetries of
order `m`, the authoritative construction is now the
[filtered centralizer calculus](filtered-centralizer-calculus.md).  If `p` and
`q` are the principal symbols of `L` and a candidate `Q`, the highest commutator
symbol is

```text
sym_([ord L]+m-1)([L,Q]) = (hbar/i){p,q}_Poisson.        (9)
```

The constructor first solves the invariant equation `{p,q}=0` in a selected
covariance module, not in the space of every coordinate coefficient.  It then
quantizes a surviving symbol, computes the lower-order residual, and recursively
cancels only the terms forced by that residual.  Failure returns a class in the
cokernel of the next symbol equation.  Nonuniqueness returns the affine ambiguity
modulo lower-order centralizers.

This gives a finite **order descent**, not a universal finite algorithm.  The
determining equation may remain as hard as the original PDE, and completeness is
always tagged relative to order, covariance types, and coefficient class.  A raw
bounded ansatz is a fallback, never evidence that the full centralizer is absent.

## 10. Bilateral round-trip certificate

For a successful inverse result, retain an element `u_L` of the generated algebra
with represented action

```text
rho(u_L)|_C = L|_C.                                    (10)
```

Starting from the generated representation and applying the forward differential
realization must reproduce (10), the same boundary realization, and the same named
observable.  Conversely, beginning with a represented algebra can recover only its
effective image on the selected cyclic sector; covers, kernels, inactive factors,
and alternative algebra completions remain ambiguity data.

## 11. Benchmarks and frontier

The [quadratic-oscillator inverse](../benchmarks/inverse-quadratic-oscillator.md)
constructs its modes, ladders, spectrum, and oscillator algebra from the PDE
coefficients without a supplied group.  It is a regression with a genuine inverse
construction because its factor coefficients come from a finite generalized
eigenproblem, not from a known eigenfunction.

The [noncentral oscillator cross-probe](../benchmarks/oscillator-cross-probe.md)
reuses that construction against the complete quadratic-centralizer route. Both
produce identical primitive projectors, modal representation, spectrum, and heat
trace, so the inverse engine selects direct factorization and retains the larger
centralizer construction only for its distinct completeness claim.

The [singular-oscillator transfer](../benchmarks/singular-oscillator-polynomial.md)
executes the next closure branch. From finite Laurent coefficients, the complete
six-dimensional `E^2` module produces two hidden quadratic integrals. Their
third-order commutator fails linear closure but closes exactly through degree-two
words, so the machine returns `PolynomialAlgebra` and does not invent a group.
An anisotropic control removes one hidden direction. The
[polynomial bridge](polynomial-algebra-bridge.md) records why an enveloping-algebra
parent, energy-shell Lie shadow, and polynomial algebra are distinct objects.
On each central character, the same relations force a positive finite Jacobi
module, recover `E_N=2N+6` and multiplicity `N+1`, and generate an interbasis
recurrence without naming its orthogonal-polynomial realization. The
[interbasis cross-probe](../benchmarks/singular-interbasis-cross-probe.md) constructs
an independent factor `su(1,1)` route, identifies `A` as an affine coproduct
Casimir, and proves exact equality of the normalized transition probabilities.

The [Coulomb hidden-algebra bench](../benchmarks/coulomb-hidden-so4.md) now tests a
stronger route. The metric generates and quotients the complete order-two
candidate module; Coulomb coefficients select the Runge--Lenz sector, whose
compact vector obstruction forces the inverse-radius form; Hermitian lift and
bracket closure produce the negative-energy
`su(2)+su(2)` algebra; one Casimir calculation returns the complete bound energy
and degeneracy formulas.  The group name is a late output.  The calculation is a
regression because the physics is known, but it tests the new machine rather than
generating its rules.

Relative completeness is now realized for scalar even quadratic symbols on `E^2`,
including polynomial and a finite radial--Laurent coefficient domain.  The latter
rediscovers the two-dimensional Coulomb Runge--Lenz operators from the complete
module and closes their energy-shell algebra. The
[three-dimensional module](e3-quadratic-centralizer.md) now computes its
nontrivial presentation quotient and rejoins exact `so(4)` closure. The active
frontier is no longer closure classification, the first positive representation,
or the first same-observable polynomial--Lie cross-probe. The
[boundary-domain probe](../benchmarks/boundary-domain-symmetry-complexity.md) now
shows that the inverse must intersect formal commutants with the boundary-domain
stabilizer: the disk keeps rotation and gains an exact dense Ritz block reduction,
while the ellipse refuses every connected generator. The weakest cost bridge is
whether that gain survives fixed continuum accuracy, conditioning, and a best
sparse/partial-spectrum baseline. A second polynomial presentation,
dimension-/metric-parametric generation, and higher-order graded centralizers
remain open but do not outrank this cost discriminator. The
[whole-route audit](../complexity-reduction-audit.md) continues to distinguish work
eliminated from analytic difficulty merely relocated.
