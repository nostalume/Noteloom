# Analytical Mechanics

Analytical mechanics is a language for dynamics. Instead of resolving every
force into Cartesian components, it describes a system by its possible
configurations and asks how a trajectory through configuration space is
selected. The same language exposes constraints, symmetries, conserved
quantities, and the bridge to quantum mechanics.

This note assumes Newtonian mechanics, multivariable calculus, and ordinary
differential equations. Repeated indices are summed. A dot means a time
derivative.

## Configuration before equations

A system with \(n\) independent degrees of freedom has generalized coordinates

\[
q = (q^1,\ldots,q^n).
\]

Coordinates label configurations; they need not be lengths or angles, and they
need not form a globally valid chart. A holonomic constraint
\(f_a(q,t)=0\) removes independent directions from configuration space. The
main practical advantage of generalized coordinates is that ideal constraint
forces can often be eliminated before writing the equations of motion.

For a conservative particle system, the Lagrangian is commonly

\[
L(q,\dot q,t)=T(q,\dot q,t)-V(q,t),
\]

but the formalism needs only a function \(L\) whose stationary curves describe
the dynamics. It is the action

\[
S[q]=\int_{t_1}^{t_2}L(q,\dot q,t)\,dt
\]

that is varied, with the endpoint configurations held fixed.

## From stationary action to motion

Perturb a path by \(q^i(t)\mapsto q^i(t)+\epsilon\eta^i(t)\), where
\(\eta^i(t_1)=\eta^i(t_2)=0\). To first order,

\[
\delta S
=\int_{t_1}^{t_2}
\left(
\frac{\partial L}{\partial q^i}\eta^i
+\frac{\partial L}{\partial \dot q^i}\dot\eta^i
\right)dt.
\]

Integrating the second term by parts removes \(\dot\eta^i\). Since the remaining
variations are arbitrary in the interior, a physical path obeys

\[
\frac{d}{dt}\frac{\partial L}{\partial\dot q^i}
-\frac{\partial L}{\partial q^i}=0.
\]

The action is stationary, not necessarily minimal. This distinction matters for
long trajectories and for systems with conjugate points.

### Example: a plane pendulum

For a bob of mass \(m\) on a rigid rod of length \(\ell\), choose the angle
\(\theta\) as the only coordinate:

\[
L=\frac12m\ell^2\dot\theta^2-mg\ell(1-\cos\theta).
\]

The Euler--Lagrange equation gives

\[
\ddot\theta+\frac{g}{\ell}\sin\theta=0.
\]

The constraint has disappeared from the equation because it was built into the
coordinate choice.

## Symmetry produces conservation laws

Suppose an infinitesimal transformation

\[
q^i\mapsto q^i+\epsilon X^i(q,t)
\]

changes the Lagrangian only by a total derivative,
\(\delta L=\epsilon\,dF/dt\). On solutions of the Euler--Lagrange equations,

\[
J=\frac{\partial L}{\partial\dot q^i}X^i-F
\]

is conserved. This is the working form of Noether's theorem for point
transformations.

The familiar cases are structural rather than accidental:

- spatial translation symmetry gives linear momentum;
- rotational symmetry gives angular momentum;
- time-translation symmetry gives energy when \(L\) has no explicit time
  dependence.

A coordinate absent from \(L\) is cyclic, so its conjugate momentum is constant.
This is the simplest local manifestation of the symmetry statement.

## Hamiltonian structure

Define canonical momenta

\[
p_i=\frac{\partial L}{\partial\dot q^i}.
\]

When the velocity Hessian of \(L\) is nonsingular, the velocities can be written
in terms of \((q,p,t)\). The Legendre transform

\[
H(q,p,t)=p_i\dot q^i-L(q,\dot q,t)
\]

then yields the first-order system

\[
\dot q^i=\frac{\partial H}{\partial p_i},
\qquad
\dot p_i=-\frac{\partial H}{\partial q^i}.
\]

These equations evolve a point in phase space. They do not merely repackage the
Euler--Lagrange equations: they make canonical transformations, phase-space
volume, and the relation between generators and conserved quantities explicit.

For functions \(f(q,p,t)\) and \(g(q,p,t)\), define

\[
\{f,g\}
=\frac{\partial f}{\partial q^i}\frac{\partial g}{\partial p_i}
-\frac{\partial f}{\partial p_i}\frac{\partial g}{\partial q^i}.
\]

Evolution becomes

\[
\frac{df}{dt}=\frac{\partial f}{\partial t}+\{f,H\}.
\]

Thus \(f\) is conserved precisely when its explicit time dependence and its
Hamiltonian flow cancel.

## Where rigid-body dynamics fits

A rigid body's configuration contains a translation and a rotation. After the
center-of-mass motion is separated, its rotational kinetic energy is

\[
T_{\mathrm{rot}}=\frac12\boldsymbol\omega^{\mathsf T}
I\boldsymbol\omega,
\]

where \(I\) is the inertia tensor in a body-fixed frame. This is an application
of the same configuration-space method, but rotations live on the group
\(SO(3)\), not in an unconstrained three-component vector space. That geometric
fact explains why body-frame angular velocity and angular momentum need not be
parallel and why Euler's equations contain cross terms.

The print companion [notes.typ](notes.typ) develops coordinates, rotating
frames, rigid bodies, Hamilton--Jacobi theory, and problem work. The separate
[Galilean symmetry study](galilean-symmetry.typ) treats Lie groups, Noether
theory, and rigid-body reduction in greater depth.

## References and next steps

- Iain Stewart, [MIT 8.09 Classical Mechanics III lecture notes](https://ocw.mit.edu/courses/8-09-classical-mechanics-iii-fall-2014/pages/lecture-notes/).
- David Tong, [Lectures on Classical Dynamics](https://www.damtp.cam.ac.uk/user/tong/dynamics.htm).

Natural continuations are small oscillations, canonical transformations,
Hamilton--Jacobi theory, action--angle variables, perturbation theory, and
geometric mechanics. Each should be added through a worked system rather than
as an isolated formula catalogue.
