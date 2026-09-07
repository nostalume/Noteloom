# Return-compiler dispositions

Status: the scalar return, observable-indexed instrument, finite Hamiltonian
departure, Gaussian continuum/moment completion, bounded cross-form-factor
transfer, and native Anderson thermal branch are synthesized below

Decision policy: `K-research-1` in
`open-tree-compiler-v1-disposition.md`. Exact in-domain counterexamples dominate;
regression cannot promote transfer, transfer cannot promote leverage, and cost
failure does not weaken mathematical correctness.

## `V_return-1` — single-model return

### Frozen contract and evidence

The domain is a quadratic number-conserving Hamiltonian with one discrete mode,
one compact continuum channel, preparation of the discrete excitation, flat
coupling `v=1`, `e_0=-1/2`, `g=1/4`, and finite-mode budget `256`. It excludes
multiparticle production, loops, infrared dressing, and multichannel phases.

Computation manifest: `ccd4f25342bc03b33a882874b86e6f54454dd9d8`
(`return_bridge.py` blob `cac0f6ac636d3dbd77e6aeccfcb922cc6daa1d6c`,
certificate `290207484e02e39418cbf099bafee27e74f18515`).

- `E-RT-01`: projecting the field Hamiltonian gives `B=gv`,
  `M_B(d omega)=g^2|v|^2d omega`, and the exact Schur return.
- `E-RT-02`: the same measure gives bound pole `-0.5637634916846831`, residue
  `0.9337988784207747`, pole residual `3.05e-14`, and elastic unitarity residual
  `2.22e-16`.
- `E-RT-03`: direct arrowhead inversion and reduced return differ by
  `3.14e-16` at `N=256`; continuum error falls from `2.979e-4` at `N=16` to
  `1.162e-6` at `N=256`.
- `E-RT-04`: dense work proxy is `16,975,361` versus `770` reduced operations,
  but the competent Schur baseline also costs `770`; invalid coupling, budget,
  and pole brackets are refused.

| Dimension | Domain map | Disposition |
| --- | --- | --- |
| visible return and bound/open recovery | `D+`: frozen one-channel field model | supported |
| finite-mode reconstruction and unitarity | `D+`: declared family/elastic channel | supported |
| leverage over dense inversion | `D+`: same projected result | baseline-naive |
| leverage over expert Schur route | `D-`: identical operation | rejected |
| interacting or multichannel composition | `D?`: outside frozen domain | underdetermined |

Synthesis trigger was decisive completion of the analytic, finite-mode, unitarity,
refusal, and cost benches on 2026-09-06. There is no live `Dx`. The result is a
semantic bound/open bridge, not a new rank-one algorithm.

## `V_instrument-1` — observable-indexed visible return

### Frozen contract and evidence

Given finite `B:P->Q`, channel effects, an optional detector partition, and a
resource budget, retain `Phi_B(A)=B^dagger A B` and generate inclusive and channel
returns, positivity/additivity certificates, `B R_P B^dagger`, and cyclic support.
The contract does not generate `B`, a continuum algebra, or a scattering theorem.

Computation blobs: `instrument.py`
`9f6e9f2c91626a8925730cbeb8d039b94fbfa0a0`; certificate
`c43520f8979a23b8b548649a59734a1abdf63831`.

- `E-VI-01`: normalized rays `B_+` and `B_-` have the same `B^dagger B` and
  coordinate returns, but a coherent effect gives `1` and `0`. This exact seed
  rejects scalar-measure universality but cannot establish transfer.
- `E-VI-02`: an unchanged post-freeze `P=C^2`, `Q=C^3` compiler recovers the
  inclusive return, two additive cells, coherent return, and open kernel exactly.
- `E-VI-03`: compressed effects are positive, partition residual is zero, and
  cyclic rank is three. Non-Hermitian, nonpositive, above-identity, unavailable,
  mismatched, incomplete-partition, and budget requests are refused. Full cyclic
  rank is an honest no-compression verdict on that algebra.

| Dimension | Domain map | Disposition |
| --- | --- | --- |
| scalar-measure universality | `D-`: coherent two-channel counterexample | rejected |
| visible-map, positivity, and partition recovery | `D+`: finite exact `2 -> 3` bench | supported |
| open-kernel reconstruction | `D+`: matching finite retained resolvent | supported |
| cyclic semantic quotient | `D+`: declared finite effect generators | supported, relative |
| action generation, continuum transfer, and leverage | `D?`: absent consumers | underdetermined |

