# N10d — Generated Compact-Source Causal Use

Status: supported as a generated-to-causal interoperability bench for the Maxwell
specialization; single-instance computational gain rejected, while N10e closes the
first higher-spin source transfer and Clifford causal transfer remains open  
Consumes: [N10c generative residual constructor](10c-generative-residual-constructor.md)
and [N4e Maxwell Green construction](04e-maxwell-green-construction.md)  
Computation: [generated compact-source causal use](../computation/10d-generated-causal-use/README.md)  
Produces: an internally constructed compact conserved current, one retarded-support
witness, one nonzero physical-shell class, and a complete shared-cost audit

## Research contract

- **Obstruction:** N10c generated equations and passed an off-shell symbol test,
  but no generated object had yet acted on a spacetime source. A rational `Q^-1`
  cannot choose retarded support or prove that a physical shell class survives.
- **Capability:** start with N10c's returned field system, construct rather than
  assume an admissible compact source, pass it through N4e's causal Green operation,
  and recover nonzero screen data.
- **Invariant target:** the same compact current class and its same null-shell
  transverse amplitude under the hand-assembled N4e route and generated N10c route.
- **Presumptions:** four-dimensional Minkowski spacetime, the N4e de Rham Green
  theorem, smooth compact support, and Fourier convention declared below.
- **Internal benchmark:** a separable bump current, one observation event, and one
  null momentum. The analytic construction owns conservation, support, and
  nonvanishing; numerical quadrature is only a finite witness.
- **Horizon:** this node does not regenerate the primitive de Rham grammar, prove
  the Green theorem, normalize a one-particle state, or transfer compact-source use
  to higher spin, half-integer spin, interactions, or curved spacetime.

## 1. The unresolved obstruction is use, not another equation

N10c returns

```text
R=P,
C=A-(1/2)PT,
D=Q-PA+(1/2)P^2T,
D+RC=Q.                                                (1.1)
```

This output is useful only if a downstream operation can consume it without
reconstructing the finished field equation. Spin one is the smallest complete
test. A rank-one field and rank-zero gauge parameter have no trace channel, so
specializing the same returned operations computes

```text
R=P,
C=A,
D=Q-PA.                                                (1.2)
```

Under the de Rham interpretation `P=d`, `A=delta`, and
`Q=d delta+delta d`, (1.2) becomes

```text
D=delta d.                                             (1.3)
```

This is not a separately imported Maxwell formula. It is the rank-one image of
the generated family. N4e then supplies the analytic operation that N10c cannot
construct from a polynomial symbol alone: the retarded and advanced Green maps
of `Q`.

## 2. Antisymmetry generates an admissible compact source

Define the standard smooth bump

```text
       { exp(-1/(1-s^2)),  |s|<1,
b(s) = {
       { 0,                |s|>=1,

chi(t,x,y,z)=b(t)b(x)b(y)b(z).                         (2.1)
```

It is not enough to choose a current and later test its divergence. Instead choose
a compact antisymmetric two-tensor `K` and apply the source-constraint operation:

```text
K^{01}=chi,
K^{10}=-chi,
J^mu=partial_nu K^{nu mu}.                             (2.2)
```

The same input `K` remains visible in the conservation computation:

```text
partial_mu J^mu
 =partial_mu partial_nu K^{nu mu}
 =(1/2)partial_mu partial_nu(K^{nu mu}+K^{mu nu})
 =0.                                                   (2.3)
```

Thus compactness comes from (2.1), and admissibility comes from applying a
nilpotent complex operation in (2.2)--(2.3). In the selected coordinate witness,

```text
J^0=-partial_x chi,
J^1= partial_t chi,
J^2=J^3=0.                                             (2.4)
```

Components appear only here to evaluate one finite witness; they did not discover
the current or prove its conservation.

## 3. The generated factorization constructs the causal response

Let `G^+` and `G^-` be N4e's retarded and advanced scalar wave Green maps. Since
they commute with the de Rham operations and `delta J=0`, define

```text
A^+/-=G^+/- J.
```

Then the generated factorization, on the same `J`, computes

```text
C A^+/-=delta G^+/-J=G^+/-delta J=0,

D A^+/-
 =(Q-RC)G^+/-J
 =J-RG^+/-CJ
 =J.                                                   (3.1)
```

So the generated object reaches an actual sourced solution. The support choice is
not hidden in `Q^-1`: it is the distinct analytic input `G^+` or `G^-`.

For `Box=partial_t^2-Delta`, the retarded component at the spatial origin is

```text
A_+^1(t,0)
 = integral_[[-1,1]^3]
   b'(t-|y|) b(y_1)b(y_2)b(y_3)/(4 pi |y|) d^3y.       (3.2)
```

