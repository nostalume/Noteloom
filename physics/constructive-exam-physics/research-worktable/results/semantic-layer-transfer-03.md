# Semantic-layer transfer result 03

## Question

Does separating domain-specific meaning from general mathematical relations create
a coherent route back to the original physics, or merely rename equations?

## Cross-domain extraction table

| Problem | `P0`: specific physics | `P1/M1`: extracted skeleton | Generic computation | Return ledger |
| --- | --- | --- | --- | --- |
| A25-05 dielectric | Gauss law, constitutive `D=epsilon E`, polarization | scalar source `D` generates field shape `E=KD`; voltage is linear functional | `U=L(KD)=L(K)D` | electric units, `epsilon>0`, planar boundary, bound-charge sign |
| A24-05 rod | Faraday induction, Ohmic heating | scalar source `dI/dt` generates field shape `E=Ku`; heating is quadratic functional | `P=<u,K* sigma K u>` | loop orientation, cylindrical measure, conductivity, averaging |
| A23-05 coil | flux induction, R-L dynamics, mechanical opposition | harmonic linear response followed by quadratic loss | pull loss through inverse impedance, then divide by `omega` | phase convention, steady state, average versus instantaneous torque, resisting sign |
| A25-02 orbit | Newtonian central gravity and tangential impulse | conserved latent quantities plus a turning-point relation | eliminate energy and angular momentum | positive radius, impulse point, bound-orbit range, pericentre/apocentre meaning |

## Strong transfer

The dielectric and conducting-rod cases share a nontrivial intermediate skeleton:

```text
one source amplitude -> field shape -> target functional.
```

Linear and quadratic targets give respectively

```text
L(Ku)=L(K)u,
<Ku,WKu>=<u,K*WKu>.
```

This common computation removes the distributed field as an independent unknown.
Returning the result requires different physical ledgers, so the unification does
not assert that displacement and current rate are the same physical quantity.

## Weaker transfer

The satellite joins the other cases only at the coarser relation-elimination layer.
It does not justify the source-to-field abstraction. This gives a graded result:

```text
same physical law:                 no
same structural response pattern: dielectric and rod, yes
same target-conditioned relation operation: all four, yes
same return conditions:            no
```

The framework is therefore a hierarchy of shared semantics, not one flattened
analogy.

## Return obstruction

The rotating-coil case supplies a falsifier. Mapping phase-resolved current to its
magnitude squared supports average power but destroys the information required for
instantaneous torque. A proposed return to the instantaneous observable fails.
The required repair is forced: retain the complex phase or two real quadratures.

## Executable unseen-area transfer

The typed compiler was given a mechanics packet not used to motivate the original
electromagnetic cases:

```text
v_1=2v,
v_2=-v,
P=3v_1^2+5v_2^2.
```

It inferred rather than received

```text
K=(2,-1)^T,
Q=diag(3,5),
P=v^T K^T Q K v=17v^2.
```

The return ledger restored driving speed, damper-speed meanings, viscous regime,
positive-dissipation convention, and the power dimension. The returned relation
was checked both as a consequence of the original ideal and by reconstructing the
hidden damper speeds. This is transfer of one generated interface, not similarity
assigned after solving.

Seven semantic-compiler tests now cover the two electromagnetic regressions, this
mechanical transfer, lost phase, dimensional mismatch, field-budget refusal, and a
nonlinear source-to-field refusal.

## Verdict

The user's three-step speculation survives the bounded test after one correction:

```text
separate specific and general knowledge
  -> extract at a declared semantic resolution
  -> compute on the shared mathematical relation
  -> lift through a retained physical-context ledger
  -> refuse or descend if the lift fails.
```

The return is not an inverse transformation because abstraction loses information.
It is a certified contextual lift. This layer-relative view is a stronger spine
than a single universal relation language because it explains both transfer and
the point where transfer ceases to preserve the requested physics. The next open
bridge is extraction of a richer skeleton—multiple sources, nonlinear maps, or
phase-resolved response—without encoding the expected reduced answer.
