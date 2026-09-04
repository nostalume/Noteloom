# Natural-operation grammar

Status: generated for bounded free-power and first-order factorization requests

## Obstruction

The residual solver cannot be generative if its token list and relations already
encode the desired field equation. Construct the operation grammar from carrier
laws and admitted invariant resources first.

## Typed request

Input:

```text
free power: symmetric or exterior power of V*
coefficient action: optional module action
resources: metric pairing, invariant tensors, Clifford factorization
budget: maximum word length and rank range
```

No field coefficient, route name, or expected equation is an input.

## Construction

Functorial multiplication and derivation generate rank-raising/lowering operations.
Metric duality generates trace/insertion only when the metric resource is present.
Exterior exchange generates its sign; Clifford factorization generates its
quadratic reduction.

For example, evaluating both composites on one symmetric tensor constructs

```text
A P - P A = Q + U T-sensitive rank term,
```

with the precise rank coefficient computed from the power law. For exterior power,
the exchange calculation instead generates

```text
A P = -P A + Q,  P^2=A^2=0.
```

For a requested first-order factor `G`, polarization of `G(p)^2=Q(p)I` generates
the Clifford relation rather than importing gamma components.

## Normalization and refusal

Orient relations by an explicit decreasing word order. Enumerate words only up to
the supplied budget, reduce them, and verify idempotence:

```text
N(N(w))=N(w).
```

Return a typed refusal for missing metric/action/factorization resources,
nondecreasing rules, ambiguity within the bounded closure, or insufficient depth.

## Retained interface

```text
NaturalGrammar(carrier_law, resources, budget)
  -> operations + typed degrees + rewrite rules + certificates
  | refusal(reason, unresolved_words, provenance)
```

The implementation and transfer certificates live in the shared computation
workbench. Symmetric, exterior, and Clifford cases test regression and transfer.

## Edges and boundary

- [Residual compiler](14-residual-repair-compiler.md) consumes the grammar.
- [Carrier/source boundary](15-carrier-source-obstructions.md) consumes projected
  operations and costs.

The compiler does not enumerate arbitrary invariant maps, mixed-symmetry carriers,
or carrier presentations from a particle label. That depth-4 problem remains open.
