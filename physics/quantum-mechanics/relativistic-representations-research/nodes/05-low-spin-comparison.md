# N5 — Low-Spin Comparison as a Recovery Test

Status: supported bounded synthesis for spins `0,1/2,1,3/2,2`; N10j upgrades the
massless integer-spin potential/curvature comparison to a polynomial forward map
and physical-shell isomorphism, while conventional massive spin-`3/2` and spin-`2`
carrier equivalences remain open
Consumes: [N3 realization bridge](03-realization-bridge.md),
[N3a massive spin one](03a-massive-spin-one.md),
[N3b massless helicity one](03b-massless-helicity-one.md),
[N4 local symbols](04-local-symbol-extension.md),
[N4a bosonic potentials](04a-polynomial-complex-details.md),
[N4b fermionic potentials](04b-half-integer-potential.md), and
[N4o massive Dirac construction](04o-dirac-coulomb-local-graph.md), with the
[N10j curvature generator](10j-generated-curvature-compatibility.md) as a later
revision of the integer-spin comparison
Produces: the bounded comparison contract and the supported input for manuscript
Section 7

## Research contract

- **Question/capability:** when two familiar low-spin equations are said to
  describe the same particle, which equality has actually been constructed?
- **Presumptions:** four-dimensional Minkowski spacetime, proper orthochronous
  Poincare spin cover, free constant-coefficient systems, positive-energy massive
  or nonzero-null orbit, and only the carrier families already constructed by the
  incoming nodes.
- **Invariant target:** the standard-momentum physical little-group fiber and its
  orbitwise induced Poincare representation.
- **Construction:** specialize the universal symbols at low rank; compare two
  realizations only through an explicit map of kernels/cohomology or through their
  already-constructed isomorphisms with the same physical fiber.
- **Internal benchmark:** classify spins `0,1/2,1,3/2,2` by the strongest supported
  coincidence—same equation, local physical-cohomology map, or only orbitwise
  representation equivalence—and name every additional presumption.
- **Boundary:** no component elimination, massive Rarita--Schwinger theorem,
  massive Fierz--Pauli theorem, interaction equivalence, or uniqueness/minimality
  theorem is supplied here.

## 1. Comparison means an induced map on physical fibers

For two symbol complexes at one standard momentum,

```text
G --R(k)--> F --D(k)--> T,
G'--R'(k)-> F'--D'(k)-> T',
```

a carrier map `L_k:F->F'` compares physical content only after the two tests

```text
L_k(ker D(k)) subset ker D'(k),
L_k(im R(k)) subset im R'(k).
```

They construct

```text
bar L_k:ker D(k)/im R(k) -> ker D'(k)/im R'(k).
```

If `bar L_k` is a little-group isomorphism, N3 transports it over the orbit and
the two solution spaces carry the same induced one-particle representation. This
does **not** by itself prove that `L(p)` is polynomial, has a local inverse, preserves
an action, or survives coupling.

When a direct `L_k` has not been constructed, suppose instead that incoming nodes
give little-group isomorphisms

```text
j:H(k) ~= V_sigma,
j':H'(k) ~= V_sigma.
```

Then

```text
bar L_k=(j')^(-1)j
```

is an orbitwise physical-fiber equivalence. Its dependence on the choices in
`j,j'` records why representation equivalence is weaker than local-complex
equivalence.

## 2. Spin zero

For the scalar carrier `C`, both the massive and massless symbols are evaluations
of the same invariant polynomial:

```text
D_m(p)=p^2-m^2,
D_0(p)=p^2.
```

At a standard momentum on the selected shell their kernels are `C`, on which the
little group acts trivially. There is no gauge image. Hence they realize massive
spin zero or massless helicity zero directly. A real scalar condition and a choice
of action are additional structures; the complex representation alone supplies
neither.

## 3. Spin one half

### Massless

The direct chiral maps are the two off-diagonal blocks of the Clifford action:

```text
c_p:S->bar S,
bar c_p:bar S->S,
slash p=gamma(p)=matrix(0,bar c_p;c_p,0)
  on Delta=S direct-sum bar S.
```

Therefore evaluation on the same pair gives

```text
ker(slash k)=ker c_k direct-sum ker bar c_k.
```

N4 identifies the two summands as the chiral helicity lines, and N4b identifies
the left side as its `n=0` physical fiber. Thus the parity-paired massless Dirac
carrier is exactly the direct sum of the two Weyl realizations; there is no gauge
map at this rank. A single Weyl sector and the paired system are not the same
parity or reality choice.

### Massive

The direct chiral baseline is `(p^2-m^2)I_S`. N4o constructs the additional
chirality-paired first-order operator

```text
D_m^Dir(p)=slash p-m,
(slash p+m)D_m^Dir(p)=(p^2-m^2)I_Delta.
```

For `k=m tau`, let `B_tau=gamma(tau)` and
`Pi_tau^+=(I+B_tau)/2`. Then

```text
ker D_m^Dir(k)=im Pi_tau^+ ~= V_(1/2).
```

