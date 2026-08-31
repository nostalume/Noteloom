# N9g kinetic-scale regression

This computation evaluates the kinetic generator constructed from N9d's
coupling-free density:

```text
A=pi m_0(Delta)+i PV integral dnu_0(x)/(Delta-x),
gamma_0=2 Re A.
```

Run from the repository root:

```powershell
python -B physics/quantum-mechanics/relativistic-representations-research/computation/09g-kinetic-scale/kinetic_scale.py
```

It reports the rate, Lamb phase, physical times corresponding to fixed kinetic
times, the bounded exponential comparator versus its secular tangent, and the
growth of N9f's fixed-time remainder after `t=tau/g^2`.

The exponential is theorem-supported for the excitation-conserving Friedrichs
comparator. The script does not simulate or certify N9e's complete Fock dynamics;
that transfer is the explicit obstruction recorded in N9g section 4.
