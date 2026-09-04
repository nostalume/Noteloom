# Certified Observable-Window Source Contracts

These contracts support
[certified observable window](../nodes/12-certified-observable-window.md). node 12 derives its combined
parity quotient, form constants, scalar error formula, finite-sector norms, and
numerical window internally.

## COW-01 — Feshbach reduction supports explicit discrete-spectrum bounds

- **Source:** Geneviève Dusson, Israel Michael Sigal, and Benjamin Stamm,
  [The Feshbach--Schur Map and Perturbation
  Theory](https://arxiv.org/abs/2105.02058).
- **Hypotheses consumed:** a self-adjoint reference operator, an isolated
  discrete eigenvalue, a complementary gap, and a perturbation controlled
  relative to the reference form.
- **Output consumed:** the Feshbach--Schur map is a fixed-point construction for
  the perturbed eigenvalue/eigenvector and supports explicit eigenvalue and
  eigenvector estimates.
- **Internal replacement:** node 12 computes the one-dimensional Schur equation,
  inverse identity, and constants directly for the scalar model rather than
  importing the paper's estimates.
- **Boundary:** the theorem concerns isolated spectrum. It does not control the
  embedded excited preparation or its long-time decay.

## COW-02 — Linear small-system/field Hamiltonians require operator domains

- **Source:** Jacob Schach Møller,
  [Fully Coupled Pauli--Fierz Systems at Zero and Positive
  Temperature](https://arxiv.org/abs/1210.7500).
- **Hypotheses consumed:** a finite-dimensional small system, scalar bosonic
  Fock field, linear field coupling, and the standard field-operator domain
  conditions.
- **Output consumed:** the Hamiltonian and its unitary dynamics are legitimate
  operator-theoretic objects once the form-factor hypotheses are imposed.
- **Internal replacement:** node 11 supplies self-adjointness for the massive
  Gaussian model; node 12 acts only on its finite-particle analytic core when it
  iterates Duhamel and then uses unitarity for the unexpanded left factor.
- **Boundary:** node 12 does not transfer arbitrary-coupling spectral conclusions or
  positive-temperature Liouvillean results.

## COW-03 — A perturbative boundary is not a resonance theorem

- **Source:** Jana Reker,
  [Existence of Resonances for the Spin-Boson Model with Critical Coupling
  Function](https://arxiv.org/abs/1805.02263).
- **Hypotheses consumed:** two-level/Fock coupling and the distinction between a
  perturbative decay scale and a constructed resonance.
- **Output consumed:** a finite-coupling resonance needs additional spectral
  deformation, multiscale estimates, and Feshbach--Schur analysis.
- **Research use:** node 12 interprets failure of its long-time norm certificate as
  a re-entry condition for such a new construction, not as permission to
  exponentiate node 11's boundary rate.
- **Boundary:** node 12 is massive and finite-time; it imports neither the critical
  massless form factor nor the resonance result.

## Supported boundary

The packet supports the operator setting, discrete-state Feshbach interpretation,
and stop before resonance. All observable equalities and remainder formulas are
internal. The numerical crossings are regressions of those formulas, not
literature claims or independently interval-certified constants.
