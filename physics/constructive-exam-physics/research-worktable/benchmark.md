# Observable Reduction Benchmark

## Contract metadata

| Field | Frozen value |
| --- | --- |
| tabulated case rows | 175 uniquely named cases |
| active research tests | 189 tests at the consolidation baseline |
| retained adapter tests | 18 tests at the consolidation baseline |
| consolidation conformance tests | 4 direct-flow and import-isolation tests |
| A617 source SHA-256 | `B84E9D24468628433D1A126771DC8DE5A9D3CA7C2DBD01A78597FDDF01C8D764` |
| `uv.lock` SHA-256 | `3A464A3DBD4312589486B99C723987E647E490415E85210CF0152F0C04FA1D1D` |
| evidence cutoff | 2026-09-11; checked-in evidence only |

Counts describe this frozen benchmark contract; they are metadata, not part of
the benchmark name and not a claim of corpus-wide or human validity.

## Capability under test

Given one human-validated semantic problem request, select its admitted construction
owner and preserve that owner's exact result, certificates, provenance, and
obstruction. For polynomial requests, construct every retained consequence; for
an accepted source answer, also construct a lift into the original physical
relations. Every operation must expose rather than silently resolve missing data,
algebraic-closure artifacts, physical branches, or unsupported request shapes.
When a declared second stage is present, preserve the typed value, source
provenance, certificates, and direct parent identity across that single edge.

## Exact harmonic-response cases

The harmonic contract uses `Re(z exp(i omega t))` and admits only finite exact
systems linear in declared complex response unknowns.

| ID | Source or boundary | Required result |
| --- | --- | --- |
| H-W | A21-03 fixed reflection at `11 pi/2` | reflected amplitude `iA`, total `2iA cos(theta)`, exact nodes/antinodes, Q signal |
| H-C | A25-06 numerical series RLC | exact complex impedance/current, magnitude, phase cosine, `always_direct` cost boundary |
| HR-X | quadratic phasor law | `nonlinear_phasor_law` |
| HR-U | one law for two response unknowns | `underdetermined_phasor_response` |
| H-Z | zero phase reference | `undefined_phase_reference` |
| H-I | constant-magnitude response on a finite interval | `nonfinite_spatial_pattern` |

A21-03 generated the phase-loss obstruction; A25-06 is a different-area transfer,
not seed evidence. Both source statements are bound to the same PDF checksum.

## Exact harmonic-product cases

The product contract consumes two exact phasors at the same positive frequency and
must reconstruct their scaled real-signal product as DC plus a `2 omega` channel.

| ID | Source or boundary | Required result |
| --- | --- | --- |
| M-G | unequal complex phasors | exact DC, second-harmonic phasor, real return, and direct-product certificate |
| M-23 | A23-05 rotating square coil with self-inductance | emf, current, mean torque, torque ripple, power balance, and `always_direct` admission |
| M-11 | A11-06 small coil in a much larger current loop | unchanged response-product pipeline with `L=0` |
| M-X | time-dependent phasor, complex scale, or zero frequency | reject at typed request admission |

A23-05 is the obstruction-generating source; A11-06 is a bounded second-source
transfer. Neither establishes transfer outside electromagnetism.

## Typed one-successor composition cases

The composition contract accepts one routed root and one declared compatible
consumer. It must not infer ports, retry with another operator, or execute an
arbitrary callback.

| ID | Root to consumer | Required result |
| --- | --- | --- |
| C-23 | A23-05 harmonic response to harmonic product | exact established torque plus inherited provenance, certificates, and one root parent |
| C-14 | A14-06 path functional to two-path circuit | exact established terminal voltage through the same artifact envelope |
| C-U | underdetermined harmonic root | `upstream_underdetermined_phasor_response` and no artifacts |
| C-X | path payload sent to harmonic consumer, or absent named harmonic port | `incompatible_pipeline_step` or `missing_parent_observable` without fallback |

These four tests add architecture and evidence-flow coverage. Both successful
source problems were already complete corpus executions, so corpus counts and
physics-grammar coverage do not change.

## Cross-grammar problem-routing cases

The frozen router contract accepts one human-validated semantic request and must
select an existing owner without problem-ID or expected-answer rules.

