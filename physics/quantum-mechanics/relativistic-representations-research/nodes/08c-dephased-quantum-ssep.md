# N8c — Dephased Quantum Chain and SSEP Recovery

Status: conserved quantum density, exact current relaxation, Green--Kubo diffusion,
and leading strong-monitoring SSEP quotient constructed; finite-chain algebra
verified; finite-system two-time charge continued in N8d  
Consumes: [N8 collective diffusion response](08-collective-diffusion-response.md),
[N8a exact SSEP collective regression](08a-ssep-exact-collective-regression.md),
[N8b equilibrium SSEP current large deviations](08b-ssep-current-large-deviation.md),
and [dephased quantum-chain contracts](../sources/quantum-diffusion-contracts.md)  
Produces: the first explicit quantum-to-collective reduction, its same-coefficient
witness, and the precise boundary between a Lindblad state and a monitored
classical trajectory

## Research contract

- **Question:** which SSEP transport objects survive when hopping is genuinely
  coherent before local dephasing removes phase information?
- **Presumptions:** a finite periodic spinless-fermion chain with `N>=3` and nearest-neighbor
  hopping `J`; Markovian local occupation dephasing `L_x=sqrt(gamma)n_x`; the
  stationary infinite-temperature Bernoulli state at density `0<rho<1`; and,
  only for the trajectory statement, the occupation-monitoring unraveling of
  QD-01.
- **Output:** an exact conserved current, susceptibility, current autocorrelation,
  and diffusion coefficient; a constructed pinching map from quantum density
  matrices to occupation probabilities; and an SSEP generator of rate
  `kappa=2J^2/gamma` in the strong-monitoring slow limit.
- **Boundary:** exact equality of diffusion coefficients does not imply equality
  of finite-`gamma` current distributions. The unconditional Lindblad semigroup,
  a monitored trajectory, and a two-time quantum charge measurement are different
  observable constructions.

## 1. Why this is the discriminating comparator

N8a begins with a classical configuration and N8b assigns probabilities to its
current histories. A quantum comparator must add an object that SSEP does not
possess and then show how, when, and at what cost that object becomes irrelevant.
The smallest such object is coherence between occupation configurations.

The comparison therefore keeps the same local exclusion and conserved occupation
but replaces classical exchanges by coherent hopping:

```text
SSEP configuration probability
  -> quantum density matrix with diagonal populations and off-diagonal coherences
  -> local occupation monitoring/dephasing
  -> population quotient in a controlled slow limit.
```

This tests a genuine semantic reconstruction. SSEP should emerge as an effective
object, not be inserted as the original dynamics.

## 2. Local exclusion constructs the quantum algebra and dynamics

At each site `x` use a two-state occupation space. The annihilation and creation
maps `a_x,a_x^dagger` are joined across sites by the CAR relations

```text
{a_x,a_y^dagger}=delta_(xy),
{a_x,a_y}=0,
n_x=a_x^dagger a_x,
n_x^2=n_x.
```

Thus the same `0/1` exclusion used by SSEP is retained, while superpositions of
different occupation configurations are now allowed.

On the periodic lattice `Lambda_N`, define

```text
H_J=-J sum_x(a_(x+1)^dagger a_x+a_x^dagger a_(x+1)),

L_gamma(rho_q)
  =-i[H_J,rho_q]
   +gamma sum_x{
       n_x rho_q n_x-(1/2){n_x,rho_q}
     }.
```

The subscript on `rho_q` distinguishes the quantum state from the scalar density
used in N8a. The dissipator is internally tied to the chosen observable:

```text
gamma[n_x rho_q n_x-(1/2){n_x,rho_q}]
  =-(gamma/2)[n_x,[n_x,rho_q]].
```

It leaves every occupation probability fixed instantaneously and damps only
matrix elements that distinguish eigenvalues of `n_x`. This is precisely the
unconditional back-action of monitoring local occupation; it is not particle
loss, injection, or thermalization.

The total occupation

```text
N_tot=sum_x n_x
```

commutes with `H_J` and every `n_x`. Hence the adjoint generator satisfies

```text
L_gamma^dagger(N_tot)=0.
```

Quantum evolution has changed the carrier of state information but has preserved
the same conserved quantity required by N8.

## 3. The equilibrium input retains N8a's susceptibility

For a dimensionless chemical potential `mu`, construct

```text
rho_eq(mu)=Z^(-1)exp(mu N_tot).
```

