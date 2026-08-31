# N8 — Collective Diffusion as a Same-Observable Reduction

Status: leading linear diffusion response is constructively reduced from one
microscopic conserved density under explicit equilibrium, locality, isotropy, and
derivative-expansion presumptions; microscopic coefficient evaluation, a uniform
remainder theorem, nonlinear fluctuations, and large deviations remain
model-dependent, with N8a supplying the first exact stochastic evaluation  
Consumes: [N4q semantic computability](04q-semantic-computability.md), [N4s
field/particle extraction](04s-field-particle-extraction.md), [N4y quantization
and recovery](04y-quantization-recovery-bridge.md), and [collective-response
contracts](../sources/collective-response-contracts.md)  
Produces: the first non-particle collective recovery map, a minimal transport
kernel, and a precise boundary between hydrodynamic compression and microscopic
coefficient computation

## Research contract

- **Question:** can the global field/mechanics/particle view construct a
  collective variable rather than postulate one, and can its reduced dynamics be
  verified against the same microscopic observable?
- **Presumptions:** a quantum system with a spatially homogeneous stationary
  thermal state `omega` at zero equilibrium charge density; one locally conserved
  `U(1)` current `J^mu`; charge-conjugation invariance so the linear charge
  channel decouples from energy and momentum (or an independently proved
  equivalent decoupling); finite positive static susceptibility `chi`; finite
  nonnegative conductivity `sigma`; isotropy and parity; and a controlled
  low-frequency, long-wavelength derivative expansion.
- **Output:** a density response depending at leading order only on

  ```text
  chi, sigma, D=sigma/chi,
  ```

  with pole `omega=-iD|k|^2`, plus a same-observable comparison to the
  microscopic retarded correlator.
- **Boundary:** the node does not derive finite transport from a generic
  Hamiltonian, assert a universal error constant, or identify diffusion with a
  vacuum particle. Those are separate microscopic and approximation obligations.

## 1. Why diffusion is the smallest honest collective test

The first model must differ structurally from the earlier particle and bounded-
state examples. Four candidates were audited:

| Candidate | Extra structure before response | Why not first |
| --- | --- | --- |
| diffusion of one charge | one conserved observable and an equilibrium state | selected |
| sound | coupled energy and momentum densities | larger response matrix |
| Goldstone mode | a chosen broken-symmetry state and order parameter | slow variable already partly postulated |
| plasmon | charge response plus dynamical gauge/Coulomb kernel | mixes collective extraction with field-sector elimination |

Diffusion wins because conservation constructs its slow variable internally and
because its pole is not a real mass shell. It is therefore the smallest
regression against the false claim that every predictive mode is a particle.

## 2. Construct the variable from a microscopic observable

Start with the local microscopic current in the charge-neutral equilibrium, not
an effective field:

```text
partial_t n + div j=0,
n=J^0.
```

Couple a weak external chemical potential to the same density,

```text
delta H(t)=-integral mu_ext(t,x)n(t,x) dx.
```

Define the density perturbation by the microscopic retarded response

```text
delta<n>(omega,k)
 =R_nn^micro(omega,k) mu_ext(omega,k).
```

The static susceptibility is the response to a slowly varying equilibrium
chemical potential:

```text
chi=partial<n>/partial mu,
delta mu_int=delta n/chi
```

at leading derivative order. Thus `delta n` is not introduced because it looks
macroscopic; it is the expectation value of the named microscopic observable
that the source already probes.

Conservation provides the first computability gain. At `k=0`, the total charge
cannot relax, so any relaxation rate for this channel must vanish there. Locality,
isotropy, and parity then forbid a zeroth-order vector current and permit, at the
first dissipative derivative order, only the gradient of the electrochemical
potential:

```text
delta j
 =-sigma grad(delta mu_int-mu_ext)+higher derivatives
 =-D grad(delta n)+sigma grad(mu_ext)+higher derivatives,

D=sigma/chi.
```

This is the constructive origin of Fick's law in this node: one scalar
thermodynamic force is mapped to the only leading isotropic vector derivative,
with its coefficient named by the microscopic conductivity.

## 3. Continuity computes the reduced response

Insert the constitutive map into the same continuity equation:

```text
(partial_t-D Laplacian)delta n
 =-sigma Laplacian(mu_ext)+higher derivatives.
```

With Fourier convention `exp(-i omega t+i k.x)`, both sides act on the same
source and give

