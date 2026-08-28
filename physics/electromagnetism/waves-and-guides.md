# Electromagnetic Waves and Waveguides

Covariant form:

$$
\partial_{\mu} F^{\mu \nu}= - \mu_0 j^\nu \\
\text{lorentz gauge:} \quad \partial_{\mu} A^\mu = 0 \\
\square A^\nu = - \mu_0 j^\nu
$$

No source:
$$
\square A^\nu = 0 \\
\therefore (-\frac{1}{c^2}\frac{\partial^2}{\partial t^2} + \nabla^2) A^\nu = 0
$$

Given 4-vector $k$ for simplicity:
$$
A^\mu = \mathcal{A}_k \epsilon^\mu(k) e^{-ikx}
$$

Insert will results:
$$
k^2 = 0 \\
$$

Lorentz gauge gives:
$$
\partial_\mu A^\mu = \partial_\mu (\epsilon^\mu(k)e^{ikx}) = ik_{\mu} \epsilon^\mu (k) e^{ikx} = 0 \\
\therefore k_{\mu} \epsilon^{\mu}(k) = \eta_{\mu \nu} k^\mu \epsilon^{\nu}(k) = 0
$$

So based on two restrictions, we choose as $(t,\mathbf{x})$:
$$
k^{\mu} = k_0(1,0,0,1) \\
\epsilon^{\mu}_1(k) = (0,1,0,0) \\
... = (0,0,1,0) \\
\epsilon^{\mu}_{weird}(k) = (1,0,0,1) \\
$$

The third is parallel to $k$, but how? Notice that it's not realistic! $\eta_{\mu \nu} \epsilon^\mu(k) \epsilon^{\nu}(k) = 0$ for the weird polarization direction.

Actually, lorentz gauge can be restricted further.

$$
A^\mu \to A'^\mu = A^\mu - \partial^{\mu} \theta \quad \square \theta = 0 \\
\partial_\mu A'^\mu = 0 \\
\text{Then we choose:} \quad \theta = ae^{ikx} \\
A^\mu - iak^{\mu} e^{ikx}
$$
Can always reduce the direction parallel to $k$.

The basis is called linear polarization, which means the amplitude always in the fixed direction.

Another basis for circular polarization:
$$
\hat{e}_1 = \frac{1}{\sqrt{2}}(0,1,i,0) \\
\hat{e}_2 = \frac{1}{\sqrt{2}}(0,1,-i,0) \\
(0,1,i,0) \sim \mathrm{Re}((\hat{x} + i\hat{y})(e^{ikx})) \sim cos (k_\mu x^\mu + \delta_1) \hat{x} + sin (k_\mu x^\mu + \delta_2) \hat{y}
$$

Which will circle around.

A general solution would be a wave packet summation of every plane waves.

$$
A^\mu(t,\mathbf{x}) = \int \frac{d^3k}{2\pi^3} \sum_{\lambda=1,2}(\epsilon_{\lambda}(\mathbf{k})A_{\mathbf{k},\lambda}e^{ikx} + \epsilon^*_{\lambda}(\mathbf{k})A^*_{\mathbf{k},\lambda}e^{-ikx})|_{k^0 = +|\mathbf{k}|}
$$

Where the bottom notation saying:
$$
\frac{\omega}{c} = +|\mathbf{k}|
$$

We could even incorporate $d\omega$ and give a $\delta (\frac{\omega}{c} - |\mathbf{k}|)$.

$$
E^i = \partial^0 A^i - \partial^i A^0 \\
\sim -i\omega A^i - ik^i A^0 \\
B^k = \frac{1}{2}(\partial^i A^j - \partial^j A^i) \epsilon_{ijk} = \epsilon_{ijk} \partial^i A^j \sim \epsilon_{ijk} ik^i A^j \\
\mathbf{E} \perp \mathbf{B}
$$

The last proposal is due to the reason that $E^i$ is proportional to $A^i$ while $B^i$ is perpendicular (or cross product) of $A^i$. While the time component is perpendicular to space component, it doesn't effect the relation.(Or you can see the basis $\epsilon^\mu$, there's no time component $A^0$.)

Then we exploit that $k^i \sim \omega/c$, so:
$$
c \mathbf{B} = \hat{k} \times \mathbf{E} \\
u(t,\mathbf{x}) = \frac{1}{2}(\epsilon_0 \mathbf{E}^2 + \frac{1}{\mu_0}\mathbf{B}^2) = \epsilon_0 \mathbf{E}^2
$$

