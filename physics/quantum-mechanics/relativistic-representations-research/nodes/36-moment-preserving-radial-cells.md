# Moment-preserving radial cells

Status: `V_radial-moment-1` supports second-order common certification and only
amortized query leverage; single-query leverage and cross-family transfer remain
unsupported

Consumes: node 35's shell-normalized finite departure and its rejected
first-order accuracy certificate.

Produces: either a reusable second-order certificate for the same bound/open
queries or a cost/tightness obstruction that stops this route.

## Obstruction: exact mass does not cancel spectral drift

Node 35 preserves every cell mass `m_j`, but assigns the midpoint energy
`epsilon_j=E(r_mid)`. For a transform `F`, its cell error begins with

```text
F'(epsilon_j) integral_(I_j)(E(r)-epsilon_j)dM(r).       (36.1)
```

Nothing makes (36.1) vanish. Bounding it by the largest energy displacement
therefore produces the observed first-order Lipschitz certificate even though the
actual midpoint error happens to decay quadratically.

## Construct the representative from the missing equality

Keep node 35's generated action coefficient `c_j=sqrt(m_j)` unchanged. Construct
the channel energy from the first energy moment instead:

```text
u_j=integral_(I_j) E(r)dM(r),
e_j=u_j/m_j,
q_j=integral_(I_j)(E(r)-e_j)^2dM(r).                    (36.2)
```

Then the previously failed equality is repaired internally:

```text
integral_(I_j)(E(r)-e_j)dM(r)=u_j-e_j m_j=0.            (36.3)
```

For twice differentiable `F`, Taylor's identity at `e_j` gives

```text
integral F(E)dM-m_jF(e_j)
 =F'(e_j) integral(E-e_j)dM
  +integral (E-e_j)^2 integral_0^1(1-s)F''(e_j+s(E-e_j))ds dM,

|error on [0,R]| <=(1/2) sup|F''| sum_j q_j.            (36.4)
```

If numerical integration returns `u_hat_j` with error `eta_j`, use
`e_hat_j=u_hat_j/m_j`. The linear residual is then bounded by `eta_j`; compute a
nonnegative upper estimate `q_hat_j+xi_j` for the centered second moment. The
executable certificate is

```text
|error on [0,R]|
 <=sup|F'| sum_j eta_j +(1/2)sup|F''| sum_j(q_hat_j+xi_j). (36.5)
```

This explicitly admits the numerical substrate instead of treating quadrature as
an exact moment oracle.

For the bound resolvent below threshold, with `d=mu-z`, (36.5) and node 35's tail
become

```text
epsilon_res <=eta/d^2+q/d^3+T_R/d.                      (36.6)
```

For `K_t=|integral_0^t exp(-is delta)ds|^2`, differentiating the integral gives

```text
|K_t'|<=t^3,
|K_t''|<=2(t^3/3)t+2(t^2/2)^2=7t^4/6,
epsilon_open <=t^3 eta +(7t^4/12)q+t^2T_R.              (36.7)
```

Thus one pair `(eta,q)` must certify both observables; no observable-specific cell
fit is admitted.

## Frozen candidate and bench

```text
CompileRadialDeparture(C_radial-moment-v1)
 -> unchanged shell masses and finite Fock departure
    + moment-centered channel energies
    + centering-error and second-moment bounds
    + first- and second-order transform certificates
    + moment-construction evaluation count
 | the refusals inherited from C_radial-v1.
```

The implementation uses the already pinned SciPy quadrature substrate. Its error
estimate is part of the numerical certificate and is not promoted to an interval-
arithmetic proof. The candidate's semantics are frozen before the bench: examples
may change parameters but cannot change the centering or error law.

The decisive fixture remains node 35's Gaussian model, `R=5`, `N=16,32,64`,
`z=0`, and `t=1/2`. Promote tight certification only if both second-order bounds
contain the continuum comparison, decrease approximately as `N^-2`, and improve
over the first-order bounds. Count every integrand evaluation used to construct
the moments. Compare total work for `Q` mixed bound/open queries against direct
adaptive quadrature at matched requested tolerance; report a break-even query count
rather than hiding preprocessing.

An independent Gaussian parameter fixture tests robustness only. Cross-form-factor
transfer remains outside this contract. Refuse leverage if the certified cell count
or full moment-construction cost cannot beat the direct route for any declared
query regime.

## Execute the frozen bench

The moment integration reports total centering error `4.74e-15` for every declared
refinement. The centered second-moment bound falls from `3.07664e-3` at 16 cells to
`1.97937e-4` at 64 cells. The two observable results are:

| cells | bound error / certificate | old bound | open error / certificate | old open |
| ---: | ---: | ---: | ---: | ---: |
| 16 | `4.44213e-4 / 3.07664e-3` | `4.74764e-2` | `1.50268e-5 / 1.12169e-4` | `5.93455e-3` |
| 32 | `1.14462e-4 / 7.87126e-4` | `2.29230e-2` | `3.84091e-6 / 2.86973e-5` | `2.86537e-3` |
| 64 | `2.88402e-5 / 1.97937e-4` | `1.12360e-2` | `9.65632e-7 / 7.21646e-6` | `1.40450e-3` |

Both new certificates contain the continuum comparison and fall by factors
`0.256` then `0.251`, consistent with the constructed second-order remainder.
They exceed observed error by only about `6.9` for the resolvent and `7.5` for the
open kernel, rather than by hundreds. The bound-transform approximation itself is
less accurate than node 35's midpoint value: moment preservation improves the
certificate, not every transform value. This prevents an illicit promotion from
certifiability to universal approximation quality.

Moment construction costs `42N` integrand evaluations; a mixed bound/open batch
costs `2N` compiled evaluations. Direct adaptive quadrature at each compiled
certificate's requested tolerance uses 75 evaluations per transform. The complete
evaluation-count comparison is therefore:

| cells | preprocess | compiled batch | direct batch | first winning batch |
| ---: | ---: | ---: | ---: | ---: |
| 16 | 672 | 32 | 150 | 6 |
| 32 | 1344 | 64 | 150 | 16 |
| 64 | 2688 | 128 | 150 | 123 |

The compiler loses for a single batch and wins only after the stated number of
repeated mixed queries. This is an amortized sufficient-statistic gain under a
pinned integrand-evaluation model, not a wall-time theorem. The second Gaussian
fixture also contains both errors (`7.77e-5 <= 4.95e-4` bound and
`3.57e-7 <= 2.53e-6` open). Numerically underresolved cells and inherited invalid
requests return typed refusals.

Executable evidence lives in
[`test_radial_moments.py`](../computation/tests/test_radial_moments.py); the
replayable disposition and exact implementation hashes live in
[`return-compiler-dispositions.md`](../results/return-compiler-dispositions.md).

## Horizon and stop rule

The horizon is the same regulated monotone scalar family and finite-time/below-
threshold transforms as node 35. Containment, rate, robustness, refusals, and the
declared complete evaluation-count comparison are classified, so this branch
stops. Re-enter interval rigor only if a downstream result requires proof beyond
the admitted SciPy numerical error; re-enter transfer only with a structurally
different positive form factor. Re-enter cost only with a named repeated-query
consumer or a cost model that weights integrand bodies and memory as well as calls.
