# Complete local coefficient-route leverage

## Frozen contract `C_G16_v1`

G16 does not ask whether exact algebra is intrinsically “better.” It fixes one
model-conditioned problem:

```text
(G10 model, C,C_1,C_2, selected cluster, finite window, preparation,
 complement probability, accuracy)                                      (1)
```

and compares two routes to that same probability. G9/G10 model realization is a
shared stage and is named but not timed. Original unbounded-PDE propagation and
continuous-window/domain certification are unpaid on both sides. The sampled
route's truncation error is admitted by paired comparison with the exact route,
not a standalone error theorem. Consequently this node cannot establish an
original-PDE speedup or certified independent baseline.

## The compared routes

The exact route is the unchanged G14--G15 composition:

```text
(C,C_1,C_2) -> exact spectral projectors and Sylvester jets
             -> (P,Q P_1 P,Q P_2 P)
             -> finite carrier Hamiltonians -> complement probability.       (2)
```

The direct dense baseline constructs a quadratic local coefficient sample

```text
C_h(t)=C+t C_1+t^2 C_2/2                                       (3)
```

at `t=-h,0,h`, performs three Hermitian eigensolves, selects the central cluster
by a declared tolerance and the side clusters by nearest equal rank, and uses

```text
P_1^h=(P(h)-P(-h))/(2h),
P_2^h=(P(h)-2P(0)+P(-h))/h^2.                                  (4)
```

It then forms the same off-block arrows, Hamiltonians, preparations, matrix
exponentials, and norm-weighted complement probability. Ambiguous clusters,
oversized carriers, invalid policies, excessive projector/unitarity residuals,
zero preparation, and unmet observable accuracy refuse distinctly.

## Non-scalar cost witness

No weight converts rational factor work, exact Sylvester products, numerical
eigensolves, and matrix exponentials into one invariant unit. The tool therefore
retains them as separate coordinates:

| Stage | Exact G14--G15 | Sampled dense baseline |
| --- | ---: | ---: |
| coefficient samples | 0 | 3 |
| numerical eigendecompositions | 0 | 3 |
| complement Sylvester blocks | 2 | 0 |
| frame-coordinate solves | 0 | 0 |
| coupling entries, window `n`, carrier `q` | `n q^2` | `n q^2` |
| dense matrix exponentials | `n` | `n` |

The two ledgers are heterogeneous and neither receives a fabricated scalar
break-even. Both retain the full `q`-dimensional propagation bottleneck.

## Evidence packet `E_G16_1`

The transfer family uses non-rigid repeated-Pauli coefficient jets with
multiplicity `m=2,3`, carrier `q=2m`, window sizes `n=1,4`, step `h=10^-3`, and
five alternating-order timing repetitions. The exact and sampled observables
agree as follows:

| `m` | `q` | `n` | observable error | exact median (s) | sampled median (s) | ratio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 4 | 1 | `1.55e-8` | `0.02880` | `0.000489` | `58.9` |
| 2 | 4 | 4 | `3.87e-8` | `0.03878` | `0.001011` | `38.3` |
| 3 | 6 | 1 | `9.81e-10` | `0.50202` | `0.001676` | `299.6` |
| 3 | 6 | 4 | `2.99e-9` | `0.40255` | `0.003003` | `134.1` |

The environment was CPython 3.14.6, NumPy 2.5.2, SciPy 1.18.1 on
Windows 11 (`10.0.26200`), timed with `perf_counter`. Runtime ordering is an
environment-bound observation, not a theorem; the non-monotone exact medians also
show why asymptotic conclusions cannot be extracted from four small cases.

The reusable constructors are `compare_complete_routes` and
`construct_sampled_route`; their public laws and repeated-multiplicity adapters
are retained in `test_complete_route_leverage.py`.

Step refinement from `h=0.05` to `h=0.01` lowers the sampled observable error.
Multiplicity three and a larger window pass through the unchanged comparator.
An excessive cluster tolerance and a coarse step under a `10^-14` observable
tolerance refuse, so numerical convenience cannot silently become admissibility.

## Human computability and disposition

The declared replay protocol counts semantic object types and nonlocal
transformations, not source lines. The exact route retains four independent
objects, six transformations, no route-specific numerical choice, and two theorem
contracts. The sampled route retains six objects, eight transformations, two
numerical choices, and one convergence theorem contract. This supports lower
declared semantic depth for the exact route, with greater theorem debt; it is not
an empirical statement about human completion time.

The domain-wise disposition is:

- **Supported:** same-observable comparison, exact structural certificates,
  multiplicity/window transfer, and lower declared exact-route semantic depth.
- **Refuted on this bench:** runtime dominance of the exact route; the sampled
  baseline is faster in all four observations.
- **Underdetermined:** scalar proxy dominance and asymptotic break-even.
- **Unpaid:** original-PDE propagation, continuous domains/windows, sparse large
  carriers, standalone certified finite-difference error, and measured human
  performance.

The runtime failure does not reject G14/G15 correctness. It locates the remaining
cost: full ambient propagation. The next useful probe must reduce the prepared
observable's active invariant subspace before exponentiation.
