# N9f — Certified Finite-Coupling Window for the N9d Observables

Status: N9e's exact scalar Hamiltonian now supports an explicit ground-energy
remainder and an exact finite-time detector remainder; at `g=0.01` the analytic
ground certificate is below `0.671%`, while the open probability has uniform
absolute error at most `0.001` through `t=6.474` and at most `0.01` through
`t=11.450`; the prior `t=80` boundary-rate comparison remains a coefficient
diagnostic and is not certified at finite coupling  
Consumes: [N9d operational observables](09d-operational-bound-open-channel.md),
[N9e scalar provenance](09e-scalar-interaction-provenance.md), and
[certified-window contracts](../sources/certified-observable-window-contracts.md)  
Produces: an interacting ground eigenvalue with an explicit order-`g^2`
remainder, an exact detector-amplitude remainder, a finite predictive window,
and a constructive long-time obstruction for the short norm route

## Research contract and spine binding

- **Upstream anchor:** N9e constructs the exact self-adjoint fiber `H_g(0)` and
  N9d constructs one bound coefficient and one emitted-boson coefficient from
  its leading departure measure.
- **Bridge question:** do those coefficients approximate the same exact
  observables with explicit nonvacuous errors, without solving the dressed Fock
  spectrum or evolution?
- **Invariant target:** the exact ground energy issued from `|g,Omega>` and the
  exact detector event `D_emit exp(-itH_g)|e,Omega>`; neither target is changed
  while estimating it.
- **Downstream effect:** promote the measure from an explanatory coefficient to
  a controlled prediction where possible, and mark the time scale where this
  certificate stops carrying information.
- **Special resources:** positive boson mass, Gaussian form factor, small
  coupling, conserved combined parity, and finite observation time.
- **Internal benchmark:** produce a nonvacuous bound for both observables at the
  existing parameters, then test the displayed long-time point `t=80` with the
  same certificate.
- **Stop:** no resonance, kinetic limit, wave operator, higher spin, cutoff
  removal, or higher perturbative coefficient. Each would change the output or
  the model after this benchmark has decided the present bridge.

The tested composite is

```text
exact H_g and exact preparation/detector
  |-> symmetry-reduced Feshbach map -> exact bound energy E_g
  |      compare with the same N9d Stieltjes coefficient
  `-> finite-sector Duhamel identity -> exact P_emit(t,g)
         compare with the same N9d detector coefficient
  -> explicit remainder or explicit loss of certification.
```

## 1. Why the leading coefficient is not yet a prediction

N9d computes

```text
E_g(g)=g^2 e_2+O(g^4),
P_emit(t,g)=g^2 p_2(t)+O_t(g^4).                 (1.1)
```

The notation in (1.1) records order but does not give a number bounding either
remainder. The diagnostic `Gamma t<0.25` controls neither one: it compares a
golden-rule scale with time, whereas a remainder must compare the exact and
truncated constructions on the same state and observable.

The present node therefore does not calculate `e_4` or `p_4`. It bounds all
unexpanded terms together. This is computationally shorter and answers the
actual predictive question.

## 2. Construct the symmetry quotient before the estimate

Let

```text
Z=|e><e|-|g><g|,
R_F=(-1)^N,
Xi=Z R_F.                                       (2.1)
```

The free Hamiltonian commutes separately with `Z` and `R_F`. The interaction
`V=S Phi(h)` anticommutes with each factor:

```text
Z S Z=-S,
R_F Phi(h) R_F=-Phi(h).                          (2.2)
```

Apply both conjugations to the same product:

```text
Xi V Xi
 =(Z S Z)(R_F Phi(h)R_F)
 =(-S)(-Phi(h))
 =V.                                            (2.3)