| ID | Semantic card | Required routed result |
| --- | --- | --- |
| O-D | A24-09 one-law capacitance target | `direct_relation` with exact certificate |
| O-P | A13-02 laws with hidden impact speed | `polynomial_relation` |
| O-F | unseen-area viscous functional packet | `source_functional` transfer |
| O-L | finite repeated linear dynamics | `linear_closure` |
| O-E | A15-01 zero event plus physical interval | `event_relation` and `always_direct` admission |
| O-I | A15-02 restitution plus bounded Coulomb impulse | `frictional_impact` and `always_direct` admission |
| O-A | A14-06 oriented induced-work paths | `path_functional` |
| O-T | unchanged A10-06 path transfer | `path_functional` |
| O-W | A21-03 reflected-wave request | `harmonic_response` |
| O-C | A25-06 series-circuit request | `harmonic_response` and `always_direct` admission |
| O-M | two minimal packets with different target relations | preserve `ambiguous_minimal_packets` |
| O-X | transcendental target relation | preserve `unsupported_relation_shape` |

The first ten cases must retain passing domain certificates in the common result.
The final two are correct routing dispositions but not successful physical
constructions. This bench tests orchestration and evidence preservation; it does
not add grammar coverage.

## Frictional-impact projection cases

The impact contract treats the incoming normal and tangent speeds as magnitudes.
Newton restitution fixes the normal impulse; maximum dissipation projects the
impulse required for zero tangent speed onto the Coulomb interval.

| ID | Input or source | Required result |
| --- | --- | --- |
| I-G | exact symbolic component speeds | complementary tangential-arrest/sliding branches, piecewise return, and five exact certificates |
| I-N | exact numeric data on each side of the boundary | select the correct regime and preserve the same impulse law |
| I-Z | zero friction | unchanged outgoing tangential speed and saturated impulse zero |
| I-15 | A15-02 wall geometry | exact reflected speed and angle in both symbolic regimes plus `always_direct` admission |
| I-X | zero/negative mass, normal speed, tangent speed, friction, or restitution | reject at typed admission |

The source packet is a nonrotating point particle. Rotation, compliance, and
multiple contacts are not silently folded into the scalar tangent impulse.

## Path-functional reconstruction cases

| ID | Obstruction/input | Required constructed result |
| --- | --- | --- |
| F-A | A14-06 induced field, arc and chord, two resistive branches | exact work/length functionals, constant-curl area witness, terminal voltage, and conserved branch currents |
| F-T | A10-06 with short arc, long arc, and no conductor | unchanged path interface; exact arc works; `no_scalar_potential_certificate` for endpoints alone |
| F-R | one path and its orientation reversal | work changes sign while length is invariant |
| F-C | conservative field with supplied scalar potential | every path recovers the same endpoint-potential difference |
| F-M | paths with unequal oriented endpoints | `endpoint_mismatch` before comparison |
| F-S | source transfer runner | construct both source-bound problems without answer-specific interface changes |

These cases test an obstruction-driven grammar extension. Direct integration is
not sufficient: on constant-curl fields the result must also prove that every
same-endpoint work difference equals curl times signed area between paths.

## Relation-projection cases

| ID | Input relation class | Required output |
| --- | --- | --- |
| R-P | two linear maps followed by a scalar target | the same target relation as `T^Tq` pullback |
| R-Q | linear field amplitudes followed by quadratic loss | eliminate field components to one source-target relation |
| R-C | full two-frequency dynamics and observable coordinates | the same two closed equations as the closure constructor |
| R-N | A25-02 dimensionless orbit relations | turning polynomial and both algebraic radii |
| R-U | no relation involving the target | `target_not_constrained` |
| R-B | four variables under a three-variable budget | refusal before elimination |
| R-I | contradictory laws | `inconsistent_relations` |

## Event-construction cases

| ID | State/predicate input | Required constructed result |
| --- | --- | --- |
| E-A | A15-01 energy, vertical acceleration, horizontal-resultant predicate, released interval | generate `15c^2-c-5=0`, lift both roots, select `(1+sqrt(301))/30` |
| E-M | quadratic state map with two roots in one physical interval | `ambiguous_event_branches`; do not order roots arbitrarily |
| E-N | algebraic roots outside the declared interval | `no_admissible_event` |
| E-X | transcendental state relation in the rational-polynomial kernel | `unsupported_relation_shape` |
| E-B | two event variables under a one-variable budget | `variable_budget_exceeded` before branch solving |
| E-C | source transfer plus same-substrate handwritten audit | machine construction succeeds while literal exam route remains `always_direct` |

These cases distinguish generation, full-state recovery, and physical selection.
The A15-01 input does not contain the expected event polynomial or root.

## Semantic extraction-and-return cases