Synthesis was triggered by completion of the frozen independent bench and refusal
classes on 2026-09-06. There is no live `Dx`. `M_B` survives as the inclusive
restriction of `Phi_B`, not as a universal open object.

## `V_departure-1` — Hamiltonian interaction departure

### Frozen contract and evidence

`C_departure-v1` applies linear normal-ordered creation or annihilation vertices to
a finite matter--boson preparation, projects into declared channels, and returns
`B=Q V_+ J`, Bose factors, term provenance, closure, and resource receipt. Couplings
and matter transitions are supplied dynamics; occupation action, aggregation,
projection, and closure are generated. Continua, gauge/fermion relations,
renormalization, and asymptotic scattering are excluded.

Computation blobs: `departure.py`
`baa698d73074130e96a868c1cabbde166d076bb6`; certificate
`1a8a4b7f28776c280b68864f4897b18d84f902a9`.

- `E-DP-01`: node 19 retains an unsquared vertex but its detector fails descent;
  node 29 has a physical open amplitude but no common Hamiltonian bound sector;
  node 32 has that Hamiltonian but supplies `B`. Their different missing edges
  motivate the candidate and are not transfer evidence.
- `E-DP-02`: five signed vertices acting on two vacuum preparations generate the
  exact rank-two departure in node 34, including phases and term provenance.
- `E-DP-03`: appending this `B` to independently supplied `H_P,H_Q` gives zero
  direct/Schur determinant and resolvent residuals. Two poles lie below threshold;
  direct and compressed detector routes give `2961141300/27086113357` at `z=i`.
- `E-DP-04`: the unchanged occupied-sector bench generates
  `(sqrt(2)g_c,g_a)^T`, supporting transfer of Bose multiplicity.
- `E-DP-05`: truncated channels, duplicate/inconsistent bases, invalid actions or
  modes, empty departure, and insufficient resources produce typed refusals.

| Dimension | Domain map | Disposition |
| --- | --- | --- |
| term action, aggregation, and channel closure | `D+`: finite linear bosonic vertices | supported |
| Bose multiplicity transfer | `D+`: independent occupied-sector bench | supported, finite |
| bound determinant and off-axis detector | `D+`: same finite Hamiltonian | supported |
| existing physical-packet transfer | `D?`: nearby packets miss another obligation | underdetermined |
| continuum/asymptotic transfer and complete cost | `D?`: no adapter or fair comparison | underdetermined |

Planned closure of composition, transfer, and refusal benches triggered synthesis
on 2026-09-06. There is no live `Dx`. The finite semantic composition edge is
closed; the field-theory edge is not.

## Propagation through `V_departure-1`

Nodes 11 and 18 may cite `V_return-1`; node 33 may cite the finite instrument; node
34 may cite finite action-to-return composition. Node 19 cannot inherit detector
support across node 24's counterexample, and `C_open-v1` remains unchanged.

Its re-entry trigger asked whether node 11's neutral scalar radial form factor is
the continuum completion of finite generated departures. `V_radial-1` below records
the resulting disposition; the historical trigger no longer owns the cursor.

## `V_radial-1` — Gaussian continuum completion

### Frozen contract and evidence

`C_radial-v1` integrates the exact shell-weight mass of every radial cell, uses its
square root as the unchanged finite creation coefficient, and only then assigns a
midpoint channel energy. It returns the atomic measure, analytic Gaussian tail,
energy-variation witness, and common bound/open error laws. The contract is limited
to node 11's monotone regulated Gaussian scalar family.

Computation blobs: `models.py`
`5075ad1b18012d88e3f8ee1d060309dd6c6fb14b`; certificate
`bdf41b11dd8c91c687de1d3e66546266fefd4c3b`.

- `E-RD-01`: cell masses generate the finite Fock departure through
  `C_departure-v1`; its norm equals the truncated continuum mass and the analytic
  tail completes the full Gaussian mass.
- `E-RD-02`: at `R=5`, `N=16,32,64`, both actual bound/open transform errors lie
  inside the shared variation-plus-tail law and decrease under refinement.
- `E-RD-03`: a second mass/cutoff/coupling fixture preserves shell normalization;
  this is parameter robustness within one family, not structural transfer.
- `E-RD-04`: nonfinite/nonpositive cutoff, noninteger/nonpositive cell count, zero
  coupling, and insufficient finite-departure budget are refused.
- `E-RD-05`: observed errors decay much faster than the Lipschitz certificates;
  the bounds remain hundreds of times larger and do not yet support efficient
  tolerance selection.

