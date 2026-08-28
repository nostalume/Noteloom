# Green Functions in Electrostatics

$$
\nabla^2 \phi = -\rho(r)/\epsilon_0
$$
General form in **Green function**
$$
\int_\Omega(\phi\nabla^2G-G\nabla^2\phi)dV = \int_{\partial\Omega}(\phi \frac{\partial G}{\partial n}-G\frac{\partial \phi}{\partial n})dS \\
\nabla^2G = \delta(r-r') \quad r,r' \in V \\
\phi(r) = \int_\Omega \rho(r)/\epsilon_0 \, G dV + \int_{\partial\Omega}(\phi \frac{\partial G}{\partial n}-G\frac{\partial \phi}{\partial n})dS
$$
notice that this still work in $\rho(r)=0$ but you don't want to solve it again in coordinates, so we will take laplace equation with given basis for ease.

**Image**
in given boundary condition, we want to solve for $G(r,r')$ , usually with dirichlet condition $\phi(r)|_S = f(r)$, in such case we take $G(r,r')|_S = 0$, how to solve this in several case?
$$
\nabla^2 G(r,r') = \delta(r-r') \\
G(r,r')|_S = 0 \quad S = \text{spherical or plane} + \, \text{infinity boundary} \\
G(r,r') = G(r',r) \\
$$
take seperation:
$$
G_i(r,r') = G^{inner}_{i} + G^{boundary}_{i} \\
\nabla^2 G^{boundary}_i = 0 \\
G_i(r,r') = -\frac{1}{|r-r'|} + G^{boundary}_i
$$
if in usual case: $\nabla^2\phi = \sum_i-q_i/\epsilon_0\delta(r-r')$ and $\phi|_s = 0$ for conductor
$$
\phi = \sum_i -q_i/\epsilon_0G_i(r,r') \\
\phi_{inner} = \sum_i \frac{q_i/\epsilon}{|r-r'|} \\
\nabla^2\phi_{boundary} = 0 \\
$$
if in spherical coordinate($\sigma$ is for many image charge with $r_{outer}$ outside the volume)
$$
\phi_{boundary} = \sum_{\sigma}\sum_l(A_l r^l+B_l r^{-(l+1)})P_l(cos\theta) \\
 or \\
\nabla^2\phi_{boundary} = \delta(r-r_{outer}) \\
\phi_{boundary} +\phi_{inner}|_s = f(r)
$$
