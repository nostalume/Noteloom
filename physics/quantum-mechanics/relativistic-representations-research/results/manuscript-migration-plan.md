# Manuscript Migration Plan: Poincare Representations to Free Fields

Status: tracked relocation and publication verification complete  
Source worktable: `physics/quantum-mechanics/relativistic-representations.typ`  
Manufactured manuscript: `physics/quantum-mechanics/poincare-to-free-fields.typ`  
Architecture: [manuscript-architecture.md](manuscript-architecture.md)

## Composition progress

- Pass 1, Section 1: composed from `N1`.
- Pass 1, Sections 2--4: composed from `N2/N2a/N2b/N3/N3c` on 2026-08-30.
- Pass 1, Section 5: composed from `N4/N4a/N4b/N4m` with the action boundary
  checked against `N4c/N4i` on 2026-08-30.
- Pass 1, Section 6: composed from `N4c/N4e--N4l/N4y/N4z` on 2026-08-30.
- Pass 1, Section 7: composed from `N3a/N3b/N4/N4b/N4o/N5` on 2026-08-30.
- Pass 1, Section 8: composed from `N4q/N5/N7` on 2026-08-30.
- Pass 1 semantic composition is complete; the frontier is Pass 2 publication
  closure.
- The complete research worktable was relocated to the tracked destination on
  2026-08-31; all 127 meaningful paths were accounted for.
- `field-equations-to-computable-observables.md` now composes the N4n--N9g
  exploration as a Markdown companion while retaining the canonical nodes.

Sections 2--4 now export the induced physical representation, explicit massive and
null stabilizer fibers, finite Lorentz carriers with actual stabilizer
intertwiners, and the ordinary/gauge orbitwise realization theorem. The source
worktable remains unchanged.

Section 5 now supplies the fixed-carrier polynomial-lift criterion, the direct
chiral local realization for every separate finite massive spin and massless
helicity, and the parity-paired symmetric bosonic and fermionic potential
complexes. Independent bounded checks pass for bosonic spins `1--6` and fermionic
tensor ranks `0--3`; the invariant exact-sequence proofs remain the all-rank
support.

Section 6 follows one compact admissible source through trace reversal, causal
response, the source/solution quotient, physical-shell restriction, positive
completion, and CCR/CAR Fock recovery. The theorem is deliberately limited to the
source-generated closed invariant subspaces: density in the complete abstract
induced spaces, real fermion forms, and the corresponding massive potential
completion remain open rather than being inferred from local fiber recovery.

Section 7 applies one quotient-map comparison contract to spins
`0,1/2,1,3/2,2`. It separates exact block coincidence, polynomial physical-shell
equivalence, and orbitwise representation equivalence. Maxwell potential/curvature
reaches the strongest supported local shell map; conventional massive
Rarita--Schwinger and Fierz--Pauli comparisons remain outside the baseline.

Section 8 indexes equivalence by its preserved structure, states the strongest
finite free-field realization and recovery theorem actually constructed, and
computes a curvature obstruction to transporting the free Dirac factorization
through a general `U(1)` coupling. It then types prediction as
input--response--observable composition and closes the paper with exact re-entry
conditions. The supporting synthesis is [N7](../nodes/07-equivalence-boundary.md).

## Composition decision

The supported finite free-field spine is synthesis-ready. The old Typst note remains
an unchanged worktable while a new manuscript is manufactured from supported node
outputs. Migration is promotion, not copying: research chronology, failed routes,
and heavy calculations do not determine paper order.

The scoped paper claims only the following route:

```text
Poincare orbit and stabilizer representation
  -> physical massive-spin or massless-helicity fiber
  -> chosen covariant Lorentz carrier
  -> equivariant local symbol or differential complex
  -> physical kernel/cohomology/quotient
  -> causal and positive-frequency realization
  -> free CCR/CAR quantization and one-particle recovery.
```

Symmetry fixes the one-particle representation under the declared spectral
assumptions; it does not uniquely fix the carrier, equation, action, interaction,
state, or observable. This determination boundary is the paper's thesis and its
stop condition.

