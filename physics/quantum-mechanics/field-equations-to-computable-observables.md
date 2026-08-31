# From Field Equations to Computable Observables

This companion records the exploratory continuation of *From Poincare
Representations to Local Free Fields*. The free-field paper constructs how a
particle representation can be realized by local fields. The present question
begins where that construction stops:

> After a field equation, interaction, state, and preparation have been supplied,
> what part of the dynamics must actually be constructed to predict a named
> observable?

This is an exploration manuscript, not a claim that one reduction solves every
Hamiltonian. It retains rejected routes and changes of viewpoint because they
determine the scope of the supported result. Detailed derivations, source
contracts, and executable checks remain in the linked research graph rather than
being copied here.

## 1. A field equation is a presentation, not a prediction

The representation-to-field construction ends with an admissible physical space
and a free evolution. A prediction needs more data:

\[
\mathcal I
  \xrightarrow{\operatorname{Sol}_{\mathcal C}}
\mathcal P
  \xrightarrow{O}
\mathcal Z.
\]

Here \(\mathcal I\) contains the preparation and boundary data,
\(\operatorname{Sol}_{\mathcal C}\) is the response selected by the field complex
and its analytic completion, and \(O\) is an operational observable. The object to
preserve is the composite

\[
F_{\mathcal C,O}=O\circ\operatorname{Sol}_{\mathcal C},
\]

not the appearance of the intermediate equation.

An invertible change of field variables preserves meaning only when the response
and observable are transported together. It may expose locality, sparsity, or
conditioning, but it is not automatically a computation reduction. The complete
cost also includes constructing the transformation, solving in the new
representation, and recovering the observable. This distinction is developed in
[N4q](relativistic-representations-research/nodes/04q-semantic-computability.md).

## 2. The failed universal-solver search changes the question

The first continuation asked whether bounded spectra could be extracted by a
universal algebraic replacement for radial or coordinate calculation. The answer
was negative, but the failure was constructive.

[N4n](relativistic-representations-research/nodes/04n-algebraic-spectrum-bridge.md)
tests several mechanisms on the same capability: hidden symmetry for Coulomb,
normal form for the oscillator, variational computation for the quartic
oscillator, isospectral embedding for integrable many-body systems, and resolvent
methods spanning point and continuous spectra. These mechanisms do not arise from
one discoverable algebra. What survives is an open graph of verified reductions:
each edge must name its input, output, equality or error witness, observable
recovery, and complete cost.

The Dirac--Coulomb branch makes the limitation sharper. [N4o](relativistic-representations-research/nodes/04o-dirac-coulomb-local-graph.md)
constructs the coupled Hamiltonian from the massive representation carrier, a
local \(U(1)\) comparison, and a selected time direction. Curvature obstructs the
free scalar factorization. Rotations still supply an exact invariant
decomposition, but [N4p](relativistic-representations-research/nodes/04p-dirac-angular-reduction.md)
shows that its half-line blocks retain the hard spectral problem. Exact
decomposition is therefore not the same as semantic or computational compression.

This rejected route produces the first view shift:

```text
Do not ask for the algebra that solves a Hamiltonian.
Ask which information a named observable requires and which verified route
constructs exactly that information at lower complete cost.
```

## 3. Mechanics and particles are selected sectors of field dynamics

The next branch asks how mechanical and particle descriptions arise without
deleting the field by assumption.

Let \(J:\mathcal K\to\mathcal H\) be a preparation isometry into the full field
Hilbert space, with

\[
\Pi=JJ^\dagger,\qquad Q=1-\Pi,\qquad B=QHJ.
\]

The departure map \(B\) measures the failure of the prepared sector to be
invariant. Eliminating the complementary sector gives the exact prepared
resolvent

\[
J^\dagger(z-H)^{-1}J
  =\bigl(z-J^\dagger HJ-\Sigma(z)\bigr)^{-1},
\qquad
\Sigma(z)=B^\dagger(z-QHQ)^{-1}B.
\]

This is not yet an approximation: it is a block-resolvent identity on its stated
domain. [N4r](relativistic-representations-research/nodes/04r-field-mechanics-stability.md)
uses it to construct prepared mechanics, reconstruction of the eliminated field,
and observable-stable variation. Difficulty may remain inside \(\Sigma\), so the
identity is a semantic reduction only when the requested observable needs less
than the complete field state.

