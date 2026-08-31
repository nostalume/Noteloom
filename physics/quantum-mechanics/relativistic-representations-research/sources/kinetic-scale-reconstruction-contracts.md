# Kinetic-Scale Reconstruction Source Contracts

These contracts support
[N9g](../nodes/09g-kinetic-scale-reconstruction.md). N9g constructs its departure
kernel, boundary generator, excitation sectors, event decomposition, and numerical
scale internally. Sources delimit which kinetic limits are established and which
do not transfer automatically to N9e's recoil fiber.

## KSR-01 — Reduced weak coupling produces a Markov semigroup

- **Source:** E. B. Davies,
  [Markovian master equations](https://doi.org/10.1007/BF01608389),
  *Communications in Mathematical Physics* 39 (1974), 91--110.
- **Hypotheses consumed:** a weakly coupled system/reservoir dynamics, a suitable
  projection onto the small system, correlation decay/mixing conditions, and the
  scale `lambda^2 t` held fixed.
- **Output consumed:** memory can converge to a Markov generator and exponential
  decay on the rescaled time variable.
- **Internal replacement:** N9g constructs the scalar generator directly from
  N9d's measure in (2.2)--(2.4); it does not import a rate formula.
- **Boundary:** reduced dynamics controls small-system observables. It does not by
  itself identify N9d's vacuum-survival or exclusive one-boson projections.

## KSR-02 — The Friedrichs model supplies the exact comparator limit

- **Source:** Jan Dereziński and Wojciech De Roeck,
  [Extended Weak Coupling Limit for Friedrichs
  Hamiltonians](https://arxiv.org/abs/math-ph/0604058).
- **Hypotheses consumed:** a finite-dimensional discrete space coupled
  off-diagonally to a continuum, a regular energy representation near the
  discrete energy, and the weak-coupling scale `lambda^2 t`.
- **Output consumed:** the compressed discrete evolution converges uniformly on
  compact rescaled-time intervals to a contractive semigroup; the suitably
  rescaled full evolution converges to its unitary dilation.
- **Internal replacement:** N9g constructs the invariant one-excitation space and
  its Friedrichs block from the N9e form factor and energy. It then computes the
  one-dimensional generator and detector partition explicitly.
- **Boundary:** the theorem applies to the off-diagonal direct-sum Hamiltonian.
  It does not justify deleting N9e's counter-rotating multi-boson paths.

## KSR-03 — Extended Pauli--Fierz limits can retain reservoir observables

- **Source:** Jan Dereziński and Wojciech De Roeck,
  [Extended Weak Coupling Limit for Pauli--Fierz
  Operators](https://arxiv.org/abs/math-ph/0610054).
- **Hypotheses consumed:** a finite-dimensional small system, a bosonic Fock
  reservoir with an additive second-quantized free generator, regular coupling
  near the Bohr frequencies, and the paper's rescaling/identification maps.
- **Output consumed:** a strong-star extended weak-coupling limit to a quantum
  Langevin unitary; suitable reservoir observables can be studied in that limit.
- **Research use:** this identifies the kind of theorem needed before an
  exclusive emitted-field event may accompany the reduced exponential law.
- **Boundary:** N9e's fixed-total-momentum free fiber contains `P_f^2/(2M)` and
  hence momentum cross terms on multiparticle sectors. The cited theorem is not
  asserted to cover that fiber, and its rescaled reservoir observables are not
  automatically the physical projection `Pi_1`.

## Supported boundary

The packet supports N9g's kinetic law for its internally constructed Friedrichs
comparator and the general distinction between reduced and extended limits. It
does not establish uniform suppression of N9e's multiparticle sectors, an exact
exclusive detector limit for the recoil model, a convergence rate, or a
finite-coupling resonance law.