$$
[\epsilon_0][\mathbf{E}][L^2] = [Q] \\
[\mathbf{E}][Q]= [F] \\
[\epsilon_0][\mathbf{E}^2] = [Q][L^{-2}][F]/[Q] = [F][L]/[L^3] = [W]/[V] \\
$$
$$
[\mu_0^{-1}][\mathbf{B}][L] = [\mathbf{J}][L^2] \\
[\mathbf{B}][\mathbf{J}] = [F]/[L^3] \\
[\mu_0^{-1}][\mathbf{B}^2] = [\mathbf{J}][L^{-2}][F]/[\mathbf{J}] = [F][L]/[L^3] = [W]/[V]
$$

Which is energy density.

The momentum density must be proportional to:
$$
g(t,\mathbf{x}) \sim \mathbf{E} \times \mathbf{B}
$$

We know $[E] \sim \epsilon_0\mathbf{E}^2 \sim \epsilon_0 c \mathbf{E} \mathbf{B}$, then $[P] \sim [E]/[V] \sim \epsilon_0 \mathbf{E} \mathbf{B}$.

$$
g(t,\mathbf{x}) = \epsilon_0/c \mathbf{E} \times \mathbf{B}
$$

Poynting vector must be $[E][V] \sim c \epsilon_0 \mathbf{E}^2$. Then $\mathbf{S} = c^2 g(t,\mathbf{x})$.

The time average is simple, we use $\hat{e}$ as basis for simplicity:
$$
\braket{\mathbf{E}^2} = \frac{1}{4}(\hat{e} E e^{ikx} + \hat{e}^* E^* e^{-ikx})^2 \\
$$

Notice that, $e^{2i\omega t}$ in time period integral is zero. So $LHS = \frac{1}{2} E^2$.

## Constant and Isotopic Media

With $\epsilon\mathbf{E} = \mathbf{D}$ and $\mathbf{B} = \mu \mathbf{H}$. We know the wave propagation of $c^2 = \frac{1}{\epsilon_0 \mu_0}$ to $v^2 = \frac{1}{\epsilon \mu}$ and it's reasonable due to isotopic property, where every direction is unchanged.

$$
v \mathbf{B} = \hat{k} \times \mathbf{E} \\
\sqrt{\frac{\epsilon}{\mu}} \mathbf{H} = \hat{k} \times \mathbf{E} \\
\frac{c}{v} = \sqrt{\frac{\epsilon \mu}{\epsilon_0 \mu_0}} = \sqrt{\epsilon_r \mu_r} = n\\
k = \frac{\omega}{v} = \frac{n \omega}{c} \\
$$

Consider a interface in $n1,n2$. With boundary condition:
$\hat{n} \times (\mathbf{E_2} - \mathbf{E_1}) = 0$.

In incidence, transmition/refracted, reflection wave:$\mathbf{E}_i \sim \tilde{E}_i e^{ikr}$.

It's useful to notice that, for normal condition(Same for electric field):
$$
\bold{H_1} = \sqrt{\epsilon_1/\mu_0} (E_i \sin \theta_1 + E_r \sin \theta_1) \hat(z) \\
\bold{H_2} = \sqrt{\epsilon_2/\mu_0} (E_t \sin \theta_2) \\
E_i + E_r = E_t \\
\to \mu_1 \sqrt{\epsilon_1/\mu_1} \sin \theta_1 = \mu_2 \sqrt{\epsilon_2/\mu_2}\sin \theta_2 \\
\to n_1 \sin theta_1 = n_2 \sin theta_2
$$

So we only consider tangent boundary condition.

In media with $z=0$ boundary:

$$
\hat{n} \times (E_i e^{ik_i r} + E_r e^{ik_rr}) = \hat{n} \times (E_t e^{ik_t r}) \quad z=0
$$

If it satisfy in every possible $x,y,t$, we know $k_{ix/y} = k_{r x/y} = k_{tx/y}$

Which means there're all in the same plane, so we restrict it to $x-z$ plane. With:
$$
k_i = k_r \sim k_0 n_1 \\
k_t \sim k_0 n_2 \\
$$

