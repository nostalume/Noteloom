#import "../../manus/manus.typ": daily-en
#show: daily-en.with(
  title: [Observable Reduction],
  abstract: [A constructive exam-solving manual for general physics.],
  keywords: ("physics", "exam review", "observable reduction"),
)



This manual presents a way to organize familiar physics knowledge around the
observable requested by a problem. It does not replace mechanics,
electromagnetism, thermodynamics, waves, or optics with one universal formula.
Instead, it separates two questions that are often mixed together:

+ *Which physical laws describe the situation?*
+ *What is the smallest safe computation that reaches this target?*

The first answer remains area-specific. The second often belongs to a small set of
reusable operations. The central exam interface is

```text
TARGET -> PHYSICAL PACKET -> SLICE -> DIRECT GATE
       -> OBSTRUCTION -> OPERATOR -> RETURN -> CHECK.
```

The direct gate is essential. A framework that rewrites every easy solution in a
new language increases work rather than reducing it. Use a structural operator
only when it removes a visible obstruction from the complete route.

This manual has two uses. On a first reading, it explains why the operators exist
and works through representative computations. During review, use the memory
kernel in Section 3 and the operator table in Section 4. Under exam conditions,
write only the few lines belonging to the selected route; the framework is a
decision discipline, not required notation.

= What is being unified

== The physical packet

Before algebra, represent a problem from physical area `a` by the packet

$ P_a = ( &"quantities", "dimensions", "laws", "geometry/boundary", "regime", \
          &"givens", "target", "branch convention" ). $

The packet prevents a mathematical resemblance from being mistaken for a physical
law. A current, a velocity, and a temperature may occupy the same position in a
linear relation, but their meanings, units, admissible values, and governing laws
remain different.

The target conditions the packet. If a problem asks for dissipated power, laws
that reach only a magnetic-field subpart need not enter the simultaneous system.
If the target changes to an instantaneous phase, a magnitude-only description
that was sufficient for average power is no longer sufficient.

== Four temporary views

The solver may move upward through four views, stopping as soon as a useful
operation becomes visible.

#table(
  columns: 3,
  table.header(
    [*View*],
    [*What is retained*],
    [*Examples*],
  ),
  [Physical],
  [phenomenon, law, units, regime],
  [force, charge, torque, dielectric law],
  [Structural],
  [shared physical role],
  [balance, response, boundary, event, constraint],
  [Relational],
  [typed mathematical dependence],
  [source-to-field map, path functional, constraint relation],
  [Algebraic],
  [execution representation],
  [equation set, polynomial, phasor, matrix, nullspace],
)

Moving upward deliberately forgets some detail. Therefore every reduction carries
a *return ledger*:

#table(columns: 2, [units], [law provenance], [regime], [boundary data], [sign/orientation], [branch], [target convention], [original-law recovery])

The final answer is accepted only if it can be returned through this ledger to the
original physical packet.

== The invariant of a legal reduction

A legal reduction preserves the admissible relation between givens and target,
together with the target's physical meaning. Schematically,

```text
physical packet ----------------------> physical answer
      |                                      ^
      | extract                              | return
      v                                      |
mathematical skeleton ---- compute ----> reduced relation.
```

The two routes must agree on the admissible `(givens, target)` pairs. Four checks
make this operational:

+ *Lift:* reconstructed hidden quantities satisfy the original laws.
+ *Dimension:* units and scalar/vector types agree.
+ *Regime:* approximations and inequalities remain valid.
+ *Meaning:* sign, orientation, averaging, boundary, and branch conventions
   match the requested observable.

If any check fails, the solver forgot too much and must return to a richer view.

= What the learner must remember

The framework reduces organization and computation; it cannot eliminate physical
knowledge. Memory is divided into three layers.

== Area-specific knowledge

The learner still needs:

- governing laws such as Newton's laws, conservation laws, Maxwell relations, and
  thermodynamic balances;
- constitutive laws such as Hooke, Ohm, dielectric response, viscosity, and
  friction;
- geometric and boundary meanings;
- approximation regimes such as small oscillation, quasistatic response, steady
  harmonic state, massless junction, and point-particle impact;
- sign and orientation conventions.

These facts decide which relations may enter the packet. The common framework is
not allowed to invent them.

== Reusable computational knowledge

Instead of remembering a separate trick for every chapter, remember a small map
from obstruction to operation:

```text
irrelevant laws       -> slice
explicit hidden chain -> substitute
repeated internal term-> cancel
implicit event        -> vanish, transport, restrict
bounded response      -> project
path dependence       -> compare paths through a loop
phase dependence      -> retain a complex amplitude
harmonic product      -> split mean and ripple
too many coordinates  -> reduce to admissible motion
unit-scale redundancy -> take a dimensional nullspace
hidden network states -> condense and recover.
```

== Return knowledge

At the end, ask a fixed sequence:

- correct units
- meaningful sign or direction
- physically reached root
- valid approximation regime
- requested instant, average, frame, and branch
- recovery of the original laws