| ID | Extraction | Required return witness |
| --- | --- | --- |
| S-L | dielectric field to rank-one linear-functional skeleton | recover voltage, dimensions, constitutive regime, and bound-charge sign |
| S-Q | induced field to rank-one quadratic-functional skeleton | recover Joule power, cylindrical measure, and time-average factor |
| S-H | R-L phasor response to linear-response/quadratic-loss skeleton | recover average resisting torque and steady-state convention |
| S-N | orbit to latent-relation skeleton | recover both turning points, then select apocentre using geometry and `alpha` range |
| S-X | replace average torque target by instantaneous torque after phase removal | refuse return and require phase/two-quadrature state |

These are deductive semantic benchmarks, not additional software tests. They test
whether each mathematical result returns to the same physical observable and
whether over-abstraction produces an explicit failure.

## Executable semantic-compiler cases

| ID | Physical packet | Required generated result |
| --- | --- | --- |
| X-L | dielectric samples and voltage target | infer linear skeleton and return `U-3D=0` |
| X-Q | induced-field samples and heating target | infer quadratic skeleton and return `P-13s^2=0` |
| X-T | unseen viscous-dissipation mechanics packet | reuse quadratic skeleton and return `P-17v^2=0` |
| X-P | instantaneous target after magnitude-only extraction | `semantic_feature_lost` for phase |
| X-D | dimensionally mistyped target | `dimension_mismatch` |
| X-B | two fields under a one-field budget | `field_budget_exceeded` |
| X-N | nonlinear source-to-field law | `unsupported_relation_shape` at this layer |

These seven cases are software tests. X-T is the first transfer to an area not used
to motivate the electromagnetic source-to-field skeleton.

## Dimensional-quotient cases

| ID | Area/input | Required result |
| --- | --- | --- |
| Q-D1 | pendulum period, length, gravity | construct primitive group `T^2 g/L`; supplied pendulum law returns `4 pi^2` |
| Q-D2 | density, speed, length, viscosity | unchanged constructor returns Reynolds group `rho v L/mu` |
| Q-D3 | elapsed time, resistance, capacitance | unchanged constructor returns `t/(RC)`; one time constant returns `1` |
| Q-D4 | independent mass and length | `irreducible`; no dimensionless group |
| Q-D5 | three already dimensionless quantities under budget two | `group_budget_exceeded`; no partial basis |

The first case is regression and downstream use, the next two are cross-area
transfer, and the last two are boundaries. These cases establish exact
four-base-dimensional quotient construction. They do not derive a pendulum law,
Reynolds dynamics, an RC response law, a unique preferred basis, or handwritten
speed reduction.

## Boundary-network condensation cases

| ID | Area/input | Required result |
| --- | --- | --- |
| Q-N1 | electrical three-node conductance chain | exact two-terminal response and junction-voltage recovery |
| Q-N2 | four-node chain with two interleaved hidden states | exact three-edge response and both hidden-state recoveries |
| Q-N3 | mechanical two-spring chain | unchanged constructor returns the series stiffness and junction displacement |
| Q-N4 | thermal chain with hidden source `Q` | effective response, split boundary source, and affine junction temperature |
| Q-N5 | hidden free mode | `internal_block_singular`; no partial reduction |
| Q-N6 | symbolic hidden coefficient without assumptions | `internal_invertibility_undetermined` |
| Q-N7 | hidden count above budget | `internal_budget_exceeded` before elimination |
| Q-N8 | no hidden variables | `irreducible`; original boundary law is preserved |

These cases establish exact finite linear boundary condensation plus recovery, not
automatic topology parsing, physical-law discovery, nonlinear-network reduction,
or a handwritten time advantage.

## Sparse network-ordering cases

| ID | Probe | Required result |
| --- | --- | --- |
| Q-O1 | center-first declared order on branched reciprocal network | exact boundary/recovery; 6 fill edges and 19 nonzero local updates |
| Q-O2 | greedy minimum-current-fill order on same network | leaf, leaf, center; exact boundary/recovery; 1 fill edge and 5 updates |
| Q-O3 | unchanged elastic semantic adapter | same selected order and condensed matrix; displacement meaning retained |
| Q-O4 | same sparse branch with central source | add only its two affected source updates; total ledger is 7 |
| Q-O5 | reciprocal invertible hidden block with zero scalar diagonals | `no_provable_scalar_pivot`, although block condensation succeeds |
| Q-O6 | nonreciprocal response | `nonreciprocal_response` at planner boundary |
| Q-O7 | step-budget overflow | `elimination_step_budget_exceeded`; no partial plan |
| Q-O8 | no internal variables | `irreducible`; original boundary law retained |
| Q-O9 | unknown strategy | admission error before computation |

