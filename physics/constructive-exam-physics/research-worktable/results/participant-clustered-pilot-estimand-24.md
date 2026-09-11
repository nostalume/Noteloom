# Result 24: participant-clustered pilot estimand

## Tension

`C-human-v2` records the observables needed for a learner pilot, but its first
summary counted eligible family pairs and their signs. One execution participant
contributes four families in each of three phases. Treating those pairs as
independent would multiply the apparent sample size and use within-person
variation as if it were between-learner evidence.

The schema was observable-complete; the analysis operation was not yet
estimand-complete.

## Construction `C-pilot-time-v1`

For participant `p`, phase `q`, and family `f`, the already frozen paired outcome is

```text
d[p,q,f] = t(operator) - t(direct).
```

Let `F` be the four frozen families. The constructor admits a participant-phase
only when all four `d[p,q,f]` exist under the complete, correct, route-adherent
timing rule, and returns

```text
z[p,q] = (1 / 4) sum over f in F of d[p,q,f].
```

For `n_q` admitted participant clusters in phase `q`, it computes exactly

```text
mean[q] = (1 / n_q) sum over p of z[p,q]
var[q]  = sum over p of (z[p,q] - mean[q])^2 / (n_q - 1).
```

The variance is absent when `n_q < 2`. It is not replaced by zero. If all eight
observations forming one participant-phase cluster have reliable timing
boundaries, the same averaging map returns a four-component delta for
interpretation, setup, computation, and return. Their sum recovers the independent
total delta, but component timing never substitutes for that total.

## Preservation and refusals

Incorrect, incomplete, or nonadherent work remains in all-attempt accuracy,
completion, and adherence counts. It makes its pair timing-ineligible and therefore
removes the participant's entire four-family cluster from the timing estimand. This
prevents the easiest surviving families from determining the time claim.

Each phase additionally returns expected and missing pair slots, eligible and
ineligible pairs, timing reliability, unobserved variants, and maximum per-variant
direct/operator assignment imbalance. The constructor refuses duplicate pair,
family-within-phase, variant, or observation identities and observations whose
phase, variant, or assigned route conflicts with their pair.

## Synthetic witness

Two synthetic participants contribute complete data in every phase. Their four
family deltas average to `-25` and `15` seconds. The unchanged constructor returns

```text
cross-participant mean:             -5 seconds
cross-participant sample variance: 800 seconds^2
maximum variant-route imbalance:     0
```

Changing one operator attempt to incorrect retains all eight operator attempts and
records seven correct, but reduces eligible pairs from eight to seven and complete
timing clusters from two to one. The remaining cluster mean is `15` seconds and
the variance becomes absent. These are computation fixtures, not learner evidence.

## Present disposition and boundary

The checked-in execution template has zero rows, so every phase has zero clusters,
no mean, no variance, and no phase decomposition. The returned status is
`unobserved`.

`design_inputs_observed` will mean only that at least two complete timing clusters
make a variance computable in every phase. It will not certify sample adequacy,
speed improvement, accuracy noninferiority, internalization, or delayed robustness.
Those decisions require a separately frozen confirmatory contract constructed from
pilot design inputs and evaluated on new held-out learners.