This repetition is deliberate. It moves common exam errors from vague caution into
a finite checking procedure.

== Reframing the usual subject areas

The framework changes the index under which knowledge is recalled. Textbooks
usually index a result by chapter and object: projectile, pendulum, capacitor,
wave, heat engine. Observable reduction adds a second index: balance, event,
boundary response, path accumulation, phase, constraint, or quotient. The first
index supplies the physics; the second suggests the computation.

#table(
  columns: 3,
  table.header(
    [*Area*],
    [*Physical knowledge that remains specific*],
    [*Structural questions used for retrieval*],
  ),
  [Mechanics],
  [force law, inertia, constraints, restitution, friction],
  [balance, invariant, event, admissible motion, bounded impulse],
  [Gravitation/orbits],
  [central force, energy, angular momentum, bound regime],
  [hidden-invariant elimination, turning branch],
  [Electrostatics],
  [Gauss law, potential, dielectric boundary laws],
  [source-to-field map, boundary observable, linear functional],
  [Induction],
  [Faraday law, field orientation, material circuit],
  [path functional, loop comparison, harmonic response],
  [Circuits],
  [Kirchhoff laws, element constitutive laws, initial conditions],
  [network condensation, phase response, transient refusal],
  [Waves/optics],
  [propagation law, impedance, boundary conditions],
  [complex response, interference, stationary/event conditions],
  [Thermodynamics],
  [state variables, process restrictions, first/second laws],
  [balance cancellation, path/process dependence, admissible regime],
  [Fluids],
  [continuity, momentum balance, constitutive regime],
  [flux cancellation, dimensionless quotient, boundary response],
  [Rigid assemblies],
  [geometry, mass distribution, joint constraints],
  [symmetry-compatible tangent space, generalized impulse],
)

This table is not a replacement formula list. It is a retrieval map. For example,
“turning branch” reminds the learner to use zero radial speed and restrict roots,
but only orbital mechanics supplies the energy and angular-momentum relations.
“Path functional” reminds the learner not to collapse a nonconservative field to
endpoints, but Faraday's law still determines the field or loop integral.

=== Mechanics as events, balances, and admissible motions

Mechanics problems often become long because position, velocity, force, impulse,
and constraint variables are all carried at once. Target conditioning separates
three common cases:

- If the target concerns a special instant, construct the event predicate first
  and transport it through energy or kinematics.
- If an internal force or impulse appears with opposite signs, eliminate it through
  a balance rather than solve for it.
- If constraints reduce the possible instantaneous motions, parameterize that
  admissible motion space before expanding components.

The physical layer decides whether energy is conserved, whether an impulse model
is valid, and which constraints are ideal. The structural layer only prevents
unnecessary state from surviving into the target calculation.

=== Fields and circuits as maps, paths, and boundaries

Field problems share several mathematical shapes but not one ontology. A source
may generate a field through a linear map `f=Ku`; a target may then be a linear
functional `L(f)` or quadratic functional `Q(f)`. Elimination gives

$ L(f) = L(K u), quad Q(f) = Q(K u). $

This form can describe dielectric voltage, induced heating, or viscous
dissipation only after the area-specific packet supplies `K`, measures, units, and
regimes. If the field is nonconservative, a path rather than an endpoint becomes
part of the observable. If a finite network has many internal states, the
boundary/hidden partition determines what may be condensed.

=== Waves and oscillations as phase-bearing response

Oscillatory problems are unified at the representation layer: a real sinusoid is
encoded by a complex amplitude so differentiation, propagation, and linear
boundary laws become algebraic. This does not make a wave and a circuit physically
identical. It says that both must preserve phase until the requested observable no
longer depends on it.

The target controls when compression is legal. Average Joule power can consume
`|I_hat|^2`; instantaneous current cannot. Mean torque consumes a relative-phase
pairing; its ripple additionally needs the product phasor. A transient target
forces a return to time-domain modes because the steady phasor deliberately forgot
initial data.

=== Thermodynamics and fluids as constrained processes

In thermal and fluid problems, a state relation, a process path, and a balance law
must not be conflated. A state function may depend only on endpoints, while work or
heat depends on the path. A steady balance may remove storage terms that a
transient target requires. Dimensional coordinates can expose regime variables,
but they cannot generate the constitutive law or its empirical transition value.

The reframing question is therefore not “which universal equation covers this
chapter?” It is:

#quote(block: true)[
  Which physical distinctions can this target safely ignore, and which common
  operation becomes available after they are removed?
]

= The exam-time kernel

== The eight moves

Write three boxes:

#align(center)[*GIVEN* $mid$ *HIDDEN* $mid$ *TARGET*]

Then perform the following moves.

+ *Bind.* Write exactly one target, including instant or average, direction,
   frame, units, and requested branch.
