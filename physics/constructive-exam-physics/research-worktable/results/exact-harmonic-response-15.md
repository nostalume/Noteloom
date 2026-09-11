# Exact harmonic response from a phase-loss obstruction

## Question and spine position

Can an A617 problem outside the current grammar force a genuinely new semantic
request, rather than another pre-encoded adapter, and can the resulting operation
transfer unchanged across physics areas?

The weakest bridge after the common router was physical-request expansion. A21-03
requires a reflected wave's phase in order to recover its standing-wave pattern and
the signal at Q. A25-06 requires circuit lead/lag in order to return current and
power factor. A phase-free real relation cannot preserve either target.

## Source contract

- Source: `中国科学技术大学研究生入学考试习题汇编—普通物理A617.pdf`.
- SHA-256:
  `B84E9D24468628433D1A126771DC8DE5A9D3CA7C2DBD01A78597FDDF01C8D764`.
- Structure: 36 pages, unencrypted; author metadata `任 宇`, creation/modification
  date 2025-01-02.
- A25-06: PDF page 5, series `R=30 ohm`, `L=45 mH`, `C=35 microfarad`, source
  `200 cos(omega t) V`, `omega=100 rad/s`; asks for complex impedance, current,
  and power factor.
- A21-03: PDF page 12, incident wave traveling in `+x`, source at equilibrium and
  moving negative at `t=0`, denser reflecting boundary at `11 lambda/4`, equal
  incident/reflected amplitudes; asks for both waves, their sum, nodes, antinodes,
  and the Q-point signal at distance `3 lambda/4` from the boundary.
- Extraction: pypdf 6.17.0; visual validation: PyMuPDF 1.28.2 renders of both
  complete pages. The rendered equations and diagram agree with the extracted
  statements above.

The PDF supplies problem data, not an official answer. No expected source answer
enters either request or routing rule.

## Exact obstruction

The preceding rational-polynomial request was tried without changing its domain.
For A25-06 its law contains the imaginary unit in the impedance coefficient. For
A21-03 its fixed-boundary law contains complex exponentials. Both executions
return:

```text
A25-06-probe  refused  unsupported_relation_shape
A21-03-probe  refused  unsupported_relation_shape
```

Splitting real and imaginary parts manually would make a particular case
polynomial, but it would erase the invariant operation that both problems need:
complex-amplitude composition followed by magnitude, relative-phase, and real-time
return. The obstruction therefore forces a phase-preserving response object.

## Frozen contract `C-harmonic-v1`

### Admitted domain

- one human-validated set of time-independent harmonic laws;
- finitely many declared complex response unknowns;
- exact coefficients and parameters;
- laws linear in the declared response unknowns;
- convention `z -> Re(z exp(i omega t))` with explicitly real `omega` and `t`;
- named phasor observables and optional nonzero phase references;
- optional bounded real spatial interval whose exact node and stationary sets are
  finite and within a declared point budget.

### Generated output

```text
HarmonicResponse(laws, unknowns, observables, budget)
  -> unique exact phasor solution
  -> complex observable amplitudes
  -> squared magnitudes, real signals, relative-phase cosines
  -> exact law-residual, unknown-elimination, and real-return certificates
  -> typed obstruction otherwise
```

The spatial consumer acts only on a generated phasor:

```text
SpatialPattern(phasor(theta), [lower, upper], budget)
  -> solve |phasor|^2 = 0
  -> solve d|phasor|^2/dtheta = 0
  -> order exact stationary amplitudes
  -> finite nodes, global antinodes, maximum, certificates
```

### Falsifiers and refusals

The claim fails if a nonlinear law is silently linearized, a nonunique response is
selected, phase is removed before return, a failed certificate is marked
constructed, a nonfinite spatial set is enumerated as finite, or problem identity
selects the operator. Current typed boundaries include nonlinear, inconsistent,
underdetermined, unknown-budget, zero-reference, nonfinite-pattern,
point-budget, unordered-extrema, and recovery failures.

## A21-03 construction

Let `theta=kx`, `omega=2 pi nu`, and represent a real wave by
`Re(y_hat(theta) exp(i omega t))`. The source condition fixes the incident phasor:

```text
y_hat_i(theta) = i A exp(-i theta).
```

Write the unknown reflected amplitude as `B`, so
`y_hat_r(theta)=B exp(i theta)`. The denser boundary is a displacement node at
`theta_b=11 pi/2`; the constructor solves the supplied boundary law:

```text
0 = y_hat_i(theta_b) + y_hat_r(theta_b)
  = -A - i B
  -> B = i A.
```

Substitution constructs, rather than supplies, the total response:

```text
y_hat(theta)
  = i A exp(-i theta) + i A exp(i theta)
  = 2 i A cos(theta),

|y_hat(theta)|^2 = 4 A^2 cos^2(theta).
```

On `0 <= theta <= 11 pi/2`, exact zero and maximum construction gives:

```text
nodes     = (pi/2, 3pi/2, 5pi/2, 7pi/2, 9pi/2, 11pi/2),
antinodes = (0, pi, 2pi, 3pi, 4pi, 5pi).
```

Q is `3 lambda/4` left of the boundary, hence `x_Q=2 lambda` and
`theta_Q=4 pi`. Returning the generated phasor to a real signal gives:

```text
y_Q(t) = Re(2 i A exp(i omega t)) = -2 A sin(omega t).
```

The same total response satisfies the fixed-boundary node and the original
negative velocity at the origin.

## A25-06 transfer

Without changing the constructor, the circuit packet supplies the series harmonic
law `Z I_hat-U_hat=0`. Exact substitution of the source values gives:

```text
Z = R + i(omega L - 1/(omega C))
  = 30 - (3937/14)i ohm,

I_hat = 200/Z
      = 1176000/15676369 + (11023600/15676369)i ampere,

|I_hat|^2 = 7840000/15676369 ampere^2,
power factor = 420/sqrt(15676369).
```

The positive imaginary current component records that this capacitive circuit's
current leads the source. This is cross-area transfer from wave reflection to
circuit response under the unchanged finite linear phasor operation.

## Human-computation boundary

An atomic same-observable ledger compares the standard handwritten phasor route
with the literal compiler route. Both must select the same relation and perform the
same reactance, impedance, current, magnitude, and phase computations; the compiler
route additionally encodes a semantic request. The exact Pareto disposition is
`always_direct`. The constructor is therefore a review, verification, and transfer
tool on this case, not a faster handwritten solution.

## Evidence and disposition `V-harmonic-2026-09-06`

| Evidence ID | Operation | Permitted consequence |
| --- | --- | --- |
| E15-SOURCE | hash-bound extraction plus full-page visual checks | exact provenance for the two problem statements |
| E15-OBSTRUCTION | unchanged rational-polynomial probes refuse both laws | complex phase is outside the predecessor grammar |
| E15-RED | absent public request, spatial contract, source fixtures, router cards, CLI, and corpus promotions each fail before implementation | the new behaviors were not already present |
| E15-WAVE | exact A21 solve and spatial certificates | regression on the obstruction-generating waves case |
| E15-CIRCUIT | unchanged constructor on A25 plus exact recovery | bounded cross-area transfer |
| E15-REFUSAL | nonlinear, underdetermined, zero-reference, and nonfinite-pattern tests | typed negative-domain behavior |
| E15-USE | atomic A25 route comparison | correctness transfers; exam leverage is rejected on this card |
| E15-ROUTER | eleven-card common bench | `C-router-v2` admits harmonic response without weakening earlier results |
| E15-REGRESSION | complete pinned suite passes 104 tests | no detected predecessor-contract regression |

Under the unchanged decision kernel `K-router-v1`:

| Claim dimension | Disposition | Boundary |
| --- | --- | --- |
| exact finite linear harmonic construction | `D+ supported` | exact coefficients, supplied laws, unique finite response |
| spatial nodes and antinodes | `D+ supported-bounded` | finite orderable exact sets on one closed interval |
| waves-to-circuit transfer | `D+ supported-bounded` | A21-03 to A25-06 under unchanged construction |
| common-router grammar expansion | `D+ supported` | one new admitted request in `C-router-v2` |
| handwritten exam leverage | `D- rejected on A25-06` | standard phasor route strictly avoids request encoding |
| physical-law construction | `D? unresolved` | human still supplies the phasor and boundary/circuit laws |
| nonlinear, transient, distributed response | `D? outside contract` | no such solver or approximation is claimed |
| novelty and learner advantage | `D? unresolved` | no literature protocol or learner observations |

The implementation budget closes at 280 lines for `harmonic.py`, 185 for the
separate spatial consumer, 213 for source fixtures/commands, 161 for focused tests,
and 16 added router lines. No dependency was added.

## Re-entry and reproduction

Reopen `C-harmonic-v1` only if a source problem forces nonlinear harmonics,
transient initial-value response, a nonfinite periodic-set representation,
continuum boundary laws, or parameter-dependent extrema that cannot be ordered.
More finite phasor examples alone do not revise this disposition.

From `computation/` run:

```text
uv run python -m unittest tests.test_harmonic_response -v
uv run python -m worktable harmonic-transfer
uv run python -m worktable routing-benchmark
uv run python -m unittest discover -s tests -v
```
