# Field--mechanics reduction boundary

Status: supported problem-local reduction; universal spectral solver rejected

## Question

After a free field realization exists and dynamics is supplied, which object is
actually computable for bound, scattering, stable-particle, and composite regimes?

## Common reduction request

Fix `(H,P,O)`: Hamiltonian, prepared subspace, and observable. Let `Q=1-P`. The
departure map and projected resolvent are

```text
B=QHP,
Sigma(z)=P H Q (z-QHQ)^(-1) Q H P.
```

Whenever the resolvent exists, block elimination computes

```text
P(z-H)^(-1)P
  = (z-PHP-Sigma(z))^(-1).
```

This equality preserves the prepared response; it does not solve `QHQ` for free.
Reduction succeeds only when symmetry, sparsity, integrability, locality, or a
controlled approximation makes the right-hand construction cheaper.

## Why bound and scattering regimes separate

- A bound state is a discrete pole/eigenvector in a normalizable sector. Its
  energy is determined by a spectral zero or variational minimum; radial spectral
  work remains essential after angular/group reduction.
- A stable particle is an isolated dispersion shell of a field Hamiltonian.
- A resonance is a continued pole or decay feature, not a Hilbert eigenvector.
- Scattering compares asymptotic intertwiners between free and full evolution and
  needs open-channel boundary values.
- An infraparticle lacks an isolated one-particle pole; forcing a bound-state
  reduction changes the physical object.

## Problem-local mechanisms retained

The worktable preserves five witnesses as mechanisms, not a universal recipe:

1. Runge--Lenz closure constructs the Coulomb degeneracy only after a hard-to-find
   conserved operator is supplied or discovered by a bounded ansatz.
2. Dirac angular symmetry reduces carrier multiplicity before the radial problem;
   it does not remove the energy equation.
3. Relativistic mass-shell and sine--Gordon breather poles test stable/exact
   particle extraction.
4. Neutral composite and effective-mass calculations use a prepared projected
   resolvent.
5. A controlled nonintegrable deformation shows where exact algebraic closure
   ceases to transfer.

## Computability verdict

A valid reduction must compare

```text
discovery + construction + reduced solve + observable recovery + error
```

against the complete baseline route. Representation theory can expose blocks or
invariants; it cannot guarantee a useful hidden algebra for a general Hamiltonian.

## Output and edges

Output: the projected response as a common object and a refusal when its
construction cost is not reduced.

- [Visible spectral measure](11-visible-spectral-measure.md) compresses `B` and
  `QHQ` relative to the prepared observable.
- [Collective boundary](10-collective-response-boundary.md) applies the same
  projection and construction-cost discipline to collective generators.
- [Certified window](12-certified-observable-window.md) bounds approximate use.

## Boundary

No universal transformation discovery, analytic radial spectrum, complete dressed
Fock solution, or generic scattering matrix is claimed.
