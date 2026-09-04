# N10j — Generated Curvature Compatibility Operator

Status: supported for every separate parity-paired positive integer helicity in
four-dimensional flat spacetime; the local forward map and physical-shell
isomorphism are generated, N10k consumes them in a sourced causal output, and a
polynomial local inverse or independent curvature-source complex remains
obstructed or open
Consumes: [N2b chiral Lorentz carriers](02b-lorentz-carriers.md),
[N4 direct chiral symbols](04-local-symbol-extension.md),
[N4a symmetric potential complex](04a-polynomial-complex-details.md),
[N5 low-spin comparison boundary](05-low-spin-comparison.md),
[N10c generated potential system](10c-generative-residual-constructor.md), and
[N10i presentation selector](10i-capability-relative-presentation-selector.md)
Sources: [higher-spin curvature contracts](../sources/higher-spin-curvature-contracts.md)
Computation: [curvature-compatibility generator](../computation/10j-generated-curvature-compatibility/README.md)
Produces: a minimal-degree potential-to-chiral-curvature operation, gauge and
covariance certificates, a physical-shell quotient isomorphism, an inverse
obstruction, and a revised frontier obtained by reusing N10i's selector  
Construction-origin correction: [audit](../results/07-construction-origin-audit.md) —
the invariant multiplicity argument and spin-indexed evaluator are retained, but
the executable `boundedMultiplicityTrace` encodes rather than computes the Hom
multiplicities

## Research contract

- **Upstream anchor:** N10i refuses the higher-spin potential/curvature bridge
  because N5 had only common-fiber equivalence beyond Maxwell.
- **Bridge question:** can the missing map be generated from the potential carrier,
  gauge operation, and chiral target rather than imported as the de Wit--Freedman
  formula?
- **Invariant target:** the same two null-screen helicity lines must become the two
  direct chiral kernel lines.
- **Downstream effect:** re-invoking N10i's retained selector with the generated
  packet admits potential routes for a gauge-invariant curvature output and charges
  the derivative order needed to recover it.
- **Special resources:** four-dimensional spinor factorization, the two invariant
  alternating spinor forms, and N2b's Hodge-chiral bivector split.
- **Internal benchmark:** generate the first admissible polynomial degree, kill
  the gradient gauge image, recover both physical lines for spins `1` through `6`,
  verify covariance, and make the selector consume the returned packet.
- **Horizon:** separate finite integer spin, flat constant-coefficient symbols,
  forward curvature output, and nonzero null-shell recovery. No half-integer,
  curved, interacting, countable-spin, or curvature-source completion belongs here.

## 1. The obstruction is a missing invariant output

N10c returns a symmetric potential system with field carrier

```text
F_s=ker T^2 subset Sym^s(V_C^*),
R_s(p)epsilon=P_p epsilon.                              (1.1)
```

Its quotient recovers the helicity pair, but a downstream observer requesting a
gauge-invariant local amplitude cannot consume the potential representative
directly. The requested target already exists in N4:

```text
C_s^curv=Sym^(2s)(S) direct-sum Sym^(2s)(bar S).         (1.2)
```

The generator must therefore construct an equivariant polynomial symbol

```text
K_s(p):F_s -> C_s^curv,
K_s(p)P_p=0,                                            (1.3)
```

and show that it carries the potential quotient to N4's direct physical kernel.
Equation (1.3), rather than a remembered curvature formula, is the capability
request.

## 2. Carrier weight forces the first derivative order

N2b constructs

```text
V_C ~= S tensor bar S,
H_r ~= Sym^r(S) tensor Sym^r(bar S),                    (2.1)
```

where `H_r` is the traceless rank-`r` symmetric Lorentz carrier. A degree-`d`
polynomial symbol receives one factor from `Sym^d(V_C)` and one from `F_s`.
Decompose both into trace levels. A top momentum level and a top field level carry
left spins `d/2` and `s/2`; every trace lowers them. Their tensor product can have
left spin at most

```text
j_L^max=(d+s)/2.                                       (2.2)
```

The plus target in (1.2) has left spin `s`. If `d<s`, then

```text
(d+s)/2<s,                                             (2.3)
```

