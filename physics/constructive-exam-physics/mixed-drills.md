# Mixed route-selection and computation drills

These are authored review exercises, not new A617 source evidence. Work without the
operator-card headings. For every item, first write

```text
TARGET | shortest direct slice | obstruction | route
```

Allowed route labels are `direct`, `slice/eliminate`, `event`, `projection`,
`path`, `harmonic`, `product`, `symmetry`, and `refuse-card`.

## Part A: choose the route before calculating

1. A mass is dropped from rest through a known height. Find its speed immediately
   before impact, neglecting drag.

2. A multi-part circuit question supplies enough data for resistance, current,
   magnetic field, and heating. This subpart asks only for Joule heat in one known
   resistor during a known interval.

3. A pendulum question asks for the first instant at which its string tension
   vanishes.

4. A point particle strikes a rough fixed wall. Applying the saturated friction
   impulse would reverse its tangential velocity during the instantaneous impact.

5. Two wires connect the same endpoints through a time-varying magnetic-flux
   region. The question asks for the difference between their open-wire voltages.

6. A series RLC circuit in steady sinusoidal operation asks for current magnitude,
   lead/lag, and the real current signal.

7. A rotating coil asks only for the cycle-averaged mechanical torque, given the
   current and orientation phasors.

8. A uniform sphere with spin strikes a rough wall. The point-particle impact card
   is available.

9. A driven oscillator asks for the full transient response immediately after
   switching, but only a steady-state phasor law has been supplied.

10. A conservative electrostatic field with a verified scalar potential asks for
    the voltage between two points.

11. A symmetric linkage has twelve vertex-velocity components but only two
    symmetry-compatible instantaneous degrees of freedom under the stated impulse.

12. A vertical water jet supports a body. Its target height depends on one hidden
    impact speed through momentum flux and ballistic deceleration.

## Part B: execute the selected operator

### B1. Eliminate one hidden speed

A vertical jet leaves an opening at `v_0=10 m/s`. Its mass flux is
`rho A v_0=10 kg/s`. Half the incident water sticks and half rebounds downward at
the impact speed `w`. It supports a `9 kg` body; take `g=10 m/s^2`. Find `w` and
the stationary height `H`, using

```text
(2-alpha)rho A v_0 w=Mg,
w^2=v_0^2-2gH,
alpha=1/2.
```

### B2. Project a friction impulse

A nonrotating point particle reaches a fixed wall with normal speed magnitude
`u_n=4 m/s` and tangential speed `u_t=3 m/s`. Let restitution `e=1/2` and friction
coefficient `mu=1/4`. Determine the impact regime, outgoing components, speed, and
the tangent of the reflection angle measured from the wall normal.

### B3. Preserve path dependence

For the planar field

```text
E(x,y)=(-y/2,x/2),
```

compare the oriented work from `(0,0)` to `(1,1)` along:

- the straight segment `gamma_s(t)=(t,t)`;
- the broken path that goes along the `x` axis to `(1,0)` and then vertically to
  `(1,1)`.

Explain why an endpoint-only voltage is not defined by this field.

### B4. Preserve harmonic phase

A steady series response has impedance `Z=3+4i` and real voltage phasor `U=5` under
the convention `i(t)=Re(I exp(i omega t))`. Find `I`, its magnitude, whether the
current leads or lags the voltage, and the real signal.

### B5. Split a harmonic product

Let

```text
x(t)=2cos(omega t),
y(t)=3sin(omega t).
```

Find the mean and the complete twice-frequency channel using complex amplitudes,
then verify by a direct trigonometric identity.

### B6. Restrict an event branch

Let `c=cos(phi)`, with physical motion restricted to `1/10<=c<=1`. The transported
event laws reduce to

```text
15c^2-c-5=0.
```

Construct both algebraic roots, select the physical one, and state what additional
conclusion would be required if both roots lay inside the interval.

### B7. Use symmetry-compatible momentum

A constraint reduction has already been verified and gives

```text
T(u,v)=m(5u^2-uv+5v^2)/3.
```

An impulse excites the `u` coordinate but supplies no generalized impulse in the
`v` direction. Find `v/u`. State the reconstruction check still required before
accepting the reduced answer.

## Part C: transfer and refusal prompts

For each prompt, name the preserved structure and the boundary that prevents an
overgeneralization.

1. Transfer the path card from induced electric work to mechanical work by a
   nonconservative planar force field.
2. Transfer the harmonic-response card from an RLC circuit to reflected waves at a
   fixed boundary.
3. Transfer the harmonic-product card from electrical power to maintaining torque
   of a rotating coil.
4. Explain why the impact projection does not transfer unchanged from a point
   particle to a spinning sphere.
5. Explain why a finite steady-state phasor solve does not return a switching
   transient.
6. Explain why an algebraically closed target relation may still fail the physical
   return step.
