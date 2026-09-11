# Result 23: route-key preflight decision kernel

## Tension

`C-key-v1` can acquire independent review, but acquisition alone leaves a policy
choice after results arrive. An ambiguous task could be dropped, rewritten, scored
with the author key, or subjected to more votes. Choosing among those routes after
seeing learner outcomes would make the recognition claim outcome-dependent.

The missing construction is a decision kernel frozen before expert or learner
evidence.

## Kernel `K-key-v1`

For each of the twelve task audits, the kernel partitions statuses into:

```text
admit      = {agreed}
review     = {unreviewed, protocol_invalid, insufficient_review}
revise     = {ambiguous, key_disputed}
```

It then applies one precedence order:

```text
revise nonempty -> contract_revision_required
else review nonempty -> additional_review_required
else -> ready_for_learner_pilot
```

This precedence is semantic rather than majoritarian. More votes can close absent
or insufficient evidence, but they cannot silently repair a prompt that already
supports incompatible routes or a key unanimously disputed by admitted reviewers.
Such a task requires a new prompt/key contract before learner results are seen.

The return preserves ordered task identifiers in three separate sets: admitted,
needs-review, and revision-required. It refuses missing, duplicate, or unknown task
audits rather than treating an incomplete audit table as readiness.

## Boundary

`ready_for_learner_pilot` means only that the recognition key passed this preflight.
It does not establish recognition accuracy, route usefulness, solution correctness,
retention, or time savings. A later learner disposition still requires D4-P data
under `C-human-v2`.

The kernel does not automatically replace a disputed authored route with the
reviewer plurality. A revision must state whether the defect was wording,
route-vocabulary overlap, multiple competent solutions, or an incorrect author
key, and must create a successor contract before recruitment.

## Verification and present disposition

The intended RED showed that no public preflight operation existed. Focused tests
now cover all-agreed readiness, simultaneous revision/review obligations, revision
precedence, and the empty-evidence case. Synthetic audits verify the operation but
are not expert evidence.

With the checked-in zero-row templates, all twelve tasks are `unreviewed` and
`K-key-v1` returns:

```text
status: additional_review_required
admitted tasks: 0
needs-review tasks: 12
revision tasks: 0
```

The human-benefit disposition remains `unobserved`. The next irreducible action is
still blinded external review; the worktable now fixes both its acquisition and its
consequences in advance.
