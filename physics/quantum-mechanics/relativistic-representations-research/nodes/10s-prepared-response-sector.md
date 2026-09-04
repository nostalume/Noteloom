# N10s — Preparation-Selected Minimal Response Sector

Status: the spin-two preparation-to-sector bridge is supported; a local Weyl-seed
preparation generates one physical invariant layer with a nonzero null-screen
output, but the same preparation also trivializes the compensated source adapter,
so no complete-route computational dominance is obtained

Consumes: [N10r direct constrained Green generator](10r-direct-constrained-green.md),
[N10e generated source adapter](10e-generated-source-adapter.md), and
[N10j generated curvature](10j-generated-curvature-compatibility.md)

Computation: [prepared response-sector discriminator](../computation/10s-prepared-response-sector/README.md)

Produces: a retained preparation-to-layer selector, a mixed-support regression, a
local single-layer transfer with nonzero physical screen, an exact same-response
certificate, and a negative whole-route cost verdict

## Research contract

- **Upstream anchor:** N10r generates a direct response on every invariant layer
  and reduces it to one scalar Green operation when preparation supplies a single
  layer, but does not construct that layer from preparation.
- **Bridge question:** can a local physical preparation generate a nonzero
  observable source in one layer without receiving its layer label, and does that
  reduce the complete response route relative to compensation?
- **Invariant target:** the same spin-two null-screen/curvature observable and the
  same retarded or advanced scalar Green prescription in both presentations.
- **Special resources:** four-dimensional flat symmetric rank-two symbols, one
  compact scalar profile, invariant harmonic operations, and—only in the transfer
  case—a finite algebraic seed constructed by its required symmetries.
- **Internal benchmark:** use the N10e compact current as regression; construct a
  second local preparation from the failed layer condition; discover support from
  `B=R_1 A/Q`; require a nonzero null screen; then count discovery, adaptation,
  active response, and recovery for both routes.
- **Horizon:** spin two, constant-coefficient symbols, and exact non-null/null
  representatives. Interactions, curved backgrounds, arbitrary source carriers,
  and discretization-dependent conditioning are outside this node.

## 1. Conservation does not select a constrained layer

Let `J_B` be N10e's compact bivector current. Its construction makes it conserved:

```text
A J_B=0.                                                (1.1)
```

The constrained field carrier is harmonic, so the simplest source candidate is
its rank-two harmonic head

```text
H J_B=(I-U T/8)J_B.                                    (1.2)
```

This operation does not preserve (1.1). Compute the divergence on the same current,
using `A U=U A+2P` and the fact that `T J_B` is scalar:

```text
A H J_B
 =A J_B-(1/8)A U T J_B
 =-(1/4)P T J_B.                                      (1.3)
```

Thus a traceful conserved current does not enter `ker A` after harmonic projection.
The missing single-layer property is an obstruction produced by the preparation,
not a reason to prescribe a projector.

At the non-null representative `p=(2,1,0,0)`, the exact-small computation finds

```text
T J_B !=0,
support(H J_B)={l=0,l=2},
gauge layer l=1 absent.                                (1.4)
```

The support is calculated by the N10r spectral projectors of `B=R_1 A/Q`; neither
`0` nor `2` is supplied to the selector. At `p=(1,0,0,1)`, the same preparation has
screen contrast `J_xx-J_yy=2`, so (1.4) is a genuine nonzero-observable regression,
not a zero-source failure. Its direct route needs layer separation, whereas N10e's
compensated route still uses one scalar Green operation.

## 2. The failed conditions construct a new seed carrier

To obtain one layer without an inverse momentum, require the preparation itself to
produce a symmetric source satisfying

```text
A J=0,
T J=0.                                                 (2.1)
```

Start with the lowest nontrivial differential candidate containing two derivatives
of a compact seed:

```text
J_(mu nu)=partial^alpha partial^beta
           (C_(mu alpha nu beta) chi).                 (2.2)
```

The desired identities generate the algebraic type of `C`:

1. antisymmetry in `(mu,alpha)` makes the divergence vanish because
   `partial^mu partial^alpha` is symmetric;
2. exchange of the two index pairs makes `J_(mu nu)` symmetric;
3. vanishing metric trace of `C` makes `J` trace free.

These operations construct the algebraic Weyl carrier from the source obstruction;
the name is applied after its symmetries are forced. Direct evaluation gives

```text
partial^mu J_(mu nu)
 =partial^mu partial^alpha partial^beta
   (C_(mu alpha nu beta) chi)
 =0,                                                   (2.3)

eta^(mu nu)J_(mu nu)
 =partial^alpha partial^beta
   (eta^(mu nu)C_(mu alpha nu beta) chi)
 =0.                                                   (2.4)
```

