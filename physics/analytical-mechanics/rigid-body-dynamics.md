---
title: Chapter 3
markmap:
  colorFreezeLevel: 2
---

## **Rotation**

- Angular Velocity:
$\bold{v} = \frac{d \bold{r}}{dt} = \omega \times \bold{r}$
- Euler Angle:
  $\omega_1 = \dot{\phi}sin\theta sin\psi + \dot{\theta}cos \psi$
  $\omega_1 = \dot{\phi}sin\theta cos\psi - \dot{\theta}sin \psi$
  $\omega_3 = \dot{\phi}cos \theta + \dot{\psi}$
  With $\phi$ precession angle; $\psi$ rotation angle; $\theta$ nutation angle.

## **Force on Rigid Body**

- **Decomposition of Force**:
  A force on arbitrary point of rigid body can be decomposed as:
  - a force on reference point of rigid body.
  - a torque between the point and reference point.
  - $F|_O \sim F|_{O'} + r_{OO'} \times F$

- **Force Balance**
  $\bold{F} = 0$; $\bold{M} = 0$

## **Property of Rigid Body**

### **Rotational Inertia**

- $I_{ij} = \int dm (\delta_{ij}\sum_k x_k^2 - x_ix_j)$
  If we choose a axis to project:
  $I = I_{ij}cos \theta_i cos\theta_j$
  $I\omega^2 = I_{ij}\omega^2 cos\theta_i cos\theta_j = I_{ij}\omega_i \omega_j$
  $I = mk^2$

### **Huygens–Steiner Theorem**

- Rotational inertia can change its reference point respect position vector $\bold{c}$:
  $I_{ij} = I_{ij}^{CM} + M(\bold{c}^2 \delta_{ij} - c_i c_j)$

### **Angular Momentum**

- Choose a reference point in rigid body by $c+r'$
  $\bold{J} = M(\bold{c} \times \bold{V} + \bold{c} \times (\omega \times \bold{R'}) + \bold{R'} \times \bold{V}) + \int dm \, r' \times (\omega \times r')$
  If the reference point is the center of mass, we know $\bold{R'} = 0$
  $\bold{J} = M(\bold{c} \times \bold{V}) + \int dm \, r' \times (\omega \times r') = \bold{J}_{CM} + \bold{J}_{r}$
  $J_i = I_{ij}\omega_j$

### **Kinetic Energy**

- Choose a reference point in rigid body by $c+r'$
  $E_k = \frac{1}{2}M \bold{V}^2 + M \bold{V} \cdot(\omega \times \bold{R}) + \frac{1}{2}\int dm (\omega \times r')^2$
  If the reference point is the center of mass, we know $\bold{R'} = 0$
  $E_k = \frac{1}{2}M \bold{V}^2 + \frac{1}{2}\int dm (\omega \times r')^2 = {E_k}_{CM} + {E_k}_{r}$
  $E_k = \frac{1}{2}I_{ij}\omega_i\omega_j$

## **Rigid Body Motion**

### **Velocity**

- Notice $\omega$ is independent of reference frame.
  $v_i = v_r + \omega \times r_{ir}$

### **Acceleration**

- We choose $\alpha$ as angle acceleration.
  $a_i = a_r + \alpha \times r_{ir} + \omega \times (\omega \times r_{ir})$

### **Instantaneous Center of Rotation**

- Take the point on rigid body with total velocity is zero
  $0 = v_r + \omega \times (r_i - r_r)$
  Now we can see $v_r$ is reversely determined by $r_{ri}$.
  $v_r = \omega \times r_{ri}$

### **Plane**

- We choose $z$ as axis perpendicular to the plane.
  $\frac{d J_z}{dt} = M_z$
  General Energy relation in conservative force:
  $\frac{1}{2}I_{zz}|_{CM}\omega^2 + {E_k}_{CM} = E$
  With fixed rotational axis:
  $\frac{1}{2}I_{zz}\omega^2 + E_p = E$
- Non-Slip scrolling: $v_{CM} - \omega \times R|_{bottom} = 0$

### **Fixed Point**

- **Euler Equation of Motions**
  $\frac{d \bold{J}}{dt} = \bold{M}$
  $\dot{J} + \omega \times {J} = \bold{M}$
