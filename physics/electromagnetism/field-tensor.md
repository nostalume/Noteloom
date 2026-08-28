# Electromagnetic Field Tensor

$$
\nabla \cdot \mathbf{E} = \rho / \epsilon_0 \\
\nabla \times \mathbf{B} - \frac{1}{c^2}\frac{\partial\mathbf{E}}{\partial t} = \mu_0 \mathbf{j} \\
\nabla \cdot \mathbf{B} = 0 \\
\nabla \times \mathbf{E} + \frac{\partial\mathbf{B}}{\partial t} = 0 \\
\mathbf{F} = \rho \mathbf{E} + \mathbf{j} \times \mathbf{B}
$$

## Static Application

### Static Energy

In electric field, choose $\mathbf{B} = 0, \mathbf{j} = 0$, in magnetic field, choose $\mathbf{E} = 0, \rho =0$

Take equation (2) and (4), multiply electro field or magnetic field and integrate:

$$
\frac{1}{2}\frac{\partial}{\partial t}(\frac{1}{c^2}\mathbf{E}^2) = 0 \\
\frac{1}{2}\frac{\partial}{\partial t}(\mathbf{B}^2) = 0 \\
$$

Usually, we take factor as $\frac{1}{2}$, coincide with:
$$
\delta\mathcal{E}_{electric} = \mathbf{E} \, \delta \mathbf{E} \\
\delta\mathcal{E}_{magnetic} = \mathbf{B} \, \delta \mathbf{B}
$$

### Static Force

We integrate with Eisenstein convention(We will omit $\epsilon_0$ and $\mu_0$ for clarity)

$$
\rho E_j =(\partial_i E_i )E_j = \partial_i(E_iE_j) - \partial_i(E_j)E_i
$$

Notice, in static situation, $\nabla \times \mathbf{E} = 0 \sim \partial_i E_j = \partial_j E_i$

$$
LHS = \partial_i(E_iE_j) - \partial_j(E_i)E_i =\partial_i{E_i E_j} - \partial_j (\frac{1}{2}E^2) \\
\mathcal{P} = \partial_i(E_i E_j - \delta_{ij}\frac{1}{2}E^2) = \rho E_j
$$

$LHS$ means the general force of total electric field(**including itself**!) applied on charges it wrapped,

$$
\mathbf{j} \times \mathbf{B} = \nabla \times \mathbf{B} \times \mathbf{B} = B_i\partial_i B_j - (\partial_j B_i) B_i \\
$$

Notice, in static situation, $\nabla \cdot \mathbf{B} = 0$, so $B_i\partial_iB_j = \partial_i (B_i B_j)$

$$
LHS = \partial_i (B_i B_j) - \partial_j\frac{1}{2}(B^2) = \partial_i (B_i B_j - \delta_{ij} \frac{1}{2}B^2) \\
\mathcal{P} = \partial_i (B_i B_j - \delta_{ij} \frac{1}{2}B^2) = \mathbf{j} \times \mathbf{B}
$$
$LHS$ means the general force of total magetic field(**including itself**!) applied on current it wrapped.

## Dynamic Application

Based on above analysis, the generalization must contains cross term between electric and magnetic field.

### Energy

It's same as before, but we can't take their corresponding term as zero. Notice that the total force exerted by field to charge should be of form $q(\mathbf{E} + \dot{\mathbf{r}} \times \mathbf{B}) \cdot \dot{\mathbf{r}}dt = q \mathbf{E} \cdot \mathbf{v} dt$, so it should contains the term like $\mathbf{E}\cdot \mathbf{j}$

$$
\frac{d W}{d t} = \mathbf{E} \cdot \mathbf {j} \\
= \frac{1}{\mu_0} \mathbf{E} \cdot (\nabla \times \mathbf{B}) - \epsilon_0 \mathbf{E} \frac{\partial\mathbf{E}}{\partial t} \\
= \frac{1}{\mu_0} [\nabla \cdot (\mathbf{B} \times \mathbf{E}) + \mathbf{B} \cdot (\nabla \times \mathbf{E})] - ... \\
= - \frac{1}{\mu_0}\mathbf{B} \cdot \frac{\partial \mathbf{B}}{\partial t} - \epsilon_0 \mathbf{E} \frac{\partial\mathbf{E}}{\partial t} - \frac{1}{\mu_0} \nabla \cdot (\mathbf{E} \times \mathbf{B}) \\
= - \frac{\partial}{\partial t}(\frac{1}{2}(\epsilon_0 \mathbf{E}^2 + \frac{1}{\mu_0} \mathbf{B}^2)) - \frac{1}{\mu_0} \nabla \cdot (\mathbf{E} \times \mathbf {B})
$$

We take the second term as $\mathbf{S}$ as **Poynting** vector, actually, the formal meaning should be the momentum(actually there's a factor selection difference) of electromagnetic field.

As the first term, it's well known in static case, which is the energy $\mathcal{E}$ of electromagnetic field.

Results equation's meaning is the loss of energy in time and the momentum exerted by field will be transformed to energy given to source, if there's no source, we can state in vacuum: Energy and Momentum exchange, maintaining conservation(**continuity equation for electromagnetic enery**):

$$
 (\frac{\partial \mathcal{E}}{\partial t} + \nabla \cdot \mathcal{S} ) = - \mathbf{E} \cdot \mathbf{j}
$$

### Force

We have already seen static part of force by field to source. We indeed has another part which is the loss of momentum in time and the force exerted by field will be transformed to force given to source.

$$
\rho \mathbf{E} + \mathbf{j} \times \mathbf{B} = \epsilon_0 \nabla \cdot \mathbf{E} \, \mathbf{E} + (\frac{1}{\mu_0}\nabla \times \mathbf{B} - \epsilon_0 \frac{\partial \mathbf{E}}{\partial t} )\times \mathbf{B} \\
= \mathcal{P}_{electric} - \frac{1}{\mu_0}((\mathbf{B}\cdot \nabla)\mathbf{B}-\frac{1}{2}\nabla \mathbf{B}^2) - \epsilon_0 \frac{\partial \mathbf{E}}{\partial t} \times \mathbf{B} \\
= \mathcal{P}_{electric} + \mathcal{P}_{magnetic} - \frac{1}{c^2} \mathbf{S}
$$

Usually, we will take this form, first take $\frac{1}{c^2} \mathbf{S} = \mathbf{g}$ as the real momentum. Second, take minus sign to indicate loss! Third, use partial and tensor form!

Results:

$$
\frac{\partial g_i}{\partial t} + \partial_j T_{ij} = -(\rho E_i + (\mathbf{j} \times \mathbf{B})_i)
$$

Where
$$
g_i = \epsilon_0 (\mathbf{E} \times \mathbf{B})_i \\
T_{ij} = -(E_i E_j - \delta_{ij}\frac{1}{2}E^2) - (B_i B_j - \delta_{ij} \frac{1}{2}B^2)
$$
We change sign to indicate loss

Now we absorb time term as $0$, gives

$$
T_{00} = \mathcal{E}_{electro} + \mathcal{E}_{magnetic} \\
T_{0i} = T_{i0} = g_i
$$

Finish our energy tensor.

We can achieve above by $F_{\mu \nu}$ and noether theorem, which is also a toil.
