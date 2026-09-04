# N10q — Projected-Carrier Source-Response Discriminator

Status: exact nonzero-momentum source-quotient equivalence is supported for spins
two through five; gauge-slice transport is rejected as a local causal constructor,
and [N10r](10r-direct-constrained-green.md) now closes the independent generic Green
comparison negatively on its declared load metric

Consumes: [N10p null-orbit comparison](10p-null-orbit-carrier-comparison.md),
[N10e source adapter](10e-generated-source-adapter.md),
[N10j curvature generator](10j-generated-curvature-compatibility.md),
[N10k sourced curvature transport](10k-sourced-curvature-transport.md), and
[N10l compatible curvature sources](10l-compatible-curvature-source.md)

Computation: [source-response discriminator](../computation/10q-source-response-discriminator/README.md)

Produces: a source-annihilator constructor, a divergence-generated gauge slice and
dual source lift, an algebraic same-observable transport, and a polynomial-locality
refusal for the constrained harmonic presentation

## Research contract

- **Upstream anchor:** N10p shows that the constrained harmonic, compensated
  harmonic, and compressed symmetric presentations carry the same null helicities,
  but it does not compare their off-shell physical-source interfaces.
- **Bridge question:** can the constrained harmonic presentation accept the same
  physical source and compute the same gauge-invariant response by a cheaper local
  causal route?
- **Invariant target:** one source functional on the physical field quotient and
  the curvature response generated from that same functional.
- **Downstream effect:** decide whether gauge-slice equivalence itself supplies a
  local response reduction and expose any strictly independent construction still
  needed before judging the constrained presentation.
- **Special resources:** free constant-coefficient four-dimensional symbols, a
  nonzero momentum representative, finite harmonic carriers, and the already
  constructed compensated/symmetric response route.
- **Internal benchmark:** spins two through five, with spin two as regression and
  spin three as the first transfer; exact source-space coincidence, explicit lift,
  same gauge-invariant observable, and a locality decision are required.
- **Horizon:** interaction vertices, curved backgrounds, distributional completion
  through `p=0`, and numerical conditioning do not belong to this node.

## 1. A physical source is constructed from the gauge pairing

Let the harmonic field carrier be `H_s`. The constrained branch does not admit all
parameters in `H_(s-1)`; it admits

```text
K = ker(A:H_(s-1)->H_(s-2)).                         (1.1)
```

Its gauge map is therefore `G_c=R|_K`. A source is initially only a functional
`j in H_s^*`. It descends to the gauge quotient precisely when its value does not
change along a gauge direction. Evaluate the change on the same parameter
`epsilon in K`:

```text
<j,phi+R epsilon>-<j,phi>
  = <j,R epsilon>
  = <R^dagger j,epsilon>.                            (1.2)
```

Hence `j` is admissible exactly when `R^dagger j` annihilates `ker A`. Finite
nondegenerate duality computes that annihilator as

```text
(ker A)^perp = im A^dagger,

R^dagger j in im A^dagger.                           (1.3)
```

This is weaker than writing `R^dagger j=0`, but it is not yet an extra physical
source class: the constrained field carrier has also discarded `H_(s-2)`. The
comparison must construct the missing dual datum before counting sources.

For the compensated field `(phi,chi) in H_s direct-sum H_(s-2)`, N10o generated

```text
G epsilon = (R epsilon,A epsilon).
```

Pairing it with `(j,k)` gives

```text
<(j,k),G epsilon>
  = <R^dagger j+A^dagger k,epsilon>.
```

The compensated source condition is therefore constructed as

```text
R^dagger j+A^dagger k=0.                              (1.4)
```

No conservation equation has been imported: (1.3) and (1.4) are the two gauge
pairings evaluated on their declared parameter spaces.

## 2. The missing source datum forces a divergence section

At a nonzero non-null momentum, the computation verifies that

```text
A:H_(s-1)->H_(s-2)
```

is surjective for spins two through five. Surjectivity permits a section

```text
S:H_(s-2)->H_(s-1),
A S=1.                                                (2.1)
```

The section is not chosen for convenience. It is forced by the request to remove
the compensator `chi`: reaching `chi=0` requires solving

```text
A epsilon=-chi.
```

Using (2.1), define the field slice

```text
sigma(phi,chi)=phi-R S chi.                            (2.2)
```

Let `i(phi)=(phi,0)`. Compute both quotient witnesses:

```text
sigma i(phi)=phi,

(phi,chi)-i sigma(phi,chi)
  =(R S chi,chi)
  =(R S chi,A S chi)
  =G(S chi).                                          (2.3)
```

Thus `sigma` and `i` are inverse on gauge classes. This constructs the
nonzero-momentum meaning of “the constrained carrier is a gauge slice”; dimension
counting is only its later certificate.

## 3. Dualizing the slice generates the source lift

For a constrained source satisfying (1.3), construct

```text
L_S(j)=(j,-S^dagger R^dagger j).                       (3.1)
```

Because `R^dagger j` lies in `im A^dagger`, write it as `A^dagger w`. Then

`S^dagger A^dagger=(A S)^dagger=1` on `H_(s-2)^*`. Evaluate the compensated
source obstruction:

