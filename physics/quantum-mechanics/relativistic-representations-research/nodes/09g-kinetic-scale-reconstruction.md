# N9g — Kinetic-Scale Reconstruction and Detector Obstruction

Status: the N9d measure constructs a unique kinetic decay generator and an exact
one-excitation Friedrichs comparator whose survival and one-boson probabilities
converge to the same exponential law; transfer of that law to N9e's exact recoil
fiber and exclusive detector remains open because neither excitation number nor
the standard additive-reservoir structure survives  
Consumes: [N9d operational channel](09d-operational-bound-open-channel.md),
[N9e scalar provenance](09e-scalar-interaction-provenance.md),
[N9f certified window](09f-certified-observable-window.md), and
[kinetic-scale contracts](../sources/kinetic-scale-reconstruction-contracts.md)  
Produces: the internally constructed kinetic generator, a same-measure
Friedrichs recovery, an exact inclusive/exclusive event decomposition, and the
smallest theorem obligation still needed for the full model

## Research contract and spine binding

- **Upstream anchor:** N9f preserves N9d's exact event but its phase-blind
  remainder is vacuous before the `t=80` rate probe.
- **Bridge question:** does `tau=g^2 t` turn N9d's continuum boundary into a
  controlled decay law for the same preparation and detector?
- **Invariant target:** `chi_e=|e,Omega>`, the N9e zero-momentum Hamiltonian,
  N9d's density `m_g=g^2 m_0`, and the projections onto survival and emitted
  field states.
- **Downstream effect:** decide whether N9d's golden-rule coefficient is already
  a long-time prediction or only the generator of a candidate effective law.
- **Special resources:** `Delta>mu`, a smooth Gaussian form factor, zero field
  temperature, weak coupling, and bounded kinetic time `0<=tau<=T`.
- **Internal benchmark:** construct the generator from the same departure
  measure; recover N9d's tangent and exact detector partition in the
  one-excitation comparator; then test whether the theorem and observable
  transfer to the exact recoil fiber without changing their meaning.
- **Research horizon:** no explicit convergence rate, finite-`g` resonance,
  scattering matrix, massless limit, cutoff removal, or driven/thermal field.

The bounded route is

```text
N9f exact event plus failed fixed-time certificate
  -> expose tau=g^2 t
  -> construct the on-shell generator from N9d's same measure
  -> one-excitation comparator: exact kinetic recovery
  -> exact N9e fiber: audit sector and theorem coincidence
  -> supported law or named transfer obstruction.
```

## 1. Why a new time object is necessary

N9f's exact amplitude remainder has the form

```text
R_A(t)<=C |g|^3 t^3.                            (1.1)
```

Substitute the time actually needed for cumulative decay:

```text
t=tau/g^2

R_A(tau/g^2)<=C tau^3/|g|^3.                   (1.2)
```

The same bound that vanishes at fixed `t` diverges at fixed nonzero `tau`.
Equation (1.2) computes the incompatibility; it does not say that the dynamics
diverges. The estimate discarded the phases before taking the scale on which
their accumulation matters.

Remove the coupling from N9d's measure:

```text
dnu_g(x)=g^2 dnu_0(x),
m_g(x)=g^2 m_0(x).                              (1.3)
```

Its fixed-order event obeys

```text
g^2 p_2(t)/t -> 2 pi g^2 m_0(Delta).            (1.4)
```

At `t=tau/g^2`, (1.4) becomes an order-one tangent

```text
g^2 p_2(tau/g^2) -> gamma_0 tau,
gamma_0=2 pi m_0(Delta).                        (1.5)
```

The right side exceeds one when `tau>1/gamma_0`. Therefore it cannot itself be
a probability law. It is the derivative that a bounded kinetic law must recover.

## 2. Construct the kinetic kernel from the departure vector

N9e already constructs

```text
b=|g,a^dagger(h)Omega>,
epsilon(k)=omega(k)+|k|^2/(2M).                 (2.1)
```

The excited preparation has free energy `Delta`; the one-boson departure vector
has free energy `epsilon(k)`. Apply both free evolutions to the same matrix
element:

```text
K_0(u)
 =<b,exp[-iu(H_Q^(0)-Delta)]b>
 =integral exp[-iu(epsilon(k)-Delta)]|h(k)|^2 d^3k
 =integral exp[-iu(x-Delta)]dnu_0(x).           (2.2)
```

Thus the kernel is not imported from a bath ansatz: it is the return amplitude
of N9e's constructed departure vector.

For the massive Gaussian benchmark, radial pushforward gives a smooth density
on `(mu,infinity)`, and `Delta>mu` lies in its interior. The only stationary
endpoint of the radial phase is `r=0`. Writing `y=r^2` gives an amplitude
proportional to `y^(1/2)` there; endpoint stationary phase therefore yields
`K_0(u)=O(u^(-3/2))`. Hence `K_0` is integrable at infinity. This is the
model-local regularity needed by the weak-coupling contract; it does not prove a
full-model theorem by itself.

