# Global Semantic-Computability Source Contracts

These sources type irreducible theorem inputs and boundaries for N4q. They do not
replace the internal same-observable computations in that node.

## GC-01 — Isospectral sector elimination

- **Source:** M. Griesemer and D. Hasler, [On the Smooth Feshbach--Schur
  Map](https://arxiv.org/abs/0704.3244).
- **Hypotheses consumed:** a closed operator pair and partition operators satisfying
  the Feshbach-pair invertibility and domain conditions.
- **Output consumed:** the Feshbach map is isospectral in the precise sense that
  invertibility and kernels can be transferred with explicit reconstruction maps.
- **Boundary:** writing a Schur complement is not itself computational gain. The
  eliminated inverse, reconstruction, and iteration estimates must be controlled.

## GC-02 — Eigenvalue transfer to an auxiliary operator

- **Source:** J. Behrndt, A. F. M. ter Elst, and F. Gesztesy, [The Generalized
  Birman--Schwinger Principle](https://arxiv.org/abs/2005.01195).
- **Hypotheses consumed:** a factorized perturbation and resolvent point for the
  reference operator, with the analytic/domain assumptions stated by the theorem.
- **Output consumed:** eigenvalues and their geometric/algebraic multiplicities can
  be transferred to zeros/eigenvalues of an operator-valued Birman--Schwinger
  function.
- **Boundary:** the theorem transfers the query; it does not ensure compactness,
  an easier kernel, good conditioning, or lower observable-recovery cost.

## GC-03 — Positive commutators control the continuum

- **Source:** Sylvain Golenia and Thierry Jecko, [A new look at Mourre's
  commutator theory](https://arxiv.org/abs/math/0607275).
- **Hypotheses consumed:** local regularity with respect to a conjugate operator and
  a Mourre estimate on a declared interval.
- **Output consumed:** a limiting absorption principle and propagation/continuous
  spectral control, including a reduced formulation around point spectrum.
- **Boundary:** a positive commutator estimate does not calculate isolated bound
  energies and requires its own domain and regularity construction.

## GC-04 — Observable-specific low-entanglement compression

- **Source:** Yichen Huang, [Approximating local properties by tensor network
  states with constant bond dimension](https://arxiv.org/abs/1903.10048).
- **Hypotheses consumed:** the stated one-dimensional area-law or gapped-ground-state
  conditions and a target accuracy for local observables.
- **Output consumed:** local properties admit matrix-product-state approximation
  with system-size-independent bond dimension controlled by the accuracy.
- **Boundary:** this is an observable-specific approximation theorem, not an exact
  full-state representation or a dimension-independent universal algorithm.

## GC-05 — Graph combinatorics of renormalization

- **Source:** Alain Connes and Dirk Kreimer, [Hopf Algebras, Renormalization and
  Noncommutative Geometry](https://arxiv.org/abs/hep-th/9808042).
- **Hypotheses consumed:** perturbative QFT graphs with their divergent subgraph and
  contraction structure.
- **Output consumed:** a Hopf-algebraic organization of recursive counterterms,
  including overlapping subdivergences.
- **Boundary:** the graph algebra does not evaluate the associated integrals,
  establish convergence, or resum a nonperturbative bound-state pole by itself.

## GC-06 — Universal spectral computation is impossible

- **Source:** Toby Cubitt, David Perez-Garcia, and Michael M. Wolf,
  [Undecidability of the Spectral Gap](https://arxiv.org/abs/1502.04573).
- **Hypotheses consumed:** the broad translationally invariant nearest-neighbor
  two-dimensional local Hamiltonian family constructed in the theorem.
- **Output consumed:** no algorithm decides the promised gapped/gapless alternative
  for every Hamiltonian in that family.
- **Boundary:** this does not prove a specified finite atomic or field model is
  intractable. It rejects only a universal spectral solver across the broad class.