+ *Packet.* List only justified physical laws and their regimes.
+ *Slice.* Trace backward from the target through laws that can reach it.
+ *Gate.* If the slice is one short competent chain, solve it directly.
+ *Diagnose.* Name the first obstruction preventing safe closure.
+ *Operate.* Apply the smallest matching operation to that obstruction.
+ *Return.* Restore every item in the return ledger.
+ *Check.* Substitute into an original law and test a dimension, limit, or
   branch.

== The direct gate

Use the direct route when the proposed framework would merely rename two familiar
equations, introduce a representation used only once, or add more live quantities
than it removes. A correct output of the framework is often

#quote[Direct: the supplied physical-law chain is already shorter.]

For example, a single constant-acceleration calculation needs no relation
compiler. A one-loop RLC phasor equation is already the reduced route. The general
harmonic constructor remains useful for understanding transfer and checking phase,
but its full notation should not be reproduced on that exam problem.

== Unknown-problem search

When a problem does not resemble a memorized pattern, do not guess the chapter and
expand every available law. Search from the observable:

```text
start with target-bearing laws
-> mark unresolved quantities as open ports
-> attach a justified law that connects one port toward a given
-> eliminate and test closure
-> stop at the first complete depth
-> compare complete routes at that depth.
```

Prefer an attachment that connects directly to a given, represents a conservation
or boundary law, introduces fewer new hidden quantities, and has a clear validity
regime. Reject a route that closes algebraically but fails dimensions, signs,
limits, or symbol meaning. If no route closes, identify the missing law or datum;
additional algebra cannot repair missing physics.

= Operator map

#table(
  columns: 3,
  table.header(
    [*Visible obstruction*],
    [*Operation*],
    [*Fast memory line*],
  ),
  [no obstruction],
  [direct gate],
  [do not abstract a one-chain problem],
  [irrelevant relations],
  [target slice],
  [keep only laws that can reach the target],
  [explicit hidden chain],
  [substitution],
  [replace a named hidden quantity immediately],
  [repeated internal exchange],
  [weighted cancellation],
  [choose weights that kill the internal term],
  [event defined in words],
  [event restriction],
  [vanish, transport, restrict],
  [desired response may overshoot a bound],
  [bounded projection],
  [desire, clip, return],
  [endpoints do not determine work],
  [path functional],
  [path first, loop for comparison],
  [magnitude erases phase],
  [harmonic response],
  [freeze one convention and keep phase],
  [two harmonics multiply],
  [harmonic product],
  [mean uses conjugate; ripple does not],
  [coordinates exceed motion freedom],
  [symmetry reduction],
  [solve on admissible motion, then reconstruct],
  [base-unit scale is redundant],
  [dimensional quotient],
  [invariant monomials lie in `kernel(D)`],
  [target is only at terminals],
  [network condensation],
  [eliminate hidden nodes and retain recovery],
)

The frozen eight-card review set consists of the direct gate, target slice, event,
projection, path, harmonic response, harmonic product, and symmetry reduction.
Substitution and cancellation are elementary operations inside the target-slice
card. Dimensional quotient and network condensation are advanced candidate tools:
they are exact and reusable, but current work does not show that learners execute
them faster under exam time.

= Core operators and complete examples

Every route below has the same admission contract. This ledger separates the
physics that must be remembered from the computation newly constructed from it.

#table(
  columns: (1.15fr, 1.45fr, 1.55fr, 1.25fr, 1.35fr),
  table.header([*Route*], [*Remember*], [*Construct*], [*Return / check*], [*Assume / refuse*]),
  [satellite slice], [central-force energy and angular momentum], [eliminate invariant hidden variables], [physical turning root and bound regime], [tangential impulse; refuse noncentral force or time target],
  [pendulum event], [energy and acceleration components], [vanish, transport, restrict], [reached arc and traversal], [ideal pendulum; refuse roots outside the motion],
  [rough-wall impact], [restitution and Coulomb impulse bound], [project desired tangential impulse], [outgoing speed, angle, branch], [point mass and fixed wall; refuse rotation or multicontact],
  [induced-voltage path], [Faraday law and oriented line work], [compare paths by their closed loop], [wire or probe path and sign], [refuse endpoint voltage without path or potential certificate],
  [harmonic response], [linear fixed-frequency laws], [retain one complex amplitude convention], [real signal, phase, and boundary], [refuse transient, nonlinear, or underdetermined response],
  [harmonic product], [same-frequency real-signal convention], [split mean and twice-frequency channels], [power balance and requested channel], [refuse mixed frequencies without extending the spectrum],
  [hinged hexagon], [rigid-link constraints and impulse momentum], [parameterize the admissible symmetric motion], [reconstruct every vertex velocity], [refuse broken geometry, loading, or symmetry],
  [dimensional quotient], [dimension assignments], [compute the nullspace of the dimension map], [dimensionless coordinates], [refuse absent or oversized nullspace within budget],
  [boundary condensation], [linear balance matrix and boundary partition], [eliminate the invertible hidden block], [terminal law plus hidden-state lift], [refuse an unproved or singular hidden block],
  [sparse elimination], [reciprocal local linear balance], [pivot locally with a fill-aware order], [reverse recovery and boundary law], [refuse a zero pivot or a route whose setup costs more],
)

