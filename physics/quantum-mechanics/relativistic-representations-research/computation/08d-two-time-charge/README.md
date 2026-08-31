# N8d Two-Time Charge Computation

This computation evaluates an operational two-projective-measurement (TPM) charge
difference in the finite dephased hopping chain of N8c and compares it with the
finite SSEP produced by N8c's Zeno quotient.

## Semantic observable

On an open four-site chain, the right subsystem is sites `{2,3}` and

```text
N_R=n_2+n_3.
```

Measure `N_R` at time zero, evolve unconditionally, measure `N_R` again, and set
`Q=N_R(t)-N_R(0)`. Since the Bernoulli initial state commutes with `N_R`, its
characteristic function is

```text
phi(theta,t)
  =Tr[exp(i theta N_R)
      E_t(exp(-i theta N_R)rho_eq)].
```

Here `Q` belongs to `{-2,-1,0,1,2}`. Five Fourier samples therefore recover the
entire probability distribution exactly up to time-integration error. No numerical
differentiation of a cumulant-generating function is used. Adjoint preservation
gives `phi(-theta)=conjugate(phi(theta))`, reducing the five samples to three
independent evolutions.

## Inputs

- open chain with `N=4`, Fock dimension `16`;
- hopping `J=0.7` and Bernoulli density `rho=1/2`;
- dephasing values `gamma in {0.5,1,2,4,8}`;
- fixed SSEP slow time `tau=kappa*t=0.75`, with
  `kappa=2J^2/gamma`;
- standard-library complex arithmetic and deterministic fourth-order Runge--Kutta;
- no random sampling.

The SSEP comparator uses the same open bonds, initial probability, right charge,
and slow time. The largest-`gamma` quantum run is repeated at half the time step to
measure integration error.

## Run

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/08d-two-time-charge/two_time_charge.py
```

## Reported outputs

- the full five-point TPM and SSEP charge distributions;
- second and fourth cumulants;
- total-variation distance to the same-input SSEP distribution;
- normalization, reality, positivity, odd-cumulant, and time-step-refinement
  diagnostics.

## Acceptance criteria

- distribution normalization and imaginary leakage below `10^-9`;
- probabilities no smaller than `-10^-9`;
- equilibrium mean and third cumulant below `10^-8`;
- largest-`gamma` step-refinement discrepancy below `2*10^-7`;
- the largest-`gamma` total-variation distance is smaller than the smallest-
  `gamma` distance.

## Boundary

The calculation is a finite-size, finite-slow-time TPM probe. Charge is bounded,
so its cumulants eventually saturate; this computation cannot establish an
infinite-line large-deviation speed or a thermodynamic steady-current theorem.
Its purpose is to exhibit finite-coherence corrections and verify recovery of the
specific Zeno SSEP observable.