The direct chiral rest carrier is also `V_(1/2)`, so the common-fiber composite of
Section 1 proves orbitwise one-particle equivalence. The first-order factorization,
chirality pair, scalar mass coupling, invariant Dirac pairing, and any disconnected
parity action are additional inputs, not consequences of the spin label.

## 4. Spin one

### Massive

The direct chiral baseline is `(p^2-m^2)I_(Sym^2 S)`. N3a constructs the vector
symbol

```text
K_Proca(p)A=(m^2-p^2)A+p(p dot A),
p dot K_Proca(p)A=m^2(p dot A).
```

At `k=(m,0,0,0)`,

```text
ker K_Proca(k)=k^perp ~= V_1.
```

Both carriers therefore produce the same massive induced representation through
their maps from `V_1`. The resulting orbitwise equivalence is not a proved local
field redefinition between the chiral and Proca equations. The vector carrier,
transversality constraint, parity-even second-order ansatz, minimal degree, and
absence of an extra longitudinal characteristic are Proca-side presumptions.

### Massless

The `s=1` bosonic potential machine is Maxwell:

```text
R(p)alpha=p alpha,
K_Max(p)A=i_p(p wedge A)=p^2A-p(p dot A).
```

N3b constructs the curvature map on the same potential class,

```text
bar d_p:ker K_Max(p)/im R(p) -> wedge^2 V_C,
bar d_p[A]=p wedge A.
```

At nonzero null `p`, contraction with any `n` satisfying `n dot p=1` constructs its
inverse on closed and coclosed curvatures:

```text
F=p wedge(i_n F).
```

Thus potential and curvature are locally related on the physical shell. Hodge
duality splits the curvature into the two direct chiral helicity lines. Gauge
redundancy belongs to the potential route; choosing one duality sector, a real
field, parity pairing, global topology, or an action adds further information.

## 5. Spins three halves and two

For massless spin `3/2`, specialize the fermionic potential complex at `n=1`:

```text
ker S_1(k)/im R_1(k)
 ~=H_1(Q_k,W_k)
 ~=C_(+3/2) direct-sum C_(-3/2).
```

For massless spin `2`, specialize the bosonic potential complex at `s=2`:

```text
ker D_2(k)/im R_2(k)
 ~=Sym_0^2(Q_k tensor C)^*
 ~=C_(+2) direct-sum C_(-2).
```

The direct chiral curvature systems at `h=3/2` and `h=2`, together with their
conjugates, have the same two character lines. The common-fiber construction in
Section 1 therefore gives orbitwise representation equivalences.

N10j now strengthens the integer-spin statement. For every `s>=1`, it generates a
degree-`s` polynomial map from the symmetric potential to the paired chiral
curvature, proves that it kills the gradient gauge image, and computes that its
two screen endpoint lines map nontrivially to the two direct chiral kernels. Thus
spin two has a physical-shell potential/curvature isomorphism, not merely a
common-fiber comparison. Momentum homogeneity simultaneously proves that its
inverse cannot be a nonnegative-degree polynomial local operator. The half-integer
spin-`3/2` local curvature map remains open.

The `n=1` vector-spinor complex may be called the massless symmetric
Rarita--Schwinger/Fang--Fronsdal branch, and the `s=2` symmetric tensor complex the
massless metric-potential branch, only within the displayed constraints and gauge
maps. Conventional massive Rarita--Schwinger and Fierz--Pauli carriers are not
outputs of N4 and are not comparison theorems of this node.

## 6. Bounded verdict

| Spin | Strongest supported comparison | Additional input exposed |
| --- | --- | --- |
| `0` | direct scalar realization | reality and action |
| `1/2` | massless blockwise identity; massive orbitwise equivalence after Dirac factorization | chirality pairing, first order, mass coupling, parity |
| `1` | Maxwell potential/curvature physical-shell isomorphism; Proca/chiral orbitwise equivalence | gauge or vector carrier, duality/reality, minimality conditions |
| `3/2` | massless common-fiber orbitwise equivalence | vector-spinor potential, gamma constraints, gauge; local curvature map open |
| `2` | degree-two polynomial forward curvature map and physical-shell isomorphism | metric potential, trace constraints, gauge; polynomial local inverse obstructed |

The low-spin cases validate the universal physical fibers and expose presumption
debt. They do not select a unique equation. This is the stopping benchmark:
developing component formulae or massive conventional systems would not change the
paper's supported representation-recovery theorem and requires a separate node.

## Edges

- `N4/N3a/N3b/N4o -> N5`: supported low-spin symbols and fiber maps construct the
  bounded comparison.
- `N5 -> manuscript Section 7`: only the comparison levels and extra presumptions
  are promoted.
- `N5 -> N7`: the failure to upgrade most common-fiber maps to local action
  equivalences supplies the equivalence hierarchy and stop boundary.
- `N5 -> N10j`: pass the common-fiber-only integer-spin boundary; N10j owns the
  generated strengthening, while this table is updated as its compact synopsis.
