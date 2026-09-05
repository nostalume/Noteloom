# Semantic integrand lowering

Status: exact two-point denominator quotient supported; node 22 consumes the sole
nonlocal bubble and rejects isolated-pole recovery at its touching threshold

## Capability and spine binding

Node 19 constructs the relatively Ward-closed packet

```text
Pi_2^1PI=Gamma_CC-Gamma_D/2,
```

and node 20 supplies a dimension-compatible spin-two Green family. Those results
still leave an unresolved analytic expression. This node asks whether the packet's
finite-fiber expression can be transformed into a smaller analytic object before
integration.

- **Upstream anchor:** the action-generated cubic/contact jet, Ward lift, and
  dimension-`d` trace-reversed Green edge from nodes 19--20.
- **Bridge question:** does invariant Ward reduction turn the loop numerator into a
  bounded denominator algebra rather than merely rename a tensor integral?
- **Invariant target:** the same order-`kappa^2` scalar two-point kernel and external
  inverse-kernel quotient.
- **Downstream effect:** separate the local renormalization sector from the one
  nonlocal kernel and test whether it supports both pole and continuum recovery.
- **Special resources:** flat background, minimal scalar metric action, one massless
  spin-two edge, one massive scalar edge, de Donder representative after packet
  closure, and dimensional regularization.
- **Rejoin edge:** exact coefficients of the surviving scalar integral sectors plus
  a reconstruction certificate and refusal boundary.

The horizon ends before evaluating or subtracting the master integrals. Generic
multi-leg and multiloop integration-by-parts reduction is not part of this bench.

## Construct the numerator from the current

Let `p` be the external scalar momentum and `k` the internal scalar momentum. The
spin-two edge carries `q=p-k`. Retain only invariant scalars

```text
P=<p,p>,        K=<k,k>,        S=<p,k>,        mu=m^2.
```

The cubic action polynomial in node 19 can be represented, after stripping its
overall vertex normalization, by the symmetric current

```text
j(p,k)=p tensor k+k tensor p-U(S-mu).
```

Indeed, pairing `j/2` with a symmetric metric deformation `H` gives

```text
<j/2,H>=<p,Hk>-(tr H)(S-mu)/2=C(H;k,p).
```

Thus `j` is not an imported stress-tensor rule; it is the tensor representing the
already generated cubic action map. The overall factor `1/2` remains in the
declared coupling normalization and does not change the integral sectors.

Put `c=S-mu`. The symmetric pairing evaluates the current square without choosing
components:

```text
<j,j>
  =2 P K+2 S^2-4cS+d c^2,

Tj=2S-dc.
```

Node 20 generated the trace-reversal inverse, so its normalized internal edge
constructs

```text
N_d(P,K,S,mu)
  =<j,j>-(Tj)^2/(d-2),            d != 2.
```

Substitute the two calculated expressions into the same scalar target:

```text
(d-2)N_d
  =(d-2)(2PK+2S^2-4cS+d c^2)
   -(4S^2-4dSc+d^2 c^2)

  =2(d-2)PK+4(d-2)mu S-2d mu^2.
```

Therefore

```text
N_d=2PK+4mu S-2d mu^2/(d-2).       (21.1)
```

The quadratic `S^2` expression has disappeared before integration. This is the
first reduction in this node: trace reversal maps a degree-two carrier contraction
to an affine invariant numerator. Dimension two remains a generated refusal.

## Quotient by the propagator denominators

The two internal edges construct the denominators

```text
A=K-mu,
B=(p-k)^2=P+K-2S.
```

They span both loop invariants. Solve these definitions rather than introduce a
tensor basis:

```text
K=A+mu,
S=(P+A+mu-B)/2.                    (21.2)
```

Substitution of (21.2) into (21.1) computes

```text
N_d
  =2(P+mu)A-2mu B+C_B(P),

C_B(P)=4Pmu-4mu^2/(d-2).           (21.3)
```

Dividing the same equality by `AB` gives the semantic integral reduction

```text
N_d/(AB)
  =C_B(P)/(AB)-2mu/A+2(P+mu)/B.    (21.4)
```

Define only now

```text
I_(a,b)(P)=integral d^d k/(2pi)^d A^(-a) B^(-b).
```

The two-cubic graph therefore requests

```text
C_B(P) I_(1,1)(P)-2mu I_(1,0)+2(P+mu)I_(0,1).   (21.5)
```

No Gram-matrix inversion, component tensor decomposition, or integration-by-parts
search was needed: this one-loop topology has no irreducible scalar product.

## Keep structural and analytic cancellation distinct

In dimensional regularization, shift `l=p-k` in `I_(0,1)`. Its loop expression has
no mass or external scale:

```text
I_(0,1)=integral d^d l/(2pi)^d 1/l^2=0.          (21.6)
```

