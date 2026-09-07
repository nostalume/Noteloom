# Prepared matter-event compiler

Status: scalar and parity-doubled fermion amplitudes reach positive conditional
detector measures on declared `2+1`-dimensional Born-event domains; an absolute
cross section, a single-parity trace, infrared completion, and loops remain open

Consumes: node 29's characteristic scalar amplitude and fixed-event effect, node
27's ordered fermion subset state, and node 05's exterior/Clifford normal form.

Produces: shell-generated detector densities, conditional aperture observables,
fermionic use-level cost receipts, and the resolved three-photon density consumed
by node 31.

## Obstruction

A positive point effect is not yet a detector probability: it has no shell
pushforward, accepted region, or normalization. Conversely, attaching an arbitrary
phase-space integral would not test whether graph/algebra compression survives its
physical consumer. The measure must be generated from the same shell data, and the
compressed and explicit routes must reach the same event before their complete
costs are compared.

## Generate a finite scalar detector measure

Use `eta=diag(-1,1,1)`, `p=(m,0,0)`, `q=(omega,omega,0)`, and
`q'=omega'(1,cos(theta),sin(theta))`. Evaluating the generated final momentum
`p'=p+q-q'` on its shell computes

```text
0=eta(p',p')+m^2
 =2m(omega'-omega)+2omega omega'(1-cos(theta)),
omega'=m omega/[m+omega(1-cos(theta))].          (30.1)
```

Declare `<r|s>=2E_r(2pi)^2 delta^2(r-s)`. Eliminating spatial momentum from its
positive shell distribution and differentiating the remaining energy constraint
`F` on (30.1) gives

```text
dPhi_2=[d omega' d theta/(8pi E')]delta(F),
|partial_(omega')F|=[m+omega(1-cos(theta))]/E',
dPhi_2=d theta/[8pi(m+omega(1-cos(theta)))].     (30.2)
```

The amplitude and density share reflection symmetry. Quotient the circle with its
multiplicity two and set `t=tan(theta/2)` on `0<=theta<pi`; direct substitution
constructs

```text
dPhi_2=dt/[2pi(m+(m+2omega)t^2)], 0<=t<infinity. (30.3)
```

For `m=omega=1`, node 29's compiler returns

```text
epsilon_in=(0,0,1),   epsilon_out=(0,2t/(1+t^2),-(1-t^2)/(1+t^2)),
<epsilon_in,epsilon_in>=<epsilon_out,epsilon_out>=1,

M(t)=2(1-t^2)/(1+t^2),

dnu(t)=|M(t)|^2 dPhi_2
      =2(1-t^2)^2/[pi(1+t^2)^2(1+3t^2)]dt.      (30.4)
```

Every factor is nonnegative and the Ward residual vanishes before integration, so
`nu` is a positive measure on detector apertures. Its total mass and symmetric
forward aperture are

```text
nu([0,infinity))=-2+4sqrt(3)/3,
nu([0,1])=-1-1/pi+8sqrt(3)/9,

P([0,1] | declared event)
 =nu([0,1])/nu([0,infinity))
 =7/6+sqrt(3)/3-(sqrt(3)+3/2)/pi.                (30.5)
```

Numerical pushforward reproduces these values with errors `1.85e-14`, `2.46e-15`,
and `5.07e-14`, using `105`, `63`, and `168` density evaluations. Normalization is
conditional on the declared tree event; without incoming flux and charged
asymptotic completion it is not a cross section.

## Transfer the consumer to an ordered fermion line

Fermion vertices retain their order, so the scalar recurrence cannot be relabelled.
Node 05's operation `{C(v),C(w)}=-2eta(v,w)` instead generates

```text
K(r)=C(r)-m,  S(r)=-(C(r)+m)/(m^2+eta(r,r)),
K(r)S(r)=1,   C(k)=K(r+k)-K(r).                 (30.6)
```

For two photons the finite difference forces the two ordered insertions. Between
the shell projectors `Pi,Pi'`, replacing either polarization by its momentum
telescopes to zero. The parity-even effect is therefore

```text
R_f=2 grade_0[N(Pi') star N(A) star N(Pi) star N(A)^bar]. (30.7)
```

