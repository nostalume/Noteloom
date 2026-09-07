# Relativistic field computation workbench

This directory contains the executable part of the representation-to-observable
research graph. Conceptual derivations live in `../nodes/`; this package retains
only operations reused across nodes and compact behavioral certificates.

## Environment and verification

The project uses uv-managed CPython 3.13 with two direct mathematical
dependencies: SymPy for exact algebra and SciPy for numerical integration.

```powershell
uv sync --locked
uv run --locked python -m unittest discover -s tests
```

`uv.lock` fixes transitive versions. `.venv`, bytecode, raw traces, and generated
plots are never research artifacts.

## Ownership

- `fieldcalc.rewrite`: bounded semantic word rules, budgets, and refusals;
- `fieldcalc.exact`: exact-domain rank/kernel certificates;
- `fieldcalc.grammar`: operations, dimension-compatible trace reversal, scalar
  metric jets, and polarized momentum vertices generated from carrier laws and
  action data;
- `fieldcalc.residual`: obstruction-driven exact repair, Ward lifts, observable
  descent, source adapters, and cost verdicts;
- `fieldcalc.lowering`: invariant two-point numerators, denominator quotients,
  integral sectors, reconstruction certificates, and bounded refusals;
- `fieldcalc.spectral`: subtracted massive--massless bubble boundaries, continuum
  densities, shell diagnostics, finite-resolution effects, and refusals;
- `fieldcalc.worldline`: scalar-line matching quotients, chamber recovery counts,
  budgeted multilinear kernels, and exact Euclidean subset transfer;
- `fieldcalc.amplitude`: scalar-Compton shell generation, endpoint-amputated
  scalar-QED transfer, Ward ideal certificates, and complete route costs;
- `fieldcalc.clifford`: abstract Clifford words and recurrence/Pfaffian traces;
- `fieldcalc.exterior`: bounded exterior-grade quotient, products, and certificates;
- `fieldcalc.fermion`: projected fermionic Ward transfer, positive event effects,
  selectable trace baselines, and complete cost receipts;
- `fieldcalc.fermion_line`: exterior-valued subset transfer, ordered-history
  recovery, endpoint Ward identities, budgets, and complete product counts;
- `fieldcalc.multiphoton`: shell-generated three-photon slices, projected fermion
  effects, outgoing-arm exchange, soft boundaries, and route-cost receipts;
- `fieldcalc.soft_channel`: endpoint factorization and leading-soft
  virtual/unresolved/resolved detector-bin transfer with completion boundaries;
- `fieldcalc.return_bridge`: one-channel visible returns shared by a bound pole and
  an elastic continuum channel, with direct/Schur comparison and cost receipts;
- `fieldcalc.instrument`: exact departure-map compression into inclusive,
  detector-indexed, open-kernel, and cyclic-support outputs with typed refusals;
- `fieldcalc.departure`: finite matter--boson action terms applied to Fock
  preparations, preserving Bose multiplicity, phases, channel closure, and budgets;
- `fieldcalc.pfaffian`: skew elimination with update and pivot-condition receipts;
- `fieldcalc.numeric`: validated SciPy quadrature requests with value, error, and
  evaluation receipts shared by retained numerical constructions;
- `fieldcalc.radial`: positive radial channel adapters, shell/moment compilation,
  finite action, common transform certificates, and complete numerical receipts;
- `fieldcalc.impurity`: CAR-generated finite Anderson systems, quadratic-bath
  returns, block-Dyson coefficients, and independent full-Hilbert recovery;
- `fieldcalc.impurity_expansion`: action-factored determinant Green coefficients,
  ordered-simplex costs, and resource refusal;
- `fieldcalc.pauli_fierz`: kinetic-square interaction generation, regulated
  matter--photon returns, second-order history recovery, and bound/open receipts;
- `fieldcalc.return_reduction`: observable-cyclic return projection in Euclidean or
  state-generated positive metrics, moment and off-axis residual certificates,
  fair cached-query costs, and finite Pauli--Fierz/thermal-Anderson adapters;
- `fieldcalc.moment_return`: scalar correlation-functional moments, Stieltjes/Jacobi
  return generation, residual certificates, and a two-thermal-action Anderson
  adapter that does not form density or transition matrices;
- `fieldcalc.perturbative_return`: coefficient-valued endpoint correlation
  functionals, resolvent and moment recurrences, rank-defect diagnostics, and the
  finite Anderson time-quadrature comparison;
- `fieldcalc.graded_return`: interaction-valued free spectral closure, graded
  reachable modules, reduced multi-frequency recurrences, closure certificates,
  complete break-even costs, and bounded refusals;
- `fieldcalc.path_functional`: deterministic closed interaction-path contractions
  for scalar graded-functional ports, paired quadrature evidence, costs, and
  bounded refusals without endpoint coefficient matrices;
- `fieldcalc.operator_factorization`: selective local--bath rank factorization of
  generated graded carriers and observable insertions, recovery/stability audits,
  functional regression, and factor-budget refusals;
- `fieldcalc.car_words`: charge-adapted normal-ordered CAR decomposition of only
  retained bath factors, with tolerance, reconstruction, and word-budget receipts;
- `fieldcalc.gaussian_functional`: endpoint-extended thermal Wick/Pfaffian
  construction, word-native Anderson functional evaluation, sharing/cost receipts,
  and bounded refusals;
- `fieldcalc.native_car`: normal-ordered CAR multiplication, internally generated
  trace metric, and local-operator/CAR-word graded reachability with reusable
  reduced actions and support/cost certificates;
- `fieldcalc.native_dual`: right-Hamiltonian/action closure seeded by requested
  native insertions, with consumable block-action output on success and partial
  rank/support receipts on bounded refusal;
- `fieldcalc.native_hankel`: identity-reachable native thermal prefixes,
  reusable behavioral-observability closure, quotient actions, grade-resolved
  packet evaluation, and explicit rank/resource rejection when either a packet or
  composed consumer is faithful;
- `fieldcalc.models`: admitted benchmark parameters and the Gaussian analytic-mass
  adapter used by retained scalar fixtures;
- `fieldcalc.measures`: visible measures, positive prepared-event effects,
  phase-space pushforwards, conditional apertures, and errors.

A tool may be imported by a test; a tool never imports a test. A probe is deleted
after its conclusion is promoted. A retained certificate checks a semantic law,
not stdout text or a private helper call.

Exact test-only matrix models may certify a typed map identity such as a gauge
projector law. They do not replace the invariant derivation and are not promoted to
production helpers unless a second node needs to generate the same object.

## Flow

```text
carrier/model request
  -> typed admission
  -> project semantic grammar or measure construction
  -> SymPy exact solve or SciPy value/error transform
  -> generated object or structured refusal
  -> certificate consumed by a surviving node
```

The package is private research infrastructure. It does not promise a public API,
arbitrary tensor algebra, carrier-global discovery, or a generic spectral solver.
