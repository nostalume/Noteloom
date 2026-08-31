# N4k — Half-Integer Positive-Energy Particle/Antiparticle Construction

Status: faithful positive two-shell one-particle construction supported for every separate finite half-integer spin; full induced-space density remains open  
Consumes: [N2a helicity fibers](02a-spin-and-helicity.md), [N3 realization bridge](03-realization-bridge.md), [N4b spinor-screen cohomology](04b-half-integer-potential.md), [N4i hyperbolic response](04i-half-integer-green-construction.md), [N4j causal quotient](04j-half-integer-causal-quotient.md), and [positive-frequency contracts](../sources/positive-frequency-contracts.md)  
Produces: an invariant positive metric on the spinor-screen fiber, future particle and conjugate-past antiparticle amplitudes, and their positive-energy Hilbert completion

## Research contract

- **Question:** how does the complex half-integer causal quotient become a
  positive-energy particle/antiparticle space without choosing gamma matrices or
  confusing the indefinite action pairing with a Hilbert norm?
- **Presumptions:** one fixed finite rank `n>=0`, helicity magnitude
  `h=n+1/2`; four-dimensional oriented and time-oriented Minkowski spacetime;
  compact complex sources; N4j's complex causal quotient; the nonzero future and
  past null orbits with their invariant measures.
- **Output:** a real-linear shell map

  ```text
  W_n^pair:O_n^C -> L2(O_+;H_n^part direct-sum H_n^anti)
  ```

  with positive fiber metric and positive-energy Poincare action, followed by the
  Hilbert completion of its complex span.
- **Boundary:** [N4l](04l-half-integer-support-faithfulness.md) supplies the
  spacelike-compact gamma-traceless gauge lift and proves faithfulness. Density,
  Majorana reality, curved backgrounds, and interactions are not claimed. The
  causal-Euler/CAR normalization is closed downstream by N4z.

The semantic route is

```text
admissible compact source
  -> first-order on-shell solution amplitude
  -> spinor-screen cohomology
  -> positive future and conjugate-past fibers
  -> particle/antiparticle Hilbert completion.
```

## 1. The null direction constructs a positive spinor metric

Fix a nonzero null momentum `r`, future or past directed, and let

```text
W_r=ker(gamma(r):Delta->Delta).
```

N4b constructs `W_r=im gamma(r)` and its two helicity-half lines. Positivity is
not inherited from N4i's Lorentz-invariant Dirac pairing `beta`, which is
indefinite on the full spinor carrier.

Choose a null `a_r` with the same time orientation as `r` and
`r.a_r=1`. Put `epsilon_r=+1` on the future orbit and `-1` on the past orbit, and
define on `W_r`

```text
kappa_r(w,v)=epsilon_r beta(w,gamma(a_r)v).
```

This form does not depend on the witness `a_r`. If `a'_r` is another witness,
then `q=a'_r-a_r` satisfies `r.q=0`. For the same `w,v in W_r`, N4b's Clifford
homotopy gives `w=(1/2)gamma(r)gamma(a_r)w`, so

```text
kappa'_r(w,v)-kappa_r(w,v)
 =epsilon_r beta(w,gamma(q)v)
 =(epsilon_r/2)beta(gamma(a_r)w,gamma(r)gamma(q)v)
 =(epsilon_r/2)beta(gamma(a_r)w,
                    [2r.q-gamma(q)gamma(r)]v)
 =0.
```

Both routes evaluate the same spinor pair, and the Clifford relation is the
coincidence witness.

To compute its sign, set

```text
t_r=epsilon_r(r+a_r)/sqrt(2).
```

Then `t_r` is future unit timelike. Normalize `beta` once so that
`<u,v>_(t_r)=beta(u,gamma(t_r)v)` is the positive spinor metric selected by this
future observer. Since `gamma(r)w=0`, evaluation on the same `w` gives

```text
<w,w>_(t_r)
 =(epsilon_r/sqrt(2))beta(w,gamma(a_r)w)
 =(1/sqrt(2))kappa_r(w,w).
```

Thus `kappa_r` is positive definite. No frame or matrix representative survives
the construction.

For `A` in the proper orthochronous Lorentz group, use `Aa_r` as the witness at
`Ar`. Invariance of `beta` and covariance of Clifford multiplication compute

