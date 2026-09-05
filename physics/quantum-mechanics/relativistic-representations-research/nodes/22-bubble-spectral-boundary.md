# Bubble spectral boundary and pole obstruction

Status: once-subtracted bubble boundary and open-channel density supported;
isolated Fock-pole recovery is rejected at the massless spin-two threshold, while
an exact infraparticle claim remains outside the one-loop horizon

## Capability and spine binding

Node 21 reduced the complete scalar--spin-two packet to one local massive tadpole
and one nonlocal massive--massless bubble. The proposed next step was to use that
bubble for both a pole quantity and an open-channel quantity. This node tests
whether both outputs actually exist in the same representation.

- **Upstream anchor:** node 21's coefficient `C_B(P)` and bubble `I_(1,1)(P)`.
- **Bridge question:** can one subtracted spectral boundary support both an isolated
  scalar pole/residue and its scalar--spin-two continuum?
- **Invariant target:** the same normalized nonlocal two-point kernel; local
  subtraction data are kept separate.
- **Downstream effect:** either complete the bound/open reuse claim or replace the
  pole endpoint by a threshold/dressed-state endpoint.
- **Special resources:** `mu=m^2>0`, a massless internal spin-two field, flat
  spacetime, the upper Feynman boundary, and a real subtraction point `P_0<mu`.
- **Rejoin edge:** a positive threshold density, its subtracted Cauchy transform,
  and a pole-admissibility/refusal record.

The horizon is the one-loop nonlocal kernel. It does not resum soft gravitons,
construct coherent asymptotic states, or prove an exact infraparticle theorem.

## Construct the finite boundary by subtraction

Node 21 generated the Feynman-parameter denominator

```text
l^2-x[mu-(1-x)P].
```

Put `y=1-x`. Near `d=4`, loop integration separates the bubble into a local
divergent constant and the finite `P`-dependent term

```text
-integral_0^1 dy log[mu-yP-i0].
```

Do not assign a finite value to the local constant. Choose `P_0<mu` and subtract
the same kernel at that point. The logarithm of the common Feynman-parameter factor
cancels, giving the finite boundary

```text
B(P;P_0)
  =-integral_0^1 dy
     log[(mu-yP-i0)/(mu-yP_0)].                 (22.1)
```

This subtraction preserves the nonlocal content and moves only affine local terms
into the renormalization data already separated in node 21.

For `P` below the cut, define the normalized primitive

```text
b(P)=1+(mu-P)/P log(1-P/mu),
b(0)=0.                                         (22.2)
```

Its origin is checked rather than asserted. Differentiate the integral in (22.1):

```text
d/dP [-integral_0^1 dy log(1-yP/mu)]
  =integral_0^1 dy y/(mu-yP)
  =-1/P-mu/P^2 log(1-P/mu).                    (22.3)
```

Direct differentiation of (22.2) gives the same expression, and both constructions
vanish at `P=0`. Therefore their common initial value and derivative construct

```text
B(P;P_0)=b(P)-b(P_0).                           (22.4)
```

The retained operation refuses a nonpositive `mu` or a subtraction point on or
above the cut.

## Generate the continuum from the same logarithm

Let `s>mu`. The argument `mu-ys` becomes negative precisely on

```text
y in (mu/s,1).
```

Across the upper/lower logarithmic boundaries, that interval contributes `2pi i`
times its length. Hence

```text
Disc b(s)=2pi i rho_B(s),

rho_B(s)=1-mu/s,       s>=mu.                  (22.5)
```

This density reconstructs the same subtracted boundary:

```text
B(P;P_0)
  =(P-P_0) integral_mu^infinity ds
    rho_B(s)/[(s-P-i0)(s-P_0)].                (22.6)
```

The executable certificate evaluates both sides below threshold and returns the
same value within quadrature error. Equation (22.6), not a second analytic model,
is the edge to the visible-measure compiler.

At `d=4`, node 21's nonlocal coefficient is

```text
C_4(P)=4mu P-2mu^2=2mu(2P-mu).
```

Therefore the packet's normalized open-channel density is

```text
rho_Sigma(s)
  =C_4(s)rho_B(s)
  =2mu(2s-mu)(1-mu/s),       s>=mu.            (22.7)
```

It starts continuously but not flat:

```text
rho_Sigma(mu)=0,

lim_(s->mu+) rho_Sigma(s)/(s-mu)=2mu.          (22.8)
```

This is a generated continuum kernel, up to the action's unresolved overall
coupling/Fourier normalization. It is not yet an inclusive cross section.

## The requested pole collides with the continuum

The free scalar shell is

```text
P_shell=mu.
```

