# N4v — Rest Mass, Curvature Mass, and Poincare-Shell Closure

Status: exact shell-closure, mass-coincidence, and nonrelativistic recovery
identities supported under the declared sharp single-orbit hypotheses; existence
and numerical mass of a generic interacting relativistic composite remain
dynamical obligations; N4w evaluates one integrable bootstrap model  
Consumes: [N2 representation spaces](02-three-representation-spaces.md),
[N4r field/mechanics projection](04r-field-mechanics-stability.md),
[N4s field/particle extraction](04s-field-particle-extraction.md),
[N4t neutral-composite same-state test](04t-neutral-composite-same-state.md),
[N4u effective-mass audit](04u-effective-mass-route-audit.md),
[relativistic-shell source contracts](../sources/relativistic-shell-contracts.md),
and [finite shell regression](../computation/04v-relativistic-shell/README.md)  
Produces: the exact condition under which an interacting spectral branch is one
massive Poincare orbit, the coincidence of orbit/rest/curvature mass, a
coordinate-free Hessian, an exact low-momentum recovery bound, and a separation
of symmetry compression from dynamical mass computation

## Node contract

- **Question/capability:** when does the energy of a mechanically prepared bound
  composite become the mass of a relativistic particle, and what part of its
  motion can then be computed without resolving every momentum fiber?
- **Presumptions:** a positive-energy unitary Poincare action and its translation
  spectral measure have been constructed; a nonzero sharp stable spectral
  component is invariant, connected, contains a rest point, and carries one
  massive orbit rather than several species or a continuum. The field-created
  particle quotient has nonzero access to it. Differentiability is needed only
  when curvature is requested.
- **Representation choices:** the time orientation chooses the positive sheet.
  A rest frame is used to name the mass, but the resulting Minkowski norm and
  shell are frame independent.
- **Output:** a same-input covariance computation closing the rest state into a
  shell, the invariant dispersion and its Hessian, an exact comparison with the
  nonrelativistic kinetic energy, and the precise datum that dynamics must still
  supply.
- **Boundary:** Poincare symmetry does not prove that the shell exists, is stable,
  or is accessible, and does not determine its numerical mass, residue, spin,
  width, or scattering matrix.

## 1. Begin with an interacting spectral state, not a free dispersion

N4s constructs particle candidates from the actual translation spectrum of a
field theory. Retain the following typed data:

```text
H                  physical Hilbert space,
U(a,Lambda)        positive-energy Poincare action,
E(Delta)           joint translation spectral measure,
K_b=E(Sigma_b)H    nonzero stable spectral subspace.
```

N4r may supply a prepared pole in the rest fiber, while N4s supplies the
additional field-created access and stability obligations. Neither input alone
licenses the free formula `sqrt(M^2+|P|^2)`.

Assume the spectral component admits the usual measurable fiber description and
contains the rest momentum

```text
k=(M_b,0),  M_b>0.
```

The fiber over `k` contains the rest-frame internal state; it is not asserted to
be a normalizable sharp-momentum vector in the full direct integral. Here `M_b`
is initially only the time-translation spectral value of that rest fiber. It is
not an internal Coulomb eigenvalue and is not yet called a curvature mass. The
single-orbit presumption says that the connected spectral support selected as
this particle species contains exactly the momenta obtained from `k` by proper
orthochronous Lorentz transformations. This is a dynamical spectral-selection
input, not a conclusion from covariance alone.

## 2. Covariance transports the same spectral state

Translation covariance already computed in N2 and used by N4s is

```text
U(Lambda)E(Delta)U(Lambda)^(-1)=E(Lambda Delta).
```

Take any `psi in K_b` and any measurable spectral neighborhood `Delta` inside
the selected component. Apply covariance to its localized wave packet:

```text
E(Lambda Delta)U(Lambda)E(Delta)psi
 =U(Lambda)E(Delta)U(Lambda)^(-1)
   U(Lambda)E(Delta)psi
 =U(Lambda)E(Delta)psi.
```

Thus the transformed packet is not a second state inserted by analogy: it is the
same particle subrepresentation with transported spectral support. In the direct-
integral disintegration, this identity induces the corresponding map from the
fiber over `p` to the fiber over `Lambda p` almost everywhere. The semantic
invariant is the state in the covariant particle subrepresentation; only its
inertial-frame spectral support changes.

Lorentz transformations preserve the quadratic form. Therefore every transported
momentum satisfies

```text
(Lambda k)^2=k^2=M_b^2
```

and has positive energy because the connected group preserves time orientation.
Conversely, let `P` be any spatial momentum. If `P` is nonzero, put

```text
n=P/|P|,
sinh rho=|P|/M_b.
```

The boost acting on the time--`n` plane and fixing its orthogonal complement
computes

```text
B_(rho,n) k
 =(M_b cosh rho, M_b sinh rho n)
 =(sqrt(M_b^2+|P|^2),P).
```