On the unit Compton family, `N(A)` has six blades and gives the positive expression
`[(2t^3-t)^2+1]/[(1+t^2)^2(1+3t^2)]`. Its forward fraction is
`0.630203193162627`. Effect plus Ward admission takes `293` exterior products
against `1386` trace-recurrence updates and preserves the same measure. This is a
use-level algebra transfer, but because the interface and bench were co-developed
it is not independent transfer evidence for the frozen compiler contract.

## Generate a resolved three-photon event

Take one incoming photon and two outgoing photons in the fixed angular cell

```text
p=(1,0,0), q=(1,1,0),
r_1=x(1,0,1), r_2=y(1,0,-1), p'=p+q-r_1-r_2.  (30.8)
```

The final fermion shell computes

```text
0=1+eta(p',p')=-2+4x+4y-4xy,
y=(1-2x)/[2(1-x)],             0<x<1/2.        (30.9)
```

With the declared one-particle normalization, eliminate `p'` and then `y` from
the three-body shell distribution. Since the energy-delta derivative is
`(2-2x)/E'`, the `E'` factor cancels and leaves, per unit angular acceptance,

```text
dPhi_3=dx/[64pi^3(2-2x)].                       (30.10)
```

Both endpoints are soft. A detector resolution `delta>0` must therefore be input.
Requiring both outgoing energies to exceed it generates

```text
x_+=(1-2delta)/[2(1-delta)],
x_delta(u)=delta+(x_+-delta)u/(1+u),  0<u<infinity.
```

For `delta=1/10`, the compiler obtains

```text
x=(40u+9)/[90(u+1)], y=(5u+36)/(50u+81),
dPhi_3=31du/[128pi^3(u+1)(50u+81)].             (30.11)
```

Node 27 generates the three-photon operator `A_3=F_{0,1,2}`. The projected
grade-zero readout gives a nonnegative rational effect; its numerator has strictly
positive coefficients in `u`. Contracting each photon gives
`Pi'W_iA_3Pi=0`, so the effect descends before integration.

Reflection followed by outgoing-arm exchange is generated by

```text
J(u)=81/(50u), J(J(u))=u,
x(J(u))=y(u), rho(J(u))|J'(u)|=rho(u).          (30.12)
```

Its fixed point is `u_*=9sqrt(2)/10`; hence each side has exactly half the resolved
measure. Numerically the total per-unit-angular-acceptance mass is
`0.00033282609489790034` with error `8.01e-16`. The complete subset route—amplitude,
three projected Ward checks, and effect—takes `801` products versus `980` for
ordered histories. Isolated-process timings favor the subset route, but shared
symbolic caches can reverse them; product counts are the stable comparison.

Resolution is a physical boundary, not a removable placeholder. Exact endpoint
calculation gives

```text
lim_(x->0+) x^2 rho_x=1/(1024pi^3),
lim_(x->1/2-) (1-2x)^2 rho_x=1/(512pi^3).       (30.13)
```

The Born measure diverges when either soft boundary is restored. The compiler
refuses `delta=0`; node 31 consumes these residues to construct a leading detector-
bin transfer and to expose the remaining logarithmic obstruction.

## Retained interface and boundary

```text
CompileScalarComptonKinematics(mass, incoming energy, angle parameter)
 -> signed shell data + recoil map + positive phase density + certificates
 | refusal(unproved positive scales or an untyped parameter).

CompilePreparedEventMeasure(event-effect family, shell density, support)
 -> positive measure + aperture/total/conditional queries + errors
 | refusal(unavailable effect, invalid support, or unproved positivity).

CompileFermionComptonEffect(kinematics, parity resource)
 -> exterior amplitude + projected Ward residuals + positive effect + cost
 | refusal(characteristic internal line, unresolved odd trace, or failed positivity).

CompileResolvedThreePhotonSlice(parameter, resolution)
 -> shell-generated energies + exchange map + phase density + soft boundary
 | refusal(nonpositive or empty resolution window).

CompileFermionThreePhotonEvent(slice, budget, route)
 -> exterior amplitude + three Ward projections + effect + route-cost receipt
 | refusal(characteristic line, unresolved parity, gauge, positivity, or budget).
```

The node establishes bounded conditional event measures and a complete product-
count advantage on one resolved fermionic event. It constructs neither an absolute
cross section nor an infrared-inclusive event. Its evidence status is synthesized
in `../results/open-tree-compiler-v1-disposition.md`; node 31 owns the soft-channel
continuation.
