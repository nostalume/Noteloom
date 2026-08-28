# Magnetostatics

$$
\begin{align}
\mathbf{A} &=
\frac{1}{4\pi \mu_0}\int dS \boldsymbol{M}(\boldsymbol{r'})\times \nabla \frac{1}{|r-r'|} \\
&= - \frac{1}{4\pi \mu_0}\int dl  (\boldsymbol{M}(r')\frac{1}{|r-r'|}) + \frac{1}{4\pi \mu_0}\int dS \nabla \times \boldsymbol{M}(r') \frac{1}{|r-r'|}
\end{align}
$$

We can see $\boldsymbol{m}\times \hat{n}$ or $\boldsymbol{m} \cdot \hat{t} = \boldsymbol{K} $ which is boundary current. $\nabla \times \boldsymbol{m} = \boldsymbol{j}$ which is the bound current.

$$
\begin{align}
    \nabla \times \mathbf{B} = \mu_0 (j_f + j_c ) \\ = \mu_0 (j_f + \nabla \times \mathbf{M}) \\
    \frac{1}{\mu_0} \nabla \times (\mathbf{B} - \mu_0 \mathbf{M}) = \mu_0 j_f \\
    \nabla \times \mathbf{H} = \nabla \times (\mathbf{B}-\frac{1}{\mu_0} \mathbf{M}) = \mu_0j_f
\end{align}
$$