Construct the half-line transform by first inserting `s>0`:

```text
A_s
 =integral_0^infinity exp(-su)K_0(u)du
 =integral dnu_0(x)/[s+i(x-Delta)].             (2.3)
```

The real numerator `s/[s^2+(x-Delta)^2]` converges to a delta mass, while the
imaginary numerator converges to a principal value. Both act on the same
`m_0`, so

```text
A=lim_(s downarrow 0) A_s
 =pi m_0(Delta)+i delta_0,

delta_0=PV integral dnu_0(x)/(Delta-x),
gamma_0=2 Re A=2 pi m_0(Delta).                 (2.4)
```

The dissipative rate and Lamb phase are thus the two boundary components of the
same constructed transform.

## 3. The exact model in which the measure is sufficient

Let `sigma_-=|g><e|`, `sigma_+=|e><g|` and retain the interaction operations
that preserve

```text
N_exc=Pi_e+N:

V_rw=sigma_- a^dagger(h)+sigma_+ a(h).          (3.1)
```

Starting from `chi_e`, the `N_exc=1` space is

```text
H_1=C|e,Omega> direct-sum
    {|g,a^dagger(f)Omega>:f in L^2(R^3)}.       (3.2)
```

Evaluate (3.1) on both summands. It maps the first to the second by `h` and the
second back by the scalar product with `h`; no other Fock sector occurs. The
restricted Hamiltonian is therefore the Friedrichs operator

```text
H_g^F = [[Delta, g<h|],
         [g|h>, epsilon]].                       (3.3)
```

This is a constructed comparator, not a quotient of the full N9e dynamics.
It keeps the same preparation, one-boson energy, form factor, measure, and
detector, while explicitly changing the interaction by deleting
excitation-changing operations.

Write its interaction-picture state as

```text
exp(-itH_g^F)chi_e
 =exp(-iDelta t)c_g(t)|e,Omega>
  +integral exp[-i epsilon(k)t]b_g(k,t)|g,k> d^3k.
                                                               (3.4)
```

The two block equations from (3.3) give

```text
dot b_g(k,t)=-ig h(k)exp[i(epsilon(k)-Delta)t]c_g(t),

dot c_g(t)
 =-g^2 integral_0^t K_0(t-s)c_g(s)ds.           (3.5)
```

Both equations are computed on the same state; eliminating `b_g` produces the
Volterra memory rather than assuming it.

Set `C_g(tau)=c_g(tau/g^2)`. The Friedrichs weak-coupling theorem contract,
whose regularity is supplied by the smooth interior density above, gives
uniformly on compact `tau` intervals

```text
C_g(tau) -> exp[-A tau].                         (3.6)
```

Using (2.4), the phase-corrected amplitude and survival probability are

```text
exp(i delta_0 tau)
 exp(i Delta tau/g^2)
 <chi_e,exp(-iH_g^F tau/g^2)chi_e>
   -> exp(-gamma_0 tau/2),

P_surv^F(tau/g^2,g)->exp(-gamma_0 tau).          (3.7)
```

On `H_1`, unitarity and the orthogonal decomposition (3.2) compute the detector
identity at every `g,t`:

```text
P_emit,1^F(t,g)=1-P_surv^F(t,g).                (3.8)
```

Consequently

```text
P_emit,1^F(tau/g^2,g)->1-exp(-gamma_0 tau).      (3.9)
```

Finally, differentiate the right side at `tau=0`:

```text
d/dtau [1-exp(-gamma_0 tau)]|_(tau=0)=gamma_0.  (3.10)
```

Equation (3.10) is the semantic-coincidence witness with N9d (1.5): its boundary
coefficient is exactly the tangent of the reconstructed bounded probability.

## 4. Why this does not yet prove the exact N9e event

The full interaction is

```text
V=V_rw+V_cr,
V_cr=sigma_- a(h)+sigma_+ a^dagger(h).          (4.1)
```

Although `V_cr chi_e=0`, it acts after the first emission. For example,

```text
|e,Omega> --V_rw--> |g,F_1>
          --V_cr--> |e,F_2>.                    (4.2)
```

N9f's conserved combined parity gives the exact decomposition of the evolved
state:

```text
Xi=+1:
  |e> tensor F_even  direct-sum  |g> tensor F_odd.             (4.3)
```

Define the inclusive internal probabilities and N9d's exclusive projections:

```text
P_e^inc=||[Pi_e tensor 1]U_g(t)chi_e||^2,
P_g^inc=||[Pi_g tensor 1]U_g(t)chi_e||^2,

P_surv=||[Pi_e tensor Pi_0]U_g(t)chi_e||^2,
P_emit,1=||[Pi_g tensor Pi_1]U_g(t)chi_e||^2.    (4.4)
```

Resolve (4.3) by boson number. Orthogonality computes

