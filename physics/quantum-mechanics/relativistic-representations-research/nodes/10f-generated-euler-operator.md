# N10f — Obstruction-Generated Bosonic Euler Operator

Status: supported for every separate finite symmetric integer-spin carrier in four
dimensions; the generated operator supplies a free quadratic action and consumes
N10e's physical spin-two current; N10g closes Clifford transfer, while normalization,
interactions, and single-instance gain remain open  
Consumes: [N10c generative residual constructor](10c-generative-residual-constructor.md),
[N10e generated source adapter](10e-generated-source-adapter.md), and
[N4c action-completion audit](04c-action-completion-audit.md)  
Computation: [generated Euler operator](../computation/10f-generated-euler-operator/README.md)  
Produces: an independently generated Euler multiplier, identity-only refusal,
constraint-factorized adjoint certificate, quadratic-action interface, and sourced
spin-two Euler response

## Research contract

- **Upstream anchor:** N10c generates the equation `D`; N10e generates a physical-
  source adapter but does not establish variational integrability.
- **Bridge question:** can failure of `D` to be formally self-adjoint generate an
  equation-equivalent Euler operator, or does action capability require new
  resources?
- **Invariant target:** the same vacuum solutions, gauge classes, compact spin-two
  current, and sourced response carried by N10c--N10e.
- **Downstream effect:** success makes the retained bosonic output action-capable;
  failure would separate physical-source compatibility from variational dynamics.
- **Special resources:** four-dimensional Lorentz metric, Fischer pairing,
  double-traceless carrier, traceless parameter, and compact-support/boundary
  convention.
- **Internal benchmark:** generate or refuse a normalized left multiplier using at
  most one metric insertion; factor every remaining adjoint defect through `T^2`;
  verify spins `2--6`; recover N10e's same physical current through `E phi=J`.
- **Horizon:** overall normalization, positivity, boundary charges, canonical
  variables, quantization, interactions, arbitrary carriers, and Clifford reality
  data are outside this node.

## 1. A source adapter is not yet an action

N10e constructed `S=M^(-1)J` so a physical conserved current can enter N10c's
scalar Green operation. A quadratic action needs a stronger property. For

```text
I[phi]=(1/2)<phi,E phi>,                                (1.1)
```

the two cross terms in `I[phi+t delta phi]` combine into one Euler variation only
when `E` is formally self-adjoint on the declared field carrier. Thus the new
capability is

```text
E^dagger=E on F_s=ker T^2,
ker E=ker D.                                            (1.2)
```

Equation (1.2) is not supplied by the source identity `R^dagger M=C`; it defines an
independent obstruction problem.

## 2. The equation itself is the cheapest failed candidate

Use the Lorentz-metric Fischer pairing already constructed by the need to couple a
source. Its primitive adjoints are

```text
P^dagger=A,
T^dagger=U,
Q^dagger=Q.                                            (2.1)
```

N10c returns

```text
D=Q-PA+cP^2T,
c=1/2.                                                  (2.2)
```

The normalized cheapest Euler candidate is `E_0=D`; choosing zero would lose the
equation. Apply (2.1) to the same returned operation:

```text
D^dagger=Q-PA+cUA^2,

D-D^dagger=c(P^2T-UA^2).                               (2.3)
```

Neither channel in (2.3) begins with `U^2` or ends with `T^2`, so it is visible in
the pairing on `F_s`. The identity-only multiplier is therefore refused. This is
the action obstruction; it is not a post-hoc check of a known Euler tensor.

## 3. The skew defect constructs the minimal correction

The two channels in (2.3) differ by replacing a trace-removing operation with its
metric adjoint. A rank-preserving zero-order repair must consequently use the
smallest trace/metric composite `UT`. Set

```text
M=I+mUT,
E=MD.                                                   (3.1)
```

To compute the correction, keep the semantic composites rather than expanding
tensor components. The self-adjoint middle term `-PA` gives

```text
-UTPA+PAUT=2(P^2T-UA^2),                               (3.2)
```

because `TP=PT+2A` and `AU=UA+2P`. The trace term gives

```text
UTP^2T-UA^2UT
 =UP^2T^2-U^2A^2T,                                    (3.3)
```

since both intermediate `4UPAT+2UQT` contributions coincide and cancel. Combining
(2.3), (3.2), and (3.3) computes the complete residual on the same field input:

```text
MD-D^dagger M
 =(c+2m)(P^2T-UA^2)
   +mc(UP^2T^2-U^2A^2T).                              (3.4)
```

