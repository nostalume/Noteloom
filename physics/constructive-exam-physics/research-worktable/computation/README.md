# Exact observable-relation kernel

This directory is the reproducible computation companion to the
[framework](../framework.md). It accepts human-validated, structured physical
requests; it does not infer laws from prose. SymPy supplies exact algebra, Ruff
checks source style, and `uv.lock` fixes the environment. Nothing here is a
published package.

## Setup and project boundary

Requirements are Python 3.11 or newer and `uv`. From this directory run:

```text
uv sync --dev
```

`occ` owns reusable constructions. `worktable` owns source-bound case records and
the command-line projections used by this research directory. `occ/__init__.py`
is a compatibility facade; new code should import the direct owner. There is no
second algorithm facade in `worktable`.

## Ownership

| Capability | Direct owner |
| --- | --- |
| polynomial projection and typed problem packets | `occ.relation`, `occ.problem`, `occ.records` |
| supplied-law search and finite events | `occ.adaptive`, `occ.event` |
| linear pullback and observable closure | `occ.pullback`, `occ.linear` |
| semantic extraction and physical return | `occ.semantic` |
| planar paths and frictional impact | `occ.path`, `occ.impact` |
| harmonic response, spatial pattern, and product | `occ.harmonic`, `occ.harmonic_pattern`, `occ.harmonic_product` |
| dimensional quotient | `occ.dimensional` |
| network condensation and elimination order | `occ.network`, `occ.network_order` |
| network human boundary and instruments | `occ.network_human`, `occ.network_study*`, `occ.network_admission*` |
| route cost, calibration, and learner instruments | `occ.cost`, `occ.calibration`, `occ.study`, `occ.micro_study`, `occ.pilot` |
| problem-card routing and one-successor composition | `occ.routing`, `occ.composition` |
| retained typed-adapter slices | `occ.parameterized`, `occ.free_surface`, `occ.harmonic_current`, `occ.zeeman`, `occ.phonon` |
| fixtures and command rendering | `worktable.*_cases`, `worktable.__main__` |

## Common entry contracts

Use the smallest direct owner when the request type is already known. Use routing
only when a caller needs one uniform envelope:

```python
from occ.routing import ProblemCard, compile_problem_card

result = compile_problem_card(
    ProblemCard(problem_id, observable, provenance, admitted_semantic_request)
)
```

The card contains exactly one human-admitted request. Selection consults semantic
types and construction evidence, never the problem identifier or expected answer.
It returns the selected owner, its domain result, certificates, obstruction, source
status, and selection witness. A short sufficient law with no hidden quantity is
`direct_relation`; hidden-variable elimination is `polynomial_relation`;
ambiguous minimal law sets and unsupported shapes are refusals.

One downstream transformation is available through a separate typed contract:

```python
from occ.composition import ProblemPipelineCard, compile_problem_pipeline

result = compile_problem_pipeline(
    ProblemPipelineCard(root=card, output_observable=name, step=typed_step)
)
```

The root must succeed with passing certificates. The compiler then dispatches one
declared payload/step pair and preserves parent identity, provenance, and both
certificate sets. It supports harmonic-response to same-frequency product and
two planar paths to a circuit. It is not a callback registry, branching graph, or
prose planner.

The retained adapter probe is similarly bounded:

```python
from occ.parameterized import compile_problem

result = compile_problem(problem)
```

It covers the structured rotating-surface, weak-field Zeeman, scalar harmonic
current, phonon-count, and phonon-to-thermal slices recorded in the
[compiler baseline](../results/compiler-baseline.md). It provides interface and
refusal evidence, not a demonstrated handwritten shortcut.

## Operation catalog

