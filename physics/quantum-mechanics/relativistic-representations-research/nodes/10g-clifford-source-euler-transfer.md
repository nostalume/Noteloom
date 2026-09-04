# N10g — Obstruction-Generated Clifford Source/Euler Transfer

Status: supported for every separate finite symmetric half-integer-spin carrier in
four dimensions; the retained constructor now generates the completion, source
adapter, restricted Euler operator, inverse interface, and scalar-wave response,
and N10h now supplies its grammar from carrier-functor data; a real Grassmann action,
presentation selection, and whole-route computational gain remain open  
Consumes: [N10c generative residual constructor](10c-generative-residual-constructor.md),
[N10f bosonic Euler transfer](10f-generated-euler-operator.md), and
[N4i half-integer Green construction](04i-half-integer-green-construction.md) as a
regression baseline only  
Computation: [generated Clifford transfer](../computation/10g-clifford-source-euler-transfer/README.md)  
Produces: a generated Clifford wave completion, two-layer minimality refusal,
independently coincident source/Euler multiplier, and a sourced-response interface

## Research contract

- **Upstream anchor:** N10c generates `R=P`, `S=Slash-P Gamma`,
  `Gamma epsilon=0`, and `Gamma^3 psi=0`, but stops before source duality and an
  Euler representative.
- **Bridge question:** does the retained obstruction calculus transfer beyond
  bosonic traces, or must the Clifford multiplier still be imported from N4i?
- **Invariant target:** the same constrained Fang--Fronsdal solutions, gauge
  classes, admissible source, and scalar-wave response before and after the
  transfer.
- **Downstream effect:** success establishes cross-family transfer of one
  source/Euler construction interface; refusal would restrict the tool to the
  bosonic trace algebra.
- **Special resources:** the complex Dirac--Fischer pairing, the symmetric
  spinor-tensor carrier, four-dimensional Clifford relations, and the generated
  gamma constraints.
- **Internal benchmark:** generate `B` from the actual returned `S`; independently
  solve source and adjoint obstructions without a supplied multiplier; require a
  cheaper-budget refusal; consume the result in one sourced response; stop before
  another carrier family.
- **Horizon:** a Majorana or other reality structure, Grassmann variation,
  positivity, quantization, interactions, arbitrary Lorentz carriers, and a claim
  of cheaper single-instance prediction are outside this node.

## 1. The equation generates the missing completion

The construction starts from N10c's returned operation, not N4i's finished data:

```text
S=Slash-P Gamma.                                      (1.1)
```

The response capability requires a scalar-wave completion. Compute the failure of
the cheapest composite `S^2` using the same input field:

```text
Q-S^2
 =2P A-P Slash Gamma-P^2Gamma^2
 =2P[A-(1/2)Slash Gamma-(1/2)P Gamma^2].              (1.2)
```

Every residual channel begins with the generated gauge map `P`. The constructor
strips that common map and normalizes the contraction head to one. This produces

```text
B=A-(1/2)Slash Gamma-(1/2)P Gamma^2,                  (1.3)

S^2+2PB=Q.                                            (1.4)
```

The coefficient `2` is also output: it is the contraction-head coefficient in the
factored residual. Thus `B` is not supplied as a Bianchi ansatz. A second composite
then returns

```text
BS=(1/2)P^2Gamma^3,                                   (1.5)
```

which vanishes on the generated field carrier. Equations (1.2)--(1.5) turn the
local equation into a scalar-wave response interface before any source multiplier
is considered.

## 2. Source conservation forces two gamma layers

Let `Y` be gamma insertion, constructed as the Fischer adjoint of gamma trace.
The physical source condition is the constrained adjoint of the gradient. We seek
a normalized rank-preserving map `M` such that

```text
<P epsilon,M psi>=<epsilon,B psi>,
Gamma epsilon=0.                                      (2.1)
```

Equivalently, `A M-B` may contain terms beginning with `Y`, because moving that
`Y` to the parameter slot produces `Gamma epsilon=0`.

The identity candidate leaves two visible channels:

```text
A-B=(1/2)Slash Gamma+(1/2)P Gamma^2.                  (2.2)
```

One correction layer `Y Gamma` can cancel the first but not the second. The exact
solver therefore refuses the basis `{I,Y Gamma}`. The obstruction itself requests
the next admissible layer. Write

```text
M=I+aY Gamma+bY^2Gamma^2.                             (2.3)
```

Using only

```text
A Y=Y A+Slash,
A Y^2=Y^2A+2P,                                       (2.4)
```

and quotienting the leading-`Y` terms, evaluation on the same field gives

```text
A M-B
 =(a+1/2)Slash Gamma+(2b+1/2)P Gamma^2
   +aY A Gamma+bY^2A Gamma^2.                        (2.5)
```

The visible channels independently force

```text
a=-1/2,
b=-1/4,                                               (2.6)

M_source=I-(1/2)Y Gamma-(1/4)Y^2Gamma^2.              (2.7)
```