The first two cases are a same-observable structural cost comparison, not a learner
trial. Greedy current minimum fill is not asserted to be globally optimal.

## Deductive network human-cost cases

| ID | Probe | Required result |
| --- | --- | --- |
| Q-H1 | compile declared and sparse plans to handwritten ledgers | `(1,3,5,19,0,0,1)` versus `(1,3,5,5,0,3,1)` with atomic accounting |
| Q-H2 | construct positive-weight boundary | conditional inequality `3*w_representation_changes < 14*w_symbolic_actions` |
| Q-H3 | two hypothetical sensitivity profiles | unit weights select sparse; recognition weight six selects declared |
| Q-H4 | claim boundary with no observations | speed `conditional_weights_unmeasured`; learnability `human_observations_required` |
| Q-H5 | one-hidden-node same-order transfer | `always_direct`; recognition adds one action and saves nothing |
| Q-H6 | scalar-planning obstruction or missing identity | no cost boundary from incomplete routes; reject missing problem identity |

These tests prove a model-relative break-even region and a direct gate. They do not
supply action-time weights or human recognition, accuracy, retention, and transfer
observations.

## Matched network acquisition cases

| ID | Probe | Required result |
| --- | --- | --- |
| Q-S1 | frozen phase topology sets | delayed families equal immediate families; unseen families are disjoint |
| Q-S2 | twelve executable answer keys | exact first-boundary current; block, declared, and sparse laws agree |
| Q-S3 | `N1`/`N2` crossover | each phase balances two direct/two sparse trials; every variant reverses route across sequences |
| Q-S4 | empty learner/reviewer templates | `unobserved`, `additional_review_required`, benefit dispositions `not_evaluated` |
| Q-S5 | observation restoration | refuse assignment, strip, delay, session, timing, identity, and error-code conflicts |
| Q-S6 | correctness and timing | exact scoring; only complete/correct/adherent pairs enter participant-phase clusters |
| Q-S7 | independent key preflight | two blinded positive reviewers per variant; an admitted dispute requires revision |
| Q-S8 | booklet/key separation | schedules/prompts are visible; exact answers are absent from the participant booklet |

These are instrument-integrity tests. Synthetic observations exercise the
estimand but are explicitly not learner or expert evidence.

## Adaptive network-admission cases

| ID | Probe | Required result |
| --- | --- | --- |
| Q-A1 | balanced three-valued key | each phase has one `direct_gate`, `conditional_candidate`, and `refuse` |
| Q-A2 | key generation | boundary class or typed planner obstruction constructs every decision and witness |
| Q-A3 | `A1`/`A2` schedules | reverse task order independently inside all three phases |
| Q-A4 | empty schemas | `additional_review_required`, `unobserved`, and no recognition disposition |
| Q-A5 | observation loader | restore task/key; refuse schedule, vocabulary, delay, session, and identity defects |
| Q-A6 | participant clustering | require all three classes before participant-phase accuracy/time enters analysis |
| Q-A7 | key preflight | two identified blinded reviewers; disagreement or ambiguity requires revision |
| Q-A8 | cohort isolation | reject participant overlap between recognition and assigned execution |
| Q-A9 | material separation | participant booklet contains tasks but no expected-decision mapping |

The conditional label preserves unknown human weights. These tests cannot make
`sparse` an unconditional correct answer or supply recognition evidence.

## Corpus audit cases

| ID | Inventory property | Required result |
| --- | --- | --- |
| C-I | all top-level problems | 126 unique IDs across 15 included years |
| C-E | execution evidence | 25 full, 3 partial, and 2 shape-only executions |
| C-O | operation routing | every row names a family and used or missing operator |

These tests establish corpus accounting, not physics-solution correctness. Static
candidate labels remain hypotheses until the corresponding source packets execute.

## Multi-target and locked-batch cases

| ID | Capability | Required result |
| --- | --- | --- |
| P-M | several targets in one source packet | exact per-target projections and one complete status |
| P-P | constrained plus missing target | partial status without discarding the constrained result |
| P-L | target-conditioned law selection | unrelated subpart variables never enter the projection |
| P-D | direct relation | constrain a target with an empty hidden-variable set |
| B-I | locked corpus identity | batch IDs equal the nineteen indexed polynomial routes |
| B-E | exact batch consequences | every expected relation belongs to its source-law ideal |
| B-S | partial semantic boundary | 16 complete and 3 partial packets; 41 constrained and 3 underdetermined targets |

