# Pauli--Fierz dual-return bench

Status: frozen bench completed; same-action semantic composition, physical contact
closure, graph recovery, and dual bound/open use are supported on the regulated
fixture, while leverage over the expert Schur baseline is rejected

Consumes: node 38's graph-independent interaction return, node 33's
operator-valued visible instrument, and node 32's same-Hamiltonian comparison.

Produces: one regulated action, one prepared interface, and one effective operator
whose blocks can generate both a bound correction and a finite-resolution open
response while retaining an optional graph expansion.

Source boundary: `../sources/interaction-return-transfer-contracts.md`, contracts
`IRT-01` and `IRT-02`.

## Why this is the next discriminator

Node 38 still permits a false success: choose one toy for a level shift, another
for scattering, and identify their formulas only after both are known. The bench
must instead force the two outputs to share the same action-generated object.

Minimal coupling is the smallest nontrivial test because its linear interaction
cannot be selected independently of its contact interaction. Sequential histories
alone are therefore not physically closed. At the same time, a bound charged
system coupled to radiation has both a dressed low-energy sector and open photon
channels. These two demands meet before relativistic loop or infrared difficulties
are introduced.

A two-level matter truncation is not admitted as the physical fixture. Such a
truncation can violate the sum rule that relates the sequential and contact terms;
it could make the proposed compiler pass only by deleting its obstruction. A
matter-basis hierarchy is allowed only with an explicit low-energy sum-rule defect.

## Generate the interaction from one kinetic square

Use units with `hbar=m=1`. Let

```text
H_m=p^2/2 + U(x),                 U(x)=x^2/2+x^4/20,
H_f=sum_(j=1)^J omega_j a_j^dagger a_j,
A=sum_(j=1)^J c_j(a_j+a_j^dagger),
H(g)=(p-gA)^2/2+U(x)+H_f.                         (39.1)
```

`A` acts on the field factor and commutes with `p` in this dipole-regulated
fixture. The compiler is given the kinetic square, not a list of vertices.
Multiplication constructs

```text
H(g)=H_0+gV_1+g^2V_2,
V_1=-pA,
V_2=A^2/2.                                        (39.2)
```

Without the dipole simplification the same operation returns
`V_1=-(pA+Ap)/2`; no later rule is changed. Equation (39.2) is the first
obstruction-generated contact: deleting `V_2` is no longer a legal graph choice.

The finite regulator consists of:

- the lowest `N` eigenvectors of the declared anharmonic `H_m`;
- `J` positive photon frequencies and real UV-decaying coefficients `c_j`;
- total photon occupation at most `M`; and
- a positive detector resolution `eta`, so no finite box is called a scattering
  continuum.

The numerical tuple `(N,J,M,omega,c,g,eta)` belongs to the later computation
fixture. The scientific contract is the nested regulator family, not one lucky
matrix size.

## One preparation means one interface, not one vector

Let `phi_0` be the nondegenerate matter ground state and `Omega` the field vacuum.
Construct

```text
b=phi_0 tensor Omega,
o(f)=phi_0 tensor a^dagger(f)Omega,
P_b=|b><b|,
P_o=projection onto {o(f):f in C^J},
P=P_b+P_o,                 Q=1-P.                (39.3)
```

The phrase "one preparation" is therefore sharpened to one prepared interface
`P`. Different vectors in this interface are bound and open questions posed to the
same compiled operator. Replacing `P` between the two calculations would reject
the bench.

For `Im(z)>0`, solve the `Q` component of `(z-H)psi=y`. Substitution into its `P`
component constructs the effective operator

```text
K_P(z)=PHP+PHQ(z-QHQ)^(-1)QHP,
P(z-H)^(-1)P=[zP-K_P(z)]^(-1).                   (39.4)
```

This is the operator-valued return demanded by node 33. It retains channel phases
and off-diagonal amplitudes that a scalar measure `B^dagger E_Q B` would erase.
It is also the common target: direct inversion of the full regulated Hamiltonian
and (39.4) must agree before either physical output is interpreted.

## The graph packet is a coefficient, not an input

Because `P` reduces `H_0`, expand (39.4) at fixed `z`:

```text
K_P(z)=PH_0P+gK_1+g^2K_2(z)+O(g^3),
K_1=PV_1P,
K_2(z)=PV_2P+PV_1Q(z-QH_0Q)^(-1)QV_1P.           (39.5)
```

Thus the contact and every two-step history are generated together. In an
`H_0` eigenbasis `{|n,s>}` of `Q`, a matrix element of the second term is computed,
not merely described, by

```text
<u|K_2(z)|v>
 =<u|V_2|v>
  +sum_((n,s) in Q)
    <u|V_1|n,s><n,s|V_1|v>/(z-E_n-E_s).           (39.6)
```

For `u=o(h)` and `v=o(f)`, `V_1` changes photon number by one. The index `s`
therefore separates into the zero- and two-photon intermediate sectors. Drawing
those two summands gives the two sequential time orderings; drawing the first term
gives the contact graph. Equation (39.6), rather than those three drawings, is the
retained calculation.

## Two consumers of the same return

The bound consumer is the `b,b` block. Its first nonzero shift is

```text
delta E_b^(2)
 =<b|V_2|b>
  +sum_((n,s) in Q)
    |<n,s|V_1|b>|^2/(E_0-E_n-E_s).                (39.7)
```

The sequential denominator is negative above the prepared ground state, while the
contact contribution has the sign generated by the square. Neither sign is
supplied by graph convention. At finite `g`, the bound pole is a zero of
`det[zP-K_P(z)]` below the first admitted photon threshold.

The open consumer chooses normalized one-photon wave packets `f,h` and an energy
`E`. At finite regulator it is deliberately the resolvent response

```text
R_(h,f)(E,eta)
 =<o(h)|[E+i eta-H(g)]^(-1)|o(f)>,                (39.8)
```

reconstructed from the `P_o,P_o` block of (39.4). Its order-`g^2` interaction
kernel is

```text
T_(h,f)^(2)(E,eta)=<o(h)|K_2(E+i eta)|o(f)>.      (39.9)
```

Sending volume to infinity and `eta` to zero requires wave operators and channel
normalization; it is a later Rayleigh-scattering transfer. The present bench tests
a finite-resolution open-channel effect and makes no finite-box `S`-matrix claim.

Equations (39.7) and (39.9) are not analogous formulas from two models. They are
two blocks of the identical `K_2(z)` generated in (39.5).

## Do not let truncation fake closure

For the exact matter Hamiltonian,

```text
[x,[H_m,x]]=1,
2 sum_(n>0)(E_n-E_0)|<phi_0|x|phi_n>|^2=1.       (39.10)
```

The second line follows by inserting the complete matter eigenbasis into the first.
It measures the oscillator strength that a few-level projection discards. For the
lowest `N` matter states, record

```text
epsilon_TRK(N)
 =abs(1-2 sum_(n=1)^(N-1)
              (E_n-E_0)|<phi_0|x|phi_n>|^2).     (39.11)
```

Every equality inside one regulated matrix is an algebraic regression only.
Promotion to physical evidence additionally requires convergence of (39.7)--(39.9)
while `epsilon_TRK(N)` decreases. A small observable error with a large sum-rule
defect is classified as accidental agreement, not support.

The photon cutoff gets its own boundary receipt: `M>=2` contains every
intermediate photon sector in (39.6) for a one-photon input at order `g^2`, but an
exact finite-`g` comparison must be repeated as `M` increases. UV, volume, and
`eta -> 0` errors remain distinct rather than being hidden in one tolerance.

## Frozen evidence and falsifiers

The later executable bench must produce these independent receipts:

1. **action receipt:** automatic expansion of the kinetic square gives exactly
   `V_1,V_2` in (39.2);
2. **common-target receipt:** full inversion and (39.4) agree at frozen off-axis
   points;
3. **graph-recovery receipt:** explicit contact plus zero-/two-photon histories
   agree with (39.6) at order `g^2`;
4. **bound receipt:** a full-Hamiltonian eigenvalue and the pole of (39.4) agree;
5. **open receipt:** full and reduced values of (39.8) agree for coherent `f,h`;
6. **closure receipt:** `epsilon_TRK(N)` and regulator convergence are reported;
7. **cost receipt:** action construction, basis construction, `Q` solves, graph
   recovery, observable evaluation, and error certification are all counted.

