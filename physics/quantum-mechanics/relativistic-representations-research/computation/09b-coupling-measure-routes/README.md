# N9b coupling-measure route regression

This standard-library computation asks what information survives when N9a's exact
coupling density is accessed through moments rather than directly.

Run from the repository root:

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/09b-coupling-measure-routes/multi_route_regression.py
```

The normalized density `lambda exp(-lambda)` has moments `(n+1)!`. Its orthogonal
polynomials are the generalized Laguerre family with parameter `1`, so multiplication
by energy has Jacobi coefficients

```text
b_n=2n+2,
a_(n+1)=sqrt[(n+1)(n+2)].
```

The two-site truncation is therefore

```text
J_2=[[2,sqrt(2)],[sqrt(2),4]].
```

Its spectral measure at the first site is the unique two-node Gaussian quadrature
matching moments through degree three. The script compares this same finite measure
with the exact real-time memory, Euclidean correlation, below-threshold resolvent,
and bound pole.

Acceptance checks verify that:

- moments `mu_0` through `mu_3` coincide to floating-point precision;
- the next moment differs, so no stronger exactness is implied;
- the finite chain cannot reproduce the continuum's long-time decay;
- its threshold self-energy shifts the bound pole substantially; and
- Euclidean data at positive time can hide a tiny high-energy atom that changes a
  high moment by more than a factor of fifty.

The result is a route discriminator, not a universal ranking. A finite moment chain
is useful for short-time or off-axis approximation, but threshold, scattering, and
long-time questions require information not contained in finitely many moments.
