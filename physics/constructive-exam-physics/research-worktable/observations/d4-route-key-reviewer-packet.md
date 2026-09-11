# D4-K blinded route-key reviewer packet

This packet evaluates whether the authored route key is sufficiently determinate
for a learner pilot. It does not evaluate whether the framework saves time.

## Reviewer boundary

- Complete the reviewer manifest before judging tasks. State the physics domain in
  which you are qualified to review introductory examination problems.
- Do not consult the authored answer key, operator cards, another review, or learner
  results. If exposure occurs, record it truthfully; the audit retains but excludes
  the affected judgments.
- Use assigned order `R1` from R01 to R12 or `R2` from R12 to R01.
- Select one route and give a short physical reason. Do not calculate a final
  numerical answer and do not discuss the tasks until submission.

Route vocabulary is neutral with respect to the tasks:

- `direct`: the standard short physical-law route is already sufficient;
- `slice`: retain only relations ancestrally required by the named target;
- `event`: bind a first/last/trigger condition and restrict to reachable branches;
- `projection`: project a desired update onto an admissible bound or regime;
- `path`: preserve a path functional when endpoints alone are insufficient;
- `harmonic`: preserve complex magnitude and phase in a linear response;
- `product`: separate mean and oscillatory channels of a harmonic product;
- `symmetry`: reduce to a symmetry-compatible subspace after checking invariance;
- `refuse-card`: the offered reduction loses information required by the problem.

## Independent judgments

| ID | Prompt | Selected route | Physical rationale |
| --- | --- | --- | --- |
| R01 | A mass is dropped through a known height; find its pre-impact speed. | | |
| R02 | A circuit subpart asks only for heat in one known resistor and interval. | | |
| R03 | Find the first instant when a pendulum string tension vanishes. | | |
| R04 | Saturated wall friction would reverse a point particle's tangent speed. | | |
| R05 | Compare open-wire voltages on two paths through changing magnetic flux. | | |
| R06 | A steady series RLC problem asks for magnitude, lead/lag, and real signal. | | |
| R07 | A rotating coil asks only for cycle-averaged torque from two phasors. | | |
| R08 | A spinning sphere hits a rough wall; only a point-particle card is offered. | | |
| R09 | Find a switched oscillator's full transient using only a steady phasor law. | | |
| R10 | A verified electrostatic potential is given; find endpoint voltage. | | |
| R11 | A symmetric linkage has twelve components but two admissible coordinates. | | |
| R12 | Jet-supported height and momentum flux share one hidden impact speed. | | |

Transcribe the manifest to `d4-route-key-reviewer-template.tsv` and the twelve
judgments to `d4-route-key-review-template.tsv`. The administrator audits task
agreement only after every assigned reviewer has submitted.