```text
P_e^inc
 =P_surv+sum_(n>=2, even) P_(e,n),

P_g^inc
 =P_emit,1+sum_(n>=3, odd) P_(g,n),

P_e^inc+P_g^inc=1.                              (4.5)
```

Therefore

```text
P_surv+P_emit,1
 =1-P_multi,

P_multi=sum_(n>=2, even)P_(e,n)
        +sum_(n>=3, odd)P_(g,n).                (4.6)
```

At fixed time, N9d/N9f place `P_multi` beyond the retained order. At
`t=tau/g^2`, that statement is not uniform. The desired same-event recovery
requires the new estimate

```text
sup_(0<=tau<=T) P_multi(tau/g^2,g) -> 0.         (4.7)
```

Neither parity nor the scalar measure proves (4.7).

There is also a theorem-transfer obstruction. Standard Pauli--Fierz weak-coupling
results use an additive reservoir generator `dGamma(epsilon)`. N9e's exact fiber
contains

```text
P_f^2/(2M)|_(F_n)
 =sum_i |k_i|^2/(2M)+sum_(i<j) k_i.k_j/M.        (4.8)
```

The cross term in (4.8) shows by direct evaluation that the free fiber is not
`dGamma(epsilon)` beyond one boson. Conversely, undoing the fiber restores a
mobile particle with an infinite-dimensional translation space, not the finite
small system in the cited theorem. The standard extended theorem therefore
cannot simply be named as proof of (4.7).

## 5. Evaluated kinetic scale

The isolated [kinetic-scale
computation](../computation/09g-kinetic-scale/README.md) evaluates (2.4) with
N9d's parameters. It obtains

```text
m_0(Delta) = 4.10346265971,
gamma_0    = 25.78281629203,
delta_0    = -2.07454527144,
1/gamma_0  = 0.03878552245.                     (5.1)
```

At `g=0.01`, one kinetic lifetime corresponds to

```text
t=1/(g^2 gamma_0)=387.855224.                   (5.2)
```

This is far beyond N9f's uniform `0.01` error window `t<=11.450`. At N9d's
`t=80`, `gamma_0 tau=Gamma t=0.2062625`; the kinetic comparator predicts

```text
1-exp(-Gamma t)=0.186381...,                     (5.3)
```

whereas the linear boundary tangent is `Gamma t=0.2062625`. Their difference is
the secular curvature that fixed-order probability cannot retain. This number
is a comparator prediction, not a certified value of N9e's exact detector.

## 6. Global computability verdict and stop

The branch separates three claims that were previously easy to conflate:

| Claim | Construction | Verdict |
| --- | --- | --- |
| N9d boundary determines a kinetic generator | half-line transform of the same `nu_0` | supported |
| the generator yields bounded decay and the exclusive detector law | exact `N_exc=1` Friedrichs comparator | supported for the comparator |
| the same exclusive law holds for N9e's recoil fiber | requires (4.7) plus a model-compatible extended limit | open |

The useful compression is real: one density supplies both rate and phase, and a
one-dimensional Volterra equation replaces continuum amplitudes in the
comparator. But deleting `V_cr` is a dynamical approximation, not semantic
quotienting; its whole-route cost includes proving that the deleted sectors are
invisible to the requested event on kinetic times.

This node stops here. Its internal benchmark has discriminated the route: more
numerical refinement of the exponential cannot alter the global claim. Re-enter
only to prove or refute (4.7) for the recoil fiber, or if the requested observable
is deliberately changed to an inclusive internal population. A finite-`g`
lifetime would instead require resonance theory.

## Verification ledger

| Obligation | Witness | Verdict |
| --- | --- | --- |
| explain failure of N9f on kinetic time | substitution (1.2) | exact |
| construct rate and phase from the same measure | common transform (2.2)--(2.4) | exact |
| construct rather than assume the solvable comparator | excitation action and block operator (3.1)--(3.3) | exact |
| recover the memory equation | same-state block elimination (3.4)--(3.5) | exact |
| obtain exponential kinetic law | Friedrichs theorem contract with smooth interior density | supported for comparator |
| recover N9d boundary coefficient | derivative equality (3.10) | exact |
| equate survival and one-boson emission | invariant one-excitation space (3.8) | exact only for comparator |
| transfer the exclusive event to N9e | multi-sector remainder (4.7) | open |
| import standard Pauli--Fierz extended limit | recoil cross term (4.8) | rejected without a new theorem match |

## Edges

- `N9d/N9f -> N9g`: pass the same departure density, exact exclusive event,
  boundary tangent, and failure of fixed-time certification.
- `N9e -> N9g`: pass the exact recoil fiber, interaction, preparation, and
  combined-parity sectors used to test same-model transfer.
- `N9g -> synthesis audit`: pass the kinetic generator and comparator recovery,
  but retain the exact detector law as an explicit open bridge.
- `N9g -> possible recoil kinetic-limit node`: pass equation (4.7) and the
  additive-reservoir obstruction as the complete next obligation; re-enter only
  if long-time exclusive detection remains the selected output.
