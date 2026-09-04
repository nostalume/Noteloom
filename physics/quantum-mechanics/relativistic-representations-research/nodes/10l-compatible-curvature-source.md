# N10l — Compatible Direct-Curvature Source Constructor

Status: mathematical compatible-source construction, finite-rank verification,
same-output use, and negative cost verdict are supported for each separate
parity-paired positive integer spin on four-dimensional Minkowski spacetime; the
executable currently consumes theorem-defined lift/syzygy rules rather than
generating their maps from independent input

Consumes: [N4 direct chiral equation](04-local-symbol-extension.md),
[N10e source adapter](10e-generated-source-adapter.md),
[N10j curvature generator](10j-generated-curvature-compatibility.md), and
[N10k sourced curvature transport](10k-sourced-curvature-transport.md)

Sources: [higher-spin curvature contracts](../sources/higher-spin-curvature-contracts.md)

Computation: [compatible direct-curvature sources](../computation/10l-compatible-curvature-source/README.md)

Produces: a short direct chiral source complex, its normalized back operation,
retarded/advanced Green maps on compatible sources, an order-`s-1` potential-source
lift, a same-output theorem, and a complete negative cost verdict  
Construction-origin correction: [audit](../results/07-construction-origin-audit.md)

## Research contract

- **Upstream anchor:** N10k constructs the curvature response but refuses an
  unrestricted source for N4's overdetermined first-order equation.
- **Bridge question:** which source data are actually accepted by that equation,
  can they be generated from N10e's physical current, and do they shorten the route
  to the same curvature observable?
- **Invariant target:** the same adapted compact potential source `S=M_s^(-1)J`
  and the same retarded/advanced chiral curvature distribution.
- **Downstream effect:** either obtain a genuine direct first-order causal
  interface or retain the rank refusal; then decide whether it changes the global
  computability claim.
- **Special resources:** two-dimensional chiral spinor carriers, their alternating
  forms, homogeneous symmetric algebra, flat constant coefficients, and the scalar
  wave Green maps.
- **Internal benchmark:** construct the source compatibility operator and back
  map without spacetime components; execute the direct-complex identities for
  spins `1--6`; derive the source-lift syzygies in symmetric algebra; recover
  N10k's exact output; compare all Green-channel loads.
- **Horizon:** separate finite integer spin and free flat response. No arbitrary
  interacting current, curved deformation, countable completion, or runtime claim.

## 1. The rank defect asks for closed sources, not a projection

Put `n=2s`. For one chirality, N4 constructs

```text
Z_s(p):Sym^n(S) -> Sym^(n-1)(S) tensor bar S.           (1.1)
```

At non-null `p`, the spinor momentum map is invertible. Use its adjugate to convert
the remaining primed source index into an unprimed covector. A source

```text
j in Sym^(n-1)(S) tensor bar S                         (1.2)
```

then becomes a homogeneous one-form `j_hat` of polynomial degree `n-1` on `S`.
Equation (1.1) becomes the gradient operation

```text
phi |-> d phi.                                         (1.3)
```

This internally explains N10k's rank defect. A general homogeneous one-form has
`2n` coefficients, whereas an exact one has `n+1`. The missing `n-1` conditions
are not data to discard; they are the antisymmetric derivative of `j_hat`.

The cheapest Lorentz-natural compatibility operation is therefore

```text
Y_s(p):Sym^(n-1)(S) tensor bar S -> Sym^(n-2)(S),
Y_sj = antisymmetric part of d j_hat.                   (1.4)
```

Commuting derivatives on the same `phi` computes

```text
Y_sZ_sphi=antisym(d^2phi)=0.                            (1.5)
```

The conjugate chirality gives the generated complex

```text
Curv_s --Z_s--> E_s^curv --Y_s--> I_s^curv,            (1.6)

dim Curv_s=4s+2,
dim E_s^curv=8s,
dim I_s^curv=4s-2.                                     (1.7)
```

At non-null momentum, the converted source carrier decomposes into a totally
symmetric part and one antisymmetric remainder:

```text
Sym^(n-1)(S) tensor S
  ~=Sym^n(S) direct-sum Sym^(n-2)(S).                   (1.8)
```

