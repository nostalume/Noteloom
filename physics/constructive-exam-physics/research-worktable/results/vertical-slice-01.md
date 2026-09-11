# Vertical-slice result 01

## Question

Can the same stable compiler boundary execute one continuous/oriented mechanics
construction and one discrete/spectral atomic construction without using problem
identifiers or expected answers as inputs?

## Bound artifacts

- implementation: [`../computation/occ`](../computation/occ);
- executable specification: [`../computation/tests/test_vertical_slices.py`](../computation/tests/test_vertical_slices.py);
- source status: problem wording is provisionally bound to the public shared-chat
  transcripts described in [`../materials.md`](../materials.md). Original PDF page
  bindings remain unavailable.

## Constructed outputs

### Mechanics

The adapter constructs the local rotation vector from scalar angular speed and
latitude, computes `-2 Omega cross v`, derives the horizontal free-surface gradient
from steady pressure balance, and projects it onto the supplied cross-channel
displacement. It returns the signed height difference and a balance residual.

### Atomic physics

The adapter validates typed `LSJ` terms, parity, electric-dipole term rules, and an
explicit weak-field hierarchy. It constructs exact Landé factors, magnetic
sublevels, the `Delta m` selection graph, distinct shift coefficients, and
polarization counts.

## Fresh executable evidence

Environment: CPython 3.11 on Windows. Canonical focused command:

```text
python -m unittest discover -s tests -v
```

The fresh expanded run passed nine tests. It established:

- the source Coriolis result, its signed orientation reversal, and transfer from
  northward to eastward flow;
- missing-latitude refusal;
- six lines for the supplied weak-field transition;
- transfer to a different `LS` transition with twelve generated edges;
- refusal of a missing or nonweak field hierarchy and a same-parity electric-dipole
  transition;
- refusal when no adapter supports the semantic types.

## Supported interpretation

The common boundary can host two physically different adapter computations and
return uniform solution/refusal records. This supports the software interface and
the separation of kernel from domain laws for these two slices.

It does **not** yet establish:

- trustworthy recovery of the original exam statements or answers;
- blind transfer, because the present expected outputs were visible during local
  development;
- automatic extraction from natural language;
- a cross-area composition;
- a complete-route computational advantage;
- extension to electromagnetism, condensed matter, or statistical physics.

## Rejoin edge

The compact result returns to T0 and the `M-R/M-I/M-X` and `Q-R/Q-I/Q-X` portion
of SPPC-Bench-17. The next discriminating edge is a locked hidden transfer set
followed by one cross-area port composition.
