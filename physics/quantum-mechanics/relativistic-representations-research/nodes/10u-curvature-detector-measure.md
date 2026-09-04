# N10u — Curvature-Detector Spectral Measure

Status: supported for separate positive integer spins at the complete coefficient
through order `g^2`; the null-orbit measure and generated curvature construct the
detector-visible density, and one measure computes both a bound ground shift and an
excited open-channel event; finite coupling and physical higher-spin matter remain
outside the horizon

Consumes: [N4y quantization and recovery](04y-quantization-recovery-bridge.md),
[N9d operational bound/open channel](09d-operational-bound-open-channel.md),
[N10j generated curvature](10j-generated-curvature-compatibility.md), and
[N10t observable-factored response](10t-observable-factored-response.md)

Sources: [curvature-detector contracts](../sources/curvature-detector-contracts.md)

Computation: [curvature-detector measure
compiler](../computation/10u-curvature-detector-measure/README.md)

Produces: a representation-to-measure compiler, a cubic spin-one regression, a
quintic spin-two transfer, same-measure bound/open predictions, and an explicit
boundary between generated field content and supplied detector dynamics

## Research contract and motivation

N10t compiles every free curvature query to `G_Q K_s J`, but that is still a
classical response operation. Repeating another local curvature functional would
remain inside N10t's closed class and would not test whether the construction can
predict a quantum event.

The new obstruction is operational:

```text
the representation generates a physical curvature channel,
but it does not yet generate the measure seen by a prepared quantum probe.
```

The bench therefore asks:

> Given the N4y vacuum representation and N10j curvature operation, can a finite
> detector preparation construct its departure measure without solving a dressed
> Fock problem, and can the same constructed measure compute one bound and one open
> observable?

The internal stop is strict. The node must derive the frequency power, transfer
from spin one to spin two without a component polarization basis, recover both
observables from one measure, and audit the complete route. It must not infer a
universal higher-spin matter coupling, an exact resonance, or an `S` matrix.

## 1. Separate what the field generates from what the detector supplies

Fix a positive integer spin `s`. N4g/N4y provide the positive-energy helicity
space and its bosonic Fock vacuum `Omega_F`. N10j provides the gauge-invariant
order-`s` curvature operation `K_s`.

The detector supplies only the data a representation cannot choose:

```text
K_D=C|g> direct-sum C|e>,
H_D=Omega |e><e|,
m=|g><e|+|e><g|,
f=localized spatial smearing,
e=detector contraction on the curvature carrier,
g=coupling strength.                                  (1.1)
```

Construct the smeared curvature observable

```text
C_s(f,e)=integral f(x) <e,K_s Phi_s(x)> d^3x           (1.2)
```

and the effective interaction Hamiltonian

```text
V_s=m tensor C_s(f,e),
H_s=H_D+H_F+g V_s.                                    (1.3)
```

Equation (1.3) is a declared detector model, not a consequence of Poincare
symmetry. Its virtue is narrower: because `K_s` annihilates gauge images, the
probe couples directly to N10t's physical observable quotient and never asks for
a gauge representative.

## 2. Construct the departure map before naming a bath

Use the common prepared subspace

```text
Ran P=span{|g,Omega_F>,|e,Omega_F>},  Q=1-P.            (2.1)
```

The free detector-plus-field Hamiltonian preserves `P`, while the annihilation
part of `C_s(f,e)` kills the vacuum. Therefore the departure map is computed:

```text
B_s=Q V_s P,
B_s|g,Omega_F>=|e> tensor c_s^dagger(f,e)Omega_F,
B_s|e,Omega_F>=|g> tensor c_s^dagger(f,e)Omega_F.      (2.2)
```

The full perturbative departure is `gB_s`. Through the first nonzero return order,
both departures lie exactly in the
one-particle sector. Thus the coefficient through order `g^2` requires neither a
dressed Fock eigenvector nor a Fock truncation. As in N9d, the two prepared
vectors lead to shifted diagonal entries of one operator-valued measure; they do
not pretend that one vector is both isolated and embedded.

## 3. Generate the scalar measure from the null orbit and curvature

Write a future null momentum as `p=omega(1,n)`, with `omega>0` and `n in S^2`.
The invariant shell measure becomes

```text
d^3p/(2|p|)=(omega/2) d omega dOmega(n).               (3.1)
```

Let `kappa_(s,h)(n)` be the normalized curvature shell image of helicity
`h=+-s`, and let `Pi_(s,h)(n)` be its rank-one orthogonal projector. No component
formula is needed. The detector-visible angular operator is first constructed as

```text
Q_s=integral_(S^2)[Pi_(s,+)(n) direct-sum Pi_(s,-)(n)]dOmega(n). (3.2)
```