== Three elementary hand patterns

The specialist cards are unnecessary unless these smaller operations fail to close
the target slice.

=== Explicit substitution

If one law defines a hidden quantity in terms of givens, remove that name at once:

$ h = f(g), quad o = Phi(h) quad arrow.r.long quad o = Phi(f(g)). $

This is the ordinary engine behind constitutive chains. Examples include inserting
`I=U/R` into `P=I^2R`, an image distance into a magnification law, or a field shape
into an energy integral. The reduction is useful only if `h` is not itself a
requested intermediate and substitution does not create a worse expression.

=== Weighted cancellation

Suppose two supplied balances contain an internal exchange `q`:

$ A: a_1 x + b_1 q = c_1, quad B: a_2 y + b_2 q = c_2. $

Choose weights `lambda_1,lambda_2` from

$ lambda_1 b_1 + lambda_2 b_2 = 0. $

Then `lambda_1 A+lambda_2 B` removes `q` without calculating it. The weights are
not a memorized trick; the cancellation condition constructs them. Internal-force
cancellation in center-of-mass motion, junction-current cancellation, and internal
heat exchange in a combined energy balance share this pattern.

Return carefully: cancellation computes a global observable but may discard the
internal exchange needed by a later stress, temperature-difference, or component
target. Rebuild the target slice when the requested quantity changes.

=== Turning or boundary relation

At a turning point, interface, or constrained boundary, a differential statement
often becomes an algebraic relation:

#table(columns: 2, [*Event*], [*Vanishing component*], [turning point], [radial or coordinate speed], [interface], [required field component], [steady node], [net flux or force minus source], [contact loss], [normal reaction])

Insert this defining relation before solving the full trajectory or field. The
operation is cheap, but the return must still identify which turning point,
interface side, or traversed event the algebraic solution represents.

== Target slice and elimination: the satellite orbit

*Capability.* Compute the requested apocentre without carrying the entire orbit
as a time-dependent trajectory.

*Physical input.* A satellite initially moves on a circular orbit of radius
`R_0`. A tangential impulse multiplies its speed by `alpha`. Let
`rho=R_max/R_0`; the bound outgoing regime is `1<alpha<sqrt(2)`.

After nondimensionalizing the post-impulse energy and angular momentum as `e` and
`l`, the target slice contains only

$ 2 e - alpha^2 + 2 = 0, quad ell - alpha = 0, quad 2 e rho^2 - ell^2 + 2 rho = 0. $

The first two relations explicitly determine the hidden quantities:

$ 2 e = alpha^2 - 2, quad ell = alpha. $

Substitution into the turning relation gives

$ (alpha^2 - 2) rho^2 - alpha^2 + 2 rho = (rho - 1) ((alpha^2 - 2) rho + alpha^2). $

The factorization does not by itself label the roots. The return ledger supplies
their meaning:

- `rho=1` is the known impulse point;
- for `1<alpha<sqrt(2)`, the other root exceeds one and is the apocentre;
- at `alpha>=sqrt(2)`, no finite apocentre exists.

Therefore

$ R_max/R_0 = alpha^2/(2 - alpha^2), quad 1 < alpha < sqrt(2). $ <satellite-apocentre>

@satellite-apocentre is valid only with the branch and regime shown; the
algebraic fraction alone is not the returned observable.

*What was reduced.* A trajectory problem became elimination on three invariant
relations. *What was not reduced.* Conservation laws and physical root meaning
still came from orbital mechanics.

*Refuse the shortcut when.* The force is not central, the impulse is not
tangential as assumed, or the requested observable requires time along the orbit
rather than a turning radius.

== Event restriction: a pendulum condition stated in words

*Obstruction.* “The resultant acceleration is horizontal” is not a supplied time
or angle. It defines an event inside the motion, and an algebraic equation may
contain states that the released pendulum never reaches.

Use the three-line event card:

- *Vanish:* identify the observable component that is zero.
- *Transport:* express it using one event coordinate.
- *Restrict:* retain the reached interval and direction.

For A617 2015 problem 1, let

$ c = cos(phi), quad s = v^2/(g l), quad a = a_y/g. $

with downward vertical acceleration positive. Energy and kinematics provide

$ a = 0, quad s = 2(c - 1/10), quad a = 1 - c^2 - s c, quad 1/10 <= c <= 1. $

Substitution constructs the event relation:

$ 0 = 1 - c^2 - 2(c - 1/10)c quad arrow.l.r.double quad 15 c^2 - c - 5 = 0. $

Thus

$ c = (1 + sqrt(301))/30 quad "or" quad c = (1 - sqrt(301))/30. $

Only the positive root lies on the released arc, so

$ phi = arccos((1 + sqrt(301))/30). $

