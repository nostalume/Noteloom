# Effective-Mass Route Regression

Question: do direct eigenbranch differentiation and scalar Feshbach
self-energy differentiation return the same curvature on one prepared branch?

The finite model is

```text
H(t)=
  [ h+t^2/(2M)   b                  0             ]
  [ b              a+t^2/(2M)       w t           ]
  [ 0              w t              c+t^2/(2M)   ].
```

The first basis vector is the prepared mechanical sector. The second is an even
eliminated state coupled to it, and the third is an odd eliminated state. The
involution `diag(1,1,-1)` sends `H(t)` to `H(-t)`, so the selected eigenbranch
has zero first derivative at the origin. This is a finite spectral regression,
not an atom or photon truncation presented as physical data.

Run:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/04u-effective-mass/check-effective-mass-routes.mjs
```

The check compares:

1. the reduced-resolvent Hessian of the full matrix;
2. the second derivative of the lowest eigenvalue by a five-point stencil;
3. the scalar Feshbach tangent-solve formula.

It also verifies the Feshbach secular equation and recovered eigenvector. Every
comparison must agree within its declared tolerance. The promoted result is only
the equality of routes and their solve structure; the numerical curvature is not
a prediction for the Pauli--Fierz model.
