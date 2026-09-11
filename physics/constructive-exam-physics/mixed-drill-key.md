# Mixed-drill route and answer key

Check the route decision before comparing algebra. A different correct derivation
is acceptable; the framework is not a required notation.

## Part A

1. **Direct.** Energy or constant-acceleration kinematics is already a short law
   chain; another representation adds setup.
2. **Slice/eliminate.** Retain only the resistor power law and the time relation.
   Laws used solely for magnetic-field targets are outside this backward slice.
3. **Event.** The trigger is the vanishing tension. Transport `T=0` through radial
   dynamics and energy, then restrict to the actually traversed arc.
4. **Projection.** Saturated friction overshoots zero tangent speed, so project the
   desired arrest impulse onto the Coulomb interval.
5. **Path.** The material routes differ and the field is induced/nonconservative;
   compare their closed loop or flux rather than assigning one endpoint scalar.
6. **Harmonic.** Magnitude, lead/lag, and real signal require the complex phase.
7. **Product.** Only the mean channel is requested, so use
   `Re(a conjugate(b))/2` and omit the ripple calculation.
8. **Refuse-card.** Spin couples tangential impulse to angular velocity; the
   nonrotating point-particle return is not preserved.
9. **Refuse-card.** A steady phasor omits initial data and homogeneous transient
   modes. A time-domain construction is required.
10. **Direct.** The verified scalar potential makes the endpoint voltage
    well-defined; a path-functional calculation is unnecessary.
11. **Symmetry**, conditionally. Use the two reduced coordinates only after checking
    that geometry, mass distribution, constraints, and loading preserve the stated
    symmetry.
12. **Slice/eliminate**, conditionally. Eliminate the impact speed between momentum
    flux and ballistic descent. The locked cost boundary does not guarantee this is
    faster for every learner.

## Part B

### B1

Here `(2-alpha)rho A v_0=(3/2)(10)=15 kg/s`, so force balance gives

```text
w=Mg/15=90/15=6 m/s.
```

Ballistic return gives

```text
H=(v_0^2-w^2)/(2g)=(100-36)/20=16/5 m.
```

Both `w` and `H` are nonnegative, so the supplied regime is consistent.

### B2

Per unit mass, the normal impulse magnitude is

```text
J_n/m=(1+e)u_n=(3/2)4=6 m/s.
```

The friction capacity is `mu J_n/m=3/2 m/s`, smaller than the desired arrest
change `u_t=3 m/s`. Therefore the particle remains in the sliding branch:

```text
u_n'=e u_n=2 m/s,
u_t'=3-3/2=3/2 m/s,
v'=sqrt(2^2+(3/2)^2)=5/2 m/s,
tan(theta')=u_t'/u_n'=3/4.
```

### B3

For the straight segment, `d gamma_s=(1,1)dt` and

```text
E(gamma_s) dot d gamma_s=(-t/2,t/2) dot (1,1)dt=0,
```

so `W_s=0`. Along the horizontal part of the broken path the work is zero. Along
the vertical part, `x=1`, `dl=(0,dy)`, and

```text
E dot dl=(1/2)dy,
```

so `W_b=1/2`. Also `curl(E)=1`, and the work difference equals the oriented area
between the paths. Equal endpoints with unequal work rule out an endpoint-only
scalar potential on this region.

### B4

```text
I=U/Z=5/(3+4i)=3/5-4i/5,
|I|=1.
```

Its phase is negative relative to the real voltage, so current lags. Returning to
the real signal,

```text
i(t)=(3/5)cos(omega t)+(4/5)sin(omega t).
```

### B5

Use `a=2` and `b=-3i`. Then

```text
mean = Re(a conjugate(b))/2 = Re(6i)/2 = 0,
2 omega phasor = ab/2 = -3i.
```

Therefore

```text
x(t)y(t)=Re(-3i exp(2i omega t))=3sin(2omega t).
```

This matches `6cos(omega t)sin(omega t)=3sin(2omega t)`.

### B6

The algebraic roots are

```text
c=(1+sqrt(301))/30,
c=(1-sqrt(301))/30.
```

Only the positive root lies in `[1/10,1]`, so

```text
phi=arccos((1+sqrt(301))/30).
```

If both full-state roots survived the physical interval and source-law checks, the
problem would remain ambiguous until another physical condition selected the
requested event, such as first occurrence or direction of traversal.

### B7

No generalized impulse in the `v` direction gives

```text
p_v=partial T/partial v=m(-u+10v)/3=0,
```

so `v/u=1/10`. Acceptance still requires reconstructing all original component
velocities and verifying every rigid-link velocity constraint. The reduced kinetic
energy alone does not certify that reconstruction.

## Part C

1. **Path transfer:** preserve oriented line work and the curl/closed-loop witness.
   Refuse endpoint-only work when no scalar potential exists.
2. **Harmonic transfer:** preserve one complex-amplitude convention, boundary laws,
   and relative phase. Refuse nonlinear, transient, or incomplete-boundary models.
3. **Product transfer:** preserve two same-frequency phasors and the real physical
   scale. The mean uses a conjugate; the twice-frequency channel does not.
4. **Impact refusal:** rotational inertia and contact-point velocity introduce an
   angular state absent from the point-particle card.
5. **Transient refusal:** phasors encode a particular steady response, not the
   initial-data-dependent homogeneous solution.
6. **Return refusal:** elimination may retain an algebraic candidate that violates
   dimensions, sign, parameter regime, interval, or an original source law. A full
   lift check is therefore part of the answer contract.
