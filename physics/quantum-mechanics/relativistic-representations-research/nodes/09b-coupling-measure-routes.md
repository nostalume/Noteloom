# N9b — Multiple Routes to the Coupling-Visible Field Spectrum

Status: common cyclic compression proved; six construction routes compared; exact
moment-chain discriminator evaluated; the first bounded atom--field route is now
evaluated by N9c, while remaining model choices stay observable-dependent  
Consumes: [N4n spectral bridge](04n-algebraic-spectrum-bridge.md),
[N4u effective-mass route](04u-effective-mass-route-audit.md),
[N4w sine-Gordon particle test](04w-sine-gordon-breather-rest-pole.md),
[N8 collective response](08-collective-diffusion-response.md),
[N9 observable dynamics](09-observable-dynamics.md),
[N9a threshold spectral measure](09a-threshold-spectral-measure.md), and
[route contracts](../sources/coupling-measure-route-contracts.md)  
Produces: the minimal coupling-visible reducing sector, a common operator-valued
measure target, six non-equivalent construction paths, one exact route
discriminator, and a global branching frontier

## Research contract

- **Question:** by which materially different routes can a field coupling measure
  be constructed, and which route is computationally meaningful for bound,
  scattering, memory, Euclidean, or collective outputs?
- **Regime:** the global spine through the measure is in development; how to obtain
  that measure from a realistic field is a local discovery region. No route is
  selected in advance.
- **Presumptions:** sections 2--7 use a self-adjoint complementary Hamiltonian
  `H_Q`, a finite-dimensional prepared space `P`, and a bounded map `W:P->QH`.
  For dynamical elimination `W=B=QHP`; a field-created state can instead use
  `W=QAP`. These maps must not be silently identified.
- **Output:** an exact semantic compression before computation, route-specific
  constructions and failure boundaries, and several connected next probes.
- **Boundary:** nonnormal Liouvillians need not possess a positive measure of this
  type; a prepared spectral measure alone does not construct a full multichannel
  scattering matrix.

## 1. Hold the global object fixed while allowing several paths

N9a prescribed one scalar density and evaluated its consequences. The next problem
is not “find a better density formula.” It is to construct the spectral information
seen by a named preparation or coupling.

Let `E_Q(Delta)` be the spectral resolution of `H_Q`. For any declared access map
`W:P->QH`, construct

```text
M_W(Delta)=W^dagger E_Q(Delta)W.                 (1.1)
```

The type of `W` records the physical question:

```text
W=QHP  -> field departure and return: self-energy and memory;
W=QAP  -> field-created spectral content of preparation A;
W=J    -> an externally constructed channel injection.
```

Only when two routes use the same `W`, `H_Q`, and prepared inner product do they
claim the same measure. This prevents a local-field two-point function from being
renamed the Feshbach self-energy without a bridge between `A` and `H`.

## 2. First compress the field to the coupling-visible cyclic sector

Construct

```text
C_W=closure span{E_Q(Delta)Wp:
                  Delta a Borel set, p in P}.    (2.1)
```

This is not an arbitrary Krylov ansatz. It is the smallest reducing subspace of
`H_Q` containing the range of `W`.

To verify reduction, apply any spectral projection to a generating vector:

```text
E_Q(Omega)[E_Q(Delta)Wp]
  =E_Q(Omega intersection Delta)Wp in C_W.       (2.2)
```

Thus every `E_Q(Omega)` preserves `C_W`; self-adjointness also preserves its
orthogonal complement. To verify minimality, let `R` be any closed reducing
subspace containing `Ran W`. Then

```text
Wp in R
  -> E_Q(Delta)Wp in R
  -> C_W subset R.                               (2.3)
```

Now take `v in C_W^perp`. Any bounded spectral function preserves that complement,
while `Wp` belongs to `C_W`. On the same `p,v`,

```text
<p,W^dagger f(H_Q)v>
  =<Wp,f(H_Q)v>
  =0.                                            (2.4)
```

