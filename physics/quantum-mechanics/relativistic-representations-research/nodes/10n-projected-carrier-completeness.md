# N10n — Projected-Carrier Operation Completeness

Status: supported for the one-row harmonic carrier in dimension at least three,
with symbolic construction through a declared rank budget, exact independent
`O(3)` Hom-space checks at ranks one through three, and one constrained downstream
residual use; the complementary mixed carrier is exposed but not yet constructed

Consumes: [N10m natural-operation compiler](10m-natural-operation-compiler.md),
[N10c residual constructor](10c-generative-residual-constructor.md), and
[N2b Lorentz carriers](02b-lorentz-carriers.md)

Sources: [projected-carrier contracts](../sources/projected-carrier-contracts.md)

Computation: [projected-carrier completeness](../computation/10n-projected-carrier-completeness/README.md)

Produces: an obstruction-generated trace-preserving momentum raise, its
rank-indexed composition law, an independent same-family completeness certificate,
a typed missing-mixed-carrier obstruction, and a downstream constrained wave
factorization

## Research contract

- **Upstream obstruction:** N10m assumes that universal multiplication by momentum
  stays inside the selected free-power carrier. A projected carrier need not be
  closed under that operation.
- **Why this carrier:** `H_r=ker T` is the smallest nontrivial projector boundary
  and therefore a compiler stress test. It is also the irreducible one-row
  orthogonal carrier after trace descendants are removed. It is **not** inferred
  from the particle representation or assumed to be the preferred gauge-potential
  presentation; N10o makes that carrier choice capability-relative.
- **Independent input:** the carrier equation `Tf=0`, the metric-generated
  operations `{T,U,E,P,A,Q}`, their directly evaluable commutators, dimension, and
  rank budget. No projector, corrected raise, rewrite coefficient, or field
  equation is supplied.
- **Benchmark:** generate every linear-in-momentum rank-changing operation that
  remains inside the one-row harmonic family; compare its multiplicity with an
  independent equivariant calculation; retain the complementary channel; make a
  residual consumer use the rank-indexed law.
- **Horizon:** ordinary flat orthogonal carrier algebra. The exact Hom calculation
  is bounded to `O(3)` and ranks one through three. Mixed-carrier construction,
  arbitrary-dimension characters, physical-shell recovery, and interactions remain
  open.

## 1. The projector is demanded by a failed operation

Represent `Sym^r(V*)` by degree-`r` polynomials in an auxiliary vector `x`. The
metric constructs

```text
T=partial_x^2,    U=x^2,    E=x dot partial_x,
P=p dot x,        A=p dot partial_x,    Q=p^2.
```

Conditionally request the irreducible one-row carrier by removing its trace
descendants:

```text
H_r={f in Sym^r(V*):Tf=0}.                            (1.1)
```

This is a presentation input, not a physical theorem. A reducible traceful field
may recover the same particle quotient through equations and gauge symmetry. The
purpose here is to test whether the compiler respects a declared projector.

Try N10m's raw raise `P`. Direct evaluation gives

```text
T(Pf)=P(Tf)+2Af=2Af.                                  (1.2)
```

Thus `P` is not an operation on the carrier family. Equation (1.2), rather than a
remembered traceless-gradient formula, motivates the repair.

At momentum degree one and rank shift `+1`, metric contraction supplies only two
same-family candidates on `ker T`:

```text
P,    UA.                                              (1.3)
```

Terms ending in `T` vanish on the input; further powers of `U` have the wrong rank
shift. Hence the normalized candidate is internally forced to be

```text
R_r=P+c_rUA.                                           (1.4)
```

For `r>0`, evaluate the second candidate using

```text
TU=UT+4E+2d,
E(Af)=(r-1)Af:

T(UAf)=2(2r+d-2)Af.                                   (1.5)
```

Cancellation of (1.2) and (1.5) computes

```text
c_r=-1/(2r+d-2),
R_r=P-[1/(2r+d-2)]UA.                                 (1.6)
```

At `r=0`, `A` vanishes and the construction correctly returns `R_0=P`; no
invisible correction coefficient is claimed.

## 2. Projection forces a rank-indexed grammar

N10m's rewrite rules have constant coefficients. That representation fails after
projection. Compose the generated raise with the lowering operation and evaluate

```text
AP=PA+Q,
AU=UA+2P.                                             (2.1)
```

Substitution of (1.6) gives

```text
A R_r
 =Q+[(2r+d-4)/(2r+d-2)]PA
    -[1/(2r+d-2)]UA^2.
```

The last two terms are exactly the prior-rank projected raise followed by `A`:

```text
A R_r
 =Q+rho_r R_(r-1)A,
rho_r=(2r+d-4)/(2r+d-2).                              (2.2)
```

