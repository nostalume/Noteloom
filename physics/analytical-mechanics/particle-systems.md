---
title: 理论力学第二章
markmap:
  colorFreezeLevel: 2
---

## Particle System

### Force

#### Internal Force: force exert by each particles for other particles

- **Meaning**: $F^{(i)}_{ij} + F^{(i)}_{ji} = 0$

- **Conclusion**:
  The sum of internal force for a system is zero.
  $F^{i} = \sum_{i} \sum_{j,j \neq i} F_{ij}^{(i)} = 0$

#### External Force: force exert outside system

#### Center of Mass: mean of position of particles

- **Meaning**: $\vec{r}_c = \sum_i m_i \vec{r}_i/\sum_i m_i$

- **Deduction**:
$\vec{\dot{r}}_c = \sum_i m_i \vec{\dot{r}}_i/\sum_i m_i$
$\vec{\ddot{r}}_c = \sum_i m_i \vec{\ddot{r}}_i/\sum_i m_i$
$x_{c\,i} = \int_\Omega \rho x_i dV / \sum_i \rho dV $

## Momentum

- **Description**: $\frac{d\vec{p}}{dt} = \sum_i \bm{F}^{(e)}_i$

- **Conservation**:
if $\sum_i \bm{F}^{(e)}_i = 0$
then $\frac{d\vec{p}}{dt}=0 \quad \vec{p} = constant$

## Angular Momentum

- **Description**: $\frac{d}{dt}\sum_i(r \times \frac{dp_i}{dt}) = \frac{d}{dt}\sum_i J_i = \sum_i(r_i \times \bm{F}_i^{(e)} )= \sum_i M_i$

- **Conservation**:
if $\frac{dJ}{dt} = 0$
then $J = constant$

- **Deduction**: On center of Mass
($r'$ means related to cernter of Mass)
$\frac{d}{dt}\sum_i(r' \times \frac{dp'_i}{dt}) = \sum_i(r'_i\times \bm{F}_i^{(e)})$

## Kinetic Energy

- **Description**: $dE_k = \sum_i (\bm{F}^{(e)}_i + \bm{F}^{(i)}_i)\cdot dr_i$

- **Conservation**:
if external force is conservative force
then $E_k+E_p = E = constant$

- **Deduction**: König theorem
($r'$ means related to cernter of Mass, $r_c$ means the position of center of Mass)
$E_k = \frac{1}{2}m \dot{r}_c^2 + \frac{1}{2}\sum_i m_i \dot{r}'^2_i$

- **Deduction**: On center of mass
($r'$ means related to cernter of Mass)
$dE_k = \sum_i (F_i^{(e)} + F_i^{(i)})\cdot dr'_i$

## Application

### Lab and Center of Mass System of Coordinates

- **Description**:
In scattering or collision, we want to describe such two particle system easily.

- **Lab**:
System of Coordinates which is stable for one of particle.

- Center of Mass:
System of Coordinates which is relative to center of mass.

- **Relation**:
($u$ is velocity of center of mass, $u'_1$ is velocity of particle 1 relative to center of mass)
$tan \, \theta_{lab} = \frac{u'_1 sin\,\theta_{c}}{u'_1cos \theta_c+u}$

- **Deduction**:
$tan \, \theta_{lab} = \frac{ sin\,\theta_{c}}{cos \theta_c+ \frac{m_1}{m_2}}$

### Two body Problem

- **Description**:
We need to consider the mass of star(sun) in planetary system.

- **Equation of Motion**:
$\mu \frac{d^2\vec{r}}{dt^2} = - k^2\frac{m}{r^2}\hat{r}$

- **Deduction**:
($a_i$ means semi-major axis of trajectory of planet， $\tau_i$ means period of planet)
$\frac{a_1^3}{\tau_1^2} : \frac{a_2^3}{\tau_2^2} = \frac{m_{sun} + m_1}{m_{sun} + m_2}$

- **Conclusion**:
kepler's third law is a approximation!

### Variable Mass System

- **Description**:
  $\frac{d}{dt}(m\vec{v})- \frac{dm}{dt}\vec{u}=\bm{F}$

- **Application(Rocket)**:
  $m_0$ is the initial mass, $v_r$ is the relative velocity.
  $v = v_0 + v_rln\frac{m_0}{m}$
  $m'$ means fuel mass.
  $v = 2.3v_rlg(1+\frac{m'}{m})$

### Virial Theorem

- **Description**:
  $ G = \sum_{i=1}^n \bm{p}_i \cdot \bm{r}_i $
  $ \frac{G(\tau) - G(0)}{\tau} = 2\overline{E}_k + \overline{\sum_{i=1}^n\bm{F}_i\cdot\bm{r}_i}$

- **Deduction**:
  If it's periodic motion or all mass point retain finite value on position and momentum.
  $lim_{\tau \to \infin} \frac{G(\tau) - G(0)}{\tau} \to 0$
  then
  $\overline{E}_k = -\frac{1}{2} \overline{\sum_{i=1}^n\bm{F}_i\cdot\bm{r}_i}$
