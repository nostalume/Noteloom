# N10v visible-measure compiler

This packet retains the common generator behind N10u's massless curvature detector
and N9c's massive scalar recoil channel:

```text
orbit radial Jacobian
  * observable shell weight
  * preparation weight
  -> positive radial departure measure
  -> monotone energy pushforward
  -> visible spectral measure.
```

The compiler never receives an expected spectral density, power, threshold
exponent, or observable result. It receives typed factor maps and either constructs
the pushforward or refuses when the energy map is not one-to-one on the declared
window.

Run from the repository root:

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/10v-visible-measure-compiler/visible_measure_compiler.py
```

Acceptance checks cover:

- generation of the massless scalar, Maxwell, and spin-two density ladder with
  powers `1,3,5`; the scalar angular compiler integrates the one-dimensional
  identity fiber separately instead of duplicating two chiral lines;
- generation of N10u's massless spin-two quintic density using the angular response
  compiled from the detector tensor;
- analytic mass, negative bound shift, and positive open boundary of that measure;
- transfer of the same interface to N9c's massive recoil dispersion;
- equality with N9c's independently implemented density and analytic total mass;
- recovery of the massive square-root threshold coefficient;
- a refusal certificate for a nonmonotone energy map whose branches were not
  supplied.

The scalar pushforward is supported only when rotations have already reduced the
visible channel and the radial energy is monotone. Anisotropic angular kernels,
multiband/noninjective dispersions, higher Fock returns, and finite-coupling error
control remain separately typed outputs rather than being hidden in a scalar
density.

The executable's finite-grid monotonicity audit is a regression guard, not a proof
for arbitrary user-supplied functions. Admission of a new analytic channel requires
the theorem-level positivity of its energy derivative, as constructed explicitly
for both channels in the node.
