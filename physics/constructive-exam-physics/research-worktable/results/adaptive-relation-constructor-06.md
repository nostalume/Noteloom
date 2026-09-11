# Result 06: obstruction-guided adaptation to an unidentified problem

## Question

Can the relation compiler act when a problem has not already been assigned a
chapter label or a hand-selected law subset?

Yes, within a precise boundary. The new constructor accepts an unordered finite
bag of justified physical laws, the givens, one target, and a resource budget. It
discovers a smallest supplied-law packet whose exact projection constrains the
target. It does **not** invent a physical law missing from that bag.

This changes the interface from

```text
human names the correct laws -> eliminate hidden quantities
```

to

```text
human supplies plausible laws with provenance
  -> construct target-connected component
  -> enumerate packets by increasing law count
  -> eliminate their hidden quantities exactly
  -> return a minimal packet and target relation, or a typed obstruction.
```

## Constructed object

The executable interface is

```text
Construct(law bag, givens, target, law/attempt/variable budgets)
  -> selected laws
  -> projected exact relation
  -> all equivalent minimal packets
  -> elimination certificates
  -> attempt count
  -> obstruction and next action on refusal.
```

The inputs do not contain the expected answer. A law is a relation plus a name and
provenance. Search first removes law components disconnected from the target. For
packet sizes `1,2,...,k`, it eliminates every hidden symbol and checks whether the
resulting elimination ideal contains a relation involving the target. Search stops
only after the whole first successful size has been checked, because otherwise it
could hide a competing explanation.

The first successful size is minimal in number of supplied laws inside the declared
search bounds. This is not a proof of minimum handwritten time or minimum algebraic
operation count.

## Ambiguity is a result

Two smallest packets can have three different meanings:

1. Their canonical projected ideals coincide. They are algebraically equivalent;
   the cheaper expression packet is returned and both packets remain visible.
2. Their projected ideals differ. The constructor returns
   `ambiguous_minimal_packets`; it does not rank physical explanations by algebra.
3. One packet violates a regime, sign, dimension, or provenance condition. That
   rejection belongs to the physical return layer, not to polynomial elimination.

Thus adaptation is not unrestricted equation matching. Mathematical reachability
generates candidates; physical semantics adjudicates them.

## A617 transfer without a problem-family label

The transfer test supplies the A617 2013 water-jet relations from PDF page 29 in a
bag containing unrelated capacitor and atomic relations. The request contains the
givens

```text
(launch speed, gravity, detached fraction, density, jet area, supported mass)
```

and target `height`, but no mechanics/fluid chapter label and no selected law names.
The target-connected search checks three candidate packets and selects exactly

```text
ballistic speed,
momentum flux.
```

Eliminating impact speed returns an ideal containing

```text
(2-alpha)^2 rho^2 A^2 u^2 (u^2-2gh) - m^2 g^2 = 0.
```

The test verifies this relation by exact ideal membership. The unrelated laws do
not enter the selected packet. The physical branch obligations—nonnegative impact
speed and height—remain for the return step.

## Refusal map for unfamiliar inputs

| Obstruction | Calculated meaning | Required human response |
| --- | --- | --- |
| `no_target_path` | no supplied law mentions the target | recall or derive a target-bearing law |
| `disconnected_target` | the target component neither reaches a given nor fixes the target alone | supply a bridge law or datum |
| `target_not_constrained` | hidden freedom survives every admissible packet | add an independent law/condition or weaken the target |
| `ambiguous_minimal_packets` | smallest packets imply different retained relations | use regime, sign, dimension, or provenance evidence |
| `unsupported_relation_shape` | a necessary candidate is not an exact rational polynomial system | route it to an integral, differential, transcendental, inequality, or piecewise backend |
| `search_budget_exceeded` | minimality/closure was not certified inside the declared budget | prune with justified structure or raise the budget |

These codes distinguish “I do not know the physics” from “the supplied physics is
underdetermined” and from “the current algebra backend is the wrong tool.”

## Human computation rule

The executable exhaustive search is exponential in the worst case:

```text
sum from j=1 to k of C(m,j) elimination attempts
```

where `m` is the number of target-connected laws. The exam version therefore uses
the same construction as a best-first hand search:

1. Circle the target and write every law that directly contains it.
2. Mark the unknown symbols in each law as open ports.
3. Attach the cheapest remembered law that closes an open port toward a given.
4. Eliminate immediately; stop expanding a route once the target is constrained.
5. If two routes close at the same depth, test units, regime, signs, limits, and
   source meaning before choosing.
6. If no route closes, name the obstruction instead of adding algebra blindly.

This is the computational reduction: solve the smallest relation packet, not the
full physical state and not the whole chapter taxonomy.

## Evidence and boundary

Nine new software tests cover distractor rejection, competing minimal packets,
equivalent packets, missing target paths, disconnected data, underdetermination,
law-budget exhaustion, nonpolynomial refusal, and the A617 water-jet transfer. The
full bench now contains 46 passing tests.

The construction adapts to unknown **arrangements of known justified laws**. A
problem requiring a genuinely absent constitutive law, new physical object, or new
experimental datum correctly stops. The next research layer is therefore not more
subset search: it is typed law generation from events, boundaries, symmetries, and
conservation obstructions, followed by the same relation constructor.
