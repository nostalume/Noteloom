# N10c — Generative Residual Constructor

Status: supported as a cross-family regression generator and bounded-refusal
mechanism for constrained symmetric bosonic and spinor-tensor search cells; N10d
closes compact-source causal use for the Maxwell specialization and N10e generates
the first higher-spin physical-source adapter; N10f independently generates its
coincident Euler multiplier; N10g transfers completion, source adaptation, and
restricted Euler generation to the Clifford branch; N10h now generates both input
grammars from declared symmetric carrier functors, while full little-group recovery,
off-shell presentation selection, and whole-route gain remain open  
Consumes: [N10 obstruction resolution](10-equivariant-obstruction-resolution.md),
[N4a polynomial complex](04a-polynomial-complex-details.md), and
[N4m finite integer-spin field machine](04m-finite-integer-spin-field-machine.md)  
Computation: [generative residual constructor](../computation/10c-generative-residual-constructor/README.md)  
Produces: a retained exact operation that turns a typed natural-operator grammar
and resource budget into a constrained local complex, internal certificates, or
an explicit obstruction record

## Research contract

- **Upstream anchor:** N10 has constructed the residual logic and the complete
  fixed-carrier invariant map spaces; N4m supplies the downstream `FieldSystem`
  interface.
- **Bridge question:** can those derivations be retained as an operation that
  generates a field system, rather than ending as a proof of an already assembled
  equation?
- **Invariant target:** the parity-paired massless helicity quotient recovered by
  the corresponding constrained symmetric tensor or spinor-tensor complex.
- **Downstream effect:** a generated `(R,C,D)` must be usable by N4m's scalar-wave
  response construction without reconstructing its derivation.
- **Special resources:** four-dimensional flat metric, symmetric tensor or
  spinor-tensor carrier shape, no auxiliary carrier, and momentum degree at most
  two. Trace and gamma constraints are outputs rather than supplied resources.
- **Internal benchmark:** generate bosonic and fermionic equation coefficients and
  carrier constraints without supplying them; reject budgets that cannot cancel
  the residual or preserve the carrier; then pass the bosonic output to one
  response-symbol computation.
- **Horizon:** this node does not enumerate arbitrary Lorentz carriers, prove a
  general PBW theorem, construct an action, evaluate a causal distribution on a
  compact source, or claim computational leverage.

## 1. Retain the operator grammar rather than the answer

The input grammar consists of typed natural operations:

| Primitive | Momentum degree | Symmetric-rank shift | Meaning |
| --- | ---: | ---: | --- |
| `Q` | 2 | 0 | scalar wave symbol `p^2` |
| `P` | 1 | `+1` | symmetric multiplication by momentum |
| `A` | 1 | `-1` | contraction with momentum |
| `T` | 0 | `-2` | trace |

Their relations are operations on the same polynomial input:

```text
A P = P A + Q,
T P = P T + 2 A,
T A = A T,
Q central.                                             (1.1)
```

The constructor normal-orders words with (1.1), enumerates only words of the
requested map type and resource degree, and solves the resulting coefficient
system over exact rationals. Neither the Fronsdal coefficients nor a component
matrix is an input.

This is intentionally smaller than the general map space (N10, 3.1). The grammar
is a theorem input extracted from the symmetric carrier; generating such a grammar
from arbitrary Lorentz modules remains a separate transfer boundary.

## 2. The scalar-wave failure generates the defect map

Take the gradient gauge map

```text
R=P:G_s->F_s.                                            (2.1)
```

The requested defect map has momentum degree one and rank shift `-1`. Enumeration
and normal ordering produce the basis

```text
{A,P T}.                                                (2.2)
```

Write `C=a A+b P T`. Before imposing a parameter constraint, evaluate both basis
maps after the same `R`. Equation (1.1) computes

```text
A P epsilon
 =P A epsilon+Q epsilon,

P T P epsilon
 =P(P T+2A)epsilon
 =P^2T epsilon+2P A epsilon.                            (2.3)
```