N10j's two chiral curvature summands restrict under rotations to two irreducible
spin-`s` modules, each of dimension `2s+1`. For either sign, covariance computes

```text
U_s(R) Q_(s,+) U_s(R)^(-1)
 =integral U_s(R)Pi_(s,+)(n)U_s(R)^(-1)dOmega(n)
 =integral Pi_(s,+)(Rn)dOmega(n)
 =Q_(s,+).                                             (3.3)
```

Thus `Q_(s,+)` is an intertwiner of one irreducible rotation module and must be
`c_s I`. The coefficient is not calibrated. Taking the trace on the same operator
gives

```text
(2s+1)c_s=Tr Q_(s,+)
 =integral Tr Pi_(s,+)(n)dOmega(n)
 =4 pi,

c_s=4 pi/(2s+1).                                      (3.4)
```

The conjugate summand has the same coefficient. If the supplied detector
contraction decomposes as `e=e_+ direct-sum e_-`, the scalar response is therefore
generated:

```text
A_(s,e)=<e,Q_s e>
 =(4 pi/(2s+1))(||e_+||^2+||e_-||^2).                 (3.5)
```

The detector tensor and its invariant norm remain physical inputs; their integrated
response does not. A zero norm returns a blind-channel refusal. If the smearing is
anisotropic, its angular weight lies inside the integral and (3.3) no longer
commutes with all rotations. The compiler then retains a direction-dependent
positive operator and refuses the scalar radial quotient.

N10j constructed `K_s` with derivative degree `s`. On the null ray its creation
amplitude therefore gains `omega^s`; the spectral weight gains `omega^(2s)`.
Multiplying, rather than merely comparing, the three constructed factors gives

```text
orbit shell       omega/2
curvature square  omega^(2s)
smearing square   |fhat(omega n)|^2
------------------------------------------------------
dnu_(s,e)(omega)
 = (A_(s,e)/2) omega^(2s+1)|fhat(omega)|^2 d omega.   (3.6)
```

Equation (3.6) is the retained compiler output. The frequency exponent was not a
prescribed spectral density. It is generated as

```text
(spatial dimension - 2) + 2*(curvature degree)
 =1+2s.                                                (3.7)
```

For the isotropic Gaussian regression

```text
|fhat(omega)|^2=exp[-(omega/Lambda)^2],                (3.8)
```

the total visible weight supplies an independent analytic check:

```text
nu_s(R_+)=(A_(s,e)/4)Lambda^(2s+2) Gamma(s+1).         (3.9)
```

## 4. One operator-valued measure, two preparations

The free complementary energies relative to the two prepared states differ:

```text
ground departure:   Omega+omega,
excited departure:  omega-Omega.                       (4.1)
```

The ground vacuum is below its complementary continuum. Its complete order-`g^2`
energy shift and prepared residue are the off-axis transforms

```text
delta E_g^(2)=-g^2 integral_0^infinity
                    dnu_s(omega)/(Omega+omega),
Z_g^(2)=1-g^2 integral_0^infinity
                    dnu_s(omega)/(Omega+omega)^2.      (4.2)
```

For the excited vacuum, Dyson's first transition amplitude gives the complete
emitted-one-particle event through the same order:

```text
P_emit^(2)(t)=g^2 integral_0^infinity
  4 sin^2[(Omega-omega)t/2]/(Omega-omega)^2
  dnu_s(omega).                                        (4.3)
```

If (3.3) has a continuous density `rho_s` at `Omega`, the boundary coefficient is

```text
Gamma_s=2 pi g^2 rho_s(Omega),
P_emit^(2)(t)/t -> Gamma_s.                            (4.4)
```

This is an order-`g^2` long-time coefficient, not a proof that survival is
`exp(-Gamma_s t)` at finite coupling. The Fourier transform

```text
K_s(t)=g^2 integral exp(-i omega t)dnu_s(omega)         (4.5)
```

is retained by the same measure for memory queries; no second bath or fitted
kernel enters.

## 5. Regression and transfer

For a detector with `||e_+||^2+||e_-||^2=1`, `Lambda=2`, `Omega=1.2`, and
`g=0.005`, the compiler returns

```text
spin 1: rho_1(omega)=(2pi/3)omega^3 exp[-omega^2/Lambda^2],
spin 2: rho_2(omega)=(2pi/5)omega^5 exp[-omega^2/Lambda^2]. (5.1)
```

The spin-one cubic law is a regression of the derivative-field phase-space count;
it is not identified with a particular atom. Spin two is constructed by changing
only the representation label. At the same detector norm and frequency,

```text
rho_2(omega)/rho_1(omega)=(3/5)omega^2,                (5.2)
```

so the transfer exposes both the extra derivative order and the generated change
in coherent-frame normalization rather than hiding either in a fitted density.

