# Carrier, source, and observable compiler

Status: presentation-dependent reductions are rejected unless the same visible
response is cheaper; radial visible-measure compilation is supported

## Obstruction

Removing components from a carrier does not necessarily reduce the complete
source-to-observable calculation. The compiler must retain a transformation that a
consumer can apply, compare equivalent presentations at the right level, and
refuse reductions that merely relocate work.

## Generate and test a projected carrier

For rank-`r` harmonic tensors, naive multiplication fails to preserve trace
freedom. Cancelling the computed trace constructs

```text
R_r=P-U A/(2r+d-2),
T R_r=0.
```

The denominator follows from solving the second equality. Trace freedom itself is
a requested presentation, not a consequence of the physical representation.

Constrained harmonic, compensated harmonic, and full symmetric complexes have the
same tested quotient dimension and transverse-screen rank. The assembly

```text
Phi=phi+U chi/(2s)
```

identifies compensated and compressed physical content. But restricted sources
must satisfy

```text
R^dagger j in im A^dagger,
```

while compensation requires `R^dagger j+A^dagger k=0`. A section `S` with `AS=1`
equates the source slices, yet its inverse momentum degree proves that this
equivalence is nonlocal. Direct constrained Green construction avoids the section
but requires a deeper rank-dependent solve. Neither presentation dominates on the
declared complete-cost metric.

## Factor the named observable

If a curvature or detector `K` obeys `KR=0`, every gauge-raised layer disappears.
Under the commuting-symbol contract both presentations reduce to

```text
K G_D J=G_Q KJ.
```

This is genuine observable compression and is presentation-neutral. Normalize the
composite once, cache it per admitted source, and expose the same response to every
detector transform.

## Generate the visible measure

Supply orbit measure, one-particle factor `b`, observable multiplier `k`, detector
contraction `d`, coupling, and an energy map `E(r)`. The departure weight is

```text
w(r)=orbit_density(r)|b(r)k(r)d(r)|^2.
```

For explicitly declared monotone branches `r_i(lambda)`, change of variables
constructs

```text
rho(lambda)=sum_i w(r_i(lambda))/|E'(r_i(lambda))|.
```

The Jacobian and threshold power are outputs, not supplied expectations. Missing
partitions for a nonmonotone energy map cause refusal. Massless spin-`s` curvature
in three spatial dimensions produces threshold power `2s+1`; a massive scalar
recoil transfers the same interface to a nonlinear square-root threshold.

The identical measure then feeds

```text
bound(z)=integral rho(lambda)/(z-lambda)dlambda,
open(t)=integral |(1-exp(-it(lambda-Delta)))/(lambda-Delta)|^2
                 rho(lambda)dlambda.
```

Values retain integration error, domain, approximation order, and one measure
identifier so a comparison cannot silently switch physical questions.

## Retained interface and boundary

```text
CompileVisibleResponse(carrier, source, observable, energy, branches)
 -> factored response + measure + bound/open transforms + cost/provenance
 | refusal(nonlocal adapter, no gain, missing branch, or divergent integral).
```

The current compiler filters supplied carrier candidates; it does not solve

```text
(physical fiber, capability, locality/resources)
 -> admissible carrier presentations.
```

Interacting measures, arbitrary anisotropic pushforwards, finite-coupling dressing,
and fermionic detector signs remain open. [Node 18](18-observable-return-calculus.md)
provides the common dynamical return consumed by the perturbative branch.