The second line already belongs to the double-trace constraint ideal. Cancelling
the first line forces

```text
m=-c/2=-1/4.                                           (3.5)
```

The executable constructor reads `c` and the `PA` coefficient from N10c's actual
`D`, generates the correction image, and solves (3.4) over exact rationals. It does
not receive (3.5) as input.

## 4. The remaining defect vanishes for semantic reasons

Substitution of the generated coefficient gives

```text
E=MD,
M=I-(1/4)UT,

E-E^dagger
 =(1/8)(U^2A^2T-UP^2T^2).                              (4.1)
```

This is not zero as an ambient polynomial operator. Formal self-adjointness is a
statement on the constructed carrier. For arbitrary `phi,psi in ker T^2`, evaluate
both terms in the same Fischer pairing:

```text
<psi,U^2A^2T phi>=<T^2psi,A^2T phi>=0,
<psi,UP^2T^2phi>=0.                                    (4.2)
```

Therefore

```text
<psi,E phi>=<E psi,phi>                                (4.3)
```

for every finite `s`. Finite natural-map matrices check the ambient factorization
and restricted pairing for spins `2` through `6`; (4.2) owns the uniform result.

## 5. Two independent obstructions select one retained operation

Only after generating `M` from (2.3)--(3.5) compare it with N10e's source output:

```text
M_action=I-(1/4)UT=M_source.                            (5.1)
```

This equality has a consequential meaning:

```text
source obstruction:
  R^dagger M=C
  -> physical J maps to admissible S=M^(-1)J;

action obstruction:
  MD=(MD)^dagger on ker T^2
  -> Sourced equation is the variation of one quadratic functional. (5.2)
```

The two constructions share no expected coefficient input. Their coincidence
compresses two interfaces into one generated operation rather than maintaining
separate trace corrections.

Invertibility from N10e preserves the vacuum equation:

```text
E phi=0
 iff MD phi=0
 iff D phi=0.                                          (5.3)
```

Gauge invariance also reuses a generated identity rather than a new calculation:

```text
E R=M D R=0.                                           (5.4)
```

## 6. The generated operator constructs the quadratic action

For compact fields, or a declared boundary convention removing integrations by
parts, define the returned functional operation

```text
I[phi;J]
 =(1/2) integral <phi,E phi> dx
  -integral <phi,J> dx.                                (6.1)
```

Evaluate it on the same variation `delta phi`. The two kinetic cross terms coincide
by (4.3), so

```text
d/dt I[phi+t delta phi;J]|_(t=0)
 =integral <delta phi,E phi-J> dx.                     (6.2)
```

Nondegeneracy of the restricted Fischer pairing turns stationarity into

```text
E phi=J.                                               (6.3)
```

For an admissible physical current, N10e supplies `S=M^(-1)J`. N10c then constructs
`D G_QS=S`, and the generated Euler composite recovers the same current:

```text
E G_QM^(-1)J
 =M D G_QM^(-1)J
 =M M^(-1)J
 =J.                                                   (6.4)
```

At N10e's off-shell spin-two probe, the executable result is

```text
||D phi-S||=2.22e-16,
||E phi-J||=3.33e-16.                                  (6.5)
```

Thus the new output is consumed at the physical source endpoint; it does not end as
a formal adjoint proof.

## 7. Global verdict and bounded frontier

```text
representation/locality obstruction
  -> generated (R,C,D)
  -> physical-source obstruction -> generated M_source
  -> variational obstruction      -> generated M_action
  -> M_source=M_action
  -> retained quadratic action and causal source response. (7.1)
```

Within the declared finite symmetric bosonic grammar, the retained tool now reaches
the whole free classical chain: local complex, constrained carriers, physical-source
adapter, causal response, Euler operator, and quadratic action. The new capability
is real, but it is not predictive novelty or single-instance computational leverage;
N4c already supplies the hand-derived baseline, and obstruction solving adds work
for one field.

The supported compression is generative: one multiplier, independently selected by
two failures, serves source conversion, equation equivalence, variational
integrability, and gauge response across finite spin. Further bosonic examples would
not change that claim, so this branch stops.

[N10g](10g-clifford-source-euler-transfer.md) now closes the Clifford transfer: its
source and Euler obstructions independently generate the two-layer Clifford
multiplier and consume it in a sourced response. The weakest consequential bridge
has moved upstream to generating the primitive operator grammar from Lorentz-carrier
data. Full normalization, quantization, interactions, arbitrary-carrier completion,
and neighboring-framework comparison remain parked.