This is the new reusable object. A projected-carrier compiler must know the current
rank when normalizing a word. Treating `R` as a flat token would erase semantic
information and return wrong coefficients.

## 3. Completeness is checked independently

The construction used the small invariant ansatz (1.3). To check that this ansatz
did not hide another operation, the computation packet builds a second route that
does not use (1.6):

```text
monomial polynomials
  -> exact kernel of the Laplacian = H_r
  -> exact so(3) generator matrices on H_r
  -> tensor action on H_r tensor V
  -> full linear intertwiner equations
  -> one reflection equation to distinguish O(3) from SO(3)
  -> exact rational nullspace dimension.
```

For `r=1,2,3`, the resulting multiplicities are

| target | multiplicity |
| --- | ---: |
| `H_(r+1)` | `1` |
| `H_r` | `0` |
| `H_(r-1)` | `1` |

The generated `R_r` and `A` therefore exhaust the operations landing back in the
one-row harmonic family on this independent bench.

This calculation is deliberately isolated. Coordinates and row reduction verify
the invariant construction; they do not motivate or define it.

## 4. Completeness exposes, rather than removes, the mixed channel

The domain has dimension `3(2r+1)` in the `O(3)` bench. The two represented
harmonic targets have total dimension

```text
dim H_(r+1)+dim H_(r-1)
 =(2r+3)+(2r-1)=4r+2.
```

The complement therefore has dimension

```text
3(2r+1)-(4r+2)=2r+1.                                 (4.1)
```

For the connected rotation group this is the familiar middle angular-momentum
channel; under `O(3)` it carries the reflection parity of the hook/determinant-
twisted representation and is not another copy of `H_r`. The reflection equation
is essential: using only Lie-algebra generators would incorrectly report a
same-carrier operation.

Equation (4.1) is a successful obstruction, not a completeness failure. The
one-row compiler is complete for outputs in its declared family, and it reports
the missing projected carrier required to become complete in the whole tensor
product. It does **not** follow that this complement repairs the later gauge
residual; residual typing must decide that separately.

## 5. Downstream use reveals a physical limitation

To test whether (2.2) is computationally usable, take a field in `H_s` and a
parameter in `H_(s-1)`. The generated gauge candidate is

```text
R=R_(s-1).
```

The degree-two wave repair admitted by the same-family operations is

```text
D=Q-R_(s-1)A,
C=A,
D+RC=Q.                                               (5.1)
```

Now use the rank-indexed relation rather than a supplied equation identity:

```text
D R_(s-1)
 =-rho_(s-1)R_(s-1)R_(s-2)A.                         (5.2)
```

The residual has one irreducible right factor. It generates the smallest parameter
condition within this carrier cell:

```text
A epsilon=0.                                          (5.3)
```

At `d=3`, `s=3`, the executable result is

```text
R=R_2,
D=Q-R_2A,
DR_2=-(3/5)R_2R_1A.
```

Thus the projected grammar is consumed and produces a real refusal: trace-free
projection alone does not yield an unconstrained same-family gauge system. The
result is not promoted as a preferred higher-spin equation. The primitive defect
in (5.2) is `A epsilon in H_(s-2)`. N10o therefore tests the repairs licensed by
that lower-rank carrier instead of inferring the unrelated mixed complement.

## 6. Global verdict and stop

N10n strengthens N10m in three ways:

1. carrier preservation generates an operation rather than merely admitting one;
2. rewrite semantics become rank-indexed;
3. independent completeness detects a missing carrier instead of allowing the
   chosen vocabulary to certify itself.

The supported spine is now

```text
free power law                         [N10m]
  -> operation grammar
projected carrier constraint           [N10n]
  -> failed raw operation
  -> obstruction-generated projected operation
  -> independent same-family completeness
  -> missing mixed channel
  -> downstream residual and constraint.
```

[N10o](10o-projected-carrier-choice.md) corrects the carrier motivation and consumes
the residual. It generates two genuine branches—restrict `A epsilon` or introduce
`chi in H_(s-2)` with `delta chi=A epsilon`—and retains a third option: abandon the
trace-free presentation if no requested capability authorizes it. The mixed
complement remains recorded, but its construction is parked until a residual or
capability actually lands in that channel.

## Edges

- `N10m -> N10n`: replace free-power closure by an explicit projected-carrier
  preservation obligation.
- `N2b/projector sources -> N10n`: pass the harmonic carrier and invariant metric
  algebra, not a finished projected gradient.
- `N10n -> residual consumer`: pass the rank-indexed relation and receive the
  generated parameter obstruction.
- `N10n -> N10o`: pass the complementary-channel count and residual as distinct
  facts; let residual typing, rather than dimension, choose the repair carrier.