Therefore all field directions outside `C_W` are invisible to every return map
`W^dagger f(H_Q)W`. The exact replacements

```text
H_Q -> H_Q restricted to C_W,
W   -> W with codomain C_W                       (2.5)
```

preserve the complete measure, memory, self-energy, and Euclidean correlation.
This is the strongest model-independent compression found so far: it removes
uncoupled field information before choosing coordinates or an algorithm.

It may still be infinite-dimensional. Construction cost is the cost of generating
or accessing `C_W`; the theorem does not promise a small basis.

## 3. Construct the spectral realization of the cyclic sector

Equation (1.1) itself constructs an `L^2` realization. Start from finite spectral
sums in `C_W` and map

```text
sum_j E_Q(Delta_j)Wp_j
  |-> sum_j 1_(Delta_j) p_j.                     (3.1)
```

The source inner product is computed without components:

```text
<E_Q(Delta)Wp,E_Q(Omega)Wq>
  =<Wp,E_Q(Delta intersection Omega)Wq>
  =<p,M_W(Delta intersection Omega)q>.           (3.2)
```

The target is therefore the space of `P`-valued simple functions with inner
product induced by `M_W`, quotiented by zero-norm functions and completed. Equation
(3.2) makes (3.1) isometric and extends it to `C_W`. Under this map,

```text
H_Q -> multiplication by lambda,
Wp  -> the constant function p.                 (3.3)
```

This explains why an operator-valued measure is sufficient: it is the full
spectral model of precisely the field sector that can depart from and return to
the preparation.

## 4. Six paths construct or observe the same target differently

### 4.1 Symmetry-channel path: reduce before evaluating energy

Suppose orthogonal projectors `R_c` resolve the complement and commute with
`H_Q`. Since they also commute with every `E_Q(Delta)`, insert their identity into
(1.1):

```text
M_W(Delta)
  =sum_c W^dagger R_c E_Q(Delta)R_c W
  =sum_c M_c(Delta).                             (4.1)
```

Each `M_c` is positive by the same norm computation as N9a. If a charge, angular
momentum, total momentum, or parity selection rule gives `R_cW=0`, that whole
channel vanishes before any spectral solve.

This path can greatly reduce multiplicity and expose thresholds. It does not
determine the energy dependence inside a surviving channel. N4u's fixed-total-
momentum fiber and one-photon/atomic sectors are the existing worktable example.

### 4.2 Resolvent path: target bound poles and off-axis response

For `Im z!=0`, construct

```text
Sigma_W(z)=W^dagger(z-H_Q)^(-1)W
          =integral dM_W(lambda)/(z-lambda).      (4.2)
```

The measure is recovered at continuity endpoints by integrating the boundary
imaginary part:

```text
M_W((a,b))
  =-lim_(epsilon->0+) (1/pi)
     integral_a^b Im Sigma_W(E+i epsilon)dE.      (4.3)
```

Indeed, the integrand applies the positive approximate identity

```text
-Im[1/(E+i epsilon-lambda)]/pi
  =(1/pi) epsilon/[(E-lambda)^2+epsilon^2]        (4.4)
```

to the same measure. This route is direct for N4r/N4u bound poles because `z`
stays away from the continuum. Near the real boundary the complementary linear
solve becomes poorly conditioned; a compact self-energy formula can hide the
original field computation.

### 4.3 Real-time path: target memory and finite-time observables

Prepare `Wp`, evolve it in the complement, and return it through `W^dagger`:

```text
K_W(t)=W^dagger exp(-itH_Q)W
      =integral exp(-it lambda)dM_W(lambda).      (4.5)
```

Knowing all matrix elements of `K_W(t)` for all real `t` uniquely determines the
finite measure by Fourier uniqueness. A finite time interval does something
different: multiplying by an observation window convolves the measure with the
window's frequency kernel, so its energy resolution is of order `1/T` rather than
pointwise.

This is the natural route when time propagation is cheap or the requested output
is already a memory kernel. It is expensive for a very narrow pole or a threshold
tail because those require long propagation.

