# Vertical-slice result 02

## Question

Does the retained compiler boundary extend to all four target areas and compose
a condensed-matter output with a statistical observable without pretending that
an insufficient intermediate object is sufficient?

## Bound artifacts

- implementation: [`../computation/occ`](../computation/occ);
- executable specification: [`../computation/tests/test_vertical_slices.py`](../computation/tests/test_vertical_slices.py);
- historical benchmark contract: [`compiler-baseline.md`](compiler-baseline.md);
- source boundary: [`../materials.md`](../materials.md).

The cases remain synthetic/transcript-bound probes because the original PDF
pages and answers are not locally available. They are not scored as source-locked
SPPC-Bench-17 passes.

## New constructions

### Electromagnetic response

For a scalar linear medium, the adapter constructs
`J_cond = sigma E` and `J_disp = i omega epsilon E`. It recovers
`|J_cond|/|J_disp| = sigma/(omega epsilon)`, the quadrature phase, or the
crossover frequency `omega = sigma/epsilon`. It refuses tensor media when the
request lacks the direction and norm needed to define one scalar ratio.

### Lattice mode counting

For `p` atoms per primitive cell in `d` dimensions, the adapter constructs `dp`
branches, `d` acoustic branches, and `d(p-1)` optical branches. It converts a
declared atom or primitive-cell population into a total mode count and refuses an
untyped population convention.

### Spectral-to-thermal composition

The composition port accepts a discrete frequency measure
`{(omega_i, degeneracy_i)}`. For each mode it constructs
`x_i = hbar*omega_i/(k_B*T)` and evaluates

```text
C_V = k_B sum_i g_i x_i^2 exp(x_i)/(exp(x_i)-1)^2.
```

The executable probe checks invariance when every frequency and the temperature
are scaled by the same factor. It also refuses a bare total mode count: that count
cannot determine frequency-dependent Bose occupation.

## Fresh executable evidence

Environment: CPython 3.11 on Windows. Canonical command:

```text
python -m unittest discover -s tests -v
```

The fresh run passed 18 tests. The suite now contains:

- mechanics: one regression-shaped case, two orientation transfers, and one
  missing-datum refusal;
- atomic physics: one regression-shaped case, one different-transition transfer,
  and two regime/type refusals;
- electromagnetism: scalar response, crossover recovery, and an anisotropic
  nonuniqueness refusal;
- condensed matter: diamond counting, general `d,p` transfer, and an ambiguous
  population refusal;
- composition: spectral-to-thermal construction, dimensionless scaling transfer,
  and insufficient-port refusal;
- kernel: refusal for unsupported semantic types.

All returned certificates passed. During the run, the electromagnetic residual
certificate exposed a scale-dependent floating-point check; it was repaired by
checking reconstruction relative to the constitutive scale rather than demanding
an inappropriate absolute-zero residual.

## Verdict and frontier

This result supports the representation, generation, and explicit-refusal
behavior of a small cross-domain prototype. It also shows one real typed port:
frequency measure, not merely shared vocabulary, connects lattice dynamics to a
thermal observable.

It does **not** establish blind transfer, source regression, tensor response,
strong-field reconstruction, supercell invariance, continuum density-of-states
integration, or complete-route leverage. The next discriminating work is to lock
independent expected outputs before development of `M-T`, `E-T`, `Q-T`, and
`C-T`, then measure the same-observable route cost.

## Rejoin edge

The executable evidence rejoins T0, D0, C3, and the provisional `X-C` edge. The
research spine remains in discovery until P0/P1 ground truth and A0 route-cost
evidence exist.
