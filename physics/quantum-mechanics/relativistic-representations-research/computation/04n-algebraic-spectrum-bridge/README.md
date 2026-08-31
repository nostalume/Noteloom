# Bounded Runge--Lenz Search

Question: within the rotationally covariant classical ansatz

```text
A_g=p cross L+g(r)x,
```

which central potentials `V(r)` permit `dA_g/dt=0`?

The invariant vector calculation in N4n reduces conservation to

```text
g=-mu r V',
g'=mu V',

rV''+2V'=0.
```

For a power law `V=c r^alpha`, the obstruction is

```text
c alpha(alpha+1) r^(alpha-1).
```

Run:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/04n-algebraic-spectrum-bridge/check-runge-lenz-search.mjs
```

The regression checks powers `-4` through `4`, then evaluates Coulomb, oscillator
and Yukawa potentials at four radii. It must isolate `alpha=-1` as the only
nontrivial passing power and must reject the oscillator and Yukawa potentials in
this vector class.

Boundary: failure means only that no conserved vector exists in this declared
ansatz. The oscillator, for example, has a different hidden tensor algebra. The
script neither searches arbitrary operators nor proves nonintegrability.

## Heterogeneous reduction checks

The companion regression deliberately uses three incompatible mechanisms:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/04n-algebraic-spectrum-bridge/check-reduction-portfolio.mjs
```

- harmonic-oscillator factorization checks the coefficients and canonical
  normalization of the ladder construction for three choices of units;
- inverse-square dynamics checks the three classical conformal Poisson brackets
  at three phase-space points;
- quartic-oscillator computation optimizes a Gaussian Rayleigh quotient for
  `lambda=0.1,1,10`, including the exact `lambda=1` stationary width `alpha=2` and
  rigorous variational upper bound `0.8125`.

These cases do not form an algorithm-selection pipeline. They falsify the claim
that one algebra-search specification is the general route to computability.
