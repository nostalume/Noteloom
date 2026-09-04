# N10k — Generated Sourced-Curvature Transport

Status: supported as a potential-derived causal curvature operation for every
separate finite positive integer spin in four-dimensional flat spacetime; an
unrestricted first-order curvature-source Green interface is obstructed; N10l
constructs the compatible direct-curvature source complex selected by that defect

Consumes: [N4 direct chiral symbols](04-local-symbol-extension.md),
[N4f finite-spin causal construction](04f-finite-integer-spin-green-construction.md),
[N10e generated source adapter](10e-generated-source-adapter.md), and
[N10j generated curvature compatibility](10j-generated-curvature-compatibility.md)

Computation: [sourced curvature transport](../computation/10k-sourced-curvature-transport/README.md)

Produces: a retained physical-source-to-curvature response, exact two-route and
causal-quotient certificates, a channel-load comparison, and a typed refusal of an
arbitrary direct-curvature source Green operation

## Research contract

- **Upstream anchor:** N10e turns a compact conserved physical current into an
  admissible scalar-wave source; N10j turns a potential into its gauge-invariant
  chiral curvature.
- **Bridge question:** can the generated curvature map be used before or after
  causal propagation without changing the sourced observable, and does that give
  the direct chiral presentation an independent source theory?
- **Invariant target:** the same compact current class `[J]` and the same resulting
  chiral curvature distribution.
- **Downstream effect:** separate a reusable curvature-output operation from the
  stronger, presently unsupported claim that curvature has its own unrestricted
  causal source interface.
- **Special resources:** flat constant-coefficient operators, the componentwise
  scalar retarded/advanced wave distributions, compact sources, and N4f's causal
  exact sequence.
- **Internal benchmark:** consume N10e's spin-two current, prove equality of both
  routes and source-quotient descent, then compare complete formal channel load for
  spins `1--6` and refuse the stronger direct-source request where its symbol rank
  fails.
- **Horizon:** no interacting, curved, half-integer, countable-spin, regularized,
  or numerical runtime claim is included.

## 1. “Curvature first” names two different operations

Let N10e supply a compact physical current and its adapted source,

```text
R_s^dagger J=0,
S=M_s^(-1)J,
C_sS=0.                                                (1.1)
```

N4f then constructs the potential response

```text
phi_J^+/-=G_(F,s)^+/-S,                                (1.2)
```

and N10j supplies the generated order-`s` operation

```text
K_s:F_s -> Curv_s,
K_sR_s=0.                                              (1.3)
```

The first admissible curvature output is therefore

```text
mathcal C_J^+/-=K_sG_(F,s)^+/-M_s^(-1)J.               (1.4)
```

Equation (1.4) is already gauge invariant and sourced. It does not yet say that
the first-order chiral equation from N4 accepts arbitrary curvature sources. The
present node keeps these capabilities distinct:

```text
potential-derived curvature transport
  != independent direct-curvature source theory.       (1.5)
```

## 2. The common scalar Green operation constructs a second route

Let `g^+/-` be the scalar retarded/advanced fundamental distribution used by N4f.
Tensoring it with the identity on `Curv_s` constructs

```text
G_(Curv,s)^+/-=g^+/- tensor identity_(Curv_s).          (2.1)
```

This is a scalar-wave Green operation on the curvature carrier, not a Green
operation for N4's first-order chiral equation. Since `K_s` has constant
coefficients, differentiation commutes with convolution on the same compact input
`S`. Evaluating both composites gives

```text
K_sG_(F,s)^+/-S
 =K_s(g^+/- * S)
 =g^+/- * (K_sS)
 =G_(Curv,s)^+/-K_sS.                                  (2.2)
```

Both sides of (2.2) are curvature-valued distributions with the same support
prescription. This constructs the two-route operation

```text
potential first:
  J -> S -> G_F^+/-S -> K_sG_F^+/-S,

curvature transport first:
  J -> S -> K_sS -> G_Curv^+/-K_sS.                    (2.3)
```

It also computes the sourced scalar-wave equation

```text
Q mathcal C_J^+/-=K_sS.                                (2.4)
```

The executable constructor retains (2.3) rather than discarding it after checking
(2.2). Missing convolution or causal-exactness resources produce a refusal.

## 3. The causal output descends to the physical source quotient

N4f identifies physical compact sources modulo Euler-equation sources. Let

```text
J' =J+E_sa,
E_s=M_sD_s.                                            (3.1)
```

Applying the same adapter to the same shift computes

```text
M_s^(-1)J'=S+D_sa.                                     (3.2)
```

N10c gave `D_s=Q-R_sC_s`, while N10j gave `K_sR_s=0`. Because `K_s` commutes with
the scalar wave operator, evaluation on `a` gives

```text
K_sD_sa
 =K_s(Qa-R_sC_sa)
 =QK_sa.                                               (3.3)
```

Let `Delta_Curv=G_Curv^+-G_Curv^-`. The scalar causal exact sequence gives
`Delta_Curv Q=0`; substituting (3.3) into the shifted output yields

```text
Delta_Curv K_s(S+D_sa)-Delta_Curv K_sS
 =Delta_Curv K_sD_sa
 =Delta_Curv QK_sa
 =0.                                                   (3.4)
```

