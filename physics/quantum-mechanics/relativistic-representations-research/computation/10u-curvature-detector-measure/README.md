# N10u curvature-detector measure regression

This packet checks the first quantum observable generated downstream of N10t's
curvature channel. It derives the radial density power from two inputs:

```text
massless null-orbit measure in three spatial dimensions -> omega^1;
order-s curvature amplitude, squared                   -> omega^(2s).
```

The resulting compiled detector measure is

```text
dnu_s(omega)
 = (A_s/2) omega^(2s+1) exp[-(omega/Lambda)^2] d omega.
```

`A_s` is no longer calibrated. The detector supplies the invariant squared norms
of its contractions in the two chiral spin-`s` modules. Covariance, irreducibility,
and trace generate

```text
A_s=(4*pi/(2s+1)) (||e_+||^2+||e_-||^2).
```

The detector tensor and coupling remain physical inputs. Neither the angular
response nor the frequency power is accepted as an answer-bearing input.

Run from the repository root:

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/10u-curvature-detector-measure/curvature_detector_measure.py
```

The check constructs spins one and two from the same compiler and verifies:

- cubic and quintic densities, including their angular normalizations, are
  generated, respectively;
- the factored shell/curvature route equals the compiled density;
- numerical measure mass equals its analytic Gaussian moment;
- the same density gives a negative order-`g^2` ground shift and a positive
  excited-state open-channel rate;
- the finite-time emitted probability approaches the same boundary rate while
  `Gamma t<0.25`;
- under the regression convention of equal compiler-normalized couplings, the
  spin-two/spin-one density ratio at fixed detector norm is `(3/5)omega^2`;
- the memory at zero equals the mass of the same measure;
- anisotropic smearing and a blind detector return explicit scalar-reduction
  refusals.

The cross-spin ratio is not a physical comparison until coupling dimensions and
normalizations are matched. The program does not claim an exact finite-coupling pole, exponential decay,
physical atomic or gravitational coupling, or an `S` matrix. It evaluates the
complete coefficient through order `g^2` for the declared effective detector.
