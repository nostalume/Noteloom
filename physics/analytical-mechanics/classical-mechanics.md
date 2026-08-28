# Classical Mechanics

## Common Objects

Ideal Smooth/Rough Surface: Exerts only a normal force. Prevents motion perpendicular to the surface. As a restriction, it won't impede tangential force because it doesn't affect motion along itself. However, in rough surface, normal force imply a friction force opposes motion with magnitude related to the coefficient of normal force.

Ideal Regid Body: An object with size and shape, where the distance between any two points within the body remains constant regardless of applied forces. So there's no inner force because no translation between two points. While point motion will affect others. $v = v_0 + \omega \times (r - r_0)$ in a certain frame for point $r_0$ related to any point $r$.

Ideal String/Rope: It's inextensible but flexible. So in taut state, it can only apply tension to resist taut. Notice it's tangential otherwise will apply a torque to move string around which is impossible. For a massless string, any acceleration is impossible in $F = T_2 - T_1$, so $T_2 = T_1$ in any points. Usually a condition to analysis end points.

Ideal Pulley: A wheel that can rotate freely about a fixed axle, used to change the direction of a string. Massless and frictionless. So the tension of string will be tangential to the pulley. Because of massless property, $I = 0$, so $T_1 \times R = T_2 \times R$, results $T_1 = T_2$.

Ideal Support:

Pin Joint/Hinge: Prevents translation at the location of the pin. Allows rotation about the pin axis.

Fixed Support (Clamp/Cantilever End): Prevents all translation and all rotation at the point of fixation. It means to apply counteract torque and moment.

Roller Support: Prevents translation perpendicular to the surface it's on. Allows translation parallel to the surface and allows rotation. Coincide to Ideal Surface.

## Force analysis

Contact forces are primarily constraint forces that prevent the objects from interpenetrating or to resist relative motion between their surfaces at the point of contact. The nature of the contact force depends on the properties of the idealized surfaces or connections involved.

Consider the tangent plane of two objects, which is the minial restriction of interpenetration. If they contacts, two tangent plane will be in coincidence otherwise it will cause interpenetration which is unstable.

Edge cases:

points and surface: points has no or any possible tangent plane, so the common tangent plane would the surface.(Usually stick end points or sharp object).

### Analysis in Plane

We can translate force along its direction on a rigid body, otherwise, there's a torque because $r \times F \neq 0$ for the new position vector.

Given a reference point, we has the force apply to the rigid body can be moving around the body and it's torque on the body. So the force can be sum in one point and consider all torque independently.

### Positive and Negative

First determine x-y directions as a upwards or positive.

Then based on x-y, we form a reference system, assume every unknown force or torque on positive direction to simplify burden. Then for the relations of force/acceleration or/and torque/angular acceleration, we identify the change on positive or negative to get their relation; for relations between objects with restriction, we does the same way.

**Example**:
Assume x-y system with x right, y up. If the acceleration of a roller is right, and the rotation is anticlockwise(which is positive direction), then we ger $-\alpha R = a$ because rotation induce a left acceleration, so even **both quantity is positive, their relation isn't positive always**.

Assume a rope with a pulley connect two particle with one end in x, and another in -y. Then the relation is $a_1 = - a_2$ because one particle move in x will results another on -y.

### Static

Consider a torque on a rigid body:
Torque Translation:
$$
\sum_i (r_i + r_0) \times F_i = \sum_i (..) + \sum r_0 \times F_i
$$

In static case: $\sum_i F_i = 0$, so we can see that we can choose arbitrarily a reference point as frame to determine torque sum as zero.

Usually, if there's only 3 forces on a rigid body, notice that we take a reference point on the intersection of two forces direction line, then the third force must counteract other two force, form a triangle in vector summation, and it's torque must be zero otherwise there's a rotation, so it's force direction line must pass the reference point.

**We conclude that in 3 forces on a rigid body, 3 forces has triangle summation and their direction line must pass one point.**

---

Consider a system:

$$
\delta S= 0 \\
\delta (\frac{1}{2} m \dot{r}^2 - V) = 0 \\
m \dot{r} \delta \dot{r} - \delta V = 0 \\
\\- m \ddot{r} \delta{r} + \delta r K = 0 \quad K = - \frac{\partial V}{\partial r}
$$

We don't consider any constraint force, which is in vain in $\delta S$. It's the direct formulation of $\delta Z = 0$.

If we analyze one object with external force applied.
We get the answer:
$$
(K - m \ddot{r} + Z)\delta r = 0
$$
in static:
$$
(K + Z)\delta r = 0 \\
\delta W = 0
$$

Usually, we omit consideration of those known constraint force which contributes nothing.

### Dynamics

Usually, to deal with rigid body rotation, to seek a point speed on rigid body in static reference frame is unrealistic.

We decompose the speed of the point to two part:

Based on $r = r_0 + r'$, we get $v = v_0 + v' + \omega \times r'$.

