# N9a — One Spectral Measure Across Bound, Memory, and Scattering Regimes

Status: rank-one threshold bridge constructed and numerically verified; lift to a
field-derived, operator-valued coupling measure remains open  
Consumes: [N4n spectral bridge](04n-algebraic-spectrum-bridge.md),
[N4r field/mechanics projection](04r-field-mechanics-stability.md),
[N4s particle extraction](04s-field-particle-extraction.md),
[N9 observable dynamics](09-observable-dynamics.md), and
[threshold-memory contracts](../sources/threshold-memory-contracts.md)  
Produces: one internally constructed coupling measure whose Stieltjes and Fourier
transforms give the bound pole, dressing weight, exact memory, continuum density,
and one-channel scattering boundary

## Research contract

- **Question:** can one constructed eliminated-field object explain both the
  mechanical bound regime and the open scattering/memory regime, rather than
  treating them as unrelated calculations?
- **Presumptions:** a self-adjoint one-level Friedrichs Hamiltonian on
  `C direct-sum L^2([0,infinity),d lambda)`, a bounded rank-one coupling, and the
  standard wave-operator contract when the boundary ratio is called scattering.
- **Output:** the coupling spectral measure, its exact time and resolvent
  transforms, the below-threshold pole/residue, the continuum boundary density,
  and a reproducible density crossing the threshold.
- **Boundary:** the node does not derive the measure from an interacting field,
  prove a second-sheet resonance pole, or solve a multiparticle/multichannel
  problem. These are the next model-local obligations.

## 1. Why N9 needs a model rather than another complement formula

N9 proved that time memory and the resolvent self-energy use the same eliminated
propagator. N4n already observed that one resolvent can carry discrete atoms and a
continuous density. Neither result computes the common object or tests whether it
actually saves work.

The smallest nontrivial test retains one prepared amplitude and eliminates one
continuum. It is restrictive enough to calculate, yet it contains the threshold
operation that separates a bound state from an open channel.

## 2. Construct the coupling measure from the eliminated dynamics

Let

```text
H = P H direct-sum Q H,
P H = C,
Q H = L^2([0,infinity),d lambda).
```

The continuum Hamiltonian `H_Q` multiplies by `lambda`; the bare prepared energy
is `e_0`; and `B:P H->Q H` is the departure map. On a pair `(p,u)`, construct

```text
H(p,u)=(e_0 p+B^dagger u, Bp+H_Q u).             (2.1)
```

Let `E_Q(Delta)` be the spectral projection of `H_Q`. The eliminated field enters
the prepared sector through the positive measure

```text
M(Delta)=B^dagger E_Q(Delta)B.                   (2.2)
```

Positivity is computed on the same prepared amplitude:

```text
<p,M(Delta)p>
  =<E_Q(Delta)Bp,E_Q(Delta)Bp>
  =||E_Q(Delta)Bp||^2 >=0.                       (2.3)
```

For a one-dimensional prepared sector, `M` is scalar. If `Bp` has wavefunction
`b(lambda)p`, then

```text
dM(lambda)=m(lambda)d lambda,
m(lambda)=|b(lambda)|^2.                         (2.4)
```

This construction is coordinate-free until the final spectral representation of
`H_Q`; `m` is not an imported line shape but the energy distribution of the same
departure vector `Bp`.

## 3. One measure has a time transform and a spectral transform

The coupling memory and self-energy are

```text
K(t)=B^dagger exp(-itH_Q)B
    =integral exp(-it lambda)dM(lambda),          (3.1)

Sigma(z)=B^dagger(z-H_Q)^(-1)B
        =integral dM(lambda)/(z-lambda).          (3.2)
```

Our sign convention makes `Im Sigma(z)<=0` for `Im z>0`. Direct integration of
the same exponential gives

```text
Sigma(z)=-i integral_0^infinity exp(izt)K(t)dt,  Im z>0.   (3.3)
```

This is semantic coincidence, not analogy: (3.1) and (3.2) apply two transforms
to the same positive measure (2.2).

The Schrödinger equation verifies how (3.1) enters prediction. Its two blocks are

```text
i dot p=e_0 p+B^dagger u,
i dot u=Bp+H_Q u.                                (3.4)
```

Solve the second block and substitute that same solution into the first:

```text
u(t)=exp(-itH_Q)u(0)
     -i integral_0^t exp[-i(t-s)H_Q]Bp(s)ds,

i dot p(t)=e_0p(t)+B^dagger exp(-itH_Q)u(0)
     -i integral_0^t K(t-s)p(s)ds.               (3.5)
```

