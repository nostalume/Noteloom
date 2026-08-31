# Field/Particle Extraction Source Contracts

These contracts support [N4s](../nodes/04s-field-particle-extraction.md). They
type when a field theory contains Wigner particles, when local operators generate
their scattering states, and where a sharp-shell particle construction fails.

## FP-01 — Stable spectral subspace to asymptotic particle states

- **Source:** Detlev Buchholz and Wojciech Dybalski, [Scattering in relativistic
  quantum field theory: basic concepts, tools, and
  results](https://arxiv.org/abs/math-ph/0509047), Sections 1--3, especially
  equations (1.1)--(1.2), (2.1)--(2.7), and Theorems 1--2.
- **Hypotheses consumed:** a local relativistic field theory on a physical Hilbert
  space; positive-energy Poincare representation and invariant vacuum; a massive
  one-particle subspace carrying a sharp dispersion law; nonzero overlap with
  admissible interpolating operators; and the stated stability/regularity
  condition near the mass shell.
- **Output consumed:** time-smeared local operators converge on the vacuum to the
  one-particle projection; products with separated velocity supports construct
  incoming/outgoing Fock states; the resulting Moller maps are isometric and
  Poincare-intertwining. LSZ reduction extracts scattering amplitudes from the
  same on-shell asymptotic content.
- **Research use:** N4s constructs the one-particle quotient and its covariance
  internally. FP-01 supplies convergence, Fock inner products, and LSZ as theorem
  contracts.
- **Boundary:** asymptotic completeness is not generic. The unitary Poincare
  representation alone does not encode the interaction; its action on local
  operators and the incoming/outgoing embeddings do. The displayed review
  theorem is formulated for bosons; fermionic, braid-statistics, or nonlocally
  charged sectors require their corresponding graded/localized scattering
  theorem rather than an unmentioned change of Fock symmetry.

## FP-02 — Stable massive particles can survive a massless continuum

- **Source:** Wojciech Dybalski, [Haag--Ruelle scattering theory in presence of
  massless particles](https://arxiv.org/abs/hep-th/0412226), equations (2)--(8)
  and Theorem 1.1.
- **Output consumed:** under Herbst-type regularity, a sharp massive particle
  subspace can generate scattering states without an isolating mass gap. The
  paper names a neutral hydrogen atom in its ground state as a model physical
  situation: a sharp massive object immersed in massless photon spectrum.
- **Research use:** N4s distinguishes “isolated shell” from the weaker but still
  constructive “stable sharp shell plus regularity” condition. A composite bound
  object is not excluded merely because massless field excitations exist.
- **Boundary:** the regularity condition is additional dynamics, not a consequence
  of Poincare symmetry or of a pole guessed from perturbation theory.

## FP-03 — Long-range charged excitations require particle weights

- **Sources:** Martin Porrmann, [The Concept of Particle Weights in Local Quantum
  Field Theory](https://arxiv.org/abs/hep-th/0005057); Buchholz and Dybalski,
  [Scattering in relativistic quantum field theory](https://arxiv.org/abs/math-ph/0509047),
  Section 6, equations (6.1)--(6.5) and Theorem 5.
- **Output consumed:** temporal detector limits define positive weights on an
  ideal of localizing operators. Their zero-norm quotient and completion carry
  translations and decompose into improper sharp-momentum components. This
  includes infraparticle situations in which Gauss-law dressing prevents a
  normalizable sharp-mass Wigner subspace.
- **Research use:** N4s uses this as the alternative output type when the ordinary
  shell projection does not construct a normalizable charged one-particle space.
- **Boundary:** a complete general scattering theory of particle weights is not
  supplied. Inclusive observables may remain meaningful even when an ordinary
  `S` matrix does not.

## FP-04 — Particle extraction does not prove completeness

- **Source:** Buchholz and Dybalski, [Scattering in relativistic quantum field
  theory](https://arxiv.org/abs/math-ph/0509047), Section 7.
- **Output consumed:** constructing some stable one-particle and scattering
  sectors does not prove that every physical state is asymptotically composed of
  them. Superselection sectors and long-range forces obstruct the naive Fock
  picture; even in ordinary local theories, asymptotic completeness remains open
  in most models.
- **Research use:** N4s treats completeness, countable particle inventory, and
  recovery of total conserved quantities as downstream tests rather than hidden
  assumptions.

## Supported boundary

The contracts support a general *typed relation*, not a universal particle
solver. A stable Wigner particle requires a sharp spectral subspace plus
interpolating overlap and stability; its scattering states require asymptotic
limits. A bound composite enters by the same spectral construction. A resonance
without a real spectral subspace and a charged infraparticle are different output
types, not defective Wigner particles.
