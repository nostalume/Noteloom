# Source Inventory: Relativistic Representations

Recorded: 2026-08-28. Search results are discovery aids; claims below are bound to
the linked primary paper or authoritative research notes.

Active quantization bindings are recorded in
[quantization and one-particle recovery contracts](sources/quantization-recovery-contracts.md):
CCR/CAR construction for linear gauge systems, quasifree/Fock one-particle
recovery, the locally covariant Dirac regression, and the interacting asymptotic
boundary.

## Primary worktable

### Current manuscript

- Material: `physics/quantum-mechanics/relativistic-representations.typ`
- Revision: repository `44e5324`; 1,499 lines; compiles with Typst 0.15.1.
- Role: developing manuscript and source of present conjectures/calculations.
- Reliability: mixed. It contains useful derivation fragments but also unnamed
  structure, convention drift, unproved general claims, and known suspect formulas.
- Main route: scalar functions on the Poincare group, left/right actions, spin
  coordinates, invariant operators, dimension-specific representations, and
  extraction of finite-component equations.

## Bound external sources

### Foundational representation bridges

- M. H. Stone, [On One-Parameter Unitary Groups in Hilbert
  Space](https://doi.org/10.2307/1968538), _Annals of Mathematics_ 33 (1932),
  643--648. Primary source for the strongly-continuous unitary group/self-adjoint
  generator bridge used in `N2`.
- V. Bargmann, [On Unitary Ray Representations of Continuous
  Groups](https://doi.org/10.2307/1969831), _Annals of Mathematics_ 59 (1954),
  1--46. Primary source for projective unitary group actions and their covering
  representations.
- G. W. Mackey, [Imprimitivity for Representations of Locally Compact Groups
  I](https://doi.org/10.1073/pnas.35.9.537), _PNAS_ 35 (1949), 537--545. Primary
  source for the converse bridge between covariant spectral projections on an orbit
  and representations induced from its stabilizer.

These sources validate theorem contracts. The active node still states the input,
output, and semantic reason for each bridge instead of citing the theorem name as a
derivation.

### Gitman and Shelepin: fields on the Poincare group

- D. M. Gitman and A. L. Shelepin, [Fields on the Poincare group: arbitrary spin
  description and relativistic wave equations](https://arxiv.org/abs/hep-th/0003146),
  2000; published in _International Journal of Theoretical Physics_ 40 (2001).
- Authority: primary source and direct source of the manuscript's current route.
- Relevant output: treats scalar functions on the Poincare group as generating
  functions for spin-tensor fields; develops 2D, 3D, and 4D cases; defines discrete
  transformations as group automorphisms; compares finite-dimensional nonunitary
  and infinite-dimensional unitary Lorentz representations.
- Research caution: equivalence claims are explicitly free-field claims; the paper
  notes that interaction can distinguish systems because covariant derivatives do
  not commute.
- Concrete extraction: [gitman-shelepin-2000.md](sources/gitman-shelepin-2000.md).

### Gitman and Shelepin: analytic status of group functions

- D. M. Gitman and A. L. Shelepin, [Field on Poincare group and quantum
  description of orientable objects](https://arxiv.org/html/0901.2537), 2009.
- Authority: primary follow-up source.
- Relevant output: explicitly separates the unitary regular space `L2(G)` from
  finite nonunitary polynomial spin sectors, and gives the generalized left/right
  action and coefficient expansion.
- Research use: decisive typing evidence for `N2` and bridge correction in `N3`.
- Concrete extraction: [gitman-shelepin-2009.md](sources/gitman-shelepin-2009.md).

### Wigner: unitary particle representations

- Eugene Wigner, [On unitary representations of the inhomogeneous Lorentz
  group](https://doi.org/10.2307/1968551), _Annals of Mathematics_ 40 (1939).
- Authority: foundational primary paper.
- Relevant output: classification problem for unitary irreducible representations
  of the inhomogeneous Lorentz/Poincare group.
- Research use: state-space side of the bridge; do not silently identify this
  unitary representation with a finite-dimensional Lorentz field representation.

### Bargmann and Wigner: covariant wave equations

- Valentine Bargmann and Eugene Wigner, [Group theoretical discussion of
  relativistic wave equations](https://doi.org/10.1073/pnas.34.5.211), _PNAS_ 34
  (1948), 211--223.
- Authority: foundational primary paper.
- Research use: covariant realization of definite-spin representations and a
  comparison point for the universal finite-spin family in `N4` and conventional
  carrier comparisons in `N5`.

### Bekaert and Boulanger: modern representation classification

- Xavier Bekaert and Nicolas Boulanger, [The unitary representations of the
  Poincare group in any spacetime dimension](https://arxiv.org/abs/hep-th/0611263),
  v2 revised 2021.
- Authority: authoritative research lecture notes.
- Relevant output: induced representations reduce Poincare classification to
  stability subgroups; distinguishes massive, massless helicity, infinite-spin,
  and tachyonic sectors; gives covariant equations for nonnegative mass squared.
- Research use: modern baseline for `N1`, `N2`, the arbitrary finite-label boundary
  in `N4`, and the tower boundary in `N6`.

### Weinberg: Lorentz-covariant free fields

- Steven Weinberg, [Feynman Rules for Any Spin III](https://doi.org/10.1103/PhysRev.181.1893),
  _Physical Review_ 181 (1969), 1893.
- Authority: primary paper.
- Relevant output: constructs free fields in general irreducible homogeneous
  Lorentz representations and calculates propagators.
- Research use: conventional covariant-field side of `N2` and `N3`.

### Weinberg: massless particle-to-field restriction

- Steven Weinberg, [Feynman Rules for Any Spin II: Massless
  Particles](https://doi.org/10.1103/PhysRev.134.B882), _Physical Review_ 134
  (1964), B882.
- Authority: primary paper.
- Relevant output: relates massless particle helicity to allowed Lorentz field
  types and exposes the special status of potential representations through the
  non-semisimple massless little group.
- Research use: determination boundary in `N1`, massless bridge test in `N3`, and
  external comparison for the chiral helicity family in `N4`.

### Weinberg: invariant massless little-group subgroup

- Steven Weinberg, [Massless Particles in Higher
  Dimensions](https://arxiv.org/abs/2010.05823), 2020.
- Authority: primary research paper extending the author's four-dimensional
  particle-to-field restriction.
- Relevant output: a Lorentz field can create a finite-helicity state only through
  a little-group sector on which the invariant Abelian subgroup acts trivially.
- Research use: external theorem boundary for the direct null-helicity line and
  gauge-subquotient distinction in `N2b/N3`; the active nodes construct the
  null line and unipotent invariants intrinsically.
- Active extraction: [Lorentz-carrier theorem contracts](sources/lorentz-carrier-contracts.md).

### Higher-spin modern comparison

- Rakibur Rahman and Massimo Taronna, [From Higher Spins to Strings: A
  Primer](https://arxiv.org/abs/1512.07932), 2015.
- Authority: research review/primer by subject specialists.
- Relevant output: Wigner classification, covariant massive and massless equations,
  Lagrangian formulation, and unfolded reformulation.
- Research use: downstream lens for `N6`; it must not determine the elementary
  construction before low-spin examples are understood.

### Algebraic gauge realization of massless modules

- K. B. Alkalaev, M. Grigoriev, and I. Yu. Tipunin, [Massless Poincare modules and
  gauge invariant equations](https://arxiv.org/abs/0811.3999), 2008.
- Authority: primary research paper.
- Relevant output: starts from massless Poincare modules, constructs gauge-field
  equations, relates gauge-inequivalent solutions to the starting module through
  cohomological machinery, and checks the Wigner little-group content.
- Research use: modern comparison for `N4`, especially the distinction between a
  physical module and a gauge presentation that realizes it.
- Research caution: its BRST/parent treatment and mixed-symmetry scope do not prove
  the simpler finite polynomial-symbol criterion reconstructed in this project.
- Active extraction: [polynomial gauge-resolution contracts](sources/polynomial-gauge-contracts.md).

### Fang and Fronsdal: half-integer gauge potentials

- J. Fang and C. Fronsdal,
  [Massless fields with half-integral spin](https://doi.org/10.1103/PhysRevD.18.3630),
  _Physical Review D_ 18 (1978), 3630--3633.
- Authority: foundational primary paper.
- Relevant output: symmetric rank-`n` spinor-tensor potentials, triple gamma-trace
  field constraint, gamma-traceless gauge parameter, and the finite
  half-integer-spin family.
- Research use: external boundary for N4b; N4b internally reconstructs the
  polynomial complex and physical little-group quotient.
- Active extraction: [polynomial gauge-resolution contracts](sources/polynomial-gauge-contracts.md),
  contract `PG-04`.

### Constrained and unconstrained action principles

- C. Fronsdal,
  [Massless fields with integer spin](https://doi.org/10.1103/PhysRevD.18.3624),
  _Physical Review D_ 18 (1978), 3624--3629.
- D. Francia and A. Sagnotti,
  [Minimal Local Lagrangians for Higher-Spin Geometry](https://arxiv.org/abs/hep-th/0507144),
  _Physics Letters B_ 624 (2005), 93--104.
- D. Francia, J. Mourad, and A. Sagnotti,
  [Current Exchanges and Unconstrained Higher Spins](https://arxiv.org/abs/hep-th/0701163).
- Authority: primary research papers.
- Relevant output: constrained Fronsdal actions, the auxiliary-field cost of
  removing trace constraints while retaining locality, and the role of Bianchi
  identities and source exchange in distinguishing vacuum-equivalent equations.
- Research use: source boundary for N4c; N4c reconstructs the constrained Bianchi
  identities internally and records the remaining adjoint/equivalence obligations.
- Active extraction: [action-principle contracts](sources/action-principle-contracts.md).

### Green-hyperbolic and Maxwell observable contracts

- Christian Baer, [Green-hyperbolic operators on globally hyperbolic
  spacetimes](https://arxiv.org/abs/1310.0738), *Communications in Mathematical
  Physics* 333 (2015), 1585--1615.
- Marco Benini, [Relative Cauchy evolution for the vector potential on globally
  hyperbolic spacetimes](https://doi.org/10.2140/memocs.2015.3.177), *Mathematics
  and Mechanics of Complex Systems* 3 (2015), 177--226.
- Marco Benini, [Optimal space of linear classical observables for Maxwell
  `k`-forms via spacelike and timelike compact de Rham
  cohomologies](https://arxiv.org/abs/1401.7563), 2014.
- Authority: primary mathematical-physics research and a general analytic theorem
  source.
- Relevant output: retarded/advanced Green operators with causal support, the
  exact sequence of the causal propagator, the Maxwell Lorenz-gauge completion,
  the conserved-source quotient, and its support/topology boundary.
- Research use: analytic theorem contracts for N4e. N4e reconstructs the
  commutation, response, gauge-independence, and null-shell coincidence internally.
- Active extraction: [Maxwell Green contracts](sources/maxwell-green-contracts.md).

### Linearized-gravity and finite-spin Green contracts

- Christopher J. Fewster and David S. Hunt, [Quantization of linearized gravity in
  cosmological vacuum spacetimes](https://arxiv.org/abs/1203.0261), *Reviews in
  Mathematical Physics* 25 (2013), 1330003.
- Thomas-Paul Hack and Alexander Schenkel, [Linear bosonic and fermionic quantum
  gauge theories on curved spacetimes](https://arxiv.org/abs/1205.3484), *General
  Relativity and Gravitation* 45 (2013), 877--910.
- Authority: primary mathematical-physics research.
- Relevant output: normally hyperbolic de Donder completion, causal Green maps for
  linearized gravity, and the abstract source-to-solution construction for linear
  gauge theories.
- Research use: independent spin-two and analytic boundaries for N4f. The uniform
  flat-space identities for every finite integer spin are proved internally from
  N4a/N4c rather than attributed to these sources.
- Active extraction: [finite-spin Green contracts](sources/finite-spin-green-contracts.md).

### Half-integer action and Green completion

- J. Fang and C. Fronsdal, [Massless fields with half-integral
  spin](https://doi.org/10.1103/PhysRevD.18.3630), _Physical Review D_ 18 (1978),
  3630--3633.
- I. L. Buchbinder, V. A. Krykhtin, and A. Pashnev, [BRST approach to Lagrangian
  construction for fermionic massless higher spin
  fields](https://arxiv.org/abs/hep-th/0410215), _Nuclear Physics B_ 711 (2005),
  367--391.
- Thomas-Paul Hack and Alexander Schenkel, [Linear bosonic and fermionic quantum
  gauge theories on curved spacetimes](https://arxiv.org/abs/1205.3484), *General
  Relativity and Gravitation* 45 (2013), 877--910.
- Authority: primary higher-spin and mathematical-physics research.
- Relevant output: the constrained Fang--Fronsdal action exists at every finite
  half-integer rank; an unconstrained BRST formulation reduces to it after partial
  gauge fixing in four dimensions; the spin-`3/2` gauge system admits a
  trace-redefined Dirac-type Green completion.
- Research use: N4i internally constructs the all-rank Dirac--Fischer pairing,
  formal-adjoint identity, wave reduction, and admissible retarded/advanced
  response. N4j then reconstructs the compact-source/spacelike-compact-solution
  quotient proof from those identities and wave Green exactness. Hack--Schenkel's
  general theorem is an external boundary check, not a replacement for that
  computation.
- Active extraction: [fermionic Green
  contracts](sources/fermionic-green-contracts.md).

### Positive-frequency arbitrary-helicity completion

- Fernando Lledo, [Massless relativistic wave equations and quantum field
  theory](https://arxiv.org/abs/math-ph/0303031), _Annales Henri Poincare_ 5
  (2004), 607--670.
- Authority: primary mathematical-physics research.
- Relevant output: constructs constrained covariant test-function embeddings into
  positive-energy one-particle Hilbert spaces carrying massless Wigner
  representations for arbitrary discrete helicity, while keeping covariant and
  canonical fibers distinct.
- Research use: external analytic comparison for N4g's internally constructed
  future-shell source map and N4k's internally constructed fermionic two-shell
  map. It does not by itself prove faithfulness or density for the particular
  projected-conserved symmetric-potential source quotients.
- Active extraction: [positive-frequency contracts](sources/positive-frequency-contracts.md).

### Compatibility complexes and support-preserving gauge lifts

- Igor Khavkine, [Compatibility complexes of overdetermined PDEs of finite
  type](https://arxiv.org/abs/1805.03751), _Classical and Quantum Gravity_ 36
  (2019), 185012.
- Igor Khavkine, [The Calabi complex and Killing sheaf
  cohomology](https://arxiv.org/abs/1409.7212), _Journal of Geometry and Physics_
  113 (2017), 131--169.
- Igor Khavkine, [Cohomology with causally restricted
  supports](https://arxiv.org/abs/1404.1932), _Annales Henri Poincare_ 17 (2016),
  3577--3603.
- Marco Benini, [Optimal space of linear classical observables for Maxwell
  `k`-forms via spacelike and timelike compact de Rham
  cohomologies](https://arxiv.org/abs/1401.7563), 2014.
- Authority: primary mathematical and mathematical-physics research.
- Relevant output: regular finite-type differential operators admit complete
  compatibility complexes; the Killing operator produces the Calabi complex;
  causal-support cohomology reduces on a product spacetime to compact-support
  cohomology of a Cauchy surface. The de Rham/Maxwell case supplies the low-spin
  support check.
- Research use: N4h converts zero shell amplitude into a complete compatibility
  equation, then computes the obstruction to one spacelike-compact gauge lift as
  `H_c^1(R^3;Z_s)=0`. This discharges PF-04(a) without shellwise division.
- Active extraction: [support-faithfulness
  contracts](sources/support-faithfulness-contracts.md).

### Algebraic spectra, sector reduction, and field-theoretic bound states

- G. Jordan Maclay, [Dynamical Symmetries of the H Atom: SO(4) to
  SO(4,2)](https://arxiv.org/abs/2305.18229).
- G. A. Kerimov and A. Ventura, [On algebraic models of relativistic
  scattering](https://arxiv.org/abs/0808.1156).
- Davide Batic, Marek Nowakowski, and Aya Mohammad Abdelhaq, [New vistas on the
  Laplace--Runge--Lenz vector](https://arxiv.org/abs/2305.04229).
- Primitivo Acosta-Humanez and David Blazquez-Sanz, [Non-integrability of some
  Hamiltonians with rational potentials](https://arxiv.org/abs/math-ph/0610010).
- F. Nicacio, [Williamson theorem in classical, quantum, and statistical
  physics](https://arxiv.org/abs/2106.11965).
- Djamil Bouaziz and Michel Bawin, [Singular inverse-square potential:
  renormalization and self-adjoint extensions for medium to weak
  coupling](https://arxiv.org/abs/1402.5325).
- Przemyslaw Koscik and Anna Okopinska, [The optimized Rayleigh--Ritz scheme for
  determining the quantum-mechanical spectrum](https://arxiv.org/abs/1008.4606).
- Ana L. Retore, [Introduction to classical and quantum
  integrability](https://arxiv.org/abs/2109.14280).
- Toby S. Cubitt, David Perez-Garcia, and Michael M. Wolf,
  [Undecidability of the Spectral Gap](https://arxiv.org/abs/1502.04573).
- M. Griesemer and D. Hasler, [On the Smooth Feshbach--Schur
  Map](https://arxiv.org/abs/0704.3244).
- Genevieve Dusson, Israel Sigal, and Benjamin Stamm, [The Feshbach--Schur map
  and perturbation theory](https://arxiv.org/abs/2105.02058).
- Edit Matyus et al., [The Bethe--Salpeter QED wave equation for bound-state
  computations of atoms and molecules](https://arxiv.org/abs/2211.02389).
- C. P. Burgess, Peter Hayman, Markus Rummel, and Laszlo Zalavari,
  [Point-Particle Effective Field Theory III: Relativistic Fermions and the
  Dirac Equation](https://arxiv.org/abs/1706.01063).
- Gernot Eichmann et al., [Bound states from the spectral Bethe--Salpeter
  equation](https://arxiv.org/abs/2310.16353).
- Jean Dolbeault, Maria J. Esteban, and Eric Sere, [Distinguished self-adjoint
  extension and eigenvalues of operators with gaps. Application to
  Dirac--Coulomb operators](https://arxiv.org/abs/2206.11679).
- Maria J. Esteban, Mathieu Lewin, and Eric Sere, [Dirac--Coulomb operators with
  general charge distribution. I. Distinguished extension and min--max
  formulas](https://arxiv.org/abs/2003.04004).
- Jan Derezinski and Blazej Ruba, [Holomorphic family of Dirac--Coulomb
  Hamiltonians in arbitrary dimension](https://arxiv.org/abs/2107.03785).
- A. A. Abrikosov Jr., [Dirac operator on the Riemann
  sphere](https://arxiv.org/abs/hep-th/0212134).
- Matteo Gallone and Alessandro Michelangeli, [Discrete spectra for critical
  Dirac--Coulomb Hamiltonians](https://arxiv.org/abs/1710.11389).
- J. Behrndt, A. F. M. ter Elst, and F. Gesztesy, [The Generalized
  Birman--Schwinger Principle](https://arxiv.org/abs/2005.01195).
- Sylvain Golenia and Thierry Jecko, [A new look at Mourre's commutator
  theory](https://arxiv.org/abs/math/0607275).
- Yichen Huang, [Approximating local properties by tensor network states with
  constant bond dimension](https://arxiv.org/abs/1903.10048).
- Alain Connes and Dirk Kreimer, [Hopf Algebras, Renormalization and
  Noncommutative Geometry](https://arxiv.org/abs/hep-th/9808042).
- Authority: primary mathematical-physics research and modern research reviews
  with explicit computations.
- Relevant output: exceptional hidden algebras can compute spectra or scattering
  intertwiners, but their construction and nonexistence tests are model- and
  ansatz-dependent; quadratic normal forms, variational bounds, singular-domain
  analysis and Lax constructions expose different routes; Feshbach--Schur maps
  give exact sector reductions; field-theoretic bound poles and continuum response
  can be extracted from a common spectral Green-function construction; no
  algorithm can decide even the gap question for every Hamiltonian in a broad
  local many-body class.
- Research use: N4n internally computes the Coulomb Casimir consequence, the
  elementary sector Schur complement, and the common pole/continuum distinction.
  The sources delimit analytic and model-dependent hypotheses rather than
  licensing a universal group-theoretic solution. N4r consumes the exact sector
  theorem, equal-time field/mechanics shape, heavy-source effective-data
  boundary, and general-charge domain theorem; its projected-resolvent and
  stability identities remain internal computations.
- Active extractions: [algebraic-spectrum
  contracts](sources/algebraic-spectrum-contracts.md) and [computability endpoint
  contracts](sources/computability-endpoint-contracts.md), extended by [global
  semantic-computability contracts](sources/global-computability-contracts.md)
  and [field/mechanics variation
  contracts](sources/field-mechanics-variation-contracts.md).

### Observable dynamics, memory, and descent

- Guy Cohen and Eran Rabani, [Memory Effects in Nonequilibrium Quantum Impurity
  Models](https://arxiv.org/abs/1105.5348).
- Andres Montoya-Castillo and David R. Reichman, [Approximate but Accurate
  Quantum Dynamics from the Mori Formalism: I. Nonequilibrium
  Dynamics](https://arxiv.org/abs/1603.01903).
- Ayoub Gouasmi, Eric Parish, and Karthik Duraisamy, [A Priori Estimation of
  Memory Effects in Coarse-Grained Nonlinear Systems Using the Mori--Zwanzig
  Formalism](https://arxiv.org/abs/1611.06277).
- Authority: primary quantum-dynamics and reduced-order research deriving or
  evaluating exact projection-memory equations.
- Relevant output: projection onto retained variables produces exact
  instantaneous, initial-correlation, and memory terms; the projected or
  orthogonal evolution required to compute the kernel can retain the original
  many-body or high-dimensional burden.
- Research use: N9 derives the bounded linear memory identity internally, then
  uses these sources to delimit quantum-Liouvillian, nonlinear, short-memory, and
  computational boundaries. It combines this time-domain construction with the
  existing Feshbach contracts rather than treating them as separate analogies.
- Active extraction: [observable-dynamics
  contracts](sources/observable-dynamics-contracts.md).

### Threshold spectral measure, bound poles, and scattering boundary

- K. O. Friedrichs, [On the Perturbation of Continuous
  Spectra](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160010404).
- Davide Lonigro, [The self-energy of Friedrichs-Lee models and its application
  to bound states and resonances](https://arxiv.org/abs/2109.02939).
- Savannah Garmon, Tomio Petrosky, Lena Simine, and Dvira Segal, [Amplification
  of non-Markovian decay due to bound state absorption into
  continuum](https://arxiv.org/abs/1204.6141).
- Authority: original Friedrichs construction and primary modern spectral and
  threshold analyses.
- Relevant output: one discrete/continuum coupling measure generates the
  projected self-energy, bound-state condition, continuum boundary values, and
  threshold long-time behavior; a resonance claim requires analytic
  continuation beyond a real-axis peak.
- Research use: N9a derives and evaluates a rank-one model internally, using the
  sources to delimit self-adjointness, scattering, resonance, and general
  threshold claims.
- Active extraction: [threshold-memory
  contracts](sources/threshold-memory-contracts.md).

### Multiple constructions of a coupling-visible spectral measure

- Fritz Gesztesy and Eduard Tsekanovskii, [On Matrix-Valued Herglotz
  Functions](https://arxiv.org/abs/funct-an/9712004).
- Alex W. Chin, Ángel Rivas, Susana F. Huelga, and Martin B. Plenio, [Exact
  mapping between system-reservoir quantum models and semi-infinite discrete
  chains using orthogonal polynomials](https://arxiv.org/abs/1006.4507).
- Martin Hansen, Alessandro Lupo, and Nazario Tantalo, [On the extraction of
  spectral densities from lattice correlators](https://arxiv.org/abs/1903.06476).
- G. Delfino and G. Mussardo, [Two-point Correlation Function in Integrable QFT
  with Anti-Crossing Symmetry](https://arxiv.org/abs/hep-th/9310130).
- Authority: primary mathematical spectral theory, exact open-system chain
  mapping, modern lattice spectral reconstruction, and integrable-QFT spectral
  evaluation.
- Relevant output: a finite-rank coupling produces an operator-valued measure;
  exact infinite chains, resolvent boundaries, real/Euclidean correlations, and
  form-factor sums can represent the same coupling-visible sector under distinct
  hypotheses.
- Research use: N9b proves the minimal cyclic-sector compression internally and
  uses the sources to delimit matrix inversion, infinite-chain, smeared Euclidean,
  and asymptotic form-factor claims.
- Active extraction: [coupling-measure route
  contracts](sources/coupling-measure-route-contracts.md).

### Field-derived bound/open coupling-measure regression

- Jürg Fröhlich, Marcel Griesemer, and Benjamin Schlein, [Rayleigh Scattering at
  Atoms with Dynamical Nuclei](https://arxiv.org/abs/math-ph/0509009).
- Fumio Hiroshima and K. R. Ito, [Mass Renormalization in Non-relativistic
  Quantum Electrodynamics with Spin
  1/2](https://arxiv.org/abs/math-ph/0412026).
- Christian Gérard, Jacob Schach Møller, and Morten Grud Rasmussen,
  [Asymptotic Completeness in Quantum Field Theory: Translation Invariant Nelson
  Type Models Restricted to the Vacuum and One-Particle
  Sectors](https://arxiv.org/abs/1503.02166).
- Authority: primary fixed-momentum atom--field, effective-mass response, and
  translation-invariant Nelson-model scattering sources.
- Relevant output: translation invariance constructs field fibers and vacuum
  one-boson departure; curvature of one dressed band defines effective mass; a
  continuum resolvent boundary becomes scattering information only after channel
  dynamics and wave operators are supplied.
- Research use: N9c constructs a smaller massive Gaussian scalar bench
  internally, evaluates its field-derived order-`g^2` measure through bound,
  Fourier, moment, and boundary routes, and uses these sources to delimit transfer
  to physical atom--radiation and scattering claims.
- Active extraction: [field-derived measure
  contracts](sources/field-derived-measure-contracts.md).

### Operational bound/open recovery and spin--boson boundaries

- Jana Reker, [Existence of Resonances for the Spin-Boson-Model with Critical
  Coupling Function](https://arxiv.org/abs/1805.02263).
- V. Debierre, T. Durt, A. Nicolet, and F. Zolla, [Spontaneous light emission by
  atomic Hydrogen: Fermi's golden rule without
  cheating](https://arxiv.org/abs/1502.06404).
- Miguel Ballesteros, Dirk-André Deckert, and Felix Hänle, [Relation between the
  Resonance and the Scattering Matrix in the massless Spin-Boson
  Model](https://arxiv.org/abs/1801.04843).
- Authority: primary mathematical spin--boson resonance/scattering research and
  a finite-time spontaneous-emission calculation with an explicit coupling.
- Relevant output: a two-level system coupled to a quantized field supports
  distinct ground, resonance, and scattering constructions; finite-time emission
  can be evaluated before assuming an exponential law; relating a resonance to a
  scattering kernel needs asymptotic channel objects.
- Research use: N9d internally derives one finite-time emitted-boson event from
  the field departure measure, proves its survival/memory/boundary coincidences,
  and uses these sources to stop before resonance or `S`-matrix overclaim.
- Active extraction: [operational-channel
  contracts](sources/operational-channel-contracts.md).

### Kinetic weak-coupling reconstruction and detector boundary

- E. B. Davies, [Markovian master
  equations](https://doi.org/10.1007/BF01608389), *Communications in Mathematical
  Physics* 39 (1974), 91--110.
- Jan Dereziński and Wojciech De Roeck, [Extended Weak Coupling Limit for
  Friedrichs Hamiltonians](https://arxiv.org/abs/math-ph/0604058).
- Jan Dereziński and Wojciech De Roeck, [Extended Weak Coupling Limit for
  Pauli--Fierz Operators](https://arxiv.org/abs/math-ph/0610054).
- Authority: foundational reduced weak-coupling theorem and primary extended
  weak-coupling constructions for direct-sum and bosonic Fock models.
- Relevant output: fixed `lambda^2 t` can produce a contractive Markov semigroup;
  the Friedrichs model admits a full unitary dilation limit; suitable reservoir
  observables require an extended rather than merely reduced limit.
- Research use: N9g constructs its generator from N9d's measure and proves the
  exclusive detector equality in the one-excitation comparator. It uses the
  sources to delimit, not assume, transfer to N9e's recoil fiber, whose
  multiparticle free energy is not additive.
- Active extraction: [kinetic-scale reconstruction
  contracts](sources/kinetic-scale-reconstruction-contracts.md).

### Field-to-particle extraction and asymptotic regimes

- Detlev Buchholz and Wojciech Dybalski, [Scattering in relativistic quantum
  field theory: basic concepts, tools, and
  results](https://arxiv.org/abs/math-ph/0509047).
- Wojciech Dybalski, [Haag--Ruelle scattering theory in presence of massless
  particles](https://arxiv.org/abs/hep-th/0412226).
- Martin Porrmann, [The Concept of Particle Weights in Local Quantum Field
  Theory](https://arxiv.org/abs/hep-th/0005057).
- Authority: authoritative mathematical-physics review and primary theorem/thesis
  sources in local quantum physics.
- Relevant output: sharp stable translation-spectrum subspaces and interpolating
  overlap construct Wigner one-particle spaces and, under locality/regularity,
  incoming and outgoing Fock embeddings. Neutral massive composites may remain
  sharp in a massless continuum. Long-range charged excitations instead require
  particle weights or inclusive asymptotic data because a normalizable sharp-mass
  Wigner subspace can fail.
- Research use: N4s internally constructs the field-created shell quotient and
  its covariance, then uses these sources for the asymptotic convergence,
  scattering, infraparticle, and completeness theorem boundaries.
- Active extraction: [field/particle extraction
  contracts](sources/field-particle-extraction-contracts.md).

### Neutral composite fiber test

- Michael Loss, Tadahiro Miyao, and Herbert Spohn, [Lowest energy states in
  nonrelativistic QED: atoms and ions in
  motion](https://arxiv.org/abs/math-ph/0605005).
- Jürg Fröhlich, Marcel Griesemer, and Benjamin Schlein, [Rayleigh Scattering at
  Atoms with Dynamical Nuclei](https://arxiv.org/abs/math-ph/0509009).
- Authority: primary mathematical-physics theorem sources for translation-
  invariant atom--radiation Hamiltonians, dressed ground-state fibers, and the
  restricted Rayleigh scattering channel.
- Relevant output: a neutral Pauli--Fierz atom has total-momentum fibers and
  dressed ground states under stated binding/momentum assumptions; the
  simplified infrared-cutoff model constructs a simple dressed-atom band,
  asymptotic photons, wave operators, and low-energy asymptotic completeness.
- Research use: N4t computes the exact common dressed state selected by a
  prepared mechanical spectral weight, full band projection, and zero-photon asymptotic
  channel. It also records that this is a nonrelativistic quasiparticle test, not
  yet a Poincare/Wigner composite-particle theorem.
- Active extraction: [neutral composite fiber
  contracts](sources/neutral-composite-fiber-contracts.md).

### Effective-mass evaluation routes

- Jürg Fröhlich, Marcel Griesemer, and Benjamin Schlein, [Rayleigh Scattering at
  Atoms with Dynamical Nuclei](https://arxiv.org/abs/math-ph/0509009).
- Fumio Hiroshima and K. R. Ito, [Mass Renormalization in Non-relativistic
  Quantum Electrodynamics with Spin
  1/2](https://arxiv.org/abs/math-ph/0412026).
- Tosio Kato, [Perturbation Theory for Linear
  Operators](https://link.springer.com/book/10.1007/978-3-642-66282-9), Chapter
  VII.
- Authority: primary mathematical-physics theorem sources and the authoritative
  analytic-perturbation monograph.
- Relevant output: the dressed atom has a simple gapped modified fiber and a
  momentum derivative; effective mass is a ground-energy Hessian expressible as
  a reduced-resolvent response; an isolated analytic branch permits controlled
  weak-coupling expansion.
- Research use: N4u constructs the full response and Feshbach tangent formulas
  on the same branch, proves their equality, rejects generic exact cost gain, and
  reduces the leading scalar-model correction to an atomic-resolvent integral.
- Active extraction: [effective-mass route
  contracts](sources/effective-mass-route-contracts.md).

### Relativistic mass-shell closure

- Xavier Bekaert and Nicolas Boulanger, [The unitary representations of the
  Poincare group in any spacetime
  dimension](https://arxiv.org/abs/hep-th/0611263).
- Detlev Buchholz and Wojciech Dybalski, [Scattering in relativistic quantum
  field theory: basic concepts, tools, and
  results](https://arxiv.org/abs/math-ph/0509047).
- Wojciech Dybalski, [Haag--Ruelle scattering theory in presence of massless
  particles](https://arxiv.org/abs/hep-th/0412226).
- Authority: authoritative representation-theory lectures, mathematical-physics
  review, and primary scattering theorem.
- Relevant output: a positive massive irreducible Poincare sector is supported
  on one orbit through a timelike rest momentum; a sharp interacting massive
  spectral subspace requires additional field access and dynamical stability
  before it becomes an asymptotic particle, including in a massless continuum.
- Research use: N4v internally closes one such interacting orbit, constructs its
  dispersion, proves orbit/rest/curvature mass coincidence, and derives an exact
  low-momentum recovery bound. The sources delimit classification and stability;
  they do not compute the composite mass.
- Active extraction: [relativistic mass-shell
  contracts](sources/relativistic-shell-contracts.md).

### Evaluated relativistic neutral-composite regression

- Julian Schwinger, [Gauge Invariance and Mass.
  II](https://doi.org/10.1103/PhysRev.128.2425).
- A. B. Zamolodchikov and Al. B. Zamolodchikov, [Factorized S-matrices in two
  dimensions as the exact solutions of certain relativistic quantum field theory
  models](https://doi.org/10.1016/0003-4916(79)90391-9).
- Sidney Coleman, [Quantum sine-Gordon equation as the massive Thirring
  model](https://doi.org/10.1103/PhysRevD.11.2088).
- Sergei Lukyanov, [Form-factors of exponential fields in the sine-Gordon
  model](https://arxiv.org/abs/hep-th/9703190).
- Al. B. Zamolodchikov, [Mass scale in the sine-Gordon model and its
  reductions](https://doi.org/10.1142/S0217751X9500053X).
- Daniela Cadamuro and Yoh Tanimoto, [Wedge-local fields in integrable models
  with bound states](https://arxiv.org/abs/1502.01313).
- Authority: foundational exact-scattering and bosonization papers, primary
  form-factor and mass-scale results, and a modern operator-algebraic
  constructive-boundary analysis.
- Relevant output: the attractive sine-Gordon soliton S-matrix has physical-strip
  poles for neutral breathers with exact mass ratios; the massive-Thirring
  presentation gives the first breather a fermion--antifermion interpretation;
  local exponential fields have particle form factors; one ultraviolet
  normalization fixes the soliton mass scale; bound-state poles create additional
  domain and locality obligations in constructive field theory.
- Research use: N4w selects this model as the first exact relativistic composite
  regression, reconstructs the mass from pole kinematics, proves the first-
  breather stability gap, joins fusion and local-field access, and applies N4v to
  its full shell without transferring integrability to QED.
- Active extraction: [sine-Gordon breather
  contracts](sources/sine-gordon-breather-contracts.md).

### Nonintegrable composite robustness

- G. Delfino, G. Mussardo, and P. Simonetti,
  [Non-integrable Quantum Field Theories as Perturbations of Certain Integrable
  Models](https://arxiv.org/abs/hep-th/9603011).
- G. Delfino and G. Mussardo,
  [Non-integrable aspects of the multi-frequency Sine-Gordon
  model](https://arxiv.org/abs/hep-th/9709028).
- Z. Bajnok, L. Palla, G. Takacs, and F. Wagner,
  [Nonperturbative study of the two-frequency Sine-Gordon
  model](https://arxiv.org/abs/hep-th/0008066).
- Sergei Lukyanov, [Form-factors of exponential fields in the sine-Gordon
  model](https://arxiv.org/abs/hep-th/9703190).
- Gabor Takacs, [Form factor perturbation theory from finite
  volume](https://arxiv.org/abs/0907.2109).
- Sergei B. Rutkevich, [Soliton confinement in the double sine-Gordon
  model](https://arxiv.org/abs/2311.07303).
- Authority: foundational form-factor perturbation theory, primary
  multi-frequency sine-Gordon analyses, exact reference form factors, a finite-
  volume higher-order construction, and a modern weak-confinement computation.
- Relevant output: a crossed diagonal reference form factor computes the first
  mass tangent away from integrability; semilocality with the old soliton detects
  confinement; unequal-frequency relevant perturbations are generically
  nonintegrable; higher orders require regulated finite-volume spectral sums.
- Research use: N4x contrasts a second harmonic that preserves the old soliton
  channel with a half-frequency harmonic that confines it, derives a certified
  threshold-gap radius, and isolates the exact numerical form-factor/remainder
  computation still needed.
- Active extraction: [nonintegrable composite
  contracts](sources/nonintegrable-composite-contracts.md).

## Source gaps represented as graph work

- A normalized numerical evaluation of the connected crossed diagonal
  `cos(2 beta phi)` form factors at `xi=1/5`, followed by finite-volume and
  continuum remainder bounds sufficient to instantiate N4x's stability radius
  and local-overlap inequality.
- A complete operator-algebraic construction of the matrix-valued sine-Gordon
  bound-state theory with self-adjoint strongly commuting wedge fields,
  nontrivial double-cone algebras, and a recovered local spectral projector for
  `B_1`. N4w currently stops at exact factorized-scattering and form-factor
  contracts because SG-05 leaves these domain and locality steps open.
- A primary Mackey source or a precise modern theorem for induced representations,
  if `N2` needs measure-theoretic detail beyond Wigner/Bekaert--Boulanger.
- A precise classification theorem for nonchiral tensor and potential complexes
  with prescribed little-group cohomology in `N4a/N5`; N4a now internally
  constructs the symmetric bosonic integer-spin family and N4b constructs the
  symmetric half-integer family, while mixed-symmetry and classification claims
  remain comparison work rather than consequences imported from the BRST/parent
  construction of Alkalaev--Grigoriev--Tipunin.
- Primary sources for the massive Proca/Fierz--Pauli comparisons and normalization
  claims beyond the internally constructed symmetric massless gauge complexes;
  action sources are now bound in N4c, while their full internal adjoint proof is
  still open.
- A rigorous comparison of free equation equivalence versus interacting
  inconsistency for `N7`.
- A proof that compact projected-conserved symmetric-potential sources have dense
  future-shell image in the full induced `L2` helicity-pair space. N4h now
  discharges the support-sensitive faithfulness claim PF-04(a); only PF-04(b)
  remains instead of being assumed from orbitwise cohomology.
