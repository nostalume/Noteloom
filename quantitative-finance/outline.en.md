# Quantitative Finance: From Usable Information to Executable Decisions

Argument-based core outline v0.7 — aligned with the seventeen-chapter lecture · 2026-10-12 · bilingual prose revision

## Purpose and scope

This outline sets out the tutorial's content, order of argument, main conclusions, and practical starting points alongside the completed seventeen-chapter Typst lecture. The preceding revision supplied missing derivations and explained concepts at their first use; this revision improves the flow of both language editions. Once the exposition has matured, its judgments and procedures can be developed into skills. The present work focuses on the tutorial; skill changes, trading-system construction, and publication remain separate projects.

**Language and revision convention:** maintain the English and Chinese outlines and lectures together, preserving their arguments, formulas, examples, assumptions, and references. Each edition follows the conventions of its language while conveying the same content. Earlier Chinese outlines remain historical references; the paired editions are the current reading and revision copies.

The tutorial draws on the supplied excerpts from *Misaligned Quantitative Finance* and related material, developing their insights into target design, information representation, search and verification, estimation error, and implementation. It reconstructs the arguments so that terminology, model choices, and scope can be understood. Coverage follows the material actually obtained: the author's profile was incompletely accessible and some excerpted formulas were missing. Those gaps remain identified.

### From a principle to a usable starting design

A principle becomes useful when the reader can begin research with it. Each major task therefore answers four questions: **what to do first, how to construct it, why it is an appropriate starting point, and what observation would warrant a change of course**. Chapters develop a workable design and then use counterexamples and failure cases to explain its reach.

Conclusions operate at three levels: mathematical consequences under stated assumptions, defaults selected for recurring tasks, and empirical winners established by matched tests. Keeping these levels clear allows a decisive, well-supported design choice. The direction layer starts with binary probabilities; engineered timing factors go first to shallow trees; cross-sectional relations use restrained set attention; allocation uses risk budgets when expected returns lack support. Each choice comes with an explanation and an implementation path, while empirical comparisons require the corresponding tests.

The numerical settings below are **fixed teaching starting points**. They make the first experiment reproducible and show what each parameter does. Small, recorded development comparisons can guide changes. Their role is to establish a clear experiment; optimality and actual performance require further evidence.

### Reader prerequisites and exposition

Assume only basic linear algebra, calculus, and probability: vectors, matrices, derivatives, integrals, random variables, expectation, and variance. Conditional expectation, information theory, statistical inference, optimization, machine learning, online learning, stochastic processes, stochastic calculus, and changes of measure enter progressively through the problems that call for them. When a basic operation is unfamiliar, provide a small example sufficient to continue.

Sections follow the needs of their problems, with several shared expository commitments:

- Begin with a concrete trading, observational, or computational difficulty and explain why the existing approach is inadequate.
- State the objects, timestamps, units, and available material before introducing a new concept.
- Explain consequential symbols, operations, and assumptions beside their formulas so the reader can reconstruct the argument behind a technique.
- Distinguish definitions, conditional deductions, empirical observations, approximations, and unverified hypotheses.
- Use counterexamples to clarify scope, and interpret code and equity curves through their mechanisms and evidence.
- Choose structures for the distinctions they preserve and the operations they enable. Introduce concepts in the main text and use appendices for supporting detail.

First-passage labels, for example, begin with two paths that share an endpoint but have different intermediate gains and losses. Comparing their outcomes under an exit rule reveals what a fixed-horizon label leaves out and motivates the first barrier-hitting time. Replication starts with stock and cash on a binomial tree; the resulting price can then be rewritten as a discounted average under another set of probabilities.

### The book's organizing argument

Quantitative research constructs justified, testable, implementable decisions for a defined task. Information theory explains the input–target relation, statistics examines what finite data can establish, and portfolio construction and execution determine the conditions under which predictions become realized results. Information metrics serve this decision-making purpose.

The book builds four bridges:

1. From an economic problem to observable and learnable objects.
2. From relations in data to verified predictions or structural judgments.
3. From judgments to constrained holdings, cash flows, and achievable returns.
4. From specified contracts and models to pricing, numerical computation, and hedging.

These bridges connect the stages and provide routes for revision. Inadequate data, failed validation, or infeasible execution may call for a change to the original representation of the problem.

### Revision history: explain the principle before delimiting it

Version 0.1 compressed important arguments into tool names and correction notes. Version 0.2 substantially rewrote forecasting limits, features and labels, optimization, and the factor pipeline. Version 0.3 checked all seven attachments and supplementary conversation material, brought the remaining chapters to comparable depth, and added learning-rate–batch–gradient-noise derivations, distinctions among information concepts, and a coverage audit. These revisions connect motivation, construction, conclusion, and conditions, using corrections to clarify the methodology.

Version 0.4 rechecked single-instrument timing, cross-sectional relation learning, multi-asset allocation, and the eight-step closing summary. It corrected the tendency for caveats to overwhelm design conclusions. Separate mathematical necessities, the book's selected research defaults, and empirical claims requiring confirmation. Say what to do first, why the derivation supports it, and what evidence would justify changing course. A clear task scope supplies the basis for decisive design judgments.

Version 0.5 audits the same problem at the construction level. Some v0.4 conclusions named a preferred family but still left the first experiment, parameter choices, decision mapping, or replacement rule unspecified. Each chapter now has an integrated practical default. Binary coarse-graining includes its information-retention comparison and a probability-to-action procedure; the other chapters likewise connect derivations to an executable research design. These routes support offline teaching; performance is established through subsequent tests, and live operations require separate authorization.

Version 0.6 audits the completed seventeen-chapter lecture equation by equation. It supplies missing conditioning, algebra, chain-rule, expectation, variance, normalization, and inequality steps; separates finite constructions from cited limit theorems; repairs notation errors; and synchronizes the outline and Chinese edition. The checks cover symbols, inputs, operations, intermediate equalities, conclusions, and scope.

Version 0.7 revises the organization of prose in both editions. Concrete mechanisms, causal explanations, and paragraph transitions carry the argument, with necessary conditions and scope integrated into the analysis. Formulas, examples, and explicit practical choices remain intact.

**Navigation convention:** the numbers below identify outline design points. Lecture subsections follow the expanded exposition and have their own numbering. The coverage audit uses chapter-level topics, with lecture navigation listed separately to keep references accurate as the text grows.

Source mapping: the source's “Limits of Prediction” maps to Chapter 1; “Why Feature Engineering and Labeling Are Needed” maps to Chapter 2 and is implemented in Chapters 3 and 5. [Source Chapter 4, Optimization: How to Search for Factors](https://zhuanlan.zhihu.com/p/2081433899159250399) maps to Chapter 7. [Source Chapter 5, The Factor Pipeline](https://zhuanlan.zhihu.com/p/2081770959481082320) maps to Chapter 8 and connects to Chapters 9–12. Earlier direct access to both links returned HTTP 403. The reconstruction therefore uses the pasted optimization and pipeline material; the latest complete pages remain unchecked.

### Principles running through the book

1. **Prediction is bounded by the information supplied.** Representation, estimation, and optimization help a model use its observations; observational limits and irreducible error bound its eventual ability. Diagnose the bottleneck before deciding how to expand capacity.
2. **Targets match decisions.** Trend timing starts with direction or first-passage outcomes, and cross-sectional selection starts with ranking. These targets remove precise-price details irrelevant to the action while separately retaining distinctions needed for payoff, cost, and risk.
3. **Feature engineering makes information usable.** New observations may add conditional information; deterministic transformations may turn existing relations into a representation a limited model can use. Each route has a distinct role and information-theoretic explanation.
4. **Choose structure and capacity separately.** First make the required relation expressible; then restrict freedom using credible priors, constraints, and the support provided by the sample.
5. **Optimization depends on supplied feedback.** Zeroth-, first-, and second-order methods obtain different levels of information. Search develops around that feedback; a score misaligned with the task gives stronger search more power to fit the wrong objective.
6. **Account for search intensity and its statistical cost together.** A high score depends on the complete trial and selection history. More throughput also produces more opportunities for attractive noise.
7. **Separate discovery from confirmation across the entire chain.** Labels, transforms, generation, models, and portfolios all participate in selection. Repeatedly selected-on data are no longer untouched confirmation data.
8. **A factor library stores conditional knowledge.** Expressions, definitions, data lineage, selection history, validation distributions, costs, and scope form a research record in which a high IC has an interpretable meaning.
9. **Infrastructure supports credible evaluation.** Correct data, reliable scoring, and affordable throughput jointly determine research capacity. Software and cluster choices are evaluated through their actual contributions to these capabilities.
10. **Prediction has to survive portfolio construction and execution.** Constrain unsupported exposures and choose the scope of optimization according to the evidence. Monitoring and retirement belong to research, and the ability to supply fresh alpha also needs testing.
11. **Learning rates govern different objects and scales.** A gradient step controls numerical updates, boosting shrinkage controls new-tree contributions, and an expert learning rate controls concentration of trust. Curvature, noise, or properties of the relevant loss justify their values; mutual information has no direct conversion into these quantities.
12. **Realizing an edge depends on cash-flow structure.** Trends, events, statistical relations, and strict replication have different foundations. Research examines both the eventual payoff and the ability to meet margin and financing demands along the way.
13. **Pricing and forecasting answer different questions.** Pricing under a fixed model is deterministic, allowing learning to amortize computation. Values, derivatives, boundaries, model errors, and hedging errors each have their own evaluation.
14. **Regularization accounts for information retention.** Low-amplitude components may contain useful signals even as unsupported freedom is restricted. The effects of reconstruction, sparsity, normalization, and optimization stability are evaluated in the intended task.
15. **Every major principle yields a constructive default.** Move from a starting representation and estimator or algorithm to parameter selection, evaluation, and reasons to change course. Exceptions and counterexamples help the reader understand the reach of that route.

### Eight buy-side steps and their dependencies

Define the economic task → construct labels → establish point-in-time data → construct features → search and independently verify → aggregate and model → form risk-constrained positions → temporal backtest, implement, and monitor.

**The book gives priority to target design, usable relations, and independent verification before addressing the model's remaining gap.** In the refined-factor route, this directs effort toward labels, features, and verification. Three practical cases and the closing summary turn these priorities into concrete designs.

Dependencies connect the eight stages. Labels specify the problem, data determine whether they can be constructed from available information, representations determine what limited models can see, verification supplies grounds for trust, and portfolios and execution test economic consequences. Failure sends revision back along the relevant dependency. The factor pipeline repeatedly generates, verifies, admits, uses, and monitors factors within this broader strategy-development process.

## Part I: Forecasting limits and task reconstruction

### Chapter 1 — Forecasting limits: connect information, models, and decisions

#### 1.1 Begin with an “accurate” price curve

Compare forecasts that both lie close to actual prices: one merely copies today's price into tomorrow; the other captures some next-period increment. Both curves may look attractive, yet have different trading value. We therefore ask what additional judgment the input supplies about future tradable outcomes beyond the price already known.

Ignoring financing, dividends, and contract multipliers, holding $q_t$ units produces cash P&L $q_t(P_{t+h}-P_t)-C_{t,t+h}$. Distinguish price levels, increments, simple returns, and log returns. Log returns add across time but do not replace cash-flow accounting. Comparisons along time, assets, and events produce timing, cross-sectional, and event tasks. Alpha describes performance relative to an explicit benchmark and risk interpretation; a positive return alone leaves that comparison unspecified.

**Principle:** construct the prediction target from the economic problem. Compare with available persistence and historical-mean baselines to identify the incremental contribution behind a visually attractive fit.

#### 1.2 Why an observation cannot reconstruct the entire market

Use different supply-and-demand configurations yielding the same price to introduce hidden state $S$ and observation $X=g(S)$. If $g$ is many-to-one, there can be $S_1\ne S_2$ with $g(S_1)=g(S_2)$. Any algorithm receiving only $X$ must treat them as the same input. If the required outcomes differ, it cannot answer both correctly. This limitation comes from observational indistinguishability: the optimizer receives the same input in both states.

Price histories, trades, orders, and fundamentals each reveal different aspects of the market, so the observation mechanism deserves a more specific description than an irreversible “hash.” Many-to-one observation does not imply every consequence is unpredictable: if the states have the same effect on target $Y$, losing their distinction is harmless for that target.

Construct information measures first for finite discrete outcomes. A probability forecast $q(y)$ has log loss $-\log_2q(y)$. With true probabilities $p(y)$, define:

$$
H(Y)=-\sum_y p(y)\log_2p(y),\qquad
D(p\Vert q)=\sum_y p(y)\log_2\frac{p(y)}{q(y)}.
$$

Subtract logarithms to obtain average loss $H(Y)+D(p\Vert q)$; prove $D\ge0$ using $\ln u\le u-1$. For $X=x$, divide joint by marginal probabilities to form a conditional distribution, then average its entropy over observations to obtain $H(Y\mid X)$. Thus:

$$
I(X;Y)=H(Y)-H(Y\mid X).
$$

Mutual information is the improvement in optimal average log loss supplied by observation. Along the actual observation and deterministic-feature chain $S\to X\to F$, complete input can simulate every predictor using its summary, so $I(F;Y)\le I(X;Y)\le I(S;Y)$. For a general stochastic chain, establish the corresponding conditional-independence assumptions before using this inequality.

**Principle:** a model can exploit only distinctions it actually receives and that matter to the target. If a crucial distinction has disappeared, add observations or change the question. Depth cannot recover erased distinctions. Noninvertibility therefore limits the distinctions a forecast can use, with its consequences depending on the particular target.

#### 1.3 Three boundaries inside prediction error

Let $m(X)=\mathbb E[Y\mid X]$, introducing conditional expectation as the average under the post-observation distribution. With a finite second moment, expand the square. The cross term vanishes because $\mathbb E[Y-m(X)\mid X]=0$:

$$
\mathbb E[(Y-f(X))^2]
=\mathbb E[(Y-m(X))^2]+\mathbb E[(m(X)-f(X))^2].
$$

For a restricted model family $\mathcal F$, define $R_{\mathcal F}^*=\inf_{f\in\mathcal F}\mathbb E[(Y-f(X))^2]$. Decompose the population risk of the trained predictor $\hat f$:

$$
R(\hat f)
=R^*+(R_{\mathcal F}^*-R^*)+(R(\hat f)-R_{\mathcal F}^*),
\qquad R^*=\mathbb E[(Y-m(X))^2].
$$

The terms are the irreducible component under the current information set, the family's expression gap, and the actual fit's gap from the family's optimum. The last term includes finite-sample estimation and optimization; without further argument they are not independent additive error components.

Likewise, a valid probability forecast has log loss $H(Y\mid X)+\mathbb E_XD(p(\cdot\mid X)\Vert q(\cdot\mid X))$. Enlarging the family may reduce approximation error, but cannot reduce $H(Y\mid X)$ for the same input and target. Inadequate samples can make actual prediction worse.

If the future target is additionally assumed independent of current observations, then $H(Y\mid X)=H(Y)$ and $I(X;Y)=0$; the squared-loss optimum is the unconditional mean. The impossibility of improvement comes from independence, not a noisy-looking chart. Unanticipated information can create difficult residuals, but zero conditional mean is not residual independence, and an unobserved mechanism is not proof of no statistical relation.

**Principle:** diagnose observation, representation, sample, or optimization bottlenecks before adding capacity. For thin signals, model restraint follows from the available resources and estimation burden; the suitability of an architecture still depends on the task and evidence. Training error and population risk are different quantities.

#### 1.4 Precise prices may request far more information than a useful forecast supplies

Given today's price, approximate tomorrow's increment by a Gaussian with standard deviation $\sigma$ and discretize it into bins of width $\delta$. Approximate bin probabilities by $p_j\approx f(z_j)\delta$, substitute into discrete entropy, and approximate the sum by an integral:

$$
H_\delta\approx-\int f(z)\log_2f(z)\,dz-\log_2\delta
=\log_2\frac{\sqrt{2\pi e}\,\sigma}{\delta}.
$$

The last step uses the Gaussian log density and $\mathbb E[Z^2]=\sigma^2$. It requires bins fine relative to volatility and a declared treatment of tails. It measures the burden of discrete precision, not a unit-invariant continuous entropy.

Now let standardized signal $X$ and standardized future increment $Z$ be jointly Gaussian with correlation $\rho$. Conditional variance is $1-\rho^2$. Computing unconditional and conditional Gaussian entropies and subtracting gives:

$$
I(X;Z)=-\frac12\log_2(1-\rho^2)
\approx\frac{\rho^2}{2\ln2}\quad(|\rho|\text{ small}).
$$

Use $\sigma=1$ yuan, $\delta=0.02$ yuan, and $\rho=0.05$ **as teaching parameters, not reconstructed missing source numbers**. Target entropy is approximately $7.69$ bits; this signal's information about the complete increment is about $0.001806$ bits. Under fine discretization the latter serves as an upper bound and approximation benchmark for discrete mutual information. Their ratio is about $0.0235\%$: the target requests many distinctions while this signal helps with very few.

**Principle:** numerical precision, predictable structure, and trading-required precision are separate questions. Interpret these numbers within the specified signal, distribution, and grid. They quantify its recoverable proportion; judgments about price copying, numerical prediction, and MSE require out-of-sample model comparisons.

Encoding must also retain required geometry. If neighboring bins are unrelated categories, ordinary cross-entropy does not distinguish a one-bin miss from a distant miss by numerical distance. Structured representations, order constraints, or suitable losses can preserve distance. Whether a tokenized model learns numerical relations depends on its representation, loss, and data. Encoding and the economic value of a target remain different issues.

#### 1.5 Why an edge may remain: drift, friction, and breadth

Write future returns as $Y=m(X)+\epsilon$ with $\mathbb E[\epsilon\mid X]=0$. Risk compensation, gradual information diffusion, supply-and-demand constraints, and participant behavior may change conditional means or distributions. Each explanation motivates a separately testable economic hypothesis whose signal strength can vary across markets. Distinguish public-signal claims from the applicable market-efficiency hypothesis; risk premia are not automatically mispricing.

Hit rate $p$, average gain $G$, average loss $L$, and cost $c$ imply $\mathbb E[\Pi]=pG-(1-p)L-c$. For $p=0.6,G=1,L=2,c=0$, expected loss is still $0.2$. Conversely, a positive net expectancy can be repeatedly realized when risk and dependence are controlled: $N$ independent, equally scaled trades have mean $Na$ and standard deviation $\sqrt N s$, giving mean-to-standard-deviation ratio $(a/s)\sqrt N$. Retain covariance when trades depend on one another. Stock count and trade count are not independent breadth.

**Conclusion:** use forecasting limits to direct effort toward questions that matter to the decision and can be supported by the inputs. The next chapter develops this route through target and representation design.

#### Practical default — a directional forecasting experiment

For a trend direction layer, start with $B_t=\mathbb1[R_{t,t+h}>0]$ and estimate $p_t=\Pr(B_t=1\mid F_t)$ using binary log loss. Define the feasible entry, holding horizon, and treatment of zero returns before constructing labels. Compare a no-input frequency forecast, a fixed momentum sign, and a restrained classifier on the same opportunities. Use features computable before entry, and evaluate held-out probability loss and the fixed policy's net cash outcomes separately.

**Why this is the default.** The Gaussian calculation explains this alternative: $H(B)=1$ while $I(X;B)\approx\rho^2/(\pi\ln2)$, retaining about $2/\pi$ of complete-increment information at weak correlation. At the chapter's teaching parameters, the recoverable fraction rises from $0.0235\%$ to $0.1148\%$, about $4.9$ times. The target drops expensive, action-irrelevant distinctions while retaining a substantial part of the directional relation. Chapter 2 derives this result and turns probabilities into actions.

For profit/stop exits, replace the fixed-horizon sign with Chapter 3's policy first-passage classes. Retain magnitude estimates where costs, asymmetric payoffs, or risk sizing require them; give each estimate its place in the decision process while retaining the directional default. Begin by specifying the target, features, baselines, decisions, and timestamps.


#### Derivation checkpoints retained in the lecture

Expand mutual information as a double sum before identifying the average KL divergence; explain the law of total expectation when removing the conditional squared-error cross term. In the Gaussian construction, verify the completed square, normalize the marginal density, and explicitly cancel unconditional and conditional density entropies. Differentiate binary entropy twice to derive its Taylor coefficient. Rearrange the gain/loss expectation into both long and short thresholds, retaining the no-trade band and the fixed-payout assumptions.

#### Market-specific first experiments

Retain three distinct first experiments: A-share continuation versus reversal under executable holding and sale permissions; mechanically detected crypto stress with liquidity-based abstention and a separate unleveraged baseline; and a documented equity-token contract conditioned on reference-market availability. Rapid price moves alone do not identify coordinated manipulation. An old closed-market reference quote is not an executable hedge, and the token, direct share, and derivative identities remain separate.

### Chapter 2 — Why features and labels are needed: change the problem before the solver

#### 2.1 Two different jobs: what to ask and what to show the model

Labeling maps future paths or outcomes into target $Y$; feature engineering maps the observation history available at the time, $X$, into input $F=g(X)$. Labels decide which distinctions deserve an answer; features decide how existing distinctions become visible. Design both around the trading task: label simplicity and feature count are useful insofar as they preserve and expose decision-relevant distinctions.

For this book's trend strategies, the direction layer explicitly switches from precise prices to direction or first-passage outcomes under a specified exit policy. The gain comes from focusing the model on the details required by the selected action. Define the opportunity set, decision time, allowed actions, and exit policy first. Retain distinctions these require; account for payoff magnitudes, costs, and risk in their relevant layers. Section 2.6 derives the choice from action losses and participation thresholds.

**Principle:** labels define the task; features define the representation a limited model can access. The model fits within that constructed task. Labels should be decided early logically, but generating them requires historically usable data and a specified execution schedule; justified revisions remain possible.

#### 2.2 Why coarsening helps: discard target details and concentrate on decisions

Continue the joint-Gaussian construction from Chapter 1. Let $B=\mathbb 1[Z>0]$. Symmetry gives $H(B)=1$ bit. The conditional Gaussian distribution gives:

$$
p(x)=\Pr(B=1\mid X=x)
=\Phi\!\left(\frac{\rho x}{\sqrt{1-\rho^2}}\right),
$$

Here $\Phi$ integrates the standard-normal density from negative infinity to its argument. Construct binary entropy $h_2(p)=-p\log_2p-(1-p)\log_2(1-p)$ to obtain the exact expression:

$$
I(X;B)=1-\mathbb E[h_2(p(X))].
$$

Derive the scale of this information by expanding the expressions. For small $\rho$, expand $\Phi(a)=1/2+a/\sqrt{2\pi}+O(a^3)$ and $h_2(1/2+u)=1-2u^2/\ln2+O(u^4)$. Average over standard-normal $X$ using $\mathbb E[X^2]=1$:

$$
I(X;B)=\frac{\rho^2}{\pi\ln2}+O(\rho^4).
$$

Compared with complete-increment information $\rho^2/(2\ln2)$, direction retains approximately $2/\pi$ of the information; it creates none. Under Chapter 1's parameters, target entropy falls from about $7.69$ to $1$, direction information is about $0.001148$ bits, and the recoverable proportion rises from $0.0235\%$ to $0.1148\%$, approximately $4.9$ times higher. The improvement concerns the information ratio. Profit, prediction error, and generalization each require their own evaluation.

