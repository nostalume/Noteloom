# Off-shell resolution and graph-geometry source contracts

These sources bound nodes 25, 27, and 29: off-shell propagation as a local
resolution, open-line worldline compression, and characteristic endpoint
amputation. The kinetic-defect, subset recurrence, quotient witness, and compiler
ordering are derived inside the nodes.

## Brouder--Duetsch 2007

- Primary source: C. Brouder and M. Duetsch, *Relating on-shell and off-shell
  formalism in perturbative quantum field theory*,
  [arXiv:0710.3040](https://arxiv.org/abs/0710.3040).
- Hypotheses consumed: causal perturbation theory with time-ordered products of
  free scalar, Dirac, or gauge fields.
- Contracted output: multilinearity of the on-shell time-ordered product conflicts
  with the Action Ward identity; an off-shell extension and a section back from
  on-shell fields restore the relation under the paper's hypotheses.
- Research use: supports the claim that off-shell extension carries local
  composability and derivative identities, rather than additional asymptotic
  states.
- Boundary: it does not provide a lower-cost amplitude or graph-integration
  algorithm.

## Macrelli--Sämann--Wolf 2019

- Primary source: T. Macrelli, C. Sämann, and M. Wolf, *Scattering Amplitude
  Recursion Relations in BV Quantisable Theories*,
  [arXiv:1903.05713](https://arxiv.org/abs/1903.05713).
- Hypotheses consumed: a BV-quantizable field theory represented by a cyclic
  `L_infinity` algebra with contraction data.
- Contracted output: the minimal model and its quasi-isomorphism recursively
  generate tree-level scattering amplitudes; the contracting homotopy may contain
  the Feynman propagator.
- Research use: supplies the theorem contract behind node 25's transferred
  physical products and identifies graph recursion as homotopy transfer.
- Boundary: the cited construction does not establish loop-level computational
  leverage or convergence.

## Nützi--Reiterer 2018

- Primary source: A. Nützi and M. Reiterer, *Scattering amplitudes in YM and GR as
  minimal model brackets and their recursive characterization*,
  [arXiv:1812.06454](https://arxiv.org/abs/1812.06454).
- Hypotheses consumed: Yang--Mills or general relativity about Minkowski spacetime
  encoded by the differential-graded structures used in the paper.
- Contracted output: on-shell tree amplitudes are minimal-model brackets;
  propagator homotopies can be chosen to expose factorization, and amplitudes admit
  a residue-based recursive characterization.
- Research use: supports a spin-one/spin-two transfer bench and the possibility of
  replacing graph triangulations by physical residue recursion.
- Boundary: this is a tree-level theorem and does not make arbitrary loop
  integration or bound-state dynamics tractable.

## Bonezzi--Chiaffrino--Diaz-Jaramillo--Hohm 2024

- Primary source: R. Bonezzi, C. Chiaffrino, F. Diaz-Jaramillo, and O. Hohm,
  *Tree-level Scattering Amplitudes via Homotopy Transfer*,
  [arXiv:2312.09306](https://arxiv.org/abs/2312.09306).
- Hypotheses consumed: a cyclic homotopy algebra for the action, finite sums of
  plane waves, and the paper's well-defined inclusion, projection, and homotopy.
- Contracted output: transferred higher brackets generate tree amplitudes, while
  their generalized Jacobi relations imply the associated Ward identities.
- Research use: supports nodes 25 and 27 in identifying transfer trees with the
  action-generated amplitude family and bounds the functional domain of the claim.
- Boundary: the paper explicitly exposes a precise version of the familiar tree
  algorithm; it does not claim lower complete computational cost or worldline
  integration leverage.

## Chuang--Lazarev 2008

- Primary source: J. Chuang and A. Lazarev, *Feynman diagrams and minimal models for
  operadic algebras*, [arXiv:0802.3507](https://arxiv.org/abs/0802.3507).
- Hypotheses consumed: algebras over the relevant cobar construction with the
  Hodge/contraction data required in the paper.
- Contracted output: minimal-model maps are sums over decorated trees; for modular
  operads, trees are replaced by general Feynman graphs.
- Research use: supports the loop-level graph-indexing expectation while preventing
  node 25 from claiming that the tree formula itself proves quantum transfer.
- Boundary: it is an algebraic graph theorem, not an evaluator of physical loop
  integrals or a general BV-renormalization result.

## Chiaffrino--Hassan--Hohm 2024

- Primary source: C. Chiaffrino, N. Hassan, and O. Hohm, *Off-Shell Quantum
  Mechanics as Factorization Algebras on Intervals*,
  [arXiv:2412.06912](https://arxiv.org/abs/2412.06912).
- Hypotheses consumed: the harmonic oscillator and spin-one-half systems treated
  by the paper's BV and factorization-algebra constructions.
- Contracted output: local off-shell observable algebras on intervals are
  quasi-isomorphic to their on-shell counterparts.
- Research use: supplies a controlled example in which off-shell locality and
  on-shell physical equivalence coexist as different presentations.
- Boundary: the result does not extend by citation alone to interacting
  four-dimensional gauge theory.

## Arkani-Hamed--Bai--He--Yan 2017

- Primary source: N. Arkani-Hamed, Y. Bai, S. He, and G. Yan, *Scattering Forms and
  the Positive Geometry of Kinematics, Color and the Worldsheet*,
  [arXiv:1711.09102](https://arxiv.org/abs/1711.09102).
- Hypotheses consumed: the kinematic and theory classes constructed in the paper,
  including the biadjoint scalar associahedron and selected massless theories.
- Contracted output: a canonical differential form on positive geometry encodes
  tree amplitudes; its boundaries realize locality and factorization recursively.
- Research use: supplies a candidate direct physical-boundary generator against
  which graph-indexed transfer can be compared.
- Boundary: the construction is not a universal positive geometry for massive,
  nonplanar, gauge, gravity, loop, bound, or detector observables.

## Runkel--Szőr--Vesga--Weinzierl 2019

- Primary source: R. Runkel, Z. Szőr, J. P. Vesga, and S. Weinzierl, *Integrands
  of loop amplitudes within loop-tree duality*,
  [arXiv:1906.02218](https://arxiv.org/abs/1906.02218).
- Hypotheses consumed: generic perturbative QFT amplitudes with the regularized
  forward limits and on-shell renormalization used in the paper.
- Contracted output: a renormalized loop amplitude is related to phase-space
  integration of regularized multi-forward tree-like objects, with recurrence
  constructions discussed through three loops.
- Research use: provides an on-shell evaluation backend for the same transferred
  quantum object.
- Boundary: forward-limit regularization, modified prescriptions, and UV
  subtraction remain and must be counted.

## Ahmadiniaz et al. 2022

- Primary source: N. Ahmadiniaz et al., *Summing Feynman diagrams in the worldline
  formalism*, [arXiv:2208.06585](https://arxiv.org/abs/2208.06585).
- Hypotheses consumed: the worldline representations and examples treated in the
  paper.
- Contracted output: worldline master integrals combine families of Feynman
  diagrams and can integrate selected insertions before ordinary graphwise
  evaluation.
- Research use: supplies a moduli-integral evaluator that may reduce diagram
  enumeration after physical transfer.
- Boundary: it retains proper-time propagation and does not remove the need for
  physical quotienting or generic multiloop integration.

## Ahmadiniaz--Bashir--Schubert 2015/2016

- Primary source: N. Ahmadiniaz, A. Bashir, and C. Schubert, *Multiphoton
  amplitudes and generalized LKF transformation in Scalar QED*,
  [arXiv:1511.05087](https://arxiv.org/abs/1511.05087); concise conference account
  [arXiv:1609.03034](https://arxiv.org/abs/1609.03034).
- Hypotheses consumed: scalar QED and the paper's worldline representation for
  an open scalar line dressed by `N` plane-wave photons.
- Contracted output: one worldline master formula contains all permuted current
  insertions and contact/seagull contributions; replacing an external polarization
  by its momentum produces a proper-time boundary term.
- Research use: supplies node 27's master-kernel theorem contract and its global
  Ward endpoint law after node 25 shows no four-point term-count advantage. Node 29
  consumes that endpoint law but constructs amputation and ideal membership
  internally.
- Boundary: the master formula does not itself establish that the worktable's
  matching recurrence lowers proper-time integration and observable-recovery cost.

## Bashir et al. 2009

- Primary source: A. Bashir, Y. Concha-Sanchez, R. Delbourgo, and M. E.
  Tejeda-Yeomans, *On the Compton scattering vertex for massive scalar QED*,
  [arXiv:0906.4164](https://arxiv.org/abs/0906.4164).
- Hypotheses consumed: massive scalar QED and the Ward--Fradkin--Green--Takahashi
  relation between its three- and four-point vertices.
- Contracted output: the longitudinal four-point structure is constrained by the
  three-point vertex, while a transverse sector remains dynamical and requires
  separate calculation.
- Research use: bounds node 25's Ward-generated contact coefficient and prevents
  promotion of Ward completion into a claim that gauge symmetry determines the
  full interacting vertex.
- Boundary: the paper's general one-loop transverse construction is outside node
  26's tree and route-cost horizon.

## Borinsky 2020 and Borinsky--Münch--Tellander 2023

- Primary sources: M. Borinsky, *Tropical Monte Carlo quadrature for Feynman
  integrals*, [arXiv:2008.12310](https://arxiv.org/abs/2008.12310); M. Borinsky,
  H. J. Münch, and F. Tellander, *Tropical Feynman integration in the Minkowski
  regime*, [arXiv:2302.08955](https://arxiv.org/abs/2302.08955).
- Hypotheses consumed: algebraic or parametric Feynman integrals with the tame or
  quasi-finite kinematics, contour deformation, and dimensional regulation stated
  by the papers.
- Contracted output: tropical/polyhedral structure yields practical Monte Carlo
  samplers and numerical evaluation methods for high-loop or multiscale parametric
  integrals.
- Research use: supports tropical evaluation of the metric-graph cells constructed
  after quotienting.
- Boundary: the method begins with a supplied Feynman integrand and does not by
  itself produce the gauge quotient or observable.

## Borinsky 2025/2026

- Primary source: M. Borinsky, *Tropicalized quantum field theory and global
  tropical sampling*, [arXiv:2508.14263](https://arxiv.org/abs/2508.14263).
- Hypotheses consumed: the paper's tropicalization of massive scalar field theory
  and metric `k`-regular graph moduli.
- Contracted output: the tropicalized scalar theory obeys a nonlinear recursion;
  its graph-moduli volumes and global sampling normalization can be computed with
  polynomial resource bounds stated in the paper, with a high-loop scalar
  demonstration.
- Research use: supplies the strongest candidate for avoiding graph-by-graph
  sampling after physical transfer.
- Boundary: exact solvability belongs to the tropicalized scalar theory. The paper
  motivates, but does not establish here, polynomial-time exact evaluation of
  general gauge/gravity amplitudes; recovery weights and variance must be measured.

## Supported comparison

The source contracts distinguish three operations:

```text
off-shell/BV resolution
  -> makes local interaction and identities composable;

minimal model or positive boundary recursion
  -> transfers that interaction to physical data;

worldline, loop-tree, or tropical geometry
  -> evaluates or samples the surviving analytic graph/moduli object.
```

Node 25 treats this ordering as a candidate reconstruction. None of the sources
alone establishes the complete compiler or its computational advantage.