[N4s](relativistic-representations-research/nodes/04s-field-particle-extraction.md)
reverses the earlier representation-to-field direction. A sharp isolated
translation shell constructs a particle representation; a stable asymptotic
channel constructs a scattering particle; loss of a sharp shell changes the
output into a resonance or infraparticle rather than a badly normalized particle.
Elementary and composite particles use the same spectral criterion.

The following nodes test how much of this picture survives in concrete models:

- [N4t](relativistic-representations-research/nodes/04t-neutral-composite-same-state.md)
  follows one neutral dressed atom through its fiber band, mechanical preparation,
  global spectral selection, and asymptotic channel.
- [N4u](relativistic-representations-research/nodes/04u-effective-mass-route-audit.md)
  compares direct eigenstate differentiation with self-energy curvature on the
  same effective-mass observable. Their common target is exact, while the
  weak-coupling route removes the full Fock eigenproblem only at its declared
  order.
- [N4v](relativistic-representations-research/nodes/04v-relativistic-mass-shell.md)
  shows that a covariant isolated shell constructs its dispersion from one rest
  datum and identifies rest, curvature, and invariant mass under the stated
  differentiability assumptions.
- [N4w](relativistic-representations-research/nodes/04w-sine-gordon-breather-rest-pole.md)
  uses the sine--Gordon breather as an integrable regression: a physical-strip pole
  and residue construct a stable composite mass and fusion channel.
- [N4x](relativistic-representations-research/nodes/04x-nonintegrable-composite-robustness.md)
  separates what survives loss of integrability from what was purchased by
  factorization. Stability can preserve the pole and shell; a channel-destroying
  perturbation shows that symmetry alone need not preserve the old composite.

The portable statement is limited but useful: mechanics, bound states, particles,
and scattering channels are different reductions or spectral regimes of supplied
field dynamics. No single one is the universal primitive of the others.

## 4. Collective dynamics is an observable-scale closure

The field/particle branch does not cover collective response. A collective
variable can become autonomous only after an exact quotient or a controlled scale
limit.

[N8](relativistic-representations-research/nodes/08-collective-diffusion-response.md)
constructs density from a microscopic conserved observable, derives continuity,
and states a same-observable recovery contract for diffusion. The SSEP regression
then tests every part of that contract:

- [N8a](relativistic-representations-research/nodes/08a-ssep-exact-collective-regression.md)
  obtains exact finite-lattice density dynamics, susceptibility, conductivity, and
  the continuum error from the microscopic generator.
- [N8b](relativistic-representations-research/nodes/08b-ssep-current-large-deviation.md)
  constructs a current event and compresses its path law to a scaled generating
  function and one-dimensional dual rate computation.
- [N8c](relativistic-representations-research/nodes/08c-dephased-quantum-ssep.md)
  derives current relaxation and diffusion in a dephased quantum chain, then
  constructs the classical SSEP quotient by eliminating one-hop coherence.
- [N8d](relativistic-representations-research/nodes/08d-two-time-quantum-charge.md)
  holds the finite two-time charge event fixed and verifies convergence of its
  complete law, not only its variance.

This branch supplies the second view shift:

```text
“First” and “second” quantization do not form an explanatory ladder.
Different effective dynamics arise when different observables, sectors, and
scales close under the same underlying evolution.
```

## 5. One coupling-visible measure unifies several queries

[N9](relativistic-representations-research/nodes/09-observable-dynamics.md)
classifies three possibilities after selecting an observable:

1. its kernel is invariant, so the observable descends to autonomous dynamics;
2. descent fails, so exact elimination produces memory and self-energy;
3. a scale limit makes the memory asymptotically local and produces a Markov or
   kinetic closure.

For a preparation \(J\), the departure map constructs the positive
operator-valued measure

\[
M_B(\Delta)=B^\dagger E_{QHQ}(\Delta)B.
\]

Its Stieltjes and Fourier transforms are

\[
\Sigma(z)=\int\frac{M_B(d\lambda)}{z-\lambda},
\qquad
K(t)=\int e^{-it\lambda}M_B(d\lambda).
\]

Thus the prepared resolvent, memory kernel, threshold boundary, and moment chain
are different queries on one coupling-visible object. [N9a](relativistic-representations-research/nodes/09a-threshold-spectral-measure.md)
tests this unity in a rank-one threshold model. [N9b](relativistic-representations-research/nodes/09b-coupling-measure-routes.md)
then compares symmetry-channel, resolvent, real-time, moment/Lanczos, Euclidean,
and form-factor routes. They construct or observe the same target with different
resolution, conditioning, and recovery costs; no route dominates independently of
the requested output.