The restriction is part of the computation, not cleanup after solving. If two
full-state roots survived, “first occurrence” or traversal direction would need to
select the event. If no root survived, the event would not occur.

*Exam use.* Write the three physical relations directly. The event card is a
recognition and branch-control tool; spelling out its general formalism would add
work on this one problem.

== Bounded projection: rough-wall impact

*Obstruction.* The equality `|J_t|=mu J_n` describes saturated sliding friction.
If that impulse would reverse the tangential velocity, the equality has been used
beyond the effect it is meant to produce. The correct response is bounded.

Let `u_n>0` be incoming speed toward a fixed wall and `u_t>=0` tangential speed.
For a nonrotating point particle, Newton restitution constructs

$ J_n = m(1 + e) u_n, quad u_n' = e u_n. $

The tangential impulse desired to arrest slip is

$ J_t^* = -m u_t. $

Coulomb friction permits only `[-mu J_n,mu J_n]`, so the smallest construction is

$ J_t = op("proj")_[-mu J_n, mu J_n](J_t^*), quad u_t' = u_t + J_t/m. $ <impact-projection>

Evaluating the projection exposes the two physical regimes:

The bounded map in @impact-projection, rather than the saturated equality, is the
single construction valid on both regimes.

$ u_t' = cases(0 & "if" u_t <= mu(1+e)u_n, u_t - mu(1+e)u_n & "if" u_t > mu(1+e)u_n). $

Return speed and angle by

