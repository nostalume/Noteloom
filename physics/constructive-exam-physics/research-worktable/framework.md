# Target-conditioned observable construction

This document owns the stable semantics shared by the bounded constructions. It
does not replace area physics: a human or admitted adapter must still supply the
objects, laws, regime, geometry, conventions, and requested observable. Detailed
derivations and evidence belong to the linked [results](results/); learner practice
belongs to the project-root [manual](../observable-reduction.typ),
[kernel](../exam-kernel.typ), [cards](../operator-cards.md), and
[drills](../mixed-drills.md).

## One invariant across four layers

For givens `g`, hidden quantities `h`, and requested observable `o`, the physical
packet defines an admissible relation

```text
R subset G x H x O.
```

The answer object is its target-conditioned projection

```text
Ans_R = {(g,o) : there exists h with (g,h,o) in R}.
```

The invariant is not an equation's appearance. It is the same physically
admissible `(g,o)` pairs with the same units, regime, orientation, branch, boundary
data, and observable convention. Four layers keep that invariant inspectable:

| Layer | Owns | May forget | Must export |
| --- | --- | --- | --- |
| physical packet | quantities, laws, geometry, regime, givens, target, conventions | nothing needed by physics | justified typed relation and provenance |
| semantic extraction | target dependency and reusable structure | quantities disconnected from the target | exact forgotten distinctions and return obligations |
| mathematical computation | elimination, quotient, closure, projection, spectral/variational operation | area vocabulary not used by the operation | relation/result, witness, branches, obstruction or refusal |
| physical return | original target meaning | no required distinction | units, signs, regime, branches, limits, and original-law check |

An empty fibre means inconsistent assumptions. Several admissible members expose a
branch obligation. No target-bearing consequence means underdetermination. A
returned equation is not yet an answer when its candidate solutions cannot lift
to the original physical relations and side conditions.

## Physical packet and return ledger

Before generic computation, construct one packet:

```text
PhysicalPacket {
  source and provenance,
  typed quantities and dimensions,
  givens and exactly one target,
  justified laws and geometry,
  regime and boundary/initial data,
  sign, orientation, phase and branch conventions
}
```

Extract only the lowest relation that exposes a useful operation. At the same
moment retain a return ledger:

```text
ReturnLedger {
  forgotten physical names and distinctions,
  unit and dimension map,
  regime and boundary obligations,
  orientation/phase convention,
  branch selector and target interpretation,
  reconstruction into original laws
}
```

If the ledger cannot reconstruct the requested meaning, the abstraction is too
coarse. Descend one layer and restore the first lost distinction. The typed
extractor and its cross-domain boundary are owned by
[Result 03](results/semantic-layer-transfer-03.md); it does not parse prose or
invent laws.

## Constructor

```text
construct(packet):
  bind one target and its required physical meaning
  find the shortest justified direct dependency chain
  if direct work already closes within the handwritten budget:
      return direct_gate(chain)
  extract the least shared relation and a return ledger
  if extraction loses a required return distinction:
      return refuse(missing_distinction)
  compute with the admitted operator
  if computation is ambiguous, unsupported, or over budget:
      return typed obstruction/refusal
  lift candidates through the ledger into the original laws
  restrict by regime, geometry, orientation, inequalities, and boundary data
  if exactly one admissible return remains:
      return result + witness + checks
  return inconsistency, underdetermination, or branch obligation
```

For an unidentified finite supplied-law packet, search target-bearing dependency
subsets by increasing size and compare every route at the first complete depth.
Equivalent minimal packets remain visible; competing packets, disconnected data,
unsupported algebra, and exhausted budgets refuse. This operation is owned by
[Result 06](results/adaptive-relation-constructor-06.md). It selects supplied
relations; it does not discover physics.

## Admitted operations

