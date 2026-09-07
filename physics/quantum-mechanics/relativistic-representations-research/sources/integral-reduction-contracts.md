# Integral reduction contracts

These sources delimit established tensor/master-integral reduction from the
project's narrower semantic denominator quotient. They do not prove node 20's
algebra, which is constructed and certified internally.

## Anastasiou--Karlen--Vicini 2023

- Primary source: C. Anastasiou, J. Karlen, and M. Vicini, *Tensor reduction of
  loop integrals*, [arXiv:2308.14701v2](https://arxiv.org/abs/2308.14701).
- Hypotheses used here: a dimensionally regulated loop integral with tensor
  numerators and a declared external-momentum space.
- Contracted output: tensor structures may be organized using external momenta and
  the metric transverse to their span, with scalar coefficients obtained through a
  dual basis.
- Research use: expert baseline for the claim that invariant tensor reduction can
  avoid repeated component systems. Node 20 uses a still smaller two-point
  denominator quotient because its two denominators span all loop invariants.
- Boundary: the paper does not generate this project's action vertices, Ward
  packet, observable quotient, or complete-route leverage claim.

## Laporta 2000/2001

- Primary source: S. Laporta, *High-precision calculation of multi-loop Feynman
  integrals by difference equations*,
  [arXiv:hep-ph/0102033](https://arxiv.org/abs/hep-ph/0102033).
- Hypotheses used here: a fixed integral family and dimensional regularization in
  which integration-by-parts relations can be generated and ordered.
- Contracted output: generic integrals can be reduced algorithmically to a selected
  set of master integrals, with difference/differential equations used for their
  evaluation.
- Research use: downstream theorem/tool boundary if a future packet leaves
  irreducible scalar products or higher denominator powers after semantic lowering.
- Boundary: an IBP solver does not decide the action, graph packet, physical
  quotient, regulator compatibility, or whether constructing the reduction is
  cheaper for the requested observable.

## Denner--Dittmaier 2005

- Primary source: A. Denner and S. Dittmaier, *Reduction schemes for one-loop tensor
  integrals*, [arXiv:hep-ph/0509141v2](https://arxiv.org/abs/hep-ph/0509141).
- Hypotheses used here: one-loop tensor integrals, including kinematic regions in
  which conventional Gram-determinant reduction becomes unstable.
- Contracted output: tensor coefficients can be reduced to scalar integrals using
  schemes adapted to small or vanishing Gram determinants.
- Research use: failure boundary for future multi-leg transfer. Node 20's
  two-point substitution does not invert a Gram matrix, so that instability is not
  present in the active bench.
- Boundary: numerical stability and general one-loop coverage do not imply Ward
  closure or semantic compression for the current observable.