### 5.1 A field-derived same-model benchmark

The decisive bench asks whether \(M_B\) can be constructed from an actual field
Hamiltonian and preparation without solving the complete dressed Fock problem,
then used for both a bound and an open-channel observable.

[N9c](relativistic-representations-research/nodes/09c-field-derived-coupling-measure.md)
constructs the order-\(g^2\) measure of a regulated massive scalar model. Exact
boson-number, rotational, and dispersion reductions turn the leading return
coefficient into one radial energy measure. Its transforms yield a bound pole
shift, residue/effective-mass data, memory and threshold behavior, and a moment
chain without reconstructing the dressed state.

[N9d](relativistic-representations-research/nodes/09d-operational-bound-open-channel.md)
enlarges the prepared space to contain ground and excited inputs. The same
operator-valued measure then controls a bound observable and a finite-time emitted-
boson detector event. The continuum boundary is interpreted only through that
constructed event; it is not silently renamed an \(S\)-matrix or exponential
lifetime.

The original bridge defect was that this Hamiltonian and its Gaussian profile had
been supplied independently of the free-field construction. [N9e](relativistic-representations-research/nodes/09e-scalar-interaction-provenance.md)
closes the defect for one model:

```text
massive scalar positive shell
  -> smeared free field
  -> declared mobile two-level coupling
  -> self-adjoint translation-covariant Hamiltonian
  -> exact total-momentum fiber
  -> departure map and the N9d measure.
```

The profile, two-level system, coupling, and nonrelativistic matter dynamics remain
additional physical inputs. The bridge is model-local, not a consequence of
Poincare representation theory.

### 5.2 Prediction requires an error-bearing window

A complete perturbative coefficient is not automatically a finite-coupling
prediction. [N9f](relativistic-representations-research/nodes/09f-certified-observable-window.md)
constructs combined parity before estimating, then obtains a controlled ground-
energy window and an exact finite-time detector remainder. The norm route becomes
vacuous at the earlier long-time rate probe, which records a genuine limitation
rather than an invitation to call the coefficient a lifetime.

[N9g](relativistic-representations-research/nodes/09g-kinetic-scale-reconstruction.md)
constructs the kinetic generator selected by the same measure and proves the
exponential law in an exact one-excitation Friedrichs comparator. Transfer to the
full recoil model remains obstructed by a named multiparticle remainder and cross
term. This is the present stopping point: the comparator explains the candidate
law, but it does not certify the exact detector event.

## 6. Global synthesis

The exploration supports the following coherent route:

```text
symmetry and representation
  -> admissible free state content
  -> local field realization and free quantum field
  -> separately supplied interaction, state, and preparation
  -> observable-selected departure or quotient
       |-> invariant sector: bound or stable-particle dynamics
       |-> noninvariant sector: exact memory and self-energy
       |-> scale-separated sector: collective or kinetic closure
       `-> asymptotic sector: scattering channel
  -> recover the same named observable
  -> audit the complete construction and recovery cost.
```

The common part is not a universal solver. It is a construction discipline:

- identify the semantic object that must be preserved;
- quotient only distinctions invisible to that object;
- expose memory when the quotient is not dynamically invariant;
- use symmetry, sparsity, locality, conditioning, or recursion where they reduce
  the complete route;
- require a same-input equality or controlled error at recovery;
- stop when a special model no longer changes the global claim.

## 7. Supported frontier and open boundary

The supported result has three strengths:

1. exact structural identities for projection, memory, resolvent, cyclic measure,
   and observable descent;
2. exact or controlled model reductions for the SSEP/dephasing regressions and the
   regulated scalar benchmark;
3. complete leading perturbative coefficients plus bounded ground and short-time
   finite-coupling windows in that scalar model.

The following remain open and must not be inferred from the current constructions:

- a universal interaction selected by symmetry or a free field equation;
- a general algorithm discovering hidden algebras or optimal reductions;
- full finite-coupling dressed measures without solving the hard residual problem;
- a certified long-time decay law for the exact recoil detector event;
- resonance poles or normalized scattering amplitudes for that model;
- massless infrared, physical atomic, relativistic-matter, or higher-spin
  interaction extensions.

These are re-entry conditions, not missing paragraphs. The canonical node graph
retains the detailed calculations, failed paths, source provenance, and executable
checks from which any later focused paper must be composed.
