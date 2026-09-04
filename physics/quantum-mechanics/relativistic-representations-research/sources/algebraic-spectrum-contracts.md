# Algebraic Spectrum and Scattering Contracts

Recorded: 2026-08-29  
Used by: [field--mechanics boundary](../nodes/09-field-mechanics-reduction-boundary.md)

## AS-01 — Hydrogen dynamical symmetry

- **Source:** G. Jordan Maclay, [Dynamical Symmetries of the H Atom, One of the
  Most Important Tools of Modern Physics: SO(4) to SO(4,2), Background, Theory,
  and Use in Calculating Radiative Shifts](https://arxiv.org/abs/2305.18229).
- **Output consumed:** angular momentum and the Runge--Lenz operator generate the
  bound-state degeneracy algebra; larger non-invariance/spectrum-generating
  algebras organize bound and continuum states and calculational relations.
- **Boundary:** this is exceptional Coulomb structure. It does not imply that a
  generic central potential has a closed hidden algebra, nor that symmetry alone
  selects the Coulomb Hamiltonian.

## AS-02 — Algebraic scattering as an intertwiner

- **Source:** G. A. Kerimov and A. Ventura, [On algebraic models of relativistic
  scattering](https://arxiv.org/abs/0808.1156).
- **Output consumed:** when the interacting mass operator is tied to a Casimir of
  a noncompact dynamical group, the scattering matrix can be constructed from an
  intertwining relation between equivalent representations; the paper executes an
  `SO(3,1)` model.
- **Boundary:** the dynamical-group/Casimir relation and asymptotic representation
  are additional dynamics. A noncompact algebra by itself does not determine an
  `S` matrix for an arbitrary potential.

## AS-03 — Exact sector reduction

- **Sources:** M. Griesemer and D. Hasler, [On the Smooth Feshbach--Schur
  Map](https://arxiv.org/abs/0704.3244); Genevieve Dusson, Israel Sigal, and
  Benjamin Stamm, [The Feshbach--Schur map and perturbation
  theory](https://arxiv.org/abs/2105.02058).
- **Output consumed:** Schur/Feshbach reduction is isospectral under its
  hypotheses and converts a full spectral equation into an effective equation on
  a selected subspace; the latter source gives explicit eigenvalue/eigenfunction
  fixed-point estimates for discrete spectra.
- **Internal use:** node 09 derives the elementary block elimination directly on the
  same vector. The source contract supplies analytic hypotheses and the boundary
  of the formal inverse.
- **Boundary:** above an eliminated-sector threshold, boundary values and open
  channels replace an ordinary self-adjoint inverse; approximation and error
  control must then be reconstructed.

## AS-04 — Field-theoretic bound-state equation

- **Source:** Edit Matyus, David Ferenc, Peter Jeszenszki, and Adam Margocsy,
  [The Bethe--Salpeter QED wave equation for bound-state computations of atoms and
  molecules](https://arxiv.org/abs/2211.02389).
- **Output consumed:** relativistic atomic bound states can be formulated through
  Bethe--Salpeter/equal-time reductions of field-theoretic Green functions; this
  exposes rather than erases the additional kernel, relative-time, and
  approximation problems.
- **Boundary:** a Bethe--Salpeter equation is not automatically a computable
  spectrum. Kernel truncation, renormalization, gauge consistency, and error
  estimates remain obligations.

## AS-05 — Poles and continuum from one spectral field object

- **Source:** Gernot Eichmann et al., [Bound states from the spectral
  Bethe--Salpeter equation](https://arxiv.org/abs/2310.16353).
- **Output consumed:** a spectral Dyson--Schwinger/Bethe--Salpeter construction can
  compute a bound-state pole while retaining continuum spectral information; the
  paper demonstrates the method in three-dimensional scalar `phi^4` theory with
  declared truncations.
- **Boundary:** this is evidence for a common spectral backend, not a universal
  closed-form algorithm and not a proof for QED or arbitrary gauge theories.

## AS-06 — Hidden-integral discovery is model- and class-dependent

- **Sources:** Davide Batic, Marek Nowakowski, and Aya Mohammad Abdelhaq, [New
  vistas on the Laplace--Runge--Lenz vector](https://arxiv.org/abs/2305.04229);
  Primitivo Acosta-Humanez and David Blazquez-Sanz, [Non-integrability of some
  Hamiltonians with rational potentials](https://arxiv.org/abs/math-ph/0610010).
- **Output consumed:** explicit Runge--Lenz generalizations beyond the Coulomb
  problem require model-specific construction; rigorous absence results require a
  separately declared integrability class and obstruction method, such as the
  differential-Galois conditions used in the second source.
- **Research use:** node 09 treats hidden-algebra discovery as a bounded ansatz search
  with an explicit failure boundary. It does not infer global nonintegrability from
  failure of one vector ansatz.
- **Boundary:** neither source provides a universal decision procedure for all
  quantum differential operators or all nonlocal conserved quantities.

## AS-07 — Heterogeneous constructive mechanisms

- **Sources:** F. Nicacio, [Williamson theorem in classical, quantum, and
  statistical physics](https://arxiv.org/abs/2106.11965); Djamil Bouaziz and
  Michel Bawin, [Singular inverse-square potential: renormalization and
  self-adjoint extensions for medium to weak
  coupling](https://arxiv.org/abs/1402.5325); Przemyslaw Koscik and Anna
  Okopinska, [The optimized Rayleigh--Ritz scheme for determining the
  quantum-mechanical spectrum](https://arxiv.org/abs/1008.4606); Ana L. Retore,
  [Introduction to classical and quantum
  integrability](https://arxiv.org/abs/2109.14280).
- **Output consumed:** positive quadratic Hamiltonians admit symplectic normal
  forms; inverse-square spectral output depends on renormalization/self-adjoint
  extension despite formal scale structure; optimized Ritz spaces compute strongly
  anharmonic spectra; Lax and `R`-matrix constructions produce conserved charges
  within integrable model classes.
- **Research use:** node 09 uses these as four counterexamples to any mandatory
  hidden-algebra route, then internally constructs one minimal equality or bound
  for each mechanism.
- **Boundary:** the sources validate class-specific methods. They do not provide an
  automatic selector that chooses the best reduction for a new Hamiltonian.

## AS-08 — Boundary on any universal spectral framework

- **Source:** Toby S. Cubitt, David Perez-Garcia, and Michael M. Wolf,
  [Undecidability of the Spectral Gap](https://arxiv.org/abs/1502.04573).
- **Output consumed:** for a constructed class of translationally invariant,
  nearest-neighbour two-dimensional quantum spin systems, deciding gapped versus
  gapless is undecidable.
- **Research use:** node 09 therefore cannot claim an algorithm that discovers or
  selects a successful reduction for every Hamiltonian. It retains only an open
  graph language for auditing reductions that research actually constructs.
- **Boundary:** this theorem does not make the finite Dirac--Coulomb problem
  undecidable and does not prevent complete algorithms on restricted model
  classes. It limits the quantifier in the claimed framework.

## Supported boundary

The sources support a heterogeneous conclusion: hidden algebras can make
exceptional spectra algebraic, but discovering or excluding them is class- and
model-dependent; normal forms, variational bounds, domain analysis, Lax objects,
scattering intertwiners and Schur/Green-function reductions solve different
semantic obstructions. The universal claim that one of these is the framework for
every bound or scattering problem is rejected. Even gap detection is undecidable
on a broad local many-body class; only a problem-local reduction graph and its
semantic edge audits survive.