The surviving terms begin with `Y`, so (2.1) follows by an explicit pairing
calculation. The second gamma layer is therefore a constructed resource, not a
copy of the textbook trace reversal.

## 3. The Euler obstruction independently returns the same map

For an Euler equation, the cheapest normalized candidate is `E_0=S`. Its formal
adjoint is

```text
S^dagger=Slash-YA,
S-S^dagger=YA-P Gamma.                                (3.1)
```

The residual is visible on `ker Gamma^3`, so the identity budget fails. For a
candidate multiplier `M`, the constructor now solves

```text
M S-S^dagger M=0                                      (3.2)
```

modulo words beginning with `Y^3` or ending with `Gamma^3`; these are exactly the
two field-constraint ideals in the pairing. The correction images are calculated,
not prescribed:

```text
delta(Y Gamma)
 =2YA-2P Gamma-Y P Gamma^2+Y^2A Gamma,

delta(Y^2Gamma^2)
 =2Y P Gamma^2-2Y^2A Gamma
   -Y^2P Gamma^3+Y^3A Gamma^2.                       (3.3)
```

One layer again leaves the independent pair
`{Y P Gamma^2,Y^2A Gamma}` and is refused. Exact elimination with two layers
returns

```text
M_action=I-(1/2)Y Gamma-(1/4)Y^2Gamma^2.              (3.4)
```

Only after both constructions finish do we compare their outputs:

```text
M_action=M_source=M.                                  (3.5)
```

The ambient residual is not falsely reported as zero:

```text
M S-S^dagger M
 =(1/4)(Y^2P Gamma^3-Y^3A Gamma^2).                   (3.6)
```

The first term vanishes on the second field slot; moving `Y^3` in the second term
to the first slot makes it vanish there. Hence `E=MS` is formally self-adjoint on
the constructed carrier.

## 4. The generated object remains usable

The gamma--Fischer decomposition, constructed in N4i, is now used only as an
inverse algorithm for the returned map:

```text
psi=h_0+Yh_1+Y^2h_2,
Gamma h_j=0,

M_n^(-1)psi
 =h_0-(1/n)(Yh_1+Y^2h_2),       n>=1.                (4.1)
```

At `n=0`, `M_0=I`. Thus the constructor does not discard its proof and leave an
implicit inverse.

For a compact physical source `J`, set

```text
K=M^(-1)J,
psi_J=S G_Q K.                                        (4.2)
```

The generated constrained-adjoint identity turns source conservation into
`BK=0`. Applying the generated completion (1.4) to this same `K` computes

```text
S psi_J
 =S^2G_QK
 =(Q-2PB)G_QK
 =K,

E psi_J=M K=J.                                        (4.3)
```

The bounded executable consumer constructs a nonzero rank-two `K in ker B`, forms
`J=MK`, and obtains

```text
||E psi_J-J||=4.44e-16,
||BK||=5.55e-17,
source-conservation residual=2.22e-16.                (4.4)
```

Finite matrix realizations independently check ranks `1--4` at null and non-null
momenta. Their largest reported residual is `7.11e-15`. These matrices are a
regression backend; the invariant obstruction computation owns the construction.

## 5. Global verdict and stop condition

```text
generated Clifford equation S
  -> its wave obstruction generates B
  -> source obstruction  --two layers--> M_source
  -> Euler obstruction   --two layers--> M_action
  -> M_source=M_action
  -> inverse plus sourced scalar-wave response.        (5.1)
```

This is a genuine transfer result. The same retained capability interface now
works in the bosonic trace and fermionic Clifford grammars, while allowing their
different constraint depths and coefficients to be computed rather than unified
by analogy. It passes regression, bounded refusal, cross-family transfer, and one
downstream use.

It still does not make a single familiar free-field response cheaper than the
hand-derived route. [N10h](10h-carrier-to-grammar.md) now derives its primitive and
adjoint grammars once the symmetric spinor-tensor presentation is declared. The
remaining upstream choice is therefore sharper:

```text
physical representation
  -?-> chosen off-shell carrier presentation
  -> generated natural-operator grammar
  -> retained obstruction solver
  -> local equation/source/response.                  (5.2)
```

Further trace or gamma examples would not change the supported claim, so this
branch stops. Re-enter source/Euler transfer only for a selected carrier whose
adjoint ideal cannot be expressed by the present bounded layer grammar, or when
real fermionic action data become a downstream requirement.

## Edges

- `N10c -> N10g`: the generated Clifford complex supplies `R`, `S`, and both gamma
  constraints without supplying `B` or `M`.
- `N4i -> N10g`: the hand construction supplies regression identities and the
  already constructed gamma--Fischer inverse semantics, not expected coefficients.
- `N10f/N10g -> next representation-to-grammar bridge`: pass the common typed
  capability and the two different successful operator grammars; the next node
  must generate those grammars from carrier data or return a bounded obstruction.
