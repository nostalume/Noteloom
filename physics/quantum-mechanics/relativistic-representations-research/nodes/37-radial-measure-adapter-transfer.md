# Radial measure-adapter transfer

Status: `V_radial-transfer-1` supports bounded transfer across Gaussian and
algebraic-tail adapters; general radial and cost leverage claims remain open

Consumes: node 36's moment-preserving atomic return and its unresolved
cross-form-factor region.

Produces: either a reusable radial channel interface or a proof that the Gaussian
closed form is part of the construction rather than an adapter resource.

## Tension: the density and its integral are fused

Nodes 35--36 generate finite creation coefficients from shell masses,

```text
c_j=sqrt(m_j),  m_j=integral_(I_j) 4pi r^2 |a(r)|^2 dr.   (37.1)
```

Their implementation nevertheless obtains every `m_j` by subtracting the analytic
Gaussian tail. Two alternatives remain live:

1. moment compression is a Gaussian rule whose exact tail is indispensable; or
2. it consumes a positive radial measure, while Gaussian integration is only one
   certified realization of that measure.

A second Gaussian parameter cannot distinguish them. An algebraically decaying
amplitude can: it changes the tail class and forces numerical cell masses while
leaving the shell, moment, Fock-action, and observable semantics unchanged.

## Construct the interface from the invariant measure

For an isotropic three-dimensional channel, admit

```text
RadialData=(a, E, E_min, gap, support, provenance, mass_operation),
dM(r)=4pi r^2 |a(r)|^2 dr.                              (37.2)
```

Squaring the supplied channel amplitude constructs positivity; the caller does not
assert an unrelated positive density. The mass operation may be an analytic
adapter or the shared numerical integrator, but it receives only an interval and
returns `(mass,error,evaluations)`. It never sees `z`, `t`, or a requested
transform, so it cannot encode the observable answer.

Let `m_hat_j` and `delta_j` be its cell result and error, `u_hat_j` and `alpha_j`
the first-energy moment, and

```text
e_hat_j=u_hat_j/m_hat_j,
beta_j=alpha_j+|e_hat_j| delta_j,
q_j >= integral_(I_j)(E-e_hat_j)^2 dM.                  (37.3)
```

Then direct subtraction at the common target gives

```text
|integral_(I_j) F(E)dM-m_hat_j F(e_hat_j)|
 <=||F|| delta_j+||F'|| beta_j+(1/2)||F''||q_j.         (37.4)
```

Equation (37.4), rather than a model name, is the compiler contract. Summing it
and adding the certified tail produces the same resolvent and finite-time bounds
as node 36, now including mass-integration error. An exact adapter has
`delta_j=0`; a numerical adapter pays and reports the additional term.

## Frozen candidate `C_radial-v2`

```text
CompileRadialDeparture(RadialData, cutoff R, cells N, budget, tolerance)
 -> cell masses/errors + unchanged coefficients sqrt(m_hat_j)
    + moment-centered energies + second-order common certificate
    + finite departure + measure identity + complete evaluation receipt
 | refusal(invalid support/threshold/tolerance, nonmonotone energy contract,
           nonfinite or unresolved mass/moment/tail, zero departure, or budget).
```

Changing amplitude, tail class, or an interval-integration strategy is adapter
data. Changing (37.1), moment centering, transform laws, or refusal semantics
creates another candidate version.

## Frozen bench and decision rule

The regression adapter is node 36's Gaussian channel with its analytic cell/tail
operation. It must preserve the finite departure and both certificates within the
existing numerical tolerance.

The post-freeze transfer adapter is

```text
a_R(r)=g/(1+(r/Lambda)^2)^2,                             (37.5)
```

with the same massive-recoil energy class but no Gaussian tail subtraction. Its
mass operation is the shared numerical integrator. At `R=12` and
`N=16,32,64`, the unchanged compiler must preserve departure/measure identity,
contain direct continuum bound and open queries, and show decreasing certificates.
This supports transfer only across the Gaussian/algebraic-tail pair.

An adapter with a nonfinite threshold, invalid support, false monotonicity
contract, zero amplitude, or unresolved numerical cells must return a typed
refusal. Complete preprocessing/query counts are recorded, but transfer does not
promote cost leverage; that requires a separately frozen consumer and baseline.

Planned closure of regression, structural transfer, refusal, and cost-receipt
benches triggers synthesis. The horizon excludes anisotropic/operator-valued
channels, nonmonotone energy branches, threshold/on-cut resolvents, long-time
scattering, sign-indefinite spectral weights, and interval-rigorous numerics.

## Execute the frozen bench

The Gaussian regression retains its analytic mass adapter and therefore reports
zero mass-integration error. The independent algebraic-tail adapter uses numerical
mass, first-moment, second-moment, and tail operations. Its continuum values are
`-0.0344360031` for the below-threshold resolvent and `0.0121997293` for the
finite-time open event. The unchanged compiled route gives:

| cells | bound error / certificate | open error / certificate | preprocess / query |
| ---: | ---: | ---: | ---: |
| 16 | `4.25597e-4 / 2.31392e-3` | `1.06766e-5 / 8.44462e-5` | `1143 / 16` |
| 32 | `1.43258e-4 / 6.70252e-4` | `3.12903e-6 / 2.45208e-5` | `2151 / 32` |
| 64 | `3.78712e-5 / 1.72988e-4` | `8.07717e-7 / 6.39145e-6` | `4167 / 64` |

Every error is contained. The common second-moment term decreases from
`2.31352e-3` to `1.72592e-4`; the numerical cell-mass error
`5.48e-16`, centering error `1.76e-15`, and tail certificate `3.96103e-7`
remain explicit rather than being silently treated as exact. The generated finite
departure norm equals the truncated mass `0.0493476259`.

At each compiled error budget, direct bound/open quadrature costs respectively
`45+45`, `45+75`, and `45+75` evaluations. The compiled pair costs `2N` only
after preprocessing. Thus `N=16` can amortize after about twenty comparable mixed
batches, `N=32` after about thirty-nine, and `N=64` never beats this direct pair.
These are evaluation-count receipts, not a runtime or universal reuse advantage.

Invalid domains and thresholds, absent monotonicity admission, nonpositive
tolerances, and nonfinite mass operations return typed refusals. In particular,
the compiler checks that the declared threshold actually bounds the channel energy;
otherwise its resolvent certificate would have no semantic basis.

## Synthesis and boundary

`V_radial-transfer-1` rejects the hypothesis that Gaussian tail subtraction is an
essential part of moment compression. Positivity, shell mass, moment centering,
finite Fock action, and the two observable certificates survive unchanged across
one exponential and one algebraic form-factor family. What transfers is therefore
the radial measure interface, not merely a Gaussian formula.

The evidence does not support arbitrary positive densities, nonmonotone or
multibranch dispersion, anisotropic/operator-valued channels, on-cut or long-time
limits, interval rigor, or automatic computational leverage. This node stops:
another radial example cannot change the central verdict unless it crosses one of
those named boundaries. Executable evidence lives in
[`test_radial_transfer.py`](../computation/tests/test_radial_transfer.py); the
replayable disposition and implementation hashes live in
[`return-compiler-dispositions.md`](../results/return-compiler-dispositions.md).