```

Thus `[Xi,H_g]=0`. This is a reducing quotient, not an approximate selection
rule.

The ground preparation has `Xi=-1`. Inside that sector the free states are

```text
|g> tensor even boson number,
|e> tensor odd boson number.                     (2.4)
```

After removing `chi_g=|g,Omega>`, the first possibilities are two ground-label
bosons or one excited-label boson. Since recoil is nonnegative,

```text
d_- =min(2 mu,Delta+mu).                         (2.5)
```

The opposite sector begins with one ground-label boson or the excited vacuum:

```text
d_+ =min(mu,Delta).                              (2.6)
```

For the benchmark, `d_-=2` and `d_+=1`. Estimating the ground complement before
this quotient would incorrectly pay for states that cannot couple to the ground
branch and would reduce the usable gap by half.

## 3. One field inequality controls both spectral sectors

Construct the two norms already checked by N9e:

```text
beta=||h||,
alpha=||h/sqrt(omega)||.                         (3.1)
```

The annihilation estimate and the CCR give, on the finite-energy form domain,

```text
||a(h)psi||<=alpha ||H_f^(1/2)psi||,

||a^dagger(h)psi||^2
 =||a(h)psi||^2+beta^2||psi||^2.                (3.2)
```

Take the square root of the second line, add the first, and use
`sqrt(x+y)<=sqrt(x)+sqrt(y)`:

```text
||Phi(h)psi||
 <=2 alpha ||H_f^(1/2)psi||+beta||psi||.         (3.3)
```

On any free sector with `H_0>=d` and `H_f<=H_0`, Cauchy--Schwarz computes

```text
|<psi,V psi>|
 <=C(d)<psi,H_0 psi>,

C(d)=2 alpha/sqrt(d)+beta/d.                    (3.4)
```

Consequently

```text
H_0+gV >=(1-|g|C(d))H_0.                        (3.5)
```

For a theorem bound that does not depend on numerical quadrature, use
`omega>=mu`:

```text
alpha<=beta/sqrt(mu),
beta^2=pi^(3/2)Lambda^3.                         (3.6)
```

At the N9d parameters, these analytic majorants give

```text
Cbar_-=4.517028...,
Cbar_+=7.079191...,
1-g Cbar_-=0.954830...,
1-g Cbar_+=0.929208....                          (3.7)
```

Both complementary sectors therefore stay positive. This turns the Feshbach
inverse below into a constructed bounded object and also prevents a lower state
from appearing in the opposite parity sector.

## 4. The ground branch and its remainder

Work inside `Xi=-1`. Put

```text
P_0=|chi_g><chi_g|,
Q_-=1-P_0,
A=Q_- H_0 Q_-,
W=Q_- V Q_-,
b=Q_- V chi_g=|e,a^dagger(h)Omega>.              (4.1)
```

Here `A>=d_-`. Equations (3.4)--(3.5) construct the form operator

```text
K=A^(-1/2) W A^(-1/2),
||K||<=C_-=C(d_-),
H_Q(g)=A^(1/2)(1+gK)A^(1/2).                    (4.2)
```

For `E<0`, the complementary block is positive and invertible. Apply the two
block equations to a vector `c chi_g+q`. The `Q_-` equation computes

```text
q=-g c (H_Q(g)-E)^(-1)b.                        (4.3)
```

Substitute this same `q` into the `P_0` equation:

```text
E=-g^2 <b,(H_Q(g)-E)^(-1)b>.                    (4.4)
```

The right side is continuous and negative. The function obtained by moving it
to the left is strictly increasing from a negative value at `E=-infinity` to a
positive value at `E=0`. It has one root. Equation (4.3) reconstructs its
eigenvector. Because both complementary parity sectors are positive, this root
is the global fiber ground energy.

Now construct the error without expanding the Fock sectors. Define

```text
u=A^(-1/2)b,
s=||u||^2=<b,A^(-1)b>,
c_-=1-|g|C_->0.                                 (4.5)
```

The vector `u` has internal label `e` and one boson. The operator `K` flips it
to the ground label and zero or two bosons; `Q_-` removes the zero-boson ground
vector. Hence

```text
<u,Ku>=0.                                       (4.6)
```

Use the exact inverse identity

```text
(1+gK)^(-1)
 =1-gK+g^2 K(1+gK)^(-1)K.                       (4.7)
```

Equations (4.6)--(4.7) give

```text
|<b,H_Q(g)^(-1)b>-s|
 <=g^2 s C_-^2/c_-.                             (4.8)
```

Since `E<=0`, resolvent monotonicity in (4.4) also computes

```text
|E|<=g^2 s/c_-,

|<b,(H_Q(g)-E)^(-1)b>-<b,H_Q(g)^(-1)b>|
 <=g^2 s^2/(c_-^3 d_-).                         (4.9)
