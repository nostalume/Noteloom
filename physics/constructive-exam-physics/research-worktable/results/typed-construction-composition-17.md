# Typed construction composition without a general workflow engine

## Question and spine position

Can two independently certified construction stages be joined without erasing the
physical observable, source provenance, parent identity, or refusal boundary?

Result 16 exposed the architecture obstruction. A23-05 needs harmonic response
followed by harmonic product, but the common `ProblemCard` intentionally admits
exactly one semantic request. The path branch already has the same shape: A14-06
first constructs oriented path functionals and then closes two paths into a
resistive circuit. Copying these sequences into source runners works, but the
relation between stages is implicit and cannot be inspected or reused.

## Exact obstruction

A routed result contains a typed physical construction and certificates, yet the
next operation previously received only an ordinary Python value. That handoff did
not state:

- which observable and source problem the value represents;
- which artifact is its direct parent;
- whether upstream certificates passed before consumption;
- which downstream types are compatible;
- how an upstream refusal prevents downstream execution.

Adding another problem-specific router branch would conceal this missing edge. A
general callback or arbitrary DAG would go too far: it could bypass typed semantic
ports and create orchestration machinery unsupported by two short source chains.

## Frozen contract `C-composition-v1`

The admitted object is one routed root plus one typed successor:

```text
ProblemPipelineCard(root ProblemCard, output observable, typed step)
  -> compile root through the existing router
  -> wrap the successful result as a ConstructionArtifact
  -> require all root certificates to pass
  -> dispatch only a declared compatible (payload type, step type) pair
  -> construct one child artifact with exactly one parent reference
```

Each artifact carries:

```text
artifact identity
problem identity
observable name
source provenance
operation name
typed payload
certificates
direct parent references
```

The two admitted successor types are deliberately concrete:

| Root payload | Successor | Child payload |
| --- | --- | --- |
| `HarmonicResponseResult` | `HarmonicProductStep` selecting one named response | `HarmonicProductResult` |
| `PathFunctionalResult` | `TwoPathCircuitStep` selecting two named paths | `TwoPathCircuitResult` |

There are no arbitrary callbacks, reflection-based port discovery, branching,
loops, natural-language planning, or multi-level scheduling. The original
single-request router remains unchanged.

## Two structurally different executions

### A23-05: response to product

The root card constructs the induced-current phasor. The successor selects the
named `induced current` observable and consumes it with the orientation phasor.
The child exactly reproduces Result 16's applied torque, including the DC and
`2 omega` channels. Its only parent is
`A23-05:root:harmonic_response`, and it inherits the page-9 provenance.

### A14-06: path functional to circuit

The root card constructs the arc and chord work/length functionals. The successor
selects `minor arc` and `straight chord`, supplies resistance per length, and
constructs the two-path terminal voltage and branch currents. The child exactly
reproduces Result 13's terminal voltage. Its only parent is
`A14-06:root:path_functional`, and it inherits the page-28 provenance.

The second chain matters because it tests the envelope on a non-harmonic payload
and a different physical return. The common construction is the typed evidence
edge, not the physics performed by either specialist owner.

## Refusal semantics

The composition layer adds only edge-specific refusals:

- a root refusal is preserved as `upstream_<root code>` and creates no artifacts;
- a constructed root with any failed certificate returns
  `upstream_certificate_failed`;
- a mismatched root/step pair returns `incompatible_pipeline_step`;
- an absent named response or path returns `missing_parent_observable` or
  `missing_parent_path`;
- a downstream domain refusal is preserved as `downstream_<domain code>`.

No alternate operator is guessed after a refusal.

## Human-computation disposition

This construction reduces software and review complexity: one can inspect the
root result, the exact semantic port consumed, the child result, and the proof
lineage in one envelope. It also makes the two existing source pipelines
reproducible without duplicating their handoff logic.

It does not yet reduce handwritten exam work. Both chains use problems already
classified as full executions, and the A23-05 direct route remains
`always_direct`. No timing, error, retention, or learner-transfer observations
were added. The composition card is therefore an architecture and verification
tool, not an exam-shortcut claim.

## Evidence and disposition `V-composition-2026-09-06`

| Evidence ID | Operation | Permitted consequence |
| --- | --- | --- |
| E17-RED-CORE | importing the absent typed-step API failed | the composition API was not already present |
| E17-RED-CLI | `composition-benchmark` was rejected by the command parser | the public bench boundary was not already present |
| E17-A23 | typed response-product output equals the established exact torque | one harmonic successor chain is supported |
| E17-A14 | typed path-circuit output equals the established exact terminal voltage | the envelope transfers to a different payload family |
| E17-LINEAGE | both children preserve problem, provenance, certificates, and exactly one parent | bounded evidence flow is supported |
| E17-REFUSAL | underdetermined root, incompatible step, and missing port stop explicitly | unsafe or meaningless composition is not guessed |
| E17-CORPUS | neither execution is new | corpus counts remain 24 full, 3 partial, 2 shape-only, 19 candidates, 74 outside, 4 qualitative |

| Claim dimension | Disposition | Boundary |
| --- | --- | --- |
| typed one-successor composition | `D+ supported-bounded` | exactly the two declared payload/step pairs |
| provenance and parent preservation | `D+ supported` | one successful root and one child |
| cross-family envelope reuse | `D+ supported-bounded` | harmonic and planar-path chains only |
| general workflow or arbitrary DAG | `D- not implemented` | no branching, loops, callbacks, or step registry |
| new physics grammar coverage | `D- none added` | existing specialist constructors own all mathematics |
| handwritten exam leverage | `D? unresolved; no new positive evidence` | zero learner observations and prior negative structural evidence |

## Re-entry and reproduction

The next composition expansion requires a source problem that needs a third stage,
a branch whose alternatives must remain explicit, or a new typed consumer shared
by at least two source problems. Mere desire for a generic workflow engine is not
sufficient evidence.

The later [frictional-impact result](frictional-impact-projection-18.md) tests the
explicit-branch alternative. A15-02 constructs its regimes inside one specialist
physical result, so it does not expand the one-successor composition contract.

From `computation/` run:

```text
uv run python -m unittest tests.test_composition -v
uv run python -m worktable composition-benchmark
uv run python -m unittest discover -s tests -v
```
