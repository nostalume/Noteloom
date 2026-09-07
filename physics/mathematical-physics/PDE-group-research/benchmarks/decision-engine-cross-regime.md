# Cross-regime audit of the decomposition decision engine

## Purpose and horizon

This audit asks one bounded global question: can the
[decision engine](../nodes/decomposition-decision-engine.md) classify the existing
worktable cases through the same reduction-witness contract without using a group
name as its first decision?

It is a synthesis check, not a new solution of the individual models. The
invariant target is each bench's already declared state or observable. The audit
stops once it detects whether the common interface preserves statuses and failure
boundaries.

## Classification

| Input presented to the engine | Intrinsic trigger | Constructed witness | Residual/status | Engine output |
| --- | --- | --- | --- | --- |
| positive quadratic Schrödinger PDE | positive quadratic symbol and residual-cancellable first-order factors | normal-mode/Fock analysis and occupation channels | exact ladder and reconstruction identities on the common core | `ExactReduction` regression |
| constant-curvature Pauli PDE | Clifford symbol plus constant curvature commutator | spin/Fock/longitudinal channel analysis | exact differential reconstruction with stated direct-integral data | `ExactReduction` regression within its global assumptions |
| compact homogeneous de Rham family | symbol complex `d^2=0` and compact Hodge realization | multiplicity complexes and exact/coexact/harmonic projectors | zero complex and Casimir residuals under theorem contracts | `ExactReduction` bundle transfer |
| variable spin-texture PDE | separated two-level internal symbol | eigenline bundle and projected connection PDE | exact nonzero `[H,P]`; conditional momentum-sector error contract | `FormalControlledCandidate` until sector propagation is closed |
| `SU(3)` tensor operator | supplied compact action, adjoint operator type, dynamics, preparation, and probe | bracket/Jordan multiplicity space and an `H^2 -> L^2` adjoint-valued PDE core | exact finite transition and differential-core recovery; full regular representation open | `ExactReduction` on one smooth coefficient copy; global spectrum still formal |
| isolated associated-Legendre equation | scalar ODE alone | no unique carrier family, tensor arrows, measure, or global boundary data | inverse information is insufficient | `Underdetermined`, not “SO(3) recovered” |
| quartic-oscillator refusal probe | declared finite Lie/factor ansatz | residual ideal specified but not executed in this worktable | no computed elimination certificate | `PendingBoundedSearch`, not `NoCandidateWithinBudget` |

The classifier preserves distinctions that a group-first workflow would blur:

- exact algebra versus analytic realization;
- a controlled candidate versus a proved approximation;
- insufficient inverse data versus nonexistence;
- a specified refusal computation versus a completed obstruction certificate.

## Semantic checks

### Exact constant limit

In the spin-texture bench, set the field direction `n(x)` constant. Then

```text
dP_s=0,
[H_epsilon,P_s]=0,       R_A=R_S=0,
Phi_s=0.
```

The engine changes the tag from a controlled-mode candidate to an exact fixed-spin
reduction without changing its interface. This checks that the approximate branch
recovers an exact regime rather than forming a separate formalism.

### Coupled-cluster limit

If `|B|` vanishes, the two spin eigenvalues meet and the reduced-resolvent step is
undefined. The sum projector is `P_++P_-=I`, so the smallest separated cluster is
the full two-component carrier. The engine returns a coupled spinor PDE rather
than two scalar band equations. This is loss of reduction, not loss of the
original dynamics.

### Information-loss limit

Removing the `m`-family, measure, endpoint conditions, and azimuthal gluing from
the Legendre realization leaves the same differential expression compatible with
inequivalent global carriers. Since these candidates can agree on the local ODE
while differing in analysis/synthesis, the recovery and observable residuals
cannot be certified. `Underdetermined` is therefore forced by the witness contract.

## Global verdict

The same residual interface classifies all seven cases without identifying their
groups first. This supports the decision engine as a semantic synthesis of the
worktable.

It does **not** show that the six candidate probes automatically discover the
right witness from arbitrary coefficients. Nor does it establish computational
leverage: the audit preserves established outputs and prevents false upgrades, but
it does not compare a complete observable computation against a baseline.

The requested selection experiment is now the
[observable-cyclic quadratic bench](observable-cyclic-quadratic.md). It gives the
full-mode and cyclic probes the same survival amplitude and selects conditionally
by the discovered relative degree `r`. The next unresolved transfer removes the
quadratic-closure resource and requires a controlled, rather than exact, cyclic
observable error.
