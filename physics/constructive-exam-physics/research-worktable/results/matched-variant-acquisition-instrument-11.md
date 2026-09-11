# Result 11: matched-variant acquisition instrument

## Question and source binding

Can the empty observation node be turned into a usable experiment whose data can
enter the paired-route calibrator without reusing a training problem as validation?

The six structures remain bound to the local 36-page A617 compilation, SHA-256
`B84E9D24468628433D1A126771DC8DE5A9D3CA7C2DBD01A78597FDDF01C8D764`.
PDF pages 4, 7, 10, 26, 29, and 33 were re-extracted and visually inspected. The
new questions are authored numerical variants, not official A617 items.

## Constructed instrument

The instrument contains:

- six source-bound matched pairs and twelve unique numerical variants;
- exact symbolic answer keys with branch, regime, unit, and frame checks;
- four calibration families and two problem-family holdouts;
- two counterbalanced sequences, each divided into two six-problem blocks;
- an empty TSV observation schema and a validated loader into W0 observations.

The two variants of a source structure appear six positions apart. Each block has
three direct and three proposed assignments. Across sequences `S1` and `S2`, every
variant is assigned once to each route, balancing route order and variant assignment
at cohort level.

## Rank and holdout construction

On the active axes `(H,P,S,X)`, the four calibration families have delta matrix

```text
             H   P   S   X
A25-03       0   0   1   1
A15-08       0   0   0   1
A13-02      -1   0  -1   1
A11-03       0   1   0   1
```

Its rank is four, so the four active coefficients are algebraically identifiable.
A24-09-3 and A22-03-1 are excluded from fitting and retained as holdout families.
Their deltas use no axis outside `(H,P,S,X)`, so W0 can predict them without filling
an unmeasured coefficient.

This split is deliberately by source problem, not by repeated observation row. It
therefore satisfies the calibrator's training-problem leakage guard.

## Material outputs

- `observations/d1-study-booklet.md` contains route cards, both schedules, and all
  participant-facing problems.
- `observations/d1-answer-key.md` contains exact administrator-only answers and
  physical return checks.
- `observations/d1-observation-template.tsv` contains the accepted ingestion schema
  and no empirical rows.
- `computation/worktable/study_cases.py` constructs all prompts and exact answers.
- `python -m worktable study-audit` reproduces pair counts, rank, empty-data status,
  and both schedules.

The TSV loader requires distinct matched variants, declared route order, positive
times, Boolean correctness, participant/session provenance, and a known source
problem. It restores the route boundary from the locked H0 ledger instead of
trusting a typed cost delta.

## Supported claim and failure boundary

Six new tests establish source-page bindings, answer-key equalities, rank four,
holdout-axis coverage, two-sequence counterbalancing, empty-template honesty, and
provenance-bearing ingestion. This validates the acquisition instrument, not equal
human difficulty or exam leverage.

The authored A/B variants are mathematically isomorphic within each source
structure, but equal cognitive difficulty is still a presumption. Counterbalancing
removes systematic variant assignment only across participants. For one learner,
four calibration pairs fit four coefficients with no residual degrees of freedom;
the two holdouts test prediction but do not provide a stable population estimate.
Strong evidence therefore needs participants assigned across both sequences or
additional independently authored variant sets.

The current empirical row count remains zero. D1 is now a supported, unpopulated
instrument. The next evidence-bearing action is a pilot that produces consented,
anonymized completed rows; without those observations the scientific claim must
remain unchanged.
