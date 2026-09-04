# Curvature-detector source contracts

Consumed by: [observable/measure compiler](../nodes/16-observable-measure-compiler.md).

Status: primary-source boundary for node 16; its departure maps, spectral
densities, transfer, and same-measure observables are internally constructed

## CD-01 — A positive one-particle structure admits vacuum Fock realization

- **Source:** Igor Khavkine and Valter Moretti, [Algebraic QFT in Curved
  Spacetime and quasifree Hadamard states: an
  introduction](https://arxiv.org/abs/1412.5945), Proposition 11 and Theorem 2.1.
- **Input consumed:** the positive one-particle map already constructed in nodes 06 and 07.
- **Output consumed:** in the corresponding quasifree representation, a smeared
  linear field acting on the vacuum produces its one-particle image through the
  creation part.
- **Boundary:** the source treats the scalar theorem directly. node 16 uses the
  abstract Fock consequence only after the project has independently constructed
  the higher-spin positive source quotient. It does not obtain an interacting
  vacuum from this contract.

## CD-02 — Higher-spin curvature has derivative order `s`

- **Source:** Dario Francia and Augusto Sagnotti, [Free geometric equations for
  higher spins](https://arxiv.org/abs/hep-th/0207002).
- **Input consumed:** a symmetric massless spin-`s` potential on flat spacetime.
- **Output consumed:** the generalized curvature is an order-`s` differential
  operation. node 15 independently constructs the chiral operation and its gauge
  annihilator; node 16 consumes only its derivative degree and physical shell action.
- **Boundary:** the nonlocal geometric equations discussed in the source are not
  used, and the derivative count is not promoted to an interacting higher-spin
  detector theory.

## CD-03 — Derivative coupling changes detector response by frequency weights

- **Source:** T. Rick Perche and Matheus H. Zambianco, [Duality between amplitude
  and derivative coupled particle detectors in the limit of large energy
  gaps](https://arxiv.org/abs/2305.11949).
- **Input consumed:** a localized detector may couple to a derivative of a quantum
  field, and its transition probability is determined by the correspondingly
  differentiated two-point response.
- **Research use:** this delimits the model class. node 16 does not import the
  paper's large-gap duality; it derives its own `omega^(2s)` multiplier from the
  curvature action on a one-particle shell.
- **Boundary:** a scalar derivative detector is not evidence for a universal
  matter coupling to every higher-spin curvature. node 16's detector remains an
  effective probe even though its angular response is now generated from its
  supplied contraction.

## CD-03a — Covariant coherent states resolve the identity

- **Source:** Manu Mathur and H. S. Mani, [SU(N) Coherent
  States](https://arxiv.org/abs/quant-ph/0206005).
- **Input consumed:** a compact-group irreducible representation and the covariant
  orbit of a normalized rank-one state.
- **Output consumed:** the covariant coherent-state family admits a resolution of
  the identity.
- **Research use:** node 16 does not import its normalization. It constructs the
  spin-`s` sphere-projector average internally: covariance makes it an intertwiner,
  irreducibility makes it scalar, and trace fixes `4 pi/(2s+1)`.
- **Boundary:** the source's oscillator realization and general `SU(N)` machinery
  are not transferred to the curvature detector.

## CD-04 — Finite-time emission precedes a golden-rule limit

- **Source:** V. Debierre, T. Durt, A. Nicolet, and F. Zolla, [Spontaneous light
  emission by atomic Hydrogen: Fermi's golden rule without
  cheating](https://arxiv.org/abs/1502.06404).
- **Input consumed:** start from an excited preparation and its field coupling,
  calculate the finite-time transition probability, and only then compare its
  long-time coefficient with the golden-rule boundary.
- **Research use:** node 16 reuses node 11's internally derived finite-time kernel for its
  curvature-generated measure.
- **Boundary:** no hydrogen coupling, accuracy estimate, exponential decay,
  resonance, or scattering claim transfers to the effective higher-spin probe.

## Supported boundary

The contracts support the free Fock/vacuum bridge, the curvature derivative count,
and the distinction between finite-time probability and a boundary rate. They do
not select the detector gap, smearing, tensor response, or coupling normalization;
those remain explicit preparation inputs. They also do not turn a linear
higher-spin probe into a consistent interacting higher-spin matter theory.