```text
(-i omega+D|k|^2)delta n
 =sigma |k|^2 mu_ext.
```

Therefore the leading reduced response is

```text
R_nn^hyd(omega,k)
 =chi D|k|^2/(D|k|^2-i omega).
```

If the retarded Green function is instead defined by
`delta<n>=-G_nn^R mu_ext`, this is the conventional equivalent expression

```text
G_nn^R(omega,k)=chi D|k|^2/(i omega-D|k|^2).
```

Declaring the response convention prevents a sign convention from masquerading
as physics.

The denominator has one pole

```text
omega_diff(k)=-iD|k|^2.
```

For `D>0` it lies in the lower half-plane and approaches the origin as `k->0`.
It is a relaxation mode of a chosen state, not a positive-energy orbit of the
vacuum Poincare spectrum.

## 4. The same-observable recovery contract

The microscopic and reduced routes begin and end with identical data:

```text
(mu_ext, microscopic density n)
  -> R_nn^micro -> delta<n>,

(mu_ext, chi, sigma)
  -> R_nn^hyd   -> delta n_hyd.
```

The hydrodynamic claim is a scaling claim, not an exact all-frequency identity.
Introduce microscopic relaxation and length scales `tau_micro, ell_micro`. The
controlled theorem target is that, in a stated channel and norm,

```text
|omega| tau_micro << 1,
|k| ell_micro << 1,
```

the inverse relaxation kernel and static response admit

```text
L_micro(omega,k)
 =-i omega+D|k|^2
   +O(omega^2 tau_micro,
      omega |k|^2 ell_micro^2,
      D|k|^4 ell_micro^2),

chi_micro(k)=chi+O(|k|^2 ell_micro^2),
```

so the reconstructed response agrees with `R_nn^hyd` to the corresponding
derivative order. N8 records this as the model's approximation contract; it does
not claim that the displayed `O` terms have been bounded for every microscopic
system.

This separates two questions that are often conflated:

```text
structural reduction:
  conservation + constitutive symmetry -> response shape;

microscopic computation:
  Hamiltonian/state -> numerical chi and sigma + error scales.
```

The first is completed here. The second remains model-dependent and may require
kinetic theory, a Kubo calculation, numerics, experiment, or another semantic
compression. [N8a](08a-ssep-exact-collective-regression.md) evaluates the second
route completely for SSEP: exclusion closes the microscopic mean-density sector,
so `chi`, conductivity, `D`, and the lattice-to-continuum error are all computed
without diagonalizing the full Markov generator. Its stochastic boundary is part
of the result, not evidence that generic quantum transport has become easy.

## 5. Four same-input checks

### Conservation check

For nonzero frequency, set `k=0`:

```text
R_nn^hyd(omega,0)=0.
```

A spatially uniform perturbation cannot dynamically change an exactly conserved
total charge in the closed system.

### Equilibrium check

Take the static limit first:

```text
lim_(k->0) lim_(omega->0) R_nn^hyd(omega,k)=chi.
```

The response recovers the susceptibility used to construct it.

### Order-of-limits check

Take the homogeneous limit first:

```text
lim_(omega->0) lim_(k->0) R_nn^hyd(omega,k)=0.
```

The noncommuting limits distinguish thermodynamic equilibration from exact
charge conservation. They are not a singularity to be hidden.

### Stability check

For `chi>0` and `sigma>=0`,

```text
D>=0,
Im omega_diff(k)<=0.
```

Thus the same positivity that makes entropy production nonnegative places the
retarded pole on the stable side of the frequency plane.

## 6. What was compressed—and what was not

For this one observable and scaling regime, the microscopic response surface is
compressed to two static/transport numbers:

```text
{many-body spectrum and matrix elements relevant to R_nn}
  -> {chi,sigma}
  -> one rational hydrodynamic kernel.
```

This is not quotienting of states as in N4s. It combines four kinds of
compression from N4q:

- **semantic quotient:** retain only the conserved-density response;
- **locality:** organize the kernel by derivative order;
- **sparsity:** one conservation law leaves one longitudinal scalar channel;
- **conditioning/stability:** positivity fixes the allowed pole half-plane.

The compression is strong because these mechanisms act on the same observable,
not because any one mechanism solves the microscopic dynamics.

