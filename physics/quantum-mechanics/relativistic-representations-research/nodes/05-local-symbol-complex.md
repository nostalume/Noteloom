# Local complex and free-field machine

Status: declared finite symmetric, exterior, and Clifford families support local
cohomology and free bosonic/fermionic completion

## Obstruction

An orbitwise carrier is not yet a local field, a causal response, or a quantum
algebra. These must be generated while preserving the physical cohomology rather
than inferred from the particle label.

## Construct the local complex

Supply a finite carrier `V`, gauge carrier `G`, equation carrier `E`, and invariant
resources. Search bounded homogeneous equivariant symbols

```text
R(p):G->V,  D(p):V->E,  C(p):E->K
```

and calculate

```text
r_1(p)=D(p)R(p),
r_2(p)=C(p)D(p).
```

Exact coefficient solving must make the polynomial residuals vanish. At a
standard momentum,

```text
H(k)=ker D(k)/im R(k)
```

must be explicitly intertwined with the requested physical fiber. Equivariance
then transports the quotient over the orbit.

Symmetric carriers use multiplication `P`, divergence `A`, trace `T`, metric
insertion `U`, and wave scalar `Q`. Exterior carriers use wedge and contraction.
For fermions, a first-order symbol `S` is admitted only when factorization gives

```text
S(p)^2=Q(p)I.
```

Polarization then constructs, rather than imports, the Clifford relation:

```text
S(p)S(q)+S(q)S(p)=2 eta(p,q)I.
```

The bounded operation grammar and residual solver are owned by
[node 13](13-natural-operation-grammar.md). Components serve only as finite
rank/sign certificates.

## Construct causal bosonic propagation

An action requires a pairing, density/orientation, formal adjoint, boundary
domain, and normalization in addition to `DR=0`. Given its self-adjoint Euler
operator `D`, admit compact sources with `R^dagger j=0`. A gauge-fixed Green
operator must satisfy on the source/solution quotients

```text
D G j=j mod im R,
G D f=f mod im R.
```

Gauge representatives pair identically because

```text
<j,R epsilon>=<R^dagger j,epsilon>=0.
```

The causal propagator `E=G_ret-G_adv` constructs the solution image and symplectic
form. Positive-energy restriction gives `K`, and the CCR field is

```text
Phi(j)=a(Kj)+a^dagger(Kj),
[Phi(j),Phi(k)]=i sigma(j,k)I.
```

The commutator follows from the CCR and the constructed symplectic form; it is not
a second consequence of group representation alone.

## Construct fermionic propagation

If first-order factors obey `S_-S_+=QI`, a scalar causal inverse constructs

```text
G_S=S_-G_Q,
S_+G_S=S_+S_-G_Q=QG_Q=I
```

on admitted fermionic sources. Positive-frequency completion yields `H_1`; its
antisymmetric Fock construction gives

```text
Psi(f)=a(Kf)+a^dagger(JKf),
{Psi(f),Psi(g)^*}=<Kf,Kg>I,
```

where the required real/charge-conjugation structure `J` is supplied. Tensoring
the abstract Clifford action with symmetric operations produces bounded
spinor-tensor families; gamma/trace constraints are generated when the residual
fails to preserve physical cohomology. No gamma-matrix table is primitive.

## Construct a representation-free spin readout

For the mostly-plus convention used by node 30, set `B=-eta` and write the
polarized factor as `C`, so `{C(v),C(w)}=2B(v,w)`. A matrix-free parity-even trace
is forced by cyclicity, `tau(1)=1`, and `tau(odd word)=0`. Moving the first factor
through an even word computes

```text
tau(C(v_1)...C(v_(2n)))
 =sum_(j=2)^(2n)(-1)^j B(v_1,v_j)
  tau(C(v_2)...omit C(v_j)...C(v_(2n))).
```

Thus every spin sum reduces to invariant pairings, not gamma entries. Parity
doubling is an admitted resource: it cancels the dimension-three odd trace that
would otherwise require an orientation and a selected irreducible parity sector.

The recurrence itself generates a second representation. For a word of length
`2n`, form the skew matrix `A` by `A_(ij)=B(v_i,v_j)` for `i<j`. Expanding
`Pf(A)` along its first row is exactly the recurrence above, hence

```text
tau(C(v_1)...C(v_(2n)))=Pf(A).                 (05.8)
```

This is not an imported trace formula. It is the recurrence stored once as a skew
normal form. A nonzero pivot `a=A_(12)` generates the smaller matrix

```text
A'_(ij)=A_(ij)-[A_(1i)A_(2j)-A_(1j)A_(2i)]/a,
Pf(A)=a Pf(A').                                (05.9)
```

The compiler retains every uncertain condition `a!=0`; equality to the polynomial
recurrence supplies continuation across a vanishing pivot. The two realizations
therefore preserve the same semantics but expose different costs: factorial
expanded pairings, shared recurrence updates, and skew-elimination updates.

But all three wait until words have been multiplied. To quotient before that
growth, let `N` retain exterior grades. The defining relation forces the action
`L_v` of a new Clifford factor on a blade:

```text
L_v(w_1 wedge ... wedge w_r)
 =v wedge w_1 wedge ... wedge w_r
  +sum_j (-1)^(j-1) B(v,w_j)
    w_1 wedge ... omit(w_j) ... wedge w_r.       (05.10)
```

Set `N(C(v)x)=L_v N(x)`. On two vectors the two orders then compute

```text
L_v(w)+L_w(v)
 =v wedge w+B(v,w)+w wedge v+B(w,v)=2B(v,w).    (05.11)
```

Thus `N` descends through exactly the Clifford relation. Bilinear extension of
`L_v` defines `star` with `N(xy)=N(x) star N(y)`, while
`tau(x)=grade_0 N(x)` in the parity double. In
dimension `d` it retains at most `2^d` blade coefficients regardless of word
length. The executable backend serializes those blades in a supplied orthogonal
frame; it refuses a nonorthogonal frame rather than hiding basis construction.

The massive shell itself generates the external projector

```text
Pi(p)=(1+C(p)/m)/2,
Pi(p)^2-Pi(p)=-(eta(p,p)+m^2)/(4m^2)=0.
```

These operations are consumed by [node 30](30-prepared-matter-event.md).
Their semantic advantage does not imply computational advantage: node 30 compares
the generated trace backends on the complete observable before selecting one.

## Retained interface and boundary

```text
LocalFreeField(carrier, resources, source_domain)
 -> local complex + physical cohomology
 -> causal quotient + positive shell + CCR/CAR field
 | refusal(residual, source, domain, or factorization failure).

CliffordTrace(word, metric, parity resource)
 -> invariant value + expanded/shared/Pfaffian costs + pivot conditions
 | refusal(unresolved odd trace sector).

ExteriorNormalForm(words, admitted orthogonal frame)
 -> at most 2^d grades + product/relation certificate
 | refusal(nonorthogonal serialization frame).
```

Maxwell, spin `1/2`, spin `3/2`, and bounded symmetric higher-spin cases are
regressions. The node does not generate an interaction, state beyond the supplied
free vacuum, generic higher-spin source, mixed-symmetry complex, or countable
carrier completion. [Node 08](08-realization-equivalence-boundary.md) specifies
what equivalence and computational replacement require; node 30 tests whether the
retained quotient calculus reaches an interacting detector observable.
