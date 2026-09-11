# Operator cards

Each card has the same interface. `Trigger` diagnoses a visible obstruction;
`Preserve` prevents semantic loss; `Reduce` names the intended compression;
`Compute` is the handwritten operation; `Return` reconstructs the requested
observable; `Check` is a local certificate; `Refuse` bounds use; and `Gate` decides
whether the card should be used at all.

## Card 0: direct gate

- **Trigger:** the target is already reached by one short, familiar dependency
  chain with no unresolved branch or lost feature.
- **Preserve:** the original physical quantities, frame, sign, units, and regime.
- **Reduce:** remove only laws belonging to other targets or subparts.
- **Compute:** write the shortest competent physical-law chain and solve it.
- **Return:** answer in the form requested, not merely an intermediate invariant.
- **Check:** dimensions and one defining law or limiting case.
- **Refuse:** do not call an expression “direct” if it silently guesses a branch,
  path, phase, or constitutive regime.
- **Gate:** direct work is the default. Another card must repay its recognition,
  representation, and return cost.

## Card 1: target slice and elimination

- **Trigger:** the problem supplies several laws or subparts, but the target depends
  on only a connected subset; one or more hidden quantities lie between givens and
  target.
- **Preserve:** the meaning and domain of every retained law and the target's return
  conditions.
- **Reduce:** take the backward dependency slice of the target and eliminate hidden
  quantities one at a time.
- **Compute:** use explicit substitution when `h=f(g)` is available; otherwise form
  a weighted combination whose coefficients cancel a shared internal quantity.
- **Return:** a relation containing givens and the target, followed by physical
  branch selection.
- **Check:** substitute the result into every retained source law. A relation that
  does not lift to a physical state is not an answer.
- **Refuse:** if the slice has no path to a given, remains underdetermined, or needs
  a law not supplied by the model, state that obstruction.
- **Gate:** use the slice even when solving directly; use a formal elimination
  representation only when it removes more work than it adds.

### Worked source: A13-02 water jet

Let `w` be the jet speed at the supported cylinder and `H` its height. The two
target-connected laws are

```text
w^2 = v_0^2 - 2gH,
(2-alpha) rho A v_0 w = Mg.
```

The second law explicitly gives

```text
w = Mg / [(2-alpha) rho A v_0].
```

Substitution into the first gives

```text
H = {v_0^2 - [Mg/((2-alpha)rho A v_0)]^2}/(2g).
```

Return requires `w>=0` and `H>=0`. This is the only case in the locked six-problem
bench with a conditional structural admission boundary; the relation representation
is preferable only when its setup costs less than the hidden-quantity and symbolic
work it removes.

## Card 2: event and restriction

- **Trigger:** words such as *first meets*, *just loses contact*, *becomes
  horizontal*, *turns*, or *reaches* define a state by an event.
- **Preserve:** the evolving state, event orientation, reachable interval, and any
  initial or boundary condition.
- **Reduce:** express the event as a zero condition in one convenient coordinate.
- **Compute:** write `VANISH`, transport that condition through the evolution law or
  invariant, then solve the resulting finite relation.
- **Return:** reconstruct every candidate in the full state and restrict it to the
  actually traversed interval.
- **Check:** substitute the surviving state into both the event predicate and all
  evolution laws.
- **Refuse:** two surviving states mean genuine ambiguity; no surviving state means
  the requested event is not reached under the stated motion.
- **Gate:** on a familiar one-off problem, write the event equations directly. The
  general event packet is chiefly a review and verification tool.

### Worked source: A15-01

With `c=cos(phi)`, `s=v^2/(gl)`, and downward `a=a_y/g`, use

```text
VANISH:    a=0,
TRANSPORT: s=2(c-1/10),
           a=1-c^2-sc,
RESTRICT:  1/10 <= c <= 1.
```

Eliminating `a,s` gives

```text
15c^2-c-5=0.
```

Only `c=(1+sqrt(301))/30` lies in the released interval, so the requested angle is
`phi=arccos((1+sqrt(301))/30)`.

## Card 3: bounded projection

- **Trigger:** an unconstrained equality law may carry a state past a physical
  bound, producing reversal, negative capacity, or another inadmissible result.
- **Preserve:** the admissible interval, impulse/flux orientation, constitutive
  regime, and complementarity between saturated and unsaturated behavior.
- **Reduce:** compute the unconstrained desired correction, then project it onto the
  admissible interval.
- **Compute:** for a nonrotating point particle striking a rough fixed wall,

```text
J_n=m(1+e)u_n,
J_t*= -m u_t,
J_t=projection of J_t* onto [-mu J_n,mu J_n].
```

- **Return:** `u_n'=e u_n`, `u_t'=u_t+J_t/m`, followed by speed and reflection
  angle.
- **Check:** the impulse lies inside the Coulomb interval, opposes slip, and cannot
  reverse tangent motion under the maximum-dissipation contract.
- **Refuse:** rotating bodies, compliant contact, several simultaneous contacts, or
  a different friction law need a richer model.
- **Gate:** the projection is a compact branch/error check. In A15-02 its full
  notation adds a representation action, so direct component work remains cheaper.

