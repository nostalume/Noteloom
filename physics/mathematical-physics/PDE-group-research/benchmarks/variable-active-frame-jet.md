# Variable active-frame jet probe

## Target and role

`E_G19_probe_1` targets the frame-covariance and rank dimensions of the
[G19 inquiry](../research-graph.md#resolved-bridge-ledger-g19-variable-active-module-bundle).
It is a discovery probe, not evidence that a variable active module can already
be generated from arbitrary PDE coefficients.

## Invariant witness shell

Let `B(x): C^r -> E_x` be a supplied smooth constant-rank frame on an admitted
region, with synthesis `S_B u=B u`. Construct

```text
G=B^dagger B,       A_B=G^(-1)B^dagger,       P=S_B A_B,
D_B=A_B D S_B,      R_B=(I-P)D S_B.                         (1)
```

Here `D` is a linear differential operator on a stated common core. The
definitions compute, without component expansion,

```text
D S_B = S_B D_B + R_B,        A_B R_B=0.                    (2)
```

All product-rule connection, induced lower-order, and off-module terms are
contained in the two operator compositions in (1). Equation (2) is exact once
`G^(-1)` and the compositions exist; it does not construct `B` or their domains.

For an invertible variable frame change `B_new=B U(x)`, multiplication operators
give

```text
S_new=S_B M_U,       A_new=M_(U^(-1)) A_B,       P_new=P,
D_new=M_(U^(-1)) D_B M_U,     R_new=R_B M_U.                 (3)
```

Derivatives of `U` are part of the compositions in (3). Individual connection or
leakage coefficients may therefore redistribute by differential order while the
ambient reconstruction remains unchanged. A pulled-back preparation/effect is
frame-invariant when its coordinate transformations and domain are carried with
(3).

## Exact local jet certificate

At one base point take `D=-partial_x^2 I+H`, ambient dimension three, retained
dimension two, and derivative jets

```text
B_0=[e_1,e_2],       B_1=[e_3,0],       B_2=[-e_1,0],
H=[[2,1,0],[1,3,0],[0,0,5]].                                (4)
```

Then `H B_0=B_0 A_0` with `A_0=[[2,1],[1,3]]`; the preparation `e_1` and `H e_1`
generate `span{e_1,e_2}`. For coefficients ordered as
`(partial_x^2,partial_x,1)`, (1) returns

```text
D_B: (-I, 0, [[3,1],[1,3]]),
R_B: (0, [[0,0],[0,0],[-2,0]], 0).                          (5)
```

Now use a rotating reduced frame with jets

```text
U_0=I,       U_1=J=[[0,-1],[1,0]],       U_2=-I.             (6)
```

The connection changes from zero to `J`. Direct product-rule evaluation gives

```text
D_new: (-I, -2J, [[4,1],[1,4]]),
R_new: (0, [[0,0],[0,0],[-2,0]], [[0,0],[0,0],[0,2]]).      (7)
```

Substitution of (5)--(6) into (3) gives (7) exactly. Direct ambient
reconstruction of every derivative order also agrees. This is a small independent
matrix certificate for the invariant identities, not the generative method.

## Rank-jump control

For the polynomial frame candidate `B_jump(x)=[e_1,x e_2]`,

```text
G_jump=diag(1,x^2),       det G_jump=x^2.                    (8)
```

The rank is two at `x=1` and one at `x=0`; `A_B` is undefined at the jump.
Pointwise success away from zero therefore cannot certify an admitted
neighborhood. A G19 constructor must return a constant-rank region certificate,
stratify the base, or refuse.

## Reproduction and disposition

The integer identities were independently replayed under CPython 3.14.6 and
NumPy 2.5.2 in the locked workbench environment. Base worktable revision:
`504bc2977fb66e9d461acd4ce7ff4626f1f9e312`. Transient checker SHA-256:
`D1EAC4E72E904EB1C576364E117CB96B5FB714DB1B146260B41BBC4385C28253`;
transient JSON SHA-256:
`331DB77D7194695A50359C4FBE58DF8FEE439CB9FA551AE3D48B69BF90DF9DEC`.
The packet retains the complete finite calculation; the scratch checker and raw
JSON were discarded rather than admitted as a G19 implementation.

Disposition: **exact support** for the witness-shell decomposition and variable
frame covariance when a smooth constant-rank frame and compatible operator domain
are supplied. Equation (8) is an exact adversarial boundary. The probe does not
construct the frame from coefficient jets, certify rank on a general region,
establish non-Pauli physical transfer, descend boundary data, control leakage, or
show computational leverage.
