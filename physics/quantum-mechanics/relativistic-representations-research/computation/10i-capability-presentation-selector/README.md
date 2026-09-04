# N10i computation — capability-relative presentation selector

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10i-capability-presentation-selector/check-presentation-selector.mjs
```

The selector accepts a parity-paired positive integer helicity, required output
capabilities, and optional upper bounds on named cost axes. It then:

1. constructs only the three routes already certified by the worktable;
2. removes routes lacking a required witness;
3. removes routes exceeding the resource budget;
4. returns every nondominated survivor under componentwise cost order.

It deliberately refuses weighted scoring. Operator order, carrier content, gauge
depth, recovery depth, and raw execution size have no intrinsic common unit.

The regression demonstrates four distinct outcomes: the spin-two realization
trade remains plural; the direct curvature route dominates the realization-only
spin-three bench under the declared axes; an action/source/causal request selects
the completed potential machine; and a higher-spin potential/curvature request
without a generated certificate returns a typed refusal. N10j later invokes this
same selector with its spin-indexed compatibility packet, which admits the forward
curvature capability while retaining refusal of a polynomial local inverse. The
program does not enumerate new Lorentz carriers or claim global minimality.