so the equivariant map space is zero. This is the polynomial-lift obstruction:
no lower-derivative candidate exists in the declared carriers.

At `d=s`, reaching left spin `s` requires both top traceless levels and the highest
Clebsch--Gordan channel. Reaching right spin zero uses the unique singlet in
`(s/2) tensor (s/2)`. Both occur once. Consequently

```text
dim Hom_L(Sym^s(V_C) tensor H_s, Sym^(2s)(S))=1,        (2.4)
```

and likewise for the conjugate target. The lower field layer `U H_(s-2)` cannot
reach left or right chiral weight `s`, so the same map automatically ignores the
trace layer. Thus the obstruction and multiplicity calculation force both the
degree and a unique operation up to normalization.

The executable constructor performs this bounded degree search. A budget below
`s` returns the trace of zero multiplicities rather than emitting a formula.

## 3. The unique operation is built from one chiral bivector map

The alternating forms on `S` and `bar S` construct the two maps

```text
b_+:V_C tensor V_C -> Sym^2(S),
b_-:V_C tensor V_C -> Sym^2(bar S),                     (3.1)
```

obtained by taking `x wedge y`, applying N2b's two Hodge projections, and using
`Lambda^2_+ V_C ~= Sym^2(S)` and
`Lambda^2_- V_C ~= Sym^2(bar S)`.

For a decomposable symmetric potential amplitude, define

```text
K_s^+(p)(v_1 symmetric-product ... symmetric-product v_s)
  =symmetric-product_(i=1)^s b_+(p,v_i),

K_s^-(p)(v_1 symmetric-product ... symmetric-product v_s)
  =symmetric-product_(i=1)^s b_-(p,v_i).                (3.2)
```

The right sides are symmetric in the `v_i`, so they descend from tensor inputs to
`Sym^s(V_C^*)`; linear extension constructs them on all of `F_s`. Each contains
exactly `s` momentum factors and lands in the two targets of (1.2). By (2.4), (3.2)
is not one convenient ansatz among several: after normalization it is the operation
forced at the first nonempty degree.

At `s=1`, (3.2) is the self-dual/anti-self-dual split of `p wedge A`. At `s=2`, it
is the chiral Weyl part of the linearized curvature. These are regression names;
they do not define the general operation.

## 4. Gauge annihilation is computed on the same input

Take a polarized gauge parameter

```text
epsilon=v_2 symmetric-product ... symmetric-product v_s.
```

The gauge map constructs

```text
P_p epsilon=p symmetric-product v_2 symmetric-product ... symmetric-product v_s.
```

Evaluate (3.2) on that same amplitude. One factor in every chiral product is

```text
b_+(p,p)=pr_+(p wedge p)=0,
b_-(p,p)=pr_-(p wedge p)=0.                             (4.1)
```

Therefore

```text
K_s(p)P_p epsilon=(0,0).                               (4.2)
```

Polarized symmetric tensors span the parameter carrier, so (4.2) holds for every
`epsilon`. The generated operation descends to the potential gauge quotient. This
is the internal proof attached to the returned tool; a component cancellation is
not its origin.

## 5. The null screen computes the physical-shell isomorphism

Let a nonzero null momentum factor as

```text
p=lambda tensor bar(lambda).                            (5.1)
```

Choose temporary spinors `mu,bar(mu)` satisfying

```text
epsilon(lambda,mu)=1,
bar(epsilon)(bar(lambda),bar(mu))=1.                    (5.2)
```

N4a's two trace-free screen endpoint lines have representatives

```text
v_+=lambda tensor bar(mu),
v_-=mu tensor bar(lambda),                              (5.3)
```

up to the helicity-sign convention. Substitution into (3.1) computes

```text
b_+(p,v_+)=lambda symmetric-product lambda,
b_-(p,v_+)=0,

b_+(p,v_-)=0,
b_-(p,v_-)=bar(lambda) symmetric-product bar(lambda).   (5.4)
```

Applying (3.2) to the same rank-`s` endpoint amplitudes gives

```text
K_s(v_+^s)=(lambda^(2s),0),
K_s(v_-^s)=(0,bar(lambda)^(2s)).                        (5.5)
```