The remaining new test rejects duplicate target names before elimination. The batch
is a source-packet benchmark: physical laws are supplied theorem contracts, not
outputs of a prose parser.

## Prior exact fast-path cases

Seven observable-closure cases test scalar closure, two-dimensional closure,
transfer across reciprocal couplings/masses, zero target, and equation-budget
failure. Five pullback cases test linear composition, two quadratic physical
fixtures, an R-L real-quadrature fixture, and incompatible ports.

## Adaptive unidentified-input cases

| ID | Unordered supplied-law input | Required result |
| --- | --- | --- |
| A-S | three-law target chain plus two distractors | select exactly the three-law chain and derive the target relation |
| A-A | two smallest packets with different target relations | `ambiguous_minimal_packets` with both witnesses |
| A-E | two scaled forms of the same smallest relation | construct once and retain both equivalent packets |
| A-N | no law containing the target | `no_target_path` before elimination |
| A-D | target component contains no given and does not close alone | `disconnected_target` |
| A-U | target connected to a given but one hidden freedom survives | `target_not_constrained` |
| A-B | a three-law chain under a two-law budget | `search_budget_exceeded` |
| A-X | target law contains a transcendental operation | `unsupported_relation_shape` |
| A-T | unlabeled A617 water-jet laws mixed with capacitor and atomic laws | select ballistic plus momentum-flux relations and certify the height polynomial |

These cases test adaptation to new combinations of supplied theorem contracts, not
automatic physical-law discovery.

## Handwritten whole-route cost cases

| ID | Same-observable comparison | Required result |
| --- | --- | --- |
| H-L | action ledger to cost vector | derive counts; do not accept unbound totals |
| H-P | one route no worse on every axis | identify the Pareto winner without weights |
| H-T | each route better on different axes | retain `tradeoff`, not a scalarized win |
| H-S | six A617 source bindings across four areas | preserve PDF page and identical targets |
| H-G | current six-case feasibility gate | 5 baseline wins, 1 trade-off, 0 compiler wins |
| H-R | unsupported action type | reject invented timing as a structural action |
| H-A | one symbolic line changes three subjects | derive three atomic symbolic units |
| HW-U | symbolic action omits its subjects | refuse an unidentified work unit |
| HW-X | routes use different execution substrates | refuse the comparison |

The H0 gate is deliberately capable of rejecting the exam-leverage claim. It does
not convert structural action counts into elapsed time or learner performance.

## Cost-aware route-admission cases

| ID | Admission behavior | Required result |
| --- | --- | --- |
| J-D | proposed-minus-direct vector | exact delta and symbolic break-even inequality |
| J-I | direct route Pareto-dominates | `always_direct` for every positive profile |
| J-C | mixed-sign delta | declared profiles can select opposite sides of the boundary |
| J-B | proposed route exceeds peak-live budget | direct route regardless of weighted gain |
| J-A | six locked H0 comparisons | 5 `always_direct`, 1 `conditional`; unit probe admits A13-02 only |
| J-P | zero or incomplete cost weights | refuse the untyped/nonpositive profile |

The unit-action profile is explicitly hypothetical. J0 supports the boundary and
decision computation, not the empirical profile used to choose a side.

## Paired-route calibration cases

| ID | Calibration behavior | Required result |
| --- | --- | --- |
| W-R | full-rank synthetic H0 differences | recover all four active weights exactly |
| W-K | two non-spanning observations | `insufficient_rank` with unidentified axes |
| W-C | no pair has two correct routes | exclude the pairs and return `no_correct_pairs` |
| W-P | timing differences imply a nonpositive cost | refuse `nonpositive_fit` |
| W-H | new problem uses identified axes | predict and score the cheaper correct route |
| W-L | training problem reused for evaluation | refuse training leakage |
| W-U | held-out delta uses a new axis | refuse `unidentified_prediction_axis` |
| W-M | training rows contain two participants | refuse a mixed personal profile |
| W-Q | holdout belongs to another participant | refuse `participant_mismatch` |

## Matched-variant acquisition cases

