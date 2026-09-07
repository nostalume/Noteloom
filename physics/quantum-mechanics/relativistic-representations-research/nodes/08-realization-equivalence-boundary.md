# Equivalence and dynamical reduction boundary

Status: equivalence is typed by observable level; only problem-local mechanical
and collective reductions are supported

## Obstruction

Equal spin/helicity counts do not imply equal locality, sources, causal response,
quantum algebra, dynamics, observables, or cost. Likewise, a free field equation
does not make a supplied interacting Hamiltonian or collective generator
computable.

## Equivalence ladder

| Level | Required witness |
| --- | --- |
| physical fiber | unitary little-group intertwiner |
| local realization | chain map inducing fiber-cohomology isomorphism |
| source/response | quotient maps commuting with Green response |
| free quantum field | unitary map preserving CCR/CAR and vacuum |
| interacting theory | map preserving supplied dynamics and observables |
| computation | identical observable within error and complete-route cost |

A lower witness never licenses a higher claim. Maxwell potentials and chiral
curvatures, for example, recover the same null helicities but have different field
and source interfaces. Higher-spin screen-rank agreement proves only
physical-fiber equivalence.

## Common mechanical reduction

Supply `(H,P,O)`: dynamics, prepared sector, and observable. With `Q=1-P`, define

```text
B=QHP,
Sigma(z)=PHQ(z-QHQ)^(-1)QHP.
```

Block elimination computes, wherever the resolvent exists,

```text
P(z-H)^(-1)P
 =(z-PHP-Sigma(z))^(-1).
```

This preserves the prepared response but does not solve `QHQ`. It is useful only
when symmetry, sparsity, integrability, locality, or controlled approximation
makes

```text
discovery + construction + reduced solve + recovery + error
```

cheaper than the complete route.

Bound states are discrete normalizable poles and retain their radial spectral
problem after angular reduction. Stable particles are isolated field shells;
resonances are continued poles; scattering requires open-channel boundary values;
infraparticles have no isolated one-particle pole. Substituting one regime for
another changes the physical question.

Runge--Lenz closure, Dirac angular reduction, breather poles, neutral-composite
resolvents, and nonintegrable deformations remain problem-local witnesses. They do
not form a universal hidden-algebra finder.

## Collective reduction

For microscopic dynamics `X_t` and proposed variable `Y=pi(X)`, autonomous closure
requires a semigroup `S_t` satisfying

```text
E[f(pi(X_t)) | pi(X_0)=y]=(S_t f)(y)
```

exactly or in a controlled limit. Failure measures memory. A conserved-density
mean law such as

```text
partial_t rho=div(D(rho)grad rho)
```

does not determine fluctuations; a tilted generator or large-deviation functional
must construct their additional mobility/noise data.

SSEP, dephased quantum hopping, and two-time charge statistics test exact closure,
controlled coherence elimination, and preservation of the same observable. They
are three witnesses of one obstruction, not a “third quantization.”

## Retained output and boundary

Output: the witness level needed for replacement, a projected response or
collective generator, and a refusal when closure, error, or total cost fails.

[The visible-measure node](11-visible-spectral-measure.md) compresses a prepared
response and certifies its bound/open use. No universal transformation discovery,
complete dressed Fock solution, arbitrary nonequilibrium closure, or generic
scattering matrix is claimed.