$ v' = sqrt((e u_n)^2 + (u_t')^2), quad tan(theta') = u_t'/(e u_n). $

For an incidence speed `v_1` at angle `theta` from the normal, substitute
`u_n=v_1 cos(theta)` and `u_t=v_1 sin(theta)`. The branch boundary is

$ tan(theta) = mu(1 + e). $

*Refuse the card when.* The body rotates, several contacts act simultaneously,
the wall moves, or the friction law is not the point-particle Coulomb model. Those
cases introduce states absent from this return map.

== Path functional: induced voltage

*Obstruction.* An endpoint scalar `U(P,Q)` assumes path independence. A changing
magnetic field can produce `curl(E_ind) != 0`, so two material paths with the same
endpoints can have different line work.

The failed endpoint equality forces the richer observable

$ W[gamma; P arrow.r Q] = integral_gamma bold(E)_"ind" dot dif bold(l). $

For two paths with common endpoints,

$ W[gamma_1] - W[gamma_2] = ∮_(gamma_1 - gamma_2) bold(E)_"ind" dot dif bold(l). $ <path-difference>

If the planar curl is constant, Green's theorem turns path comparison into a
signed-area computation. @path-difference keeps the orientation visible:

$ W[gamma_1] - W[gamma_2] = (op("curl") bold(E)_"ind") A_"signed"(gamma_1 - gamma_2). $

For A14-06, take

$ kappa = (dif B_z)/(2 dif t), quad bold(E)_"ind"(x,y) = (kappa y, -kappa x), quad op("curl") bold(E)_"ind" = -2 kappa. $

Orient the indicated arc and chord from `P=(-a,a)` to `Q=(a,a)`. Direct evaluation
returns

$ W_"arc" = pi kappa a^2, quad L_"arc" = pi a/sqrt(2), quad W_"chord" = 2 kappa a^2, quad L_"chord" = 2a. $

Hence

$ W_"arc" - W_"chord" = kappa a^2(pi - 2). $

The signed area between the paths is `-a^2(pi/2-1)`; multiplying it by
`-2kappa` independently returns the same difference.

For one open wire at zero current, `V_Q-V_P=W_path`. If both paths are resistive
branches with resistance per length `rho`, use

$ U = W_j - I_j rho L_j, quad I_"arc" + I_"chord" = 0. $

Solving these two branch laws gives

$ U = (2 pi kappa a^2(sqrt(2)+1))/(pi+2sqrt(2)), quad I_"arc" = (sqrt(2) kappa a(pi-2))/(rho(pi+2sqrt(2))), quad I_"chord" = -I_"arc". $

*Adaptive return.* If a verified potential satisfies `E=-grad(V)`, every path
returns `W=-(V(Q)-V(P))`; collapse back to the simpler endpoint view. Without a
wire, probe path, or scalar-potential certificate, refuse to invent one endpoint
voltage.

== Harmonic response: preserve phase

*Obstruction.* Squared amplitudes retain energy-like magnitudes but discard the
phase needed for interference, lead/lag, boundary matching, or a value at a
specified point.

Freeze one convention:

$ z quad "represents" quad Re(z exp(i omega t)). $

Then derivatives multiply by `i omega`, propagation contributes phase factors,
and linear boundary or circuit laws become a finite complex system. Return through

$ z = a + i b quad arrow.r quad a cos(omega t) - b sin(omega t). $

For A21-03, the source condition gives incident amplitude
`iA exp(-i theta)`. The fixed denser boundary at `theta=11pi/2` forces reflected
amplitude `iA`. Their sum is

$ z_"total" = 2 i A cos(theta). $

Nodes follow from zero magnitude, antinodes from bounded maxima, and at the point
`theta=4pi` the real signal is

$ -2 A sin(omega t). $

The same representation transfers to a series RLC circuit:

$ Z hat(I) = hat(U), quad Z = R + i(omega L - 1/(omega C)). $

Here the direct phasor equation is already the shortest exam route. The shared
operator explains why wave reflection and circuit response preserve the same
mathematical phase structure without pretending their physical laws are identical.

*Refuse the steady phasor route when.* The target includes transient initial-data
modes, the response is nonlinear, the frequency is not fixed, or boundary data do
not determine a unique harmonic response.

== Harmonic product: mean and ripple

*Obstruction.* Power, torque, and intensity often multiply two same-frequency
real signals. Expanding four trigonometric terms is unnecessary when only the mean
or twice-frequency channel is needed.

Under the same convention, let

$ x(t) = Re(a exp(i omega t)), quad y(t) = Re(b exp(i omega t)). $

Expanding each real part as half the sum of positive- and negative-frequency
components gives

$ x(t)y(t) = Re(a overline(b))/2 + Re((a b/2) exp(2 i omega t)). $ <harmonic-product>

Therefore

Reading @harmonic-product by output channel gives

$ "mean channel" = Re(a overline(b))/2, quad "2ω phasor" = a b/2. $

The conjugate belongs only in the mean channel.

For A23-05, let `K=NBa^2`. The current phasor is

$ hat(I) = -(K omega(omega L + i R))/(R^2 + omega^2 L^2). $

The applied torque is `K i(t)sin(omega t)`, and the sine phasor is `-i`. Applying
the product rule gives

$ tau_"mean" = (K^2 omega R)/(2(R^2+omega^2 L^2)), quad hat(tau)_(2 omega) = (K^2 omega(-R+i omega L))/(2(R^2+omega^2 L^2)). $

The physical return check is power balance:

$ omega tau_"mean" = R abs(hat(I))^2/2. $

Use this card when a channel can be omitted or when it prevents a phase error. On
the complete source problem, the ordinary phasor calculation is already compact;
the general notation is primarily a transfer and checking tool.

== Symmetry-compatible coordinates: the hinged hexagon

*Obstruction.* Six rigid rods appear to require twelve endpoint-velocity
components, but fixed-length constraints and reflection symmetry leave a much
smaller admissible instantaneous motion space.

For A617 2016 problem 3, the symmetry-compatible motion is described by the
opposite horizontal-edge velocities `u` and `v`. For a uniform rod with endpoint
velocities `v_A` and `v_B`, the exact kinetic energy is

$ T_"rod" = m(abs(bold(v)_A)^2 + abs(bold(v)_B)^2 + bold(v)_A dot bold(v)_B)/6. $

Substituting the six constrained endpoint pairs and summing constructs

$ T(u,v) = m(5u^2 - u v + 5v^2)/3. $

The impulse acts on the `u` coordinate and supplies no generalized impulse in the
`v` direction. Thus the conjugate impulsive momentum satisfies

$ p_v = (partial T)/(partial v) = m(-u + 10v)/3 = 0. $

so

$ v = u/10. $

*Return certificate.* Reconstruct every vertex velocity and verify that adjacent
relative velocities are perpendicular to their rods. A reduced energy expression
without this lift is not enough.

*Refuse or enlarge the coordinates when.* Geometry, mass distribution,
constraints, or loading break the assumed reflection symmetry.

= Advanced constructive tools

These tools go beyond the frozen eight-card review set. They demonstrate how a new
operator is constructed from a failure rather than added as another analogy.

== Dimensional quotient

*Capability.* Remove arbitrary base-unit scale while retaining invariant physical
comparisons.

For quantities `x_1,...,x_n`, put their mass, length, time, and current exponents
in the columns of an integer matrix `D`. A monomial

$ Pi(a) = product_i x_i^(a_i). $

changes under unit rescaling by the dimension vector `Da`. The obstruction to
invariance therefore constructs the exact request

$ D a = 0. $

Primitive integer vectors in `kernel(D)` generate dimensionless coordinates. The
unchanged operation returns, for example,

#table(
  columns: 3,
  table.header(
    [*Physical packet*],
    [*Generated coordinate*],
    [*Physics supplied afterward*],
  ),
  [pendulum `T,L,g`],
  [`T^2g/L`],
  [small-angle law sets it to `4pi^2`],
  [fluid `rho,v,L,mu`],
  [`rho vL/mu`],
  [experiment/theory identifies regimes],
  [circuit `t,R,C`],
  [`t/(RC)`],
  [one-time-constant law sets it to `1`],
)

The constructor generates coordinates, not dynamics, constants, or empirical
thresholds. It returns irreducible when the nullspace is zero and should refuse an
oversized basis beyond the available computation budget.

== Boundary-network condensation

*Capability.* Compute only terminal behavior while preserving a route back to
every hidden state.

