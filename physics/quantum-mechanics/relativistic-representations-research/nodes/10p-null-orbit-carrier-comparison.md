# N10p — Null-Orbit Carrier Comparison

Status: common null quotient, transverse-screen recovery, and Fischer chain
coincidence are supported for spins two through five; N10q rejects the first
off-shell gauge-slice response route; N10r closes the direct generic Green comparison
negatively on its declared load, while interactions and conditioning remain open

Consumes: [N10o carrier choice](10o-projected-carrier-choice.md),
[N10n projected operations](10n-projected-carrier-completeness.md),
[N10c residual constructor](10c-generative-residual-constructor.md), and
[N4a polynomial complex](04a-polynomial-complex-details.md)

Computation: [null-orbit carrier comparison](../computation/10p-null-orbit-carrier-comparison/README.md)

Produces: a common-shell quotient comparison, a zero-order Fischer chain
isomorphism, a partial-gauge cost identity, and a negative free-physical-novelty
verdict for the projected-carrier branch

## Research contract

- **Upstream question:** N10o shows that trace freedom is optional and produces a
  constraint/compensator/full-symmetric portfolio. Which branches actually recover
  the target massless helicities?
- **Common input:** four-dimensional Lorentz metric, one null momentum, the same
  trace-free parameter carrier, and the same two-dimensional transverse screen.
- **Forbidden shortcut:** no expected quotient dimension, preferred branch, or
  textbook equation name is supplied to the comparator.
- **Benchmark:** construct all three complexes, verify gauge identities, compute
  quotient and screen ranks, construct any zero-order chain map between them, and
  charge carrier reduction against lost gauge directions.
- **Horizon:** separate finite integer spins `2--5` at one null representative.
  Full little-group action is inherited from the earlier screen construction, not
  recomputed here. No action, source, Green operation, or interaction claim.

## 1. The three presentations meet at one null momentum

Fix

```text
eta=diag(1,-1,-1,-1),
p=(1,0,0,1),
Q=p^2=0.                                               (1.1)
```

For each `s>=2`, compare:

```text
A. constrained harmonic
   epsilon in ker(A:H_(s-1)->H_(s-2)),
   phi in H_s,
   R=R_(s-1),
   D=Q-R_(s-1)A;

B. compensated harmonic
   epsilon in H_(s-1),
   (phi,chi) in H_s direct-sum H_(s-2),
   delta phi=R_(s-1)epsilon,
   delta chi=A epsilon,
   E=D phi+rho_(s-1)R_(s-1)R_(s-2)chi;

C. compressed symmetric baseline
   epsilon in ker T=H_(s-1),
   Phi in ker T^2 subset Sym^s,
   delta Phi=P epsilon,
   harmonic head of the generated symmetric equation.
```

They are not compared by formula length. The invariant target is the same null
solution quotient and its transverse screen.

## 2. The compensator internally reconstructs the trace layer

N10o introduced `chi` because the projected gauge residual is typed by
`A epsilon in H_(s-2)`. Combine the two harmonic fields by

```text
Phi=phi+[1/(2s)]U chi.                                (2.1)
```

This coefficient is not chosen from the symmetric baseline. Since `chi` has rank
`s-2`, the invariant algebra gives

```text
T(U chi)=4s chi.                                      (2.2)
```

Therefore

```text
T Phi=2chi,
T^2Phi=0,
chi=(1/2)T Phi,
phi=Phi-[1/(4s)]UT Phi.                               (2.3)
```

Equations (2.1)--(2.3) construct mutually inverse maps

```text
H_s direct-sum H_(s-2)  ~=  ker T^2.                  (2.4)
```

Thus the additional harmonic field is exactly the first trace layer that was
removed when `H_s` was selected.

## 3. The gauge maps coincide under the same assembly

For `epsilon in H_(s-1)`, N10n gives

```text
R_(s-1)epsilon
 =P epsilon-[1/(2s)]UA epsilon.                       (3.1)
```

Use both compensated gauge laws in (2.1):

```text
delta Phi
 =R_(s-1)epsilon+[1/(2s)]U A epsilon
 =P epsilon.                                          (3.2)
```

