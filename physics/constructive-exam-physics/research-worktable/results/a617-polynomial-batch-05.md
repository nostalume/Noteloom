# A617 finite-polynomial transfer batch

## Result

The previously unexecuted nineteen-problem finite-polynomial queue has now been
run as one locked, page-bound batch. Sixteen problem packets are complete under the
declared physical interpretation; three are partial. Across 44 declared targets,
41 have exact projected relations and three return `target_not_constrained` at the
semantic boundary. Every expected algebraic relation is certified as a consequence
of its supplied physical-law ideal.

This supports transfer of the relation-projection backend after a human constructs
the area-specific law packet. It does **not** support automatic solution from exam
prose, automatic law discovery, physical correctness of an unreviewed law packet,
or reduced exam time.

## Construction under test

The new public operation is

```text
compile_polynomial_problem(
  problem id,
  page,
  named physical laws with provenance,
  target-conditioned law selections,
  retained givens,
  hidden quantities,
  regime and branch obligations
)
  -> per-target projections + complete/partial/refused status.
```

Target-conditioned law selection matters. A four-part problem should not force the
student or algebra kernel to carry every field, energy, and circuit variable into
every subpart. Direct target relations are now admitted without inventing a dummy
hidden variable. Nonzero physical assumptions can be encoded constructively by an
inverse witness, which prevents invalid cancellation while remaining polynomial.

The executable batch and its independent expected relations are in
[polynomial_cases.py](../computation/worktable/polynomial_cases.py). The compiler
itself is in [problem.py](../computation/occ/problem.py).

## Compact results

Here `k=1/(4 pi epsilon_0)`. Signs and square-root choices listed under the branch
column remain physical return obligations rather than decisions made silently by
the elimination backend.

| ID | Status | Projected result | Return boundary |
| --- | --- | --- | --- |
| A25-03 | complete | `tau = 36000000/sqrt(120000^2-1) days`, approximately `300.00000001 days` | positive proper time; 60 GeV treated as total energy and source rest energy is 0.5 MeV |
| A24-09 | complete | `C0=epsilon_0 S/d`; `Cm=epsilon_0 S/(d-l)`; `W=epsilon_0 S U0^2 l/[2(d-l)^2]`; `Cd=epsilon_0 epsilon_r S/[epsilon_r(d-l)+l]` | `0<l<d`; work assumes charging with the metal inserted before disconnecting |
| A22-03 | complete | `a_parallel^2=(F/m)^2(1-beta^2)^3`; `a_perp^2=(F/m)^2(1-beta^2)` | choose the component with the force-component sign |
| A20-03 | complete | `|alpha_AB|/|alpha_BC|=3/4` | identical uniform rods released from rest in the shown 90-degree geometry |
| A19-07 | complete | `E_1s=-13.6 eV`; orbital `L=0`; orbital magnetic moment `0` | the problem is interpreted as orbital rather than spin moment |
| A18-04 | complete | inner sphere `-2Q/5`; shell inner surface `2Q/5`; outer surface `3Q/5`; gap energy `kQ^2/(25a)`; `C=2a/k=8 pi epsilon_0 a` | radial field and potential are returned by the region coefficients below |
| A16-03 | complete | opposite rod velocity `v=u/10` | infinitesimal impulse and mirror-symmetric regular-hexagon response |
| A16-04 | partial | `int(E dot D)/2 = 19kQ^2/(8a)`; `int(epsilon_0 E^2)/2 = 37kQ^2/(16a)` | the compilation does not define how its two Chinese energy labels map to these conventions |
| A15-07 | complete | total helium ionization energy `79.0 eV` | uses hydrogenic `He+` energy `54.4 eV` |
| A15-08 | complete | `lambda=h/sqrt(3m_n k_B T)`, approximately `1.45 angstrom` at 300 K | positive nonrelativistic momentum branch |
| A14-08 | partial | first Balmer-line separation approximately `0.238 nm` with the stated mass approximation | isotope assignment without wavelength measurement is not a polynomial target |
| A13-01 | complete | east bank minus west bank `=2 omega v b sin(A)/g` | steady northern-hemisphere flow and small surface slope |
| A13-02 | complete | `H=[v0^2-(mg/(rho S v0(2-alpha)))^2]/(2g)` | requires nonnegative impact speed and height |
| A13-06 | complete | `J_conduction,rms/J_displacement,rms=sigma/(epsilon omega)` | nonzero single-frequency field amplitude |
| A13-09 | complete | `B=3hc(1/lambda_2-1/lambda_1)/(7 mu_B)`, approximately `15.78 T` | weak-field Landé factors `4/3` and `2/3`; positivity selects the crossing field |
| A11-03 | complete | meeting distance `270 m`; ground-frame time `9.0e-7 s` | ground inertial frame and `c=3e8 m/s` |
| A11-07 | partial | reduced-mass ratio `201.292`; binding magnitude approximately `10.95 keV`; muon radius approximately `0.002484 a0 = 1.31e-13 m`; electron radius approximately `a0` | the probability curve and chemical analogy require a non-polynomial semantic return |
| A10-01 | complete | cabin magnitude `3m2 g/[2(m1+m2)]`; ground components are obtained by adding the elevator's `g/2` upward acceleration | vector directions remain in the return ledger |
| A10-03 | complete | each ruler measures the other as `8l0/17` | positive length branch after relative speed `15c/17` |

