# N9d — Operational Bound and Open Outputs from One Field Hamiltonian

Status: one two-level particle--field Hamiltonian now produces an order-`g^2` bound
observable and a finite-time emitted-boson event from one operator-valued departure
measure; probability, memory, and boundary-rate coincidences are evaluated through
order `g^2`; resonance and full scattering remain outside the horizon  
Consumes: [N9 observable dynamics](09-observable-dynamics.md),
[N9c field-derived measure](09c-field-derived-coupling-measure.md), and
[operational-channel contracts](../sources/operational-channel-contracts.md)  
Produces: a same-Hamiltonian bound/open recovery bridge, an operational meaning for
N9c's continuum boundary, a finite-time computation, and a stop before resonance
or `S`-matrix overclaim

Scalar upstream provenance is constructed downstream as a closure audit in
[N9e](09e-scalar-interaction-provenance.md); N9d remains the recovery target and
does not consume N9e, preserving the research DAG.
Finite-coupling error control is tested downstream in
[N9f](09f-certified-observable-window.md): the ground energy and a short-time
emission window are certified, while the displayed `t=80` rate probe is not.
[N9g](09g-kinetic-scale-reconstruction.md) constructs the resulting exponential
law for the exact one-excitation comparator, but shows why it does not yet prove
the exclusive event for the recoil fiber.

## Research contract and global binding

- **Upstream anchor:** N9c derives a scalar one-boson measure from a field
  Hamiltonian, but its open result `2 pi m(E)` is only a complementary resolvent
  boundary.
- **Bridge question:** can an actual preparation and detector event turn that
  boundary into a computed open-channel observable while the same Hamiltonian
  still produces a bound observable?
- **Invariant target:** the same Hamiltonian, preparation map `P`, departure map
  `B=QHP`, base one-boson measure, and field energy are retained across the
  Stieltjes, memory, and detector routes.
- **Downstream effect:** decide whether the measure spine has reached prediction or
  still only renames eliminated dynamics.
- **Special resources:** two internal levels, massive bosons, radial Gaussian
  cutoff, rotations, and the complete coefficient through order `g^2`.
- **Internal benchmark:** recover one ground-state observable and the complete
  finite-time one-boson event; prove survival loss, memory curvature, and
  continuum-boundary rate coincide; keep `Gamma t<0.25` in the numerical run.
- **Stop:** do not construct complex resonances, kinetic-limit exponentiation,
  massless infrared behavior, or wave operators unless a downstream claim needs
  one of those new output types.

## 1. Why the prepared space must contain two vectors

A single scalar preparation at one energy cannot simultaneously be an isolated
bound state and an embedded unstable state. Calling the same vector both would
change its spectral location without recording the change.

The smallest honest common preparation is therefore

```text
K=C|g> direct-sum C|e>,
Ran P=span{|g,Omega>,|e,Omega>}.                  (1.1)
```

The common object is not one scalar matrix element; it is one operator-valued
measure on this two-dimensional `P K`. Its two diagonal inputs ask different
operational questions of the same dynamics.

## 2. Construct the Hamiltonian and departure map

Use N9c's Fock space, massive dispersion, recoil, and radial form factor. Add the
internally constructed excitation cost `Delta>0`:

```text
H_0(p)
 =(p-P_f)^2/(2M)+H_f+Delta |e><e|,

V=(|g><e|+|e><g|) Phi(h),
H_g(p)=H_0(p)+gV.                                (2.1)
```

The off-diagonal internal operator is selected by the capability: radiation must
change the internal preparation. With

```text
P=I_K tensor |Omega><Omega|,
Q=1-P,
B=QH_g(0)P,                                     (2.2)
```

evaluate `B` on the two typed inputs. Free terms preserve the vacuum and are
removed by `Q`; annihilation kills it; creation produces one boson. Therefore

```text
B|g,Omega>=g |e,a^dagger(h)Omega>,
B|e,Omega>=g |g,a^dagger(h)Omega>.               (2.3)
```

This computation explains both surviving channels. It does not import them as a
level diagram.

## 3. Construct one operator-valued measure

Define the base recoil-plus-boson energy and measure

```text
epsilon(k)=sqrt(|k|^2+mu^2)+|k|^2/(2M),
dnu(x)=g^2 integral d^3k |h(k)|^2
                 delta(x-epsilon(k))dx.          (3.1)
```

N9c already constructs its radial density `m(x)`. At order `g^2`, free
complementary evolution leaves the two internal one-boson channels orthogonal.
Applying the spectral projection to (2.3) gives, on the prepared basis,

```text
M_B(A)
 =diag(
    integral 1_A(Delta+x)dnu(x),
    integral 1_A(x)dnu(x)
   )+O_return(g^4).                              (3.2)
```