### 4.4 Moment/Lanczos path: construct a local chain from repeated action

When the domains permit it, repeated application of `H_Q` to `W` constructs

```text
mu_n=W^dagger H_Q^n W
    =integral lambda^n dM_W(lambda).              (4.6)
```

The Gram matrix of the vector-polynomial orbit is computed from the same moments:

```text
<(H_Q^iWp),(H_Q^jWq)>
  =<p,mu_(i+j)q>.                                (4.7)
```

Gram--Schmidt on this orbit therefore constructs a scalar Jacobi or block-Lanczos
chain. Multiplication by `lambda` raises polynomial degree by one; orthogonality
to all degrees below `n-1` makes the representation tridiagonal rather than dense.
The infinite chain is the same cyclic sector (3.3), not a discretization.

A chain truncated after `N` sites has a finite atomic measure and matches only a
finite moment set. It can compress short-time propagation or off-axis resolvents,
but at fixed `N` it cannot contain a continuum branch cut or irreversible
long-time decay.

### 4.5 Euclidean path: access positivity but accept inverse resolution

If the complement energy is nonnegative, imaginary-time evolution constructs

```text
C_W(tau)=W^dagger exp(-tau H_Q)W
        =integral exp(-tau lambda)dM_W(lambda).   (4.8)
```

For every `p` and `n`, differentiation computes

```text
(-1)^n d^n/dtau^n <p,C_W(tau)p>
  =integral lambda^n exp(-tau lambda)
     d<p,M_W(lambda)p>
  >=0.                                           (4.9)
```

Complete monotonicity is thus a positivity check on the measured correlator. But
the inverse Laplace transform amplifies high-energy and noise-sensitive
directions. CR-03's smeared density is an honest output because its resolution
kernel is declared; an unsmeared pointwise density is not automatically recovered.

### 4.6 Form-factor path: resolve the coupling vector into physical channels

Assume a model supplies a complete asymptotic identity in the relevant sector,
with normalized `n`-particle states `|theta_1,...,theta_n;c>` and phase-space
measure `dPhi_(n,c)`. Define the same coupling amplitudes

```text
F_(n,c)(p;theta)=<theta_1,...,theta_n;c|Wp>.      (4.10)
```

Insert that identity on both sides of `E_Q(Delta)` in (1.1). On prepared inputs
`p,q`, both routes land in the same scalar matrix entry:

```text
<p,M_W(Delta)q>
  =sum_(n,c) (1/n!) integral dPhi_(n,c)
     1_Delta(E_(n,c)(theta))
     conjugate(F_(n,c)(p;theta))F_(n,c)(q;theta). (4.11)
```

This is attractive in N4w's integrable sine-Gordon branch, where scattering data
and local form factors are already available. It becomes combinatorially heavy as
particle number grows, and it depends on asymptotic completeness and normalization.
For infraparticles, unstable resonances, or generic nonintegrable fields, a short
form-factor sum need not exist or converge rapidly.

## 5. One exact regression discriminates the paths

Use N9a's normalized density

```text
dM(lambda)/G=lambda exp(-lambda)d lambda.         (5.1)
```

Its moments and orthogonal-polynomial chain are

```text
mu_n/G=(n+1)!,
b_n=2n+2,
a_(n+1)=sqrt[(n+1)(n+2)].                        (5.2)
```

The first two chain sites give

```text
J_2=[[2,sqrt(2)],[sqrt(2),4]].                   (5.3)
```

Its two eigenvalues and spectral weights at the first site are

```text
lambda_-=3-sqrt(3),  w_-=(1+1/sqrt(3))/2,
lambda_+=3+sqrt(3),  w_+=(1-1/sqrt(3))/2.        (5.4)
```

Substitution into `sum w lambda^n` gives exactly `1,2,6,24` for `n=0,1,2,3`.
This verifies the moment route without a component expansion of a large bath.

The isolated [multi-route regression](../computation/09b-coupling-measure-routes/README.md)
then applies the exact and two-site measures to the same outputs:

