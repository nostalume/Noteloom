# Field-Derived Coupling-Measure Source Contracts

These contracts support
[N9c](../nodes/09c-field-derived-coupling-measure.md). The numerical bench is
defined and derived inside N9c; the sources delimit which parts transfer to
atom--radiation fibers, effective-mass response, and open channels.

## FM-01 — Fixed-total-momentum field fibers and one-boson departure

- **Source:** Jürg Fröhlich, Marcel Griesemer, and Benjamin Schlein,
  [Rayleigh Scattering at Atoms with Dynamical
  Nuclei](https://arxiv.org/abs/math-ph/0509009), especially the fiber
  Hamiltonians in equations (43)--(58) and the dressed-atom construction.
- **Hypotheses consumed:** translation invariance, total-momentum fiber
  decomposition, ultraviolet-regular linear field coupling, a vacuum field
  preparation, and the gapped modified-dispersion regime when an isolated pole
  is differentiated.
- **Output consumed:** the structural fiber

  ```text
  H_g(P)=(P-P_f)^2/(2M)+H_at+H_f+g Phi(F_x)
  ```

  and the fact that one application of a linear field coupling to a vacuum
  preparation enters the one-boson sector.
- **Research use:** N9c removes the internal atom to form the smallest scalar
  regression that still retains recoil, a field continuum, and a genuine Fock
  Hamiltonian. Its Gaussian form factor and massive dispersion are declared
  benchmark choices, not claims copied from the source.
- **Boundary:** the paper's physical model is richer and includes the atomic
  internal space. N9c does not claim to compute its exact interacting spectral
  measure.

## FM-02 — Effective mass is a same-branch spectral response

- **Source:** Fumio Hiroshima and K. R. Ito, [Mass Renormalization in
  Non-relativistic Quantum Electrodynamics with Spin
  1/2](https://arxiv.org/abs/math-ph/0412026), especially Sections 1.2 and 2.1.
- **Hypotheses consumed:** a translation-invariant cutoff field fiber, an
  isolated differentiable ground branch near zero momentum, and a reduced
  resolvent on its complement.
- **Output consumed:** effective mass as the inverse curvature of the same
  ground-energy branch and its representation by a positive complementary
  resolvent response.
- **Research use:** N9c derives the scalar order-`g^2` curvature internally and
  checks that it is a weighted transform of the same radial departure measure.
- **Boundary:** spin matrices and the paper's ultraviolet asymptotics are not
  imported. A scalar energy measure determines the weight used by N9c only
  because its radial channel energy is injective.

## FM-03 — A field boundary needs channel dynamics before it is scattering

- **Source:** Christian Gérard, Jacob Schach Møller, and Morten Grud Rasmussen,
  [Asymptotic Completeness in Quantum Field Theory: Translation Invariant Nelson
  Type Models Restricted to the Vacuum and One-Particle
  Sectors](https://arxiv.org/abs/1503.02166).
- **Hypotheses consumed:** a massive boson field, translation-invariant
  Pauli--Fierz-type Hamiltonians, spectral localization below a multiparticle
  threshold, and wave-operator/channel hypotheses.
- **Output consumed:** vacuum and one-particle sectors are meaningful
  scattering objects only together with comparison dynamics and wave operators.
- **Research use:** N9c calls `2 pi m(E)` a continuum boundary loss or channel
  access density. It becomes a decay rate or cross-section ingredient only
  after a prepared energy and channel normalization are supplied.
- **Boundary:** N9c does not establish asymptotic completeness, a full
  scattering matrix, or a resonance pole.

## Supported boundary

The contracts support the chosen field-fiber structure, curvature observable,
and distinction between a resolvent boundary and a scattering theorem. The
actual density, transforms, moments, and regression numbers are internally
constructed. Exact finite-coupling spectral data would still require the
interacting complementary Fock dynamics; N9c controls only the first nonzero
order in `g`.
