# Result 09: substrate-aware atomic handwritten cost reconstruction

## Question and obstruction

Can the route-admission boundary be used as a human exam tool when one ledger entry
may conceal several eliminations or recovered observables?

No: the earlier ledger admitted entries such as “eliminate five hidden quantities”
as one symbolic action. That convention measures a computer-algebra invocation, not
handwritten work. It made the capacitor and meeting-event compiler routes appear to
save symbolic actions without constructing those savings.

The earlier strict Pareto audit nevertheless reached the durable negative result:
there was no compiler-route Pareto win. This reconstruction preserves that verdict
while replacing its invalid non-atomic symbolic accounting. The corrected bench is
stronger and more precise: five direct wins and one conditional trade-off.

## Construction

Every route now declares an execution substrate:

```text
handwritten | tool_assisted
```

Routes are comparable only on the same substrate. A handwritten symbolic action
also declares its distinct **symbolic subjects**: the quantities whose expression
or solved/eliminated status is changed. Its atomic lower-bound cost is

```text
u(action) = number of distinct symbolic subjects.
```

Every non-symbolic ledger entry contributes one unit on its own axis. Thus

```text
eliminate (C_m, C_0, Q, U_i, U_f) -> 5 symbolic units,
recover (meeting time, meeting distance) -> 2 symbolic units.
```

An empty subject list, a duplicate subject, an unknown action kind, or a comparison
across substrates is rejected. The route vector is derived from the ledger; an
annotator cannot enter a claimed total separately.

This is deliberately a lower bound. It does not yet count expression size,
fraction complexity, arithmetic, or error probability. Its purpose is narrower: a
single line may not hide several output-changing handwritten operations.

## Recomputed six-case bench

| Problem | Direct vector | Proposed vector | Atomic verdict |
| --- | --- | --- | --- |
| A25-03 | `(3,2,3,2,1,0,1)` | `(3,2,3,3,1,1,1)` | always direct |
| A24-09-3 | `(6,5,3,5,1,0,1)` | `(6,5,6,6,1,1,1)` | always direct |
| A22-03-1 | `(2,1,2,2,1,0,1)` | `(2,1,2,2,1,1,1)` | always direct |
| A15-08 | `(2,1,2,2,1,0,1)` | `(2,1,2,2,1,1,1)` | always direct |
| A13-02 | `(3,2,2,3,2,0,1)` | `(3,1,2,2,2,1,1)` | conditional |
| A11-03 | `(3,1,2,3,1,0,1)` | `(3,1,3,3,1,1,1)` | always direct |

The capacitor trade-off vanishes because eliminating five quantities costs at least
five symbolic subject transformations. The meeting-event trade-off vanishes because
recovering time and distance has two subjects. The water-jet case remains genuinely
conditional:

```text
w_representation_changes
  < w_hidden_quantities + w_symbolic_actions.
```

Therefore the current exam rule is much more selective: use the direct route for
five locked cases; use the relational route for A13-02 only when a provenance-bearing
personal profile satisfies the displayed boundary and its peak-live budget.

## Semantic computation and certificates

The constructed input is an ordered, source-bound route ledger. The operation maps
each action to atomic axis units, sums the seven axes, subtracts direct from proposed,
and classifies the exact positive-weight region. Both routes retain the same physical
target, frame, units, regime, and return check.

Executable tests witness multi-subject counting, refusal of untyped symbolic work,
same-substrate comparison, the six revised Pareto results, and the revised admission
classes. The H0 and J0 scripts reproduce the complete vectors and boundaries.

## Supported boundary and next evidence

This correction supports a reproducible **structural lower bound**, not a cognitive
cost model. A tool-assisted elimination may legitimately be one invocation, but it
must live in a separate substrate and cannot be used to claim handwritten exam
leverage. Real learner weights, time, error, retention, and transfer are still
unmeasured.

The W0 frontier is now well-typed: collect repeated-self or learner observations on
atomic handwritten ledgers, estimate a provenance-bearing profile, and test route
choice on held-out problems. Until such observations exist, the single conditional
boundary remains a sensitivity statement rather than an empirical recommendation.
