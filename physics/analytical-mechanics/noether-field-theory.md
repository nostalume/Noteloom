# Noether's Theorem in Field Theory

We identify a special tiny translation in $\delta ... = X^\mu_a(...)\xi^a$ for $\xi^a$ as possible parameters.

$$
x'^\mu = x^\mu + \delta x^\mu \\
\phi'^i(x') = \phi^i(x) + \delta\phi^i(x) + \partial_\mu \phi^i(x)\delta x^\mu = \phi^i(x) + D\phi^i(x)
$$

$$
\begin{align}
S'[\phi'] = \int_{\Omega'} d^4x' \mathcal{L}(\phi'(x'),\partial_{\mu'}\phi'(x')) \\
\frac{\partial x'^\mu}{\partial x^v} = \delta^\mu_v + \partial_v \delta x^\mu \\
\frac{\partial x^\mu}{\partial x'^v} = \delta^\mu_v - \partial_v \delta x^\mu \\
det(\delta^\mu_v + \partial_v \delta x^\mu ) = 1 + \partial_v \delta x^\mu \\
\end{align}
$$
notice our partial derivative on $\phi'(x')$ is in new coordinates.
$$
S'[\phi'] = \int_{\Omega} d^4x(1+\partial_v \delta x^\mu) \mathcal{L}(\phi'(x'),(\delta^v_\mu - \partial_\mu \delta x^v)\partial_v\phi'(x')) \\
$$

We only consider linear term, which means twice $\delta$ or $D$ won't be considered.

$$
S'[\phi'] = \int_{\Omega} d^4x(1+\partial_v \delta x^\mu) \mathcal{L}(\phi,\partial_\mu\phi) + \frac{\partial\mathcal{L}}{\partial\phi^i}D\phi^i + \frac{\partial\mathcal{L}}{\partial(\partial_\mu\phi^i)}(\partial_\mu D\phi^i - \partial_\mu \delta x^v \partial_v \phi^i) \\
$$

Notice that:
$$
\partial_\mu D\phi^i(x) = \partial_\mu \delta\phi^i(x) + \partial_\mu(\partial_v \phi^i(x)\delta x^v)
$$

So:
$$
= \int_{\Omega} d^4x\mathcal{L}(\phi,\partial_\mu\phi) + \mathcal{L}\partial_\mu \delta x^\mu + \frac{\partial\mathcal{L}}{\partial\phi^i}(\delta\phi^i + \partial_\mu\phi^i\delta x^\mu) + \frac{\partial\mathcal{L}}{\partial(\partial_\mu\phi^i)}(\partial_\mu\delta\phi^i(x) +\partial_\mu\partial_v\phi^i \, (\delta x^\mu)) \\
$$

$$
= \int_{\Omega} d^4x\mathcal{L}(\phi,\partial_\mu\phi) + \mathcal{L}\partial_\mu \delta x^\mu + {\partial_\mu \mathcal{L}}\delta x^\mu + \partial_\mu (\frac{\partial\mathcal{L}}{\partial (\partial_\mu \phi^i)}\delta\phi^i) \\
$$
Finally:
$$
\delta S[\phi] = \int_{\Omega} d^4x \partial_\mu\{\frac{\partial\mathcal{L}}{\partial(\partial_\mu\phi^i)}X_{\phi^i,I} + \mathcal{L}X_{x,I}^\mu\}\xi_I
$$

An usual application is energy tensor for($a$ as parameter):
$$
\delta x^\mu = a^\mu = \delta^\mu_v a^v\\
D \phi^i = 0
$$
which means:
$$
\delta \phi^i = -\partial_\mu \phi^i a^\mu = -\delta^v_\mu \partial_v \phi^i a^v
$$
and results:
$$
T^\mu_v a^v = (\frac{\partial \mathcal{L}}{\partial(\partial_\mu \phi^i)}\partial_v\phi^i - \mathcal{L}\delta^\mu_v)a^v
$$

## Discrete

Then $\phi^i$ would be $q^i$, and the coordinates $x^\mu$ would be restricted to $t$, then each partial for $\mu$ becomes for $t$, sum each coordinates, finally as $T^0_0 = H$.
$$
D q = \delta q + \dot{q} \delta t \\
\delta S[q] = \int dt \frac{d}{dt}(\frac{\partial L}{\partial \dot{q}} \delta q - L\delta t) \\
H = \frac{\partial{L}}{\partial(\dot{q})}\dot{q} - L
= p\dot{q} - L
$$