`Z_s` fills the first summand and `Y_s` detects the second. Hence

```text
ker Y_s(p)=im Z_s(p),       p^2!=0.                    (1.9)
```

This constructs the minimal compatible source carrier `ker Y_s`; it does not
project an arbitrary source nonlocally into one.

## 2. Euler homogeneity generates the back operation

The desired Green operation needs a numerator that returns a compatible source to
the curvature carrier. For `j_hat` homogeneous of degree `n-1`, the cheapest
candidate is contraction with the Euler vector `x`. Normalize it by `n`:

```text
B_s(p)j=(1/n) x dot j_hat.                              (2.1)
```

Evaluate (2.1) on the same equation source `Z_sphi`. Adjugate followed by momentum
is multiplication by `q=p^2` in the chosen normalization, while Euler's identity
gives `x dot d phi=n phi`. Therefore

```text
B_sZ_sphi=q phi.                                       (2.2)
```

For a general `j`, differentiating (2.1) separates its symmetric derivative from
the antisymmetric remainder:

```text
Z_sB_sj=qj+H_sY_sj                                    (2.3)
```

for the generated reinsertion map `H_s`. On the constructed source space,

```text
Y_sj=0  =>  Z_sB_sj=qj.                               (2.4)
```

Equations (1.5), (2.2), and (2.4) are evaluated directly by the homogeneous
polynomial computation packet. No gamma or spacetime tensor components enter.

## 3. Compatible sources give the first-order equation a causal inverse

Let `G_Q^+/-` be the scalar retarded/advanced wave maps acting componentwise on
`E_s^curv`. Since every operation has constant coefficients, construct

```text
G_Z^+/- j=B_sG_Q^+/-j,       Y_sj=0.                   (3.1)
```

Applying `Z_s` to the same input and using (2.4) gives

```text
Z_sG_Z^+/-j
 =Z_sB_sG_Q^+/-j
 =qG_Q^+/-j
 =j.                                                   (3.2)
```

Conversely, for compact curvature `phi`, (2.2) gives

```text
G_Z^+/-Z_sphi
 =B_sG_Q^+/-Z_sphi
 =G_Q^+/-B_sZ_sphi
 =G_Q^+/-qphi
 =phi.                                                 (3.3)
```

`B_s` is differential, so it does not enlarge the retarded or advanced support
selected by `G_Q^+/-`. Thus N10k's unrestricted refusal is sharpened rather than
reversed: `Z_s` has Green maps exactly on `ker Y_s`, not on all of `E_s^curv`.

## 4. The potential source obstruction forces an order-`s-1` lift

N10e supplies

```text
S=M_s^(-1)J,
C_sS=0.                                                (4.1)
```

We need a local operation `L_s:S |-> j` landing in (1.2). At derivative degree
`d`, the largest left spin available from the traceless source layer and `d`
momenta is `(s+d)/2`. The target has left spin `s-1/2`, so

```text
d<s-1  =>  no lift exists in the declared chiral
           polynomial carrier cell.                    (4.2)
```

At `d=s-1`, the highest left channel and the lowest right channel each occur once.
Within this carrier cell, the obstruction therefore forces one operation up to
normalization. It is the partial curvature map

```text
(L_s^+(p)S)_(A_1...A_(2s-1) A')
 =p_(A_1)^(B'_1) ... p_(A_(s-1))^(B'_(s-1))
  S_hat_(A_s...A_(2s-1)) A' B'_1...B'_(s-1),          (4.3)
```

with symmetrization over the displayed unprimed indices; `S_hat` is the traceless
source layer. `L_s^-` is its conjugate. Formula (4.3) is constructed by stopping
N10j's order-`s` curvature product one contraction early, leaving precisely the
source index demanded by (1.1).

Two residuals must vanish on (4.1). Evaluating the generated symmetric products
gives the syzygies

```text
Y_sL_s=N_sC_s,
B_sL_s=K_s.                                            (4.4)
```

where `N_s` retains the terms containing the potential constraint. The first
identity says that the only failure of source compatibility is the original
source-conservation obstruction. The second is exact: `B_s` supplies the one
contraction deliberately withheld by `L_s`, with normalization fixed by N10j's
`K_s`. Both maps vanish on the lower trace layer by Lorentz weight. On the same
adapted source `S`, (4.1) computes

