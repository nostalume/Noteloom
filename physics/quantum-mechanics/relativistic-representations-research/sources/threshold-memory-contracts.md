# Threshold, Memory, and Friedrichs-Model Contracts

Recorded: 2026-08-30  
Used by: [visible spectral measure](../nodes/11-visible-spectral-measure.md)

node 11 derives the rank-one block elimination, coupling measure, pole residue,
boundary density, and explicit example internally. These contracts delimit the
operator-theoretic and scattering claims that are not reproved there.

## TM-01 — The Friedrichs model is a controlled discrete/continuum coupling

- **Primary sources:** K. O. Friedrichs, [On the Perturbation of Continuous
  Spectra](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160010404); Davide
  Lonigro, [The self-energy of Friedrichs-Lee models and its application to bound
  states and resonances](https://arxiv.org/abs/2109.02939).
- **Inputs consumed:** one discrete sector, an absolutely continuous sector, a
  coupling vector, and a self-adjoint block Hamiltonian under the stated domain
  hypotheses.
- **Output consumed:** the projected resolvent is governed by a self-energy built
  from the continuum spectral measure; real solutions outside the continuum give
  bound states, while continuation through the continuum boundary describes
  resonances.
- **Internal use:** node 11 chooses a bounded rank-one coupling and computes all scalar
  formulas directly. The papers supply the unbounded/self-adjoint model contract
  and the interpretation of continued self-energy poles.
- **Boundary:** this is a one-excitation, rank-one realization. It does not by
  itself construct a coupling spectral measure for a relativistic interacting
  field, handle multiparticle production, or include a nontrivial continuum
  background scattering matrix.

## TM-02 — Boundary values and resonance poles are different obligations

- **Primary source:** Lonigro,
  [arXiv:2109.02939](https://arxiv.org/abs/2109.02939).
- **Inputs consumed:** analytic self-energy off the continuum, suitable boundary
  values, and an analytic continuation through the continuous spectrum when a
  resonance pole is claimed.
- **Output consumed:** a bound pole is a real eigenvalue outside the continuum; a
  resonance is a pole/zero on a continued sheet, not merely a maximum of the real
  boundary density.
- **Internal use:** node 11 computes the exact continuum boundary density and a real
  on-shell center/width scale. It deliberately does not rename these data an
  exact resonance pole.
- **Boundary:** existence and uniqueness of a second-sheet pole require analytic
  continuation hypotheses beyond the real-axis calculation.

## TM-03 — Thresholds generate nonexponential long-time behavior

- **Primary source:** Savannah Garmon, Tomio Petrosky, Lena Simine, and Dvira
  Segal, [Amplification of non-Markovian decay due to bound state absorption into
  continuum](https://arxiv.org/abs/1204.6141).
- **Inputs consumed:** a lower continuum threshold, a spectral density with
  controlled near-threshold behavior, and survival dynamics coupled to that
  continuum.
- **Output consumed:** threshold branch structure produces inverse-power long-time
  behavior; absorption of a bound state at threshold can enhance the
  non-Markovian contribution.
- **Internal use:** node 11 derives its chosen `t^-2` memory exactly from the coupling
  density. This source supports the broader interpretation and warns against an
  exact exponential-decay claim.
- **Boundary:** the power and crossover depend on the actual threshold density and
  analytic structure. They are not universal constants.

## TM-04 — Boundary-ratio scattering needs a wave-operator contract

- **Sources:** Friedrichs,
  [original model](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160010404);
  Manuel Gadella and G. Pronko, [The Friedrichs Model and its use in resonance
  phenomena](https://arxiv.org/abs/1106.5782).
- **Inputs consumed:** the standard one-channel Friedrichs pair, existence and
  completeness of its wave operators, and incoming/outgoing boundary values of
  the scalar resolvent denominator.
- **Output consumed:** in the chosen convention the on-shell scattering factor is
  the ratio of the two boundary denominators and is unitary on the real continuum.
- **Internal use:** node 11 verifies the algebraic unit modulus of that ratio. Its
  identification as the physical scattering matrix is consumed from this
  contract.
- **Boundary:** multichannel models replace the scalar phase by an operator-valued
  scattering matrix; a background continuum interaction changes the formula.

## Supported boundary

The packet supports one controlled comparison:

```text
one coupling spectral measure
  -> analytic pole and residue below threshold
  -> boundary density and scattering phase above threshold
  -> time memory and threshold tail by Fourier transform.
```

It does not establish that a realistic field coupling measure is easy to obtain or
that the reduced dynamics is Markovian.
