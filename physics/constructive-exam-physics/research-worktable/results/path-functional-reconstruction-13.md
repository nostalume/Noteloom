# Result 13: obstruction-driven path-functional reconstruction

## Claim

The working grammar is not frozen. A14-06 exposes a precise failure of its old
endpoint-observable assumption: in a time-varying magnetic field, the induced
electric field need not be conservative, so `U(P,Q)` is not determined by the two
points alone. The smallest repair is not another formula catalogue. It is a new
computational object,

```text
W[gamma; P -> Q] = integral_gamma E_ind dot dl,
```

together with orientation, endpoint, closed-loop, material-path, and conservative-
recovery rules.

This result constructs that object exactly on A617 A14-06, transfers the unchanged
interface to A10-06, and refuses the path-free question when no scalar-potential
certificate exists. It is a reproducible extension `G_n -> G_(n+1)`, not a claim
that `G_(n+1)` is final.

## Source binding

- A14-06, PDF page 28: points `P=(-a,a)` and `Q=(a,a)` lie inside an infinite
  cylindrical region with uniform changing axial magnetic field. The problem asks
  for the voltage between the endpoints when connected by the indicated circular
  arc, by a straight segment, and by both wires with constant resistance per unit
  length.
- A10-06, PDF page 36: the axial magnetic field is uniform inside a circle and
  varies sinusoidally. The problem compares the voltage between two boundary
  points along a short arc, a long arc, and with no conductor present.

Both pages were rendered and visually checked. The bound compilation is not an
official answer key; signs below follow the declared path orientation and a signed
`B_z` convention.

## Obstruction and reconstruction

The prior endpoint grammar silently expected an observable of the form

```text
U : (P,Q) -> scalar.
```

But if `curl(E_ind) != 0`, two paths with the same endpoints can have different
work. The failed equality itself supplies the new invariant:

```text
W[gamma_1] - W[gamma_2]
  = closed_integral_(gamma_1 - gamma_2) E_ind dot dl.
```

For a planar field of constant scalar curl `omega`, the constructor also generates
and verifies

```text
W[gamma_1] - W[gamma_2]
  = omega * A_signed(gamma_1 - gamma_2),

A_signed[gamma] = (1/2) integral_gamma (x dy - y dx).
```

Thus direct parametrized integration is a fallback evaluator; the reusable semantic
object is the relative path class witnessed by oriented area or flux.

## A14-06 construction

Let

```text
kappa = (1/2) dB_z/dt,
E_ind(x,y) = (kappa y, -kappa x),
curl(E_ind) = -2 kappa.
```

Orient both paths from `P` to `Q`. Exact construction gives

```text
W_arc   = pi kappa a^2,
L_arc   = pi a / sqrt(2),
W_chord = 2 kappa a^2,
L_chord = 2a,

W_arc - W_chord = kappa a^2 (pi - 2).
```

Independently, the signed-area difference is

```text
A_arc - A_chord = -a^2 (pi/2 - 1),
```

so `curl(E_ind) * (A_arc-A_chord)` reconstructs exactly the same work difference.
That equality is checked by the executable certificate.

For one open conducting path at zero current,

```text
V_Q - V_P = W_path.
```

When both branches are present, let `rho>0` be resistance per unit length and use
the common terminal value `U=V_Q-V_P`. Each oriented branch obeys

```text
U = W_j - I_j R_j,      R_j = rho L_j,      I_arc + I_chord = 0.
```

The constructed results are

```text
U = 2 pi kappa a^2 (sqrt(2)+1) / (pi+2sqrt(2)),

I_arc = sqrt(2) kappa a (pi-2)
        / [rho (pi+2sqrt(2))],

I_chord = -I_arc.
```

The executable separately verifies current conservation and recovery of the same
terminal voltage from both branch laws.

## Unchanged transfer to A10-06

Use the same field contract and orient both arcs from
`(r,0)` to `(0,r)`. The interface is unchanged; only path data change:

```text
W_short = -pi kappa r^2/2,
L_short = pi r/2,

W_long = 3 pi kappa r^2/2,
L_long = 3 pi r/2,

W_long - W_short = 2 pi kappa r^2.
```

For the printed field directed into the page,
`B_z=-B_0 sin(omega t)` and hence
`kappa=-B_0 omega cos(omega t)/2`; substituting this signed value fixes the
source-specific signs without changing the constructor.

Along either conductor, the open-wire voltage is the corresponding path work. With
no conductor or measurement path, the request for an endpoint-only potential
difference returns `no_scalar_potential_certificate`. This is a semantic answer,
not a failed integral: a nonconservative field does not define the requested scalar
from endpoints alone.

## Conservative recovery

The extension contains the old endpoint grammar as a certified special case. If a
supplied scalar potential satisfies

```text
E = -grad(V),
```

the constructor checks that every declared path returns

```text
W[gamma;P->Q] = -(V(Q)-V(P)).
```

Only after that check may a path-independent endpoint value be returned. Therefore
the extension changes representation when curl obstructs a scalar potential and
pulls back to the simpler endpoint view when the obstruction vanishes.

## Reproducibility

The implementation is in `computation/occ/path.py`; the source fixtures and transfer
run are in `computation/worktable/path_cases.py`; seven focused tests cover construction,
area/curl recovery, circuit closure, unchanged transfer, orientation reversal,
conservative recovery, endpoint mismatch, and the path-free refusal.

## Boundary and next obstruction

Current support is deliberately bounded:

- exact planar parameterized paths;
- exact line, length, and signed-area integrals evaluated by the maintained SymPy
  substrate;
- a supplied field law with provenance;
- an area certificate only when curl is constant in the two spatial coordinates;
- two-branch wires with positive resistance per unit length.

It does not yet construct the induced field from Maxwell equations, choose a path
from a diagram, handle piecewise field support, general three-dimensional surfaces,
topological holes, moving conductors, or gauge-dependent decompositions. It also
does not establish that writing the path formalism is faster on an exam. The next
extension must be forced by one of those concrete obstructions and must recover
this result as a special case; accumulating more pre-encoded curves would not be
research progress.
