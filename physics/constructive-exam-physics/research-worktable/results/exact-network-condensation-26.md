# Result 26: exact boundary-network condensation

## Tension

The framework could already select relations and eliminate polynomial variables,
but it had no reusable operation for a common exam structure: many coupled
internal states are present while the target concerns only terminals or boundary
observables. Calling electrical series reduction, spring reduction, and thermal
resistance analogous would be a taxonomy. A construction must derive the reduced
law and retain an exact route back to every eliminated state.

## Construction `C-network-v1`

For a supplied finite linear balance law `K x=f`, partition the state into boundary
variables `u` and internal variables `h`:

```text
K_BB u + K_BI h = f_B,
K_IB u + K_II h = f_I.
```

When `K_II` is provably invertible, the hidden equation constructs

```text
h = A u + b,
A = -K_II^-1 K_IB,
b = K_II^-1 f_I.
```

Substitution returns the boundary law

```text
K_eff u = f_eff,
K_eff = K_BB - K_BI K_II^-1 K_IB,
f_eff = f_B - K_BI K_II^-1 f_I.
```

This is a Schur complement used as an observable projection, not as a formula to
memorize without its recovery map. Certificates substitute `(A,b)` into the hidden
block, substitute it into the boundary block, and verify that the semantic
boundary/internal partition remains disjoint under one area-specific state kind.

## Frozen distinguishing bench

| Packet | Boundary result | Hidden-state return |
| --- | --- | --- |
| two conductances in series | `g_eff=g_1 g_2/(g_1+g_2)` | junction voltage is the conductance-weighted boundary value |
| three-edge conductance chain | exact three-coefficient series response | two interleaved hidden variables are recovered together |
| two springs through a massless junction | `k_eff=k_1 k_2/(k_1+k_2)` | junction displacement uses the same exact affine map |
| two thermal conductances with hidden heat source `Q` | the same response matrix plus split effective boundary source | junction temperature includes `Q/(h_1+h_2)` |
| free hidden mode | `internal_block_singular` | no unique reconstruction is claimed |
| assumption-free symbolic hidden coefficient | `internal_invertibility_undetermined` | nonzero status is not guessed |

The thermal source makes the transfer discriminating: the output is not merely a
renamed equivalent coefficient but an affine source return. All successful cases
use the unchanged constructor and all certificates pass.

## Semantic boundary

`NetworkVariable.state_kind` retains voltage, displacement, or temperature without
forcing temperature into the older four-base `Dimension` record. The area adapter
must still justify the supplied balance law and coefficient/source dimensions.
The generic layer knows only the exact linear relation and the declared observable
partition; after computation, the area tag, physical names, state kind, and
provenance remain attached.

## Disposition

`C-network-v1` is **supported-bounded as an exact finite linear reduction
constructor**. It removes hidden variables, returns an effective boundary law,
reconstructs hidden states, and refuses singular, assumption-undetermined, or
over-budget elimination.

It does not parse a diagram, discover Kirchhoff/force/heat-balance laws, infer a
massless or steady-state approximation, solve nonlinear elements, handle dynamics
or frequency dependence unless already represented by an admitted exact matrix,
or prove handwritten savings. The candidate learner card is therefore outside
`C-review-v1` and `C-human-v2`.

The elimination-order question is continued in
[Result 27](sparse-network-elimination-order-27.md), which constructs a reversible
greedy sparse route and compares its structural work with declared order. The next
independent operator family should quotient a supplied conservation or symmetry
action, not accumulate more three-node examples.
