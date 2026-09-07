# Open-tree compiler `C_open-v1`: frozen contract and interim disposition

Status: restricted support; exact recovery and bounded use are supported, while
independent cross-family transfer and global field/mechanics leverage remain open

Synthesis trigger: user-requested interim synthesis after the compiler and its
examples had already been co-developed.

Cutoff: 2026-09-06, computation manifest
`a637c86d08541acfe538917176a0be6b5f01674b`.

## Frozen local contract `C_open-v1`

### Capability and preserved semantics

Given a finite labelled Abelian open matter line, an action-generated insertion
jet, noncharacteristic proper-subset kernels, a physical endpoint quotient, and a
finite resource budget, construct a shared-state evaluation that preserves the
complete ordered-history amplitude and its declared detector consumer.

The candidate is the pair

```text
state = (consumed label subset, algebra normal form),

step(state, remaining insertion)
 -> next state + transition/contact contribution.
```

For commuting scalar insertions the algebra normal form is scalar. For an ordered
fermion line it is the exterior representative of the Clifford product. Endpoint
amputation and Ward contraction are operations on the same state, not independent
post-processing expansions.

The frozen output is

```text
CompileOpenTree(action jet, labelled insertions, endpoint data,
                detector request, budget)
 -> shared states + characteristic amplitude/effect
    + ordered-history recovery + Ward/refusal certificate
    + detector result + complete declared cost
 | refusal(characteristic internal kernel, unsupported algebra/arity,
           failed shell/gauge/positivity, or budget).
```

No rule may be added to this core in response to a bench. Model-specific
kinematics, shell densities, trace/parity resources, and detector supports are
adapters and must not change the state or step semantics.

### Independent claim dimensions

1. **Recovery:** shared-state evaluation equals the explicit ordered-history sum.
2. **Quotient correctness:** endpoint Ward images lie in the external kinetic
   ideal and vanish after admitted shell projection.
3. **Algebra transfer:** the same subset-state semantics survives replacement of
   scalar coefficients by an order-sensitive Clifford/exterior normal form.
4. **Use:** the compiled output reaches the same positive detector effect or
   measure as explicit histories.
5. **Leverage:** construction, certification, and observable recovery together
   cost less than the declared explicit-history baseline on a named domain.

### Domain and exclusions

Admitted: finite labelled Abelian scalar or parity-doubled spin-`1/2` open trees,
singleton current insertions and action-generated pair contacts, invertible proper-
subset kernels, declared orthogonal serialization frame, exact shell/Ward algebra,
nonnegative detector weights, and finite-resolution `2+1` event measures.

Excluded: loops, closed fermion cycles, non-Abelian color ordering, internal
factorization poles, single-parity odd traces, absolute flux normalization,
infrared-inclusive charged scattering, arbitrary carrier discovery, and bound-
state spectral computation.

### Falsifiers and promotion conditions

- A matched exact history whose shared-state value differs rejects recovery on
  that domain.
- A nonzero projected Ward residual rejects quotient correctness there.
- A new algebra requiring a change to subset-state or step semantics rejects the
  frozen transfer claim; an adapter-only change does not.
- A negative or representative-dependent readout rejects use on that detector
  domain.
- Equal-observable complete cost greater than or equal to the fair baseline
  rejects leverage for that bench without rejecting correctness.
- Promotion of transfer requires a post-freeze structurally distinct bench using
  the unchanged core. Promotion of global leverage additionally requires analytic
  and observable-recovery cost, not only graph/product counts.

## Decision kernel `K-research-1`

Admit a packet only when its target dimension, domain, operation, witness,
implementation/source revision, and permitted consequence are explicit. Exact
in-domain counterexamples dominate positive examples; proof/test conflict creates
`Dx`; regression cannot promote transfer; transfer cannot promote leverage; and a
cost failure does not weaken mathematical correctness. Source contracts delimit
hypotheses but do not prove internal generation or novelty. Cache-sensitive timing
cannot decide leverage when an exact stable operation count is available.

Allowed dispositions are `supported`, `restricted`, `contested`, `rejected`, and
`underdetermined`, each attached to `D+`, `D-`, `D?`, or `Dx` rather than used as a
global scalar label.

## Active evidence closure `A_2026-09-06`

### `E-OT-01` — scalar history recovery

- Target: recovery and quotient correctness.
- Operation: compare explicit singleton/contact histories with the subset
  recurrence and contract each labelled polarization.
- Witness: node 27 equations (27.8)--(27.10), plus
  `tests/test_worldline_quotient.py` and `tests/test_scalar_line_transfer.py`.
- Result: exact equality on the rational four-photon fixture; `66` histories are
  recovered from `16` states and `56` transitions; endpoint residuals vanish.
- Warrant/boundary: exact deductive witness with regression certificates; finite
  Abelian scalar open trees with invertible proper-subset kernels.
- Permitted consequence: supports recovery/quotient correctness, not transfer.

### `E-OT-02` — characteristic scalar descent and cost

- Target: quotient correctness, fixed-event use, and bounded leverage.
- Operation: move endpoint amputation inside the recurrence, compare its Ward ideal
  with the explicit endpoint identity, and attach a nonnegative event weight.
- Witness: node 29 equations (29.2)--(29.14),
  `tests/test_physical_scalar_amplitude.py`, and
  `tests/test_prepared_event_effect.py`.
- Result: exact shell/Ward residuals vanish; the conservative scalar route costs
  `1520<1830` operations at five photons but `424>216` at four.
- Warrant/boundary: exact regression/use packet; graph/event-operation cost only.
- Permitted consequence: supports use and a domain-split leverage verdict.

