# Projector-native non-rigid differential propagation

## Frozen contract `C_G15_v1`

G14 constructs an isolated coefficient-derived projector jet
`(P,P_1,P_2)`. G13 formerly accepted only frame derivatives supplied by G11.
G15 asks for the smaller common object needed by the second-order complement
observable:

```text
D=(P,T_1,T_2),       T_1=Q P_1 P,       T_2=Q P_2 P,       Q=I-P.   (1)
```

The constructor admits each arrow only when `P T_j=0` and `T_j P=T_j` exactly.
Thus it cannot silently turn retained connection terms into leakage.

## Why these two arrows suffice locally

Let `B` synthesize the selected carrier, so `P B=B`, and choose the canonical
Grassmann-horizontal lift at the evaluation point. Differentiating once gives

```text
Q B_1=P_1 B.                                                   (2)
```

For the horizontal lift, `B_1=P_1 B` is off block. Since a projector derivative
is off diagonal, `Q P_1 Q=0`. Differentiating `P B=B` again therefore gives

```text
Q B_2=Q(P_2 B+2P_1 B_1)=Q P_2 B.                              (3)
```

Consequently the complement part of a second-order product rule depends on a
section amplitude `u` only through

```text
Q partial^2(Bu)=T_2 B u+2 T_1 B partial u.                     (4)
```

At momentum `k` and slow scale `epsilon`, the invariant carrier arrow is

```text
T(k)=epsilon(2 k T_1+T_2).                                    (5)
```

This is local differential geometry, not a claimed global frame or integrated
group action.

## One propagation core

G13 now lowers its frame leakage columns through the exact analysis map `A`, with
`A B=I` and `B A=P`, to the same value:

```text
T_1=K A,                  T_2=L A.                              (6)
```

G14 supplies (1) directly. Both routes then construct, for every declared
momentum and positive gap,

```text
H_0=Delta(I-2P)/2,
H=H_0+T(k)+T(k)^dagger.                                        (7)
```

Exact Gaussian-rational arithmetic owns the arrow laws, Hermiticity, preparation
quadratic forms, and the short-time/gap bound. SciPy evaluates the finite matrix
exponential and reports unitarity and reality residuals under the existing G13
tolerance. The observable remains probability in `Q` for both routes.

## Evidence packet `E_G15_1`

- **Question:** does the invariant interface retain `P_2`, recover rigid G11/G13,
  and remain independent of a constant reduced-frame choice?
- **Regression:** for the rigid repeated-Pauli jet, every momentum coupling
  operator and both rational bounds equal the G11/G13 route exactly; observed
  probabilities agree to fourteen decimal places.
- **Transfer/use:** adding a non-rigid Hermitian second-coefficient jet produces
  at `k=0`

  ```text
  T(0) e_1=T(0) e_3=-(1/3)e_0.
  ```

  The coherent bright preparation has transition probability
  `0.08988742896805166` with bound `8/81`; the dark difference has exact coupling
  zero and numerical probability below `7e-36`. Because `k=0`, this result cannot
  come from the first arrow.
- **Covariance:** swapping the two reduced frame columns and preparation
  coordinates preserves the carrier arrow, rational bound, and observed
  probability.
- **Refusal:** a projector/model mismatch and a value violating either off-block
  law refuse before propagation.
- **Reproducibility:** exact admission, construction, and unit tests are owned by
  `off_block_differential.py`, `projector_native_propagation.py`,
  `finite_window_propagation.py`, and `test_projector_native_propagation.py` in
  the pinned computation environment.

## Cost, disposition, and boundary

The projector-native adapter performs zero frame-analysis coordinate solves; the
rigid G11 regression performs four. Both still construct one dense ambient arrow
per momentum and numerically exponentiate the same four-dimensional blocks. This
supports a construction-stage saving and human removal of a frame/transport
choice, not a general runtime-speed claim.

Disposition: **supported bounded** for one-coordinate, finite
Gaussian-rational Hermitian projector jets with an isolated cluster, finite
momentum set, positive supplied gaps, and supplied retained preparations.

Several coordinates require curvature and path-compatibility data. Global bundle
topology, continuous spectra, unbounded domains, nonnormal pencils, automated
coefficient differentiation, certified transcendental propagation, and nonlinear
feedback remain outside G15.
