# Dephased Quantum-Chain Transport Contracts

Recorded: 2026-08-30  
Used by: [collective-response boundary](../nodes/10-collective-response-boundary.md)
and [collective-response boundary](../nodes/10-collective-response-boundary.md)

This packet binds only the theorem-scale statements that node 10 does not reproduce.
The local continuity equation, current relaxation, Green--Kubo coefficient, and
second-order pointer-state generator are reconstructed inside the node.

## QD-01 — Strong monitoring produces an exclusion process

- **Source:** Denis Bernard, Tony Jin, and Ohad Shpielberg, [Transport in quantum
  chains under strong monitoring](https://arxiv.org/abs/1802.05048), especially
  equations (2)--(7) and the convergence qualification following equation (5).
- **Inputs consumed:** a finite quantum chain, local nondegenerate occupation
  measurements, Hamiltonian hopping, measurement strength tending to infinity,
  and the slow observation time.
- **Output consumed:** projection to occupation pointer states; the second-order
  effective generator

  ```text
  L_slow=-P L_H (L_deph|_Q)^(-1) L_H P;
  ```

  for a fermionic/XY hopping chain, its pointer-state probabilities evolve as
  SSEP.
- **Internal use:** node 10 evaluates this operator on the same occupation projector
  and obtains its rate in node 10's `J,gamma` convention.
- **Boundary:** trajectory convergence is weak (the cited paper formulates it at
  the level of finite correlation functions), and the limit uses a rescaled slow
  time. It does not state equality of finite-dephasing quantum trajectories with
  SSEP or justify exchanging the Zeno, thermodynamic, and large-time limits.

## QD-02 — Exact dephased tight-binding relaxation is diffusive

- **Source:** Mariya V. Medvedyeva, Fabian H. L. Essler, and Tomaž Prosen,
  [Exact Bethe ansatz spectrum of a tight-binding chain with dephasing
  noise](https://arxiv.org/abs/1606.09122), especially the correlation-function
  duality, equations (13)--(15), and the strong-dephasing discussion.
- **Inputs consumed:** a tight-binding fermion chain with local dephasing and the
  one-dimensional thermodynamic/late-time regime.
- **Output consumed:** exact closure of fixed-order correlations, a diffusive
  low-lying Liouvillian band, and reduction of the strong-dephasing slow sector
  to the classical ferromagnetic/SSEP generator.
- **Internal use:** this contract supports promoting node 10's exact current
  relaxation coefficient to the hydrodynamic diffusion datum and supplies an
  independent spectral boundary check.
- **Boundary:** the paper uses its own hopping and dephasing normalization and an
  imaginary-coupling Hubbard/Bethe representation. node 10 does not import those
  component Bethe equations to determine its coefficient; it computes the
  coefficient directly in its declared convention.

## QD-03 — Exact transport methods do not make the full Lindbladian free

- **Source:** Tony Jin, João S. Ferreira, Michele Filippone, and Thierry Giamarchi,
  [Exact description of quantum stochastic models as quantum
  resistors](https://arxiv.org/abs/2106.14765), especially its local-dephasing
  model and transport discussion.
- **Inputs consumed:** locally dephased quadratic fermions coupled to density
  sources or reservoirs.
- **Output consumed:** diffusive/Ohmic transport is exactly accessible through
  selected one-particle/Keldysh objects even though the density-matrix
  Liouvillian is not a free quadratic generator.
- **Internal use:** node 10 uses this as a scope check for its observable-relative
  compression: exact density transport must not be advertised as a solution of
  arbitrary many-body coherences or current statistics.
- **Boundary:** reservoir conductance and the present periodic equilibrium
  Green--Kubo calculation are different setups. Only their shared
  observable-relative transport conclusion is consumed.

## Frontier source — noisy-fermion current universality

João Costa, Pedro Ribeiro, and Andrea De Luca, [Emergence of universality in
transport of noisy free fermions](https://arxiv.org/abs/2504.00188), reports a
strong-noise Q-SSEP universality class whose transferred-charge large-deviation
function agrees with classical SSEP. node 10 records this as a downstream candidate,
not as support for finite-`gamma` current statistics of the deterministic local-
dephasing Lindblad semigroup. Q-SSEP uses stochastic hopping amplitudes and retains
coherence fluctuations that the unconditional dephasing state does not specify.

## QD-04 — Boundary-driven current statistics recover SSEP hydrodynamics

- **Source:** Marko Žnidarič, [Large-deviation statistics of a diffusive quantum
  spin chain and the additivity principle](https://arxiv.org/abs/1401.7341),
  especially equations (24)--(26) and the finite-size discussion.
- **Inputs consumed:** an open XX chain with bulk dephasing, Markovian particle
  reservoirs at both ends, stationary boundary driving, current counted through
  reservoir jumps, and the thermodynamic limit.
- **Output consumed:** transport data proportional to
  `D(n)=constant` and `sigma(n)=2D n(1-n)`; numerical higher-cumulant/additivity
  evidence; and a thermodynamic current generating function matching the open
  SSEP after normalization.
- **Internal use:** node 10 uses this as evidence that finite dephasing need not destroy
  SSEP hydrodynamic current statistics at large scale.
- **Boundary:** this is not node 10's infinite-line annealed equilibrium current and
  not node 10's isolated-system two-projective-measurement charge difference. The
  reservoir-jump long-time limit at fixed length, thermodynamic limit, and
  equilibrium half-filling Gaussian specialization must not be transferred across
  those geometries without a constructed bridge.

## Supported boundary

The source contracts support

```text
coherent hopping + strong local monitoring
  -> occupation pointer manifold
  -> SSEP slow process;

local-dephasing quantum chain
  -> diffusive low-lying density sector.
```

They do not identify a Lindblad density matrix with a unique monitored trajectory,
nor do they make every quantum observable classical.
