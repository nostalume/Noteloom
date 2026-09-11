#import "../../manus/manus.typ": daily-en
#show: daily-en.with(
  title: [Observable-Reduction Exam Kernel],
  abstract: [Rapid route selection and return checks.],
  keywords: ("physics", "exam kernel", "route selection"),
  normal-size: 8pt,
  margin: (top: 35pt, bottom: 35pt, left: 44pt, right: 44pt),
)


Use this sheet after reading the
#link("observable-reduction.typ")[full manual]. It is a decision aid, not a
required solution format.

= The route

```text
TARGET -> PACKET -> SLICE -> DIRECT GATE
       -> OBSTRUCTION -> OPERATOR -> RETURN -> CHECK
```

Write first:

#align(center)[*GIVEN* $mid$ *HIDDEN* $mid$ *TARGET*]

Read every card through the same five fields:

#table(
  columns: (auto, 1fr),
  [*Cue*], [the obstruction that makes the direct route unsafe or expensive],
  [*Remember*], [the area law and regime that license the card],
  [*Reduce*], [one operation on the target-bearing relations],
  [*Return + check*], [restore physical meaning and test an original law],
  [*Refuse / escalate*], [name the failed premise or missing datum; move to a richer view],
)

+ Bind one target: instant/average, frame, direction, units, branch.
+ List justified laws and their regimes.
+ Trace backward from the target; omit relations that cannot reach it.
+ If one short chain closes, solve directly.
+ Otherwise name the first obstruction and use one matching operation.
+ Return units, regime, sign/orientation, branch, boundary, and target convention.
+ Substitute into an original law; check one dimension, limit, or interval.

= Obstruction map

#table(
  columns: 3,
  table.header(
    [*See this*],
    [*Do this*],
    [*Write this*],
  ),
  [short competent chain],
  [direct],
  [no extra representation],
  [irrelevant laws],
  [slice],
  [backward cone from target],
  [explicit hidden quantity],
  [substitute],
  [`h=f(g), o=Phi(h)`],
  [repeated internal exchange],
  [cancel],
  [weights forced by zero internal term],
  [implicit instant],
  [event],
  [vanish, transport, restrict],
  [equality overshoots a bound],
  [project],
  [desire, clip, return],
  [path-dependent work],
  [path],
  [orient path; compare by loop],
  [lost phase],
  [harmonic],
  [`Re(z exp(i omega t))`],
  [product of harmonics],
  [product],
  [mean with conjugate; ripple without],
  [too many coordinates],
  [symmetry],
  [parameterize admissible motion],
  [unit-scale redundancy],
  [dimension],
  [solve `Da=0`],
  [hidden network states],
  [condense],
  [eliminate locally; recover in reverse],
)

= Four high-value cards

== Event

- *Vanish:* set the event component to zero.
- *Transport:* express it using state laws.
- *Restrict:* retain only reached full-state roots.

Do not select a root before restoring interval and traversal direction.

== Bounded response

$ "desired action" arrow.r "admissible interval" arrow.r "projection" arrow.r "physical return". $

For point-particle wall impact:

$ J_n = m(1+e)u_n, quad J_t = op("proj")_[-mu J_n,mu J_n](-m u_t). $

Refuse this card for rotation or multiple contacts.

== Path

$ W[gamma] = integral_gamma bold(E) dot dif bold(l), quad W[gamma_1]-W[gamma_2] = ∮ bold(E) dot dif bold(l). $

Use an endpoint scalar only after a conservative-field certificate. With no
material or probe path in a nonconservative field, refuse endpoint-only voltage.

== Harmonic and product

$ z arrow.r Re(z exp(i omega t)), quad op("mean")(Re(a e^(i omega t)) Re(b e^(i omega t))) = Re(a overline(b))/2, quad hat(z)_(2 omega) = a b/2. $

Keep phase for interference, lead/lag, boundary values, and instantaneous return.
Steady phasors do not contain initial-data transients.

= Unknown problem

```text
target-bearing law
-> unresolved symbols become open ports
-> attach one justified law toward a given
-> eliminate and test closure
-> stop at first complete depth
-> compare complete routes.
```

Prefer conservation/boundary laws and attachments introducing fewer new hidden
quantities. If the route fails dimensions, regime, or physical meaning, reject it.
If no route closes, name the missing bridge or datum.

= Direct-gate tests

Stay direct when the operator:

- merely renames one or two familiar equations;
- introduces a representation used only once;
- creates more live quantities than it removes;
- cannot omit a channel, control a branch, or prevent a likely error;
- saves execution only by treating recognition or recovery as free.

For a trade-off, compare

$ C_"route" = C_"recognition" + C_"setup" + C_"execution" + C_"return". $

Use the structural route only when its setup debt is smaller than its execution
saving for the learner and problem at hand.

= Return checklist

- $square$ correct units and mathematical type
- $square$ restored sign, direction, and orientation
- $square$ physical root in the reached interval
- $square$ valid approximation/regime inequalities
- $square$ respected boundary and initial conditions
- $square$ recovery in the original laws
- $square$ answer matches the requested observable

= Memory sentence

#quote(block: true)[
  Preserve physics, forget only what the target cannot see, compute at the lowest
  useful layer, and restore everything needed to interpret the answer.
]

