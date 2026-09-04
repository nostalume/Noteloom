# Effective-Mass Route Source Contracts

These contracts support [field--mechanics boundary](../nodes/09-field-mechanics-reduction-boundary.md).
They type the differentiable fiber branch, the full-space response formula, and
the analytic expansion used by the one-photon reduction.

## EM-01 — The atom--radiation fiber supplies the observable branch

- **Source:** Jürg Fröhlich, Marcel Griesemer, and Benjamin Schlein, [Rayleigh
  Scattering at Atoms with Dynamical
  Nuclei](https://arxiv.org/abs/math-ph/0509009), especially equations
  (43)--(58), Proposition 2, Corollary 6, and the velocity formula following
  equation (129).
- **Hypotheses consumed:** the model and cutoff assumptions NC-02 records; small
  coupling; energy below the ionization and velocity thresholds; and the
  modified soft-boson dispersion used to open a fiber gap.
- **Output consumed:**

  ```text
  H_g(P)=(P-P_f)^2/(2M)+H_at+H_f+g Phi(F_x),
  ```

  a simple dressed ground state on the stated momentum region, equality of the
  physical and modified ground energies, a positive gap for the modified fiber,
  and the first-derivative identity

  ```text
  grad E_g(P)=<psi_P,(P-P_f)/M psi_P>.
  ```

- **Research use:** node 09 constructs the effective-mass tensor from the curvature
  of this same branch and performs ordinary Feshbach differentiation only in the
  gapped modified/no-soft sector.
- **Boundary:** the source does not evaluate the second derivative or prove that
  the self-energy route is cheaper.

## EM-02 — Full-space curvature is a reduced-resolvent response

- **Source:** Fumio Hiroshima and K. R. Ito, [Mass Renormalization in
  Non-relativistic Quantum Electrodynamics with Spin
  1/2](https://arxiv.org/abs/math-ph/0412026), especially Sections 1.2 and 2.1,
  equations (2.32)--(2.35), and Corollary 2.15.
- **Hypotheses consumed:** an infrared- and ultraviolet-cutoff Pauli--Fierz
  fiber; a differentiable ground-state branch near zero momentum; the paper's
  small-coupling analyticity assumptions; and the reduced inverse on the
  orthogonal ground-state complement.
- **Output consumed:** effective mass as the inverse Hessian of the ground energy
  at zero momentum and the exact current--reduced-resolvent formula. Positivity
  of the reduced inverse shows mass enhancement in the paper's model.
- **Research use:** node 09 reconstructs the formula invariantly for the NC-02
  composite fiber instead of importing the paper's spin matrices or component
  expansion.
- **Boundary:** the paper studies a single dressed electron, not the neutral
  composite of node 09; its ultraviolet asymptotics are not transferred to that
  atom.

## EM-03 — Isolated analytic eigenbranches admit controlled differentiation

- **Source:** Tosio Kato, [Perturbation Theory for Linear
  Operators](https://link.springer.com/book/10.1007/978-3-642-66282-9),
  Chapter VII, together with EM-01's simple gapped modified fiber.
- **Hypotheses consumed:** a common operator domain and analytic family in the
  coupling/momentum parameters; a simple isolated eigenvalue separated by a
  positive gap.
- **Output consumed:** a local analytic eigenvalue/eigenprojection branch and a
  convergent perturbative expansion whose remainder is controlled on a smaller
  parameter neighborhood.
- **Research use:** node 09 expands the gapped scalar atom--radiation self-energy to
  second order in `g`, where field parity removes odd powers.
- **Boundary:** this theorem cannot be applied directly after the gap closes.
  Removing the infrared modification requires separate uniform estimates; a
  formal `g` expansion at a threshold is not licensed.

## Supported boundary

The contracts support exact curvature identities in the gapped fiber and a
leading weak-coupling reduction to an atomic resolvent integral. They do not
provide a numerical atom mass until `V`, the form factor, cutoffs, and units are
fixed, nor do they establish a cutoff-independent relativistic mass.
