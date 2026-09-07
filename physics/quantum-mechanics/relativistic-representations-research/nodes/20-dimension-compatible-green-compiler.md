# Green and semantic-integrand compiler

Status: a dimension-compatible spin-two Green family and exact two-denominator
lowering are generated; renormalized packet evaluation remains open

## Obstruction

The Ward-closed packet still needs an internal contraction compatible with the
regulator dimension, followed by analytic lowering that does not re-expand tensor
components. Spin two is the stress test because gauge projection, trace reversal,
dimension continuation, and contact closure meet in the same calculation.

## Generate the gauge contraction

At momentum `q`, define `Q=<q,q>`,

```text
R_qxi=q tensor xi+xi tensor q,
A_qh=i_qh,  Th=tr h,  P_qc=cq.
```

Since `A_qR_qxi=Qxi+<q,xi>q` and `TR_qxi=2<q,xi>`, solving
`F_q=A_q+cP_qT` for a scalar composite generates

```text
F_q=A_q-P_qT/2,  F_qR_q=QI.                    (20.1)
```

For `Q!=0`, this constructs

```text
P_g=R_qQ^(-1)F_q,  P_t=I-P_g,
P_g^2=P_g,  F_qP_t=0,  P_tR_q=0.               (20.2)
```

Metric insertion obeys `TU=dI`. Trace reversal

```text
M_d=I-UT/2
```

is not an involution away from four dimensions:

```text
M_d^2=I+(d-4)UT/4.
```

Solving `M_d(I+cUT)=I` instead gives

```text
M_d^(-1)=I-UT/(d-2),  d!=2,                    (20.3)
```

with `d=2` a generated refusal.

The invariant Euler symbol

```text
E_q=QI-R_qA_q+P_q^2T+U(A_q^2-QT)
```

satisfies `E_qR_q=0` and, on `F_qh=0`, `E_qh=QM_dh`. In the trace-reversed
pairing this yields

```text
K_q=M_d^(-1)E_q=QP_t,
G_t=Q^(-1)P_t.                                  (20.4)
```

For gauge parameter `alpha!=0`,

```text
L_alpha=K_q+alpha^(-1)R_qF_q,
G_alpha=G_t+alpha R_qQ^(-2)F_q,
L_alphaG_alpha=I.                               (20.5)
```

Moreover `G_alpha-G_beta` is gauge exact. A boundary-value realization must keep
`D_1=[(Q+i0)^(-1)]`, `D_2=[(Q+i0)^(-2)]` together with
`QD_1=1`, `QD_2=D_1`; multiplying singular factors independently is refused.

## Lower the invariant numerator

Let external momentum be `p`, internal scalar momentum `k`, spin-two momentum
`q=p-k`, and

```text
P=<p,p>,  K=<k,k>,  S=<p,k>,  mu=m^2.
```

The action-generated current is

```text
j=p tensor k+k tensor p-U(S-mu).
```

Invariant contraction gives

```text
<j,j>=2PK+2S^2-4(S-mu)S+d(S-mu)^2,
Tj=2S-d(S-mu).
```

Applying (20.3) and collecting—not expanding components—produces

```text
N_d=<j,j>-(Tj)^2/(d-2)
   =2PK+4mu S-2d mu^2/(d-2).                   (20.6)
```

The propagators define

```text
A=K-mu,
B=P+K-2S,
K=A+mu,
S=(P+A+mu-B)/2.
```

Substitution into the same numerator constructs

```text
N_d=2(P+mu)A-2mu B+C_B(P),
C_B(P)=4Pmu-4mu^2/(d-2),

N_d/(AB)=C_B(P)/(AB)-2mu/A+2(P+mu)/B.          (20.7)
```

Thus the two-cubic graph lowers exactly to

```text
C_B(P)I_(1,1)(P)-2mu I_(1,0)+2(P+mu)I_(0,1).  (20.8)
```

Dimensional regularization makes `I_(0,1)=integral d^dl/l^2=0`; the contact
packet’s scale-free massless tadpole vanishes only after its Ward role has been
retained. The unresolved analytic output is therefore

```text
Sigma_red(P)=C_B(P)I_(1,1)(P)-2mu I_(1,0).     (20.9)
```

The tadpole is local. Feynman parameterization of the bubble gives

```text
1/(AB)=integral_0^1 dx[xA+(1-x)B]^(-2),
xA+(1-x)B=l^2-x[mu-(1-x)P],                    (20.10)
```

so its nonlocal threshold begins at `P=mu`.

## Retained interface and boundary

```text
CompileGreenAndLower(d, action symbol, boundary law, packet numerator)
 -> projectors + Green homotopy + gauge-exact difference
    + master sectors + scaleless flags + zero reconstruction residual
 | refusal(d=2, incompatible boundary, or irreducible higher numerator).
```

The exact certificate records degree two before trace collection, affine degree
afterward, three sectors generated, two retained, and zero reconstruction
residual. This is semantic compression, not yet a whole-route advantage over an
expert one-loop reduction. [Node 22](22-bubble-spectral-boundary.md) constructs
the common bubble boundary and tests the requested observables.