For `P=0`, use the identity boost. Hence the orbit through `k` is exactly the
positive massive shell

```text
O_(M_b)^+
 ={p | p^2=M_b^2, p^0>0}.
```

This does not repeat N2's free classification. N2 constructs what one massive
orbit means. The new statement is conditional identification: if the interacting
stable component selected by N4s is one orbit through the rest pole supplied by
the field dynamics, then that component has this shell.

## 3. The shell constructs the dispersion rather than assuming it

Spatial translation labels slice the positive shell once. Let `E_b(P)` denote
the unique positive time component above `P`. Evaluating the invariant on that
same shell point gives

```text
E_b(P)^2-|P|^2=M_b^2.
```

The positive-energy choice removes the second algebraic root, so

```text
E_b(P)=sqrt(M_b^2+|P|^2).
```

This equation has three constructed inputs: the rest spectral value `M_b`, the
Lorentz orbit generated from the same state, and the positive time orientation.
Its output is the energy of that state at every momentum. No local field equation,
gamma matrix, or component wavefunction enters the deduction.

On the shell subspace, the same statement is also an operator identity. The joint
spectral calculus applies the function `p -> p^2` to the translation generators:

```text
P_mu P^mu=M_b^2 I_(K_b),
H|_(K_b)=sqrt(M_b^2+bold P^2).
```

The equality is restricted to `K_b`. It is not an identity on the full field
Hilbert space, whose spectrum also contains vacuum, other particles, and
continua.

## 4. One invariant differentiation identifies the three masses

Let `X,Y` be spatial momentum variations. Differentiate the shell identity as a
map between Euclidean spatial momentum space and energy:

```text
2 E_b(P) dE_b(P)[X]=2 <P,X>.
```

Both sides evaluate the variation of the same invariant equation in the same
direction `X`. Since `E_b(P)>0`, division constructs

```text
dE_b(P)[X]=<P,X>/E_b(P).
```

Differentiate this scalar response in direction `Y`:

```text
Hess E_b(P)[X,Y]
 =<X,Y>/E_b(P)
  -<P,X><P,Y>/E_b(P)^3.
```

At the rest point,

```text
E_b(0)=M_b,
dE_b(0)=0,
Hess E_b(0)[X,Y]=<X,Y>/M_b.
```

N4u defines the inverse effective-mass tensor by this Hessian. Therefore, on a
sharp massive Poincare shell,

```text
M_orbit=M_rest=M_curvature=M_b.
```

This is an equality of three constructions on one spectral branch:

1. `M_orbit^2` is the value of the translation Casimir on `K_b`;
2. `M_rest` is the positive time-translation value at the rest point;
3. `M_curvature` is the inverse quadratic response of that same branch.

The coincidence is not true for an arbitrary translation-invariant band. N4t's
nonrelativistic atom has no boosts, so its `E_g(0)` and `M_eff` remain independent
dynamical data.

## 5. Dynamics computes one rest datum; covariance propagates it

N4r's prepared equation can locate a pole through

```text
F_0(z)=z-h_0-Sigma_0(z).
```

If a zero `M_b` of this exact rest-fiber equation is a sharp stable field
eigenvalue and N4s's field-created quotient accesses it, N4v uses covariance to
obtain the entire branch. For a heavy composite comparison, the rest value may
have the semantic decomposition

```text
M_b=E_ref+epsilon_internal+delta_field,
```

where `E_ref` contains constituent rest and renormalization reference data,
`epsilon_internal` is the mechanically computed binding contribution, and
`delta_field` contains the corrections retained by the exact prepared kernel.
This line is a bookkeeping identity only after all terms are defined in one
renormalization convention; symmetry does not compute any of them.

The computational compression, when the hypotheses are met, is therefore

```text
one rest-pole computation plus a shell-existence/stability proof
  -> one number M_b
  -> exact E_b(P), velocity, and curvature at every momentum.
```

Repeated interacting fiber eigenvalue solves are unnecessary for these
kinematic observables. The gain is genuine because covariance removes momentum
dependence rather than hiding it in another inverse. It does not reduce the
rest-pole, self-energy, renormalization, or stability computation.

## 6. The nonrelativistic band is recovered with an exact error witness

Subtract the rest energy and write

```text
K_rel(P)=E_b(P)-M_b.
```

Rationalizing the same shell equation gives the exact identity

```text
K_rel(P)=|P|^2/[E_b(P)+M_b].
```

Compare it with the nonrelativistic kinetic energy on the same momentum:

```text
K_rel(P)-|P|^2/(2M_b)
 =-|P|^4/[2M_b(E_b(P)+M_b)^2].
```

The right side is the equality witness, not an unspecified Taylor remainder.
Since `E_b(P)+M_b>=2M_b`,

```text
|K_rel(P)-|P|^2/(2M_b)|
 <=|P|^4/(8M_b^3).
```