For an admitted finite linear balance law `Kx=f`, partition boundary variables
`u` from hidden variables `h`:

$ K_"BB" u + K_"BI" h = f_B, quad K_"IB" u + K_"II" h = f_I. $

If `K_II` is invertible, the hidden equation constructs

$ h = -K_"II"^(-1) K_"IB" u + K_"II"^(-1) f_I. $

Substitution into the boundary block returns

$ K_"eff" = K_"BB" - K_"BI" K_"II"^(-1) K_"IB", quad f_"eff" = f_B - K_"BI" K_"II"^(-1) f_I, quad K_"eff" u = f_"eff". $ <network-condensation>

The returned terminal law in @network-condensation transfers across conductance, spring-stiffness, and steady
thermal networks. The area adapter must still construct the correct balance
matrix and justify steady, linear, massless, or other approximations. A singular
or unproved-invertible hidden block blocks unique recovery and must produce a
refusal.

== Sparse local elimination

The block formula proves equivalence but can be poor handwritten execution. If `K`
is reciprocal and a hidden scalar state `h` has a provably nonzero pivot, eliminate
it locally:

$ K'_"ij" = K_"ij" - (K_"ih" K_"hj")/K_"hh", quad f'_i = f_i - (K_"ih" f_h)/K_"hh", quad x_h = f_h/K_"hh" - sum_j (K_"hj"/K_"hh")x_j. $

Only current neighbors of `h` change. Choose the next pivot by least new fill,
then least active-neighbor count; replay the recovery equations in reverse.

On the frozen branched network, center-first elimination creates six fill edges
and nineteen nonzero local updates. Leaf-first elimination creates one fill edge
and five updates, while returning the same boundary law and hidden states.

This is genuine structural reduction, but it is not automatically human-time
reduction. Charging three pivot-choice representation actions gives route ledgers

$ c_"declared" = (1,3,5,19,0,0,1), quad c_"sparse" = (1,3,5,5,0,3,1). $

For positive action weights, sparse execution is cheaper exactly when

$ 3 w_"representation changes" < 14 w_"symbolic actions". $

On a one-hidden-node chain, sparse recognition saves no execution and adds one
choice, so the correct gate is always direct. If no nonzero scalar pivot exists,
the local planner must refuse even when block condensation remains possible.

= Adaptation rather than a frozen grammar

The operator table is not a claim that all future problems fit ten boxes. It is a
method for constructing a new box only when an exact failure demands one.

Use this extension loop:

```text
requested capability
-> shortest existing route
-> calculate its failure
-> retain the distinction that failure erased
-> construct the smallest new operation
-> recover old successful cases
-> transfer unchanged to a different admissible case
-> state a refusal boundary.
```

Path work illustrates the loop. Endpoint voltage failed because equal endpoints
did not give equal work; retaining an oriented path repaired the failure. Bounded
impact illustrates it differently: saturated friction failed by overshooting zero
tangential speed; projection repaired the equality. Neither repair was obtained by
adding an unrelated formula.

For a truly new problem, the solver should first stay in the physical packet and
search the target relation graph. If an existing operation closes the route, use
it. If not, state the concrete obstruction. During an exam, solving directly or
naming a missing datum is preferable to inventing an unverified abstraction.

= How this can reduce exam complexity

Complexity has several components:

$ C_"route" = C_"recognition" + C_"setup" + C_"execution" + C_"physical return". $

A compact middle formula is not enough. An operator is useful when its complete
route does one or more of the following without increasing a more important cost:

- selects fewer relations;
- introduces fewer hidden quantities;
- lowers peak simultaneous equations;
- removes repeated symbolic actions;
- prevents a branch, phase, sign, or regime error;
- yields an intermediate object reusable across subparts;
- makes refusal possible before futile algebra.

The current six-case handwritten audit did not establish a universal speed win:
five competent direct routes were structurally cheaper and one route had a
trade-off. That negative result shapes this manual. The framework aims first to
improve selection, error control, and transfer; it recommends structural execution
only when a gate is satisfied.

== A personal admission rule

When direct and structural routes trade setup for execution, write

$ C_"setup" < Delta C_"execution saving". $

Prefer the structural route only if practice shows that the avoided work is a real
personal bottleneck. Never learn a weight from a fast incorrect attempt. Correct
both routes first; compare complete times on matched variants; keep route order
counterbalanced.

== A four-pass learning cycle

+ *Recognition pass:* identify target, direct gate, obstruction, and refusal
   without completing algebra.
+ *Execution pass:* reproduce one operator with the physical laws supplied.
+ *Transfer pass:* solve an unlabeled changed-context problem and explain which
   meaning must be returned.
+ *Retention pass:* repeat selected problems after a delay, recording the first
   error location.

Use the error labels

$ ("target", "law", "representation", "algebra", "branch", "sign", "unit", "return"). $

These labels tell the learner what to repair. More undifferentiated repetition does
not necessarily repair a target-binding or representation error.

== A worked diagnosis protocol