```text
kappa_(Ar)(Aw,Av)
 =epsilon_r beta(Aw,gamma(Aa_r)Av)
 =kappa_r(w,v).
```

Hence the positive metric transports naturally over each energy orbit.

## 2. The screen kernel inherits positivity

N2a constructs the Euclidean screen

```text
Q_r=r^perp/span(r),
g_Q([x],[y])=-eta(x,y).
```

Equip `Sym^n(Q_r tensor C)^* tensor W_r` with the tensor-product Hermitian
metric induced by `g_Q` and `kappa_r`. N4b constructs the physical fiber as the
gamma-traceless subspace

```text
H_n(r)
 ={u in Sym^n(Q_r tensor C)^* tensor W_r | Gamma_Q u=0}.
```

Restriction of a positive metric to a subspace remains positive. Therefore
`H_n(r)` carries a natural positive Hermitian metric `h_(n,r)`. N4b's intrinsic
Clifford reduction has already computed

```text
H_n(r)~=C_(+(n+1/2)) direct-sum C_(-(n+1/2)).
```

The norm is constructed before choosing either helicity line, so positive energy
does not silently become a chirality projection.

## 3. A fermionic source needs one first-order operation on shell

Let

```text
O_n^C
 ={J in Gamma_c(F_n) | R_n^dagger J=0}/E_n Gamma_c(F_n)
```

be N4j's complex causal source quotient. For a representative `J`, construct

```text
K_J=M_n^(-1)J,
X_J(p)=S_n(p) K_J_hat(p).
```

The extra `S_n(p)` is forced rather than guessed. Source admissibility and N4i's
constrained adjoint give `B_nK_J=0`. Evaluate the hyperbolic identity on this same
datum at a null momentum:

```text
S_n(p)X_J(p)
 =S_n(p)^2 K_J_hat(p)
 =[p^2 I-2R_n(p)B_n(p)]K_J_hat(p)
 =0.
```

Thus `X_J(p)` is an actual field-kernel element, and N4b's quotient map produces

```text
w_n[J](p)=res_p(X_J(p)) in H_n(p).
```

This is the fermionic realization bridge. It uses one first-order invariant
operation instead of an explicit propagator numerator.

The amplitude is square-integrable. At large real momentum, the Fourier transform
of a compact smooth source decreases faster than any power. Near the removed
origin, `X_J(p)=O(|p|)`, while `kappa_p` has homogeneity `|p|^(-1)`; hence the
fiber norm squared is `O(|p|)`, which is locally integrable against
`dmu_0=d3p/(2|p|)`.

## 4. The shell amplitude depends only on the Euler-source class

Replace `J` by `J'=J+E_na` with compact `a`. Since `E_n=M_nS_n`, both
trace-reversed data are evaluated in the same field bundle:

```text
K_(J')-K_J=S_na,

X_(J')(p)-X_J(p)
 =S_n(p)^2 a_hat(p)
 =[p^2I-2R_n(p)B_n(p)]a_hat(p).
```

On either null orbit this difference lies in `im R_n(p)`. N4b proves that screen
restriction has exactly this gauge image as kernel, so

```text
res_p(X_(J')(p))-res_p(X_J(p))=0.
```

Therefore the amplitude is defined on `O_n^C`, not on an arbitrary source
representative.

## 5. The two energy signs construct particle and antiparticle sectors

A complex source has independent future- and past-shell data. Discarding the past
shell would therefore create a false null space. Parameterize both by `p in O_+`
and define

```text
w_n^+[J](p)=w_n[J](p) in H_n(p),

w_n^-[J](p)=conjugate(w_n[J](-p))
             in conjugate(H_n(-p)).
```

The first is the particle amplitude. The conjugated past amplitude is the
antiparticle amplitude. Conjugation reverses each little-group character, but the
parity pair is stable as an unordered fiber:

```text
H_n^part(p)~=C_(+h) direct-sum C_(-h),
H_n^anti(p)~=C_(+h) direct-sum C_(-h),
h=n+1/2.
```

No charge conjugation or Majorana identification between the two copies is used.

The paired map is real-linear. Its behavior under multiplication of the source by
`i` computes the distinction between the two sectors:

```text
W_n^pair(iJ)=(i w_n^+[J],-i w_n^-[J]).
```

