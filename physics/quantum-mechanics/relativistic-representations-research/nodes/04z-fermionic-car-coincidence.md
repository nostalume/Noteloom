# N4z — Fermionic Causal Form and CAR Coincidence

Status: the local causal Euler form and the positive particle/antiparticle CAR
form coincide for every separate finite half-integer spin on Minkowski spacetime,
up to the single overall normalization convention of the free quadratic action  
Consumes: [N4i fermionic Euler and Green construction](04i-half-integer-green-construction.md),
[N4j causal quotient](04j-half-integer-causal-quotient.md), [N4k positive
shell construction](04k-half-integer-positive-frequency.md), [N4l support
faithfulness](04l-half-integer-support-faithfulness.md), [N4y quantization and
recovery](04y-quantization-recovery-bridge.md), and
[quantization--recovery contracts](../sources/quantization-recovery-contracts.md)  
Produces: one same-source equality witness joining the local Euler quotient,
the positive two-shell norm, the self-dual CAR algebra, and graded locality

## Research contract

- **Question:** does the positive form constructed from particle and antiparticle
  shell amplitudes equal the causal form of the local Euler equation, or are they
  merely two unrelated fermionic structures?
- **Presumptions:** one fixed finite rank `n>=0`; the Fourier, causal-propagator,
  and Dirac-pairing conventions of N4i--N4k; compact admissible complex sources;
  and one nonzero normalization of the free quadratic action.
- **Output:** an invariant, component-free computation on the same two source
  classes proving

  ```text
  q_n([J],[K])=z_n^pair([J],[K]),
  tau_n([J],[K])=2 Re z_n^pair([J],[K])
  ```

  after fixing that normalization once.
- **Boundary:** the proof concerns each separate finite-rank free system and the
  compact-source image. It does not prove density in the full induced Hilbert
  space, select a Majorana real form, or extend the construction to curved or
  interacting backgrounds.

The semantic route has four operations:

```text
admissible source
  -> annihilate the gauge part of a canonical shell lift
  -> remove trace reversal on the physical screen
  -> apply the null Clifford homotopy once
  -> obtain the positive two-shell metric.
```

No gamma matrix, spinor component basis, or rank-by-rank propagator numerator is
needed.

## 1. Construct the causal form before comparing it

N4i/N4j construct

```text
O_n^C
 ={J in Gamma_c(F_n) | R_n^dagger J=0}/E_n Gamma_c(F_n),

G_n^causal[J]=S_n Delta_n M_n^(-1)J.
```

Let `<.,.>_n` denote the integrated Lorentz Dirac--Fischer pairing. For the
moment retain a convention constant `c_n != 0` and define

```text
q_n([J],[K])
 =c_n integral_M <J,G_n^causal K>_n.
```

The causal Green form is anti-Hermitian before the conventional factor `i` is
inserted. Accordingly `c_n` separates into the fixed phase that makes `q_n`
Hermitian and one nonzero real normalization of the rank-`n` quadratic action.
It is not new dynamics, and the action is never rescaled by a complex phase.

This form descends to the quotient. If the second source changes by `E_na`, N4i
computes

```text
G_n^causal(E_na)=-2R_n Delta_n B_na.
```

Admissibility of `J` then gives

```text
<J,G_n^causal(E_na)>_n
 =-2<R_n^dagger J,Delta_nB_na>_(n-1)
 =0.
```

If the first source changes by `E_na`, formal self-adjointness of `E_n` and the
homogeneous equation `E_nG_n^causal K=0` give the same result. Thus the equality below is
an equality of observable classes, not representatives.

Because `G_n^causal` has causal support, the same formula also gives

```text
q_n([J],[K])=0
```

whenever the source supports are causally disjoint. This is the future graded-
locality witness.

## 2. Put both forms on the same null-shell input

For an admissible source put

```text
K_J=M_n^(-1)J,
X_J(p)=S_n(p)K_J_hat(p),
r_J(p)=res_p X_J(p).
```

On the nonzero null cone, N4b's physical exact sequence is

```text
0 -> G_n --R_n(p)--> ker S_n(p)
  --res_p--> H_n(p) -> 0.
```

For `r_K(p)` choose its canonical screen lift `tilde r_K(p)`. It is constructed
by extending only over the Euclidean screen, with

```text
Gamma tilde r_K=0,
S_n(p)tilde r_K=0,
res_p tilde r_K=r_K.
```

Exactness compares this lift with the actual shell field:

```text
X_K(p)-tilde r_K(p)=R_n(p)epsilon(p).
```

Now evaluate both representatives against the *same* admissible source. Since
`R_n^dagger J=0`,

```text
<J_hat(p),X_K(p)>_n
 =<J_hat(p),tilde r_K(p)>_n.
```

The discarded term is precisely gauge. This is stronger than saying that two
paths are equivalent: their difference is constructed and its pairing is
computed to zero.

## 3. Trace reversal disappears on the physical representative

N4i gives `J=M_nK_J`, with `M_n^dagger=M_n`. The canonical lift is gamma
traceless, so its trace-reversal layers vanish and

```text
M_n tilde r_K=tilde r_K.
```

Consequently

```text
<J_hat,tilde r_K>_n
 =<M_nK_J_hat,tilde r_K>_n
 =<K_J_hat,M_ntilde r_K>_n
 =<K_J_hat,tilde r_K>_n.
```

Only the restriction `v_J` of `K_J_hat` to the screen tensor slots contributes
to the last expression. On those slots the field amplitude is

```text
r_J=gamma(p)v_J.
```

Thus all off-screen and trace-reversal data have been removed by verified
quotients before positivity is discussed.