Because the summands `n_x` commute and are projectors, this state factorizes in
the occupation basis. Its one-site density is

```text
rho=exp(mu)/[1+exp(mu)].
```

It commutes with `H_J`, and every dephasing term annihilates it, so it is
stationary. Differentiating the same state gives

```text
chi=d rho/d mu=rho(1-rho)
   =(1/N)Var_(rho_eq)(N_tot).
```

The quantum model and SSEP therefore receive the same density and susceptibility;
their dynamical comparison is not contaminated by different equilibrium inputs.

## 4. Continuity constructs the quantum current

Only the two hopping terms adjacent to `x` fail to commute with `n_x`. Evaluate
the adjoint generator on that same local density. The dephasing double commutator
vanishes because all occupations commute, while the Hamiltonian terms give

```text
L_gamma^dagger(n_x)=j_(x-1)-j_x,

j_x=iJ(a_(x+1)^dagger a_x-a_x^dagger a_(x+1)).
```

The current is therefore the oriented bond term produced by the local
continuity equation. It is not inferred from SSEP or from a continuum ansatz.

Let

```text
J_tot=sum_x j_x.
```

There is a short invariant reason that its coherent evolution vanishes. If `S`
is one-site translation on the one-particle lattice and

```text
dGamma(A)=sum_(x,y) a_x^dagger A_(xy)a_y,
```

then

```text
H_J=dGamma[-J(S+S^dagger)],
J_tot=dGamma[iJ(S-S^dagger)].
```

Both one-particle maps are polynomials in the commuting pair `S,S^dagger`.
Using `[dGamma(A),dGamma(B)]=dGamma([A,B])` on the same Fock space gives

```text
[H_J,J_tot]=0.
```

No momentum-mode expansion or Liouvillian diagonalization is required.

## 5. Dephasing makes the total current an exact eigen-observable

For the oriented hopping map

```text
A_x=a_(x+1)^dagger a_x,
```

only occupations `n_x,n_(x+1)` fail to commute with it. Directly applying both
double commutators gives

```text
sum_y [n_y,[n_y,A_x]]=2A_x.
```

The same holds for `A_x^dagger`. Therefore

```text
L_gamma^dagger(J_tot)=-gamma J_tot,

J_tot(t)=exp(-gamma t)J_tot.
```

This is the first quantum computational compression: a `4^N`-dimensional density-
matrix evolution contracts to one exact current eigen-operator.

The equilibrium equal-time covariance is also local. On one bond,

```text
j_x^2
  =J^2{
      n_x(1-n_(x+1))+n_(x+1)(1-n_x)
    }.
```

For `N>=3`, different bonds have zero current covariance in the diagonal Bernoulli state.
Evaluating the same occupation events gives

```text
(1/N)<J_tot^2>_eq=2J^2 rho(1-rho)=2J^2 chi.
```

Quantum regression on the same stationary state now yields

```text
C_JJ(t)
  =(1/N)<J_tot(t)J_tot(0)>_eq
  =2J^2 chi exp(-gamma t).
```

## 6. The exact response coefficient needs one scalar integral

Define the dimensionless-chemical-potential Green--Kubo diffusion coefficient by

```text
D_GK=(1/chi) integral_0^infinity C_JJ(t)dt.
```

Substitute the constructed current correlation rather than a phenomenological
relaxation time:

```text
D_GK
  =(1/chi)(2J^2 chi) integral_0^infinity exp(-gamma t)dt
  =2J^2/gamma.
```

QD-02 supplies the independent spectral theorem boundary that the low-lying
density sector is diffusive. Thus N8's leading response becomes

```text
R_quantum(omega,k)
  =chi D_GK k^2/[D_GK k^2-iomega]+higher-gradient terms.
```

This statement is hydrodynamic, not an exact finite-lattice response formula.
The limit `gamma->0` is singular: `D_GK` diverges while the undephased clean chain
is ballistic. One must take the long-wavelength/long-time diffusive limit at
fixed `gamma>0`; setting `gamma=0` first changes the transport type.

## 7. Occupation pinching constructs the classical state quotient

Let `|eta>` be the joint occupation eigenvector for a configuration
`eta:Lambda_N->{0,1}` and `Pi_eta=|eta><eta|`. The monitoring-selected pinching is

```text
P(X)=sum_eta Pi_eta X Pi_eta,
Q=identity-P.
```

