# Frictional impact as a constrained impulse projection

## Question and spine position

Does the first post-composition corpus expansion require a larger workflow engine,
or does a source problem force a new specialist mathematical object?

A15-02 supplies the discriminator. It asks for the reflected speed and angle of a
small particle striking a rough wall with known friction and restitution
coefficients. Restitution determines the normal impulse, but writing the kinetic
friction equality blindly can reverse the tangential velocity during an
instantaneous impact. The missing object is an impulse constrained by the Coulomb
interval, not a third generic pipeline stage.

## Frozen source contract

- Source: `中国科学技术大学研究生入学考试习题汇编—普通物理A617.pdf`.
- SHA-256:
  `B84E9D24468628433D1A126771DC8DE5A9D3CA7C2DBD01A78597FDDF01C8D764`.
- A15-02: PDF page 25 (printed 2015 page 22), a particle of mass `m` strikes a
  vertical rough wall with speed `v_1` and incidence angle `theta`; friction
  coefficient `mu` and restitution coefficient `e` are given; reflected speed
  `v_1'` and reflection angle `theta'` are requested.
- Extraction: pypdf was used on the unencrypted 36-page source. Page 25 was
  rendered at 2x with PyMuPDF and visually checked for the wall-normal direction,
  incident/reflected quadrants, and angle convention.

The executable packet uses the conventional nonrotating point-particle reading of
“small ball.” Newton normal restitution and maximum-dissipation Coulomb impulse
are explicit theorem/model contracts. A finite rotating sphere, compliant contact,
or a prescribed tangential restitution law would be a different problem.

## Obstruction and internal construction

Let `u_n>0` be the incoming speed toward the wall and `u_t>=0` the tangential
speed. Take positive normal direction away from the wall. Newton restitution gives

```text
u_n' = e u_n,
J_n = m(u_n' + u_n) = m(1+e)u_n.
```

The impulse that would stop tangential slip is

```text
J_t* = -m u_t.
```

Coulomb friction admits only

```text
-mu J_n <= J_t <= mu J_n.
```

The maximum-dissipation impulse is therefore constructed, rather than guessed, by
projecting `J_t*` onto this interval:

```text
J_t = proj_{[-mu J_n, mu J_n]}(-m u_t)
    = -min(m u_t, mu J_n).
```

This one operation generates both physical regimes:

```text
sticking/tangential arrest:
  u_t <= mu(1+e)u_n,
  J_t = -m u_t,
  u_t' = 0;

sliding:
  u_t > mu(1+e)u_n,
  J_t = -mu J_n,
  u_t' = u_t-mu(1+e)u_n.
```

Equivalently, the branch-free scalar return is

```text
u_t' = max[u_t-mu(1+e)u_n, 0].
```

The `max` is not a silent case choice. The result retains the two named branches,
their exact conditions, impulses, and outputs as well as the piecewise return.

## A15-02 return

The source geometry supplies

```text
u_n = v_1 cos(theta),
u_t = v_1 sin(theta),
0 <= theta < pi/2.
```

The regime boundary becomes

```text
tan(theta) <= mu(1+e)       tangential arrest,
tan(theta) >  mu(1+e)       sliding.
```

For tangential arrest:

```text
v_1' = e v_1 cos(theta),
theta' = 0.
```

For sliding:

```text
v_1' = v_1 sqrt(
          e^2 cos^2(theta)
          + [sin(theta)-mu(1+e)cos(theta)]^2
       ),

tan(theta') = [tan(theta)-mu(1+e)]/e.
```

At `mu=0`, the constructor recovers unchanged tangential speed and ordinary
normal restitution. At the regime boundary the two returns agree continuously.
The result answers the requested speed and angle without choosing a regime that the
symbolic givens do not determine.

## Frozen contract `C-impact-v1`

### Admitted input

- exact positive mass and incoming normal speed;
- exact nonnegative incoming tangential speed and friction coefficient;
- exact positive restitution coefficient;
- nonrotating point-particle impact with one fixed planar wall;
- Newton normal restitution plus maximum-dissipation Coulomb impulse.

### Generated output