For an unfamiliar problem, make a diagnosis record before lengthy algebra:

```text
TARGET:    one observable with convention and units
PACKET:    justified laws plus their regimes
SLICE:     target-bearing laws and unresolved open ports
DIRECT?:   shortest closing chain, if one exists
FAILURE:   first reason that chain is unsafe or incomplete
OPERATOR:  smallest repair, or DIRECT/REFUSE
RETURN:    dimensions, branch, sign, boundary, limiting case
```

Consider a new setup in which two different wires connect the same points inside a
changing magnetic field and the target is branch current. The words “same points”
may suggest one voltage, but the packet also says induction. The target-bearing
branch law has an open port for electromotive work. Testing the endpoint shortcut
fails because `curl(E)` is nonzero. That calculated failure selects the path
operator. Each material wire supplies one `W[gamma]`; current conservation joins
them; the return restores orientation and resistance. The route was selected from
the obstruction, not from recognition of a numbered source problem.

Now mutate the target to voltage between the points in a verified electrostatic
field. The endpoint shortcut no longer fails: a scalar potential exists. The
direct gate rejects the path construction. Adaptation therefore means recomputing
the target slice and obstruction, not attaching the same preferred operator to
every superficially related problem.

= What is established and what remains open

== Established within the worktable

- Exact finite relation elimination can preserve target relations and reconstruct
  accepted hidden states on the admitted source packets.
- Event restriction constructs and filters the A15-01 branches.
- Path work repairs endpoint failure on A14-06 and transfers unchanged to A10-06.
- Complex harmonic response preserves phase across one wave and one circuit case.
- Harmonic product returns exact mean and twice-frequency channels on two
  electromagnetic cases.
- Constrained impulse projection returns the arrest/sliding split for the admitted
  point-particle impact.
- Dimensional nullspace and boundary-network condensation are exact reusable
  constructors over their stated finite domains.
- Sparse network ordering reduces fill and local updates on the frozen branched
  bench while preserving boundary and recovery results.

== Not established

- automatic extraction of physical laws from arbitrary prose or diagrams;
- one universal operator or fixed final grammar for all physics;
- general continuous-field, nonlinear, transient, or inequality reasoning;
- universal handwritten savings;
- measured learner speed, accuracy, retention, or unfamiliar-problem transfer.

== The human-evidence bridge

Mathematics can prove that two routes return the same observable and a structural
ledger can count their actions. Neither observation identifies how quickly a
person recognizes the route, how reliably it is learned, or whether it transfers
after delay. Those claims require independent route-key review and observations of
real learners on matched correct attempts, with timing, retention, and unseen
transfer kept distinct.

This bridge is a boundary on claims, not a prerequisite for using the review
method. The present material can be studied and criticized now. It simply does not
rename finite instructions or lower symbolic counts as demonstrated cognitive
improvement.

= Final memory page

The framework can be compressed to five questions:

+ What exactly is requested?
+ What is the shortest justified physical-law chain to it?
+ If that chain does not close safely, what is the first obstruction?
+ Which smallest operation removes it without losing meaning?
+ What must be restored before the result is a physics answer?
+ Is the complete route actually cheaper than direct work?

And one adaptive rule:

#quote(block: true)[
  Climb only until a shorter valid computation appears; descend whenever the
  requested physical meaning cannot be recovered.
]

For rapid review, continue with #link("exam-kernel.typ")[the two-page exam kernel], then
attempt #link("mixed-drills.md")[the mixed drills] before consulting
#link("mixed-drill-key.md")[the route and answer key]. The normalized operator reference
is in #link("operator-cards.md")[operator-cards.md].

= Source and reproducibility trail

This manual is a reader-facing projection of bounded constructions in the parent
worktable. Detailed contracts, certificates, limitations, and executable entry
points remain in the corresponding research results:

- #link("research-worktable/results/event-relation-branch-constructor-12.md")[event relation and branch construction];
- #link("research-worktable/results/path-functional-reconstruction-13.md")[path-functional reconstruction];
- #link("research-worktable/results/exact-harmonic-response-15.md")[exact harmonic response];
- #link("research-worktable/results/harmonic-product-return-16.md")[harmonic-product return];
- #link("research-worktable/results/frictional-impact-projection-18.md")[frictional-impact projection];
- #link("research-worktable/results/exact-dimensional-quotient-25.md")[dimensional quotient];
- #link("research-worktable/results/exact-network-condensation-26.md")[boundary-network condensation];
- #link("research-worktable/results/sparse-network-elimination-order-27.md")[sparse network ordering];
- #link("research-worktable/results/deductive-network-human-boundary-28.md")[deductive human-cost boundary].

The source-bound corpus inventory is in the
#link("research-worktable/sources/a617-local-corpus.md")[A617 local-source audit]. The
#link("research-worktable/computation/README.md")[computation guide] gives the canonical executable
routes. These artifacts support the exact and bounded claims above; they do not
alter the open human-evidence status.
