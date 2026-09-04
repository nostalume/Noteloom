# N10v — Visible-Measure Compiler and Cross-Regime Transfer

Status: supported for positive radial one-particle channels with an already reduced
finite internal fiber and a strictly monotone energy map; one retained compiler
recovers N10u's massless curvature-detector measure and N9c's massive recoil
measure, their bound/open transforms, threshold behavior, and refusal boundaries

Consumes: [N9c field-derived measure](09c-field-derived-coupling-measure.md),
[N10u curvature-detector measure](10u-curvature-detector-measure.md),
[field-derived measure contracts](../sources/field-derived-measure-contracts.md),
and [curvature-detector contracts](../sources/curvature-detector-contracts.md)

Computation: [visible-measure
compiler](../computation/10v-visible-measure-compiler/README.md)

Produces: a typed factor-to-pushforward generator, a cross-regime transfer witness,
same-object transform operations, and refusals for unjustified scalar reduction

## Research contract and paper-level obstruction

N10u generates a curvature-detector density, but its first executable could still
be read as a spin-dependent formula generator. A paper-owning tool must retain the
operation common to a genuinely different channel. N9c supplies the discriminator:
its one-boson energy is massive and nonlinear in radius, its Hilbert measure is
`L^2(d^3k)`, and its threshold density is a square root rather than a massless odd
power.

The bridge question is therefore:

> Can one interface construct the observable-visible spectral measure from typed
> orbit, observable, preparation, and energy factors, without receiving either
> expected density, and can its output compute bound and open quantities in both
> the massless-curvature and massive-recoil regimes?

The invariant target is the departure measure itself. The internal benchmark is:

1. derive the pushforward operation on arbitrary admitted radial factors;
2. recover N10u including its generated angular coefficient;
3. transfer without changing the interface to N9c and recover its independent
   density and square-root threshold;
4. use both returned measures in bound and open transforms;
5. refuse a noninjective radial energy unless its monotone branches are supplied.

Finite coupling, anisotropic angular operators, multiband branch enumeration, and
publication novelty are outside this node. The executable samples monotonicity as a
regression guard; admission of a new analytic channel still requires a mathematical
positivity witness for `epsilon'`.

## 1. The common object is not a field equation or a guessed bath

After the physical internal fiber has been reduced, let `r>=0` parameterize a
radial one-particle channel. The compiler receives four independent factor maps:

```text
q(r) dr       orbit/Hilbert radial measure,
a(r)          observable shell amplitude,
h(r)          preparation/departure amplitude,
epsilon(r)    complementary energy.                   (1.1)
```

Their origins remain typed:

- representation and Hilbert normalization construct `q`;
- the named observable constructs `a`;
- physical preparation supplies `h`;
- dynamics supplies `epsilon`.

The representation does not generate the last two. Conversely, the user does not
supply the product density. The compiler constructs the positive radial measure

```text
dM_rad(r)=q(r)|a(r)|^2|h(r)|^2 dr.                     (1.2)
```

This multiplication is the semantic quotient: every direction absent from the
prepared observable matrix element has already vanished, while every surviving
weight retains its provenance.

## 2. Monotone energy constructs the spectral pushforward

Assume `epsilon(0)=E_th` and `epsilon'(r)>0` for `r>0` on the declared window.
Then `r(E)=epsilon^(-1)(E)` is single valued. The spectral measure is defined by
pushforward, not by a density ansatz:

```text
M(Delta)=integral 1_Delta(epsilon(r))dM_rad(r).         (2.1)
```

To construct its density, evaluate both routes on an arbitrary compactly supported
test function `F`. Substitute `E=epsilon(r)` in the radial route:

```text
integral F(E)dM(E)
 =integral F(epsilon(r))q(r)|a(r)|^2|h(r)|^2 dr
 =integral_(E_th)^infinity F(E)
    [q(r(E))|a(r(E))|^2|h(r(E))|^2/epsilon'(r(E))]dE. (2.2)
```

Both expressions are linear functionals on the same `F`; their equality constructs

```text
m(E)=q(r(E))|a(r(E))|^2|h(r(E))|^2/epsilon'(r(E)).    (2.3)
```

No expected exponent occurs in the input. If `epsilon` turns around, equation
(2.3) omits branches and is false. The retained compiler therefore refuses rather
than silently choosing one root. A future multibranch extension must accept or
construct a branch partition and sum the corresponding positive densities.

## 3. Regression: massless curvature detector

N10u supplies, for spin `s` and isotropic detector smearing,

```text
q_s(r)=r/2,
|a_s(r)|^2=A_(s,e)r^(2s),
|h_s(r)|^2=g^2 exp[-(r/Lambda)^2],
epsilon_s(r)=r,                                       (3.1)

A_(s,e)=(4pi/(2s+1))(||e_+||^2+||e_-||^2).            (3.2)
```

The general construction (1.2)--(2.3), rather than a curvature-specific branch,
returns

```text
m_s(E)=(g^2 A_(s,e)/2)
       E^(2s+1)exp[-(E/Lambda)^2].                     (3.3)
```

For spin two, unit detector norm, `Lambda=2`, and `g=0.005`, the executable obtains

```text
A_(2,e)=4pi/5,
M(R_+)=0.002010619298297407...,
delta E_g^(2)=-0.0004667403137295436...,
2pi m_2(1.2)=0.0003426809465268917....                 (3.4)
```

The generated density agrees with the independently factored N10u route to
`2.2e-19` at the tested frequencies, and its total mass agrees with the analytic
Gaussian moment to `6.1e-17` absolute error.

## 4. Transfer: massive scalar recoil without changing the interface

N9c supplies different factor maps:

```text
q(r)=4pi r^2,
|a(r)|^2=1,
|h(r)|^2=g^2 exp[-(r/Lambda)^2],
epsilon(r)=sqrt(r^2+mu^2)+r^2/(2M).                   (4.1)
```

The energy is strictly increasing for `r>0` because

```text
epsilon'(r)=r[1/sqrt(r^2+mu^2)+1/M]>0.                (4.2)
```

Thus the same compiler admits the channel and returns (2.3). With N9c's
`M=2`, `mu=Lambda=1`, and `g=0.2`, it obtains

```text
M(R)=0.2227331198732604...,
m(1.5)=0.1641385063882749...,
Sigma(0)=-0.1286719829210452...,
2pi m(1.5)=1.031312651681211....                       (4.3)
```

These values coincide with N9c's independently implemented radial/density routes.
The total mass differs from `g^2 pi^(3/2)Lambda^3` by `8.0e-15`, and the density at
`E=1.5` agrees with N9c's closed inversion to displayed precision.

The threshold law is also generated rather than entered. Put

```text
epsilon(r)=mu+c r^2+O(r^4),
c=(1/2)(1/mu+1/M).                                    (4.4)
```

Then `r(E)=sqrt((E-mu)/c)+O((E-mu)^(3/2))`. Substitution in (2.3) computes

```text
m(mu+y)
 =[2pi g^2/c^(3/2)]sqrt(y)+O(y^(3/2)).                (4.5)
```

At `y=10^-6`, the compiler's ratio `m(mu+y)/sqrt(y)` differs from the constructed
coefficient by `3.01e-7`. The same interface has therefore transferred from a
massless odd-power threshold to a massive square-root threshold without receiving
either result.

## 5. Retained operations and actual use

The public research interface is

```text
CompileVisibleMeasure(
  radial orbit/Hilbert factor q,
  observable shell action a,
  preparation amplitude h,
  energy epsilon,
  construction window)
 -> positive radial measure,
    spectral pushforward and density,
    Stieltjes/Fourier/boundary transform operations,
    provenance and positivity certificates,
    monotonicity or branch-refusal record.             (5.1)
```

The two uses are not identical physical models, which is precisely why the transfer
matters:

| Input | Generated measure feature | Bound use | Open use |
| --- | --- | --- | --- |
| massless spin-two curvature detector | quintic density and `4pi/5` angular coefficient | detector ground shift | excited detector rate at its gap |
| massive scalar recoil field | square-root threshold and nonlinear energy Jacobian | vacuum self-energy at `z=0` | complementary boundary loss at `E=1.5` |

Both uses call the same returned Stieltjes and boundary operations. Neither
reconstructs the field equation, shell quotient, or density for each query.

## 6. Whole-route computation verdict

```text
unreduced prepared field channel
  -> remove gauge/internal directions invisible to the observable
  -> multiply three provenance-preserving radial factors once
  -> push through one energy map once
  -> cache M
  -> reuse transforms for bound, open, and memory questions.
```

This is more than shorter notation. At the supported perturbative return order:

- the massless route replaces direction, two helicity lines, and gauge
  representatives by one radial density after an exact projector average;
- the massive route replaces a three-dimensional one-boson integral by one radial
  measure and, when useful, one energy density;
- repeated observables reuse the same measure rather than repeat angular/shell
  construction;
- construction cost is one factor assembly and monotonicity audit per channel;
- recovery cost is one scalar transform per requested observable.

The compiler does not reduce the generic interacting spectral problem. Higher Fock
returns alter the departure measure; anisotropy retains an angular operator;
noninjective bands require branch data; and no runtime theorem is claimed without a
concrete discretization. The supported gain is exact semantic compression and
one-dimensional transform reuse within the stated order and symmetry class.

## 7. Global verdict and synthesis readiness

N10v passes regression, transfer, and use:

- **regression:** it reconstructs the complete N10u massless density without its
  formula as input;
- **transfer:** the unchanged interface reconstructs N9c's nonlinear massive
  density and threshold law;
- **use:** both outputs compute a bound and an open quantity through retained
  transforms;
- **failure:** an unpartitioned nonmonotone dispersion returns a branch refusal.

This closes the smallest generative-tool obligation identified after N10u. The
supported paper spine may now be organized around the visible-measure compiler,
with the field-equation machinery serving as construction substrate and regression
evidence. This is synthesis readiness, not a publication novelty verdict. A focused
literature comparison and manuscript composition remain separate outputs.

Re-enter research only if the paper's scoped claim requires anisotropic operator
measures, explicit perturbative remainder control, or a multibranch physical model.
Do not add more spins, dimensions, or transforms merely to enlarge the table.

## Verification ledger

| Obligation | Witness | Verdict |
| --- | --- | --- |
| do not receive expected density | factor-only `RadialChannel` interface | supported |
| construct pushforward semantics | arbitrary-test-function equality (2.2) | exact under monotonicity |
| generate angular response | N10u projector average and trace | exact for isotropic smearing |
| massless regression | equations (3.1)--(3.4) and executable | passed |
| genuinely different transfer | massive nonlinear dispersion (4.1)--(4.5) | passed against independent N9c route |
| downstream use | bound and boundary transforms in both regimes | passed |
| noninjective input | nonmonotone regression | refused; branch partition required |
| finite-coupling prediction | not constructed | rejected outside scope |

## Edges

- `N10u -> N10v`: pass the generated curvature shell weight and angular projector
  average as the massless regression input.
- `N9c -> N10v`: pass the independent massive one-boson factors, nonlinear energy,
  and reference outputs as the transfer discriminator.
- `N10v -> paper synthesis`: pass the factor-to-measure generator, its two
  inequivalent uses, and all refusal/approximation boundaries as the main
  constructive claim.
