# N9e — Scalar Interaction Provenance from the Free Shell to N9d

Status: the missing scalar interface is closed at the regulated model level: the
massive Klein--Gordon shell constructs the bosonic field, a declared spatial
smearing constructs N9d's form factor, translation covariance constructs the
fixed-total-momentum fiber, and the same vacuum departure map recovers N9d's
leading operator-valued measure; the interaction profile itself is not derived
from Poincare symmetry  
Consumes: [N4 local realization](04-local-symbol-extension.md),
[N4y free quantization](04y-quantization-recovery-bridge.md),
[N9d operational channel](09d-operational-bound-open-channel.md), and
[scalar-provenance contracts](../sources/scalar-interaction-provenance-contracts.md)  
Produces: a same-object composite from the scalar positive shell to N9d's
Hamiltonian, an exact total-momentum reduction, a source--shell normalization
witness, and a precise limitation ledger

## Research contract

- **Defect:** N4/N4y construct free field content, while N9d begins with a
  separately written particle--field fiber. No node previously showed that its
  `Phi(h)` is the quantization of the scalar field in the free spine or that its
  recoil term is the exact fiber of a translation-covariant full Hamiltonian.
- **Question:** can the smallest massive scalar example close this interface by
  equality, without claiming that symmetry determines an interaction?
- **Presumptions:** three spatial dimensions; scalar mass `mu>0`; a mobile
  nonrelativistic body of mass `M`; a two-dimensional internal space with gap
  `Delta`; one declared real spatial profile; and the bosonic Fock
  representation selected by positive energy.
- **Output:** construct the shell amplitude, smeared field, full Hamiltonian,
  conserved total momentum, fiber Hamiltonian, preparation, departure map, and
  leading free-complement measure, then compare every object with N9d.
- **Stop:** scalar provenance only. Do not infer a relativistic matter model, a
  symmetry-selected coupling, a compactly supported interaction, a higher-spin
  interaction machine, finite-coupling resonance data, or scattering theory.

The closure benchmark is one commuting composite:

```text
massive scalar orbit and Klein--Gordon equation
  -> positive-shell Hilbert space H_1
  -> Fock field Phi_0
  -> declared translated smear h_X
  -> translation-covariant full Hamiltonian H_full
  -> exact total-momentum fiber H_g(p)
  -> vacuum preparation J and departure B
  -> free-complement measure M_(B,2)
  == N9d equations (2.1)--(3.2).
```

The last equality, not similarity of vocabulary, is what repairs the interface.

## 1. Construct the massive scalar shell

N4's spin-zero massive symbol is

```text
D_mu(q)=q^2-mu^2.                                (1.1)
```

Its positive-energy kernel is supported on

```text
q=(omega(k),k),
omega(k)=sqrt(|k|^2+mu^2).                       (1.2)
```

The invariant orbit measure is `d^3k/(2 omega(k))`. Multiplication by
`(2 omega)^(-1/2)` identifies that realization unitarily with

```text
H_1=L^2(R^3,d^3k).                               (1.3)
```

This normalization is a choice of coordinates on the already constructed
positive shell, not a new particle assumption. On `H_1`, time translations and
spatial translations act by multiplication with `exp(-it omega(k))` and
`exp(i k.a)` respectively.

Apply N4y's symmetric Fock functor:

```text
F=Gamma_s(H_1),
Omega=(1,0,0,...),
H_f=dGamma(omega),
P_f=dGamma(k).                                   (1.4)
```

For `u in H_1`, construct

```text
Phi_0(u)=a^dagger(u)+a(u),
Phi_0(u)Omega=a^dagger(u)Omega=iota_1(u).         (1.5)
```

Thus the field excitation and the positive-shell vector are literally the same
one-particle object under N4y's canonical injection.

## 2. A spatial profile constructs the form factor

At time zero, smear the Klein--Gordon field distribution with a real Schwartz
profile `f`. The shell factor is fixed by the canonical pairing, not inserted as
a mnemonic. For another real profile `r`, put

