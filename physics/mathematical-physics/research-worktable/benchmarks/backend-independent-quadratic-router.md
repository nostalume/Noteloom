# Backend-independent quadratic route discovery

## Bridge and horizon

This benchmark tests whether the computation workbench can begin from a physical
problem rather than a group or reduction-backend name.

- **Upstream:** the quadratic Schrödinger factor construction, observable-cyclic
  calculus, and common reduction witness.
- **Question:** can independent probes construct, compare, select, and refuse
  routes for the same observable?
- **Invariant target:** the survival amplitude of one prepared excitation.
- **Horizon:** dimension three, exact rational matrices, identity kinetic term,
  distinct rational frequencies for the cross-probe, and a supplied reusable
  frequency action `L` satisfying `L^2=K`.
- **Stop condition:** route choice changes with preparation visibility, and the
  cyclic route survives a bounded exact factor obstruction.

No eigenbasis, group, symmetry algebra, polynomial family, or backend is supplied.

## Typed problem

The PDE is

```text
H_L = -Delta + x^T Kx,                 K=L^2>0,
```

on `Schwartz(R^3)`. The input supplies `K`, the reusable action `L`, a nonzero
coefficient vector `u`, and the observable

```text
C_u(t)=<Wu,exp(-itH_L)Wu>/<Wu,Wu>,
```

where `Wu=a_u^+ psi_0` is constructed by the common ground-state factorization.
The tool verifies `L^2=K`; it does not trust this relation as metadata.

The one-excitation intertwiner gives the common finite dynamics

```text
H_L W = W T,              T=tr(L)I+2L,
<Wu,Wv>=2 u^T L v.
```

Both probes therefore receive the same operator `T`, metric `L`, preparation `u`,
and observable. This shared reduction is constructed from the PDE before either
route is selected.

## Independent probes

The full-mode probe tries to split `L` into exact rational primitive projectors.
When it succeeds, it returns the finite spectral measure

```text
mu_u = sum_i [u^T L P_i u/(u^T L u)] delta_(tr(L)+2 omega_i).
```

The cyclic probe instead applies `T` repeatedly to `u` in the `L` metric. Exact
termination constructs a Jacobi recurrence of degree

```text
r=dim span{u,Lu,L^2u,...}.
```

It does not consume the full-mode projectors. Each probe returns its first
obstruction independently.

## Exact cross-probe

Use

```text
L = [[41/25,-12/25,0],
     [-12/25,34/25,0],
     [0,0,3]],

K = [[73/25,-36/25,0],
     [-36/25,52/25,0],
     [0,0,9]].
```

Exact multiplication verifies `L^2=K`; the frequencies of `L` are `1,2,3` and
`tr(L)=6`.

For `u=(3,4,0)`, only the frequency-one projector is visible. The two routes
construct the same spectral measure

```text
mu_u=delta_8,
```

the cyclic recurrence terminates at `r=1`, and the decision is
`observable-cyclic`. Two ambient directions are certified invisible to this
preparation and observable.

For `u=(1,0,1)`, every mode is visible. The common measure is

```text
mu_u=(9/116)delta_8+(8/29)delta_10+(75/116)delta_12.
```

The cyclic recurrence terminates at `r=3`; it supplies no dimension gain, so the
decision changes to `full-modes`.

For both inputs the executable coincidence certificate verifies exactly:

1. `L^2=K`;
2. the factor projectors resolve the identity;
3. spectral weights sum to one;
4. factor and cyclic normalized moments coincide through order `2r-1`;
5. visible factor support has size `r`;
6. the cyclic minimal polynomial vanishes on every visible energy.

The last three checks establish equality of the finite observable-visible
representations, not merely agreement at a sampled time.

## Independent-refusal transfer

Use the positive action

```text
L = [[2,1,0],
     [1,3,0],
     [0,0,4]],

K=L^2=[[5,5,0],
       [5,10,0],
       [0,0,16]].
```

The two-dimensional block has eigenvalues `(5+-sqrt(5))/2`. The bounded exact
full-mode probe therefore returns `NonRationalSpectrum`; it does not downgrade to
floating point or label the problem unsolvable. With `u=(1,0,0)`, the cyclic
probe uses only rational action arithmetic, terminates exactly at `r=2`, and is
selected. Failure of one candidate no longer collapses the portfolio.

The indefinite control `K=diag(1,-1,9)` returns `NonPositiveStiffness` before
either lowest-weight route is admitted.

## Whole-route cost verdict

The input deliberately supplies an applicable action `L`. The common cost is:

```text
verify L^2=K,
construct the ground factor and one-excitation carrier,
form/apply T=tr(L)I+2L.
```

After that shared cost, the full route constructs all primitive projectors while
the cyclic route retains only `r` Krylov directions. Hence the cyclic choice is a
supported relative gain when `r<3` and one preparation is requested.

This benchmark does **not** claim the same gain when only an opaque `K` is given.
Constructing its positive square root may require a full spectral calculation and
erase the advantage. That case returns `MissingFrequencyAction` in the current
bounded tool rather than hiding square-root cost.

## Human object

The compact decision card reports:

```text
applicability and first residual for each probe,
selected route and visible dimension,
number of eliminated directions,
retained recurrence or projector object,
recovery rule,
exact coincidence certificate,
validity boundary.
```

Matrices and full route certificates remain available in detailed output but do
not occupy the human summary.

## Result and boundary

Supported:

- backend-free problem input for one bounded PDE family;
- two independently executed candidate probes;
- preparation-dependent route selection;
- exact same-observable coincidence when both routes apply;
- continued exact computation when the factor probe is obstructed;
- structural refusal for nonconfining input;
- an explicit compact human decision card.

Not supported:

- constructing `L` cheaply from a general opaque `K`;
- irrational full-mode certificates in the exact rational backend;
- repeated frequencies, arbitrary dimension, or nonidentity kinetic matrices;
- higher-excitation, multi-preparation, or nonlinear observables;
- routing among factor, centralizer, orbit, complex, and bundle probes for one
  unrestricted problem grammar.

This closes the first backend-independent routing bridge. It is a transfer result
for the decision architecture, not evidence of a universal PDE solver.
