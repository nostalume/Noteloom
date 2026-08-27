+++
date = '2025-04-22T19:12:58+08:00'
draft = false
title = 'Special Relativity'
tag = ["physics", "special relativity"]
author = ["nostalgia"]
+++

## Symmetry

$$
t' = \gamma(t - \frac{v}{c^2}x) \\
x' = \gamma(x - vt)
$$

or:

$$
ct' = \gamma(ct - \beta x) \\
x' = \gamma(x - \beta ct)
$$

Which is same for interval as a vector.

What does it say? It means we describe the 4-vector component in another frame $\Sigma'$ by $\Sigma$. That's means basis will changes reversely($t' \hat{t'} + r' \hat{r'}$).

It's symmetric that $x'^\mu = \Lambda^\mu_\nu x^\nu \lrarr x^\mu = \Lambda^{-1 \mu }_\nu x^\nu$.

Where reverse just be $\Lambda(-v) = \Lambda^{-1}(v)$.

Contraction: We measure length in which the time of the frame is instant, that's the time interval is zero:$\Delta t = 0$

We use symmetry to deduce in opposite direction:

Suppose $(..)'$ is the measure frame.
$$
t' = \gamma(t-(v/c^2) x) \\
x' = \gamma(x - v t) \\
$$

We only know $t' = 0$, so $t = (v/c^2)x$, then

$$
x' = x/\gamma
$$

Or reversely:

$$
x = \gamma(x' + v t') \\
t' = 0 \\
x/\gamma = x'
$$

Dilation: We measure time in which the position of the frame is instant, that's the position interval is zero:$\Delta x = 0$

We also deduce in oppsite direction:

$$
t' = \gamma(t-(v/c^2) x) \\
x' = \gamma(x - v t) \\
$$

We know $x = vt$, then
$$
t' = t/\gamma
$$

Notice that $t'$ is the answer of clock comoving(relative static) with the measure frame, which goes slower, giving a shorter time.

$$
t = \gamma(t' + (v/c^2)x')
$$

Gives: $t' = t/\gamma$.

### Implicit Condition

Another exposition, which is rather common, is to choose $x = 0$ rather $x' = 0$. indicating the clock is comoving with the original frame, which results $t' = \gamma t$, a.k.a the clock time in original frame measured by measure frame is longer, giving us time dilation.

Usually, if we measure time of a event interval in measure frame, it won't gives $x' = 0$ because the event usually moves.

Samely in length contraction, choose $t = 0$ means we measure in original frame rather measure frame. Due to symmetry, we will results the same answer(with relative velocity $-v$). But we now know that $t=0$ in one frame doesn't impose $t'=0$ in the other frame.

We could deduce another of another frame by repeating transformation.
$$
t'' = \gamma'\gamma(1- \frac{v'v}{c^2})t - \gamma'\gamma\frac{v' - v}{c^2}x \\
x'' = \gamma'\gamma(1-\frac{v'v}{c^2})x - \gamma'\gamma(v' -v)t \\
$$
Or: $\eta = \gamma \beta$
$$
ct'' = (\gamma'\gamma - \eta' \eta) ct - (\gamma \eta' - \gamma' \eta) x \\
x'' = ...
$$

Which is just matrix composition.

The useful information can be extracted that:

$$
(\gamma' \gamma - \eta' \eta) = \gamma'' \\
(\gamma \eta' -\gamma' \eta) = \eta'' \\
\frac{\eta''}{\gamma''} = \beta'' = \frac{\beta' - \beta}{1- \beta'\beta}
$$

Above is a underneath condition for many problems.

However, they are many possible condition that given a measure information in one frame and deduce in another or possible, another and another frame...

Example(**All movement is in same direction**):

Suppose a stick with rest length $l_0$, moving with velocity $v$ in a certain frame $\Sigma$, we want to measure the length by a frame $\Sigma'$ with a velocity $-v$ relative to the certain frame $\Sigma$.

This problem involves 3 different frame, and we only knows two given information one is explicit, one is underneath that in:

Choose stick rest frame is $\Sigma_l$:

$$
\Sigma_l: x = l_0 \\
\Sigma': t' = 0
$$

We apply in this routine, because $t' = 0$, we expand to $\Sigma'$ rather from it:

$$
l_0 = \gamma(v) (x-vt) = \gamma(v)\gamma(v')(1-\frac{vv'}{c^2})x' + (...)t'
$$

Apply $t' = 0$, and $v = v, v' = -v$:

$$
l_0 = \frac{(1+v^2/c^2)}{(1-v^2/c^2)}x' \\
x' = \frac{(1-v^2/c^2)}{(1+v^2/c^2)}l_0
$$

Which is reasonable because it should be shorter.

**We see that the most often confusion comes from the implicit condition**.