Thus N4u's curvature description is recovered at low momentum with a controlled
same-observable error. A general nonrelativistic dressed band may still contain
independent higher-order coefficients; the Poincare shell fixes all of them only
in the relativistic theory satisfying this node's hypotheses.

## 7. Bound mechanics, one particle, and scattering are different spectral levels

An internal bound state is discrete in relative variables. Once the whole system
is translation invariant, its center-of-mass momentum varies continuously, so
the bound state generates a continuous one-particle shell. These are compatible,
not competing descriptions:

```text
discrete internal pole
  + translation covariance
  + stable Lorentz orbit
  -> one composite-particle shell.
```

Scattering lives at a further level. Several stable shells combine into
multi-particle spectral continua, and incoming/outgoing maps compare their
asymptotic embeddings in the interacting field Hilbert space. Knowing `M_b`
fixes the external kinematics of one scattering species but not the scattering
operator, form factors, production amplitudes, or graph integrals.

This explains the earlier mechanics/field separation. Bound mechanics primarily
computes the internal pole. Field theory must additionally construct whether
that pole survives as a covariant particle and how several such excitations
interact asymptotically.

## 8. Failure boundaries change the output rather than the notation

- If the spectral component contains several massive orbits, one scalar `M_b`
  does not describe it; decompose the invariant spectral measure first.
- If the state is a resonance, its continued complex pole is not a normalizable
  Poincare-shell subspace and has no exact curvature-mass identity of this kind.
- If long-range charge produces an infraparticle, no sharp mass shell exists;
  N4s's particle-weight output replaces this node.
- If a medium, lattice, background source, or cutoff breaks boosts, rest energy
  and curvature mass again become independent, and the curvature may be a tensor.
- If the branch meets a continuum and loses the required stability, covariance
  of the full spectrum does not rescue a one-particle interpretation.

## 9. Checks, computability verdict, and frontier

The [finite regression](../computation/04v-relativistic-shell/README.md) checks
that a rapidity boost maps a rest momentum to the derived shell while preserving
the Minkowski norm, that a five-point curvature agrees with `1/M_b`, and that the
exact nonrelativistic recovery residual vanishes. It is only a bounded coordinate
check of the invariant derivation above.

Supported:

- covariance transports the same sharp spectral state along its orbit;
- the single massive orbit through a rest point is the positive mass shell;
- positive shell slicing constructs the relativistic dispersion;
- orbit, rest, and curvature masses coincide exactly;
- subtracting the rest energy recovers nonrelativistic kinetic energy with an
  explicit quartic error bound;
- once a sharp rest mass is known, covariance genuinely eliminates repeated
  momentum-fiber solves for shell kinematics.

Open:

- a full constructive local-QFT realization of the N4w integrable same-particle
  diagram and a `3+1`-dimensional neutral model;
- a local vacuum-to-composite interpolator with nonzero shell projection;
- proof that an N4r prepared rest pole remains a sharp stable shell in that model;
- numerical computation and renormalization of `M_b`;
- spin multiplicity, residues, form factors, and scattering amplitudes on the
  resulting shell;
- charged infraparticle and unstable-resonance replacements.

The first such model test is now [N4w](04w-sine-gordon-breather-rest-pole.md).
It computes a neutral sine-Gordon breather mass from a soliton--antisoliton pole,
constructs local-field access within the exact bootstrap/form-factor contracts,
and exposes the remaining constructive-locality boundary. The generic next
question is no longer whether shell propagation works; it is which parts of that
pole/fusion/access route survive without integrability and in `3+1` dimensions.

## Edges

- `N2 -> N4v`: pass the internally constructed translation spectrum, Lorentz
  orbit, positive massive shell, and rest stabilizer.
- `N4r -> N4v`: pass the exact prepared rest-pole equation and its field-state
  recovery obligations.
- `N4s -> N4v`: pass the field-created sharp-shell quotient, covariance, access,
  stability, resonance, and infraparticle boundaries.
- `N4t -> N4v`: pass the nonrelativistic dressed band and the missing-boost
  boundary as the comparison case.
- `N4u -> N4v`: pass curvature mass and the distinction between exact
  reformulation and genuine momentum-dependence compression.
- `RS-01/RS-02 -> N4v`: pass the massive-orbit classification and stable-shell
  theorem boundaries; all mass-coincidence and recovery equations are computed
  internally here.
- `C4v -> N4v`: pass the finite boost, curvature, and recovery regression.
- `N4v -> relativistic rest-pole evaluation`: pass the one required dynamical
  number, its shell/stability checks, and the exact kinematic outputs recovered
  from it.
- `N4v -> N4w`: pass the rest-mass-to-shell propagation and require an actual
  interacting pole, stability gap, and nonzero field-access map.
- `N4v -> N7/manuscript synthesis`: pass the precise field/mechanics/particle
  relation and the boundary between symmetry-determined shell form and
  dynamics-determined mass.