Different frame transformation results(without restriction of frame):

$$
v_{PO} = v_{\Sigma O} + v_{P \Sigma} + \omega_{O} \times r_{P \Sigma} \\
v_{P \Sigma} = v_{\Theta \Sigma} + v_{P \Theta} + \omega_{\Sigma} \times r_{P \Theta} \\
v_{PO} = v_{\Sigma O} + v_{\Theta \Sigma} + v_{P \Theta} + \omega_{\Sigma} \times r_{P \Theta} + \omega_{O} \times r_{P \Sigma} \\
= ... + \omega_{\Sigma} \times r_{P \Theta} + \omega_{O} \times (r_{P \Theta} + r_{\Theta \Sigma}) \\
$$

Notice
$$
v_{\Theta O} = v_{\Sigma O} + v_{\Theta \Sigma} + \omega_{\Sigma} \times r_{\Theta \Sigma}
$$

So
$$
v_{PO} = v_{\Theta O} + v_{P \Theta} + (\omega_{\Sigma} + \omega_{O})\times r_{P \Theta}
$$

Suppose the reference point is on the rigid body, notice the relative speed of them is zero.

**Any vector is invariant in frame change rather the expression changes among different basis.**

$v = v_0 + \omega \times r'$, is a mixed component of $v_0$ in static frame and $\omega \times r'$ in co-rotation frame, or you can express in static term as $\omega \times (r_p - r_c)$ with a frame change. So there are two ways to understand this, first is due to the rotation based on frame; second is due to rotation based on point(**it's so common that we omit the existence of the frame rotation of reference pt $r_c$**, and represent in original frame).

The kinematic energy is:
$$
\frac{1}{2} m_i (v_p + \omega \times r_i)^2 = \frac{1}{2}m_i (v_p^2 + 2 v_p \cdot \omega \times r_i + (\omega \times r_i)^2)
$$

If the $r_i$ is the relative position to $r_c$, then $m_i r_i = 0$, so (be careful!!), $K = \frac{1}{2}M v_c^2 + \frac{1}{2} \omega \mathbf{I}_c \omega^T$

Also we could get $\mathbf{L} = \mathbf{L}_c + \mathbf{L}_i$. Notice that $\mathbf{L}_i = \mathbf{r}_{i|c} \times m_i (\omega \times r_{i|c})$ which means in O frame, $r_i$ is only changed by purely rotational effect, we get $\mathbf{L}_i = \mathbf{I}_{c} \omega$. However, it's always workable in $r_c$. However, you can't expand $\mathbf{L} = \mathbf{I}_{O} \omega_{O}$!

---

Example:

Often choose $r_0$ as $r_c$, for example, the point speed of a roller in a no-slip rotation would be $v_{p} = v_c + \omega \times r_{pc}$, in 2 dimension, we have $\omega \times r_{pc} = \omega r_{pc}$, $v_{p} = v_c + \omega r_{pc}$. This is so common that we usually omit the step.

Another way to understand is to decompose $r' = r_{p} - r_{0}$. Then if we seek a point that $v_0 = 0$, therefore $v = \omega \times (r_{p} - {r_0})$. In 2 dimension, it's always possible to find the point based on 2 other pts, suppose $\omega$ point out of the plane, the pt is the intersection of normal line of 2 other pts velocity. In no-slip roller, we know that the bottom pt has $v = 0$ due to restriction $|v| = |\omega R|$ and $v = v_c - \omega R = v - \omega R = 0 $. For example: $v_{top} = \omega (r_{top} - r_{bottom}) = 2\omega R$.

Notice, $v_c$ in certain frame could also be expanded as $v_c + \omega_{O} \times r_c$ due to frame rotation existence.

---

Example:
consider a cuboid with $(2a,2b,2c)$, initial position in $S_{lab}$ original position.

Rotation axis is in $S_{lab}$ z axis. But axis rotates around $S_{lab}$ y axis. Second, the position of axis translates in $S_{lab}$ x axis, $x(t) = vt$.

First in $S_{cm}$:
$$
\frac{1}{3}M
\begin{bmatrix}
 b^2 + c^2 & 0 & 0 \\
 0 & a^2 + c^2 & 0 \\
 0 & 0 & a^2 + b^2 \\
\end{bmatrix}
$$

An easy misunderstanding will occur based on translation.

Ones may naively want to take account of translation.

$$
\mathbf{I}_{d, lab} =
\begin{bmatrix}
 0 & 0 & 0 \\
 0 & (vt)^2 & 0 \\
 0 & 0 & (vt)^2 \\
\end{bmatrix}
$$

$$
\mathbf{I'}(t) = ... + I_{d,lab} = \mathbf{I}_{cm} + M(\mathbf{d}_{cm}^2 \mathbf{E} - \mathbf{d}_{lab} \mathbf{d}_{lab}^{T}) \\
$$

Notice, the translation part not only dispensable, but also **wrong**, as we know $r_c \times p_c$ results zero. And $\mathbf{L}_{O} \neq \mathbf{I}_{O} \omega$! It works if and only if the frame contains solely rotation effect!

We should assume below $S_{lab}$ and $S_{cm}$ in the same reference point without translation.

Then deal with rotation of axis, which is on the y axis which is the rotation effect of $S_{lab}$:

$$
\mathbf{R}(t) =
\begin{bmatrix}
 cos \Omega t & 0 & sin \Omega t \\
 0 & 1 & 0 \\
 (- sin \Omega t) & 0 & cos \Omega t \\
\end{bmatrix}
$$

$$
\mathbf{I}_{lab}(t) = \mathbf{R}(t)\mathbf{I}'(t)\mathbf{R}^{T}(t)
= \mathbf{R}(t)\mathbf{I}_{cm}\mathbf{R}^{T}(t)
$$

We can reversely take the operation by reviewing $S_{cm}$ first.

Here, we know in $S_{cm}$(co-rotation in rotation) is a rotation reference with:
$$
\bold{\omega} =
\begin{bmatrix}
 0 \\
 \Omega \\
 \omega_{spin} \\
\end{bmatrix}
$$

$$
\mathbf{L}_{cm} = \mathbf{I}_{cm} \bold{\omega} \\
= \frac{1}{3} M
\begin{bmatrix}
 0 \\
 \Omega (a^2+c^2) \\
 \omega_{spin} (a^2+b^2) \\
\end{bmatrix} \\
$$
$$
\mathbf{L}_{lab} = \mathbf{R}(t) \mathbf{L}_{cm} \\
= \frac{1}{3} M
\begin{bmatrix}
 \omega_{spin}(a^2+b^2) sin\Omega t \\
 \Omega(a^2+c^2) \\
 \omega_{spin}(a^2+b^2) cos \Omega t \\
\end{bmatrix}
$$
We can take derivative to get $\bold{\tau}_{lab}$. Or by transformation!
$$
\bold{\tau}_{cm} = \frac{d \mathbf{L}_{cm}}{d t} + \omega_{body|lab} \times \mathbf{L}_{cm} \\
\bold{\tau}_{lab} = \mathbf{R}(t) \bold{\tau}_{cm}
$$

We can see beside the rotation may occurs in $v_c$, the solely rotation effect comes from the static and co-rotation(relatively static to rigid body) reference frame of the same point, which we choose cm to ease burden. However, in general transformation of the co-rotation frame isn't simple, we use principal axis and euler angle to deal with it. $\phi, \theta, \psi$ could be expanded in co-rotation reference frame.

The workflow would be:

- choose $r_c$ (it won't restrict any reference frame direction).
- choose arbitrarily static reference frame.
- transform co-rotation(relatively static to rigid body) frame as a new co-rotation frame by principal axis.
- Then giving euler angle, we know how to decomposed parameters to co-rotation frame.
- exploit answer by dynamic relation.

$$
\tau_{cm} = \mathbf{I}_{cm} \dot{\omega}_{cm} + \omega_{cm} \times (\mathbf{I}_{cm} \omega_{cm})
$$

Even in static frame we don't have second term, but actually we need to take derivative of $\mathbf{I}_{O}(t)$! So usually we apply in co-rotation frame.

## Orbit

$$
\frac{1}{2}m(\dot{r}^2 + r^2 \dot{\theta}^2) - \frac{k}{r} = E
$$

Take $mr^2\dot{\theta} = J$
$$
\frac{1}{2}m\dot{r}^2 + \frac{J^2}{2mr^2} - \frac{k}{r} = E \\
$$

Take $\dot{r} = 0$
$$
\frac{J^2}{2mr} - k = Er \\
$$

Now back to case where:
$$
r^2 + \frac{k}{E}r - \frac{J^2}{2mE} = 0
$$

We know that there's two root:
$$
r_1 + r_2 = - k/E \\
a = \frac{-k}{2E} \\
r_1r_2 = \frac{-J^2}{2mE} = a^2(1-(\frac{c}{a})^2) \\
\frac{c}{a} = \epsilon
$$

We can see if $r_1 = r_2 = r$
$$
r = \frac{-k}{2E} \\
r^2 = \frac{-J^2}{2mE} \\
r = \frac{J^2}{mk} \\
$$
Now back to:
$$
a^2 = \frac{k^2}{4E^2} \\
1-\epsilon^2 = \frac{2J^2E}{mk^2} = \frac{-J^2}{mka}
$$
So we get the form of kepler third law:
$$
\pi^2 a^2 b^2 = \pi^2 a^4(1-\epsilon^2) \\
= \pi^2 a^4 \frac{-J^2}{mka} \\
= \pi^2 a^3\frac{-J^2}{mk} \\
= \frac{(JT)^2}{4m^2}
$$

$$
T^2 = a^3\frac{4m\pi^2}{k}
$$
