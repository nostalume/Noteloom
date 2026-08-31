# Result — What the Two Spin-One Bridges Establish

Status: supported synthesis of the two `N3` constructions  
Inputs: [massive spin one](../nodes/03a-massive-spin-one.md) and [massless helicity one](../nodes/03b-massless-helicity-one.md)

| Semantic object | Massive spin one | Massless helicity one |
| --- | --- | --- |
| Standard momentum | `k=(m,0,0,0)` | nonzero future-null `k` |
| Little-group physical fiber | `k^perp` | `k^perp / span(k)` |
| Equation presentation | Proca symbol | Maxwell symbol complex |
| Gauge image | none | `span(k)` |
| Physical content | rotation spin one, three polarizations | helicities `+1 direct-sum -1`, two polarizations |
| Decisive check | little-group action on the kernel | little-group action on the quotient |
| Group-function economy | no reduction at fixed spin | no reduction at fixed helicity |

The common supported result is narrower than a globalization theorem. Once a
Lorentz-equivariant polynomial complex is already available, its physical content
can be tested at standard momentum by computing the kernel, gauge image, and
little-group action. Dimension matching alone is insufficient.

The vector checks also expose what remains undetermined. The particle representation
does not uniquely choose a covariant carrier or local operator. Locality,
differential order, auxiliary fields, gauge presentation, reality/parity, and an
action principle are additional construction criteria. [N4](../nodes/04-local-symbol-extension.md)
now gives a universal chiral local family; Proca and Maxwell remain supported
alternative-carrier realizations against which that family can be compared.
[N4a](../nodes/04a-polynomial-complex-details.md) owns the general polynomial and
gauge-complex checks required by further alternatives. It now makes those checks
finite for fixed carriers and order, and its symmetric family specializes to
Maxwell at spin one and the metric-potential symbol at spin two. The intrinsic
screen exact sequence now closes the physical quotient uniformly, giving
helicities `+s direct-sum -s` for every finite bosonic integer `s`.

[N4b](../nodes/04b-half-integer-potential.md) supplies the matching Clifford
sequence. In particular, the vector-spinor potential has the physical quotient
`C_(+3/2) direct-sum C_(-3/2)` without a component count; the same proof covers
all finite half-integer ranks.
