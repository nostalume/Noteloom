# Computation Contract — Generative Residual Constructor

Parent node: [N10c generative residual constructor](../../nodes/10c-generative-residual-constructor.md)

## Semantic question

Can constrained bosonic and fermionic local complexes be produced from typed
natural-operator grammars and failed seed equations, without supplying the
Fronsdal or Fang--Fronsdal coefficients and carrier constraints to the constructor?

The retained interface is

```text
Construct(grammar, capability, resource budget)
  -> FieldSystem or obstruction record.
```

This first bounded grammar contains only

```text
Q: momentum degree 2, rank shift  0,
P: momentum degree 1, rank shift +1,
A: momentum degree 1, rank shift -1,
T: momentum degree 0, rank shift -2,
```

with the internally used relations

```text
A P = P A + Q,
T P = P T + 2 A,
T A = A T,
Q central.
```

The capability request fixes symmetric carrier shapes, no auxiliary carrier, and
momentum degree at most two. It does not supply `C`, `D`, `S`, or the trace/gamma
constraints.

## Construction

The program enumerates normal words with the required map type. It first seeks a
rank-lowering defect map `C` satisfying

```text
C P epsilon = Q epsilon.
```

The unconstrained residual cannot be cancelled. The remaining channel constructs
`T epsilon=0`; preservation by `P` then selects the shallowest field constraint
`T^2 phi=0`.

The admitted basis is generated as `{A,P T}`. Normal ordering computes the two
images; exact rational elimination returns

```text
C=A-(1/2)P T.
```

It then exports

```text
R=P,
D=Q-R C,
```

and independently solves the direct equation residual in the automatically
enumerated quadratic basis. Equality of the two generated outputs is an internal
certificate, not an input.

The same solver then receives the Clifford grammar `{Q,L,P,A,G}` with

```text
G P=P G+L,
G L=-L G+2A,
L^2=Q,
```

and the compatible ordering relations. Its unconstrained residual generates
`G epsilon=0`, then returns

```text
S=L-P G.
```

Searching the constraints preserved by `P` rejects depths one and two and
constructs `G^3 psi=0` at depth three.

## Run

```text
node check-residual-constructor.mjs
```

The check requires:

- exact semantic certificates `C R=Q`, `D R=0`, and `D+R C=Q`;
- coincidence of defect-factorization and direct-residual construction;
- residual generation of `T epsilon=0`, `T^2 phi=0`, `G epsilon=0`, and
  `G^3 psi=0`;
- zero non-null and two null cohomology classes for spins `2` through `6`;
- zero non-null and two null complex cohomology classes for fermionic tensor ranks
  `1` through `4`;
- an explicit refusal when the resource budget forbids trace operations.
- explicit refusals when the field-constraint depth is too shallow in either
  operator algebra.
- recovery of an automatically constructed admissible non-null source basis through
  the generated scalar Green-symbol response.

The component matrices are used only after generation, as finite-rank witnesses.
The existing N10 scripts remain separate regression oracles.

## Boundary

This is a cross-family regression generator and a downstream interface probe. Each
normal grammar is supplied rather than generated from arbitrary Lorentz carriers,
the null test checks quotient dimension rather than the complete little-group
action, and the Green response is not yet evaluated on a compact source with causal
support. Whole-route computational leverage is therefore not yet claimed.