### Research-record format decision (2026-08-31)

The material outside this scoped theorem was not flattened into a second Typst
paper during migration. The canonical companion is the complete tracked research
worktable at `physics/quantum-mechanics/relativistic-representations-research/`.
This includes `plan.md`, `framework.md`, `sources.md`, `sources/`, `nodes/`,
`computation/`, and `results/`. The tree was relocated as one unit rather than
copied, so its relative evidence links remain valid and no public mirror competes
with the staging copy.

One-file-per-node is retained because it already provides a concrete benefit: each
question, computation, rejected route, and re-entry edge can be read without
loading a linear manuscript or the entire research history. Source packets,
computation packets, and synthesis results are not node duplication: they own
provenance, reproducibility, and cross-node evaluation respectively.

The distinction is therefore:

```text
Markdown research graph
  = canonical exploration, provenance, failures, supported frontier, open edges

Typst manuscript
  = derived linear synthesis of one supported sub-spine for a named audience
```

The field-to-observable continuation is now composed as a Markdown companion. A
future Typst paper remains possible, but it would be another output composed from
supported nodes rather than the archive into which those nodes are discarded. No
meaningful exploration is superseded merely because it is absent from the current
free-field paper.

Non-bloat is enforced by ownership rather than deletion:

- a source claim is extracted once in `sources/` and linked by nodes;
- heavy computation and its reproducibility contract live once in `computation/`;
- a node owns the semantic construction and imports only compact evidence;
- `results/` owns cross-node audits and synthesis decisions;
- `plan.md` owns navigation and the current frontier, not repeated derivations;
- generated caches and reproducible raw output are not migrated.

### Lossless-relocation contract

The 2026-08-31 inventory contains 128 files: 109 Markdown packets, 18 executable
checks, and one generated Python bytecode cache. The meaningful migration surface
is therefore 127 files. No two current files have the same content hash, and the
Markdown contains 234 relative links. Eighteen files contain an explicit
`.agents/research` path, principally reproducibility commands.

Relocation is accepted only when:

1. a pre-move manifest records every meaningful relative path, byte count, and
   content hash;
2. the complete tree moves once to the tracked destination, excluding only
   `__pycache__/` and `*.pyc` generated artifacts;
3. the internal relative layout remains unchanged, preserving the 234 relative
   links without rewriting them;
4. the 18 explicit old-root references are changed to the new root;
5. every local Markdown link resolves and every computation README names an
   existing program;
6. the executable checks pass from the new location;
7. a post-move manifest accounts for every pre-move artifact, allowing only the
   declared path-command edits;
8. `.agents/research/` is absent afterward, leaving exactly one canonical tree.

Later semantic compression is a separate audit. It may replace repeated summaries
with links to a canonical owner, but it cannot be combined with relocation: moving
and rewriting simultaneously would make information-loss diagnosis ambiguous.

## Research horizon and re-entry rule

Baseline `R1` includes the supported results of `N1--N5`, the finite bosonic and
fermionic potential/causal branches, and `N4y/N4z`. Supported parts of `N7` enter
only as equivalence boundaries.

Composition reopens research only when one of these events occurs:

- a promoted manuscript claim lacks a deductive computation or theorem contract;
- two promoted nodes use incompatible domains, conventions, or exactness levels;
- a low-spin recovery contradicts the general finite-spin construction;
- a required global recovery map cannot be constructed.

Countable-spin completion, interacting particle extraction, bound-state mechanics,
collective dynamics, and observable-compression benchmarks remain active or parked
branches in the Markdown graph. They enter a Typst paper only when a paper thesis
consumes them, but paper inclusion is not required for their preservation.

## Two-pass manufacture

### Pass 1: semantic manuscript

Construct the main deduction in dependency order, not source order:

| Section | Consumed support | Section output |
| --- | --- | --- |
| 1. Problem and determination boundary | `N1` | exact input, choices, thesis, and scope |
| 2. Physical representation data | `N2`, `N2a` | induced representation and physical fiber |
| 3. Covariant Lorentz carriers | `N2b` | carrier families and restricted fiber maps |
| 4. Realization theorem | `N3`, `N3c` | typed intertwiner and physical recovery criterion |
| 5. Universal local finite-spin complexes | `N4`, `N4a`, `N4b`, `N4m`, `N4i` | polynomial equation/complex and standard-fiber cohomology |
| 6. Causal and quantum completion | `N4e--N4l`, `N4y`, `N4z` | Green/source quotient, positive shell, CCR/CAR recovery |
| 7. Low-spin comparison | `N3a`, `N3b`, `N4o`, `N5` | bounded checks for spins `0,1/2,1,3/2,2` |
| 8. Equivalence boundary | `N4q`, `N5`, `N7` | hierarchy of equivalence, coupling obstruction, prediction boundary, and stopping theorem |

Every section must construct an object consumed by the next section. Every
displayed equation must expose constructed inputs, the operation, a common target,
an equality or obstruction witness, and its validity boundary. Component
calculations may check a structural result but may not carry the main deduction.

### Pass 2: comparison and publication closure

- compress technical proofs into appendices only when the main semantic witness
  remains visible;
- recover the familiar low-spin equations from the general construction;
- add theorem-contract citations and a bibliography;
- resolve notation, equation references, terminology, and exactness labels;
- perform a claim audit, full Typst compile, and PDF readability inspection;
- close the migration ledger so every old region and research branch has a durable
  disposition.

## Disposition vocabulary

Each item receives exactly one primary disposition:

- **promote**: rewritten into the main semantic deduction;
- **compress**: retained as a lemma, appendix, table, or bounded check;
- **separate**: remains a first-class Markdown node outside this paper's linear
  argument; it may later supply a companion synthesis;
- **supersede**: omitted because a supported construction replaces it; Git history
  remains the durable archive only after the superseded source has actually been
  tracked.

No source material is deleted during manufacture. A disposition may change only
when a manuscript claim consumes a different result.

## Research-node migration ledger

| Research material | Disposition | Manuscript destination or reason |
| --- | --- | --- |
| `N1` | promote | Section 1 determination boundary |
| `N2`, `N2a` | promote | Section 2 physical spaces, orbit, stabilizer, spin/helicity |
| `N2b` | promote | Section 3 invariant Lorentz-carrier construction |
| `N3`, `N3c` | promote | Section 4 orbitwise intertwiner and analytic boundary |
| `N3a`, `N3b`, `N4o`, `N5` | promote + compress | Section 7 bounded comparison and its exact equivalence levels |
| `N4` | promote | Section 5 direct finite chiral construction |
| `N4a`, `N4b` | promote + compress | Section 5 theorem; detailed exact sequences in appendices |
| `N4c`, `N4d` | compress | action/Green theorem contracts and explicit open obligations |
| `N4e--N4h` | promote + compress | Section 6 bosonic causal theorem; technical proof appendix |
| `N4i--N4l` | promote + compress | Sections 5--6 fermionic construction; proof appendix |
| `N4m` | promote | Section 5 finite integer-spin field machine |
| `N4n--N4p` | separate | retain as Markdown mechanics/spectral-reduction exploration; not a free-field proof |
| `N4q` | compress | Section 8 semantic-computability and determination boundary |
| `N4r--N4x` | separate | retain as Markdown interacting field/particle and composite-shell branch |
| `N4y`, `N4z` | promote | Section 6 free bosonic/fermionic quantization recovery |
| `N8--N8d` | separate | retain as Markdown collective-dynamics branch |
| `N9--N9g` | separate | retain as Markdown observable-compression branch |
| source packets | compress | bibliography and exact theorem contracts only |
| computation packets | compress | reproducible checks; only compact invariant outputs enter appendices |
| synthesis audits | retain as Markdown evidence | do not enter theorem prose verbatim, but preserve the evaluated routes and migration rationale |

## Old-worktable migration ledger

Line locators refer to the unchanged 2026-08-30 worktable revision and will be
refreshed only if that source file changes.