What if $l_0$ isn't the length at rest, rather, is the length measured in $\Sigma$, and we change $-v$ to arbitrary $u$, what's the result?

We still list the condition:
$$
\Sigma: x = l_0 \\
\Sigma': t' = 0
$$

$$
l_0 = \gamma(u)(x'-vt') \\
t = \gamma(u)(t' - \frac{u}{c^2}x')
$$

Impose condition, get: $t = -\gamma(u)\frac{u}{c^2}x'$. Isn't that a addtional unuseful for our dedution? It seems we already get the answer from first equation.

The answer is no, the left hand shouldn't be $l_0$. Because in previous example, $l_0$ is at rest, so no matter $t$ changes in the original frame, the space interval is always the same. But if the event(like particle, stick, car etc...) are moving, now we impose the third principle beside above two:

$$
x = vt + c \\
$$

Thus:
$$
\Sigma: x = l_0 + vt
$$

For a event interval relation, the $v$ isn't frame relative velocity, but the event velocity observed in one frame. It's just like Galileo principle(Actually is reduced form in Poincare transformation), because we didn't suppose a invariance in frame transformation. If the event interval contains no velocity, we are back to $c = l_0$ as usual. If the event space interval is zero, we are back to $x = vt$.

Now back to our first equation:

$$
l_0 + vt = l_0 - \gamma(u)\frac{vu}{c^2}x' = \gamma(u)x' \\
x' = \frac{l_0}{\gamma(u)(1+vu/c^2)}
$$

Now we check positive or negative by $\plusmn vu$
If $u$ is in same direction with $v$, the length contraction effect should be reduced, a.k.a longer. So, it should be $-vu$, and vice versa.

Suppose a S-R device with a length $l_0$, sunk at the medium with refractive index $n$. Suppose the medium moves at velocity $v$, we want to measure the time of light from S to R.

We have two frame, first is comoving with medium $\Sigma$, and second is comoving or rest with S-R device $\Sigma'$.

list condition:
$$
\Sigma: v_0 = \frac{c}{n}, x = v_0t \\
\Sigma': x' = l_0
$$

$$
x = \gamma(x' - vt') \\
t = \gamma(t' - \frac{v}{c^2}x')
$$

Impose condition:
$$
t' = \frac{\frac{v}{nc}+1}{\frac{c}{n}+v} l_0
$$

Which is correct.

---

### Angle

Now we extend to situation involving angle or multiple directions.

In multiple directions, we then generalize by:

$$
\gamma = (1- v^2/c^2)^{-\frac{1}{2}} \\
\eta_i = \gamma \beta_i = \gamma v_i /c \\
$$

Notice $v^2$ is $v_iv^i$, sum all directions.

Then we could extracted different boost in different direction.

What if the boost isn't on direction of given basis like $x,y,z$?

$$
ct' = \gamma ct - \eta_i x^i_{\parallel} \\
x'^i_{\parallel} = \gamma x^i_{\parallel} - \eta^i ct \\
x'^i_{\perp} = x'^i_{\perp}
$$

We see in $\eta^i = \eta_i$ because it's space component

$$
x'^i = \gamma x'_{\parallel} - \eta^i ct + x'^i_{\perp}
$$

I found that decompose $x^i_{\perp} = x^i - x^i_{\parallel}$ to deduce further isn't much useful in problem solving.

This also indicates that previous condition will be extended to:
$$
x_i = v_it + c_i\\
v_iv^i = v^2
$$

---

The first problem we usually want to solve is, in original frame, what's the angle measured in measure frame?

$$
x = \gamma(x' - vt') \\
t' = 0 \\
x/\gamma = x' \\
y = y' \\
tan\theta' = y'/x' = \gamma y/x = \gamma tan\theta
$$

Second, extend the previous S-R problem, what if the medium moving in another direction perpendicular to $x$?

Suppose the frame comoving with S-R is $\Sigma'$ and comoving with media is $\Sigma$.
$$
\Sigma': x' = l_0 = v'_x t' \\
y' = 0 = v'_y t'\\
x' = (c/n) t' = v_x' t'
$$
$$
\Sigma: x = l_0 = v_x t\\
y = v_y t
$$

With final condition on total velocity(This can be applied to every frame):
$$
v_x^2 + v_y^2 = (c/n)^2 \\
$$

$$
x = x' \\
y = \gamma(y' - vt') \\
t = \gamma(t' - \frac{v}{c^2}y') \\
$$

