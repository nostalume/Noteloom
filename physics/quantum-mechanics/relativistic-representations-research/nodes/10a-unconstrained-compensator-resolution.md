# N10a — Unconstrained Compensator Resolution

Status: supported for the local equation complex and its free physical quotient;
local action and source-response comparison remain separate capabilities  
Consumes: [N10 obstruction resolution](10-equivariant-obstruction-resolution.md),
[N4a polynomial complex](04a-polynomial-complex-details.md), and
[N4c action audit](04c-action-completion-audit.md)  
Source contracts: [action-principle contracts](../sources/action-principle-contracts.md),
especially `AP-03` and `AP-04`  
Produces: the obstruction-generated unconstrained bosonic compensator complex, an
explicit quotient equivalence with the constrained realization, and a
capability-relative cost verdict

## Research contract

- **Upstream anchor:** N10 constructs the constrained symmetric-spin complex and
  computes the residual `(1/2)P_p^3T epsilon` when the gauge parameter is not
  traceless.
- **Bridge question:** what is the smallest local carrier enlargement that cancels
  this residual, and does removal of the algebraic trace constraint reduce the
  complete route to the same helicity quotient?
- **Invariant target:** the parity-paired massless helicity fiber
  `C_(+s) direct-sum C_(-s)` at every finite integer `s`.
- **Capability boundary:** first compare local equation realizations. A local
  quadratic action and ordinary conserved-current coupling require an additional
  multiplier and are priced separately.
- **Internal benchmark:** construct the enlarged complex from the residual, prove
  its gauge quotient is the constrained quotient, and compare the whole carrier,
  derivative, and recovery costs. Stop before general BRST or mixed-symmetry
  extensions.

## 1. Removing one trace constraint creates two calculable failures

Let the gauge parameter range over the full symmetric carrier

```text
Gbar_s=Sym^(s-1)(M_C^*),
delta phi=P_p epsilon.                              (1.1)
```

The Fronsdal symbol constructed in N10 obeys on this same input

```text
D_sP_p epsilon=(1/2)P_p^3T epsilon.                (1.2)
```

There is also a carrier failure. Using `[T,P_p]=2A_p` twice gives

```text
T^2P_p epsilon
 =T(P_pT epsilon+2A_p epsilon)
 =P_pT^2epsilon+4A_pT epsilon.                     (1.3)
```

Thus an arbitrary parameter neither preserves `ker T^2` nor leaves the equation
invariant. These are independent outputs of the same trace `T epsilon`; the
cheapest repair should represent that trace once rather than cancel its two images
separately.

## 2. The residual constructs the compensator and both equations

Introduce one rank-`s-3` symmetric field

```text
alpha in Sym^(s-3)(M_C^*),
delta alpha=T epsilon.                              (2.1)
```

The coefficient and derivative order of its first appearance are forced by (1.2):

```text
A_s(phi,alpha)
 =D_s phi-(1/2)P_p^3alpha.                         (2.2)
```

Evaluate (2.2) on the same parameter:

```text
delta A_s
 =D_sP_p epsilon-(1/2)P_p^3T epsilon
 =0.                                               (2.3)
```

The carrier obstruction (1.3) constructs a second output

```text
B_s(phi,alpha)
 =T^2phi-4A_palpha-P_pT alpha.                     (2.4)
```

Its variation is another same-input cancellation:

```text
delta B_s
 =(P_pT^2+4A_pT)epsilon-4A_pT epsilon-P_pT^2epsilon
 =0.                                               (2.5)
```

Hence the typed unconstrained complex is

```text
Sym^(s-1)
  --Rbar_s=(P_p,T)-->
Sym^s direct-sum Sym^(s-3)
  --(A_s,B_s)-->
Sym^s direct-sum Sym^(s-4).                        (2.6)
```

Negative-rank summands are absent. For `s<=2`, no compensator exists and the trace
restriction is automatic. For `s=3`, `alpha` is scalar and `B_s` is absent. The
normalization differs from conventions that symmetrize indices with unnormalized
sums; the invariant cancellation (2.3)--(2.5) fixes the coefficients used here.

## 3. Fischer splitting constructs the reduction to the constrained complex