| output | exact continuum | two-site moment chain | verdict |
| --- | ---: | ---: | --- |
| `mu_0,...,mu_3` | matched | matched within `2.3e-15` | exact promised data |
| `mu_4` | `19.2` | `17.28` | stronger moment claim rejected |
| `|K(10)|` | about `0.001584` | about `0.09254` | finite chain misses decay |
| `Sigma(0-)` | `-0.16` | `-0.1066667` | threshold location not preserved |
| bound pole at `e_0=0.1` | `-0.04164364` | `-0.00617503` | short-moment pole is poor |

The moment chain is excellent near `t=0` because its first derivatives are the
matched moments. It is also increasingly accurate for resolvents far from the
spectrum: the self-energy error falls from about `1.64e-2` at `z=-0.25` to
`5.57e-5` at `z=-5`. Neither fact licenses threshold or long-time use.

The Euclidean path has a different ambiguity. Replace the normalized measure by

```text
(1-epsilon)M/G+epsilon delta_L,
epsilon=10^(-8), L=1000.                         (5.5)
```

This remains positive and normalized. On `tau=1,2,4`, its dimensional correlator
differs by at most `4.1e-10`, yet the dimensional fourth moment changes from
`19.2` to about `1619.2`. Thus finite-precision positive-time data do not determine
high-energy moments at comparable precision. Smearing or prior information is a
semantic part of the Euclidean observable, not a numerical afterthought.

## 6. Route selection depends on the requested output

| Requested capability | First useful route | Reusable compression | Principal obstruction |
| --- | --- | --- | --- |
| isolated bound energy/residue | symmetry channels, then off-axis resolvent | channel elimination and reusable `Q` solves | gap closing and hidden inverse cost |
| threshold exponent/long memory | symmetry channels plus long-time or analytic boundary | only coupling-visible sector | long time and boundary conditioning |
| short/intermediate time response | real-time or moment/Lanczos chain | Krylov/nearest-neighbor recursion | recurrence and finite-window resolution |
| nonperturbative Euclidean field data | Euclidean smeared density | positivity and chosen resolution kernel | inverse-Laplace ill-conditioning |
| integrable relativistic spectrum/correlator | form-factor spectral sum | exact particles, selection rules, low-particle terms | completeness and multiparticle growth |
| generic multichannel scattering | symmetry plus resolvent and wave operators | channel blocks | `M_W` alone lacks reference dynamics and flux map |

There is no context-free winner. The path must be chosen after naming the
observable, resolution, accessible operation on the field, and recovery cost.

## 7. Global view: common memory, divergent computational geometries

The global field/mechanics construction is now

```text
symmetry representation and field realization
  -> algebra, state, full dynamics H
  -> operational preparation/coupling W
  -> exact coupling-visible sector C_W
  -> positive operator-valued measure M_W
       |-> off-axis resolvent: bound mechanics
       |-> real boundary + reference dynamics: scattering
       |-> real-time Fourier transform: memory/decay
       |-> Euclidean Laplace transform: smeared nonperturbative spectrum
       |-> moment chain: recursive finite-time/off-axis computation
       `-> form-factor sum: particle-channel field correlation
  -> recover the same named observable
  -> audit construction, approximation, and recovery cost.
