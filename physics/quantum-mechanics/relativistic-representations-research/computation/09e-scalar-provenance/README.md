# N9e scalar interaction-provenance regression

This isolated check verifies the two numerical identities on which the bridge to
N9d depends:

```text
f_hat(k)=sqrt(2 omega(k)) h(k)
  -> h_f(k)=f_hat(k)/sqrt(2 omega(k))=h(k),

same h and epsilon
  -> same N9d measure mass and on-shell density.
```

Run from the repository root:

```powershell
python physics/quantum-mechanics/relativistic-representations-research/computation/09e-scalar-provenance/scalar_provenance_regression.py
```

The script also checks the two regularity norms used by the field-operator
estimate. It does not approximate the full interacting Fock spectrum or test a
resonance claim.
