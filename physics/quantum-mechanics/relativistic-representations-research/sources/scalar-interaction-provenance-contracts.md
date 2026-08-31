# Scalar Interaction-Provenance Source Contracts

These contracts support
[N9e](../nodes/09e-scalar-interaction-provenance.md). N9e constructs its shell
normalization, translation commutators, fiber unitary, preparation, and departure
measure internally. The sources delimit the model class and the claims that may
be transferred from it.

## SIP-01 — Mobile matter plus a quantized field fibers at total momentum

- **Source:** Jürg Fröhlich, Marcel Griesemer, and Benjamin Schlein,
  [Rayleigh Scattering at Atoms with Dynamical
  Nuclei](https://arxiv.org/abs/math-ph/0509009), especially equations (43)--(58).
- **Hypotheses consumed:** nonrelativistic mobile matter, a quantized radiation
  field, translation invariance, ultraviolet/infrared regularization, and fixed
  total momentum.
- **Output consumed:** the structural fact that total-momentum reduction turns
  the matter kinetic energy into a recoil term involving `p-P_f`, while a
  translated field coupling becomes independent of the center coordinate.
- **Internal replacement:** N9e proves the required commutator cancellation and
  unitary conjugations directly for its scalar two-level model.
- **Boundary:** the source studies a richer atomic model and scattering. N9e
  imports neither its electromagnetic interaction nor its completeness theorem.

## SIP-02 — Translation invariance is the reason for the fiber, not notation

- **Source:** Christian Gérard, Jacob Schach Møller, and Morten Grud Rasmussen,
  [Asymptotic Completeness in Quantum Field Theory: Translation Invariant Nelson
  Type Models Restricted to the Vacuum and One-Particle
  Sectors](https://arxiv.org/abs/1503.02166).
- **Hypotheses consumed:** a translation-invariant Nelson/Pauli--Fierz-type
  Hamiltonian and the conserved total momentum.
- **Output consumed:** such Hamiltonians are fibered with respect to total
  momentum; their spectral and scattering analysis is then performed on the
  fiber Hamiltonians.
- **Research use:** N9e constructs the relevant conserved generator before it
  writes `H_g(p)`. N9d's `p` is therefore the spectrum variable of `P_tot`, not
  an externally inserted parameter.
- **Boundary:** fiber decomposition alone supplies neither asymptotic fields nor
  scattering completeness.

## SIP-03 — Two-level linear field coupling is a genuine interacting field model

- **Source:** Jana Reker,
  [Existence of Resonances for the Spin-Boson-Model with Critical Coupling
  Function](https://arxiv.org/abs/1805.02263).
- **Hypotheses consumed:** a two-level system, bosonic Fock field, off-diagonal
  linear coupling, a controlled form factor, and small coupling for resonance
  analysis.
- **Output consumed:** the two-level/Fock Hamiltonian is an interacting field
  model, while promoting a perturbative boundary to a resonance requires
  additional complex-deformation, multiscale, and Feshbach--Schur work.
- **Research use:** N9e closes Hamiltonian provenance but leaves N9d's stop before
  resonance intact.
- **Boundary:** N9e uses a massive Gaussian shell amplitude and mobile recoil; it
  does not import the paper's massless critical coupling or resonance theorem.

## SIP-04 — Regular form factors support closed Hamiltonians

- **Source:** Davide Lonigro,
  [Self-adjointness of a Class of Multi-Spin--Boson Models with Ultraviolet
  Divergences](https://arxiv.org/abs/2301.10694).
- **Hypotheses consumed:** positive boson mass, a second-quantized free energy,
  spin--field coupling through form factors, and normalizable cutoff
  approximations.
- **Output consumed:** self-adjointness/domain control is a separate operator
  obligation and can be stable under normalizable ultraviolet cutoffs.
- **Internal replacement:** N9e uses the stronger regular Gaussian assumptions
  and records the elementary creation/annihilation energy estimates that make
  its interaction infinitesimally form-bounded.
- **Boundary:** the source permits singular rotating-wave form factors; N9e does
  not claim that generality.

## Supported boundary

The contracts support the translation-invariant mobile field model, total-momentum
fiber interpretation, two-level coupling class, and operator-domain obligation.
The exact source--shell normalization and recovery of N9d are internal
calculations. No source is used to claim that Poincare representation theory
selects the interaction profile, internal system, or coupling strength.
