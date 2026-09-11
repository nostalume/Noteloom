# Local A617 corpus audit

## Bound artifact

- file: [中国科学技术大学研究生入学考试习题汇编—普通物理A617.pdf](</H:/Storage/Affair/普通物理/中国科学技术大学研究生入学考试习题汇编—普通物理A617.pdf>);
- size: 1,372,540 bytes;
- SHA-256: `B84E9D24468628433D1A126771DC8DE5A9D3CA7C2DBD01A78597FDDF01C8D764`;
- pages: 36;
- encryption/forms: unencrypted, no interactive form fields;
- media box: 595.32 by 841.92 points;
- creator metadata: Microsoft Word 2019;
- creation/modification metadata: 2025-01-02 11:12:31 +08:00.

All 36 pages contain extractable text. Representative PDF pages 4–9, 12, 25, 28,
34, and 36 were rendered and visually inspected against extraction for the 2025,
2024, 2023, 2021, 2015, 2014, 2011, and 2010 problems used below. Equations remain visually authoritative where font
extraction is garbled.

The complete page-level top-level-problem inventory is maintained separately in
[a617-corpus-index.tsv](a617-corpus-index.tsv). It contains 126 numbered problems
across 15 included years; 2017 is absent from the compilation. Its admission labels
are a reproducible triage queue, not claims that unexecuted problems are solved.

The evidence vocabulary is deliberately asymmetric:

| Label | Admitted meaning |
| --- | --- |
| `executed-full` | complete source relations, target consequence, and physical return were checked |
| `executed-partial` | named source subparts were executed; the whole top-level problem was not |
| `executed-shape-only` | a simplified fixture preserves one structural shape, not the full printed problem |
| `candidate-unexecuted` | static inspection suggests an existing kernel may apply; this is queue state, not coverage |
| `outside-current-grammar` | at least one essential physical or mathematical operation is absent |
| `qualitative-only` | the primary target needs an explanatory rather than computational rubric |

Current counts are produced by `python -m worktable corpus-audit`; they belong to
the active graph rather than this source-description cutoff.

## Provenance cautions

- The cover says 2010–2024, while the table of contents and body include a 2025
  paper.
- The preface calls the collection quantum mechanics `(828)`, while the cover,
  headers, and inspected exam pages identify general physics A617. This appears to
  be an internal template inconsistency and is not silently corrected.
- The document describes itself as a community compilation for free exam
  preparation. It is not treated as official marking guidance.

## Selected recent bindings

| ID | PDF page | Printed exam page | Problem | Role in framework |
| --- | ---: | ---: | --- | --- |
| A25-02 | 4 | 2025-1 | tangential satellite impulse, escape, and apogee | nonlinear invariant-extension test |
| A25-05 | 5 | 2025-2 | layered and continuously varying dielectric | linear functional pullback through constitutive field map |
| A25-06 | 5 | 2025-2 | numerical series RLC impedance, current, and power factor | exact harmonic-response cross-area transfer and cost boundary |
| A24-05 | 6 | 2024-3 | time-dependent solenoid with conducting rod | quadratic Joule functional pulled to current derivative |
| A23-05 | 9 | 2023-6 | rotating square coil with resistance and self-inductance | harmonic response chain and torque/power recovery |
| A21-03 | 12 | 2021-9 | incident/reflected wave, standing-wave pattern, and Q signal | phase-loss obstruction and exact harmonic/spatial construction |
| A15-01 | 25 | 2015-22 | pendulum resultant horizontal after release from `cos(theta)=0.1` | generated event relation and physical-branch transfer |
| A15-02 | 25 | 2015-22 | point particle reflecting from a rough wall | constrained impulse projection with tangential-arrest/sliding return |
| A14-06 | 28 | 2014-26 | induced voltage along an arc, chord, and their two-wire circuit | obstruction-driven path functional and area/curl certificate |
| A11-06 | 34 | 2011-31 | rotating small coil in a much larger current loop | unchanged harmonic-product transfer in the negligible-inductance limit |
| A10-06 | 36 | 2010-36 | induced voltage along alternative arcs and without a conductor | unchanged path transfer and endpoint-only refusal |

## Use boundary

The worktable records compact problem descriptions, page bindings, and derived
calculations. It does not reproduce the compilation. Any discrepancy between a
derived answer and a future official solution must remain explicit.