Asking for the scalar-wave homotopy `C R=Q` gives

```text
C P epsilon
 =a Q epsilon+(a+2b)P A epsilon+bP^2T epsilon,

a=1,
a+2b=0,
bT epsilon=0.                                          (2.4)
```

The first two equations demand `b=-1/2`, so the last channel cannot be cancelled
inside the no-auxiliary budget. It constructs the minimal parameter restriction
`T epsilon=0`. Exact elimination on that generated carrier then gives

```text
C=A-(1/2)P T.                                          (2.5)
```

The constructor next searches trace powers preserved by `R`. On the generated
parameter carrier,

```text
T P epsilon=2A epsilon !=0,
T^2P epsilon=T(PT+2A)epsilon=0.                         (2.6)
```

Thus the first admissible field carrier is `ker T^2`; double tracelessness is an
output rather than a hidden input.

The field equation is exported as the residual complement

```text
D=Q-R C
 =Q-P A+(1/2)P^2T.                                    (2.7)
```

Now the gauge identity is not separately guessed:

```text
D R
 =(Q-R C)R
 =Q R-R(C R)
 =Q R-R Q
 =0.                                                   (2.8)
```

The semantic invariant is the same gauge input throughout (2.3)--(2.8). The
generated `C` measures the obstruction to scalar-wave propagation; `D` removes
exactly that gauge direction.

## 3. Independent generation closes the circularity check

The constructor also enumerates rank-preserving momentum-degree-two normal words.
Within the declared trace budget it obtains

```text
{Q,P A,P^2T}.                                          (3.1)
```

It fixes only the cheapest seed coefficient, `Q`, and solves

```text
(Q+b P A+c P^2T)P epsilon=0.                           (3.2)
```

Normal ordering calculates the residual channels and exact elimination returns

```text
b=-1,
c=1/2.                                                 (3.3)
```

Equality between (2.7) and the independently generated (3.2)--(3.3) is an internal
construction certificate. Thus factorization is not being used to smuggle the
finished equation into the direct residual route.

## 4. Insufficient resources return an obstruction

Set the admissible trace depth to zero. The defect-map basis collapses to `{A}`.
For any coefficient `a`, (2.3) becomes

```text
a A P epsilon=a Q epsilon+a P A epsilon.                (4.1)
```

Matching the required `Q` fixes `a=1`, while cancelling the independent `P A`
channel requires `a=0`. The system is inconsistent. The constructor therefore
returns

```text
phase: defect-map,
basis: {A},
uncancelled channel span: {Q,P A},
reason: admitted maps cannot cancel every residual.     (4.2)
```

This refusal has semantic content: within this carrier and degree budget, access
to the trace operation is necessary for the scalar-wave completion. It is not a
runtime failure and it is not a claim about every possible carrier enlargement.

## 5. Generated output is consumed once

The returned object contains

```text
FieldSystem_local=(R,C,D,Q),
C R=Q,
D R=0,
D+R C=Q.                                               (5.1)
```

N4m's response step now consumes (5.1). For an admissible source symbol `S` with
`C S=0` at non-null momentum, set

```text
phi=Q^(-1)S.                                           (5.2)
```

On that same source,

```text
D phi
 =(Q-R C)Q^(-1)S
 =S-R Q^(-1)C S
 =S.                                                   (5.3)
```

The executable probe constructs a basis of such sources and verifies (5.3) for
spins `2` through `6`. This is a real consumer of the generated maps, but only an
off-shell symbol analogue of Green response. It does not yet establish the full
use-level computational claim for compact sources and causal support.

## 6. The same operation transfers to the Clifford grammar

Supply a second primitive grammar, not a finished equation:

```text
L=Slash,       G=Gamma,
G P=P G+L,
G L=-L G+2A,
G A=A G,
L^2=Q,                                                (6.1)
```

with the compatible ordering relations among `P,L,A,Q`. The cheapest
rank-preserving first-order seed is `L`; the generated correction span is `{P G}`.
Without a parameter constraint,