Thus the measure describes the field information that leaves the prepared level,
evolves with a definite continuum energy, and returns.

## 4. Below threshold: construct the bound pole and recover its field part

For real `E<0`, solve `(H-E)(p,u)=0`. The continuum equation gives

```text
u=(E-H_Q)^(-1)Bp.                                (4.1)
```

Substituting this recovered component into the prepared equation leaves one
scalar obligation:

```text
f(E)=E-e_0-sigma(E)=0,
sigma(E)=integral dM(lambda)/(E-lambda).          (4.2)
```

The derivative is not guessed from a level-repulsion picture:

```text
sigma'(E)=-integral dM(lambda)/(E-lambda)^2 <=0,
f'(E)=1-sigma'(E)>0.                             (4.3)
```

Hence at most one root lies below the threshold. Its prepared probability follows
from normalizing the same recovered vector (4.1):

```text
||u||^2
  =|p|^2 integral dM(lambda)/(E-lambda)^2
  =-sigma'(E)|p|^2,

Z_b=|p|^2=1/[1-sigma'(E_b)].                     (4.4)
```

The residue of the prepared resolvent and the norm of the recovered field cloud
are therefore the same computed quantity.

## 5. On the continuum: construct density and scattering boundary

Assume `dM=m(E)dE` has the required boundary regularity. The two boundary values
are

```text
sigma(E+i0)=Delta(E)-i pi m(E),
sigma(E-i0)=Delta(E)+i pi m(E).                  (5.1)
```

The prepared resolvent is

```text
G_P(z)=1/[z-e_0-sigma(z)].                       (5.2)
```

Taking its boundary imaginary part constructs the prepared continuum density:

```text
rho_P(E)=m(E)/{[E-e_0-Delta(E)]^2+[pi m(E)]^2}.  (5.3)
```

When a below-threshold pole exists, the prepared spectral measure is

```text
Z_b delta(E-E_b)+rho_P(E)dE;                    (5.4)
```

otherwise the example below is purely continuous.

Define the boundary denominators

```text
D_+(E)=A(E)+i pi m(E),
D_-(E)=A(E)-i pi m(E),
A(E)=E-e_0-Delta(E).                             (5.5)
```

Under TM-04's one-channel wave-operator contract, our incoming/outgoing convention
gives

```text
S(E)=D_-(E)/D_+(E).                              (5.6)
```

Because both denominators are boundary values of the same measure and are complex
conjugates on the real axis, (5.6) immediately computes `|S(E)|=1`. A real zero
of `A(E)` marks an on-shell phase center; it is not by itself a resonance pole.
That stronger claim requires a zero of the analytically continued denominator on
the appropriate second sheet.

## 6. One explicit measure crosses the threshold

Normalize the threshold and cutoff scale to `0` and `1`, and choose

```text
m(lambda)=G lambda exp(-lambda),
G=0.16.                                          (6.1)
```

The transforms are evaluated without a continuum-component expansion:

```text
K(t)=G integral_0^infinity lambda exp[-(1+it)lambda]d lambda
    =G/(1+it)^2,                                 (6.2)

Delta(E)=G[E exp(-E)Ei(E)-1],                    (6.3)
```

where `Ei` is the real principal-value exponential integral in (6.3) for `E>0`.
At the threshold,

```text
sigma(0-)=-integral_0^infinity m(lambda)/lambda d lambda=-G,
f(0-)=G-e_0.                                     (6.4)
```

Since `f(-infinity)<0` and (4.3) makes it strictly increasing:

```text
e_0<G  -> exactly one below-threshold bound state;
e_0>G  -> no below-threshold bound state.        (6.5)
```

At `e_0=G`, the formal root reaches zero but is not normalizable:

```text
integral_0^infinity m(lambda)/lambda^2 d lambda
  =G integral_0^infinity exp(-lambda)/lambda d lambda
  =infinity.                                     (6.6)
```

The threshold does not merely move an eigenvalue; it changes the admissible
spectral type.

## 7. Same measure, two sides of the threshold

The isolated [regression computation](../computation/09a-threshold-spectral-measure/README.md)
uses only scalar bisection and one-dimensional adaptive quadrature.

| quantity | bound choice `e_0=0.10` | open choice `e_0=0.60` |
| --- | ---: | ---: |
| below-threshold energy `E_b` | `-0.041643641293168` | none by (6.5) |
| prepared bound weight `Z_b` | `0.769732542717280` | `0` |
| prepared continuum weight | `0.230267457288710` | `1.000000000006340` |
| on-shell center `A(E_*)=0` | not used | `0.453736006803024` |
| coupling density `m(E_*)` | not used | `0.046117757707016` |
| boundary width scale `2 pi m(E_*)` | not used | `0.289766417624793` |

