# Sine-Gordon Breather Pole Regression

Question: does the physical-strip pole produce the declared breather mass,
stability gap, Poincare curvature, and shallow-binding mechanical limit?

Run:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/04w-sine-gordon-breather/check-breather-pole.mjs
```

The deterministic check evaluates several attractive couplings and verifies:

1. `s(iu_n)=m_n^2` with
   `u_n=pi(1-n xi)` and `m_n=2M_s sin(n pi xi/2)`;
2. the allowed breather masses increase with `n` and stay below the constituent
   threshold where their pole exists;
3. the first-breather neutral stability gap is positive;
4. at `xi=1/2`, `m_1=sqrt(2)M_s` and shell curvature is `1/m_1`;
5. the exact binding formula tends to `kappa^2/M_s` as the pole approaches the
   two-soliton threshold.

This script checks kinematics and inequalities only. It does not derive the exact
S-matrix, its residue, a local form factor, or the quantum field theory.
