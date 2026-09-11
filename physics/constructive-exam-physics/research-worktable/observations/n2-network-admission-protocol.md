# N2 adaptive network-admission protocol

`C-network-admission-v1` measures whether a learner can classify a network as a
direct gate, a conditional sparse candidate, or a refusal without being assigned a
route. It contains no reviewer or learner evidence by itself.

## Separation from N1 execution

N1 asks participants to execute an assigned direct or sparse route. N2 asks them
to select a warranted status before solving. A participant must not enter both
cohorts in the same study wave: N2 vocabulary would prime N1, while N1 route
practice would train N2. The executable cohort validator rejects overlap.

## Frozen phases

| Phase | Task classes | Structural relation to training | Sheet visible |
| --- | --- | --- | --- |
| `immediate_unassisted` | gate, candidate, refusal | trained families, new coefficients | no |
| `delayed_same_topology` | gate, candidate, refusal | same three families after delay | no |
| `unseen_topology` | gate, candidate, refusal | three disjoint families later | no |

Each phase balances the three decisions, preventing an always-specialize or
always-refuse strategy from scoring well. `A1` and `A2` reverse order inside each
phase. The exact key is generated from the cost-boundary constructor or its typed
planner obstruction.

## Administration

1. Obtain appropriate consent and use anonymous participant identifiers.
2. Train every participant with the same training sheet, then remove it.
3. Assign exactly one sequence and reveal one task at a time.
4. Start the decision timer at reveal. Stop when the participant selects exactly
   one of `direct_gate`, `conditional_candidate`, or `refuse` and gives a brief
   structural justification. Do not solve the network or reveal the key.
5. Run each phase in a distinct session. Record exact elapsed hours from the end
   of training. The unseen session must occur after the delayed session.
6. Do not return prior tasks, answers, or scratch work.

Completion may be `complete`, `timeout`, or `abandoned`. The loader restores phase,
task, and expected decision from the frozen schedule and exact constructor.

## Analysis unit

A participant-phase is complete only when all three decision classes are present
and complete. Its accuracy and mean decision time are computed across those three
tasks; only these participant-phase values are averaged across participants.
Individual tasks do not masquerade as independent learners. Selection counts and
all errors remain visible.

`design_inputs_observed` requires two complete participant clusters in every
phase. It is not a recognition, retention, or transfer verdict. Confirmatory
thresholds, accuracy tolerances, uncertainty, sample size, exclusions, and stopping
rules remain to be frozen from pilot design inputs and evaluated on held-out
participants.

## Key preflight

At least two qualified reviewers per task must independently classify while blind
to the authored key and peer work. They judge both key agreement and prompt
ambiguity. An admitted disagreement or ambiguity yields `revision_required`;
insufficient admitted reviews yield `additional_review_required`; only complete
agreement yields `ready_for_pilot`.

## Materials

- [training sheet](n2-network-admission-training.md)
- [participant booklet](n2-network-admission-booklet.md)
- [administrator key](n2-network-admission-answer-key.md)
- [reviewer packet](n2-network-admission-reviewer-packet.md)
- [empty observation template](n2-network-admission-template.tsv)
- [empty reviewer template](n2-network-admission-review-template.tsv)