| Trigger/obstruction | Constructed operation | Returned witness | Exact boundary |
| --- | --- | --- | --- |
| explicit hidden definition `h=f(g)` | substitute/pull back `o=Phi(f(g))` | equality in original graph relation | explicit linear/quadratic graph |
| repeated linear law sends target outside its span | residual-generated adjoint closure | invariant retained row space and reduced dynamics | finite linear system and closure budget |
| finite rational polynomial laws | eliminate hidden variables | retained ideal consequence plus physical lift where admitted | algebraic closure is not a general existential/inequality solver |
| observable component vanishes on a traversed event | project zero set, lift all roots, restrict domain | full-state roots and interval/branch certificate | finite zero-dimensional exact polynomial event |
| Coulomb equality would overshoot zero tangent speed | project desired impulse onto the admissible interval | arrest/sliding branches and recovery | fixed planar point particle |
| endpoint scalar fails in nonzero curl | lift to oriented path functional | loop area/flux difference and conservative recovery | supplied evaluable planar paths/field |
| phase loss destroys requested signal | finite exact complex harmonic solve | residuals, real signal, magnitude/relative phase, finite spatial pattern | supplied steady linear one-frequency laws |
| target multiplies two same-frequency signals | DC plus `2 omega` product decomposition | direct-product and reality certificate | two exact phasors at one positive frequency |
| a certified result feeds one named consumer | typed one-successor composition | parent identity, port, provenance, cumulative certificates | no callbacks, branching, loops, or inferred ports |
| base-unit rescaling changes a monomial | exact dimension-kernel quotient `D a=0` | primitive integer exponent vectors | integral exponents over the declared bases; no dynamics |
| hidden linear states obscure a boundary observable | Schur complement plus affine recovery | block substitution and hidden-state reconstruction | supplied finite exact partition with provably invertible hidden block |
| block quotient hides a usable sparse route | reversible greedy scalar elimination | local updates, fill ledger, reverse recovery | reciprocal matrix and provably nonzero scalar pivots |

The detailed source-bound discriminators live in Results
[01](results/oscillator-closure-01.md),
[05](results/a617-polynomial-batch-05.md),
[12](results/event-relation-branch-constructor-12.md),
[13](results/path-functional-reconstruction-13.md),
[15](results/exact-harmonic-response-15.md),
[16](results/harmonic-product-return-16.md),
[17](results/typed-construction-composition-17.md),
[18](results/frictional-impact-projection-18.md), and
[25-28](results/exact-dimensional-quotient-25.md). The canonical
[research graph](research-graph.md) binds every operation to its exact current
owner and boundary.

## Human computation and admission

The paper-facing route is:

```text
TARGET -> PHYSICAL PACKET -> SLICE -> DIRECT GATE
       -> OBSTRUCTION -> OPERATOR -> RETURN -> CHECK
```

Its compact execution rules are:

1. Bind givens and one target; make ambiguity explicit.
2. Separate area law from the mathematical relation it induces.
3. Draw the backward target cone and retain only connected laws.
4. Use direct substitution, cancellation, symmetry, or a familiar invariant when
   that already closes the target.
5. Admit a specialist operator only for a named obstruction and preserve its
   refusal condition.
6. Eliminate one hidden dependency at a time; if a repeated law creates a residual,
   add only the smallest observable needed for closure.
7. Return units, signs, phase/orientation, regime, boundary data, and branches;
   substitute the answer into the original laws.

Direct work is the default, not a failed use of the framework. The complete
handwritten route ledger is

```text
(relations selected,
 hidden quantities introduced,
 maximum simultaneous equations,
 symbolic actions on distinct result subjects,
 branch/regime checks,
 representation changes,
 contextual return checks).
```

Computer-algebra and handwritten ledgers are different substrates and cannot be
silently compared. Unconditional improvement requires component-wise non-worse
cost with at least one strict improvement. A mixed difference returns a positive-
weight break-even region, not an arbitrary score. The corrected six-case evidence
has five direct wins, one trade-off, and no compiler win
([Result 09](results/atomic-handwritten-cost-reconstruction-09.md)); exact admission
regions are in [Result 08](results/route-admission-boundaries-08.md).

Personal weights cannot be inferred from unrelated problem times. They require
correct matched routes on counterbalanced variants, independent variation of cost
axes, identical conditions, and refusal outside the observed span. The calibration
constructor and empty acquisition instrument are Results
[10](results/paired-route-calibration-constructor-10.md) and
[11](results/matched-variant-acquisition-instrument-11.md). Current expert and
learner templates remain empty; timing, error, retention, and transfer are
`unobserved`.

## Refusal and reconstruction boundary

The framework refuses rather than hides:

- missing or competing physical laws, ambiguous targets, disconnected data, and
  unsupported relation shapes;
- nonunique physical branches, inconsistent assumptions, or target
  underdetermination;
- loss of units, regime, orientation, phase, boundary data, or observable meaning;
- unproved inversion, exceeded state/nullity/elimination budgets, or a planner
  outside its exact structural domain;
- transfer from shared algebra to shared physical semantics without separate
  adapters and return witnesses;
- inference from fewer symbolic operations to human time, accuracy, retention, or
  transfer.

The current capability is therefore a bounded target-conditioned constructor,
verification backend, and review method. It is not a universal physics solver, a
new physical theory, an automatic law generator, or a proven exam shortcut. The
[benchmark](benchmark.md) freezes exact tested cases; the
[research graph](research-graph.md) owns the current frontier and seven-dimensional
claim disposition.
