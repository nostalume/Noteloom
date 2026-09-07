# Off-shell resolution and physical transfer

Status: off-shell propagation is constructed as internal homotopy transfer and
validated by scalar QED; loop-level physical compression remains open

## Obstruction

Treating a Green kernel as the observable led to node 24’s characteristic failure.
The prior question is what off-shell space does before integration. The answer must
distinguish internal resolution from external physical cohomology.

## Construct virtuality and contraction

External data satisfy `K(k_i)u_i=0`. A partial local composite carries

```text
p_S=sum_(i in S)k_i,
omega_S=K(p_S)u_S.                              (25.1)
```

`omega_S` is the kinetic defect of composition, not a new state. On a generic
internal stratum a homotopy `h` resolves it by

```text
K(p_S)h(p_S)omega_S=omega_S.                    (25.2)
```

More generally, for the free complex `(C,d)` with physical cohomology `H`, choose

```text
pi i=I_H,
dh+hd=I_C-i pi.                                 (25.3)
```

Every cochain decomposes as

```text
c=i pi(c)+dh(c)+hd(c).
```

The identity cannot hold as an inverse on a characteristic external channel where
cohomology survives; that is precisely the boundary found in node 24.

## Generate transferred operations

For interaction maps `ell_r`, write

```text
F(a)=sum_(r>=2)ell_r(a,...,a)/r!,
da+F(a)=0.
```

Using (25.3) and the gauge choice `ha=0` gives the constructive iteration

```text
a_(n+1)=ix-hF(a_n),
F_H(x)=pi F(a[x])=0.                            (25.4)
```

At cubic order,

```text
T_3(x_1,x_2,x_3)
 =-sum_cyclic pi ell_2(ix_1,h ell_2(ix_2,ix_3)). (25.5)
```

Thus a decorated tree has semantic roles

```text
external leg -> i,
local vertex -> ell_r,
internal edge -> h,
physical readout -> pi.
```

A Schwinger representation may subsequently turn each internal contraction into a
metric-graph coordinate,

```text
K_e^(-1)=integral_0^infinity exp(-alpha_eK_e)dalpha_e,
M_Gamma=R_(>0)^(E(Gamma))/Aut(Gamma),            (25.6)
```

but worldline/tropical evaluation occurs only after the physical quotient.

## Scalar-QED construction test

Local phase transport

```text
phi->exp(ie alpha)phi,
A->A+dalpha
```

forces `D_A=d-ieA`; direct substitution verifies covariance. Expanding
`<D_Aphi,D_Aphi>` constructs both the current and the quadratic contact. With the
unpolarized metric convention, its action coefficient is `c_action=2`.

For scalar Compton data

```text
p+k=p'+k',
p^2=(p')^2=m^2,
k^2=(k')^2=0,

D_s=(p+k)^2-m^2,
D_u=(p-k')^2-m^2,
```

the two homotopy transfers are

```text
T_ex^(mu nu)
 =-(2p+k)^mu(2p'+k')^nu/D_s
  -(2p'-k)^mu(2p-k')^nu/D_u.                   (25.7)
```

Ward contraction applies the kinetic operator and collapses each homotopy:

```text
k dot(2p+k)=D_s,
k dot(2p'-k)=-D_u,
k_muT_ex^(mu nu)=-2k^nu.
```

The contact column gives `k_mu(c eta^(mu nu))=ck^nu`; exact residual solving
therefore returns

```text
(-2,-2)+c(1,1)=(0,0) -> c=2,

T_phys=T_ex+2eta,
k_muT_phys^(mu nu)=0,
k'_nuT_phys^(mu nu)=0.                          (25.8)
```

The action coefficient and obstruction coefficient coincide. This validates the
semantics:

```text
kinetic defect -> homotopy -> Ward collapse -> local descendant
 -> higher action jet cancels descendant -> physical projection.
```

## Retained interface and boundary

```text
PhysicalTransfer(free complex, interaction, contraction grammar,
                 observable, coupling/loop budget)
 -> transferred physical operations + decorated graph classes
    + factorization cells + Ward certificates + complete cost
 | refusal(characteristic, anomaly, or budget).
```

The four-point test has two exchanges plus one contact on both the transfer and
textbook routes, so it proves meaning but no computational gain. [Node 27](27-open-line-worldline-quotient.md)
tests multiplicity, where the same transfer can compress many histories. Fermionic
spin transport, scalar--spin-two transfer, and loop quotient cells remain open.
