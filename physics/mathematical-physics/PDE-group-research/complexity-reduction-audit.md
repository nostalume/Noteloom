# Whole-route complexity audit

This document is the compact decision ledger for computational and human
leverage. Derivations belong to [research nodes](nodes/README.md), concrete inputs
and measurements to [benchmarks](benchmarks/README.md), and executable replay to
the [computation workbench](computation/README.md).

## 1. Comparison contract

No complexity claim is admitted until both routes share

```text
(model/dynamics, preparation, observable, accuracy,
 domain/boundary, arithmetic/error policy, resource scale)
```

For route `r` and `N` repeated queries, record

```text
C_r(N) = C_discovery + C_construction + N C_solve + C_recovery
```

together with symbolic growth, memory, conditioning, theorem debt, and refusal
conditions. One-time construction and per-query work must remain separate. A
smaller carrier, shorter formula, or exact closure is not itself a complete-route
gain.

Route comparison returns dominance only when all required dimensions are no worse
and one is better. Otherwise it returns a Pareto set, conditional preference, or
no-gain result.

## 2. Cost vocabulary

| Class | Meaning | Required witness |
| --- | --- | --- |
| eliminated | work cannot affect the named observable and is not performed | exact projector/quotient/selection certificate |
| compressed | the same information is generated with a smaller representation | analysis/synthesis and recovery equality |
| relocated | work disappears locally but reappears in seed discovery, basis change, boundary descent, or recovery | full pipeline ledger |
| amortized | larger construction cost is repaid by repeated cheaper queries | observed or symbolic break-even under fixed contract |
| unpaid | domain, convergence, global integration, propagation, or observable recovery is assumed | named theorem/solver debt |

Semantic compression and runtime acceleration are independent claim dimensions.
The exact route may be more intelligible while slower, and an invertible numerical
route may be faster without changing the semantic carrier.

## 3. Human computability

Human cost is evaluated by the operations a reader must reproduce:

- number of independently chosen objects and case splits;
- derivation depth and maximum live dependency width;
- raw component/orbit enumeration avoided;
- need for preferred coordinates, eigenvectors, or group labels;
- size of the retained certificate and recovery map;
- reusable intermediate structure across parameters or observables.

Authored scores are diagnostic only. A claim about actual human performance
requires a blinded matched reconstruction task; that experiment is not yet done.

## 4. Bilateral and PDE-level result ledger

| Evidence family | Complete-route result | Boundary |
| --- | --- | --- |
| Euclidean quadratic centralizers | exact candidate/closure construction replaces an unbounded symmetry guess by a finite kernel problem | completeness is relative to order-two polynomial coefficients |
| Coulomb and `E^3` modules | full modules expose degeneracy and cross-sector action unavailable to radial ODE separation alone | analytic domain and representation integration remain separate |
| factor vs centralizer oscillator | equal spectrum/heat observable; factor route avoids the full compatibility system | preference is model- and observable-specific |
| observable-cyclic quadratic/quartic | invisible sectors can be eliminated; recurrence also returns no-gain or controlled truncation | closure need not be Lie or spectrally complete |
| singular interbasis probe | parent-Lie and polynomial routes recover the same finite observable but neither dominates every capability | basis recovery can erase a local advantage |
| boundary-fixed accuracy | domain construction and accuracy can reverse the preferred symmetry route | compare continuum accuracy, not mode count alone |
| axial and warped quotient PDE | cohomogeneity lowers a 3D PDE to a 2D PDE while preserving descended strata | singular isotropy adds domain work rather than disappearing |
| Pauli/spinor | Clifford projectors and topology replace scalar ladders; flux supplies multiplicity for the heat observable | global gain requires integral flux, domain, and measure contracts |
| adjoint multiplicity | two natural SU(3) channels and one SU(2) control avoid component Clebsch--Gordan enumeration | outer multiplicity remains explicit; it is not a scalar spectrum |
| matrix PDE inverse/covariance | coefficient closure and invariant pairing construct the effective algebra and differential action | global group remains non-unique and observable-relative |
| adjoint semigroup | one visible compact heat block is analytically promoted | this is not the full regular-representation spectrum |

These rows establish useful PDE decomposition beyond Cartesian separation: quotient
and bundle routes may reduce the number of independent variables, fiber
multiplicity, or observable-visible carrier even when no product ODE separation
exists.

## 5. Construction-cost ledger

