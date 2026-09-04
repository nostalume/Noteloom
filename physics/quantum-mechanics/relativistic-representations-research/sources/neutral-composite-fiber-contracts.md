# Neutral Composite Fiber Source Contracts

These contracts support [field--mechanics boundary](../nodes/09-field-mechanics-reduction-boundary.md).
They separate the physical Pauli--Fierz ground-band theorem from the stronger
Rayleigh-scattering theorem proved for a simplified infrared-cutoff model.

## NC-01 — A neutral Pauli--Fierz atom has total-momentum fibers

- **Source:** Michael Loss, Tadahiro Miyao, and Herbert Spohn, [Lowest energy
  states in nonrelativistic QED: atoms and ions in
  motion](https://arxiv.org/abs/math-ph/0605005), especially equations
  (5)--(7), Theorems 2.3--2.5, and the hydrogen example following Proposition
  7.5.
- **Hypotheses consumed:** one nucleus and finitely many electrons coupled to
  the transverse quantized radiation field; ultraviolet cutoff; the stated
  potential, energy-inequality, binding, neutrality, and momentum conditions.
- **Output consumed:** the full Hamiltonian strongly commutes with total
  momentum and decomposes as `direct-integral H(P) dP`; for a neutral system no
  infrared cutoff is required in the ground-state theorem; under the stated
  binding and momentum bounds, `H(P)` has a ground state.
- **Research use:** node 09 obtains a physically meaningful dressed neutral-atom
  fiber branch without calling the internal Coulomb eigenvalue the full atom
  energy.
- **Boundary:** the theorem gives existence, not a simple eigenvalue, a smooth
  global dispersion, nonzero overlap with any chosen bare preparation, an
  explicit self-energy, or asymptotic completeness.

## NC-02 — Dressed-atom wave packets and the Rayleigh channel

- **Source:** Jürg Fröhlich, Marcel Griesemer, and Benjamin Schlein, [Rayleigh
  Scattering at Atoms with Dynamical
  Nuclei](https://arxiv.org/abs/math-ph/0509009), especially equations
  (5)--(21), (43)--(44), (130)--(132), and Theorems 8--9.
- **Hypotheses consumed:** a translation-invariant one-electron/one-nucleus
  model with nonrelativistic matter, scalar massless bosons, ultraviolet decay,
  a positive infrared interaction cutoff for the completeness theorem, small
  coupling, energy below ionization, the velocity bound, and the paper's
  hypotheses (H0)--(H2).
- **Output consumed:** fixed-total-momentum Hamiltonians `H_g(P)`; a simple
  dressed-atom ground state `psi_P` on the stated momentum region; the invariant
  wave-packet space

  ```text
  H_das={direct-integral f(P) psi_P dP};
  ```

  asymptotic photon fields; an isometric wave operator on the dressed-atom plus
  free-photon channel; and asymptotic completeness below the paper's restricted
  threshold.
- **Research use:** node 09 identifies the same dressed-atom vector as a fiber
  spectral state and as the zero-asymptotic-photon channel, then separates the
  stable atom from emitted photons without a trajectory calculation.
- **Boundary:** this is a simplified nonrelativistic model. Photon helicity is
  omitted, coupling is infrared-cut off in the completeness theorem, and the
  result supplies translations and time evolution but no Lorentz boosts or
  Wigner mass hyperboloid.

## NC-03 — Prepared spectral weight survives a massless threshold

- **Sources:** NC-01 and NC-02, together with
  [node 09's operator contract](field-mechanics-variation-contracts.md).
- **Output consumed:** the neutral dressed ground state can exist at the bottom
  of a massless continuum. Consequently, `E(P)-QH(P)Q` need not be invertible
  even when `E(P)` is a fiber eigenvalue.
- **Research use:** node 09 uses the spectral atom

  ```text
  s-lim_(epsilon down to 0)
    i epsilon J_P^dagger(E(P)+i epsilon-H(P))^(-1)J_P
  =J_P^dagger P_b(P)J_P
  ```

  as the threshold-safe mechanical datum. If the eigenvalue is isolated, this
  atom is also the resolvent residue. The pointwise recovery map `K_P(E(P))` is
  retained only when an actual spectral gap or a stronger threshold Feshbach
  theorem has been supplied.
- **Boundary:** a threshold eigenvalue need not produce a meromorphic resolvent
  pole on a punctured neighborhood. Calling the prepared spectral atom a residue
  without isolation would be incorrect.

## Supported boundary

The sources support a nonrelativistic dressed-composite band and, in the
simplified model, its Rayleigh asymptotic channel. They do not support the claim
that this band is already a relativistic composite particle or that a local
vacuum-sector field creates the atom. Those are the two exact obligations passed
back to node 09.
