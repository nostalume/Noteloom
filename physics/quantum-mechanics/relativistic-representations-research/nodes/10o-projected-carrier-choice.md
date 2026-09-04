# N10o — Projected-Carrier Motivation and Residual Repair

Status: the role of the trace-free carrier is corrected and the first
capability-relative repair portfolio is supported; exact residual cancellation and
nonzero Euclidean `O(3)` contraction-surjectivity checks pass through rank three,
while [N10p](10p-null-orbit-carrier-comparison.md) closes the finite null-orbit
physical-equivalence test and [N10q](10q-source-response-discriminator.md) rejects
gauge-slice transport as a local causal constructor; N10r rejects generic direct
Green gain on its declared load, while interactions and conditioning remain open

Consumes: [N10n projected-carrier completeness](10n-projected-carrier-completeness.md),
[N10m natural-operation compiler](10m-natural-operation-compiler.md), and
[N10a compensator resolution](10a-unconstrained-compensator-resolution.md)

Sources: [projected-carrier contracts](../sources/projected-carrier-contracts.md)

Computation: [projected-carrier choice](../computation/10o-projected-carrier-choice/README.md)

Produces: a corrected motivation ledger, residual-typed constraint and compensator
branches, an exact nonzero-momentum gauge-slice certificate, capability-relative
selection, and a refusal to infer mixed symmetry from dimension alone

## Research contract

- **Correction:** N10n proved that a projected one-row carrier has a generated
  operator calculus. It did not prove that physics requires that carrier.
- **Question:** when is `H_r=ker T` a legitimate input capability, and what does
  its generated residual actually demand?
- **Invariant target:** do not choose a field equation in advance. Preserve either
  the smallest local carrier or the full harmonic gauge-parameter interface,
  according to the requested capability.
- **Independent input:** N10n's relation
  `AR_r=Q+rho_rR_(r-1)A`, field rank, and capability. No constraint,
  compensator, mixed carrier, or repair coefficient is supplied.
- **Benchmark:** type the residual before proposing a repair; generate all minimal
  branches licensed by that type; verify the nonzero-momentum parameter map; select
  by capability rather than a scalar simplicity score.
- **Horizon:** nonzero Euclidean `O(3)` symbol bench. The massless Lorentz orbit,
  little-group quotient, action, sources, and interactions remain separate.

## 1. Why might one use a trace-free carrier?

There are three distinct questions that must not be collapsed.

### 1.1 Representation decomposition

The invariant metric splits a symmetric tensor into harmonic and trace descendants:

```text
Sym^r(V*) = H_r direct-sum U H_(r-2) direct-sum ... .  (1.1)
```

Selecting `H_r` removes the lower-rank trace summands and gives the irreducible
one-row orthogonal carrier in the ordinary semisimple regime. This is useful when
the requested output is specifically an irreducible finite-dimensional carrier or
when trace descendants would duplicate channels already represented elsewhere.

### 1.2 Field presentation

A field is an interpolating/gauge carrier, not the particle Hilbert space itself.
It may be reducible off shell. Gauge symmetry, equations, and quotient recovery can
remove its surplus components. Therefore

```text
irreducible particle fiber
  does not imply
irreducible trace-free gauge potential.               (1.2)
```

Constrained and compensator formulations of symmetric higher-spin fields are a
known warning: algebraic trace restrictions can be traded for additional fields.
The choice belongs to the presentation capability and cost ledger, not to particle
classification alone.

### 1.3 Compiler benchmark

N10n used `H_r` for a narrower reason: it is the smallest carrier on which N10m's
raw multiplication operation fails closure. It tests whether the compiler can
generate a projector-preserving operation and rank-indexed relations. That makes
`H_r` a useful diagnostic even if it is not ultimately the preferred physical
presentation.

Hence N10n should be read conditionally:

```text
if the user requests the one-row harmonic carrier,
then its natural operations are generated as recorded.
```

It must not be read as “the particle representation requires trace-free fields.”

## 2. The residual, not the complement, names the repair carrier

For a field `phi in H_s` and parameter `epsilon in H_(s-1)`, N10n constructs

```text
R=R_(s-1),
D=Q-R_(s-1)A.
```

Its rank-indexed relation computes

```text
D R_(s-1)epsilon
 =-rho_(s-1)R_(s-1)R_(s-2)A epsilon.                (2.1)
```

The primitive unresolved datum in (2.1) is

```text
A epsilon in H_(s-2).                                (2.2)
```

This corrects the prior inference. The mixed summand in
`V tensor H_(s-1)` exists, but it does not appear in (2.1). Dimension complement
alone cannot authorize it as a repair. A mixed carrier should enter only when a
residual lands in that channel or when an independently named capability requests
it.

## 3. Branch one: restrict the interface

The cheapest local response to (2.2) is

```text
A epsilon=0.                                          (3.1)
```

Then `DR=0` with no additional field. This preserves the one-row field carrier but
reduces the gauge-parameter interface to

```text
ker(A:H_(s-1)->H_(s-2)).                              (3.2)
```

