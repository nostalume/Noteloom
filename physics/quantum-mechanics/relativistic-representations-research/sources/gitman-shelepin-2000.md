# GS — Gitman and Shelepin (2000/2001)

Consumed by: [representation spaces](../nodes/02-representation-spaces.md) and
[spin, helicity, and carriers](../nodes/03-spin-helicity-carriers.md).

## Raw locator

- Paper: D. M. Gitman and A. L. Shelepin, _Fields on the Poincare group: arbitrary
  spin description and relativistic wave equations_.
- Stable source: <https://arxiv.org/abs/hep-th/0003146>, version 2, 2000-10-06.
- Journal: _International Journal of Theoretical Physics_ 40 (2001), 603--684.
- Size: 70 pages in the authors' arXiv description.
- Authority: primary source for the manuscript's current construction.
- Local cache: none; open only cited sections/equations when required.

## Semantic map

| Claim ID | Paper region | Compact extraction | Bound nodes |
| --- | --- | --- | --- |
| `GS-01` | Abstract; proper-group setup | Scalar functions on the Poincare group are used as generating functions for conventional spin-tensor fields. | `N2`, `N3` |
| `GS-02` | Proper Poincare group and generalized regular representations | Left and right actions supply different commuting operator families; their meaning must be typed before use. | `N2`, `N3` |
| `GS-03` | Discrete transformations section | `C`, `P`, and `T` are represented through automorphisms/complex conjugation on the group-function realization. | `N2`, `N7` |
| `GS-04` | 2D/3D/4D classification sections | Dimension-specific scalar functions are classified to obtain definite mass/spin equations. | later dimensional comparison |
| `GS-05` | 4D proper-group equations, around the Fierz--Pauli discussion | For integer spin in suitable Lorentz carriers, Klein--Gordon plus divergence-free and trace-free conditions isolate the intended massive spin. | nodes 05--08 |
| `GS-06` | 4D improper-group and comparative sections | Parity-completed systems connect `(j_1,j_2)` and `(j_2,j_1)` sectors; first-order systems occur only for restricted adjacent representations. | `N2`, `N6` |
| `GS-07` | Comparative section, free equations | Several free systems can have the same `2(2s+1)` solutions and be related by component elimination. | `N3`, `N7` |
| `GS-08` | Comparative section, interaction warning | Free equivalence can fail after minimal coupling because `[D_mu,D_nu]` produces field-strength terms. | `N7` |
| `GS-09` | Abstract and classification summary | Finite-dimensional nonunitary and infinite-dimensional unitary Lorentz sectors can describe the same mass/spin labels but yield different field realizations. | `N1`, `N3`, `N6` |

## Presumptions exposed

- The configuration space is enlarged from Minkowski space to the Poincare group.
- Spin variables are encoded as coordinates on the Lorentz-group factor.
- A scalar group function is considered a generating object for component fields.
- Mass and spin irreducibility are imposed through invariant-operator eigenvalues
  and subsidiary conditions.
- Equivalence is principally assessed in the free theory.

These are research inputs, not automatically necessary properties of every
relativistic field construction.

## Current manuscript binding

- Lines 13--345 reproduce group parametrization, regular actions, generators, and
  discrete transformations related to `GS-01`--`GS-03`.
- Lines 348--424 introduce the generating-function decomposition and central thesis.
- Lines 426--1091 follow the paper's lower-dimensional route.
- Lines 1092--1499 develop the 3+1 spinor and vector sectors.

The binding identifies content ownership only. It does not certify copied formulas.

## Extraction boundary

Do not reproduce the paper's large spinor-polynomial and component expansions here.
When a formula is needed, add its exact equation number and a one-sentence semantic
role to the table. A disputed expansion becomes a derivation or computation node;
only its compact checked invariant returns to this packet.

## Open challenges

- Construct an explicit intertwiner from the selected group-function sector to a
  Wigner-induced Hilbert representation (`N3`).
- Determine which right-action quantum numbers are physical and which label the
  chosen realization (`N2`, `N3`).
- Compare invariant eigenvalue equations with polynomial-symbol/gauge-complex
  constructions (node 05).
- Test the claimed free equivalences and their curvature obstruction (`N7`).