| Dimension | Domain map | Disposition |
| --- | --- | --- |
| shell normalization and finite-action reuse | `D+`: regulated Gaussian radial cells | supported |
| mass and bound/open convergence | `D+`: one frozen refinement family | supported, error-bounded |
| parameter robustness | `D+`: second Gaussian fixture | supported, same family |
| cross-form-factor transfer | `D?`: no independent density family | underdetermined |
| tight accuracy certification | `D-`: current bench relative to observed error | rejected for current bound |
| complete-cost leverage | `D?`: no matched accuracy/work accounting | underdetermined |

Planned closure of convergence, robustness, and refusal benches triggered synthesis
on 2026-09-06. There is no live `Dx`. The result closes the finite-to-continuum
semantic edge for one regulated family, but not the practical accuracy or general
field-theory edges.

The first re-entry alternative is evaluated by `V_radial-moment-1` below. The
remaining transfer route requires a new form-factor family using unchanged shell-
mass and finite-action semantics. Extra midpoint samples cannot alter the verdict.

## `V_radial-moment-1` — moment-preserving radial cells

### Frozen contract and evidence

`C_radial-moment-v1` retains `C_radial-v1`'s exact shell masses and finite Fock
action, replaces midpoint channel energy by the cell's computed first energy
moment, and returns centering-error, centered-second-moment, old Lipschitz, new
Taylor, tail, query, and preprocessing receipts. It uses the pinned SciPy numerical
error model; this is not an interval-arithmetic theorem.

Computation blobs: `models.py`
`7bb5518b4b4e9f6211fbec285628b2849fd2a232`, `measures.py`
`ba37f993b688203f2a439bbe61f69a7fb56c0ae7`, `numeric.py`
`26df39d64c1a6659d0b868b8b94edca6743022b6`; certificate
`0082f95d0cf0dfdd70931b6e610ddc7de34de6fe`.

- `E-RM-01`: computed first moments repair the linear cell residual up to reported
  integration error without changing shell masses or creation coefficients.
- `E-RM-02`: for `N=16,32,64`, one centering/second-moment pair contains both
  bound and open errors. Both certificates fall by factors `0.256` then `0.251`
  and overestimate observed errors by about sevenfold rather than hundreds.
- `E-RM-03`: moment preprocessing costs `42N` evaluations. Against two direct
  75-evaluation transforms at matched reported tolerance, the compiled route first
  wins after 6, 16, and 123 repeated mixed batches for `N=16,32,64` respectively.
- `E-RM-04`: a second Gaussian parameter fixture preserves containment; an
  underflowing cell mass is refused rather than divided by zero.
- `E-RM-05`: the moment-centered resolvent values are less accurate than node 35's
  midpoint values on the frozen fixture. Tight certification therefore does not
  establish uniformly better point approximation.

| Dimension | Domain map | Disposition |
| --- | --- | --- |
| common second-order certificate | `D+`: frozen Gaussian refinement | supported, numerical-error-bounded |
| parameter robustness | `D+`: second Gaussian fixture | supported, same family |
| uniformly better transform values | `D-`: bound-transform regression | rejected |
| single-batch computational leverage | `D-`: preprocessing included | rejected |
| repeated-query leverage | `D+`: declared evaluation model beyond break-even | supported, amortized |
| cross-form-factor transfer | `D?`: no independent density family | underdetermined |

Planned closure of containment, rate, robustness, refusal, and cost benches
triggered synthesis on 2026-09-06. There is no live `Dx`. The generated object is a
reusable moment summary for smooth transforms; it is not a generally superior
quadrature rule. Re-entry requires a structurally different positive form factor,
a downstream repeated-query consumer, or an interval-rigorous error requirement.

## `V_radial-transfer-1` — positive radial adapter transfer

### Frozen contract and evidence

`C_radial-v2` constructs the measure density as `4 pi r^2 |a(r)|^2`, accepts a
monotone energy, threshold, support, provenance, and optional certified interval-
mass operation, and generates cell masses, moment-centered energies, finite Fock
action, common bound/open certificates, and complete evaluation receipts. The
adapter never receives the observable parameters. Its domain is positive isotropic
three-dimensional radial channels with a declared monotone energy and controlled
tail; this is not a generic spectral-measure compiler.

Computation blobs: `radial.py`
`a0c21c2778ef3c45b77ce2f246e4b79f7fe80345`, `models.py`
`3b45914ed08d3abf82c2f6089afa70f48b5e485f`, `numeric.py`
`26df39d64c1a6659d0b868b8b94edca6743022b6`; certificate
`69375207d473d2bd364dfd188348ae7647d1885e`.