The candidate is rejected or split if the two consumers require different
effective objects, if the contact cannot be generated from the supplied action, if
the graph sum contains information absent from `K_P`, or if regulator convergence
and the sum-rule defect disagree. Equality alone supports semantic unification,
not computational leverage: a structure-aware Schur baseline may have the same
cost. Leverage requires reuse across many bound/open queries or a later
factorization of the `Q` solve that the fair baseline lacks.

## Horizon and next edge

This bench is nonrelativistic, dipole regulated, finite resolution, and initially
bounded at order `g^2`, with an exact finite-`g` matrix comparison. It does not yet
supersede loop renormalization, infrared-inclusive scattering, pair creation, or
relativistic spinor interactions. Its job is narrower and decisive: determine
whether action generation, physical contact closure, graph recovery, and two
observable regimes really inhabit one reusable return object.

This bench passes semantically but not computationally. Its next edge is therefore
not another QED process; it is a reusable factorization or quotient of the `Q`
return that improves on the expert elimination route.

## Execution and local disposition

Evidence `E39-pf-return-v1` uses the frozen tuple

```text
primitive oscillator dimension L=28,
retained matter levels N=6,
photon frequencies omega=(0.65,1.10),
field coefficients c=(0.30,0.16),
total photon cutoff M=2,
coupling g=0.08, resolution eta=0.20.                  (39.12)
```

The generated field basis has six states, so the full regulated space has dimension
36. The prepared interface has dimension three (`b` plus two coherent one-photon
ports), leaving a 33-dimensional `Q` sector.

Projecting the primitive kinetic square after expansion and independently forming
`H_0+gV_1+g^2V_2` gives residual `4.38e-14`. Both generated operations are nonzero:

```text
||V_1||=4.3118742553,
||V_2||=0.6331672765.                                  (39.13)
```

At `z=E_0+0.82+0.20i`, direct full inversion and the effective return (39.4)
agree with Frobenius residual `1.20e-15`. Expanding the same return through order
two gives

```text
||K_2-(contact+all generated histories)|| =2.40e-17,
||K_2^open-(contact+zero/two-photon histories)||=2.64e-17. (39.14)
```

The contact, zero-photon, and two-photon open contributions have norms `0.182780`,
`0.179236`, and `0.080394`, respectively. None may be discarded as numerically
absent.

The two consumers use the identical return identifier `pf:6:2:2:0.08`. The full
ground energy and reduced pole are

```text
E_full=0.532788957271657,
E_pole=0.532788957271657, residual=1.11e-16.             (39.15)
```

For incoming `(1,i)/sqrt(2)` and outgoing `(1,-1)/sqrt(2)` photon packets, the
finite-resolution open response is

```text
R_full=0.383076203830307-0.267299834279175i,
R_reduced=0.383076203830306-0.267299834279176i,
residual=9.49e-16.                                      (39.16)
```

The closure hierarchy is independently visible:

```text
epsilon_TRK(2)=9.39499e-4,
epsilon_TRK(4)=8.02721e-7,
epsilon_TRK(6)=7.38744e-10.                             (39.17)
```

Increasing `M` from two to three changes the full bound energy by `4.37e-12`;
increasing the primitive basis from 20 to 28 changes it by `9.28e-13`. These are
regulator-stability receipts, not continuum or infinite-basis proofs.

The direct dense inversion count is `36^3=46,656`; the reduced route counts
`33^3+3^3=35,964`. The structure-aware expert Schur route has the same count
`35,964`. Therefore:

- **correctness, error-bounded:** action generation, contact closure, graph
  recovery, common-target equality, bound pole, and coherent open response pass;
- **same-action bridge, reproduced:** one compiled `K_P` serves both consumers;
- **regulator stability, error-bounded:** the declared `N`, `M`, and primitive
  hierarchy is stable at the reported resolution;
- **complete-route leverage, comparative rejection:** the proposed return is the
  expert Schur complement and provides no extra asymptotic or measured advantage;
  and
- **unresolved:** continuum volume, `eta -> 0`, UV removal, asymptotic scattering,
  infrared completeness, and relativistic pair/spin channels.

The executable constructor is `fieldcalc.pauli_fierz`; its certificate is
`computation/tests/test_pauli_fierz_return.py`. This closes node 39 and activates
the planned synthesis of `C_response-v1`.
