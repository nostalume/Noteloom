# Gap-aware leakage bound

## Frozen contract `C_G12_v1`

G11 constructs exact first/second off-block columns `K_j,L_j`, but their being
nonzero says nothing quantitative. G12 admits one prepared reduced-frame column,
one exact momentum `k`, a slow scale `epsilon`, positive gap `Delta`, and
propagation time `t`. It constructs rather than supplies the effective coupling:

```text
w_j(k)=epsilon (2 k K_j+L_j),
gamma^2=<w_j,w_j>.                                                   (1)
```

This is a finite momentum-sector calibration. It is not a norm claim for an
unbounded differential operator or a uniform estimate over all momenta.

## Two-channel construction

When `gamma` is available in the exact rational field, construct

```text
H=[[-Delta/2, gamma], [gamma, Delta/2]],
Omega^2=(Delta/2)^2+gamma^2.                                        (2)
```

The machine verifies Hermiticity and the exact identity

```text
H^2=Omega^2 I.                                                      (3)
```

Consequently, by separating the even and odd powers of `H`,

```text
exp(-itH)=cos(Omega t) I-i sin(Omega t) H/Omega.                    (4)
```

For preparation in the first channel and observation of the second, the exact
transition formula is

```text
p(t)=(gamma^2/Omega^2) sin^2(Omega t).                              (5)
```

The constructor retains the rational coefficient and phase exactly; only the
final sine observation is evaluated in floating point.

## Certified bounds

The inequalities `|sin x|<=|x|` and `Omega^2>=Delta^2/4` give two independent
probability bounds:

```text
p(t) <= gamma^2 t^2,
p(t) <= 4 gamma^2/Delta^2,
p(t) <= min(1, gamma^2 t^2, 4 gamma^2/Delta^2).                     (6)
```

Thus time, gap, preparation, observable, and recovery are all part of the result.
A zero or negative gap returns `ClosingGapObstruction`; unsupported square roots
return a field-extension refusal rather than a floating exactness claim.

## Evidence and transfer

For the moving repeated-Pauli jet, select the nonzero leakage column and set

```text
k=1/2, epsilon=20/101, Delta=198/101, t=2.
```

Equation (1) gives `gamma=20/101`; (2) gives `Omega=1`. The exact transition
coefficient is `400/10201`, the observed probability is
`0.032421206173191101`, and the selected upper bound is
`400/9801 = 0.040812162024283234`.

Swapping the two reduced frame vectors and transforming the prepared column with
that frame preserves the carrier off-block vector and the observable. With the
constant G11 jet, `gamma=p(t)=bound=0`. A zero gap refuses, and a positive input
whose frequency requires `sqrt(5)` refuses exact construction.

## Cost, disposition, and boundary

G11 remains the upstream construction cost
`O(q^3+d^2 q^2)` with `O(q^2+qd)` storage. Given its jet, (1) scans `q` carrier
coordinates and the two-channel recovery is constant size. This is a transparent
cost account, not a runtime-leverage claim.

Disposition: **supported bounded** for a single exact rational momentum sector and
the canonical two-channel transition observable. G12 demonstrates how differential
leakage plus analytic inputs becomes a controlled observable statement.

It does not establish approximation of the original full PDE, uniform control on
an energy window, multichannel interference, domain preservation, crossings, or
long-time superadiabatic behavior. Those require a full block propagator or an
explicit energy-localized theorem contract.