- exact normal impulse and friction-impulse limit;
- named tangential-arrest and sliding regimes with complementary conditions;
- exact regime impulses, outgoing components, speed, and reflection-angle tangent;
- a piecewise common return and a selected regime when exact numeric data decide
  the inequality;
- normal/tangential momentum, Coulomb saturation, and speed-recovery certificates.

Zero normal incidence, negative speeds or coefficients, and zero restitution are
rejected at typed admission. Rotation, finite contact duration, deformation,
adhesion, multiple simultaneous contacts, 3D tangent cones, and restitution above
the stated source model remain outside the contract.

## Router and composition relation

`C-router-v3` adds `FrictionalImpactRequest` as a seventh semantic request family.
The twelve-card frozen router now returns ten certified constructions, one
ambiguity, and one unsupported-backend refusal. Selection depends on the admitted
request type, never on `A15-02` or an expected formula.

The Result 17 composition contract is unchanged. The impact constructor owns its
internal regime split because the alternatives share one physical impulse law and
one returned observable. Encoding the split as arbitrary workflow branching would
separate the inequality from the law that generates it and add no reusable
capability.

## Human-computation disposition

The useful exam card is compact:

```text
resolve u_n,u_t
J_n=m(1+e)u_n
J_t=proj_{[-mu J_n, mu J_n]}(-m u_t)
return u_n'=e u_n, u_t'=u_t+J_t/m
```

It prevents the common overshoot error and displays the branch boundary before
algebraic expansion. However, a competent direct component solution uses the same
three physical relations, branch check, and final reconstruction. The atomic route
audit adds one representation action for the projection card and therefore returns
`always_direct`. This is a review and exact-checking tool, not positive evidence of
exam-time savings.

## Evidence and disposition `V-impact-2026-09-06`

| Evidence ID | Operation | Permitted consequence |
| --- | --- | --- |
| E18-SOURCE | hash check, text extraction, and 2x visual inspection of page 25 | exact statement and angle provenance |
| E18-OBSTRUCTION | saturated friction equality can overshoot zero tangent speed | a bounded impulse rather than one unconditional equality is required |
| E18-RED-CORE | public impact request/constructor import failed before implementation | the specialist operation was absent |
| E18-RED-INTEGRATION | corpus, router, and CLI expectations failed before their production changes | the new execution was not already claimed |
| E18-LAW | symbolic projection returns complementary regimes and five exact certificates | the bounded impulse construction is supported |
| E18-NUMERIC | exact sticking and sliding fixtures select their correct regimes | inequality selection is executable |
| E18-LIMIT | `mu=0` preserves tangential speed | smooth-wall regression is recovered |
| E18-A15 | component-to-angle adapter returns both requested source observables | A15-02 is a full execution under the stated contracts |
| E18-USE | atomic same-observable route comparison | handwritten advantage is rejected on this source card |

| Claim dimension | Disposition | Boundary |
| --- | --- | --- |
| planar point-particle impulse projection | `D+ supported-bounded` | exact scalar normal/tangent speeds and frozen impact laws |
| A15-02 speed and angle | `D+ supported` | both parameter regimes retained |
| automatic regime selection | `D+ supported when decidable` | symbolic inequalities remain explicit branches |
| rotating rigid-body or multi-contact impact | `D? outside contract` | inertia, spin, contact coupling, and cone geometry are absent |
| general workflow branching | `D- unnecessary here` | the branch is internal to one generated physical result |
| handwritten exam leverage | `D- rejected on A15-02` | projection adds one representation action |
| learner error reduction | `D? unresolved` | no empirical observations exist |

Corpus evidence becomes 25 full, 3 partial, 2 shape-only, 18 unexecuted
candidates, 74 outside the grammar, and 4 qualitative problems.

## Re-entry and reproduction

Reopen the impact contract only when a source requires rotation, coupled normal and
tangent restitution, several contacts, compliant contact time, or a higher-
dimensional friction cone. More point particles against fixed planar walls can test
robustness but cannot expand this disposition.

From `computation/` run:

```text
uv run python -m unittest tests.test_impact_projection -v
uv run python -m worktable impact-transfer
uv run python -m worktable routing-benchmark
uv run python -m unittest discover -s tests -v
```
