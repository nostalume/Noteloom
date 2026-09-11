# D3 selective micro-tool study protocol

This protocol operationalizes `C-human-v2`, which supersedes the unpopulated
`C-human-v1` schema. The schedules and problems are unchanged. Version 2 adds the
observables required to audit route-key ambiguity, actual delay, independent total
time, and phase-boundary reliability. It is not evidence that the review cards save
time or reduce errors.

## Claim dimensions

The study keeps four questions separate and uses two non-overlapping instruments:

1. **Recognition:** can a learner identify the obstruction-specific route from the
   prompt alone?
2. **Assistance:** with the relevant card visible, does the operator route change
   correctness or complete solution time relative to a competent direct route?
3. **Internalization:** after training, does the operator remain usable without the
   card?
4. **Delayed unseen robustness:** after a declared delay, does the result persist on
   new numerical variants in the same four families?

`D3-R` measures recognition without solving. `D3-E` measures execution with a
route assigned when the prompt is revealed. A learner never diagnoses an execution
item first: doing so would teach or prime the operator and contaminate the direct
baseline.

Assign a participant to `D3-R` or `D3-E`, not both, within one study wave. This
prevents the recognition vocabulary from acting as undeclared execution training
and prevents assisted execution cards from teaching the later recognition task.

The last dimension is near-family robustness, not cross-family transfer. A later
instrument must supply genuinely changed physical families before making that
claim.

## Frozen bench

The four families and assigned operator routes are:

| Family | Operator route | Primary obstruction |
| --- | --- | --- |
| vertical jet | `slice` | one hidden impact speed joins momentum flux to height |
| rough-wall point impact | `projection` | saturated friction can overshoot zero tangential speed |
| planar line work | `path` | common endpoints do not determine nonconservative work |
| same-frequency product | `product` | mean and twice-frequency channels require different phase pairings |

Each phase has two new variants per family. Within a sequence, one is assigned the
competent direct route and the other the named operator route. The two attempts are
four trials apart. Across sequences `M1` and `M2`, each variant is assigned once to
each route.

## D4-K route-key preflight (`C-key-v1`)

Before learner recruitment, obtain independent closed-book judgments from at least
two qualified reviewers for every recognition prompt. Each reviewer records one
route and a rationale without seeing the authored key or another review. The
executable audit returns:

```text
unreviewed | protocol_invalid | insufficient_review
agreed | ambiguous | key_disputed
```

The reviewer manifest records the assigned `R1`/`R2` order, declared expertise,
authored-key blinding, peer-review blinding, and provenance once per reviewer.
Task judgments reference that reviewer. A missing or unblinded manifest does not
delete the judgment; it produces `protocol_invalid` and an excluded-review count.

Only `agreed` tasks may contribute a keyed recognition-accuracy summary.
`ambiguous` and `key_disputed` tasks remain visible as selection distributions and
instrument defects; they are never silently rescored after learner outcomes are
seen.

Before opening learner recruitment, apply the frozen preflight kernel:

```text
any ambiguous or key_disputed task
  -> contract_revision_required
else any unreviewed, protocol_invalid, or insufficient_review task
  -> additional_review_required
else
  -> ready_for_learner_pilot
```

Revision has precedence over gathering more reviews because a semantic task/key
defect cannot be repaired by adding votes. `ready_for_learner_pilot` admits only the
recognition instrument; it is not a human-benefit disposition.

## D3-R recognition administration

- Use the separate recognition booklet with sequence `R1` or reversed sequence
  `R2`. Assign one sequence per participant.
- Show one prompt at a time. The learner selects exactly one of `direct`, `slice`,
  `event`, `projection`, `path`, `harmonic`, `product`, `symmetry`, or
  `refuse-card`.
- Stop at the decision. Do not solve the problem, reveal an answer, show a card, or
  reuse the item in `D3-E`.
- Record decision time. Correctness is restored from the frozen executable task,
  not entered by the administrator.

The direct and refusal decoys are essential. Without them, an instrument could
reward choosing some special operator on every prompt rather than recognizing when
reduction is warranted or invalid.

The frozen expected route is a scoring convention for these authored prompts, not
proof that human experts perceive a unique route. The pilot must record adjudicator
disagreement or recurring alternative justifications as an ambiguity defect before
confirmation.

## D3-E execution administration

- Obtain appropriate consent and use anonymous participant identifiers.
- Assign exactly one sequence per participant and never switch it mid-study.
- Use paper only. Do not expose the answer key or computation source.
- Reveal the prompt and its frozen assigned route together. Start the
  interpretation timer at that reveal.
- On an assisted operator trial, reveal only the corresponding operator card. No
  card is visible on an assisted direct trial.
- No card is visible during internalized or delayed-unseen phases.
- Use separate sessions for the three phases and record exact elapsed hours from
  the assisted reference session. An assisted row must record zero; a
  delayed-unseen row must record a positive interval. Do not reuse paper or answers
  between sessions.
- Run an independent whole-trial timer on every attempt. Record whether the four
  phase boundaries were observed reliably.

Timing phases are operationally defined as:

```text
interpretation: prompt + assigned-route reveal -> target/law model is bound
setup:          bound model -> first complete solvable relation representation
computation:    first solvable representation -> target value/expression
return:         target value -> units, regime/branch, and final source-law check
```

The independent whole-trial time, not the sum of phase fields, owns the speed
comparison. When phase timing is reliable, the loader requires the four phases to
sum exactly to that independent total. When it is unreliable, set
`phase_timing_reliable=false`; do not estimate missing boundaries, and do not use
the breakdown as phase evidence.

## Route instructions

**Direct:** use the shortest competent physical-law solution. Do not deliberately
recreate the general card notation.

**Operator:** use the assigned `slice`, `projection`, `path`, or `product` card. A
different correct method is retained as route nonadherence rather than silently
recoded as operator use.

All work remains in the accuracy dataset. A paired timing outcome is eligible only
when both matched attempts are complete, correct, and route-adherent.

## Outcome and error coding

Record unresolved final errors using zero or more semicolon-separated codes:

```text
target; law; representation; algebra; branch; sign; unit; return; timeout
```

A correct row must be complete and have no unresolved error. Incorrect, timed-out,
abandoned, or nonadherent work is excluded from paired timing but retained for
accuracy and feasibility analysis.

The primary speed quantity for one eligible pair is

```text
time_delta = operator total seconds - direct total seconds.
```

Negative values favor the operator. This is descriptive for a pilot. It does not
become a supported population or universal claim without a frozen statistical
model, a meaningful-effect threshold, and uncertainty evaluated on held-out data.
The current pilot summarizer therefore returns observed counts and signs while
fixing `speed_disposition=not_evaluated`.

## Frozen execution-pilot estimand (`C-pilot-time-v1`)

The independent sampling unit for timing is a participant, not one of that
participant's twelve matched pairs. For participant `p`, phase `q`, and the four
families `F`, construct

```text
d[p,q,f] = operator total seconds - direct total seconds
z[p,q]   = (1 / |F|) sum over f in F of d[p,q,f].
```

`z[p,q]` exists only when every family pair in that participant-phase is complete,
correct, and route-adherent. A failed attempt remains in the route-specific
accuracy, completion, and adherence counts but removes the whole participant-phase
from timing; the remaining family pairs cannot masquerade as independent learners.
Across participants, report the exact mean of `z[p,q]` and the sample variance only
when at least two complete participant clusters exist.

When every observation in a complete cluster has reliable phase boundaries, apply
the same construction separately to interpretation, setup, computation, and
return time. These component deltas diagnose where a total-time change arose; they
do not replace the independent total-time estimand.

For every phase, also report missing pair slots, ineligible pairs, all-attempt
direct/operator correctness, completion, adherence, timing reliability, unobserved
variants, and the largest direct/operator assignment imbalance for one variant.
`design_inputs_observed` means only that a cross-participant timing variance is
computable in every phase. It is neither a sufficient pilot-size judgment nor a
speed-benefit disposition.

## Promotion and rejection boundaries

- **Speed support:** requires correctness not to fall beyond a preregistered
  tolerance and an uncertainty interval for held-out paired time reduction to clear
  the preregistered meaningful-effect threshold.
- **Accuracy support:** uses every assigned attempt, including unfinished work; it
  is not inferred from the both-correct timing subset.
- **Internalization support:** cannot be inferred from assisted trials.
- **Delayed robustness support:** cannot be inferred from immediate internalized
  trials.
- **Cross-family transfer:** cannot be inferred from this D3 bench.
- **Universal framework speed:** remains rejected by the existing structural cost
  bench regardless of a local positive result.

The first pilot estimates adherence, phase-boundary reliability, variant imbalance,
and participant-clustered time variability. Sample size for a confirmatory study is
set only after those quantities are observed and the pilot is excluded from
confirmation. The meaningful-effect and accuracy-loss thresholds must be justified
without tuning them to whichever pilot direction appears favorable.

## Materials and executable boundary

- [participant booklet](d3-micro-tool-booklet.md)
- [route-recognition booklet](d3-route-recognition-booklet.md)
- [administrator answer key](d3-micro-tool-answer-key.md)
- [empty execution TSV schema](d3-micro-tool-observation-template.tsv)
- [empty recognition TSV schema](d3-route-recognition-observation-template.tsv)
- [empty independent route-key review schema](d4-route-key-review-template.tsv)
- [empty route-key reviewer manifest](d4-route-key-reviewer-template.tsv)
- [blinded route-key reviewer packet](d4-route-key-reviewer-packet.md)
- [operator cards](../../operator-cards.md)

The execution loader restores phase, pair, variant, and assigned route from the
executable schedule; it refuses assignment tampering, invalid card visibility,
unknown error codes, duplicate observations, mixed sequences for one participant,
an inconsistent reliable timing sum, invalid delay, and a correct row with an
unresolved error. The recognition loader independently restores task and expected
route and rejects schedule tampering. The key audit refuses duplicate reviewer/task
judgments, admits only manifested blinded reviewers, and distinguishes absent or
invalid evidence from agreement. A cohort validator
refuses any participant identifier present in both learner instruments. The
outcome constructor creates a time difference only from two correct, complete,
route-adherent execution attempts, using the independent total timer.
