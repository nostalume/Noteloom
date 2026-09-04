# N10e — Obstruction-Generated Higher-Spin Source Adapter

Status: supported for every separate finite symmetric integer-spin carrier in four
dimensions, with an actual compact spin-two causal/shell consumer; N10f independently
generates the coincident Euler multiplier, while Clifford transfer and
single-instance prediction gain remain open  
Consumes: [N10c generative residual constructor](10c-generative-residual-constructor.md),
[N10d Maxwell causal use](10d-generated-causal-use.md), and
[N4f finite-spin Green construction](04f-finite-integer-spin-green-construction.md)  
Computation: [generated source adapter](../computation/10e-generated-source-adapter/README.md)  
Produces: a retained source-adapter constructor, identity-only refusal, exact
cross-spin inverse, compact spin-two source, causal response, and helicity-two shell
witness

## Research contract

- **Upstream anchor:** N10c returns `(R,C,D)` and the scalar-wave response interface;
  N10d proves use only where Maxwell makes the source adapter invisible.
- **Bridge question:** can the mismatch between paired source conservation and
  `C S=0` generate the missing adapter rather than importing N4f's trace reversal?
- **Invariant target:** the same compact conserved current `J`, its adapted Green
  input `S`, and the same spin-two screen contrast used by the generated and N4f
  routes.
- **Downstream effect:** success promotes the retained tool from equation generation
  to a pairing-compatible physical-source interface; failure would restrict it to
  vacuum complexes.
- **Special resources:** four-dimensional Lorentz metric, Fischer pairing,
  double-traceless symmetric carrier, traceless parameter, one metric-insertion
  layer, and one frame-oriented compact source preparation.
- **Internal benchmark:** generate or refuse `M`; test its inverse for spins `2--6`;
  then require one compact spin-two current for which `CJ !=0` but
  `C M^(-1)J=0`, followed by causal and shell recovery.
- **Horizon:** no arbitrary carrier, full action, interacting current, Clifford
  source, curved background, countable-spin completion, or computational-leverage
  claim is included.

## 1. Maxwell concealed a missing semantic map

N10c's returned factorization accepts a Green source `S` satisfying

```text
C S=0.                                                 (1.1)
```

A physical current is instead defined through the carrier pairing: gauge invariance
of `<phi,J>` requires

```text
<R epsilon,J>=<epsilon,R^dagger J>=0.                  (1.2)
```

At spin one, `C=R^dagger=A`, so N10d could pass directly from (1.2) to (1.1).
For higher spin, N10c generates

```text
R=P,
C=A-(1/2)PT.                                           (1.3)
```

The two source types no longer coincide. This is not an optional action refinement:
without a map between them, a conserved physical source cannot safely enter the
generated scalar-wave response.

## 2. The need to pair constructs the adjoint operation

The symmetric carrier is built from the Lorentz covector representation. Complete
metric contraction therefore constructs its invariant Fischer pairing. Evaluation
on the same two homogeneous polynomials gives

```text
<P epsilon,phi>=<epsilon,A phi>,
<U alpha,phi>=<alpha,T phi>.                           (2.1)
```

Thus `P^dagger=A` and `U^dagger=T`; no component inner product is introduced. The
parameter is traceless, so a target term in `im U` pairs to zero:

```text
<epsilon,U rho>=<T epsilon,rho>=0.                     (2.2)
```

The required adapter is now a typed operation `M:F_s->F_s` satisfying the paired
identity

```text
A M-C in im U.                                         (2.3)
```

Equation (2.3), rather than the known name “trace reversal,” defines the search.

## 3. The identity failure forces one metric insertion

Begin with the cheapest normalized candidate `M_0=I`. Substituting the generated
`C` from (1.3) into the common target of (2.3) computes

```text
A M_0-C=(1/2)PT.                                       (3.1)
```

This is not pure trace and cannot disappear in (2.2). The identity-only budget is
therefore refused with residual channel `PT`.

The obstruction contains one trace `T` and must return to the same field rank. The
smallest Lorentz-natural repair resource is consequently one metric insertion `U`.
On the double-traceless carrier, the canonical rank-preserving zero-order normal
words with at most one trace are

```text
{I,UT}.                                                (3.2)
```

Write `M=I+mUT`. Product differentiation constructs rather than assumes the image
of the new word:

```text
A U T
 =(U A+2P)T
 =UAT+2PT.                                             (3.3)
```

Substitution of (3.3) and (1.3) into the same residual gives

```text
A M-C
 =(2m+1/2)PT+mUAT.                                     (3.4)
```

The second channel is admitted by (2.2); cancelling the first forces

```text
m=-1/4,
M=I-(1/4)UT,
A M-C=-(1/4)UAT.                                       (3.5)
```

The executable constructor enumerates (3.2), forms the images in (3.3), and solves
the rational coefficient system against N10c's actual returned `C`. It does not
receive `-1/4` as input.

## 4. Invertibility is constructed on semantic trace layers

For `phi in ker T^2`, trace subtraction constructs the unique decomposition

```text
phi=h+Uk,
Th=Tk=0.                                               (4.1)
```

In four dimensions, product differentiation gives `T(Uk)=4s k`. Hence the generated
adapter acts diagonally on the two meaningful layers:

```text
M(h+Uk)=h+(1-s)Uk.                                     (4.2)
```

It is invertible for every separate `s>=2`. Rather than importing the inverse,
compose `I+mUT` with `I+n_sUT` on (4.1). Since `(UT)^2=4sUT` there, the nonidentity
coefficient is

```text
m+n_s+4s m n_s=0.
```

Substitution of the generated `m=-1/4` computes

```text
n_s=-1/[4(s-1)],
M_s^(-1)=I-[1/(4(s-1))]UT.                             (4.3)
```

