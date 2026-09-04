# SSEP Response and Fluctuation Contracts

Recorded: 2026-08-30  
Used by: [collective-response boundary](../nodes/10-collective-response-boundary.md)
and [collective-response boundary](../nodes/10-collective-response-boundary.md)

This packet binds the microscopic model and macroscopic fluctuation statements
needed for the first evaluated collective response. The linear response,
transport coefficients, lattice symbol, continuum error, and equilibrium rate
function are reconstructed inside node 10.

## SR-01 — Microscopic exclusion and macroscopic fluctuation theory

- **Source:** Lorenzo Bertini, Alberto De Sole, Davide Gabrielli, Giovanni
  Jona-Lasinio, and Claudio Landim, [Macroscopic fluctuation
  theory](https://arxiv.org/abs/1404.6466), especially Sections II.1--II.2,
  V.4, and VIII.1, VIII.7--VIII.9.
- **Inputs consumed:** a Markovian conservative lattice gas, diffusive scaling,
  local equilibrium, one density/current pair, and an external thermodynamic
  field.
- **Output consumed:** continuity plus a diffusive constitutive current; the
  mobility-weighted trajectory large-deviation functional; and the microscopic-
  to-hydrodynamic theorem boundary for exclusion processes.
- **Internal use:** node 10 computes the SSEP density generator and response exactly
  before using the source to type the full trajectory large-deviation
  continuation.
- **Boundary:** macroscopic fluctuation theory is a scaling theorem/description,
  not an exact finite-lattice identity for arbitrary trajectory probabilities.
  Its hypotheses must not be transferred automatically to Hamiltonian quantum
  systems.

## SR-02 — Exact SSEP mobility and time-dependent fluctuation regression

- **Source:** Kirone Mallick, Hiroki Moriya, and Tomohiro Sasamoto, [Exact
  solution of the macroscopic fluctuation theory for the symmetric exclusion
  process](https://arxiv.org/abs/2202.05213), especially equations (4)--(7) and
  the microscopic definition preceding them.
- **Inputs consumed:** the one-dimensional nearest-neighbor symmetric exclusion
  process and Bernoulli initial data.
- **Output consumed:** diffusion coefficient `D=1`, MFT noise mobility
  `sigma_MFT(rho)=2rho(1-rho)`, the Bernoulli free-energy functional, and an
  exact time-dependent current-fluctuation check against microscopic results.
- **Internal use:** node 10 distinguishes this noise mobility from node 10's linear
  conductivity, which differs by the conventional factor two, and uses the
  Bernoulli input to reconstruct susceptibility and the static rate function.
  node 10 binds the paper's optimized current function to the same microscopic
  current evaluated by SR-03.
- **Boundary:** the paper solves a particular time-dependent MFT current problem
  by an integrable transformation. The nodes use its theorem output without
  reproducing that heavy inverse-scattering calculation and do not claim that
  arbitrary diffusive models are integrable.

## SR-03 — Exact integrated-current generating function

- **Source:** Bernard Derrida and Antoine Gerschenfeld, [Current Fluctuations of
  the One Dimensional Symmetric Simple Exclusion Process with a Step Initial
  Condition](https://arxiv.org/abs/0902.2364), especially equations (1)--(5),
  (10), and (14)--(16).
- **Inputs consumed:** SSEP on the infinite one-dimensional lattice; independent
  Bernoulli occupations of density `rho_a` on the left and `rho_b` on the
  right; and the signed integrated current `Q_T` through the origin.
- **Output consumed:** the exact annealed large-time scaled cumulant-generating
  function

  ```text
  log E[exp(lambda Q_T)]
    =sqrt(T) F(omega)+o(sqrt(T)),

  F(omega)
    =(1/sqrt(pi)) sum_(n>=1) (-1)^(n+1) omega^n/n^(3/2),

  omega
    =rho_a(exp(lambda)-1)
     +rho_b(exp(-lambda)-1)
     +rho_a rho_b(exp(lambda)-1)(exp(-lambda)-1),
  ```

  together with the equilibrium second and fourth cumulants and the current
  large-deviation tail.
- **Internal use:** node 10 specializes both input densities to the same `rho`,
  derives the reduced scalar `omega_rho(lambda)`, reconstructs the cumulants,
  and performs the one-dimensional Legendre computation. The exact microscopic
  determinant/Bethe-ansatz derivation remains attached to this source contract.
- **Boundary:** the theorem concerns annealed Bernoulli initial data on the
  infinite line and the `Q_T=O(sqrt(T))` rare-current scale. It is not a
  finite-ring long-time current theorem, a quenched-initial-data theorem, or a
  universal consequence of diffusion alone.

SR-02 independently recovers this same current generating function from the
time-dependent SSEP macroscopic fluctuation equations. node 10 uses that agreement as
a same-observable microscopic/macroscopic witness, not as permission to transfer
SSEP integrability to a generic diffusive theory.

## Supported boundary

The sources support

```text
microscopic SSEP
  -> deterministic diffusion with D=1
  -> noise mobility 2rho(1-rho)
  -> trajectory large deviations in the diffusive scaling limit
  -> one exact equilibrium integrated-current rate function.
```

They do not turn SSEP into a unitary quantum field theory. Its role is an exact
interacting stochastic benchmark for the collective-response construction.
