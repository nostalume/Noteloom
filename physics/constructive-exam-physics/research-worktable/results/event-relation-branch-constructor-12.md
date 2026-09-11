# Result 12: event relation and physical-branch constructor

## Question and spine binding

Can the framework generate an event equation and its physical branch rather than
receiving the final event formula as a supplied law?

- **Upstream anchor:** Q0 ranks event/branch generation as the largest finite
  operator gap in the indexed A617 corpus; the existing polynomial backend already
  projects supplied exact relations.
- **Bridge question:** turn a state evolution, an observable component, and the
  verbal event meaning into a retained event-coordinate relation with full-state
  lift and domain certificates.
- **Invariant target:** the same physical event before and after elimination.
- **Downstream effect:** a new input can return a unique event, an ambiguous set, no
  reachable event, or a typed backend refusal without being given its answer
  polynomial.
- **Special resources:** finite zero-dimensional polynomial systems over exact
  rational coefficients and constant closed interval domains.
- **Research horizon:** one source-bound unseen transfer, two branch-boundary
  fixtures, nonpolynomial refusal, and variable-budget refusal. Symbolic parameter
  domains, inequalities between parameters, transcendental events, and derivation
  of the state laws from prose are outside this bench.

## Generated object

The retained interface is

```text
ConstructEvent(state laws, event predicate, unknowns,
               event coordinate, physical intervals, resource budget)
  -> projected event relation
  -> all finite algebraic full-state lifts
  -> real interval-admissible lifts
  -> unique selected branch
     or ambiguity/no-event/refusal certificate.
```

The caller does not supply an expected answer relation or root. A
provenance-bearing event predicate states what vanishes. Exact elimination generates
its coordinate equation. A finite polynomial solve reconstructs every state branch;
substitution into every original law and the predicate certifies each lift. Closed
physical intervals then filter the branches. More than one admissible lift is
reported as ambiguity rather than resolved by expression order.

This is a constructional tool, not a new physical law. The state evolution, the
observable whose component defines the event, and the physically traversed domain
remain justified physics inputs.

## Source-bound transfer: A617 2015 problem 1

The supplied compilation was inspected at PDF page 25, including a visual render of
the statement and pendulum diagram. It gives a pendulum released from rest at

```text
cos(theta) = 1/10
```

and asks for the later angle `phi` at which the resultant force is horizontal.
No answer from the compilation is used.

Construct dimensionless state coordinates

```text
c = cos(phi),
s = v^2/(g l),
a = a_y/g                         (downward vertical positive).
```

The released descent supplies the physical interval

```text
1/10 <= c <= 1.
```

Mechanical-energy evolution constructs

```text
s - 2(c-1/10) = 0.
```

The downward component of radial plus tangential acceleration constructs

```text
a = sin^2(phi) - s cos(phi),

a - 1 + c^2 + sc = 0.
```

The event meaning supplies only the predicate

```text
horizontal resultant <=> a = 0.
```

Eliminating `s` and `a` generates

```text
c^2 - c/15 - 1/3 = 0,
```

equivalently

```text
15c^2-c-5=0.
```

The finite full-state solve produces two algebraic lifts:

```text
c_- = (1-sqrt(301))/30,   s_- = (-2-sqrt(301))/15,   a=0,
c_+ = (1+sqrt(301))/30,   s_+ = (-2+sqrt(301))/15,   a=0.
```

Both tuples are substituted into the two state laws and the event predicate and
give zero exactly. Only `c_+` lies on the declared released arc; `c_-` also gives a
negative scaled speed and is not a state reached by this motion. Therefore

```text
cos(phi) = (1+sqrt(301))/30,
phi = arccos((1+sqrt(301))/30)
    ~= 0.9126580386 rad
    ~= 52.29 degrees.
```

The executable output contains the generated monic polynomial, two algebraic
branches, one admissible branch, the selected exact cosine, and three passing
certificates: eliminated-symbol closure, exact elimination-ideal construction, and
full-state/unique-domain recovery.

## Adaptation and refusal semantics

The common object is not a mechanics chapter label. It is the zero set of an event
functional restricted to an admissible evolution:

```text
state relation R(z)=0
  + observable map q=Q(z)
  + event predicate q=0
  + reachable domain D
  -> projection onto event coordinate
  -> full-state lifts intersected with D.
```

This covers, when their laws are supplied in the admitted algebra, contact loss
(`normal force = 0`), turning (`radial speed = 0`), component alignment
(`forbidden component = 0`), collision (`relative separation = 0`), and threshold
crossing (`diagnostic-threshold = 0`). Their area-specific semantics remain in
`Q`, provenance, and `D`; the projection/lift/filter operation is shared.

The tests also establish three non-success outputs:

| Output | Constructed meaning |
| --- | --- |
| `ambiguous_event_branches` | two exact full-state roots survive the supplied domain |
| `no_admissible_event` | algebraic roots exist but none lies in the physical domain |
| `unsupported_relation_shape` | a required relation, such as `cos(angle)`, is outside the rational-polynomial backend |
| `variable_budget_exceeded` | the declared event state is too large before branch solving begins |

## Human computation and route admission

The exam-readable residue of the constructor is a three-question card:

```text
1. What observable component vanishes at the requested event?
2. Which evolution or invariant expresses that component in one state coordinate?
3. Which interval or orientation was actually traversed?
```

For A15-01 this becomes `a_y=0`, energy substitution, and
`1/10 <= cos(phi) <= 1`. It prevents a common error—selecting an algebraic root
before checking whether it lifts to the motion—but it is not cheaper than the
competent direct derivation when written literally.

The atomic handwritten audit gives

```text
direct route:       (2,1,2,2,1,0,1)
literal event card: (3,2,3,3,1,1,1)
```

on `(relations, hidden quantities, peak live relations, symbolic actions, branch
checks, representation changes, return checks)`. The direct route wins on every
strictly increased axis, so its admission class is `always_direct` for positive
action weights. The executable constructor is therefore supported here as a study,
answer-generation, and branch-audit tool—not as an A15-01 handwritten shortcut.
Whether repeated use of the compact three-question card improves learner time,
error, retention, or transfer remains an empirical D2/T0 question.

## Supported frontier

This closes the first bounded Q0 bridge: the framework now generates an event
equation, reconstructs its full branches, and performs an exact physical-domain
selection on a newly executed A617 problem. It does not close I0. Conservation of
energy and the acceleration projection were still supplied as justified physical
relations; deriving such laws or invariants from primitive dynamics remains open.

The next event-constructor expansion is warranted only if it changes one of two
downstream claims: parameterized-domain support must enable a genuinely new source
family, or an unseen learner study must show that the compact event card changes
correct-route performance. Merely encoding more zero predicates would be an
explanatory plateau.
