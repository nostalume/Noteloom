# Research Plan: Representation, Fields, and Computable Observables

Status: active research graph; known spine with bounded discovery at the
generative-construction frontier

## Research target

The current question is not whether familiar relativistic equations can be
formalized. It is whether a physical representation request and a finite resource
budget can generate reusable local operations, expose their obstructions, and
then reduce a named observable without hiding the whole computational cost.

The candidate reusable tool is an equivariant obstruction-resolution calculus:

```text
physical representation and capability
  -> orbit and little-group fiber
  -> finite carrier and operation budget
  -> compute carrier, lift, residual, and characteristic obstructions
  -> generate the smallest admissible equation/complex or refusal
  -> recover the same physical fiber
  -> combine supplied dynamics, preparation, and observable
  -> reduce to a reusable response or spectral object
  -> compute the named output and audit complete cost.
```

Symmetry constrains admissible representations and operations. It does not alone
generate the carrier, action, Hamiltonian, interaction, state, preparation,
observable, boundary condition, or approximation regime.

## Worktable ownership

- `nodes/` owns bounded research questions, constructions, derivations,
  challenges, and open boundaries.
- `computation/` owns substantial executable calculation and its compact
  reproducibility contract.
- `sources/` owns source extraction and theorem contracts; [sources.md](sources.md)
  is only their index and source-gap list.
- `results/` owns cross-node scientific results whose verdict changes a research
  claim or validity boundary.
- [poincare-to-free-fields.typ](../poincare-to-free-fields.typ),
  [observable-visible-spectral-measures.typ](../observable-visible-spectral-measures.typ),
  and [field-equations-to-computable-observables.md](../field-equations-to-computable-observables.md)
  are linear syntheses of supported sub-spines.
- Manuscript repair, template/code audits, migration ledgers, and execution order
  live only in the ignored private plan
  `.agents/plan/research-worktable-maintenance.md`.

Git owns superseded state. This directory is not an editorial-history archive.

## Global semantic spine

```text
Poincare representation
  -> physical massive-spin or massless-helicity fiber
  -> finite covariant carrier and local realization
  -> action, quantum algebra, state, and full dynamics [additional inputs]
  -> preparation/observable constructs a selector
  -> test selector under evolution
       |-> invariant sector: bound state or stable particle
       |-> noninvariant sector: memory/self-energy, pole or resonance
       |-> scale-separated sector: collective autonomous law
       `-> asymptotic intertwiner: scattering
  -> recover the same named observable and compare complete route cost.
