# Typed relation planner for natural tensor reduction

## Frozen contract `C_G2_v1`

G1 constructs a smaller exact route, but the elasticity adapter still says
“metric first” and translates two named symmetry classes by hand. The obstruction
is now route assembly, not row reduction: a new tensor kind would require editing
the adapter even when it satisfies an already known mathematical relation.

G2 compares two alternatives on the unchanged G1 input and observable:

1. **Plural hand-selected adapters:** retain the G1 code path and document each
   new structured order beside its physics schema.
2. **Typed relation planner:** tensors expose only rank, slot-action type,
   permutation generators, certified capabilities, and components. Generic rules
   match those facts, emit route operations with prerequisites and certificates,
   and expose typed rejection when no rule is justified.

The planner may know the mathematical rules “a nondegenerate symmetric bilinear
form generates its infinitesimal kernel” and “a permutation-invariant covariant
tensor admits orbit coordinates.” It may not know the words elasticity, axis,
rotation, or the expected stabilizer dimension/basis.

## Typed objects and laws

A relation input consists of

```text
TensorRelation = (
    tensor: V*^(tensor rank),
    slot_action: covariant,
    permutation_generators: subgroup generators in S_rank,
    capabilities: certified semantic predicates,
    certificate_origin: construction | checked input
)
```

The admitted capability in `C_G2_v1` is
`nondegenerate-symmetric-bilinear-form`. Its rule emits

```text
candidate module: g^-1 Lambda^2(V*)
discharged defect: delta_g
certificate: image = ker(delta_g)
```

For every remaining tensor, the permutation generators act on multi-indices. The
planner constructs their finite orbits and retains the lexicographically least
index of each orbit. This replaces the G1 strings `symmetric-2` and `elasticity` by
one algorithm. Completeness follows from two typed facts: the input tensor is
certified invariant under those generators, and the covariant infinitesimal action
commutes with slot permutations.

An empty permutation list means “no symmetry declared,” not “symmetric.” The raw
route remains admissible, but a requested structured codomain must return
`UndeclaredPermutationSymmetry`; it may not guess a compression.

## Frozen discriminators

- The planner emits both raw and structured route plans from the frozen tensor
  relations; the adapter contains no metric-first route assembly.
- The structured dependency order is
  `metric-kernel -> permutation-orbits -> defect-kernel -> bracket-closure`.
- Generic orbit construction yields 6 representatives for a symmetric rank-two
  tensor and 21 for the elasticity permutation generators in dimension three.
- The public elasticity and axis outputs, exact raw/structured span coincidence,
  costs `1638/117`, break-even 8, and observable error remain unchanged.
- Removing the permutation certificate from a rank-four tensor yields a typed
  structured-plan rejection while leaving the raw plan intact.
- Removing or duplicating the seed capability yields respectively a missing or
  ambiguous seed rejection; no arbitrary preferred seed is chosen.

The candidate is falsified if a physics-kind branch remains in the planner, an
expected group/basis enters a rule, undeclared symmetry is used, plan replay is
nondeterministic, or route construction changes the frozen observable.

## Pseudocode and code boundary

```text
plan(relations):
    raw <- End(V) + full targets for every tensor

    seed_sources <- tensors carrying nondegenerate-symmetric-form
    if count(seed_sources) != 1:
        reject structured plan with MissingSeed or AmbiguousSeed

    candidates <- metric_kernel(seed_sources[0])
    operations <- [metric-kernel]
    for tensor in input order except discharged seed:
        if tensor has no certified permutation action:
            reject structured plan with UndeclaredPermutationSymmetry
        targets <- orbit_representatives(tensor.permutation_generators)
        operations += [permutation-orbits(tensor), tensor-defect(tensor)]

    operations += [simultaneous-kernel, visible-quotient, bracket-closure]
    return raw plan, structured plan, deterministic cost/dimension estimates

execute(plan, budget):
    pass plan candidates, blocks, action, and bracket to defect compiler
    preserve plan certificates and rejection in the public witness
```

The new planner is limited to roughly 250 source lines. The generic tensor algebra
remains below roughly 330 lines and the physics/use adapter below roughly 500 after
route assembly is removed. Exact relation planning is finite and deterministic;
global search optimality, arbitrary Young functors, mixed variance, spinors, jets,
nonlinear symmetries, and analytic integration are outside `C_G2_v1`.

## Evidence ledger

- `E-G2-01` (exact construction tests): anonymous rank-two and rank-four tensors,
  identified only by capabilities and three permutation generators, deterministically
  generate the five-operation structured plan. The orbit target has dimension 21,
  and replay returns an equal immutable plan.
- `E-G2-02` (adversarial refusals): an uncertified rank-four permutation relation
  yields `UndeclaredPermutationSymmetry`; zero metric-capable tensors yield
  `MissingSeedRelation`; two yield `AmbiguousSeedRelation`. In each case only the
  raw plan remains preferred, so input order cannot choose a hidden answer.
- `E-G2-03` (public regression/use): the unchanged elasticity and axis fixtures
  preserve the G1 stabilizer spans, ranks, exact brackets, costs, budget behavior,
  and controlled observable. The detailed witness now exposes relation facts,
  both plans, completeness certificates, and the selected rule chain.

## Cost distinction exposed by the probe

The old `117` is still the declared defect-compilation proxy. Generic orbit
construction, however, currently canonicalizes all `3^4=81` indices against the
eight-element permutation group, an upper-bound 648 permutation checks. Counting
that transparent planner work gives

```text
raw:        compiler upper bound 1782 + target planning 90  = 1872
structured: compiler proxy       117 + orbit checks    648 = 765.
```

The structured route still wins this expanded proxy, but its corresponding
repeated-query break-even is 48 rather than the stabilization-only value 8. Neither
proxy is a runtime measurement, and metric inversion/candidate arithmetic are not
normalized in this count.

The present benchmark executable also materializes **both** planned routes because
exact raw/structured span equality is its certificate. The witness now labels this
policy explicitly. Consequently, 765 is a selected-route model, not the measured
cost of the current comparison process. Operational leverage requires a lazy
executor that checks budgets from symbolic dimensions, materializes only the
selected route, and runs the raw comparison only as a separate audit.

## Disposition

`C_G2_v1` is **supported bounded** for deterministic, physics-name-free route
assembly and typed refusal in the admitted covariant-tensor grammar. It improves
internal and human computability: the reader sees a five-rule dependency chain
rather than adapter control flow, and the same planner accepts anonymous tensors.

The computational-leverage dimension is **restricted**. Genericity has reintroduced
a raw `d^r |Pi|` orbit-canonicalization bound before the compressed defect map is
formed, and certification still executes both alternatives. These costs are visible
rather than hidden, but this is not the desired final machine. The next bridge must
construct quotient coordinates compositionally—at least for symmetric blocks and
block exchange—and materialize only an admitted selected route.
