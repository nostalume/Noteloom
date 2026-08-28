---
markmap:
  colorFreezeLevel: 2
---

# Non-Inertial Frames of Reference

## Plane Rotating Reference Frames

- **Concept**: Kinematics of a particle in a reference frame rotating in a plane relative to an inertial frame.
- **Position Vector**:
  $$ \vec{r} = \vec{r}' $$
  (Assuming origins O and O' coincide)
- **Velocity Transformation**:
  $$ \vec{v}_{\text{abs}} = \vec{v}_{\text{rel}} + \vec{\omega} \times \vec{r}' $$
  where $\vec{v}_I$ is velocity in inertial frame, $\vec{v}_R$ is velocity in rotating frame, $\vec{\omega}$ is angular velocity of the rotating frame.
- **Acceleration Transformation**:
  $$ \vec{a}_{\text{abs}} = \vec{a}_{\text{rel}} + 2\vec{\omega} \times \vec{v}_{\text{rel}} + \vec{\omega} \times (\vec{\omega} \times \vec{r}') + \dot{\vec{\omega}} \times \vec{r}' $$
  - Terms:
    - $\vec{a}_R$: Acceleration in rotating frame
    - $2\vec{\omega} \times \vec{v}_R$: Coriolis acceleration
    - $\vec{\omega} \times (\vec{\omega} \times \vec{r}')$: Centripetal acceleration (often viewed as $-\vec{\omega} \times (\vec{\omega} \times \vec{r}')$ for centrifugal force)
    - $\frac{d\vec{\omega}}{dt} \times \vec{r}'$: Euler acceleration (or azimuthal acceleration)

### Space Rotating Reference Frames

- **Concept**: Kinematics in a reference frame undergoing general rotation in 3D space, possibly with a translating origin.
- **Position Vector**:
  $$ \vec{r}_I = \vec{R}_O + \vec{r}' $$
  where $\vec{R}_O$ is the position of the origin of the rotating frame O' in the inertial frame I.
- **Velocity Transformation**:
  $$ \vec{v}_I = \vec{V}_O + \vec{v}'_R + \vec{\omega} \times \vec{r}' $$
  where $\vec{V}_O = \dot{\vec{R}}_O$ is the velocity of O'.
- **Acceleration Transformation**:
  $$ \vec{a}_I = \vec{A}_O + \vec{a}'_R + 2\vec{\omega} \times \vec{v}'_R + \vec{\omega} \times (\vec{\omega} \times \vec{r}') + \dot{\vec{\omega}} \times \vec{r}' $$
  where $\vec{A}_O = \ddot{\vec{R}}_O$ is the acceleration of O'.

### Dynamics in Non-Inertial Frames

- **Equation of Motion**: Newton's second law in a non-inertial frame.
  $$ m\vec{a}'_R = \vec{F}_{\text{net, actual}} - m\vec{A}_O - 2m(\vec{\omega} \times \vec{v}'_R) - m[\vec{\omega} \times (\vec{\omega} \times \vec{r}')] - m(\dot{\vec{\omega}} \times \vec{r}') $$
- **Fictitious Forces (Inertial Forces)**:
  - **Translational Inertial Force**:
    $$ \vec{F}_{\text{trans}} = -m\vec{A}_O $$
  - **Coriolis Force**:
    $$ \vec{F}_{\text{Cor}} = -2m(\vec{\omega} \times \vec{v}'_R) $$
  - **Centrifugal Force**:
    $$ \vec{F}_{\text{cf}} = -m[\vec{\omega} \times (\vec{\omega} \times \vec{r}')] $$
    Magnitude for circular motion: $F_{\text{cf}} = m\omega^2 r'_{\perp}$, where $r'_{\perp}$ is perpendicular distance from axis of rotation.
  - **Euler Force (or Azimuthal Force)**:
    $$ \vec{F}_{\text{Euler}} = -m(\dot{\vec{\omega}} \times \vec{r}') $$
    Arises from non-uniform rotation.

### Influence of Earth's Revolution and Rotation

- **Dominant Effects**: Primarily due to Earth's rotation ($\vec{\omega}_E$). Revolution causes negligible effects on local phenomena.
- **Earth's Angular Velocity**:
  $$ \omega_E \approx \frac{2\pi}{24 \text{ hours}} \approx 7.27 \times 10^{-5} \text{ rad/s} $$
- **Effective Gravitational Acceleration**:
  The true gravitational force $\vec{F}_g = m\vec{g}_0$ combines with the centrifugal force due to Earth's rotation.
  $$ \vec{g}_{\text{eff}} = \vec{g}_0 - \vec{\omega}_E \times (\vec{\omega}_E \times \vec{R}) $$
  where $\vec{R}$ is the position vector from the Earth's center. This leads to variation of $g$ with latitude and the plumb line not pointing exactly to Earth's center (except at poles and equator).
- **Equation of Motion for an object on Earth's surface**:
  $$ m\vec{a}'_R = \sum \vec{F}_{\text{applied}} + m\vec{g}_{\text{eff}} + \vec{F}_{\text{Cor}} $$
  $$ m\vec{a}'_R = \sum \vec{F}_{\text{applied}} + m\vec{g}_{\text{eff}} - 2m(\vec{\omega}_E \times \vec{v}'_R) $$

### Coriolis Force on Free Fall

- **Effect**: Causes an eastward deviation of a freely falling object.
- **Setup**: Object dropped from height $h$ at latitude $\lambda$.
  - $\vec{\omega}_E$ has components: $\omega_{E,y'} = \omega_E \cos\lambda$ (North), $\omega_{E,z'} = \omega_E \sin\lambda$ (Up, local vertical)
  - Velocity of falling body (approx): $\vec{v}'_R \approx -gt \hat{k}'$ (downwards, neglecting air resistance and initial horizontal velocity).
- **Coriolis Force Components**:
  $$ \vec{F}_{\text{Cor}} = -2m (\vec{\omega}_E \times \vec{v}'_R) $$
  $$ \vec{F}_{\text{Cor}} = -2m ((\omega_E \cos\lambda \hat{j}' + \omega_E \sin\lambda \hat{k}') \times (-gt \hat{k}')) $$
  $$ \vec{F}_{\text{Cor}} = -2m (-\omega_E gt \cos\lambda (\hat{j}' \times \hat{k}')) = 2m \omega_E gt \cos\lambda \hat{i}' $$
  (where $\hat{i}'$ is East, $\hat{j}'$ is North, $\hat{k}'$ is Up)
- **Eastward Deviation ($d_E$)**:
  Acceleration $a_x = \frac{F_{\text{Cor},x}}{m} = 2\omega_E gt \cos\lambda$.
  $$ d_E = \int_0^t \int_0^{t'} a_x dt'' dt' = \int_0^t v_x dt' = \int_0^t (\omega_E g t'^2 \cos\lambda) dt' = \frac{1}{3} \omega_E g t^3 \cos\lambda $$
  Using $h = \frac{1}{2}gt^2 \implies t = \sqrt{\frac{2h}{g}}$:
  $$ d_E = \frac{1}{3} \omega_E \cos\lambda \sqrt{\frac{8h^3}{g}} $$

### Coriolis Force on Trade Winds

- **Mechanism**:
  1. Air heats up at the equator, rises, creating low pressure. Cooler air from subtropics (higher pressure) flows towards the equator.
  2. In the Northern Hemisphere, this southward moving air is deflected to its right (westward) by the Coriolis force: $\vec{F}_{\text{Cor}} \propto -(\vec{\omega}_E \times \vec{v}'_R)$.
If $\vec{v}'_R$ is southward and $\vec{\omega}_E$ has an upward component, the force is eastward. For surface winds moving towards equator, $\vec{v}'_R$ has a component towards the equator.
  This force component is to the West (right). Thus, Northeast trade winds.
  3. In the Southern Hemisphere, this northward moving air is deflected to its left (westward) by the Coriolis force. Thus, Southeast trade winds.
- **Result**: Formation of Northeast trade winds (NH) and Southeast trade winds (SH).

### Coriolis Force on Geological Landforms

- **Baer's Law (River Bank Erosion)**:
  - In the Northern Hemisphere, rivers flowing in any direction tend to experience a Coriolis force deflecting water to the right bank (facing downstream). This can lead to greater erosion on the right bank.
  - In the Southern Hemisphere, the deflection and thus greater erosion is towards the left bank.
- **Ocean Currents**: Large-scale ocean gyres rotate clockwise in the NH and counter-clockwise in the SH due in part to Coriolis forces acting on wind-driven surface currents.

### Coriolis Force on Typhoons/Cyclones

- **Formation**:
  1. Warm, moist air rises over tropical waters, creating an area of low pressure.
  2. Surrounding air rushes in towards the low-pressure center.
- **Rotational Effect**:
  - In the Northern Hemisphere, the inflowing air is deflected to the right by the Coriolis force. This results in a counter-clockwise rotation around the low-pressure center.
    $$ \vec{F}_{\text{Cor}} = -2m(\vec{\omega}_E \times \vec{v}'_R) $$
    For air moving towards a central point, $\vec{v}'_R$ is radial. The $\sin\lambda$ component of $\omega_E$ (vertical component) is most effective.
  - In the Southern Hemisphere, the inflowing air is deflected to the left, resulting in a clockwise rotation.
- **Note**: Coriolis force is zero at the equator ($\lambda=0$), so hurricanes/typhoons typically do not form very close to the equator.
  $$ F_{\text{Cor}} \propto \sin\lambda $$