The compensated branch has therefore reconstructed the ordinary symmetric gauge
map exactly. The operation that looked like an auxiliary repair is the coordinate
needed to undo the harmonic projection.

## 4. Its equation is the harmonic head of the symmetric equation

Let `D_F` denote the symmetric residual constructor's second-order equation. The
comparison needs no component expansion. Work modulo `im U`, because the harmonic
head is the quotient of `Sym^s` by its metric-inserted trace layer.

Substitute (2.1) into N10o's compensated equation. Since `R=P` modulo `im U`,

```text
E(phi,chi)
 =QPhi-PA Phi+(2/(2s)+rho_(s-1))P^2chi  mod im U.
```

In four dimensions

```text
rho_(s-1)=(s-1)/s,
2/(2s)+rho_(s-1)=1,
chi=(1/2)T Phi.
```

Hence

```text
E(phi,chi)
 =QPhi-PA Phi+(1/2)P^2T Phi  mod im U
 =D_F Phi mod im U.                                  (4.1)
```

The finite computation independently verifies equality of the equation kernels
under (2.1) for spins two through five. Together with (2.4) and (3.2), this is a
zero-order chain isomorphism, not merely equal degree counting.

## 5. All three branches recover the same null fiber

The executable constructs each kernel and gauge image at (1.1). The results are:

| spin `s` | constrained `dim field` | constrained `dim gauge image` | compensated/baseline `dim field` | compensated/baseline `dim gauge image` | quotient | screen |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `2` | `9` | `3` | `10` | `4` | `2` | `2` |
| `3` | `16` | `5` | `20` | `9` | `2` | `2` |
| `4` | `25` | `7` | `34` | `16` | `2` | `2` |
| `5` | `36` | `9` | `52` | `25` | `2` | `2` |

Every gauge residual has rank zero. Each solution quotient and transverse-screen
image has dimension two. This verifies the common helicity-pair dimension in the
declared finite bench; the earlier representation nodes own its helicity action.

## 6. The constrained saving is exactly partial gauge fixing

In four dimensions

```text
dim H_s=(s+1)^2,
dim ker T^2=dim H_s+dim H_(s-2)=2s^2+2.               (6.1)
```

The constrained branch saves

```text
(2s^2+2)-(s+1)^2=(s-1)^2                              (6.2)
```

field components. At null momentum, contraction

```text
A:H_(s-1)->H_(s-2)                                   (6.3)
```

has full target rank in the finite bench. Imposing `Aepsilon=0` therefore removes

```text
dim H_(s-2)=(s-1)^2                                  (6.4)
```

parameter directions—the exact number of field components saved in (6.2).

So the constrained harmonic branch does not compress the physical quotient. It
chooses a partial gauge slice before the quotient and removes the matching trace
layer. This may still be useful for a named off-shell calculation, but free-shell
component count alone gives no gain.

## 7. Verdict and stop

The null-orbit discriminator resolves the motivation question:

```text
compensated harmonic branch
  = zero-order Fischer reparameterization
    of the compressed symmetric baseline;

constrained harmonic branch
  = partial gauge presentation
    with equal field saving and removed gauge directions;

all three
  -> the same two-dimensional null screen.
```

There is no new free physical content and no demonstrated computational
compression. The trace-free carrier remains useful as a compiler regression and
as an explicitly requested partial-gauge interface. It should not replace the
symmetric baseline in the paper merely because its raw field carrier is smaller.

[N10q](10q-source-response-discriminator.md) names the first such capability. It
constructs the common physical source quotient but shows that its
constrained-to-compensated lift requires a non-polynomial divergence section. Thus
gauge-slice transport cannot supply the local causal response. N10q does not infer
from this that an independently generated constrained Green operation is impossible.

## Edges

- `N10o -> N10p`: pass the three capability-relative branches to a common null
  physical benchmark.
- `N10p -> N10c/N4a`: identify the compensated branch with the existing compressed
  symmetric complex rather than retaining a duplicate presentation.
- `N10p -> N10q`: carry the constrained harmonic branch into one named physical
  source/locality calculation before deciding whether it deserves re-entry.