At `t=2`, support restricts the integral to `1<|y|<sqrt(3)`. There
`0<2-|y|<1` and `b'(2-|y|)<0`, so (3.2) is strictly negative. The advanced
argument is `2+|y|>1`, outside the temporal support, hence

```text
A_+^1(2,0)<0,
A_-^1(2,0)=0.                                          (3.3)
```

The potential component in (3.3) is a boundary-selected Lorenz representative,
not by itself the gauge-invariant endpoint. Its role is to prove that the generated
field system reached the causal spacetime consumer.

## 4. The same source has nonzero physical-shell content

Use

```text
f^(omega,k)=integral exp(i(omega t-k.x)) f(t,x) dt d^3x.
```

At the future-null covector

```text
p=(omega,0,0,omega),  omega=1/2,                       (4.1)
```

the `x`-polarized screen component of (2.4) is

```text
J^1(p)=-i omega chi^(p),

chi^(p)=B(omega)^2 B(0)^2,
B(a)=integral_[-1,1] b(s) cos(a s) ds.                 (4.2)
```

Both `B(0)` and `B(1/2)` are positive because `b` is positive inside its
support and `cos(s/2)>0` on `[-1,1]`. Therefore

```text
|J^1(p)|=omega B(omega)^2B(0)^2>0.                     (4.3)
```

At (4.1), an equation-exact source shift lies in `span(p)` and has no transverse
`x` component. Equation (4.3) therefore constructs a nonzero class in

```text
p^perp/span(p),                                        (4.4)
```

the physical screen quotient recovered in N4e. Continuity makes the amplitude
nonzero on a shell neighborhood, so this is not merely a measure-zero numerical
accident. No polarization basis beyond the one named observable is used.

## 5. Executable witness

The computation packet first imports and checks the actual N10c return value; it
does not type the Maxwell coefficients as an alternative input. It then evaluates
(3.2) at increasing midpoint resolutions and (4.2) by Simpson integration:

| Quantity | Computed value |
| --- | ---: |
| `B(0)` | `0.4439938162` |
| `B(1/2)` | `0.4352796692` |
| `|J^1(p)|` | `0.01867500010` |
| retarded `A_+^1(2,0)`, `52^3` cells | `-0.00006082581819` |
| relative change from `36^3` | `0.00025913` |
| advanced `A_-^1(2,0)` | `0` |

The exact statements are conservation (2.3), strict signs and support (3.3), and
nonvanishing (4.3). Quadrature checks implementation coincidence with those
statements; it is not their proof.

## 6. Same-output comparison rejects single-instance gain

Both routes now compute the same source class, the same boundary-selected response,
and the same shell amplitude:

```text
hand route:
  de Rham complex -> Maxwell completion -> J -> G^+/-J -> screen class

generated route:
  typed grammar -> enumerate/normalize/solve/refuse
  -> specialize returned FieldSystem -> J -> G^+/-J -> screen class. (6.1)
```

The source construction, Green theorem, Fourier transform, and numerical work are
shared. For this single spin-one prediction, the generated route additionally pays
for grammar normalization, word enumeration, rational elimination, carrier search,
and specialization. It is therefore not a computational reduction of N4e.

What survives is a different, reusable capability:

- equation coefficients and constraints retain their construction provenance;
- insufficient resource budgets produce obstruction records;
- one operation already transfers across bosonic and Clifford grammars;
- the returned bosonic object interoperates with a causal consumer.

These are generative and maintenance gains, not yet prediction-cost gains. An
amortized advantage across many carriers or a source constructor that eliminates
new hand assembly remains a hypothesis, not a result.

## 7. Global verdict and bounded next frontier

```text
N10/N10c obstruction-generated local complex
  -> N10d compact admissible source
  -> N4e retarded/advanced Green operation
     |- causal spacetime response
     `- null-shell screen class
  -> same-output cost audit.                           (7.1)
```

The use obstruction is closed for the Maxwell specialization: a generated system
does drive a compact-source causal prediction and recovers physical-shell content.
The stronger thesis—generation reduces the cost of one prediction—is rejected on
this bench.

N10e now consumes the hidden obstruction. For `s>1`, paired source conservation
`R_s^dagger J=0` and the Green condition `C_sS=0` require an adapter. Treating
`R^dagger M-C` as the residual generates `M=I-(1/4)UT`, its finite-spin inverse,
and an identity-only refusal. A compact conserved spin-two current then fails the
unadapted `C` constraint, passes after `S=M_2^(-1)J`, and yields causal plus
helicity-two outputs. Thus the transfer discriminator is supported without
hand-restoring N4f's formula.

The remaining next discriminator is Euler construction: determine whether the same
retained algebra generates formal self-adjointness of `MD`, or whether that stronger
capability needs new resources. Neighboring-framework comparison, Clifford source
transfer, arbitrary carriers, countable spin, and interactions remain separate.
