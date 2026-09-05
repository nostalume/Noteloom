# Dimension-compatible spin-two Green compiler

Status: the rational off-shell family is generated for symbolic `d != 2`; a common
boundary-value algebra is specified, while regulated loop evaluation remains open

## Capability and spine binding

Node 19 constructs a scalar order-`g^2` graph packet whose gauge variation closes
up to the external scalar equations, provided changes of the internal spin-two
Green operator are gauge-exact. This node must generate that Green family and make
it compatible with the dimension parameter used by the candidate regulator.

```text
node 05/13 free invariant operations
  + node 17 spin-two edge and scalar coupling
  + node 19 relative Ward-closed graph packet
  -> dimension-compatible Green compiler
  -> common distributional packet
  -> node 21 semantic integrand lowering
  -> regulated scalar two-point observable and cost comparison.
```

The invariant target is still node 19's scalar two-point packet. We do not switch
to a graviton observable, a vacuum graviton loop, or full nonlinear gravity.

## Why spin two owns this bench

Spin two is selected here for a consequential reason, not because it is the first
or easiest gauge theory. It is the first generated carrier in the active spine for
which all three compiler layers meet:

1. the representation/local-symbol branch supplies a reducible covariant field and
   a vector-valued gauge map;
2. the scalar metric action jet supplies both cubic and contact graph vertices;
3. the graph branch needs a gauge-dependent internal edge but must recover a
   gauge-independent external quotient.

A scalar exchanged field would test graph enumeration but not the gauge quotient.
A spin-one field would test the simpler relation `div grad=Q`, but it would not test
whether trace, pairing, and dimension-dependent carrier operations survive the
algebra-to-graph bridge. Spin two forces the framework to retain these otherwise
hidden obligations:

```text
trace correction in the gauge detector,
trace-reversed action pairing,
dimension-dependent inverse of trace reversal,
contact vertices from the same metric action,
and a graph packet closed only modulo external equations.
```

Success is therefore a stress test for the claimed compiler composition. It is not
evidence that spin-two physics is universally primary, and it is not yet a claim of
computational advantage over an expert gravity calculation.

## Horizon

Construct the free spin-two Green family without a component tensor inverse and
show that its algebra survives symbolic dimension and one common boundary-value
prescription. Stop before evaluating or renormalizing the loop. Re-enter the graph
calculation only when the regulator can preserve the same packet identity and
external ideal.

## Generate the gauge detector

At momentum `q`, let

```text
Q=<q^sharp,q^sharp>,

R_q xi=q tensor xi+xi tensor q,

A_q h=i_(q^sharp)h,       T h=tr_g h,

P_q c=cq,                P_q^2 c=c(q tensor q).
```

`R_q` generates a pure-gauge symmetric tensor. Contraction does not detect it as a
scalar wave operator because, with `r=<q^sharp,xi>`,

```text
A_q R_q xi=Q xi+r q,

T R_q xi=2r.
```

Search `F_q=A_q+c P_q T` for a detector whose composite with `R_q` has no `q`
component. Substitution gives

```text
F_q R_q xi
  =Q xi+(1+2c)r q.
```

The obstruction coefficient vanishes only at `c=-1/2`. Therefore

```text
F_q=A_q-P_q T/2,       F_q R_q=Q I_G.        (20.1)
```

For `Q != 0`, (20.1) generates

```text
P_g=R_q Q^(-1)F_q,       P_t=I-P_g.          (20.2)
```

The projector and annihilation laws are computations, not names:

```text
P_g^2
  =R_q Q^(-1)(F_q R_q)Q^(-1)F_q
  =P_g,

F_q P_t=F_q-(F_q R_q)Q^(-1)F_q=0,

P_t R_q=R_q-R_q Q^(-1)(F_q R_q)=0.           (20.3)
```

Thus `P_g` retains the gauge orbit direction and `P_t` retains the de Donder
representative. Their sum remains the same covariant field.

## Generate trace reversal at symbolic dimension

Let metric insertion satisfy the carrier law

```text
T U=d I.
```

The de Donder detector factors as `F_q=A_q M_d` with

```text
M_d=I-U T/2.
```

At fixed four dimensions, `M_4` is an involution. A dimensionally continued
calculation cannot silently reuse that fact:

```text
M_d^2
  =I-U T+(U T U T)/4
  =I+(d-4)U T/4.                              (20.4)
```

The workbench therefore solves an inverse rather than assuming an involution. Put
`M_d^(-1)=I+c U T`. Then

```text
M_d(I+c U T)
  =I+[c-1/2-cd/2]U T.
```

Setting the residual coefficient to zero gives

```text
c=-1/(d-2),

M_d^(-1)=I-U T/(d-2),       d != 2.           (20.5)
```

Dimension two is a generated refusal: the trace sector has no inverse under this
presentation. At `d=4`, (20.5) returns `M_4`, recovering the familiar involution as
a regression value rather than a premise.

## Generate the transverse inverse from the action

The scalar metric coupling needs the spin-two Euler symbol in the ordinary tensor
pairing. The invariant operations produce

```text
E_q=Q I-R_q A_q+P_q^2 T+U(A_q^2-Q T).        (20.6)
```

Two evaluations determine its relevant action. First,

```text
E_q R_q xi
  =Q R_q xi-R_q(Q xi+r q)+2rP_q^2
   +U(2Qr-2Qr)
  =0.                                         (20.7)
```

Second, if `F_q h=0`, then `A_q h=P_q T h/2`, so

```text
E_q h
  =Qh-R_q(P_q T h/2)+P_q^2 T h
   +U(Q T h/2-Q T h)
  =Q M_d h.                                   (20.8)
```

Use the action pairing `<h,k>_(M_d)=<h,M_d k>_0`. In that pairing the same Euler
bilinear form is represented by