## 4. One Clifford homotopy turns the action pairing into the positive metric

Choose the null witness `a_p` of N4k, with `p.a_p=1`, and write
`epsilon_p=sign(p^0)`. Since `r_K in ker gamma(p)`, the Clifford relation gives

```text
gamma(p)gamma(a_p)r_K
 =[2-gamma(a_p)gamma(p)]r_K
 =2r_K.
```

Use the Dirac adjoint property on the same pair `v_J,r_K`:

```text
kappa_p(r_J,r_K)
 =epsilon_p beta(gamma(p)v_J,gamma(a_p)r_K)
 =epsilon_p beta(v_J,gamma(p)gamma(a_p)r_K)
 =2epsilon_p beta(v_J,r_K).
```

Therefore

```text
beta(v_J,r_K)=(epsilon_p/2)kappa_p(r_J,r_K).
```

The Lorentz metric restricted to each of the `n` spacelike screen slots is
`-g_Q`. Hence their symmetric tensor contraction contributes the fixed sign
`(-1)^n`, while N4k's positive tensor-screen metric contributes `h_(n,p)`:

```text
<J_hat(p),X_K(p)>_n
 =((-1)^n epsilon_p/2) h_(n,p)(r_J(p),r_K(p)).
```

This is the pointwise coincidence witness. It is independent of rank except for
the transparent screen sign.

## 5. The causal sign makes both energy shells positive

The scalar-wave causal propagator has Fourier support

```text
Delta_hat(p)=c_Delta epsilon_p delta(p^2),
```

where `c_Delta` is the fixed Fourier convention phase. Multiplying this by the
previous pointwise identity cancels the energy sign:

```text
epsilon_p * epsilon_p=1.
```

Splitting the cone into future `p` and past `-p`, then applying N4k's conjugate-
past definition, gives

```text
q_n([J],[K])
 =C_n integral_(O_+) [
     h_(n,p)(w_n^+[J],w_n^+[K])
    +conjugate(h_(n,-p))(w_n^-[J],w_n^-[K])
   ] dmu_0(p)
 =C_n z_n^pair([J],[K]),
```

with one nonzero rank-dependent convention constant

```text
C_n=c_n c_Delta (-1)^n/2.
```

After the Hermitian phase has been fixed, `C_n` is real and nonzero. Multiplying
a free quadratic action by a nonzero real constant changes neither its Euler
equation nor its gauge quotient; it rescales its causal pairing. Fix that allowed
normalization once by `C_n=1`. The result is

```text
q_n=z_n^pair.
```

The important claim is not the arbitrary numerical convention. It is that the
two forms are proportional by a *single global scalar*, with no momentum-,
helicity-, or source-dependent correction.

## 6. Realification constructs the local CAR algebra

The complex source quotient need not be given a Majorana constraint. Regard it
as a real vector space and define

```text
tau_n(x,y)=2 Re q_n(x,y)
          =2 Re z_n^pair(x,y).
```

N4k proves positivity of `z_n^pair`, and N4l proves faithfulness of its shell
map. Hence

```text
tau_n(x,x)=2 ||W_n^pair x||^2 > 0
```

for nonzero `x`. The positive-type condition required by the self-dual CAR
construction is therefore not assumed; it is inherited from the same causal
Euler form.

On the antisymmetric Fock space, define

```text
b_n(x)=a(W_n^pair x)+a^dagger(W_n^pair x).
```

Then the CAR computation and the causal computation now have the identical
right-hand side:

```text
{b_n(x),b_n(y)}
 =2 Re <W_n^pair x,W_n^pair y>
 =tau_n(x,y) identity.
```

For causally disjoint source supports, Section 1 gives `tau_n(x,y)=0`; therefore
the smeared fields anticommute. Acting on the vacuum still gives N4y's exact
one-particle recovery:

```text
P_1 b_n(x)Omega=iota_1(W_n^pair x).
```

Local equation, positive particles, CAR, and vacuum recovery are now one
commuting construction.

## 7. Verification ledger and boundary

| Obligation | Same-input witness | Verdict |
| --- | --- | --- |
| quotient independence | pair `G_n(E_na)=-2R_nDelta_nB_na` with `R_n^dagger J=0` | supported |
| remove gauge lift | `X_K-tilde r_K=R_nepsilon` paired with the same admissible `J` | supported |
| remove trace reversal | `M_n^dagger=M_n` and `M_ntilde r_K=tilde r_K` | supported |
| action/screen equality | one null Clifford homotopy on `v_J,r_K` | supported |
| two-shell positivity | causal `epsilon_p` times screen `epsilon_p` | supported |
| CAR equality | realify the normalized Hermitian equality | supported |
| graded locality | causal support of `G_n^causal` | supported |
| faithfulness | `tau_n(x,x)=2||W_n^pairx||^2` plus N4l | supported |

Still open:

- density of the compact-source image in the entire induced Wigner space;
- an optional Majorana or other invariant smaller real form;
- countable-spin topology, curved backgrounds, and interactions;
- comparison of different action normalizations across ranks if the separate
  finite-rank systems are embedded into one coupled theory.

## Edges

- `N4i/N4j -> N4z`: pass the formally self-adjoint Euler representative,
  admissible causal response, and local observable quotient.
- `N4k/N4l -> N4z`: pass the positive two-shell form and its faithfulness.
- `N4y -> N4z`: pass N4y's isolated fermionic CAR-locality obligation; N4z
  closes it without changing the global quantization/recovery diagram.
- `N4z -> N7/manuscript synthesis`: pass one normalized local free fermionic
  theory in which causal, spectral, and CAR forms have been proved equal.