```text
j_s=L_sS,
Y_sj_s=0,
B_sj_s=K_sS.                                          (4.5)
```

The flat arbitrary-spin Damour--Deser identity is an independent theorem contract
for the curl/Fronsdal factorization in (4.4); the present construction owns its
four-dimensional chiral specialization and normalization.

The evidence is deliberately split: the executable packet evaluates the direct
complex and back identities for finite ranks, while (4.4) is the symbolic
symmetric-algebra derivation checked against that independent theorem contract.
The route normalizer consumes (4.4); it is not presented as an additional
componentwise verification of it.

## 5. Both causal routes now compute the same curvature

Pass the compatible source `j_s=L_sS` through the direct Green map:

```text
direct first-order route:
  J -> S -> L_sS -> B_sG_Q^+/-L_sS.
```

Constant-coefficient commutation and (4.5) evaluate this composite:

```text
B_sG_Q^+/-L_sS
 =G_Q^+/-B_sL_sS
 =G_Q^+/-K_sS
 =K_sG_F^+/-S.                                        (5.1)
```

The last expression is exactly N10k's potential-derived curvature. Equation (5.1)
is the required same-observable coincidence, not merely common shell cohomology.
It also gives the sourced first-order equation

```text
Z_s(K_sG_F^+/-S)=L_sS.                                (5.2)
```

For spin one, `L_1` has order zero and (5.2) is the chiral Maxwell equation with a
conserved vector source. For spin two, `L_2` takes one chiral derivative of the
adapted stress source, matching the linearized Weyl/Bianchi source structure.
These are regression readings of the generated family, not its definition.

## 6. The direct route fails the computational benchmark

All three routes start from the same physical current and recover the same
curvature. Their componentwise scalar Green loads are

```text
potential first:          2s^2+2,
curvature transport:      4s+2,
direct compatible source: 8s.                          (6.1)
```

The direct route additionally applies an order-`s-1` lift and a first-order back
operation. It always propagates more channels than curvature transport:

```text
8s-(4s+2)=4s-2>0.                                     (6.2)
```

Commuting `B_s` before the scalar Green map removes exactly those compatibility
channels, but (5.1) shows what remains:

```text
L_s -> B_s -> G_Q
  =K_s -> G_Q.                                         (6.3)
```

That optimized route is N10k, not a new first-order algorithm. The direct complex
therefore adds semantic capability—native compatible sources and a first-order
equation—but no calculation reduction for this potential-derived observable.

## 7. Retained interface and stop boundary

The returned operation is

```text
CompatibleCurvatureSource(
  N10j curvature packet,
  N10k sourced transport,
  spinor and scalar-Green resources,
  derivative budget)
 -> (Z_s,Y_s,B_s,L_s),
    compatible source j_s,
    retarded/advanced direct Green operations,
    complex/source-lift/same-output certificates,
    insufficient-degree or missing-resource refusal,
    whole-route cost record.                            (7.1)
```

The supported spine is now

```text
physical current -> adapted potential source                  [N10e]
  -> generated curvature and causal transport                 [N10j/N10k]
  -> rank defect of arbitrary first-order sources              [N10k]
  -> internally constructed source complex and back operation  [N10l]
  -> theorem-derived local lift from the same physical source  [N10l]
  -> identical direct and transported curvature                [N10l]
  -> direct-route computational gain rejected.                 [N10l]
```

This closes the compatible-source bridge within the flat free finite-spin horizon.
More source-complex ranks cannot change the current verdict. Re-entry requires a
native preparation or interaction that supplies compatible chiral sources without
first constructing a potential current, or evidence that the first-order complex
improves conditioning/locality for a fixed numerical observable despite its larger
carrier.

## Edges

- `N4/N10k -> N10l`: pass the direct symbol and its arbitrary-source rank defect.
- `N10e/N10j -> N10l`: pass the adapted physical source and retained curvature
  operation.
- `N10l -> global presentation verdict`: return a supported direct source
  capability, exact equality with N10k, and a rejected computational-gain claim.
