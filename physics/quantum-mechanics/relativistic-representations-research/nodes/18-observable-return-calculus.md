# Observable-return calculus across mechanics and fields

Status: exact projection, memory, and perturbative refinement are supported under
their declared domains

## Obstruction

An operation algebra does not describe repeated dynamics; a graph enumerator does
not know which compositions are physical or which observable they serve. Their
common object must be constructed from a prepared return request.

## Construct the return

Supply

```text
A = typed physical operations and relations,
L = dynamical generator on X,
P = retained preparation/observable sector,
O = readout on PX,
Q = 1-P.
```

The four blocks are

```text
L_P=PLP,  L_Q=QLQ,  B=QLP,  C=PLQ.
```

Writing `(z-L)(u+v)=eta` with `u in PX`, `v in QX` gives

```text
(z-L_P)u-Cv=eta,
-Bu+(z-L_Q)v=0.
```

When `R_Q(z)=(z-L_Q)^(-1)` exists, the second equation constructs
`v=R_Q(z)Bu`; substitution into the first yields

```text
Sigma_P(z)=CR_Q(z)B,
P(z-L)^(-1)P=[z-L_P-Sigma_P(z)]^(-1)P.
```

The same decomposition in time gives

```text
v(t)=exp(tL_Q)v(0)
 +integral_0^t exp((t-s)L_Q)Bu(s)ds,

dot u(t)=L_Pu(t)+Cexp(tL_Q)v(0)
 +integral_0^t K_P(t-s)u(s)ds,

K_P(t)=Cexp(tL_Q)B.
```

For self-adjoint unresolved dynamics and `C=B^dagger`, the spectral theorem
constructs the single datum

```text
M_B(Delta)=B^dagger E_(H_Q)(Delta)B,
Sigma_P(z)=integral (z-lambda)^(-1)dM_B(lambda),
K_P(t)=integral exp(-itlambda)dM_B(lambda).
```

Resolvent, memory, and continuum descriptions are therefore transforms of the
same return, not analogies between mechanics and fields.

## Generate perturbative graphs from it

Let `L=L_0+gV` with `QL_0P=PL_0Q=0`. Then

```text
B=gB_1,  C=gC_1,
L_Q=L_(Q,0)+gW,

R_Q(z)=sum_(n>=0)g^n(R_0W)^nR_0,

Sigma_P(z)=sum_(n>=0)g^(n+2)C_1(R_0W)^nR_0B_1.
```

Each term has the generated excursion shape

```text
P -> B_1 -> Q -> R_0 -> (W -> R_0)^n -> C_1 -> P.
```

The algebra/diagram factorization is

```text
Alg(A) -> colors, generators, grading, relations, normal forms;
Diag(Alg(A)) -> typed contraction diagrams modulo isomorphism/relations;
Ev_R:Diag(Alg(A))->End(X_R).
```

Correct normalization means `Ev_R(Normalize(D))=Ev_R(D)`. Different mechanical,
field, or collective realizations may share this construction while retaining
different state spaces, analytic boundaries, and costs.

## Retained interface and boundary

```text
ObservableReturn(A,L,P,O,budget)
 -> irreducible excursions + resolvent/memory/measure representations
    + realization-specific evaluator and cost
 | refusal(no domain, no closure, or no gain).
```

This calculus unifies a semantic operation, not entire theories. It neither finds
`L`, selects `P/O`, nor makes `R_Q` cheap. [Node 17](17-algebra-graph-compiler-bridge.md)
generates the field-port refinement; [node 11](11-visible-spectral-measure.md)
certifies outputs from the retained measure.

[Node 32](32-single-model-return-bridge.md) realizes this return on one exact field
sector and recovers both its bound pole and elastic channel. The same construction
is also the expert Schur baseline, so the result certifies semantic unity rather
than a new computational advantage.