`P rho_q` retains exactly the classical probabilities

```text
p(eta)=<eta|rho_q|eta>
```

and discards phase relations between different configurations. This quotient is
not chosen because diagonal matrices are simpler; it is constructed by the
observable that the environment measures.

The dephasing action makes the separation quantitative. On a matrix unit,

```text
D_gamma(|eta><xi|)
  =-(gamma/2)d_H(eta,xi)|eta><xi|,
```

where `d_H` counts the sites on which the two occupation records differ. Hence

```text
ker D_gamma=im P.
```

A single allowed hop exchanges `10` and `01`, so the associated coherence has
`d_H=2` and decays with eigenvalue `-gamma`. Populations are slow; the exact
coherences created by one hop have a known inverse `-1/gamma`.

## 8. Eliminating one-hop coherence constructs SSEP

Write the coherent superoperator as

```text
V(X)=-i[H_J,X].
```

QD-01 supplies the strong-monitoring slow-generator contract

```text
L_slow=-P V (D_gamma|_Q)^(-1) V P.
```

Evaluate this composite on one occupation projector `Pi_eta`. If occupations on
bond `x` agree, the hopping term annihilates that bond state. If they are `10` or
`01`, write `eta^x` for their exchange. The first `V` creates only the coherence
between `eta` and `eta^x`; dephasing inversion multiplies it by `-1/gamma`; the
second `V`, followed by `P`, returns the population difference. On that same
two-state bond subspace,

```text
P V^2(Pi_eta)
  =2J^2[Pi_(eta^x)-Pi_eta].
```

The fermionic parity phase in the hopping amplitude cancels against its conjugate,
so the output depends only on whether the move is allowed. Summing the bonds gives

```text
L_slow(Pi_eta)
  =kappa sum_x[Pi_(eta^x)-Pi_eta],

kappa=2J^2/gamma,
```

with terms of equal neighboring occupation contributing zero. On probabilities,

```text
partial_t p(eta)
  =kappa sum_x[p(eta^x)-p(eta)].
```

This is precisely SSEP with bond rate `kappa`. The equality is at the level of the
same pointer-state probability, not an analogy between a quantum current and a
classical random walk.

The coefficient closes a nontrivial same-observable triangle:

```text
exact quantum Green--Kubo coefficient
  =2J^2/gamma
  =strong-monitoring SSEP bond rate
  =SSEP diffusion coefficient.
```

At finite `gamma`, the Green--Kubo formula remains exact for this clean model, but
`kappa` no longer generates the full population evolution autonomously. That
evolution has memory through coherences and is not the SSEP Markov semigroup.

## 9. What happens to N8b current statistics

The word “current trajectory” now splits into three constructions:

1. **Unconditional state:** `rho_q(t)` determines ensemble observables and quantum
   regression functions, but not a unique classical history `eta(t)`.
2. **Occupation-monitoring trajectory:** the measurement record selects random
   pointer states; QD-01 states that their slow strong-monitoring dynamics
   converges weakly to SSEP.
3. **Two-time charge measurement:** measuring half-line charge before and after
   evolution defines a separate quantum full-counting observable, even if the
   environment record is discarded.

Different monitoring unravelings can generate the same unconditional Lindblad
equation while assigning different path statistics. Therefore the finite-`gamma`
Lindblad generator alone does not authorize importing N8b's current rate function.

For the occupation-monitoring trajectory, however, the Zeno limit constructs a
specific current: count pointer exchanges `10->01` minus `01->10` across the
origin. In the natural slow time

```text
tau=kappa t,
```

this is N8b's unit-rate SSEP current. After the pointer-process limit and then the
infinite-line large-time limit,

```text
log E[exp(lambda Q_t)]
  ~sqrt(kappa t)
    F(2chi[cosh(lambda)-1]),

P(Q_t/sqrt(kappa t) approximately q)
  ~exp[-sqrt(kappa t)Phi_rho(q)].
```

This recovery is ordered:

```text
strong-monitoring slow-process limit
  -> infinite-line/thermodynamic limit
  -> large slow-time current limit.
```

No uniform estimate justifying exchange of these three limits has been constructed
here. [N8d](08d-two-time-quantum-charge.md) constructs a finite-system two-time
charge observable and verifies its Zeno SSEP recovery through the full bounded
distribution. The infinite-line, finite-dephasing current law remains open. The
recent noisy-hopping Q-SSEP result recorded in the source packet is a candidate
comparison, not a substitute for that missing calculation.