### `E-OT-03` — scalar finite detector consumer

- Target: downstream use.
- Operation: push the compiled two-photon effect through its shell-generated
  positive measure and compare analytic and numerical aperture queries.
- Witness: node 30 equations (30.1)--(30.5) and
  `tests/test_event_measure_pushforward.py`.
- Result: identical measure identity; errors below `5.1e-14` on total, aperture,
  and normalized queries.
- Warrant/boundary: exact plus error-bounded regression; conditional `2+1` Born
  event, not a flux-normalized cross section.

### `E-OT-04` — fermionic algebra/use bench

- Target: algebra transfer and downstream use.
- Operation: retain insertion order in subset states while replacing matrix/gamma
  expansion by the exterior normal form, then consume it in the same aperture.
- Witness: nodes 05, 27, and 30; `tests/test_clifford_normal_forms.py`,
  `tests/test_fermion_subset_transfer.py`, and
  `tests/test_fermion_compton_transfer.py`.
- Result: exact history and Ward residuals vanish; six blades remain; effect plus
  Ward work is `293` exterior products versus `1386` trace updates.
- Warrant/boundary: exact seed/regression evidence in a parity-doubled `2+1`
  Clifford fixture. Because candidate and bench were co-developed, it does not
  independently promote transfer.

### `E-OT-05` — resolved three-photon use/cost

- Target: use and leverage after multiplicity growth.
- Operation: generate the shell slice, evaluate subset and explicit fermion routes,
  project three Ward images, form the same positive effect, and integrate it on the
  same detector support.
- Witness: node 30 equations (30.8)--(30.13) and
  `tests/test_fermion_multiphoton_event.py`.
- Result: both routes give the same resolved mass
  `0.00033282609489790034` within `8.01e-16`; complete product counts are
  `801<980`; zero resolution is refused.
- Warrant/boundary: exact plus error-bounded seed/use evidence; one fixed angular
  `2+1` nonlinear-Compton slice.

### `E-OT-06` — leading-soft boundary

- Target: refusal boundary, not promotion of the core compiler.
- Operation: factor each soft endpoint through the hard event, generate the three
  detector-bin weights from one positive kernel, and extract the next Laurent term.
- Witness: node 31 and `tests/test_soft_bin_transfer.py`.
- Result: leading transfer and channel normalization residuals vanish, while a
  nonzero `-1/E` coefficient leaves an unmatched logarithm.
- Warrant/boundary: exact counterexample to full infrared completion by the current
  leading tool. It supports a typed boundary, not an infrared-finite cross section.

### `E-OT-07` — fresh local reproduction

- Target: implementation consistency of all admitted packets.
- Operation: `uv run --locked python -m unittest discover -s tests` under the
  pinned CPython 3.13/SymPy/SciPy environment.
- Result: `100` tests passed in `29.220 s` on 2026-09-06.
- Provenance: manifest
  `a637c86d08541acfe538917176a0be6b5f01674b`; local reproduction, not independent
  external replication.
- Permitted consequence: supports implementation reproducibility only.

## Excluded material

- Nodes 17--24 are excluded from this claim's evidence closure: they establish a
  spin-two packet, lowering, and a detector obstruction, but do not exercise the
  frozen open-line state or the same detector output.
- Node 11's visible measure is excluded: it belongs to a different Hamiltonian and
  does not consume the open-tree compiler.
- Source packets delimit assumptions but are not admitted as transfer, novelty, or
  cost evidence because no claim-specific literature protocol was frozen here.
- Isolated runtimes are secondary diagnostics because symbolic caches can reverse
  their order; exact product/event counts own the present cost verdict.

## Replayable disposition `V_open-1`

Applying `K-research-1` to `C_open-v1` and evidence `E-OT-01`--`E-OT-07` gives:

| Dimension | Domain map | Disposition |
| --- | --- | --- |
| recovery | `D+`: admitted scalar/fermion finite open-tree fixtures and deductive recurrence domain; `D?`: excluded algebras/loops | supported, bounded |
| quotient correctness | `D+`: admitted endpoint-shell/Ward domain; `D?`: anomalies, internal characteristic channels | supported, bounded |
| algebra transfer | `D+`: retrospective parity-doubled scalar/Clifford compatibility; `D?`: independent post-freeze transfer | provisional |
| downstream use | `D+`: fixed event and declared finite `2+1` aperture measures; `D?`: absolute/inclusive scattering | supported, bounded |
| leverage | `D+`: scalar five-photon and resolved fermion product-count benches; `D-`: small scalar benches where certification costs more; `D?`: analytic, loop, infrared, and end-to-end wall-clock regimes | restricted |
| full infrared completion | `D-`: current leading-soft tool on both tested endpoints | rejected for `C_open-v1` |
| global field/mechanics compiler | `D?`: no common Hamiltonian/preparation bench | underdetermined |

There is no live `Dx` in the admitted closure. The headline disposition is
**restricted support**: the worktable owns a genuine bounded generator and use-level
compression, but not independent transfer, universal leverage, or a unified
bound/open field compiler.

## Propagation and re-entry

Nodes 27, 29, 30, and 31 may cite `V_open-1` for the exact domain above. Manuscripts
must not promote its provisional or unresolved dimensions. `C_open-v1` remains
frozen; a change to its state, step semantics, output, or refusal creates
`C_open-v2`.

The next global inquiry is not another QED multiplicity example. It asks whether
one field Hamiltonian and preparation can generate a visible return whose bound
pole and open-channel boundary are both recovered without full-state
diagonalization. A successful bridge may consume `V_open-1`; it cannot silently
extend it.
