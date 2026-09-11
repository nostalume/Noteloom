# Harmonic-product return from a multiplicative-observable obstruction

## Question and spine position

Can the phase-preserving response of Result 15 compute an instantaneous physical
observable that is a product of two harmonics, or does that downstream return
force a new reusable operation?

A23-05 already exposed the obstruction: its current is a one-frequency response,
but the requested maintaining torque is current multiplied by the sinusoidal
orientation factor. A one-frequency phasor result cannot itself represent the
resulting mean plus twice-frequency ripple. This is downstream use evidence, not
another example of the same linear solve.

## Frozen source contract

- Source: `中国科学技术大学研究生入学考试习题汇编—普通物理A617.pdf`.
- SHA-256:
  `B84E9D24468628433D1A126771DC8DE5A9D3CA7C2DBD01A78597FDDF01C8D764`.
- Structure: 36 pages, unencrypted, 595.32 by 841.92 points.
- A23-05: PDF page 9 (printed 2023 page 6), square coil of side `a` and
  `N` turns rotating at `omega` in uniform `B`, with resistance `R` and
  self-inductance `L`; asks for emf, steady current, and maintaining torque.
- A11-06: PDF page 34 (printed 2011 page 31), a small coil of radius `a` and
  resistance `R` rotating inside a fixed much larger coil `b >> a` carrying
  constant current `I`; self-inductance is neglected; asks for induced current
  and maintaining torque.
- Extraction: pypdf 6.17.0. Both complete pages were rendered at 2x with
  PyMuPDF 1.28.2 and visually checked, including the rotation axes and diagrams.

The compilation supplies problem statements, not official answers. The field at
the centre of a circular loop and the uniform-field approximation for `b >> a`
are explicit theorem/regime contracts in the A11 construction.

## Exact obstruction

Result 15 returns a complex amplitude `a` and the real signal

```text
x(t) = Re(a exp(i omega t)).
```

Torque requires the product of this signal with a second harmonic factor. Keeping
only a magnitude loses the relative phase and therefore changes both the mean and
the ripple. Keeping only the original phasor has the opposite problem: a linear
one-frequency representation is not closed under multiplication.

The smallest closed return follows by multiplying the real-signal forms:

```text
Re(a exp(i omega t)) Re(b exp(i omega t))
  = (1/2) Re(a conjugate(b))
    + Re((ab/2) exp(2 i omega t)).
```

The product constructs two channels: a real DC component and a complex
second-harmonic phasor. No trigonometric case expansion is part of the public
contract.

## Frozen contract `C-harmonic-product-v1`

### Admitted input

- two exact, time-independent phasors under the same
  `Re(z exp(i omega t))` convention;
- one explicitly positive real angular frequency and real time coordinate;
- an explicitly real, time-independent physical scale;
- a problem identity and product-observable name.

### Generated output

```text
HarmonicProduct(a, b, omega, scale)
  -> dc = scale * Re(a conjugate(b)) / 2
  -> second = scale * a b / 2 at frequency 2 omega
  -> real time signal
  -> exact direct-product recovery and reality certificates
```

Time-dependent inputs, non-real scales, and zero or sign-undetermined frequencies
are rejected at admission. A failed exact reconstruction returns
`harmonic_product_recovery_failed`. Different-frequency mixing, products of three
or more factors, stochastic spectra, and nonlinear response generation are outside
this contract.

The product owner is separate from `harmonic.py`: the linear response constructs
phasors, while the new operation consumes them. This preserves a visible pipeline
and avoids turning the response solver into a domain-specific torque routine.

## A23-05 construction

Let

```text
K = N B a^2,
Phi_ext = K cos(omega t),
emf = -d Phi_ext/dt = K omega sin(omega t).
```

Under the fixed convention, `emf_hat=-i K omega`. The unchanged response solver
constructs

```text
(R + i omega L) I_hat = -i K omega,

I_hat = -K omega(omega L + iR)/(R^2 + omega^2 L^2),

i(t) = K omega[R sin(omega t) - omega L cos(omega t)]
       /(R^2 + omega^2 L^2).
```

With positive applied torque defined along the imposed rotation direction, the
magnetic torque opposes the motion and

```text
tau_applied(t) = K i(t) sin(omega t).
```

The product constructor consumes `I_hat` and the sine phasor `-i` and returns

```text
<tau_applied>
  = K^2 omega R / [2(R^2 + omega^2 L^2)],

tau_hat_2omega
  = K^2 omega(-R + i omega L) / [2(R^2 + omega^2 L^2)].
```

Consequently