```

Combining the two differences in their common scalar target produces

```text
|E+g^2 s|
 <=g^4 [s C_-^2/c_-+s^2/(c_-^3 d_-)].           (4.10)
```

This is the desired finite-coupling certificate. The same `s` is exactly N9d's
ground Stieltjes coefficient:

```text
s=integral |h(k)|^2/[Delta+epsilon(k)]d^3k.      (4.11)
```

For a completely analytic majorant, use

```text
s<=beta^2/(Delta+mu),                            (4.12)
```

and obtain a lower bound by retaining the ball `|k|<=Lambda` and replacing the
denominator by its maximum on that ball. The Gaussian ball mass is

```text
pi^(3/2)Lambda^3 erf(1)-2 pi Lambda^3 exp(-1).   (4.13)
```

The evaluated result is

```text
N9d leading shift              =-0.000168380320369,
analytic absolute remainder    <=0.000000504447980,
analytic relative certificate  <=0.670388%.      (4.14)
```

Using the evaluated `alpha` and `s` rather than their analytic majorants gives
the sharper regression `2.87199350e-7`, or `0.170566%` of the displayed leading
shift. That sharper number is a numerical evaluation; (4.14) is the theorem
certificate.

## 5. An exact finite-time remainder without a Dyson tail

Let

```text
U_g(t)=exp[-it(H_0+gV)],
U_0(t)=exp(-itH_0),
chi_e=|e,Omega>,
D_emit=|g><g| tensor Pi_1.                       (5.1)
```

Use the Duhamel identity with the exact propagator kept at the left. Iterating
it twice produces

```text
U_g(t)chi_e
 =U_0(t)chi_e+g U_1(t)chi_e+g^2 U_2(t)chi_e
  +R_3(t),                                      (5.2)
```

where, apart from powers of `-i`,

```text
R_3(t)
 =g^3 integral_(s1+s2+s3<=t)
   U_g(t-s1-s2-s3)V U_0(s3)V U_0(s2)V U_0(s1)chi_e
   ds1 ds2 ds3.                                 (5.3)
```

This is an exact remainder, not the beginning of an infinite tail. The final
`U_g` is unitary; all three unbounded field operators act first on free-evolved
finite-particle vectors.

Boson number and the internal flip compute the path

```text
e tensor F_0
  --V--> g tensor F_1
  --V--> e tensor (F_0 direct-sum F_2)
  --V--> g tensor (F_1 direct-sum F_3).          (5.4)
```

Therefore `D_emit U_0 chi_e=0` and `D_emit U_2 chi_e=0`. The projected first
term is exactly the N9d amplitude `eta_1(t)`:

```text
D_emit U_g(t)chi_e=g eta_1(t)+r_3(t),
||eta_1(t)||^2=p_2(t),
r_3=D_emit R_3.                                  (5.5)
```

The field norms on the three successive finite-sector inputs are bounded by

```text
beta,
sqrt(3) beta,
(sqrt(2)+sqrt(3))beta.                           (5.6)
```

The first is exact on the vacuum. For the second, annihilation and creation land
in orthogonal zero- and two-boson sectors. For the third, use their operator
norms on `F_0 direct-sum F_2`. Since the time simplex has volume `t^3/6`, (5.3)
gives

```text
||r_3(t)||
 <=R_A(t)
 :=|g|^3 t^3 beta^3
   sqrt(3)(sqrt(2)+sqrt(3))/6.                   (5.7)
```

Evaluate the exact and leading probabilities on the same projected vector:

```text
|P_emit(t,g)-g^2 p_2(t)|
 <=2 |g|sqrt(p_2(t)) R_A(t)+R_A(t)^2.            (5.8)
```

For a bound uniform over the entire interval `0<=t<=T`, use the first-operation
estimate `||g eta_1(t)||<=|g|beta t`:

```text
sup_(0<=t<=T)|P_emit(t,g)-g^2p_2(t)|
 <=2|g|beta T R_A(T)+R_A(T)^2.                   (5.9)