For A18-04 the complete piecewise return is

```text
E(r) = 0                              r<a,
     = -2kQ/(5r^2) r_hat              a<r<2a,
     = 0                              2a<r<3a,
     = 3kQ/(5r^2) r_hat               r>3a;

V(r) = 0                              r<a,
     = -2kQ/(5r)+2kQ/(5a)             a<r<2a,
     = kQ/(5a)                        2a<r<3a,
     = 3kQ/(5r)                       r>3a.
```

The compiler eliminates the region coefficients; spherical Gauss-law shapes are a
named domain-adapter theorem contract. Potential continuity and the correct normal
field jumps at `a`, `2a`, and `3a` are the return witnesses.

For A16-03, the domain adapter reduces the symmetric linkage velocities to the two
opposite horizontal-edge velocities `u` and `v`. Substituting the edge constraints
into the six uniform-rod kinetic energies gives

```text
T = m(5u^2-uv+5v^2)/3.
```

The impulse acts only on the `u` coordinate, so the conjugate impulse for `v`
vanishes:

```text
p_v = partial T / partial v = m(-u+10v)/3 = 0,
```

which produces `v=u/10`. This is a useful example of the intended separation: the
linkage geometry is area-specific, while target-conditioned elimination of the
latent momentum is general.

## What the batch establishes

- The exact backend transfers across mechanics, relativity, electrostatics,
  response theory, and elementary atomic/spectral algebra without problem-ID rules
  in the compiler.
- A problem can expose many targets while each subpart selects only its necessary
  laws. This is a concrete exam-complexity operation, not merely a shared notation.
- Partial status is compositional: 41 successful targets are retained without
  converting three semantic gaps into false algebraic answers.
- The locked polynomial batch contributed 17 full packet executions, 3 partial
  packet executions, and 3 shape-only executions. Result 12 subsequently promotes
  A15-01 through the separate event constructor, and Result 13 promotes A14-06 and
  A10-06 through the path-functional constructor, so the current corpus totals are
  20 full, 3 partial, 3 shape-only, 21 unexecuted candidates, 75 outside the
  grammar, and 4 qualitative problems.

## What remains open

The largest unresolved issue is still construction of the physical packet. The
current tool starts after a human has chosen conservation laws, symmetry reduction,
constitutive laws, or coupling rules. The batch proves that projection is reusable;
it does not prove that relation selection is faster than a competent conventional
solution. No baseline action counts are reported because complete handwritten
routes have not yet been independently locked.

The next corpus-forced constructor is the event-branch compiler. Fifteen indexed
problems explicitly require it and 23 belong to the broader event/invariant family.
Its benchmark must construct event predicates and branch filters rather than accept
them as prose obligations.

## Reproduction

From `computation/` run:

```text
uv run python -m worktable polynomial-batch
uv run --with sympy==1.14.0 python -m unittest discover -s tests -v
```

The first command reports `19/19` packet certificates. The second includes locked
tests for exact queue identity, 16 complete and 3 partial packets, 41 constrained
and 3 underdetermined targets, multi-target compilation, law selection, direct
relations, and the earlier regression/refusal cases.

## Source and limitations

All relevant PDF pages were rendered and visually inspected for this batch: 4, 7,
10, 15, 19, 21, 23, 24, 26, 28, 29, 30, 33, 34, and 35. The source remains the
36-page local compilation with SHA-256
`B84E9D24468628433D1A126771DC8DE5A9D3CA7C2DBD01A78597FDDF01C8D764`.
It is a community compilation without an official answer key. Therefore these are
internally checked derivations from visually read statements, not claims of
agreement with official marking guidance.