```text
tau_applied(t)
  = K^2 omega R[1-cos(2 omega t)]/[2D]
    - K^2 omega^2 L sin(2 omega t)/[2D],

D = R^2 + omega^2 L^2.
```

An independent energy-return check passes exactly:

```text
omega <tau_applied> - (R/2)|I_hat|^2 = 0.
```

This check fixes the torque sign and relates mechanical input power to average
resistive loss; average inductive power is zero in the steady state.

## A11-06 unchanged transfer

For `b >> a`, the supplied large-loop theorem and uniform-field approximation give

```text
B_center = mu_0 I/(2b),
K = B_center pi a^2.
```

Setting `L=0` in the same response-product pipeline yields

```text
i(t) = (K omega/R) sin(omega t),

<tau_applied> = K^2 omega/(2R),

tau_hat_2omega = -K^2 omega/(2R),

tau_applied(t) = K^2 omega[1-cos(2 omega t)]/(2R).
```

The product operation and its certificates are unchanged. This is a second
source-bound electromagnetic transfer across inductive and noninductive response;
it is not evidence of cross-area or universal transfer.

## Human-computation and router boundaries

The human card is compact:

```text
PHASORS a,b -> mean = Re(a conjugate(b))/2
             -> ripple phasor = ab/2 at 2 omega
             -> restore scale, sign, and units.
```

It prevents phase loss and avoids expanding two sine/cosine forms when only the
mean or ripple channel is wanted. On A23-05, however, a competent standard phasor
solution performs the same physics and algebra without encoding two semantic
requests. The atomic ledger therefore returns `always_direct`. The executable
constructor is admitted as a review, derivation, and exact-checking tool on this
card, not as evidence of an exam-time speedup.

The current `ProblemCard` admits exactly one request. A23-05 composes a response
request followed by a product request, so the common router is deliberately not
weakened or given an answer-specific composite variant. Multi-stage semantic
request composition is a recorded architecture obstruction, not silently hidden.

## Evidence and disposition `V-harmonic-product-2026-09-06`

| Evidence ID | Operation | Permitted consequence |
| --- | --- | --- |
| E16-SOURCE | hash-bound extraction and full-page visual checks of PDF pages 9 and 34 | exact provenance for both statements and diagrams |
| E16-OBSTRUCTION | multiplication leaves the one-frequency linear phasor representation | a DC-plus-`2 omega` consumer is required |
| E16-RED | absent public product API, corpus promotions, and CLI command fail before implementation | behavior was not already present |
| E16-LAW | generic unequal-complex-phasor fixture reconstructs the direct product | exact bilinear channel law on the frozen domain |
| E16-A23 | response plus product returns all three requested observables and energy balance | full execution of the obstruction-generating source |
| E16-A11 | unchanged pipeline at `L=0` under the large-loop theorem contract | bounded second-source transfer |
| E16-BOUNDARY | invalid time dependence, complex scale, and zero frequency are rejected | explicit admission boundary |
| E16-USE | atomic A23 same-observable comparison | handwritten advantage rejected on this card |
| E16-CORPUS | A23-05 and A11-06 promoted with executable tests | 24 full, 3 partial, 2 shape-only, 19 candidates, 74 outside, 4 qualitative |

| Claim dimension | Disposition | Boundary |
| --- | --- | --- |
| exact same-frequency harmonic product | `D+ supported` | two exact phasors, real scale, positive shared frequency |
| mean and second-harmonic torque return | `D+ supported` | A23-05 and A11-06 with stated physical law contracts |
| inductive-to-noninductive transfer | `D+ supported-bounded` | two electromagnetic rotating-coil problems |
| handwritten exam leverage | `D- rejected on A23-05` | standard route avoids request encoding |
| multi-stage common routing | `D? unresolved` | current card owns exactly one semantic request |
| different-frequency or higher products | `D? outside contract` | no mixing lattice or spectral algebra is implemented |
| law discovery, novelty, learner advantage | `D? unresolved` | neither sources nor current tests establish these claims |

## Re-entry and reproduction

Reopen this contract only if a source problem forces different-frequency mixing,
more than two factors, a nonperiodic/transient product, or a composition result that
cannot be expressed by the current linear pipeline. More rotating-coil examples
alone cannot expand the claim.

The later [typed composition result](typed-construction-composition-17.md) closes
the recorded architecture obstruction with a separate one-successor artifact
contract. It does not change this result's harmonic-product or exam-leverage
dispositions.

From `computation/` run:

```text
uv run python -m unittest tests.test_harmonic_product -v
uv run python -m worktable harmonic-product
uv run python -m unittest discover -s tests -v
```