No section, `Q^(-1)`, response layer, or final field equation occurs in this
preparation constructor.

For the executable transfer, a symmetric trace-free electric seed

```text
E=diag(1,-1,0)                                         (2.5)
```

generates the remaining Weyl components by pair symmetry and trace freedom. The
compiler rejects a traceful `E`; this is a seed-typing refusal rather than a failed
downstream verification.

## 3. The selector discovers the one-layer output

Because (2.3)--(2.4) place `J_C` directly in `H_2` and `ker A`, calculate

```text
B J_C=(R_1 A/Q)J_C=0.                                 (3.1)
```

N10r generated the distinct spectrum

```text
c_(2,l)=[6-l(l+1)]/4,   l=0,1,2.                      (3.2)
```

The unique zero of (3.2) is `l=2`; consequently (3.1), rather than an input label,
identifies

```text
support(J_C)={l=2}.                                    (3.3)
```

The calculation uses one application of `B`. If the divergence residual does not
vanish, the same selector constructs all Lagrange spectral projectors from (3.2),
which is how it obtains the mixed result (1.4).

The transfer is not physically empty. At null momentum `p=(1,0,0,1)`, direct
contraction of the seed (2.5) gives

```text
J_xx=2,
J_yy=-2,
J_xx-J_yy=4.                                          (3.4)
```

It is simultaneously conserved and trace free. Thus the local preparation reaches
one physical response layer and preserves a nonzero screen.

## 4. Both presentations now return the same response

Let `G_Q` carry the same retarded or advanced boundary condition in both routes.
For the direct constrained equation `D=Q-R_1 A`, define

```text
phi_c=G_Q J_C.
```

Since constant-coefficient `A` commutes with `G_Q`, compute

```text
D phi_c
 =Q G_Q J_C-R_1 G_Q A J_C
 =J_C.                                                 (4.1)
```

For the compensated route, N10e's adapter is a polynomial in `U T`. Equation (2.4)
makes both the adapter and its inverse act as the identity on `J_C`; its response is
therefore

```text
phi_u=G_Q J_C=phi_c.                                   (4.2)
```

The potentials already coincide, so applying N10j's curvature operation gives the
same curvature and screen without a further quotient argument. Equations
(4.1)--(4.2) are the same-input observable witness required by the bench.

## 5. Preparation succeeds but computational dominance does not

The complete comparison is:

| preparation | discovered layers | discovery | direct Green depth | compensated depth | screen |
| --- | --- | ---: | ---: | ---: | ---: |
| N10e bivector current | `0,2` | six `B` applications by full projectors | 2 | 1 | 2 |
| Weyl-seed double divergence | `2` | one `B` application | 1 | 1 | 4 |

The second row satisfies N10r's re-entry condition, but it does not make the direct
route computationally dominant. The same trace-free conserved preparation makes
the compensated adapter the identity, its auxiliary source channel zero, and its
active observable-visible sector the same five-dimensional `l=2` space. Counting
the declared carriers as `9` versus `10` would count an unexcited compensated
channel as work. The honest active comparison is therefore

```text
same order-two preparation
  + same one scalar Green operation
  + same active l=2 response
  + identical potential/curvature recovery.            (5.1)
```

The preparation bridge is generative and reusable; the proposed speedup is
rejected. What remains useful is the selector:

```text
PreparedResponse(preparation, boundary, screen capability)
  -> calculated harmonic/divergence residuals
  -> discovered invariant support
  -> minimal response rule
  -> screen/recovery certificate
  -> complete-cost verdict or refusal.                 (5.2)
```

This output is stronger than another carrier verification: it determines when the
N10r conditional route is physically realized and prevents carrier dimension from
being mistaken for active computational work.

## Stop and re-entry

The bounded local spin-two preparation discriminator is closed. More spins or seed
components cannot change its scoped verdict. N10t tests its repeated-curvature
re-entry and finds a common observable compiler rather than a constrained-carrier
advantage. Further re-entry requires a different observable, noncommuting dynamics,
or measured discretization evidence.

## Edges

- `N10e -> N10s`: pass the compact conserved current, one-Green compensated
  baseline, adapter, and nonzero screen regression.
- `N10r -> N10s`: pass the generated layer spectrum, direct inverse, conditional
  single-layer route, and complete-cost obligation.
- `N10j -> N10s`: pass the common curvature/screen observable.
- `N10s -> global generative spine`: return a supported preparation-to-sector
  selector and reject computational dominance for the first successful local
  single-layer transfer.
- `N10s -> N10t`: pass the same-preparation refusal and require the repeated
  observable claim to count cached active work on both routes.
