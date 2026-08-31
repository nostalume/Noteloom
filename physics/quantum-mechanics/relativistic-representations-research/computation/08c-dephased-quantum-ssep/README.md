# N8c Finite-Chain Algebra Check

This computation represents the invariant maps in N8c on a four-site fermionic
Fock space. Components are used only as an independent finite-dimensional witness;
the node's derivation is stated through CAR operators, pinching, and a Schur/Zeno
reduction.

## Semantic question

For the same periodic hopping Hamiltonian, occupation dephasing, equilibrium
state, and current, does direct matrix evaluation verify all four claims?

1. local continuity;
2. exact current relaxation `L^dagger(J_tot)=-gamma J_tot`;
3. static current covariance `C_JJ(0)/N=2J^2 chi`;
4. second-order diagonal slow generator equals SSEP with bond rate
   `kappa=2J^2/gamma`.

## Inputs

- sites `N=4`;
- periodic spinless-fermion CAR Fock space, dimension `2^N=16`;
- hopping `J=0.7`;
- dephasing convention `L_x=sqrt(gamma)n_x`, `gamma=1.3`;
- Bernoulli equilibrium density `rho=0.37`;
- standard-library complex arithmetic; no third-party dependency and no
  randomness.

The code constructs creation and annihilation maps with their fermionic parity
signs. It evaluates the dephasing inverse only on off-diagonal matrix units, where
its eigenvalue is fixed by the occupation Hamming distance.

## Run

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/08c-dephased-quantum-ssep/check_quantum_ssep.py
```

## Acceptance criteria

- Frobenius/operator discrepancies for continuity, current decay, susceptibility,
  current covariance, and effective-generator equality below `10^-11`;
- probability conservation of the effective generator below `10^-11`;
- off-diagonal effective rates nonnegative up to `10^-12`.

## Boundary

This is not a thermodynamic simulation, a proof of the Zeno convergence theorem,
or evidence for finite-dephasing full counting statistics. It checks normalization,
fermionic signs, the semantic projection, and the SSEP rate on one complete finite
Fock space.