In the de Donder representative, the contact vertex contains no internal
spin-two momentum and its sole massless loop is another polynomial massless
tadpole. It vanishes by the same rule.

This does **not** permit deleting the contact graph from the graph packet. Before a
regulator is chosen, its variation cancels the internal descendants of the
two-cubic graph. The valid order is

```text
retain contact graph
  -> construct Ward-closed packet
  -> choose the common de Donder/dimensional prescription
  -> classify its analytic sector as scaleless
  -> remove its value while retaining its closure certificate.
```

A cutoff, curved background, massive spin-two edge, or another scale-bearing
prescription need not annihilate this sector. Equation (21.6) is regulator- and
model-bound, unlike the action-jet Ward identity.

After the dimensional prescription, the unresolved analytic output is only

```text
Sigma_red(P)
  =C_B(P) I_(1,1)(P)-2mu I_(1,0),               (21.7)
```

up to the declared coupling and vertex normalization.

## Why the two surviving sectors mean different things

`I_(1,0)` contains no external momentum. It can change local mass/counterterm data
but cannot by itself generate an open-channel discontinuity in `P`.

For the bubble, Feynman parameterization is an equality on the common pair of
denominators:

```text
1/(AB)=integral_0^1 dx [xA+(1-x)B]^(-2).
```

With `l=k-(1-x)p`, direct substitution gives

```text
xA+(1-x)B
  =l^2-x[mu-(1-x)P].               (21.8)
```

The bracket can reach zero for `x in (0,1)` precisely when `P >= mu`. Hence the
bubble carries the massive-scalar plus massless-spin-two threshold. The same
nonlocal function presents two candidate downstream operations:

```text
real/subtracted boundary value -> proposed dressed pole and residue,
discontinuity for P >= mu       -> open-channel spectral weight.
```

This reconnects the graph compiler to nodes 16 and 18, but does not guarantee both
endpoints. Node 22 shows that the continuum touches the proposed pole and rejects
an isolated Fock residue in this bench.

## Retained operation and executable certificate

The workbench retains two operations:

```text
ScalarSpin2Numerator(P,K,S,mu,d)
  -> N_d | refusal(d=2),

TwoPointLower(numerator,K,S,P,mu)
  -> integral sectors
   + scaleless flags
   + exact reconstruction residual
   | refusal(nonpolynomial or denominator degree > 1).
```

The second input does not contain the expected bubble/tadpole coefficients. It
generates them by substituting the two denominator definitions and collecting their
affine quotient. A transfer certificate applies the same map to an arbitrary
affine invariant numerator. A quadratic remainder is exposed rather than passed to
an unrestricted simplifier or hidden behind the name “tensor reduction.”

The current exact certificate records

```text
carrier numerator degree:      2 before trace-reversal collection,
denominator numerator degree:  1,
generated sectors:             3,
dimensionally retained:        2,
reconstruction residual:       0.
```

This is semantic compression and a reusable lowering interface. It is not yet a
whole-route computational advantage over an expert one-loop calculation, who can
also begin with a trace-reversed current and two scalar masters. The stronger claim
requires measured expression size and recovery cost after subtraction.

## Checks, boundary, and next edge

Supported:

- the action-generated current pairing produces (21.1) without components;
- denominator substitution produces (21.3)--(21.5) with zero reconstruction
  residual;
- dimensional scalelessness leaves only a bubble and massive tadpole;
- the bubble threshold begins at `P=mu` and is the only nonlocal sector;
- unrelated affine numerators transfer through the same reducer; and
- dimension two and higher denominator degree return explicit refusals.

Still open after node 22:

- fix the overall Fourier/coupling normalization against the action convention;
- fix the local tadpole subtraction in the declared renormalization convention;
- prove that subtraction preserves the external inverse-kernel ideal;
- replace the rejected isolated-pole target by a dressed/inclusive observable; and
- compare complete invariant and expert-baseline construction costs.

Node 22 constructs the bubble's subtracted spectral boundary and finds that its
continuum touches the scalar shell. Node 23 consumes the same reduced output in a
finite-resolution effect. Generic IBP or a fermionic transfer re-enters only if the
cut/observable morphism requires analytic structure unavailable to this quotient.

## Materials and edges

- Nodes 19--20 supply the packet, trace-reversal edge, dimension, and boundary
  contract.
- `computation/src/fieldcalc/lowering.py` owns the retained denominator quotient.
- `computation/tests/test_integrand_lowering.py` owns regression, transfer,
  reconstruction, and refusal certificates.
- [Integral reduction contracts](../sources/integral-reduction-contracts.md) bound
  the relation to tensor and master-integral reduction literature.

```text
19 Ward-closed action packet
  + 20 dimension-compatible Green edge
  -> 21 invariant numerator and denominator quotient
  -> 22 subtracted bubble spectral boundary and pole obstruction
  -> 23 resolution-native effect algebra
  -> 16/18 observable-return reuse and realization comparison.
```