Solve it by directly plugin $t = l_0/(v_x)$:
$$
t' = l_0/(\gamma v_x) \\
y = v_y t = v_y l_0/v_x = \gamma v t' = \gamma v l_0/v_x' \\
v_y/v_x = \gamma v/v_x' \\
v_x^2 (1 + (\frac{\gamma v}{v_x'})^2) = (c/n)^2
$$
Pluin the $v_x$ into $t$ we yield the final results.

We should notice that in $\Sigma$, S-R is moving in $y$ direction with velocity $-v$ could be derived in the first equation. Therefore the problem could be reformulated that what if S-R is moving in $y$ direction.

---

## Four-vector dynamics

$d\tau = dt/\gamma(v) = dt'/\gamma(v') $ is a invariance.

Second, we know the 4-vector position is invariance.

So $\frac{dx^\mu}{d\tau}$ is a invariance governed by lorentz transformation.

Here, we notice that, the $\gamma$ in the differentiation, stem from the velocity of the 4-vector position rather a general frame transformation.
Usually, give us:
$$
\frac{dx^\mu}{d\tau} = \gamma(v)(c,v^i) = u^\mu \\
u^\mu u_\mu = -c^2
$$

Follow the same routine, we know the **rest** mass is a invariance, define momentum as:
$$
p^\mu = mu^\mu \\
p^\mu p_\mu = -m^2c^2 \\
$$

Choose $v=0$ as rest case:
$$
-p_0^2 = -m^2c^2 = -E^2/c^2 \\
dE/dt = v^i dp^i/dt
$$

Comment:
use lagrangian is more abvious:$-mc^2\int d \tau $.
The same refrain that: $p'^\mu = p'^0\hat{t'}+ p'^i \hat{x'^i}$

Follow the same routine, we differentiate again:
$$
a^\mu = \frac{d u^\mu}{d \tau} \\
f^\mu = ma^\mu \\
$$

However, we also known that we can't acquire $\tau$ as a parameter in real life, so $dt$ is also a useful representation, we often extract space component as the information of certain frame can view.

$$
v^\mu = (c,v^i) \\
F^\mu = f^\mu / \gamma(v) = \frac{1}{\gamma(v)}(m \frac{d u^\mu}{d \tau})
$$

Another confusion is that why we didn't define $F^\mu = \frac{d^2 x^\mu}{d t^2} $, we see that due to second differentiation, it doesn't fully match.

It only works that, in electromagnetics, the force proportional to $u_v$.

$$
f^\mu = \frac{dp^\mu}{d\tau} = q F^{\mu\nu}u_\nu \\
= q(\frac{u^0}{c}\mathbf{E} + \mathbf{u} \times \mathbf{B}) = q \gamma (\mathbf{E} + \mathbf{v} \times \mathbf{B})
$$

Now we see if we define $F^\mu = 1/\gamma(v) f^\mu$ is consistent:
$$
\frac{d p^i}{d t} = q(E^i + \epsilon_{ijk}v_j B_k) \\
\frac{d p^0}{d t} = q E^i v_i
$$

---

Conceptually, invariance and momentum conservation tell us that $p^\mu_{in} = p^\mu_{out}$ which is applicable in every possible frame.

A rather complicated thing is CP frame and lab frame transformation:

We know that $E/c = p^0$. We know $p^0$ is the observer frame in which observer take the component as mass energy they view which is $m'c$.

So $\sum_i E_i/c^2 \mathcal{V} = \sum_i p_i $

Where $p_i$ is the space part of 4-vector momentum of each particle.

However, does $\sum_i p'_i = 0$?

We see that $\sum_i p'_i = \sum_i \gamma(\mathcal{V})(\bold{p}_i - \frac{\mathcal{V}}{c} E_i/c) = 0$

Give us the same results.

That's indicates this is a lorentz invariance, because CP frame is inherited from the particles system rather from a specific frame.

Suppose we know only $E_1$, $m_2$ and $p^i_1$, which is the observer could view.

$$
\mathcal{V}^i = \frac{p^i_1}{E_1/c^2 + m_2}
$$

The modulus could be computed, by $p^ip_i = E^2/c^2 - m^2 c^2$

$$
\mathcal{V} = \frac{\sqrt{p^ip_i}}{E_1/c^2+m_2} \\
= \frac{\sqrt{E^2/c^2 - m^2c^2}}{...}
$$

The tricky thing is related to momentum transformation which is:

$$
\gamma_{CP} = \gamma(\mathcal{V})
$$

Things can be reduced if we only consider two particles with one is at rest, which is the usual case:

$$
E_2'/c = \gamma(\mathcal{V}) m_2 c \\
p'^i_2 = \gamma(\mathcal{V}) m_2 (-\mathcal{V^i}) \\
$$

by: $p_1' + p_2' = 0$

$$
p'^i_1 = \gamma(\mathcal{V})(p^i - (\mathcal{V^i}/c)E_1/c) \\
p'^i_1 = - p'^i_2 = (...)\mathcal{V^i} \\
E'_1/c = \gamma(\mathcal{V})(E'/c - (\mathcal{V^i}/c) p_i)
$$
