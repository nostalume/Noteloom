# Bounded refusal probe

## Purpose

The inverse machine must distinguish:

```text
no candidate found within a finite declared ansatz
```

from

```text
no symmetry or representation exists.
```

Only the first conclusion is available to a bounded symbolic search.

This file is now a **fallback/control**, not the primary inverse workflow.  The
[filtered centralizer calculus](../nodes/filtered-centralizer-calculus.md) first seeks a
geometric Poisson-symbol obstruction and forced lower-order lift.  The coefficient
budget below is used only when no canonical covariance module or finite-type
symbol description has been constructed.

## Probe family

Use the one-dimensional Schrödinger family on a stated self-adjoint domain,

```text
H_g = -partial_x² + x² + g x⁴,  g != 0,
```

as a challenge to the same finite Lie-realization ansatz that handles the harmonic
oscillator at `g=0`.  The point is not to prove universal non-solvability of the
quartic oscillator.  It is to test whether the constructor refuses an unsupported
finite closure or shape-invariant chain.

## Search budget

Declare before solving:

- at most three first-order generators
  `X_i = a_i(x) partial_x + b_i(x)`;
- polynomial `a_i,b_i` of degree at most two over `Q(g)`;
- constant structure coefficients;
- realization of `H_g` by a filtered-degree-two element of the generated
  enveloping algebra, modulo an additive scalar;
- optional first-order factorization with polynomial/rational superpotential of a
  separately stated degree bound;
- exact rational-function zero testing.

## Construction

1. Form the coefficient equations for
   `[X_i,X_j] - sum_k c_ij^k X_k = 0`.
2. Form the coefficient equations for
   `H_g - rho(u) - c I = 0`.
3. Impose Jacobi identities and discard linearly dependent or purely scalar
   generators.
4. If factorization is requested, calculate both products `BA` and `AB` and the
   parameter-shift residual; do not infer shape invariance from one factorization.
5. Solve or eliminate exactly and retain the residual ideal/rank defect.

## Valid outputs

```text
Candidate(... certificates ...)
```

or

```text
NoCandidateWithinBudget(
  operator = H_g,
  ansatz = {...},
  unsatisfied_residuals = {...},
  zero_policy = exact over Q(g),
  conclusion = "this finite realization ansatz is rejected",
  reentry = "raise generator/coefficient degree, allow non-polynomial
             coefficients, change target tag, or weaken exact equality"
)
```

## Comparison case

Run the identical interface at `g=0`.  Recovery of the oscillator's ladder
structure is a regression check that the refusal at `g != 0` is not merely a broken
search.  The final report must separate what is special to `g=0` from what persists
for the family.

## Downstream meaning

A bounded refusal narrows the machine's advertised domain and may motivate a
different semantic target—perturbative effective variables, numerical spectral
measures, differential-Galois information, or an infinite/nonlinear algebra.  It
does not by itself select among those reconstructions.

The [Coulomb bench](coulomb-hidden-so4.md) demonstrates the preferred refusal
shape inside one declared module: a rotation-covariant degree-two vector exists
only if `(r^2V')'=0`.  That scalar obstruction is stronger and more readable than
an unsuccessful coordinate coefficient search, while still making no claim about
all possible higher-order symmetries.
