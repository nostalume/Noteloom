# N8b SSEP Current Computation

This computation evaluates the scalar objects constructed in N8b. It does not
simulate the exclusion process or discretize the MFT optimal path.

## Question

For equilibrium density `rho`, do the integral and convergent-series forms of
the exact scaled cumulant-generating function agree, is its derivative monotone,
and does the scalar Legendre optimizer recover the requested current with a small
stationarity residual?

## Inputs and conventions

- unit SSEP bond rate;
- annealed Bernoulli equilibrium;
- default `rho=1/2`;
- `mu(lambda)=F(2rho(1-rho)[cosh(lambda)-1])`;
- nonnegative rate `Phi(q)=sup_lambda[lambda q-mu(lambda)]`;
- standard-library Python only; deterministic computation, no random seed.

The improper integrals are truncated at `k=8`. Their omitted Gaussian tails are
far below the requested accuracy for the displayed input range. Composite
Simpson quadrature with `4096` panels supplies the integral values; bisection
solves the monotone stationarity equation.

## Run

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/08b-ssep-current/ssep_current.py
```

The script reports:

1. analytic scaled second and fourth cumulants and independent centered finite-
   difference checks;
2. integral-versus-series agreement where the series is convergent;
3. `2048`-versus-`4096`-panel stability at moderate and large tilt;
4. monotonicity of `mu'` on a nonnegative grid;
5. `lambda(q)`, `Phi(q)`, the stationarity residual, and the Gaussian-center
   comparison for representative currents.

## Acceptance criteria

- integral/series discrepancy below `10^-10` on the test points;
- quadrature refinement discrepancy below `10^-10` on the test points;
- finite-difference cumulant discrepancies below `5*10^-6` at step `0.05`;
- no decrease of `mu'` larger than `10^-10` on the grid;
- Legendre stationarity residual below `10^-9` for every displayed `q`;
- `Phi(0)=0` and all displayed rates nonnegative.

## Failure boundary

The script verifies numerical evaluation of the already-bound exact formula. It
does not prove SR-03, certify a generic MFT solver, test quenched initial data, or
establish finite-time error bounds. Large-current evaluation is stable through
the positive integral representation, whereas the alternating power series is
used only at small `omega`.