The lightest state in the internal channel is the same scalar plus a spin-two
quantum of arbitrarily small energy, so the generated bubble threshold is

```text
P_threshold=(sqrt(mu)+0)^2=mu.                 (22.9)
```

Thus this bench has no spectral gap between the proposed particle pole and the open
channel. The obstruction is already visible in the same primitive. From (22.3),

```text
lim_(P->mu-) b'(P)=+infinity.                  (22.10)
```

The packet coefficient does not remove it:

```text
C_4(mu)=2mu^2 != 0.                            (22.11)
```

Consequently the conventional residue expression

```text
Z^(-1)=1-Sigma'(P_pole)
```

is not admitted at `P_pole=mu` by the one-loop Fock-space boundary. Local
counterterms can select mass and field normalization conditions, but they cannot
cancel the nonanalytic logarithmic derivative with a local polynomial.

A fixed-order local term might appear to move a trial root below the *free*
threshold. That does not construct an isolated dressed particle: the internal
scalar mass and the continuum endpoint must then be updated consistently. This is
a reconstruction signal, not an exact conclusion about the fully dressed theory.
The source contracts on soft gravity support coherent asymptotic dressing as one
perturbative realization and also record an obstruction to making it the universal
gravitational asymptotic Hilbert space. This node selects neither realization.

## What the common spectral object can and cannot compute

The original two-output request separates as follows:

```text
same rho_B
  |- subtracted Cauchy transform below mu
  |    -> finite off-shell/resolvent probes;
  |
  |- boundary discontinuity at and above mu
  |    -> supported open-channel kernel;
  |
  `- evaluation at the touching shell mu
       -> logarithmic derivative obstruction,
          no supported isolated Fock pole/residue.
```

This is more informative than forcing a pole calculation. It explains why the
bounded and scattering languages separate here: arbitrarily soft field quanta make
the open sector touch the nominal one-particle sector.

The downstream target must therefore be revised from

```text
isolated pole + continuum from one bubble
```

to

```text
threshold spectral boundary
  -> finite-resolution or inclusive open observable
  -> coherent/dressed asymptotic-state construction when required.
```

An infrared regulator can temporarily create a gap and provide a regression pole,
but the regulator-removal limit must track the residue and spectral measure. It
cannot be declared the physical endpoint in advance.

## Retained operation and checks

The workbench retains

```text
SubtractedBubble(mu,P_0)
  -> b(P)-b(P_0)
   + rho_B(s)
   + scalar-spin-two rho_Sigma(s)
   + shell diagnostic
   | refusal(mu<=0 or P_0>=mu).
```

Supported certificates cover:

- equality of the primitive derivative and the parameter-integral derivative;
- zero normalization at `P=0`;
- numerical coincidence of (22.4) and the dispersive reconstruction (22.6);
- the threshold value and slope in (22.8);
- divergence (22.10), nonzero coefficient (22.11), and the resulting shell
  refusal; and
- a transfer probe strictly below threshold, where the boundary is analytic but
  does not pretend to solve a pole equation.

## Boundary and next edge

Supported: one subtracted nonlocal kernel generates both its below-threshold
resolvent values and its continuum density. Rejected: the same bare Fock packet
does not support the requested isolated pole/residue at its touching massless
threshold.

Node 23 consumes the positive density and constructs a nested finite-resolution
effect algebra, its minimal cyclic realization, and a normalization-free
conditional response. Node 24 then rejects direct descent of that window through
the bare packet's external Ward quotient. Still open after that obstruction:

- fix local renormalization and overall action normalization;
- construct a characteristic external grammar whose Ward image repairs the window
  residual at `q^2=0`;
- compare coherent dressing, memory sectors, and algebraic asymptotic observables
  on node 23's same effects; and
- compare that complete route with the ordinary soft-factor baseline.

The next discriminating edge is the characteristic external completion generated
by node 24. Further master-integral manipulation would not change the pole or
observable-descent obstructions and is parked.

## Materials and edges

- Node 21 supplies `C_4`, the bubble, and the local/nonlocal split.
- `computation/src/fieldcalc/spectral.py` owns the retained boundary operation.
- `computation/tests/test_bubble_boundary.py` owns its equality, threshold,
  transfer, and refusal certificates.
- [Soft-gravity boundary contracts](../sources/soft-gravity-boundary-contracts.md)
  delimit the coherent-state interpretation.

```text
21 two-sector analytic lowering
  -> 22 subtracted bubble and touching-threshold obstruction
       -> 23 resolution-native effect algebra
       -> 24 external-ideal descent refusal
       -> characteristic completion and realization comparison.
```
