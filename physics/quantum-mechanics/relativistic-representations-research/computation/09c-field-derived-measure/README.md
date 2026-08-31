# N9c field-derived coupling-measure regression

This computation evaluates the bounded N9c bench on a fixed-total-momentum scalar
particle--boson fiber. It uses no dressed Fock-space eigenvector.

Run from the repository root:

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/09c-field-derived-measure/field_measure_regression.py
```

The declared parameters are

```text
particle mass M=2,
boson mass mu=1,
Gaussian cutoff Lambda=1,
coupling g=0.2,
h(k)=exp(-|k|^2/2).
```

At total momentum zero, the vacuum preparation leaves through
`B Omega=g a^dagger(h)Omega`. At order `g^2`, the return visits only the free
one-boson sector with energy

```text
epsilon(k)=sqrt(|k|^2+mu^2)+|k|^2/(2M).
```

The program verifies four realizations of its pushforward spectral measure:

- radial field momentum integration;
- energy-density integration;
- Stieltjes self-energy and bound observables;
- Fourier memory and a two-site moment chain.

Acceptance checks cover measure normalization, negative bound-energy shift,
prepared residue, mass enhancement, the square-root continuum threshold, equality
of the radial and energy Fourier routes, the `t^-3/2` memory tail, exact matching of
the first four chain moments, and off-axis self-energy accuracy.

The one-boson resummed pole and residue are diagnostics of the constructed leading
measure. Only their order-`g^2` expansions are claimed as controlled predictions of
the full Fock Hamiltonian; full higher sectors and removal of the boson-mass
regularization are outside this research horizon.

The script prints both the order-`g^2` expansion of `M_eff` and the reciprocal of
the truncated inverse mass. The latter is labeled a diagnostic because taking
that reciprocal retains uncontrolled higher powers of `g`.
