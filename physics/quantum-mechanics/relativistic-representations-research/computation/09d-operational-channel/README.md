# N9d operational-channel regression

This computation turns N9c's continuum boundary into a finite-time emitted-boson
event. It uses one two-level particle coupled to the same massive Gaussian scalar
field and retains the complete coefficient through order `g^2`.

Run from the repository root:

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/09d-operational-channel/operational_channel_regression.py
```

The declared parameters are

```text
particle mass M=2,
boson mass mu=1,
internal gap Delta=1.5,
Gaussian cutoff Lambda=1,
coupling g=0.01.
```

The smaller coupling keeps `Gamma t<0.25` over the longest finite-time check. This
does not make fixed-order perturbation uniform as `t` tends to infinity and is not
an error bound on omitted Dyson terms. It is only a secular-loss diagnostic for
the displayed coefficient.

Acceptance checks cover:

- negative ground-state shift, residue below one, and mass enhancement;
- positive on-shell excited-state density and its principal-value partner;
- equality of radial-field and pushed-forward density calculations of the complete
  emitted-boson event;
- the exact order-`g^2` identity
  `P_emit''(t)=2 Re[exp(i Delta t)K(t)]`;
- approach of `P_emit^(2)(t)/t` to `2 pi m(Delta)`;
- explicit monitoring of the secular parameter `Gamma t`.

The program does not exponentiate the survival law. A resonance, exponential
decay theorem, or scattering matrix needs additional analytic continuation or
wave-operator constructions and remains outside this benchmark.