```text
h_f(k)=f_hat(k)/sqrt(2 omega(k)),
j_r(k)=sqrt(omega(k)/2) r_hat(k),

phi(0,f)=a^dagger(h_f)+a(h_f),
pi(0,r)=i(a^dagger(j_r)-a(j_r)).                  (2.1)
```

The Fock CCR computes

```text
[phi(0,f),pi(0,r)]
 =i 2 Re <h_f,j_r>
 =i integral f(x)r(x)d^3x.                       (2.2)
```

The factors `omega^(-1/2)` and `omega^(1/2)` are therefore reciprocal maps from
the same Cauchy pairing to the positive shell; their product cancels before
Plancherel is applied. In particular `phi(0,f)=Phi_0(h_f)`.

Equations (2.1)--(2.2) are the semantic bridge missing from N9d: a profile in physical
space and a vector in shell space are related by the positive-shell
normalization. They must not be given the same informal name.

N9d uses the shell amplitude

```text
h(k)=exp(-|k|^2/(2 Lambda^2)).                    (2.3)
```

It is obtained exactly from the declared profile

```text
f_hat(k)=sqrt(2 omega(k)) h(k).                   (2.4)
```

Because `mu>0`, multiplication by `(2 omega)^(1/2)` preserves the Schwartz
class when applied to the Gaussian. Substitution, rather than analogy, gives

```text
h_f(k)=sqrt(2 omega(k))h(k)/sqrt(2 omega(k))=h(k).
                                                               (2.5)
```

This corrects a possible misreading of N9d: `h` is Gaussian in shell momentum;
the spatial profile `f` is not itself asserted to be Gaussian. It also has
Schwartz tails rather than compact support. The ultraviolet regulator is
therefore a chosen interaction resource, not a consequence of the free scalar
representation.

Translate the body to `X` by translating the same profile. On the shell this is

```text
h_X(k)=exp(-i k.X)h(k).                           (2.6)
```

No component expansion of the field is required after (2.1); all later
operations act on the shell vector `h_X`.

## 3. Construct a translation-covariant interacting Hamiltonian

Let

```text
K=C|g> direct-sum C|e>,
Pi_e=|e><e|,
S=|g><e|+|e><g|,
H_full_space=L^2(R^3_X) tensor K tensor F.        (3.1)
```

The internal operator `S` is not inferred from the scalar field. It is the
minimal declared capability that a field quantum can change the internal
preparation. Construct

```text
H_full
 =P_X^2/(2M)+Delta Pi_e+H_f+g S Phi_0(h_X),
P_X=-i nabla_X.                                  (3.2)
```

Here `Phi_0(h_X)` acts fiberwise in `X`. The Gaussian obeys
`h in H_1` and `h/sqrt(omega) in H_1`. On the finite-particle core,

```text
||a(h)Psi||
 <=||h/sqrt(omega)|| ||H_f^(1/2)Psi||,

||a^dagger(h)Psi||
 <=||h/sqrt(omega)|| ||H_f^(1/2)Psi||
   +||h|| ||Psi||.                               (3.3)
```

The elementary inequality `sqrt(x)<=epsilon x+(4 epsilon)^(-1)` then makes the
interaction infinitesimally bounded with respect to the free energy. The usual
form-sum closure therefore gives a self-adjoint, lower-bounded Hamiltonian. This
is where ultraviolet regularity is spent.

Now compute translation covariance rather than naming it. Since

```text
[P_X,a^dagger(h_X)]=-a^dagger(k h_X),
[P_f,a^dagger(h_X)]=+a^dagger(k h_X),             (3.4)
```

their sum vanishes; the annihilation relation is the adjoint. Every other term
in (3.2) also commutes with

```text
P_tot=P_X+P_f.                                   (3.5)
```

Hence `H_full` decomposes over the spectrum of the total momentum.

## 4. The fiber is exactly N9d's Hamiltonian

The unitary

