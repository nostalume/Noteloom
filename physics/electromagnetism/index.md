# Electromagnetism

Classical electromagnetism is a local field theory of charges, currents, and two
coupled fields. Its central equations simultaneously describe electrostatics,
magnetism, induction, radiation, and light. This note uses SI units and begins
with the microscopic vacuum equations; material response is introduced later as
a modeling layer.

Prerequisites are vector calculus, ordinary and partial differential equations,
and special relativity for the final section.

## Sources must be conserved

Charge density \(\rho(\mathbf x,t)\) and current density
\(\mathbf J(\mathbf x,t)\) are not independent. Local charge conservation is

\[
\frac{\partial\rho}{\partial t}+\nabla\cdot\mathbf J=0.
\]

Integrating over a fixed volume says that charge can change inside only by
flowing through the boundary. Any proposed source model should pass this test
before a field equation is solved.

## Maxwell's equations

The electric and magnetic fields obey

\[
\begin{aligned}
\nabla\cdot\mathbf E &= \frac{\rho}{\varepsilon_0}, &
\nabla\cdot\mathbf B &= 0,\\
\nabla\times\mathbf E &= -\frac{\partial\mathbf B}{\partial t}, &
\nabla\times\mathbf B &= \mu_0\mathbf J
+\mu_0\varepsilon_0\frac{\partial\mathbf E}{\partial t}.
\end{aligned}
\]

The divergence equations constrain a field on each time slice. The curl
equations determine how changing electric and magnetic fields generate one
another. Taking the divergence of the Ampère--Maxwell equation reproduces the
continuity equation, so charge conservation is built into the field dynamics.

A particle of charge \(q\) and velocity \(\mathbf v\) responds through the
Lorentz force

\[
\mathbf F=q(\mathbf E+\mathbf v\times\mathbf B).
\]

Maxwell's equations determine fields from sources; the Lorentz force determines
how those fields exchange momentum with matter.

## Potentials and gauge freedom

Because \(\nabla\cdot\mathbf B=0\), write

\[
\mathbf B=\nabla\times\mathbf A.
\]

Faraday's law then permits

\[
\mathbf E=-\nabla\phi-\frac{\partial\mathbf A}{\partial t}.
\]

The potentials are not unique. For any smooth scalar \(\chi\),

\[
\mathbf A\mapsto\mathbf A+\nabla\chi,
\qquad
\phi\mapsto\phi-\frac{\partial\chi}{\partial t}
\]

leaves \(\mathbf E\) and \(\mathbf B\) unchanged. A gauge condition chooses a
representative; it does not add a physical field.

## Static limits

When sources are time independent, electric and magnetic problems decouple.
Electrostatics gives

\[
\nabla^2\phi=-\frac{\rho}{\varepsilon_0},
\qquad \mathbf E=-\nabla\phi,
\]

so boundary conditions are as important as the source. Green functions are a
systematic way to encode both the differential operator and those boundary
conditions.

For steady currents, \(\nabla\cdot\mathbf J=0\) and

\[
\nabla\times\mathbf B=\mu_0\mathbf J.
\]

The Biot--Savart law is a solution in unbounded space, not a replacement for the
local Maxwell equation.

## Energy flow

Combining the curl equations with the Lorentz power density
\(\mathbf J\cdot\mathbf E\) gives Poynting's theorem,

\[
\frac{\partial u}{\partial t}+\nabla\cdot\mathbf S
=-\mathbf J\cdot\mathbf E,
\]

where

\[
u=\frac12\left(\varepsilon_0E^2+\frac{B^2}{\mu_0}\right),
\qquad
\mathbf S=\frac{1}{\mu_0}\mathbf E\times\mathbf B.
\]

This equation is the reliable way to reason about where electromagnetic energy
is stored, how it crosses a boundary, and how it is transferred to matter.

## Waves are a consequence, not an extra postulate

In a source-free region, taking another curl yields

\[
\nabla^2\mathbf E-rac{1}{c^2}
\frac{\partial^2\mathbf E}{\partial t^2}=0,
\qquad
c=\frac{1}{\sqrt{\mu_0\varepsilon_0}},
\]

with an analogous equation for \(\mathbf B\). Plane-wave solutions are
transverse: \(\mathbf E\), \(\mathbf B\), and the propagation direction are
mutually perpendicular in vacuum. Interfaces then select reflection,
transmission, or guided modes through Maxwell's boundary conditions.

## Matter is an effective description

Macroscopic media replace microscopic charge motion by polarization
\(\mathbf P\) and magnetization \(\mathbf M\):

\[
\mathbf D=\varepsilon_0\mathbf E+\mathbf P,
\qquad
\mathbf H=\frac{\mathbf B}{\mu_0}-\mathbf M.
\]

Relations such as \(\mathbf D=\varepsilon\mathbf E\) are constitutive models,
not additional universal Maxwell equations. They may depend on frequency,
position, field strength, and past history. Dispersion and absorption therefore
belong to the response model and must be checked against causality and energy
balance.

## Relativistic organization

Electric and magnetic fields are frame-dependent parts of one antisymmetric
field tensor. Written covariantly, Maxwell's equations separate into a sourced
equation and a geometric identity. This explains why magnetism appears when an
electric configuration is viewed from a moving frame and why the four-current
must satisfy a continuity equation.

The print companion [notes.typ](notes.typ) contains longer electrostatic,
magnetic, tensor, and radiation calculations.

## Detailed notes

- [Green functions in electrostatics](green-functions.md)
- [Magnetostatics](magnetostatics.md)
- [Electromagnetic media](media.md)
- [Electromagnetic field tensor](field-tensor.md)
- [Waves and waveguides](waves-and-guides.md)

## References and next steps

- David Tong, [Lectures on Electromagnetism](https://www.damtp.cam.ac.uk/user/tong/em.html).
- MIT OpenCourseWare, [8.02 Electricity and Magnetism](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/).

Good next additions are one boundary-value problem, one radiation calculation,
and one dispersive-medium example, each with assumptions and limiting checks
made explicit.
