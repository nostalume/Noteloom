# N1 matched network study protocol

This is the frozen acquisition contract `C-network-study-v1`. It can acquire the
evidence requested by `C-network-human-v1`; it contains no expert or learner
observations and therefore establishes no human-speed, retention, or transfer
claim.

## Questions kept separate

1. **Immediate assistance:** with the local sparse strip visible, can a learner
   execute it correctly and does total time differ from a competent direct nodal
   route?
2. **Delayed retention:** on new numbers in the same two topology families, can
   the learner execute the sparse route without the strip after a recorded delay?
3. **Unseen-topology transfer:** without the strip, can the learner use the same
   local rule on two topology families absent from training?

The phases are not interchangeable. Immediate work cannot support retention;
same-topology delay cannot support unseen-topology transfer.

## Preflight before learners

Give the neutral reviewer packet to at least two qualified reviewers per variant.
Each must solve independently, remain blind to the authored routes and peer
reviews, and judge the exact answer, both routes, and whether the direct baseline
is competent. A single admitted negative judgment produces
`revision_required`. Fewer than two admitted positive reviewers for any variant
produces `additional_review_required`. Recruit only after the executable audit
returns `ready_for_pilot`.

That status admits acquisition; it does not validate the method.

## Participant allocation

- Use anonymous identifiers and obtain appropriate consent.
- Assign one counterbalanced sequence, `N1` or `N2`, and never switch it.
- Use paper only. Reveal one prompt and its assigned route at a time.
- For `direct`, ask for the shortest competent nodal/balance-law solution; do not
  force a deliberately poor elimination order.
- For `sparse`, require the local strip below. A different correct method is
  retained as route nonadherence, not silently recoded.
- In `immediate_assisted`, show the strip only on a sparse trial. Show no strip in
  the two later phases.
- Run each phase in a distinct session. Record exact hours from the immediate
  session. The unseen session must occur after the delayed same-topology session.
- Do not reveal answers or return earlier scratch work between sessions.

## Sparse local strip

```text
1. Mark boundary nodes; keep their physical meaning fixed.
2. Among hidden nodes, choose one with minimum current fill; break ties by fewer
   active neighbors, then by the printed node order.
3. From k_pp*x_p + sum(k_pj*x_j) = f_p, write
      x_p = f_p/k_pp - sum(k_pj/k_pp)*x_j.
4. Substitute only into the active neighboring balances and delete p.
5. Repeat until only L and R remain; evaluate I_L at the stated boundary values.
6. Check the returned boundary law (sign and one balance/reciprocity check).
```

This strip preserves physical law selection and observable meaning. It compresses
only the elimination representation.

## Timing and scoring

Use an independent whole-trial timer. Phase fields are:

```text
interpretation: prompt/route reveal -> physical target and balances identified
setup:          balances identified -> first solvable representation complete
computation:    representation complete -> submitted target expression/value
return:         target obtained -> sign/unit/boundary-law check complete
```

When phase boundaries are reliable, their exact sum must equal the independent
total. Otherwise mark `phase_timing_reliable=false`; never estimate a boundary.
Enter the participant's normalized exact scalar in `submitted_answer`. The loader,
not the administrator, compares it with the route-independent executable key.

All attempts remain in accuracy counts. A pair contributes time only when both
routes are complete, exactly correct, and route-adherent. For participant `p`,
phase `q`, and its two topology pairs:

```text
d[p,q,f] = t_sparse - t_direct
z[p,q]   = mean over both f of d[p,q,f].
```

The analysis unit is `z[p,q]`, not an individual trial or pair. Mean and sample
variance are constructed across participants only; variance is absent below two
complete participant clusters. Pilot output is limited to design inputs and keeps
all benefit dispositions at `not_evaluated`.

## Error codes and boundaries

Use zero or more unresolved codes:

```text
target; law; representation; algebra; sign; unit; return; timeout
```

This instrument does not yet freeze a confirmatory meaningful-time threshold,
accuracy-loss tolerance, sample size, uncertainty interval, exclusion rule, or
stopping rule. Those must be fixed after a pilot and evaluated on new held-out
participants. It also does not measure unprompted recognition of when the sparse
tool should be refused; that remains a separate adaptive-admission instrument.

## Files

- [participant booklet](n1-network-study-booklet.md)
- [administrator answer key](n1-network-study-answer-key.md)
- [empty learner template](n1-network-study-template.tsv)
- [neutral reviewer packet](n1-network-key-reviewer-packet.md)
- [empty reviewer template](n1-network-key-review-template.tsv)
