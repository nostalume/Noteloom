# Computation Contract — Generated Higher-Spin Source Adapter

Parent node: [N10e generated source adapter](../../nodes/10e-generated-source-adapter.md)

## Semantic question

Can the failure of N10c's generated Green-input condition to coincide with physical
source conservation generate the missing source adapter, and can that returned
adapter drive a compact spin-two causal/shell calculation?

The input does not include trace reversal. It contains:

```text
R=P,
C=A-(1/2)PT,
```

from N10c, the Lorentz-metric Fischer pairing, and a resource budget allowing zero
or one metric insertion.

## Residual construction

Pairing with a traceless parameter means target terms beginning with `U` are pure
trace and vanish. The identity candidate gives

```text
A-C=(1/2)PT,
```

which cannot vanish. The canonical zero-order normal words with one trace layer are
generated as `{I,UT}`. Evaluating the new word before taking the paired quotient gives

```text
A U T=U A T+2PT  ->  2PT.
```

Exact rational elimination against the generated `C` returns

```text
M=I-(1/4)UT,
A M-C=-(1/4)UAT.
```

The remaining term pairs to zero against every traceless parameter. A budget with
no metric insertion returns an explicit `PT` obstruction.

On the double-traceless spin-`s` carrier, `UT` acts by `4s` on the trace layer.
The program therefore constructs, rather than supplies,

```text
M_s^(-1)=I-[1/(4(s-1))]UT,  s>=2.
```

## Compact spin-two use

Choose a compact scalar bump `chi` and two constant two-forms selecting the
`t-x` and `t-y` planes. Their antisymmetry constructs the symmetric current

```text
J(u)=[(u.B_x.partial)^2-(u.B_y.partial)^2]chi.
```

Its divergence vanishes because a symmetric derivative pair contracts an
antisymmetric two-form. The bench chooses an off-shell momentum where `TJ` is
nonzero, so `CJ` is nonzero. It then checks

```text
S=M_2^(-1)J,
C S=0,
M_2 S=J.
```

The generated adapter is therefore necessary for this source; it is not merely
present in an output record.

## Run

```text
node check-generated-source-adapter.mjs
```

The run checks:

- identity-only refusal and exact generation of `M`;
- paired-adjoint and inverse identities for spins `2` through `6`;
- compact spin-two source conservation, nonzero unadapted residual, adapted
  admissibility, and source recovery;
- positive retarded screen contrast and exactly zero advanced response at
  `(t,x)=(2.5,0)`;
- a nonzero `e_x tensor e_x-e_y tensor e_y` future-null shell contrast.

The finite matrices represent invariant natural maps only as regression witnesses.
The construction and current conservation remain coordinate-free; the selected
screen contrast is the named observable component.

## Boundary

The adapter is generated inside the four-dimensional, double-traceless symmetric
carrier grammar with one trace layer. This packet does not generate the Lorentz
metric, prove self-adjointness of the full Euler operator `MD`, produce a new Green
theorem, normalize the one-particle state, or transfer to the Clifford grammar.
For one spin-two observable it adds construction cost relative to N4f; its supported
gain is a retained physical-source interface and cross-spin refusal/inverse logic.