The two branches are

```text
u_t <= mu(1+e)u_n:  u_t'=0,
u_t >  mu(1+e)u_n:  u_t'=u_t-mu(1+e)u_n.
```

## Card 4: path functional

- **Trigger:** a requested work or voltage is assigned to endpoints even though the
  field may be nonconservative.
- **Preserve:** path orientation, material path, endpoints, curl/flux law, and the
  distinction between open-wire work and a path-free scalar potential.
- **Reduce:** replace ambiguous endpoint notation by the oriented functional
  `W[gamma]=integral_gamma E dot dl`.
- **Compute:** evaluate one convenient path directly; compare a second path through
  the closed loop. For constant planar curl,

```text
W[gamma_1]-W[gamma_2]
  = curl(E) * (signed area_1-signed area_2).
```

- **Return:** for an open wire, return its path-dependent terminal voltage; for a
  two-path circuit, combine `U=W_j-I_jR_j` with current conservation.
- **Check:** reversing a path reverses work but not length. A verified scalar
  potential must recover path independence in the conservative limit.
- **Refuse:** without a material/probe path or a scalar-potential certificate, do
  not invent an endpoint voltage.
- **Gate:** use the loop relation when it replaces an awkward integral. If symmetry
  or Faraday's law already gives the requested result in one step, stay direct.

### Small transfer computation

For `E=(-y/2,x/2)`, the curl is `1`. From `(0,0)` to `(1,1)`, the straight line has
zero work. The broken path along the `x` axis and then vertically at `x=1` has work
`1/2`. Their difference is exactly the signed area contribution; endpoint notation
alone would lose it.

## Card 5: harmonic response

- **Trigger:** the target asks for interference, lead/lag, power factor, nodes, or a
  signal at a specified point and magnitude-only variables would discard phase.
- **Preserve:** one declared real-signal convention, frequency sign, boundary data,
  and relative phase.
- **Reduce:** encode a steady sinusoid by one complex amplitude.
- **Compute:** under `x(t)=Re(z exp(i omega t))`, replace derivatives by `i omega`
  and propagation by `exp(+ikx)` or `exp(-ikx)`, then solve the finite linear laws
  once.
- **Return:** if `z=a+ib`, then `x(t)=a cos(omega t)-b sin(omega t)`.
- **Check:** reconstruct the original linear laws and use `z conjugate(z)` for
  magnitude squared.
- **Refuse:** transients, nonlinear response, nonfinite spatial extrema, or missing
  boundary laws lie outside this card.
- **Gate:** use the standard direct phasor solution when it is already one line.
  The card earns its place when it prevents phase loss or reuses one solve for
  several observables.

### Small transfer computation

For a series response with `Z=3+4i` and real voltage phasor `5`,

```text
I=5/(3+4i)=3/5-4i/5,
|I|=1,
i(t)=(3/5)cos(omega t)+(4/5)sin(omega t).
```

## Card 6: harmonic product

- **Trigger:** the target is a mean, power, torque, intensity, correlation, or full
  product of two same-frequency real signals.
- **Preserve:** both complex phases, the common positive frequency, and the real
  physical scale and sign convention.
- **Reduce:** split the product into a constant channel and a twice-frequency
  channel.
- **Compute:** for `x=Re(a exp(i omega t))` and
  `y=Re(b exp(i omega t))`,

```text
mean(xy) = Re(a conjugate(b))/2,
2 omega phasor = ab/2.
```

- **Return:** multiply both channels by the real physical scale and reconstruct only
  the signal components the target asks for.
- **Check:** direct multiplication must reproduce the same real signal. The
  conjugate occurs in the mean channel, not the ripple channel.
- **Refuse:** different frequencies, time-dependent phasors, higher products, or
  complex physical scales require another construction.
- **Gate:** use the mean identity alone when only average power is requested; retain
  the second channel only when ripple or instantaneous behavior matters.

For `x=2cos(omega t)` and `y=3sin(omega t)`, take `a=2`, `b=-3i`. The mean is zero
and the `2 omega` phasor is `-3i`, returning `xy=3sin(2omega t)`.

## Card 7: symmetry-compatible coordinates

- **Trigger:** component coordinates greatly outnumber the instantaneous degrees of
  freedom because constraints and symmetry tie them together.
- **Preserve:** the constraint tangent space, mass/kinetic metric, applied impulse
  direction, and quantities broken by the loading.
- **Reduce:** parameterize only symmetry-compatible velocities or generalized
  coordinates before forming momentum or energy.
- **Compute:** substitute the reduced velocities into kinetic energy, then obtain
  generalized momentum by differentiation.
- **Return:** reconstruct the original components and verify every constraint.
- **Check:** relative velocity along each rigid link vanishes; discarded modes are
  not excited by the imposed symmetry and impulse.
- **Refuse:** asymmetric geometry, loading, mass distribution, or an unverified
  reduction requires returning to the full constraint system.
- **Gate:** use only when the reduced coordinates can be recognized and written
  more cheaply than the component constraints.

For the developed hinged-hexagon example,

```text
T(u,v)=m(5u^2-uv+5v^2)/3,
p_v=partial T/partial v=m(-u+10v)/3=0,
v=u/10.
```