```text
K_q=M_d^(-1)E_q.
```

Equations (20.3), (20.7), and (20.8) evaluate `K_q` on both summands:

```text
K_q P_g=0,       K_q P_t=Q P_t,

K_q=Q P_t,       G_t=Q^(-1)P_t.              (20.9)
```

The transverse inverse is therefore generated for every symbolic `d != 2`; it is
not hidden behind a four-dimensional propagator numerator.

The adjoint relation also keeps its normalization visible. With the unnormalized
symmetric product and the declared pairings,

```text
R_q^ddagger=2F_q.                              (20.10)
```

The factor two affects conventions but not the projectors or gauge-exact homotopy.

## Generate the rational Green family

For nonzero gauge parameter `alpha`, define

```text
L_alpha=K_q+alpha^(-1)R_q F_q,

G_alpha=G_t+alpha R_q Q^(-2)F_q.             (20.11)
```

Using `K_qG_t=P_t`, `K_qR_q=0`, `F_qG_t=0`, and (20.1),

```text
L_alpha G_alpha
  =P_t+0+0+R_q Q^(-1)F_q
  =P_t+P_g
  =I.                                         (20.12)
```

The right inverse follows by the declared adjoint pairing. Gauge variation requires
no new inverse:

```text
G_alpha-G_beta
  =(alpha-beta)R_q Q^(-2)F_q
  =R_q X+X^ddagger R_q^ddagger,

X=(alpha-beta)Q^(-2)F_q/2.                   (20.13)
```

This is exactly the homotopy consumed by node 19. The factor two in (20.10)
cancels between `X^ddagger` and `R_q^ddagger`.

## Retain the composite boundary value

The rational notation in (20.11) is valid only off the characteristic set. Do not
assign independent meanings to its inverse powers and multiply singular objects
afterward. Supply one common boundary prescription with tokens

```text
D_1=[(Q+i0)^(-1)],       D_2=[(Q+i0)^(-2)]
```

and the multiplication laws

```text
Q D_1=1,       Q D_2=D_1.                    (20.14)
```

Keep the numerator and double-pole token as the typed composite `R_q D_2 F_q`.
The distributional Green request becomes

```text
mathcal G_alpha
  =D_1 I+(alpha-1)R_q D_2 F_q.               (20.15)
```

To verify it without components, put `N=R_qF_q`. Equation (20.1) gives

```text
N^2=R_q(F_qR_q)F_q=Q N.
```

Also

```text
L_alpha=Q I+(alpha^(-1)-1)N.
```

Multiplying with (20.15) and applying (20.14), the identity coefficient is one and
the coefficient of `N D_1` is

```text
(alpha-1)+(alpha^(-1)-1)
 +(alpha-1)(alpha^(-1)-1)=0.                 (20.16)
```

Thus `L_alpha mathcal G_alpha=I` in the common boundary-value algebra. This is not
yet a renormalized loop result: (20.14) is an admission contract that a concrete
prescription and regulator must realize.

## Regulator-facing compiler contract

Dimension continuation must begin before trace identities are simplified. The
compiler receives

```text
(d, metric carrier laws, R_q, action Euler symbol,
 boundary prescription, gauge parameter, resource budget)
```

and returns

```text
(M_d, M_d^(-1), P_g, P_t, K_q,
 mathcal G_alpha,
 inverse and homotopy certificates,
 singular-dimension refusal,
 unresolved regulator obligations).
```

The graph compiler may consume this output only if its regulator:

1. uses the same symbolic `d` in trace laws, action vertices, and loop measure;
2. preserves the common relations (20.14), or returns their breaking residual;
3. acts on the already Ward-closed packet, not on a cubic graph in isolation;
4. preserves the external inverse-kernel ideal through subtraction and recovery.

Dimensional regularization is the current candidate because it continues the
dimension appearing in (20.4)--(20.6), but its suitability for this packet remains
a proposition to test. The classic gauge-field construction and action-principle
results are theorem contracts for the analytic method; they do not replace the
packet-level calculation.

## Checks and boundary

Supported now:

- exact residual solving generates `M_d^(-1)` and refuses `d=2`;
- `d=4` recovers involutive trace reversal;
- invariant evaluation generates `F_qR_q=Q`, the projectors, and `K_q=QP_t`;
- the rational Green family is a two-sided inverse under the declared pairing;
- every gauge-parameter difference is gauge-exact;
- the common distribution algebra proves the inverse coefficient cancellation in
  (20.16) before loop integration.

Still open:

- consume node 21's exact two-sector denominator quotient in one explicitly
  subtracted scalar two-point packet;
- test whether subtraction preserves zero internal Ward residual and the external
  ideal;
- compare maximum tensor rank, expression growth, and master kernels with an expert
  component/Ward baseline for the same observable.

Reject the regulator if it requires restoring the packet identity by hard-coded
diagram-specific counterterms without returning the breaking residual. Reject the
computability claim if the complete invariant route does not reduce construction,
reduction, integration, or recovery cost.

## Materials and edges

- Node 19 supplies the graph packet and exact homotopy shape it consumes.
- `computation/tests/test_gauge_homotopy.py` certifies the projector, trace inverse,
  rational inverse, external quotient, and boundary-algebra coefficient laws.
- `sources/finite-spin-green-contracts.md` supplies the Green-hyperbolic boundary.
- `sources/action-principle-contracts.md` supplies the dimensional-regularization
  and action-principle theorem boundary.

Edges:

```text
05/13 invariant carrier operations
  + 17 action-generated spin-two coupling
  + 19 relative Ward-closed packet
  -> 20 dimension-compatible Green compiler
  -> 21 semantic integrand lowering
  -> regulated packet evaluator
  -> 16/12 certified observable window.
```
