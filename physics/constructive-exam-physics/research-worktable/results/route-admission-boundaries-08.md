# Result 08: exact break-even boundaries for route admission

## Question

Can the solver decide when to stay with a direct physical solution and when to
activate a relational abstraction without hiding the decision inside arbitrary
cost weights?

The original strict Pareto audit exposed an obstruction retained and corrected by
[Result 09](atomic-handwritten-cost-reconstruction-09.md). Every literal compiler
route adds a representation action. Therefore a route that saves several symbolic
steps but adds that one setup step becomes a `tradeoff` and can never be called a
Pareto win. The gate correctly rejects unconditional dominance, but it cannot decide
whether the trade is worthwhile for a particular learner or tool context.

The repair is to construct the **break-even boundary**, leaving learner-specific
weights as declared inputs rather than silently fixing them.

## Construction

For the seven-axis route vectors

```text
c_direct, c_proposed in N^7,
```

construct

```text
Delta = c_proposed-c_direct.
```

A cost profile is a provenance-bearing positive vector

```text
w in Q_{>0}^7.
```

The exact cost difference is

```text
Delta C(w) = w dot Delta.
```

The proposed route is admitted exactly when

```text
Delta C(w) < 0,
```

subject to a hard peak-live-relation budget. The constructor returns one of four
structural results before any profile is supplied:

| Result | Delta condition | Meaning |
| --- | --- | --- |
| `always_direct` | every component is nonnegative and at least one is positive | no positive profile can rescue the abstraction |
| `always_proposed` | every component is nonpositive and at least one is negative | every positive profile favors the abstraction |
| `equivalent` | every component is zero | the structural ledger cannot distinguish the routes |
| `conditional` | Delta has both signs | return the exact half-space where abstraction pays |

This is not an empirical model of cognition. It is a symbolic sensitivity result:
the problem supplies the boundary, while measured or explicitly hypothetical
learner costs locate a user on one side of it.

## Six source-bound boundaries

| Problem | Class | Proposed route is cheaper when |
| --- | --- | --- |
| A25-03 | always direct | impossible for strictly positive weights |
| A24-09-3 | always direct | impossible for strictly positive weights |
| A22-03-1 | always direct | impossible for strictly positive weights |
| A15-08 | always direct | impossible for strictly positive weights |
| A13-02 | conditional | `w_X < w_H + w_S` |
| A11-03 | always direct | impossible for strictly positive weights |

Here `w_H`, `w_P`, `w_S`, and `w_X` are the declared costs of one hidden quantity,
one peak-live relation, one symbolic action, and one representation change.

Three conclusions follow.

1. The proper-time, capacitor, parallel-acceleration, de Broglie, and meeting-event
   cases should remain direct for every strictly positive cost profile represented
   by this model.
2. The water-jet case cannot be decided from problem structure alone. It requires
   the learner profile.
3. Route admission is not chapter classification. The same relativity area contains
   both `always_direct` and `conditional` cases.

## Water-jet use case

For A13-02 the proposed route removes one explicit hidden quantity and one symbolic
action, but adds one representation step. Its boundary is

```text
w_representation_changes
  < w_hidden_quantities + w_symbolic_actions.
```

Thus a learner who can enter the target-relation view cheaply, but finds an extra
intermediate flow variable and substitution expensive, should use the relation
route. A learner for whom the abstraction itself is expensive should solve directly.

Under a hypothetical unit-action sensitivity probe (`w_i=1`), A13-02 is admitted
and the other five remain direct. This is the first source-bound conditional use of
the route selector, but **not** evidence that real learners have unit weights.

## Human admission card

The hand rule is now:

```text
1. Construct the shortest direct route and one candidate structural route.
2. Cancel cost components common to both routes.
3. If only added costs remain, solve directly.
4. If only savings remain, use the structural route.
5. If both remain, write "setup debt < execution saving" explicitly.
6. Use a known personal bottleneck or a measured profile; otherwise keep the
   decision conditional.
7. Reject a route that exceeds the peak simultaneous-relation budget even when its
   weighted total would be smaller.
```

This changes the framework from one universal procedure into a portfolio of routes
with an internally calculated admission boundary.

## Evidence and boundary

The atomic reconstruction in Result 09 adds tests for symbolic-subject counting and
same-substrate refusal, then recomputes these boundaries. The current worktable
bench at that stage contained 82 passing tests after the event-constructor extension; the admission
tests described here remain unchanged. They prove exact delta construction,
dominance invariance under all positive profiles, profile-dependent reversal on the
conditional case, hard peak-budget refusal, positive-weight validation, and the
six-case J0 audit.

The result does not identify real cognitive weights, does not measure time or error,
and depends on the explicit atomic-subject convention of Result 09. It also compares
only one direct
and one proposed route per problem. The next decisive evidence is calibration:
observe learner or repeated-self route costs, bind them to a profile with provenance,
and test whether the admission decision predicts the cheaper correct route on held-
out problems. Until then, only the structural boundary—not the chosen side—is a
supported general result.
