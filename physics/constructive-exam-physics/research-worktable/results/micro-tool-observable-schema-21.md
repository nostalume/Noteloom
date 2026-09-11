# Result 21: micro-tool observable-schema closure

## Tension

The superseded `C-human-v1` instrument separated twelve route-recognition tasks
(`D3-R`, schedules `R1/R2`) from twelve matched execution pairs across assisted,
internalized, and delayed-unseen phases (`D3-E`, 24 variants, schedules `M1/M2`).
Participants could enter only one instrument in a study wave, preventing
recognition priming of execution; direct/refusal decoys, route adherence, card
visibility, and complete/correct paired timing were explicit guards. Its protocol
also promised to estimate delay, phase-boundary reliability, and route-key
ambiguity, but those quantities were not fields or independent records in
`C-human-v1`.

This is not a missing statistical technique. Two datasets can agree in every
version 1 column while differing in actual delay, timer reliability, independent
total time, or expert route judgment. Therefore the intended pilot disposition was
not a function of the recorded data.

## Observable-closure probe

The probe asked whether every promised pilot quantity had a reconstructing map from
checked-in records:

| Quantity | `C-human-v1` reconstruction | Obstruction | `C-human-v2` repair |
| --- | --- | --- | --- |
| complete trial time | sum four observer phases | sum is not an independent timer | `independent_total_seconds` |
| phase reliability | absent | an uncertain boundary looked measured | `phase_timing_reliable` plus exact-sum check |
| delayed robustness interval | prose only | “delayed” had no duration | `hours_since_assisted` |
| route-key ambiguity | authored answer only | author convention looked like human uniqueness | independent reviewer records and typed audit |

The problems, exact answers, operator semantics, and `R1/R2` and `M1/M2` schedules
are unchanged. The candidate is versioned because its admitted inputs and refusals
changed, not because an outcome was inconvenient.

## `C-human-v2` construction

Every execution attempt now carries a whole-trial timer independent of its four
phase marks. If phase timing is declared reliable, the loader requires

```text
interpretation + setup + computation + return
  = independent_total_seconds.
```

If phase timing is unreliable, the whole-trial value remains usable but the phase
breakdown cannot support a phase claim. Assisted rows define zero elapsed hours;
delayed-unseen rows require a positive recorded interval. Paired outcomes use the
independent total.

The new `D4-K` route-key review accepts independent reviewer, task, selected-route,
rationale, and provenance records. For each task it returns exactly one state:

```text
unreviewed
insufficient_review
agreed
ambiguous
key_disputed
```

At least two reviews are required merely to make disagreement observable. This is
a preflight boundary, not a claim that two agreeing experts establish universal
route uniqueness. Only `agreed` tasks may enter a keyed recognition-accuracy
summary; all other selections remain reportable without being called errors.

The existing disjoint-cohort refusal remains active, preventing recognition and
execution from training one another within a study wave.

A descriptive summarizer consumes the three typed record families. It scores
recognition only for `agreed` keys, counts all execution accuracy/adherence rows,
and counts faster/slower/tied eligible pairs. Its speed disposition is hard-bound to
`not_evaluated`; there is no outcome-driven promotion path before a confirmatory
contract exists.

## Verification and disposition

Test-first construction produced three intended failures: version 1 accepted a
reconstructed total that disagreed with a proposed independent timer, the route-key
API did not exist, and no descriptive summarizer existed. The implemented checks
now distinguish reliable from unreliable phase timing, reject invalid delayed
intervals, classify independent key reviews, reject duplicate reviewer/task
records, and preserve zero-row inputs as `unreviewed` rather than agreement.
Synthetic fixtures verify the summarizer's classification logic but are excluded
from scientific evidence.

`X6`, the schema-observability obstruction, is **supported** by exact field and
reconstruction inspection. `C-human-v2` is **constructed-unpopulated**. No learner
or expert review rows exist, so speed, accuracy, retention, ambiguity, and
near-family robustness remain unresolved.

The next dependency-ordered action is narrow. Result 22 supplies the
[blinded acquisition contract](blinded-route-key-review-constructor-22.md):

```text
D4-K independent key review
  -> repair or exclude disputed recognition tasks without seeing learner outcomes
  -> D4-P descriptive learner pilot
  -> freeze confirmatory thresholds/model only from pilot quantities
  -> V7 bounded human-use disposition
```

Cross-family human transfer remains outside this bench.
