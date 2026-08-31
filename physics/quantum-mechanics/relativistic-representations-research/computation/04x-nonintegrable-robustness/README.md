# Nonintegrable Composite Robustness Regression

Question: once certified first-order mass bounds are supplied, does the N4w
first-breather stability gap survive, and does the semilocality test distinguish
the channel-preserving and confining perturbations?

Run:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/04x-nonintegrable-robustness/check-stability-budget.mjs
```

The deterministic check verifies:

1. the `xi=1/5` benchmark has `beta^2=4 pi/3`, a relevant and first-order
   strictly renormalizable second harmonic, four breather poles, and
   `m_1/M_s=2 sin(pi/10)`;
2. `cos(2 beta phi)` has zero soliton annihilation residue and equal values on
   every old vacuum, while `cos(beta phi/2)` has nonzero residue and alternating
   old-vacuum values;
3. for declared Lipschitz bounds `C_s,C_1`,

   ```text
   d(eta)/M_s >= d_0/M_s-[2 max(C_s,C_1)+C_1]|eta|;
   ```

4. adversarial mass shifts inside those bounds cannot close the gap below the
   computed safe radius;
5. a nonzero local-field overlap remains nonzero under the declared continuity
   inequality.

The numerical `C_s,C_1` fixture exercises the bound only. It is not a physical
form-factor evaluation. A predictive deformation radius requires NI-04/NI-05's
form factors, normalization, remainders, and continuum control.
