# Semantic-Gap Audit: N1–N3

Status: active audit after internal-construction revision  
Scope: `N1`, `N2`, `N3`, and the massive spin-one bridge

## Classification rule

Every arrow is acceptable only if it is one of:

- an explicit physical/analytic presumption;
- a definition applied to an already constructed object;
- a theorem contract with exact input and output;
- a deduction whose equation can be checked from preceding equations.

Naming a familiar object does not close a bridge.

## Audit

| ID | Previous jump | Required bridge | Disposition |
| --- | --- | --- | --- |
| `SG-01` | inertial frame -> affine map | state affine spacetime as a presumption; derive only the composition and metric restriction | repaired in `N2` |
| `SG-02` | probability preservation -> unitary `U(g)` | rays, unitary/antiunitary theorem, connected-component choice, projective phase | repaired in `N2` |
| `SG-03` | projective Lorentz action -> spin cover | expose central phase and why a `2pi` rotation may act as `-1` on vectors | repaired in `N2` |
| `SG-04` | continuity -> `U(a)=exp(i a.P)` | strong continuity, Stone generator, spectral calculus, generator domain | repaired in `N2` |
| `SG-05` | commuting translations -> momentum | joint spectral measure and definition of momentum as its support | repaired in `N2` |
| `SG-06` | Lorentz covariance -> momentum orbit | covariance of spectral projections plus explicit single-orbit presumption | repaired in `N2` |
| `SG-07` | standard boost -> little group | preimage ambiguity, stabilizer definition, measurable-section boundary | repaired in `N2` |
| `SG-08` | little group -> internal fibers | construct associated bundle `(L x V_sigma)/~` | repaired in `N2` |
| `SG-09` | invariant probability -> `d3p/(2E)` | restrict invariant `d4p` with `delta` and derive the Jacobian | repaired in `N2` |
| `SG-10` | Wigner rotation -> state representation | prove stabilizer membership, cocycle, norm preservation, and phase composition | repaired in `N2` |
| `SG-11` | all one-particle UIRs have this form | state the imprimitivity theorem as a converse theorem contract | repaired in `N2` |
| `SG-12` | covariance -> field transformation | derive pullback/value action and verify the group law | repaired in `N2` |
| `SG-13` | invariant group norm -> Haar measure | theorem contract, unimodularity, and direct Jacobian check | repaired in `N2` |
| `SG-14` | coefficient readings recover the field | cyclic covector definition and injectivity/reconstruction proof | repaired in `N2` |
| `SG-15` | polynomial sector is not `L2(G)` | analyze finite matrix coefficients along a noncompact boost | repaired in `N2` |
| `SG-16` | coefficient map is equivariant | substitute the group law and derive the intertwining identity | already explicit in `N2` |
| `SG-17` | spin-one fiber -> Proca symbol | derive the minimal Lorentz-equivariant polynomial symbol from the target transverse kernel | repaired in massive result |
| `SG-18` | Proca kernel dimension -> spin-one representation | identify `k^perp` with the rest spatial space and its stabilizer action | already explicit in massive result |
| `SG-19` | structural proof -> no computation needed | show every requested invariant follows before choosing components | already explicit in massive result |

## Bridges resolved downstream

- `OPEN-1`: the null stabilizer and finite-helicity representation are constructed
  in the [massless helicity-one bridge](../nodes/03b-massless-helicity-one.md).
- `OPEN-2`: the potential/curvature/gauge complex and its helicity `+/-1` quotient
  are constructed in the same result.

## Remaining open bridges

These are not silently filled:

- `OPEN-3`: derive a general equation-construction criterion from equivariant
  symbols or complexes, including the analytic passage from a standard fiber to
  global distributions;
- `OPEN-4`: construct an operator-level group-function equation and compare it with
  the direct carrier equation; coefficient packaging alone is not such an operator;
- `OPEN-5`: establish when right Poincare quantum numbers have physical meaning
  rather than encoding a choice of body-frame reading;
- `OPEN-6`: prove any general-spin economy claim with scaling data instead of
  extrapolating from spin one.

Until resolved, these remain questions in `N3`–`N6`, not manuscript conclusions.