For the bound choice, `Z_b+integral rho_P=1` to `6.0e-12`. For the open choice,
`integral rho_P=1` to `6.4e-12`; sampled boundary ratios obey `|S|-1` to
`2.3e-16`. Refining the continuum cutoff from `30` to `40` changes either weight
by less than `6e-12`.

These are not two independent Hamiltonians in the relevant sense. They use the
same continuum, coupling vector, spectral measure, self-energy, and memory kernel;
only the position of the bare prepared level changes.

## 8. Exact memory rejects the simplest Markov estimate

Equation (6.2) gives

```text
|K(t)|=G/(1+t^2),
K(t)~-G/t^2.                                     (8.1)
```

The memory is absolutely integrable, but the first moment required by N9's
Lipschitz Markov bound is

```text
integral_0^T t|K(t)|dt
  =(G/2)log(1+T^2),                              (8.2)
```

which diverges. Therefore this example supports an inexpensive pole computation
while refusing that particular time-local error estimate. A different scaling,
subtraction, or nonlocal reduced law would be needed; integrability of memory
alone does not license Markov closure.

More generally, a threshold density `m(E_th+x)~C x^alpha` transforms, after
`u=tx`, into a `t^{-(alpha+1)}` contribution under the regularity assumptions of
TM-03. The explicit `alpha=1` calculation above verifies the mechanism without
outsourcing it to that general statement.

## 9. Relation to mechanics, particles, and fields

This construction sharpens the global view:

```text
full field dynamics plus preparation
  -> departure vector Bp
  -> its Q-energy distribution M
       |-> Stieltjes transform: bound pole or continuum boundary
       |-> Fourier transform: exact return memory
       `-> recovered Q component: dressing or open-channel amplitude.
```

- **Bound mechanics:** a pole below the field threshold yields one autonomous
  eigenstate after including its recovered field dressing; the bare prepared
  amplitude alone remains memory-bearing.
- **Stable particle:** the atom in the full spectral measure is the sharp shell
  case of N4s, not a field-free coordinate state.
- **Scattering:** above threshold the same prepared excitation is distributed over
  continuum energies and the two boundary values construct its phase response.
- **Field theory:** constructing `M` means computing how the chosen preparation
  overlaps the eliminated field spectrum. In a realistic theory that can be the
  hard correlator or spectral-density problem; the present node has compressed
  the consequences of `M`, not its field-theoretic construction.

Thus “mechanical” and “field” descriptions are not separated by quantization
order. They are spectral regimes and operational selections inside one dynamics.

## 10. Computability and construction audit

| Obligation | Construction | Verdict |
| --- | --- | --- |
| eliminate the continuum | solve the `Q` block once and preserve its spectral measure | exact |
| preserve semantics across time/spectrum | Fourier and Stieltjes transforms act on the same `M` | exact |
| find a bound state | one monotone scalar root | cheap in this rank-one model |
| recover the field dressing | apply `(E-H_Q)^(-1)B` and normalize by the same derivative | exact |
| obtain open spectral output | one boundary density and scalar quadrature | cheap here |
| call an on-shell peak a resonance pole | would require second-sheet continuation | rejected |
| infer Markov dynamics from integrable memory | first memory moment diverges | rejected |
| construct `M` from a realistic field | not supplied by the Friedrichs reduction | open/hard |
| include several channels or multiparticle creation | scalar measure is insufficient | open |

The genuine reusable object is the coupling measure `M`, not the special
exponential density. [N9b](09b-coupling-measure-routes.md) now proves the minimal
coupling-visible field sector and compares symmetry-channel, resolvent, real-time,
moment-chain, Euclidean, and form-factor routes to `M`. It rejects a forced single
continuation: the remaining field-derived probes have different observables and
conditioning.

## Edges

- `N4n -> N9a`: replace the qualitative atom/continuum unity by one evaluated
  spectral measure and normalization check.
- `N4r -> N9a`: specialize its exact prepared projection and self-energy to a
  rank-one measure while retaining the dressing recovery map.
- `N4s -> N9a`: identify the sharp atom and continuum boundary as stable-particle
  and scattering regimes of the same full spectral measure.
- `N9 -> N9a`: evaluate its shared memory/self-energy object across an actual
  threshold and test the Markov moment.
- `N9a -> N9b`: pass the evaluated scalar density for a multi-route construction
  and information-loss audit.
- `N9a -> N7/manuscript synthesis`: pass the computed bound/open unity and its
  explicit computational boundary.