The first entry belongs to ground preparation: departure must pay the internal
gap as well as the boson energy. The second belongs to excited preparation: the
internal gap is released into the field. The off-diagonal entry vanishes because
the free spectral projection preserves the orthogonal internal labels.

As in N9c, `O_return(g^4)` is a statement about the declared return transforms,
not setwise analyticity of every sharp continuum projection.

## 4. The ground input produces the bound observables

At zero momentum the ground self-energy is

```text
Sigma_g(0)
 =-integral dnu(x)/(Delta+x).                    (4.1)
```

The denominator is strictly positive because `Delta,mu>0`; this route never
touches a continuum boundary. The same complementary vector has squared norm
`integral dnu/(Delta+x)^2`, so normalization constructs

```text
Delta E_g^(2)=-integral dnu(x)/(Delta+x),
Z_g^(2)=1-integral dnu(x)/(Delta+x)^2.           (4.2)
```

Retain recoil and differentiate the same pole branch with respect to total
momentum. N9c's radial inverse `r(x)` then gives

```text
1/M_g,eff
 =1/M-(2/(3M^2))
       integral r(x)^2 dnu(x)/(Delta+x)^3
       +O(g^4).                                  (4.3)
```

No new spectral object was introduced: `(Delta+x)^(-1)`, `(Delta+x)^(-2)`, and
`r(x)^2(Delta+x)^(-3)` are three target functions applied to the ground entry of
(3.2).

## 5. The excited input constructs a detected event

Let `Pi_1` be the projection onto the one-boson Fock sector and construct the
detector and survival projections

```text
D_emit=|g><g| tensor Pi_1,
D_survive=|e,Omega><e,Omega|.                    (5.1)
```

For `chi_e=|e,Omega>`, the exact named probabilities are

```text
P_emit(t)=||D_emit exp(-itH_g)chi_e||^2,
P_survive(t)=||D_survive exp(-itH_g)chi_e||^2.   (5.2)
```

Move to the interaction picture of `H_0`. The first Dyson operation is

```text
eta_t=-ig integral_0^t Q V_I(s)chi_e ds.         (5.3)
```

Evaluate it using (2.3). A final one-boson state of energy `x=epsilon(k)` obtains
the amplitude

```text
eta_t(k)
 =-ig h(k) integral_0^t exp[-i(x-Delta)s]ds.     (5.4)
```

The detector asks only whether the system occupies the ground internal state with
one boson, without resolving its momentum. Its probability coefficient is the
norm of this constructed vector:

```text
P_emit^(2)(t)
 =||eta_t||^2
 =integral 4 sin^2[(Delta-x)t/2]/(Delta-x)^2
       dnu(x).                                   (5.5)
```

At `x=Delta`, the quotient is defined by its continuous value `t^2`. Equation
(5.5) is an operational open observable: preparation, evolution interval, and
detector projection are all named.

Unitarity gives the same-event recovery witness. Through second order, the only
first-order direction leaving `chi_e` is `eta_t`. Apply norm preservation to the
same evolved vector; field parity removes odd probability powers:

```text
P_survive(t)+P_emit(t)=1+O(g^4),
P_survive^(2)(t)=1-P_emit^(2)(t).                (5.6)
```

This is not an assumed exponential survival law. It is finite-time probability
conservation at the retained order.

## 6. Memory and boundary are the same event at different resolution

Construct the excited return memory from the same `nu`:

```text
K(t)=integral exp(-ixt)dnu(x).                   (6.1)
```

To expose rather than merely assert coincidence, square the time integral in
(5.4), set `u=s-s'`, and integrate over the square `[0,t]^2`. Pairs with the same
difference occupy length `t-|u|`. Conjugate halves combine to give

```text
P_emit^(2)(t)
 =2 Re integral_0^t (t-u)exp(iDelta u)K(u)du.    (6.2)
```

Differentiate this constructed Volterra integral twice:

```text
d^2 P_emit^(2)/dt^2
 =2 Re[exp(iDelta t)K(t)].                       (6.3)
```

Thus the memory kernel is directly observable as the curvature of accumulated
emission, not merely analogous to it.

For `Delta>mu`, divide (5.5) by `t`. The kernel

```text
(1/t) 4 sin^2(yt/2)/y^2
```

has integral `2 pi` and concentrates at `y=0`. Applying it to the continuous
density at `Delta` computes

```text
lim_(t->infinity) P_emit^(2)(t)/t
 =2 pi m(Delta)
 =-2 Im Sigma_e(Delta+i0).                       (6.4)
```

The limit is for the perturbative coefficient. At fixed nonzero `g`, its linear
growth eventually violates probability boundedness. Exponential decay requires a
kinetic-limit or resonance construction and is not inferred from (6.4).

The real part of the same boundary gives the principal-value shift

```text
Delta E_e^(2)=PV integral dnu(x)/(Delta-x).       (6.5)
```