Then we know $k_{ix} = k_{r x} \sim sin\theta_i = sin\theta_r$ and $k_{ix} = k_{tx} \sim n_1 sin\theta_i = n_2 sin\theta_t$.

We know that $|k_i| = \omega/v$, if $k_{tx} > |k_r|$,
which means:
$$
k_{tz} = \sqrt{k_r^2 - k_{tz}^2} = k_0 \sqrt{1 - sin^2 \theta (\frac{n_2}{n_1})^2} = ik_0\sqrt{sin^2\theta(\frac{n_2}{n_1})^2 - 1} \\
e^{ik_{tz}z} = e^{-k_0\sqrt{sin^2\theta(\frac{n_2}{n_1})^2 - 1}\, z}
$$

Which becomes decaying wave with $\kappa^{-1} z = (...)z$ as a characteristic distance.

Then, we can calculate energy flow:
$$
    \braket{S} = E \times H \\
    \braket{S}_x = E_y H_z - E_z H_y \\
$$
For $E \perp$ incident plane, we know $E_z = 0, E = E_y$, and $H \parallel$ incident plane, and we suppose it's on the $x-z$ plane, so $H_y$ = 0.

Then we know in the media:
$$
    E = E_0 e^{-\kappa z} e^{i(k_x x - \omega t)} = E_y\\
    H_z = \sqrt{\epsilon_2/\mu_2 } k \times E = (...) (k_x = \sin \theta) E_0(...) \\
    H_y = (...) i \sqrt{(\sin^2 theta)/(n^2_{21}) - 1} (...)
$$
Where $\kappa z$ is the decay wave, and $H_y$ is imagination part.

In the transmission media:
$$
    \braket{S}_x =  1/2 \sqrt{\epsilon_2/\mu_2} |E''|^2 e^{-2 \kappa z} \sin \theta/n_{2 1} \\
    \braket{S}_z = E_y H_x = 0
$$

We can decompose the incident wave $E_i = E_{i s} + E_{i p}$ which component perpendicular and parallel to the incident plane.

- $E \perp \text{incident plane} \sim E_{i p} = 0$

$\hat{t} \cdot ({E_2 - E_1}) = 0$ and $\hat{t} \cdot ({H_2 - H_1}) = K = 0$
$$
E_i + E_r = E_t \\
cos\theta_1 \sqrt{\frac{\epsilon_1}{\mu_1}}(E_i - E_r) = cos\theta_2 \sqrt{\frac{\epsilon_2}{\mu_2}} E_t \\
$$
Define:
$$
\tilde{r}_s = \frac{E_{rs}}{E_{is}} \\
\tilde{t}_s = \frac{E_{ts}}{E_{is}} \\
\mu \sim \mu_0 \to n \sim \sqrt{\epsilon_r}
$$

We get:
$$
\tilde{r}_s = \frac{n_2 cos\theta_2 - n_1 cos\theta_1}{n_1 cos\theta_1 + n_2 cos\theta_2} = \frac{sin(\theta_2 - \theta_1)}{sin(\theta_2 + \theta_1)} \\
\tilde{t}_s = \frac{2n_1 cos\theta_1}{n_1 cos\theta_1 + n_2 cos\theta_2} = \frac{2 sin\theta_2 cos\theta_1}{sin(\theta_1 + \theta_2)}
$$

- $E \parallel \text{incident plane} \sim E_{is} = 0$

$$
(E_{i} + E_{r})cos\theta_1 = E_{t}cos\theta_2 \\
\sqrt{\frac{\epsilon_1}{\mu_1}}(E_i - E_r) = \sqrt{\frac{\epsilon_2}{\mu_2}} E_t \\
$$

$$
\tilde{r}_p = \frac{n_2 cos\theta_1 - n_1 cos\theta_2}{n_2 cos\theta_1 + n_1 cos\theta_2} = \frac{\frac{1}{2} (sin2\theta_1 - sin2\theta_2)}{\frac{1}{2} (sin2\theta_1 + sin2\theta_2)} \\ = \frac{cos(\theta_1+\theta_2)sin(\theta_1-\theta_2)}{sin(\theta_1 + \theta_2)cos(\theta_1-\theta_2)} = \frac{tan(\theta_1-\theta_2)}{tan(\theta_1 + \theta_2)} \\
\tilde{t}_s = \frac{2n_1 cos\theta_1}{n_2 cos\theta_1 + n_1 cos\theta_2} = \frac{4 sin\theta_2 cos\theta_1}{sin2\theta_1 + sin2\theta_2} = \frac{2cos\theta_1sin\theta_2}{sin(\theta_1 + \theta_2)cos(\theta_1 - \theta_2)}
$$