The executable independently factors (3.3), checks (3.6), computes (4.2)--(4.5),
and verifies `Gamma_s t<0.25` at its `t=160` finite-time rate probe. Its printed values are
the numerical record; the mathematics does not depend on those chosen scales.

## 6. Complete-route cost and what has actually been compressed

```text
representation-derived free field + vacuum
  -> generated curvature K_s
  -> declared finite detector preparation
  -> one-particle departure B_s
  -> exact helicity/angular quotient
  -> one scalar measure nu_s
       |-> Stieltjes transform: bound shift and residue
       |-> finite-time kernel: emitted event
       |-> continuum boundary: rate coefficient
       `-> Fourier transform: memory.
```

| Task | Unreduced route | N10u route | Reason the reduction is valid |
| --- | --- | --- | --- |
| order-`g^2` departure | field operator on full Fock space | one created particle | vacuum annihilation and one interaction insertion |
| detector-visible channel | momentum, direction, helicity, gauge representative | scalar radial measure | curvature kills gauge; isotropic smearing and (3.2) integrate the finite physical fiber |
| ground shift | complementary resolvent matrix element | one positive radial quadrature | ground denominator is off spectrum |
| emitted event | time-dependent field amplitudes | one kernel transform of the same measure | Parseval/spectral resolution at fixed perturbative order |
| repeated query | rebuild shell contraction | cache `nu_s`, change transform | every output factors through the same departure vector |
| exact finite coupling | dressed cyclic Fock spectrum | not attempted | higher returns leave the one-particle sector |

The strongest compression is semantic: gauge and detector-invisible directions are
removed exactly. The practical gain then comes from sparsity in perturbative order,
rotational integration, and reuse of one scalar measure. No component polarization
or tensor expansion is required. What remains expensive is honest: a non-isotropic
detector retains angular data, higher orders reach multiparticle sectors, and an
interacting higher-spin theory is not generated by this free construction.

## 7. Global verdict and stop

N10u is genuinely different from N10t. N10t compiles a classical free response;
N10u constructs the reduced quantum object visible to a prepared probe and uses it
for two operationally different outputs. The retained generative tool is

```text
CompileCurvatureDetectorMeasure(
  spatial dimension,
  positive one-particle helicity representation,
  generated curvature degree and shell action,
  detector contraction and smearing)
 -> positive visible measure,
    spin-transfer law,
    bound/open/memory transform interface,
    angular-generation and horizon certificates.      (7.1)
```

The node reaches its internal bench and stops. Re-entry is justified only by one
of these new obstructions:

1. anisotropic or moving detectors that prevent the angular quotient;
2. finite-coupling control of the cyclic Fock sector;
3. a physically derived matter coupling rather than the effective probe (1.3);
4. an interacting or curved background where `K_s` no longer commutes with the
   selected dynamics;
5. an incoming asymptotic channel requiring an actual `S` matrix.

## Verification ledger

| Obligation | Witness | Verdict |
| --- | --- | --- |
| construct rather than prescribe the density power | equations (3.1) and (3.6)--(3.7), plus executable factor route | exact in the declared free isotropic model |
| avoid component polarizations | covariant projector average (3.2)--(3.5) | exact; detector norm is supplied, response is generated |
| refuse an unjustified scalar quotient | anisotropic and blind-detector regressions | supported with explicit failure records |
| retain physical screen only | `K_s` gauge annihilation plus nonzero `A_(s,e)` | exact conditional on a seeing detector |
| recover a bound observable | shift and residue (4.2) | complete coefficient through order `g^2` |
| recover an open observable | finite event (4.3) and boundary coefficient (4.4) | complete coefficient through order `g^2`; no exponential claim |
| use one measure for both | identical `nu_s` in (4.2)--(4.5) | exact |
| transfer beyond a single example | generated powers `3` and `5`, ratio (5.2) | checked for spins one and two; formula applies separately to every positive integer spin |
| claim physical higher-spin matter | detector coupling is supplied | rejected |
| claim finite-coupling prediction | multiparticle returns omitted | rejected |

## Edges

- `N4y -> N10u`: pass the vacuum Fock representation and the exact
  vacuum-to-one-particle creation map.
- `N10j -> N10u`: pass the generated order-`s` gauge-invariant curvature shell
  action and its two physical helicity lines.
- `N10t -> N10u`: pass the observable-first rule and the refusal to construct a
  gauge-dependent field response before the named curvature query.
- `N9d -> N10u`: pass the two-preparation operator-valued measure semantics and
  finite-time bound/open transforms; N10u replaces N9d's scalar prescribed field
  channel by the curvature measure generated from the representation spine.
- `N10u -> global generative spine`: return the first representation-generated
  quantum spectral measure with same-object bound/open use and its explicit
  effective-detector boundary.
