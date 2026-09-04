# N10g computation — generated Clifford source/Euler transfer

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10g-clifford-source-euler-transfer/check-clifford-transfer.mjs
```

`clifford-transfer-constructor.mjs` consumes N10c's generated Clifford complex,
not N4i's finished multiplier. It normal-orders the invariant Clifford operator
algebra, generates the wave-completion operator from `Q-S^2`, and solves two
independent exact-rational obstruction problems:

- constrained source compatibility `A M = B` modulo a leading `Y`;
- restricted formal self-adjointness `M S=(M S)^dagger` modulo the two
  `Gamma^3` field constraints in the pairing.

Both routes refuse the one-gamma-layer budget and return

```text
B=A-(1/2)L Gamma-(1/2)P Gamma^2,
M=I-(1/2)Y Gamma-(1/4)Y^2Gamma^2.
```

The executable matrix calculation is deliberately an independent bounded check,
not the construction. It uses one Dirac-matrix realization only to verify ranks
`1--4` at null and non-null momenta, and it consumes the generated multiplier in a
rank-two sourced Euler response.
