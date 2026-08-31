# N8d — Two-Time Quantum Charge and Its SSEP Quotient

Status: regression leaf; operational finite-system charge observable constructed; its complete
five-point law and second/fourth cumulants evaluated; strong-dephasing recovery of
the same finite SSEP observable verified; infinite-volume finite-dephasing law
left open  
Consumes: [N8b equilibrium SSEP current large deviations](08b-ssep-current-large-deviation.md),
[N8c dephased quantum chain and SSEP recovery](08c-dephased-quantum-ssep.md),
and [dephased quantum-chain contracts](../sources/quantum-diffusion-contracts.md)  
Produces: a two-projective-measurement charge construction, a same-input quantum/
classical recovery check for N8c, and the boundary separating finite isolated
charge, infinite-line current, and reservoir current statistics

## Research contract

- **Question:** does N8c's quantum-to-SSEP reduction recover an operational charge
  distribution, rather than only its diffusion coefficient?
- **Presumptions:** the open four-site dephased hopping chain of N8c; Bernoulli
  equilibrium at density `rho=1/2`; the right charge `N_R=n_2+n_3`; projective
  measurements of that charge at the beginning and end; and fixed slow time
  `tau=(2J^2/gamma)t` as `gamma` grows.
- **Output:** the joint two-measurement probability, its characteristic function,
  an exact finite Fourier recovery, and a numerical same-input comparison with
  open-chain SSEP through the fourth cumulant.
- **Boundary:** this finite isolated charge is bounded. It is neither N8b's
  infinite-line integrated current nor a boundary-reservoir jump count, and it
  cannot establish either large-deviation theorem.

## 1. The cut constructs the charge observable

Use the open chain with sites `0,1,2,3` and choose the right subsystem

```text
R={2,3},
N_R=n_2+n_3.
```

Because there is no exterior boundary bond, the change of `N_R` is exactly the
net occupation transported across the single cut `(1,2)`. This avoids defining a
quantum path by analogy with classical jumps. Measure `N_R` at time zero, evolve
with N8c's unconditional Lindblad channel `E_t=exp(t L_gamma)`, measure it again,
and define

```text
Q=n-m,
```

where `m,n` are the two observed eigenvalues. If `Pi_m^R` is the spectral
projector of `N_R`, the joint probability is constructed by the measurement
operations themselves:

```text
p_t(m,n)
  =Tr[Pi_n^R E_t(Pi_m^R rho_eq Pi_m^R)].
```

It is normalized because the projectors resolve the identity and `E_t` is trace
preserving. It is nonnegative because a completely positive map sends the first
post-measurement state to a positive state. No unraveling or unobserved trajectory
has been inserted.

## 2. The characteristic map follows from the same operations

Weight the constructed joint events by `exp(i theta(n-m))`:

```text
phi(theta,t)
  =sum_(m,n) exp(i theta(n-m))p_t(m,n).
```

The Bernoulli state is diagonal in occupation and hence commutes with `N_R`. Thus

```text
sum_m exp(-i theta m)Pi_m^R rho_eq Pi_m^R
  =exp(-i theta N_R)rho_eq.
```

Using the spectral resolution of the final measurement gives the computable form

```text
phi(theta,t)
  =Tr[exp(i theta N_R)
      E_t(exp(-i theta N_R)rho_eq)].
```

This is a deduction from the two measurement maps, not an externally imported
counting-field rule. It immediately checks `phi(0,t)=1`. Adjoint preservation and
self-adjoint initial data also give

```text
phi(-theta,t)=conjugate(phi(theta,t)).
```

Since `N_R` has eigenvalues `0,1,2`, the transferred charge belongs to
`{-2,-1,0,1,2}`. Therefore five character values at
`theta_l=2 pi l/5` recover the whole law:

```text
P_t(Q=q)
  =(1/5)sum_(l=0)^4 exp(-i theta_l q)phi(theta_l,t).
```

The conjugation identity reduces this to three independent Liouville evolutions.
The reduction is exact; only time-integration error remains.

## 3. The comparator keeps every semantic input fixed

N8c constructs the strong-monitoring population generator

```text
G_SSEP f(eta)
  =kappa sum_(x=0)^2 [f(eta^x)-f(eta)],
kappa=2J^2/gamma,
```

where a term vanishes if the occupations on the open bond agree. Give this
process the same Bernoulli initial distribution, the same open bonds, the same
right charge, and the same two-time difference. In slow time

```text
tau=kappa t,
```

the comparator is unit-rate open-chain SSEP evolved for `tau`. Thus the tested
arrow is not “both models diffuse,” but

```text
same initial occupation event
  -> quantum dephasing channel -> final right charge

same initial occupation event
  -> Zeno population generator -> final right charge.
```

QD-01 supports convergence of the finite slow population process in the strong-
monitoring limit. Here the entire endpoint event is additionally evaluated on the
same four-site system. No claim of a uniform thermodynamic or late-time remainder
is made.

## 4. The complete finite law converges, not only its variance

The reproducible computation uses `J=0.7`, `rho=1/2`, and `tau=0.75`. For the
same-input SSEP comparator it finds

```text
P_SSEP(-2,-1,0,1,2)
  =(0.000423320, 0.107957710, 0.783237940,
    0.107957710, 0.000423320),

kappa_2=0.2193019771,
kappa_4=0.0851815750.
```

The quantum TPM results are:

