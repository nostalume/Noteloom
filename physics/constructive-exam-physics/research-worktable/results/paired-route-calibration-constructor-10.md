# Result 10: paired-route learner-cost calibration constructor

## Question

How can a personal route-admission profile be inferred from observed exam work
without confusing problem difficulty with the cost of the route representation?

Timing unrelated problems directly is not sufficient: a harder problem may take
longer even when its chosen route is better. The construction therefore uses
matched direct and proposed attempts on the same problem class or controlled
variants.

## Paired-difference construction

For problem or matched variant `i`, model the two correct route times as

```text
t_D,i = d_i + c_D,i dot w + e_D,i,
t_P,i = d_i + c_P,i dot w + e_P,i.
```

Here `d_i` is route-independent problem difficulty, `c` is the atomic seven-axis
ledger, and `w` is a personal seconds-per-unit profile. Subtraction constructs

```text
y_i = t_P,i-t_D,i
    = (c_P,i-c_D,i) dot w + (e_P,i-e_D,i).
```

The unknown nuisance term `d_i` cancels. With the rows `Delta c_i`, form the design
matrix `X`. Only axes that vary in the observations are active. The constructor
requires those active columns to have full rank and computes

```text
w_hat = (X^T X)^(-1) X^T y.
```

All arithmetic is exact rational arithmetic. The result retains residual sum of
squares, training sample IDs, problem IDs, substrate, order-control statement, and
source provenance. It refuses a fitted coefficient that is zero or negative rather
than silently clipping it into the positive cost model.

This linear additive model is a declared approximation, not a theory of cognition.
Its purpose is to turn the earlier arbitrary weight choice into a falsifiable
personal prediction.

## Admission and refusal grammar

Each observation contains:

```text
sample id
problem or matched-variant id
derived direct/proposed boundary
direct and proposed times
correctness of both attempts
provenance
order-control statement
```

Only pairs in which both routes are correct enter the timing fit. Incorrect pairs
are retained as exclusions rather than treated as fast solutions. The constructor
returns:

| Condition | Result |
| --- | --- |
| no pair has two correct attempts | `no_correct_pairs` |
| correct pairs have no cost variation | `no_cost_variation` |
| active cost columns are not independent | `insufficient_rank` |
| least-squares coefficient is nonpositive | `nonpositive_fit` |
| all active axes are identified with positive coefficients | partial calibrated profile |

A personal profile also contains a typed participant identifier; mixed-participant
training and another participant's holdout are refused. A profile is intentionally
partial: it contains only empirically identified axes.
A held-out route is refused when its delta uses another axis. Reusing a training
problem as “held out” is also refused. When both checks pass, the predicted sign of
`Delta c dot w_hat` is compared with the observed cheaper correct route.

## Executable evidence

Seven tests exercise the constructor. A synthetic exact-recovery fixture uses the
real six-case H0 delta matrix and declared weights on hidden quantities, peak-live
relations, symbolic subjects, and representation changes. The fit recovers those
four weights exactly. A separate unseen fixture consumes the profile in a route
prediction. Further tests force rank deficiency, an unphysical nonpositive fit,
incorrect-pair exclusion, training leakage, and an unidentified held-out axis.

This is regression and synthetic transfer evidence for the algorithm only. It is
not learner evidence. Running `python -m worktable calibration-probe` reports the actual worktable
state:

```text
empirical_observations  0
status                  refused
obstruction             no_correct_pairs
```

## Collection protocol and boundary

For real repeated-self data, use matched variants rather than immediately solving
the identical numerical item twice. Counterbalance route order, keep the same exam
conditions and allowed tools, time from interpretation through physical return
check, and retain incorrect attempts. Each proposed/direct pair must use the same
execution substrate and independently constructed atomic ledger.

Result 11 constructs a rank-four matched-variant instrument and two held-out source
families. A large number of repetitions along one delta direction still does not
repair rank deficiency. Until completed observation rows are collected, W0 remains
an implemented calibration constructor with an explicit data obstruction, not a
calibrated learner model.