| ID | Acquisition behavior | Required result |
| --- | --- | --- |
| D-S | six source-bound structures | twelve distinct variants with page provenance |
| D-A | exact authored answer keys | preserve all six physical relations and returns |
| D-R | four calibration families | rank four on `(H,P,S,X)`; holdouts introduce no new axis |
| D-C | two sequences and two blocks | balance route order; separate each pair by six trials |
| D-Z | header-only empirical template | load exactly zero observations |
| D-I | one valid completed row | restore locked boundary, time, order, and provenance |

## Selective micro-tool acquisition cases

| ID | Instrument behavior | Required result |
| --- | --- | --- |
| D3-F | four families in three phases | twelve pairs and twenty-four exact variants |
| D3-C | two execution sequences | exchange every variant's direct/operator route; pair attempts four apart |
| D3-R | mixed recognition-only tasks | twelve decisions including `direct` and `refuse-card`; reversed `R1`/`R2` order |
| D3-S | independent frozen schemas and cohorts | restore assignments; refuse tampering and participant overlap |
| D3-V | assisted card rule | card visible only on an assisted operator trial |
| D3-P | guarded paired outcome | time delta only for two correct, complete, route-adherent executions |
| D3-Z | two header-only templates | load zero recognition and zero execution observations |

## Micro-tool observable-closure cases

| ID | Observable behavior | Required result |
| --- | --- | --- |
| D4-T | independent whole-trial timer | reliable phases sum exactly; unreliable phases cannot replace total |
| D4-D | elapsed time from assisted reference | assisted is zero; delayed-unseen is positive |
| D4-K | two or more independent key reviews | distinguish agreement, ambiguity, and unanimous key dispute |
| D4-A | absent or single key review | `unreviewed` or `insufficient_review`, never agreement |
| D4-R | duplicate reviewer/task record | typed refusal before audit |
| D4-B | missing or unblinded reviewer manifest | retain judgment, exclude from agreement, return `protocol_invalid` |
| D4-F | frozen key-preflight precedence | revision beats more review; only all-agreed reaches learner-pilot readiness |
| D4-S | descriptive pilot summary | score only agreed keys; count eligible time signs; never emit a speed verdict |
| D4-G | complete two-participant execution fixture | four within-person family deltas become one cluster per participant-phase; exact mean and sample variance |
| D4-H | one incorrect operator attempt | retain it in operator accuracy; exclude its entire participant-phase timing cluster |
| D4-I | zero execution rows | return `unobserved`; do not invent a mean, variance, or phase decomposition |
| D4-V | repeated variant identity | typed refusal before balance diagnostics |

## Coherence equalities

For a graph relation `y=Tx`, eliminating `y` from

```text
y-Tx=0,
z-q^T y=0
```

returns `z-(T^Tq)^T x=0`. This is the output of the pullback fast path.

For `x''=-Ax`, `y=B^Tx`, and `B^TA=RB^T`, eliminating `x,x''` returns

```text
y''+Ry=0.
```

This is the output of the closure fast path. The executable tests verify ideal
membership of both reduced equations in the supplied full-law relation system.

## Same-observable and cost contract

Correctness is equality of the projected relation, not agreement at one numerical
point. Computational leverage is a separate claim. For each source problem compare

```text
(relations selected,
 hidden quantities introduced,
 maximum simultaneous equations,
 symbolic actions,
 branch/regime checks,
 representation changes,
 contextual return checks)
```

for a competent baseline and the compiled route. Unconditional dominance requires
a component-wise non-worse vector with at least one strict improvement. Mixed-sign
differences generate a break-even region rather than a universal verdict. Learner
speed, error, and the profile selecting a side require direct measurement.

## Pass and rejection conditions

The finite coherence, source-packet, corpus-accounting, adaptive-search,
whole-route-cost, atomic-substrate, route-admission, paired-calibration,
matched-acquisition, event, path-functional, harmonic-response, harmonic-product,
typed-composition, frictional-impact, selective-micro-tool, micro-pilot-observable,
network acquisition/admission, and cross-grammar routing bench passes when all 189 active tests
return exact relations, comparisons, admission boundaries, or declared obstructions
without answer-specific rules. The
accepted orbital branches lift symbolically to the original law system, and each
accepted semantic compilation carries dimensional, ideal-membership, and lift
certificates.

The broader exam claim must be narrowed or rejected if relation selection costs as
much as solving the problem, polynomial elimination exceeds the handwritten
budget, branch conditions cause frequent errors, or unseen transfer does not
improve against a competent structural baseline.

The layered-semantics claim is rejected if an extraction cannot name what it
forgets, if its ledger merely repeats the complete original solution, or if two
problems are called equivalent without a shared operation and separate physical
return witnesses.