This card is a promising compression pattern, but unlike the path and harmonic
cards it does not yet have a frozen cross-area transfer bench in the worktable.

## Candidate card 8: dimensional quotient

This card is not part of the frozen `C-review-v1` learner instrument. N1 execution
and N2 adaptive admission use their own separately frozen projections of it.

- **Trigger:** several dimensional quantities describe one target, and changing
  base measurement units should not change the physical regime or relation shape.
- **Preserve:** physical quantity meanings, the declared base dimensions, target,
  regime, and every supplied dynamical or constitutive law.
- **Reduce:** place quantity-dimension vectors in columns of `D`; construct exponent
  vectors `a` satisfying `D a=0`.
- **Compute:** convert a rational nullspace basis to primitive integer exponents and
  write `Pi=product_i x_i^a_i`.
- **Return:** interpret each `Pi` as a comparison, regime coordinate, or normalized
  target; use supplied physics to determine its value or relation.
- **Check:** add the exponent-weighted dimensions and obtain zero; substitute a
  known physical law when one is available.
- **Refuse:** no nullspace means no nonconstant group. Missing base dimensions,
  affine units, an excessive group count, or a request to infer dynamics from units
  lies outside the card.
- **Gate:** use it when it reduces parameters, exposes a scaling law, or checks a
  proposed formula. Stay direct when the governing law already gives the target in
  one short step.

Three unchanged constructions are:

```text
pendulum: T^2 g/L       -> 4 pi^2 after the pendulum law is supplied
fluid:    rho v L/mu    -> Reynolds regime coordinate
circuit:  t/(RC)        -> 1 at one supplied RC time constant
```

Dimensions generate these coordinates but not their dynamics, constants, or
empirical transition thresholds.

## Candidate card 9: boundary-network condensation

This card is not part of the frozen `C-review-v1` learner instrument.

- **Trigger:** the target concerns terminal or boundary variables, while a supplied
  finite linear balance contains internal junction states.
- **Preserve:** area law, boundary orientation, state meanings, sources,
  coefficient units, approximation regime, and the boundary/internal partition.
- **Reduce:** reorder `Kx=f` into boundary and internal blocks. If `K_II` is
  invertible, form `K_eff=K_BB-K_BI K_II^-1 K_IB` and
  `f_eff=f_B-K_BI K_II^-1 f_I`.
- **Compute:** solve only `K_eff u=f_eff` for the requested boundary observable.
- **Return:** recover hidden states with
  `h=-K_II^-1 K_IB u+K_II^-1 f_I` when the problem asks for them.
- **Check:** substitute the recovery map into both original block equations;
  inspect sign/orientation and one limiting case.
- **Refuse:** a singular or unproved-invertible hidden block, nonlinear elements,
  unknown topology, or an unjustified steady/massless approximation needs a richer
  physical construction.
- **Gate:** for one obvious series pair, write the recognized equivalent law
  directly. Use block condensation when several hidden states would otherwise stay
  live or when internal sources must be returned correctly.

For a two-edge chain with coefficients `c_1,c_2`,

```text
c_eff = c_1 c_2/(c_1+c_2),
x_h = (c_1 x_L+c_2 x_R+f_h)/(c_1+c_2).
```

The algebra is shared; voltage, displacement, or temperature and the meaning of
the source come back only through the area-specific ledger.

### Sparse execution strip

Do not expand the block inverse by hand. For each hidden node whose diagonal pivot
is known nonzero:

1. Count its current neighbors and the absent neighbor-to-neighbor links that its
   removal would create.
2. Remove the node with the fewest new links; use neighbor count and the written
   variable order only as tie-breakers.
3. Update only its neighbor block and retain its one-line recovery equation.
4. Continue until only boundary variables remain; recover hidden values in reverse
   order only if the target requires them.

On the frozen two-leaf branch, center-first elimination creates six links and 19
nonzero coefficient updates. Leaf-first elimination creates one link and five
updates. Both return the same boundary law. These counts justify a candidate route,
not a learner-speed claim; a visually obvious series/parallel reduction remains the
direct gate.

The full handwritten-ledger gate for this fixture is

```text
use sparse only if
3*(cost of a pivot-recognition step)
  < 14*(cost of a symbolic update).
```

The coefficients are constructed; the human costs are not. With one hidden node,
both orders do the same algebra and the sparse scan is pure overhead, so stay
direct. Do not memorize `leaf first` as an unconditional rule: recompute current
fill, and use the card only after its recognition debt is justified.
The drop in active-neighbor width is a useful memory hypothesis, but it is not the
same as fewer simultaneously live equations and is not counted in this inequality.

### Adaptive admission strip

Before solving, return exactly one status:

```text
reciprocity or provable scalar pivot fails -> refuse this strip
same elimination work plus scan overhead   -> direct_gate
fewer updates plus scan overhead           -> conditional_candidate
```

For a conditional candidate, retain the generated cost inequality; do not shorten
the status to “use sparse.” There is no `always_sparse` response while human action
weights remain unknown. `Refuse` rejects this scalar representation, not the
physical problem or every possible solver.
