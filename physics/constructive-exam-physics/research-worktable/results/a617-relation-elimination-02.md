# A617 target-conditioned elimination result 02

## Source and question

The four problems below are bound to the audited 36-page local A617 compilation,
SHA-256
`B84E9D24468628433D1A126771DC8DE5A9D3CA7C2DBD01A78597FDDF01C8D764`.
See the [source audit](../sources/a617-local-corpus.md).

The question is whether one operation—not a list of topic analogies—constructs
the requested observable in each case. The operation tested is elimination of all
unrequested quantities from the physical relation system.

## A25-05: continuously varying dielectric

Let `d=d_1+d_2`. Planar symmetry and absence of free volume charge give
`dD/dx=0`, so `D` is one scalar hidden amplitude. The relevant relations are

```text
E(x)=D/epsilon(x),
U=integral_0^d E(x) dx,
P(x)=[epsilon(x)-epsilon_0]E(x),
rho_b(x)=-dP/dx.
```

Eliminate the field `E` from the voltage relation:

```text
U=D C_epsilon,
C_epsilon=integral_0^d dx/epsilon(x).
```

For `epsilon(x)=epsilon_0(1+kx)`:

```text
C_epsilon=ln(1+kd)/(epsilon_0 k),
D=epsilon_0 k U/ln(1+kd),
E(x)=kU/[(1+kx)ln(1+kd)],
rho_b(x)=-epsilon_0 k^2 U/[(1+kx)^2 ln(1+kd)].
```

The projection removes an arbitrary field profile as an independent unknown. The
continuous integral is a supplied calculus/theorem operation outside the finite
polynomial kernel.

## A24-05: solenoid and conducting rod

Use `s=dI/dt` as the source quantity. Faraday's law and Joule heating supply

```text
E_phi(r)=-(mu_0 n r/2)s,
P=sigma integral E_phi(r)^2 dV.
```

Eliminating the field gives

```text
P = sigma integral_0^h dz integral_0^a 2pi r dr
      [(mu_0 n r/2)s]^2
  = [sigma pi h a^4(mu_0 n)^2/8]s^2.
```

For `I=I_0 sin(omega t)`, eliminate `s` and average `cos^2`:

```text
average(P)=sigma pi h a^4(mu_0 n I_0 omega)^2/16.
```

The executable quadratic fixture is the finite two-mode version of exactly this
field elimination and returns `P-13s^2=0` from two field relations.

## A23-05: rotating R-L coil

Let `A=a^2`. The target is the magnitude of the average resisting torque. The
connected relation chain is

```text
lambda=N B A cos(omega t),
emf=-d lambda/dt,
(R+i omega L) I_hat=emf_hat,
average(P_J)=R|I_hat|^2/2,
|average(tau_em)|=average(P_J)/omega.
```

Eliminate flux, emf, and current:

```text
|emf_hat|=N B A omega,
|I_hat|^2=(N B A omega)^2/[R^2+(omega L)^2],
|average(tau_em)|
  =N^2 B^2 a^4 omega R/[2(R^2+(omega L)^2)].
```

With positive torque defined along the imposed rotation, the electromagnetic
torque is the negative of this magnitude. This route is valid for steady periodic
response and average torque. Instantaneous torque retains phase-resolved current;
changing the target changes what may be eliminated.

## A25-02: satellite after tangential impulse

With dimensionless `rho,e,l` defined in the framework, the physical relations are

```text
2e-alpha^2+2=0,
l-alpha=0,
2e rho^2-l^2+2rho=0.
```

The exact nonlinear kernel eliminates `e,l` and returns

```text
(rho-1)[(alpha^2-2)rho+alpha^2]=0.
```

It then exposes, without selecting, both candidates

```text
rho=1,
rho=alpha^2/(2-alpha^2).
```

The initial-radius root and the apocentre root are selected by geometry and the
bound-orbit condition `1<alpha<sqrt(2)`. This is the first full nonlinear
source-bound pass; the former document only stated the known invariant answer.

## Coherence witness

| Case | Hidden quantities eliminated | Retained target relation |
| --- | --- | --- |
| dielectric | `E(x)`, then `D` as needed | `U-D C_epsilon=0`, then `rho_b(U,x)` |
| conducting rod | `E_phi(r)` | `P-C s^2=0` |
| rotating coil | flux, emf, current | `average(tau)-f(N,B,a,omega,R,L)=0` |
| satellite | `e,l` | turning polynomial in `alpha,rho` |
| linear closure probe | full coordinates and accelerations | reduced equations in observable coordinates |

The shared semantic object is the same set of admissible `(given,target)` pairs.
For these displayed cases, explicit reconstruction verifies that eliminating the
hidden quantities does not add a selected answer. The physical relations differ by
domain; the target-conditioned elimination question does not.

## Evidence and boundary

Seven new behavioural tests cover deterministic pullback, quadratic reduction,
linear closure as projection, nonlinear orbital elimination, underdetermination,
inconsistent laws, and budget refusal. The orbital roots are also lifted
symbolically through the original relations. Together with the twelve prior exact
tests, the relation subsystem contains nineteen tests. The later semantic-layer
compiler adds seven tests, bringing the current active suite to twenty-six.

No claim is made that the compiler discovers the correct physical relations from
prose, automatically proves invariants, selects inequality-dependent branches, or
beats an expert solution on time. Those are now explicit downstream questions
rather than gaps concealed by a general word such as “pullback.”