| Old note region | Disposition | Compact result retained |
| --- | --- | --- |
| lines 1--47 | supersede + promote | corrected Poincare convention and determination boundary |
| lines 48--91 | compress | spin-cover/vector-carrier convention check |
| lines 92--345 | compress | one verified left/right generator convention in Appendix A |
| lines 346--421 | compress | optional coefficient-function map after the physical bridge |
| lines 422--425 | supersede | rigid-determination claim replaced by `N1` |
| lines 426--661, dimension 1+1 | separate | dimension-specific comparative note |
| lines 662--1091, dimension 1+2 | separate | dimension-specific comparative note |
| lines 1092--1189 | compress | spin-cover construction checked against invariant Section 3 route |
| lines 1190--1288 | compress | bounded low-spin sigma/gamma verification in Appendix C |
| lines 1289--1350 | compress | spinor-polynomial backend and corrected carrier labels |
| lines 1351--1381 | separate/computation | recursive chirality elimination; not a proof until independently checked |
| lines 1382--1499 | compress | Dirac/Proca examples recovered from the general construction |

The known repeated label near old line 1298 and the unsupported component
elimination near lines 1366--1381 are not promotable claims.

## Claim and exactness ledger

| Claim class | Current paper status | Required presentation |
| --- | --- | --- |
| one-particle orbit/little-group classification | theorem contract + internal construction | state hypotheses and construct the standard-fiber ambiguity |
| orbitwise field realization | supported | prove well-definedness and intertwining on the same input |
| finite direct chiral local realization | supported | main theorem with standard-momentum kernel computation |
| finite bosonic/fermionic potential complexes | supported in declared families | main theorem plus exact-sequence proof contract |
| compact-source causal and positive-shell recovery | supported with image boundary | state density limitation explicitly |
| free CCR/CAR one-particle recovery | supported | compute the vacuum one-field map on the same source class |
| equivalence of most conventional carriers | partial | examples or open boundary, never universal theorem |
| completed countable-spin tower | open | excluded from the scoped theorem |
| interacting dynamics from symmetry | unsupported | explicitly denied by the determination boundary |

Use only these exactness labels in composition: **constructed identity**,
**theorem under named contracts**, **finite-family theorem**, **bounded check**, and
**open boundary**.

## Completion bench

The manuscript reaches version `v1` when:

1. the abstract, thesis, main finite-spin theorem, and conclusion agree in scope;
2. each main section exports the typed object consumed downstream;
3. massive spin and massless helicity recover their physical fibers through one
   visible realization framework;
4. spins `0,1/2,1,3/2,2` check rather than define the general construction;
5. the positive-frequency and free-quantization maps recover the same one-particle
   vectors on the declared source image;
6. no primary proof depends on unexplained Pauli/gamma components;
7. every old region and research node has a final disposition;
8. citations, cross-references, equations, and the generated PDF pass a fresh
   compile and readability audit.

At this bench the paper stops. Further generality is a new research question, not
a publication prerequisite.

## Landed migration and verification

The 2026-08-31 manufacture pass established three durable layers:

1. `../../poincare-to-free-fields.typ` is the linear, supported theorem spine;
2. `../../field-equations-to-computable-observables.md` is the readable companion
   synthesis of `N4n--N9g`;
3. this research directory remains the canonical lossless graph of nodes,
   computations, sources, framework, and audit results.

All 127 retained worktable files were relocated into this tracked destination;
the sole excluded item was a generated Python bytecode cache. The old
`.agents/research` location and its empty directories were removed. Fresh checks
resolved 539 local Markdown links with zero broken targets, passed all 18 retained
computation programs from their new paths, and compiled the Typst manuscript and
all 18 neighboring template consumers. The final manuscript query finds one
semantic title, one bibliography, three tables, twelve labeled figures or theorem
environments, and no heading below the orphan threshold. A rendered 40-page PDF
was also inspected page by page.

This is a lossless migration, not a flattening: the companion preserves the route
and its failed branches, while detailed premises, calculations, provenance, and
limitations remain at their graph nodes instead of bloating either linear paper.