For $\rho>0$, the zero–one-loss optimal direction rule is $\operatorname{sign}X$. Write $Z=\rho X+\sqrt{1-\rho^2}U$ with independent standard-normal $X,U$. Angular symmetry of their planar density and the angle between the two sign half-planes yield:

$$
\Pr(\operatorname{sign}X=\operatorname{sign}Z)
=\frac12+\frac{\arcsin\rho}{\pi}.
$$

For $\rho=0.05$, the result is about $51.59\%$. This depends on joint Gaussianity and symmetric misclassification costs. Mutual information does not generally determine a unique hit rate, and hit rate does not determine net profit.

**Conclusion:** actively remove unnecessary price details in the selected direction task, concentrating estimation on directional bias with a smaller prediction burden. The Gaussian example explains information retention; Section 2.6 determines economic sufficiency. Keep the decision in view when reducing entropy: a constant label has zero entropy but cannot select actions.

#### 2.3 Why feature engineering works: present information is not necessarily usable information

Complete input $X$ can compute deterministic $F$, so $I(F;Y)\le I(X;Y)$. A limited predictor, however, may be unable to perform that transformation. Begin with a noiseless example.

Let $X$ be uniform on $\{-1,0,+1\}$ and $Y=\mathbb 1[X\ne0]$. A classifier limited to one threshold on raw $X$ cannot put both ends in one class and the middle in another; minimum error is $1/3$. With $F=X^2$, threshold $F>1/2$ has zero error. Raw input already contains all label information; the transformation exposes it to the model without adding Shannon information.

Introduce predictor family $\mathcal V$ only after this difficulty. Its members output valid probabilities and may ignore the input. Define optimal average log losses:

$$
H_{\mathcal V}(Y)=\inf_{q\in\mathcal V_{\varnothing}}\mathbb E[-\log_2q(Y)],\qquad
H_{\mathcal V}(Y\mid F)=\inf_{q\in\mathcal V_F}\mathbb E[-\log_2q(Y\mid F)],
$$