```text
(L+bP G)P epsilon
 =(1+b)L P epsilon+bP^2G epsilon.                     (6.2)
```

Cancelling the first channel requires `b=-1`, while cancelling the second for an
arbitrary parameter requires `b=0`. The residual therefore constructs

```text
G epsilon=0.                                          (6.3)
```

On this generated carrier, exact residual solving returns

```text
S=L-P G,
S P epsilon=0.                                        (6.4)
```

The field constraint is selected by preservation rather than supplied. The same
normalizer computes

```text
G P epsilon=L epsilon !=0,
G^2P epsilon=2A epsilon !=0,
G^3P epsilon
 =P G^3epsilon+L G^2epsilon+2A G epsilon
 =0.                                                   (6.5)
```

Thus `G^3psi=0` is the shallowest admitted field constraint. Budgets capped at
gamma depth two return an explicit carrier-preservation obstruction. Finite-rank
matrices recover zero non-null and two null complex quotient classes for tensor
ranks `1` through `4`.

This is transfer of the retained residual/repair interface: the bosonic and
Clifford adapters supply different primitive identities, while enumeration, exact
coefficient solving, constraint search, certificates, refusal semantics, and
regression consumption are shared. It remains transfer across two declared
symmetric grammars, not a universal Lorentz-module compiler.

## 7. Checks and supported claim

The executable packet establishes:

1. exact rational generation of the bosonic and fermionic coefficients;
2. residual generation of `T epsilon=0`, `T^2phi=0`, `G epsilon=0`, and
   `G^3psi=0`;
3. the identities in (5.1), construction coincidence, fermionic gauge invariance,
   and both carrier-preservation certificates;
4. explicit refusal at trace/gamma depth zero and at insufficient field-constraint
   depth;
5. zero non-null and two null quotient dimensions for bosonic spins `2` through
   `6` and fermionic tensor ranks `1` through `4`;
6. exact recovery of admissible non-null bosonic source symbols through
   (5.2)--(5.3).

Finite matrices enter only after generation. They certify the physical regression;
they do not select the coefficients. The supported claim is therefore:

> For the declared symmetric bosonic and Clifford grammars, the shared residual
> constructor generates their constrained local equations and minimal preserved
> carrier constraints, returns meaningful budget refusals, and exports the bosonic
> maps to the scalar-wave response interface.

This passes regression, bounded refusal, and cross-family transfer within the two
declared grammars. It is not yet a complete little-group-action certificate, a
compact-source causal use result, or a whole-route computational gain.

## 8. Graph relation and next discriminator

```text
N10 invariant residual calculus
  -> N10c retained normal-order/solve operation
     |- bosonic grammar -> generated (R,C,D,T,T^2)
     `- Clifford grammar -> generated (R,S,G,G^3)
  -> N4m scalar-wave response interface
  -> N10d Maxwell compact-source causal use.             (8.1)
```

The coefficient/constraint constructor has survived the Clifford transfer. N10d
now also specializes its returned bosonic object to spin one, constructs a compact
conserved current, and recovers a nonzero retarded response and physical screen
class. This closes interoperability, but its complete cost audit rejects
single-instance prediction gain: generation adds work to the shared Maxwell Green
calculation.

N10e closes the first higher-spin causal discriminator. The paired residual
generates `M=I-(1/4)UT`, an exact inverse family and a refusal without metric
insertion; a discriminating compact spin-two source consumes the returned adapter.
N10f now generates formal self-adjointness of `MD` from the separate skew-adjoint
residual and proves coincidence with N10e's multiplier. N10g now completes the
Clifford transfer: the equation generates its wave completion, two independent
obstruction routes generate the same two-layer multiplier, and a rank-two source
consumer uses it. N10h now supplies both primitive grammars from the symmetric
carrier functor, invariant metric, and optional Clifford action; label-only input
is refused. Further re-entry requires one of: a failed normal-form confluence check,
an incorrect little-group action despite the quotient dimension, or a capability-
relative search that chooses the off-shell presentation before grammar generation.