```text
G^dagger L_S(j)
  =R^dagger j-A^dagger S^dagger R^dagger j
  =A^dagger w-A^dagger S^dagger A^dagger w
  =A^dagger w-A^dagger w
  =0.                                                  (3.2)
```

The same construction preserves the source functional, not merely its dimension:

```text
<L_S(j),(phi,chi)>
  =<j,phi>-<S^dagger R^dagger j,chi>
  =<j,phi-R S chi>
  =<j,sigma(phi,chi)>.                                 (3.3)
```

The exact computation confirms that every compensated admissible source is in the
span of these lifts and that restricting `L_S(j)` to the harmonic head returns
`j`. Therefore the two source spaces are dual presentations of the same quotient
at nonzero momentum.

## 4. Gauge-invariant response agrees only after the nonlocal transport

Let the existing compensated/symmetric route return a response class

```text
v(p)=G_u(p)L_S(p)j
```

away from `p=0`. Transport it to the constrained slice by

```text
G_c(p)j=sigma(p)G_u(p)L_S(p)j.                         (4.1)
```

If `C` is the curvature operation already constructed in N10j, then `C G=0`.
Equation (2.3) supplies the equality witness on the same response:

```text
v-i sigma(v)=G(S chi),

C v-C i sigma(v)=C G(S chi)=0.                         (4.2)
```

Thus (4.1) preserves the gauge-invariant curvature response on the punctured
momentum domain. It does **not** yet construct a compact-source causal operation.
That stronger claim depends on the locality of `S`.

## 5. The section cannot be polynomial-local

The divergence symbol is linear in momentum:

```text
A(lambda p)=lambda A(p).
```

A homogeneous natural section satisfying `A(p)S(p)=1` must consequently scale as
`S(lambda p)=lambda^(-1)S(p)`. More decisively, suppose `S(p)` were a polynomial
symbol of a constant-coefficient local differential operation. Evaluating its
required identity at zero momentum gives

```text
A(0)S(0)=0,
```

which cannot equal the identity on `H_(s-2)`. Therefore

```text
no polynomial-local S can satisfy A S=1 globally.       (5.1)
```

The inverse-momentum resource occurs twice: in the field slice `sigma` and in the
dual source lift `L_S`. It can also be singular where the rank of `A(p)` changes.
Consequently an existing causal Green operation cannot simply be passed through
(4.1) while preserving compact support or causal support. A new distributional
construction would be required.

## 6. Exact bounded computation

At the four-dimensional Euclidean representative `p=e_0`, exact rational
harmonic-polynomial linear algebra gives:

| spin `s` | `dim H_s` | `dim H_(s-2)` | `dim ker A` | constrained sources | compensated sources |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 9 | 1 | 3 | 6 | 6 |
| 3 | 16 | 4 | 5 | 11 | 11 |
| 4 | 25 | 9 | 7 | 18 | 18 |
| 5 | 36 | 16 | 9 | 27 | 27 |

For every row the computation also certifies:

```text
A S=1;
G^dagger L_S=0;
restriction after L_S = identity;
span(im L_S) = ker G^dagger.
```

The matrices are an independent finite-rank check. Equations (1.2)--(5.1) own the
semantic construction and locality verdict.

## 7. Gauge-slice verdict and the remaining direct obstruction

The constrained presentation does not generate new physical source classes. It
repackages the compensated/symmetric source quotient through `S`. Its local field
carrier saves `dim H_(s-2)=(s-1)^2` directions, but reconstructing the same source
functional and response requires precisely the discarded defect carrier together
with an inverse-momentum operation.

For the attempted gauge-slice route, the verdict is therefore:

```text
compensated/symmetric presentation
  -> retained local source-compatible baseline;

constrained harmonic gauge-slice transport
  -> exact nonzero-momentum gauge slice,
  -> algebraically equivalent source and curvature response,
  -> no polynomial-local source lift,
  -> rejected as a local causal constructor.             (7.1)
```

This does not yet reject every direct constrained response construction. A local
constrained Euler operator and compact-source Green map might be generated without
transporting through `S`; N10q has neither constructed nor forbidden that route.
The next obstruction is consequently precise:

```text
constrained gauge complex
  -> generate its self-adjoint Euler/source interface
  -> construct a causal Green operation without S
  -> recover the same curvature observable
  -> compare complete cost with the compensated baseline. (7.2)
```

More spins or carrier variants cannot change the failure of the gauge-slice route.
[N10r](10r-direct-constrained-green.md) now constructs (7.2) without `S`. Its
generic route is costlier in scalar-Green depth, while a preparation that supplies
one invariant layer remains the supported re-entry condition.

## Edges

- `N10p -> N10q`: pass the null-equivalent presentations and the unresolved
  off-shell capability question.
- `N10e/N10j/N10k/N10l -> N10q`: pass the already constructed physical source,
  curvature, and compensated causal-response interfaces as the common baseline.
- `N10q -> direct constrained Euler/Green frontier`: reject local response by
  gauge-slice transport and require an independent response generator before
  judging the constrained presentation itself.
- `N10q -> N10r`: pass that independent response obligation without passing the
  nonlocal section as a permitted resource.
