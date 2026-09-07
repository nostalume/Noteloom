# Ward-closed interaction packet

Status: the scalar--spin-two action jet and order-`kappa^2` packet are generated;
internal Ward closure holds modulo the external inverse-kernel ideal

## Obstruction

The conserved on-shell current of node 17 cannot be inserted unchanged into a
loop: its internal scalar momentum is off shell. The failure must generate the
higher interaction and the graph packet before regularization.

## Calculate the off-shell identity

Put `E(p)=Q_p-m^2`, `q=p'-p`, and `s=<p,p'>`. For

```text
J_0(p',p)=P_pP_(p')1-U(s-m^2)/2
```

direct contraction gives

```text
A_qJ_0(p',p)=E(p')P_p-E(p)P_(p').              (19.1)
```

The improvement `I_q=P_q^2-UQ_q` remains divergence-free. Inside a graph,
`E(k)Delta_E(k)=1`, so Ward contraction cancels the adjacent propagator:

```text
Delta_E(k)A_qJ_xi(k,p)=P_p                     (19.2)
```

when the external leg is on shell. This local descendant is the obstruction that
forces a contact operation.

## Generate the action jet

Start from the supplied invariant scalar action

```text
S[g,phi]=1/2 integral [g^(-1)(dphi,dphi)-m^2phi^2]vol_g.
```

Write `g_kappa=eta circle(I+kappa H)`, `t=tr H`, `u=tr(H^2)`. Solving inverse and
volume residuals through second order gives

```text
R_1=-H,  R_2=H^2,
v_1=t/2,  v_2=t^2/8-u/4,

D_1=(t/2)I-H,
D_2=H^2-(t/2)H+(t^2/8-u/4)I.                  (19.3)
```

These coefficients generate `S_0,S_1,S_2`. Gauge invariance under
`delta_xi phi=kappa L_xi phi` and
`delta_xi h=R_0xi+kappa L_xi h` yields, coefficient by coefficient,

```text
D_hS_1[R_0xi]+D_phiS_0[L_xi phi]=0,

D_hS_2[R_0xi]+D_hS_1[L_xi h]
 +D_phiS_1[L_xi phi]=0.                        (19.4)
```

Thus the second vertex is a generated coherence boundary, not a memorized
seagull.

The invariant cubic map is

```text
C(H;p',p)=<p,Hp'>-(tr H)(s-m^2)/2,
```

and substitution of
`R_0(q,xi)=q tensor xi^flat+xi tensor q^flat` reproduces (19.1):

```text
C(R_0(q,xi);p',p)
 =E(p')<p,xi>-E(p)<p',xi>.                     (19.5)
```

Polarization of (19.3) constructs the quartic map through

```text
v_2(H_1,H_2)
 =(tr H_1)(tr H_2)/8-tr(H_1H_2)/4,

D_2(H_1,H_2)
 =(H_1H_2+H_2H_1)/2
 -[(tr H_1)H_2+(tr H_2)H_1]/4
 +v_2(H_1,H_2)I.                               (19.6)
```

## Generate and close the packet

The normalized interaction is

```text
S_int=kappa/(2!1!)C(phi,phi,h)
     +kappa^2/(2!2!)D(phi,phi,h,h)+O(kappa^3).
```

Orbit counting gives cubic--cubic weight `+1` and contact weight `-1/2`, hence

```text
Pi_2^1PI=Gamma_CC-(1/2)Gamma_D.                 (19.7)
```

The packet is invariant under spin-two field rescaling because
`C'=lambda^(-1)C`, `D'=lambda^(-2)D`, and `G'=lambda^2G` cancel in both terms.

For a gauge-exact edge variation

```text
delta G=R_0X+X^dagger R_0^dagger,
```

the two-cubic descendants and the contact term calculate

```text
delta Gamma_CC
 =X_L+X_R-Delta_E(k)[E(p_L)Y_L+E(p_R)Y_R],

delta[-Gamma_D/2]=-X_L-X_R,

delta Pi_2^1PI
 =-Delta_E(k)[E(p_L)Y_L+E(p_R)Y_R]
 in I_ext=<E(p_L),E(p_R)>.                     (19.8)
```

Equivalently, exact residual solving returns

```text
(1,1)+c(2,2)=(0,0) -> c=-1/2.
```

## Retained interface and boundary

```text
WardClosedPacket(action, ports, order, topology request, budget)
 -> canonical typed orbits + generated weights
    + zero internal residual + external ideal witness
    + unresolved analytic kernels and construction cost
 | refusal(missing action jet, failed closure, or budget).
```

The compiler keeps internal closure distinct from observable descent. It does not
claim that the off-shell two-point kernel is physical, nor that dimensional
regularization preserves (19.8). [Node 20](20-dimension-compatible-green-compiler.md)
constructs its Green family and lowers the remaining numerator; [node 24](24-external-ideal-observable-descent.md)
tests the external ideal.
