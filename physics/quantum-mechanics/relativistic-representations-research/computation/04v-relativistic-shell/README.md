# Relativistic Mass-Shell Regression

Question: do the bounded coordinate representatives agree with N4v's invariant
construction of a massive shell, its curvature, and its low-momentum recovery?

Run:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/04v-relativistic-shell/check-mass-shell-coincidence.mjs
```

The script deterministically checks:

1. a rapidity boost sends `(M,0)` to
   `(sqrt(M^2+|P|^2),P)` and preserves the Minkowski norm;
2. a five-point second derivative of the shell energy at rest agrees with
   `1/M`;
3. the exact identity

   ```text
   E(P)-M-|P|^2/(2M)
    =-|P|^4/[2M(E(P)+M)^2]
   ```

   has zero residual and obeys the quartic error bound.

This is a finite coordinate regression, not the derivation and not an
interacting mass calculation. The promoted output is only consistency of the
representatives used by N4v.