The route still owes the cost of obtaining `chi` and especially `sigma`.
Hydrodynamics may reduce repeated prediction after those coefficients are known,
while the first coefficient calculation remains hard. This is the exact analogue
of N4r's self-energy boundary and N4s's stable-shell discovery boundary. N8a is a
positive gradient-model regression where this cost collapses algebraically; it
does not erase the generic boundary.

## 7. Relation to the previous global view

The three major reductions now have distinct spectral signatures:

| Reduction | Selector | Reduced object | Recovery |
| --- | --- | --- | --- |
| bounded mechanics, N4r | prepared subspace and isolated contour | projected Hamiltonian/resolvent | dressed field state |
| particle, N4s | sharp real translation shell | Wigner one-particle quotient | field-created shell state |
| diffusion, N8 | conserved observable in an equilibrium state and hydrodynamic scaling | lower-half-plane response pole | same density response |

Their common form is

```text
field algebra + state + named observable
  -> selector appropriate to the question
  -> reduced object
  -> recovery of the same observable.
```

This is the generalization sought after the representation-derived field
equation. The equation supplies local observables and dynamics; it does not
predetermine which selector—bound projector, particle shell, scattering limit,
or collective scaling—is useful.

## 8. Downstream construction: fluctuations and large deviations

The deterministic density is only the mean response. In a thermal state, a
downstream node may add a conserved noise current `xi` constrained by fluctuation-
dissipation data,

```text
partial_t n-D Laplacian n+div xi=0,

<xi_i(t,x)xi_j(t',x')>
 =2T sigma delta_ij delta(t-t')delta(x-x')
```

under the appropriate classical/low-frequency convention. The probability cost
of a current history then becomes the bridge to dynamical large-deviation
theory. This is deliberately downstream: local KMS/noise assumptions and the
large-deviation scaling must be constructed and checked rather than smuggled
into the deterministic response.

N8a performs the first model-local construction. For SSEP it derives the
equilibrium density rate function directly from the microscopic Bernoulli measure,
proves that its curvature is `chi^(-1)`, and binds the dynamical density/current
action to an established scaling theorem. Its zero-cost path is the same diffusion
equation. Solving a nontrivial rare-current variational problem remains the next
large-deviation computation.

Other immediate extensions are finite-density hydrodynamics or sound (a coupled
conserved-density matrix), a Goldstone mode (broken-state orbit plus response),
and a plasmon (density response closed through a dynamical gauge kernel). Each
should reuse the same-observable contract above. The scalar formula in this node
must not be carried to finite density before diagonalizing that coupled response.

## 9. Verification ledger

| Obligation | Witness | Verdict |
| --- | --- | --- |
| variable is internally constructed | `n=J^0` of the microscopic conserved current | supported |
| reduced equation preserves semantics | continuity plus the leading electrochemical constitutive map | supported under presumptions |
| response is computable | one scalar inversion `(-iomega+Dk^2)^(-1)` | supported |
| particle interpretation is rejected | pole is at `-iDk^2`, not a real vacuum orbit | supported |
| same observable is recovered | both routes compute `delta<n>/delta mu_ext` | supported at leading derivative order |
| conservation and equilibrium limits agree | the two explicitly ordered limits above | supported |
| microscopic coefficients are cheap | no general reduction supplied | open/model-dependent; exact SSEP regression in N8a |
| approximation remainder is certified | theorem target stated, no universal bound claimed | model-dependent; explicit SSEP bound in N8a |
| nonlinear fluctuations/large deviations | downstream noise/path construction | static SSEP rate and dynamic theorem contract in N8a; quantum/KMS branch open |

## Edges

- `N4q -> N8`: pass observable-relative computability and the requirement to
  count semantic quotient, locality, sparsity, stability, and recovery together.
- `N4s -> N8`: pass the sharp-shell particle selector so the dissipative
  response pole can be distinguished rather than renamed a particle.
- `N4y -> N8`: pass the algebra/state/response placement and the requirement that
  a collective mode begin with a named microscopic observable.
- `N8 -> N8a`: pass the conserved density, transport kernel, and exact missing
  coefficient/noise/remainder obligations; N8a evaluates the stochastic SSEP
  benchmark.
- `N8 -> N9`: pass the asymptotic density selector, same-observable response, and
  missing remainder estimate as the hydrodynamic closure case.
- `N8 -> N9b`: pass real-time response as an alternative access to spectral or
  memory information, together with its finite-window resolution boundary.
- `N8 -> N7/manuscript synthesis`: pass the first same-observable collective
  reduction beside bounded mechanics and particle extraction.