Thus the retained causal operation is genuinely defined on the source class:

```text
[J] |-> Delta_Curv K_sM_s^(-1)J.                       (3.5)
```

Retarded and advanced fields themselves change under (3.1); only their causal
difference has the exact quotient invariance (3.4). The tool records this boundary
instead of promoting representative equality into a quotient theorem.

## 4. The existing spin-two source is an actual consumer

N10e constructs, from one compact bump and two constant bivectors, a conserved
spin-two current `J` whose unadapted constraint fails and whose adapted source
`S=M_2^(-1)J` succeeds. Its null-shell screen contrast is nonzero. Applying the
returned N10j packet gives

```text
[J]
 -> S
 -> Delta_(F,2)S
 -> K_2Delta_(F,2)S
 =Delta_(Curv,2)K_2S.                                  (4.1)
```

N10j proves that `K_2` is an isomorphism on the two physical screen lines, so the
nonzero N10e helicity-two class remains nonzero in (4.1). This is the use test: the
generated adapter and curvature operation are consumed together to produce a
causal, gauge-invariant output without reconstructing either proof.

The result is interoperability, not a new observable prediction. Both sides of
(4.1) use the same current, scalar fundamental distribution, and curvature map.

## 5. Why this is not yet the direct chiral causal theory

For one chirality, N4's first-order zero-rest-mass symbol has type

```text
Z_s:Sym^(2s)(S)
  -> Sym^(2s-1)(S) tensor bar S.                        (5.1)
```

The two carrier dimensions are

```text
dim domain(Z_s)=2s+1,
dim codomain(Z_s)=4s.                                  (5.2)
```

For every `s>=1`, (5.2) makes `Z_s(p)` unable to be surjective. After adjoining
the conjugate chirality, an arbitrary equation-source interface has pointwise
surjectivity defect

```text
8s-(4s+2)=4s-2.                                        (5.3)
```

Consequently there can be no symbolwise right inverse, hence no unrestricted
translation-invariant Green operation satisfying `Z_sG=id` on all compact
equation sources. Curvature sources must obey compatibility conditions. This rank
calculation does not forbid a Green operation on a constructed compatible source
space; it proves that such a source space and its compatibility map are mandatory.

The transported source `K_sS` in (2.4) is automatically in the potential-derived
image, but the present packets do not yet construct an off-shell identity relating
`Z_sK_s` to the potential constraint/source operations. Therefore (2.4) must not be
renamed a sourced version of (5.1). The constructor returns this missing
compatibility complex as a typed refusal.

## 6. Whole-route cost gives a limited result

The two routes share source adaptation, one scalar Green application, one order-`s`
curvature operation, support handling, and observable recovery. Only the carrier on
which the scalar Green operation is applied changes:

```text
dim F_s=2s^2+2,
dim Curv_s=4s+2.                                       (6.1)
```

| Spin | Potential Green channels | Curvature Green channels | Formal verdict |
| ---: | ---: | ---: | --- |
| `1` | `4` | `6` | potential is smaller |
| `2` | `10` | `10` | equal |
| `s>=3` | `2s^2+2` | `4s+2` | curvature transport is smaller |

This is conditional channel compression from spin three onward, not established
runtime leverage. Applying `K_s` before propagation differentiates the compact
source to order `s`; regularity, high-frequency amplification, conditioning,
storage layout, and the cost of recovering the requested observable remain in the
complete route. On the actual spin-two consumer the channel load is exactly equal,
so no computational gain is claimed.

## 7. Retained interface and global boundary

The generated operation is

```text
SourcedCurvatureUse(
  generated FieldSystem,
  source adapter,
  curvature packet K_s,
  scalar causal Green resources,
  requested capability)
 -> source-to-curvature operations,
    route-equality and causal-quotient certificates,
    support and shell certificates,
    whole-route channel record,
    or a typed compatibility refusal.                   (7.1)
```

The supported spine is now

```text
generated potential equation and source adapter            [N10c/N10e]
  -> generated gauge-invariant curvature                   [N10j]
  -> same sourced curvature by two scalar-wave routes       [N10k]
  -> direct first-order arbitrary-source request
  -> rank obstruction and compatible-source obligation         [N10k]
  -> internally constructed compatible source complex and
     verified causal operation.                                [N10l]
```

This meets the declared bench and stops the transport branch. Further scalar-wave
examples would not alter the verdict. N10l consumes its re-entry condition: it
constructs the smallest compatible source carrier and the off-shell identity for
`Z_sK_s`, then compares the direct-curvature and transported routes on the same
source class and observable.

## Edges

- `N4f/N10e -> N10k`: pass the scalar causal operation and physical-source adapter.
- `N10j -> N10k`: pass `K_s` as a retained operation, not its proof prose.
- `N4 -> N10k`: pass the direct first-order chiral symbol whose unrestricted source
  interface is tested and refused.
- `N10k -> N10l`: pass the defect `4s-2`, the transported admissible image, and the
  off-shell intertwining obligation.
- `N10k -> N10t`: pass causal commutation, the common curvature response, and the
  formal carrier-channel comparison to an observable-visible batch compiler.