The observation is below:
n
for $\tilde{r}_p$, if $\theta_1 + \theta_2 = \pi/2$, $\tilde{r}_p \to 0$, so $n_1 sin\theta_1 = n_2 sin(\pi/2 -\theta_2) \to tan\theta_1 = \frac{n_2}{n_1}$ which is **Brewster angle**.

for $\tilde{r}_s$, if $n_1 < n_2 \to \theta_1 > \theta_2 $, $\tilde{r}_s < 0$, which means $\pi$ delay phase factor. Actually, $\tilde{r}_p$ will be negative after $\theta_1 > \theta_{B}$ which is bigger than Brewster angle.

### Metal in Constant and Isotopic Media

$$
\mathbf{J} = \sigma \mathbf{E} \\
\nabla \times \mathbf{H} = \epsilon \frac{\partial \mathbf{E}}{\partial t} + \sigma \mathbf{E} \sim i\omega (\epsilon + \frac{\sigma}{i\omega}) \mathbf{E} = i \omega \epsilon' \mathbf{E} \\
$$

So does the $k^2$:

$$
k^2 = \omega^2 \mu (\epsilon + \frac{\sigma}{i \omega}) \\
k = \beta + i\alpha
$$

Suppose in low frequency limit: $\omega^2 \mu \epsilon \to 0$
$$
\beta^2 - \alpha^2 = \omega^2 \mu \epsilon \to 0 \\
\alpha \beta = \frac{1}{2} \omega \mu \sigma
$$

Results:
$$
\alpha = \beta = \frac{\sqrt{2}}{2}\sqrt{\omega \mu \sigma} \\
k \approx \frac{1 + i }{\sqrt{2}}\sqrt{\omega \mu \sigma}
$$

We know imaginary part induce the decay wave.

$$
k_I = (\frac{\omega \mu \sigma}{2})^{\frac{1}{2}} \\
\delta_{skin}(\omega) = 2\pi/k_I \sim (\frac{1}{\omega})^{\frac{1}{2}}
$$

Usually, for cooper in room temperature, it corresponding to a wave length much greater 50 $\mu \text{m}$, with roughly 10 MHZ frequency as infrared light. So in radio frequency, the interaction between vaccum wave and metal will focus on the surface mainly.

## Resonant Cavity/Wave Guide

Suppose in media, insulator for electromagnetic wave, which is metal for high frequency. We has:

$$
    e_n \times (E_1 - E_2) = 0 \\
$$
We know metal has $E_2 = 0$ almost, so:
$$
    e_n \times E = 0 \\
    e_n \times H = \alpha \\
    e_n \cdot B = 0
$$

We could suppose it's ideal wave model for it's excellent reflection property.

$$
    E(t, x) = E_0(x,y,z) e^{-i \omega t + i k x}
$$

We list the maxwell equation, could yield:
$$
    (\frac{-1}{c^2} \frac{\partial^2}{\partial t^2} + \nabla^2 ) E = 0 \\
    \omega^2/c^2 E_0 + \nabla^2 E_0 = 0 \\
    k^2 E_0 + \nabla^2 E_0 = 0
$$

For example, the $x$ plane, the corresponding boundary condition on one side must be like:
$$
    E_{y/z}|_{x=0/a} = 0 \\
$$
With divergence condition for normal:
$$
    \frac{\partial E_x}{\partial x}|_{x=0/a} = 0 \\
$$

For general $E_n$ on normal direction $n$.

Then above would give the integer-mode for $k$:
$$
    k_i = (m \pi)/(L_i) \quad m \in \bf{Z}
$$
With divergence, we know it must has, for amplitude:

$$
    k_i A_i = 0 \\
    \omega = c \pi \sqrt{(\frac{n_i}{L_i})^2}
$$

Notice, from divergence we know there's no $001$ eigenvalue because two defines all three mode, so the final is also zero.

The thing could be simpler for wave guide, because one directions the boundary condition disappear, then for any kinds of $k$ is fine, so it could be a arbitrary $m,n$ and a independent $l$ for a direction.
