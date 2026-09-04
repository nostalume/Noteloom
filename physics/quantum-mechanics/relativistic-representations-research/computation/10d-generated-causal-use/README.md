# Computation Contract — Generated Compact-Source Causal Use

Parent node: [N10d generated causal use](../../nodes/10d-generated-causal-use.md)

## Semantic question

Can N10c's retained constructor drive N4e's causal response interface on an actual
compact admissible source and recover nonzero physical-shell data, without importing
a component Maxwell equation as a new starting point?

The packet uses the smallest complete specialization. N10c generates

```text
R=P,
C=A-(1/2)PT,
D=Q-PA+(1/2)P^2T.
```

On a rank-one field the trace operations vanish, so the same returned object becomes

```text
R=P,
C=A,
D=Q-PA.
```

This is the Maxwell/Lorenz interface consumed by N4e.

## Internally constructed source

Let `b(s)=exp(-1/(1-s^2))` for `|s|<1` and zero otherwise, and set

```text
chi(t,x,y,z)=b(t)b(x)b(y)b(z).
```

Choose the compact antisymmetric tensor with `K^{01}=chi`, `K^{10}=-chi`, all
other entries zero, and construct

```text
J^mu=partial_nu K^{nu mu}.
```

Commuting derivatives are symmetric in `(mu,nu)` while `K` is antisymmetric, so
`partial_mu J^mu=0`. Conservation is therefore a construction certificate, not a
numerical divergence test.

## Run

```text
node check-generated-causal-use.mjs
```

The executable then checks two downstream uses of this same current:

1. the scalar retarded Green formula produces a nonzero potential component at
   `(t,x)=(2,0)`, while the advanced value is exactly zero by source support;
2. at the null covector `(omega,0,0,omega)`, `omega=1/2`, the transverse
   `x`-polarized Fourier amplitude is nonzero.

The retarded cube integral is evaluated by midpoint sequences at `24`, `36`, and
`52` cells per direction. Fourier factors use composite Simpson integration. The
analytic sign/support and current-conservation arguments own the result; quadrature
only supplies a finite numerical witness.

## Boundary

This probe tests generated-to-causal interoperability, not a new Green theorem.
N4e supplies existence, uniqueness, support, and source/solution quotient
coincidence. A nonzero shell value is an amplitude witness; continuity gives a
nonzero neighborhood, but this packet does not normalize a one-particle state.
The rank-one specialization also does not establish compact-source transfer for
higher spin or the Clifford family.
