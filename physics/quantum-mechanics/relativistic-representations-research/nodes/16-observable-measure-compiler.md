# Observable and visible-measure compiler

Status: generated in the radial one-particle class with explicit refusals

## Capability

Retain only the response visible to a supplied preparation and observable, then
derive both bound and open outputs from one constructed measure.

## Observable factorization

Input is a generated field response, preparation/source `J`, and observable `K`
with a certified annihilator relation `KR=0`. Normalize the composite before
building the full field:

```text
K G_D J -> G_Q K J.
```

All gauge-raised layers vanish by the same relation. The compiler caches this
factored response once per source and exposes it to every detector functional.

## Measure generation

Supply orbit measure, one-particle factor `b`, observable multiplier `k`, detector
contraction `d`, coupling, and monotone energy map `E(r)`. The radial departure
weight is constructed by multiplication:

```text
w(r) = orbit_density(r) |b(r) k(r) d(r)|^2.
```

For each monotone branch `r_i(lambda)` of `E`, pushforward gives

```text
rho(lambda)=sum_i w(r_i(lambda))/|E'(r_i(lambda))|.
```

The Jacobian follows from change of variables; it is not an expected threshold
exponent supplied to the compiler. Nonmonotone energy without an explicit branch
partition returns a refusal.

For a massless spin-`s` curvature in three spatial dimensions, radial shell power
`d-2` plus twice the generated curvature degree gives the threshold power `2s+1`.
Angular covariance and irreducibility construct the polarization coefficient from
the detector's chiral norm. The massive scalar recoil case transfers the same
interface to a nonlinear energy map with square-root threshold behavior.

## Bound and open transforms

From the identical measure identity, compute

```text
bound(z) = integral rho(lambda)/(z-lambda) dlambda,
open(t)  = integral |(1-exp(-it(lambda-Delta)))/(lambda-Delta)|^2
                    rho(lambda) dlambda.
```

Each numerical result returns value, estimated integration error, domain, and
approximation order. The same measure identifier certifies that comparison did not
switch physical questions.

## Retained interface

```text
CompileVisibleMeasure(orbit, factor, observable, preparation, energy, branches)
  -> measure + resolvent/Fourier/moment/open transforms + provenance
  | refusal(nonmonotone, inadmissible domain, missing branch, divergent integral)
```

## Output and boundary

This passes regression, inequivalent transfer, downstream use, and refusal inside
the declared radial free/effective class. It does not construct interactions,
finite-coupling dressed measures, CAR detector signs, arbitrary anisotropic
pushforwards, or a carrier presentation.