- `E-RA-01`: the Gaussian adapter retains its exact mass operation and zero mass-
  integration error while preserving the earlier finite departure and transform
  regressions.
- `E-RA-02`: a post-freeze algebraic-tail amplitude uses the unchanged compiler.
  At `N=16,32,64`, both continuum errors are contained and both certificates
  decrease; the generated departure norm equals its atomic measure mass.
- `E-RA-03`: numerical cell-mass, centering, second-moment, and tail errors all
  enter the same certificate. No Gaussian tail identity enters the common core.
- `E-RA-04`: malformed domains, unbounded thresholds, absent monotonicity
  declarations, invalid tolerances, and unresolved numerical mass return typed
  refusals.
- `E-RA-05`: preprocessing costs `1143,2151,4167` evaluations. Against matched-
  budget direct mixed queries costing `90,120,120`, compiled query costs are
  `32,64,128`; only the first two can amortize, after about 20 and 39 batches.

| Dimension | Domain map | Disposition |
| --- | --- | --- |
| shell/moment/action interface transfer | `D+`: Gaussian and algebraic-tail pair | supported, bounded |
| common bound/open containment | `D+`: below threshold and finite time | supported, numerical-error-bounded |
| analytic mass operation | `D+`: Gaussian; numerical for algebraic tail | adapter-specific |
| single-batch computational leverage | `D-`: complete preprocessing included | rejected |
| repeated-query leverage | `D+`: `N=16,32` beyond stated break-even | supported, conditional |
| arbitrary radial or anisotropic channels | `D?`: outside frozen pair/domain | underdetermined |

Regression, post-freeze structural transfer, refusal, and complete-cost evidence
triggered synthesis on 2026-09-06. There is no live `Dx`. Another isotropic form-
factor refinement cannot promote universality. Re-entry requires a named consumer,
a nonmonotone/multibranch or operator-valued channel construction, or interval-
rigorous error as an actual downstream obligation.

## `V_native-thermal-1` — exact thermal functional boundary

### Frozen contract and evidence

The branch asks whether [the native CAR return compiler](../nodes/49-native-car-return.md)
can also
generate the interacting Anderson thermal functional needed by the same scalar
Green coefficients, below 100 million declared work units. The fixed domain is the
two-impurity-mode, four-bath-mode finite fixture at `beta=2`; continuum,
thermodynamic, real-axis, approximate-time, and other-observable claims are
excluded.

- `E52-native-CAR-reachability-v1`: native CAR words generate the exact rank-30
  commutator module with 294 retained coefficients and 128,000 counted operations.
- `E53-native-dual-closure-v1`: Gibbs differentiation forces right multiplication;
  the commutator module escapes with residual `0.553`, and 31-seed closure crosses
  100 million work units during thermal grade one.
- `E54-trace-Hankel-v1`: identity reachability completes at rank 120 under a relaxed
  diagnostic ceiling, but the 31-output continuation space also has rank 120. It
  recovers all 155 packet coefficients within `8.26e-11` at a cost of 407,361,547.
- `E55-final-Green-faithfulness-v1`: composing the actual resolvent and normalized
  Green consumer lowers ten seed rows to rank four, but their invariant
  continuation closure returns to rank 120. All five final coefficients are
  recovered within `2e-8`.

| Dimension | Domain map | Disposition |
| --- | --- | --- |
| native dynamical algebra generation | `D+`: frozen rank-30 commutator module | supported, exact/error-bounded |
| reuse of that module for the Gibbs state | `D-`: measured right-action escape | rejected |
| packet-relative invariant quotient | `D-`: rank `120/120` | rejected |
| final-Green invariant quotient | `D-`: continuation rank `120` from seed rank `4` | rejected |
| native thermal complete-route leverage | `D-`: 407.4M versus 100M boundary | rejected |
| approximate window or different state/observable primitive | `D?`: outside contract | underdetermined |

The decisive counterexample and horizon triggers are constructed in
[the native thermal boundary](../nodes/53-native-thermal-boundary.md) and synthesize
this disposition on
2026-09-07. There is no live `Dx`: correctness, semantic rank, and cost answer
different claim dimensions consistently. The rank-30 algebra compiler remains a
valid reusable dynamical tool; it does not propagate a thermal-state or
complete-route leverage claim. The native thermal branch is stopped. Re-entry
requires a changed time/accuracy contract, observable algebra, or generated state
primitive capable of changing semantic rank or complete-route cost; faster kernels
for the same exact rank-120 realization do not qualify.