Finite natural-map matrices verify (3.5) and (4.3) for spins `2` through `6`; the
two-layer calculation owns the all-finite-spin statement.

## 5. Antisymmetry constructs a discriminating spin-two current

Reuse N10d's compact scalar bump `chi`. Choose constant two-forms `B_x` and `B_y`
on the `t-x` and `t-y` planes and define the first-order operations

```text
L_a(u)=u^mu (B_a)_(mu nu) partial^nu,

J(u)=(L_x^2-L_y^2)chi.                                 (5.1)
```

This preparation selects a real spin-two screen orientation; it is physical source
data, not a claim that the dynamics selects a frame. The current is symmetric
because it is quadratic in `u`. Apply its divergence to the same input:

```text
A J
 =partial_mu partial/(partial u_mu)(L_x^2-L_y^2)chi
 =2[(B_x)_(mu nu)partial^mu partial^nu L_x
    -(B_y)_(mu nu)partial^mu partial^nu L_y]chi
 =0.                                                    (5.2)
```

Each last contraction vanishes because the derivative pair is symmetric and `B_a`
is antisymmetric. Thus (5.2) constructs `R^dagger J=0` without solving a component
conservation equation.

The bench must make the adapter necessary. Tracing (5.1) gives

```text
T J=2(partial_x^2-partial_y^2)chi,                     (5.3)
```

which is not zero. Therefore

```text
CJ=AJ-(1/2)PTJ=-(1/2)PTJ !=0.                         (5.4)
```

The physical current is conserved but is not itself an admissible input to N10c's
Green operation. Apply the generated inverse and compute on the same `J`:

```text
S=M_2^(-1)J,

C S
 =C M_2^(-1)J
 =R^dagger M_2 M_2^(-1)J
 =R^dagger J
 =0,

M_2S=J.                                                (5.5)
```

At the off-shell regression momentum `(1,0.3,0,0)`, the finite witness gives

```text
||TJ||=0.18,
||CJ||=0.09,
||CS||=6.77e-17,
||M_2S-J||=1.11e-16.                                   (5.6)
```

Thus the returned adapter changes an executable capability; it is not discarded
after proving (3.5).

## 6. The adapted source reaches causal and helicity-two outputs

Let `G^+/-` be N4f's scalar retarded/advanced maps on the spin-two carrier and set

```text
phi^+/-=G^+/- S.                                       (6.1)
```

Using `CS=0` from (5.5) in N10c's returned factorization computes

```text
D phi^+/-
 =(Q-RC)G^+/-S
 =S,

M D phi^+/-=M S=J.                                    (6.2)
```

Metric reinsertion changes the `xx` and `yy` entries equally. The selected screen
contrast therefore survives adaptation:

```text
S_xx-S_yy=J_xx-J_yy=2 partial_t^2 chi.                 (6.3)
```

At the spatial origin, its retarded value is

```text
Phi_+(t)=integral 2b''(t-|y|)b(y_1)b(y_2)b(y_3)
                    /(4 pi|y|) d^3y.                  (6.4)
```

Choose `t=2.5`. Source support restricts `1.5<|y|<sqrt(3)`, so
`3^(-1/4)<2.5-|y|<1`. Direct differentiation gives

```text
b''(s)=2b(s)(3s^4-1)/(1-s^2)^4>0                      (6.5)
```

on that region. Hence `Phi_+(2.5)>0`, while the advanced argument
`2.5+|y|>1` makes `Phi_-(2.5)=0`. The quadrature witness is

```text
Phi_+(2.5)=5.80543e-11,
relative change from 104^3 to 144^3=7.62e-5,
Phi_-(2.5)=0.                                           (6.6)
```

At `p=(omega,0,0,omega)`, `omega=1/2`, (5.1) restricts to the trace-free screen
tensor

```text
J_hat|_Q=-omega^2 chi_hat(p)
  (e_x tensor e_x-e_y tensor e_y).                     (6.7)
```

Its `xx-yy` contrast has magnitude

```text
2omega^2 B(omega)^2B(0)^2=0.01867500010>0.             (6.8)
```

This is a nonzero real combination of helicities `+2` and `-2`. The same current
has now passed conservation, adaptation, causal response, and physical-shell
recovery.

## 7. Global verdict and cost boundary

```text
N10c generated (R,C,D)
  -> source obstruction A-C=(1/2)PT
  -> N10e generated M, M^(-1), and refusal
  -> compact conserved J
  -> adapted S=M^(-1)J
  -> scalar causal Green response
  -> helicity-two screen class.                        (7.1)
```

This closes the source-interface gap for the finite symmetric bosonic family inside
the declared grammar. The tool now retains equation generation, carrier constraints,
budget refusals, and a physical-current-to-Green-input operation. N10d's Maxwell
success was not accidental; N10e exposes and repairs the structure it concealed.

The complete single-instance route is still not cheaper than N4f. Both routes need
the pairing, compact current, Green theorem, shell restriction, and observable
evaluation; the generated route additionally enumerates and solves the adapter.
Its supported gain is semantic and amortized: the same failure calculation produces
the coefficient, inverse family, and refusal instead of re-deriving trace reversal
for each spin. No predictive novelty or runtime leverage is claimed.

N10f now resolves the next bridge independently. Starting from `D`, not N10e's
answer, its skew-adjoint residual generates the same `M=I-(1/4)UT`; the remaining
defect factors through `T^2`, and the returned `E=MD` recovers this node's same
physical current. Thus source and action capabilities select one retained operation.
The next discriminator is Clifford source/Euler transfer. Neighboring-framework
comparison remains parked until that cross-family test delimits the generative claim.
