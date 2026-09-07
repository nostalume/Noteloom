# Interaction-return transfer contracts

These contracts delimit the Pauli--Fierz and impurity benches in nodes 39 and 40.
They do not establish the proposed common calculus. The kinetic-square expansion,
Feshbach return, oscillator-strength defect, bath elimination, and common-target
equalities must be constructed inside the worktable.

## IRT-01 -- One atom--field Hamiltonian has bound and photon sectors

- **Source:** J. Froehlich, M. Griesemer, and B. Schlein,
  [Rayleigh Scattering at Atoms with Dynamical
  Nuclei](https://arxiv.org/abs/math-ph/0509009).
- **Hypotheses consumed:** nonrelativistic charged matter coupled to a quantized
  radiation field with ultraviolet and infrared regulation, below ionization.
- **Output consumed:** a stable dressed ground sector and Rayleigh photon channels
  can belong to the same regulated Hamiltonian.
- **Research use:** node 39 may use one matter--field action for its bound/open
  interface rather than joining two unrelated models.
- **Boundary:** node 39 imports neither asymptotic completeness nor infrared-cutoff
  removal, and its dipole fixture is not the source's full atomic model.

## IRT-02 -- Material truncation is not neutral to gauge structure

- **Source:** Daniele De Bernardis, Philipp Pilar, Tuomas Jaako, Simone De Liberato,
  and Peter Rabl, [Breakdown of Gauge Invariance in Ultrastrong-coupling Cavity
  QED](https://arxiv.org/abs/1805.05339).
- **Hypotheses consumed:** cavity light--matter models in different gauges and a
  finite-level material approximation.
- **Output consumed:** the validity of the two-level approximation can be gauge
  dependent and can fail strongly in the Coulomb gauge.
- **Research use:** node 39 rejects an isolated two-level fixture and requires a
  convergent matter hierarchy plus its internally derived sum-rule defect.
- **Boundary:** this source does not prove convergence or gauge equivalence for the
  chosen benchmark regulator.

## IRT-03 -- Hybridization admits a graph expansion around a local impurity

- **Source:** Philipp Werner, Armin Comanac, Luca de' Medici, Matthias Troyer, and
  Andrew J. Millis, [A Continuous-time Solver for Quantum Impurity
  Models](https://arxiv.org/abs/cond-mat/0512727).
- **Hypotheses consumed:** a quantum impurity coupled to a fermionic bath and a
  perturbative expansion in impurity--bath hybridization.
- **Output consumed:** the hybridization expansion is a genuine computational
  realization of an interacting impurity problem and can be compared with exact
  diagonalization.
- **Research use:** node 40 selects graph recovery in hybridization order as the
  condensed-matter realization, rather than importing a relativistic diagram
  convention.
- **Boundary:** stochastic efficiency, low-temperature reach, and any favorable
  sign behavior are not inherited by the finite exact bench.

## IRT-04 -- Finite bath discretization is an approximation obligation

- **Source:** M. Schueler, C. Renk, and T. O. Wehling,
  [Variational Exact Diagonalization Method for Anderson Impurity
  Models](https://arxiv.org/abs/1503.09047).
- **Hypotheses consumed:** an Anderson impurity with a continuous environment
  represented by a finite auxiliary bath for exact diagonalization.
- **Output consumed:** bath discretization is required for conventional finite
  exact diagonalization and its choice affects the approximation.
- **Research use:** node 40 treats the finite bath as an exact common target only
  for that regulated model; continuum transfer needs a separate discretization
  error contract.
- **Boundary:** the proposed calculus does not import the paper's variational bath
  optimization or its accuracy claims.

## Supported boundary

These sources support the physical coexistence of bound/open sectors, the danger
of material truncation, the legitimacy of a hybridization graph realization, and
the separate status of bath discretization. They do not support a cross-domain
compiler, semantic equivalence between QFT and impurity theories, or computational
leverage. Those are exactly the frozen bench obligations.
