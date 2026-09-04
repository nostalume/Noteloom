# Collective Response Contracts

Recorded: 2026-08-30  
Used by: [collective-response boundary](../nodes/10-collective-response-boundary.md)

This packet isolates the external analytic contracts for the first genuinely
collective branch. The node itself constructs the slow variable, response, and
recovery map from one conserved microscopic observable.

## CR-01 — Diffusion from conservation and linear response

- **Source:** Pavel Kovtun, [Lectures on hydrodynamic
  fluctuations in relativistic
  theories](https://arxiv.org/abs/1205.5040), especially Section 2.1.
- **Inputs consumed:** a homogeneous charge-neutral equilibrium state whose
  charge channel decouples from energy and momentum, one conserved density,
  finite static susceptibility `chi`, finite conductivity `sigma`, and the
  long-wavelength/low-frequency derivative expansion.
- **Output consumed:** the diffusion equation, `D=sigma/chi`, and the retarded
  density response with its hydrodynamic pole at `omega=-iDk^2`.
- **Internal use:** node 10 re-derives the response from continuity and the leading
  constitutive map, fixes its own source/sign convention, and checks the two
  noncommuting static and homogeneous limits.
- **Boundary:** hydrodynamics determines the response from `chi` and `sigma`; it
  does not compute those coefficients from a generic microscopic Hamiltonian or
  supply a universal remainder bound outside the derivative-expansion regime.
  At nonzero equilibrium density, charge generally mixes with energy and momentum
  and requires a coupled response matrix.

## CR-02 — Conserved modes, noise, and local KMS structure

- **Source:** Michael Crossley, Paolo Glorioso, and Hong Liu, [Effective field
  theory of dissipative
  fluids](https://arxiv.org/abs/1511.03646), especially the construction from
  long-lived modes associated with conserved quantities and the local-KMS
  constraint.
- **Inputs consumed:** a thermal state, Schwinger--Keldysh doubling, conserved
  slow variables, locality, and the stated KMS assumptions.
- **Output consumed:** a local effective description of dissipative response and
  fluctuations, with fluctuation relations constraining noise and transport.
- **Internal use:** node 10 uses this only to type the downstream stochastic/large-
  deviation continuation. The deterministic diffusion reduction does not depend
  on importing the full effective action.
- **Boundary:** local KMS and a derivative expansion are physical assumptions,
  not consequences of Poincare representation theory or of the free field
  equation.

## Supported boundary

The sources support

```text
microscopic conserved density in a thermal state
  -> long-wavelength response fixed by susceptibility and conductivity
  -> dissipative pole and, with extra KMS/noise data, fluctuating hydrodynamics.
```

They do not identify a diffusion pole with a vacuum Wigner particle, nor do they
make generic microscopic transport coefficients analytically cheap.
