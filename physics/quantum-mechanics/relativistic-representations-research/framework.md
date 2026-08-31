# Concrete Research Worktable Framework

## Three material layers

Every large paper, manuscript, dataset, or computation is handled in three layers.

### 1. Raw material

The authoritative or reproducible bulk object remains intact:

- a paper at its DOI/arXiv URL or an optional local PDF cache;
- the Typst manuscript at its repository revision;
- a dataset with provenance and checksum;
- a program plus run directory containing logs, expansions, tables, or figures.

Raw material is not copied into node prose and is not loaded by default.

### 2. Semantic extraction

A small Markdown packet records only what research nodes can consume:

- exact locator: section, page, theorem, equation, manuscript lines, or run ID;
- claim or construction expressed in our notation;
- presumptions and validity regime;
- relation to competing sources or worktable material;
- unresolved contradiction or required verification.

Source packets live in `sources/`. Computation result packets live beside their
program under `computation/<node>/`.

### 3. Node result

A node imports named claims or compact computation results, not the raw expansion.
It produces a checked semantic output with validity conditions. Only that output
flows along DAG edges or into manuscript synthesis.

```text
paper/PDF ──> source packet ──┐
                              ├──> research node ──> checked node result
program ──> raw run ──> result packet ──┘                    │
                                                             └──> downstream node
```

## Workspace

```text
physics/quantum-mechanics/relativistic-representations-research/
  plan.md                            current graph and supported frontier
  framework.md                       this material protocol
  sources.md                         compact source index
  sources/
    <source-key>.md                   locator and semantic extraction
    raw/                              optional cached bulk sources, created on use
  nodes/
    <node-key>.md                     concrete active node packets
  computation/
    <node-key>/
      node.md                         semantic question and reproducibility contract
      program.*                       executable calculation
      result.md                       compact promoted result
      runs/<run-id>/                  bulk logs/expansions/plots, created on use
  results/
    <node-output>.md                  supported conceptual outputs, created on use
```

Do not create empty directories or placeholder artifacts. A packet appears when its
material becomes active.

## Loading rule

- To understand the whole program, load the graph only.
- To choose a node, load its node packet and incoming result packets.
- To inspect a claim, load its source packet; open the raw paper only at named
  locators that require verification.
- To consume a computation, load `result.md`; inspect code or raw runs only when
  reproducing, debugging, or challenging it.
- To synthesize the manuscript, load supported node results, not every source note
  or computation trace.

## Large paper protocol

A source packet uses stable claim IDs, for example `GS-01`. The node cites `GS-01`
and the packet owns the mapping to the paper's section/equation. Long derivations
stay in the paper. If a derivation must be challenged, create a computation or
derivation node bound to the exact formula range; do not paste the whole range into
the source packet.

## Heavy computation protocol

Before execution, the computation node defines the invariant question and reduction.
Each substantial run gets an immutable run ID and records:

- program revision/hash and environment;
- exact inputs, conventions, parameters, and precision;
- raw stdout/stderr, generated expressions, data, and figures;
- resource scale and failure state.

`result.md` promotes only:

- the run ID and reproducibility command;
- compact invariants, ranks, coefficients, error bounds, or plots;
- checks and failed checks;
- semantic interpretation and validity boundary.

If an expansion grows enormously, store it in the run directory and summarize its
normal form, invariant content, or hash. Size does not justify moving it into a node
or manuscript.

## Problem-local reduction graph

When a node asks for a computable observable, do not choose a method from a fixed
global catalogue. Open a local graph whose vertices are concrete representations
of that problem or partial computed objects. A newly invented transformation is
an edge only after it records:

- its input type, domain and constructed output;
- an exact equality or quantitative error witness;
- how the requested observable is recovered;
- construction, verification and recovery cost;
- its failure boundary and a direct-computation fallback.

Edges compose only when the intermediate types and domains match and their
witnesses compose. The useful route can contain normal forms, algebra, variational
bounds, resolvents, graphs, numerical solvers or a mechanism not previously named.
This list is illustrative, not exhaustive. The framework audits and composes
discovered reductions; it does not pretend to discover them automatically.

If no edge reduces the whole cost at the requested tolerance, the honest node
output is the smallest directly computable residual problem with its error
contract. A failed candidate invalidates only itself, not the node or other routes.

## Revision rule

Raw material is append-preserving or versioned. Semantic packets and node results
may be corrected or superseded. A changed source edition or computation program
invalidates only claims bound to the changed locator/run, not the entire graph.