```

Field equations are intermediate realization objects, not predictive endpoints.
“First” and “second” quantization name restricted constructions inside this spine;
they do not define an ontological ladder.

## Branch index

| Branch | Canonical packets | Supported output and present boundary |
|---|---|---|
| determination and representation spaces | [N1](nodes/01-determination-boundary.md), [N2](nodes/02-three-representation-spaces.md), [spin/helicity](nodes/02a-spin-and-helicity.md), [Lorentz carriers](nodes/02b-lorentz-carriers.md) | types physical, group-function, coefficient, and field spaces; constructs massive spin and null helicity fibers and finite Lorentz carriers |
| orbitwise realization | [N3](nodes/03-realization-bridge.md), [massive spin one](nodes/03a-massive-spin-one.md), [massless helicity one](nodes/03b-massless-helicity-one.md), [details](nodes/03c-realization-details.md) | constructs the little-group-intertwiner/cohomology bridge; group functions remain optional packaging |
| finite local free fields | [N4](nodes/04-local-symbol-extension.md), [polynomial complexes](nodes/04a-polynomial-complex-details.md), [half-integer potentials](nodes/04b-half-integer-potential.md), [action completion](nodes/04c-action-completion-audit.md), [computation interface](nodes/04d-computation-interface.md) | supports separate finite complex chiral fields and declared bosonic/fermionic potential families; action and source data remain additional |
| causal and one-particle completion | [N4e](nodes/04e-maxwell-green-construction.md) through [N4m](nodes/04m-finite-integer-spin-field-machine.md), plus [N4y](nodes/04y-quantization-recovery-bridge.md) and [N4z](nodes/04z-fermionic-car-coincidence.md) | constructs bounded Green/source quotients, positive-frequency spaces, and free CCR/CAR recovery on declared source-generated images |
| mechanics and particle extraction | [N4n](nodes/04n-algebraic-spectrum-bridge.md) through [N4x](nodes/04x-nonintegrable-composite-robustness.md) | compares problem-local reductions, projected resolvents, stable shells, exact integrable regression, and controlled deformation; no universal spectral solver |
| comparison and equivalence | [N5](nodes/05-low-spin-comparison.md), [N7](nodes/07-equivalence-boundary.md) | separates fiber, local-complex, response, quantum, deformation, and predictive equivalence; textbook equations are bounded regressions |
| collective dynamics | [N8](nodes/08-collective-diffusion-response.md) through [N8d](nodes/08d-two-time-quantum-charge.md) | constructs diffusion/large-deviation and dephased quantum-to-SSEP tests; finite-size regression does not prove arbitrary nonequilibrium closure |
| observable dynamics | [N9](nodes/09-observable-dynamics.md) through [N9g](nodes/09g-kinetic-scale-reconstruction.md) | builds common cyclic/spectral objects for bound, open, memory, and kinetic outputs; full dressed, multichannel, and long-time transfer remain open |
| generative obstruction calculus | [N10](nodes/10-equivariant-obstruction-resolution.md) through [N10w](nodes/10w-first-order-factorizer.md) | generates bounded operation grammars, residual repairs, presentation selection, constrained response, observable quotient, and visible measure; carrier-global generation remains open |

Node numbers name research regions, not permission gates or manuscript sections.
Read only the active packet, its named inputs, and the compact computation result
needed for the current question.

## Supported frontier

### Representation to free field

For every separate finite massive spin or massless helicity in the declared
four-dimensional complex setting, the worktable constructs the physical
little-group fiber, a finite covariant realization, its local symbol or complex,
and the standard-momentum physical kernel/cohomology. Selected symmetric bosonic
and fermionic potential families also have causal/source quotients and free
one-particle recovery. Countable completion, most real structures, mixed symmetry,
and interacting higher-spin dynamics are not inferred.

### Field, mechanics, and observable reduction

The mechanics branch rejects a fixed universal reduction method. It retains a
problem-local graph whose edges must preserve the named observable and expose
construction, solution, and recovery cost. The field/particle branch supports
stable-shell and exact-regression examples while distinguishing bound poles,
resonances, infraparticles, scattering sectors, and collective limits.

The N9 branch shows that one coupling-visible measure can feed Stieltjes,
Fourier, finite-time, and continuum-boundary operations after the preparation-
dependent energy maps are kept explicit. The exact dressed measure, generic
scattering matrix, and uncontrolled long-time rate do not follow.

### Generative construction

N10c--N10g form a genuine residual-and-repair generator once an operation grammar
is supplied. N10m and N10w generate bounded symmetric, exterior, and Clifford
grammar cells from free-power or first-order-factorization requests. N10n--N10r
construct carrier-relative alternatives and their cost/refusal certificates.
N10s--N10v connect physical preparation and curvature observables to a reusable
positive radial measure and its bound/open transforms.

This passes bounded regression, transfer, use, and refusal tests. It is not yet a
carrier-global compiler: mixed-symmetry enumeration, carrier selection from
particle data, native compatible-source physics, real-structure selection,
interactions, and finite-coupling control remain outside the result.

## Scientific result index

- [Semantic-gap audit](results/02-semantic-gap-audit.md): classifies unsupported
  transitions in the early representation bridge.
- [Low-spin comparison](results/03-low-spin-comparison.md): compares the massive
  and massless spin-one physical fibers.
- [Invariant-route audit](results/04-invariant-route-audit.md): evaluates
  readability, construction, semantic computation, and simplicity of the early
  spine.
- [Computability-endpoint audit](results/05-computability-endpoint-audit.md):
  determines where the representation route reaches actual observables and where
  reduction fails.
- [Field-to-observable synthesis](results/06-field-to-observable-synthesis-audit.md):
  relates field realization to supplied dynamics, preparation, and observables.
- [Construction-origin audit](results/07-construction-origin-audit.md): separates
  genuine generated tools from formal or handwritten shells in N10.

These remain research results even when named “audit” because their verdicts alter
scientific claims and downstream boundaries.

## Open boundaries

- carrier-global and mixed-symmetry operation generation;
- completed countable-spin topology and uniform operator domains;
- real/parity structures beyond declared cells;
- native interacting sources and higher-spin matter couplings;
- CAR detector measures and fermionic graph signs;
- finite-coupling dressed poles, resonances, and full scattering matrices;
- anisotropic or nonmonotone visible-measure reductions;
- measured runtime/conditioning advantage over complete baseline routes;
- density of compact projected-source images where still unproved;
- focused literature/novelty evaluation for the manufactured observable paper.

Open boundaries re-enter only when the user selects them or when a contradiction
undermines a supported edge. More examples do not reopen a branch by themselves.

## Node and computation contract

A supported node exposes question, presumptions, material bindings, construction,
semantic computation, output, checks, downstream edge, and open boundary. A
nontrivial equation must arise from typed inputs, an explicit operation, a common
target, and an equality or obstruction witness.

Substantial expansion, numerical work, graph enumeration, simulation, or plotting
belongs in `computation/<node>/`. Its README names the question, program, inputs,
checks, compact output, and limitation. The conceptual node retains the smallest
decisive equality; it does not paste raw execution traces.

## Maintenance rule

Correct or supersede packets in place. Keep current navigation here, provenance in
source packets, detailed claims in nodes, and executable evidence in computation
packets. Do not append delivery chronology, migration records, formatting audits,
or repeated node summaries to this file.