Consequently complexification separates the two components explicitly:

```text
(1/2)[W_n^pair(J)-iW_n^pair(iJ)]=(w_n^+[J],0),
(1/2)[W_n^pair(J)+iW_n^pair(iJ)]=(0,w_n^-[J]).
```

Particle/antiparticle doubling is therefore constructed from the two shell signs;
it is not inserted as an unexplained extra copy.

## 6. The positive norm and its faithfulness boundary

Let the past fiber use the conjugate of `h_(n,-p)`. Define

```text
z_n^pair([J],[K])
 =integral_(O_+) [
    h_(n,p)(w_n^+[J],w_n^+[K])
   +conjugate(h_(n,-p))(w_n^-[J],w_n^-[K])
  ] dmu_0(p).
```

Its diagonal is nonnegative. The provisional spectral null space is

```text
Z_n=ker W_n^pair,
```

The positive one-particle completion is equivalently

```text
H_(src,n)
 =closure_C(span_C W_n^pair(O_n^C))
 =closure_C(w_n^+(O_n^C))
   direct-sum closure_C(w_n^-(O_n^C)).
```

For `n=0` there is no gauge image. If both shell amplitudes vanish, the Fourier
amplitude of N4j's Dirac causal solution vanishes on both shell components, so the
solution is zero. N4j's injectivity then gives `[J]=0`; hence `Z_0=0`.

For `n>=1`, `W_n^pair[J]=0` constructs a gauge amplitude at each shell momentum.
[N4l](04l-half-integer-support-faithfulness.md) uses the complete finite-type
compatibility complex and `H_c^1(R^3)=0` to assemble them into one
spacelike-compact gamma-traceless gauge parameter. Hence

```text
Z_n=0 for every finite n>=0.
```

The positive form is therefore a norm directly on the realification of `O_n^C`;
no spectral quotient remains.

## 7. Covariance turns both shells into positive energy

Let `g=(a,A)` be a proper orthochronous Poincare transformation and
`q=A^(-1)p`. Naturality of `M_n`, `S_n`, and screen restriction gives

```text
w_n^+[g.J](p)
 =exp(i p.a) A_H w_n^+[J](q).
```

At past momentum `-p`, the untranslated phase is `exp(-i p.a)`. Conjugation in
the antiparticle definition changes it back:

```text
w_n^-[g.J](p)
 =exp(i p.a) conjugate(A_H) w_n^-[J](q).
```

Both components therefore have positive translation spectrum. The invariant orbit
measure and Section 1's fiber isometries compute

```text
||W_n^pair(g.J)||=||W_n^pair(J)||.
```

The completion is a positive-energy invariant subrepresentation of the direct sum
of N3's particle and antiparticle induced representations.

## 8. Supported frontier and checks

Supported for every separate finite `n>=0`:

- positive spinor-screen and gamma-traceless physical-fiber metrics;
- a quotient-independent shell map with no component propagator;
- internally separated particle and antiparticle amplitudes;
- positive-energy covariance and a positive Hilbert completion;
- faithfulness without a spectral quotient for every finite `n`, with the
  gauge-rank support proof owned by N4l.

The existing [bounded spinor-tensor computation](../computation/04b-half-integer-potential/README.md)
independently checks witness independence and positivity of the physical
spinor-screen metric for `n=0,1,2,3`. It is a regression check, not the all-rank
proof above.

Open:

- density of each compact-source image in the full induced Hilbert space;
- Majorana or other real forms, charge conjugation, countable-spin topology,
  curved backgrounds, and interactions.

## Edges

- `N4b/N4i/N4j -> N4k`: screen cohomology, first-order wave reduction, and the
  causal source quotient construct the positive shell amplitudes.
- `N4k -> N4l`: the zero-amplitude condition is the input to the
  support-preserving gauge-lift theorem.
- `N4k/N4l -> N4y`: pass the faithful free fermionic particle/antiparticle shell
  quotient; N4y constructs antisymmetric multiplicity and exact one-particle
  recovery.
- `N4k/N4l -> N4z`: pass the positive two-shell form and faithfulness; N4z proves
  its normalized equality with the local causal Euler form and CAR locality.
- `N4k/N4l -> N4s`: pass the faithful free fermionic shell quotient as a
  regression case for interacting spectral extraction; density remains a
  separate obligation.
