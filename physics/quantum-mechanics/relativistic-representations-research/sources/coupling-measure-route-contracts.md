# Coupling-Measure Construction Route Contracts

Recorded: 2026-08-30  
Used by: [visible spectral measure](../nodes/11-visible-spectral-measure.md)

node 11 internally proves the coupling-visible cyclic reduction, transform identities,
channel decomposition, finite-moment example, and route comparisons. This packet
owns the theorem and model boundaries that are not reproved there.

## CR-01 — Finite-rank self-energies are operator-valued measure transforms

- **Primary source:** Fritz Gesztesy and Eduard Tsekanovskii, [On Matrix-Valued
  Herglotz Functions](https://arxiv.org/abs/funct-an/9712004).
- **Inputs consumed:** a finite-dimensional prepared space, a self-adjoint
  complementary Hamiltonian, and a bounded departure map.
- **Output consumed:** the corresponding matrix-valued resolvent function has a
  positive operator-valued measure representation and matrix-valued boundary/
  support theory. With node 11's convention, `-Sigma` rather than `Sigma` is Herglotz.
- **Internal use:** node 11 constructs `M(Delta)=B^dagger E_Q(Delta)B` directly and
  uses the source for the general matrix-valued representation and inversion
  contract.
- **Boundary:** a positive matrix-valued function does not make its boundary value
  or underlying field Hamiltonian computationally accessible.

## CR-02 — Orthogonal polynomials give an exact continuum-to-chain map

- **Primary source:** Alex W. Chin, Ángel Rivas, Susana F. Huelga, and Martin B.
  Plenio, [Exact mapping between system-reservoir quantum models and semi-infinite
  discrete chains using orthogonal polynomials](https://arxiv.org/abs/1006.4507).
- **Inputs consumed:** a system linearly coupled to a bosonic or fermionic
  continuum and the continuum spectral weight.
- **Output consumed:** an exact unitary map replaces the continuum by a
  semi-infinite nearest-neighbor chain whose coefficients are recurrence
  coefficients of the orthogonal polynomials for that weight.
- **Internal use:** node 11 derives the coupling-visible cyclic subspace and its first
  two Jacobi sites directly. CR-02 supports the infinite-chain model contract and
  its open-system interpretation.
- **Boundary:** truncating the chain is an approximation. Finite moment matching
  does not preserve a continuum threshold, branch cut, or long-time decay.

## CR-03 — Euclidean spectral inversion requires a resolution contract

- **Primary source:** Martin Hansen, Alessandro Lupo, and Nazario Tantalo, [On the
  extraction of spectral densities from lattice
  correlators](https://arxiv.org/abs/1903.06476).
- **Inputs consumed:** noisy finite Euclidean correlator data, a chosen smearing
  kernel, finite-volume data, and an uncertainty procedure.
- **Output consumed:** smeared spectral densities can be extracted with declared
  resolution and uncertainty; pointwise unsmeared inversion is a difficult
  inverse problem.
- **Internal use:** node 11 proves that the Euclidean correlator is the Laplace
  transform of the same coupling measure and gives a positive-measure
  finite-precision counterexample. CR-03 supplies the practical smeared-output
  contract.
- **Boundary:** Euclidean accessibility is not direct access to a real-time
  threshold or resonance pole. Analytic continuation and resolution errors remain.

## CR-04 — Form factors can evaluate a spectral sum in an integrable QFT

- **Primary sources:** G. Delfino and G. Mussardo, [Two-point Correlation Function
  in Integrable QFT with Anti-Crossing
  Symmetry](https://arxiv.org/abs/hep-th/9310130); H. Babujian, A. Fring, M.
  Karowski, and A. Zapletal, [Exact Form Factors in Integrable Quantum Field
  Theories: the Sine-Gordon Model](https://arxiv.org/abs/hep-th/9805185).
- **Inputs consumed:** a complete asymptotic particle basis in the selected model,
  local-operator form factors, phase-space normalization, and the integrable
  scattering data used to construct those form factors.
- **Output consumed:** inserting asymptotic intermediate states turns a two-point
  function and its spectral measure into a sum of squared form factors integrated
  over multiparticle phase space; in the cited integrable examples the terms can
  be evaluated explicitly.
- **Internal use:** node 11 constructs the spectral sum from a declared resolution of
  identity and binds this path to node 11.
- **Boundary:** convergence, completeness, disconnected terms, and normalization
  are model-specific. Generic nonintegrable or infraparticle theories do not
  inherit an exact low-particle truncation.

## Supported boundary

The contracts support several representations of one measure:

```text
field departure map
  -> positive operator-valued spectral measure
       |-> matrix self-energy boundary
       |-> exact infinite chain
       |-> smeared Euclidean reconstruction
       `-> form-factor spectral sum when asymptotic completeness is available.
```

They do not rank these routes independently of the requested observable, energy/
time resolution, model structure, and recovery cost.