The independent polynomial evaluator chooses a nonzero Euclidean momentum
representative and computes the exact rational rank of `A`. For `O(3)`, ranks one
through three, `A:H_r->H_(r-1)` is surjective. Since `dim H_r=2r+1`, its kernel has
dimension two. At spin three this means

```text
dim H_2=5,
dim H_1=3,
constraint (3.1) removes 3 parameter directions.      (3.3)
```

The branch is minimal in added carrier load, not universally minimal in semantic
cost: it purchases simplicity by refusing three admissible harmonic inputs.

## 4. Branch two: let the defect construct a compensator

If the requested capability retains every `epsilon in H_(s-1)`, represent the
primitive defect once:

```text
chi in H_(s-2),
delta chi=A epsilon.                                  (4.1)
```

The coefficient and insertion map are already present in (2.1), so the repaired
equation is forced:

```text
E(phi,chi)
 =(Q-R_(s-1)A)phi
   +rho_(s-1)R_(s-1)R_(s-2)chi.                      (4.2)
```

Vary both terms on the same parameter:

```text
delta[(Q-R_(s-1)A)phi]
 =-rho_(s-1)R_(s-1)R_(s-2)A epsilon,

delta[rho_(s-1)R_(s-1)R_(s-2)chi]
 =+rho_(s-1)R_(s-1)R_(s-2)A epsilon.                 (4.3)
```

Their sum vanishes. At `d=3`, `s=3`, this gives

```text
chi in H_1,
delta chi=A epsilon,
E=(Q-R_2A)phi+(3/5)R_2R_1chi.                        (4.4)
```

Surjectivity of `A:H_2->H_1` at the tested nonzero momentum constructs a gauge
slice `chi=0`; its remaining parameters are exactly `ker A`, returning branch one.
The compensator therefore trades the three removed parameter directions in (3.3)
for three added field components. This is a capability exchange, not a free
simplification.

The nonzero Euclidean gauge-slice result is not yet a massless Lorentz theorem.
Null momentum can change the rank and quotient structure.

## 5. Branch three: reconsider the projected presentation

If neither an irreducible one-row field carrier nor removal of trace descendants is
part of the requested capability, the honest response is not to repair `H_s` at
all. Return to the full symmetric carrier and rerun N10m/N10c:

```text
H_s presentation obstruction
  -> question the presentation
  -> Sym^s carrier
  -> regenerate its constraints, equations, and costs. (5.1)
```

This is not automatically cheaper: the traceful carrier contains more components
and its residual constructor may generate trace constraints or other auxiliaries.
But those costs must be compared after the capability is stated. They cannot be
avoided by declaring trace freedom physically mandatory.

## 6. Capability-relative selection

The retained selector has no scalar score:

| Requested capability | Selected branch | Cost paid |
| --- | --- | --- |
| smallest local carrier inside the harmonic presentation | constrain `Aepsilon=0` | remove `dim H_(s-2)` parameter directions at the tested nonzero momentum |
| every harmonic gauge parameter | add `chi in H_(s-2)` | add `dim H_(s-2)` field components and a gauge-slice recovery |
| every harmonic parameter and no extra carrier | refuse | nonzero residual (2.1) |
| no independent need for the harmonic field carrier | reconsider `Sym^s` | rerun the free-power construction and compare its whole route |

The mixed channel is recorded but not selected. Its re-entry condition is explicit:
a residual must land there, or a requested observable/locality/interface capability
must require it.

## 7. Global verdict and next bench

N10o changes the spine in a small but important way:

```text
particle/capability target
  -> candidate carrier is provisional
  -> compile its operations
  -> type the residual
  -> either constrain, enlarge, or reject the carrier
  -> compare recovery and carrier costs
  -> only then retain a presentation.
```

[N10p](10p-null-orbit-carrier-comparison.md) now moves the portfolio to the
massless Lorentz orbit. At one common null momentum it compares:

1. the constrained harmonic branch;
2. the harmonic compensator branch;
3. the regenerated full symmetric branch.

All three recover the same two-dimensional transverse quotient for spins two
through five. More strongly, the compensated harmonic branch is a zero-order
Fischer reparameterization of the compressed symmetric baseline. The constrained
branch removes exactly as many null gauge directions as field components. Thus the
trace-free carrier is demoted to a compiler regression or explicitly requested
partial-gauge interface; it is not promoted into the paper's main generative spine.

[N10q](10q-source-response-discriminator.md) then constructs the source-side gauge
slice. The constrained and compensated source quotients coincide, but their lift
requires a section `AS=1` of inverse momentum degree. Consequently equivalence by
gauge-slice transport cannot establish a cheaper local causal-source presentation;
a direct constrained construction remains a separate obligation.

## Edges

- `N10n -> N10o`: pass the projected operation law and residual, while retracting
  the inference that its mixed complement is the repair.
- `N10a -> N10o`: pass the general lesson that algebraic restrictions and
  compensators are capability trades; do not import N10a's finished equations.
- `N10o -> N10m/N10c`: reopen the full symmetric presentation when trace freedom
  lacks independent authority.
- `N10o -> N10p`: compare actual null-screen recovery before retaining any
  projected presentation.
- `N10p -> N10q`: price the remaining partial-gauge candidate against one named
  local source-response capability.