Equations (6.4)--(6.5) are therefore the dissipative and dispersive parts of the
same excited-preparation transform.

## 7. Evaluated same-input regression

The isolated [operational-channel
computation](../computation/09d-operational-channel/README.md) uses

```text
M=2, mu=Lambda=1, Delta=1.5, g=0.01.
```

It obtains

```text
ground shift                 = -0.000168380320369,
ground residue               =  0.999947617514768,
ground mass expansion        =  2.000011126648661,

excited principal-value shift= -0.000207454527144,
m(Delta)                     =  0.000410346265971,
Gamma=2 pi m(Delta)          =  0.002578281629203.   (7.1)
```

At `t=80`,

```text
P_emit^(2)=0.202293228339,
P_survive^(2)=0.797706771661,
P_emit^(2)/t=0.002528665354.                     (7.2)
```

The last value differs from `Gamma` by `1.92%`, while `Gamma t=0.206<0.25`
records that the displayed run has not entered gross secular loss. This is a
diagnostic, not a bound on the omitted Dyson terms. Radial field-momentum
and energy-density routes agree within `6.0e-15` over all tested times. At `t=5`,
the five-point derivative of (5.5) and the independent memory expression (6.3)
agree within `3.92e-12`.

## 8. Complete-route cost and global verdict

```text
representation-derived field realization
  -> two-level internal preparation P
  -> departure B=QHP
  -> operator-valued field measure M_B
       |-> ground Stieltjes functions: bound shift/residue/mass
       `-> excited Fourier window: emitted-boson event
              -> memory curvature
              `-> on-shell boundary rate
  -> recover identical finite-time event
  -> audit perturbative and scattering boundaries.
```

| Route | Large operation | Recovery | Verdict |
| --- | --- | --- | --- |
| direct dressed Fock evolution | propagate all populated Fock sectors | project onto detector event | unnecessary through `g^2` |
| N9d field-measure route | one radial density plus target kernels | direct scalar integrals | genuine weak-coupling compression |
| exponential master equation | one rate | cheap survival curve | rejected without kinetic-limit error control |
| resonance construction | complex-deformed interacting resolvent | pole and decay law | new capability, outside this bench |
| scattering construction | asymptotic fields/wave operators | normalized incoming/outgoing amplitude | new observable, outside this bench |

N9c's boundary has now become a prediction: it is the long-time concentration
rate of a completely specified finite-time detector event. The same field
Hamiltonian also produces a bound ground shift and mass response. What remains
common is the operator-valued departure measure; what differs is the prepared
vector and target function applied to it.

This closes the nearest unsupported global edge. Further work on exact resonance
or scattering is not automatic continuation: it changes the output type and pays
for new analytic/asymptotic structure. Re-enter only when the manuscript needs a
finite-coupling lifetime, a normalized cross section, a massless limit, or a
physical atomic form factor.

## Verification ledger

| Obligation | Witness | Verdict |
| --- | --- | --- |
| use one Hamiltonian for bound and open outputs | two prepared inputs of (2.1)--(2.3) | exact |
| force one scalar state to be bound and unstable | incompatible spectral locations | rejected |
| construct the common measure | free spectral action on both departure vectors (3.2) | exact return coefficient through `g^2` |
| recover bound observables | target functions of the ground diagonal entry | complete coefficient through `g^2`; ground-energy remainder closed downstream by N9f, residue/mass still coefficient-only |
| construct an operational open event | detector projections and Dyson norm (5.1)--(5.5) | complete fixed-time coefficient through `g^2`; no uniform-time remainder bound |
| conserve probability | unitary norm on the same evolved input (5.6) | through `g^2`, remainder even |
| identify event with memory | square-to-triangle calculation (6.2)--(6.3) | exact for the coefficient |
| identify boundary rate | normalized concentrating kernel (6.4) | asymptotic coefficient; numerically checked |
| certify exact finite-`g` event | N9f Duhamel remainder | short-time window supported; `t=80` rejected by this certificate |
| infer exponential decay at fixed `g` | secular growth of coefficient | rejected |
| infer an `S` matrix | incoming/outgoing asymptotic construction absent | rejected |

## Edges

- `N9 -> N9d`: pass the noninvariant-preparation memory equation and requirement
  that a retained output be operationally named.
- `N9c -> N9d`: pass the field-derived base measure, radial inverse, transform
  routes, and the unresolved meaning of its continuum boundary.
- `OC-01/OC-02/OC-03 -> N9d`: delimit field-model, finite-time emission,
  resonance, and scattering transfers.
- `N9d -> N7/manuscript synthesis`: pass one same-Hamiltonian bound/open
  coefficient calculation, its semantic-coincidence witnesses, and the exact point where a new
  output requires resonance or scattering theory.
- `N9d -> N9g`: pass the coupling-free boundary density, exclusive event, and
  finite-time tangent as the recovery targets of the kinetic construction.