N4 identifies the two right-hand lines as its direct chiral kernels. N4a proves
that the two left-hand lines exhaust the potential quotient. Since (4.2) makes the
map quotient-defined and (5.5) is nonzero on both one-dimensional summands, it
constructs the little-group isomorphism

```text
bar K_s:
ker D_s(p)/im R_s(p)
  ~= ker D_s^+(p) direct-sum ker D_s^-(p).              (5.6)
```

Changing `mu` by a multiple of `lambda`, or `bar(mu)` by a multiple of
`bar(lambda)`, changes (5.3) by the gauge direction `p`; equation (4.2) removes
that change. Thus the temporary complement verifies (5.6) without becoming part
of the invariant output.

## 6. Why the inverse is not a local polynomial operation

The forward symbol is homogeneous:

```text
K_s(t p)=t^s K_s(p).                                    (6.1)
```

Suppose a polynomial local inverse `L(p)` of nonnegative homogeneous degree `r`
existed on the physical quotient. Evaluating the proposed composite at the same
rescaled nonzero null momentum would give

```text
[L(t p)K_s(t p)]=t^(r+s)[L(p)K_s(p)].                  (6.2)
```

The quotient identity is unchanged by rescaling `p`, because
`im R_s(tp)=im R_s(p)` for `t!=0`. Equality with that identity would require

```text
r+s=0.                                                 (6.3)
```

For `s>=1`, no nonnegative polynomial degree satisfies (6.3). A shellwise inverse
must therefore introduce negative momentum degree, a complement/normalization, or
another nonlocal resource. N10j supports a local forward map and an isomorphism of
physical fibers; it explicitly rejects a polynomial local inverse. Hence it does
not claim local-complex equivalence.

## 7. Retained interface and checks

The returned operation is

```text
CurvatureCompatibility(
  generated potential system,
  integer spin s,
  chiral bivector resources,
  derivative budget)
 -> degree-s K_s^+ direct-sum K_s^-,
    multiplicity trace,
    gauge/covariance/shell certificates,
    provenance,
    inverse obstruction or resource refusal.            (7.1)
```

The executable evaluator represents symmetric spinors by homogeneous polynomials.
For spins `1` through `6`, it verifies without spacetime tensor expansion:

- no admitted degree below `s` and multiplicity one at `s`;
- exact annihilation of a polarized gradient gauge input;
- nonzero, separated images of both screen endpoint lines;
- covariance under independent determinant-one transformations of `S` and
  `bar S`.

The transfer and use checks are distinct. Transfer changes `s` without supplying
the expected output coefficients. Use passes the generated spin-two packet to
N10i, which then admits the potential routes for curvature output and charges
recovery order `2`. Without that packet the same selector request still refuses.
A request for a polynomial local inverse refuses even with the packet.

## 8. Global effect and stop boundary

The supported spine is now

```text
potential gauge residual -> generated field system            [N10c]
  -> missing invariant output                                 [N10i]
  -> minimal-degree carrier obstruction
  -> generated curvature operation                            [N10j]
  -> same potential/direct physical lines                     [N4/N4a]
  -> revised capability-relative presentation comparison      [N10j using N10i].
```

This closes the missing same-output bridge for separate finite integer helicity.
It does not make the potential route cheaper: recovering curvature costs `s`
derivatives, while the direct route stores it as the field. Nor does it give the
direct route the action, source, or causal capabilities already owned by N4m.

Further curvature identities or mixed-symmetry generalization would not change the
current selector. N10k now consumes the returned operation in N4m's causal source
route. It proves equality with curvature-first scalar-wave transport and exposes
the rank obstruction to an unrestricted first-order chiral source Green map. The
remaining re-entry condition is a constructed compatible curvature-source complex,
not another rank check.

## Edges

- `N2b/N4 -> N10j`: pass the chiral bivector split and direct curvature target.
- `N10c/N4a -> N10j`: pass the generated potential gauge map and its exact
  physical null-screen quotient.
- `N5/N10i -> N10j`: pass the common-fiber-only boundary, typed missing
  curvature-output certificate, and retained selector operation; N10j owns the
  strengthened integer-spin comparison and re-evaluation after generating the
  packet.
- `N10j -> N10k`: pass `K_s` as an operation to be applied before or after scalar
  causal transport rather than reconstructed from this proof.
