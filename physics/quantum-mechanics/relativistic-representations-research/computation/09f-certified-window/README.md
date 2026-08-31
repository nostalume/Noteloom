# N9f certified finite-coupling window

This computation evaluates explicit remainder bounds for the same two observables
used by N9d:

```text
bound input |g,Omega>   -> exact ground energy versus its order-g^2 coefficient,
open input  |e,Omega>   -> exact one-boson detector probability versus its
                           order-g^2 coefficient.
```

Run from the repository root:

```powershell
python -B physics/quantum-mechanics/relativistic-representations-research/computation/09f-certified-window/certified_window.py
```

The ground certificate uses the conserved combined parity, a form-resolvent
Feshbach estimate, and the exact N9d radial coefficient. The open certificate
uses an exact twice-iterated Duhamel formula: the detector kills the zeroth and
second terms, and the unexpanded remainder contains exactly three field
interactions acting on finite Fock sectors before a final unitary evolution.

The theorem-level ground certificate and uniform open window use analytic Gaussian
majorants. Tighter ground and pointwise relative figures use numerical quadrature
and are labeled regressions. Failure of the finite-time bound at long time does
not show that perturbation theory is inaccurate there; it shows that this short
norm certificate cannot establish its accuracy.