```text
U=Fourier_X exp(i X.P_f)                          (4.1)
```

performs two computable operations:

```text
exp(i X.P_f) P_X exp(-i X.P_f)=P_X-P_f,
exp(i X.P_f) a^dagger(h_X) exp(-i X.P_f)=a^dagger(h).
                                                               (4.2)
```

The first transfers field momentum into recoil; the second removes the common
translation phase from the coupling. Fourier transformation then replaces
`P_X` by the conserved value `p`. Therefore

```text
U H_full U^dagger
 =integral^direct H_g(p)d^3p,

H_g(p)
 =(p-P_f)^2/(2M)+Delta Pi_e+H_f+g S Phi_0(h).     (4.3)
```

Equation (4.3) is exactly N9d (2.1), including its recoil term, internal flip,
Fock field, and Gaussian shell amplitude. No effective fiber Hamiltonian has
been guessed after the reduction.

The free limit is also literal:

```text
H_g(p)|_(g=0)
 =(p-P_f)^2/(2M)+Delta Pi_e+dGamma(omega),        (4.4)
```

whose field factor is the N4/N4y scalar Fock construction. This does not make
the nonrelativistic body a Poincare representation; the coupling has retained
spatial translations and rotations while giving up full Lorentz covariance.

## 5. The same preparation recovers N9d's departure map

Define the preparation isometry and its projections by

```text
J:K->K tensor F,       Jv=v tensor Omega,
Pi=J J^dagger=I_K tensor |Omega><Omega|,
Q=1-Pi,
B(p)=Q H_g(p)J.                                  (5.1)
```

Apply (4.3) to the two basis inputs. The recoil, internal energy, and free field
terms preserve `Ran J` and are killed by `Q`; annihilation kills `Omega`; only
creation leaves the prepared space. Consequently

```text
B(p)|g>=g |e,a^dagger(h)Omega>,
B(p)|e>=g |g,a^dagger(h)Omega>.                  (5.2)
```

This is N9d (2.3), now reached from the field realization. It is independent of
`p` because the free recoil remains inside the vacuum preparation.

At `p=0`, use the free complementary operator

```text
H_Q(0)=Q H_0(0)Q.                                (5.3)
```

On the two departure vectors its spectral action is multiplication by

```text
ground input:  Delta+epsilon(k),
excited input: epsilon(k),
epsilon(k)=omega(k)+|k|^2/(2M).                  (5.4)
```

Thus the leading operator-valued departure measure is computed as

```text
M_(B,2)(A)
 =B(0)^dagger E_(H_Q(0))(A)B(0)

 =diag(
    g^2 integral 1_A(Delta+epsilon(k))|h(k)|^2 d^3k,
    g^2 integral 1_A(epsilon(k))|h(k)|^2 d^3k
   ).                                            (5.5)
```

Equation (5.5) is exactly N9d (3.2) at its declared order. Because the same
`h`, `omega`, recoil, and preparation occur, all N9c/N9d radial densities,
Stieltjes transforms, Fourier memories, finite-time emission coefficients, and
displayed regression values remain unchanged.

## 6. What has and has not been repaired

The repaired path is now

```text
N4 scalar shell
  -> N4y Fock injection
  -> profile-to-shell map f |-> h_f
  -> H_full and conserved P_tot
  -> exact fiber H_g(p)
  -> N9d B and M_(B,2)
  -> bound/open target transforms.
```

The semantic invariant changes in a controlled way:

| Arrow | Object preserved |
| --- | --- |
| scalar equation -> shell | the same positive-energy scalar solution amplitude |
| shell -> Fock field | the same `h` under `Phi_0(h)Omega=iota_1(h)` |
| translated smear -> fiber | the same interaction after exact unitary conjugation |
| Hamiltonian -> departure | the same action of `H_g` on the named vacuum preparation |
| departure -> measure | the same free-complement spectral weight |
| measure -> N9d outputs | the same target functions of that weight |

