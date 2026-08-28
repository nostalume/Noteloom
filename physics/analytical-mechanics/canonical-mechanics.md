# Analytical Mechanics

---

## Constraints & Generalized Coordinates

### Constraints

- **Definition:** Restrictions on the motion of a system.
- **Classification:**
  - **Holonomic vs. Non-holonomic**
    - **Holonomic:** Expressible as an algebraic equation relating coordinates and time: $f(q_1, q_2, ..., q_n, t) = 0$.
      - *Example:* Particle on a sphere, $x^2 + y^2 + z^2 - R^2 = 0$.
    - **Non-holonomic:** Cannot be expressed in the above form; often involve inequalities or non-integrable differentials.
      - *Example:* Particle inside a sphere, $x^2 + y^2 + z^2 - R^2 \le 0$.
  - **Scleronomous vs. Rheonomous**
    - **Scleronomous:** Constraints are independent of time (time does not explicitly appear in $f$).
      - *Example:* Fixed length pendulum.
    - **Rheonomous:** Constraints explicitly depend on time.
      - *Example:* Pendulum with a string whose length is changing, $r - L(t) = 0$.
  - **Ideal vs. Non-ideal**
    - **Ideal:** The virtual work done by the constraint forces is zero for any virtual displacement consistent with the constraints, $\sum_i \mathbf{F}_i^c \cdot \delta \mathbf{r}_i = 0$.
    - **Non-ideal:** Virtual work done by constraint forces is non-zero.

### Generalized Coordinates

- **Definition:** A set of independent coordinates ($q_1, q_2, ..., q_n$) that completely specify the configuration of a system.
- **Degrees of Freedom (DOF):** The minimum number of independent coordinates required. For $N$ particles and $k$ holonomic constraints, DOF $= 3N - k$.
- **Transformation:** Cartesian coordinates $\mathbf{r}_i$ can be expressed as functions of generalized coordinates and time: $\mathbf{r}_i = \mathbf{r}_i(q_1, ..., q_n, t)$.

---

## Principle of Virtual Work

### Virtual Displacements ($\delta\mathbf{r}_i$)

- **Definition:** Infinitesimal, imaginary displacements consistent with the instantaneous constraints of the system.
- **Properties:**
  - Occur at fixed time ($dt=0$).
  - Do not necessarily represent actual motion.
  - Related to generalized coordinates by: $\delta \mathbf{r}_i = \sum_j \frac{\partial \mathbf{r}_i}{\partial q_j} \delta q_j$.

### Actual Displacements ($d\mathbf{r}_i$)

- **Definition:** Infinitesimal displacements that occur during actual motion over a time interval $dt$.

### Principle of Virtual Work (for static equilibrium)

- A system is in equilibrium if and only if the total virtual work done by all forces (applied and constraint) is zero for any arbitrary virtual displacement consistent with the constraints: $\sum_i \mathbf{F}_i \cdot \delta \mathbf{r}_i = 0$.

### D'Alembert's Principle

- **Extension to dynamics:** For a system not in equilibrium, the sum of the virtual work done by the actual forces and the inertial forces is zero:
  - $\sum_i (\mathbf{F}_i - m_i \ddot{\mathbf{r}}_i) \cdot \delta \mathbf{r}_i = 0$.
- **Ideal Constraints:** If constraints are ideal, the virtual work done by constraint forces is zero. Thus, D'Alembert's Principle simplifies to considering only applied forces and inertial forces.

---

## Lagrangian Equations of Motion

### Lagrangian ($L$)

- **Definition:** $L = T - U$, where $T$ is the kinetic energy and $U$ is the potential energy.
- **Kinetic Energy:** $T = \frac{1}{2} \sum_i m_i |\dot{\mathbf{r}}_i|^2 = T(q_j, \dot{q}_j, t)$.
- **Potential Energy (for conservative systems):** $U = U(q_j, t)$.

### Lagrange's Equations (Basic Form)

- For a system with **holonomic, ideal constraints**, and derived from D'Alembert's principle:
  - $\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}_j}\right) - \frac{\partial L}{\partial q_j} = Q_j$.
  - $Q_j$ are the **generalized non-conservative forces**: $Q_j = \sum_i \mathbf{F}_i^{nc} \cdot \frac{\partial \mathbf{r}_i}{\partial q_j}$.

### Conservative Systems

- If all forces are derivable from a potential energy $U(q_j, t)$, then $Q_j = -\frac{\partial U}{\partial q_j}$.
- Lagrange's equations become: $\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}_j}\right) - \frac{\partial L}{\partial q_j} = 0$.
- Here, $L = T - U$.

### Cyclic (Ignorable) Coordinates

