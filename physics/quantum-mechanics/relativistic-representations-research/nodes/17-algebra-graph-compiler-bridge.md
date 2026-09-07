# Algebra-to-graph compiler bridge

Status: typed tree generation and quotienting are supported; the one-channel
spin-two regression establishes connection but not computational leverage

## Obstruction

The free algebra compiler produces local operations, not perturbative histories.
A useful bridge must generate vertices, contractions, graph weights, and grading
from those operations rather than receive a textbook diagram list.

## Retained compiler datum

```text
CompiledFieldDatum={
  field colors, duals, and parity;
  physical quotient;
  certified Green pairing;
  interaction-generated local vertex maps;
  contraction normal form, selection rules, provenance
}.
```

A vertex is a typed multilinear map

```text
v:X_(c_1) tensor ... tensor X_(c_r)->C.
```

The compiler separately tracks algebra depth, coupling degree, and loop degree
`E-V+C`. For a fixed multiset of vertices, the relabelling group

```text
G_n=product_v (Aut(v)^(n_v) semidirect S_(n_v))
```

acts on contraction histories. The physical graph is the orbit
`Gamma=G_n dot h`. Orbit--stabilizer then constructs its weight:

```text
1/|G_n| sum_(h' in G_n dot h) Ev(h')
 =Ev(h)/|Stab_(G_n)(h)|
 =Ev(Gamma)/|Aut_ext(Gamma)|.
```

Odd transpositions contribute `chi(h)=(-1)^(number of odd transpositions)`, so
fermionic signs arise from the graded action rather than a diagram annotation.

## Connect to the observable return

For `H(g)=H_0+gV`, assume `QH_0P=0` and `PVP=0`. Then

```text
B(g)=QH(g)P=gB^(1),

Sigma^(2)(z)
 =g^2(B^(1))^dagger(z-QH_0Q)^(-1)B^(1),

M^(2)(Delta)
 =g^2(B^(1))^dagger E_(QH_0Q)(Delta)B^(1).
```

Thus the algebra-to-graph output refines the same projected return and visible
measure as nodes 18 and 11; it does not create a new observable.

## Generated spin-two regression

For on-shell scalars `E(p)=Q_p-m^2=0`, `q=p'-p`, and `s=<p,p'>`, the naive
symmetric product has divergence

```text
A_q[P_p P_(p')1]=(s-m^2)P_q.
```

Since `A_q[U(s-m^2)]=2(s-m^2)P_q`, residual cancellation generates

```text
J_0(p',p)=P_pP_(p')1-U(s-m^2)/2,
A_qJ_0=0.
```

The grammar also exposes the conserved improvement

```text
I_q=P_q^2-UQ_q,
J_xi=J_0+xi I_q,
A_qJ_xi=0.
```

Two typed scalar--scalar--spin-two vertices generate the three pair orbits

```text
{{1,2},{3,4}}, {{1,3},{2,4}}, {{1,4},{2,3}},
```

and hence

```text
A_4^(2)=g_2^2 sum_pairings
 <J_xi(p_j,p_i),G_Q M_2^(-1)J_xi(p_l,p_k)>.
```

At the declared right-angle massive transfer,

```text
<J_13,J_24>=53/16,
TJ_13=TJ_24=3/2,
N_alg=53/16-(1/4)(3/2)^2=11/4,
A_t^(2)/g_2^2=-11/2.
```

The component de Donder baseline gives `N_dD=11/2`; the relation
`N_alg=N_dD/2` is exactly the declared symmetric-pairing normalization. This is a
regression certificate, not an efficiency win. A curvature-visible current was
also rejected as a discriminator because trace reversal acts trivially after the
curvature annihilates gauge and trace layers.

## Retained interface and boundary

```text
CompileGraphs(field datum, interaction, observable, order, budget)
 -> typed graph orbits + weights/signs + normalized fiber contractions
    + observable-return target + construction cost
 | refusal(missing jet, incompatible ports, or budget).
```

The bridge replaces remembered diagrams by generated orbits, but this four-point
bench has the same three channels as the expert baseline. [Node 19](19-off-shell-graph-completion.md)
tests the stronger off-shell obstruction where isolated tree conservation is
insufficient. [Node 38](38-graph-independent-interaction-return.md) consumes this
result but revises its ontology: graph generation becomes an optional recovery
map from an interaction-return class rather than the framework endpoint.
