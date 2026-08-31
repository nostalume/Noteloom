# GS09 — Field on the Poincare Group and Orientable Objects

## Raw locator

- Paper: D. M. Gitman and A. L. Shelepin, _Field on Poincare group and quantum
  description of orientable objects_ (`arXiv:0901.2537v2`, 2009).
- Stable HTML: <https://arxiv.org/html/0901.2537>
- Authority: primary follow-up that makes the function-space distinction and
  left/right action more explicit than the current manuscript.

## Semantic extraction

| Claim | Exact locator | Compact result | Use |
| --- | --- | --- | --- |
| `GS09-01` | Eq. (16); Eqs. (94)--(100) | Generalized regular action has the form `T(g_l,g_r)f(q)=f(g_l^-1 q g_r)`; left and right actions commute. | `N2` group-function action |
| `GS09-02` | Eqs. (82), (97)--(102) | The spin-cover Poincare group is parameterized by translation and `SL(2,C)` orientation variables with explicit left/right transformations. | `N2` convention check |
| `GS09-03` | Eqs. (106), text immediately after | `L2(G,dmu)` carries a unitary regular representation with invariant measure. | `N2` Hilbert regular space |
| `GS09-04` | text after Eq. (106) | Polynomial functions of spin variables carry finite-dimensional nonunitary Lorentz representations and are not in that `L2(G)` space; the relevant integral diverges. | decisive `N2` separation |
| `GS09-05` | Eqs. (114)--(117) | Separating `f(x,z)=phi^n(z) psi_n(x)` gives contragredient Lorentz transformations of basis functions and multicomponent fields. | `N2` coefficient sector |
| `GS09-06` | discussion around Eqs. (118)--(119) | Right Lorentz transformations act on orientation without changing spacetime, whereas right translations mix spacetime and orientation variables. | scope right-type selection in `N2/N3` |
| `GS09-07` | Section 10, Eq. (159) | Equivalence of realizations requires an explicit nonsingular intertwiner, not common labels alone. | `N3` bridge criterion |

## Research consequence

“Scalar functions on the Poincare group” cannot be used as one untyped space. At
least two regimes must be separated:

1. the unitary regular Hilbert space `L2(G,dmu)`;
2. finite polynomial/matrix-coefficient sectors used as generating functions for
   nonunitary Lorentz carriers.

The second may be a useful algebraic representation but is not a Hilbert subspace
of the first. Any bridge claiming unitarity must therefore supply a different norm,
completion, distributional interpretation, or physical quotient.