The following debts remain and must not be hidden by the new composite:

1. **Interaction selection:** N4's representation does not select `f`, `S`, `g`,
   `M`, or `Delta`; these are additional model inputs.
2. **Covariance:** the mobile body and equal-time coupling are
   nonrelativistic. The constructed model is translation and rotation covariant,
   not Poincare covariant.
3. **Locality:** `Phi_0` comes from the local Klein--Gordon distribution, but the
   exact Gaussian shell cutoff corresponds to a Schwartz spatial tail, not a
   compactly supported interaction. N9e uses the completed shell space and a
   time-zero Schwartz smear; it does not prove that this `h` lies in the image of
   N4g's compact spacetime-source map.
4. **Spin:** this closes only the massive scalar boson interface. It supplies no
   gauge-compatible or higher-spin interaction functor.
5. **Exactness:** the full Hamiltonian and fiber decomposition are exact; (5.5)
   and N9d's predictions are the complete coefficient through order `g^2`, not
   the exact interacting spectral measure. The bare-vacuum preparation is
   constructed; N9f constructs the zero-momentum interacting ground vector and
   finite-coupling energy remainder downstream.
6. **Open dynamics:** no finite-coupling ground-state error bound, resonance pole, exponential lifetime,
   wave operator, or `S` matrix has been constructed.

These limitations are not failures of the bridge. They mark precisely where a
new research question would have to add new structure.

## 7. Computability and global verdict

The bridge adds no dressed-state solve. Its complete construction cost is

```text
one shell normalization
  + one Fock functor
  + one multiplication profile
  + one exact translation unitary
  + one application of H_g to two vacuum inputs
  + one radial pushforward already owned by N9c/N9d.
```

This is a semantic compression: the field equation supplies `omega` and the
one-particle normalization; the profile supplies only `h`; translation symmetry
supplies recoil and the fiber; preparation supplies `B`; the observable supplies
the final transform. None of those roles is duplicated.

The former audit verdict “two modules separated by an unconstructed interface”
is therefore amended for this one regulated scalar model. The universal verdict
is unchanged: free representation theory still does not determine interactions.

## Verification ledger

| Obligation | Equality witness | Verdict |
| --- | --- | --- |
| scalar equation -> one-particle space | positive mass shell plus invariant-measure unitary | exact |
| spatial profile -> N9d Gaussian | `f_hat=sqrt(2 omega)h`, hence `h_f=h` | exact; noncompact Schwartz profile |
| interaction -> conserved total momentum | cancellation in (3.4) | exact on the common core |
| full Hamiltonian -> fiber | unitary identities (4.2) | exact |
| free field recovery | set `g=0` in (4.3) | exact |
| preparation -> departure | direct action on `|g/e,Omega>` in (5.2) | exact |
| departure -> N9d measure | free complementary spectral action (5.4)--(5.5) | complete coefficient through `g^2` |
| interacting ground state | scalar Feshbach root and remainder | closed downstream by N9f at `p=0` |
| finite-coupling bound/open observables | N9f error bounds and N9g kinetic audit | ground and short-time event certified; kinetic law supported only for the one-excitation comparator, with exact exclusive transfer open |

## Edges

- `N4 -> N9e`: pass the massive spin-zero Klein--Gordon shell and dispersion.
- `N4y -> N9e`: pass the symmetric Fock functor and exact vacuum one-particle
  injection.
- `N9c/N9d -> N9e`: pass the benchmark Hamiltonian, preparation, and measure as
  the exact recovery target; N9e supplies their previously absent upstream
  provenance.
- `N9e -> synthesis audit`: replace the scalar missing-interface verdict by a
  supported model-local composite while retaining every universal limitation.
- `N9e -> N9f`: pass the exact fiber Hamiltonian and bare preparations for the
  finite-coupling same-observable test.
- `N9e -> N9g`: pass the recoil fiber, full counter-rotating interaction, and
  parity sectors that expose the multiparticle kinetic-transfer obligation.