$\mathcal V_{\varnothing}$ contains no-input forecasts, while $\mathcal V_F$ contains forecasts allowed with representation $F$; ignoring input must remain compatible between them. Define $I_{\mathcal V}(F\to Y)=H_{\mathcal V}(Y)-H_{\mathcal V}(Y\mid F)$. This is usable information under computational and model restrictions; see [Xu et al.'s original paper](https://arxiv.org/abs/2002.10689). The example's hard-classification error and this log-loss quantity assess different aspects of prediction.

For finite, positive baseline loss, introduce the diagnostic ratio:

$$
\mathcal L_{\mathcal V}
=\frac{I_{\mathcal V}(F\to Y)}{H_{\mathcal V}(Y)}
=1-\frac{H_{\mathcal V}(Y\mid F)}{H_{\mathcal V}(Y)}.
$$

Ignoring input is feasible and log loss is nonnegative, so the population ratio lies in $[0,1]$. The denominator equals $H(Y)$ only if the no-input family can express the true marginal. This preserves the source's numerator–denominator intuition but is explicitly this tutorial's diagnostic convention. It depends on family, representation, labels, and loss; its interpretation and financial estimation therefore need those choices to remain explicit.

**Conclusion:** in the refined-factor route, use feature engineering first to perform the transformation a limited model cannot express or cannot learn reliably from available samples; then let a restrained model consume the relations. This sets representation improvement before default network expansion. Where relations remain buried in raw paths or text, a representation model may perform this work. The same representational work can thus be performed by handcrafted transformations or learned representations, as the bottleneck warrants.

#### 2.4 Two ways to raise the numerator

First, add observations $A$ genuinely complementary to $X$. The chain rule gives $I((X,A);Y)=I(X;Y)+I(A;Y\mid X)$. The gain is conditional dependence after existing input is known. Satellite, inventory, or text data raise the ceiling only if timely available and conditionally informative; their contribution depends on that conditional information and availability.

Second, reorganize existing observations. Returns and ratios address scale; multi-horizon summaries expose trend and reversal within the current snapshot; standardization expresses relative position; neutralization removes selected exposures; high-frequency summaries preserve relations that survive a change in frequency. Chapter 5 derives these operations and explains their use.

Retain both failure modes: transforms can destroy important information, and more columns can chiefly enlarge selection freedom and estimation variance. Use incremental comparisons with a fixed model and protocol to assess the transformed output's contribution.

#### 2.5 The division of labor among models, labels, and features

Under this convention, labels remove distinctions unused by decisions; features improve relations accessible to the limited family; fitting seeks the family's attainable performance. If optimal no-input loss equals Shannon entropy, the source's $I_{\mathcal V}/H$ expression is recovered. Improve labels and representations before the remaining model gap. Changing the family can itself improve usable information; the ordering follows the bottleneck, including cases where the model family itself needs improvement.

Operational questions:

1. Does the target preserve distinctions that alter actions, risks, and returns? If not, reconstruct labels.
2. Do timely available observations contain those distinctions? If not, seek observations or narrow the task.
3. Are the distinctions present but inaccessible to current representation and model? Compare explicit representation constructions and suitable structures first.
4. Do refined factors require only a simple relation? Start with a restrained baseline instead of assuming expensive representation learning is necessary.
5. Does improvement occur only in repeatedly optimized samples? Return to verification; an attractive fit cannot conceal selection bias.

**Conclusion:** the first levers for refined-factor strategies are labels, features, and verification, followed by model changes directed at a diagnosed bottleneck. Information limits and task reconstruction justify this priority. Upgrade models when the remaining bottleneck is clearly expression or optimization, and independently confirm whether the improvement holds.

#### 2.6 Why this book chooses direction and first-passage outcomes, not precise prices

**Decision.** Trend timing does not use tomorrow's or several-weeks-ahead precise price as its default target. Its direction layer forecasts direction or first-passage outcomes under a stated exit policy. Cross-sectional selection forecasts relative ranking. Organize optimization around the decisions these predictions support. Estimate magnitude, volatility, costs, and tails separately where they change participation or size; do not require the direction layer to answer everything.

**Step 1: derive which distinctions an action can discard.** Let complete future outcome be $Z$, label $Y=g(Z)$, and action loss $\ell(a,Z)$. If the fixed policy permits $\ell(a,Z)=\tilde\ell(a,g(Z))$, then:

$$
\mathbb E[\ell(a,Z)\mid X]
=\sum_y\tilde\ell(a,y)\Pr(Y=y\mid X).
$$

Group the conditional average by labels to obtain the equality. If evaluation no longer distinguishes outcomes inside a label class, the decision needs class probabilities, not exact within-class numbers. This establishes why within-class detail has no additional value for this decision. The effect on a particular model's estimation still needs evaluation. Spend modeling resources on distinctions that change actions.

**Step 2: apply the result to trading.** Fix direction and exit policy. In a two-outcome illustration, success yields $G>0$ before participation cost, failure loses $L>0$, participation costs $c\ge0$, and success probability is $p(X)$. Conditional expected P&L is:

$$
p(X)G-[1-p(X)]L-c,
$$

Abstaining yields zero, so participate exactly when $p(X)>(L+c)/(G+L)$. With symmetric $G=L=g$, long and short expectations are $g(2p-1)-c$ and $g(1-2p)-c$. Go long above $1/2+c/(2g)$, short below $1/2-c/(2g)$, and abstain in between. The choice is determined by probabilities and specified payoff scales.

Triple barriers predefine volatility-scaled gains, losses, and maximum holding time, aligning labels with policy. If a timeout class exists, retain its probability and conditional outcome using Section 3.3's three-class expectation. Keep timeout P&L in the expectation so that the class design preserves the policy's outcomes. Gaps and incomplete fills must return to actual accounting; they do not require reconstructing the entire future price path first.

**Step 3: explain why the reduction matters under thin signals.** In Section 2.2, the sign retains roughly $2/\pi$ of complete-increment information while target entropy drops from about $7.69$ bits to $1$. Many hard-to-recover details are removed while substantial direction-relevant information survives. This supports putting finite samples and capacity into decision-relevant bias rather than finer future-state reconstruction. The entropy ratio is not a profit proof; payoff thresholds and subsequent validation provide that judgment.

**Step 4: identify exactly what “positive versus negative” means.** The sign probability of a general fixed-horizon return $R$ does not by itself determine $\mathbb E[R\mid X]$. For instance, $R=+1$ with probability $0.6$ and $R=-2$ with probability $0.4$ has more up outcomes but negative expectation. Thus a hit rate above one-half still needs to be combined with payoff magnitudes and costs. Direction/first-passage labels carry directional and participation judgments; payoff structure, cost, and risk determine whether and how much to trade. Binary probabilities suffice under fixed-magnitude simplified contracts. When magnitudes vary, add conditional payoffs or appropriate return strata to supply the missing decision-relevant distinction.

**Final conclusion.** Task-aligned coarsening is selected because exact price levels provide no commensurate incremental value for the chosen action while enlarging the structure to estimate. Add a numerical target only when exact magnitudes or continuous sensitivities genuinely change actions and have a clear, verifiable use: justified allocation means, barrier/risk volatility, or derivative prices and Greeks. These uses give numerical targets explicit roles alongside the trend chapters' directional default.


#### Practical default — build a probability model and an economic action rule

1. Define the direction task and label $B$; choose binary log loss $-[B\log p+(1-B)\log(1-p)]$. The conditional $H+D$ decomposition shows why its ideal output is the true class probability, not an uncalibrated confidence score.
2. Construct the small feature panel in Chapter 5. Compare explicit transforms with raw observations using the same restrained model, so a representation gain is not confused with a simultaneous capacity increase.
3. In the symmetric teaching contract with gain/loss magnitude $g$ and cost $c$, go long when $p>1/2+c/(2g)$, short when $p<1/2-c/(2g)$, and abstain between them. With $g=1,c=0.1$, the thresholds are $0.55$ and $0.45$. The no-trade band follows from these payoffs and costs; changing them changes the thresholds.
4. If a fixed-horizon sign does not represent the exits, use first-passage labels. If gain and loss magnitudes differ, use $pG-(1-p)L-c$; if timeouts matter, retain their class and conditional payoff. Construct only the additional quantities the decision actually uses.
5. Freeze this whole route before confirmation. Report probability improvement over the no-input forecast, calibration by probability groups, and net policy outcomes. Prefer the coarse task as the selected action's smaller estimation problem, with profit assessed through the policy's cash outcomes.

**Replacement rule.** Add a numerical target when two outcomes merged by the label lead to materially different participation, sizing, or risk decisions. Specify where that numerical component enters the decision and test its incremental effect, concentrating on the missing payoff distinction.




#### Derivation checkpoints and the first solver

Reconstruct the Gaussian sign-hit probability through polar area element, radial normalization, and the two disagreement sectors. Quantify the one-split example in log loss: the shared no-input loss is $h_2(2/3)$; raw input loss is $2/3$; transformed loss is zero. Explicitly cancel price rescaling in log moves and moving-average deviations. For the first refined-factor baseline, define sigmoid probabilities from linear log odds and minimize average binary log loss plus $\lambda\|\beta\|^2/2$. Carry out the chain rule $\partial\ell/\partial s=p-B$ and distinguish coefficient regularization from learning-rate choice. Use held-out calibration, probability loss, and net policy accounting as three different checks.

#### Market-specific target choices

Preserve coarse trend direction, A-share relative ranks, crypto policy-success outcomes, and executable token/reference relations as predictions supporting different decisions. The token identity $T=aS(1+b)$ gives log token appreciation as reference appreciation plus change in relative gap; token direction is not synonymous with convergence. All event-detector constants and payout examples remain teaching choices, not measured profitable thresholds.

## Part II: Constructing targets, observations, and representations

### Chapter 3 — Labeling and decision decomposition: represent achievable outcomes

#### 3.1 Derive labels from the trading policy

**Motivation.** Two paths can share an endpoint: one rises and retraces, the other falls and recovers. Holding to maturity may yield the same result; exiting along the path need not. Define actions and exit policy before deciding whether labels describe endpoints or paths.

Given timely information $X_t$ and allowed action $a$, compare $\mathbb E[\Pi(a)\mid X_t]$ or an explicit risk-adjusted objective. Direction, rank, first-passage outcomes, and event completion are different proxies for these comparisons. Simplify outcomes when the merged distinctions leave the required decision unchanged, or when their approximation loss is acceptable.

**Conclusion.** Trend direction layers do not predict precise prices; timing with profit/stop exits uses first-passage labels; cross-sectional cases use ranking. Fixed-horizon targets apply to fixed-holding tasks without path-dependent exits. Specify how the labels and decisions handle costs, zero returns, failures, and unfinished events. These choices implement the selected task and make its results interpretable.

#### 3.2 Triple barriers: first-passage outcomes and endogenous holding periods

Let entry reference time be $t$ and path return $R_{t,s}$. Estimate volatility scale $\hat\sigma_t$ using known history. Set upper and lower barriers $u_t=a\hat\sigma_t$, $d_t=b\hat\sigma_t$, and maximum observation horizon $h$. Construct exit time:

$$
\tau_t=\min\left\{\inf\{s>t:R_{t,s}\ge u_t\},
\inf\{s>t:R_{t,s}\le-d_t\},t+h\right\}.
$$

The first hit of an empty set is infinity. First upper/lower hits receive $+1/-1$; the selected prototype retains timeout as class $0$, not an assumed zero payout. Trigger duration is generated jointly by path and policy. Distinguish information cutoff from executable entry $e(t)$, trigger $\tau(t)$, and actual exit fill $e^{\mathrm{exit}}(t)$. Store the trigger interval and full entry-to-fill interval. A class matures when its observations arrive; realized payout and meta-labels also wait for fill and cost records.

**Why scaling is needed.** If $R_{t,t+h}\approx\sigma_t\sqrt h\,Z$, a fixed return barrier $u$ has standardized distance $u/(\sigma_t\sqrt h)$, which changes with volatility. Scaling the barrier with the corresponding volatility makes relative distances comparable. Daily and $h$-day volatility have different scales; square-root-of-time scaling requires conditions such as additive increment variances and cannot be applied mechanically.

**Design conclusion.** The Shanghai copper case uses profit-taking, stops, and a maximum holding period, so its labels should represent that policy's first-passage outcomes, not an arbitrary endpoint's sign. Volatility scaling provides relative comparability at the chosen horizon. Consistency with the policy is the primary reason for this choice; any information gain needs its own evidence. Distinguish close and intrabar hits, same-bar OHLC double-hit ambiguity, and gap fills. Unknown terminal labels remain unknown, not automatically neutral.

#### 3.3 When class probabilities become an economic score

Suppose the three classes correspond to gain $G$, loss $L$, and average timeout outcome $A_0$, with probabilities $p_+,p_-,p_0$. Under this simplified policy:

$$
\mathbb E[\Pi\mid X]=p_+G-p_-L+p_0A_0-c.
$$

The probability difference $p_+-p_-$ is proportional to expected outcome only with symmetric $G=L$, negligible timeout contribution, and suitable cost/other conditions. Asymmetric barriers, state-dependent payoffs, or heterogeneous timeouts invalidate the shortcut.

**Conclusion.** Label codes, forecast probabilities, economic scores, and positions are four different objects. Turning classification output into holdings requires separate checks of calibration, payoff magnitudes, and portfolio constraints.

#### 3.4 Meta-labeling: separate direction priors from participation gates

**Motivation.** A primary model may propose useful directions without reliably identifying when participation is worthwhile. Freeze a direction policy $s(X)\in\{-1,+1\}$, label whether trading that direction under the specified exit policy achieves the success criterion, and let the meta-model answer only participation.

With success probability $p$, gain/loss $G,L>0$, and participation cost $c$, the threshold against abstention is $p>(L+c)/(G+L)$. It follows from the payoff structure; a value such as $0.55$ needs the corresponding gains, losses, and costs. With random payoff magnitudes, use corresponding conditional expectations.

**Complexity argument.** Once $s$ is fixed, restrict position candidates to $\{s(X)m(X):m\in\mathcal M\}$: only filter or scale an existing direction. This removes actions available to a fully free end-to-end model and may reduce estimation burden. Binary output alone does not prove the whole two-stage system has lower complexity. Any search or training of the direction rule still incurs selection cost.

Meta-training requires appropriate out-of-sample primary forecasts. High recall trades missed opportunities against excess candidates and can still leave some successful opportunities unproposed. A gate can filter proposed opportunities but cannot recover omitted ones. Measure precision, recall, and thresholds against an independently defined opportunity set.

**Design conclusion.** Where direction can be frozen, the first version separates direction and participation: the primary model proposes candidates; a small meta-model gates them; risk policy governs size. Preserve trusted directional structure and allocate P&L-sensitive modeling freedom to dimensions that can be verified separately. Probabilities determine participation thresholds; Chapter 10 supplies utility, risk, and capital constraints. A continuous sizing model requires separate incremental evidence.

#### 3.5 Ranking and event labels also have timestamps and universes

Cross-sectional labels $y_{t,i}=\operatorname{rank}_{j\in U_t}(r_{t+h,j})$ depend on historical universe $U_t$, horizon, and tie policy. Their meaning is comparison within the same date's universe. Ranking removes absolute level and scale but also payoff spacing, so economic evaluation still concerns the final portfolio.

Event samples are defined by events rather than uniform calendar time. Repeated announcements and updates about one event may belong to one decision process, not independent bets. **Chapter principle:** a label represents an observable policy outcome, preserves distinctions governing actions and risks, and states when the outcome actually becomes known.

#### Practical default — volatility-scaled policy labels, then a separate gate

For the copper worked example, freeze a ten-session maximum horizon, upper/lower return barriers $2\hat\sigma_t$, and a volatility estimate from the last twenty available daily returns. These chosen constants define the source-inspired teaching prototype; optimization would require a separate development comparison. Here $\hat\sigma_t$ is explicitly a one-day scale; the barrier is two such scales, not automatically two ten-day standard deviations. Entries occur only after the signal is available. Use actual contract prices and the selected executable-entry reference.

Scan observations after entry in chronological order; stop at the first observed barrier or the horizon. Save both class and outcome interval, along with actual exit payoff, costs, and any ambiguity flag. A close-observed prototype triggers on completed closes and executes at its declared later feasible opportunity. An intrabar resting-stop policy requires a different execution replay. Intrabar implementation requires finer observations or a declared conservative ambiguity policy. Unmatured or unusable outcomes are not filled with neutral labels.

First fit a three-class probability model and convert its output to an economic score with $p_+G-p_-L+p_0A_0-c$. The score then enters the position decision; the probability difference $p_+-p_-$ alone leaves payoffs and costs unspecified. For a participation-gate comparison, freeze a primary momentum direction or an out-of-sample primary classifier; train a small binary gate on that direction's policy success, using out-of-sample primary predictions. Start with capped risk-scaled size only after the payoff-derived gate passes. Compare the same primary policy with and without the gate: this isolates the contribution of filtering while keeping the direction strategy fixed.

**Why and when to change.** The stopping-time derivation aligns labels with the selected cash-producing exits; scaling makes the policy relative to known volatility. To change barriers or the horizon, define a justified policy comparison and record it during development. Preserve the default even while fixing its data and fill semantics.


#### Derivation checkpoints and executable fixtures

Derive the $w-1$ variance denominator from the centered-square identity under independent common-variance returns, while retaining its limited role as a local dispersion statistic outside that model. Expand simple-return compounding to explain when summing returns and square-root-of-time scaling are approximations. Derive softmax normalization, the shared-score redundancy, and class gradient $p_k-\mathbb1[Y=k]$. Give normalized midrank examples with and without ties. Derive the illustrative linear-long maintenance boundary by rearranging equity equals required maintenance and check the monotonic breach side.

The A-share fixture must not reward an intraday exit prohibited for newly acquired inventory. The leveraged-crypto fixture must retain forced-exit/path-solvency outcomes despite a favorable terminal price. The closed-reference token fixture must not assume an unavailable hedge fill. Keep no-fill opportunities distinct from filled losses, and record receipt and label-availability times.

### Chapter 4 — Data and information timing: correctness starts with the research object

#### 4.1 Record occurrence, release, and revision separately

**Motivation.** Inventory referring to a week need not have been published that week; current financial statements can include revisions unavailable then. Represent a record as $(e,k,v)$: event time, actual availability time, and content version. A query at $t$ requires $k\le t$, then selects the latest version available then under the object's semantics.

Filtering only $e\le t$ makes late publications appear before they were known. This counterexample shows why point-in-time queries need the availability clock alongside event chronology. Transmission, cleaning, and computation may delay availability beyond public release.

**Conclusion.** Let $\mathcal I_t$ contain information available at $t$. Features, model selection, and actions use the corresponding information only. Future labels may be generated retrospectively but cannot enter training or updates before maturity.

#### 4.2 Historical opportunity sets: future selection can manufacture an edge

Let $U_t$ be assets selectable then and $U_T$ today's survivors or index members. Replaying history with $U_T$ applies a filter depending on future survival and membership. Even perfect prices now describe the wrong population.

An asset tradable then but later delisted illustrates the problem: deleting its poor performance alters mean returns, rankings, and risk distributions. Reconstruct historical membership, listings/delistings, suspensions, shortability, and contract lifecycles as required by the task, so that missingness is interpreted within the actual opportunity set.

**Conclusion.** Completeness includes whether every object that should have appeared then is present. Missing, nontradable, unreleased, and zero-valued are distinct states.

#### 4.3 Bridge price series to assets that can actually be held

A stock split changes both per-share price and share count; align them and include dividends to reconstruct cash outcomes. Adjusted prices are a research representation. Do not silently insert future scale changes into historical absolute-price thresholds. Some ratios cancel a common scale; the actual formulas therefore determine which adjustments affect the historical decision.

Continuous futures splice distinct real contracts. Splice differences are not automatically holding returns. A genuine replay records old-contract closure, new-contract entry, costs, multipliers, and settlement. **Conclusion:** every research representation needs a mapping back to real assets and cash flows. A continuous chart cannot replace it.

#### 4.4 Cleaning and alignment can erase required distinctions

Trades are realized flows; the order book is cancelable stock. Aggregating both as the same “volume” can change the relation being studied. Multi-source alignment must distinguish not-yet-occurred, not-yet-received, and repeated revisions. Joining a late quote to an earlier trade illustrates asynchronous-join leakage.

Fit means, quantile cutoffs, and imputation parameters within the relevant training material. Fixed-time cross-sectional statistics use the contemporaneous universe and are not the same as fitting across dates. Window order, asset groups, and time breaks determine the economic meaning of the computation.

**Chapter conclusion.** A good data layer preserves object, time, and version semantics so that upper layers cannot easily misuse future information. Chapter 8 implements this discipline through queries, read-only snapshots, and caches across storage systems.

#### Practical default — an as-of data view and a cash-flow mapping

Use a minimal record containing `asset_id`, `event_time`, `available_time`, `version`, `value`, and a missingness/status code. Keep originals immutable. At each decision time, filter by `available_time <= decision_time`, select the then-available version, and join by persistent asset/contract identity. Materialize a historical investable-universe view separately; do not substitute today's members.

For stocks, retain actual prices, quantities, corporate-action events, and dividends alongside research-adjusted series. For futures, retain actual contracts and an explicit roll ledger. Features may use a continuous representation, but positions and cash outcomes use real holdings. Fit across-time transforms within each training fold; derive same-time cross-sectional transforms from that date's available universe.

**Construction check.** Create a tiny fixture containing a delayed release, a later revision, a delisting, and a contract roll. Query before and after each availability time and reconstruct the holdings' cash result. These fixtures show whether the observation/filter operations implement the intended semantics. After these operations have passed the checks, build the large feature matrix. At small scale, partitioned columnar files and a version manifest are sufficient; adopt a database when repeated query workload requires it.

**Decision.** Start with this auditable view and let its workload guide platform choices. The $(e,k,v)$ argument establishes which version each historical decision may see and thereby determines the actual query.

#### Derivation and implementation details retained in the lecture

The minimal record includes field and event identity as well as persistent asset identity: availability/version selection is performed **within the object–field–event key**, never globally. Label availability is a separate clock. The hand fixtures retain the exact cash checks: a split plus cash dividends reconstructs wealth 102; the two actual futures legs earn gross P&L 2 rather than the continuous-chart change 6. Same-date context is legal only for the historically eligible, actually available population. A-share sale/limit states, crypto mark/index/funding/finality clocks, and token wrapper/reference calendars apply the same information-timing rule in different market settings without adding prediction assumptions.

### Chapter 5 — Features and cross-frequency representations: encode economic relations in usable coordinates

#### 5.1 Multiple horizons encode temporal state

**Motivation.** A stateless predictor sees the current row, not omitted distinctions in the preceding path. With available prices $c_t$, construct momentum $m_w(t)=\log c_t-\log c_{t-w}$ and moving-average deviation $b_w(t)=c_t/(w^{-1}\sum_{j=0}^{w-1}c_{t-j})-1$.

A positive short-window return can occur inside either a long uptrend or a long decline. Retaining short and long windows lets the model distinguish those combinations, encoding some temporal state in the current vector. Endpoints remain insufficient for tasks needing peaks, arrival order, or execution processes.

**Design conclusion.** The timing case explicitly supplies multi-scale momentum and deviations because a stateless model must receive required history in its current row. Choose windows to express policy horizons and short/long state relations; their values form a reasoned starting grid. Test additional windows incrementally under a fixed protocol. Temporal operators run within the correct asset and order; shuffled minibatches cannot masquerade as historical windows.

#### 5.2 Turn economic priors into computable features

For actual near/far futures $F_t^{\mathrm n},F_t^{\mathrm f}$ with maturity gap $\Delta T>0$, define per-time curve slope $c_t=\log(F_t^{\mathrm n}/F_t^{\mathrm f})/\Delta T$. Monthly and annual scales cannot be mixed without conversion.

Let $b_t=\log F_t^{\mathrm n}-\log F_t^{\mathrm f}$. With fixed contract identities, basis momentum $b_t-b_{t-w}$ equals their log-return difference. The algebra establishes how basis momentum measures steepening or flattening. Contract changes within windows require identity handling.

Inventory, warehouse warrants, open interest, and trading volume observe different aspects. Term structure motivates hypotheses about scarcity, holding benefits, and risk compensation. Joint price/open-interest changes describe state but do not identify participant types or guarantee upward direction. Keep observations, economic explanations, and target outcomes separately supported.

**Design conclusion.** The futures case prioritizes term structure, basis changes, and available open-interest/inventory families instead of treating a price chart as the whole market state. Write the economic relation first, compute it, and confirm its incremental contribution. Curve slope is a relational measure, not already realized roll return. Correct accounting does not cancel the reason to observe futures-specific state.

#### 5.3 Standardization and neutralization do different jobs

Within a day's universe, $z_i=(x_i-\bar x)/s_x$ removes mean and scale while retaining relative position; $s_x=0$ makes that comparison undefined. Time-series standardization uses history available by the decision time. Standardization does not guarantee the same economic meaning across markets or regimes.

To remove selected industry or size exposures, let full-column-rank $B$ contain those exposures. Minimize $\|x-B\gamma\|^2$ and differentiate:

$$
\hat\gamma=(B^\top B)^{-1}B^\top x,\qquad
x_\perp=x-B\hat\gamma,\qquad B^\top x_\perp=0.
$$

The residual removes selected in-sample linear components. It can reduce unwanted exposures but also remove predictive content. If market-wide state is still needed, preserve removed means/scales as separate available context instead of erasing them inadvertently.

**Conclusion.** Judge units, relative comparison, exposure neutrality, and information retention separately. Distinguish “factor” as input feature, return explanation, or risk-model component. Choose cross-sectional z-scores when relative position is the relation the task needs.

#### 5.4 From ticks to daily decisions: specify retention before compression

**Motivation.** Low trading frequency does not make finer observations worthless, but feeding all high-frequency noise into a large model does not make them useful. A summary $A(H_t)$ of available event history $H_t$ should focus on the relations relevant to the specified future decision, leaving other event details out of that representation.

Compare cheap summaries such as totals, persistent imbalance, and replenishment speed. If histories with the same summary have testably different required outcomes, add order, state, or other missing distinctions. Use the evidence of such a task-specific difference to decide whether a more complex representation is warranted.

A learned summary may take the form $z_t=\sum_{u\in W_t}a_{t,u}v_{t,u}$ with nonnegative weights summing to one and determined only by available inputs; supervision comes from relevant low-frequency targets. Weights select events, but attention values do not prove economic causality. Future supervision still requires temporal separation of training and confirmation.

**Conclusion.** Cross-frequency representation and expert aggregation may both be called stacking, but solve different problems: retaining event structure versus allocating trust among existing judgments.

#### 5.5 Good reconstruction can preserve exactly the wrong component

Construct $X=(N,S)$: independent high-variance noise $N$ and low-variance target-relevant component $S$. One-dimensional linear squared-error reconstruction chooses the largest-variance direction. If $\mathrm{Var}(N)>\mathrm{Var}(S)$, optimal reconstruction may keep $N$ and discard $S$, since orthogonal-projection reconstruction error equals discarded variance.

Evaluate autoencoders, sparse representations, and smoothers on the target task alongside their reconstruction properties. In an orthogonal coordinate, minimizing $(z-a)^2/2+\lambda|z|$ yields soft threshold $z=\operatorname{sign}(a)(|a|-\lambda)_+$. An amplitude-only sparsity penalty may erase a small useful signal.

**Chapter conclusion.** Representation and regularization must match task-relevant relations and scales. Information is unevenly distributed across coordinates, states, and time. The appropriate amount of compression depends on which of these relations the task needs. Chapter 2 explains the possibility in terms of usable information; verification determines whether it was achieved.


#### Practical default — a small state panel before learned compression

For daily futures timing, construct three layers: (i) scale-relative bar state—one-day log return, range/close, available volatility, and volume anomaly; (ii) multiscale memory—momentum at 1, 5, 10, 20, and 60 sessions and moving-average deviations at 5, 10, 20, and 60; (iii) contract relations—near/far curve slope per declared time unit, twenty-session basis change, and open-interest change. Add inventory only when its release/version history is usable. The window set is a concrete teaching starting panel: short, policy-length, and longer-state comparisons supply memory to a stateless model.

Compute temporal operators within actual asset histories and availability rules. Remove exact duplicates and constant columns. For linear/probability baselines, standardize with training-only or past-only scales; tree models generally preserve their splits under monotone rescaling, so unit differences alone need not motivate z-scoring. For cross-sectional tasks, first express each factor's contemporaneous relative position and preserve separately needed market context. Select specified unsupported exposures for neutralization, retaining the other relations intended for prediction.

For tick-to-daily use, first summarize each available session/window with traded quantity, signed trade imbalance, spread/depth distribution, and persistent imbalance. Compare three nested panels—basic state, added contract relations, added high-frequency summaries—under a fixed learner and policy. When simple summaries miss a tested, task-relevant ordering or state distinction, train an attention summary or supervised bottleneck to represent it. Supervise it on the actual low-frequency task rather than reconstruction error alone.

**Why and when to change.** Multiscale equations distinguish states a single return merges; futures-specific relations add observations beyond a chart; the reconstruction counterexample selects supervised/use-specific compression. Retain a new family on the strength of confirmed incremental prediction or net policy value; reconstruction loss describes a separate property.



#### Inspectable algebra and practical scope

Expand $\|x-B\gamma\|^2=x^\top x-2\gamma^\top B^\top x+\gamma^\top B^\top B\gamma$. Full column rank gives $a^\top B^\top Ba=\|Ba\|^2>0$ for $a\ne0$, so the normal-equation stationary point is the unique minimum. Substitution proves $B^\top x_\perp=0$.

For one-dimensional reconstruction with $\|w\|=1$, expanding the square gives $\mathbb E\|X-ww^\top X\|^2=\mathbb E\|X\|^2-\mathbb E(w^\top X)^2$. Centering and independence remove the cross term; captured variance is $v_S+(v_N-v_S)w_N^2$, explicitly proving the loss of the low-variance signal. Soft-thresholding retains the one-sided derivatives and the zero-point condition. Fine-history summaries distinguish executed flow from cancellable depth and duration-weight states rather than message counts. Market-specific panels measure A-share limit/activity state, crypto liquidity/derivative stress, and token reference/contract state; each panel turns a market narrative into conditional hypotheses that can be tested.

## Part III: Learning, search, and evidence

### Chapter 6 — Models, capacity, parameters, and losses: restraint needs a reason

#### 6.1 Choose models from information location and problem structure

Refined factors may require only a few thresholds and interactions; trees or simple regression are reasonable baselines. Raw paths, books, or text still require representation extraction, where sequence, set, and language structures perform different work. More capacity expresses more relations but increases the burden of selecting them from finite data.

**Design conclusion.** For low-breadth tabular timing with state already encoded, prioritize shallow constrained boosted trees, not a large network by default. Fit thresholds and interactions among supplied factors instead of relearning the entire representation. Choose appropriate structures where paths, books, text, or cross-sectional relations still need extraction. Structure asks how economically a relation can be expressed; capacity asks how much selection freedom data support. Its scope is the stated task; matched comparisons establish its empirical value.

#### 6.2 Construct estimation variability before prescribing complexity control

Penalized least squares $\|y-X\beta\|^2+\lambda\|\beta\|^2$ yields $\hat\beta=(X^\top X+\lambda I)^{-1}X^\top y$ by differentiation. Along an eigendirection of $X^\top X$, the inverse denominator changes from $s_j$ to $s_j+\lambda$, suppressing perturbation amplification at small eigenvalues while also shrinking true coefficients.

Then illustrate selection cost with $K$ fixed prediction functions, $n$ IID observations, and losses in $[0,1]$. The log exponential moment's second derivative is variance under a tilted distribution, at most $1/4$. Integrate twice from zero to bound the exponential moment by $\exp(\lambda^2/8)$. Exponential Markov on the sample mean and a union bound over candidates give:

$$
\Pr\!\left(\max_f|R(f)-\hat R_n(f)|>\varepsilon\right)
\le2K e^{-2n\varepsilon^2}.
$$

With probability at least $1-\delta$, every candidate's deviation is at most $\sqrt{\ln(2K/\delta)/(2n)}$; the empirical winner's excess population risk is at most twice this bound. VC and Rademacher ideas extend the accounting of selection freedom to infinite families. Introduce them only as needed, not by equating parameter count with exact complexity.

**Conclusion.** Small edges tolerate little estimation error. Reducing unsupported freedom, increasing genuinely effective observations, or strengthening priors matters. The IID bound motivates the argument; it does not certify market sequences or convert low mutual information into an optimal parameter count. Functions must be fixed in advance. If each candidate is trained on the same data, training-run count alone is not $K$: control the actual function class or condition on frozen candidates and evaluate on independent data.

#### 6.3 What tree hyperparameters actually control

**Selected design.** Begin with shallow trees, sufficient node support, small new-tree contributions, leaf-value regularization, and temporal-validation early stopping. Restrict unsupported partitions and cumulative responses instead of minimizing training error with deep trees. Encode reliable output-specific monotonic priors as constraints. Choose shrinkage and iteration count together: one limits individual updates; the other accumulates fit. Numerical settings follow a frozen development protocol, not a mutual-information conversion.

Boosting constructs $F_m=F_{m-1}+\nu h_m$, where $h_m$ fits a local improvement direction for the current loss and $\nu$ shrinks each contribution. Depth controls partitions and interactions; minimum leaf support/weight limits tiny regions; row/column sampling changes available content per round; leaf penalties limit response magnitude; tree count and early stopping control the selection path's length.

**Derivation and conclusion.** If a proposed improvement is supported by few samples, finer partitions permit stronger accommodation. Shrinkage reduces one update but can be offset by more iterations. Small $\nu$ must therefore be coordinated with iteration count and validation stopping; it is not automatic overfitting prevention, and the source's $0.03$ is not universally optimal. Missing-value routing, monotone transforms, and feature importance remain algorithm-specific behaviors requiring semantic and bias checks—not proof that ineffective features disappear automatically.

A credible monotone prior can forbid declining scores as $x_j$ increases, reducing allowed responses. If effects reverse by regime, that constraint can be wrong. Specify output, range, and conditions; multiclass score constraints are not automatically monotonicity of an individual class probability. Verify semantics against [official XGBoost parameters](https://xgboost.readthedocs.io/en/stable/parameter.html): `min_child_weight`, for example, generally constrains child-node Hessian weight, not necessarily sample count. No implementation version or universal default is prescribed here.

#### 6.4 Cross-sectional structure: relative comparison and permutation equivariance

Let $X$ contain the day's asset rows and $P$ permute those rows. Scores should obey $f(PX)=Pf(X)$. A shared per-asset function already obeys this symmetry but need not use other assets. Explicit context, set summaries, and attention can supply those relations.

Set $Q=XW_Q,K=XW_K,V=XW_V$ and attention $\operatorname{softmax}(QK^\top/\sqrt d)V$, with rowwise softmax. Permutation transforms the score matrix to $P(QK^\top)P^\top$; rowwise normalization permutes correspondingly, yielding $P$ times the original output. Shared nonpositional residuals and rowwise transforms preserve equivariance; order-dependent masks may break it. See [Set Transformer](https://proceedings.mlr.press/v97/lee19d.html).

**Design conclusion.** Use shallow set attention without positional encoding as the cross-sectional relation-learning route: assets compare with one another while irrelevant row order is structurally excluded. This relation-learning role provides a definite reason for choosing attention. Trees with explicit cross-sectional context are required controls. A common confirmation protocol compares empirical performance, including the cross-sectional predictions of the tree controls. Evaluate relative labels, interaction use, and equivariance separately, while accounting for common shocks in samples and breadth.

#### 6.5 Shallow, narrow, dropout, RMSNorm, and low rank have different roles

**Capacity choice.** Start with a shallow, narrow cross-sectional relation model controlled by regularization and early stopping. Use correct symmetry to save learning effort, then restrict unsupported freedom; more cross-sectional rows do not automatically justify greater depth. Dropout, low rank, and normalization address different gaps. The decision to restrain capacity is explicit; it does not require pushing every hyperparameter to an extreme.

Depth/width limit compositional expression and computation; early stopping limits continued adaptation to samples; dropout randomly masks responses and changes training, not market information. Stronger penalties can remove Chapter 5's low-amplitude true signals.

RMSNorm normalizes by root-mean-square response scale, chiefly changing numerical scale and training conditions; it is not proof of reduced capacity. Rank-$r$ parameterization $W=AB^\top$ replaces $mn$ parameters with at most approximately $r(m+n)$ and restricts expression. Singular-value penalties and hard rank limits are related but different. Specify “low rank decay” as an explicit penalty or parameterization so that its restriction can be inspected.

**Conclusion.** For each parameter, explain the restriction, its task-specific reason, and its sacrifice. Development evidence selects depth, head count, dropout, and rank, with validation choices included in the selection account.

#### 6.6 Choose losses for the object being estimated

**Selected targets.** Use appropriate classification objectives for direction/first-passage probabilities and rank or suitable IC objectives for relative selection—not precise future-price regression by default. Evaluation and actions need those distinctions. Retain numerical regression for justified means, magnitudes, volatility, or pricing sensitivities. MSE estimates conditional means; do not claim every MSE model reconstructs every noise realization.

MSE's population optimum is the conditional mean; probability cross-entropy estimates conditional distributions; ranking losses support relative comparison. With centered cross-sectional vectors $s_c,r_c$, Pearson IC is $s_c^\top r_c/(\|s_c\|\|r_c\|)$, so its negative can be minimized. Define unavailability handling when either variance is zero.

IC is invariant to positive score rescaling and translation; high IC does not calibrate payoff magnitude. Spearman correlates ranks; exact sorting is usually not directly differentiable. Specify a smooth surrogate or pairwise loss. For $y_{ij}=\operatorname{sign}(r_i-r_j)$, minimizing $\log(1+\exp[-y_{ij}(s_i-s_j)])$ encourages correct order but does not fully price spacing, tails, or costs.

Optimizing portfolio net return or a risk–return ratio includes holding and cost policies, improving economic alignment while increasing strategy freedom and estimation difficulty. **Chapter conclusion:** target alignment, structural fit, and capacity restraint must all be answered. No attractive metric substitutes for the other two.

#### Practical default — select the model route, then a reproducible restrained prototype

First make the probability baseline explicit. With features $F$, use $p(F)=1/(1+\exp[-(\beta_0+\beta^\top F)])$, a linear score mapped into $(0,1)$, and minimize mean binary cross-entropy plus a coefficient penalty. It uses few degrees of freedom and establishes whether the supplied representation already exposes a simple relation. For natural-log loss, each unpenalized sample's gradient is $(p-B)(1,F)$ and curvature multiplier is $p(1-p)\le1/4$. If $M$ is the standardized design matrix including an intercept and the coefficient penalty is $\lambda\|\beta\|^2/2$, a smoothness bound is $L\le\|M\|_{\rm op}^2/(4N)+\lambda$. This gives an actual safeguarded gradient-step scale for this baseline. It does not transfer unchanged to tree shrinkage or Adam's adaptive update.

| Task | Starting model and target | Frozen teaching prototype | What warrants expansion |
|---|---|---|---|
| Engineered timing factors | Logistic baseline, then shallow boosted trees; binary or first-passage class probabilities | Depth 3, shrinkage $\nu=0.03$, at most 300 rounds; row/column sampling 0.8; leaf L2 penalty 2; child Hessian-weight threshold 20; development-period early stopping | Stable omitted thresholds/interactions that a larger model captures incrementally |
| A fixed direction's participation gate | A small binary classifier on out-of-sample primary directions and a restricted panel | Depth 2; shrinkage 0.03; at most 150 rounds; child Hessian-weight threshold 50; leaf L2 penalty 4 | Confirmed filtering gain, not a demand for freely optimized signed size |
| Whole-date cross-sectional relations | Shared linear/tree controls with explicit context, then nonpositional set attention; within-date pairwise ranking loss | Two pre-RMSNorm attention blocks, width 64, four heads, dropout 0.2, shared scalar output per asset; development early stopping | Confirmed missing relational expression, not raw row count alone |

The numerical choices are starting experiments, adapted from the source or selected for the tutorial; none is a universal optimum. Parameter meanings follow the relevant implementation: a child Hessian-weight threshold is not generally a sample-count threshold. See [XGBoost's parameter contract](https://xgboost.readthedocs.io/en/stable/parameter.html). Use fixed budgets and date-grouped development/confirmation splits. Mask unavailable assets; train with complete same-date groups or a documented set approximation. Test $f(PX)=Pf(X)$ by permuting rows in evaluation mode and undoing the output permutation.

**Construction and advantage.** A shallow depth-$d$ tree has at most $2^d$ leaves, explicitly limiting local regions and interactions. Shrinkage controls each region's incremental contribution; early stopping controls accumulated fitting. In cross-sections, set attention supplies shared comparisons without learning arbitrary input order. Neither correct structure nor a small learning rate removes the need to limit the selection path. RMSNorm is included for numerical response scale, not counted as a capacity restriction. As a separate compression experiment, a rank-16 factorization of a 64-by-64 projection uses 2048 rather than 4096 matrix parameters; compare its held-out task value before adopting it. This makes low rank a concrete restriction, not an unexplained “decay” label. The architecture and its empirical selection are different claims; [Set Transformer](https://proceedings.mlr.press/v97/lee19d.html) supports the set-based construction, not these financial settings.

**Loss decision.** Probability consumers use class log loss; relative-selection consumers start with within-date pairwise logistic ranking loss and assess rank IC plus net benchmark-relative results. Direct IC loss is a documented comparison when the portfolio uses broader correlation, not an undefined “optimize what earns money” instruction. First stabilize labels, predictions, and portfolio accounting. Then evaluate end-to-end Sharpe optimization as a broader strategy comparison.

#### Formula-level reader bridges

The bounded-loss proof explicitly defines $A(a)=\mathbb E e^{aX}$, differentiates $\log A$ twice into a tilted variance, and bounds that variance through the interval midpoint. Integrating $\psi''\le1/4$ gives $\psi(a)\le a^2/8$. Independence factors exponential averages; exponential Markov divides by $e^{an\varepsilon}$, optimizing at $a=4\varepsilon$; opposite tails and candidate union supply $2K$. These are not IID market guarantees.

For logistic scores, derive $p'(S)=p(1-p)$ and $\ell'(S)=p-B$, then $\ell''(S)=p(1-p)$. Summing the local Taylor expansions plus $\lambda w^2/2$ gives the leaf update. The coefficient baseline uses mean loss plus $\lambda\theta^\top R\theta/2$, giving gradient $M^\top(p-B)/N+\lambda R\theta$ and its Hessian. Quadratic-form comparison establishes $L_0=\|M\|_{\mathrm{op}}^2/(4N)+\lambda$ and the safeguarded step; tree shrinkage and Adam remain distinct.

Attention states every matrix dimension and the residual output projection; the permutation proof carries row/column normalization and masks. For IC, let $H=I-\mathbf1\mathbf1^\top/n$, $u=Hs$, $v=Hr$. The quotient-rule gradient is $v/(\|u\|\|v\|)-(u^\top v)u/(\|u\|^3\|v\|)$, followed by $H$; centered terms remain unchanged. Nonzero norms are essential. Model/loss defaults remain probability baselines and shallow trees for engineered timing, shared context-aware controls before shallow set attention, and pairwise ranking for relative selection.

### Chapter 7 — Optimization: how to search for factors, and what each step can ask

#### 7.1 Distinguish the optimized object from available feedback

Manual construction, genetic programming, and generative search seek high-scoring candidates. Let $f$ be a factor, $Q_D(f)$ its development-data score, and $\mathcal A$ the legal set: $\max_{f\in\mathcal A}Q_D(f)$. The score is a proxy for population use, not “true alpha.” Rank IC, Sharpe, and learnability are not interchangeable.

For parameterized candidates, write minimization of $J(\theta)$. Zeroth order observes values, first order also observes derivatives, and second order also observes curvature. **Order describes the feedback available to an algorithm.** Quality depends on how that feedback serves the task. Changing a symbolic operator is discrete; continuous backtests may contain nondifferentiable operations or be accessible only as black boxes.

Define legal candidates before search: economic meaning, units, and availability of leaves; operator input/output types, windows, and missing-data policies; complexity budget. Price plus price retains price units; price plus volume usually has no interpretable unit. Nondimensionalization can change legality, but must be an explicit construction.

#### 7.2 First-order optimization: local direction and the role of step size

Taylor expansion gives $J(\theta+\delta)\approx J(\theta)+\nabla J(\theta)^\top\delta$. For a fixed Euclidean displacement, Cauchy–Schwarz yields steepest descent along $-\nabla J$, motivating $\theta_{k+1}=\theta_k-\alpha\nabla J(\theta_k)$.

If $\|\nabla J(a)-\nabla J(b)\|\le L\|a-b\|$, integration along the segment gives:

$$
J(\theta+\delta)\le J(\theta)+\nabla J(\theta)^\top\delta+\frac L2\|\delta\|^2.
$$

Substitution of the gradient step gives:

$$
J(\theta-\alpha\nabla J(\theta))
\le J(\theta)-\alpha\left(1-\frac{L\alpha}{2}\right)\|\nabla J(\theta)\|^2.
$$

For $0<\alpha\le1/L$, obtain sufficient descent. Step-size control respects the local approximation; descent does not imply convexity or global optimality in a nonconvex problem.

With Hessian $H$, the quadratic approximation is $J(\theta)+g^\top\delta+\delta^\top H\delta/2$. Positive-definite $H$ gives Newton direction $\delta=-H^{-1}g$ by setting its gradient to zero. Curvature adjusts direction and scale, at the cost of forming/approximating $H$ and solving a system. Indefinite curvature or a limited local neighborhood requires corrections and step control; “second order” is not universal reliability.

If $J=N^{-1}\sum_jJ_j$, uniformly sampled averaged minibatch gradients are unbiased: $\mathbb E[\hat g]=\nabla J$. Unbiased does not mean low variance; temporal sampling and nonuniform weighting can change the estimator. Explain momentum as historical-gradient averaging and Adam as per-coordinate gradient-scale adjustment. They modify updates, not market information. Noise improving generalization is a conditional research claim, not a guaranteed benefit in finance.

**Principle:** first order obtains local direction through computation, with costs from gradient calculation, noise, and approximation validity. Backpropagation organizes the chain rule efficiently; it does not provide free direction for every parameter and task.

#### 7.3 Zeroth-order optimization: evaluate after trying

Central differences $(J(\theta+\epsilon e_i)-J(\theta-\epsilon e_i))/(2\epsilon)$ estimate coordinate derivatives; a complete $d$-dimensional estimate uses about $2d$ evaluations. Tiny perturbations amplify score noise; large ones increase bias. Expensive backtests make this cost consequential.

Genetic programming searches expression trees with defined observations as leaves and legal operators as nodes: population generation, scoring, selection, crossover, mutation, and complexity penalties. Simulated annealing proposes candidates and accepts worse ones with temperature-controlled probability. Neither requires continuous differentiability, but both require reliable scores and budgets. Method labels alone do not establish universal inferiority or efficiency.

Zeroth order can estimate direction. For $\epsilon\sim N(0,I)$, define $J_\sigma(\theta)=\mathbb E[J(\theta+\sigma\epsilon)]$. Under differentiation–integration interchange conditions, differentiating the shifted Gaussian density gives:

$$
\nabla J_\sigma(\theta)
=\frac1\sigma\mathbb E[J(\theta+\sigma\epsilon)\epsilon].
$$

Average $m$ perturbations to estimate this gradient. A constant baseline leaves expectation unchanged since $\mathbb E[\epsilon]=0$. Unbiasedness concerns the **smoothed objective**, not unconditionally the original function. Variance depends on dimension, smoothing, the function, and score noise; distinguish evaluation count from parallel throughput. [Salimans et al.](https://arxiv.org/abs/1703.03864) study evolution strategies; those experiments do not prove financial efficiency.

Expose dimension cost with noiseless $J(\theta)=a^\top\theta$. After subtracting $J(\theta)$, one-direction estimator is $g=(a^\top\epsilon)\epsilon$. Gaussian second/fourth moments yield $\mathbb E[g]=a$ and $\mathbb E[\|g-a\|^2]=(d+1)\|a\|^2$; averaging $m$ independent directions gives error $(d+1)\|a\|^2/m$. The lecture expands coordinates. This illustrates difficulty recovering a high-dimensional gradient from few random directions, not a universal black-box efficiency law.

**Principle:** without a direct gradient, spend evaluations to estimate direction or search discrete candidates, but account for cost and variance. Larger search budgets also enlarge opportunities to fit historical noise; Chapter 8 quantifies that cost.

#### 7.4 Reinforcement-learning generators change proposal preferences, not backtest differentiability

Treat an expression as a grammar-generated token sequence with probability $\pi_\theta(f)$. To improve expected reward $R(f)$, use $\nabla\pi=\pi\nabla\log\pi$ and justified interchange of differentiation and summation:

$$
\nabla_\theta\mathbb E_{f\sim\pi_\theta}[R(f)]
=\mathbb E[R(f)\nabla_\theta\log\pi_\theta(f)].
$$

Generation probabilities are differentiable, so gradients need not pass through swapping close for open, sorting, or matching. High-scoring samples increase corresponding generation tendencies; poor ones reduce them. Experience enters shared generator parameters and shapes later proposals. This is the source's valuable AlphaGPT-style construction; independent confirmation then evaluates its out-of-sample financial value.

Expression probability factors into token conditional probabilities, so its log gradient sums token-level log gradients. One terminal backtest score weights the whole operation sequence, explaining sparse feedback and credit-assignment difficulty. A baseline independent of the current candidate preserves expectation while changing variance; clipping and other stabilization need their own conditions. Genetic populations also inherit information, so a comparison with RL measures how effectively each route uses its inherited experience.

**Principle:** the generator optimizes a proposal distribution. Black-box rewards remain costly, noisy, and selection-biased. Pretraining choices, model size, and the particular RL updater are empirical alternatives within this construction.

#### 7.5 The reward is what search actually pursues

Write $\hat Q_D(f)=Q(f)+\epsilon_D(f)$, with $Q$ the claimed population-use performance and $\epsilon_D$ estimation error interacting with selection. The optimizer sees only the left side. When noise exceeds genuine differences, maximization can predominantly select large error. A stronger optimizer faithfully optimizes a wrong proxy; it cannot identify the “real” term by itself.

Declare benchmark, temporal validation, costs, complexity, and incremental contribution to the existing library. Rolling development scores and penalties can help, but no weighted reward automatically guarantees honesty; penalty coefficients and reward definitions are themselves tuned. Feeding DSR or purged validation back into search does not keep those repeatedly queried data as final out-of-sample evidence.

**Chapter conclusion:** establish legal candidates and honest evaluation before selecting search tools. Compare fixed targets, constraints, evaluation counts, resources, and uncontaminated confirmation outcomes. Efficiency comparisons assess the complete route, including evaluation and confirmation costs alongside high-IC production. This is the bridge to the factor pipeline.

#### 7.6 Learning rate, batch size, and noise: derive a transparent example

**Motivation.** Full-gradient descent bounds omit minibatch noise. Step size controls both convergence speed and residual fluctuation. Use scalar $J(w)=a(w-w_*)^2/2$, $a>0$, error $e_k=w_k-w_*$, and gradient estimate $ae_k+\xi_k$. Conditional on the past, noise has mean zero and variance $v/B$, where $B$ is the size of an independent average.

Constant step $\alpha$ yields:

$$
e_{k+1}=(1-\alpha a)e_k-\alpha\xi_k,\qquad
\mathbb E e_{k+1}^2=(1-\alpha a)^2\mathbb E e_k^2+\alpha^2v/B.
$$

Without noise, $0<\alpha<2/a$ gives geometric contraction. With noise, stationary mean-square error is:

$$
\lim_k\mathbb E e_k^2=
\frac{\alpha v}{Ba(2-\alpha a)}.
$$

A smaller step or larger independent batch lowers the noise floor; a smaller step also slows initial descent. With $\alpha_k=1/(ak)$, error can be expressed as an average of past noise, giving $1/k$ mean-square decay under independent equal-variance conditions. This example does not establish nonconvex Adam rates. Multidimensional quadratic eigendirections have different curvatures: the steepest restricts stable steps, the flattest slows convergence, motivating preconditioning and second-order approximations.

**Batch boundary.** Correlated gradients have averaged variance $B^{-2}\sum_{i,j}\mathrm{Cov}(g_i,g_j)$, not automatically $v/B$. Same-day stocks, overlapping labels, and neighboring book events do not become independent inside a large batch. Account for batch computation and fewer update opportunities. Unbiased sampling of a fixed training set establishes unbiasedness relative to its empirical objective, not equality with the future population objective.

**Conclusion.** Choose steps using curvature/local scale, noise, actual batch dependence, training budget, and validation. Decay and warm starts are particular designs, not universal financial requirements. Check numerical descent, statistical generalization, and market advantage separately. See [Bottou, Curtis, and Nocedal](https://arxiv.org/abs/1606.04838).

#### 7.7 Thin information affects gradients but does not prescribe a learning rate

Let $Y=\beta X+\epsilon$, with independent zero-mean $X,\epsilon$ of finite variance, model $wX$, and loss $(wX-Y)^2$. Population gradient is $2(w-\beta)\mathbb EX^2$. At $w=\beta$, single-sample gradient variance is $4\mathrm{Var}(\epsilon)\mathbb EX^2$. Large noise relative to signal makes a small $\beta$ hard to distinguish from finite samples even when the population objective is a simple convex quadratic.

For Gaussian $X,\epsilon$, $I(X;Y)=\tfrac12\log[1+\beta^2\mathrm{Var}(X)/\mathrm{Var}(\epsilon)]$ in natural-log units. It describes signal-to-noise in that distribution, not every parameterization's optimization geometry. Multiply loss by $c>0$: information is unchanged, but gradient and curvature scale by $c$, so stable step sizes must adjust. Input/parameter rescaling can also change geometry without changing information.

**Conclusion.** Thin information calls for stricter estimation and confirmation, limited unsupported freedom, and appropriate noise control—not a fixed tiny learning rate deduced from $I$. Smaller steps add no market information; more precisely minimizing empirical loss may fit its noise more faithfully. Information, statistics, and optimization are related but noninterchangeable layers.

#### 7.8 Momentum and adaptive steps modify updates, not the available signal

Exponential momentum $m_k=\beta m_{k-1}+(1-\beta)g_k$ geometrically weights old gradients. Under a fixed signal and independent noise, stationary noise variance changes from $v$ to $v(1-\beta)/(1+\beta)$, with history scale about $1/(1-\beta)$. This explains both smoothing and lag after genuine directional changes. Nonstationarity requires more than celebrating variance reduction. This EMA example is not a convergence proof for every momentum optimizer.

Adam also tracks $v_k=\beta_2v_{k-1}+(1-\beta_2)g_k^{\odot2}$ and normalizes bias-corrected $\hat m_k$ componentwise by $\sqrt{\hat v_k}+\epsilon$: $w_{k+1}=w_k-\alpha\hat m_k/(\sqrt{\hat v_k}+\epsilon)$. The denominator is historical gradient scale, not market volatility. Relative updates on low-gradient coordinates can increase, jointly governed by $\alpha$, smoothing horizons, and numerical stabilization. AdamW additionally applies decoupled factor $(1-\alpha\lambda)$; this is not unconditionally equivalent to putting L2 inside an adaptive-gradient objective.

**Design conclusion.** Use the source's momentum/adaptive-ruler intuition to motivate task-specific comparisons. Record optimizer, loss normalization, batches, step trajectory, decay, and stopping; compare complete training routes under the same validation protocol, not optimizer names.


#### Practical default — choose the feedback route and make step selection operational

**Factor search.** Begin with economically specified candidates and a small typed grammar of available leaves, arithmetic/ratio operators, and within-asset lag/window operators. Freeze depth/node and evaluation budgets. Use bounded genetic programming as the first automated symbolic-search baseline because it operates directly on legal discrete expressions without a differentiable backtest. Validate scores, reject illegal trees, simplify duplicates, cache common subexpressions, then mutate/cross/score/select only on development material. Promote a shortlist, not the entire winning population, to separate confirmation.

Use a policy-gradient generator as the next learned-proposal comparison when repeated motifs could improve proposals and the evaluation budget supports it. Enforce grammar during generation; sample expressions; compute the frozen development reward; subtract a candidate-independent baseline; update generation probabilities; retain the full trial log. Compare discovery per evaluation and per wall-clock budget, including training overhead. Differentiable proposal preferences are the construction's advantage; backtests have not become differentiable and superiority has not been assumed. Directly differentiable continuous tasks instead use their actual gradients, rather than paying symbolic black-box costs.

**Full-gradient teaching problems.** Standardize input units, use $\alpha=1/L$ when a credible global curvature bound is known, and otherwise start a backtracking search: reduce a trial step by a factor of two until $J(\theta-\alpha g)\le J(\theta)-\alpha\|g\|^2/2$. The descent inequality proves acceptance for sufficiently small steps when its smoothness conditions hold. This turns respect for local curvature into an operational method for selecting the step. Do not apply the deterministic test unchanged to noisy minibatch scores.

**Neural training prototype.** Start with normalized inputs and mean loss, an AdamW baseline, and a development-only pilot comparing initial rates $10^{-4},3\times10^{-4},10^{-3}$ under the same architecture, batch construction, stopping rule, and update budget. These are a bounded starter grid, not numbers deduced from information theory. Reject numerical instability; select on forward validation, not the lowest training loss. Keep complete dates/independent event groups as batch units where their relationships are needed. Average additional groups when gradient variation is the measured bottleneck; correlation prevents pretending that every asset row divides noise independently. Check versions before executable implementation.

**Tie the parameters to a deduction.** The scalar recurrence gives noise floor $\alpha v/[Ba(2-\alpha a)]$ and contraction $|1-\alpha a|$. It explains the starting practice: use the largest reliably stable, validated update scale; reduce it or increase independent averaging when noise dominates late progress; use decay or validation stopping rather than endless empirical optimization. Diagnose instability, a training–validation gap, and flat validation separately. Instability calls for scale/step repair; a widening gap calls for capacity/regularization or stopping; flat confirmed performance calls for a target/representation review—not automatically a smaller step.

**Selected conclusion.** Prefer actual derivatives when the task supplies them, bounded typed search for discrete or black-box tasks, and learned proposals when a measured comparison supports the upgrade. Learning-rate selection has an explicit construction and a finite budget; thin market information governs statistical restraint, not a magical universal rate. The optimization distinctions are consistent with [Bottou, Curtis, and Nocedal](https://arxiv.org/abs/1606.04838).

#### Expand the numerical mechanisms rather than infer rates from bits

Expand the noisy quadratic update squared, remove the cross term by conditional mean-zero feedback, and retain the finite recurrence $V_k=\rho^kV_0+c(1-\rho^k)/(1-\rho)$ with $\rho=(1-\alpha a)^2$, $c=\alpha^2v/B$. Only $\rho<1$ permits the limiting noise floor. Loss rescaling changes gradient/curvature and hence step units without changing mutual information.

For Gaussian smoothing, state the density $p_\theta(z)$ and differentiate it: $\nabla_\theta p_\theta=p_\theta(z)(z-\theta)/\sigma^2$. Under admitted differentiation/integrability, integrate $J(z)$ against this derivative and change variables to obtain the score-function gradient of the **smoothed** objective. Show fourth moments by Gaussian integration by parts and subtract the squared mean to derive the random-direction dimension cost. Learned symbolic generation differentiates proposal probabilities, not the backtest itself; finite legal support and fixed evaluator are retained. The typed, bounded GP control and measured optimizer diagnostics remain the first practical routes.

### Chapter 8 — The factor pipeline: connect discovery, verification, admission, and retirement

#### 8.1 Produce bounded evidence, not just expressions

Following Chapter 7, the loop is candidate generation → development scoring → independent verification and gates → documented admission → portfolio consumption → performance/implementation monitoring → retention, downweighting, retirement, or renewed research. The source groups some operations into five stages; this outline separates scoring from confirmation so a high development score does not automatically authorize use.

The pipeline connects two distinct flows: generation proposes hypotheses, and evidence determines how much trust they deserve. A repeatedly optimized historical score cannot certify both. Automation is useful when it faithfully repeats the operations that supply and assess evidence.

**Principle:** every transition from candidate to usable factor carries evaluation grounds and applicability conditions. Infrastructure grows with measured scale; a few single-machine files can preserve separation of responsibilities, while a cluster does not create discipline automatically.

#### 8.2 More search produces more attractive noise

Begin with significance for one fair-coin experiment, then contrast a prespecified experiment with selecting the best of many. For $M$ independent tests with false-positive probability $\alpha$, at least one false positive has probability $1-(1-\alpha)^M$. Without independence, the union bound still gives $\Pr(\text{at least one false positive})\le M\alpha$. Bonferroni therefore uses per-test $\alpha/M$, not the single-test threshold.

Quantify the source's “luck floor.” Let null standardized scores $Z_j$ be standard normal, initially independent. For $u>0$, exponential Markov and $\mathbb E[e^{\lambda Z_j}]=e^{\lambda^2/2}$ with $\lambda=u$ give $\Pr(Z_j>u)\le e^{-u^2/2}$. Obtain the exponential moment by completing the square in the density integral. Union bounding gives:

$$
\Pr\!\left(\max_{j\le M}Z_j>u\right)\le M e^{-u^2/2}.
$$

A sufficient threshold at level $\alpha$ is $u\ge\sqrt{2\ln(M/\alpha)}$. For independent normals, the maximum's typical large-$M$ scale is $\sqrt{2\ln M}$, as seen from $\Pr(\max Z_j\le u)=\Phi(u)^M$ and normal-tail decay. Develop lower-order terms in the lecture; the scale is not the exact expectation. The union bound needs no independence, but dependence changes the precise extreme-value distribution.

If an ideal IID correlation statistic also satisfies $\sqrt n\,\widehat{\mathrm{IC}}\sim N(0,1)$ approximately, the best null IC scale becomes:

$$
\max_j\widehat{\mathrm{IC}}_j\ \text{ noise scale}
\ \approx\sqrt{\frac{2\ln M}{n}}.
$$

For teaching values $M=200000,n=2500$, this is about $0.099$. It is not a universal admission threshold. Rank IC, time dependence, overlapping labels, candidate correlation, and adaptive generation require the appropriate null distribution. Adaptively selected statistics cannot simply retain the prespecified-candidate normal null assumption.

**Principle:** a high score's rarity cannot be interpreted without the number and manner of selections that produced it. Search finds candidates and representations; it does not create market information from the same input. Record failures, and do not reset trial history when changing model generations.

#### 8.3 Logic before search: how priors reduce cost

Turn economic explanations into candidate restrictions: which behavior or risk exposure is observed, when it may work, where it may reverse, and what would refute it. Carry, term structure, and inventory motivate candidates; explanations are not verified returns, and carry's sign is not a universal invariant.

In the ideal score example, restricting $M$ candidates to $m<M$ lowers the extreme scale from $\sqrt{2\ln M}$ to $\sqrt{2\ln m}$. Reducing unsupported freedom can reduce selection burden; an economic story does not exempt testing. Reliable monotonicity, symmetry, and constraints trade fewer selectable relations for robustness, while wrong priors can exclude genuine relations.

An automatically discovered, initially unexplained candidate is not automatically false. It requires the same confirmation discipline, possibly stronger cross-period/environment checks. Economic logic, statistical evidence, and execution value constrain one another; none substitutes for the others.

**Principle:** remove unsupported hypotheses before search rather than narrate the winning score afterward. Explicitly constrain, remove, or neutralize dimensions without an edge instead of allowing optimization to fit their noise.

#### 8.4 Isolate development and confirmation across the complete chain

Development generates candidates, selects windows, changes rewards, and tunes parameters. Internal validation used for selection remains development. Freeze candidates and evaluation rules before testing on confirmation periods untouched by that selection. Revising after failure incorporates the former confirmation result into new development history; do not keep testing until something passes.

Chronological splitting alone may be insufficient. Labels span $[t,\tau_t]$; purge training samples whose labels overlap test intervals according to the protocol. Embargo intervals follow actual dependencies and input construction. Fitted standardization, neutralization, reduction, primary models, and meta-models respect their training partitions. Further portfolio selection creates a new hypothesis space.

Use rolling or expanding windows in deployment order as the main replay. Combinatorial purged validation can examine stability across temporal partitions, but training on data after a test date cannot be presented as performance achievable at that date. Paths sharing data are not independent tests.

Expand variance to obtain:

$$
\mathrm{Var}\!\left(\frac1n\sum_tZ_t\right)
=\frac1{n^2}\sum_t\sum_s\mathrm{Cov}(Z_t,Z_s).
$$

Dependence explains how overlapping labels, common same-day shocks, and persistent holdings alter uncertainty. Choose time-block resampling, grouped comparisons, or another appropriate method with explicit conditions; no arbitrary effective-sample-number adjustment solves everything.

Construct Sharpe from sample mean and volatility, then discuss estimation and extreme selection. The deflated Sharpe ratio (DSR) combines a selection-adjusted benchmark with nonnormal returns to assess support for an observed Sharpe. It is a probability-style statistical assessment—not raw Sharpe minus a number or profitability certification. See [Bailey and López de Prado](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf). Preserve raw trial history, candidate correlation, and effective-independent-trial assumptions separately; generated-candidate count is not universally the input to every formula.

**Derive the estimation motive.** For single-period excess returns, $S=\mu/\sigma$; standardized skewness/kurtosis are $\gamma_3,\gamma_4$, with kurtosis here not excess kurtosis. Under IID observations, finite fourth moment, and valid asymptotics, first-order ratio expansion gives $\delta S\approx\delta\mu/\sigma-\mu\,\delta(\sigma^2)/(2\sigma^3)$. Expanding variances and covariance of sample mean and variance yields:

$$
\mathrm{se}(\hat S)^2\approx
\frac{1-\gamma_3S+(\gamma_4-1)S^2/4}{n}.
$$

Use estimated moments and the method's finite-sample corrections in practice. Equal mean and volatility can coexist with different tail shapes and different estimation reliability. A zero benchmark addresses one estimation problem; after search, replace it by expected best null-candidate Sharpe $S_0$, determined by trial count and score dispersion, connecting to Section 8.2.

Under the stated normal approximation, $\Phi((\hat S-S_0)/\widehat{\mathrm{se}})$ expresses support above the adjusted benchmark. Explain how $S_0$ and independent-trial approximations are obtained. This is not an unconditional Bayesian probability of profitability. Do not mix daily formulas with annualized numbers. Dependence, absent fourth moments, or adaptive selection breaking assumptions require appropriate inference, not mechanical substitution.

**Principle:** gates prevent selection from masquerading as discovery, not merely one model's overfitting. Repeated choices in labels, features, rewards, thresholds, and combinations enter the record. Individually admitted factors do not certify arbitrary later combinations.

#### 8.5 Admission stores a factor dossier, not an expression string

A consumable dossier records at least:

- **Definition and origin:** expression, economic explanation or exploratory status, operator versions, windows, units, missingness handling, generator, and parent candidates.
- **Time and objects:** data versions, historical opportunity set, release rules, feature timestamps, label intervals, and exit policy.
- **Selection history:** variants tried in this and related earlier development, failures, reward changes, duplication and dependence. Preserve raw records rather than invent one universal exact $M$.
- **Supporting evidence:** development/confirmation periods, purging rules, IC and net results across windows, statistical assumptions, and simple-baseline comparisons.
- **Use conditions:** signal orientation, risk exposure, turnover, costs/capacity estimates, data dependencies, permitted roles, and failure conditions.

Admission jointly checks computability, temporal validity, evidence, implementation cost, and incremental contribution. Correlation gates identify redundancy; zero Pearson correlation is not independence, and high correlation does not automatically eliminate complementarity. Compare $Q(\text{existing library}+f)-Q(\text{existing library})$ under a fixed protocol, while recording repeated comparisons as development.

**Principle:** traceability is part of evidence. The library stores usable definitions and their evidence, extending the search beyond a collection of winning expressions. Retrieval returns factors with use conditions; Chapters 9–11 determine aggregation, holdings, and execution. Library queries must not silently optimize the whole portfolio.

#### 8.6 Infrastructure's real job: honest evaluation within a budget

The source's infrastructure insight is not a database shopping list. Large-scale discovery jointly depends on correct data, affordable backtesting, and computation supply. A fast wrong scorer mass-produces wrong evidence; a correct but prohibitively slow scorer makes search infeasible.

If complete evaluation costs time $c$ and available work budget is $B$, serial evaluations number at most about $B/c$. Reading $b$ bytes per candidate over $M$ evaluations costs about $Mb$ bytes. Shared caches and subexpression reuse reduce repeated work, but reused results must bind data, operators, and time rules. More throughput enlarges both search capability and selection burden.

Discuss requirements by workload:

1. **Storage and recovery:** immutable originals, versioned derived data, read-only research inputs separated from result writes. Redundancy aids availability; backups address deletion/disaster; restore tests establish usable copies. NAS and RAID are not universal prerequisites.
2. **Query and correctness:** column pruning and time/asset partitioning reduce appropriate reads. Preserve historical membership, corporate actions, actual contracts, and PIT queries. Brands do not create discipline; CSV and ordinary databases are not unconditionally forbidden.
3. **Replay/scoring throughput:** vectorization, batching, shared features, and expression caches address repetition first. Before parallelism, check independence, consistent snapshots, and failure handling that cannot masquerade as high scores.
4. **Training resources:** distinguish parameters, gradients, optimizer states, and activations. DDP replicates model states; sharding distributes selected components over $G$ workers with communication and transient peaks. Total memory does not necessarily fall to $1/G$. Introduce multi-GPU/multinode structures only when measured capacity or throughput requires them; version-specific choices belong to later engineering topics.

**Principle:** infrastructure supports reliable evaluations at an affordable scale. Keep the same discipline at small scale; add structure to measured bottlenecks at large scale. Let the research task and measured bottlenecks guide platform expansion.

#### 8.7 Monitoring and retirement: factors are conditional, potentially expiring knowledge

Monitor predictions, inputs, and execution while factors are consumed. When rolling IC or net performance leaves the development-supported range, distinguish data faults, relation drift, cost changes, and holding-policy changes before retaining, weakening, or retiring. Competition can erode alpha, but not every decline has that cause or the same lifetime.

Restarting search or moving thresholds cannot erase trial history. Repeated monitoring also creates false alarms and selection issues. Permit a pipeline to pause for absent progress, data anomalies, or unaffordable next steps; pausing when further work lacks value is also part of research discipline.

**Chapter conclusion:** a real factor pipeline distinguishes and connects candidates, evidence, dossiers, consumption, and failure handling. Optimization proposes; verification limits trust; infrastructure repeats these operations faithfully and affordably. None replaces the others.

#### Practical default — one small honest factory before a large automatic one

Build the first version as immutable data snapshots → typed candidate generator → deterministic development scorer → frozen shortlist → independent confirmation gate → versioned factor dossiers → separately evaluated aggregation → monitoring. Store invalid candidates and failures as trials, not missing successes. Keep scoring read-only and bind caches to data/operator/target versions. Start with partitioned columnar files, one process, and subexpression caching; measure reads and scoring time before introducing more machines.

Choose chronological rolling development folds with label-overlap purging and all transforms fitted within folds. Reserve a later period for one frozen confirmation batch. The scorer uses the same target and fixed policy as consumption, records predictive metrics and cost-adjusted outcomes, and penalizes unsupported expression complexity under a frozen rule. Internal folds can guide proposals; their scores are not final confirmation.

The admission decision is concrete: executable and temporally valid; orientation and behavior consistent across the declared folds; independent incremental support beyond the stated simple baseline; viable turnover/cost/risk exposure; and useful increment to the existing consuming system. Prespecify materiality and risk tolerances in the development specification. Report selection-adjusted inference with its trial/dependence assumptions; do not replace this joint decision with one arbitrary DSR or IC threshold. If there is no confirmed increment, do not admit a factor merely to keep the factory moving.

**Derivation to operation.** The $\sqrt{2\ln M/n}$ example makes trial history necessary. The covariance sum makes time-grouped validation necessary. The incremental comparison makes an existing-library baseline necessary. Each becomes a field or operation in the factory, not a closing warning.

Track live/offline consumption with the same label-maturity rules and costs. Data faults suspend the affected input; persistent loss of confirmed usefulness triggers a recorded retirement/redevelopment review. A larger generator or faster cluster is an upgrade to evaluation supply only after this route is correct, affordable, and bottleneck-measured.

#### Complete the Sharpe uncertainty expansion

With $A=1/\sigma$ and $B=-\mu/(2\sigma^3)$, explicitly compute $A^2\operatorname{Var}(\delta\mu)+B^2\operatorname{Var}(\delta v)+2AB\operatorname{Cov}(\delta\mu,\delta v)$. The three terms are $1/n$, $S^2(\gamma_4-1)/(4n)$, and $-S\gamma_3/n$. This identifies why skewness enters with a minus sign and why numerator/denominator uncertainties cannot be assessed separately. The result remains leading-order IID finite-fourth-moment inference, not an exact small-sample or dependent-return guarantee. The development/confirmation boundary includes target, orientation, calibration, aggregation, and execution choices; joint admission is not replaced by a single IC/DSR threshold.

### Chapter 9 — Online aggregation: learning rates set reaction scales, and guarantees belong to losses

#### 9.1 Allocate trust beyond yesterday's leading factor

**Motivation.** Relative factor quality can change. A one-time fit and all-in historical-winner selection can both be unstable. Compare equal weight, periodic retraining, and roundwise updating before defining experts as factors/rules with evaluable judgments. Regret is extra cumulative loss against a specified comparator, not another word for return or drawdown.

Follow-the-leader (FTL) selects minimum cumulative loss. Alternating losses of two experts can make aggressive switching repeatedly select the newly worse one. Soft allocation moderates the concentration created by all-in switching. For confirmed factors, begin with simple online exponential trust updates and equal-weight controls. Keep high-capacity interaction search as a separate comparison. Inputs are already judgments; the main work is robust trust allocation and adaptation. Add aggregation capacity when new interactions have confirmable value; batch retraining remains another comparison route.

#### 9.2 Derive exponential weights from regularized selection

For $K\ge2$ experts with equal initial trust and cumulative losses $L_{t-1,i}$, minimize $\sum_iw_iL_{t-1,i}+\eta^{-1}\sum_iw_i\ln w_i$ on the probability simplex. The entropy term discourages premature extreme concentration. Differentiate with the sum-to-one multiplier:

$$
w_{t,i}=\frac{e^{-\eta L_{t-1,i}}}{\sum_je^{-\eta L_{t-1,j}}},\qquad
v_{t+1,i}=v_{t,i}e^{-\eta\ell_{t,i}}.
$$

**Conclusion.** Larger $\eta$ follows accumulated differences more sharply; smaller $\eta$ preserves dispersion. A loss difference $d$ multiplies relative weight by $e^{-\eta d}$, so a learning rate is meaningful only relative to loss units. Multiplying loss by $a>0$ and dividing $\eta$ by $a$ leaves updates unchanged.

#### 9.3 Static regret and the learning-rate trade-off

Assume full feedback of all expert losses $\ell_{t,i}\in[0,1]$, weights chosen before outcomes, and mixture loss $\hat\ell_t=\sum_iw_{t,i}\ell_{t,i}$. Chapter 6's bounded exponential-moment argument over expert-index probabilities gives:

$$
\ln\sum_iw_{t,i}e^{-\eta\ell_{t,i}}
\le-\eta\hat\ell_t+\frac{\eta^2}{8}.
$$

Randomization is over experts, not an IID market assumption. With $W_t=\sum_iv_{t,i}$, accumulate $\ln W_{T+1}\le\ln K-\eta\sum_t\hat\ell_t+\eta^2T/8$. Lower-bound $W_{T+1}$ by the best fixed expert's weight and combine:

$$
\sum_t\hat\ell_t-\min_i\sum_t\ell_{t,i}
\le\frac{\ln K}{\eta}+\frac{\eta T}{8}.
$$

The first term pays for not knowing the best expert; the second pays for aggressive updating. Balancing gives $\eta=\sqrt{8\ln K/T}$ and regret bound $\sqrt{T\ln K/2}$. Unknown horizons require restarted or appropriate adaptive schemes with separately stated guarantees. One expert entails no selection and zero regret. See [Freund and Schapire](https://www.sciencedirect.com/science/article/pii/S002200009791504X).

**Conclusion.** Loss range, horizon, and comparison task provide the derivation of $\eta$; financial mutual information describes a different aspect of the problem. Log candidate counts appear in both testing and aggregation as different selection costs; their guarantees are not identical.

#### 9.4 Cumulative memory conflicts with recent adaptation

If A loses one unit less over the first $m$ rounds, its weight advantage is $e^{\eta m}$. After an equal-strength reversal, about $m$ rounds are needed to erase it. Increasing $\eta$ makes concentration sharper but does not change recovery time in this symmetric example.

To track change, restart, discount history, or mix updated weights with uniform trust: $w_{t+1}=(1-\gamma)\bar w_{t+1}+\gamma/K$. Mixing preserves at least $\gamma/K$ for every expert, at the cost of continually allocating some weight to poor experts. Pure cumulative exponential updates do not guarantee rapid revival merely because weights remain nonzero.

**Design conclusion.** Use cumulative Hedge to derive static regret. The drift-adaptation teaching route uses a shared uniform weight floor and compares it with equal weights and pure cumulative Hedge, explicitly paying for continued dispersion. Handling drift also depends on the chosen memory rule. Best fixed expert, best switching sequence, and recent best are different comparators. The shared version needs its own guarantee; delay, noise, and turnover determine practical value.

#### 9.5 Return from mixture mathematics to actual trading

Taking the sign of an aggregated score generally makes its directional error differ from weighted expert errors. Convex losses permit comparisons via convexity; randomly selecting experts permits the relevant expectation interpretation. Unmatured labels cannot update weights. Overlapping horizons, multi-period attribution, delayed outcomes, and partial feedback require corresponding algorithms; immediate full-feedback guarantees do not transfer automatically.

Direction error, return loss, and cost-adjusted loss optimize different objects. Zero–one loss prefers hit rate, not necessarily net expectancy. Unbounded trading losses require suitable tail/scale controls; clipping changes the objective and must be acknowledged.

**Conclusion.** Low regret may mean losing slightly less among experts that all lose. Expert-library, rate, loss, and restart choices remain subject to Chapter 8. Online updating is not immunity to overfitting.

#### 9.6 Continuous combinations and curvature: OGD and ONS are different algorithms

On a convex weight domain, OGD uses $w_{t+1}=\Pi(w_t-\eta g_t)$, projecting back to feasibility. Projection does not increase distance; expand $\|w_t-\eta g_t-u\|^2$. With domain diameter at most $D$ and gradient norms at most $G$, accumulate and apply convexity's first-order lower bound:

$$
\sum_t\bigl(\ell_t(w_t)-\ell_t(u)\bigr)
\le\frac{D^2}{2\eta}+\frac{\eta G^2T}{2}.
$$

Choosing $\eta=D/(G\sqrt T)$ gives $DG\sqrt T$. The trade-off involves geometric distance rather than expert entropy.

A loss is exp-concave if $e^{-a\ell}$ is concave on the used domain. Twice differentiating in one dimension gives $\ell''\ge a(\ell')^2$, a stronger curvature relation. ONS uses accumulated gradient outer products to adjust geometry and can obtain logarithmic regret under bounded domains/gradients and appropriate regularization. The name “squared loss” alone does not establish the rate. AdaHedge and scale-adaptive variants have their own conditions and costs.

**Chapter principle:** aggregation requires the right loss, comparator, feedback time, and update scale. Weak and robust defines the starting layer; confirmed interaction value can justify expanding it.


#### Practical default — equal weights, log-space Hedge, then deliberate adaptation

For confirmed experts forecasting the same binary policy outcome, use orientation-aligned probabilities $p_{t,i}\in[0,1]$. Begin with equal weights and mixture $p_t=\sum_iw_{t,i}p_{t,i}$. Use bounded Brier loss $\ell_{t,i}=(p_{t,i}-B_t)^2\in[0,1]$. Convexity gives $(p_t-B_t)^2\le\sum_iw_{t,i}\ell_{t,i}$, connecting an actual probability mixture to the expert-loss comparison. Brier loss's conditional expectation is $(p-p^*)^2+p^*(1-p^*)$, so it is minimized by the true probability. Chapter 6's log-loss classifier and this aggregator's bounded probability loss have compatible ideal probabilities but different purposes.

Store unnormalized log weights $a_i$; on matured outcomes, set $a_i\leftarrow a_i-\eta\ell_i$, subtract $\max_j a_j$ before exponentiation, and normalize. Never update from outcomes not yet available. For a known $T$ mature feedback rounds, start with $\eta=\sqrt{8\ln K/T}$; for $K=20,T=252$, this is about $0.308$. The number is in these bounded-loss units and is not a gradient learning rate. Specify the update clock: the standard proof applies to immediate full-feedback rounds. For overlapping delayed trades, use a delayed-feedback design or separate nonoverlapping outcome streams and assess actual lag; do not relabel the calendar to claim the immediate bound.

For drift, compare equal weights, cumulative Hedge, and fixed-share Hedge. Select a desired recovery floor $\epsilon/K$ and mix each updated weight vector with uniform mass $\epsilon$. For an illustrative floor $\epsilon=0.02$, every expert retains at least $0.02/K$. This pays for revival with continued weight on poor experts; choose it on recorded chronological development comparisons, including turnover. Static regret remains the cumulative comparator's theorem, not automatically the shared algorithm's tracking guarantee.

**Decision mapping.** Apply the same payoff-derived no-trade band to the combined probability and independently controlled sizing. Choose a trust-update scale that permits assessment of net implementation, with portfolio transactions governed by their own rebalance rule. Adopt interactions or batch retraining only for a confirmed increment over this weak, explicit consuming layer.



#### Close the gaps in loss and geometry proofs

Carry the Hedge potential inequality through moving loss terms and dividing by positive $\eta$ before minimizing the bound. For probability mixtures, expand both Brier squares; their difference is the weighted forecast dispersion $\sum_iw_i(p_i-p)^2\ge0$. This establishes the actual mixture-loss bridge, not a sign-threshold or profit guarantee.

For OGD, use convex feasibility of $v+s(u-v)$ to differentiate squared distance at $s=0$, obtaining $(z-v)^\top(u-v)\le0$. Expand the projection distance, then the proposed gradient-step distance, and telescope the one-round inequalities. Initial distance is bounded by $D^2$; the final distance term is nonpositive. Exp-concavity is derived by $[e^{-a\ell}]''=ae^{-a\ell}[a(\ell')^2-\ell'']$. Delayed feedback, uniform-share revival, static versus switching comparators, and cash/crowding risk remain explicitly separate.

## Part IV: From judgments to strategies that survive path risk

### Chapter 10 — Portfolios and sizing: optimize less where no edge is supported

#### 10.1 Turn Scores into Feasible Holdings

**Motivation.** A high rank specifies neither expected magnitude, common risk, costs, nor capital. For asset returns $r$ with mean $\mu$ and covariance $\Sigma$, linear expectation and square expansion give portfolio mean $w^\top\mu$ and variance $w^\top\Sigma w$.

Write minimum risk at a target expected return as $\min_w w^\top\Sigma w$ subject to $w^\top\mu\ge m$, budget, and other constraints. Varying $m$ constructs the efficient frontier. This is mean–variance reasoning; a QP call is not a true-optimality certificate. Rank scores require calibration before serving as $\mu$, or must explicitly remain surrogate utilities.

#### 10.2 Why optimal solutions amplify estimation error

In the budget-free teaching problem, maximize $w^\top\mu-\lambda w^\top\Sigma w/2$ for $\lambda>0,\Sigma\succ0$. Differentiation gives $w^*=\Sigma^{-1}\mu/\lambda$. First-order perturbation is:

$$
\delta w\approx\frac1\lambda\Sigma^{-1}\delta\mu
-\Sigma^{-1}(\delta\Sigma)w^*.
$$

The first term comes from mean estimation; inverse-matrix differentiation gives the second, showing covariance error also amplifies. Small-eigenvalue directions are particularly sensitive. Optimization cannot distinguish an appealing overestimate from a real advantage.

Shrinkage $\hat\Sigma_\gamma=(1-\gamma)\hat\Sigma+\gamma\tau I$, $\tau>0$, floors small eigenvalues. Leverage, concentration, turnover, and exposure constraints also limit extreme responses. **Conclusion:** reduce input uncertainty or unsupported freedom before pursuing numerical optimality. Choose between mean–variance and risk-only methods according to which estimates have support and how their uncertainty affects the objective.

#### 10.3 From equal capital to risk contributions

Equal money in two assets does not imply equal risk. Differentiate $\sigma_p=\sqrt{w^\top\Sigma w}>0$ and multiply by weights:

$$
RC_i=w_i\frac{(\Sigma w)_i}{\sigma_p},\qquad \sum_iRC_i=\sigma_p.
$$

This decomposes current portfolio volatility into contributions. When no mean-return edge is confirmed and risk estimation passes stability checks, the multi-asset case explicitly uses risk budgeting without $\mu$ as its foundation. Removing an unreliable input reduces estimation burden; it does not create free return.

For positive budgets $b_i$ and positive-definite $\Sigma$, minimize $F(x)=x^\top\Sigma x/2-\sum_i b_i\ln x_i$ over $x_i>0$. Gradient is $\Sigma x-b/x$, Hessian $\Sigma+\operatorname{diag}(b_i/x_i^2)\succ0$. The objective grows at the boundary and infinity, giving a unique interior minimizer. At it, $x_i(\Sigma x)_i=b_i$. Normalize $w=x/(\mathbf1^\top x)$: contribution proportions are $b_i/\sum_jb_j$; equal budgets yield ERC. See [convex risk-budgeting formulations](https://portfoliooptimizationbook.com/book/11.6-vanilla-convex-formulations.html).

**Conclusion.** Use a stated objective with gradient, coordinate, or Newton methods and step control. Check positive weights, budget residuals, and stopping criteria. An alternative risk-contribution-error update needs its own objective and convergence checks; a small learning rate addresses movement size.

**Levels of retreat.** With independent assets and diagonal covariance, ERC gives $w_i\propto1/\sigma_i$, budget-constrained minimum variance gives $w_i\propto1/\sigma_i^2$, and equal capital estimates neither. They are not interchangeable names. Maximum diversification optimizes weighted individual volatility relative to portfolio volatility and still estimates volatility and correlation.

Hierarchical methods cluster using an explicit correlation distance, then allocate between groups. If standardized group portfolios have variances $v_L,v_R$ and cross-group covariance is temporarily ignored, left allocation $a$ gives variance $a^2v_L+(1-a)^2v_R$. Differentiation yields $a=v_R/(v_L+v_R)$. Recursive local allocation avoids a full global inverse, but ignored correlations, estimated trees, and recursion policies are additional assumptions—not automatic global minimum variance or ERC. This motivates HRP; particular clustering/original-algorithm variants need explicit contracts and are not mandatory tools.

#### 10.4 Neutralization and all-weather design: remove unsupported directional bets

If $B$ contains industry, size, or selected risk exposures, $B^\top w=0$ restricts those bets. Benchmark-relative constraints act on active weights $a=w-w^{\mathrm b}$. This relates to feature residualization but is not the same operation; neutral predictions do not guarantee neutral holdings.

For macro scenarios, begin with $r=Az+\epsilon$, where $z$ contains selected growth/inflation shocks and portfolio exposures are $A^\top w$. Risk-balanced assets achieve intended scenario coverage only if asset–shock mappings have support. ERC across four ETFs does not prove equal four-quadrant risk, and four quadrants do not exhaust market risks.

**Design conclusion.** Structure first, weak prediction second. Without macro-state forecasting edge, use verified risk coverage as the foundation rather than requiring the next quadrant to be guessed correctly. Independently confirmed trend tilts supplement the base within explicit bounds. Stress covariance, representative assets, leverage, and liquidity. These tests clarify the structure's role while retaining its priority over unsupported forecasts.

#### 10.5 Breadth amplifies an edge, while dependence consumes breadth

$N$ independent equally scaled P&Ls with mean $a$ and standard deviation $s$ have aggregate mean-to-volatility ratio $(a/s)\sqrt N$. If pairwise correlation is $\rho_c$, variance becomes $Ns^2[1+(N-1)\rho_c]$, giving:

$$
\frac as\sqrt{\frac{N}{1+(N-1)\rho_c}}.
$$

Positive common correlation limits gains from additional count. Stocks, factors, and events are not automatically independent breadth. The fundamental law $\mathrm{IR}\approx\mathrm{IC}\sqrt{\mathrm{BR}}$ requires appropriate forecast quality, independent opportunities, and effective implementation. Explain how IC relates to the actual prediction scale; do not substitute directional accuracy directly.

**Conclusion.** Breadth helps realize thin edges when factor validity, common tail risk, and fees are also addressed. Constraints and execution determine achievable breadth.

#### 10.6 Map probabilities to size through utility, not self-reported confidence

For repeated independent binary bets, success probability is $p$, net gain per staked unit is $b>0$, failure loses the stake, and wealth fraction is $0\le f<1$. Maximize $p\ln(1+bf)+(1-p)\ln(1-f)$. Differentiation gives unconstrained $f^*=[bp-(1-p)]/b$, then apply feasibility.

Equal probabilities but different payoff odds imply different sizes; probability-estimation error propagates directly into size. Correlation, fees, tails, capital, and uncertain probabilities change the real problem. Fractional sizing, robust estimation, and risk caps are additional designs; “Kelly” does not certify safety.

**Chapter principle:** trusted estimates determine what to optimize. Constrain and diversify unsupported dimensions. Positions are not another name for classification probabilities.

#### Practical default — three holding routes, with risk-controlled size

**Timing.** Use the payoff gate to choose sign or abstention, then scale accepted positions inversely to a past-only volatility estimate, with a fixed risk budget and leverage/concentration caps. Here $q$ denotes a return exposure, not a number of contracts: for scalar return volatility $\hat\sigma_t$, $\operatorname{Var}(qR)\approx q^2\hat\sigma_t^2$ motivates $|q|\propto1/\hat\sigma_t$. Translate exposures into actual contract quantities, rounding and multipliers; floor unusably small volatility estimates and abstain when risk inputs fail. Do not make estimated probability itself the position size. Kelly is a comparison for a known payoff model, not the starting unconstrained sizing rule.

**Cross-section.** Construct active weights $a=w-w^{\rm b}$ with $\mathbf1^\top a=0$, unsupported-exposure constraints $B^\top a=0$, per-name bounds, and turnover limits. Start from the convex objective $-s^\top a+\lambda a^\top\hat\Sigma a/2+\kappa\|a-a^-\|_1$, treating rank score $s$ explicitly as a surrogate utility unless calibrated. Choose risk and turnover budgets in development. The linear reward allocates to preferred ranks; the quadratic term restrains correlated exposure; the L1 term prices trading. Check feasibility, residuals, costs, and matched benchmark-relative performance. Score-scale changes require corresponding coefficient handling.

**Multi-asset allocation without mean edge.** Use equal capital as the reference and equal risk budgets as the selected base. Estimate past-only covariance, shrink toward a stated positive diagonal/isotropic target, and solve the strictly convex log-barrier problem in Section 10.3. Check normalized risk-contribution residuals; rebalance on a preset schedule subject to turnover and liquidity. Set a portfolio-volatility target only within cash/leverage limits. Asset–macro stress mapping determines representative coverage; bounded trend tilts are a separately confirmed supplement.

**Why and when to change.** The inverse-estimation perturbation selects shrinkage and constraints; the Euler decomposition selects risk budgets rather than equal money; the cash-flow objective selects feasible positions instead of raw scores. Add expected-return optimization only after the mean estimates' incremental use is established. Keep this concrete base as the comparison point when investigating alternatives to ERC.



#### Derivation checkpoints retained in the revised lecture

- Expand covariance with both index sums; derive the mean–variance gradient and first-order perturbed equation before applying the inverse.
- For ERC, write $c=\sum_jx_j$, $w_i(\Sigma w)_i=b_i/c^2$ and $\sigma_p^2=(\sum_jb_j)/c^2$ before cancelling normalization. Positive definiteness and log-boundary growth give attainment and uniqueness; coordinate roots are exact positive-coordinate minima, not generic gradient guesses.
- For active-risk tuning, display both inequalities $G(a_1)+\lambda_1R_1/2\le G(a_2)+\lambda_1R_2/2$ and $G(a_2)+\lambda_2R_2/2\le G(a_1)+\lambda_2R_1/2$. Addition proves $(\lambda_2-\lambda_1)(R_2-R_1)\le0$, justifying bracket/double/bisect against a preset risk cap.
- Retain the full All Weather teaching route: cash/beta/alpha distinction, growth/inflation surprises, $r=Az+\epsilon$ shock coverage, equal-ERC assets sharing one shock as a counterexample, a past-only 252-session shrunk-covariance asset ERC baseline, monthly rebalancing, and separately tested 50/200 trend multipliers 1.15/0.85. The overlay breaks exact original risk budgets; no shallow-drawdown or proprietary replication claim follows. Under covariance scaling $c\Sigma$, distinguish the new auxiliary solution $y=x/\sqrt c$ from the old $x$.
- Show Kelly's multiplication by the positive denominators, collect $bf=bp-(1-p)$, and use the negative second derivative before clipping to the permitted stake interval.

### Chapter 11 — Execution and funding paths: a correct judgment can fail before realization

#### 11.1 A backtest first simulates legitimate temporal order

**Motivation.** A signal computable only after close cannot unconditionally fill at that same close. Specify data availability → calculation → order → fill → holding → settlement. A quote touch, order accessibility, and an actual fill are different observations.

Record wealth as $V_t=B_t+q_tP_t$ using cash $B_t$, quantity $q_t$, and price $P_t$. Buying $\Delta q$ reduces cash by $P_t\Delta q$ plus costs. Same-price rebalancing creates no wealth before costs. Subsequent P&L combines inventory-price changes with cash, dividends, financing, and settlement flows.

**Conclusion.** Event replay constructs the equity curve from cash, inventory, and their costs at the appropriate times. Connect model-score time, label-reference time, and executable entry time.

#### 11.2 Turnover and impact change the optimal action

Simplified replay is $R_{k+1}^{\mathrm{net}}=w_k^\top r_{k+1}-c\|w_k-w_k^-\|_1-\mathrm{Impact}_k$, where $w_k^-$ denotes drifted pre-rebalance holdings, not the previous target. Match cash denomination, return denominator, and cost units.

For one-way quantity $q\ge0$, expected per-unit gain $\mu$, proportional cost $c$, and marginal impact $kq$, integration gives net expectancy $(\mu-c)q-kq^2/2$. For $k>0$, differentiation yields $q^*=\max((\mu-c)/k,0)$. Capacity is finite even before risk and capital constraints.

**Conclusion.** Fees can erase a small predictive edge, and scale erodes it nonlinearly. Coordinate frequency, holding horizon, aggregation updates, and risk limits. A model learning rate controls fitting, while trading frequency governs implementation. The quadratic impact example is a teaching model requiring empirical testing, not a market law.

#### 11.3 Express multi-leg risk as actual residual exposure

Desired fills $q^*$ and actual fills $q^{\mathrm{fill}}$ leave residual $q^{\mathrm{fill}}-q^*$. Limits, queues, partial fills, and rejects may prevent locking the theoretical spread. Observed quotes do not prove simultaneous executable liquidity at required size.

Canceling an unfilled order and closing a filled position have different cash consequences: closing uses a new transaction with new prices and fees. **Conclusion:** specify partial-fill responses and maximum residual exposure. “Atomic rollback” cannot conceal leg risk.

#### 11.4 Terminal correctness and interim solvency are separate requirements

Let available cash be $K_t$ and net funding requirements from margin, financing, fees, and other obligations be $D_t$. Survival to convergence requires covering each critical-time obligation under actual settlement and financing rules. Positive terminal payoff does not prove $K_t-D_t\ge0$ along the path.

Daily settlement, collateral haircuts, rolls, and rebalancing alter funding demand. Test maximum stressed cash deficits and exit feasibility alongside terminal returns. Rising dependence can make supposedly independent legs demand cash simultaneously.

**Chapter conclusion.** Net P&L, drawdowns, capital paths, capacity, and fill semantics jointly determine realization. Start with offline replay and controlled implementation; use the resulting evidence to decide how far to expand. Historical simulation does not certify future actual fills.

#### Practical default — a next-feasible-entry event ledger and capacity ladder

For daily research, start with signals computed after the selected observation cutoff and orders at the next declared feasible trading opportunity. Simulate actual prices/contract quantities, cash, fees, financing, dividends/settlement, rolls, partial fills where relevant, and exits. Keep signal time, order time, fill time, and outcome time separately. This rule supplies a replay timeline; it is not a claim that every market's next open provides an unrestricted fill.

Test the ledger on no-price-change rebalancing, one dividend/settlement event, one roll, a price gap, and a rejected or partial order. Rebalancing at one unchanged price cannot create pre-cost wealth. Reconcile the ledger with this identity before viewing performance curves.

Run a capacity ladder with frozen policy and increasing order sizes. Report gross edge, net edge, turnover, maximum stressed cash requirement, and residual risk, not just Sharpe. In the teaching impact model, $q^*=(\mu-c)_+/k$ explains why scale must stop when marginal impact consumes marginal gain; actual liquidity and funding constraints may stop it earlier. Multi-leg replay has an explicit completion/hedge/cancel policy and residual exposure limit.

**Decision.** A strategy advances from offline confirmation to a human-authorized controlled implementation only after the stated cash, cost, capacity, and failure checks pass. This tutorial supplies the offline method; it does not itself authorize orders. The failure mechanism guides revisions to horizon, turnover, position size, or exit design before a new predictive network is considered.



#### Derivation checkpoints retained in the revised lecture

- Expand the cash/stock wealth identity after a signed fill; derive drifted stock weights from the name value divided by positive total ending wealth. Futures notional is not a purchased stock value.
- For $\lambda\sigma^2>0$, the scalar concave inventory problem has band edges $(\mu-c)/(\lambda\sigma^2)$ and $(\mu+c)/(\lambda\sigma^2)$: below the band buy to its lower edge, inside retain inventory, above sell to its upper edge, then respect feasible bounds. The left/right derivative condition proves the middle case; this is not the classifier's probability band.
- Retain mechanism-scoped LTCM and UK LDI funding lessons: terminal value and liability improvement do not meet a cash deadline without accessible resources.

### Chapter 12 — Lifecycle and traceable computation: know what each improvement changed

#### 12.1 Bind results to the full research chain

**Motivation.** The same model can behave differently after data revisions, universe changes, or fill assumptions. Bind a result to its target, sources, PIT rules, representation/model versions, parameter selection, confirmation scope, benchmark, and execution policy.

For each change, identify affected downstream objects. Inventory-release timestamp changes affect features, training, and replay; fixing a plot title does not change evidence. **Conclusion:** versions delimit evidence and locate changes. Reproducibility combines the seed with the other recorded inputs and dependencies.

#### 12.2 Separate data, relation, and implementation failures in monitoring

Inspect input correctness → continued support for predictive relations → exposure/size changes → cost/fill deterioration. Falling rolling IC directs diagnosis toward drift, data faults, sample noise, target changes, and possible competitive alpha decay.

$M$ independent repeated tests at false-alarm rate $\alpha$ yield at least one false alarm with probability $1-(1-\alpha)^M$. Real rolling windows depend on one another, so this equation is not their probability, but repeated observation still changes inference. Prespecify thresholds, windows, and stopping or use suitable sequential methods; local significance at each glance does not guarantee global reliability.

**Conclusion.** Updating, downweighting, retirement, and pausing have separate triggers and retain failure records. Monitoring does not reset Chapter 8's selection history.

#### 12.3 Scale infrastructure around measured work

Read/write, compute, and communication have distinct bottlenecks. If fraction $s$ is serial and the rest splits ideally over $p$ workers, normalized time is at least $s+(1-s)/p$, so ideal speedup is its reciprocal. Synchronization, communication, and contention further affect realized speedup.

Sharing, caches, subexpression reuse, and batched inference reduce repetition; state sharding trades memory against communication. Compare identical semantics, precision, and completed work. Complete research speed includes the full workload around forward calls.

**Conclusion.** Chapter 8 supplies scoring capacity; this chapter supplies reproducibility, observation, and recovery across the chain. Redundancy, snapshots, backups, and restore testing differ. Even minimal infrastructure needs clear boundaries.

#### 12.4 Knowledge and permission are separate chains

Sources/licenses, third-party transmission, credentials, trading interfaces, controlled implementation, and publication each have authorization and service conditions. Offline explanation does not authorize these operations. Check law, exchange, and provider rules for the actual object and version; tutorial generalities are not legal conclusions.

**Chapter principle:** effective results should be repeatable, anomalies locatable, failures stoppable, and changes re-verifiable. Automation remains within established trust and permission; continued production depends on supported opportunities.


#### Practical default — an experiment manifest, shadow replay, and staged failure actions

Bind each experiment to data snapshot, universe, target/exit policy, feature/model/optimizer versions, trial history, date partitions, cost/fill assumptions, benchmark, and confirmation result. Generate predictions once from the frozen version and retain them; reconcile reruns and explain any difference. A change log identifies which downstream decision needs reevaluation.

Use three monitoring layers: data integrity/availability; prediction calibration and rolling task performance; realized exposure, cost, fill, and funding behavior. Prespecify review windows and tolerance bands from development/stress evidence. Hard data or limit violations suspend affected actions immediately. Statistical deterioration triggers a scheduled investigation; a subsequent retuning decision brings new selection and confirmation obligations. Confirmed relation failure removes/downweights the affected factor under the recorded policy. A model/data change starts in shadow replay and returns through confirmation before consumption.

Scale infrastructure in measured order: remove duplicated reads/computation, batch/cache, parallelize independent work, and use state sharding when memory/communication measurements justify it. Restore a snapshot and reconcile the replay before describing backups as recoverable.

**Why and when to change.** Full-chain binding locates the source of changed outcomes; repeated-test probability motivates scheduled or sequentially valid reviews; the serial-fraction bound selects actual bottlenecks. The result is a small operating procedure whose suspend, investigate, retire, and redevelop actions give monitoring a concrete purpose.




#### Derivation checkpoints retained in the revised lecture

- Explain $1-(1-\alpha)^M$ by multiplying independent no-alarm probabilities. For a fixed family of valid tests, use $1_{\cup_j A_j}\le\sum_j1_{A_j}$ and expectation to derive the dependence-free union bound, with a stated error budget and review schedule.
- Derive the serial plus parallel runtime before taking its reciprocal; distinguish the four full-precision Adam arrays' $16P$ bytes from complete peak memory.
- Retain the Knight Capital incident as deployment/order/exposure-control evidence, not proof of prediction decay.

## Part V: Arbitrage—known structure is not locked-in profit

### Chapter 13 — From strict arbitrage to statistical relations: identify constraints, then test realization

#### 13.1 Why identical cash flows should have identical prices

**Motivation.** Trend research asks how the future tends to move. Arbitrage first asks which prices cannot vary independently. If two tradable positions produce identical cash flows in all admissible states but have different prices, buying the cheap and selling the expensive locks their difference. Replication supplies the cash-flow cancellation on which this result rests.

Strict arbitrage, under stated trading, financing, and settlement rules, has nonpositive initial net cost and almost-surely nonnegative terminal net payoff, with strict benefit either initially or at maturity on a positive-probability event. Interim admissibility and financing must also hold. Many practical “arbitrages” have a positive conditional expectation alongside breakdown, gap, borrow, margin, and counterparty risk. Their evaluation therefore includes those losing states.

In FX triangles with units B/A, C/B, and A/C, choose executable bid/ask directions. The product must exceed one to exchange one unit A back into more A. Midquote products do not lock profit; sequential fills, size limits, and costs can erase it.

**Conclusion.** State assets, cash flows, directions, executable prices, and financing before analyzing relations. Easy identification does not imply easy realization.

#### 13.2 Public relations can shift value toward latency, inventory, and costs

**Motivation.** If everyone computes the relation immediately, differentiation often lies in earlier or cheaper execution rather than a larger forecasting network. Illustrate with remaining gross edge $\Delta(l)=\Delta_0e^{-l/\tau}$ after latency $l$, where $\tau$ is the assumed decay scale.

Net edge is $\Delta_0e^{-l/\tau}-c$. For $c>0$, positivity requires $l<\tau\log(\Delta_0/c)$. If $\Delta_0\le c$, no speed creates this edge. Latency and cost must improve together, and opportunity magnitude bounds the value of faster hardware.

**Boundary.** Exponential decay is a testable opportunity model, not all arbitrage. Merger and term-structure relations need not disappear in microseconds. Risk premia are not identical competitive mispricings. Model capability, information timing, tradability, and capital remain separate; low target entropy does not prove executability.

#### 13.3 A common trend can coexist with a stable spread

**Motivation.** High price correlation does not imply mean-reverting spreads. Construct common random walk $G_t=G_{t-1}+u_t$ and stationary disturbances $e_t^A,e_t^B$: $A_t=G_t+e_t^A$, $B_t=\beta G_t+e_t^B$, $\beta\ne0$. Individual level variances may grow, while:

$$
Z_t=A_t-B_t/\beta=e_t^A-e_t^B/\beta
$$

The linear combination removes the common trend. Nonstationary levels with a stationary linear combination motivate cointegration. Stationarity means joint-distribution invariance under time shifts, or explicitly weak stationarity of means, variances, and covariance structure—not movement toward zero every period.

For conditional reversion, separately assume $Z_{t+1}-\bar Z=a(Z_t-\bar Z)+\epsilon_{t+1}$ with $0<a<1$ and zero conditional noise mean. Then $\mathbb E[Z_{t+h}-\bar Z\mid Z_t]=a^h(Z_t-\bar Z)$. Independent equal-variance noise gives forecast variance $\sigma_\epsilon^2(1-a^{2h})/(1-a^2)$ and half-life $\log(1/2)/\log a$. These come from the dynamic model, not the word cointegration.

**Conclusion.** Correlation describes co-movement; cointegration describes long-run level constraints; conditional dynamics describe reversion speed; policy determines worthwhile bets. Log-price coefficients also need conversion to actual quantity holdings, not direct use as share counts.

#### 13.4 Define tests and exit policies alongside the relation

Explain why unit-root hypotheses permanently accumulate some shocks before introducing ADF's tested object. Engle–Granger estimates a relation then tests residuals; residual-test critical values differ from an ordinary test of a prespecified series. Johansen handles multivariate systems with explicit trends, lags, and sample requirements; the study design determines these settings.

$n$ assets yield $n(n-1)/2$ pairs, so choosing the most significant introduces selection. Fix relations and windows in development; test structure, costs, and cash sustainability out of sample. Full-sample regression followed by historical signal replay is still look-ahead.

**Policy.** Form $z_t=(Z_t-\hat m_t)/\hat s_t$ from development or timely historical estimates. Enter contrarian positions beyond $b_{\rm in}$, exit inside smaller $b_{\rm out}$, and define breakdown, horizon, and loss limits. Different entry/exit thresholds create hysteresis and reduce boundary churn. Include holding state: identical $z_t$ does not distinguish “not entered” from “waiting to exit.”

**Conclusion.** A long-run relation is not short-run funding assurance. Exit, suspension, re-estimation, and resumption conditions are part of the strategy.

#### Practical default — residual-spread research with a fixed stateful policy

Start with economically related assets, using the relation to guide a small candidate set. In development, estimate a spread coefficient and center/scale, inspect the residual's unit-root and conditional-reversion evidence with the matching test, and fit a simple AR(1) reversion model when supported. Use its estimated half-life to propose a holding horizon and to decide whether expected reversion can cover costs. Freeze the relation before forward replay or reestimate on a predefined rolling schedule using only past observations.

For the teaching prototype, form a past-standardized residual and enter contrarian beyond $|z|=2$, exit inside $|z|=0.5$, with a preset horizon, stressed cash limit, and relationship-break suspension. The thresholds are a reproducible starting hysteresis policy, not claimed statistical optima. Store whether a position is already held. Translate spread coefficients into actual quantities/delta exposures rather than directly treating a log-price regression coefficient as a share count.

**Derive participation.** From $\mathbb E[Z_{t+h}-\bar Z\mid Z_t]=a^h(Z_t-\bar Z)$, expected convergence is $(1-a^h)(Z_t-\bar Z)$. For the chosen direction and hedge units, compare this gross change with entry/exit costs and a risk/funding buffer before opening a trade. The $z$ threshold identifies an unusual state; the convergence and cash calculation decide whether trading it is worthwhile. Participation combines the stationary-residual evidence with the convergence and cash calculation.

Forward-test the frozen pair/policy against no position and simple spread baselines, retaining selection across pair/window trials. For strict replication relations, skip a reversion forecast and instead test executable cash-flow inequalities, sizes, and completion. This distinction leads to a different algorithm for each kind of relation.



#### Derivation checkpoints retained in the revised lecture

- Taking logs and multiplying the latency inequality by $-\tau$ reverses its direction. Iterate one and two AR steps before the general $a^{h-j}$ shock coefficient; condition future shocks on their own preceding information. Derive the finite squared-coefficient geometric series by telescoping.
- Convert price-level and log-price relations into different actual quantities; retain stateful hysteresis and unavailable-borrow/reference-session cases.

### Chapter 14 — Arbitrage tasks and text tools: outcomes, time, and capital determine methods

#### 14.1 Merger Arbitrage Combines Event Probability and Payoff

**Construction.** Current purchase price is $P$, success payoff $U$, failure value $D$, success probability $p$, and combined fees/funding cost $c$. Expected net payoff is $pU+(1-p)D-P-c$; with $U>D$, break-even probability is $(P+c-D)/(U-D)$. Even high success probability can be unattractive with severe failure loss. Direction accuracy misses the payoff problem.

Add payment time, stock-exchange terms, approval, cash, and borrow conditions. Equal expected spreads tied up for six months and one week use capital differently. Spread-implied “market probability” equals a physical probability only under further simplified cash-flow, discounting, and risk-pricing assumptions. Common policy shocks also limit event breadth.

**Conclusion.** Text analysis turns clauses affecting cash flows, timing, and outcome probabilities into versioned judgments that can be calibrated and used in the payoff decision.

#### 14.2 From LLM Extraction to Calibrated Event Probabilities

Separate timely document acquisition → clause/evidence-location extraction → event-state construction → outcome-probability/horizon calibration → decision calculation. Retain sources and unresolved items at every step. Retrieval can add missing content, but omissions, lost negation, and incomplete clause coverage propagate. Model agreement assists review; source checks support factual accuracy.

**Argument.** Token probability concerns the next text fragment given context; merger-completion probability concerns an event outcome. Their sample spaces differ. Event probability requires historical event labels, strict temporal splits, calibration, and payoff-sensitive error assessment. Summaries can improve usable representation or discard critical conditions, returning to Chapter 2's processing-versus-limited-model distinction.

Pretraining may contain outcomes after the replay date. A truncated retrieval corpus does not erase model memory. Freeze model, prompts, inference settings, and cache lineage, and audit leakage. Low temperature reduces some sampling variation; it does not guarantee complete reproducibility.

**Implementation principle.** Choose self-hosting, APIs, batching, caches, and inference services by permissions, sensitivity, version freezing, throughput, end-to-end latency, and total cost. A hosting preference is evaluated through these workload-specific comparisons. Factual verification, mathematical consistency, and permitted use receive separate checks.

#### 14.3 Cross-market spreads and funding: less price exposure still leaves capital constraints

$P_B-P_A$ matters only if both venues fill the required quantities. Transfer-before-sale leaves price and platform risk during transit. Prefunded inventory reduces waiting but consumes bilateral capital and requires rebalancing. A joint ledger places the spread alongside both venues' cash, inventory, transfers, and defaults.

For linear spot/perpetual contracts with approximate unit-delta hedging, long spot and short perpetual net P&L decomposes as:

$$
\Pi_T\approx b_0-b_T+\sum_k F_k-\text{financing, execution, and rebalancing costs},\qquad
b_t=P_t^{\rm perp}-S_t,
$$

$F_k$ is funding actually received by the short, with sign defined by platform rules. Positive funding today need not persist; basis and costs can offset receipts. Different collateral currencies, nonlinear contracts, and mechanisms require a rewritten ledger.

**Conclusion.** Approximately delta-neutral does not mean fixed P&L or stable margin cash demand. Separate-account marking, liquidation, and counterparty risk can prevent eventual convergence from being realized.

#### 14.4 Spot–forward and term relations: derive replication instead of memorizing formulas

**Construction.** In an ideal no-dividend market permitting borrowing and holding the asset at fixed rate $r$, borrow $S_0$, buy spot, and sell a forward at $F_0$. Delivery leaves $F_0-S_0e^{rT}$. If the reverse strategy is feasible too, no arbitrage forces $F_0=S_0e^{rT}$. Subtract present values of known cash dividends; include deterministic storage costs in replication.

Physical convenience yield is a noncash service, not necessarily tradable like known dividends. Borrow limits, unequal funding, storage capacity, and fees can turn equality into executable price bands. Calendar, cross-product, and processing spreads need quality, location, substitution, or conversion mechanisms; historical stability does not establish hard lock-in.

**Chapter conclusion.** Match method to bottleneck: events need facts and probabilities; hard relations need executable quotes and replication; statistical relations need verification; inventory/term tasks need cash management. Task analysis determines how much latency matters alongside the other dimensions.

#### Practical default — event facts into payoff states; hard spreads into ledgers

**Event route.** Start with versioned event dossiers: payment terms, consideration, deadlines, approvals, termination clauses, failure scenario, and evidence locations. A text model extracts these fields and unresolved clauses; a human/source check settles them. Use historical, temporally admissible event labels to fit a small completion-probability and time model, with frequency/calibration baselines. Feed those probabilities and state payoffs into $pU+(1-p)D-P-c$. In a teaching cash deal with $P=95,U=100,D=80,c=1$, participation requires $p>0.8$; even a probability of 0.75 is insufficient. The payoff contract determines the threshold against which the event judgment is assessed.

**Hard cross-market relation.** Query executable sides and sizes, calculate the complete net cycle or matched cash flows, and reject opportunities below costs plus an execution/funding buffer. Replay one joint ledger for both venues and prefunded inventory. Maintain explicit partial-fill and platform-failure actions; latency spending follows measured remaining edge. Transfer-before-sale and prefunded execution are distinct policies to compare, not hidden implementation details.

**Spot/perpetual and term route.** Model basis, funding actually received, borrowing, collateral, rebalance, and settlement in one cash-path calculation. Use scenario paths with funding sign reversal, basis widening, and collateral stress. Position limits come from the stressed cash path and available execution, even when approximate delta is zero. For spot–forward equality, construct the spot borrowing/holding/delivery replication first, then convert infeasible reverse legs or costs into executable bands.

**Decision.** Use event probabilities for uncertain completion; executable inequalities for replicable payoffs; verified dynamics for statistical relations; and explicit ledgers for financing/inventory. Each task thereby has a concrete design tied to its payoff and realization bottleneck.




#### Derivation checkpoints retained in the revised lecture

- Derive the merger threshold by expanding $(1-p)D$ and dividing by the positive payoff gap, preserving termination-fee recipient and cash-calendar distinctions.
- Derive each forward bound from its own executable long-spot/short-forward or reverse-carry legs; funding received and basis change need a joint spot/perpetual ledger, not a guaranteed annualized rate.
- Retain source-scoped Metallgesellschaft, Amaranth conduct/concentration, and FTX custody lessons without inventing eventual profitable counterfactuals.

## Part VI: Pricing, numerical computation, and hedging

### Chapter 15 — Replication and risk-neutrality: construct prices from cash-flow constraints

#### 15.1 One-period replication forces a different probability weighting

**Motivation.** Contractual terminal payments do not require guessing physical up probability if existing assets replicate them. Let stock $S_0$ move to $uS_0$ or $dS_0$, cash grow by $R$, and derivative pay $H_u,H_d$. Match both with $\Delta$ shares and current cash $B$: $\Delta uS_0+BR=H_u$, $\Delta dS_0+BR=H_d$.

Subtract to obtain $\Delta=(H_u-H_d)/(S_0(u-d))$; substitute and compute initial cost:

$$
V_0=\Delta S_0+B=R^{-1}[qH_u+(1-q)H_d],\qquad
q=\frac{R-d}{u-d}.
$$

$d<R<u$ gives $q\in(0,1)$ and excludes simple arbitrage in this frictionless two-state model. Physical up probability never enters replication cost. $q$ is reweighting forced by tradable prices, not investors' actual risk neutrality or a forecast of observed up frequency.

**Conclusion.** Construct replication before introducing new probabilities. Backward induction extends the same operation to multi-period trees. Discounted assets' conditional next-period average then equals their current value; only afterward name this relation a martingale.

#### 15.2 Continuous time adds a second-order term, while stock drift disappears from pricing

Introduce Brownian motion through independent zero-mean increments with variance equal to elapsed time. Increment scale is $\sqrt{dt}$, so accumulated $(dW)^2$ cannot be discarded as in ordinary calculus; its limiting contribution is $dt$. For $dS=\mu Sdt+\sigma SdW$ and smooth $V(t,S)$, second-order expansion yields:

$$
dV=(V_t+\mu SV_S+\tfrac12\sigma^2S^2V_{SS})dt+\sigma SV_SdW.
$$

First explain stochastic integration using holdings known at the time; then state smoothness, integral, and limiting conditions. The stochastic-integral construction gives the formal notation its limiting meaning. Self-financing value $H$ and shares $\Delta$ satisfy $dH=\Delta dS+r(H-\Delta S)dt$; arbitrary holding changes are not automatically self-financing.

Set $H=V$, $\Delta=V_S$ and match stochastic/drift terms:

$$
V_t+\tfrac12\sigma^2S^2V_{SS}+rSV_S-rV=0,
\qquad V(T,S)=\text{contract payoff}(S).
$$

$\mu$ disappears because dynamic replication removes stock risk, not because physical mean returns do not exist. For constant coefficients, no dividends, and a European call, risk-neutral lognormal integration gives $C=S\Phi(d_1)-Ke^{-r(T-t)}\Phi(d_2)$, where $d_1=[\log(S/K)+(r+\sigma^2/2)(T-t)]/[\sigma\sqrt{T-t}]$ and $d_2=d_1-\sigma\sqrt{T-t}$. Derive how the discounted probability and truncated stock expectation produce $d_2$ and $d_1$; the closed form follows from these expectations.

#### 15.3 Information distance between probability measures: preserve the insight and identify the object

**Motivation.** Physical $P$ concerns occurrence; pricing $Q$ expresses replication. Their difference is quantifiable but is not predictive mutual information. Define $D(P\|Q)=\mathbb E_P[\log(dP/dQ)]$, the physical-distribution average log likelihood ratio, in nats for natural logs.

With constant $\mu,r,\sigma>0$, a length-$h$ log-price increment is Gaussian under each measure, with common variance $\sigma^2h$ and means differing by $(\mu-r)h$. Taking the log density ratio and averaging under $P$ gives:

$$
D(P_h\|Q_h)=\frac{[(\mu-r)h]^2}{2\sigma^2h}
=\tfrac12\theta^2h,\qquad\theta=(\mu-r)/\sigma.
$$

Independent-increment densities multiply, so log distances add; a complete increment grid spanning $T$ gives $\tfrac12\theta^2T$. Here $\theta$ is excess drift per volatility unit: greater compensation separates path distributions more. Divide by $\log2$ for bits. Measure-change conditions establish when the finite-grid construction extends to continuous paths.

Only later construct exponential likelihoods and Girsanov changes. Under suitable absolute continuity, true exponential-martingale, and integrability conditions, the time-varying path distance takes form $\tfrac12\mathbb E_P\int_0^T\theta_t^2dt$. See [Pavliotis's stochastic-process text](https://www.ma.imperial.ac.uk/~pavl/PavliotisBook.pdf); the notes construct the finite Gaussian likelihood, state the exponential-martingale/Novikov and integrability contract for the continuous theorem, and derive the expected log likelihood under that contract; the full measure-change theorem is supplied by the cited source.

**Conclusion.** This relates distributional distance to market price of risk, not recoverable alpha bits or future certainty. Prices remain random under $Q$, and premia are not riskless arbitrage.

#### 15.4 Replicable risks determine price uniqueness

Stock and cash span two-state payoffs. More independent risks without more traded instruments generally leave some payoffs unspanned. No arbitrage may then bound a price set rather than determine one price. Pricing measures can be nonunique; specify calibration, preferences, or hedging criteria.

**Chapter conclusion.** Physical forecasting, risk-neutral computation, and risk bearing are different problems. Formulas live within replication, financing, trading, and model conditions. Frictions and model discrepancy are addressed in Chapters 16 and 17.

#### Practical default — a replicating tree before continuous-time formulas

Build a one-step stock/cash tree with stated $S_0,u,d,R$ and the contract's two payoffs. Solve the two replication equations, compute $\Delta,B,V_0$, and verify both terminal cash flows. A transparent example is $S_0=100,u=1.1,d=0.9,R=1$, strike 100: call payoffs are 10 and 0, giving $\Delta=0.5,B=-45,V_0=5$ and $q=0.5$. Changing the physical up probability does not change these matched cash flows or this replication price.

Extend by backward induction on a recombining tree; retain payoff and boundary conventions. Then derive the continuous self-financing/PDE route and compare a plain European call with its closed form. Use tree/grid refinement and finite-difference Greek checks to separate numerical error from payoff/model changes. The pricing measure and discounting follow the replication, giving a replicable option's price a direct route distinct from physical-return classification.

For an unspanned payoff, show the failed cash-flow matching system before selecting a calibration or risk criterion. That criterion becomes part of the price definition. A solver's unique output is then interpreted through that additional criterion, alongside the incomplete replication.

**Why this is the default.** The finite linear system is reconstructible with the reader's prerequisites. It establishes why probabilities are reweighted and what a hedge actually holds before stochastic calculus is introduced. Advanced models extend this explicit base in response to its identified gaps.



#### Derivation checkpoints retained in the revised lecture

- Keep downward multiplier $d$ a scalar variable, not the differential operator $\mathrm d$. Display the subtraction, cash substitution, and common-denominator collection producing $q=(R-d)/(u-d)$.
- Derive the normal fourth moment by integration by parts. Independent Brownian squares have sum expectation $T$ and variance $2T^2/n$, giving a mean-square quadratic-variation limit. For adapted step holdings, use the tower rule before the later shock to eliminate cross terms and derive the stochastic-integral isometry.
- Show which Taylor terms survive, then display both Itô and self-financing drifts and cancel $\mu SV_S$ explicitly.
- In the call integral, derive the exercise lower bound, complete the normal square, shift it from $-d_2$ to $-d_1$, and cancel the exponential factors. Derive $S\phi(d_1)=Ke^{-r\tau}\phi(d_2)$ before delta/gamma/vega cancellation.
- Complete the finite Gaussian square for the likelihood shift. Distinguish this direct finite calculation from the continuous Girsanov theorem contract and the separate zero-mean/integrability step used for path relative entropy.
- Retain the three-state unspanned call and nonunique pricing weights $(a,1-2a,a)$ as an actual failed replication construction.
- Before invoking the lognormal terminal distribution, apply Itô to the logarithm of the stock price and integrate its drift and Brownian increment to derive the exponential terminal-price law.

### Chapter 16 — Volatility and paths: which risk structures must a model retain?

#### 16.1 Switching from means to volatility changes estimation difficulty

**Motivation.** A tiny directional mean does not make every price statistic equally hard. For IID Gaussian $R_i\sim N(\mu,\sigma^2)$, mean standard error is $\sigma/\sqrt n$; unbiased sample variance has variance $2\sigma^4/(n-1)$ and relative standard error $\sqrt{2/(n-1)}$. A small $|\mu|/\sigma$ makes relative mean error large without equally worsening variance estimation. This compares specified tasks, not all volatility forecasts.

Conditional volatility may persist: $R_t=\sigma_t\epsilon_t$, $\sigma_t^2=\omega+aR_{t-1}^2+b\sigma_{t-1}^2$. With independent standardized noise and suitable stability, past squared returns affect conditional variance even with zero mean. The model represents clustering, and its forecasts are assessed for generalization.

**Conclusion.** Difficulty belongs to an input–target–horizon–model combination. Thin directional information does not characterize every financial computation. Realized volatility measures historical paths; implied volatility inverts a pricing formula to match quotes. They are different observations.

#### 16.2 Smiles motivate additional volatility structure

Strike-dependent implied volatility at one maturity prevents a constant-volatility model from matching all quotes. A smile is a price-surface phenomenon, not a unique dynamic law. Local volatility lets diffusion depend on $(t,S)$; stochastic volatility adds variance state; jumps permit finite moves. Models can fit similar quotes yet imply different forward smiles and hedging risks.

**Argument.** For $k$ independent Brownian risks and $n$ traded tools with exposure matrix $A\in\mathbb R^{n\times k}$, hedging target exposure $g\in\mathbb R^k$ requires $A^Tq=g$. Full local diffusion hedging is possible only when $g$ lies in the span of available exposures. The available traded tools determine whether added stochastic-volatility exposure remains unspanned.

A price jump $\Delta S$ leaves delta-hedging residual $V(S+\Delta S)-V(S)-V_S\Delta S$, generally nonzero. An infinitesimal derivative does not hedge arbitrary finite jumps.

**Conclusion.** Evaluate quote fit, dynamics, tradable spanning, and out-of-sample hedging together. Calibration success is not dynamic correctness.

#### 16.3 Volatility trades require gamma-, path-, and cost-aware accounting

**Motivation.** “Implied exceeds realized, therefore profit” omits direction, weights, and costs. For smooth option $V$ priced at $\sigma_m$, actual continuous volatility $\sigma_a$, equal rates, no frictions, and continuous delta hedging, the PDE and actual-path Itô expansion give local net gain for long option/short $V_S$ shares plus financing:

$$
d\Pi=\tfrac12 V_{SS}S^2(\sigma_a^2-\sigma_m^2)dt.
$$

Introduce $\Gamma=V_{SS}$ to show this compares variance differences weighted by $\Gamma S^2$. Long and short gamma reverse the sign. Gamma changes along the path; discrete rehedging, jumps, and surface moves add other terms.

**Conclusion.** Volatility premia warrant research, but average IV−RV is not executable riskless profit. Steady short-option income may carry large tail losses and margin demands; evaluate survival along the path.

#### 16.4 Path dependence forces state augmentation

Asian contracts depend on accumulated averages. Construct $A_t=\int_0^tS_u\,du$, so $dA_t=S_tdt$. Equal $S_t$ with different $A_t$ can imply different value; use at least $(S_t,A_t)$. Barriers require hit status or running extrema. Begin with concrete finite-state augmentation before genuinely irreducible path functionals.

For whole-history value, ordinary $V(t,S_t)$ derivatives do not cover required changes. A horizontal derivative extends time while freezing the endpoint; a vertical derivative holds history fixed and changes only the current endpoint. Under suitable path regularity, functional Itô retains time, endpoint, and second-variation organization. Constructing these operations gives the new terminology a concrete connection to the ordinary chain rule.

#### 16.5 Path signatures represent ordered movement

**Construction.** Endpoints miss which coordinate moved first. For finite-variation path $X$, level one is $\int dX_i$, level two $\int_{u<v}dX_i(u)dX_j(v)$. Moving $(0,0)\to(1,0)\to(1,1)$ gives $S^{12}=1,S^{21}=0$; reversing order exchanges them while endpoint increments remain equal. Ordered integrals preserve the missing distinction.

Organize all levels as a signature. Truncation at level $m$ in dimension $d$ has $\sum_{k=1}^m d^k$ terms: more order detail also adds capacity. A purely one-dimensional signature depends only on total increment, so it does not encode the whole shape; a time coordinate is often needed. Full-signature identification requires path-equivalence and regularity conditions; approximation of path functions requires conditions such as compactness and continuity. Finite truncation is not automatically lossless or accurate.

**Conclusion.** Signatures offer interpretable path representation and controlled approximation, evaluated on their specified use. See [Chevyrev and Kormilitzin](https://arxiv.org/abs/1603.03788).

#### 16.6 Roughness and long memory are different concepts

$\mathbb E[(X_{t+h}-X_t)^2]\propto h^{2H}$ describes scaling; smaller $H$ means greater short-scale roughness. Fractional Brownian unit-increment covariance at lag $k$ is $\tfrac12[(k+1)^{2H}-2k^{2H}+(k-1)^{2H}]$. For $H<1/2$, it is negative with summable tails—not positive long memory in the same model. $H>1/2$ differs. See the empirical motivation in [Volatility is rough](https://arxiv.org/abs/1410.3394); fitted parameters on particular data are not universal asset constants.

**Method conclusion.** History-driven volatility can invalidate a simple finite-dimensional Markov PDE, but paths can still be simulated or approximated by augmented states. Simulation can accommodate non-Markovian histories through a specified numerical scheme. Improvement in the required surface/hedging task, computability, and verification guide added complexity.


#### Practical default — retain necessary contract state, then add volatility structure

For historical risk scaling, begin with a past-only realized-volatility estimator and a simple persistence/recursion forecast; compare them on the required horizon. For option valuation, begin with the specified constant-volatility model and a quote surface audit. Systematic strike/maturity residuals justify a smile-capable model; they do not identify its future dynamics by themselves. Select the smallest volatility structure that addresses the named pricing/hedging failure, and compare calibration and held-out hedging separately.

For path-dependent payoffs, explicitly augment state first: an Asian contract needs running sum/integral and elapsed observation count; a barrier needs hit status and its observation convention. Simulate or solve using this state. When order-sensitive whole-path information remains beyond these sufficient summaries, a truncated signature with a time coordinate is a candidate representation. Increase truncation by a fixed development comparison, since the dimension $\sum_{k=1}^m d^k$ quantifies its expression cost.

For a volatility-trading experiment, replay delta hedging with cash, discrete rebalance costs, changing gamma, jumps/stresses, and margin. Attribute outcome to the gamma-weighted variance difference and residual terms. Treat average IV–RV as a candidate explanatory feature, not the trade's P&L model. Added volatility tools are selected by their exposure span and residual reduction.

**Decision.** Preserve simple sufficient state whenever it exists; add stochastic/rough/path representation only for a demonstrated contract or risk gap. This sequence ties each model extension to a concrete development step and test.



#### Derivation checkpoints retained in the revised lecture

- Construct the centering projection $M=I-\mathbf1\mathbf1^\top/n$, its one removed direction and orthogonal Gaussian rotation; derive mean/variance of the $n-1$ squared coordinates before dividing. Average the variance recursion only under a stable finite moment.
- Subtract stock gain and consistent financing from actual-path Itô, then insert the model PDE to derive gamma-weighted variance P&L. This is a local financed excess-gain identity, not an unweighted IV–RV strategy return.
- Derive the Asian running-accumulator PDE term $SV_A$ and terminal payoff; discrete dates instead update sum/count. Calculate flat-extension and endpoint-bump functional derivatives before invoking functional Itô.
- Partition a two-segment signature's ordered time pairs into two triangles and one rectangle to derive $S^{ij}=a^ia^j/2+a^ib^j+b^ib^j/2$. For $0<H<1$ and large positive $k$, expand $f(k\pm1)=f(k)\pm f'(k)+f''(k)/2\pm f'''(k)/6+O(k^{2H-4})$. Adding gives the second difference $f''(k)+O(k^{2H-4})$, hence covariance $H(2H-1)k^{2H-2}+O(k^{2H-4})$. Integral comparison of power tails explains the below/above minus-one summability threshold. The functional Itô differential of quadratic variation is explicitly $d[X]$.

### Chapter 17 — Computation: from Monte Carlo to learned pricing and hedging

#### 17.1 A deterministic pricing map defines a computational learning task

**Motivation.** A large network can be inappropriate for weakly predictable returns yet useful for derivative computation. The different tasks share the same demand for appropriate evidence.

**Derivation.** Fix a model, its parameters, a contract, and the current conditioning state. Its theoretical price $V(x)$ is then a deterministic function of the inputs: its conditional variance is zero. Learning this map amortizes a costly computation; it does not recover tomorrow's random realized price. A ratio of continuous differential entropies would not establish “learnability equals one” for this task. Model misspecification, calibration uncertainty, numerical error, and future market randomness are different sources of error.

**Conclusion.** A learned surrogate is legitimate when the requested map is well defined, expensive, and repeatedly needed. Its numerical accuracy does not establish the truth of the underlying market model.

#### 17.2 Monte Carlo: sampling error is only one part of numerical error

**Construction.** Let independent discounted payoffs $Z_j$ have mean $V$ and finite variance. Their average $\widehat V_N=N^{-1}\sum_jZ_j$ is unbiased, with variance $\operatorname{Var}(Z)/N$. Standard error falls as $N^{-1/2}$: tenfold precision requires roughly a hundredfold path count at unchanged variance.

For a time-discretized model with price $V_h$, mean squared error is $(V_h-V)^2+\operatorname{Var}(Z_h)/N$. More paths do not remove time-discretization bias. A constant-parameter geometric-Brownian European terminal payoff can be sampled directly at maturity; it does not require an extremely fine grid. Path-dependent contracts may require fine observations or explicit treatment of crossings between observations.

If a correlated variable $C$ has known expectation, replace $Z$ by $Z-b(C-\mathbb EC)$. The variance becomes $\operatorname{Var}(Z)-2b\operatorname{Cov}(Z,C)+b^2\operatorname{Var}(C)$, minimized at $b^*=\operatorname{Cov}(Z,C)/\operatorname{Var}(C)$. Estimating $b$ from data requires its own bias and error checks.

**Conclusion.** Diagnose sampling variance, discretization, and model error separately. The elementary Monte Carlo rate is not an uncrossable lower bound for all variance-reduction or numerical methods.

#### 17.3 Let the map's structure determine representation and training coverage

**Derivation.** If the contract and model are homogeneous, $V(aS,aK)=aV(S,K)$ implies a representation $V=Kf(S/K,T-t,\ldots)$. This reduces redundant scale variation. Fixed currency costs and nonhomogeneous payoffs can invalidate it.

Training coverage includes maturity, moneyness, volatility, and important boundary/risk regions alongside common interior points, so evaluation exposes more than average error. Monte Carlo labels have sampling error; retain their standard errors rather than training a network to reproduce label noise. If gamma is required, a piecewise-linear ReLU surrogate can have zero second derivative inside each region despite small price errors. The derivative orders needed for the task guide activation and architecture.

**Conclusion.** Use the right structural restrictions, restrained capacity, and task-specific coverage. The earlier model-design principles continue to guide numerical pricing.

#### 17.4 Accurate prices do not imply accurate sensitivities

**Counterexample.** If $\widehat V(x)=V(x)+\epsilon\sin(kx)$, price error is at most $\epsilon$, but first-derivative error can be $\epsilon k$ and second-derivative error $\epsilon k^2$. Greeks are derivatives with respect to specified inputs, not generic measures of model confidence.

**Construction.** A joint loss can compare both values and derivative labels:

$$
J=\mathbb E\left[\left(\frac{\hat V-V}{s_V}\right)^2
+\sum_j\lambda_j\left(\frac{\partial_j\hat V-g_j}{s_j}\right)^2\right].
$$

Here $g_j$ is a derivative label from the same pricing model; $s_V,s_j$ are training scales; $\lambda_j$ controls the chosen error tradeoff. Units and scaling matter. Automatic differentiation computes the surrogate's derivatives, not a certificate that they equal the desired Greeks. Pathwise, finite-difference, and PDE-derived labels have different validity conditions and errors.

**Conclusion.** Evaluate prices, Greeks, boundaries, and complete hedging outcomes separately. Record how joint-loss weights were selected. See [Differential Machine Learning](https://arxiv.org/abs/2005.02347).

#### 17.5 PDE and no-arbitrage constraints describe the full pricing problem

**Motivation and construction.** With PDE residual $R_V$, a physics-informed loss may combine data error, $\mathbb E|R_{\widehat V}|^2$, terminal conditions, and boundary conditions. A zero function satisfies many homogeneous PDEs while failing a call's terminal payoff. The equation, domain, and terminal/boundary conditions jointly define the problem. See [Physics Informed Deep Learning (Part I)](https://arxiv.org/abs/1711.10561), the cited 2017 preprint. Check residual units, region coverage, and component weights; the model's PDE is not evidence that physical markets obey it.

For a no-dividend European call at fixed maturity, $(S_T-K)^+$ is decreasing and convex in strike $K$. Positive discounted risk-neutral expectation preserves those properties. Under matching assumptions, $\max(S-Ke^{-r\tau},0)\le C\le S$. Comparisons across maturity additionally depend on discounting, dividends, and contract terms; these assumptions determine whether a maturity-monotonicity restriction applies.

**Conclusion.** Positive output alone is not no-arbitrage: $\operatorname{softplus}(-S)$ is positive but decreases with the underlying, and strictly positive activations can fail a zero boundary. Use justified structural parameterizations and cross-contract tests. Penalties on finitely many sampled points do not prove a global constraint.

#### 17.6 Optimizer stability, map smoothness, and credible explanation are distinct

Gradient clipping bounds an update's gradient; it does not bound sensitivity to input. A network Lipschitz bound involves products of layer constants and weight operator norms, $\prod_jL_j\|W_j\|_{\mathrm{op}}$. Weight control is a separate operation. [Muon](https://github.com/KellerJordan/Muon) approximately orthogonalizes matrix updates; it does not thereby project the weights onto an orthogonal set. Optimizer geometry alone proves neither accurate Greeks nor a pricing function's Lipschitz constant.

Sparse autoencoders or language-model descriptions of internal features generate explanatory hypotheses. Test these with perturbations, ablations, local derivatives, and contract constraints. A readable label is not a faithful causal explanation; excessive sparsity can erase weak distributed signals, as in Chapter 5.

**Conclusion.** Assign each tool its actual responsibility. Evaluate fitting, explanation, and output constraints with the checks appropriate to each. Claims that Thales universally outperforms numerical alternatives remain unverified without a model card, comparable benchmarks, and accessible data.

#### 17.7 Amortization determines the value of fast inference

**Derivation.** Let offline data generation, training, and maintenance cost $C_o$; surrogate cost per call be $C_s$; reference cost per call be $C_r>C_s$. For $N$ calls, the surrogate is cheaper when $C_o+NC_s<NC_r$, or $N>C_o/(C_r-C_s)$. Updates, coverage expansion, and fallback calls change this threshold.

**Conclusion.** Compare the same products, error tolerances, input coverage, hardware, and batch conditions, including total lifecycle cost. Throughput is not single-request latency. Task frequency and workload determine GPU suitability.

#### 17.8 Deep hedging: optimize an implementable policy against a specified risk

**Construction.** For a discretely hedged short claim $H$, write discounted terminal hedging error as

$$
E_T=v_0+\sum_{k=0}^{m-1}q_k(\tilde S_{k+1}-\tilde S_k)
-C(q)-\tilde H.
$$

Positions $q_k$ must use only information available then. Costs $C$ must use matching units; tildes denote discounted quantities. With trading costs, previous holdings $q_{k-1}$ are part of the state—current price alone is insufficient. Under frictionless exact replication the residual can vanish; under frictions and restricted instruments the task becomes risk minimization.

For integrable loss $L=-E_T$ and $\alpha\in(0,1)$, define

$$
\mathrm{CVaR}_\alpha(L)=\min_z\left[z+
\frac{\mathbb E(L-z)_+}{1-\alpha}\right].
$$

For a continuous loss distribution, differentiating the objective in $z$ gives $1-\Pr(L>z)/(1-\alpha)$; a minimizer is an $\alpha$-quantile. At atoms, use one-sided derivatives. This objective addresses adverse-tail losses alongside the volatility comparison. Minimizing variance alone ignores the mean, so fix pricing and expected-outcome conventions. Risk acceptance or indifference pricing requires comparison with the corresponding baseline without the short claim.

**Conclusion.** Convexity of a risk measure in loss does not make neural-policy optimization convex or guarantee a global optimum. Distinguish physical-measure risk simulation from risk-neutral valuation simulation. Validate complete paths and stresses when distributions, frictions, or constraints change. See [Deep Hedging](https://arxiv.org/abs/1802.03042).

---

#### Practical default — a validated numerical oracle, then an amortized surrogate

1. Fix contract, model, parameters/state domain, discounting, required prices/Greeks, and tolerances. Use a closed form when it covers the task, a tree/PDE for suitable low-dimensional state, or Monte Carlo with explicit path/observation rules otherwise. Benchmark plain European values before exotic claims.
2. Produce reference labels with separate sampling and discretization error budgets. Under independent finite-variance sampling, a normal-approximation half-width $\varepsilon$ at multiplier $z$ suggests $N\approx z^2\operatorname{Var}(Z)/\varepsilon^2$ after a pilot variance estimate. Check approximation conditions and use grid/path refinement separately. Introduce control variates before merely multiplying paths.
3. Sample a declared input domain including boundary and risk-sensitive regions. Apply justified homogeneity scaling. Use a small smooth surrogate when derivatives are required, with price and derivative supervision scaled by their operational tolerances. Include gamma supervision or an explicit gamma assessment if gamma is a consumer; first derivatives alone do not control second derivatives.
4. Keep data, PDE residual, terminal, boundary, and contract-shape checks distinct. Begin with reliable supervised labels and boundary/shape validation; a specified numerical use motivates a PDE residual term, whose incremental benefit is then tested. Softplus positivity or gradient clipping is not the no-arbitrage construction.
5. Gate use by held-out price/Greek errors across the full domain, constraint checks, and matched hedge outcomes. Inputs outside confirmed coverage or failed checks fall back to the reference method. Compare total generation/training/maintenance/fallback cost with $C_o+NC_s<NC_r$ before claiming an engineering advantage.

For friction-aware hedging, begin with the reference discrete delta policy, then compare a small policy taking current model state and previous holdings. Hold price, information, costs, risk measure, and simulation scope fixed; optimize the terminal-loss criterion and test entire held-out/stressed paths. Confirmed residual-risk/net-cost improvement supports policy adoption, with training loss interpreted as one development measure.

**Selected conclusion.** Numerical learning replaces repeated expensive computation inside a checked model/domain. The default is oracle → tolerance-aware data → smooth supervised surrogate → value/derivative/constraint/hedge gates → fallback and lifecycle-cost comparison. The Thales account motivates these questions, and the reproducible route supplies the evidence needed to assess them.



#### Derivation checkpoints retained in the revised lecture

- Expand Monte Carlo bias plus centered sampling error and remove the mixed term by its zero mean. Derive the control coefficient from the variance quadratic; independent antithetic units are pair averages, with variance $v(1+\rho)/2$.
- Retain normalized-unit delta/gamma chain rules. Derive the per-path call delta from $S_T=S_0M$ and its integrable difference-quotient domination. Explain why the exercise-boundary mass makes the naive almost-everywhere zero gamma wrong. Derive central-difference truncation and independent-noise amplification separately.
- For CVaR, differentiate the hinge, then use left/right slopes at atoms to obtain $\Pr(L>z)\le1-\alpha\le\Pr(L\ge z)$. Derive tail-mean cancellation and fractional threshold mass; show translation with $y=z+p$ and risk-indifference premium $R_H-R_0$.
- Retain the concrete 20,000/2,000/2,000 pricing pilot, smooth 2×64 model, learning-rate/budget convention, value/Greek/shape/fallback gates, lifecycle amortization, and distinct stateful friction-aware 2×32 hedge comparison. These are inspectable initial specifications, not trained-model or market-performance reports.

## Three practical cases: make the design decisions explicit

These cases turn the supplied methodology into concrete teaching designs, explaining the choices and research order. Reproducing the author's equity curves and establishing empirical performance require their own data and validation.

### Case A — Shanghai copper timing

**Selected design.** Use actual contracts and point-in-time observations, volatility-scaled triple-barrier outcomes, and interpretable price/volume, multiscale momentum/deviation, term-structure, and open-interest features. Start with shallow, regularized, early-stopped trees mapping factors to direction or first-passage probabilities. Keep a small participation gate and independently specified risk sizing.

**Why.** Limited time-series breadth and thin signals constrain the capacity that data can support. Multihorizon features first supply memory to stateless models, while term-structure and related observations enrich the futures state. Each tree partition consumes statistical freedom, giving shallow structure and regularization a clear role. Fixing direction before learning a gate also reduces the choices searched. Barriers connect the labels to an exit policy.

**Implementation order.** Define contract, timestamps, exits, and costs; build point-in-time labels and features; freeze evaluation windows, model, and gate; purge temporal overlaps; confirm executable fills, rolls, costs, and cash paths. Changes to models or labels call for reevaluation of the affected chain. Unknown intrabar trigger order is resolved through additional observations or an explicit handling rule, giving the exit policy a reconstructible event sequence.

**Decision.** Improve the target, observed state, and verification first. Model upgrades address an identified and confirmed representation gap, giving extra capacity a specific purpose.

### Case B — Cross-sectional index enhancement

**Selected design.** Use a historical investable universe and benchmark-relative future ranks. Keep linear/tree baselines with explicit cross-sectional context. The principal relational model is shallow, narrow set attention without positional encoding, producing per-asset scores and using rank/IC-aligned loss. Convert scores into benchmark deviations under industry, size, unsupported-exposure, and turnover constraints.

**Why.** The task depends on relative comparisons, while arbitrary input row order has no economic meaning. Attention supplies a comparison mechanism, and permutation symmetry incorporates this freedom directly into the architecture. More assets offer more opportunities, with common shocks limiting the growth of independent information. Ranking and IC evaluate relative predictions; the portfolio layer evaluates investable performance under risk and cost constraints.

**Decision.** Start with relative ranks and restrained set-based structure, retaining tree baselines that encode cross-sectional context. Split by date and compare models, losses, and net benchmark-relative performance on a common confirmation set. These comparisons determine the incremental value of architecture and depth.

### Case C — Multi-asset allocation

**Selected design.** Keep equal weight as a reference and build the base allocation from stable covariance estimates and risk budgets/ERC. Choose assets for representative economic risk coverage across environments. Macro or trend tilts form a separate prediction layer, added after independent confirmation of their incremental contribution and bounded so the base risk budget remains dominant.

**Why.** Inverse covariance amplifies unreliable expected-return estimates. Removing $\mu$ reduces dependence on that fragile estimate. Capital weights and risk contributions measure different quantities, as do asset risk budgets and macro-scenario exposures. The coverage offered by four asset classes is therefore assessed through actual exposures and scenario analysis.

**Decision.** Start with risk budgets when expected returns lack independent support, and add predictive tilts after incremental confirmation. Covariance stress, leverage, liquidity, cash needs, and gap tests establish the implementation and survival conditions for this selected route.

## Synthesis: an eight-stage research-to-execution chain

| Stage | Selected decision | Why it follows |
|---|---|---|
| 1. Define the problem | Specify the economic source of returns, opportunities, and constraints before choosing a network | The action determines the relevant outcome and available breadth |
| 2. Design the target | Choose direction, first passage, or relative rank for the task, removing irrelevant price detail | Remove irrelevant distinctions while retaining participation and payoff information where needed |
| 3. Establish data and infrastructure | Correct objects and availability times; reconstruct cash before optimizing throughput | Wrong observations invalidate every downstream score |
| 4. Engineer features | Represent economic state, memory, and relations; distinguish new observation from accessible representation | This is the principal route to additional or more usable information |
| 5. Verify | Separate search from confirmation and retain the complete selection history | Noise extremes and repeated selection change what a score means |
| 6. Aggregate and model | Combine factors conservatively, handle adaptation explicitly, and add structure to meet representation needs | Assess the roles and costs of representation complexity and drift adaptation separately |
| 7. Construct the portfolio | Bet on supported directions, constrain unsupported risks; use risk budgets without a mean edge | Realization depends on inverse-estimation error and implementation constraints |
| 8. Implement and monitor | Evaluate costs, cash paths, failures, and the incremental value of changes | Fills and financing have their own conditions, and evidence can expire as environments change |

**The research order running through the book.** Determine what the decision needs to estimate, then assess the precision the evidence can support. Remove irrelevant detail, constrain dimensions without an edge, and combine refined signals conservatively. Work through target design, representation, independent confirmation, remaining model gaps, and realization through portfolios and execution. A bottleneck in representation or optimization sends research back to that stage with a specific problem to resolve.

Chapters 1–2 establish prediction boundaries and reconstruction of the problem; Chapters 3–5 construct labels and representations; Chapters 6–9 govern learning, search, and aggregation; Chapters 10–14 cover portfolios and arbitrage. Chapters 15–17 develop a different pricing-and-hedging line: sensitivities and numerical values are genuinely required there. Directional coarse-graining serves a particular decision task; pricing and hedging retain the numerical precision they require.

## Source-coverage audit

The table locates the methodology from the seven attachments and additional conversation material. Empirical performance in those sources is evaluated through its own data and tests.

| Supplied material | Main locations | Principles retained |
|---|---|---|
| Foreword and prediction boundaries | Ch. 1: observation and prediction boundaries; Ch. 2: targets and usable information | Observation loss, signal/noise, information versus capacity, coarse-grained targets, feature engineering |
| First practical strategy | Ch. 3: policy labels/gates; Ch. 5: market state; Chs. 6–7: models/optimization; Chs. 10–11: holdings/execution | Policy-aligned labels, market state and multiscale memory, weak model design, learning-rate distinctions, meta-labeling, executable constraints |
| Genetic programming and factor factory | Ch. 7: search feedback; Ch. 8: admission pipeline; Ch. 4: data; Ch. 12: lifecycle | Oracle order, zero-/first-order search, factor-tree complexity, multiple testing, honest infrastructure, lifecycle controls |
| Markowitz and allocation | Ch. 10: estimation error/ERC/macro coverage; Ch. 11: cash/funding; allocation case | Estimation-error amplification, covariance stabilization, risk budgets, ERC, macro coverage without unsupported forecasts |
| Arbitrage | Ch. 13: statistical relations; Ch. 14: event/cross-market cash flows; Ch. 11: execution/survival | Relations rather than outright direction, convergence versus risk, execution/infrastructure, liquidity and institutional constraints |
| Derivative-pricing theory | Ch. 15: replication/pricing law; Ch. 16: volatility/paths; Ch. 17: friction-aware hedging | Replication, pricing measure, PDE assumptions, path representation, roughness, friction-aware hedging |
| Numerical pricing and Thales | Ch. 5: reconstruction/low-rank limits; Ch. 17: numerical learning/amortization | Low-rank/sparsity limits, deterministic map versus forecasting, Monte Carlo, derivative losses, PDE/no-arbitrage constraints, optimizer limits, amortization |
| Pasted feature/label/optimization discussion | Ch. 2: learnability/coarse-graining; Ch. 3: policy labels; Ch. 7: feedback/noise | Learnability, usable information, directional coarse-graining, labeling policy, feedback efficiency and noisy optimization |
| Pasted aggregation, cross-section, and summary | Ch. 6: cross-sectional structure/loss; Ch. 9: regret/adaptation; Chs. 8–12; eight-stage synthesis | Relative structure, capacity restraint, expert regret versus adaptation, target-aligned loss, complete development chain |

## Practical-design audit: what this revision repairs

The v0.4 outline already contained many selected conclusions. The recurring defect was the missing bridge from a conclusion to the reader's first experiment. The integrated defaults connect supporting derivations to experiments the reader can begin.

| Chapter | Construction previously absent or under-specified | Selected first route now supplied |
|---|---|---|
| 1 | Boundary results outweighed a concrete alternative in the lecture | Binary probability target, information-retention comparison, and a complete first experiment |
| 2 | A target choice needed a usable decision interface | Binary log loss, payoff-derived long/short/abstain bands, and scoped numerical supplements |
| 3 | Barrier/gate concepts needed a frozen initial policy | Volatility-scale convention, observation/exit labels, mature intervals, three-class score, and an out-of-sample primary/gate comparison |
| 4 | Timing prohibitions needed an actual admissible data view | Availability/version schema, as-of query, historical universe, cash mapping, and temporal fixtures |
| 5 | Feature usefulness needed a first panel and upgrade order | Multiscale bar/contract state, task-specific normalization, nested feature comparisons, and simple tick summaries first |
| 6 | Model families and parameter roles lacked a reproducible initial experiment | Explicit logistic baseline; shallow-tree/gate and small set-attention prototypes; chosen probability/ranking objectives |
| 7 | Stability/noise arguments ended without step/search selection | Typed bounded GP, measured generator upgrade, curvature/backtracking steps, finite neural-rate pilot, and failure-specific interventions |
| 8 | Verification tools needed a complete admission process | Immutable inputs, development scorer, frozen confirmation, joint admission decision, dossier, and measured infrastructure growth |
| 9 | Regret did not fully specify the consumed forecast or adaptation | Probability mixture with bounded Brier loss, log-space updates, feedback clock, explicit rate, fixed-share comparison, and action mapping |
| 10 | Risk concepts needed an actual score-to-holding route | Inverse-volatility timing; constrained active-score objective; covariance-stabilized risk-budget allocation |
| 11 | Execution caveats needed the first replay and scaling test | Next-feasible-entry ledger, accounting fixtures, capacity ladder, and explicit partial-fill/funding responses |
| 12 | “Monitor and retire” needed distinct operations | Experiment manifests; suspend, investigate, retire, shadow, and reconfirm stages |
| 13 | Reversion concepts needed a stateful entry/exit strategy | Related-pair development, frozen residual model, hysteresis, convergence-versus-cost participation, and funding limits |
| 14 | Arbitrage categories needed task-specific pipelines | Event dossier → calibrated states → payoff threshold; executable cash-flow checks and joint funding ledgers |
| 15 | Pricing distinctions needed a practical starting engine | One-step replication, backward induction, closed-form benchmark, and value/Greek refinement |
| 16 | Advanced representations lacked a clear model-development order | Simple volatility/state summaries first, observed pricing/hedging gap next, controlled path augmentation only when needed |
| 17 | Corrective constraints needed a coherent numerical-learning route | Reference oracle → error-budgeted labels → smooth supervised surrogate → complete gates → fallback and amortization |

The chapter defaults apply the derivations to specific tasks. The main text develops these constructions concept by concept, with appendices supplying further detail. Later additions retain that path from concept to practice. The choices rest on the arguments developed here; actual performance awaits testing.

## Keep seven meanings of “information” separate

1. **Market information $I(X;Y)$.** Determined by specified observations, target, and joint distribution. Converting a measured IC to bits requires corresponding distributional and model assumptions.
2. **Usable information $I_{\mathcal V}$.** Relative to a predictor family, loss, and representation. Changing the family can change it, and the trained function may fall short of the family's attainable performance. Both data and predictor family belong to its interpretation.
3. **Statistical information from finite evidence.** Estimation bias, selection, and confirmation determine what can be established. A population relation passes through finite-sample estimation and confirmation before becoming reliable evidence.
4. **Optimization feedback.** Function values, gradients, and curvature give directions for search. Their precision and noise describe scoring or updating; predictability of future market outcomes concerns the observation–target relation.
5. **The $\log K$ cost of alternatives.** Noise extremes in selection and expert regret involve related choice costs under different assumptions. The bounds have similar forms, with each conclusion resting on its own assumptions and derivation.
6. **Relative entropy $D(P\Vert Q)$.** A likelihood-based discrepancy between distributions, with different comparison objects from observation–target mutual information.
7. **Determinacy of a fixed numerical map.** Conditional on a complete model, a pricing map is deterministic. Model and calibration error can coexist with that fact; computation remains subject to verification.

## Parameter design: what each control changes

| Parameters | Design responsibility | Basic derivation and consequence | Locations |
|---|---|---|---|
| Label horizon, barriers, event triggers | Specify the action/exit policy | First passage, volatility scaling, $p_+G-p_-L$, and overlapping outcomes tie labels to realized economics | Chapter 3 |
| Feature windows, standardization, neutralization | Represent state and comparable units | Multiscale snapshots preserve useful memory; common units cancel; projections remove specified exposures | Chapter 5 |
| Model structure and context | Encode relevant symmetry and dependence | Permutation equivariance, path ordering, and required derivative orders determine the representation | Ch. 6: structure/attention; Ch. 16: path state; Ch. 17: sensitivities |
| Depth, width, rank, trees, regularization | Limit statistical/search freedom | Finite-candidate bounds, eigenvalue shrinkage, rank parameter counts, and soft thresholding explain distinct controls | Ch. 5: reconstruction; Ch. 6: capacity |
| Gradient step $\alpha$, batch size $B$ | Balance stability, speed, and gradient noise | Quadratic curvature and gradient covariance explain step restrictions and variance reduction | Ch. 7: curvature, noise, and pilots |
| Boosting rate $\nu$ | Control each added learner's contribution | $F_m=F_{m-1}+\nu h_m$ couples rate to rounds and stopping; its object differs from that of a gradient step | Ch. 6: shallow boosting |
| Expert rate $\eta$, forgetting, sharing | Balance concentration, regret, and adaptation | Bounded-loss regret controls comparison with a fixed expert; forgetting/sharing changes recovery and the comparator | Ch. 9: regret, mixtures, and drift |
| Portfolio penalties, exposure and turnover limits | Prevent unsupported estimation bets and costly reallocations | Inverse-matrix perturbation, risk budgets, and net costs identify what the constraints protect | Chapters 10–11 |
| Surrogate weights, coverage, precision | Align values, Greeks, constraints, and lifecycle cost | Units, the oscillatory-error counterexample, PDE boundaries, and amortization determine evaluation | Chapter 17 |

The chapter defaults provide explicit starting values and bounded selection procedures for reproducible experiments. $\alpha$, $\nu$, and $\eta$ act on different objects, with different units and theoretical justifications. Their values follow separate analyses of curvature, noise, or loss properties.

## Current revision and later work

1. The seventeen-chapter lecture and paired outlines form the current complete edition in both languages. This prose revision improves organization and transitions while retaining the developed arguments and practical routes.
2. The derivation audit checks symbol definitions, conditioning and availability, intermediate algebra, units, limiting/theorem conditions, and the exact consequence of each important formula. Both language editions present the formulas, arguments, and evidence scope in full.
3. Professional external sources retain their identities and links. Product and rule illustrations keep their original observation cutoff; a new experiment checks the rules and service terms then in effect. This prose revision retains the existing source coverage.
4. Empirical reproduction remains separate. It needs admitted historical data, actual contract and rule versions, a frozen protocol, and independently checked results. Lecture examples provide starting constructions and intuition; the reproduction process establishes actual performance.
5. Derive skills once the exposition has stabilized, preserving decisive judgments, information timing, operational conventions, validation, and failure conditions. Identify teaching hyperparameters and local tools with their specific experiments and environments.

**Current scope.** Revise and synchronize the prose of both outlines and lectures. Skill extraction, empirical reproduction, live operations, and ongoing monitoring remain separate work.