| Operation | Constructed result | Primary refusal boundary |
| --- | --- | --- |
| exact relation elimination | retained polynomial consequences and ideal witnesses | non-polynomial input, undeclared variables, or budget overflow |
| linear/quadratic pullback | target form after an explicit finite graph map | incompatible dimensions or map shape |
| observable closure | smallest finite adjoint-invariant space for `x''=-Ax` | nonlinear/infinite dynamics or closure budget |
| minimal supplied-law search | least relevant law subsets and target projections | ambiguity, insufficiency, or unsupported relation shape |
| finite event | zero-event relation, lifted branches, interval filter | unreachable/ambiguous events or unsupported backend |
| semantic functional | one-source linear/quadratic pullback plus return ledger | phase loss, dimension mismatch, unsupported fields |
| planar path | oriented work, length, area/curl and circuit return | absent material path or unsupported geometry |
| planar impact | tangential-arrest/sliding branches and physical return | rotation, compliance, multi-contact, higher-dimensional cone |
| harmonic response | exact phasor, magnitude, real signal and pattern | nonlinear/transient response or nonfinite/unordered extrema |
| harmonic product | DC and `2 omega` channels with exact identity check | differing/nonpositive frequency, time-dependent factor, complex scale |
| dimensional quotient | primitive exact nullspace monomials | no group, excessive nullity, unsupported base/scale |
| network condensation | Schur boundary law and affine hidden recovery | singular/unknown hidden block, nonlinear/dynamic network |
| sparse network order | replayable scalar updates and reverse recovery | nonreciprocal matrix, uncertain pivot, step budget |
| route cost/calibration | atomic ledgers, exact admission regions, or typed refusal | mixed substrate, hidden work unit, rank/positivity failure |
| learner/network instruments | frozen keys, schedules, guards, clustered summaries | missing review/data, leakage, unreliable or ineligible observations |

All constructions preserve a named observable and either return replayable
certificates or an explicit obstruction. Their detailed derivations and evidence
cutoffs live in [results](../results/), not in this usage guide.

## Reproduce

Run these commands from this directory. Their order is the frozen public command
surface: the three quality gates followed by exactly twenty research projections.

```text
uv run python -m unittest discover -s tests -v
uv run ruff check .
uv run ruff format --check .
uv run python -m worktable corpus-audit
uv run python -m worktable polynomial-batch
uv run python -m worktable route-benchmark
uv run python -m worktable route-admission
uv run python -m worktable calibration-probe
uv run python -m worktable study-audit
uv run python -m worktable micro-study-audit
uv run python -m worktable dimensional-transfer
uv run python -m worktable network-condensation
uv run python -m worktable network-ordering
uv run python -m worktable network-human-boundary
uv run python -m worktable network-study-audit
uv run python -m worktable network-admission-audit
uv run python -m worktable event-transfer
uv run python -m worktable impact-transfer
uv run python -m worktable path-transfer
uv run python -m worktable harmonic-transfer
uv run python -m worktable harmonic-product
uv run python -m worktable composition-benchmark
uv run python -m worktable routing-benchmark
```

The projections respectively audit the 126-problem corpus; replay the locked
polynomial batch; reconstruct route cost and admission; expose the empty
calibration/study boundaries; exercise dimensional and network transfers; audit
network execution and adaptive recognition instruments; reproduce event, impact,
path, harmonic, and product transfers; and finish with composition and common-card
routing. Command output is descriptive evidence at the named result cutoff; it is
not an independent source or learner observation.

## Scientific and computational boundaries

- Algebraic closure does not prove that every candidate lifts to a physical state.
  Accepted branches must satisfy the original laws, regimes, inequalities,
  geometry, units, orientations, and answer convention.
- A source packet preserves declared provenance but does not prove that a human or
  parser selected the correct physics. Official-answer comparison remains separate.
- The kernel does not parse unrestricted language, invent physical laws, infer
  diagrams, solve general PDEs/ODEs, or prove a worst-case Gröbner runtime.
  Resource limits are refusal guards, not complexity theorems.
- Exact harmonic operations are finite steady-state constructions; path and impact
  operations are planar and explicitly parameterized; network operations require
  an admitted exact linear response matrix and partition.
- Greedy sparse order is deterministic but not globally optimal. Structural action
  reduction does not establish recognition, elapsed-time, error, retention, or
  transfer benefit.
- Human-cost regions assume declared positive additive weights. Current learner
  and independent-review templates are empty, so empirical benefits remain
  `unobserved`.

The frozen active cases and evidence rules are in the [benchmark](../benchmark.md);
the [research graph](../research-graph.md) is the authoritative current claim and
frontier index.
