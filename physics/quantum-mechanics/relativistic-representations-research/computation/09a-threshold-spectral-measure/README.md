# N9a threshold spectral-measure computation

This regression evaluates the one-level Friedrichs model used in N9a without
external numerical packages. It does not discover the spectral measure; it tests
the consequences once the measure

```text
m(lambda) d lambda = G lambda exp(-lambda) d lambda
```

has been constructed from the coupling to the eliminated continuum.

Run from the repository root:

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/09a-threshold-spectral-measure/threshold_spectral_measure.py
```

The script independently checks:

- the unique below-threshold root and its residue;
- atom-plus-continuum normalization in the bound case;
- purely continuous normalization in the open case;
- cutoff refinement from `30` to `40`;
- unitarity of the boundary-ratio scattering factor; and
- the logarithmically divergent first memory moment despite an integrable
  `t^-2` memory tail.

The computation uses the convergent series for `Ei`, an asymptotic scaled form on
the far positive tail, bisection, and adaptive Simpson quadrature. Its complexity
is scalar root finding plus one-dimensional quadrature. That reduction is a
property of the rank-one model, not evidence that constructing a realistic
field-theory coupling measure is cheap.