The four-dimensional Fischer decomposition gives the exact trace sequence

```text
0 -> H_(s-1) -> Sym^(s-1) --T-> Sym^(s-3) -> 0.    (3.1)
```

Surjectivity is constructive. Decompose any `alpha` into traceless Fischer layers;
on each `U^jH_r` layer, the nonzero coefficient

```text
T(U^(j+1)h_r)
 =2(j+1)(2r+4+2j)U^j h_r                          (3.2)
```

defines a finite right inverse `J_s` with `T J_s=I`.

For any field pair `(phi,alpha)`, choose

```text
epsilon_alpha=-J_s alpha.                          (3.3)
```

Then the transformed compensator is computed, not asserted:

```text
alpha+T epsilon_alpha
 =alpha-TJ_salpha
 =0.                                               (3.4)
```

The parameters preserving this gauge are exactly `ker T=H_(s-1)`. On the slice
`alpha=0`, equations (2.2) and (2.4) become

```text
D_sphi=0,
T^2phi=0,                                          (3.5)
```

which are precisely the constrained field carrier and equation. Conversely every
constrained solution embeds as `(phi,0)`. If two such embedded solutions are
related by an unconstrained transformation, preservation of `alpha=0` computes
`T epsilon=0`, so the transformation is already a constrained one. Therefore

```text
ker(A_s,B_s)/im Rbar_s
  ~= {phi in ker T^2 : D_sphi=0}/P_p(ker T).       (3.6)
```

N10's kernel compression and N4a's screen calculation now give

```text
nonnull p:  cohomology=0,
null p!=0: cohomology=C_(+s) direct-sum C_(-s).    (3.7)
```

The traceful parameter and `alpha` form a Stueckelberg pair. Equation `B_s=0`
returns the double-trace condition after that pair is removed. This is a local
chain reduction, not merely equality of degree counts.

## 4. Capability-relative cost decides what was purchased

In four dimensions, `dim Sym^r=C(r+3,3)` and `dim H_r=(r+1)^2`. For `s>=4`:

| Resource | compressed constrained realization | unconstrained compensator equations |
| --- | ---: | ---: |
| gauge parameters | `s^2` | `C(s+2,3)` |
| field carrier | `2s^2+2` | `C(s+3,3)+C(s,3)` |
| equation target | `(s+1)^2` | `C(s+3,3)+C(s-1,3)` |
| maximum derivative order | `2` | `3` on `alpha` in `A_s` |
| algebraic restrictions | `T epsilon=0`, `T^2phi=0` | none |
| recovery operations | direct screen quotient | construct `J_s`, fix `alpha=0`, then use constrained quotient |

For the capability “realize the same free helicity fiber,” the compensator route
removes two algebraic restrictions but replaces quadratic-size irreducible carriers
by cubic-size symmetric carriers, adds a field and equation, raises derivative
order, and requires a gauge-fixing recovery map. It is therefore dominated by the
compressed constrained realization for this capability.

That verdict changes if the requested capability includes an unconstrained input
interface. Then the constrained route does not satisfy the contract, and (2.6) is
the minimal residual-generated local equation presentation found here. It changes
again for a local action with ordinary conserved sources: the primary-source
contract requires an additional rank-`s-4` multiplier, while the compensator-only
equations are not themselves Euler equations. Source exchange—not vacuum
cohomology—must decide that stronger comparison.

## 5. Global verdict and stop condition

The compensator does not reveal a cheaper realization of the particle
representation. It reveals what the Fronsdal trace constraints compress:

```text
traceful gauge direction <-> compensator Stueckelberg field,
double-trace carrier condition <-> invariant equation B_s=0. (5.1)
```

Thus constraint removal is a capability purchase, not a free simplification. The
fixed free-realization comparison is closed. Re-enter this branch only for one of
two stronger outputs:

1. a local action/current-exchange comparison, adding the multiplier demanded by
   the action contract; or
2. an interaction or background where the constrained slice cannot be maintained
   locally and the compensator changes an actual observable or consistency result.

General unconstrained BRST towers, mixed-symmetry carriers, and nonlocal curvature
equations are outside this benchmark because they do not change its realization
verdict.