| Stage | Cost result | Disposition |
| --- | --- | --- |
| G0 seed--defect | exact kernel, quotient, and closure make candidate loss/refusal visible | construction supported; arbitrary seed discovery open |
| G1 structured seeds | proxy `1638 -> 117`; break-even estimate `103 -> 8` queries | compression before elimination is decisive on elasticity transfer |
| G2 typed planner | exposes 648 orbit-canonicalization checks; selected plan+compiler proxy 765, break-even 48 | generic planning is correct but relocates enumeration |
| G3 lazy quotient | 21 direct nested-symmetric-power emits; selected proxy 138, conditional break-even 9 | operational scan removed; raw route retained only as audit |
| G4 coupled covariance | joint base/fiber defects yield closed rank-two/rank-three effective actions and linked projectors | candidate construction compressed without supplied group |
| G5 full-operator lift | ordered curvature/lower-term tests reduce the admitted action `3 -> 1` | lift cost is paid once and preserves partial evidence on refusal |
| G6 first-order transport | curvature-derived axis gives exact shifted scalar channels; transverse transport fails early | reuse adds linear recovery rather than a new search |
| G7 two-sector algebra | traces and one minimal polynomial replace preferred-basis diagonalization | gain requires commuting coefficient data |
| G8 finite split algebra | Krylov minimal polynomials generate joint idempotents and retain multiplicity | rational splitting and finite semisimplicity are explicit costs |
| G9 represented star algebra | commutant/bicommutant kernels separate center, irreducible size, and multiplicity | exact dense matrix scaling limits transfer |
| G10 simple block | four-dimensional symbol reduces to a two-dimensional primitive carrier; proxy breaks even after 62 queries | correct reduction is amortized, not one-shot dominant |
| G11 projector jet | connection plus first/second leakage make derivative work explicit | frame construction is not free |
| G12 one-channel bound | gap/time data convert a leakage norm to exact transition and controlled bounds | closing gap refuses analytic promotion |
| G13 full-block window | one coherent off-block map replaces columnwise propagation | dense finite propagation remains |
| G14 coefficient jet | exact Sylvester/projector differentiation removes eigenvector matching | isolated finite Hermitian cluster required |
| G15 common arrows | frame and coefficient routes share `QP'P,QP''P` and one propagation core | several-coordinate compatibility remains open |
| G16 complete route | exact construction has lower semantic depth but loses every sampled runtime comparison | runtime-dominance claim rejected; original-PDE propagation unpaid |
| G17 active carrier | every tested block reduces to dimension 3; one-shot loses, 64-time reuse wins in all four cases | leverage is reuse-dependent and family-bounded |

The numerical proxies compare declared primitive operations, not portable wall
clock. Timing observations remain attached to their executable benchmark and
environment; exact output equality is the primary gate.

## 6. Current complexity diagnosis

The program has reduced three different growth axes:

1. **candidate growth** through structured seeds and lazy quotient emission;
2. **representation growth** through centers, primitive commutant slices, and
   preparation-reachable carriers;
3. **differential recovery growth** through common projector arrows and coherent
   finite-window propagation.

It has not removed:

- the cost of finding a sufficient coefficient family in an unrestricted PDE;
- global domain, integration, convergence, or completeness theorems;
- dense propagation when the active module regrows to the ambient carrier;
- nonlinear closure and uncontrolled mode fusion;
- observable recovery when the requested output is itself component-resolved.

Therefore the strongest current leverage claim is conditional:

> A structurally admitted reduction is useful when its construction plus
> same-observable recovery is cheaper at the declared reuse scale; otherwise the
> result remains a semantic construction or a no-gain certificate.

## 7. Active cost probe

G18 tests whether pointwise G17 discovery is avoidable. Given
`H(k)=sum_a f_a(k)H_a`, construct the preparation-reachable module under the
coefficient algebra generated by the `H_a`. Compare:

```text
family route:
  one coefficient closure + specialization + repeated reduced propagation

pointwise route:
  sum_k(pointwise Krylov closure + reduced propagation)
```

Admission requires exact specialization invariance and identical pulled-back
effect. Success requires lower whole-window cost at a declared number of momentum
and time queries. Ambient regrowth, changed observable, or no break-even is a
valid negative result.

## 8. Audit rule

Every new cost claim must name the baseline, observable, accuracy, one-time and
per-query terms, recovery, theorem debt, environment for timings, and refusal
boundary. Promote only compact results here; keep calculations and raw measurements
with their owning node, benchmark, or executable artifact.