```

No continuum phase or radial quadrature is needed to construct (5.9). The
oscillatory N9d coefficient enters only when a sharper pointwise comparison is
requested.

## 6. Evaluated predictive window and failure boundary

The isolated [certified-window
computation](../computation/09f-certified-window/README.md) evaluates the same
parameters as N9d. Its theorem-level uniform bounds are

```text
absolute probability error <=0.001 for every 0<=t<=6.474171885,
absolute probability error <=0.01  for every 0<=t<=11.449543378. (6.1)
```

Sharper pointwise evaluations give

| `t` | N9d `g^2 p_2(t)` | pointwise error bound | evaluated relative bound | verdict |
| ---: | ---: | ---: | ---: | --- |
| `1` | `0.000531437364` | `5.50377e-7` | `0.104%` | strong |
| `5` | `0.008528343828` | `0.000277752376` | `3.257%` | nonvacuous |
| `10` | `0.021942441341` | `0.003678033470` | `16.762%` | nonvacuous but coarse |
| `20` | `0.047574861475` | `0.050763758775` | `106.703%` | coefficient comparison vacuous |
| `80` | `0.202293228339` | `42.832085621097` | `21173%` | completely vacuous |

The pointwise relative bound crosses `10%` at `t=8.0956` and `100%` at
`t=19.5545` inside the tested bracket `[5,20]`. These are numerical crossings,
not a theorem that the ratio is globally monotone.

This produces a mixed verdict:

```text
bound energy:
  N9d measure compression is a certified finite-g prediction;

short-time emission:
  N9d measure compression is a certified finite-g prediction;

long-time emission and boundary rate:
  the coefficient remains correct, but the present norm certificate loses
  predictive control before the golden-rule comparison time.
```

The failure at `t=80` is not evidence that the exact probability differs by the
huge displayed majorant. Norm estimates discard the continuum phases whose
cancellation creates the golden-rule scale. It is evidence that long-time
prediction requires a different semantic construction—kinetic scaling,
resonance, or another phase-sensitive resummation—not another refinement of the
same finite-time norm bound.

## 7. Global computability verdict

N9f identifies exactly what the leading departure measure compresses:

```text
exact H_g
  -> one parity quotient
  -> one scalar Stieltjes coefficient plus analytic field norms
  -> certified ground energy,

exact U_g(t)
  -> three finite Fock-sector norm actions
  -> N9d one-boson coefficient plus a time-polynomial remainder
  -> certified short-time detector probability.
```

No dressed eigenvector or full Fock propagation is computed. The ground route is
therefore a genuine whole-route reduction. The open route is a genuine reduction
only inside the finite window; outside it, the time-polynomial recovery cost
overwhelms the retained coefficient.

The branch reaches its internal stop. A longer-time claim may re-enter through a
named kinetic-limit or resonance node, but only because N9f has now shown the
precise observable and time scale that require it.

That kinetic re-entry is now developed in
[N9g](09g-kinetic-scale-reconstruction.md). It recovers the exponential event in
an exact one-excitation comparator and identifies the still-unproved
multiparticle suppression needed to return to N9e's exclusive detector.

## Verification ledger

| Obligation | Witness | Verdict |
| --- | --- | --- |
| discard irrelevant ground channels | exact conservation of `Xi` and sector list (2.4) | exact |
| retain complementary gap | analytic form constants and positive margins (3.7) | exact theorem bound |
| construct exact ground state | scalar Feshbach root and reconstruction (4.3)--(4.4) | exact at `p=0` |
| recover N9d bound coefficient | equality (4.11) | exact |
| bound ground remainder | inverse identity and energy-resolvent difference (4.7)--(4.10) | analytic certificate below `0.671%` |
| recover N9d detector coefficient | detector kills orders zero and two in (5.4)--(5.5) | exact |
| bound all higher detector terms | exact three-vertex Duhamel remainder (5.3), not a truncated tail | analytic finite-time certificate |
| certify displayed `t=80` probability | bound exceeds probability range | rejected by this route |
| infer exponential lifetime | no kinetic/resonance construction | rejected |

## Edges

- `N9d/N9e -> N9f`: pass the exact scalar Hamiltonian, the two preparations,
  detector, and the two leading coefficients as same-observable targets.
- `N9f -> synthesis audit`: promote the bound and short-time open coefficients to
  controlled predictions; retain the long-time boundary as coefficient-only.
- `N9f -> N9g`: pass the exact event and the loss of norm certification near
  `t~20`; N9g changes to kinetic time and audits same-model recovery.