## 10. Computability and global-view audit

The useful route is short because every reduction is observable-selected:

```text
local occupation
  -> continuity current
  -> one exact current eigen-operator
  -> one scalar Green--Kubo integral;

occupation monitoring
  -> pinching onto pointer probabilities
  -> invert only one-hop coherence decay
  -> SSEP generator.
```

No gamma matrix, spatial component expansion, many-body eigenbasis, Bethe roots,
or full `4^N` Liouvillian diagonalization enters the coefficient calculation. The
finite matrix computation is retained only as an independent normalization and
sign check.

The reduction also clarifies the earlier field/mechanics/collective view. A quantum
field or many-body Hamiltonian does not become classical mechanics by a second
quantization label. Here a named environmental observation creates a quotient of
the quantum state, and time-scale separation supplies autonomous dynamics on that
quotient. Classical exclusion is therefore an emergent collective process with a
recovery map, not a lower rung in a quantization hierarchy.

The success is restricted. Exact current relaxation relies on the clean nearest-
neighbor current commuting with the hopping Hamiltonian. Disorder, interactions,
additional conserved charges, or nonlocal dephasing can destroy that one-operator
closure. The pinching construction still exists, but its slow generator and cost
must be recomputed from the new Hamiltonian and monitored observable.

## 11. Verification ledger and frontier

The finite-chain witness is documented in
[computation/08c-dephased-quantum-ssep](../computation/08c-dephased-quantum-ssep/README.md).

| Obligation | Same-input witness | Verdict |
| --- | --- | --- |
| quantum exclusion | CAR plus `n_x^2=n_x` | exact |
| conserved density | apply the same adjoint Lindbladian to `n_x,N_tot` | exact |
| current construction | local continuity equation | exact |
| current relaxation | shift-algebra commutator plus dephasing double commutator | exact |
| susceptibility/current covariance | same Bernoulli quantum equilibrium | exact |
| diffusion coefficient | scalar integral of the exact current correlation | exact under Green--Kubo/hydrodynamic contract |
| SSEP quotient | evaluate `-P V D_Q^(-1)V P` on every occupation projector | exact leading Zeno generator |
| coefficient coincidence | `D_GK=kappa=2J^2/gamma` | exact in declared convention |
| finite-chain signs and normalization | complete four-site Fock-space evaluation | reproducibly checked |
| N8b current law | monitored pointer current after ordered Zeno and large-time limits | supported under QD-01 plus N8b contracts |
| finite-system two-time charge | N8d's same-input TPM/SSEP comparison | constructed and numerically verified |
| finite-`gamma` infinite-line current LDP | no unique trajectory from unconditional state; no controlled TPM hydrodynamic limit | open |
| uniform limit interchange/error | no thermodynamic Zeno remainder bound constructed | open |

N8d has taken the first discriminator: it computes the finite two-time transferred-
charge law and compares its second/fourth cumulants with the same finite SSEP
event. The remaining useful branches are sharper:

- construct a controlled infinite-line/hydrodynamic limit of that TPM observable
  at fixed finite `gamma`; or
- add one interaction or second conserved density and test which exact closures
  fail before seeking a new collective variable.

## Edges

- `N8/N8a -> N8c`: pass the conserved-density response, susceptibility,
  coefficient, and same-observable recovery obligations.
- `N8b -> N8c`: pass the named integrated-current hierarchy and require an
  operational quantum trajectory before transferring its rate function.
- `N8c -> N8d`: pass the unconditional/monitored/two-time distinction, exact `D`,
  and the Zeno SSEP baseline; recover the complete bounded TPM law.
- `N8c/N8d -> infinite-line quantum TPM`: pass the operational characteristic
  map and require a controlled volume/hydrodynamic limit.
- `N8c -> coupled quantum hydrodynamics`: pass the occupation pinching and require
  a new slow-manifold computation when further conserved observables are present.
- `N8c -> N9`: pass the noninvariant pinching, fast coherence decay, Zeno generator,
  and same-observable recovery as the explicit asymptotic-Markov case.
- `N8c -> N9b`: pass the nonself-adjoint Liouvillian as a counterprobe to extending
  positive self-adjoint coupling measures across every collective reduction.
- `N8c -> N7/manuscript synthesis`: pass the first constructed quantum-to-classical
  collective recovery and its ordered-limit boundary.