| `gamma` | `kappa_2` | `kappa_4` | total variation to SSEP | `gamma^2 TV` |
| ---: | ---: | ---: | ---: | ---: |
| 0.5 | 0.0325396973 | 0.0293634363 | 0.1842224 | 0.0460556 |
| 1 | 0.0995449279 | 0.0698547626 | 0.1172265 | 0.1172265 |
| 2 | 0.1839580387 | 0.0842081495 | 0.0332470 | 0.1329879 |
| 4 | 0.2118839930 | 0.0846417996 | 0.00673864 | 0.1078182 |
| 8 | 0.2175590450 | 0.0850429782 | 0.00157295 | 0.1006689 |

At `gamma=8`, the full quantum distribution is

```text
(0.000394989, 0.107199565, 0.784810892,
 0.107199565, 0.000394989).
```

Thus variance recovery is accompanied by fourth-cumulant and full-distribution
recovery. The near stabilization of `gamma^2 TV` for the last rows is numerical
evidence for a leading `O(gamma^(-2))` correction in this fixed finite test; it is
not a proved asymptotic bound.

The table must not be read as a weak-dephasing transport comparison. At fixed
`tau`, physical time is

```text
t=tau gamma/(2J^2).
```

Small `gamma` therefore also means a short physical evolution. This scaling was
chosen to test N8c's Zeno quotient, not to compare equal physical times across
dephasing strengths.

## 5. Three current laws that share local transport data

The same SSEP coefficient can appear in inequivalent observable geometries:

| Construction | Accumulated variable | Scale and boundary |
| --- | --- | --- |
| N8b infinite-line equilibrium SSEP | net crossings of one cut, equivalently half-line charge change | unbounded; cumulant generator has speed `sqrt(t)` and typical current scale `t^(1/4)` |
| N8d isolated four-site TPM | difference of two measured right charges | bounded by `-2<=Q<=2`; cumulants saturate |
| QD-04 boundary-driven dephased chain | reservoir-jump current in a stationary open system | accumulates for arbitrarily long time at fixed length; thermodynamic/additivity limit is taken separately |

For example, at half filling N8b's scaled fourth cumulant is negative, whereas
the finite N8d value at `tau=0.75` is positive. This is not a contradiction:
geometry, event, scaling speed, and limit order differ. QD-04 gives independent
evidence that a finite-dephasing quantum chain can recover open-SSEP hydrodynamic
current statistics, but it does not prove N8d's isolated TPM law or N8b's
infinite-line law.

## 6. Computability audit

N8c's diffusion coefficient was unusually cheap:

```text
one conserved density
  -> one exact current eigen-operator
  -> one scalar Green--Kubo integral.
```

The full finite charge law retains more information and therefore costs more:

```text
two measurement operations
  -> three independent tilted initial operators
  -> three evolutions in a 4^N-dimensional operator space
  -> five-point Fourier recovery.
```

Finite support and adjoint symmetry are real compressions, but they do not prevent
the operator-space cost from growing exponentially. The four-site computation is
therefore a semantic and normalization witness, not a scalable solver.

The useful common structure distilled from N8b--N8d is instead:

```text
choose one operational charge event
  -> derive its characteristic map from that event
  -> identify the slow population quotient
  -> compare the same event before and after quotienting
  -> state geometry and limit order before transferring a law.
```

This tells us exactly what a scalable continuation must preserve. A tensor-network
or hydrodynamic calculation would be relevant only if it returns this same
characteristic map or a controlled limit of it.

## 7. Verification ledger and frontier

The computation is documented in
[computation/08d-two-time-charge](../computation/08d-two-time-charge/README.md).

| Obligation | Witness | Verdict |
| --- | --- | --- |
| operational quantum event | two spectral measurements and the intervening CPTP channel | exact |
| characteristic function | derived by summing the same joint probabilities | exact when `[rho_eq,N_R]=0` |
| whole finite distribution | five-point Fourier inversion | exact up to evolution error |
| same-input classical comparator | same initial law, bonds, charge, and slow time | exact construction |
| normalization, positivity, odd cumulants | direct finite-state checks | passed |
| time-integration stability | largest-`gamma` half-step discrepancy `1.199e-15` | passed |
| strong-dephasing SSEP recovery | TV decreases from `0.1842224` to `0.00157295`; `kappa_2,kappa_4` converge | numerically supported and consistent with QD-01 |
| `O(gamma^(-2))` error | last two scaled distances are near `0.1` | observed, not proved |
| infinite-line finite-`gamma` TPM law | no thermodynamic/hydrodynamic construction here | open |
| exchange of Zeno, volume, and late-time limits | no uniform remainder | open |

The local open problem is to construct the infinite-line hydrodynamic TPM observable
from the quantum channel and decide whether, at fixed finite `gamma>0`, its large-
scale generating law is N8b's SSEP function after replacing time by `D_GK t`.
That requires either a controlled tilted-hydrodynamic reduction or a counterexample;
QD-04's different boundary observable is evidence, not the missing bridge. It is
not the next global-spine step: N9 consumes this node only as an endpoint-recovery
regression for the general descent/memory construction.

## Edges

- `N8b -> N8d`: pass the integrated-cut event and its nonlinear cumulant test,
  while changing from an infinite half-line to a finite isolated right subsystem.
- `N8c -> N8d`: pass the Lindblad channel, exact `D_GK`, Zeno SSEP generator, and
  the distinction among unconditional, monitored, and two-time observables.
- `N8d -> infinite-line quantum TPM`: pass the operational characteristic map and
  require a controlled volume/hydrodynamic limit before importing N8b's law.
- `N8d -> N9`: pass the full-distribution recovery check and demonstrate that
  recovery of one output is weaker than autonomous descent of the retained state.
