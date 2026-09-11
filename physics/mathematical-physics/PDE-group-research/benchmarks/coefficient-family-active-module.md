# Coefficient-family active-module benchmark

## Evidence identity and request

`E_G18_1` targets the correctness and complete solve-stage cost dimensions of
[`C_G18_v1`](../nodes/coefficient-family-reachable-module.md). It asks whether one
coefficient-family closure preserves the same finite-window complement probability
as repeated pointwise G17 closure, and when its exact construction work crosses
over on the frozen repeated-Pauli workload.

The inputs are multiplicities `m in {2,3}` (ambient dimensions `q in {4,6}`),
window sizes `n in {1,4}`, three exact Hermitian coefficient generators, the same
preparation and effect, and nine repetitions. Multiplicity and window variation
remain inside one Pauli model family: they test robustness and cost, not structural
or physical transfer.

## Operation and shared boundary

G14 projector construction and exact Hamiltonian assembly occur before timing.
Each repetition rotates the order of these three routes:

1. dense full-carrier exponential and complement recovery;
2. pointwise G17 exact Krylov construction, effect compression, and reduced
   exponential at every window point;
3. one G18 coefficient-algebra closure, exact specialization, and reduced
   exponential at every window point.

All routes recover the same norm-weighted finite-window complement probability.
Exact action/solve ledgers and floating wall-clock observations remain separate.

## Exact and numerical witness

| `q` | `n` | pointwise solves | family solves | ratio | active dimensions | family dimension | max probability error |
| ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| 4 | 1 | 3 | 9 | 3.00 | `[3]` | 3 | `2.6021e-18` |
| 4 | 4 | 12 | 9 | 0.75 | `[3,3,3,3]` | 3 | `2.0817e-17` |
| 6 | 1 | 3 | 9 | 3.00 | `[3]` | 3 | `3.2526e-18` |
| 6 | 4 | 12 | 9 | 0.75 | `[3,3,3,3]` | 3 | `5.2042e-18` |

Exact specialization and closure certificates passed. All observed probability
errors are below the existing `1e-11` tolerance. The exact ledger therefore
rejects construction leverage at one point and records a 25% solve reduction at
four points; it does not include the shared reduced exponentials.

## Descriptive timing witness

Times are seconds. Each cell is `median; MAD; [minimum, maximum]` over nine
samples.

| `q` | `n` | route | timing summary |
| ---: | ---: | --- | --- |
| 4 | 1 | dense | `0.000294900; 0.000055500; [0.000225600, 0.000489900]` |
| 4 | 1 | pointwise | `0.002662800; 0.000047500; [0.002615300, 0.002821800]` |
| 4 | 1 | family | `0.006113100; 0.000086100; [0.005977900, 0.006373500]` |
| 4 | 4 | dense | `0.000799000; 0.000095200; [0.000554500, 0.001893900]` |
| 4 | 4 | pointwise | `0.010495200; 0.000097800; [0.010297800, 0.011478100]` |
| 4 | 4 | family | `0.008104800; 0.000073300; [0.007922600, 0.008657500]` |
| 6 | 1 | dense | `0.000804900; 0.000305500; [0.000499400, 0.039398200]` |
| 6 | 1 | pointwise | `0.043105200; 0.018706800; [0.006256100, 0.165374800]` |
| 6 | 1 | family | `0.182884000; 0.098976200; [0.051863700, 0.360351000]` |
| 6 | 4 | dense | `0.011029900; 0.009508900; [0.001521000, 0.047879800]` |
| 6 | 4 | pointwise | `0.249950500; 0.032484700; [0.198015400, 0.504732800]` |
| 6 | 4 | family | `0.130113200; 0.060483600; [0.017158300, 0.341566500]` |

The family/pointwise median ratios were `2.296`, `0.772`, `4.243`, and
`0.521` in table order. At `(q,n)=(4,4)`, every observed family sample was lower
than every pointwise sample. At `(6,4)`, the family had a lower local median but
the ranges overlapped. The one-point family medians were higher; the `q=6` ranges
also overlapped. These are local descriptive observations, not runtime dominance.

## Provenance and reproducibility

- Base worktable revision: `52bfe3184b984b2a02e4866caceb6fc5127ae60c`.
- Benchmark source SHA-256:
  `09B08186492F01DE301CF8EEFDC5481948BD88EE36DC4260C16BFF6E361F9312`.
- `uv.lock` SHA-256:
  `9AB1C8167BDC86F83FB7E88B09C47C410C8815ECD949D9B315901719723AC2C0`.
- Transient JSON SHA-256:
  `03698F09DD1C16A36C366DDD9AA9C6F87E8099B1AD1D982C9418DAA0B974696D`.
- Environment: CPython 3.14.6, NumPy 2.5.2, SciPy 1.18.1,
  `Windows-11-10.0.26200-SP0`, and `time.perf_counter`.
- Command: `benchmark_family(9)` serialized with `json.dumps(..., indent=2)`
  through the locked `uv run` environment. The raw JSON was hashed, transcribed,
  checked, and deleted rather than retained as a second evidence owner.

## Disposition boundary

This reproduced run supports exact same-observable recovery, common dimension
three on the frozen workloads, and the stated exact solve crossover. It supplies
robustness and local cost evidence only. It cannot establish cross-family
transfer, sparse scaling, conditioning, universal runtime gain, PDE-domain lift,
or a variable active module. The synthetic cancellation control remains the
adversarial certificate that pointwise agreement cannot prove family invariance.