```

This also marks a boundary of the global unity. N8c's dephasing Liouvillian is
generally nonself-adjoint. Its projection memory and resolvent still exist by N9,
but they need not arise from a positive spectral measure; Jordan structure or
pseudospectral sensitivity can matter. In reversible equilibrium problems one may
obtain a self-adjoint representation in a weighted inner product, but that bridge
must be constructed model by model. The measure spine therefore unifies the
self-adjoint field/mechanics/particle region, not every collective reduction by
terminological analogy.

Likewise, `M_W` gives the spectral response of one access map. A scattering matrix
compares full and reference dynamics and requires wave operators. A spectral
density peak is not the complete scattering relation.

## 8. Supported branches rather than one forced continuation

The common theorem and regression support several connected probes:

1. **Atom--radiation resolvent/channel probe.**
   [N9c](09c-field-derived-coupling-measure.md) now evaluates the smallest
   regulated fixed-momentum instance: a massive scalar particle--boson fiber with
   Gaussian coupling and vacuum preparation. It derives the complete order-`g^2`
   measure and recovers bound energy, residue, mass curvature, threshold memory,
   and continuum loss. Restoring N4u's internal atom is a re-entry branch, not
   unfinished work inside this benchmark.
2. **Integrable relativistic form-factor probe.** In N4w's sine-Gordon model,
   choose one local access operator and assemble its one- and two-particle spectral
   weights. Check that the breather atom and first continuum threshold reconstruct
   the same Euclidean/real-time correlator within a controlled low-particle
   truncation.
3. **Moment-chain algorithmic probe.** Lift the two-site regression to adaptive
   Jacobi depth with a target-specific error: off-axis self-energy, finite-time
   memory, or a smeared density. Do not optimize one norm and claim all three.
4. **Euclidean-resolution probe.** Apply a declared smearing kernel to a synthetic
   or available correlator and quantify which threshold feature survives its
   resolution. This tests a nonperturbative route without pretending pointwise
   analytic continuation.
5. **Collective nonnormal counterprobe.** On N8c's finite dephased chain, compare
   the true projected Liouvillian memory with any weighted-self-adjoint candidate.
   This determines exactly where the positive-measure global spine stops.

These branches share `C_W` and the named observable but answer different
computability questions. The strongest immediate global comparison is to develop
the atom--radiation and sine-Gordon probes in parallel conceptually: one constructs
`M` through sector resolvents, the other through physical form factors. Their
agreement criteria are common, while their computational resources are genuinely
different.

## Verification ledger

| Obligation | Witness | Verdict |
| --- | --- | --- |
| remove coupling-invisible field directions | spectral-projection calculation (2.2)--(2.4) | exact |
| prove minimality of retained field sector | any reducing range containing `W` also contains every generator | exact |
| realize cyclic sector by `M_W` | same-vector inner product (3.2) | exact up to completion/null quotient |
| split symmetry channels | commuting orthogonal projectors in (4.1) | exact |
| recover measure from resolvent | Poisson approximate identity (4.3)--(4.4) | theorem boundary at endpoints |
| connect moments to chain | Gram identity (4.7) and degree orthogonality | exact infinite chain under domain/nonbreakdown conditions |
| use finite chain at threshold | explicit N9a counterexample | rejected |
| infer high-energy moments from precise Euclidean samples | positive hidden-atom construction (5.5) | rejected at finite precision |
| use form-factor sum | same asymptotic resolution inserted into (1.1) | conditional on completeness/normalization |
| extend positive measure to N8c Liouvillian | self-adjoint spectral theorem unavailable generically | rejected without extra bridge |
| choose one universally cheapest path | route table depends on output and accessible oracle | rejected |

## Edges

- `N9a -> N9b`: pass one evaluated scalar measure; N9b asks how that object can be
  constructed and which information different accesses preserve.
- `N4u -> N9b`: pass the regulated fixed-momentum atom--field sectors and atomic
  resolvent integral as the resolvent/channel candidate.
- `N4w/N4x -> N9b`: pass exact particles and form factors as the asymptotic
  spectral-sum candidate and nonintegrable boundary.
- `N8/N8c -> N9b`: pass real-time response and the nonself-adjoint collective
  counterexample to overgeneralizing positive measures.
- `N9b -> N9c`: pass cyclic compression and route-specific approximation
  boundaries; N9c constructs one field-derived `M_B` and tests bound/threshold
  observables at controlled order `g^2`.
- `N9b -> relativistic form-factor measure probe`: construct one local spectral
  measure from stable particles and continuum states.
- `N9b -> target-specific chain/Euclidean probes`: quantify approximation only for
  a named time, resolvent, or smeared spectral output.
- `N9b -> N7/manuscript synthesis`: pass the minimal cyclic compression, the
  multi-route global view, and the exact boundaries of each computational path.