- A generalized coordinate $q_j$ is **cyclic** if the Lagrangian $L$ does not explicitly depend on $q_j$ (i.e., $\frac{\partial L}{\partial q_j} = 0$).
- For a cyclic coordinate, the corresponding **generalized momentum** is conserved:
  - $p_j = \frac{\partial L}{\partial \dot{q}_j} = \text{constant}$.

### Energy Integral (Conservation of Energy)

- For a **scleronomous (time-independent constraints) conservative system**, the total mechanical energy $E$ is conserved.
- **Energy function ($h$):** $h = \sum_j \dot{q}_j \frac{\partial L}{\partial \dot{q}_j} - L$.
- If $L$ does not explicitly depend on time ($\frac{\partial L}{\partial t} = 0$), then $h$ is conserved.
- For a system where $T$ is a quadratic form in $\dot{q}_j$ and $U$ is independent of $\dot{q}_j$, then $h = T + U = E$.

---

## Hamiltonian Canonical Equations & Hamilton's Principle

### Legendre Transformation

- A mathematical tool to transform between functions of one set of variables to functions of another set of variables.
- Used to go from Lagrangian (function of $q, \dot{q}, t$) to Hamiltonian (function of $q, p, t$).
- Given a function $L(q, \dot{q}, t)$, its Legendre transform $H(q, p, t)$ is defined as:
  - $H(q, p, t) = \sum_j p_j \dot{q}_j - L(q, \dot{q}, t)$.
  - Where $p_j = \frac{\partial L}{\partial \dot{q}_j}$ are the generalized momenta.

### Hamiltonian ($H$)

- **Definition:** $H(q_j, p_j, t) = \sum_j p_j \dot{q}_j - L(q_j, \dot{q}_j, t)$.
- Represents the total energy of the system when constraints are scleronomous and forces are conservative.
- For scleronomous systems where $T$ is a homogeneous quadratic function of $\dot{q}_j$, $H = T + U = E$.

### Hamilton's Canonical Equations

- A set of $2n$ first-order differential equations that describe the evolution of a system in phase space ($q, p$).
  - $\dot{q}_j = \frac{\partial H}{\partial p_j}$
  - $\dot{p}_j = -\frac{\partial H}{\partial q_j}$
  - And if $H$ has explicit time dependence: $\frac{\partial H}{\partial t} = -\frac{\partial L}{\partial t}$.

### Hamilton's Principle (Principle of Least Action)

- **Statement:** The actual path taken by a system between two fixed configurations at two fixed times ($t_1$ and $t_2$) is that for which the **action integral** $S$ is stationary (an extremum, usually a minimum).
  - $S = \int_{t_1}^{t_2} L(q_j, \dot{q}_j, t) dt$.
  - $\delta S = \delta \int_{t_1}^{t_2} L(q_j, \dot{q}_j, t) dt = 0$.
- This is a variational principle from which Lagrange's equations (and thus Hamilton's equations) can be derived.

---

## Poisson Brackets & Canonical Transformations

### Poisson Brackets

- **Definition:** For any two functions $F(q, p, t)$ and $G(q, p, t)$ in phase space, their Poisson bracket is defined as:
  - $\{F, G\} = \sum_j \left( \frac{\partial F}{\partial q_j} \frac{\partial G}{\partial p_j} - \frac{\partial F}{\partial p_j} \frac{\partial G}{\partial q_j} \right)$.
- **Fundamental Poisson Brackets:**
  - $\{q_j, q_k\} = 0$
  - $\{p_j, p_k\} = 0$
  - $\{q_j, p_k\} = \delta_{jk}$ (Kronecker delta)
- **Time Evolution of a Dynamical Variable:**
  - For a function $F(q, p, t)$, its total time derivative is: $\frac{dF}{dt} = \{F, H\} + \frac{\partial F}{\partial t}$.
  - If $F$ is a constant of motion (conserved quantity), then $\frac{dF}{dt} = 0$.

### Canonical Transformations

- **Definition:** A transformation from one set of canonical coordinates $(q_j, p_j)$ to another set $(Q_j, P_j)$ such that Hamilton's canonical equations retain their form (i.e., the new coordinates are also canonical).
  - $\dot{Q}_j = \frac{\partial K}{\partial P_j}$
  - $\dot{P}_j = -\frac{\partial K}{\partial Q_j}$
  - Where $K(Q, P, t)$ is the new Hamiltonian.
- **Generating Functions:** Canonical transformations can be generated by a single function ($F_1, F_2, F_3,$ or $F_4$) that relates the old and new coordinates and momenta.
  - *Example (Type 1 Generating Function $F_1(q, Q, t)$):*
    - $p_j = \frac{\partial F_1}{\partial q_j}$
    - $P_j = -\frac{\partial F_1}{\partial Q_j}$
    - $K = H + \frac{\partial F_1}{\partial t}$
- **Purpose:** To simplify the Hamiltonian, making the equations of motion easier to solve, often by identifying new cyclic coordinates.
