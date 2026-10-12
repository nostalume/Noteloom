// Single-file English lecture; complete seventeen-chapter revised edition.
// Compile from the scrawl root with --root .
#import "../manus/daily-en.typ": daily-en

#show: daily-en.with(
  title: [Quantitative Finance],
  normal-size: 11pt,
  script-size: 9pt,
  margin: (top: 23mm, bottom: 23mm, left: 25mm, right: 25mm),
  head-numbering: "1.1",
  head1-size: 16pt,
)
#set text(font: "Libertinus Serif")
#show heading: set text(hyphenate: false)
#set par(leading: 0.65em, spacing: 0.7em, first-line-indent: 0pt)
#set table(inset: 7pt, stroke: 0.4pt + luma(75%))
#let E = math.op("E")
#let Pr = math.op("Pr")
#let Var = math.op("Var")
#let Cov = math.op("Cov")
#let sign = math.op("sign")
#let argmax = math.op("arg max")
#let diag = math.op("diag")
#let IC = math.op("IC")
#let principle(body) = block(
  width: 100%, inset: 10pt,
  fill: luma(96%), stroke: (left: 2pt + luma(40%)),
  breakable: false,
)[#set par(first-line-indent: 0pt)
  #body
]

= Prediction Boundaries: Why a Larger Model Cannot Supply Missing Information
#counter(math.equation).update(0)

Suppose you have a history of prices and want to train a model to predict tomorrow. Your first question might be whether to use linear regression, a tree model, or a larger neural network. This chapter postpones that choice. We first ask: *What about tomorrow is worth predicting? Which observations available today can help? And what part of the error cannot be removed by even the strongest algorithm?*

These boundaries help us direct research toward the parts of prediction we can improve. We begin with trading cash flows and a simple forecast baseline, then build tools for measuring predictive ability. Conditional expectation, entropy, and mutual information enter as the problem develops, allowing readers to proceed from basic probability.

The numerical examples in this chapter are teaching constructions; assessing a live strategy would require separate market evidence. Explanations of market mechanisms are hypotheses for subsequent verification. Probabilistic and error-related conclusions come with explicit assumptions and derivations.

== Start with a Price Curve That Looks “Accurate”

=== Staying close to the price is not knowing its next move

Today's price is 100. Tomorrow it may be 101 or 99. A predictor that studies nothing about the future can simply report “tomorrow's price will still be 100,” missing by only one unit. On a sufficiently wide vertical axis, its predicted curve will almost coincide with the observed one.

Write the problem more precisely. Let $P_(t)$ be the price known at time $t$, and let $Delta P_(t+1)=P_(t+1)-P_(t)$ be the next-period increment. Compare two predictors:

$
  hat(P)_(t+1)^((0)) = P_(t), quad
  hat(P)_(t+1)^((1)) = P_(t) + hat(Delta P)_(t+1).
$

The first is a *no-change forecast*: it carries today's price forward. The second attempts to predict the new increment. Their squared price errors are respectively

$
  (P_(t+1)-hat(P)_(t+1)^((0)))^(2) = (Delta P_(t+1))^(2),
  \
  (P_(t+1)-hat(P)_(t+1)^((1)))^(2)
    = (Delta P_(t+1)-hat(Delta P)_(t+1))^(2).
$

The second model adds value by improving on the no-change forecast for the unknown increment. Resemblance between the plotted price curves provides little help in judging that improvement. When a single-period change is small relative to the price level, both curves may look very accurate.

A simple example makes the distinction clearer. Each day's increment independently takes the value $+1$ or $-1$, with equal probabilities. Starting at 100, the price accumulates these increments. Today's price contains the sum of past increments, but no information about tomorrow's independently drawn sign. The no-change forecast misses by only one unit each day, yet no direction predictor using only the past can achieve average accuracy above one half. *Small price error and an advantage in predicting future direction are different things.*

Conversely, a signal available at the decision time may help predict the conditional average of tomorrow's increment. Its forecast curve might move only slightly away from the no-change curve. That difference may be hard to see but still represent a genuine additional judgment. Evaluate both on the same temporal split, target, and cost assumptions. The baseline makes this comparison interpretable across model choices.

=== Write down what you actually receive

Temporarily ignore financing, dividends, and contract multipliers. You hold $q_(t)$ units of an asset at time $t$, close the position at $t+h$, and incur total cost $C_(t,t+h)$. Your cash profit and loss is

$
  Pi_(t,t+h)=q_(t) (P_(t+h)-P_(t))-C_(t,t+h).
$

A positive $q_(t)$ is a long position; a negative $q_(t)$ is a short position. The current price is already a known entry condition. The change relative to that price enters the position's profit and loss. Actual contracts require additional cash flows and multipliers, but this simplified expression already establishes the research target: *prediction serves the consequences of an action.*

Keep four quantities distinct:

#table(
  columns: (1fr, 1.65fr, 2.1fr),
  table.header([Object], [Definition], [Question answered]),
  [Price level], [$P_(t)$], [What is one unit worth now?],
  [Price increment], [$Delta P=P_(t+h)-P_(t)$], [How much does one unit gain or lose before costs?],
  [Simple return], [$r=(P_(t+h)-P_(t))/P_(t)$], [What is the change relative to the entry price?],
  [Log return], [$ell=ln(P_(t+h)/P_(t))$], [How can price ratios be recorded additively across periods?],
)

Simple return satisfies $P_(t+h)=P_(t) (1+r)$. For positive prices, log return is $ell=ln(1+r)$. The first-order expansion of the logarithm gives $ell approx r$ when $r$ is small. Log returns add because taking the logarithm of multiplied price ratios turns multiplication into addition. For example, a rise from 100 to 110 followed by a fall back to 100 has total log return zero. The simple returns are $10\%$ and approximately $-9.09\%$; adding them does not give the total return. Log return gives us a convenient representation; cash accounting still follows the actual holding and its payments.

Next ask along which dimension results are compared:

- *Timing:* For one asset, decide when to hold, exit, or reverse a position. Comparisons primarily run through time.
- *Cross-section:* At one decision time, compare multiple assets to determine relative strength and form overweights and underweights. Comparisons primarily run across assets.
- *Event task:* Around a predefined event or trigger, evaluate subsequent paths and action outcomes. The sample unit is an event, not automatically a trading day.

These tasks need not use the same label. A correctly ranked cross-section can still produce a losing long portfolio when the whole market falls. Correct direction can still lose money when losses are too large. In these notes, “alpha” means excess performance relative to an explicit benchmark and specified risk explanation; its meaning therefore depends on the comparison being made.

#principle[*Design decision:* Construct the prediction target from the economic action before comparing models. The trend direction layer does not default to predicting an exact future price. It prioritizes direction or the outcome of a specified exit policy. Retain cheap baselines, such as no change or a historical average, because they reveal what the model actually adds.]

== Why an Observation Cannot Reconstruct the Entire Market

=== An ambiguity no algorithm can resolve

Markets contain states you cannot directly see: demand, inventories, position constraints, and participants' intentions. Denote the complete state relevant to the discussion by $S$, and the observation you actually receive by $X=g(S)$. Here $g$ describes how observations are produced; the prediction model acts on the resulting input.

A small mathematical example shows what losing a distinction means. The state has two components, $S=(u,v)$. You observe only their sum, $X=u+v$, but want to predict their difference, $Y=u-v$. Consider two possible states:

#table(
  columns: (1fr, 1fr, 1fr),
  table.header([Complete state $S$], [Observation $X$], [Target $Y$]),
  [$(1,0)$], [$1$], [$+1$],
  [$(0,1)$], [$1$], [$-1$],
)

An algorithm receiving only $X$ sees the same input in both cases. It cannot output $+1$ for input 1 in one case and $-1$ for that same input in the other while knowing which case occurred. Its own random numbers do not reveal the hidden state. If the states are equally probable, its best direction accuracy remains one half.

This is *non-identifiability*: the observation merges a distinction needed by the target. There are two repairs. Add an observation, such as $A=u$, and recover $v=X-A$; or change the target to $u+v$, which the existing observation already determines. Expanding a network from two layers to two hundred does not change the ambiguity.

Non-identifiability is always *relative to a target*. Failure to reconstruct $(u,v)$ does not prevent exact knowledge of $u+v$. Likewise, prices failing to retain the entire market state does not imply that price history is useless for every future outcome. Trades, order books, and financial statements are different observations. “The market hashes everything away” can be a metaphor, but cannot replace an unpredictability proof with specified inputs and targets.

We still need a measuring instrument. Prediction is rarely a choice between complete knowledge and none: an observation might raise the probability of an increase from 50% to 60%. How can we measure that partial help?

=== Construct an information measure from probability forecasts

First suppose the target $Y$ has finitely many possible values. A predictor can output probabilities $q(y)$ rather than a single assertion, with $q(y)>=0$ and $sum_(y) q(y)=1$. When outcome $y$ occurs, evaluate it using

$ L(q,y)=-log_(2) q(y) $

This is *log loss*. Why a logarithm? If outcomes are independent under the forecast, their joint probability is a product. Taking negative logarithms makes the losses additive. Assigning an extremely small probability to an outcome that occurs receives a large penalty. Assigning probability one to a certain outcome gives zero loss.

With base 2, the unit is called a *bit*. A fair binary outcome has probability $1/2$ for either result and loss 1. Four equally probable results each give loss 2. This specifies the measure's unit; it does not mean an outcome is literally stored in a particular computer bit.

Let the true probabilities be $p(y)$. The long-run average loss is the probability-weighted sum

$
 E[L(q,Y)] = -sum_(y) p(y) log_(2) q(y).
$

Add and subtract $log_(2) p(y)$ inside each logarithmic term:

$
 E[L(q,Y)]
 = underbrace(-sum_(y) p(y) log_(2) p(y), H(Y))
 + underbrace(sum_(y) p(y) log_(2) (p(y)/q(y)), D(p upright(||) q)).
$

$H(Y)$ is *entropy*: the average log loss that remains even when forecasting with the true distribution. $D(p upright(||) q)$ is *relative entropy*, or KL divergence: the additional loss from using $q$ instead of $p$. It is asymmetric, so it is not a distance in the ordinary geometric sense.

The claim that true probabilities are optimal rests on the nonnegativity of this additional loss. We can establish it with a short calculus argument. First suppose the relevant probabilities are positive. Calculus gives $ln a<=a-1$: the function $a-1-ln a$ has minimum zero at $a=1$. Substitute $a=q(y)/p(y)$, multiply by $p(y)$, and sum:

$
 sum_(y) p(y) ln (q(y)/p(y))
 <= sum_(y) (q(y)-p(y))=0.
$

Reverse the sign and divide by $ln 2>0$ to obtain $D(p upright(||) q)>=0$. When $p(y)=0$, its weighted contribution is defined as zero. When $p(y)>0$ but $q(y)=0$, the additional loss is infinite. If $q$ assigns probability outside the true support—the outcomes with positive $p$—the upper bound obtained by summing on that support only becomes smaller. The conclusion still holds.

We have proved an important fact: *the optimal average log loss is $H(Y)$, attained by forecasting the true probabilities on their support.* Entropy is neither parameter count nor tradable profit. It measures the uncertainty that this target requires us to distinguish under the specified probability distribution.

=== How much uncertainty does an observation remove?

After observing $X=x$, use conditional probabilities. Their meaning comes from recomputing outcome frequencies among the cases where $X=x$. For discrete variables,

$
 p(y mid(|) x) = (Pr(X=x,Y=y))/(Pr(X=x)), quad Pr(X=x)>0.
$

Calculate entropy for each observation, then average according to how often that observation occurs. This defines *conditional entropy*:

$
 H(Y mid(|) X)
 = sum_(x) p(x) [-sum_(y) p(y mid(|) x) log_(2) p(y mid(|) x)].
$

It is the average loss remaining when we first see the observation and then use the optimal probability forecast. Without the observation, the loss is $H(Y)$; with it, the loss is $H(Y mid(|) X)$. Their difference defines *mutual information*:

$ I(X;Y)=H(Y)-H(Y mid(|) X). $

The expansion matters because it explains why the difference cannot be negative. Rewrite the marginal entropy using $p(y)=sum_(x) p(x)p(y mid(|) x)$, then subtract conditional entropy term by term:

$
 H(Y)=-sum_(x) sum_(y) p(x)p(y mid(|) x)log_(2) p(y),
 \
 H(Y)-H(Y mid(|) X)
 =sum_(x) sum_(y) p(x)p(y mid(|) x)
 [log_(2) p(y mid(|) x)-log_(2) p(y)].
$

Combining the logarithms into a ratio gives

$
 I(X;Y)=sum_(x) p(x) D(p(dot mid(|) x) upright(||) p(dot))>=0.
$

Here $p(dot mid(|) x)$ is the entire set of target probabilities given $x$, and $p(dot)$ is the set before observing it. Mutual information is therefore the *improvement in optimal average log loss provided by the observation*. Its nonnegativity follows from the divergence result just proved.

Consider a fully reproducible example. The target $Y$ is up or down, and the signal $X$ is positive or negative. Their joint probabilities are

#table(
  columns: (1fr, 1fr, 1fr, 1fr),
  table.header([Joint probability], [Up], [Down], [Total]),
  [Positive signal], [$0.30$], [$0.20$], [$0.50$],
  [Negative signal], [$0.20$], [$0.30$], [$0.50$],
  [Total], [$0.50$], [$0.50$], [$1.00$],
)

Without the signal, up and down are equally probable, so $H(Y)=1$. With a positive signal, the probability of up is $0.30/0.50=0.60$; with a negative signal, the probability of down is 0.60. Both observations have the same conditional entropy:

$ -0.6 log_(2) 0.6-0.4 log_(2) 0.4 approx 0.97095. $

Thus $I(X;Y) approx 0.02905$ bits. The signal does not identify every outcome, but does remove a little uncertainty. This number belongs to the stipulated joint distribution. Estimating it from finite market data requires additional statistical methods; a training-set loss reduction is not automatically true mutual information.

=== Why transformations and larger models cannot create information

Let a feature $F=g(X)$ be a deterministic transformation of the original observation. Any predictor using $F$ can be simulated by a predictor possessing the full $X$: first compute $g(X)$, then make exactly the same prediction. Consequently, the optimal loss with the complete input cannot exceed the optimal loss with only its summary:

$
 H(Y mid(|) X)<=H(Y mid(|) F), quad
 I(F;Y)<=I(X;Y).
$

This is the *data processing inequality* needed here. If the observation itself is a deterministic transformation of state, $X=g_(0) (S)$, the full state can likewise simulate any observation-based predictor:

$ I(F;Y)<=I(X;Y)<=I(S;Y). $

The observation and transformation relations are what make the argument work. Randomized processing extends the result under appropriate conditional-independence assumptions; the deterministic case is sufficient for the present discussion.

None of this dismisses feature engineering. “Optimal” above allows an unlimited predictor to perform every required calculation; actual models lack that ability. Moving information into a form a finite model can use may substantially improve practical prediction, without adding information absent from the original observation. Chapter 2 constructs that distinction explicitly.

#principle[*Design decision:* When observations have lost a required distinction, add observations or change the target; changing only the network cannot recover it. Deterministic feature transformations cannot increase Shannon mutual information, but can change how difficult information is for a finite model to use. Discuss those two claims separately.]

== Three Boundaries Within Prediction Error

=== Why the average is the right answer under squared loss

The preceding section forecast probabilities. If a model must output one number and is evaluated by squared loss, what number should it choose? Assume $E[Y^(2)]<infinity$, a finite second moment. Fix an observation $x$ and denote the target's average given that observation by

$ m(x)=E[Y mid(|) X=x]=sum_(y) y p(y mid(|) x). $

This is *conditional expectation*: an average weighted by the probabilities after observation. For a continuous target, replace the sum with a density integral. It describes an average across possible future realizations.

The error of any forecast $f(x)$ can be split into two parts:

$ Y-f(X)=[Y-m(X)]+[m(X)-f(X)]. $

Squaring gives two squared terms and a cross term. Conditional on $X=x$, the second part is a known constant, while the first has mean zero:

$
 E[Y-m(X) mid(|) X=x]=m(x)-m(x)=0.
$

In detail, the conditional cross term is

$
 E[2(Y-m(X))(m(X)-f(X)) mid(|) X=x]
 =2(m(x)-f(x))E[Y-m(x) mid(|) X=x]=0.
$

Now average over $x$. For discrete observations this means multiplication by $p(x)$ and summation; for a density it means integration. This is the *law of total expectation*: averaging conditional averages recovers the overall average. With finite squared forecast error these operations are integrable. The cross term disappears in the overall risk as well. Hence

$
 E[(Y-f(X))^(2)]
 = E[(Y-m(X))^(2)]+E[(m(X)-f(X))^(2)].
$

The second term is nonnegative and vanishes when $f=m$. Thus *the conditional mean is the optimal point forecast under squared loss*. Even a perfectly learned conditional mean leaves the first term, which can be large. The first term records the variability of individual realizations around that average.

Write the first term as $R^(*)=E[(Y-m(X))^(2)]$. It is the *irreducible error for the current input, target, and distribution*. That qualification matters: new observations or a new target can change it. Its value belongs to this particular prediction problem.

For example, if the independent increments discussed earlier are $Y in {-1,+1}$, then after any historical observation $m(X)=0$. The optimal point forecast is zero, yet squared error remains 1. Under those assumptions, predicting zero is the optimal result of training.

=== From an ideal predictor to the model actually trained

An unlimited predictor helps define the boundary. Actual models belong to a restricted set of functions $cal(F)$, such as a family of linear functions or networks of fixed size. For a function $f$, define its *risk* on the future distribution as

$ R(f)=E[(Y-f(X))^(2)]. $

Here “risk” means expected prediction loss, not portfolio volatility. Let

$ R_(cal(F))^(*)=inf_(f in cal(F)) R(f) $

be the lowest risk that this family can approach. The symbol $inf$ means infimum, or greatest lower bound; it remains meaningful even if no particular function attains the lowest value. For the trained function $hat(f) in cal(F)$, add and subtract the two ideal benchmarks:

$
 R(hat(f))=R^(*)
 +[R_(cal(F))^(*)-R^(*)]
 +[R(hat(f))-R_(cal(F))^(*)].
$

The identity organizes one prediction risk into three gaps:

1. *Information boundary*, $R^(*)$: what remains after fully using the current input.
2. *Representation gap*, $R_(cal(F))^(*)-R^(*)$: how far the selected family is from the ideal conditional mean.
3. *Actual fitting gap*, $R(hat(f))-R_(cal(F))^(*)$: how far the trained function is from that family's best performance.

The third term includes finite-sample estimation and optimization problems. Without further argument, it cannot be split into independent additive “statistical error” and “optimization error.” Overfitting also appears here: a function may have small loss on observed samples but large risk on future outcomes.

Memorizing many random signs can give zero training error. If future signs are still independently drawn, that memory does not reduce their uncertainty. *The training set is a finite past realization; risk concerns average performance on outcomes not yet seen.* When the true distribution is unknown, suitable out-of-sample evaluation must assess risk. A training curve describes fit on the observed realization; the out-of-sample comparison addresses the future-use question.

Enlarging the model family may reduce its ideal representation gap. It guarantees neither that the training procedure finds the ideal solution nor that finite samples suffice to select a good one. Adjusting the learning rate mainly changes how we search for a function: an oversized step can leave the region where a local approximation is useful; an undersized step can make progress slow. Neither supplies information about unobserved random outcomes. The optimization chapter takes up these numerical questions through learning rates, gradients, and search efficiency, alongside the information boundary developed here.

Probability prediction has a corresponding decomposition. Apply the earlier $H+D$ argument to each observation and average:

$
 E[-log_(2) q(Y mid(|) X)]
 =H(Y mid(|) X)+E_(X) [D(p(dot mid(|) X) upright(||) q(dot mid(|) X))].
$

For fixed input and target, additional capacity can at most bring the second term closer to zero; it does not change the first. Whether the actual second term decreases still depends on representation, samples, and training.

=== Which conditions really imply “unpredictable”?

A clear sufficient condition is independence of target $Y$ and observation $X$. Then $p(y mid(|) x)=p(y)$ and $I(X;Y)=0$. The optimal probabilities after observation remain the original probabilities, and the optimal squared-loss forecast remains the unconditional mean $E[Y]$.

But a random-looking curve does not prove independence, nor does a zero conditional mean. Construct a counterexample: $X$ takes 1 and 2 with equal probabilities; independently, $U$ takes $+1$ and $-1$ with equal probabilities. Set $Y=X U$. For every $x$, $E[Y mid(|) X=x]=0$, and the sign remains equally likely. Yet $|Y|=X$: the observation determines the magnitude exactly. Direction can be unpredictable while risk remains predictable.

Prediction boundaries therefore belong to a specified task. Forecasting a mean, a direction, a variance, and an entire distribution are different problems.

#principle[*Design decision:* Choose the method by the bottleneck. Add data when required observations are missing; change features or structure when the relation is hard to express; limit freedom and strengthen verification when samples are insufficient; inspect steps and training when optimization is inadequate. A larger network addresses the representation gap, while the other bottlenecks call for changes to observations, estimation, or optimization.]

== Why Precise Prices May Demand Far More Than the Predictable Information

We can now examine which degree of numerical detail a prediction task can support. The central question is whether *a target may demand far more distinctions than the input helps us make*. The following calculation measures those two quantities under an explicit probability model.

=== Turn price precision into discrete labels

Given today's price $P_(t)$, tomorrow's price and tomorrow's increment differ only by a known translation. Let the increment be $W=P_(t+1)-P_(t)$, with mean zero, standard deviation $sigma$, and density

$
 f_(W) (w)=1/(sqrt(2 pi) sigma) exp(-w^(2)/(2 sigma^(2))).
$

This is a *Gaussian*, or normal, distribution. This teaching approximation makes the calculation tractable; heavy tails, jumps, and changing states in actual returns remain outside this example. A density value is not the probability of an individual point; an interval probability is the integral of the density.

If the target demands price intervals of width $delta$, use an integer $j$ to identify the interval containing $W$. For fine intervals, the density changes little inside each one:

$
 p_(j)=integral_(j delta)^((j+1)delta) f_(W) (w) dif w
 approx f_(W) (w_(j)) delta,
$

where $w_(j)$ is a representative point in the interval. Substitute into the discrete entropy of the interval label:

$
 H_(delta)=-sum_(j) p_(j) log_(2) p_(j)
 approx -sum_(j) f_(W) (w_(j))delta log_(2) (f_(W) (w_(j))delta).
$

Split the logarithm using $log(a b)=log a+log b$ and approximate the fine-grid sum by an integral:

$
 H_(delta) approx -integral f_(W) (w) log_(2) f_(W) (w) dif w-log_(2) delta.
$

The last term is just $-log_(2) delta$ because the probability weights sum approximately to 1. The integral covers the whole real line. If only a finite price range is retained, specify whether the tails are retained, merged into overflow categories, or truncated and renormalized. Those policies define different targets. This formula is a fine-grid approximation for the complete distribution; a finite range can use it only when tail effects are negligible.

The negative logarithm of the Gaussian density is

$
 -log_(2) f_(W) (w)
 =log_(2) (sqrt(2 pi) sigma)+w^(2)/(2 sigma^(2) ln 2).
$

Averaging and using $E[W^(2)]=sigma^(2)$, the integral term becomes $log_(2) (sqrt(2 pi) sigma)+1/(2 ln 2)$. Since $log_(2) e=1/ln 2$, this gives

$
 H_(delta) approx log_(2) frac(sqrt(2 pi e) sigma, delta).
$

The interpretation is direct: at fixed volatility, halving the interval width adds approximately one bit to the target. We require twice as much detail to be distinguished, without adding information to the input. Units must match: converting a currency unit into hundredths multiplies both $sigma$ and $delta$ by 100 and leaves their ratio unchanged. The intermediate density integral is often called “differential entropy.” On its own it depends on units and cannot be used as the bit burden of a discrete label. Our final discrete approximation cancels that unit dependence.

=== How much can the same weak signal explain?

To calculate the input's help, construct a standardized signal $X$ and standardized increment $Z=W/sigma$. Here standardized means mean zero and variance one. Let $X,U$ be independent standard normal variables, and set

$ Z=rho X+sqrt(1-rho^(2))U, quad |rho|<1. $

Independence gives $E[X U]=0$, so $Var(Z)=rho^(2)+(1-rho^(2))=1$ and $E[X Z]=rho$. Variance is $Var(A)=E[(A-E[A])^(2)]$, covariance is $Cov(A,B)=E[(A-E[A])(B-E[B])]$, and correlation is covariance divided by the two standard deviations. With means zero and standard deviations one, correlation is simply $E[X Z]=rho$. Variables produced by linear combinations of independent Gaussian variables are called *jointly Gaussian*.

Mean and variance alone do not prove that $Z$ is standard normal; different distributions can share those moments. Let us establish its density too. Write $d=sqrt(1-rho^(2))>0$. At fixed $x$, the transformation $z=rho x+d u$ maps an interval of width $dif z$ to one of width $dif u=dif z/d$. Independence of $X,U$ gives the joint density

$
 f_(X,Z) (x,z)=1/d f_(X) (x) f_(U) ((z-rho x)/d)
 =1/(2 pi d) exp(-1/2 [x^(2)+(z-rho x)^(2)/d^(2)]).
$

Integrate over all $x$ to obtain the density of $Z$. First complete the square:

$ x^(2)+(z-rho x)^(2)/d^(2)=(x-rho z)^(2)/d^(2)+z^(2). $

To check this identity, multiply by $d^(2)=1-rho^(2)$. The left numerator is $(1-rho^(2))x^(2)+z^(2)-2 rho x z+rho^(2)x^(2)=x^(2)-2 rho x z+z^(2)$. The right numerator is $x^(2)-2 rho x z+rho^(2)z^(2)+(1-rho^(2))z^(2)$, the same expression. Completing the square isolates one normalized Gaussian integral and one target-dependent factor.

The $z^(2)$ term is independent of $x$ and comes outside the integral. The remaining integral of $exp(-(x-rho z)^(2)/(2 d^(2)))$ is $d sqrt(2 pi)$: dividing by that factor gives a normalized Gaussian density with mean $rho z$ and standard deviation $d$. Thus

$ f_(Z) (z)=1/sqrt(2 pi) exp(-z^(2)/2). $

This calculation establishes the full standard-normal distribution of $Z$, as well as its mean and variance.

Conditional on $X=x$, the first term of $Z$ is constant and the second is still an independent normal term. Therefore

$
 E[Z mid(|) X=x]=rho x, quad Var(Z mid(|) X=x)=1-rho^(2).
$

A shift in mean does not change how much relative detail a distribution requires us to distinguish. The reduced conditional variance supplies the reduction in uncertainty. Apply the previous Gaussian integral calculation at standard deviations 1 and $sqrt(1-rho^(2))$ and take the difference:

$
 I(X;Z)=-1/2 log_(2) (1-rho^(2)).
$

More explicitly, the unconditional density entropy is $h(Z)=1/2 log_(2) (2 pi e)$. Every conditional density has entropy $h(Z mid(|) X=x)=1/2 log_(2) (2 pi e(1-rho^(2)))$, independent of its mean $rho x$. Subtracting cancels $2 pi e$ and leaves the displayed information. Here $h$ means density entropy, not the discrete interval entropy $H_(delta)$.

Why is mutual information still valid for continuous variables? Define it through the joint density:

$
 I(X;Z)=integral integral f_(X,Z) (x,z)
 log_(2) frac(f_(X,Z) (x,z), f_(X) (x) f_(Z) (z)) dif z dif x.
$

Using $f_(X,Z)=f_(X) f_(Z mid(|) X)$, the density ratio becomes $f_(Z mid(|) X)/f_(Z)$. Splitting the logarithm yields the unconditional density entropy minus average conditional density entropy. Both terms are finite in this Gaussian example, and their difference is exactly what we computed. Their unit dependence cancels. This continuous information is an upper bound on information after discretizing $Z$ into price intervals, because discretization is also deterministic processing.

For small $|rho|$, apply $-ln(1-a)=a+O(a^(2))$ at $a=rho^(2)$:

$ I(X;Z)=rho^(2)/(2 ln 2)+O(rho^(4)). $

The notation $O(rho^(4))$ means that sufficiently near zero, the remainder's absolute value is bounded by some constant times $rho^(4)$; it does not assert that the remainder equals $rho^(4)$. *Under weak Gaussian correlation, the information improvement is of the order of the squared correlation.*

Keep the jointly Gaussian assumption. Correlation measures linear covariation, not all dependence. For example, let $X$ take $-1,0,+1$ with equal probabilities, and let $Y=X^(2)$. Then $E[X Y]=E[X^(3)]=0$, so correlation is zero, but $X$ determines $Y$ completely and mutual information is $H(Y)>0$. Substituting an arbitrary small market IC into the Gaussian formula does not measure all predictable information. In financial research, IC generally denotes a correlation between predictions and outcomes. Specify Pearson or rank correlation, and whether it is measured through time or across a cross-section. Our $rho$ is only the Pearson correlation in the stated example.

=== Numbers expose the mismatch

Take $sigma=1$ currency unit, $delta=0.02$, and $rho=0.05$. These parameters illustrate an order of magnitude; they are not estimates from a market dataset.

#table(
  columns: (2.2fr, 2.4fr, 1fr),
  table.header([Quantity], [Calculation], [Approximation]),
  [Entropy of the price-interval target], [$log_(2) frac(sqrt(2 pi e), 0.02)$], [7.69 bits],
  [Signal information about the complete increment], [$-1/2 log_(2) (1-0.05^(2))$], [0.001806 bits],
  [Information divided by target entropy], [$0.001806/7.69$], [0.0235%],
)

The ratio's numerator is continuous mutual information, while its denominator approximates fine-grid discrete entropy. This is an order-of-magnitude comparison; information about the interval label cannot exceed the numerator. The target requires distinguishing nearly eight bits of detail, while this particular signal removes only a few thousandths of a bit of uncertainty. Finer price grids increase the denominator, but the numerator remains bounded by the same continuous information.

The calculation concerns the specified distribution and signal $X$. Other timely observations may add conditional information, while trading value requires its own payoff evaluation. The information ratio and the profit comparison answer different questions.

The squared-loss problem highlights a related distinction. Forecasting the conditional mean $rho x$ requires representing the drift, not reconstructing every decimal of each realization. The entropy comparison does not prove that MSE is inherently useless or that an optimizer must merely copy the current price. It diagnoses a task demanding *fine interval outcomes from a weak predictive relation*.

=== Separate target precision, encoding geometry, and trading use

If price intervals become unrelated categories evaluated by ordinary log loss, assigning the same probability to the realized category can give the same loss whether a wrong forecast is in the adjacent interval or far away. Categorical loss does not itself weight mistakes by price distance. When numerical distance, ordering, or risk meaning matters, preserve it explicitly through representation, structure, or loss. Turning a price into a token does not do this automatically.

Preserving numerical geometry still does not answer whether those fine distinctions should be predicted. Suppose the direction layer only chooses between upward and downward actions, while magnitude, position size, and costs have explicit treatment elsewhere. An increase of 1.01 rather than 1.02 usually need not be a separate answer in this layer; an increase of 1.01 rather than a decrease of 1.01 must be. Merging numerical outcomes into directions is *coarse-graining*: remove details unused by this layer's action, retain distinctions that change it.

Coarse-graining is not a prescription to make every label as simple as possible. Labeling everything with one constant gives zero entropy but cannot choose a direction. Direction probabilities also cannot by themselves resolve asymmetric payoffs and costs. Chapter 2 derives those economic thresholds together with label design.

#principle[*Design decision:* The trend direction layer uses signs or policy first-passage outcomes, not exact future prices. This is a definite task-design choice: concentrate finite samples and capacity on relations that change the action, and leave magnitude and risk to the layers that need them. The Gaussian example explains the burden a fine target may impose within this directional task. Other numerical forecasts need to be assessed through the decisions they serve.]

=== The constructive default: forecast direction probabilities

The preceding arguments now lead to a concrete first design. For a trend direction layer, our starting task is *binary direction forecasting*. A binary target has two possible values: define $B=1$ when the standardized future increment $Z$ is positive and $B=0$ otherwise. The Gaussian example assigns probability zero to an exactly zero increment; actual discrete-price data need a declared zero-return convention.

Let us compare this target with the fine price intervals, using the same signal. Symmetry gives equal probabilities for the two directions, so

$ H(B)=-1/2 log_(2) (1/2)-1/2 log_(2) (1/2)=1. $

To calculate the remaining information, reuse $Z=rho X+d U$ with $d=sqrt(1-rho^(2))$. After observing $X=x$, an upward outcome occurs exactly when $U>-rho x/d$. Define the standard-normal cumulative probability $Phi(a)$ as the density integrated from negative infinity to $a$. Symmetry of that density gives

$
 Phi(a)=integral_(-infinity)^(a) 1/sqrt(2 pi) exp(-u^(2)/2) dif u,
 \
 p(x)=Pr(B=1 mid(|) X=x)=Phi(rho x/d).
$

The conditional probability follows in two steps: $rho x+d U>0$ is equivalent to $U>-rho x/d$ because $d>0$; then symmetry gives $Pr(U>-a)=1-Phi(-a)=Phi(a)$. No direction rule has yet been assumed: this is a conditional distribution calculation.

For a binary outcome with upward probability $p$, the entropy formula already introduced becomes

$
 h_(2) (p)=-p log_(2) p-(1-p)log_(2) (1-p), quad
 I(X;B)=1-E[h_(2) (p(X))].
$

This is the exact information expression in the specified model. To see its scale, expand around weak correlation. The derivative $Phi'(0)=1/sqrt(2 pi)$ and symmetry give $Phi(a)=1/2+a/sqrt(2 pi)+O(a^(3))$. Differentiating binary entropy gives $(h_(2))' (p)=log_(2) ((1-p)/p)$ and $(h_(2))'' (1/2)=-4/(ln 2)$. Write $v$ for a small displacement from one half. Symmetry removes odd powers, yielding

$
 h_(2) (1/2+v)=1-frac(2 v^(2), ln 2)+O(v^(4)).
$

The second derivative comes from differentiating $[ln(1-p)-ln p]/ln 2$:

$
 (h_(2))'' (p)=-frac(1,ln 2)[frac(1,1-p)+frac(1,p)].
$

At $p=1/2$ the derivative is $-4/ln 2$, so the quadratic Taylor term is half that coefficient times $v^(2)$. Both the first derivative and all odd Taylor terms at one half vanish because $h_(2) (1/2+v)=h_(2) (1/2-v)$. This is why the information gain starts at a squared, rather than linear, displacement.

For small $rho$, the leading displacement is $p(X)-1/2 approx rho X/sqrt(2 pi)$. Substitute it and use $E[X^(2)]=1$:

$
 I(X;B) approx frac(2, ln 2) E[(rho X/sqrt(2 pi))^(2)]
 =rho^(2)/(pi ln 2).
$

Averaging the higher-order terms uses the finite Gaussian moments; the leading expression is a weak-correlation approximation, not an exact formula for arbitrary signals. Compare it with the complete-increment information $I(X;Z) approx rho^(2)/(2 ln 2)$. Direction retains approximately $2/pi$, or 64%, of that information. It does not retain everything, but its target requires far fewer distinctions.

#table(
  columns: (2fr, 1.35fr, 1.35fr),
  table.header([Same signal, different target], [Fine price intervals], [Binary direction]),
  [Target entropy], [7.69 bits], [1 bit],
  [Signal information], [At most 0.001806 bits], [About 0.001148 bits],
  [Information / target entropy], [At most 0.0235%], [About 0.1148%],
)

Here the direction information uses its leading approximation at $rho=0.05$, while the fine-interval comparison retains the continuous upper bound used earlier. The recoverable fraction is about 4.9 times as large. We discard most of the target's detailed burden while retaining a substantial part of the directional relation. This is the positive reason to choose coarse-graining—not simply the assertion that precise prediction is difficult.

The advantage concerns a smaller, decision-aligned estimation task. Its effect on profit or accuracy still depends on the chosen policy and estimation procedure. Under the selected division of labor, a direction change alters the direction action; small decimal differences do not. Magnitude, costs, and risk still enter other parts of the decision process. That is why *direction probabilities, not precise future prices, are the usual starting target for this layer*.

The first research version follows a definite route:

1. *Freeze the policy and target.* Specify the asset, observation cutoff, feasible entry, and horizon. Use the sign for a fixed-holding direction task. If profits/stops determine exits along the path, use their first-passage outcomes instead; Chapter 3 constructs those labels.
2. *Supply a small state representation.* Start with available returns at several horizons, volatility, and relevant asset-specific relations. A stateless model—one whose evaluation depends only on the current feature input—sees only the supplied row, so useful past distinctions must appear in it. Chapter 5 constructs this panel.
3. *Estimate a probability.* A classifier here means a function estimating $p(F)=Pr(B=1 mid(|) F)$. Start with a no-input frequency forecast, then a restrained probability model using binary log loss $-[B log_(2) p+(1-B)log_(2) (1-p)]$. The earlier conditional $H+D$ argument explains its ideal output. Compare with a fixed rule taking the sign of a past multi-period return; do not start by increasing network size.
4. *Map probability to action using payoffs.* For symmetric gain/loss magnitude $g$ and cost $c$, go long above $1/2+c/(2g)$, short below $1/2-c/(2g)$, and abstain between them. With $g=1,c=0.1$, these are 0.55 and 0.45. The next section derives the payoff threshold. Use conditional payoff magnitudes when symmetry is absent, and control size separately.
5. *Confirm the whole route forward in time.* Fit only on available, matured outcomes. Compare probability loss, calibration (whether predicted probabilities match outcome frequencies), and the frozen policy's net cash outcomes on held-out periods. A better classifier and a better implemented trade are related but distinct results.

#principle[*Constructive conclusion:* Start trend direction research with a coarse, policy-aligned probability target, a small state panel, a restrained probability model, a payoff-derived participation rule, and independent temporal confirmation. Add numerical targets where magnitudes change a specified action or risk decision. This gives the research a concrete starting design whose profitability can then be evaluated.]

== Why an Edge May Remain: Drift, Frictions, and Breadth

=== What should we seek within these boundaries?

Return to the conditional mean and write the future target as

$ Y=m(X)+epsilon, quad E[epsilon mid(|) X]=0. $

This decomposition follows from the definition. It does not add an assumption that market residuals are independent. The earlier counterexample shows that a zero conditional residual mean can coexist with predictable conditional volatility.

Research into directional or return advantages asks how $m(X)$, or more general conditional outcome probabilities, changes with observations. At least three different economic explanations can guide it:

1. *Risk compensation:* Bearing a risk may earn an expected-return premium. This need not be a pricing error; earning it does not automatically establish risk-adjusted alpha.
2. *Gradual incorporation of information:* Attention, trading restrictions, and information diffusion may prevent news from entering all asset prices simultaneously. This motivates relations such as momentum, but their periods and conditions of applicability must be tested.
3. *Supply, demand, and behavioral frictions:* Forced trading, liquidity constraints, position limits, or systematic behavior may change short-run conditional outcomes. Specify the event, direction, duration, and implementation conditions.

An explanation guides the choice of observations and labels. Turn it into a testable hypothesis: what mechanism makes which observations change which outcomes?

Likewise, saying “markets are efficient” does not imply independence between every public observation and every future target. Claims about prices reflecting information must specify the information set, required risk compensation, and implementation conditions. A conditional expected return is not riskless arbitrage; predictable compensation may bear unacceptable risk.

=== Hit rate is not net expectation

Even a directional bias must be converted into money. For a fixed trading rule, let the probability of a profitable outcome be $p$, the average gain when profitable be $G>0$, the average loss magnitude otherwise be $L>0$, and average total cost per trade be $c$. All quantities refer to the same rule and evaluation scope. Averaging the two outcomes gives

$ E[Pi]=p G-(1-p)L-c. $

The threshold for positive net expectation is therefore

$ p>(L+c)/(G+L). $

The algebra is $p G-(1-p)L-c=p(G+L)-L-c>0$. Because $G+L>0$, division preserves the inequality. With $G=L=g$, this becomes the long condition $p>1/2+c/(2g)$. A short exchanges up and down: $g(1-2p)-c>0$ gives $p<1/2-c/(2g)$. In between, both positions have nonpositive expected payoff and abstention pays zero. These are comparisons between the same fixed-size contracts, not universal probability thresholds.

It is 50% only when gain and loss magnitudes are equal and costs are zero. With $p=0.6$, $G=1$, $L=2$, and $c=0$, average profit is still $0.6-0.8=-0.2$. The payoff asymmetry outweighs the favorable hit rate in this example.

A complete strategy also allows no trade, variable position size, and conditional costs. The simplified expression forces alignment between labels and actions: a classifier optimal under zero–one loss is not automatically a trader optimal for cash profit. Coarse-graining the direction layer does not permit deleting magnitude, costs, and risk from the strategy.

=== Why a small edge matters—and why a repetition count can mislead

Suppose each net trade profit $Pi_(i)$ has mean $a>0$ and standard deviation $s$, and the profits are independent. For total profit $S_(N)=sum_(i=1)^(N) Pi_(i)$, linearity of expectation and addition of independent variances give

$ E[S_(N)]=N a, quad Var(S_(N))=N s^(2). $

The ratio of total mean to standard deviation is

$ (E[S_(N)])/sqrt(Var(S_(N)))=(a/s)sqrt(N). $

A small single-trade advantage does not imply a small aggregate signal-to-noise ratio. The average profit $S_(N)/N$ keeps expectation $a$, while its standard deviation falls to $s/sqrt(N)$. This is the mechanism behind amplifying a small edge through many bets: relative average noise declines; individual signals do not become smarter.

The gain from repetition depends on independence. With dependent trades, the variance includes every covariance:

$
 Var(S_(N))=sum_(i) Var(Pi_(i))+2 sum_(i<j) Cov(Pi_(i),Pi_(j)).
$

Here $Cov(A,B)=E[(A-E[A])(B-E[B])]$ measures how two profits jointly depart from their means. If every variance is $s^(2)$ and every distinct pair has the same correlation $kappa>=0$, there are $N(N-1)/2$ covariance pairs, each equal to $kappa s^(2)$. Thus

$
 Var(S_(N))=N s^(2) [1+(N-1)kappa],
 \
 (E[S_(N)])/sqrt(Var(S_(N)))
 =(a/s)sqrt(N/(1+(N-1)kappa)).
$

For this equal-correlation example, $N_("eff")=N/[1+(N-1)kappa]$ is an effective count relative to independent trades. With $N=500$ and $kappa=0.02$, it is approximately 45.5, not 500. This definition is for this example; strategies with unequal sizes and other dependence structures require their actual covariance and decision structure to be assessed.

Asset counts, trade counts, and dataset row counts are not automatically independent breadth. Shared macro exposures, overlapping holding periods, and a common driving event can make many trades behave like one enlarged bet. Breadth under an independence approximation explains why thin signals deserve study; dependence and implementation constraints determine how much breadth can actually be realized.

Even if $a>0$, finitely many trades can lose money. Even a favorable long-run average can have losses along the path that breach funding or risk constraints. The derivation explains repeated diversification; realized stability also depends on the funding and risk limits along the path.

#principle[*Chapter conclusion:* The starting route for trend direction research uses policy-aligned coarse labels, available state features, and restrained probability estimates. Payoffs and costs then determine participation, with risk sizing and temporal confirmation assessed separately. This focuses estimation on decision-relevant bias while discarding unnecessary target detail. Improve observations or representation as needed; expand model capacity when a verified expression gap remains.]

#heading(level: 2, numbering: none)[Take This Chapter Forward]

We now have three different tools. Cash profit determines *which outcomes are worth predicting*. Conditional means and risk decomposition locate *the remaining error bottleneck*. Entropy and mutual information diagnose *a mismatch between target burden and observational help*. These tools cannot substitute for one another, but jointly constrain one research task.

Chapter 2 uses them to redesign two things together. *Labeling* determines which distinctions the target retains. *Feature engineering* determines how existing observations are presented to a finite model. We develop the action conditions behind coarse-graining and construct failures of restricted models to explain why deterministic transformations can improve learning without increasing Shannon information. These arguments make target and feature design the first practical levers, before increasing model capacity.

#heading(level: 2, numbering: none)[Self-Check: Can You State the Boundary?]

1. A model predicts tomorrow's price with an error of only 0.5%. Does this establish a directional advantage? State the additional baseline comparison required.
2. If $X=u+v$ and the target becomes $Y=2(u+v)$, does failure to reconstruct $(u,v)$ prevent predicting $Y$?
3. In the example $Y=X U$, why does a zero conditional mean not imply that nothing is predictable?
4. With $sigma$ and the signal relation fixed, what happens to target entropy when price intervals are halved? Why does that not guarantee more useful prediction?

*Answer guide:* For question 1, compare against a no-change or conditional-mean baseline on the increment target, and examine out-of-sample direction and net profit. For question 2, compute $2X$ directly. For question 3, the observation still determines magnitude. For question 4, a fine grid adds approximately one bit, without adding an observational relation; the action may not use those details either.


== Start with a Market, an Instrument, and an Executable Question

The coarse-direction conclusion has a practical consequence: do not begin a project with “predict this market.” Begin with an instrument, a decision time, an allowed position, and a realizable outcome. The following three experiments carry that discipline through the next five chapters. They are proposed teaching protocols, not reported profitable strategies.

=== Experiment A: short-horizon A-share continuation versus reversal

Suppose a researcher observes intense turnover, a strong sector move, and a stock approaching its daily upper price limit. Two plausible stories lead to opposite decisions. Attention and order imbalance may persist into the next session; alternatively, transient demand may exhaust itself before a new buyer can exit. Calling the stock “strong” does not distinguish these hypotheses.

Our first experiment asks whether a completed-session state predicts *next-session relative performance*, using an eligible long-only opportunity set and a separately specified later entry and exit. Compare continuation and reversal definitions on the same chronological development periods. Relative performance means the stock's realized return minus a declared market or sector comparison, not a guaranteed cash hedge. The holding layer must still decide how much market exposure to retain.

Short-horizon A-share research must respect sale eligibility of newly purchased stock and instrument-specific price limits. The SSE's 2026 rules distinguish ordinary securities from instruments eligible for intraday turn-around trading, and distinguish main-board and STAR price-limit arrangements. Do not transfer an ETF's permission to an ordinary share or hard-code one limit percentage for every security. The original Chinese rules govern; the English translation supplies a reading aid. A price hitting a limit is not proof that a submitted order would fill. These are rule and execution facts, not a claim that all A-share investors behave alike.

*Selected starting design:* completed-session features, next-feasible-entry/exit outcomes, long or flat rather than an assumed freely shortable action set, and a relative-ranking baseline. Intraday continuation can be a separate inventory-aware study; it is not a shortcut around the first experiment's holding restriction.

=== Experiment B: a rapid crypto rise, followed by selling

A “pump” here first denotes a rapid upward move; a “dump” denotes rapid selling or decline. Coordinated pump-and-dump manipulation is a different evidential claim. The CFTC has documented social-media promotion schemes in thinly traded tokens, but one sharp chart alone does not identify organizers, intent, or manipulation. We study observable stress and execution, not participation in such schemes.

Two markets can rise 5% on a chart while presenting different decisions. One has broad spot participation and replenishing bids; another has a thin book, derivatives-led buying, and fragile collateral. A close-only forecast cannot tell which state generated the move. Extra observations may help, but they need event and receipt times. A perpetual contract is a derivative whose funding payments and margin rules affect the position; owning its underlying spot token is a different action. Funding is a recurring payment between long and short positions under the contract rule; margin is collateral whose insufficiency can force a position to close. These are cash and survival mechanisms, not extra names for price return.

*Selected starting design:* on liquid, historically eligible instruments, define a mechanical event from past returns and activity, freeze its first observable time, and predict a policy's continuation/failure outcome. Start with spot, long or flat, before extending the experiment to leveraged derivatives. Include a liquidity-based abstention rule. Do not label a future crash as a historical warning feature, or treat many tokens rising on one common event as independent bets.

=== Experiment C: a U.S.-equity token while the reference market is closed

The name of a company is not the identity of the instrument being traded. A direct share, an issuer's equity-linked token, a perpetual on that token or an equity index, and a token holding a futures strategy have different rights and cash flows. “Futures token” alone does not determine which of these is meant.

As a concrete current illustration, Kraken describes xStocks as equity-linked tokens without ordinary shareholder rights, and separately publishes perpetual contracts referencing xStocks. This establishes the need to distinguish objects, not the suitability or availability of a product to a particular reader. Record issuer, venue, chain, reference index, settlement currency, custody/redemption terms, and derivative contract identity before collecting prices. Specifications in this lecture were checked on 11 October 2026; they must be rechecked for an actual experiment.

*Selected starting design:* divide observations into reference-market-open and reference-market-closed states. Predict a later executable token return or a separately defined token/reference convergence, not tomorrow's exact underlying stock price by default. A closed-market last quote is stale information, not a contemporaneously executable hedge. Chapter 2 derives why that changes the target, and Chapter 4 constructs the necessary clocks.

#principle[*Market-specific conclusion:* Coarse-grain the answer, not the market's operating rules. Choose direction for a directional action, rank for relative selection, and a policy-success label for an event trade. Inventory, liquidity, funding, and reference-market availability determine which action that answer can support.]

=== A first practical route, before any large model

For each experiment, write a one-page specification containing the opportunity set, observable cutoff, later execution schedule, target, costs, and abstention rule. Construct ten hand-audited opportunities including unavailable entries and adverse paths. Then compare a no-change or unconditional forecast, one economically motivated signal, and a small probability or ranking model. Use chronological development and untouched confirmation; report coverage and net outcomes alongside prediction loss.

This route turns the prediction boundary into a sequence of research decisions. A precise-price network is not the first comparison because the decision does not use most of its target detail. A richer model becomes justified only after the cheaper route exposes a remaining relation it cannot express.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Claude E. Shannon. #link("https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf")[_A Mathematical Theory of Communication_]. _The Bell System Technical Journal_ 27, 379–423 and 623–656, 1948. Sections 6–7 develop entropy for discrete sources; Part III treats continuous variables.
- Shanghai Stock Exchange. #link("https://english.sse.com.cn/start/sserules/stocks/trading/c/10825757/files/d263e3a87f37436ca2f8e5bcfc4ff001.pdf")[_Trading Rules of Shanghai Stock Exchange (2026 Revision)_]. Articles 3.1.4–3.1.5, 3.3.13, and 6.6. Original Chinese rules prevail; check the applicable historical instrument version.
- U.S. Commodity Futures Trading Commission. #link("https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/beware_virtual_currency_pump_dump.html")[_Customer Advisory: Beware Virtual Currency Pump-and-Dump Schemes_]. 2018. Documented manipulation mechanisms, not identification of every rapid price move.
- Kraken. #link("https://www.kraken.com/legal/xstocks")[_xStocks Risk Disclosure_] and #link("https://support.mtf.kraken.com/hc/en-us/articles/25499987607837-Linear-Contract-Specifications")[_Linear Contract Specifications_]. Product identity and distinct derivative mechanics; checked 11 October 2026.
]

#pagebreak()

= Features and Labels: Change the Problem Before the Solver
#counter(math.equation).update(0)
#show table.cell: set par(justify: false)

A price table and an algorithm give us materials for research. To turn them into a prediction task, we first construct two objects: the question whose answer will change a decision, and the observations in a form that the chosen algorithm can read. These are the jobs of *labeling* and *feature engineering*.

Chapter 1 established why precise future-price prediction is not our default direction task. This chapter turns that conclusion into a design method. We will retain the distinctions used by a trading policy, discard unnecessary detail, and expose useful historical relations to a restrained probability model. The aim is the smallest well-specified prediction problem that serves the decision; its label and model can then take the form that this problem needs.

The numerical constructions below are deliberately small, so we can follow each step connecting information to decisions. An empirical strategy's profitability would need a separate test.

== Two Constructions, with Different Time Directions

=== A label says what deserves an answer

Imagine deciding after today's observations have arrived whether to enter a position at the next available execution opportunity. A label might record whether the subsequent return is positive. Another might record whether a profit target is reached before a stop. These are different questions even when they use the same price history.

Let $X_(t)$ denote observations actually available by decision time $t$. Let $Z_(t)$ denote the future outcome: it could be an endpoint return or an entire subsequent price path. Choose a target map $g$ and a representation map $phi$:

$
  Y_(t)=g(Z_(t)), quad F_(t)=phi(X_(t)).
$

The *label* $Y_(t)$ states which future distinctions we want to predict. The *feature vector* $F_(t)$ contains the numerical inputs shown to the predictor. In quantitative finance, a constructed feature is often called a *factor*. Its predictive value comes from the relation established with the specified label and decision.

The two maps have opposite availability conditions. Features must be computable when the decision is made. A future-dependent label becomes known only after its outcome matures. It is legitimate to use that label to train on a completed historical example; it is not legitimate to feed it, or a transformation depending on it, into the earlier decision.

For a fixed-horizon experiment, record the decision time, executable entry time $e_(t)$, and exit time $u_(t)$. With positive execution prices, define

$
  R_(t)=frac(P_(u_(t))-P_(e_(t)),P_(e_(t))), quad
  B_(t)=cases(1 & "if" R_(t)>0, 0 & "if" R_(t)<=0).
$

Here $B_(t)$ is an up-versus-not-up label, before costs. Exact zeros are assigned to the second class by convention. If unchanged prices are frequent and economically distinct, retain a third class instead. An after-close feature cannot silently assume execution at that same closing price; $e_(t)$ must respect the information and order schedule.

=== Define the decision before reducing the target

Write down four things first: which opportunities are eligible, when observations arrive, which actions are allowed, and how positions exit. For example: one decision per completed daily observation; entry at the next executable opportunity; long, short, or abstain; exit after a specified horizon. A stop-and-target policy replaces the last item, and generally requires a different label.

The logical order is therefore *policy → target → observations and representation → predictor*. Historically usable observations and a specified execution schedule then turn that design into labels we can actually construct.

Our default trend direction layer predicts *direction or policy outcomes*, not a precise future quote. A participation layer uses probabilities, payoffs, and costs to decide whether the opportunity is worth taking. A risk layer decides size and acceptable exposure. Each layer can therefore focus on the quantities its decision uses. Section 2.6 derives the conditions under which the reduction preserves the action.

#principle[*Design rule:* Specify what the answer will be used for. Labeling removes distinctions that the decision does not need; feature engineering presents the relevant known distinctions to its predictor. Choose the number of classes and features according to these roles.]

== Why Direction Is the Default Coarse Target

=== Less recoverable information can still be a better-sized question

Recall Chapter 1's teaching model. Independent standard-normal variables $X,U$ generate a standardized future increment

$
  Z=rho X+sqrt(1-rho^(2)) U, quad 0<rho<1.
$

The signal $X$ weakly shifts the outcome distribution. Predicting a finely binned increment asks for many more distinctions than predicting its sign. The conditional sign probability is

$
  p(x)=Pr(Z>0 mid(|) X=x)
      =Phi(frac(rho x,sqrt(1-rho^(2)))).
$

The function $Phi$ is the integral of the standard-normal density, introduced in Chapter 1. Symmetry gives the sign label $B$ marginal probability one half, hence entropy one bit. With binary entropy $h_(2) (p)=-p log_(2) p-(1-p)log_(2) (1-p)$, its remaining conditional uncertainty is the average of $h_(2) (p(X))$.

Chapter 1 obtained the weak-signal comparison by expanding $Phi$ near zero and $h_(2)$ near one half, then averaging with $E[X^(2)]=1$:

$
  I(X;Z)=frac(rho^(2),2 ln 2)+O(rho^(4)), quad
  I(X;B)=frac(rho^(2),pi ln 2)+O(rho^(4)).
$

Thus direction retains about $2/pi$, or 64%, of the complete increment's information in this model. It does not create information. What changes much more sharply is the amount of detail requested. For the earlier fine-grid example, $rho=0.05$, $sigma=1$, and grid width $delta=0.02$ gave the following comparison:

#table(
  columns: (1.45fr, 1fr, 1fr, 1.15fr),
  table.header([Target], [Target entropy], [Signal information], [Recoverable fraction]),
  [Fine increment bins], [About 7.69 bits], [About 0.001806 bits], [About 0.0235%],
  [Increment sign], [1 bit], [About 0.001148 bits], [About 0.1148%],
)

The first row uses the fine-grid approximation; the sign-information figure uses the leading weak-signal term. The recoverable fraction rises by roughly 4.9 times. The comparison concerns information burden. Its implications for profit and training depend on the policy and learning problem.

The design conclusion is decisive: *when the direction decision does not consume future-price decimals, do not make those decimals the default supervised target*. Estimate the directional bias directly. Estimate numerical payoff scales and risks where they enter participation, sizing, or risk control. A constant label would have even smaller entropy, but would erase the distinctions needed to select actions; entropy minimization alone is not the design rule.

=== How much directional accuracy does a weak signal provide?

The information comparison is easier to interpret if we also derive a hit rate. Suppose the sole criterion is whether a direction is correct, with equal penalties for the two errors. Predict up when $p(x)>1/2$ and down when $p(x)<1/2$. Since $rho>0$ and $Phi$ increases, the optimal rule predicts the sign of $X$.

We can compute its accuracy without a difficult integral. The planar density of $(X,U)$ is

$
  f(x,u)=frac(1,2 pi) exp(-(x^(2)+u^(2))/2).
$

In polar coordinates, $x=r cos theta$ and $u=r sin theta$. A small wedge has arc length $r dif theta$ and radial thickness $dif r$, giving area element $r dif r dif theta$. The density times this element depends on radius but not angle. Integrating out the radius therefore leaves a uniform angle on a full circle.

Set $alpha=arccos(rho)$. Then $rho=cos alpha$ and $sqrt(1-rho^(2))=sin alpha$. The signs of $X$ and $Z$ are the signs of projections onto unit vectors $(1,0)$ and $(cos alpha,sin alpha)$. Their positive half-planes differ by angle $alpha$. On the circle, there are two disagreement sectors, each of width $alpha$. Consequently,

$
  Pr("different signs")=frac(2 alpha,2 pi), quad
  Pr("same sign")=1-frac(arccos(rho),pi)
    =frac(1,2)+frac(arcsin(rho),pi).
$

The geometry can be verified by writing $Z=r cos(theta-alpha)$. On a full circle, $cos theta$ and $cos(theta-alpha)$ disagree only between the two pairs of zero crossings displaced by $alpha$. Each pair contributes an interval of length $alpha$, making total disagreement angle $2 alpha$. The radial integral equals $integral_(0)^(infinity) exp(-r^(2)/2)r dif r=1$, so angular probability is angle divided by $2 pi$, rather than an assumption about how frequently each radius occurs.

At $rho=0.05$, accuracy is about 51.59%. Near zero, $arcsin(rho)=rho+O(rho^(3))$: the accuracy edge is first order in $rho$, whereas information is second order. They are different measures of the same example, not interchangeable quantities.

A small average edge can matter across sufficiently diversified opportunities, as Chapter 1 explained. But 51.59% does not tell us which trades clear costs, how large losses are, or how many effectively independent opportunities exist. The same Gaussian conditional probability can be used to filter opportunities rather than trade every predicted sign. The required filter is an economic threshold, derived below—not simply “accuracy exceeds one half.”

#principle[*Conclusion:* Coarse direction is a selected practical design because it preserves the relevant bias while discarding much unnecessary target detail. The Gaussian calculation explains the reduction; the payoff calculation determines whether the resulting prediction supports an action.]

== Present Information Is Not Necessarily Usable Information

=== A three-point problem exposes the missing computation

Feature engineering seems paradoxical if a feature is only a deterministic transformation. Chapter 1 proved the data-processing boundary: $I(phi(X);Y)<=I(X;Y)$. How can a transformation improve prediction?

Construct the smallest example that separates “information present” from “information accessible to this model.” Let $X$ take $-1,0,+1$ with equal probabilities, and let $Y$ equal one at the two ends and zero in the middle:

#block(breakable: false)[#table(
  columns: (1fr, 1fr, 1fr),
  table.header([Raw input $X$], [Label $Y$], [Transformed input $F=X^(2)$]),
  [$-1$], [$1$], [$1$],
  [$0$], [$0$], [$0$],
  [$+1$], [$1$], [$1$],
)]

Restrict a classifier to one threshold on its input: one prediction below the threshold and another above it. On raw $X$, one split cannot separate the middle from both ends. At least one of the three equally likely points must be misclassified, so minimum classification error is $1/3$. With $F=X^(2)$, the single split $F>1/2$ classifies all points correctly.

The computation $X^(2)$ supplies no new observation. It changes the geometry seen by a model that cannot itself form a two-sided region with one split. A predictor allowed two raw-input splits could solve the original problem. The benefit comes from the chosen one-split restriction; richer raw-input models can perform the missing computation themselves.

=== Repeat the comparison with probabilities, not just hard classes

To compare information in log-loss units, we now repeat the classification construction with a probability predictor: one threshold and one constant probability on each side. Such a predictor is often called a *decision stump*. It may also ignore the input and report one constant probability everywhere.

For a group whose true fraction of label-one outcomes is $a$, a constant forecast $q$ has mean binary log loss

$
  L(a,q)=-a log_(2) q-(1-a)log_(2) (1-q)
        =h_(2) (a)+D((a,1-a) parallel (q,1-q)).
$

Chapter 1 showed that the last term is nonnegative and is zero when the two probability distributions agree. Thus the best probability in each group is its true fraction $a$, and the best group loss is $h_(2) (a)$.

Without input, the label-one fraction is $2/3$. The best constant forecast has loss $h_(2) (2/3) approx 0.9183$ bits. Any nontrivial threshold on raw $X$ isolates one end and leaves the middle with the other end. The isolated end has a pure label; the remaining two points have fractions one half and one half. Averaging their optimal group losses gives

$
  L_("raw")^(*)=frac(1,3) h_(2) (1)+frac(2,3) h_(2) (1/2)
              =frac(2,3) " bits".
$

With $F=X^(2)$, the two groups are pure. Their optimal loss is zero. Probability zero for an impossible class is harmless here: no realized outcome is assigned zero probability. In empirical fitting, finite samples rarely justify such certainty, so probabilities are usually kept away from zero and one when scoring.

Both $X$ and $F$ determine $Y$ exactly, so their Shannon information about $Y$ is the same, $H(Y)=h_(2) (2/3)$. Yet the best one-split probability loss falls from $2/3$ to zero after the transformation. This reduction in attainable loss gives a precise meaning to making existing information usable.

=== Define usable information only after identifying the restriction

Let $cal(V)$ be a declared family of probability predictors. For a discrete label, each predictor returns valid class probabilities. We require compatible constant forecasts: a forecast available without input must remain available when input is supplied. The predictor can then ignore an unhelpful feature. The formal predictive-family construction, including this ability to ignore input, is developed by Xu et al. (2020), cited in the references.

Write $cal(V)_(emptyset)$ for its no-input forecasts and $cal(V)_(F)$ for its forecasts using representation $F$. Their best population log losses are

$
  H_(cal(V)) (Y)=inf_(q in cal(V)_(emptyset)) E[-log_(2) q(Y)],
  \
  H_(cal(V)) (Y mid(|) F)=inf_(q in cal(V)_(F)) E[-log_(2) q(Y mid(|) F)].
$

Here an infimum is the greatest lower bound of attainable losses; a best predictor need not actually attain it. *Predictive $cal(V)$-information* is the reduction in this best loss obtained from the input:

$
  I_(cal(V)) (F arrow.r Y)
    =H_(cal(V)) (Y)-H_(cal(V)) (Y mid(|) F).
$

The arrow emphasizes prediction from $F$ to $Y$ under a restriction. This is not automatically a symmetric information relation. With all probability predictors available, the log-loss decomposition recovers Shannon conditional entropy and mutual information. With restricted predictors, the family and representation become part of the quantity being measured.

The three-point example makes the subtraction concrete: raw usable information is $h_(2) (2/3)-2/3 approx 0.2516$ bits, while transformed usable information is $h_(2) (2/3)-0 approx 0.9183$ bits. The baseline is identical in both comparisons. If both the representation and no-input family were changed, a larger difference might partly reflect a changed benchmark rather than improved use of the same observations.

For a finite, positive no-input loss, define a normalized diagnostic, which we will call the *learnability fraction*:

$
  cal(L)_(cal(V))=frac(I_(cal(V)) (F arrow.r Y),H_(cal(V)) (Y))
      =1-frac(H_(cal(V)) (Y mid(|) F),H_(cal(V)) (Y)).
$

Why is it between zero and one? Input can be ignored, so the optimal conditional loss is no greater than the no-input loss. Discrete probability log loss is nonnegative, so it is no less than zero. Dividing these inequalities by the positive baseline gives the interval. If the baseline is zero, the target is already perfectly predicted without input and this ratio is undefined; it is not a reason to award a perfect useful signal.

In the three-point construction, the no-input family includes the true label proportions. Its baseline is therefore $H(Y)$. We can now quantify the representation gain without confusing loss and accuracy:

#table(
  columns: (1.15fr, 1.1fr, 1.1fr, 1.1fr),
  table.header([Representation], [Best input log loss], [Usable information], [Learnability fraction]),
  [Raw $X$, one split], [$2/3$ bits], [About 0.2516 bits], [About 27.4%],
  [$X^(2)$, one split], [$0$ bits], [About 0.9183 bits], [100%],
)

This table is an exact population construction, apart from rounding. A fitted model on finite observations does not directly reveal these infima. With a shared feasible baseline and held-out average losses $hat(L)_(0)$ and $hat(L)_(F)$, the empirical quantity $1-hat(L)_(F)/hat(L)_(0)$ is a performance comparison, not a certified population learnability fraction. It can be negative. Repeatedly selecting the largest such score can also select noise.

The denominator equals Shannon entropy only when the no-input family can express the true marginal probabilities. Furthermore, the interval argument here uses discrete labels; probability *densities* for continuous outcomes need not have nonnegative log loss. We will not transfer this ratio unmodified to arbitrary continuous-density models.

#principle[*Feature-engineering conclusion:* For refined-factor strategies, first compute the economically motivated transformations that a restrained predictor cannot express or reliably learn. Then let the small predictor combine them. Raising usable information through representation does not violate the Shannon boundary. Changing the model family can also matter, so make its restrictions explicit in the comparison.]

== Two Routes to More Predictive Help

=== New observations raise the ceiling only through conditional contribution

Suppose $X$ is the existing history and $A$ is a newly obtained observation, such as an inventory release or a structured text measurement. We assess $A$ by the help it provides after the existing history is known.

For a finite discrete target $Y$, define conditional information gain as the reduction in conditional entropy:

$
  I(A;Y mid(|) X)=H(Y mid(|) X)-H(Y mid(|) X,A).
$

At each given $(X,A)$, compare the label distribution using both observations with that using $X$ alone. Averaging the same log-loss decomposition used above gives

$
  I(A;Y mid(|) X)
    =E_(X,A) [D(Pr(Y mid(|) X,A) parallel Pr(Y mid(|) X))]>=0.
$

Subtract and add $H(Y mid(|) X)$ in the total information to obtain

$
  I((X,A);Y)=I(X;Y)+I(A;Y mid(|) X).
$

This identity separates an expanded information set from an expanded feature list. A deterministic copy of $X$ has zero conditional contribution. An inventory observation may contribute if it distinguishes future outcomes beyond what prices already reveal. It may contribute nothing if it is redundant, stale, too noisy, or already represented in $X$.

Its availability is also part of the observation definition. A release dated on Monday but received on Tuesday cannot be used in Monday's decision. Later revisions cannot replace the values that the historical decision actually had. Data identity, publication time, receipt time, and revision policy therefore precede claims of additional information.

The practical comparison is *existing inputs versus existing inputs plus the new source*, with the target, temporal splits, predictor budget, and evaluation fixed. A source can contain additional population information yet fail to yield a reliable gain with the available sample and model. Its incremental contribution to the decision provides the reason to acquire it.

=== Existing observations can be arranged into a readable state

The second route keeps the information set fixed but changes its representation. Three simple constructions show how representation changes the problem seen by the model.

*Remove an irrelevant price unit.* With positive prices, define a past $k$-period log move and a moving-average deviation:

$
  m_(t,k)=ln(frac(P_(t),P_(t-k))), quad
  overline(P)_(t,k)=frac(1,k) sum_(j=0)^(k-1) P_(t-j), quad
  d_(t,k)=frac(P_(t),overline(P)_(t,k))-1.
$

For a positive rescaling factor $a$, the new moving average is $overline(a P)_(t,k)=a overline(P)_(t,k)$. Consequently, $ln(a P_(t)/(a P_(t-k)))=ln(P_(t)/P_(t-k))$ and $a P_(t)/(a overline(P)_(t,k))-1=d_(t,k)$. The cancellation proves the stated invariance; it is not a numerical observation from a few price paths.

If every price is multiplied by the same positive constant, both $m$ and $d$ remain unchanged. A model no longer needs to learn that a unit convention or a proportional rescaling preserves these relative moves. This does not make every asset comparable: contract changes, rolls, distributions, and market structure still require their own treatment. The equations establish a specific scale invariance, not a universal data-cleaning solution.

*Give a snapshot model the history it cannot remember.* A row-wise predictor evaluates the current row without carrying a hidden state from earlier predictions. One past return cannot reveal all longer-horizon relations. Consider two past five-step increment sequences:

$
  (1,1,1,1,1), quad (-1,-1,-1,-1,1).
$

Both have final increment $+1$. Their five-step sums are $+5$ and $-3$. A feature containing only the last increment identifies the two histories as the same; adding the five-step summary distinguishes continuing advance from a short rebound within a decline. A small set such as $m_(t,1),m_(t,5),m_(t,20)$ puts multiple time scales into today's row. These windows are an illustrative starting grid, not empirically optimal values. The reason for multiple horizons is to expose state, not to generate every window until one fits.

*Expose relative position when the task is relative.* For a cross-section of eligible assets at decision time $t$, a feature $f_(i,t)$ can be centered and scaled using that same available cross-section:

$
  z_(i,t)=frac(f_(i,t)-overline(f)_(t),s_(t)), quad
  overline(f)_(t)=frac(1,n_(t)) sum_(i=1)^(n_(t)) f_(i,t),
  \
  s_(t)^(2)=frac(1,n_(t)) sum_(i=1)^(n_(t)) (f_(i,t)-overline(f)_(t))^(2).
$

This *z-score* states how far an asset lies above or below the cross-sectional average in units of cross-sectional dispersion. It changes a raw measurement into a relative one that a row-wise model can consume. The universe and values must be available at $t$; when $s_(t)=0$, there is no relative distinction, so use a declared constant or missing-state rule rather than divide by zero. Cross-sectional scaling is not automatically the right operation for a single-asset timing task.

For timing features, a fixed training-period mean and dispersion can instead put columns on comparable numerical scales for a linear probability model. Apply the frozen transformation to later observations. If a rolling transformation is used, it may use only the stated historical window. Neither version may estimate its scaling parameters from the future evaluation period.

These constructions solve different problems: units, missing time state, and relative position. Standardization is not the definition of a factor, and a deterministic transformation can also discard something essential. For example, $X^(2)$ helped our two-sided label but would erase the sign if $Y$ were the sign of $X$. Judge a representation by the decision it is meant to support.

=== Compare the transformation, not two changing pipelines

Use a small, interpretable panel first. For each column, record its formula, required lookback, availability time, missing-value rule, and the relation it is intended to expose. Then compare a baseline representation with one justified addition using the same label, predictor family, training budget, and temporal evaluation.

This controlled comparison, adding or removing a component while keeping the rest fixed, is called an *ablation*: it asks whether the specific component contributes when the rest is held fixed. Later chapters extend it to dependence between factors and to the cost of searching many candidates. Here the essential conclusion is already clear: increasing column count is not the same as increasing usable information. The added column earns its place through a declared relation and independently checked contribution.

== Divide the Work According to the Bottleneck

The learnability fraction makes a useful division visible. Label design determines the question and its baseline burden. Observations determine which distinctions are present. Representation and predictor family determine which relations are accessible. Actual fitting determines how closely the trained predictor approaches the family's best performance. Verification determines whether an apparent improvement survives outside the choices that produced it.

The model also participates in this division of labor. Expanding $cal(V)$ can reduce the best conditional loss. With the same no-input baseline, it can increase usable information. But a larger family also gives finite-sample fitting more ways to reproduce noise. A network cannot repair an action-irrelevant target or a missing observation merely by adding parameters.

Use the following order to locate the next experiment:

#table(
  columns: (1.2fr, 1.8fr),
  table.header([Observed difficulty], [First practical response]),
  [The target asks for distinctions the policy never uses.], [Replace precise reconstruction with direction, relative rank, or policy outcomes. Keep necessary payoff and risk components.],
  [Different actionable states look identical in the available history.], [Seek a timely complementary observation, or narrow the claimed task. A deterministic transform cannot add the absent distinction.],
  [The relation is present but awkward for the restrained predictor.], [Construct a scale, history, or interaction feature; test it with the same predictor before enlarging the family.],
  [Raw paths or text still require substantial representation work.], [Use a structure suited to that input, then control its capacity. Handcrafted summaries are not compulsory.],
  [The gain appears only in repeatedly optimized samples.], [Stop increasing complexity. Return to temporal verification and account for the search already performed.],
)

The first route for an already refined factor panel is a restrained model, not a large end-to-end network. A small nonlinear model becomes the next comparison when economically plausible interactions remain. A representation model becomes relevant when the inputs still contain relations that explicit summaries do not expose. These conditions guide the choice for the current task and can change as its bottleneck changes.

#principle[*Priority:* In the refined-factor route, spend the first research effort on labels, representations, and verification. Upgrade the solver when a remaining expression or optimization limitation is demonstrated. Interpret the learnability fraction in terms of the specified model family, data, and labels.]

== Turn the Coarse Prediction into a Complete First Design

=== Derive which future distinctions an action can ignore

The information example motivates a smaller question; a decision calculation must now show which detail can actually be discarded. Let $a$ be an allowed action and $ell(a,Z)$ its loss under complete future outcome $Z$. Loss may be negative profit. Suppose a finite label $Y=g(Z)$ preserves everything that this loss uses:

$
  ell(a,Z)=tilde(ell)(a,g(Z)) " for every allowed action" a.
$

Group the conditional average by label classes. Inside class $y$, the action loss has the same value $tilde(ell)(a,y)$, so

$
  E[ell(a,Z) mid(|) X]
    &=sum_(y) E[ell(a,Z) mid(|) Y=y,X] Pr(Y=y mid(|) X)
    \
    &=sum_(y) tilde(ell)(a,y) Pr(Y=y mid(|) X).
$

To choose the action minimizing expected loss, we need only the label probabilities. The exact location within a class cannot change this decision because the decision's loss does not distinguish it. This is a sufficient condition, not a claim that every trading payoff is constant within a sign class. It tells us exactly how to check a proposed reduction.

The condition depends on the decision and the available actions. A label sufficient for the expected payoff of one fixed-size contract need not suffice for margin, drawdown control, or an option hedge. Retain the numerical quantities needed for margin, drawdown control, or hedging alongside the binary direction output.

=== A probability, a payoff contract, and a no-trade band

Start with a fixed-size two-outcome teaching contract. A successful long trade gains $G>0$, a failed one loses $L>0$, and entry plus exit costs $c>=0$. If success probability is $p(F)$, its conditional expected net payoff is

$
  A_("long")=p(F) G-(1-p(F))L-c
            =p(F)(G+L)-L-c.
$

Abstention pays zero. Long participation is favorable exactly when

$
  p(F)>frac(L+c,G+L).
$

The payoff comparison determines this threshold directly, giving it an economic interpretation. If the threshold is at least one, this contract offers no positive-expectancy long opportunity under these assumptions.

For a symmetric contract in which an up move gains $g$ for a long and loses $g$ for a short, and a down move does the reverse, let $p(F)$ be up probability. Long, short, and abstention have expected payoffs

$
  A_("long")=g(2p-1)-c, quad
  A_("short")=g(1-2p)-c, quad
  A_("flat")=0.
$

For a long, $g(2p-1)-c>0$ rearranges to $p>1/2+c/(2g)$; for a short, $g(1-2p)-c>0$ rearranges to $p<1/2-c/(2g)$. Whenever the long is positive, $p>1/2$ and long minus short is $2 g(2p-1)>0$, so it also beats the short. The reverse holds when the short is positive. When neither is positive, flat is optimal. If $c>=g$, neither strict threshold can be reached by a valid probability and every action is flat under this toy contract.

Selecting the largest gives the practical rule, with ties assigned to abstention:

$
  a(F)=cases(
    +1 & "if" p>1/2+c/(2g),
    -1 & "if" p<1/2-c/(2g),
    0 & "otherwise".
  )
$

For $g=1,c=0.1$, the thresholds are 0.55 and 0.45. A forecast of 0.52 favors up direction but gives long net expectancy $0.04-0.1=-0.06$; abstention wins. At 0.58 the expectancy is $0.16-0.1=0.06$. Direction and participation therefore answer separate questions. These magnitudes are teaching units; real costs and payouts must come from the stated execution policy.

=== A sign alone does not specify variable payouts

For a general fixed-horizon return $R$, define $p(F)=Pr(R>0 mid(|) F)$ and conditional average gain and loss magnitudes

$
  G(F)=E[R mid(|) R>0,F], quad
  L(F)=E[-R mid(|) R<=0,F].
$

When the relevant classes have positive probability and these averages exist, splitting the conditional mean by the two classes gives

$
  E[R mid(|) F]=p(F) G(F)-(1-p(F))L(F).
$

Thus a long's expected net return is that quantity minus the appropriate cost. At a zero-probability class, its weighted contribution is zero without requiring a conditional average there. If returns are $+1$ with probability 0.6 and $-2$ with probability 0.4, the mean is $0.6-0.8=-0.2$. A 60% up rate is not a profitable long rule.

For a first variable-payout experiment, estimate class-average payouts conservatively from the training period and carry them forward as an explicit initial approximation. Check the averages and net decisions on later data. If their dependence on state materially changes participation, add a restrained conditional-payoff component or meaningful payout classes and test its incremental effect. Costs may likewise depend on state and size. This numerical component supplies the payout information needed by participation while leaving the direction target focused.

=== When exits depend on the path, label the path outcome

An endpoint sign is appropriate only for an endpoint policy. Suppose entry is 100, the profit target is 102, the stop is 98, and the maximum holding time is three steps. Consider the two future paths:

$
  (100,102,101,101), quad (100,98,101,101).
$

Both end at 101 and receive a positive endpoint label. Under the specified first-hit exit, the first trade gains two units and the second loses two. The endpoint target identifies outcomes that this policy must distinguish. It is therefore the wrong label for that policy, regardless of the predictor's sophistication.

Define the first time the future path reaches the upper barrier, the first time it reaches the lower barrier, and the maximum allowed exit time. Exit at whichever occurs first. *First-passage labeling* records whether the upper or lower barrier was reached first; a third class records a timeout. These are commonly organized as the *triple-barrier method*, associated with López de Prado's labeling framework. Chapter 3 develops its volatility-scaled construction and implementation in detail.

If idealized upper and lower outcomes pay $G$ and $-L$, let their probabilities be $p_(+)$ and $p_(-)$. With timeout probability $p_(0)$ and average timeout payoff $M_(0) (F)$, the policy's expected net payoff is

$
  A(F)=p_(+) (F)G-p_(-) (F)L+p_(0) (F) M_(0) (F)-c.
$

The probabilities sum to one. Timeout payoff is not automatically zero, and merging it into a binary target can change the participation decision. Gaps can cross a barrier without a fill at its price; coarse bars may show both barriers touched without revealing their order. In those cases, retain a declared execution and ambiguity rule, or obtain finer observations. The label records the policy outcome; realized cash accounting records the actual fill and cost.

Volatility-scaled barriers use a historical estimate of move scale known at entry to express comparable policies across quiet and volatile periods. Scaling aligns the question; it does not prove that information or predictive accuracy increases in every market. The decisive reason for first-passage labels here is policy alignment: the fixed-horizon target demonstrably merges a win and a loss.

=== A restrained probability model is a concrete starting point

We now have a target and a small feature panel. We can now specify the first experiment's predictor. For a binary label, start with an intercept and a weighted feature sum

$
  s(F)=beta_(0)+beta^(T) F, quad
  hat(p)(F)=frac(1,1+exp(-s(F))).
$

The second map keeps the output between zero and one. Its log odds satisfy $ln(hat(p)/(1-hat(p)))=s(F)$. This is *logistic regression*: linearity applies to log odds, not directly to probabilities. It is a useful first comparator for refined factors because each input has a visible coefficient and the model contains no hidden representation layers. Its interactions are limited, which gives subsequent nonlinear comparisons a clear question to test.

Fit it on completed training examples $(F_(i),B_(i))$ using binary log loss and a coefficient-size penalty:

$
  J(beta_(0),beta)=frac(1,N) sum_(i=1)^(N)
    [-B_(i) ln hat(p)_(i)-(1-B_(i))ln(1-hat(p)_(i))]
    +frac(lambda,2) beta^(T) beta, quad lambda>=0.
$

Natural logarithms change the information unit by a constant; the unpenalized optimum still seeks true class probabilities. The penalty is called *regularization*. It charges for large feature coefficients, while leaving the intercept unpenalized. After columns are placed on comparable scales using training data, $lambda$ has a coherent role in controlling sensitivity to individual columns. It is not an automatic generalization guarantee.

To see what the penalty changes, differentiate $beta^(T) beta=sum_(j) beta_(j)^(2)$ coordinate by coordinate: its gradient is $2 beta$, giving penalty gradient $lambda beta$. It shrinks coefficients in the objective; it does not set the numerical step size. The intercept is absent from this penalty.

The fitting direction can also be inspected. Since $dif hat(p)/dif s=hat(p)(1-hat(p))$, differentiating one example's log loss gives

$
  frac(dif, dif s)[-B ln hat(p)-(1-B)ln(1-hat(p))]=hat(p)-B,
  \
  nabla_(beta) J=frac(1,N) sum_(i=1)^(N) (hat(p)_(i)-B_(i))F_(i)+lambda beta.
$

Here are the chain-rule steps for one example. Write $p=hat(p)$ and $l=-B ln p-(1-B)ln(1-p)$. Then

$
 frac(dif l,dif p)=-frac(B,p)+frac(1-B,1-p),
 quad frac(dif p,dif s)=p(1-p),
 \
 frac(dif l,dif s)=[-frac(B,p)+frac(1-B,1-p)]p(1-p)
 =-B(1-p)+(1-B)p=p-B.
$

Because $s=beta_(0)+sum_(j) beta_(j) F_(j)$, its derivative with respect to $beta_(j)$ is $F_(j)$. Averaging $(p-B)F_(j)$ and adding $lambda beta_(j)$ yields the displayed vector gradient. The intercept gradient is $N^(-1)sum_(i=1)^(N) (hat(p)_(i)-B_(i))$, without a shrinkage term. This derivation identifies the fitting direction but does not by itself guarantee that a chosen update step is safe.

If an up outcome was underpredicted, its contribution pushes the score upward along that example's features; the penalty pulls feature coefficients toward zero. Chapter 6 derives a safeguarded step size for this baseline; Chapter 7 develops optimization more generally. The learning rate controls the numerical move during fitting; $lambda$ changes the fitted objective. They are not interchangeable knobs.

Choose a small, declared set of penalty values on an earlier validation period, then freeze the choice before final temporal confirmation. With standardized columns and the average-loss objective above, an initial grid is $lambda in {10^(-3),10^(-2),10^(-1),1}$. This is a bounded development choice, not a universally optimal scale. Reuse this same fitting and selection budget when comparing representations. After this baseline, compare a restrained nonlinear model only if there is a plausible missing interaction and sufficient independent evidence to test it.

=== The complete first-experiment route

The default is now operational. For a fixed-horizon trend study, use the following sequence:

1. *Specify the opportunity and policy.* Fix the information cutoff, executable entry, eligible observations, horizon, and allowed actions. Construct the direction label from that policy. Save each label's entry and maturity times.
2. *Build a small available state.* Begin with scale-free moves and deviations at a few stated horizons, plus task-specific observations with an economic rationale. Fit scaling and missing-value treatments on the training data only. Keep an input dictionary explaining what each column exposes.
3. *Fit probabilities, not an unexplained score.* Use the penalized logistic model above, binary log loss, and a constant-probability baseline estimated from training label frequencies. Keep parameter selection bounded and earlier than confirmation.
4. *Add the economic gate.* Use the payoff-derived threshold. The symmetric fixed-payout example gives the 0.55/0.45 no-trade band; a variable-payout study uses its gain, loss, and cost estimates instead. A path-exit policy uses first-passage probabilities and retains timeout outcomes. Do not borrow the teaching thresholds for a different contract.
5. *Separate risk from direction.* Hold trade size fixed or use a predefined risk rule in the initial comparison. Direction probability alone does not establish an acceptable exposure. Keep funding, loss limits, and correlated positions as distinct constraints.
6. *Confirm the whole route in time order.* Train earlier, choose parameters on a later development period, and keep a final later period untouched until the route is frozen. No training label may use outcomes extending into the held-out outcome interval; later chapters construct the removal of such overlapping examples. Compare probability loss, probability reliability, and actual net policy results on the same admitted opportunities.

Probability reliability has a simple initial check, called *calibration*. Group held-out forecasts into ranges fixed before inspection. In each range compare the average predicted up probability with the observed up fraction, and report the group's observation count. Forecasts near 0.6 should correspond to roughly 60% up outcomes across comparable repetitions. Group agreement does not establish every conditional relation, and correlated observations reduce precision, but it can expose a confident score that the payoff threshold should not trust.

Report the three tests separately. Lower held-out log loss establishes better probability prediction on that period. Calibration checks whether numerical probabilities have the interpretation the gate needs. Net policy accounting checks whether the selected actions earn enough after their actual payout asymmetry and costs. Each result answers its own question, so the three checks are reported separately. Representation comparisons must include the selection already used to choose features and parameters; inspecting the final period and redesigning converts it into development data.

#principle[*Chapter conclusion:* Our first trend route is a policy-aligned coarse label, a small available feature panel, a restrained probability model, a payoff-derived participation rule, and separate risk control and temporal confirmation. This route concentrates estimation on the distinctions the action uses. As the experiment develops, add observations, representations, model structure, or numerical payoffs to address identified remaining needs.]

#heading(level: 2, numbering: none)[Take This Chapter Forward]

We have explained both halves of the design. Coarse labels reduce the target burden only insofar as they preserve the required decision distinctions. Feature transformations can expose existing information to a limited predictor, while new observations can add conditional information beyond the existing history. Neither operation is validated by an attractive training fit.

Chapter 3 turns the path-policy example into a reproducible labeling construction: historical move scales, barriers, timeouts, delayed outcomes, and participation labels. Chapter 4 establishes data and information timing. Chapter 5 develops the feature panel, and Chapter 6 connects model structure, capacity, and losses. Chapter 7 develops optimization; Chapter 8 connects the discovery and verification pipeline. The common interface is already fixed: available features enter, future policy outcomes provide training labels, probabilities support an economic action, and actual execution determines cash results.

#heading(level: 2, numbering: none)[Self-Check: Can You Construct the Smaller Problem?]

1. Two future paths have the same final price but hit opposite barriers first. Which label does an endpoint policy need, and which does a first-hit policy need?
2. In the three-point construction, compute the best no-input log loss and the best raw-input one-split log loss. Why is their difference not $1-1/3$?
3. A deterministic feature improves a fixed predictor's held-out log loss. Has it necessarily added Shannon information? What comparison isolates its representation contribution?
4. An up outcome pays one unit, a down outcome loses two, and costs are 0.1. What up probability makes a long's expected net payoff positive?
5. You predict the sign well, but positive payouts shrink specifically where the model's probability is highest. What component should be added before reverting to precise-price prediction?

*Answer guide:* For question 1, the endpoint policy uses its endpoint outcome; the first-hit policy must preserve hit order and timeout. For question 2, the losses are $h_(2) (2/3)$ and $2/3$ bits; hard error and log loss are different objectives. For question 3, no: hold the label, model family, fitting budget, and temporal splits fixed. For question 4, solve $p-2(1-p)-0.1>0$, giving $p>0.7$. For question 5, add or stratify the conditional payoff magnitude needed by the participation rule, and confirm its incremental effect.


== Coarse Targets with a Concrete Decision Attached

The information calculation motivates coarse labels, but the practical test is whether a label preserves the distinctions that change an allowed action. We now apply that test to the three experiments. Numerical probabilities and prices below are invented to expose the decision algebra; they are not estimates of a market edge.

=== Why direction is the usual first trend target

If an allowed trade earns gain $G$ on an up outcome, loses $L$ on a down outcome, and pays cost $c$, its expected net result is $p G-(1-p)L-c$. The participation threshold is $p>(L+c)/(G+L)$. Exact tomorrow-price digits do not enter this expression. Therefore start by estimating the probability of the relevant coarse outcome, and retain payoff magnitudes in a separate economic comparison. The payoff calculation provides a positive reason for this design.

Suppose a liquid-market prototype has symmetric 20-basis-point outcomes, one basis point of total cost, and up probability 0.56. A basis point is one hundredth of one percent. Expected net return is $0.56 times 20-0.44 times 20-1=1.4$ basis points, with threshold 0.525. A thin-token prototype with symmetric 200-basis-point outcomes and 40 basis points of costs has the same probability but expected result $24-40=-16$ basis points; its threshold is 0.60. The economic margin depends on the combination of probability, payout, and cost, even when the chart shows dramatic movement.

*Decision:* direction probabilities are the first trend forecast; cost and payoff state decide participation. Do not demand an exact-price forecast to recover a bias the action only needs as a probability. Do not discard magnitude when comparing economically different trades.

=== Why A-share relative selection may need ranks rather than signs

Consider three feasible next-session returns: 3%, 1%, and 2%, when the comparison portfolio earns 2%. All three have positive sign. A sign classifier cannot distinguish the asset that adds relative value from the one that subtracts it. Relative labels order the assets, while holding constraints decide whether the result is an overweight, an underweight, or no position.

For this experiment, define the investable comparison set at the decision cutoff, rank *feasible future returns*, and fit a date-grouped ranking objective. The target must reflect the entry/exit policy, not close-to-close returns if the actual policy enters later. Keep a simple continuation score and its sign-reversed counterpart as development controls. A trader's account of sector rotation motivates the comparison; the chronological experiment evaluates its orientation.

=== Why event success can be better than the next bar's sign

Suppose a crypto event rises briefly after the signal and then falls before a delayed buyer can sell. Predicting the next one-minute sign could be accurate yet irrelevant to the selected policy. Define a target such as “the frozen entry/exit policy completes with positive net payout,” and preserve the path, fill failures, timeout, and losses that produced it. This is meta-labeling only when the primary side is already fixed; otherwise it is a policy-outcome classification task. Neither label certifies that an event was manipulation.

The initial event detector uses only completed observations. A concrete development starting rule is an upward five-minute return exceeding three historical five-minute standard deviations and volume exceeding twice its trailing comparable-window median. These constants are a small teaching search specification, not empirical thresholds. Compare against matched liquid opportunities at similar times, keep overlapping events in the same evidence block, and freeze the final rule before confirmation. Never use it to solicit or coordinate a pump.

=== Why a token/reference gap is a different target

Let $T$ be a token quote, $S$ a reference share quote, and $a$ the documented share-equivalent multiplier per token, all converted to the same currency. Define the observed proportional gap $b=frac(T,a S)-1$. At a reference close of 100, token quotes of 103 and 106 imply gaps of 3% and 6%. But if the next reference price is 105, much of the apparent gap could have been information about the reference, not a token pricing error.

To see the distinction algebraically, write $T=a S(1+b)$ with a constant multiplier over the illustrated interval. Taking log ratios gives

$
  ln frac(T_(1),T_(0))=ln frac(S_(1),S_(0))+ln frac(1+b_(1),1+b_(0)).
$

Token appreciation combines the reference move and the change in relative gap. These two components give token direction and convergence their distinct targets. If both legs and conversion are executable, a convergence policy needs its two-leg payoff and costs. If the reference market is closed, begin with a session-conditioned token-return or later reopening-outcome study, not a fictional immediately hedged arbitrage.

*Target-design conclusion:* choose the lowest-detail label sufficient for the decision actually available. For ordinary trend this is usually direction or policy success; for relative stock selection it is rank; for a genuinely executable relative-value trade it is the relation's payoff. Assess usefulness through the supported decision as well as the reduction in target entropy.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Yilun Xu, Shengjia Zhao, Jiaming Song, Russell Stewart, and Stefano Ermon. #link("https://arxiv.org/abs/2002.10689")[_A Theory of Usable Information Under Computational Constraints_]. ICLR, 2020. Definitions 1–3 introduce predictive families, the ability to ignore side information, and predictive $cal(V)$-information.
- Claude E. Shannon. #link("https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf")[_A Mathematical Theory of Communication_]. _The Bell System Technical Journal_ 27, 379–423 and 623–656, 1948. The classical foundation for entropy and information.
- Marcos López de Prado. #link("https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/finance-investments-special-topics-13fiz/advances-in-financial-machine-learning-978-1-119-48208-6")[_Advances in Financial Machine Learning_]. Wiley, 2018. Chapter 3 treats financial labeling; Chapters 4 and 7 develop overlapping-outcome and validation issues.
]

#pagebreak()

= Labeling and Decision Decomposition: Represent Achievable Outcomes
#counter(math.equation).update(0)

A label becomes useful by describing the trade the policy actually makes. When the policy closes at the first stop or profit target, its outcome is determined along the path, so we begin by making the exit policy part of the label. We then separate four objects that are easily confused: a historical outcome class, its forecast probability, an economic participation score, and a position.

The worked policy is daily futures timing, motivated by the copper example. Its constants are chosen teaching settings; their empirical performance and optimality remain to be evaluated. We use actual contracts and explicitly observed execution opportunities. Chapter 4 constructs the data view; Chapter 5 supplies the features; Chapter 6 specifies restrained models.

== Construct a Path Question from an Exit Policy

=== Start with a reference that could actually be traded

Let $t$ be the information cutoff and $e_(t)$ the executable entry time after it. Let $P_(e_(t))$ be the entry reference, and define the subsequent simple return path for the same contract:

$
  R_(t,s)=frac(P_(s)-P_(e_(t)),P_(e_(t))), quad s>e_(t).
$

For a standardized long policy, fix upper return distance $u_(t)>0$, lower distance $d_(t)>0$, and monitoring deadline $v_(t)$. The label asks which exit condition becomes true first, following the trade up to the point where the policy closes it.

Define the first observed upper and lower hit times:

$
  tau_(+) (t)=inf {s>e_(t):R_(t,s)>=u_(t)}, quad
  tau_(-) (t)=inf {s>e_(t):R_(t,s)<=-d_(t)},
  \
  tau(t)=min(tau_(+) (t),tau_(-) (t),v_(t)).
$

An infimum here means the earliest eligible time; an empty hit set has time $infinity$. For a discrete observation grid, this is just a chronological scan. The trigger duration is $tau(t)-e_(t)$; actual holding duration ends at the executed exit defined below. Unlike a fixed horizon, the trigger depends jointly on the path and the policy. Such a path-dependent first-hit time is called a *first-passage time*.

Assign label $+1$ if the upper exit occurs first, $-1$ if the lower occurs first, and $0$ for timeout. Fix the tie convention before generating labels. In our close-observed prototype, a barrier hit at the last eligible close takes precedence over timeout. A finished timeout is a known policy outcome. A sample whose horizon extends beyond the dataset is *unfinished*, not a timeout with label zero.

Save the trigger interval $[e_(t),tau(t)]$ and the full realized-policy interval $[e_(t),e_(t)^("exit")]$, where $e_(t)^("exit")$ is the actual executed exit time, possibly later than the trigger. Overlap checks for economic outcomes must extend through that fill, not stop at the trigger. The hit class matures when its required observations are known; a payout or meta-label must also wait for the fill and cost records. Two examples can share future observations even if their decision dates differ. A model update on Tuesday cannot use a trade that ends on Friday merely because a retrospective file already contains its Friday label.

=== Scale the question with a known move scale

A fixed 2% barrier means something different when typical daily movement is 0.5% than when it is 3%. To make the policy comparable in relative movement units, first construct a historical one-day volatility estimate.

For the last $w$ available same-contract daily simple returns $r_(t-j)$, use

$
  overline(r)_(t)=frac(1,w) sum_(j=0)^(w-1) r_(t-j), quad
  hat(sigma)_(t)^(2)=frac(1,w-1) sum_(j=0)^(w-1) (r_(t-j)-overline(r)_(t))^(2).
$

Why does estimating the mean cost one degree of freedom? For independent historical returns with a common mean $mu$ and variance $sigma^(2)$, expand around $mu$:

$
 sum_(j=0)^(w-1) (r_(t-j)-overline(r)_(t))^(2)
 =sum_(j=0)^(w-1) (r_(t-j)-mu)^(2)-w(overline(r)_(t)-mu)^(2).
$

The cross terms cancel because the centered sample deviations sum to zero. Taking expectations gives $w sigma^(2)-w Var(overline(r)_(t))$. Independence gives $Var(overline(r)_(t))=sigma^(2)/w$, leaving $(w-1)sigma^(2)$. Division by $w-1$ therefore estimates variance without bias under this stated model. Market dependence or changing variance breaks this simple justification; the same rolling formula then remains a declared local dispersion statistic rather than a theorem about tomorrow.

Here and below a bar over a variable denotes its average. The denominator $w-1$ is the conventional sample-variance choice. This estimates recent dispersion; it does not establish constant future volatility. Require sufficient valid observations. A zero or unusable scale triggers an explicit unavailable-policy state rather than division by zero or an invented normal sample.

Our initial policy uses $w=20$, a maximum of ten sessions after entry, and

$
  u_(t)=2 hat(sigma)_(t), quad d_(t)=2 hat(sigma)_(t).
$

These barriers are two *one-day* historical standard deviations, not two ten-day standard deviations. They are fixed at entry, so future changes in volatility cannot silently move the question after it has been asked.

Why distinguish these units? For centered increments $r_(1),...,r_(h)$, basic variance algebra gives

$
  Var(sum_(j=1)^(h) r_(j))
    =sum_(j=1)^(h) Var(r_(j))+2 sum_(i<j) Cov(r_(i),r_(j)).
$

The variance identity comes from squaring the centered sum: each individual squared deviation contributes a variance, and every distinct cross-product occurs twice and contributes a covariance. Simple returns compound as $1+R_(h)=product_(j=1)^(h) (1+r_(j))$. Expanding this product gives $R_(h)=sum_(j) r_(j)+sum_(i<j) r_(i)r_(j)+dots.h$. Replacing the compounded return with the sum drops those second- and higher-order products. Log returns instead add exactly, but require a consistently log-scaled barrier policy.

If variances equal $sigma^(2)$ and cross-covariances vanish, the sum has standard deviation $sigma sqrt(h)$. For small simple returns this sum approximates the multi-period return. Dependence, changing variances, and compounding can invalidate that approximation. Thus a fixed barrier $u$ has relative horizon distance roughly $u/(sigma sqrt(h))$ under these conditions; scaling with the relevant known move scale preserves a declared relative policy. It does not license multiplying every volatility estimate by $sqrt(h)$ regardless of what it measures.

#principle[*Selected label:* Use volatility-scaled first-passage outcomes for the profit/stop/timeout policy. Scaling makes the question comparable; first passage makes it describe the selected exit. The resulting predictive information still depends on the observations and data.]

== Decide What Was Observed and What Was Filled

=== A close-observed prototype is an executable monitoring policy

The initial prototype observes completed daily closes and, when a condition becomes true, exits at the next declared executable opportunity. This schedule describes close-based monitoring; an intraday resting stop would require a different execution replay. Record the trigger close, actual exit time, fill reference, and realized payoff separately. If the execution venue permits a different order schedule, that schedule defines a different replay.

For example, entry 100 and upper trigger 102 may be followed by next-opportunity fill 101.5. The path class is upper-first, while realized gross gain is 1.5 units, not two. Conversely, a gap to 97 after a lower trigger at 98 can create a three-unit loss. When trigger and execution differ, estimate class-conditional *realized* payoffs; do not substitute ideal barrier distances into the economic gate.

An implementation wanting intrabar barriers needs intrabar observations and an order/fill convention. If a daily bar's high is above the target and its low below the stop, those two extremes do not reveal which occurred first. Mark that ambiguity, use finer data, or adopt a conservative rule specified in development. Selecting the favorable hit order manufactures performance. A gap fill is not a mathematical first contact at a price the market never offered.

=== Store the outcome, not merely its code

For each opportunity retain: decision and entry times, contract identity, historical scale, barrier distances, horizon, hit class, trigger time, executed exit, gross payoff, costs, and status. A status distinguishes valid, unfinished, ambiguous, untradable, and invalid-data outcomes. Save the policy version as well: changing a stop changes the future outcome being labeled.

Before generating a large label set, inspect four small paths: upper-first, lower-first, timeout, and unfinished. Add a double-hit bar and an adverse gap for the chosen execution variant. A fixture checks implementation against the policy. The policy's empirical edge is evaluated later on market data.

For a close-observed first prototype, the procedure is:

1. At the information cutoff, freeze scale and policy parameters; determine the executable entry reference.
2. Scan subsequent eligible closes in time order until the first barrier condition or the tenth-session deadline.
3. Resolve last-close ties using the fixed convention. If required observations are missing or the horizon is not complete, preserve the corresponding status.
4. Apply the declared exit-order schedule, then record actual price change, contract multiplier, and costs.
5. Make the completed outcome available to training only after its required records have arrived.

== From Class Probabilities to an Economic Score

=== Learn a distribution before using it

A three-class predictor returns $p_(+),p_(-),p_(0)>=0$ summing to one. Integer codes such as $-1,0,+1$ identify the outcomes; their cash meaning comes from the payout attached to each class.

One concrete baseline gives each class a score $z_(k)=beta_(k,0)+beta_(k)^(T) F$ and maps them to probabilities:

$
  p_(k) (F)=frac(exp(z_(k)),sum_(j in {-,0,+}) exp(z_(j))).
$

This normalization is called *softmax*. Adding the same constant to every score changes no probability, because it multiplies numerator and denominator equally. Fix one reference score to zero, or another declared constraint, to remove this redundant parameterization. Fit class log loss $-ln p_(Y)$ with restrained coefficients. The same conditional log-loss decomposition as Chapter 1 makes the ideal unconstrained output the true class distribution. It does not make fitted finite-sample probabilities automatically reliable.

For completeness, the normalization also supplies an inspectable fitting derivative. Put $Z_(s)=sum_(j) exp(z_(j))$. One observed class $Y$ has loss $-ln p_(Y)=-z_(Y)+ln Z_(s)$. Differentiating with respect to score $z_(k)$ gives

$
 frac(partial (-ln p_(Y)),partial z_(k))
 =-bold(1)[Y=k]+frac(exp(z_(k)),Z_(s))
 =p_(k)-bold(1)[Y=k].
$

Thus each class's probability error multiplies the feature vector in its coefficient gradient. Adding constant $a$ to every score multiplies every exponential by $exp(a)$, which cancels; this is why fixing a reference score removes a genuine redundancy. For stable arithmetic, subtract the largest score before exponentiating; probabilities stay identical while overflow is avoided. The reference constraint identifies the parameters; a separate calibration check evaluates the fitted probabilities.

Let $G(F)$ be average realized gain in the upper-first class, $L(F)$ the magnitude of average realized loss in the lower-first class, and $A_(0) (F)$ the average timeout payoff, in a common payoff unit. Under the corresponding class definitions,

$
  A(F)=p_(+) (F)G(F)-p_(-) (F)L(F)+p_(0) (F)A_(0) (F)-c(F).
$

This follows by grouping the expected realized payoff by the three classes. If a class's average payoff has the opposite sign, store the signed average instead of forcing the gain/loss notation. In the ideal fixed symmetric barrier contract, $G=L=g$ and $A_(0)=0$, giving $A=g(p_(+)-p_(-))-c$. The shortcut follows from those symmetric-payout and zero-timeout assumptions; general fills and timeouts use the full class-payoff expression.

For a numerical example, let $(p_(+),p_(-),p_(0))=(0.4,0.3,0.3)$, $G=2$, $L=3$, $A_(0)=0.2$, and $c=0.1$. Then expected net payoff is $0.8-0.9+0.06-0.1=-0.14$. More upper-first than lower-first probability does not justify participation.

Use class averages from completed training outcomes as the initial payout approximation. State-dependent magnitudes that materially change decisions provide a reason to investigate a conditional payout model. Reversed directions under asymmetric stops may have different first-passage policies; simulate each candidate's actual policy rather than negating a code whose payoff semantics no longer match.

#principle[*Four objects:* Labels describe completed paths; probabilities describe predicted class frequencies; economic scores combine those probabilities with payouts and costs; positions add size, capital, and risk constraints. Work through these conversions in sequence to connect a forecast to a feasible position.]

== Meta-Labeling: Freeze Direction, Learn Participation

=== Protect a useful direction prior

Suppose a primary rule supplies $s(F) in {-1,+1}$, such as the sign of twenty-session momentum. Freeze this rule before a gate comparison. At zero momentum, our first version proposes no candidate. Simulate the candidate trade in its proposed direction with the stated profit/stop/timeout policy. A binary *meta-label* records whether that candidate satisfies a declared success criterion; a second, smaller model predicts its success probability.

For the first gate, use success as positive realized net payoff. Save actual successful and unsuccessful payoff magnitudes as well as the binary outcome. If $G_(m)>0$ is the average net gain on success and $L_(m)>=0$ the average net loss magnitude otherwise, the gate's expected net payoff is

$
  A_(m) (F)=p_(m) (F)G_(m) (F)-(1-p_(m) (F))L_(m) (F).
$

No cost is subtracted again: these magnitudes are already net. Alternatively, defining success classes and payout averages before costs requires subtracting the corresponding cost once. Keep one convention. In the simple fixed gross gain/loss illustration from Chapter 2, the threshold is $(L+c)/(G+L)$; with net class averages it is $L_(m)/(G_(m)+L_(m))$. The two thresholds express the same grouping operation under different cost conventions.

The meta-model may see the primary side and a restricted state panel. It answers *whether to take this proposed trade*, keeping the primary direction in place. Initially use an on/off gate with a fixed or separately risk-scaled size. A map from probability directly to continuously optimized size is an additional modeling decision, not part of binary participation by definition.

=== What exactly has become smaller?

Let $cal(M)$ be the allowed participation functions. With the side fixed, candidates have the form

$
  q(F)=s(F)m(F), quad m in cal(M), quad 0<=m(F)<=1.
$

For a binary gate, $m$ is zero or one. The system cannot reverse a proposed direction, create an omitted opportunity, or enlarge size beyond its declared cap. Relative to a larger class that includes all these possibilities, we have explicitly removed actions. Removing those actions gives a concrete reason to expect a reduced selection burden.

Searching for the primary side, selecting gate features, and choosing thresholds still consume data. A highly complex primary model plus a highly complex binary gate need not be a small system. The first comparison therefore freezes the primary rule and restricts the gate to a few economically motivated features and a restrained classifier.

If the primary model is learned, build gate-training examples from *out-of-sample primary predictions*. On each historical development block, train the primary only on earlier completed outcomes, predict the next block, and record the proposed trade's subsequent result. Pool these forward-generated examples for gate development. A primary's in-sample near-perfect directions would give the gate a different opportunity distribution from deployment. Final confirmation trains and tests the entire two-stage route without borrowing later labels.

=== A gate cannot recover candidates never proposed

Define an independent opportunity set and a success criterion before evaluating selection. *Precision* is the fraction of proposed/accepted opportunities that satisfy that criterion. *Recall* is the fraction of qualifying opportunities in the defined set that were proposed/accepted. A broad candidate generator may sacrifice precision to retain recall; the gate then filters. It can also reject true successes, so improved precision alone is insufficient. Compare net outcomes, retained successes, turnover, and risk with and without the gate on the same primary opportunities.

Recall and precision describe complementary parts of the selection result. Even a high-recall generator can omit some successful opportunities. Threshold estimation or search adds development uncertainty and selection cost to that result.

== Ranking and Event Outcomes Need Their Own Boundaries

For relative selection, fix the investable universe $U_(t)$ at the decision time, the horizon, and tie handling. Let $r_(i,t)$ be each member's subsequent return. One explicit normalized midrank target is

$
  y_(i,t)=frac(
    sum_(j in U_(t)) [bold(1)[r_(j,t)<r_(i,t)]+frac(1,2)bold(1)[r_(j,t)=r_(i,t)]],
    |U_(t)|
  ).
$

For distinct returns ordered as $1\%,2\%,3\%$, the numerator is respectively $0+1/2$, $1+1/2$, and $2+1/2$. Division by three gives $1/6,1/2,5/6$. For $1\%,1\%,3\%$, each tied lower asset has zero strictly smaller observations and two equal observations, giving $(0+2/2)/3=1/3$; the upper asset remains $5/6$. The formula includes the asset itself among equal observations, which explains the half-step offset rather than endpoints zero and one.

The indicator is one if its condition is true and zero otherwise. A tied group receives the same midpoint fraction; if all returns tie, every label is one half. An asset's label depends on the contemporaneous comparison set, not only its own return. Rankings retain relative order but erase spacing: returns $(1,2,3)$ and $(1,2,30)$ have the same ordering and different portfolio payoffs. Evaluate the eventual holdings, not only ranks.

An event sample is indexed by a defined announcement, trigger, or event process rather than every calendar day. Multiple updates about the same event may share one outcome and information interval. Record event identity, information cutoff, completion time, and tradability. Repeating an event's rows does not create independent evidence or breadth.

#heading(level: 2, numbering: none)[Practical Default and Checks]

For daily copper-style timing, use a twenty-return historical one-day scale, upper/lower distances of two such scales, and a ten-session deadline. Begin with close-observed monitoring and explicitly later executable exits. Store class, outcome interval, and actual payout. Fit three-class probabilities; use the class-payoff average as the participation score. For the first meta comparison, freeze twenty-session momentum side and fit a small gate using forward-generated primary directions. Chapter 6 gives model settings. Change policy constants only as a recorded development comparison.

Before fitting, verify by hand that upper-first, lower-first, timeout, unfinished, ambiguous, and adverse-fill cases receive the intended distinct records. Before claiming a gate helps, compare the same primary policy with and without it after costs. These defaults preserve the direction/participation/risk decomposition while making the policy and its accounting inspectable.

*Self-check:* A timeout gains 0.5 units. Can it be assigned payoff zero merely because its class code is zero? If the primary's learned predictions were generated on its own training data, can they be reused unchanged for gate training? In both cases the answer is no: the first confuses an identifier with money; the second changes the evidence available to the historical candidate generator.

#principle[*Chapter conclusion:* Build policy-aligned outcomes first. Use probability estimates to compare economic participation, and keep risk sizing separate. For a trusted frozen direction, meta-labeling gives a constrained filtering design. Comparing it with the same ungated policy establishes whether the two-stage approach helps.]


== Three Path Fixtures That Change the Label

Policy-aligned labels become concrete when a seemingly obvious chart label is forced to disagree with an executable outcome. The following fixtures should exist before bulk label generation.

=== A-share fixture: an intraday profit barrier you cannot sell into

Assume an ordinary share bought at 10.20 cannot be resold during that session, and no prior sellable inventory is available. Its later intraday price reaches 10.60, but the frozen next-session exit executes at 9.40. A naive 2% upper barrier labels the intraday path a success. The executable return is instead $frac(9.40-10.20,10.20) approx -0.0784$, before costs.

The replay needs a sale-eligibility state that implements “T+1”: postpone exits until they are permitted and continue recording risk during the locked interval. This also corrects the payout that the label describes. A stop trigger can occur while selling is unavailable; its execution time is later. Pre-existing inventory is a different fixture with an explicitly different quantity ledger. This follows the settlement/turn-around distinction in the SSE rules; actual account and historical instrument permissions must be resolved, not assumed from the example.

*First policy:* observe a completed session, enter on the specified next feasible schedule, and measure an eligible later exit. Develop an intraday inventory policy separately. Do not mix its labels with new-inventory labels merely because the same stock code appears.

=== Crypto fixture: terminal direction is right, the position is gone

For a simplified linear long contract, let entry price be $P_(0)$, quantity $q>0$, initial collateral $C$, current mark $M$, and maintenance fraction $m$. A mark is the venue's valuation used for margin accounting, not necessarily the last traded price. Ignoring fees and funding only for this fixture, account equity is $C+q(M-P_(0))$ and the assumed required maintenance is $m q M$. The maintenance boundary solves

$
  C+q(M-P_(0))=m q M,
  quad M_("boundary")=frac(q P_(0)-C,q(1-m)).
$

The intermediate algebra is $C+q M-q P_(0)=m q M$, hence $q(1-m)M=q P_(0)-C$. Division requires $q>0$ and $m<1$. For this simple long-account fixture, equity minus maintenance increases with mark price at slope $q(1-m)>0$, so marks below the boundary breach maintenance. This monotonicity is specific to the stated linear contract and collateral model; it cannot simply be carried over to inverse contracts.

With $q=1,P_(0)=100,C=10,m=0.01$, the boundary is about 90.91. A mark path $100 arrow.r 89 arrow.r 105$ reaches it before the favorable terminal price. A label based solely on the final 5% gain therefore describes a position that this account could not retain. The calculation is illustrative: real venues have contract-specific tiers, collateral haircuts, fees, partial liquidation, and operational rules. A collateral haircut recognizes less than the full marked value as usable security for the position. Kraken's contract documentation distinguishes margin marking, reference indices, and funding; its parameters must not be replaced with our toy constants.

*First policy:* establish the unleveraged outcome first. Add derivatives only with mark/index histories, funding events, and a path-solvency fixture. Label actual policy completion and payout, including a failed liquidation or forced exit, rather than silently removing these observations.

=== Token fixture: apparent convergence without a realizable hedge

Suppose the token asks 103 while the reference's last quote is 100, and the next reference opening quote is 104. Calling the original gap an arbitrage profit assumes that 100 was available to the hedge at the token decision time. It was not if that market was closed. Record reference age and executable leg availability. The outcome of an unhedged token purchase, a later paired trade, and issuer redemption are three separate policies.

Start the wrapper study with one permitted spot token and a scheduled later exit. For the paired comparison, specify borrow, both execution windows, transfer/redemption conditions, and costs so that each leg can be replayed. A perpetual on the token adds another contract layer; its trigger and funding policy cannot be inherited from the spot-token label.

=== Turn the fixtures into a label-producing procedure

For each historical opportunity: check eligibility; assign information and receipt cutoffs; simulate the declared later entry or record no fill; advance cash, inventory, mark, funding, and exit permissions; trigger the first policy condition; attempt its permitted execution; and record final payout and maturity. Record an unfilled opportunity as such, with entry availability separate from conditional trade success. The complete policy evaluation can then include missed opportunities as well as filled trades.

The record should include `opportunity_id`, `instrument_contract`, `entry_status`, `first_trigger`, `trigger_time`, `exit_eligible_time`, `executed_exit`, `net_payout`, and `label_available_time`. First-passage labels are useful because they align the target with a trade's structure. The same structure includes inventory locks, gaps, and solvency limits, which remain part of its replay.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Marcos López de Prado. #link("https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/finance-investments-special-topics-13fiz/advances-in-financial-machine-learning-978-1-119-48208-6")[_Advances in Financial Machine Learning_]. Wiley, 2018. Chapters 3, 4, and 7 cover labeling, overlapping outcomes, and validation.
- Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani. #link("https://www.statlearning.com/")[_An Introduction to Statistical Learning, with Applications in R_]. Second edition, Springer, 2021. Classification and model assessment provide complementary background.
- Shanghai Stock Exchange. #link("https://english.sse.com.cn/start/sserules/stocks/trading/c/10825757/files/d263e3a87f37436ca2f8e5bcfc4ff001.pdf")[_Trading Rules (2026 Revision)_], Articles 3.1.4–3.1.5. Settlement and intraday turn-around distinctions.
- Kraken MTF. #link("https://support.mtf.kraken.com/hc/en-us/articles/25499987607837-Linear-Contract-Specifications")[_Linear Contract Specifications_]. Mark, index, funding, and instrument-specific margin definitions; checked 11 October 2026.
]

#pagebreak()

= Data and Information Timing: Correctness Starts with the Research Object
#counter(math.equation).update(0)

A feature formula can be algebraically correct and historically impossible. Inventory for Monday may arrive on Tuesday. Today's index members may exclude yesterday's failed companies. A smooth futures chart may jump between contracts that a position never held continuously. Each difference changes the observations, opportunities, or cash flows represented by the experiment, so it belongs in the research definition.

Our default is an auditable as-of view of immutable source records, a historical opportunity set, and a mapping from research series to actual holdings. Establish these objects first, then choose a data platform suited to the workload. Their time and identity semantics need to be specified whichever file format or database we use.

== “About Monday” Does Not Mean “Known on Monday”

=== Separate occurrence, availability, and version

Suppose an inventory observation describes Monday, is first received Tuesday morning with value 80, and is corrected Thursday to 75. A current table containing only Monday and 75 lets both the late publication and the correction travel backward through time.

Represent a record with persistent object identity, field, event identity/time $e$, actual availability time $k$, version $v$, value, and status. Event time says what the record concerns. Availability says when the research process could use it. Version distinguishes successive records about that same object and event.

#block(breakable: false)[#table(
  columns: (1fr, 1.2fr, 0.6fr, 0.6fr),
  table.header([Event described], [Available from], [Version], [Value]),
  [Monday inventory], [Tuesday 09:00], [1], [80],
  [Monday inventory], [Thursday 09:00], [2], [75],
)]

An as-of Tuesday 08:00 query returns no available value; Tuesday 10:00 returns 80; Thursday 10:00 returns 75. Sorting by event date alone cannot implement these answers.

For a fixed object–field–event key, first restrict records to $k<=t$, then select the latest available version according to the declared revision ordering. In the simple uniquely timestamped case,

$
  j^(*) (t)=argmax_(j:k_(j)<=t) k_(j), quad x_(t)="value of record" j^(*) (t).
$

No admissible record means unavailable, not zero. Ties require a deterministic version/source rule. Some sources revise ranges of earlier events or cancel a record. Preserve those operations within the relevant event identities, where the revision order has meaning.

The effective $k$ includes delivery, validation, and any computation needed before a feature can be used. Public release time can be earlier. A forecast about a future event may legitimately be available before that event; do not universally require $e<=t$. If a field purports to measure completed historical activity, its event interval must also satisfy that meaning. Availability and event semantics are two separate conditions.

=== A training label also has an availability time

Let $cal(I)_(t)$ denote the information actually available by $t$. This notation collects the available observations without adding a statistical assumption. A decision's features and parameters must be constructed from the applicable $cal(I)_(t)$. A historical outcome ending at $tau$ cannot enter a model update before its result is available, even if a later dataset places it in the decision-time row.

For a model fitted at cutoff $T$, eligible labeled examples satisfy

$
  k_(i)^(("label"))<=T,
$

as well as the fitting protocol's time and separation rules. For a prediction at $t$, its feature records and fitted model must both have been available then. Checking label availability alongside row chronology establishes whether each historical model was fitted with outcomes that had already matured.

#principle[*Timing rule:* Query by actual availability and record identity. Preserve the original versions. Together, these choices reconstruct the information a historical decision could have possessed.]

== Reconstruct the Population That Could Be Chosen

Let $U_(t)$ be the assets eligible for the stated strategy at time $t$. Replaying past dates with today's members $U_(T)$ conditions the experiment on future membership and survival. Even flawless prices now describe the wrong opportunity set.

Consider two assets initially worth 100. Over the evaluation interval, A ends at 110. B exits the universe with a declared final cash recovery of 50. The equally weighted initial basket returns

$
  frac(1,2)(10% -50%)=-20%.
$

Keeping only the eventual survivor A reports +10%. The population filter alone creates the 30-percentage-point discrepancy. Removing B also changes cross-sectional labels: relative ranks were defined among the assets actually eligible then.

Store historical membership as intervals, keeping both announcement and effective-time semantics. Depending on the task, eligibility includes listings, delistings, suspensions, contract expiries, trading sessions, and short availability. A quoted price does not establish an executable opportunity. A missing final return does not authorize deleting an asset that belonged to the original holding set.

Distinguish unavailable observation, nonexistent instrument, temporarily untradable instrument, and a genuine numerical zero. “Fill missing with zero” merges these states and can invent both signals and trades. In a first prototype, keep a status and decline opportunities requiring unavailable measurements. When imputation is justified, specify it as a representation operation fitted on earlier training material, keeping its historical inputs traceable.

== Bridge a Research Price Series to Actual Cash

=== Stock actions change quantities as well as prices

One share at 100 undergoes a two-for-one split. Two shares at 50 still represent wealth 100. A naive price return of -50% is not the holding return. If the two new shares subsequently pay one unit of dividend each, the holding's wealth is 102 before any other change.

For this simple cash-and-stock account,

$
  W_(t)=q_(t) P_(t)+C_(t), quad
  Delta W=W_("exit")-W_("entry").
$

Here $C_(t)$ is cash, including admitted dividends and trades; $q_(t)$ changes under the split. Actual accounting must respect the timing of each entitlement and payment. The formula separates quantity events from price changes, allowing each adjustment to enter the account through its actual mechanism.

Adjusted series are useful research representations. But a history expressed in today's per-share units can incorporate later scale changes. A ratio may cancel a common scale: multiplying both $P_(t)$ and $P_(t-w)$ by $a>0$ leaves their ratio unchanged. An absolute price threshold of 80 does not cancel that scale. Check the specific feature and action formula. The relevant safety judgment therefore concerns the particular operation and its scale dependence.

Keep actual prices, quantities, corporate actions, and dividends alongside the research representation. Use the actual records for holdings and cash reconstruction, with a declared bridge linking them to the research representation.

=== A continuous futures chart is not one contract

A continuous series joins different maturities. Suppose the old contract moves from 100 to 101, then is closed. The replacement is opened at 105 and later closed at 106. With one contract and unit multiplier, actual gross futures P&L is

$
  (101-100)+(106-105)=2,
$

before roll and other costs. A naive joined price change from 100 to 106 is six. The four-unit maturity spread at the splice is not automatically an earned holding return. Futures accounting uses contract price changes and settlement; it does not assume the entire quoted notional is paid like a stock purchase.

Retain a roll ledger: old and new contract identities, timestamps, quantities, multipliers, fills, costs, and the rule selecting the roll. A rule that retrospectively chooses whichever contract later became most liquid can itself leak future selection. The switch must be decided using information and eligibility available at that time.

Back-adjusted or ratio-adjusted continuous series can support certain indicators. Verify which relations the splice preserves and whether windows cross a contract change. The real-asset ledger determines the cash outcomes. Curve slope is separately an observation of simultaneous maturity prices, not an already realized roll profit.

== Alignment and Cleaning Are Part of the Question

=== Join what was available, not whichever timestamp is nearest

A trade is received at 10:00:00.100; a quote stamped 10:00:00.090 reaches the process at 10:00:00.200. At receipt time .100 the later-received quote is unavailable, despite its earlier event timestamp. A nearest-event-time join can therefore assign a future observation to the trade decision.

For the initial as-of join, select the most recent admissible observation received no later than the decision cutoff, subject to the field's event-time meaning and a stated staleness limit. Store both age and status. A carried-forward book retains its age and stale status, which affect whether the opportunity is usable. Clock conventions, time zones, session boundaries, and latency policies must be consistent across sources.

Similarly, traded quantity is realized flow, whereas displayed depth is a cancelable stock. Adding snapshots of depth as though they were executed volume changes the measurement. Repeated quote updates may refer to the same resting liquidity. A feature's data dictionary identifies whether it aggregates executions, snapshots, messages, or changes in state.

=== Fit transformations within the historical information set

Suppose a linear model needs standardized column $x$. Estimate mean and dispersion on the training period:

$
  z_(i)=frac(x_(i)-mu_("train"),s_("train")).
$

Apply those frozen parameters later. Estimating them from the entire future evaluation period lets later observations influence earlier features. Quantile cutoffs, learned missing-value replacements, and dimensionality reduction have the same dependency problem. A rolling transform can instead update using a specified past-only window; its convention must be identical in development and replay.

Same-date cross-sectional scaling is different: if all required assets and values are available at that cutoff, the date's cross-section is legitimate context. This does not permit future members or later releases into that date. Temporal windows must run within the right asset/contract, sorted by the right time, with declared treatment of session gaps. The asset identity, session order, and gaps give row order its economic meaning.

#heading(level: 2, numbering: none)[Practical Default: A Small As-Of View]

Start with immutable originals and a minimal schema: `asset_id`, `field`, `event_id`, `event_time`, `available_time`, `version`, `value`, and `status`. Use persistent contract identity for futures. Materialize an as-of feature view and a historical investable-universe view separately. Keep a cash/roll ledger beside research price representations. Record source and transformation versions so that a replay can reconstruct which inputs it used.

At small scale, partitioned columnar files with a version manifest are sufficient. Choose a database when repeated query workload warrants it; storage choice does not change the as-of operation. Key cached results to the relevant input, policy, and transform versions, so changes in labels or universe definitions produce the corresponding matrix.

Before building the large matrix, run four hand-inspectable checks:

1. Delayed release and revision: queries before Tuesday, on Tuesday, and after Thursday must respectively return unavailable, 80, and 75.
2. Historical universe: the failed member must remain in its earlier opportunity and holding set, including the declared final recovery.
3. Split and dividend: quantity and cash updates must reconstruct wealth 102, not a -50% price-only loss.
4. Futures roll: the two real holding legs must produce gross P&L two, not six from the spliced chart.

Then check a delayed quote join and a not-yet-matured label. These tests establish how the operations behave on the fixtures. Historical coverage and execution assumptions then need their own audit on the vendor's real dataset.

#principle[*Chapter conclusion:* Data correctness preserves the object, opportunity, time, version, and cash-flow relations the research task needs. Build the auditable view first. An incorrect historical information set changes the experiment itself, however large the resulting matrix may be, and can make its decisions historically impossible.]


== Build the Clocks for the Market You Actually Study

An A-share session, a crypto exchange, a chain, and a U.S. reference exchange do not share one natural daily row. Define universal timestamps for comparisons, but preserve each venue's local session calendar, holidays, and daylight-saving changes. A UTC midnight candle is a data convention, not the economic definition of a stock trading day.

=== A-share short-horizon view

Add historical board, security status, trading session, daily-limit reference and rule version, suspension state, and sale eligibility. Record original and adjusted prices separately. A feature for “near the upper limit” must use that date's applicable reference and tick rounding. A final daily high, turnover, sector ranking, or public trading disclosure cannot be used at 10:00 merely because its row is dated that day. Assign its actual availability time.

Filter eligibility before ranking opportunities, but preserve unavailable or unfilled candidates when measuring the strategy's opportunity coverage. Keeping this broader record exposes the difference between all limit-hit opportunities and the attractive stocks that were easy to buy.

=== Crypto event view

Retain venue, spot/perpetual identity, trade and book sequences, instrument listing/delisting intervals, quote currency, and receipt timestamps. Store trade price, mark, and index as different fields. Funding needs its publication/estimate time, rate-setting interval, and actual payment time; an eventual settled rate may be a label/accounting input without being a permissible earlier feature. Gaps in liquidation-message streams are missing observations, not evidence of zero liquidations.

For onchain observations, preserve block time, when the data arrived, and the chosen confirmation/finality rule. Finality means the chosen standard for treating a record as no longer provisional. If a later reorganization changes the record, a historical replay must reproduce what the researcher could have admitted then, not silently replace it with the eventually canonical history. Begin with one venue's measured trade/book data before introducing cross-venue or chain joins.

=== Equity-linked token view

Keep wrapper and underlying identifiers, chain/contract version, currency conversion, multiplier effective time, issuer notices, venue trading state, and the reference quote's age. The official xStocks FAQ describes a multiplier mechanism for corporate actions; that is a product-specific example of why price and quantity units must be reconciled. Do not copy its mechanism to another issuer without its terms.

A session-close table cannot supply fresh reference prices through a weekend. Carrying forward a quote may be useful if it is explicitly marked stale; it must not imply an executable underlying leg. Venue descriptions can also disagree: when checked for this lecture, the dated xStocks support FAQ described selective weekend availability, while the risk-disclosure FAQ retained an older general 24/5 description. Preserve both source dates and resolve the particular venue/instrument calendar rather than promoting either slogan into a universal market rule.

=== A ten-row acceptance test

Construct records for: a pre-open observation, an opening-auction result received later, a same-session unexitable purchase, a suspension, a vanished listing, an exchange-feed gap, a funding rate published after the signal, a provisional chain event, a reference-market holiday, and a corporate-action multiplier change. For each, ask what was observable, tradable, and mature at the decision cutoff. Check that each join preserves the question defined at that cutoff; revise joins that describe another information set.

The resulting point-in-time opportunity table includes explicit unavailable states. Those distinctions make it a trustworthy input to labeling and features, even where the price panel has gaps.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Marcos López de Prado. #link("https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/finance-investments-special-topics-13fiz/advances-in-financial-machine-learning-978-1-119-48208-6")[_Advances in Financial Machine Learning_]. Wiley, 2018. Chapter 2 discusses financial data structures; Chapters 4 and 7 discuss outcome overlap and validation.
- Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani. #link("https://www.statlearning.com/")[_An Introduction to Statistical Learning, with Applications in R_]. Second edition, Springer, 2021. Chapter 5 develops separation between model fitting and assessment.
- Kraken. #link("https://support.kraken.com/articles/xstocks-faq")[_xStocks Frequently Asked Questions_], dated 18 September 2026, and #link("https://www.kraken.com/legal/xstocks")[_xStocks Risk Disclosure_]. Corporate-action units and product disclosures. Session descriptions require dated instrument-specific reconciliation.
]

#pagebreak()

= Features and Cross-Frequency Representations: Encode Economic Relations
#counter(math.equation).update(0)

A stateless predictor can use only the state we put in its current row. A futures chart omits relations between maturities. A daily strategy can also omit useful intraday structure even though it does not trade at every tick. Feature engineering fills these specific gaps by exposing the relations needed for the decision.

We construct a small daily futures panel, then explain standardization, exposure removal, and compression. We will see which task each operation serves and where its usefulness ends. The first recommended route is explicit state features plus controlled additions; learned compression enters when those summaries demonstrably omit a relevant distinction.

== Put Several Time Scales into the Current Row

=== Construct memory for a row-wise learner

Let $c_(t)>0$ be an available close from the declared research price history. A row-wise model does not remember its previous invocation. Construct momentum over $w$ sessions and deviation from a $w$-session average:

$
  m_(w) (t)=ln c_(t)-ln c_(t-w), quad
  a_(w) (t)=frac(1,w)sum_(j=0)^(w-1)c_(t-j), quad
  b_(w) (t)=frac(c_(t),a_(w) (t))-1.
$

Momentum compares endpoints; deviation compares the latest price with the recent price neighborhood. Both cancel a common positive multiplicative price scale. Both summarize the path, leaving its other details to be represented when the task needs them. A current close must be available before an ensuing execution; a window spanning a futures splice requires the representation bridge from Chapter 4.

Recall the two increment histories ending in the same positive final step but having long-window sums of +5 and -3. A single short-window return merges them. Short and long momentum together separate rebound-in-decline from continuing advance. This is the substantive reason to use multiple windows: encode time state as coordinates a snapshot model can see.

Our initial daily panel uses momentum at 1, 5, 10, 20, and 60 sessions, and average deviations at 5, 10, 20, and 60. The ten-session horizon describes the prototype's policy length; shorter and longer windows supply local and background state. The numbers are a small declared starting grid, not market constants. Adding every possible window would multiply selection freedom and create highly redundant columns without restoring arbitrary path details.

If a task needs peak-to-trough behavior, order of arrivals, or time spent under pressure, endpoints remain insufficient. Construct that missing relation explicitly rather than assuming that more copies of endpoint momentum contain it. Always compute temporal operators within asset identity and ordered sessions. A shuffled minibatch is a fitting arrangement, not a price history.

=== Add scale-relative bar and activity state

For a completed bar with high $H_(t)$, low $L_(t)$, close $c_(t)$, volume $V_(t)$, and the historical move scale $hat(sigma)_(t)$, begin with one-day log return, relative range, volatility, and a volume anomaly:

$
  r_(t)^(("log"))=ln(c_(t)/c_(t-1)), quad
  a_(t)^(("range"))=frac(H_(t)-L_(t),c_(t)), quad
  v_(t)^(("anom"))=frac(V_(t),frac(1,20)sum_(j=1)^(20) V_(t-j))-1.
$

The volume denominator uses the previous twenty sessions, not later activity. If it is zero or unavailable, flag the anomaly as unavailable. High and low summarize a completed interval; using the final high at the interval's start is leakage. Volume is not a scale-free proxy for demand across all contracts: units, sessions, rolls, and participation change. Its anomaly is a state coordinate to test, not a proven directional mechanism.

The historical volatility used by barriers is also a useful risk/state input. A high volatility reading says movement scale increased; it does not specify the next sign. Keeping direction and scale distinct prevents a magnitude relation from being misreported as directional alpha.

#principle[*Default memory panel:* Explicitly supply short, policy-length, and longer-horizon relations to stateless timing models. Use a few justified windows and scale-relative state variables. A snapshot with missing history is not repaired by giving its learner a more impressive name.]

== Observe What Makes a Futures Market Different

=== Construct the curve slope with a declared time unit

At the same available observation time, choose actual near and far contracts with prices $F_(t)^(n),F_(t)^(f)>0$ and maturity difference $Delta T>0$ measured in years. Define

$
  c_(t)^(("curve"))=frac(ln(F_(t)^(n)/F_(t)^(f)),Delta T).
$

Positive slope in this convention means near exceeds far; negative means far exceeds near. The unit is log-price ratio per year. If the gap is entered in months, multiply the per-month slope by twelve before comparing it with per-year values. This convention must accompany the feature, because reversing the ratio reverses its sign.

Near above far is commonly called *backwardation*; far above near is *contango*. Why examine the relation at all? Holding physical inventory can provide availability benefits while requiring financing and storage. Scarcity can change the value of immediate availability relative to later delivery. Term structure and inventory therefore concern states a single maturity's chart need not reveal. Research by Gorton, Hayashi, and Rouwenhorst relates inventories, basis, and commodity futures risk premiums; its evidence motivates a family of hypotheses, not an automatic sign rule for every copper date.

The feature is an observed relation. An explanation about scarcity or risk compensation is an economic hypothesis. Future conditional returns are the prediction target. These three objects must not collapse into “positive slope guarantees a long.” Nor is the slope itself an already received roll yield: the ledger of actual holding legs determines realized roll outcomes.

=== Basis changes have an algebraic interpretation

For the same two contract identities, write log basis $b_(t)=ln F_(t)^(n)-ln F_(t)^(f)$. Over $w$ sessions,

$
  b_(t)-b_(t-w)
    =[ln F_(t)^(n)-ln F_(t-w)^(n)]-[ln F_(t)^(f)-ln F_(t-w)^(f)].
$

The right side is near log return minus far log return. Thus basis momentum measures changing relative prices, rather than duplicating one outright price trend under a different name. With near/far values $(100,102)$ initially and $(103,104)$ later, the change is $ln(103/100)-ln(104/102)>0$: the near contract strengthens relative to the far even though both rise.

Contract identity is essential to this equality. If “near” switches from one maturity to another inside the window, the algebra compares different instruments. For the first version, construct twenty-session basis changes only over stable eligible pairs with sufficient history. Mark unavailable windows instead of interpreting the switch as a market signal. A constant-maturity interpolation is a later declared construction requiring its own input and holding bridge.

=== Open interest and inventory are observations, not participant identification

Open interest counts outstanding contracts under the data source's definition; volume counts trading activity over an interval. For available positive open interest $O_(t)$, an initial feature is $Delta ln O_(t)=ln O_(t)-ln O_(t-1)$. Price movement and open-interest change together can distinguish observed states. They do not identify exactly which participants opened, closed, or financed positions; many flows can lead to the same aggregate change.

Inventory and warehouse warrants likewise measure specified stocks or claims, not interchangeable generic “supply.” Add them only when historical release and revision records support the as-of query. Preserve their units and coverage. A current inventory table without release history cannot legitimately fill the past feature matrix.

For futures timing, prioritize these contract and physical-state families after the basic multiscale panel. The practical incremental comparison is basic state versus basic state plus available contract relations. It asks whether observations outside the outright chart add useful help; it does not certify the causal story solely from improved prediction.

== Standardize Coordinates; Neutralize Only Specified Exposures

=== Numerical scale and relative comparison are different needs

For a linear probability model, training-only column scaling makes coefficient penalties comparable across units. A tree splitting $x<a$ can usually express the corresponding split after a strictly increasing rescaling; it does not require z-scores just to equalize units. Histogram approximations and numerical details still depend on the implementation. Choose standardization according to the model's scale sensitivity and the comparison the feature is meant to express.

For relative asset selection, same-time cross-sectional z-scores convey distance from that date's available average. Chapter 2 derived that construction. Centering removes the market-wide mean, so retain that mean as separate context if the task still needs market state. Standardization alone does not remove industry exposure or make the economic meaning identical across regimes.

=== Derive exposure removal from a least-squares question

Suppose a cross-sectional feature vector $x in RR^(n)$ contains an industry or size component the selection strategy does not intend to bet on. Let columns of $B in RR^(n times k)$ record those selected exposures, with independent columns. Find the exposure combination closest to $x$ by minimizing $||x-B gamma||^(2)$.

Differentiation gives $-2B^(T) (x-B gamma)=0$. Hence

$
  hat(gamma)=(B^(T) B)^(-1)B^(T) x, quad
  x_(perp)=x-B hat(gamma), quad B^(T) x_(perp)=0.
$

The last equality is the retained guarantee: the residual is orthogonal to those particular in-sample linear exposures.

The normal equations can be checked without remembering a matrix formula. Expand the objective as $x^(T) x-2gamma^(T) B^(T) x+gamma^(T) B^(T) B gamma$. Its gradient is $-2B^(T) x+2B^(T) B gamma$. Independent columns make $B^(T) B$ positive definite: for nonzero $a$, $a^(T) B^(T) B a=||B a||^(2)>0$. Thus the stationary point is the unique minimum, and substituting its normal equation gives $B^(T) x_(perp)=B^(T) x-B^(T) B hat(gamma)=0$. This substitution establishes orthogonality. The operation, called *neutralization*, removes specified exposures; centering and scaling serve the separate purpose of changing coordinates. If an intercept and all industry indicator columns are redundant, remove redundant columns or solve on an independent basis instead of inverting a singular matrix.

For a simple example, $x=(1,2,10,11)^(T)$ and $B$ contains separate indicators for two industries with two assets each. The fitted industry levels are 1.5 and 10.5; the residual is $(-0.5,0.5,-0.5,0.5)^(T)$. We removed between-industry differences while retaining within-industry differences. If the future relation depended on the industry levels, we also removed predictive content. That is acceptable only if the strategy intentionally declines that exposure or preserves it in a separately governed component.

#principle[*Exposure decision:* Select unsupported or unwanted bets for neutralization while retaining the other observable relations the strategy intends to use. State which columns of $B$ define the excluded component. Orthogonality to them is a mathematical result; better future prediction or lower realized risk is a separate empirical question.]

== Move Fine Observations into a Coarser Decision

=== Decide which relations to retain in a summary

A daily strategy can use intraday observations while trading at its own lower frequency. It may need sustained buying pressure, spread conditions, or replenishment behavior that daily endpoints omit. The future task provides the criterion for deciding which parts of that finer history are useful.

For an available session, start with executed quantities $q_(u)$ and a declared trade-sign rule $epsilon_(u) in {-1,0,+1}$. Signed trade imbalance is

$
  J=frac(sum_(u) epsilon_(u) q_(u),sum_(u) q_(u)).
$

The sign records the chosen aggressor-side classification, not the identity or intent of the final buyer. Unknown signs can be zero with an accompanying unknown-volume fraction. A zero total volume makes the ratio unavailable. Retain the total separately: the same imbalance with ten and ten thousand traded units can describe different states.

From valid simultaneous best quotes define midpoint $M=(P_("ask")+P_("bid"))/2$, relative spread $(P_("ask")-P_("bid"))/M$, and a specified-depth book imbalance

$
  I_(u)=frac(D_("bid",u)-D_("ask",u),D_("bid",u)+D_("ask",u)).
$

Depth must be measured in matching quantity units and comparable levels. Quotes are cancelable liquidity, not executions. For snapshots valid over durations $Delta_(u)$, a persistence summary is

$
  overline(I)=frac(sum_(u) Delta_(u) I_(u),sum_(u) Delta_(u)).
$

Duration weighting prevents a burst of quote messages from receiving extra weight merely because the feed repeated the same state many times. Exclude periods outside the admitted session and stale/invalid states according to the data policy. Also retain spread/depth distribution summaries, such as fixed development-selected quantiles, and event counts needed to judge coverage.

Start with traded quantity, signed trade imbalance, spread/depth summaries, and persistent book imbalance. Compare the panel with and without these summaries under the same low-frequency label and learner. The observation window must end before the decision; its future label may supervise a representation only through completed, properly separated training examples.

=== Represent order when the decision depends on it

Two windows can have imbalance states $(+1,-1)$ and $(-1,+1)$ for equal durations. Both average to zero. If end-of-window pressure or the transition matters for the decision, the average has erased it. Add recent imbalance, change, or a specified replenishment response. Then test the added relation. The example identifies a distinction lost by averaging; whether that distinction predicts actual returns remains a question for the data.

If simple state/order features remain insufficient, a learned weighted summary can take the form

$
  z_(t)=sum_(u in W_(t)) a_(t,u)v_(t,u), quad
  a_(t,u)=frac(exp(e_(t,u)),sum_(v in W_(t))exp(e_(t,v))).
$

The scores $e$ and transformed observations $v$ are computed from the available window; weights are nonnegative and sum to one. Such *attention* learns which represented events to emphasize. Its supervision should be the relevant daily direction, policy, or ranking task. An attention weight describes the emphasis chosen by the model. Establishing an event's economic effect requires separate causal evidence.

Cross-frequency summarization and factor-expert aggregation are sometimes both called stacking. They have different jobs. The first retains useful structure from event histories; the second allocates trust among already formed predictions. Each therefore needs its own input definition, target, and verification.

== Reconstruction Can Preserve Precisely the Wrong Component

=== A two-coordinate calculation explains the failure

Let $X=(N,S)^(T)$ have independent centered coordinates with variances $v_(N)>v_(S)>0$. Suppose future label is the sign of $S$, while $N$ is unrelated noise. A one-dimensional linear reconstruction keeps projection along a unit vector $w$, reconstructing $hat(X)=w w^(T) X$.

Expand the squared error using $w^(T) w=1$:

$
  E||X-w w^(T) X||^(2)
    =E||X||^(2)-E[(w^(T) X)^(2)]
    =v_(N)+v_(S)-(v_(N) w_(N)^(2)+v_(S) w_(S)^(2)).
$

Since $w_(N)^(2)+w_(S)^(2)=1$, minimizing error means maximizing captured variance, so $w_(N)^(2)=1$ and $w_(S)=0$.

To see the steps explicitly, expand the square: $||X-w w^(T) X||^(2)=X^(T) X-2(w^(T) X)^(2)+(w^(T) X)^(2)w^(T) w=||X||^(2)-(w^(T) X)^(2)$. Centering and independence give $E[N S]=0$, so $E[(w_(N) N+w_(S) S)^(2)]=w_(N)^(2)v_(N)+w_(S)^(2)v_(S)$. Replacing $w_(S)^(2)$ by $1-w_(N)^(2)$ leaves captured variance $v_(S)+(v_(N)-v_(S))w_(N)^(2)$, maximized at $w_(N)^(2)=1$. This explicitly connects the reconstruction objective to discarding the lower-variance coordinate. The best reconstruction keeps $N$ and discards all of $S$. With variances 100 and one, error is only one unit out of total variance 101, yet the retained representation has no information about the sign label.

This is the mechanism behind linear principal-component compression: keep directions of greatest variance for a reconstruction objective. An autoencoder is a learned encoder and decoder trained to reconstruct inputs; nonlinear forms need not choose exactly this projection, but good reconstruction alone still does not certify task relevance. Assess the representation on the actual future task through supervision or independent evaluation, alongside its reconstruction error.

=== An amplitude penalty can also erase a small useful response

For one coordinate, consider the penalized approximation

$
  min_(z) frac(1,2)(z-a)^(2)+lambda |z|, quad lambda>=0.
$

For $z>0$, the derivative is $z-a+lambda$, suggesting $z=a-lambda$ when $a>lambda$. For $z<0$, it is $z-a-lambda$, giving $z=a+lambda$ when $a< -lambda$. At zero, the left slope is $-a-lambda$ and the right slope $-a+lambda$; they bracket zero exactly when $|a|<=lambda$. The objective is convex on either side with increasing slopes, so these cases give its global minimum:

$
  z^(*)=cases(a-lambda & "if" a>lambda,
             0 & "if" |a|<=lambda,
             a+lambda & "if" a< -lambda).
$

This is *soft thresholding*: shrink surviving amplitudes and remove sufficiently small ones. If a low-amplitude coordinate carries the label relation, an indiscriminate penalty can remove the signal. Match the scale and restriction of regularization to the task, then check which predictive relations survive. Compression, smoothness, and sparsity describe properties of the representation; usable information describes its value for prediction.

#heading(level: 2, numbering: none)[Practical Default: Three Nested Panels]

Build and compare three named panels using one frozen learner, label policy, and temporal protocol:

1. *Basic state:* one-day log return, relative bar range, twenty-return move scale, volume anomaly; momentum at 1/5/10/20/60 sessions and average deviations at 5/10/20/60.
2. *Contract relations:* add simultaneous near/far slope per year, twenty-session stable-pair basis change, and available open-interest change. Admit inventory only with usable release/version history.
3. *Fine-history summaries:* add admitted-session traded quantity, signed trade imbalance, spread/depth summaries, and persistent book imbalance. Record coverage and unknown/stale states.

Remove exact duplicate and constant columns. Keep availability, units, lookbacks, identities, and missingness rules in the input dictionary. Use training-only scaling for linear probability baselines. For cross-sections, encode contemporaneous relative position and preserve needed market context. Select for neutralization the named exposures the strategy does not intend to exploit.

If simple features demonstrably miss a task-relevant state or order distinction, train a supervised bottleneck or attention summary to represent it. Assess the addition by independently confirmed probability/ranking and net-policy contribution; reconstruction loss and column count describe different properties. Chapter 8 develops the admission and retirement process for larger factor libraries.

*Self-check:* Why do equal one-day moves not make the five-step histories equal states? Why is curve slope not realized roll P&L? Which of the two coordinates in the reconstruction example must a direction predictor preserve? Each answer should identify the specific relation needed for the decision.

#principle[*Chapter conclusion:* Construct representations that expose economically motivated, task-relevant relations. Multiscale state, contract context, relative coordinates, exposure removal, and fine-history summaries each solve a different problem. Keep the small explicit panel as the first route; use learned compression when its additional retained relation earns independent support.]


== Turn Market Narratives into Measurable Mechanisms

A stylized pattern describes a tendency we expect to recur within a specified sample and time scale. Broad accounts such as “A-shares favor short-term speculation” or “crypto gets pumped” leave the relevant observations unspecified. To study them, identify a measurable state, consider an alternative explanation, and compare outcomes in a way that can guide the feature design.

=== An A-share continuation/reversal feature panel

Begin with four small groups: past own/sector returns; turnover relative to the stock's own history; distance to its applicable price limits; and within-session position relative to an observable traded-price average. A volume-weighted average price is $frac(sum_(j) P_(j) V_(j),sum_(j) V_(j))$ over completed trades, where $V_(j)$ is trade quantity. At an intraday cutoff, neither its full-session version nor full-session turnover is available.

Let previous close be $C$, applicable proportional upper limit $ell$, and current price $P$. Ignoring tick rounding only for illustration, limit price is $U=C(1+ell)$ and normalized remaining distance is $frac(U-P,C ell)$. At $C=10,P=10.90$, a 10% limit yields distance 0.10; a 20% limit yields 0.55. The same raw price change occupies a different institutional state. Use the historical exchange-rounded limit in an actual implementation.

The mechanism question is whether high attention continues or exhausts. Add sector participation, quote depth, and prior failed-breakout observations only if their histories and cutoffs are available. Volume alone does not identify buying by a particular “main force”; every executed share has a buyer and a seller. The initial panel measures prices, activity, and constraints, leaving investor identity as a separate inference requiring other evidence.

Use rolling time splits to compare past returns alone, the same model with activity and limit state, and the complete panel. Report next-session rank quality, long-only portfolio results, and entries that were unavailable. If the predictive direction changes across liquidity states, represent that state explicitly so the comparison tests when continuation and reversal occur.

=== A crypto continuation/stress feature panel

Start with completed-window return and volatility, turnover anomaly, spread, bid/ask depth at fixed relative distances, and a declared signed-trade measure. Signed trade quantity uses a documented aggressor-side classification; notional imbalance $frac(V_("buy")-V_("sell"),V_("buy")+V_("sell"))$ is unavailable when the denominator is zero. It measures trading pressure under that classification, not conviction or unique participants.

For a derivative extension, add perpetual/reference premium, published funding information, changes in open interest, and observed forced-close activity. Open interest is outstanding contracts; its change alone does not identify whether a particular trader opened a directional long or short. Study “spot participation plus continuing depth” against “derivative premium plus disappearing depth” as competing state descriptions. Matched evidence would be needed to establish either description as a cause.

A short worked distinction makes the added information concrete. Markets A and B both have a completed five-minute 5% rise. A has spread 5 basis points and 500,000 quote-currency units of bids within 1% below mid; B has spread 80 basis points and 10,000 units. A contemplated 20,000-unit sale is small relative to A's displayed depth and exceeds B's. Displayed depth is cancellable, so this is a state feature, not a fill promise. It nevertheless explains why returns alone omit a decision-relevant distinction.

*Starting experiment:* first screen opportunities for liquidity and tradability, then fit a small model of continuation success. Assess it using costs appropriate to the proposed trade size. Investigate suspected manipulation as a reason for risk controls or exclusion; this experiment does not seek to exploit or organize such schemes.

=== A token/reference feature panel

Keep reference-market-open state and quote age alongside normalized token/reference gap, executable spread/depth, currency basis, and documented multiplier state. If a spot token and its perpetual coexist, add their separately aligned premium and funding state. Observe issuance/redemption availability only when published and operationally applicable. A reference gap without a quote-age feature can mainly encode which market is asleep.

For an off-hours token move, compare a last-reference-only baseline, a simple available market-proxy baseline, and wrapper/liquidity additions. Use liquid index or sector observations only at their actual available times; they provide explanatory proxies, with replication error assessed separately. Evaluate open-reference and closed-reference intervals separately. An improvement appearing only after forward-filling future reference quotes is leakage, not successful feature engineering.

=== Why these additions deserve the feature budget

The three panels add different distinctions: A-share inventory and limit state, crypto execution and derivative stress, and token reference/contract state. Some require new observations; others reorganize known relations so that a small model can use them. Under the same development procedure, compare the predictive contribution and missing-data coverage of each addition. Keep those supported by the comparison before exploring a larger representation. The resulting feature panel follows the information needed for the decision and the evidence for each addition.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Gary B. Gorton, Fumio Hayashi, and K. Geert Rouwenhorst. #link("https://www.nber.org/papers/w13249")[_The Fundamentals of Commodity Futures Returns_]. NBER Working Paper 13249, 2007; published in _Review of Finance_ 17(1), 35–105, 2013. Inventory, basis, and commodity risk-premium relations.
- Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani. #link("https://www.statlearning.com/")[_An Introduction to Statistical Learning, with Applications in R_]. Second edition, Springer, 2021. Linear model regularization and principal-component methods.
- Yilun Xu et al. #link("https://arxiv.org/abs/2002.10689")[_A Theory of Usable Information Under Computational Constraints_]. ICLR, 2020. Prediction under restricted observer families.
]

#pagebreak()

= Models, Capacity, Parameters, and Losses: Restraint Needs a Reason
#counter(math.equation).update(0)

We can now choose a model for an actual constructed task. If a small factor panel already exposes state, a model mainly needs thresholds and interactions. If relevant relations remain buried in paths, books, text, or a whole market cross-section, a suitable representation structure can do essential work. Structure and capacity are two different decisions: how a relation is expressed, and how much freedom the data can support.

For low-breadth tabular timing, our selected route is the probability baseline followed by shallow constrained boosted trees. For whole-date cross-sectional relation learning, it is shared per-asset controls followed by shallow nonpositional set attention. This chapter derives these choices and specifies prototypes. Their empirical value will be judged by comparisons matched to the financial task.

== Locate the Relation Before Increasing Capacity

The Chapter 2 one-split example became easy after the representation supplied $X^(2)$. Expanding the raw-input model could also solve it, but that is a different allocation of computation and estimation freedom. Chapter 5's multiscale panel similarly performs historical calculations before a row-wise learner sees the data.

For these refined inputs, start with logistic regression because it tests whether a weighted factor relation suffices. Then use shallow trees if economically plausible thresholds or interactions remain. A depth-two tree can, for example, distinguish positive long-horizon momentum only when a volatility state is below a threshold. A linear log-odds model without that interaction cannot express the same piecewise response exactly.

Raw text needs a representation of meaning, a price path may need temporal order, and a set of assets may need relative context. There a representation model has an identifiable role. The useful role of a neural model is to express relations still missing from the supplied representation. Focusing its capacity on that work avoids spending additional freedom on calculations already provided.

The small mutual-information figures from Chapter 1 describe the prediction problem, while an appropriate parameter budget also depends on the model and fitting procedure. Those figures describe one distribution and observation relation. Family approximation, finite-sample variability, loss, and optimization determine actual fitting. We next construct two mechanisms explaining why restraint is nevertheless a rational default.

== Derive Why Unsupported Freedom Is Expensive

=== Near-redundant columns amplify estimation perturbations

Let $M$ be a fixed design matrix and $y$ the observed response vector. To expose estimation sensitivity, minimize penalized squared error:

$
  J(beta)=||y-M beta||^(2)+lambda ||beta||^(2), quad lambda>=0.
$

Differentiation gives $-2M^(T) (y-M beta)+2lambda beta=0$, hence, when the inverse exists,

$
  hat(beta)=(M^(T) M+lambda I)^(-1)M^(T) y.
$

The matrix $M^(T) M$ is symmetric and nonnegative. Along a unit eigendirection $v_(j)$ with eigenvalue $s_(j)$, the solution divides the corresponding component of $M^(T) y$ by $s_(j)+lambda$. Without a penalty, a small $s_(j)$ produces a large response to perturbations. Highly redundant columns create precisely such weakly measured directions.

For a more quantitative illustration, suppose $y=M beta^(*)+epsilon$ with centered noise covariance $tau^(2) I$. Then the numerator's noise component $v_(j)^(T) M^(T) epsilon$ has variance $tau^(2) s_(j)$. The fitted component has

$
  E[v_(j)^(T) hat(beta)]=frac(s_(j),s_(j)+lambda)v_(j)^(T) beta^(*), quad
  Var(v_(j)^(T) hat(beta))=frac(tau^(2) s_(j),(s_(j)+lambda)^(2)).
$

At $lambda=0$ and $s_(j)>0$, variance is $tau^(2)/s_(j)$. Increasing the penalty suppresses amplification but also shrinks the true coefficient. This is the concrete trade-off: reduced estimation variance at the cost of bias. Unstable directions provide the reason for a penalty; the resulting shrinkage trades some true response for greater estimation stability. The calculation assumes a fixed design and this noise covariance; it does not establish the financial data-generating process.

=== Searching many candidates can select an accidental winner

Now suppose $K$ prediction functions are fixed before seeing $n$ independent, identically distributed evaluation examples. Let each loss be in $[0,1]$, population risk $R(f)$ its expected loss, and empirical risk $hat(R)_(n) (f)$ its sample average. We want one error bound that holds even after choosing the empirical winner.

First derive a bound for a single bounded loss $Z$. Define the log exponential average

$
  psi(a)=ln E[exp(a(Z-E Z))].
$

Differentiating gives a weighted average of $Z-E Z$, where weights are proportional to $exp(a(Z-E Z))$.

For the algebra, put $X=Z-E Z$ and $A(a)=E exp(a X)$. Bounded $X$ permits differentiation under the expectation. Then

$
 psi'(a)=frac(E[X exp(a X)],A(a)), quad
 psi''(a)=frac(E[X^(2)exp(a X)],A(a))-
 (frac(E[X exp(a X)],A(a)))^(2).
$

Define the weighted expectation $E_(a) h(X)=E[h(X)exp(a X)]/A(a)$. The last expression is $E_(a) X^(2)-(E_(a) X)^(2)=Var_(a)(X)$. For any interval midpoint $m$, $Var_(a)(X)=E_(a)(X-m)^(2)-(E_(a)X-m)^(2)<=1/4$. Finally, $psi(a)=integral_(0)^(a)(a-s)psi''(s)dif s<=a^(2)/8$. These steps follow from differentiation and integration under the assumptions already stated. Differentiating again gives its variance under those weights. The weighted variable still lies in an interval of length one. Since its distance from the interval midpoint is at most one half, its variance is at most $1/4$. Therefore $psi''(a)<=1/4$, with $psi(0)=psi'(0)=0$. Integrating twice for $a>=0$ gives

$
  E[exp(a(Z-E Z))]<=exp(a^(2)/8).
$

For independent examples, exponential averages of sums multiply.

Write $X_(i)=Z_(i)-R(f)$ for one frozen candidate. Independence gives $E exp(a sum_(i)X_(i))=product_(i)E exp(a X_(i))<=exp(n a^(2)/8)$. The event $hat(R)_(n)-R>epsilon$ implies $exp(a sum_(i)X_(i))>exp(a n epsilon)$ for $a>0$. Markov therefore divides the exponential average by $exp(a n epsilon)$. Differentiating the exponent $-a n epsilon+n a^(2)/8$ gives $-n epsilon+n a/4=0$, hence $a=4epsilon$. Repeating with $-X_(i)$ and adding the two tail probabilities supplies the factor two; summing over candidates supplies $K$. Setting $2K exp(-2n epsilon^(2))=delta$ and taking logarithms yields the displayed simultaneous tolerance. For a nonnegative variable $U$ and $b>0$, $E U>=b Pr(U>=b)$, because the event $U>=b$ alone contributes at least that much to the expectation. Rearranging gives the tail bound called *Markov's inequality*. Apply it to the exponential of the centered loss sum to obtain

$
  Pr(hat(R)_(n)-R>epsilon)
    <=exp(-a n epsilon+n a^(2)/8).
$

Minimize the exponent at $a=4epsilon$ to obtain $exp(-2n epsilon^(2))$. Applying the same argument to $-Z$ bounds the opposite tail. Finally, the probability of at least one bad deviation among $K$ candidates is at most the sum of their probabilities:

$
  Pr(max_(f) |R(f)-hat(R)_(n) (f)|>epsilon)
    <=2K exp(-2n epsilon^(2)).
$

This last step is the *union bound*. For failure probability $delta in (0,1)$, choose

$
  epsilon_(n)=sqrt(frac(ln(2K/delta),2n)).
$

On the resulting simultaneous event, let $hat(f)$ minimize empirical risk and $f^(*)$ minimize population risk among the candidates. Use the error bound on each side of the empirical comparison:

$
  R(hat(f))<=hat(R)_(n) (hat(f))+epsilon_(n)
    <=hat(R)_(n) (f^(*))+epsilon_(n)<=R(f^(*))+2epsilon_(n).
$

Thus searching costs a term growing with $sqrt(ln K/n)$. At $K=100,n=2500,delta=0.05$, $epsilon_(n)$ is about 0.041. Such a worst-case guarantee is loose beside a one- or two-percentage-point directional edge; it motivates limiting selection, not dismissing all smaller empirically supported edges.

The assumptions matter. Correlated assets, overlapping labels, and market drift are not IID examples merely because a dataset has many rows. Unbounded class log loss is not automatically a $[0,1]$ loss. A bounded clipped-and-rescaled score changes the object being bounded. Candidates trained on the same evaluation sample are not $K$ pre-fixed functions: either freeze them using separate training data, or control the larger function family they could have produced.

For infinite families, one needs a measure of how many responses they can distinguish on samples. VC dimension counts the largest set of inputs on which a binary family can realize every assignment of zero/one labels. Rademacher complexity measures how strongly a family can fit independently randomized plus/minus signs on the observed inputs. These extend the accounting of selection freedom; neither is identical to raw parameter count. The finite proof already supplies the principle we need, without importing their general theorems as market guarantees.

#principle[*Capacity conclusion:* Thin edges leave little room for estimation and selection error. Limit unsupported responses, preserve credible structure, and seek genuinely informative observations. The derived IID bound explains one mechanism; temporal financial verification remains a separate obligation.]

== What Shallow Boosting and Its Parameters Actually Do

=== Build the Prediction through Additive Scores

For a binary probability model, let current score be $S_(m-1) (F)$ with probability $p=1/(1+exp(-S))$. Add a tree response $h_(m) (F)$:

$
  S_(m) (F)=S_(m-1) (F)+nu h_(m) (F), quad 0<nu<=1.
$

A tree repeatedly splits feature space into regions and gives each leaf one response. A depth-$d$ binary tree has at most $2^(d)$ leaves, so depth three provides at most eight regions *per tree*. Multiple trees can create far more combined distinctions; the round count remains a capacity and selection choice.

To see why leaf support and penalties matter, use the binary natural-log loss from Chapter 2. At example $i$, the current score derivative and curvature are

Let $b in {0,1}$, $p(S)=1/(1+exp(-S))$, and $ell(S;b)=-b ln p-(1-b)ln(1-p)$. The quotient derivative is $p'(S)=p(1-p)$. Applying the chain rule gives

$
 frac(dif ell,dif S)=(-frac(b,p)+frac(1-b,1-p))p(1-p)=p-b,
 quad frac(dif^(2)ell,dif S^(2))=p(1-p).
$

The second-order expansion $ell(S+w)=ell(S)+g w+h w^(2)/2+o(w^(2))$ is applied to every observation in the proposed leaf; summing and adding $lambda w^(2)/2$ produces the leaf objective below. The expansion is local, not an exact logistic-loss identity.

$
  g_(i)=p_(i)-B_(i), quad h_(i)=p_(i) (1-p_(i)).
$

For a proposed leaf with unshrunk constant score change $w$, a second-order local approximation plus leaf penalty is

$
  G w+frac(1,2)(H+lambda)w^(2), quad
  G=sum_(i in "leaf")g_(i), quad H=sum_(i in "leaf")h_(i).
$

Differentiation gives $w^(*)=-G/(H+lambda)$ when the denominator is positive. Increasing the L2 leaf penalty reduces the fitted response. A small curvature total makes the update depend on a weakly supported region; a child-weight requirement excludes splits that create such children. This scalar construction explains the mechanism. Multiclass and weighted implementations have their own curvature conventions.

In XGBoost, `min_child_weight` concerns summed Hessian weight, not universally a raw row count. For our unit-weight binary curvature, $h_(i)<=1/4$, so a total of twenty would require at least eighty observations, and more if many probabilities are near zero or one. Sample weighting or another objective changes that interpretation. Consult the objective and recorded implementation version before translating weight thresholds into support claims.

=== Learning rate and round count jointly control accumulated fitting

Shrinkage $nu$ limits a new tree's score contribution. It is not the same as the learning rate for a direct gradient update of neural weights, and it does not set a numerical Shannon-information budget. If every successive tree contributed the same constant $a$, accumulated change would be $M nu a$. A smaller $nu$ can therefore be offset by more rounds. Real trees adapt to the changing residuals, but the example already refutes “small learning rate alone prevents overfitting.”

Our first timing prototype uses depth 3, shrinkage 0.03, at most 300 boosting rounds, row and feature sampling 0.8, L2 leaf penalty 2, and child Hessian-weight threshold 20. Use probability objectives: `binary:logistic` for a binary gate/direction target, or `multi:softprob` with three classes for first-passage outcomes. Integer codes must be mapped to the implementation's valid class indices while preserving their original meanings in the outcome record.

Use later development data for log-loss early stopping, with a declared patience of twenty rounds and the best development checkpoint within the cap. Freeze the checkpoint policy before final confirmation. For the first meta-gate comparison, use depth 2, shrinkage 0.03, cap 150 rounds, child-weight threshold 50, and L2 penalty 4, on a smaller panel. These are reproducible teaching settings, not selected optima. Their stricter support can make a gate effectively constant when observations are sparse; report that outcome rather than secretly lowering thresholds until a profitable fit appears.

Row/column sampling changes which data and features a round can use. It may reduce reliance on particular examples; it does not make overlapping trades independent. Missing-value routing selects a computational branch, not a verdict that missingness is economically harmless. Feature importance describes the fitted model under its definition, not proof of incremental signal or causality.

=== A monotone prior is a restriction with an entry condition

If a reliable relation says increasing feature $x_(j)$ should not decrease a particular scalar score over a specified domain, a monotonicity constraint removes contrary responses. It can save selection freedom. If the effect reverses in different regimes, the same restriction can erase useful structure.

State the output, sign convention, range, and conditions before enabling it. A monotonic constraint on one multiclass score is not automatically monotonicity of its probability, because all class scores enter the denominator. The first generic prototype does not assert unconditional monotonicity for momentum or curve slope; add an output-specific constraint only with a defensible prior and a matching implementation contract.

== A Safeguarded Step Size for the Probability Baseline

The first probability model deserves an actual fitting rule. Let $M$ contain standardized feature rows plus an intercept column, $theta$ the corresponding coefficients, and $D$ diagonal with entries $p_(i) (1-p_(i))$. For average logistic loss plus L2 penalty on non-intercept coefficients, its Hessian is

To fix the objective convention, let row $m_(i)^(T)$ of $M$ be an input with intercept and set $S_(i)=m_(i)^(T)theta$. We minimize $J(theta)=N^(-1)sum_(i)ell(S_(i);B_(i))+lambda theta^(T) R theta/2$. Using the score derivatives just derived,

$
 nabla J=frac(1,N)M^(T)(p-B)+lambda R theta.
$

Differentiating each $p_(i)$ contributes $p_(i)(1-p_(i))m_(i)$, so the matrix of second derivatives is the expression below. The factor one half in the penalty is essential to its coefficient convention.

$
  nabla^(2) J(theta)=frac(1,N)M^(T) D M+lambda R,
$

where $R$ is diagonal, zero on the intercept and one on penalized coefficients. A Hessian is the matrix of second derivatives; it measures how the gradient changes locally. Since $0<=D<=I/4$, every direction $v$ satisfies

The notation $D<=I/4$ is a quadratic-form comparison: each diagonal entry obeys $p(1-p)=1/4-(p-1/2)^(2)<=1/4$. Consequently $v^(T)M^(T) D M v=sum_(i)D_(i,i)(m_(i)^(T)v)^(2)<=||M v||^(2)/4$. Also $v^(T) R v<=||v||^(2)$ and $||M v||<=||M||_("op")||v||$. Adding these inequalities and dividing the data term by $N$ gives the bound.

$
  v^(T) nabla^(2) J(theta)v
    <=[frac(||M||_("op")^(2),4N)+lambda]||v||^(2).
$

The operator norm $||M||_("op")$ is the largest stretch $||M v||$ over unit vectors $v$; its square is the largest eigenvalue of $M^(T) M$. Define the bracketed upper bound as $L_(0)$. It bounds curvature everywhere for this fixed design and objective.

Integrating curvature along a proposed displacement $d$ gives the quadratic upper estimate

$
  J(theta+d)<=J(theta)+nabla J(theta)^(T) d+frac(L_(0),2)||d||^(2).
$

One way to see the last term is to integrate the second derivative of $J(theta+s d)$ with weight $1-s$ for $s$ from zero to one; its bound is $L_(0)||d||^(2)$ and the weight integrates to one half. Now choose $d=-eta nabla J(theta)$:

$
  J(theta-eta nabla J(theta))
    <=J(theta)-eta(1-L_(0) eta/2)||nabla J(theta)||^(2).
$

For $L_(0)>0$, the simple starting choice $eta=1/L_(0)$ guarantees nonincrease of this training objective in exact arithmetic; smaller positive steps at most $1/L_(0)$ are also safe. Numerical implementations should verify objective behavior and convergence tolerance. The data and objective thus provide a concrete step scale. Financial value is assessed separately on later observations.

The coefficient penalty $lambda$ changes the objective; the step size $eta$ controls movement while solving it. Boosting shrinkage $nu$ controls additive tree contributions. Adam, an adaptive gradient optimizer developed in Chapter 7, uses still another rule. Sharing the phrase “learning rate” does not transfer this logistic curvature guarantee to those other algorithms.

== Cross-Sectional Relations and the Symmetry of an Asset Set

=== What must happen if asset rows are reordered?

For a date with $n$ assets, let $X in RR^(n times d)$ contain one feature row per asset. Let $P$ be a permutation matrix that reorders rows. Scores should satisfy

$
  f(P X)=P f(X).
$

This is *permutation equivariance*: change the arbitrary input order, and outputs follow the same assets without changing their values. A shared per-asset linear function or tree already has this property, although it need not see other rows. Contextual features, cross-sectional statistics, and shared set summaries can supply comparison information to those controls. The comparison with attention concerns how contextual relations are represented: trees can rank assets, and several architectures share this symmetry.

The positive reason is that attention can learn asset-to-asset relations from the whole contemporaneous set while preserving the irrelevant-order symmetry. The relation layer need not ask each isolated asset score to reconstruct all comparison context indirectly.

=== Construct and verify the relation operation

Choose shared matrices $W_(Q),W_(K),W_(V)$ and form

For dimensions, take $W_(Q),W_(K) in RR^(d times d_(k))$ and $W_(V) in RR^(d times d_(v))$. Then $Q,K$ are $n$ by $d_(k)$, $V$ is $n$ by $d_(v)$, and $Q K^(T)$ is $n$ by $n$. Its row $i$ assigns one comparison score to each candidate counterpart $j$; multiplying its normalized row by $V$ returns one $d_(v)$-dimensional response for asset $i$. A residual addition to $X$ requires an output projection back to width $d$ if $d_(v)!=d$.

$
  Q=X W_(Q), quad K=X W_(K), quad V=X W_(V), quad
  A(X)="softmax"_("row")(Q K^(T)/sqrt(d_(k)))V.
$

Rows of $Q$ describe what an asset seeks, rows of $K$ what other assets offer for comparison, and rows of $V$ the responses combined. Their dot products produce comparison scores. Rowwise softmax exponentiates and normalizes each row, so every asset takes a nonnegative weighted average of the available response rows. $d_(k)$ is the number of query/key coordinates. If independent coordinate products have unit variance, their sum has variance $d_(k)$; dividing by $sqrt(d_(k))$ keeps that illustrative score scale order one. It is a numerical scaling rationale, not a financial independence assumption.

Under row permutation, $Q,K,V$ become $P Q,P K,P V$, and the score matrix becomes $P(Q K^(T))P^(T)$. Reordering a row's entries before exponentiation and normalization reorders its weights without changing the denominator. Reordering rows likewise reorders their normalized outputs. Therefore

$
  "softmax"_("row")(P S P^(T))=P "softmax"_("row")(S)P^(T),
  \
  A(P X)=P "softmax"_("row")(S)P^(T) P V=P A(X),
  quad S=Q K^(T)/sqrt(d_(k)).
$

Shared rowwise transforms and residual additions preserve this equality. Positional encodings, a causal mask based on arbitrary asset order, or an unpermuted availability mask can break it. An asset's genuine attributes may be features; an arbitrary row number should not become financial information.

Our relational prototype uses two attention blocks, width 64, four heads with sixteen query/key coordinates each, and a shared scalar output for every asset. Multiple heads perform several shared comparison operations, concatenate their responses, and apply a shared output projection. Each block uses rowwise RMS normalization before attention and before a shared rowwise two-layer transform of width 128; use a declared nonlinear activation such as componentwise $tanh$. Add residual responses in the same 64-dimensional space. Include dropout 0.2 on learned residual branches during training and disable it for evaluation.

Use complete available same-date sets, mask unavailable assets consistently, and average losses by date rather than pretending every asset-date row is an independent market realization. Without positional encoding, and with masks permuted with assets, the deterministic evaluation model should pass a direct test: permute inputs, predict, undo the permutation, and compare with the original scores within numerical tolerance. To assess the financial usefulness of that symmetry-preserving relation layer, compare it with shared linear/tree controls using explicit context under the same confirmation protocol.

== Give Every Capacity and Numerical Parameter a Separate Job

Depth and width limit the transformations the model can express. Early stopping limits how long it adapts to development-selected fits. Dropout masks responses during training; it is not an increase in market information or proof of a smaller effective family. Stronger masking and penalties can remove the low-amplitude useful component illustrated in Chapter 5.

For a row response $x in RR^(d)$, a practical RMS normalization is

$
  "RMSNorm"(x)_(j)=gamma_(j) frac(x_(j),sqrt(frac(1,d)sum_(k=1)^(d) x_(k)^(2)+epsilon)),
  quad epsilon>0.
$

It divides by a root-mean-square response scale and applies learned gains $gamma_(j)$. Unlike mean subtraction, it does not recenter the row. Use $epsilon=10^(-6)$ as a declared numerical starting convention for this standardized prototype. The stabilizing term prevents division by zero and makes exact scale invariance approximate. RMSNorm chiefly governs response scale and fitting conditions; capacity restrictions come from the architecture and other explicit controls.

For an $m$-by-$n$ projection, an explicit low-rank restriction uses

$
  W=A B^(T), quad A in RR^(m times r), quad B in RR^(n times r).
$

The image of $W$ lies in the span of the $r$ columns of $A$, so its rank is at most $r$. This stores $r(m+n)$ factor parameters instead of $m n$ matrix entries, with redundant parameterizations possible. A rank-16 factorization of a 64-by-64 projection stores 2048 parameters instead of 4096, excluding biases. It also removes responses outside that rank budget. Test it as a separate compression comparison, spelling out the operation meant by “low rank decay.” A penalty on singular values and a hard rank parameterization are different operations.

For the set prototype, keep architecture and seed policy fixed in the first experiment, use date-grouped development early stopping, and begin with the stated small architecture. If a neural optimizer is required, a declared initial Adam learning rate of $10^(-3)$ and a bounded epoch cap of fifty with five-epoch development patience form a starting numerical protocol; Chapter 7 explains its adaptive updates. Reduce the step if numerical fitting is unstable. This numerical starting convention has a different basis from the logistic $1/L_(0)$ bound; financial information theory has supplied the motivation for restraint, while development comparisons select these settings.

Every change—more heads, wider blocks, heavier dropout, or smaller rank—has an identifiable sacrifice and a development comparison. Many correlated asset rows do not independently justify more layers. Proper structure saves the need to learn arbitrary order; finite data still determine how much additional relational freedom can be supported.

== Choose a Loss for the Object Being Estimated

=== Probabilities, means, and rankings serve different consumers

Direction and first-passage gates consume probabilities, so fit class log loss and check calibration. Magnitude, volatility, or justified expected-return components may consume numerical estimates; squared loss estimates a conditional mean, as Chapter 1 derived. It does not force every predictor to memorize every future decimal. For our direction consumer, a probability objective directly serves the decision; precise-price MSE serves a different estimation task.

Class weighting changes probability meaning. If true up probability is $p$ and an up example is weighted by $w>0$, expected weighted binary log loss is minimized at

$
  q^(*)=frac(w p,w p+1-p).
$

Differentiate $-w p ln q-(1-p)ln(1-q)$ and solve for zero derivative to obtain this result. Unless $w=1$, the optimal weighted forecast is not the original up probability. Class balancing changes the probability interpretation, so applying a payoff threshold afterward calls for a corresponding calibration treatment. Our first probability prototype uses unit class weights; any reweighting requires a declared consumer and calibration/accounting treatment.

=== Relative selection: construct a pairwise objective

For one date, predicted scores $s_(i)$ should rank higher realized relative returns $r_(i)$ ahead of lower ones. For a non-tied pair set $y_(i,j)=sign(r_(i)-r_(j))$ and score difference $Delta_(i,j)=s_(i)-s_(j)$. Use

$
  ell_(i,j)=ln(1+exp(-y_(i,j)Delta_(i,j))).
$

Its derivative with respect to the score difference is $-y_(i,j)/(1+exp(y_(i,j)Delta_(i,j)))$. When a better-return asset is scored too low, descending the loss raises its score relative to the worse one. The smooth objective encodes order directly, without requiring an exact future quote or differentiating a discrete sorting operation.

Average non-tied pair losses within date, then average across training dates. Fix any pair sampling scheme and budget in development. Dates with no non-tied pairs are unavailable for that loss, not zero-loss successes. For very large sets, a documented sampled-pair approximation reduces computation while changing which comparisons receive supervision. Pairwise order does not price return spacing, tail losses, turnover, or benchmark constraints; the eventual portfolio remains a separate consumer.

=== An IC objective is a different, explicit comparison

For a date, center scores and returns: $u=s-overline(s)bold(1)$ and $v=r-overline(r)bold(1)$. Pearson information coefficient is

$
  "IC"(s,r)=frac(u^(T) v,norm(u) norm(v)).
$

This is the cosine of the angle between centered vectors.

A usable IC gradient requires the centering operation as well as the quotient rule. Let $H=I-bold(1)bold(1)^(T)/n$, so $u=H s$, $v=H r$, $H^(T)=H$ and $H^(2)=H$. For fixed nonconstant $r$ and nonconstant $s$, first differentiate with respect to $u$:

$
 nabla_(u)"IC"=frac(v,||u|| ||v||)-frac((u^(T)v)u,||u||^(3)||v||),
 quad nabla_(s)"IC"=H nabla_(u)"IC".
$

Both terms are centered, so applying $H$ leaves them unchanged. The training gradient for negative IC reverses this sign. This construction does not define a gradient at a zero denominator; such dates still need the explicit unavailable or modified-objective policy. Negating it supplies a differentiable correlation objective when both norms are nonzero. A constant score or constant realized-return cross-section makes the denominator zero; mark the date unavailable for IC and report coverage. Adding a numerical floor changes the objective and must be declared, not hidden as a perfect score.

Subtracting a common score offset and multiplying scores by a positive constant leave IC unchanged. Thus high IC cannot calibrate payoff magnitude. Spearman IC applies correlation to ranks and emphasizes ordering; exact ranks change discontinuously when scores cross, so a training objective needs a stated surrogate such as the pairwise loss above. Pearson IC, rank IC, class calibration, and net profit answer different questions.

Our relative-selection default is within-date pairwise logistic ranking loss, assessed with rank IC and net benchmark-relative portfolio results. Direct IC loss is a documented comparison when broad correlation is the intended consumer. Begin by separating prediction from portfolio accounting. End-to-end historical Sharpe optimization can then be evaluated as a broader search that also selects holding, cost, sizing, and risk choices. First stabilize prediction and portfolio accounting, then treat an economic-objective change as a new strategy comparison.

#heading(level: 2, numbering: none)[Practical Default: A Frozen Model Route]

#table(
  columns: (1fr, 1.65fr, 1.45fr),
  table.header([Task], [First model and objective], [Initial constraint]),
  [Engineered timing state], [Probability baseline, then boosted trees with binary or three-class log loss.], [Depth 3; shrinkage 0.03; cap 300 rounds; child weight 20; leaf L2 2.],
  [Frozen-side participation], [Small binary gate on forward-generated primary candidates.], [Depth 2; shrinkage 0.03; cap 150 rounds; child weight 50; leaf L2 4.],
  [Whole-date relations], [Shared context-aware controls, then nonpositional set attention with pairwise loss.], [Two blocks; width 64; four heads; dropout 0.2; date-grouped stopping.],
)

Timing trees use row/column sampling 0.8 and development log-loss stopping. Set attention uses the shared rowwise and mask conventions above; low rank is a separate comparison. Keep the opportunity set, label policy, feature availability, and confirmation period fixed across model comparisons. Record actual implementation versions and training budgets when running them. These lecture prototypes are specified experiments, not executed backtests.

For every parameter, ask what is restricted and why that restriction fits the remaining bottleneck. Learning rates set numerical or incremental response scales; penalties change objectives; architecture sets expressible relations; stopping governs accumulated adaptation. These controls govern how available information is used. Expansion is justified by a demonstrated missing relation whose incremental task value is independently confirmed.

*Self-check:* Why can doubling boosting rounds partly offset halving shrinkage? Why does a child-weight threshold not identify a universal number of examples? Does a shared per-asset tree violate row permutation equivariance? Why can a well-ranked score fail a probability threshold? The answers are respectively accumulated additive fit, objective-dependent curvature, no (but context may be missing), and the difference between relative order and calibrated probabilities.

#principle[*Chapter conclusion:* Select the loss from the decision object, the structure from the relation that remains to be expressed, and capacity from the freedom that can be supported. Our restrained timing and shallow set-relation prototypes make these choices explicit. Verification determines whether the extra expression improves the task enough to justify its cost.]


== One Model Route, Three Different Market Consumers

Model selection builds on the targets and features already constructed. The defaults above provide capacity starting points; the following market examples explain how the prototypes serve their tasks. Development comparisons select the eventual parameters from these initial settings.

=== A-share relative selection

Use a fixed historically eligible universe, completed-session features, and feasible entry/exit returns. Begin with the simple continuation score, its reversed score, and a shared per-asset linear ranking model with sector context. Then compare shallow boosted trees using the same date-wise ranking target. Context means an observation such as a stock's return minus its sector return, computed from available same-date data. Shared rowwise scoring already respects permutation equivariance; it does not automatically model interactions across the set.

Residual comparisons showing useful relations missed by engineered-context models provide the reason to add set attention. Fit and stop by dates, not randomly mixed stocks; many names on the same date share shocks. Keep the final benchmark-relative risk constraints outside the predictor. A high ranking score does not create a sell permission, borrow availability, or a cash-valued alpha estimate.

=== Crypto event participation

Start with a historical eligibility/liquidity gate and the frozen long-or-flat policy. A regularized logistic probability model is the first fitted consumer, with unit class weights and development calibration checks. Then compare the restrained binary tree gate already specified above. Split by chronological event groups and compare to opportunities matched on instrument liquidity and time state.

Do not balance away rare losses and read the output as an original success probability. Do not interpret 95% success on quiet opportunities as ability to recognize a liquidation cascade. Separately report event coverage, failure severity, and net payout. If an event class has too few independent mature examples, use a fixed protective rule and continue collecting eligible observations; a large neural network does not create missing adverse-event evidence.

==== A worked probability-to-participation check

Suppose a confirmed-in-development event model gives success probability 0.60, gain 30 basis points on success, loss 50 on failure, and cost 4. Its expected result is $18-20-4=-6$ basis points. The threshold is $frac(50+4,30+50)=0.675$. Abstention is the correct output despite a probability exceeding one half. If the forecast is not calibrated, first repair or compare calibration on held-out development predictions rather than treating this arithmetic as an established trading edge.

=== Equity-linked wrapper research

Fit separate open-reference and closed-reference baselines before combining their regimes. A small state model can predict token-return direction or a specific policy's success. A relation model instead predicts an executable convergence outcome; its labels require both legs and a holding/funding policy. Do not pool direct shares, spot wrappers, and perpetuals as interchangeable rows merely because their company name matches.

Compare with “no change,” an available reference/proxy move, and no trade. Freeze observation timing and costs across these comparisons. If the wrapper-specific model has no net increment over the proxy, simplify the route. Further depth would require a new, specific relational hypothesis.

=== What the institution evidence does—and does not—support

Hurst, Ooi, and Pedersen's historical trend-following study constructs a multi-market time-series momentum comparison reaching back to 1880. It supports taking simple direction-oriented signals seriously as research baselines; it does not validate our five-minute crypto event rule, an A-share continuation orientation, or a particular wrapper. Likewise, a trader's preference for fast, inspectable trees motivates an efficient workflow but does not establish that every private fund uses them or that neural models are never useful.

In practice, choose the target, structure, and capacity from the action, missing relation, and available independent evidence in that order. Start with a predeclared modest model ladder, and investigate further architectural complexity when a specific remaining mechanism warrants the search budget. Chapter 7 then explains how curvature and noise give learning rates their role in fitting.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Wassily Hoeffding. #link("https://doi.org/10.1080/01621459.1963.10500830")[_Probability Inequalities for Sums of Bounded Random Variables_]. _Journal of the American Statistical Association_ 58(301), 13–30, 1963.
- Tianqi Chen and Carlos Guestrin. #link("https://arxiv.org/abs/1603.02754")[_XGBoost: A Scalable Tree Boosting System_]. KDD, 2016. See also the #link("https://xgboost.readthedocs.io/en/stable/parameter.html")[official parameter reference] and #link("https://xgboost.readthedocs.io/en/stable/tutorials/model.html")[boosted-tree tutorial] for implementation semantics.
- Juho Lee, Yoonho Lee, Jungtaek Kim, Adam R. Kosiorek, Seungjin Choi, and Yee Whye Teh. #link("https://proceedings.mlr.press/v97/lee19d.html")[_Set Transformer: A Framework for Attention-based Permutation-Invariant Neural Networks_]. ICML, PMLR 97, 3744–3753, 2019.
- Biao Zhang and Rico Sennrich. #link("https://arxiv.org/abs/1910.07467")[_Root Mean Square Layer Normalization_]. NeurIPS, 2019.
- Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani. #link("https://www.statlearning.com/")[_An Introduction to Statistical Learning, with Applications in R_]. Second edition, Springer, 2021.
- Brian Hurst, Yao Hua Ooi, and Lasse Heje Pedersen. #link("https://www.aqr.com/insights/research/journal-article/a-century-of-evidence-on-trend-following-investing")[_A Century of Evidence on Trend-Following Investing_]. _The Journal of Portfolio Management_ 44(1), 15–29, 2017. Historical multi-market research, not a live result for our market-specific prototypes.
]

#pagebreak()

= Optimization: Search with the Feedback the Problem Actually Provides
#counter(math.equation).update(0)

A factor expression proposes a way to measure the market. Assessing its usefulness involves three distinct achievements: finding a high historical score, solving a numerical problem, and establishing a relation that survives outside the search data. This chapter constructs the search operations. Chapter 8 places these operations inside an evidence pipeline.

Our selected first route is small, economically motivated, typed symbolic search. Use actual gradients for continuous fitting when they exist. Use genetic programming for legal discrete expressions when they do not. A learned generator can subsequently be compared as a proposal mechanism, with evaluation costs and independent confirmation included in the comparison.

== Fix the Candidate, Objective, and Feedback

Let $cal(A)$ be the set of legal factor expressions and $Q_(D) (f)$ a score computed on development data $D$. The search problem is $max_(f in cal(A)) Q_(D) (f)$. For continuous parameters $theta$, it is convenient instead to minimize $J(theta)$. A rank correlation, probability loss, and net-policy return are different scores. None is automatically the usable-information quantity of Chapter 2.

To separate the score from the relation we want, write $Q(f)$ for candidate usefulness under the declared evaluation law and policy, and define $epsilon_(D)(f)=Q_(D)(f)-Q(f)$. Thus $Q_(D)(f)=Q(f)+epsilon_(D)(f)$. The discrepancy can contain finite-sample noise, proxy mismatch, and distribution change; defining it does not make it mean-zero. Even mean-zero noise for each fixed candidate can become positive after selecting the largest observed score. Chapter 8 constructs that selection effect. A separate confirmation operation then tests whether the numerical improvement also improves the relation we want to use.

Define legality before maximizing anything. A leaf carries asset identity, availability time, unit, and missingness. An operator carries compatible input/output types and a temporal convention. Adding price to price preserves price units; adding price to traded volume has no agreed unit. Dividing two simultaneous positive prices can produce a dimensionless relation. A window operator must run inside an ordered asset history, not across adjacent rows of a shuffled matrix.

A safe initial grammar uses Chapter 5's dimensionless state leaves; addition/subtraction of matching units; multiplication and declared ratios; within-asset lag, difference, and rolling mean over a small window set. Reject a ratio with an invalid denominator rather than silently replace it by one. A protected numerical division is a different function and needs a documented economic meaning. Depth, node count, allowed windows, and duplicated expressions constrain the candidate set.

*Zeroth-order* feedback gives only a function value. *First-order* feedback also gives derivatives. *Second-order* feedback includes curvature. These terms describe the feedback available to an algorithm; quality depends on how effectively it uses that feedback for the task. Changing a tree node from close to volume is a discrete operation; there is no derivative with respect to that substitution. Sorting, thresholding, fills, and a black-box replay can also prevent direct differentiation even when some inputs are continuous.

== Construct Direction from a Derivative

=== The steepest local move depends on the displacement metric

For a differentiable scalar objective at $theta$, write $g=nabla J(theta)$. A small displacement $d$ gives $J(theta+d)=J(theta)+g^(T) d+o(norm(d))$. Among displacements of fixed Euclidean length $h$, Cauchy–Schwarz gives $g^(T) d>=-norm(g)h$. Equality occurs at $d=-h g/norm(g)$ when $g$ is nonzero. This motivates the gradient step $theta^(+)=theta-alpha g$.

The argument is local and uses Euclidean distance in this parameterization. Changing units changes that distance. It does not prove that an arbitrarily large step will improve the actual objective. Suppose gradients obey $norm(nabla J(a)-nabla J(b))<=L norm(a-b)$ along the relevant segment. Integrate the gradient difference along $theta+s d$, $0<=s<=1$:

$
  J(theta+d)-J(theta)-g^(T) d
    =integral_(0)^(1) [nabla J(theta+s d)-g]^(T) d dif s
    <=frac(L,2)norm(d)^(2).
$

Substitute $d=-alpha g$ to recover the Chapter 6 descent bound:

$
  J(theta-alpha g)<=J(theta)-alpha(1-L alpha/2)norm(g)^(2).
$

A known bound permits $alpha=1/L$. Without one, start a trial step and repeatedly halve it until $J(theta-alpha g)<=J(theta)-alpha norm(g)^(2)/2$. Under the local smoothness condition, sufficiently small positive steps pass. This *backtracking* rule turns local smoothness into an operational step-selection procedure. Stop on a declared gradient or relative-objective tolerance and an iteration cap. A zero gradient is a stationary point; without convexity it need not be a global minimum. Noisy minibatch evaluations do not inherit this deterministic acceptance test unchanged.

=== Curvature can change direction as well as length

The second-order approximation is $J(theta)+g^(T) d+d^(T) H d/2$, where $H$ is the Hessian. If $H$ is positive definite, setting the approximation's derivative to zero gives $H d=-g$. The *Newton direction* therefore scales and mixes coordinates through $H$, rather than merely shrinking a gradient step.

For $J(x,y)=(a x^(2)+b y^(2))/2$ with $a$ much greater than $b>0$, gradient descent contracts coordinates by $1-alpha a$ and $1-alpha b$. The large curvature limits a stable common step while the small curvature converges slowly. Exact Newton removes this imbalance for the quadratic in one step. In a nonlinear objective, the quadratic approximation is only local; indefinite curvature, singular systems, and the cost of estimating/solving for $H$ require safeguards or approximations. Financial reliability is assessed through the evidence pipeline, separately from this numerical curvature advantage.

Backpropagation computes derivatives by organizing the chain rule through a computation graph. For $z=h(theta)$ and $J=j(z)$, multiply the downstream derivative by the derivative of $h$, accumulating contributions wherever a parameter is reused. Its cost is comparable to a few passes through that graph, not independent of its size. It cannot differentiate an unspecified fill engine merely because neural layers occur before the engine.

== Derive the Learning-Rate and Noise Trade-Off

=== A minibatch estimates the empirical gradient

If $J=N^(-1)sum_(i=1)^(N) J_(i)$, sample $B$ indices uniformly with replacement and average their gradients. Linearity of expectation gives $E[hat(g) mid(|) theta]=nabla J(theta)$. This is unbiased for the fixed *empirical* objective. Its reference is the fixed historical objective; tomorrow's population objective can differ.

For independent gradient noise with coordinate variance $v$, the averaged variance is $v/B$. More generally,

$
  Var(frac(1,B)sum_(i=1)^(B) g_(i))
    =frac(1,B^(2))sum_(i=1)^(B) sum_(j=1)^(B) Cov(g_(i),g_(j)).
$

Uniform sampling from a fixed file and genuine independence of market opportunities are different conditions. Adjacent quotes, overlapping trades, and same-date stocks can share information and outcomes. A large batch can be necessary to represent a whole date correctly without being a large independent sample.

=== Solve a noisy scalar quadratic before interpreting an optimizer

Let $J(w)=a(w-w_(*))^(2)/2$, $a>0$, and error $e_(k)=w_(k)-w_(*)$. Suppose the gradient estimator is $a e_(k)+xi_(k)$, with conditional mean-zero noise and conditional variance $v/B$. A constant step yields

$
  e_(k+1)=(1-alpha a)e_(k)-alpha xi_(k),
  \
  E e_(k+1)^(2)=(1-alpha a)^(2) E e_(k)^(2)+alpha^(2) v/B.
$

The cross term vanishes because $e_(k)$ is known before the mean-zero new noise.

Indeed, expanding the update squared gives $(1-alpha a)^(2)e_(k)^(2)-2alpha(1-alpha a)e_(k)xi_(k)+alpha^(2)xi_(k)^(2)$. Conditional expectation removes the middle term. Put $rho=(1-alpha a)^(2)$ and $c=alpha^(2)v/B$. Repeated substitution yields the finite result

$
 E e_(k)^(2)=rho^(k)E e_(0)^(2)+c sum_(j=0)^(k-1)rho^(j)
 =rho^(k)E e_(0)^(2)+c frac(1-rho^(k),1-rho).
$

For $rho<1$, equivalently $0<alpha<2/a$, the initial term vanishes and the geometric sum converges; this stability condition is essential to taking the limit. The limiting formula therefore depends on stable curvature scaling as well as the noise model. Without noise, $0<alpha<2/a$ contracts the error geometrically. With noise, sum the geometric recurrence. For the same stable range, its limiting mean-square error is

$
  V=frac(alpha^(2) v/B,1-(1-alpha a)^(2))
    =frac(alpha v,B a(2-alpha a)).
$

At $a=1,v=1,B=10$, step 0.1 gives $V$ about 0.00526 and contraction factor 0.9; step 0.01 gives $V$ about 0.000503 but factor 0.99. The smaller step lowers late fluctuation and slows early progress. Increasing independent averaging lowers the fluctuation without changing the deterministic contraction, but costs more computation per update.

A decreasing step can remove the floor in this example. Index steps from $k=1$ and choose $alpha_(k)=1/(a k)$. Then $k e_(k+1)=(k-1)e_(k)-xi_(k)/a$. Telescoping gives $e_(k+1)=-sum_(j=1)^(k) xi_(j)/(a k)$, hence $E e_(k+1)^(2)=v/(B a^(2) k)$ for independent equal-variance noises. This proves a rate for this scalar construction, not for every nonconvex neural optimizer.

#principle[*Step-size conclusion:* Curvature sets the stable scale; noise and averaging set late fluctuation; the update budget sets how much progress can be bought. Step size balances progress against fluctuation. Numerical descent, out-of-sample generalization, and market advantage are three different checks.]

=== Thin information does not prescribe a universal tiny step

Take $Y=beta X+epsilon$ with independent centered variables and squared loss $(w X-Y)^(2)$. The population gradient is $2(w-beta)E X^(2)$. At $w=beta$, the single-example gradient is $-2X epsilon$, with variance $4 Var(epsilon)E X^(2)$. A small signal coefficient and large outcome noise make estimation difficult even though the population optimization problem is a simple convex quadratic.

For Gaussian $X$ and $epsilon$, the entropy calculation from Chapter 1 gives, in natural-log units,

$
  I(X;Y)=frac(1,2)ln(1+frac(beta^(2) Var(X),Var(epsilon))).
$

Now multiply the entire loss by $c>0$. The observations and this information are unchanged, but the gradient and curvature multiply by $c$. The safe numerical step must divide by $c$ to preserve the same update. Rescaling a parameter can likewise alter geometry without altering the market experiment. Therefore information cannot by itself specify a learning rate. Thin information motivates stricter estimation and confirmation, capacity supported by evidence, and measured noise control. Curvature and update noise supply the numerical basis for a step size.

=== Momentum smooths history and introduces lag

For a scalar gradient observation $g_(k)=g_(*)+xi_(k)$, define $m_(k)=beta m_(k-1)+(1-beta)g_(k)$ with $0<=beta<1$. Expanding the recurrence gives geometrically declining weights $(1-beta)beta^(j)$ on earlier gradients. With independent stationary noise of variance $v$, the long-run variance is

$
  Var(m)=v(1-beta)^(2) sum_(j=0)^(infinity) beta^(2j)
    =v frac(1-beta,1+beta).
$

This calculation explains smoothing. The history scale is roughly $1/(1-beta)$ updates, so it also explains lag when the true gradient changes. A parameter update using momentum can accumulate consistent movement and reduce oscillation; the stationary averaging calculation is not a convergence theorem for every momentum rule.

Adam additionally averages squared gradients. In vector notation, with squares and divisions performed coordinatewise,

$
  m_(k)=beta_(1) m_(k-1)+(1-beta_(1))g_(k),
  \
  v_(k)=beta_(2) v_(k-1)+(1-beta_(2))g_(k)^(2),
  \
  hat(m)_(k)=frac(m_(k),1-beta_(1)^(k)), quad
  hat(v)_(k)=frac(v_(k),1-beta_(2)^(k)), quad
  theta_(k+1)=theta_(k)-alpha frac(hat(m)_(k),sqrt(hat(v)_(k))+epsilon).
$

The corrections remove zero-initialization attenuation for stationary averages. The denominator estimates gradient scale, the quantity relevant to coordinatewise numerical movement. Market volatility belongs to a separate estimation task. The smoothing horizons and numerical $epsilon>0$ affect the actual move. AdamW separates a decay factor, giving $theta^(+)=(1-alpha lambda)theta-alpha hat(m)/(sqrt(hat(v))+epsilon)$ on designated coefficients. Putting L2 into an adaptive gradient instead changes its moving averages and coordinate scaling; the two operations are not generally equivalent. State which parameters receive decay, particularly intercepts and normalization gains.

== Search When Only Scores Are Available

=== Finite differences buy a direction with evaluations

For coordinate $i$, central difference is

$
  hat(g)_(i)=frac(J(theta+h e_(i))-J(theta-h e_(i)),2h).
$

Taylor expansion cancels even terms, leaving derivative error of order $h^(2)$ when a bounded third derivative is available. With independent evaluation noise of variance $s^(2)$ on each score, the difference's noise variance is $s^(2)/(2h^(2))$. Tiny $h$ reduces truncation error but amplifies score noise. Computing all $d$ coordinates requires roughly $2d$ evaluations. Common random numbers can reduce difference noise in a simulation, but only with a declared coupling that preserves the evaluated objective.

=== Random perturbations differentiate a smoothed objective

Let $epsilon$ have standard Gaussian coordinates and define $J_(sigma) (theta)=E J(theta+sigma epsilon)$, $sigma>0$. Equivalently integrate $J(z)$ against Gaussian density centered at $theta$. Differentiating that density contributes $(z-theta)/sigma^(2)$. With integrability and justified differentiation under the integral,

Write the density explicitly as $p_(theta)(z)=(2pi sigma^(2))^(-d/2)exp(-||z-theta||^(2)/(2sigma^(2)))$. Its derivative is $nabla_(theta)p_(theta)(z)=p_(theta)(z)(z-theta)/sigma^(2)$: differentiation of the squared distance supplies the sign. Thus $nabla J_(sigma)=integral J(z)p_(theta)(z)(z-theta)/sigma^(2)dif z$. Changing variables $z=theta+sigma epsilon$ turns this integral into the expectation below. The direction comes from differentiating the smooth density while retaining the black-box values of $J(z)$.

$
  nabla J_(sigma) (theta)=frac(1,sigma)E[J(theta+sigma epsilon)epsilon].
$

A Monte Carlo average of perturbations estimates this gradient. A baseline independent of the current perturbation leaves its expectation unchanged because $E epsilon=0$. The estimate targets the *smoothed* function; it need not be unbiased for $nabla J(theta)$. Smoothing, evaluation noise, and dimension affect the comparison.

Expose the dimension cost with noiseless $J(theta)=a^(T) theta$. Subtracting $J(theta)$ gives one-direction estimator $g=(a^(T) epsilon)epsilon$. Since $E[epsilon epsilon^(T)]=I$, $E g=a$. Rotate coordinates so $a=norm(a)e_(1)$, which Gaussian rotational symmetry allows. Then

$
  E norm(g)^(2)=norm(a)^(2) E[epsilon_(1)^(2) sum_(j=1)^(d) epsilon_(j)^(2)]
    =(d+2)norm(a)^(2).
$

The first-coordinate term is three; the other $d-1$ terms are one each. These Gaussian moments follow from integration by parts: $E Z^(4)=3E Z^(2)=3$.

The moment identity uses $phi'(z)=-z phi(z)$: $integral z^(4)phi(z)dif z=-integral z^(3)phi'(z)dif z=3integral z^(2)phi(z)dif z=3$, because polynomial times Gaussian density vanishes at both infinite endpoints. For $j!=1$, independent coordinates give $E[epsilon_(1)^(2)epsilon_(j)^(2)]=1$. Finally $E||g-a||^(2)=E||g||^(2)-2a^(T)E g+||a||^(2)=E||g||^(2)-||a||^(2)$. This accounts for both the fourth moment and the subtraction used by the dimension calculation. Subtract $norm(E g)^(2)$ to obtain $E norm(g-a)^(2)=(d+1)norm(a)^(2)$. Averaging $m$ independent directions divides this error by $m$. This is a transparent reason that a few random queries can poorly recover a high-dimensional direction. This cost calculation concerns the stated random-direction estimator. Other black-box constructions can have different costs, and parallel throughput measures elapsed work rather than evaluations needed.

=== Genetic programming operates directly on legal trees

An expression tree has observations as leaves and operators as internal nodes. A small initial population can be scored, a few parents selected, and new candidates formed by subtree mutation or crossover. Crossover must preserve operator types and availability. Penalizing node count discourages expressions that grow only to exploit accidental detail; it changes the reward and its coefficient is itself a development choice.

For a reproducible teaching search, begin with 100 legal candidates, ten generations, maximum depth three and fifteen nodes, windows 5/10/20, and a cap of 1,000 scored proposals including invalid attempts. Retain five elites; choose parents by tournaments of three; allocate remaining proposals between type-safe subtree crossover and mutation. Record probabilities and seeds before running. Simplify exact duplicates and cache shared computations. Evaluation and attempted-proposal counts must both be visible: invalid proposals did not produce usable evaluations, but are part of search cost.

Score fixed-orientation candidates on chronological development folds using the same future label and a frozen simple consuming model. Do not take absolute IC and then silently select its sign on confirmation. If orientation is selected in development, record and freeze it. Use a recorded predictive reward with a declared complexity penalty; report policy costs separately unless the frozen reward already includes them. Distinguishing true signal from a lucky score is the role of independent confirmation, after the generations and selection rule have produced candidates.

Simulated annealing offers another score-only route: propose a legal neighbor, accept improvements, and accept a worsening of minimization objective by $Delta>0$ with probability $exp(-Delta/T)$ at temperature $T>0$. A decreasing temperature reduces willingness to move uphill. It requires a proposal and cooling schedule; it does not promise the global optimum under arbitrary finite settings.

== Learn Proposal Preferences without Differentiating the Backtest

Suppose a grammar-constrained generator assigns probability $pi_(theta) (f)$ to expression $f$, and the frozen development evaluator returns reward $R(f)$. For a finite grammar, differentiate its expected reward term by term:

$
  nabla_(theta) sum_(f) pi_(theta) (f)R(f)
    =sum_(f) pi_(theta) (f)R(f)nabla_(theta) ln pi_(theta) (f).
$

Sampling expressions therefore estimates a gradient of proposal quality even if $R$ itself contains nondifferentiable sorting or fills. A candidate-independent baseline $b$ preserves expectation because $sum_(f) nabla pi_(theta) (f)=nabla 1=0$. Updating in the ascent direction of $(R-b)nabla ln pi$ increases tendencies associated with above-baseline outcomes. This is the score-function or policy-gradient construction underlying a learned factor generator.

If expression tokens are $a_(1),...,a_(L)$, their probability is the product of conditional probabilities. Its log gradient is $sum_(j) nabla ln pi_(theta) (a_(j) mid(|) a_(1),...,a_(j-1))$. One terminal reward weights the whole sequence. That explains sparse feedback and difficult assignment of credit to individual operations. A consistently applied grammar mask enforces syntactic legality. Economic validity is then assessed through the evaluator and confirmation process.

A learned generator shares experience through continuous parameters and can reuse productive motifs. Genetic populations also inherit useful structure. Compare them under the same legal set, evaluator, proposal/evaluation budget, confirmation protocol, and total resource cost. Pretraining and updating overhead belong in that comparison. The backtest remains a costly, noisy black box; gradients of generation probabilities have not made it differentiable or proved financial superiority.

#principle[*Search conclusion:* Prefer actual derivatives for continuous tasks that supply them. Use bounded typed GP as the first automatic symbolic route. Compare learned proposals when shared motifs can justify their overhead. The optimized development reward remains a proxy requiring independent confirmation.]

#heading(level: 2, numbering: none)[Practical Default and Diagnostic Actions]

Freeze the target, legal grammar, scorer, resource budget, and shortlist rule before search. Use the GP prototype above as the symbolic control; promote only its frozen shortlist to Chapter 8's untouched confirmation. Count failed and related searches. For directly differentiable full-gradient teaching problems, use a credible curvature bound or the backtracking construction, not a guessed universally tiny step.

Chapter 6's initial Adam run remains a control. For the neural training-route comparison, use normalized inputs and mean loss; compare AdamW initial rates $10^(-4),3 times 10^(-4),10^(-3)$ in an earlier development pilot with identical architecture, date-grouped batches, epoch cap, and stopping. Freeze smoothing/decay conventions as part of that route rather than vary every knob simultaneously. These rates are starter settings, not information-theoretic estimates. A later Adam-versus-AdamW comparison must include its extra selection and decay budget.

Distinguish three observations. Numerical instability calls for unit, derivative, and step repair. A widening training–validation gap calls for stopping or capacity/regularization review. Flat independent performance after stable fitting calls for a target/representation review. Once fitting is stable, a target or representation review is more informative than continued reductions in the learning rate.

*Self-check:* If every loss is multiplied by 100, does unchanged mutual information imply an unchanged safe step? If a score-only random-direction estimate is unbiased, for which function is it unbiased? Does a policy-gradient generator need a derivative through the expression's backtest? The answers are no, the declared smoothed function, and no: its derivative passes through generation probabilities.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Léon Bottou, Frank E. Curtis, and Jorge Nocedal. #link("https://arxiv.org/abs/1606.04838")[_Optimization Methods for Large-Scale Machine Learning_]. _SIAM Review_ 60(2), 223–311, 2018; preprint 2016. Optimization and stochastic-gradient background.
- Diederik P. Kingma and Jimmy Ba. #link("https://arxiv.org/abs/1412.6980")[_Adam: A Method for Stochastic Optimization_]. ICLR, 2015. Ilya Loshchilov and Frank Hutter. #link("https://arxiv.org/abs/1711.05101")[_Decoupled Weight Decay Regularization_]. ICLR, 2019. Definitions of the adaptive and decoupled-decay updates.
- Tim Salimans et al. #link("https://arxiv.org/abs/1703.03864")[_Evolution Strategies as a Scalable Alternative to Reinforcement Learning_]. 2017. Black-box perturbation search; not evidence for financial factor efficiency.
- Ronald J. Williams. #link("https://doi.org/10.1007/BF00992696")[_Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning_]. _Machine Learning_ 8, 229–256, 1992. Score-function gradient methods.
]

#pagebreak()

= The Factor Pipeline: Discovery Produces Candidates, Verification Produces Trust
#counter(math.equation).update(0)

An optimizer can generate a thousand impressive expressions before lunch. The useful output is much smaller: a factor definition with evidence, use conditions, and an executable role in a strategy. We now construct the process that turns proposals into that output. Its central separation is between data used to improve proposals and data reserved to assess the frozen result.

The first factory should be small and auditable: immutable inputs, a typed generator, a deterministic development scorer, a frozen shortlist, separate confirmation, a factor dossier, and monitored consumption. Measured evaluation work provides the basis for expanding infrastructure.

== Understand the Winner's Selection History

=== One fair experiment and many opportunities to be lucky

Suppose a prespecified direction rule predicts 100 independent fair signs. Its hit count has a binomial distribution with parameters 100 and one half. A one-sided tail probability asks how often that null experiment produces at least the observed count. This is a *p-value*: a probability of an outcome at least as extreme under the stated null, not the probability that the rule has no edge.

If a test has false-positive probability $alpha$ and we perform $M$ independent null tests, the probability that at least one appears significant is

$
  1-(1-alpha)^(M).
$

At $alpha=0.05,M=100$, it is about 0.994. Under arbitrary dependence the union bound still gives an upper bound $M alpha$. Allocating each of $M$ prespecified tests level $alpha/M$ therefore controls the probability of any false positive by $alpha$. This is the Bonferroni construction. Applying this accounting to a search therefore includes failed windows, orientations, targets, and model variants alongside published winners.

Adaptive search is more complicated than $M$ independent prespecified tests. The next candidate can depend on earlier observed scores. Preserving the full selection procedure and its null assumptions makes that dependence inspectable. The raw count records the search history; an effective number of independent experiments calls for additional assumptions.

=== Derive the attractive-score scale under an ideal null

Let each prespecified standardized null score $Z_(j)$ be standard normal. Completing the square in its density gives

$
  E exp(a Z)=frac(1,sqrt(2 pi))integral_(-infinity)^(infinity) exp(a z-z^(2)/2)dif z
    =exp(a^(2)/2).
$

Markov's inequality from Chapter 6 then yields $Pr(Z>u)<=exp(-a u+a^(2)/2)$. Set $a=u>0$ and union-bound the candidates:

$
  Pr(max_(j<=M)Z_(j)>u)<=M exp(-u^(2)/2).
$

The bound needs no independence between candidates with those marginal nulls. A sufficient threshold for family error at most $alpha$ is $sqrt(2 ln(M/alpha))$. Independence is needed for the exact maximum distribution $Pr(max_(j) Z_(j)<=u)=Phi(u)^(M)$, where $Phi$ is the standard-normal cumulative probability.

For positive $u$, write tail $q(u)=integral_(u)^(infinity) phi(z)dif z$, where $phi$ is the normal density. Since $phi'(z)=-z phi(z)$, integration by parts gives $q(u)=phi(u)/u-integral_(u)^(infinity) phi(z)/z^(2) dif z$. The nonnegative remainder is at most $q(u)/u^(2)$. Rearranging bounds the tail between $phi(u)u/(1+u^(2))$ and $phi(u)/u$. To locate a typical maximum, set roughly $M[1-Phi(u)]$ to one. Taking logs gives $u^(2)/2+ln u$ approximately $ln M-(ln(2 pi))/2$. The leading scale is therefore $sqrt(2 ln M)$, with logarithmic corrections. It is not the exact expected maximum or a new market constant.

If an ideal correlation statistic has an approximately standard-normal null distribution for $sqrt(n)hat("IC")$, the leading best-noise correlation scale becomes

$
  sqrt(frac(2 ln M,n)).
$

At $M=200000,n=2500$, it is about 0.099. This explains how extensive search can manufacture a historically striking small correlation. It is not a universal 0.099 admission threshold. Ranked labels, dependence, overlapping outcomes, and adaptively generated factors require the relevant null procedure rather than mechanical substitution of row counts.

#principle[*Selection principle:* Interpret a score together with the choices that produced it. Search explores existing historical realizations, so additional candidates also increase opportunities to select their noise. Preserve unsuccessful trials and related redesigns. Related redesigns retain their selection history even when the generator receives a new name.]

=== Economic logic restricts hypotheses before seeing the winner

A term-structure hypothesis can specify the simultaneous contracts, sign convention, holding role, and regimes in which the relation might fail. That removes unjustified combinations before search. In the ideal maximum calculation, reducing $M$ to $m<M$ reduces the leading scale from $sqrt(2 ln M)$ to $sqrt(2 ln m)$.

An economic explanation is most useful when it shapes the test before evidence is inspected. A wrong monotone prior can exclude useful responses; an unexplained but independently confirmed factor need not be false. Translate the explanation into a constraint or a refutable comparison before inspecting the winner; this gives it a role beyond explaining a profitable-looking tree after the search.

== Separate Development from Confirmation across the Whole Chain

=== Construct Temporal Splits from Information Dependencies

For each opportunity retain information cutoff $t_(i)$, entry $e_(i)$, executed exit $x_(i)$, and label availability $k_(i)$. Chapter 3 distinguished trigger maturity from full payout maturity. Economic comparisons use the entire interval through execution and cost availability. For a model fitted at $T$, use only examples whose required labels satisfy $k_(i)<=T$.

Suppose a training decision occurs on day 8, entry on day 9, and exit on day 14, while a validation block begins on day 11. A decision-date split assigns this row to training, yet it uses outcome information from validation. *Purging* removes training examples whose required outcome intervals overlap the held-out outcome region. The label's realized endpoint, not a nominal horizon copied into a header, decides overlap.

An *embargo* is an additional excluded interval selected to prevent identified dependencies around a held-out block. In schemes using post-block training data, future rows may contain lookbacks reaching into the held-out interval; those rows need corresponding separation or exclusion. Forward-only fitting never uses later training rows, but still needs mature labels and any gap justified by outcome or input dependencies. A universal one-percent gap cannot be inferred from the word embargo.

Fit scaling, imputation, feature selection, probability calibration, primary models, meta-gates, and portfolio parameters within their allowed development partitions. A model comparison using a later period is itself selection. Individually confirmed factors do not make an arbitrary new combination confirmed.

For a teaching dataset covering ten years, use years 1–8 for development and reserve years 9–10 for one frozen confirmation batch. Three expanding development evaluations can fit on completed data from years 1–5, 1–6, and 1–7 and evaluate years 6, 7, and 8 respectively. Apply maturity and overlap checks at every boundary. These divisions are a teaching protocol, not a claim that every strategy has enough independent evidence in ten years.

After freezing definitions and settings, fit using eligible development data and replay the complete route in years 9–10. Any scheduled updating must use only then-mature information under a frozen update policy. Inspecting confirmation and redesigning the strategy turns that result into development for the next version. It cannot keep its original status just because its file remains named `test`.

=== Account for Dependence in Uncertainty

For measured values $Z_(t)$, expand the variance of their mean:

$
  Var(frac(1,n)sum_(t) Z_(t))=frac(1,n^(2))sum_(t) sum_(s) Cov(Z_(t),Z_(s)).
$

Independent equal-variance values give $v/n$. Positively correlated values include extra terms. Duplicating one observation $n$ times leaves mean variance $v$, not $v/n$. This simple endpoint shows why same-day asset rows, shared event outcomes, and overlapping holdings cannot be counted as automatically independent breadth.

Compare candidates on the same chronological blocks so each difference refers to the same conditions. A time-block resampling comparison draws whole consecutive blocks rather than individual rows, retaining some local dependence. Its block length and validity depend on the process; it does not solve unbounded memory or structural drift. State the grouping, null, and uncertainty method. Combinatorial purged splits can explore robustness, but fitting on dates after a held-out date is not a deployable historical forecast at that date.

== Sharpe Needs an Estimation and Selection Account

=== Construct the ratio and its first-order uncertainty

For single-period excess returns with population mean $mu$ and positive standard deviation $sigma$, define Sharpe $S=mu/sigma$. Estimate both from the same return sample. A high estimate can result from an overestimated mean, an underestimated dispersion, or selection among many estimates.

Write centered return $X=R-mu$, skewness $gamma_(3)=E X^(3)/sigma^(3)$, and kurtosis $gamma_(4)=E X^(4)/sigma^(4)$. Kurtosis here is not excess kurtosis. Under IID returns and finite fourth moment, the leading sample-mean and variance perturbations have

$
  Var(delta mu)=frac(sigma^(2),n), quad
  Var(delta v) approx frac(sigma^(4) (gamma_(4)-1),n), quad
  Cov(delta mu,delta v) approx frac(sigma^(3) gamma_(3),n).
$

To see the last two expressions, approximate $delta v$ by the average of $X_(t)^(2)-sigma^(2)$ and $delta mu$ by the average of $X_(t)$. Their one-period variance is $E X^(4)-sigma^(4)$, and covariance is $E X^(3)$. Estimating the mean inside sample variance changes lower-order terms.

Differentiate $mu/sqrt(v)$ at $v=sigma^(2)$:

$
  delta S approx frac(delta mu,sigma)-frac(mu,2sigma^(3))delta v.
$

Squaring, averaging, and substituting the three moments gives

The cross term captures how mean and variance estimation move together. Retaining it gives the full first-order calculation. With $A=1/sigma$ and $B=-mu/(2sigma^(3))$, the leading variance is $A^(2)Var(delta mu)+B^(2)Var(delta v)+2A B Cov(delta mu,delta v)$. The three substitutions are respectively $1/n$, $S^(2)(gamma_(4)-1)/(4n)$, and $-S gamma_(3)/n$. Adding them gives the stated numerator. The minus sign in the skewness term comes from differentiating the inverse square root of variance.

$
  "se"(hat(S))^(2) approx frac(1-gamma_(3) S+(gamma_(4)-1)S^(2)/4,n).
$

This is a leading asymptotic standard-error calculation. Approximate normal inference additionally uses a central-limit theorem: suitably normalized IID averages with finite variance converge in distribution to a normal law. It supplies an approximation as sample size grows, not an exact finite-sample certificate. Serial dependence, unstable moments, and absent fourth moments require a different inference route.

For Gaussian returns, $gamma_(3)=0,gamma_(4)=3$, so the numerator becomes $1+S^(2)/2$. Different tail shapes can therefore change reliability even with the same estimated mean and volatility. Use single-period units consistently. Annualization by $sqrt(A)$ requires appropriate temporal scaling; multiplying the estimate while leaving its standard error unchanged is invalid.

=== Adjust the comparator after search

Testing against Sharpe zero asks whether a prespecified strategy exceeds zero. Testing the best of many null trials asks a different question. In an illustrative independent Gaussian trial model, let candidate estimates be $S_(j)=mu_(0)+tau Z_(j)$. The expected best null estimate is

$
  S_(0)=mu_(0)+tau integral_(-infinity)^(infinity) z M phi(z)Phi(z)^(M-1)dif z.
$

Differentiate the maximum distribution $Phi(z)^(M)$ to obtain this density; the integral is its expected value. It gives a constructive benchmark when the independent equal-dispersion trial model is actually appropriate. Leading extreme-value approximations can reduce numerical work, but their error and trial model must be preserved.

The deflated Sharpe ratio (DSR) combines a selection-adjusted benchmark with nonnormal-return estimation. A normal-approximation support statistic has the form $Phi((hat(S)-S_(0))/hat("se"))$, with the published method specifying benchmark and finite-sample conventions. It is not Sharpe minus a correction, nor an unconditional posterior probability of profit. Candidate dependence changes the independent-trial approximation; raw trial count, estimated effective trials, and assumptions must remain separate. Feeding DSR back into generation makes it another development reward, not untouched confirmation.

#principle[*Verification conclusion:* Inferential gates address the complete selection chain. Predictive support, tail-sensitive estimation, incremental portfolio value, and execution viability are separate tests. No one IC, p-value, or DSR threshold can replace the joint admission decision.]

== Admit a Dossier and Test Incremental Use

A factor dossier preserves expression and operator versions; origin and parents; units and missingness; data/universe/time rules; label and execution policy; search history; development and confirmation partitions; predictive and net-policy results; risk exposures; turnover/capacity; and failure conditions. The consuming model receives a definition with an orientation and scope, not an unexplained string that once won a tournament.

For an existing consuming route $C$, compare $Q(C+f)-Q(C)$ under one fixed protocol. A candidate that duplicates an existing signal may add no value even if it passes a standalone test. High correlation identifies potential redundancy, not automatic uselessness; low Pearson correlation is not independence. A nonlinear or regime complement can survive those simple summaries and still needs a recorded incremental comparison.

A concrete small scorer can use mean development Brier improvement over a frozen baseline, minus a declared node penalty, for a factor added through the same restrained probability model. For example, set penalty 0.001 per extra node before search and report predictive improvement and complexity separately. This coefficient is an illustrative development convention. It can suppress a genuinely small improvement; revise it only as a counted redesign, not after inspecting final confirmation.

Require computability and timing validity; stable declared orientation/behavior across development blocks; independent incremental support beyond the baseline; tolerable costs and risks; and an identifiable consuming role. Prespecify materiality and risk tolerances. If no candidate earns admission, retain the evidence and leave the library unchanged. This is an informative outcome of the search.

== Supply Honest Evaluations within a Work Budget

If one complete evaluation takes $c$ seconds and the work budget is $B$ seconds, serial completed evaluations cannot exceed roughly $B/c$. Reading $b$ bytes afresh for each of $M$ trials requires roughly $M b$ bytes. Cache common subexpressions, prune unused columns, and batch reusable operations before buying more processors.

A cache key must include input snapshot, universe, availability rules, expression/operators, target, and scoring version. After an exit-policy change, the earlier result still answers the old question. A versioned cache keeps that distinction visible. Errors, timeouts, and invalid trees must remain statuses rather than become favorable numerical scores.

Start with immutable source files, versioned derived columns, one deterministic scorer, and result writes separated from research inputs. Redundant disks improve availability; backups address loss and corruption; restoring and reconciling an actual replay establishes recoverability. None of these roles is automatically supplied by a database brand.

For neural training, distinguish model parameters, gradients, optimizer states, and activations. Replicated data-parallel workers generally retain a copy of model state while splitting example computation. Sharding distributes selected states but introduces communication and transient memory; total memory does not automatically become one worker's original footprint divided by worker count. Measured memory or throughput constraints can motivate these structures. The small factory described here can begin without a cluster.

#heading(level: 2, numbering: none)[Practical Default: One Honest Factory]

1. Freeze immutable data, the as-of view, label/exit policy, baseline, typed grammar, and evaluation budget.
2. Generate and score only on rolling development folds; purge relevant overlapping outcomes and fit transforms inside each fold.
3. Record every trial, status, orientation choice, penalty, and related redesign. Cache only version-compatible results.
4. Freeze a small shortlist and the complete consuming route before the reserved confirmation batch.
5. Admit only factors meeting the joint timing, evidence, increment, risk, and cost conditions; retain their dossiers.
6. Evaluate aggregation and holdings separately. Monitor input correctness, mature task performance, and realization. A decline triggers diagnosis of inputs, prediction, and realization before deciding whether the factor relation has decayed.

*Self-check:* Does a purged score remain final evidence after a generator queries it 10,000 times? Does a low-correlation factor necessarily diversify cash losses? Can a confirmation failure be erased by renaming the next run? No: each question concerns a different dependency or selection history.

== Practice Lesson: a Search Factory Needs an Execution Consumer

The institutional cost study by Frazzini, Israel, and Moskowitz uses live execution data to study how costs vary by trade size, stock characteristics, trade type, and time. Its value here is methodological: a factory's score must eventually reach a size- and policy-aware consumer. It does not supply a universal fee estimate for another fund, A-share venue, or crypto token.

For each shortlisted factor, retain its implied turnover, instrument liquidity, feasible order schedule, and candidate size ladder beside IC or forecast loss. Compare incremental value on the same dates after the same cost model. Record a fast signal that fails at realistic size in a rejected or restricted dossier, with the size and execution conditions responsible for that outcome. Conversely, do not reject every high-turnover idea by imposing someone else's unsupported flat cost. Estimate the cost appropriate to the chosen consumer and preserve its uncertainty.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Marcos López de Prado. #link("https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/finance-investments-special-topics-13fiz/advances-in-financial-machine-learning-978-1-119-48208-6")[_Advances in Financial Machine Learning_]. Wiley, 2018. Financial labels, sample overlap, and validation.
- David H. Bailey and Marcos López de Prado. #link("https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf")[_The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality_]. _The Journal of Portfolio Management_ 40(5), 94–107, 2014. Selection-adjusted Sharpe assessment; consult its exact conventions for implementation.
- Gareth James et al. #link("https://www.statlearning.com/")[_An Introduction to Statistical Learning_]. Second edition, Springer, 2021. Model selection and assessment background.
- Andrea Frazzini, Ronen Israel, and Tobias J. Moskowitz. #link("https://www.aqr.com/insights/research/working-paper/trading-costs")[_Trading Costs_]. Working paper, 2018. Size- and state-dependent costs studied using actual institutional executions.
]

#pagebreak()

= Online Aggregation: Allocate Trust with a Defined Loss and Memory
#counter(math.equation).update(0)

A confirmed library supplies candidates; allocating trust among them today adds a sequential decision. Factors can lose relative usefulness, disagree, or share the same mistake. The first consuming layer should combine comparable predictions with a weak, inspectable update rule. This starts with trust allocation among the existing judgments, keeping high-capacity interaction search as a separate research choice.

We select equal-weight probability mixtures as the control, cumulative exponential weighting as the first adaptive rule, and a uniform-share variant as a recorded drift comparison. The decisive guarantee concerns a loss and comparator under an explicit feedback clock. Profit, recovery after reversals, and selection effects are assessed separately from that loss-comparison guarantee.

== Why Not Follow Yesterday's Winner?

An *expert* is a factor-plus-rule producing an evaluable forecast of the same outcome. At round $t$, expert $i$ proposes a prediction before the outcome is known. Afterward it receives loss $ell_(t,i)$. An allocator chooses nonnegative trust weights summing to one. To compare an online route with a fixed expert, define *regret*:

$
  "Regret"_(T)=sum_(t=1)^(T) hat(ell)_(t)-min_(i) sum_(t=1)^(T) ell_(t,i).
$

Here $hat(ell)_(t)$ is the allocator loss under a specified interpretation. The comparator is the best single expert over the entire completed interval, selected in hindsight. It is neither the best expert at each date nor a known profitable strategy.

Follow-the-leader chooses the expert with minimum loss so far. Consider two experts, deterministic tie-breaking toward A, and alternating loss vectors $(1,0),(0,1),(1,0),(0,1),...$. Initially choose A and lose one. Then B leads, choose B, and lose one. At the next tie choose A again. The allocator loses on every round; for even $T$, each fixed expert loses $T/2$. Regret is $T/2$. Accurately identifying the historical leader still leaves the allocation exposed to a fragile advantage. Softening concentration addresses that failure mechanism.

A periodic batch model can adapt when retrained, and a simple constant mixture can be robust. The positive reason to begin with exponential trust updates is an explicit low-complexity way to trade historical performance against dispersion. Whether its adaptation improves actual strategy value remains a matched comparison.

== Derive Soft Trust from Regularized Selection

Let $L_(t-1,i)=sum_(s<t)ell_(s,i)$. For $K>=2$ experts, choose weights minimizing

$
  sum_(i) w_(i) L_(t-1,i)+frac(1,eta)sum_(i) w_(i) ln w_(i),
  quad w_(i)>=0, quad sum_(i) w_(i)=1,
$

with $eta>0$ and $0 ln 0$ interpreted by its zero limit. The second term is negative entropy. Equal weights make it more negative than concentration on one expert, so it penalizes premature certainty relative to the cumulative-loss advantage.

Use multiplier $a$ for the sum constraint. An interior stationary weight satisfies $L_(i)+(ln w_(i)+1)/eta+a=0$. Solve for $w_(i)$ and normalize:

$
  w_(t,i)=frac(exp(-eta L_(t-1,i)),sum_(j) exp(-eta L_(t-1,j))).
$

Finite losses give positive weights. The objective's diagonal second derivatives $1/(eta w_(i))>0$ make this stationary solution the unique minimum. This construction is called exponential weighting or *Hedge*. Maintain unnormalized weights $v_(1,i)=1$ and update

$
  v_(t+1,i)=v_(t,i)exp(-eta ell_(t,i)).
$

A cumulative loss disadvantage $d$ changes relative trust by $exp(-eta d)$. Thus larger $eta$ reacts more sharply to loss differences; smaller $eta$ spreads trust. Multiply losses by $c>0$ and divide $eta$ by $c$ to get exactly the same weights. Its meaning therefore depends on both the loss scale and the comparison horizon.

== Prove the Static-Regret Trade-Off

Assume all expert losses are revealed after each round, lie in $[0,1]$, and weights are chosen before that round's outcome. Define the weighted expert loss $hat(ell)_(t)=sum_(i) w_(t,i)ell_(t,i)$. No IID market assumption is needed for this sequence-by-sequence proof.

The bounded exponential-moment argument of Chapter 6 applies to a random expert index drawn with probabilities $w_(t)$. Its centered loss lies in an interval of length one. Therefore

$
  ln sum_(i) w_(t,i)exp(-eta ell_(t,i))
    <=-eta hat(ell)_(t)+eta^(2)/8.
$

This randomization is over expert indices for the calculation, not a claim that market dates are independent. Set $W_(t)=sum_(i) v_(t,i)$. The left side equals $ln W_(t+1)-ln W_(t)$. Sum over $T$ rounds, using $W_(1)=K$:

$
  ln W_(T+1)<=ln K-eta sum_(t) hat(ell)_(t)+eta^(2) T/8.
$

The total includes the final weight of the best fixed expert $i^(*)$, so $ln W_(T+1)>=-eta sum_(t) ell_(t,i^(*))$. Combine and divide by $eta$:

More explicitly, $-eta L_(T,i^(*))<=ln K-eta sum_(t)hat(ell)_(t)+eta^(2)T/8$. Moving both loss terms to the same side gives $eta(sum_(t)hat(ell)_(t)-L_(T,i^(*)))<=ln K+eta^(2)T/8$. Dividing a positive $eta$ leaves the regret inequality without reversing its sign. Its optimum follows from $-ln K/eta^(2)+T/8=0$; the two positive terms then equal one another.

$
  "Regret"_(T)<=frac(ln K,eta)+frac(eta T,8).
$

The first term is the cost of initially not knowing the winner. The second is the cost of aggressive updating. Differentiating the bound with respect to $eta$ balances them at

$
  eta=sqrt(frac(8 ln K,T)), quad
  "Regret"_(T)<=sqrt(frac(T ln K,2)).
$

Average regret decreases as $sqrt(ln K/(2T))$. For $K=20,T=252$, the rate is about 0.308 and the worst-case average bound about 0.077. The comparison is measured in these loss units; translating it into daily returns requires the participation, payoff, and sizing rules. For one expert, there is no selection and regret is zero. If the horizon is unknown, a declared doubling/restart or adaptive scheme needs its own accounting; changing $eta$ daily does not automatically preserve this fixed-rate proof.

The logarithm of candidate count also appeared in Chapter 8's search penalty. Both reflect uncertainty over choices, but the two results have different objects and assumptions: one addresses statistical selection on data, the other addresses sequential mixture loss against a fixed expert. Each theorem answers its own comparison question.

== Make the Mixture's Actual Forecast Match the Loss

=== A probability mixture has a useful convex bridge

Suppose every expert forecasts the same binary outcome $B_(t)$, with orientation-aligned probability $p_(t,i) in [0,1]$. Form $p_(t)=sum_(i) w_(t,i)p_(t,i)$. Use Brier loss $ell_(t,i)=(p_(t,i)-B_(t))^(2)$, bounded by one.

For true conditional success probability $p^(*)$, expand conditional expected Brier loss:

$
  E[(p-B)^(2) mid(|) F]=(p-p^(*))^(2)+p^(*) (1-p^(*)).
$

It is minimized at the true probability. It shares that ideal probability consumer with class log loss but supplies a bounded loss convenient for the expert theorem. Its arithmetic also links the weighted expert loss to the actual probability forecast:

Let $p=sum_(i)w_(i)p_(i)$. Expanding the weighted square gives $sum_(i)w_(i)p_(i)^(2)-2B p+B^(2)$; expanding the mixture square gives $p^(2)-2B p+B^(2)$. Their difference is $sum_(i)w_(i)p_(i)^(2)-p^(2)=sum_(i)w_(i)(p_(i)-p)^(2)$, because weighted deviations sum to zero. Separately, $B^(2)=B$ for a binary outcome, so expected Brier loss is $p^(2)-2p p^(*)+p^(*)=(p-p^(*))^(2)+p^(*)[1-p^(*)]$. The first identity supplies the regret bridge; the second supplies the probability interpretation.

$
  sum_(i) w_(i) (p_(i)-B)^(2)-(sum_(i) w_(i) p_(i)-B)^(2)
    =sum_(i) w_(i) (p_(i)-p)^(2)>=0.
$

Consequently the probability mixture's cumulative Brier loss is no greater than the weighted expert loss used in the proof. The same upper regret comparison holds for its actual Brier forecast. For three-class probabilities, use $ell=(1/2)sum_(k) (p_(k)-bold(1)[Y=k])^(2)$; its range is also $[0,1]$, its ideal forecast is the class distribution, and the same convexity argument applies. Combine probabilities that forecast the same event. A direction probability and success conditional on a different primary trade call for separate outcome definitions.

Thresholding a combined score into its sign breaks this bridge for zero–one directional loss. A deterministic sign error need not equal the weighted experts' sign errors. Likewise Brier accuracy does not price asymmetric gains, losses, or costs. Apply Chapter 2 or 3's payoff-derived participation rule to the mixed probability, then control size separately.

=== Feedback time is part of the algorithm

For an unfinished ten-session trade, today's update waits for the required outcome to become available, even when a retrospective file already contains its exit. Save expert predictions and their version at decision time; score them only when the required outcome is available. All experts must be scored against that same outcome, not whichever horizon suits each winner.

The preceding proof uses immediate full-feedback rounds. Delayed overlapping trades may require a delayed-feedback algorithm and a delay-dependent bound. As a first theorem-matched teaching stream, issue the next candidate only after the previous selected policy outcome has matured. Market losses can remain dependent—the algebra never required IID outcomes—but feedback now has the required order. A daily production stream can instead retain a maturity queue and measure lag; it must not claim the immediate theorem simply by naming queue completions rounds while forecasts were issued with stale weights.

Partial expert feedback also changes the problem. If an expert forecasts an outcome that becomes unobservable after the allocator abstains, full information is unavailable. Market-observed outcomes may still be scorable for all experts, but actual hypothetical fills and payoffs require an admitted replay. Define what was genuinely observed before updating trust.

== Choose Memory for the Adaptation Task

Suppose A has accumulated $m$ fewer losses than B. Their odds are $exp(eta m)$. After reversal, if B gains one loss unit per round, it takes $m$ rounds to erase the gap. Raising $eta$ makes concentration stronger but does not shorten that symmetric catch-up count. Nonzero mathematical weights can remain practically negligible.

To keep a recovery floor, first take the normalized exponential update $overline(w)_(t+1)$ and then mix with uniform trust:

$
  w_(t+1,i)=(1-gamma)overline(w)_(t+1,i)+frac(gamma,K),
  quad 0<gamma<1.
$

Each expert retains at least $gamma/K$. With $gamma=0.02$, two percent of trust is continuously shared uniformly. This *fixed-share* style update pays for potential revival by continuing to allocate some mass to weak experts. Discounting older loss or restarting are different designs. Their memory scales and comparators need to be stated.

Cumulative Hedge compares with one best fixed expert. Tracking a switching expert sequence requires paying for switches and a corresponding guarantee. The shared update above supplies a concrete drift comparison whose tracking guarantee is evaluated separately from the cumulative proof. Measure adaptation, forecast quality, and implementation turnover against equal weights and pure cumulative Hedge on the same development sequence. Loss-scale, sharing-rate, library, and restart selection all belong to Chapter 8's trial history.

#principle[*Adaptation conclusion:* Use cumulative Hedge for the static comparator it actually controls. Use a floor, restart, or discount deliberately when recovery after change is the task. Recovery speed depends on the memory rule and loss trajectory, beyond whether weights remain nonzero.]

== Continuous Weights: Geometry Can Replace Expert Entropy

=== Projected gradient descent supplies a different bound

Let $cal(W)$ be a closed convex feasible set of diameter at most $D$, convex losses $ell_(t) (w)$, and gradients $g_(t)$ with norm at most $G$. Choose $w_(t+1)=Pi_(cal(W)) (w_(t)-eta g_(t))$, where $Pi$ is the closest feasible point.

For proposed point $z$ and its projection $v$, minimizing squared distance along feasible directions gives $(z-v)^(T) (u-v)<=0$ for any feasible $u$.

To see the minimization step explicitly, $v+s(u-v)$ remains feasible for $0<=s<=1$ by convexity. The right derivative at zero of $||z-v-s(u-v)||^(2)$ must be nonnegative at its minimum: $-2(z-v)^(T)(u-v)>=0$. Now expand

$
 ||z-u||^(2)=||z-v||^(2)+||v-u||^(2)
 +2(z-v)^(T)(v-u)>=||v-u||^(2).
$

The cross term is nonnegative by the projection inequality. Next $||w_(t)-eta g_(t)-u||^(2)=||w_(t)-u||^(2)-2eta g_(t)^(T)(w_(t)-u)+eta^(2)||g_(t)||^(2)$. Substituting the projection bound and rearranging yields the one-round inequality below. Summing cancels intermediate squared distances, leaving the initial distance at most $D^(2)$ and a nonpositive final-distance term that can be dropped. Expanding squared distances then implies $norm(v-u)^(2)<=norm(z-u)^(2)$. Apply this to $z=w_(t)-eta g_(t)$:

$
  2eta g_(t)^(T) (w_(t)-u)
    <=norm(w_(t)-u)^(2)-norm(w_(t+1)-u)^(2)+eta^(2) norm(g_(t))^(2).
$

Convexity supplies $ell_(t) (w_(t))-ell_(t) (u)<=g_(t)^(T) (w_(t)-u)$. Sum, telescope distances, and bound gradients:

$
  sum_(t) [ell_(t) (w_(t))-ell_(t) (u)]<=frac(D^(2),2eta)+frac(eta G^(2) T,2).
$

Choosing $eta=D/(G sqrt(T))$ gives $D G sqrt(T)$. This is online gradient descent (OGD). Its trade-off concerns Euclidean geometry, not the entropy geometry of expert weights. Projection enforces feasibility; it does not make the loss convex if the original score-to-trade mapping was nonconvex.

=== Stronger loss curvature permits stronger algorithms

A loss is $a$-*exp-concave* on a domain when $exp(-a ell)$ is concave there. Twice differentiating in one dimension gives $ell''>=a(ell')^(2)$.

In detail, the second derivative of $h(p)=exp(-a ell(p))$ is $h''(p)=a exp(-a ell(p))[a(ell'(p))^(2)-ell''(p)]$. Concavity requires this to be nonpositive. Since $a exp(-a ell)>0$, the required inequality is precisely the displayed curvature condition. This does not assert concavity of the loss itself under an arbitrary score-to-trade transformation. For squared probability loss on $p in [0,1]$, $ell''=2$ and $(ell')^(2)<=4$, so $a<=1/2$ suffices on this bounded domain. The domain is part of the statement.

Online Newton step (ONS) accumulates gradient outer products, for example $A_(t)=A_(0)+sum_(s<=t)g_(s) g_(s)^(T)$, and uses their inverse to adjust movement with a matching projection geometry. With exp-concavity, bounded feasible domain/gradients, and the theorem's regularization and step conditions, suitable ONS algorithms have logarithmic static regret. The cited result supplies this stronger guarantee; the present derivation establishes the OGD bound. Calling a loss squared does not establish these conditions for an unbounded trading problem. OGD, ONS, and adaptive expert algorithms address sequential decisions using distinct geometries and update rules.

#heading(level: 2, numbering: none)[Practical Default: Stable Probability Trust]

Use comparable confirmed probabilities, equal weights as the control, and bounded Brier loss. For known $K,T$, initialize cumulative Hedge with $eta=sqrt(8 ln K/T)$ in these units. Keep log weights $a_(i)$: subtract $eta ell_(i)$ on mature feedback, subtract their maximum before exponentiating, and normalize. Subtracting a common maximum changes no probability and avoids needless numerical underflow/overflow. A frozen availability rule handles missing forecasts consistently, preserving the intended expert comparison.

Compare equal weights, cumulative Hedge, and uniform-share Hedge with illustrative share 0.02. Fix update timing and account for delayed labels. Apply the same economic no-trade band and risk-sizing policy across comparisons; trust updates need not mandate immediate portfolio rebalancing. A separately confirmed increment can justify adding interactions or batch retraining to this starting layer.

*Self-check:* Can all experts lose money while the allocator has low regret? Yes. Can a sign-thresholded forecast automatically inherit the mixture Brier proof? No. Does doubling $eta$ necessarily halve the time needed to overcome a symmetric cumulative loss reversal? No. Each answer identifies the particular loss, operation, or memory in the theorem.

== Manager Experience: Diagnose the Mechanism behind Losses

In his 2017 retrospective on the August 2007 quant crisis, Cliff Asness describes a liquidity-driven unwind and emphasizes that a temporary shock can still destroy a strategy that cannot survive it. This is a manager's causal interpretation of an episode, not a guarantee that future factor losses will reverse.

The practical distinction is between deteriorating prediction, common crowded positions, and forced reduction of otherwise unchanged exposures. Compare factor forecast losses, holdings overlap, spreads/depth, realized costs, and available funding. A stable forecast loss with exploding execution cost calls for reduced participation or size; it is not repaired by Hedge redistributing trust among similarly exposed experts. A genuine forecast deterioration calls for the evidence and retirement process instead. Recent return rankings also reflect holdings and realization, so compare experts on the intended prediction relation itself.

Preserve the cumulative Hedge control, but test fixed-share memory on the same defined predictive loss. Measure crowding/exposure and cash constraints in the holding layer. No regret theorem over bounded expert losses supplies immunity to a simultaneous liquidity unwind.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Yoav Freund and Robert E. Schapire. #link("https://doi.org/10.1006/jcss.1997.1504")[_A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting_]. _Journal of Computer and System Sciences_ 55(1), 119–139, 1997. Expert-mixture comparison.
- Martin Zinkevich. #link("https://www.cs.cmu.edu/~maz/publications/techconvex.pdf")[_Online Convex Programming and Generalized Infinitesimal Gradient Ascent_]. ICML, 2003. Online projected-gradient methods.
- Elad Hazan, Amit Agarwal, and Satyen Kale. #link("https://doi.org/10.1007/s10994-007-5016-8")[_Logarithmic Regret Algorithms for Online Convex Optimization_]. _Machine Learning_ 69, 169–192, 2007. Conditions for stronger online curvature-based guarantees.
- Cliff Asness. #link("https://www.aqr.com/Insights/Perspectives/The-August-of-our-Discontent-Once-More-Unto-the-Breach")[_The August of Our Discontent: Once More Unto the Breach?_]. AQR, 7 August 2017. Manager retrospective; its interpretation is not a promise of future reversals.
]

#pagebreak()

= Portfolios and Sizing: Optimize Less Where No Edge Is Supported
#counter(math.equation).update(0)

Turning a probability, rank, or economic score into holdings introduces a new decision. Positions add common exposures, capital, costs, and the possibility of an adverse path. We now choose what to optimize from the estimates we can actually support. Timing begins with a participation decision and inverse-volatility risk size. Cross-sectional selection begins with constrained active weights. When a mean-return edge remains unconfirmed, multi-asset allocation begins with risk budgets and reserves expected-return forecasts for separately supported uses.

These starting designs match the estimates we can support. A perfectly solved optimization can amplify uncertainty in its inputs, so deciding which estimates deserve a role comes before numerical refinement.

== Derive the Portfolio Quantities before Calling a Solver

For an asset return vector $r$, mean $mu=E r$, covariance $Sigma=E[(r-mu)(r-mu)^(T)]$, and fixed weights $w$, linearity gives portfolio mean $w^(T) mu$. For clarity, the centered portfolio return is $w^(T)(r-mu)=sum_(i)w_(i)(r_(i)-mu_(i))$. Its squared expectation is $sum_(i)sum_(j)w_(i)w_(j)E[(r_(i)-mu_(i))(r_(j)-mu_(j))]$. The expectation in each term is precisely $Sigma_(i,j)$, so expanding the square gives

$
  Var(w^(T) r)=w^(T) Sigma w.
$

Returns must cover compatible periods and units. Futures return exposure requires the notional-to-equity convention described below, not a stocklike cash purchase of contract price. Estimated covariance describes variation under its data window and construction; it does not enumerate every future stress.

One mean–variance question minimizes $w^(T) Sigma w$ subject to budget and a target mean $w^(T) mu>=m$. Varying $m$ traces the attainable mean/risk boundary, commonly called an efficient frontier. Constraints determine which portfolios are attainable. A numerical quadratic-program solution minimizes the stated quadratic objective over those constraints; it does not certify that estimated means, risks, or fills are true.

A rank score specifies relative preference. It can serve as a stated surrogate utility in an optimization, or be calibrated into a return estimate with separately supported magnitude. Calling an arbitrary rank $mu$ silently assigns cash meaning it did not acquire in the prediction task.

== Optimality Can Magnify Estimation Error

Consider a budget-free teaching objective $w^(T) mu-lambda w^(T) Sigma w/2$, with $lambda>0$ and positive-definite $Sigma$. For symmetric $Sigma$, differentiating the quadratic term gives $lambda Sigma w$: the two appearances of $w$ each supply one half. The first-order equation is $mu-lambda Sigma w=0$; positive definiteness makes the objective strictly concave, so its stationary point is the unique maximum. Differentiation gives

$
  w^(*)=frac(1,lambda)Sigma^(-1)mu.
$

Perturb its equation $lambda Sigma w=mu$. Write the perturbed equation as $lambda(Sigma+delta Sigma)(w^(*)+delta w)=mu+delta mu$. Subtract $lambda Sigma w^(*)=mu$, leaving $lambda Sigma delta w+lambda(delta Sigma)w^(*)+lambda(delta Sigma)delta w=delta mu$. The last product is second order. Ignore products of small perturbations and multiply by $Sigma^(-1)/lambda$ to obtain

$
  delta w approx frac(1,lambda)Sigma^(-1)delta mu-Sigma^(-1) (delta Sigma)w^(*).
$

This shows both mean and covariance errors. Along a covariance eigendirection with eigenvalue $s$, the mean-error component is divided by $lambda s$. A small estimated-risk direction can attract an enormous holding from a tiny spurious mean. If $lambda=1$, estimated mean 0.001 and variance 0.000001 imply exposure 1000 in that scalar problem. The optimizer is following its inputs faithfully; the extreme result originates in the estimates supplied to it.

For $N>1$ compatible past return rows, center them by their sample average $overline(r)$ and form $hat(Sigma)=(N-1)^(-1)sum_(t) (r_(t)-overline(r))(r_(t)-overline(r))^(T)$. For any vector $v$, its quadratic form is an average of squared projections and is therefore nonnegative. Missing-data pairwise estimates do not automatically retain that property; use a coherent admitted estimator rather than assume any assembled matrix is a covariance. A simple covariance shrinkage construction is $hat(Sigma)_(gamma)=(1-gamma)hat(Sigma)+gamma tau I$, where $0<gamma<=1$ and $tau>0$ has variance units. Every eigenvalue becomes $(1-gamma)s_(j)+gamma tau$, so it is at least $gamma tau$ for a nonnegative sample covariance. The floor limits inverse amplification. The isotropic target can also be wrong about actual relative risk; stabilization limits amplification while introducing bias, leaving uncertainty about the true risk structure.

Leverage, per-name, exposure, and turnover constraints restrict responses to uncertain inputs. Selecting these constraints before inspecting results gives them a stable role in the comparison. Risk-only allocation removes unreliable mean estimates, but still estimates covariance and can fail when that estimate or the asset coverage fails.

#principle[*Optimization principle:* Establish which inputs are trusted, then constrain the responses they can justify. A more accurate numerical solution to an unstable statistical problem can be a more extreme mistake. Stabilization and constraints are substantive model choices.]

== Equal Capital Is Not Equal Risk

=== Decompose volatility into contributions

For $sigma_(p)=sqrt(w^(T) Sigma w)>0$, differentiation gives $frac(partial sigma_(p),partial w_(i))=frac((Sigma w)_(i),sigma_(p))$. Define the volatility risk contribution

$
  "RC"_(i)=frac(w_(i) (Sigma w)_(i),sigma_(p)), quad
  sum_(i) "RC"_(i)=sigma_(p).
$

To obtain the derivative, first differentiate $w^(T) Sigma w$: its $i$th derivative is $2(Sigma w)_(i)$ because covariance is symmetric. The derivative of the square root contributes $1/(2sigma_(p))$. Multiplying the marginal volatility by the holding gives the displayed contribution. The sum follows by replacing the numerator sum with $w^(T) Sigma w$. A relative contribution is $"RC"_(i)/sigma_(p)=w_(i)(Sigma w)_(i)/(w^(T)Sigma w)$, so it is the fraction of estimated volatility attributed by this derivative decomposition. This is a decomposition of current estimated volatility, not of expected returns or every tail loss. Some contributions can be negative in hedged portfolios. A chosen positive-budget long-only construction below deliberately seeks positive contributions.

For independent assets with volatilities 10% and 20%, equal capital gives squared-risk terms 0.0025 and 0.01. The risk proportions are one fifth and four fifths, not one half each. Capital equality answers a funding allocation question; it does not answer a volatility allocation question.

=== Construct equal risk budgeting as a convex problem

Choose positive risk budgets $b_(i)$ and positive-definite covariance $Sigma$. Introduce positive auxiliary holdings $x_(i)$ and minimize

$
  F(x)=frac(1,2)x^(T) Sigma x-sum_(i) b_(i) ln x_(i), quad x_(i)>0.
$

The quadratic term restrains risk; the logarithmic term prevents positive-budget components disappearing. Its gradient is $(Sigma x)_(i)-b_(i)/x_(i)$ and Hessian is $Sigma+diag(b_(i)/x_(i)^(2))$, positive definite. Thus it is strictly convex. As any coordinate tends to zero with the others bounded, the log term diverges upward; as norm grows, positive-definite quadratic growth dominates logarithms. More explicitly, for some smallest eigenvalue $s_("min")>0$, the quadratic term is at least $s_("min")norm(x)^(2)/2$. Quadratic growth dominates every logarithm as the norm grows. Thus a sublevel set cannot escape to infinity; on a bounded sublevel set no positive coordinate can approach zero because its negative-log term diverges. A minimum is attained in the remaining compact interior region. These boundary properties ensure an interior minimizer, and strict convexity makes it unique.

At the minimizer,

$
  x_(i) (Sigma x)_(i)=b_(i).
$

Normalize $w=frac(x,sum_(j) x_(j))$. Put $c=sum_(j)x_(j)>0$. Then $(Sigma w)_(i)=(Sigma x)_(i)/c$, so $w_(i)(Sigma w)_(i)=b_(i)/c^(2)$. Summing the budget equations also gives $x^(T)Sigma x=sum_(j)b_(j)$, hence $sigma_(p)^(2)=sum_(j)b_(j)/c^(2)$. Dividing the first identity by the second cancels the common normalization. Therefore volatility-contribution proportions are

$
  frac("RC"_(i),sigma_(p))=frac(b_(i),sum_(j) b_(j)).
$

Equal budgets produce equal risk contribution (ERC). This construction uses covariance and risk budgets alone. Omitting an unsupported mean estimate reduces the estimation burden; comparative future-return performance remains an empirical question.

A concrete coordinate solver freezes other $x_(j)$, writes $c_(i)=sum_(j != i)Sigma_(i,j)x_(j)$, and solves $Sigma_(i,i)x_(i)^(2)+c_(i) x_(i)-b_(i)=0$. The positive root is

$
  x_(i)^(+)=frac(-c_(i)+sqrt(c_(i)^(2)+4Sigma_(i,i)b_(i)),2Sigma_(i,i)).
$

It is the exact minimum along that positive coordinate, so each update does not increase $F$ in exact arithmetic. Cycle coordinates and stop only when relative objective movement and budget residuals are small, subject to an iteration cap. For $c_(i)>=0$, the algebraically equivalent root $2b_(i)/(c_(i)+sqrt(c_(i)^(2)+4Sigma_(i,i)b_(i)))$ avoids subtracting nearly equal positive values; for $c_(i)<0$, the displayed numerator adds positive magnitudes. Check finite values and residuals. A damped Newton solver with positive iterates and backtracking is another valid route. An alternative update on risk-contribution errors needs its own objective and convergence checks; a small learning rate addresses the size of movement.

=== Distinguish the competing “risk-only” rules

With diagonal covariance $Sigma_(i,i)=sigma_(i)^(2)$, the budget equations give $x_(i)=sqrt(b_(i))/sigma_(i)$. Equal budgets therefore yield $w_(i)$ proportional to inverse volatility. Budget-constrained minimum variance instead differentiates $sum_(i) sigma_(i)^(2) w_(i)^(2)$ with $sum_(i) w_(i)=1$, giving $w_(i)$ proportional to $1/sigma_(i)^(2)$. For the 10%/20% pair, these rules give $(2/3,1/3)$ and $(4/5,1/5)$ respectively. Equal capital gives $(1/2,1/2)$. Their different objectives explain the different allocations.

Maximum diversification compares weighted individual volatility with portfolio volatility and still uses estimated correlation. Hierarchical allocation groups similar assets and divides risk recursively rather than invert one global covariance. To understand a local split, suppose standardized left/right group portfolios have variances $v_(L),v_(R)$ and temporarily ignore their covariance. A left fraction $a$ gives $a^(2) v_(L)+(1-a)^(2) v_(R)$, minimized at $a=v_(R)/(v_(L)+v_(R))$. Including covariance $c$ changes the solution to $(v_(R)-c)/(v_(L)+v_(R)-2c)$ before feasibility constraints.

This calculation motivates recursive risk allocation and exposes what was omitted. A correlation tree, its distance/linkage convention, and ignored between-group covariance are extra estimated structure. Hierarchical risk parity (HRP) can be a useful comparison, but avoiding a global inverse is not a proof of global minimum variance or ERC. Our first multi-asset route remains the explicit positive-budget construction with checked residuals.

== Remove Unwanted Bets at the Holding Level

For cross-sectional index enhancement, write benchmark weights $w^(b)$ and active weights $a=w-w^(b)$. If both are fully invested, $bold(1)^(T) a=0$. Let columns of $B$ describe exposures the active strategy does not intend to forecast. Impose $B^(T) a=0$ or prespecified bounded deviations. Feature residualization from Chapter 5 does not guarantee these holding constraints: a nonlinear signal map, risk optimizer, or unequal position sizes can restore exposure.

Use the following first objective for standardized rank scores $s$:

$
  min_(a) -s^(T) a+frac(lambda,2)a^(T) hat(Sigma)a
            +kappa sum_(i) |a_(i)-a_(i)^(-)|.
$

Here $a^(-)$ is the declared pre-rebalance active holding vector, not yesterday's target copied without drift. The score is a surrogate preference unless calibrated. Positive-semidefinite covariance and $lambda,kappa>=0$ make the objective convex. The linear term favors preferred assets, the quadratic term prices common active risk, and the absolute-change term prices trading.

Add budget, exposure, active/name bounds, feasible total holdings $w^(b)+a>=0$ for a long-only account, and a turnover budget. To implement the absolute term, introduce $z_(i)>=a_(i)-a_(i)^(-)$ and $z_(i)>=-(a_(i)-a_(i)^(-))$, then use $kappa sum_(i) z_(i)$ and, when required, $sum_(i) z_(i)<=T_("trade")$. This gives a quadratic program with linear constraints. Define cost per unit of *one-way* weight traded; calling half the L1 sum turnover is another convention and requires matching coefficients.

Before solving, test a known feasible holding such as the benchmark under the actual bounds. Suspensions, restricted sales, cash flows, and current inventory can make a nominal benchmark infeasible; report that condition rather than silently relax constraints. After solving, check budget/exposure/bound residuals, predicted and realized turnover, and a no-change baseline. Score rescaling $s$ by $c>0$ requires rescaling $lambda,kappa$ by $c$ to preserve this same optimization. A common score offset cancels because active weights sum to zero.

For a practical risk-coefficient rule, first fix an active variance cap $v_(a)^(2)$ in the policy. With the score/trading term and feasible set fixed, let $a_(1),a_(2)$ minimize objectives at $lambda_(1)<lambda_(2)$, and write $R_(j)=a_(j)^(T) hat(Sigma)a_(j)$. Define the common non-risk objective $G(a)=-s^(T)a+kappa sum_(i)|a_(i)-a_(i)^(-)|$. Optimality at the two coefficients means

$ G(a_(1))+frac(lambda_(1),2)R_(1)<=G(a_(2))+frac(lambda_(1),2)R_(2), \ G(a_(2))+frac(lambda_(2),2)R_(2)<=G(a_(1))+frac(lambda_(2),2)R_(1). $

Add these inequalities. The two $G$ terms cancel; after multiplication by two and collecting terms, $(lambda_(2)-lambda_(1))(R_(2)-R_(1))<=0$. Thus estimated risk does not increase with the coefficient for exact solutions. Start a positive trial coefficient, double it until the risk cap is met or a declared numerical cap is reached, then bisect the bracket to the declared risk tolerance. This selects a coefficient from the risk policy rather than whichever backtest looks best. If minimum feasible risk still exceeds the cap, report infeasibility. Fix or separately develop the utility-to-trading penalty conversion; an uncalibrated rank unit is not a currency cost.

=== Structural coverage before macro forecasting

For multi-asset allocation, suppose returns admit an explanatory linear shock map $r=A z+epsilon$, where $z$ contains selected growth and inflation shocks. Portfolio shock exposure is $A^(T) w$. This identifies the additional question behind an all-weather design: do the chosen assets actually cover the shocks, at the sizes and funding conditions used?

ERC across four assets does not automatically equalize four macro-scenario risks. The asset–shock map needs economic and stress support; quadrants do not exhaust default, liquidity, policy, or funding risks. Without an independently supported forecast of the next quadrant, choose verified structural coverage and restrained risk budgets as the base. Confirmed trend tilts may be bounded supplements, not permission to dismantle the base at every confident macro narrative.

#principle[*Selected allocation conclusion:* For unsupported mean or macro forecasts, retreat to verified structure and risk budgets rather than optimize invented precision. Keep equal capital as a control, stabilized ERC as the first risk base, and expected-return or trend tilts as separately confirmed increments.]


=== All Weather as a Complete Allocation Example

We can now turn structural coverage into an allocation experiment, keeping asset ERC and environmental balance distinct. Bridgewater's account describes three building blocks: separate cash, beta, and alpha; correct the risk concentration of capital-weighted portfolios; and balance sensitivity to growth and inflation surprises. Its early pension work paired growth-sensitive equities with appropriately risk-scaled bonds, and later added inflation-linked bonds to fill an inflation exposure gap. The firm offers these as retrospective explanations of its practice, with realized risks and losses still part of the allocation problem.

The income source matters: the strategy primarily diversifies exposure to market risk premia. Its economic rationale comes from bearing compensated risks and combining exposures. A risk premium is compensation expected for bearing a risk, not a certain next-period payment. Long-run positive premia and implementable diversification are economic inputs requiring evidence. Separate optional active alpha from that beta base rather than silently turning the base into a macro timing strategy.

==== Derive the environmental distinction in a small model

Reuse $r=A z+epsilon$ and suppose for the moment that the components of $z$ are uncorrelated, with variances $d_(k)$. A holding vector $w$ has exposure $g=A^(T) w$, so the explanatory shock component of portfolio variance is

$
  Var(w^(T) A z)=sum_(k) d_(k) g_(k)^(2).
$

This follows by expanding the variance and removing cross terms under the stated uncorrelated-shock assumption. The residual contributes its own variance and any covariance with the shock component, which the complete risk estimate also includes. Under correlated shocks, use $g^(T) Cov(z)g$ instead of assigning independent squared terms. Scenario losses and Euler asset contributions are different objects again. Equalizing one does not equalize the others.

For a diagnostic example, take two assets with $r_(1)=z+epsilon_(1)$ and $r_(2)=z+epsilon_(2)$, where the three variables are independent with variance one. Then asset variances are two and covariance is one. Symmetry gives equal-weight ERC, yet the unit-budget portfolio remains fully exposed to $z$: $0.5r_(1)+0.5r_(2)=z+0.5epsilon_(1)+0.5epsilon_(2)$. Its variance is 1.5, of which one comes from the common shock. Two equal risk contributions have not created two independent economic environments.

Now change the second asset to $r_(2)=-z+epsilon_(2)$. The same equal weights cancel the common shock and leave variance 0.5. The opposite exposure sign supplies the structural hedge; adding another ticker with the same sign would retain the common shock. Actual assets have changing and imperfect sensitivities, and no such example proves their coefficients stable. The example identifies the sensitivity evidence needed to use ERC as a macro allocation proxy.

==== Growth and inflation are exposures, not exclusive asset bins

The following table is an explanatory starting map, not a promise about every realized return. “Above/below expectation” refers to a surprise relative to what was priced, not simply positive/negative GDP growth or a high/low inflation level.

#table(
  columns: (1.1fr, 1.8fr),
  table.header([Environment question], [Exposure to investigate]),
  [Growth exceeds expectations], [Equities and economically sensitive exposures may benefit; also inspect valuation, financing, and inflation.],
  [Growth disappoints], [High-quality nominal duration may offset some contraction shocks; check credit and inflation co-moves.],
  [Inflation exceeds expectations], [Commodity and inflation-linked exposures address a gap in nominal purchasing-power protection; real-rate moves still matter.],
  [Inflation falls below expectations], [Nominal duration may benefit; do not assume that every equity or gold position is an exact opposite.],
)

These are four directional environment sensitivities, not four disjoint buckets with one ETF each. Joint growth/inflation quadrants are another useful organization, but one asset can span several. Gold is not a uniquely identified “inflation-down quadrant,” nor is a commodity token automatically a direct inflation hedge. In particular, an inflation-linked cash-flow adjustment does not remove real-rate price risk. In a one-payment teaching bond with positive real payment $D$ at horizon $h>0$ and real discount yield $y>-1$, present value is $P=frac(D,(1+y)^h)$. Differentiating gives $frac(dif P,dif y)=-frac(h D,(1+y)^(h+1))<0$. A higher real discount rate reduces its real price even though the nominal payment adjusts for inflation. Duration summarizes such local yield sensitivity; it is not a promise that a named bond always offsets an equity decline.

==== A reproducible simplified baseline

Construct a teaching universe from historical instruments representing broad equities, high-quality nominal government duration, inflation-linked government bonds, and diversified commodities. Gold can be a separately justified fifth comparison. Verify currency, total-return treatment, duration, tradability, and financing; these descriptions are not product recommendations or a claim to replicate Bridgewater's holdings. A futures-backed or tokenized wrapper needs its additional roll, issuer, reference, and funding ledger.

Use 252 completed sessions to estimate covariance, regularize it as above, and solve positive-budget ERC with equal budgets as the *first asset-risk baseline*. Keep equal capital and inverse volatility as controls. Rebalance monthly with later feasible fills, transaction costs, liquidity, concentration, and cash limits. Require budget residuals and estimated covariance validity before accepting a numerical solution. This modest experiment evaluates asset-risk allocation; the firm's proprietary environmental allocation has a different scope.

Multiplying covariance by a positive annualization constant does not change normalized ERC weights. Indeed, if the old solution is $x$, define $y=x/sqrt(c)$ for the new covariance $c Sigma$. Then $y_(i)(c Sigma y)_(i)=(x_(i)/sqrt(c))(sqrt(c)(Sigma x)_(i))=b_(i)$. This distinction between the old vector $x$ and the new vector $y$ is necessary. Normalization removes the common $1/sqrt(c)$ scale. Annualization changes the volatility unit, not the economic exposures.

After solving, inspect both risk contributions and exposure/stress outcomes. Define growth-down, inflation-up, simultaneous nominal-duration/equity loss, commodity reversal, and funding-withdrawal scenarios. Where reliable shock coefficients are available, constrain the relevant exposure map. Where they are not, compare explicit scenarios and conservative caps rather than manufacture precise macro risk contributions. ERC provides a computable baseline, and scenario analysis then evaluates the environmental coverage it achieves.

==== An optional trend overlay, evaluated separately

The original simple design multiplies each base weight by 1.15 when a completed 50-session average exceeds its 200-session average, otherwise by 0.85, then renormalizes. This is a definite, reproducible hypothesis. It uses past state to change future exposure, making it an active predictive overlay. Its accuracy concerns this trading rule, evaluated separately from a pure macro classifier or a generic direction forecast.

Retain this overlay as a *separate development comparison*, with the unmodified ERC portfolio as its benchmark. Preserve sufficient prehistory, lag its observations to the decision time, and use the same rebalance/cost conventions. If $t_(i)$ is the multiplier, the tilted weights are

$
  w_(i)^("tilt")=frac(w_(i)^("base") t_(i),sum_(j) w_(j)^("base") t_(j)).
$

They generally no longer satisfy the original equal risk budgets. Even their relative weight ratio can change by $1.15/0.85 approx 1.35$, not merely 15%. Recheck all risk/exposure/funding limits after tilting. Independently confirmed incremental net value provides the reason to retain the overlay; otherwise keep the simpler base. Structural allocation and the active layer each have their own economic rationale.

Choose leverage through risk and funding analysis, with historical CAGR as an outcome to evaluate. For a fixed exposure vector, volatility scales by the absolute leverage multiple, but financing costs, collateral demands, and exits need not. Start unleveraged; a leveraged comparison requires the Chapter 11 funding path and stress tests. “All weather” is a design objective, not a certificate of shallow drawdowns in every future crisis.

#principle[*Positive allocation decision:* Without a supported macro timing edge, begin with diversified, economically justified exposures and restrained risk budgets, not a forecast of the next quadrant. Implement asset ERC as an inspectable baseline, verify environmental coverage separately, and require active tilts and leverage to pass their own incremental and survival tests.]

== Breadth Amplifies an Edge; Dependence Consumes Breadth

Let $N$ equally scaled P&L opportunities each have mean $a$ and standard deviation $s$. Their sum has mean $N a$. Under independence its variance is $N s^(2)$, giving mean-to-volatility ratio $(a/s)sqrt(N)$. With common pairwise correlation $rho_(c)$, the sum variance is $N s^(2)+N(N-1)rho_(c)s^(2)=N s^(2)[1+(N-1)rho_(c)]$: there are $N$ diagonal terms and $N(N-1)$ ordered off-diagonal terms. Dividing mean $N a$ by this standard deviation instead gives

$
  frac(a,s)sqrt(frac(N,1+(N-1)rho_(c))).
$

For feasible positive $rho_(c)$, the improvement saturates as $N$ grows. At $N=500,rho_(c)=0.1$, the effective ratio multiplier is about 3.13, not $sqrt(500)$ about 22.36. Counting stocks, dates, and nearly duplicated factors does not measure independent breadth.

One idealized bridge to the fundamental law uses independent standardized forecasts $z_(i)$ and active returns $y_(i)$, each mean zero and variance one, with $E[z_(i) y_(i)]=IC$. For jointly Gaussian pairs, write $y_(i)=IC z_(i)+sqrt(1-IC^(2))epsilon_(i)$ with independent standard-normal $z_(i),epsilon_(i)$. The Chapter 7 fourth moment gives $E[z_(i)^(2) y_(i)^(2)]=3IC^(2)+(1-IC^(2))=1+2IC^(2)$; subtracting the squared mean yields $Var(z_(i) y_(i))=1+IC^(2)$. Summing the payoff $z_(i) y_(i)$ across independent pairs gives mean-to-volatility ratio $IC sqrt(N)/sqrt(1+IC^(2))$, approximately $IC sqrt(N)$ for small $IC$. For benchmark-relative active returns, the mean divided by their standard deviation at a declared horizon is the *information ratio*, IR. The calculation motivates $"IR" approx IC sqrt("BR")$ when BR counts suitably independent implemented opportunities. This constructs the familiar scaling under strong normalization, dependence, and implementation assumptions. Real transfer from forecasts to feasible positions can reduce it. Directional hit rate is not automatically this correlation, and breadth cannot rescue false signals or costs exceeding edge.

== Probability Is Not a Size: Derive One Utility-Based Comparison

For independent repeated binary bets, stake fraction $0<=f<=f_("max")<1$ of wealth, with a declared cap. Success probability is $p$, net gain per staked unit is $b>0$, and failure loses the stake. Expected log-wealth increment is $p ln(1+b f)+(1-p)ln(1-f)$. Differentiate:

$
  frac(p b,1+b f)-frac(1-p,1-f)=0,
  quad f^(*)=frac(b p-(1-p),b).
$

The denominators are positive on the chosen interval. Multiply the stationary equation by $(1+b f)(1-f)$ to obtain $p b(1-f)=(1-p)(1+b f)$. Expanding and collecting the $f$ terms gives $b p-(1-p)=b f$. Moreover, the second derivative is $-p b^(2)/(1+b f)^(2)-(1-p)/(1-f)^(2)<0$ for $0<p<1$, so an interior root is the maximum; otherwise clip it to the declared feasible interval. At $p=0$ or one, the monotone objective selects zero or the cap respectively. At $p=0.55,b=1$, the root is 0.10. At the same probability with $b=0.5$, it is negative, so a nonnegative-stake rule abstains. Payoff odds therefore determine size and participation alongside probability.

This is the Kelly log-utility construction for the declared payoff model. Estimated probabilities, correlated positions, costs, rare losses exceeding the stake model, and funding restrictions change the real problem. Fractional Kelly and robust/capped sizes are additional designs. The first trading route uses capped risk sizing, leaving this known-odds repeated-bet construction as a utility-based comparison.

#heading(level: 2, numbering: none)[Practical Default: Three Holding Routes]

*Timing:* Use payoff-derived direction/abstention, then a fixed risk budget. If $q$ is notional return exposure relative to equity and historical return volatility is $hat(sigma)$, $Var(q R)$ is approximately $q^(2) hat(sigma)^(2)$, motivating $|q|=v_("target")/hat(sigma)$ before caps. For equity $E_(0)$, futures price $P>0$, and multiplier $m$, one contract has notional $m P$, so target contract count is approximately $q E_(0)/(m P)$. Round under a frozen rule, check margin/cash, cap leverage and concentration, and abstain for unusable scales. Exposure caps remain binding when estimated volatility is tiny.

*Cross-section:* Use benchmark-relative convex score/risk/trading optimization above, with exposure and turnover limits fixed in development. Keep the rank interpretation explicit. For a small teaching prototype, declare per-name active bounds and one-way turnover limits in the experiment specification; select risk/trading coefficients on development while keeping those policy limits fixed. Confirm net benchmark-relative results against feasible simple ranked and benchmark controls.

*Multi-asset:* Use a stated historical eligible asset set, past-only covariance, positive-target shrinkage, equal risk budgets, and the convex solver with residual checks. An initial teaching convention is a 252-session risk window, shrinkage toward average sample variance times identity, equal budgets, and a preset monthly rebalance; shrinkage strength and risk target require development/stress selection. These numbers are initial specifications, not optimality claims. Respect liquidity and cash/leverage limits; stress shock coverage and covariance. Evaluate bounded trend supplements separately.

*Self-check:* Why do ERC and minimum variance assign different holdings even with independent assets? Why can a neutralized feature create a nonneutral portfolio? Why does a rank score need a scale convention inside an optimizer? Each answer follows from the objective or transformation used in the construction.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Harry Markowitz. #link("https://doi.org/10.1111/j.1540-6261.1952.tb01525.x")[_Portfolio Selection_]. _The Journal of Finance_ 7(1), 77–91, 1952. Mean–variance portfolio construction.
- Olivier Ledoit and Michael Wolf. #link("https://www.ledoit.net/Well-conditioned2004.pdf")[_A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices_]. _Journal of Multivariate Analysis_ 88(2), 365–411, 2004. Covariance stabilization.
- Daniel P. Palomar. #link("https://portfoliooptimizationbook.com/book/11.6-vanilla-convex-formulations.html")[_Portfolio Optimization: Theory and Application_]. Cambridge University Press, 2025. Chapter 11 develops risk-budgeting formulations and solvers.
- J. L. Kelly Jr. #link("https://doi.org/10.1002/j.1538-7305.1956.tb03809.x")[_A New Interpretation of Information Rate_]. _Bell System Technical Journal_ 35(4), 917–926, 1956. Log-growth betting criterion.
- Bridgewater Associates. #link("https://www.bridgewater.com/research-and-insights/the-all-weather-story")[_The All Weather Story_]. Institutional retrospective on cash/beta/alpha separation, environmental exposures, and risk balancing. The lecture baseline is independently specified, not a reproduction of proprietary holdings.
]

#pagebreak()

= Execution and Funding Paths: A Correct Judgment Can Fail before Realization
#counter(math.equation).update(0)

The future can move in the predicted direction while the proposed trade cannot be filled, is too expensive, or is liquidated before the movement arrives. Realization therefore needs its own model: legitimate information time, orders and fills, cash and inventory, scale-dependent costs, and interim funding. The predictor's last score therefore leads into execution and funding decisions that complete the strategy.

Our first route is offline event replay with next-feasible execution, reconciled accounting, a capacity ladder, and explicit failed/partial-order behavior. The lecture specifies research operations; it does not authorize connecting an account or submitting orders.

== A Backtest First Reconstructs Temporal Order

A completed close becomes available, features are calculated, a model returns a score, an order is issued, and an executable fill may occur afterward. Each arrow requires time and a rule. A signal using the final close cannot be assumed to fill at that same close without a matching earlier-known order protocol and venue mechanism.

For each decision record observation availability, computation completion, order issue/acceptance, fill, holding interval, exit, and settlement. The next session's open can be a teaching execution reference only when the instrument/session is eligible and the assumed size/fill rule is declared. A quoted opening price does not guarantee an unrestricted fill there. A quote touch, resting-order accessibility, and an actual matched order are different observations.

Chapter 3's trigger label and later execution now meet in the same ledger. Cash flows arise at accessible fill prices. Missing fills remain recorded events with a defined policy response. If revised execution assumptions change label payouts, gates and confirmation also need reevaluation.

== Derive the Cash and Inventory Invariant

=== Same-price rebalancing cannot create wealth

For a cash-and-stock account, let cash be $C^(-)$, quantity $q^(-)$, and mark price $P$. Wealth is $V^(-)=C^(-)+q^(-) P$. Trade signed quantity $Delta q$ at fill $F$ and fee $c>=0$:

$
  q^(+)=q^(-)+Delta q, quad C^(+)=C^(-) -F Delta q-c,
  \
  V^(+)-V^(-)=-Delta q(F-P)-c.
$

Substitution shows the cancellation explicitly: $V^(+)=C^(-)-F Delta q-c+(q^(-)+Delta q)P=V^(-)+Delta q(P-F)-c$. Thus trading transfers value between cash and stock, preserving the wealth accounting of the exchange. At $F=P$ and zero fee, rebalancing leaves wealth unchanged. At an unchanged midprice with a worse buy/sell fill, the spread reduces wealth. This identity is a basic ledger fixture: changing target weights at one price cannot manufacture pre-cost profit.

With fixed quantity between events, price movement contributes $q(P_("next")-P)$; dividends, financing, and fees enter the cash account at their admitted times. Splits change quantity and price units together. Use fill prices to account for spread/impact, or model those costs separately from a reference fill, but do not subtract them twice. Mark-to-market wealth and available cash are different account quantities.

=== Account for Futures through Settlement and Collateral

For $q$ contracts with multiplier $m$ and settlement change $Delta P$, the price-change cash flow is $q m Delta P$ under the stated settlement convention. Posted margin is collateral, not a payment of the full quoted notional. A simplified reconciled futures account tracks equity, available cash, posted collateral, realized/variation cash, fees, and open inventory. It must not add $q m P$ to equity as though that quoted notional were a purchased stock holding.

A roll closes one real maturity and opens another, producing transactions, costs, and funding changes. Chapter 4's two holding legs earned price-change P&L two, not six from a chart splice. Reconcile that fixture in the executable ledger. Contract expiry, multipliers, and eligibility therefore belong to each instrument in the replay.

=== Pre-rebalance holdings drift with returns

For a frictionless fully invested stock portfolio with targets $w_(i)$ and subsequent asset returns $r_(i)$, portfolio return is $R_(p)=sum_(i) w_(i) r_(i)$. Before the next rebalance, relative weights are

$
  w_(i)^(-)=frac(w_(i) (1+r_(i)),1+R_(p)).
$

If pre-period wealth is $V$, name $i$ begins with value $V w_(i)$ and ends with $V w_(i)(1+r_(i))$. Total ending wealth is $V sum_(j)w_(j)(1+r_(j))=V(1+R_(p))$. Dividing the first quantity by the second gives the displayed weight, assuming positive ending wealth. The denominator is the new total wealth relative to the old. Thus a constant target can require trading after unequal asset moves, while yesterday's target is not today's inventory. Cash flows, leverage, futures, and costs require their own ledger generalization rather than this stock formula pasted indiscriminately.

A simplified return replay is $w_(k)^(T) r_(k+1)-c norm(w_(k)-w_(k)^(-))_(1)-"Impact"_(k)$, when return denominator, one-way cost coefficient, and timing match. This aggregate approximation is useful when its timing and cost terms reconcile with the underlying events.

== Costs Select Participation and Limit Capacity

For one-way trade quantity $q>=0$, expected per-unit gross gain $mu$, proportional cost $c$, and increasing marginal impact $k q$ with $k>0$, total impact is the integral $integral_(0)^(q) k x dif x=k q^(2)/2$. Expected net gain is

$
  A(q)=(mu-c)q-frac(k,2)q^(2).
$

Differentiation gives marginal net gain $mu-c-k q$. The unconstrained nonnegative maximizer is

$
  q^(*)=max(frac(mu-c,k),0).
$

Suppose teaching units give $mu=0.03,c=0.01,k=0.002$. The optimum is ten units and expected net gain 0.1. At twenty units, net gain falls to zero, despite the same per-unit gross prediction. Risk, market depth, concentration, and funding may impose a lower cap. This quadratic example is an assumed cost model, not a universal market-impact law.

It gives a decisive design principle: scale a profitable small replay by examining the marginal costs at each larger size. Run a capacity ladder with the policy frozen and quantities such as one, two, four, and eight multiples of a declared base. Compare fills, gross/net contribution, turnover, cash deficits, and residual exposure. Reestimating the prediction model separately at each scale would confound capacity with a new strategy search.

Costs also explain a no-trade region. For current inventory $q^(-)$, a one-period scalar objective $mu q-lambda sigma^(2) q^(2)/2-c|q-q^(-)|$ has smooth marginal value $mu-lambda sigma^(2) q$. At $q=q^(-)$, the right and left derivatives are this value minus/plus $c$. If $|mu-lambda sigma^(2) q^(-)|<=c$, neither small buy nor small sell improves the objective, so retaining inventory is optimal for the concave teaching model. For $lambda sigma^(2)>0$, the unconstrained frictionless target is $q_(0)=mu/(lambda sigma^(2))$. The exact unrestricted optimum of this one-period concave model is

$ q^(*)=cases(frac(mu-c,lambda sigma^(2)) & "if" q^(-)<frac(mu-c,lambda sigma^(2)), q^(-) & "if" frac(mu-c,lambda sigma^(2))<=q^(-)<=frac(mu+c,lambda sigma^(2)), frac(mu+c,lambda sigma^(2)) & "if" q^(-)>frac(mu+c,lambda sigma^(2))). $

On the buy side, the derivative is $mu-lambda sigma^(2)q-c$; on the sell side it is $mu-lambda sigma^(2)q+c$. Setting each to zero produces the two band edges. If current inventory is between them, the left derivative is nonnegative and the right derivative nonpositive, so no movement is optimal. The half-width is $c/(lambda sigma^(2))$. Under an additional interval of feasible holdings, project this optimum into that interval; coupled multi-asset constraints require the full optimizer. If $lambda sigma^(2)=0$, use the original linear/cost objective and bounds instead of dividing by zero. At larger expected advantage, adjust until a boundary or another limit binds.

This trading band responds to current inventory; the classifier's probability no-trade band responds to forecast probabilities. Both are comparisons of achievable marginal benefit and cost. A factor-trust update therefore need not force an immediate portfolio transaction. A neural learning rate controls fitting; a rebalance clock and trade band control implementation. They govern adaptation at different stages of the strategy.

== Track Actual Fills and Residual Risk across Legs

Desired quantities $q^(*)$ and actual filled quantities $q^("fill")$ leave deviation $q^("fill")-q^(*)$. Convert this vector into comparable risk units using prices, multipliers, and the selected exposure map. One missing contract in a small leg and one missing contract in a large leg are not the same monetary risk.

Consider intended spread inventory $(+1,-1)$ in two related instruments. If only the first buy fills, actual inventory is $(+1,0)$. The intended offset is absent. A quoted spread may have looked positive, yet the account now holds outright movement risk while attempting to complete the second leg.

Define before replay: maximum unhedged exposure, completion time limit, whether to hedge temporarily, when to cancel remaining orders, and when/how to close filled inventory. Canceling an unfilled order differs from reversing a filled position—the latter needs a new price and fees. An “atomic rollback” in research code cannot undo a real market fill. Include reject, partial-fill, stale-quote, and price-gap fixtures; an all-or-nothing simulator is a different admitted approximation.

#principle[*Execution conclusion:* Use accessible orders and actual residual inventory as the basis of the simulation. The completion or unwind policy is part of the strategy and may change whether a theoretical relation is usable.]

== Positive Terminal Payoff Does Not Prove Interim Solvency

Let $K_(t)$ be available liquid resources before a critical obligation and $D_(t)$ the cash requirement due then. Surviving to the intended exit requires $K_(t)-D_(t)>=0$ at each such event, under actual collateral, credit, and settlement rules. Checking each funding event establishes this path condition alongside the terminal-profit calculation.

A trade starting with 100 available units can eventually gain ten but require an interim variation payment of 120. Without accessible additional funding, the positive terminal forecast is irrelevant: the policy may be forced out earlier. Conversely, an increase in posted collateral can reduce available cash without itself reducing mark-to-market equity. Keep those states separate.

Stress simultaneous margin increases, adverse gaps, financing withdrawal, collateral haircuts, delayed receipts, rolls, and expensive exits. If legs share a shock, their funding needs can peak together even when ordinary return correlation looked low. Record maximum stressed deficit and exit feasibility alongside historical maximum drawdown. This is a funding-path evaluation, not a universal margin percentage or a legal conclusion about a particular venue.

#heading(level: 2, numbering: none)[Practical Default: Ledger, Fixtures, Capacity]

1. Freeze available-signal cutoff, next feasible order schedule, instrument eligibility, fill convention, fees, financing, and settlement treatment.
2. Replay quantities and cash/collateral events; link every prediction, trigger, order, fill, and mature outcome to its version and time.
3. Reconcile no-price-change rebalancing, one dividend or variation event, the two-contract roll, an adverse gap, and reject/partial-fill paths.
4. Apply inventory-aware trade bands and fixed risk/funding limits to the transactions implied by each score update.
5. Run the frozen-policy capacity ladder. Stop scaling when marginal costs, liquidity, risk, or cash requirements consume the supported advantage.

A controlled implementation requires offline confirmation, these checks, and separate human authorization. Historical simulation supplies evidence about its assumptions; actual future fills remain subject to execution conditions. The failure mechanism guides the response: a longer horizon, lower turnover, smaller position, different order policy, or refusal of the opportunity may address it more directly than a new predictive network.

*Self-check:* What happens to wealth when inventory is exchanged at an unchanged common price without fees? Why must turnover use drifted inventory? Can an eventual positive spread cover an earlier unfunded margin call? The answers are no wealth change, actual required trades rather than target differences, and not without an available funding bridge.

== Failure Cases: a Correct Terminal Idea Can Be Unfundable

The Federal Reserve's 1998 LTCM testimony describes shrinking profit opportunities, increased leverage, large losses in a changed environment, and concern about fire-sale effects. The account points to interactions among a model, a financing arrangement, market liquidity, and position concentration. These mechanisms provide a more specific lesson than attributing every loss to disappearing cointegration. A convergent terminal forecast does not specify the cash required to remain invested along the path.

The 2022 UK LDI episode makes the distinction especially sharp. The Bank of England reports that rising yields could benefit pension schemes' overall liability positions while leveraged LDI portfolios faced collateral calls and forced gilt sales. Operational lags in obtaining new cash aggravated the pressure. Long-term balance-sheet improvement and short-term payment capability were different states.

Translate these experiences into the existing ledger: stress marks and margin together, assign deadlines to collateral calls, identify usable collateral after haircuts, and model time to obtain or liquidate funding. Include common liquidation responses by other participants rather than assume one's positions exit at ordinary depth. Report the largest deficit *by its due time* and the predetermined action if it cannot be covered. For crypto derivatives, volatile collateral or a venue outage can change that path even while the underlying eventually recovers. For equity-linked tokens, a valuable underlying security is not the same as immediately usable redemption cash.

These cases motivate a survival procedure matched to the instruments and accessible funding. Keep opportunity sizing inside the verified funding envelope. Economic attractiveness and the ability to remain funded until the intended outcome are joint requirements of the strategy.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- Robert Almgren and Neil Chriss. #link("https://doi.org/10.21314/JOR.2001.041")[_Optimal Execution of Portfolio Transactions_]. _Journal of Risk_ 3(2), 5–39, 2001. Execution cost/risk trade-offs; the scalar capacity and trading-band examples above are separately specified teaching models.
- Marcos López de Prado. #link("https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/finance-investments-special-topics-13fiz/advances-in-financial-machine-learning-978-1-119-48208-6")[_Advances in Financial Machine Learning_]. Wiley, 2018. Financial backtesting and strategy-assessment background.
- Alan Greenspan. #link("https://www.federalreserve.gov/boarddocs/testimony/1998/19981001.htm")[_Private-Sector Refinancing of Long-Term Capital Management_]. Federal Reserve testimony, 1 October 1998.
- Bank of England. #link("https://www.bankofengland.co.uk/financial-stability-report/2022/december-2022")[_Financial Stability Report, December 2022_], Section 5. LDI collateral pressure, liquidity and governance lessons.
]

#pagebreak()

= Lifecycle and Traceable Computation: Know What Each Improvement Changed
#counter(math.equation).update(0)

The same model file can produce different results after a data correction, universe change, or new fill assumption. Conversely, the same prediction can reach different holdings because risk or funding rules changed. A useful operating procedure makes these differences traceable, preserves the earlier evidence together with its changed scope, and connects each failure to a specific response.

A workable default combines a full-chain experiment record, retained frozen predictions, scheduled layered review, shadow replay for changes, and reconfirmation before use. These records give monitoring a purpose and a stopping point: further strategy development is worthwhile when the next increment has support.

== Bind Evidence to the Entire Research Route

An experiment result belongs to a tuple of target/exit policy, data snapshot, as-of rules, universe, feature/operator definitions, fitting and selection, prediction versions, aggregation, holdings, costs/fills, funding, benchmark, and evaluation period. A random seed identifies one part of this tuple; releases, dependencies, and the cash ledger also need their own recorded versions for reconstruction.

For the first route, keep one readable manifest alongside the scientific record. It names those inputs, hashes/version identifiers, partitions, trial log, selected parameters, executable environment, and confirmation disposition. Content hashes answer whether bytes changed. Historical truth and availability times are established by the source record and its timestamp evidence. Define numerical tolerance separately from exact identity for implementations that legitimately differ in floating-point ordering.

Retain predictions generated by a frozen version once, with asset/event identity, cutoff, model version, and forecast. Recompute holdings and execution from them for downstream comparisons when the prediction definition is unchanged. A comparison of two fee schedules can therefore reuse the same forecasts. If a feature, target, or input version changes, those retained predictions no longer answer the new question.

=== A change determines which evidence must be renewed

Suppose an inventory timestamp is repaired from Monday to its actual Tuesday release. Monday's feature availability changes; its training examples and historical forecasts can change; selection and replay evidence depending on them must be regenerated. A plot-title repair changes presentation, not those computations. A fee change can leave predictions intact while invalidating gate thresholds, holdings, and net results. A universe change also changes relative labels, not merely the last portfolio table.

#table(
  columns: (1.1fr, 1.6fr, 1.3fr),
  table.header([Change], [Affected consumers], [Required response]),
  [Release/version repair], [As-of features, fitting, selection, predictions, replay.], [Rebuild affected chain and reassess evidence.],
  [Exit or target change], [Labels, model/gate training, aggregation losses, policy P&L.], [Treat as a new strategy definition.],
  [Cost/fill/funding change], [Payoff gate, holdings, realized net and survival paths.], [Reuse valid predictions; recheck downstream decisions.],
  [Caption correction], [Reader-facing representation only.], [Repair and check the affected presentation.],
)

Versioning makes this dependency argument practical: each edit prompts a targeted rebuild, and performance measures stay attached to the strategy definition they evaluated.

#principle[*Traceability conclusion:* A result's validity is revision-scoped. Reuse unchanged supported computations; renew evidence where a changed dependency can alter the conclusion. Reproducibility identifies which claim was tested; economic usefulness is assessed by the resulting decision and payoff evidence.]

== Diagnose Failure before Changing the Model

=== Data integrity, predictive relation, and realization are separate layers

Begin with input integrity: expected observations arrived; clocks and identities match; versions and membership are correct; units, missingness, and stale states follow the dictionary. A critically invalid input prompts suspension of the affected actions or an explicitly approved fallback. Once input validity is restored, the predictive relation can be assessed on its own evidence.

Next inspect mature forecasts and outcomes: calibration, bounded loss against controls, rank IC where applicable, and coverage. Use the same outcome definitions and only available labels. An unfinished trade remains pending in this accounting; assigning it zero loss would distort the comparison just to maintain window length. Statistical deterioration may reflect sampling variation, changed regimes, or genuine relation failure; it does not identify a cause by itself.

Finally inspect holdings, exposure, turnover, realized fills/costs, and funding. Stable forecast loss with worsening net returns points toward changed payoff or realization, although further diagnosis is still needed. Unchanged forecasts with new exposure violations can indicate a holding or data-mapping defect. These contrasts direct investigation toward the affected layer, giving a drawdown a more specific interpretation than a general request for a new network.

=== Repeated review changes the probability of a false alarm

With $M$ independent reviews each having false-alarm rate $alpha$, the chance of at least one alarm is $1-(1-alpha)^(M)$. At weekly nominal 5% reviews for 52 independent weeks, it is about 0.931. Real rolling windows overlap, so that number is not their false-alarm probability; it illustrates why a local level cannot automatically be read as a global level.

For a fixed set of $J$ valid tests, independence is unnecessary for a union-bound policy: allocate levels $alpha_(j)$ satisfying $sum_(j) alpha_(j)<=alpha$. Let $A_(j)$ denote a false rejection under its valid null. For every outcome, $1_(union_(j) A_(j))<=sum_(j)1_(A_(j))$ because at least one individual indicator is one whenever any alarm occurs. Taking expectations gives $Pr(union_(j)A_(j))<=sum_(j)Pr(A_(j))<=sum_(j)alpha_(j)<=alpha$. No cross-test independence was used. Then the probability of any false alarm is at most $alpha$. For example, three specified metrics at four planned quarterly reviews could each use level $0.05/12$ to control that fixed family. The budget controls the family when each test is valid for its dependence and null; a test built on an invalid IID formula still needs a suitable replacement. Adding unplanned metrics or choosing review times after seeing outcomes changes the procedure.

Continual valid inference uses a sequential construction with stated assumptions and error control. For our first procedure, prespecified review dates, metrics, grouping, and tolerances provide a simpler route, while hard data/risk violations prompt immediate action. A noisy rolling statistic crossing zero starts the scheduled diagnosis; repeatedly inspecting an ordinary p-value until it looks favorable would change the procedure and its error rate.

=== Give suspend, investigate, retire, and redevelop different meanings

*Suspend* prevents affected new actions while a hard validity or limit condition is unresolved. Its rule includes existing inventory, so the response covers both stopping new orders and managing the remaining position. *Investigate* preserves a version and collects the comparisons needed to distinguish data, relation, exposure, and realization changes. *Retire/downweight* reduces or removes a factor's unsupported role in the strategy according to the recorded policy. *Redevelop* changes the strategy definition, starting a new recorded selection and confirmation process.

Prespecify which observations lead to each action. Hard input/limit violations trigger immediate containment. Statistical deterioration triggers the scheduled diagnosis; pragmatic risk reduction may be authorized while the cause remains statistically unresolved. A confirmed implementation fault requires repair/reconciliation. A persistent failure of independently supported usefulness can justify retirement. Failed versions remain in trial history through favorable recovery or redeployment.

== Evaluate Changes in Shadow and Retain Their History

A *shadow replay* runs the proposed version on the same permitted information without allowing its recommendations to become account actions. Compare forecasts, holdings, ledger events, resource use, and failure responses with the current frozen version and its controls. It can expose operational discrepancies and new costs. Agreement in shadow supports operational consistency; a newly selected predictive relation also needs independent confirmation.

For a release repair, trace the first changed row to every later dependent forecast and holding. For an optimizer change, hold the target, data, architecture, and training budget fixed, compare fitting behavior and development outcomes, and count the route selection. For a capacity upgrade, keep semantics and admitted numerical precision fixed; a faster scorer using a different fill approximation is a different research operation.

Promotion brings together the appropriate correctness, confirmation, cost, funding, and recovery checks, followed by separate authorization for actual use. A known-good version and a recovery route make rollback feasible. Restoring the old strategy means restoring its compatible transforms along with its predictor.

== Scale Work by Its Bottleneck

Suppose fraction $s$ of a fixed job is serial and the remainder can be divided ideally over $p$ workers. In units of the original execution time, even ideal parallel time is at least

$
  s+frac(1-s,p), quad
  "Speedup"<=frac(1,s+(1-s)/p).
$

The serial part still takes $s$ units; the ideally divided remainder takes $(1-s)/p$ units. Speedup is old time divided by new time, so the original unit time divided by this lower bound gives the displayed upper bound. At $s=0.2,p=8$, ideal speedup is at most about 3.33; with infinitely many workers it cannot exceed five. Communication, synchronization, and contention can lower actual performance further. The algebra supplies a reason to remove serial repeated work before adding processors. It says nothing about a larger differently defined job's speedup.

Measure data reads, transforms, scorer computation, fitting, synchronization, and failed/repeated work separately. Shared reads, common-subexpression caches, and batched inference can reduce unnecessary work. Parallelize independent evaluations with consistent snapshots and explicit failure statuses. Consistent snapshots keep differences in dataset age from masquerading as differences in factor quality.

A simple full-precision Adam memory account with $P$ scalar parameters uses four bytes each for parameters and gradients and eight for two moment arrays: about $16P$ bytes before activations, buffers, workspaces, and serialization. Different precision/optimizer implementations change this account. Replicated data parallelism keeps model copies and synchronizes gradients; sharding distributes selected states at communication and transient-memory cost. The model-state arithmetic alone does not determine peak memory or complete throughput. Measure those quantities before choosing another topology.

At the small lecture scale, partitioned files, deterministic transforms, one scorer, and a recoverable snapshot can be enough. The aim is faithful, affordable replay. A larger computer supplies more evaluations on the available market evidence; Chapter 8's selection burden grows when that capacity leads to more trials.

== Recoverability and Authority Have Their Own Checks

Redundancy keeps some failures from interrupting availability. A snapshot preserves a version. A backup retains a recoverable copy under a stated loss scenario. A restore test establishes that the copy can be reopened and the replay reconciled. Keeping multiple synchronized copies does not protect against a mistaken deletion synchronized to all of them. Test recovery of both data and the definitions needed to interpret it.

Knowledge and permission follow separate chains. Dataset access, redistribution, and third-party transmission have distinct permissions. Moving from an offline strategy result to credential use, trading, new funding, publication, or a recurring job likewise calls for the applicable user, license, provider, venue, and legal conditions for that object and date. The discussion identifies those checks; an institution-specific legal conclusion needs its own assessment.

#principle[*Lifecycle conclusion:* Make results repeatable, anomalies locatable, failures containable, and changes re-verifiable. Suspend, diagnose, retire, and redevelop deliberately. Automation operates within existing authorization, and further production depends on supported opportunities.]

#heading(level: 2, numbering: none)[Practical Default: One Experiment and Operating Record]

Freeze a readable full-chain manifest and retain its predictions, trial record, confirmation disposition, and reconciliation fixtures. Check a rerun against exact identities where appropriate and declared numerical tolerance elsewhere; investigate unexplained differences. Keep the record local, sized to its actual users and the information needed for reproducibility.

Use three monitoring layers: input integrity/availability; mature task performance/calibration; holdings, costs, fills, and funding. Choose review windows and thresholds from development/stress evidence, with enough completed opportunities for the stated comparison. Fix review frequency and error policy. Hard failures suspend affected actions; statistical deterioration triggers investigation; confirmed loss of usefulness changes how the factor is used. Modified data/model/policy versions start in shadow and return through the necessary confirmation gates.

Scale in measured order: remove duplicate work, batch/cache, parallelize independent jobs, and use sharding when an observed memory/communication need justifies it. Restoring and reconciling one snapshot tests recoverability in practice. Actual monitoring automation and trading authorization are separate implementation and permission decisions.

#heading(level: 2, numbering: none)[Synthesis: Eight Decisions, One Honest Chain]

The first twelve chapters now connect the original methodological center to an executable research design. Label and feature choices define the usable task; verification prevents selection from pretending it improved that task; holdings and execution determine whether the supported increment can survive in cash terms.

#table(
  columns: (0.8fr, 1.45fr, 1.65fr),
  table.header([Stage], [Question and selected route], [Concrete output]),
  [1. Problem], [What opportunity and economic outcome matter?], [Policy, universe, horizon, sign/relative/event role.],
  [2. Target], [Ask only required distinctions; first passage for a stop/target policy.], [Label, payout and maturity definitions; participation threshold.],
  [3. Data], [What was actually available, and which instrument was held?], [As-of version view, historical universe, cash bridge.],
  [4. Features], [Expose task-relevant state and relations.], [Small multiscale/contract panel; controlled additions.],
  [5. Verification], [What survived search-independent assessment?], [Frozen confirmation, baseline increment, factor dossier.],
  [6. Prediction], [Express remaining relations with restrained capacity.], [Probability/rank model; loss, step, budget; weak aggregation.],
  [7. Holdings], [Which supported judgments justify feasible exposure?], [Risk-sized timing, active constraints, or stabilized risk budgets.],
  [8. Realization], [Can the path be filled, funded, recovered, and monitored?], [Reconciled ledger, capacity/funding tests, lifecycle actions.],
)

This conceptual order also allows feedback from feasibility checks. Defining the target gives learning a clear direction; data and realization checks may then reveal that the target needs revision because it cannot be observed or executed. A label definition need not wait for a data platform; actual labels cannot be generated without admissible observations. Feedback changes a version and its evidence obligations, not the principle of selecting the question before fitting its answer.

For copper-style timing, the selected chain is policy-aligned coarse outcomes, a small multiscale and contract-state panel, probability baseline then shallow trees, honest factor admission, payoff participation, inverse-volatility capped size, and actual-contract replay. For cross-sectional enhancement, it is same-date relative comparisons, explicit context and restrained set structure only when useful, ranking loss, constrained benchmark-relative holdings, and net confirmation. For allocation without mean edge, it is shock coverage and stabilized risk budgets first, with bounded independently confirmed prediction supplements.

The unifying decision is to match model expression to the relation the task needs, ask for useful precision, and reserve bets for supported judgments. Depending on the task, that can mean a simpler model or a structure that captures an otherwise inaccessible relation. More exact optimization cannot repair absent information; coarse targets cannot replace payoff accounting; a low-regret aggregator cannot certify profit; a correct terminal forecast cannot finance an adverse path. The practical designs above retain the small supported increment while preventing those category changes.

*Self-check:* After changing a release timestamp, which cached results remain valid? After changing only fees, must prediction fitting always be repeated? Can a complete rerun establish that an input release time was historically true? The answers are only unaffected dependencies, not if prediction semantics are unchanged, and no: repeatability and historical validity are different evidence.

== Operational Experience: Safety Controls Beyond the Model

The SEC's findings on Knight Capital's August 2012 incident identify inadequate deployment/testing, order controls, exposure controls, and incident-response procedures. The reported trading loss exceeded 460 million dollars. The findings concern execution-system failure; they identify operational mechanisms rather than a deterioration in prediction accuracy.

The practical consequence is to test what can stop an erroneous action after prediction has succeeded. Reconcile the deployed version across workers, compare outbound orders with authorized parent intent, enforce aggregate exposure limits independently of the signal, and define an incident owner and a tested halt procedure. A halt prevents new unintended orders and includes separate handling of outstanding orders and existing inventory. The available market and exit policy determine how that inventory can be reduced. Rehearse restoration on isolated historical replay before relying on it.

Monitoring becomes actionable when dashboards lead to named responses. The research manifest connects a changed prediction or rule to its evidence; operational controls bound what a malformed or mismatched implementation can do. Together they address research validity and operational containment, with distinct checks for each.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]

- D. Sculley et al. #link("https://proceedings.neurips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html")[_Hidden Technical Debt in Machine Learning Systems_]. NeurIPS, 2015. Dependencies and operational system behavior beyond the predictor.
- PyTorch maintainers. #link("https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html")[_DistributedDataParallel_], official documentation. Model replication and synchronized gradient semantics; executable details must match the installed implementation version.
- Marcos López de Prado. #link("https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/finance-investments-special-topics-13fiz/advances-in-financial-machine-learning-978-1-119-48208-6")[_Advances in Financial Machine Learning_]. Wiley, 2018. Financial research and backtesting context for the full chain.
- U.S. Securities and Exchange Commission. #link("https://www.sec.gov/newsroom/press-releases/2013-222")[_SEC Charges Knight Capital With Violations of Market Access Rule_]. 16 October 2013. Findings concerning the 1 August 2012 incident.
]

#pagebreak()

= Arbitrage Relations: Identify the Constraint, Then Test Realization
#counter(math.equation).update(0)

The first twelve chapters developed forecasts and their route into holdings. We now ask a different question: *Which cash flows or prices are linked by a tradable construction?* A relation reduces the forecasting problem through its tradable legs, financing, and settlement. When completion remains uncertain, the same relation supports a convergence hypothesis whose outcome still carries risk.

Our first research design follows the relation: a cash-flow comparison for a hard constraint, or a small stateful residual strategy for a statistical relation. Each route identifies the quantities to estimate. The examples below are constructed arithmetic, not reported opportunities.

== Equal Cash Flows Give a Price Constraint

=== Build the trade before naming the arbitrage

Suppose positions A and B pay exactly the same amount at the same times in every permitted future state. If A costs 99 and B can be sold for 101, buy A and short B. Their future cash flows cancel, leaving two units now. This construction assumes that borrowing B is permitted, its cash flows and recall conditions are matched, and fees do not exceed the difference. These assumptions are checked through the instruments and their trading terms, beyond the resemblance of their charts.

In a one-period idealization, let a permitted strategy have initial net cost $C_(0)$ and terminal net cash flow $X_(T)$. A *strict arbitrage* has $C_(0)<=0$, $X_(T)>=0$ almost surely, and a strictly positive benefit either initially or in terminal states of positive probability. The construction also depends on interim financing and admissibility conditions. “Almost surely” means that the exceptional states have probability zero under the specified model; it is not a promise that a model describes every real-world contingency.

A positive expected payoff is different: it permits losing states. A pair that usually reverts, a merger that usually closes, and an exchange account earning funding all retain such states. Calling them arbitrage does not remove their risks.

=== A currency triangle is a unit calculation

Let an executable exchange convert A to B at $x$ units of B per A, B to C at $y$ units of C per B, and C to A at $z$ units of A per C. Starting with one A gives

$ 1 " A" -> x " B" -> x y " C" -> x y z " A". $

The product is dimensionless because the currency units cancel. Suppose the quoted executable directions are $x=2$, $y=3$, and $z=0.17$. The cycle returns 1.02 A before additional fees. If each conversion retains a fraction 0.999 after fees, the result is $1.02 times 0.999^(3) approx 1.01694$. But a midpoint rate of 0.17 with an executable rate of 0.166 would instead return 0.996 before fees. The spread changes the decision.

For each direction and size, the relevant rate is the executable bid or ask. The smallest leg capacity limits the cycle, and synchronized quotes establish its simultaneous availability. A fill on a single leg leaves an outright position until the other legs complete the cash-flow cancellation.

*Selected route:* build a unit-aware executable cycle; reject mismatched times, insufficient size, and incomplete cash-flow identity before searching for a signal. Simulate partial fills and the action for unwanted inventory. Checking the cycle itself comes before measuring the value of a faster detector.

== When the Relation Is Public, Execution Can Become the Edge

Assume, as a teaching model, that an opportunity's remaining gross edge after latency $l$ is $Delta_(0) exp(-l/tau)$, where $tau>0$ is its decay scale. Net edge after cost $c>0$ is positive exactly when

$ Delta_(0) exp(-l/tau)>c,
  quad l<tau ln(Delta_(0)/c). $

Divide by $Delta_(0)>0$, take logarithms, and obtain $-l/tau>ln(c/Delta_(0))$. Multiplying by the negative value $-tau$ reverses the inequality, giving the displayed latency limit. Since a latency cannot be negative, the second condition is useful only if $Delta_(0)>c$. For an initial edge of 10 basis points, a cost of 4, and decay scale 20 milliseconds, the maximum latency is about 18.3 milliseconds. Reducing latency from 15 to 5 milliseconds increases modeled remaining gross edge from about 4.72 to 7.79 basis points. If costs are 12 basis points, even zero latency cannot make this particular opportunity positive.

This calculation explains why public, rapidly competed relations can reward quote synchronization, inventory placement, and lower costs more than a forecasting network. The exponential decay law and the importance of latency remain properties to test for the opportunity being studied. Estimate the opportunity's decay and completion rate from admitted quote/order observations before spending on faster infrastructure. Funding constraints, uncertain completion, segmentation, and compensation for bearing risk can all sustain slow spreads alongside any computational bottleneck.

#principle[
  *Execution conclusion:* first determine whether the price relation is hard or statistical, then measure the bottleneck. Additional executable net capture gives a concrete basis for investing in faster systems.
]

== Remove a Common Trend Without Inventing Reversion

=== Correlation does not supply the required relation

Two prices can rise together because both contain the same growing component. Construct a *random walk* $G_(t)=G_(t-1)+u_(t)$ from independent, zero-mean shocks with variance $v>0$. Expanding the sum gives $Var(G_(t)-G_(0))=t v$: old shocks do not decay.

Let disturbances $e_(t)^(A)$ and $e_(t)^(B)$ have stable finite-variance distributions, and define

$ A_(t)=G_(t)+e_(t)^(A), quad
  B_(t)=beta G_(t)+e_(t)^(B), quad beta != 0. $

Their common component cancels in

$ Z_(t)=A_(t)-B_(t)/beta=e_(t)^(A)-e_(t)^(B)/beta. $

If the disturbance pair is stationary, this spread is stationary. Here *stationary* means that its joint distribution is unchanged by shifting all observation times. A weaker version keeps only means, variances, and lagged covariances unchanged. Neither definition says that tomorrow must be nearer the mean.

Nonstationary price levels with a stationary linear combination motivate *cointegration*. By contrast, two correlated random walks can still have a random-walk difference: take $B_(t)=A_(t)+H_(t)$ with an additional independent random walk $H$. Their shared movement does not make $A-B=-H$ revert.

=== A separate dynamic assumption produces a convergence forecast

Suppose the residual around a center $m$ satisfies

$ Z_(t+1)-m=a(Z_(t)-m)+epsilon_(t+1), quad 0<a<1,
  quad E[epsilon_(t+1) | "past"]=0. $

The vertical bar means averaging over future shocks given the stated current/past information. After one step, the deviation is $a(Z_(t)-m)+epsilon_(t+1)$. After two it is $a^(2)(Z_(t)-m)+a epsilon_(t+1)+epsilon_(t+2)$. Substituting the recursion repeatedly establishes the coefficient $a^(h-j)$ for the shock at $t+j$. Future shocks have conditional mean zero by iterated conditioning on their own preceding information; averaging them gives

$ Z_(t+h)-m=a^(h) (Z_(t)-m)
    +sum_(j=1)^(h) a^(h-j) epsilon_(t+j),
  \ E[Z_(t+h)-m | Z_(t)]=a^(h) (Z_(t)-m). $

For independent shocks of common variance $sigma_(epsilon)^(2)$, the conditional variance of the shock sum is the geometric series

$ sigma_(epsilon)^(2) sum_(j=0)^(h-1) a^(2j)
  =sigma_(epsilon)^(2) frac(1-a^(2h),1-a^(2)). $

The conditional variance is a sum of squared coefficients because distinct shocks have zero covariance. Its ratio is $a^(2)$: multiplying the finite sum by $1-a^(2)$ cancels all interior terms and leaves $1-a^(2h)$. The expected deviation halves when $a^(h)=1/2$, so the *half-life* is $ln(1/2)/ln(a)$. With $a=0.9$, it is about 6.58 observation periods. An initial deviation of 4 has expected convergence $4(1-0.9^(7)) approx 2.09$ units over seven periods. Combined costs of 2.5 units make that trade unattractive even before a risk allowance. A two-standard-deviation observation is not automatically a worthwhile position.

The model supplies an expectation and dispersion, not a deadline guaranteed by cointegration. Negative or near-unit fitted coefficients change the interpretation; unstable coefficients can invalidate the forecast. Use development data to estimate the relation and dynamics, and preserve uncertainty rather than reporting a half-life with spurious precision.

== Test the Relation in Light of Its Selection History

A first diagnostic asks whether shocks accumulate permanently. In a residual recursion $Z_(t)=a Z_(t-1)+epsilon_(t)$, subtracting $Z_(t-1)$ gives $Delta Z_(t)=(a-1)Z_(t-1)+epsilon_(t)$. The value $a=1$ is a *unit root*: shocks persist in levels. An augmented Dickey–Fuller regression adds lagged differences to account for serial structure and tests the corresponding zero coefficient. Its null distribution is not an ordinary independent-error regression reference.

Engle–Granger first estimates a price relation and then tests its fitted residual. Because the residual itself was selected by estimation, the residual-test critical values differ from those for a prespecified observed series. Deterministic intercept/trend choices and lag choices also change the tested question. Johansen's system method extends the analysis to several series and potentially several relations; it needs its own lag, trend, and sample specification. The study specification supplies these choices before the library call carries them out.

With $n$ assets there are $n(n-1)/2$ pairs. At 100 assets there are 4,950. Searching all pairs, windows, coefficients, and thresholds creates the selection problem of Chapter 8. Estimating a hedge coefficient on the entire history and replaying it backward leaks future information even if the subsequent entry rule looks simple.

*Practical choice:* begin with a small economically related candidate set; record its selection history; estimate relation, residual dynamics, and costs only in development. Reserve chronological confirmation for the frozen complete strategy. Gatev, Goetzmann, and Rouwenhorst provide a historical relative-value study with its own construction. Applying its lessons to a modern pair, exchange, token, or cointegration strategy calls for confirmation of that new setting.

== A Stateful Spread Policy Is the First Implementable Strategy

Use a frozen residual coefficient and timely center/scale to form $z_(t)=(Z_(t)-hat(m))/hat(s)$ with $hat(s)>0$. The teaching entry thresholds are ±2; the exit band is ±0.5. These specify *hysteresis*: entry and exit boundaries differ, reducing repeated opening and closing around one noisy threshold.

#table(columns: (1.05fr, 1.6fr, 1.6fr),
  table.header([Current state], [Observed condition], [Declared action]),
  [Flat], [$z>2$], [Consider short spread after convergence/cost and funding checks.],
  [Flat], [$z< -2$], [Consider long spread after the same checks.],
  [Spread held], [$abs(z)<=0.5$], [Exit at later feasible fills.],
  [Any held state], [Horizon, loss, cash, or relation-break limit reached], [Apply the prespecified exit/suspension response.],
)

The identical value $z=1$ means “do not enter” while flat but “continue waiting” for a previously entered short spread. The holding state gives the classifier the information needed to express this policy. A maximum horizon based on the development-supported decay scale bounds the wait for convergence. Reestimation follows a declared past-only schedule; a relation change during an open trade includes explicit treatment of its holdings and evidence.

For a spread in *price levels* $Z=A-B/beta$, one unit of spread maps to one A and $-1/beta$ B units under the model's currency/multiplier convention. For $Z=ln(A)-beta ln(B)$, a local movement is $dif Z approx dif A/A-beta dif B/B$. An exposure scale $k$ therefore maps approximately to quantities $q_(A)=k/A$, $q_(B)=-k beta/B$, not $(1,-beta)$ shares. Rebalancing these quantities changes cost and path dependence. Dividends, contract multipliers, and currencies require their own ledger.

For A-share candidates, feasibility starts with historical borrow and sale permissions for both instruments. If the available actions are long-or-flat, the resulting policy and exposure reflect that constraint. For a stock token and its reference share, first resolve the same cash-flow, conversion, issuer, and session distinctions introduced in Chapter 1. A closed reference market delays the hedge, leaving reference-session risk in the convergence trade.

*Complete first experiment:* choose related instruments → build the as-of opportunity set → estimate and freeze a relation → inspect residual dynamics → specify hysteresis, horizon, quantity conversion, and cash caps → replay later actual fills → confirm net increment against no position and a simple spread control. Preserve rejected/no-fill cases and failed relationships.

#principle[
  *Chapter conclusion:* use replication and executable inequalities for identical cash flows; use a verified dynamic model and stateful policy for uncertain convergence. The tradable construction determines how much of the forecasting task the relation can remove.
]

*Self-check:* Why can two strongly correlated prices have a nonstationary difference? What makes a seven-period convergence expectation different from a guaranteed exit? Why are log-price coefficients not share counts? Answer by constructing the extra random walk, retaining the shock sum, and differentiating the log spread.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]
- Robert F. Engle and Clive W. J. Granger. #link("https://doi.org/10.2307/1913236")[_Co-Integration and Error Correction: Representation, Estimation, and Testing_]. Econometrica 55(2), 251–276, 1987.
- Evan Gatev, William N. Goetzmann, and K. Geert Rouwenhorst. #link("https://www.nber.org/papers/w7032")[_Pairs Trading: Performance of a Relative Value Arbitrage Rule_]. NBER Working Paper 7032, 1999.
- Kraken. #link("https://www.kraken.com/legal/xstocks")[_xStocks Risk Disclosure_]. Instrument, issuer, and underlying-share distinctions; product documentation checked 11 October 2026.
]

#pagebreak()

= Arbitrage Tasks and Text Tools: Outcomes, Time, and Capital Choose the Method
#counter(math.equation).update(0)

An event, a currency cycle, an exchange spread, and a futures basis can all be called arbitrage. Yet each asks a different question. This chapter constructs a first route for each: extract contractual facts and calibrate event outcomes; test executable cash-flow identities; or manage basis and funding in a joint ledger. The economic source of the payoff guides the operation, giving each task a more useful description than the shared category name.

== A Merger Spread Is an Event-Payoff Problem

=== Derive the completion threshold

Consider a cash acquisition. A target share costs $P$ now, pays $U$ if the deal completes, and is worth $D$ in a simplified failure state. Let completion probability be $p$ and total modeled fees/funding cost be $c$. Buying one share has expected net payoff

$ E[Pi]=p U+(1-p)D-P-c=p(U-D)+D-P-c. $

Expand $(1-p) D=D-p D$ and collect the two terms containing $p$. Positive expectation is $p(U-D)>P+c-D$. Dividing by the positive payoff gap $U-D$ preserves the inequality, so when $U>D$, positive expectation requires

$ p>frac(P+c-D,U-D). $

For $P=95$, $U=100$, $D=80$, and $c=1$, the threshold is 0.80. At $p=0.75$, expected payoff is $75+20-96=-1$; at $p=0.90$, it is $90+8-96=2$. The payoff asymmetry explains the high threshold: the successful trade gains 4 after cost, while failure loses 16.

The break price is not necessarily the pre-announcement price: market moves, business damage, alternative bids, and termination payments can change it. A *reverse termination fee* is a contractual payment by the buyer in specified circumstances, not automatically a per-share payment to the investor. Extract who pays whom, under which condition, and at what time before changing $D$.

=== Time is part of the cash flow

If deterministic completion/failure payments occur at times $T_(U)$ and $T_(D)$, a constant-rate discounted comparison is

$ p U exp(-r T_(U))+(1-p)D exp(-r T_(D))-P-c. $

Use one consistent cost convention: if borrowing interest is already charged explicitly in the ledger, do not subtract it a second time by misinterpreting discounting. Distributions or explicit scenarios represent random deadlines and the variation hidden by a single average date. A two-unit expected gain in one week and in six months ties up capital differently, and an interim mark can demand cash before either payment.

For an all-stock deal paying $a$ acquirer shares, the success payoff is $a S_(T)$ rather than a fixed $U$. Shorting the matching acquirer quantity can hedge part of this exposure only with feasible borrow, dividends, and exchange terms. Collars and election clauses change the function further. First write the contract's payoff states; then choose what to predict.

Solving $P=p U+(1-p)D$ for $p$ yields a *spread-implied number*, not necessarily the physical completion probability. Discounting, risk compensation, alternative outcomes, liquidity, and investor constraints all enter observed prices. The useful judgment is a better calibrated payoff distribution for the admitted policy, assessed with those pricing influences in view.

== Make Text a Located Observation Before Making It a Forecast

=== The event dossier is the first product

The relevant information may be buried in agreements, filings, approval decisions, and amendments. A text model can help transform that material into structured observations. Begin with a small event dossier, connecting each field to the decision it informs:

#table(columns: (1fr, 1.25fr, 1.65fr),
  table.header([Field], [Required evidence], [Decision consequence]),
  [Consideration and elections], [Exact clause, units, amendment version], [Construct success cash flows and hedge quantities.],
  [Closing conditions], [Approvals, votes, financing conditions], [Define completion states, not a generic sentiment score.],
  [Termination/deadline terms], [Dates, extensions, fee recipients and triggers], [Construct failure, delay, and payment scenarios.],
  [Publication and receipt], [Source timestamp and actual availability], [Determine what a historical forecast could use.],
  [Unresolved facts], [Missing/conflicting clause locations], [Request source review or abstain from a claim.],
)

The dossier fields guide passage retrieval, supplementing textual similarity to “good deal” with the contractual details each decision needs. Preserve adjacent exceptions, definitions, and cross-references: “financing is committed” and “subject to the following conditions” can be inseparable. A passage without a clause is missing evidence, not evidence that no such clause exists.

A first pilot manually annotates a small declared set of documents, then compares model extraction with those located annotations. Record omitted clauses, wrong negation, wrong payee, and unresolved fields separately. Structured JSON supports parsing; comparison with located clauses supports factual accuracy. A second model checking the same text can assist that review, while independent source verification remains a separate check.

=== Extracted facts and calibrated probabilities are different products

An LLM's next-token probability is a distribution over text fragments. Completion probability is a distribution over event outcomes. They differ in sample space, labels, and evaluation. Bridging the two calls for an outcome model and its calibration, beyond the confidence of a narrative or a sequence of yes/no answers.

Start with a historical completion-frequency baseline and a small regularized event model using verified fields, event age, and relevant state available at the time. Training uses matured, historically available outcomes, with event-and-time splits that keep passages from a deal in the same partition. Define how still-pending events are treated; calling every unfinished event a failure biases a time-to-completion model. At a fixed horizon, distinguish completed, definitively failed, and still pending states or use a time-to-event method with explicitly handled incomplete follow-up.

Assess probability calibration and net decision value at the payoff-derived threshold. Shared buyers, jurisdictions, financing, or regulatory shocks can make many events one concentrated risk. The language model makes useful facts accessible. The event-probability model then learns from those facts and is evaluated as a separate fitted model.

=== Historical text has two leakage channels

The retrieval corpus follows the decision cutoff. The model weights introduce another channel: pretraining may already have included a later outcome, and that information can survive a restricted prompt. For a defensible historical test, use a model whose training chronology supports the evaluation interval, or a design that limits the model to checkable extraction while evaluating the consuming forecast prospectively. Report any remaining uncertainty about training contamination alongside the prompt and evaluation design.

Freeze model identity, prompt, retrieval policy, document version, decoding configuration, and output cache. Low temperature reduces a source of variation but hardware, kernels, ties, and service changes can still matter. Reproducibility and historical admissibility remain separate checks, as in Chapter 12.

=== Scale the pipeline only after its single-event route works

The useful serving chain is versioned acquisition → field-specific retrieval → bounded extraction → schema and source checks → cached dossier → calibrated event forecast. Failed requests and invalid schemas keep explicit failure statuses, making them distinguishable from genuine neutral scores. Documents are untrusted data, including any instructions embedded in them.

Self-hosting can give model/version control and keep permitted sensitive data local; a hosted service can reduce maintenance and suit a small workload. Choose from data permissions, version guarantees, actual throughput, latency, and total cost. These comparisons establish which APIs are affordable and which data may be sent externally. PagedAttention contributes serving-memory management; event-forecast accuracy is assessed downstream. One process and a frozen cache provide a starting point, with batching and replicas added in response to measured bottlenecks.

*Selected event route:* source-backed dossier → small calibrated completion/time model → scenario payoffs → participation threshold → concentrated-event and funding caps → chronological complete-policy confirmation. Clause extraction supplies evidence to review; legal interpretation and order execution retain their own authority and authorization.

== Cross-Market Spreads Need Prefunded Inventory and a Joint Ledger

Suppose the same deliverable coin can be bought at venue A for 100 and sold at B for 101. Buying at A and transferring before selling at B exposes the account to price changes and transfer delay. Buying A while selling inventory already held at B removes the immediate transfer from the execution path, but consumes prefunded cash and inventory at two venues.

For quantity $q$ with executable prices $P_(A)^("ask")$ and $P_(B)^("bid")$, matched gross cash is $q(P_(B)^("bid")-P_(A)^("ask"))$. Net contribution also includes fees, subsequent inventory rebalance, financing, and failed-leg handling. Verify asset identity, network, transfer mechanism, currency, quantity, and redemption rights: two tickers need not be the same deliverable object.

At the initial match, A loses cash and gains coin; B gains cash and loses coin. The combined account can show a profit while B becomes unable to support another sale. That makes capital placement and rebalance frequency part of the strategy. Keep venue balances separate; a dollar stranded on A cannot meet a deadline on B simply because a spreadsheet sums them.

A tokenized equity versus its reference share adds a legal and session bridge. The issuer's documented unit conversion, fees, transfer restrictions, and redemption conditions determine whether conversion is possible for this holder. A closed share market, redemption queue, or ineligible holder can destroy immediate cash-flow matching. In that case, study later relative outcomes or wrapper risk under an explicit policy instead of labeling the observed gap a strict arbitrage.

== Spot–Perpetual Funding Is a Basis-and-Cash Path

Take one unit of spot bought at $S_(0)$ and one unit of a *linear* perpetual sold at $F_(0)$, with compatible units and approximate matching price sensitivity. Let $b_(t)=F_(t)-S_(t)$ and let $f_(k)$ be actual funding received by the short, signed so payments by the short are negative. Marking both legs to $T$ gives

$ Pi_(T)=(S_(T)-S_(0))+(F_(0)-F_(T))
    +sum_(k) f_(k)-c
  =b_(0)-b_(T)+sum_(k) f_(k)-c. $

Here $c$ includes the declared execution, financing, and rebalance costs. For opening basis 2, closing basis 0.5, total received funding 0.8, and costs 0.4, net payoff is 1.9. If closing basis instead reaches 5 and funding flips to −0.3, payoff is $2-5-0.3-0.4=-3.7$. Future funding and terminal basis remain variable, so today's positive funding leaves both terms to be assessed over the path.

Even when total price delta is near zero, the short-perpetual venue can require collateral as its mark rises. An offsetting spot gain held elsewhere may be unavailable on that venue's deadline. Include mark/index conventions, margin tiers, collateral haircuts, liquidation policy, funding publication/payment clocks, and transfers. Nonlinear or inverse contracts call for a payout derivation that reflects their own units and mechanics.

The CFTC's 2024 FTX/Alameda judgment describes commingling and misappropriation of customer assets. The findings identify exchange custody/default exposure as a separate risk alongside basis and funding mathematics. Losses may differ across funding strategies, and reconciling a model ledger leaves custodian performance to its own evidence and limits. Track counterparty exposure and cash accessibility as independent limits.

*First funding experiment:* one liquid historically eligible spot/linear-contract pair; explicit entry and exit quotes; realized funding rather than advertised annualized rates; bounded prefunded collateral; and scenario paths for sign reversal, widening basis, unavailable transfer, and venue failure. Compare the complete outcome with cash/no trade before adding a rate forecaster. A small past-only rate model earns a role through improvement in that net policy.

== Derive Carry Relations from What Can Be Delivered

=== Spot borrowing and forward delivery

In an ideal market, borrow $S_(0)$ at constant continuously compounded rate $r$, buy one non-dividend asset, and sell a forward delivering that asset at $T$ for $F_(0)$. At delivery, receive $F_(0)$ and repay $S_(0) exp(r T)$. If $F_(0)>S_(0)exp(r T)$, this funded long-spot/short-forward trade has zero initial net cash and positive terminal cash. If $F_(0)<S_(0)exp(r T)$, short and deliver a borrowed spot unit, invest the proceeds, and buy the forward to recover the unit needed for return. This reverse trade has terminal excess $S_(0)exp(r T)-F_(0)$. Thus, if the reverse construction is also feasible, no arbitrage forces

$ F_(0)=S_(0) exp(r T). $

If a known cash dividend $D$ is paid at $t_(D)<T$, investing it until delivery offsets $D exp(r(T-t_(D)))$ of the debt. Thus

$ F_(0)=(S_(0)-D exp(-r t_(D))) exp(r T). $

Known storage payments add to financed carry. For borrow/lend rates $r_(b)>=r_(l)$ and ideal executable spot sides, feasible reverse/carry strategies motivate a band rather than one equality: in the simplest no-dividend, zero-fee case,

$ S_(0)^("bid") exp(r_(l) T)<=F_(0)
  <=S_(0)^("ask") exp(r_(b) T). $

For the upper bound, buy at the spot ask with borrowing rate $r_(b)$ and sell the forward; a forward sale above that financed ask creates a surplus. For the lower bound, short at the spot bid, lend at $r_(l)$, and buy the forward; a forward purchase below the financed bid creates a surplus. The lower bound requires shorting/delivering the asset; remove or alter it when borrow is unavailable. Testing the band places forward bid/ask sides and all fees on the actual arbitrage legs, connecting the theoretical comparison to executable prices and fills.

Physical *convenience yield* describes the service of having inventory available—for production or shortage protection. It is not necessarily a separable cash dividend anyone can buy and sell. Calendar and processing spreads also require matched grade, location, conversion yields, delivery dates, and facilities. A refinery margin calculated from price charts does not replicate owning the refinery's conversion capability.

=== Institutional lessons belong to the mechanism

Anatoli Kuprianov's 1995 Richmond Fed study of Metallgesellschaft examines long-dated supply commitments hedged with shorter-dated contracts and the associated funding/basis issues. The lesson centers on aligning the hedge's *cash calendar* with the obligation's calendar, while leaving the original hedge's merits open to the study's competing interpretations. Management, unwinding, model assumptions, and funding policy can all change the interpretation.

The CFTC's Amaranth settlement concerns attempted natural-gas-price manipulation. The Senate investigation separately examines concentrated positions and their market effects. Together these sources keep conduct, concentration, strategy, and liquidity in view; the margin discussion sits within that broader mechanism. Claims that the spread would eventually have been profitable would need separate evidence.

#principle[
  *Chapter conclusion:* events require located facts and calibrated payoff states; hard relations require executable cash-flow checks; basis and term trades require inventory, conversion, and funding ledgers. Approximate price neutrality is not contractual certainty or interim solvency.
]

*Self-check:* Recalculate the cash-deal threshold when failure value becomes 70. What happens to funding P&L if basis widens by four units? Which forward bound fails without spot borrow? Answers: the threshold is $26/30 approx 0.867$, basis subtracts four units from the matched trade, and the reverse-carry lower bound may no longer be enforceable.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]
- Won Kwon et al. #link("https://arxiv.org/abs/2309.06180")[_Efficient Memory Management for Large Language Model Serving with PagedAttention_]. 2023. Serving-memory and throughput mechanisms, not financial predictive validity.
- Kraken MTF. #link("https://support.mtf.kraken.com/hc/en-us/articles/25499987607837-Linear-Contract-Specifications")[_Linear Contract Specifications_]. Product-specific marking, funding, and margin documentation; checked 11 October 2026.
- U.S. Commodity Futures Trading Commission. #link("https://www.cftc.gov/PressRoom/PressReleases/8938-24")[_CFTC Obtains \$12.7 Billion Judgment Against FTX and Alameda_]. 8 August 2024. Customer-asset and custody failure findings.
- Anatoli Kuprianov. #link("https://www.richmondfed.org/-/media/RichmondFedOrg/publications/research/economic_quarterly/1995/fall/pdf/kuprov.pdf")[_Derivatives Debacles: Case Studies of Large Losses in Derivatives Markets_]. Federal Reserve Bank of Richmond Economic Quarterly 81(4), 1–39, 1995. Metallgesellschaft and the competing interpretations of its hedge/funding failure.
- U.S. Commodity Futures Trading Commission. #link("https://www.cftc.gov/PressRoom/PressReleases/5692-09")[_Amaranth Entities Ordered to Pay a \$7.5 Million Civil Fine_]. 2009. Settlement concerning attempted manipulation, not a certificate of the spread's eventual profitability.
- U.S. Senate Permanent Subcommittee on Investigations. #link("https://www.hsgac.senate.gov/subcommittees/investigations/rep/investigations-subcommittee-releases-levin-coleman-report-on-excessive-speculation-in-the-natural-gas-market/")[_Report on Excessive Speculation in the Natural Gas Market_]. 2007. Concentrated trading and market effects.
]

#pagebreak()

= Replication and Risk-Neutrality: From Cash Flows to Prices
#counter(math.equation).update(0)

The coarse direction target was selected because a trend decision often does not need an exact future price. A derivative desk has a different consumer: a promised payoff must be valued, funded, and hedged. The contract's cash-flow problem makes numerical values and sensitivities necessary, and gives the model a different job from directional forecasting.

We construct pricing from two-state replication, extend it recursively, and use that construction to introduce continuous-time randomness and new probability weights. Throughout, the price belongs to a specified ideal model. Actual quotes also reflect funding, collateral, credit, inventory, frictions, and model uncertainty. “Sell side never predicts” is not a literal description of all institutions.

== Two Equations Replace a Forecast

=== Replicate a one-period call

A *European call* gives its holder the right, at maturity $T$, to receive $max(S_(T)-K,0)$ in our cash-settled teaching convention. $K$ is the strike. Assume stock costs $S_(0)>0$, moves to $u S_(0)$ or $d S_(0)$, with $u>d>0$, and a cash account grows by factor $R>0$. Borrowing, lending, and shorting are allowed at the same rates without costs.

For any payoff pair $(H_(u),H_(d))$, hold $Delta$ shares and current cash $B$, requiring

$ Delta u S_(0)+B R=H_(u), quad
  Delta d S_(0)+B R=H_(d). $

Subtracting cancels cash and determines the share quantity. Substitution determines cash. Specifically, $B R=H_(d)-d S_(0)Delta=H_(d)-d(H_(u)-H_(d))/(u-d)=(u H_(d)-d H_(u))/(u-d)$:

$ Delta=frac(H_(u)-H_(d),S_(0) (u-d)), quad
  B=frac(u H_(d)-d H_(u),R(u-d)). $

These holdings produce the derivative's cash flow in both states. The no-arbitrage price is their current cost $V_(0)=Delta S_(0)+B$. If the derivative costs more, sell it and buy the replicating holdings; if it costs less, reverse the construction. This price comparison requires the same trade and financing permissions as the replication.

For $S_(0)=100$, $u=1.1$, $d=0.9$, $R=1$, and $K=100$, the call pays 10 or 0. Thus $Delta=0.5$, $B=-45$, and $V_(0)=5$. Terminal checks are $0.5 times 110-45=10$ and $0.5 times 90-45=0$. No estimate of how often “up” occurs entered either equation.

=== The pricing probability is forced by the traded prices

Insert the two holdings into $V_(0)=Delta S_(0)+B$ and use the common denominator $R(u-d)$. The numerator is $R(H_(u)-H_(d))+u H_(d)-d H_(u)=(R-d)H_(u)+(u-R)H_(d)$. Dividing its two coefficients by $u-d$ gives $q$ and $1-q$. Rearrange the current replication cost:

$ V_(0)=frac(1,R)[q H_(u)+(1-q)H_(d)],
  quad q=frac(R-d,u-d). $

The condition $d<R<u$ puts $q$ strictly between zero and one. If $R>=u$, short the stock and lend its proceeds: terminal cash is $S_(0) (R-u)$ or $S_(0) (R-d)$, with no initial cost and a positive benefit in at least one state. If $R<=d$, borrowing to buy stock gives the reverse arbitrage. The strict condition therefore expresses the absence of the two stock/cash arbitrages.

Let the real-world up probability be $p=0.7$. The undiscounted average call payoff is 7, yet the replication cost is still 5. A holder buying at 5 bears risk with a physical expected payoff different from the initial price. The pricing weight $q=0.5$ is not a prediction that half of future days rise. It is the weight that makes the stock's discounted expected next value equal its present value:

$ frac(q u S_(0)+(1-q)d S_(0),R)=S_(0). $

Call the physical outcome law $P$ and the replication-induced pricing law $Q$. A probability law, also called a *probability measure*, assigns probabilities to the admissible events; here it assigns weights to tree outcomes. *Risk-neutral* describes this pricing law, not an assertion that actual investors dislike no risk, that premia vanish in the world, or that price paths become deterministic.

== Repeat the Construction at Every Node

For several dates, assume the same two possible moves at each node, known before that next step. At maturity, put the contractual payoff on each node. One step earlier, repeat the two equations using those next-node values as payoffs. Continue backward to today. This is *backward induction*: it computes a current funding cost from future obligations.

In a two-step zero-rate tree with the same $u,d$, terminal stocks are 121, 99, and 81. The strike-100 call pays 21, 0, and 0. Its values one step earlier are 10.5 at stock 110 and 0 at stock 90, so the initial value is 5.25. Initial delta is $(10.5-0)/(110-90)=0.525$; after the up move it changes to $21/(121-99) approx 0.9545$. Replication of this longer claim requires the changing node-specific holdings, as the different delta values show.

A *self-financing* strategy pays for changes in stock holdings from its own cash account, without unexplained external deposits. At a rebalance, buying an additional $delta q$ shares at price $S$ reduces cash by $S delta q$ in this ideal model. This is the missing accounting operation if one simply differentiates the value of a portfolio with changing holdings.

Under $Q$, the discounted value at each node equals its conditional average at the next node. A process with this property is a *martingale*. “Conditional” means using the information at that node, not averaging over a future fact. The tree constructs the property before we name it. A martingale need not have flat sample paths or small risk; its average increment, given current information under the specified law, is zero.

*First pricing engine:* solve the one-step equations, verify both terminal cash flows, then implement this backward recursion and its cash/stock rebalances. For a continuous-time comparison, select $u=exp(sigma sqrt(h))$, $d=exp(-sigma sqrt(h))$, and $R=exp(r h)$ with step $h$. Refine the tree and check value and hedge quantities against a known benchmark. State payoff dates, early-exercise permissions, dividend treatment, and settlement conventions before changing the engine.

== Why Ordinary Calculus Loses a Term

=== Random increments have a different scale

Brownian motion $W_(t)$ is a continuous model process whose nonoverlapping increments are independent, with $W_(t+h)-W_(t)$ Gaussian of mean zero and variance $h$. Its typical increment is proportional to $sqrt(h)$, not $h$. This process is an admitted mathematical model, not a claim that all market increments are Gaussian.

For a partition of $[0,T]$ into $n$ equal pieces, write $Delta W_(j)$ for the independent increments. Then

$ E[sum_(j=1)^(n) (Delta W_(j))^(2)]=T,
  quad Var(sum_(j=1)^(n) (Delta W_(j))^(2))=frac(2T^(2),n). $

One can obtain the fourth moment without importing a new distribution theorem. For standard-normal density $phi$, $phi'(z)=-z phi(z)$. Integration by parts gives $integral z^(4)phi(z)dif z=-integral z^(3)phi'(z)dif z=3 integral z^(2)phi(z)dif z=3$, with the boundary term zero because polynomial growth is dominated by the Gaussian tail. Scaling $X=sqrt(v)Z$ gives $E[X^(4)]=3v^(2)$. Each increment has $v=T/n$; independent squared increments therefore have total variance $n times 2(T/n)^(2)=2T^(2)/n$. The variance uses the Gaussian fourth moment $E[X^(4)]=3v^(2)$ for variance $v$, so $Var(X^(2))=2v^(2)$. As the grid refines, the sum of squared increments converges in mean square to $T$, not zero. This accumulated squared movement is *quadratic variation*. For a smooth deterministic path with bounded derivative, the analogous sum is of order $n h^(2)$ and tends to zero. That is why ordinary calculus's discarded second-order term survives here.

=== Decide Holdings from the Information Available before the Shock

For known-before-step holdings $g_(j)$, define the finite trading gain $sum_(j) g_(j) Delta W_(j)$. If each $g_(j)$ uses only earlier information, independence gives zero expected gain and

$ E[(sum_(j) g_(j) Delta W_(j))^(2)]
  =E[sum_(j) g_(j)^(2) h]. $

To see a cross term, take $i<j$ and let $cal(F)_(j)$ be all information just before increment $j$. Then $g_(i)Delta W_(i)g_(j)$ is already measurable there, while $E[Delta W_(j)|cal(F)_(j)]=0$. The tower rule gives $E[g_(i)Delta W_(i)g_(j)Delta W_(j)]=E[g_(i)Delta W_(i)g_(j)E[Delta W_(j)|cal(F)_(j)]]=0$. For a diagonal term, $E[g_(j)^(2)(Delta W_(j))^(2)]=E[g_(j)^(2)E[(Delta W_(j))^(2)|cal(F)_(j)]]=h E[g_(j)^(2)]$. Cross terms vanish by conditioning on the information before the later shock. This identity supplies a controlled mean-square limit when stepwise holdings approximate a process with finite expected integrated square. That limit defines the *Itô integral*. A weight chosen after observing the same increment would not satisfy the argument and would not describe an admissible trading decision.

Consider the diffusion model

$ dif S=mu S dif t+sigma S dif W,
  quad S>0, quad sigma>0. $

Here the notation is shorthand for an integrated equation, not a ratio of infinitesimal random numbers. On a small step, the random stock movement has leading scale $sigma S sqrt(h)$. Taylor expansion of a smooth $V(t,S)$ keeps $V_(t)h$, $V_(S)Delta S$, and $frac(1,2)V_(S S) (Delta S)^(2)$. The mixed time/stock term has local scale $h sqrt(h)$ and the pure time-square term has scale $h^(2)$; summing over roughly $T/h$ steps makes these vanish under the stated regularity. The stock-square term has leading scale $sigma^(2)S^(2)h$, whose sum survives. The centered fluctuation of these squared increments vanishes in the corresponding mean-square/localization argument. Quadratic variation turns the last term into a drift contribution.

Under continuous diffusion paths, adapted coefficients with the required integrability, and $V$ with one continuous time derivative and two continuous stock derivatives, Itô's formula gives

$ dif V=(V_(t)+mu S V_(S)+frac(1,2)sigma^(2)S^(2)V_(S S))dif t
    +sigma S V_(S)dif W. $

Here localization means first stopping the path when stock, coefficients, or required derivatives leave a chosen bounded region; prove the identity on that stopped interval, then increase the bounds under the stated hypotheses. Bounded derivatives/coefficient conditions after localization justify the Taylor limits; unbounded cases need the corresponding local/integrability hypotheses. The notation $(dif W)^(2)=dif t$ summarizes quadratic variation and is not a literal multiplication rule for all stochastic processes. Jumps require additional terms.

== Self-Financing Replication Removes Drift from the Pricing Equation

A self-financing portfolio of value $H$, holding $Delta$ shares and the remainder in cash, changes by

$ dif H=Delta dif S+r(H-Delta S)dif t. $

To match $H=V$, set $Delta=V_(S)$, equating the random coefficients. The portfolio's drift becomes $mu S V_(S)+r(V-S V_(S))$. The two drift expressions must match: $V_(t)+mu S V_(S)+sigma^(2)S^(2)V_(S S)/2=mu S V_(S)+r V-r S V_(S)$. Subtract $mu S V_(S)$ from both sides and move the remaining right-side terms left. Thus equate it to the drift in Itô's formula and cancel the matching $mu$ term:

$ V_(t)+frac(1,2)sigma^(2)S^(2)V_(S S)
    +r S V_(S)-r V=0,
  quad V(T,S)=max(S-K,0). $

This is the Black–Scholes pricing partial differential equation for the stated no-dividend model. A *partial differential equation* relates a function's derivatives in several variables. Its domain and terminal/boundary conditions complete the pricing problem. For this call, $V(t,0)=0$ and the large-stock behavior approaches $S-K exp(-r(T-t))$.

Physical drift disappears because the same stock exposure is held in the derivative and its replicating portfolio. The ideal replication price can therefore be obtained without estimating the stock's physical expected return. The exposure statement remains specific to the replicated claim: an unhedged call retains directional sensitivity, and real discrete hedges leave residual risk.

== Derive the Closed Form from Two Truncated Expectations

First derive the exponential stock law rather than treating it as a new input. Under the constructed pricing law, $dif S=r S dif t+sigma S dif W^(Q)$. Apply Itô to $f(S)=ln S$, whose derivatives are $f'(S)=1/S$ and $f''(S)=-1/S^(2)$. The drift correction gives $dif ln S=(r-sigma^(2)/2)dif t+sigma dif W^(Q)$. Integrating between the present and maturity gives $ln(S_(T)/S)=(r-sigma^(2)/2)tau+sigma(W_(T)^(Q)-W_(t)^(Q))$. The Brownian increment divided by $sqrt(tau)$ is standard normal by its defining variance. Exponentiating yields the stock law below.

Under $Q$ in this constant-coefficient model, write remaining time $tau=T-t>0$ and

$ S_(T)=S exp((r-frac(1,2)sigma^(2))tau+sigma sqrt(tau) Z),
  quad Z~N(0,1). $

The normal distribution's cumulative probability is $Phi(a)=Pr(Z<=a)$ and its density is $phi(z)=exp(-z^(2)/2)/sqrt(2pi)$. The exercise condition is $Z> -d_(2)$, where

$ d_(2)=frac(ln(S/K)+(r-frac(1,2)sigma^(2))tau,sigma sqrt(tau)),
  quad d_(1)=d_(2)+sigma sqrt(tau). $

Separate the payoff into the stock paid in exercise states minus the strike paid in those states:

$ C=exp(-r tau) E_(Q) [S_(T) 1_(S_(T)>K)]
      -K exp(-r tau) Pr_(Q) (S_(T)>K). $

The second probability is $Phi(d_(2))$ by normal symmetry. For the first expectation, completing the square gives

$ exp(a z)phi(z)=exp(a^(2)/2)phi(z-a). $

Take $a=sigma sqrt(tau)$ and integrate over $z> -d_(2)$. The shifted lower boundary is $-d_(1)$, and

$ exp(-r tau)E_(Q)[S_(T)1_(S_(T)>K)]=S exp(-sigma^(2)tau/2)integral_(-d_(2))^(infinity)exp(a z)phi(z)dif z \ =S integral_(-d_(1))^(infinity)phi(y)dif y=S Phi(d_(1)), quad y=z-a. $

The factor $exp(a^(2)/2)$ from completing the square cancels $exp(-sigma^(2)tau/2)$. Thus the first discounted expectation becomes $S Phi(d_(1))$. Therefore

$ C=S Phi(d_(1))-K exp(-r tau) Phi(d_(2)). $

Weighting the exercise event by stock value explains why the two normal arguments differ. At $S=K=100$, $r=0$, $sigma=0.2$, and $tau=1$, $d_(1)=0.1$, $d_(2)=-0.1$, and $C approx 7.966$. This is a model benchmark, not a market quote.

For the cancellation identity, $d_(1)-d_(2)=sigma sqrt(tau)$ and $(d_(1)^(2)-d_(2)^(2))/2=ln(S/K)+r tau$. Hence $phi(d_(1))/phi(d_(2))=exp(-ln(S/K)-r tau)=K exp(-r tau)/S$. Also $partial_(S)d_(1)=partial_(S)d_(2)=1/(S sigma sqrt(tau))$. Product and chain rules give

$ C_(S)=Phi(d_(1))+S phi(d_(1))frac(1,S sigma sqrt(tau))-K exp(-r tau)phi(d_(2))frac(1,S sigma sqrt(tau)). $

Differentiate with respect to current stock. The identity $S phi(d_(1))=K exp(-r tau)phi(d_(2))$ cancels the derivative-of-probability terms, leaving *delta* $C_(S)=Phi(d_(1))$. Differentiating once more gives *gamma* $C_(S S)=phi(d_(1))/(S sigma sqrt(tau))$. For vega, rate and time are fixed and the two probability-derivative terms reduce, by the same density identity, to $S phi(d_(1))(partial_(sigma)d_(1)-partial_(sigma)d_(2))$. Since $d_(1)-d_(2)=sigma sqrt(tau)$, the derivative difference is $sqrt(tau)$. Differentiation with respect to $sigma$ gives *vega* $C_(sigma)=S phi(d_(1))sqrt(tau)$. These sensitivities describe how the model price responds to specified inputs; model reliability is assessed separately.

== Distinguish Distributional Distance from Predictive Alpha

=== Compute the Gaussian distance first

Under $P$ and $Q$, a length-$h$ log-price increment is Gaussian with common variance $v=sigma^(2)h$ and means $m_(P)=(mu-sigma^(2)/2)h$ and $m_(Q)=(r-sigma^(2)/2)h$. The log density ratio is

$ ln(frac(p(x),q(x)))
  =frac((x-m_(Q))^(2)-(x-m_(P))^(2),2v). $

Averaging under $P$ gives $E_(P) [(X-m_(Q))^(2)]=v+(m_(P)-m_(Q))^(2)$ and $E_(P) [(X-m_(P))^(2)]=v$. Their difference therefore yields *relative entropy*

$ D(P_(h) parallel Q_(h))
  =frac((m_(P)-m_(Q))^(2),2v)
  =frac(1,2)theta^(2)h,
  quad theta=frac(mu-r,sigma). $

The natural logarithm makes the unit nats; divide by $ln(2)$ for bits. Independent increment densities multiply, so their log ratios add. For a full grid covering $T$, the distance is $theta^(2)T/2$. This measures how two specified probability laws differ. It is not $I("past";"future")$, and a positive risk premium is not itself a forecasting signal.

=== Construct the Likelihood Change and Explain the Continuous-Limit Conditions

The finite-step density calculation is

$ frac(1,sqrt(2pi h))exp(-x^(2)/(2h))exp(-theta x-theta^(2)h/2)=frac(1,sqrt(2pi h))exp(-(x+theta h)^(2)/(2h)). $

The right side is a Gaussian density integrating to one, now centered at $-theta h$. For one Brownian increment under $P$, multiplying its density by $exp(-theta Delta W-theta^(2)h/2)$ shifts its mean from zero to $-theta h$ while preserving variance $h$; completion of the square verifies both the shift and total probability one. For a bounded drift adjustment chosen before each step, conditional multiplication repeats the operation without using future increments.

More generally, a nonnegative likelihood weight $Z$ with $E_(P) [Z]=1$ defines a new event law by $Q(A)=E_(P) [Z 1_(A)]$. The notation $dif Q=Z dif P$ summarizes that operation; the weight $Z=dif Q/dif P$ is its *Radon–Nikodym derivative* when the required absolute continuity holds. Absolute continuity means that a $P$-impossible event remains $Q$-impossible. Positive weights also retain the same null events in reverse. This operation changes the probabilities assigned to events while preserving the identity of each realized event.

In the continuous limit, the candidate density is

$ Z_(T)=exp(-integral_(0)^(T) theta_(t)dif W_(t)^(P)
               -frac(1,2)integral_(0)^(T) theta_(t)^(2)dif t). $

The measure-change theorem used here requires a drift adjustment using only current/past information, with the needed square integrability, and that this positive exponential process is a martingale of expectation one. A sufficient condition is $E_(P) [exp(frac(1,2)integral_(0)^(T) theta_(t)^(2)dif t)]<infinity$ (Novikov's condition). Under these hypotheses, defining $dif Q=Z_(T)dif P$ makes $W_(t)^(Q)=W_(t)^(P)+integral_(0)^(t)theta_(s)dif s$ Brownian under $Q$. In detail, $dif W^(P)=dif W^(Q)-theta dif t$, so $dif S=mu S dif t+sigma S(dif W^(Q)-theta dif t)=(mu-sigma theta)S dif t+sigma S dif W^(Q)$. Substitution changes stock drift from $mu$ to $r$ when $theta=(mu-r)/sigma$. Girsanov's change of measure shifts the drift while retaining Brownian randomness under the new law.

If the log likelihood is integrable and the $P$ stochastic integral has zero mean, invert the density and average:

$ D(P parallel Q) &= E_(P) [ln(frac(dif P,dif Q))]
  \ &= E_(P) [integral_(0)^(T)theta_(t)dif W_(t)^(P)
       +frac(1,2)integral_(0)^(T)theta_(t)^(2)dif t]
  \ &= frac(1,2)E_(P) [integral_(0)^(T)theta_(t)^(2)dif t]. $

The finite Gaussian construction and the theorem's hypotheses explain the formula's scope for diffusions. Defaults, jumps, singular measures, and other risk-premium models call for their own measure-change analysis. In this diffusion, $theta$ is excess drift per volatility unit with matching time units; identifying it with any reported empirical Sharpe or with “all alpha information” would change the object.

== What Happens When the Payoff Cannot Be Replicated?

In the two-state model, stock and cash span every payoff pair. In three states, their two adjustable holdings generally cannot match all three obligations. Take stock outcomes 80, 100, 120, $S_(0)=100$, $R=1$, and a strike-100 call paying 0, 0, 20. A line $Delta S+B$ matching endpoint payoffs would pay 10 at stock 100, not zero. Exact replication fails.

Pricing weights with probabilities $(a,1-2a,a)$, $0<a<1/2$, all give the stock a mean of 100, yet call values range over $20a$ in $(0,10)$. No arbitrage alone does not select one of these values in this ideal three-state market. Additional traded instruments, calibration, risk preferences, or a specified residual-hedging criterion can select a price or narrow the range. A stock-price forecasting model would need an explicit connection to such a criterion to serve this pricing role.

#principle[
  *Chapter conclusion:* begin with contract cash flows and replication. In a complete ideal model, replication constructs the pricing weights and removes physical drift from the price equation. When replication fails, identify the unspanned risk and the additional pricing/hedging criterion that selects among possible expectations.
]

*First practical route:* one-step cash-flow fixtures → backward tree and self-financing ledger → European closed-form benchmark → value/delta/gamma refinement → explicit model and contract extensions. Use the same contract and discounting throughout. Tokenized claims and derivatives on futures or equity wrappers need their actual payout, reference, collateral, and settlement definitions before this benchmark can apply.

*Self-check:* Why does changing $p$ from 0.7 to 0.3 not change the two-state replication price? Why does the Itô expansion retain a second derivative? Why can two valid pricing measures give different values in the three-state example? Matched cash flows, nonzero quadratic variation, and the failed spanning equation give the answers, each through the construction developed above.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]
- Fischer Black and Myron Scholes. #link("https://doi.org/10.1086/260062")[_The Pricing of Options and Corporate Liabilities_]. Journal of Political Economy 81(3), 637–654, 1973. The classical replication/pricing setting; the lecture supplies its own teaching derivation.
- Grigorios A. Pavliotis. #link("https://www.ma.imperial.ac.uk/~pavl/PavliotisBook.pdf")[_Stochastic Processes and Applications_], author-hosted text. Brownian motion, stochastic integration, Itô calculus, and measure-change conditions.
]

#pagebreak()

= Volatility and Path Structure: Build the State the Contract and Risk Need
#counter(math.equation).update(0)

Replication in Chapter 15 depends on its model and permitted instruments. This chapter asks what to do when a quote surface, a volatility forecast, or a path-dependent payoff cannot be expressed by that simple state. The selected development order is concrete: begin with a simple scale forecast and a constant-volatility pricing benchmark; identify the remaining discrepancy; augment the necessary state; then compare a richer volatility or path model through its pricing and hedging use.

The stochastic-calculus foundations remain those constructed in Chapter 15. Finite examples and stated theorem hypotheses introduce the advanced results below, showing when a simple running sum suffices and when richer history is useful.

== Mean and Variance Have Different Estimation Problems

=== A finite Gaussian comparison explains the distinction

For independent $R_(i)~N(mu,sigma^(2))$, the sample mean has variance $sigma^(2)/n$. Its standard error is $sigma/sqrt(n)$, so relative error compared with a small nonzero $mu$ is $sigma/(abs(mu)sqrt(n))$. Estimating a tiny drift can be difficult even in a stable ideal model.

To examine variance, use the centered residual sum $sum_(i) (R_(i)-bar(R))^(2)$. Centering is an orthogonal projection removing one direction from an $n$-dimensional Gaussian vector. Write $R=mu bold(1)+sigma Z$, with standard-normal independent coordinates in $Z$, and let $M=I-bold(1)bold(1)^(T)/n$. Then $M bold(1)=0$, $M^(2)=M$, and the centered residual vector is $M R=sigma M Z$. The unit direction $bold(1)/sqrt(n)$ is killed; every vector perpendicular to it is unchanged. Thus $M$ has one eigenvalue zero and $n-1$ eigenvalues one. An orthogonal matrix diagonalizing $M$ preserves the Gaussian density because it preserves squared length and has absolute determinant one. The rotated standard-normal coordinates consequently remain independent. Rotate coordinates so this projection retains $n-1$ independent zero-mean Gaussian coordinates with variance $sigma^(2)$. Each squared coordinate has mean $sigma^(2)$ and variance $2sigma^(4)$, by the fourth-moment calculation in Chapter 15. Hence the unbiased estimator

$ s^(2)=frac(1,n-1)sum_(i=1)^(n) (R_(i)-bar(R))^(2)
  quad "has" quad Var(s^(2))=frac(2sigma^(4),n-1). $

The mean of the residual squared sum is $(n-1)sigma^(2)$; its variance is $(n-1)2sigma^(4)$. Dividing by $(n-1)$ makes the estimator unbiased, and dividing variance by $(n-1)^(2)$ produces the displayed variance. Relative standard error is $sqrt(Var(s^(2)))/sigma^(2)$. Its relative standard error is $sqrt(2/(n-1))$, independent of how small $mu$ is. At $n=252$ and $mu/sigma=0.02$, the mean's relative standard error is about 3.15, while the variance estimator's is about 0.089. This comparison explains why risk scale can be easier to estimate than a weak mean in this specific model. Forecasting future volatility adds a temporal question to this estimation comparison, and regime changes can affect both estimates.

=== Construct a persistence forecast from the required target

For risk sizing, start with a past-only rolling squared-return scale and compare a simple recursion. Write $R_(t)=sigma_(t)epsilon_(t)$, where $epsilon_(t)$ has conditional mean zero and conditional variance one. A nonnegative variance recursion is

$ sigma_(t+1)^(2)=omega+a R_(t)^(2)+b sigma_(t)^(2),
  quad omega>0, quad a,b>=0. $

An unusually large squared return raises the next scale; the $b$ term preserves some previous scale. If a stable finite unconditional second moment exists and $a+b<1$, the conditional unit variance implies $E[R_(t)^(2)]=E[sigma_(t)^(2)]$. Write the common stationary second moment as $v$. Averaging the recursion gives $v=omega+(a+b)v$, so $(1-a-b)v=omega$ and averaging gives $E[sigma^(2)]=omega/(1-a-b)$. This expectation identity is not a full existence theorem for every parameter/noise law. The relevant forecast horizon guides fitting and testing, where the GARCH recursion is compared with its baseline.

For a first comparison, predict the next declared interval's squared-return sum using (i) a twenty-observation past-only average and (ii) a constrained recursion estimated in development. Evaluate scale error and its downstream sizing losses, including stress overshoot. Squared returns are noisy realized targets, not observable future conditional variance. A more stable scale forecast can justify safer size without improving directional accuracy.

*Realized volatility* summarizes an observed path under a sampling convention. *Implied volatility* is the volatility input that makes a chosen pricing formula match an option quote. They are not measurements of the same random variable at the same time.

== A Smile Reveals a Quote-Surface Gap and Guides Model Extensions

In Chapter 15's call formula, vega is positive for positive stock, strike, volatility, and remaining time. Within its feasible quote range, increasing the volatility input increases the price, allowing numerical inversion from price to an implied volatility.

At a single maturity, suppose strikes 90, 100, and 110 imply volatilities 0.25, 0.20, and 0.24. No single constant-volatility value can reproduce all three quotes. This cross-strike pattern is a *smile*; a one-sided slope is often called a skew. First verify executable quote quality and common contract terms. Three prices outside bid/ask or using different settlement conventions are not necessarily a meaningful surface.

Different model extensions address different missing relations:

#table(columns: (1fr, 1.65fr, 1.5fr),
  table.header([Extension], [Added object], [What must be checked]),
  [Local volatility], [A diffusion scale $sigma(t,S)$ depending on time and current stock.], [Surface consistency, calibration stability, and future smile/hedge behavior.],
  [Stochastic volatility], [A separate variance state with its own random shock, possibly correlated with stock.], [Additional risk exposures, calibration, and tradable hedge tools.],
  [Jumps], [Finite discontinuous price moves rather than only continuous diffusion.], [Jump sizes/frequencies, tail risk, and residual hedge losses.],
  [History-dependent scale], [A dependence on past observations not summarized by current stock alone.], [Required memory, identifiable parameters, and computation.],
)

Calibration means choosing model parameters to match a declared set of quotes, using their errors and tolerances. Two models can fit today's surface similarly and disagree about tomorrow's surface changes or an exotic payoff. Surface fit thus leaves a choice among dynamic laws. Compare stable calibration, withheld strikes/maturities, and subsequent hedge outcomes separately.

The first development route is therefore constant-volatility residual audit → a named strike/maturity or risk gap → the smallest extension addressing it → matched surface and hedge evaluation. A visible role for each parameter keeps the extension tied to the gap; quote coverage determines how elaborate a volatility surface can be supported.

== The Hedge Problem Is an Exposure-Spanning Problem

Suppose $k$ independent Brownian shocks drive the local risks. Let $n$ permitted hedge tools have exposure rows collected in $A in RR^(n times k)$, and let the target claim's exposure be $g in RR^(k)$. Hedge quantities $q$ cancel these local shocks only if

$ A^(T)q=g. $

With two independent shocks, one stock with row $(1,0)$ cannot match claim exposure $(0.5,0.3)$. Adding a traded option with row $(0.2,0.6)$ allows quantities solving $q_(1)+0.2q_(2)=0.5$ and $0.6q_(2)=0.3$, so $q_(2)=0.5$, $q_(1)=0.4$. The added tool removes the second local exposure in this model. Its liquidity and cost still matter.

The example makes incompleteness depend on the permitted instrument set: the target exposure has to lie in the available span. Correlation, rank changes, constraints, and ill-conditioning can weaken or prevent the hedge. Local diffusion cancellation also does not guarantee globally identical cash flows under every model error.

For a finite stock jump $J$, delta hedging leaves

$ V(S+J)-V(S)-V_(S)J. $

If $V(S)=S^(2)$, this residual is $J^(2)$ exactly. An infinitesimal slope cancels the linear component of a move, leaving its finite curvature. Local delta hedging therefore leaves jump risk; additional instruments can address a selected set of jump exposures.

Crypto derivatives add discontinuous price/liquidity episodes, different mark/reference observations, and venue-specific collateral rules. A stock-token derivative can have issuer/reference discontinuities that a continuous hedge in the underlying share does not reproduce. Actual tool exposures and availability determine the span, extending the check beyond a resemblance of tickers.

== Volatility Trading Requires Gamma-Weighted Path Accounting

Consider a smooth option priced with model volatility $sigma_(m)$, while its actual continuous stock path has volatility $sigma_(a)$, at the same cash rate $r$. Hold one long option, short its delta $V_(S)$, and finance consistently. The actual expansion is $dif V=V_(S)dif S+[V_(t)+sigma_(a)^(2)S^(2)V_(S S)/2]dif t$. A replicating-financing comparison holds stock $V_(S)$ and cash $V-S V_(S)$, whose self-financing gain is $V_(S)dif S+r(V-S V_(S))dif t$. Subtracting cancels the whole stock increment, including its physical drift and shock; what remains is the displayed financed option excess gain. Thus subtract the hedge and financing contributions from the actual-path Itô expansion:

$ dif Pi=[V_(t)+frac(1,2)sigma_(a)^(2)S^(2)V_(S S)
        -r(V-S V_(S))]dif t. $

The pricing PDE substitutes $V_(t)-r(V-S V_(S))=-sigma_(m)^(2)S^(2)V_(S S)/2$, giving

$ dif Pi=frac(1,2)Gamma S^(2) (sigma_(a)^(2)-sigma_(m)^(2))dif t,
  quad Gamma=V_(S S). $

A positive-gamma long position benefits from greater actual variance than its model-implied scale in this ideal comparison; a short position reverses the sign. The contribution is weighted by the changing $Gamma S^(2)$ along the path, not by an unweighted average of “implied minus realized volatility.” Trading costs, jumps, discrete rebalancing, and surface repricing add residual terms.

For an illustrative interval with $Gamma S^(2)=100$, actual variance 0.09, model variance 0.04, and elapsed time 0.01 years, the local ideal long gain is $0.5 times 100 times 0.05 times 0.01=0.025$ currency units. Rebalancing costs of 0.04 would more than erase it. This is local arithmetic, not a realized strategy result.

*First volatility-trade route:* freeze an option/hedge policy, quotes, and rebalance calendar; record cash, holdings, gamma, actual price path, costs, and margin. Attribute the outcome to the ideal variance contribution plus residuals. Compare with no trade and the same option under a simpler hedge. A positive historical IV–RV average is evaluated alongside path-specific risk, costs, and collateral. A calm short-option history may coexist with severe tail and collateral losses.

== Path Dependence First Asks for Sufficient State

=== An Asian payoff forces a running accumulator

Consider three equally weighted price observations with an arithmetic-average call payoff $max((S_(1)+S_(2)+S_(3))/3-K,0)$. Two histories reaching current price 100 can have previous observations 80, 90 or 110, 120. If the final observation is also 100, their averages are 90 and 110. A strike-100 claim pays 0 or 10. Current price alone cannot distinguish the contract outcomes.

For a discrete contract, retain the running sum and observation count. For a continuous-average contract, define $A_(t)=integral_(0)^(t)S_(u)dif u$, with $dif A_(t)=S_(t)dif t$. Under a Markov stock model, price can now be written $V(t,S,A)$. Ordinary multivariable Itô calculus in the augmented state adds $V_(A)dif A=S V_(A)dif t$ to the drift/PDE. Since the accumulator has finite variation, $(dif A)^(2)$ and $dif A dif S$ do not contribute quadratic variation. The no-dividend augmented pricing equation is $V_(t)+S V_(A)+sigma^(2)S^(2)V_(S S)/2+r S V_(S)-r V=0$, with terminal payoff $max(A/T-K,0)$ for the stated continuous average. The discrete observation contract instead updates its sum/count only at its monitoring dates. One state variable supplies the missing memory directly from the payoff definition.

A barrier contract similarly needs hit status, its monitoring dates, and rebate convention; a lookback needs a running extremum. Equal endpoints but different hit status are different contracts-in-progress. Discrete and continuous monitoring are not interchangeable: a path can cross and return between two observed closes.

=== Whole-path derivatives are operations on histories

When no chosen finite summary is sufficient, write value as a functional $F(t,x)$ of the history $x$ up to $t$. A functional is simply a rule taking a whole function/path as its input rather than one number.

Construct two distinct changes. To advance time without adding a new movement, extend the path flat at its current endpoint; the limiting difference per unit time defines a *horizontal derivative* $D F$. To change only the current endpoint while holding its earlier history fixed, bump it by $epsilon$; limiting first and second differences define *vertical derivatives* $nabla F$ and $nabla^(2)F$.

For $F(t,x)=integral_(0)^(t)x(u)dif u$, flat extension gives $D F=x(t)$, while changing one endpoint of a continuous-time integral gives $nabla F=0$. For $F(t,x)=x(t)^(2)$, flat extension gives $D F=0$ and the endpoint bump gives $nabla F=2x(t)$ and $nabla^(2)F=2$. For the integral functional, a flat extension of duration $h$ adds exactly $h x(t)$, while changing one endpoint does not alter a continuous-time integral: a single point has zero integration length. For the endpoint square, the bump difference is $(x(t)+epsilon)^(2)-x(t)^(2)=2x(t)epsilon+epsilon^(2)$; dividing by $epsilon$ and taking the limit gives the first derivative, and differentiating again gives two. These checks distinguish the operations before using a theorem.

For nonanticipative functionals with the functional time/endpoint regularity, continuity, and local boundedness conditions of functional Itô calculus, and a continuous semimartingale $X$, its theorem has the form

$ dif F=D F dif t+nabla F dif X+frac(1,2)nabla^(2)F dif [X]. $

$[X]$ denotes quadratic variation. A finite-variation path has a finite total absolute movement on each finite interval. A local martingale becomes a martingale after a suitable increasing sequence of stopping rules bounds its problematic excursions. A semimartingale is decomposed into a local martingale component and a finite-variation component; this is the process class for the stated stochastic-integral rule. The functional derivatives are defined on a suitable stopped-path domain allowing endpoint perturbations. Arbitrary discontinuous payoff functionals need additional treatment and need not satisfy this formula directly. The finite examples explain the operations; the cited theorem establishes the extension under its full hypotheses.

*Decision:* implement sufficient accumulators first. Functional calculus becomes useful when the required history operation exceeds that state, with contract monitoring and regularity determining the applicable formula.

== Ordered Integrals Expose What an Endpoint Erases

Take a two-coordinate, piecewise-linear path from $(0,0)$ to $(1,1)$. Path A moves the first coordinate to 1, then the second. Path B moves the second first, then the first. Endpoint increments are $(1,1)$ in both, yet order differs.

For a finite-variation path $X$, define first-level coordinates $S^(i)=integral dif X^(i)$ and second-level coordinates

$ S^(i j)=integral_(u<v)dif X^(i) (u)dif X^(j) (v). $

On A, all first-coordinate movement precedes the second, so $S^(1 2)=1$ and $S^(2 1)=0$. On B those numbers exchange. For a piecewise-linear path with successive increments $a,b$, split pairs of times into: both on the first segment, one on each, or both on the second. On one linear segment, write a unit-time parametrization so the increments are $a^(i)dif u$ and $a^(j)dif v$. The triangle $0<u<v<1$ has area one half, giving $a^(i)a^(j)/2$. Across segments every first-segment time precedes every second-segment time, producing the rectangle contribution $a^(i)b^(j)$. The last triangle contributes $b^(i)b^(j)/2$. Thus splitting the ordered integration regions gives

$ S^(i j)=frac(1,2)a^(i)a^(j)+a^(i)b^(j)
          +frac(1,2)b^(i)b^(j). $

The same construction applies to new two-segment inputs. The ordered integrals at all levels form a *path signature*. At dimension $d$, truncating after level $m$ gives $sum_(k=1)^(m)d^(k)$ nonconstant coordinates: 2+4=6 at $(d,m)=(2,2)$ and 3+9+27=39 at $(3,3)$. Extra order information consumes expression and estimation budget.

For a single finite-variation coordinate, level $k$ equals $(Delta X)^(k)/k!$; it therefore cannot distinguish arbitrary paths with the same total increment. Adding time as a coordinate, $(t,S_(t))$, can expose when movements occurred. Path parametrization, scaling, and missing observation treatment become part of the representation.

Full-signature uniqueness and approximation results require specified path equivalences and regularity/compactness conditions. Finite truncation is not lossless memory. For Brownian and rough paths, a specified stochastic/rough integration convention determines the meaning of these integrals beyond the finite-variation case. For a first empirical representation, explicitly interpolate admitted observations, use time plus only necessary coordinates, start at level two, and compare with the sufficient accumulators and ordinary multiscale summaries. A confirmed order-sensitive increment provides a reason to raise the level.

== Short-Scale Roughness and Long Memory Describe Different Features

An increment scaling law $E[(X_(t+h)-X_(t))^(2)]=c h^(2H)$ describes typical size proportional to $h^(H)$. Brownian motion has $H=1/2$; a smaller positive $H$ makes small-step fluctuations larger relative to Brownian scaling and indicates greater short-scale roughness.

In fractional Brownian motion, the covariance is $E[X_(t)X_(s)]=(t^(2H)+s^(2H)-abs(t-s)^(2H))/2$ in unit normalization. Expanding four covariances for two unit increments separated by integer lag $k>=1$ gives

$ Cov(X_(1)-X_(0),X_(k+1)-X_(k))
  =frac(1,2)[(k+1)^(2H)-2k^(2H)+(k-1)^(2H)]. $

For $H<1/2$, the function $x^(2H)$ is concave, so the second difference is negative. To expose the asymptotic step, put $f(x)=x^(2H)$. For exponents strictly between zero and one and large positive lag, Taylor expansions are $f(k+1)=f(k)+f'(k)+f''(k)/2+f'''(k)/6+O(k^(2H-4))$ and $f(k-1)=f(k)-f'(k)+f''(k)/2-f'''(k)/6+O(k^(2H-4))$. In $f(k+1)-2f(k)+f(k-1)$, constant and odd-derivative terms cancel; the result is $f(k+1)-2f(k)+f(k-1)=f''(k)+O(k^(2H-4))=2H(2H-1)k^(2H-2)+O(k^(2H-4))$. After the covariance's one-half factor, for large $k$, Taylor expansion gives approximately $H(2H-1)k^(2H-2)$. The exponent is below −1, making the absolute tail summable: a positive power tail with exponent below minus one has a finite integral from one to infinity, so the integral comparison also bounds its discrete sum. For exponents above minus one, that integral diverges, and the corresponding positive power tail is not summable. In this model, rough anti-correlated increments are not positive long-range dependence. For $H>1/2$, the sign is positive and the power tail is nonsummable.

Gatheral, Jaisson, and Rosenbaum's empirical work motivates rough volatility models from studied volatility data; its fitted exponents describe the studied data and call for estimation in a new market. History-driven volatility may break a simple finite-dimensional Markov PDE, but it does not make simulation impossible. A covariance-based Gaussian simulator, convolution discretization, or approximate multi-factor state can still provide a declared numerical route, each with cost and approximation error.

#principle[
  *Chapter conclusion:* preserve necessary contract state and distinguish scale prediction, surface calibration, local hedging, and path representation. Begin with sufficient accumulators and simple scale dynamics. A demonstrated pricing or risk gap motivates adding volatility, jump, signature, or rough structure; evaluation then follows the full pricing or risk use.
]

*Self-check:* Which extra state distinguishes the two Asian histories? Can an accurate endpoint-only predictor distinguish the two ordered paths? Does $H=0.1$ imply positive long memory in fractional Brownian increments? Answers: running sum/count, no, and no—the computed second difference is negative with a summable tail.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]
- Rama Cont and David-Antoine Fournié. #link("https://arxiv.org/abs/1002.2446")[_Functional Itô Calculus and Stochastic Integral Representation of Martingales_]. 2010 preprint; Annals of Probability 41(1), 109–133, 2013. Functional derivative definitions and regularity conditions.
- Ilya Chevyrev and Andrey Kormilitzin. #link("https://arxiv.org/abs/1603.03788")[_A Primer on the Signature Method in Machine Learning_]. 2016; expanded version 2025. Ordered integrals, path representations, and bounded theoretical guarantees.
- Jim Gatheral, Thibault Jaisson, and Mathieu Rosenbaum. #link("https://arxiv.org/abs/1410.3394")[_Volatility Is Rough_]. 2014 preprint; Quantitative Finance 18(6), 933–949, 2018. Empirical motivation and the rough-volatility distinction.
- Grigorios A. Pavliotis. #link("https://www.ma.imperial.ac.uk/~pavl/PavliotisBook.pdf")[_Stochastic Processes and Applications_]. Process and stochastic-calculus foundations.
]

#pagebreak()

= Computation: From a Numerical Oracle to Learned Pricing and Hedging
#counter(math.equation).update(0)

Forecasting an uncertain market outcome and approximating a fixed pricing computation are different learning problems. A model can be too large for the first and useful for the second. The target and its use determine which model is appropriate, so the same design principles can lead to a restrained forecaster or a useful deep approximation.

This final chapter gives a complete numerical-development route: construct a checked reference method, budget its errors, choose representation and derivative orders, train a modest surrogate, test values and risk separately, and use explicit fallback. It then constructs a friction-aware hedge policy. No surrogate training, market backtest, or performance reproduction is asserted by these teaching designs.

== A Fixed Pricing Map Is Deterministic, Its Labels Need Not Be Exact

Fix a model, parameters, contract, discounting, and current state $x$. The model price is $V(x)$, a deterministic numerical target. Different Monte Carlo seeds approximate the same target rather than predict different future market prices. The future payoff remains random, the parameters can be uncertain, and the model can be wrong.

A *surrogate* is a cheaper function $hat(V)(x)$ approximating this map over a declared domain. Its value lies in replacing repeated expensive computation within a tolerance. Exact determinacy defines that computational target; smoothness, coverage, and numerical accuracy remain to be established. A ratio of continuous differential entropies would not provide a valid learnability shortcut.

First ask whether the map needs a surrogate at all. Use a closed form where it covers the task, backward trees for suitable exercise/state problems, and a PDE/grid method for manageable state dimension. Use Monte Carlo for appropriate high-dimensional/path computations with explicit observation and exercise rules. An American contract adds optimal-exercise computation to the simulation, whereas averaging terminal European payoffs addresses a different contract.

The Black–Scholes call provides an excellent diagnostic benchmark because its closed form is cheap and available for comparison. After validating the machinery there, assess the benefit of a neural replacement on the actual costly product/domain.

== Budget Monte Carlo Error across Sampling and Discretization

=== Derive sampling precision

Let $Z_(j)$ be independent discounted model payoffs of finite variance $v$ and common mean $V$. Their average satisfies

$ hat(V)_(N)=frac(1,N)sum_(j=1)^(N)Z_(j),
  quad E[hat(V)_(N)]=V,
  quad Var(hat(V)_(N))=frac(v,N). $

Cross covariances vanish by independence. The standard error is $sqrt(v/N)$, so reducing it tenfold at fixed payoff variance requires a hundredfold path count. This is the ordinary independent Monte Carlo rate, not a lower bound on all integration methods.

For a normal-approximation confidence half-width $epsilon$, a pilot variance $hat(v)$ and multiplier $z$ suggest

$ N approx frac(z^(2)hat(v),epsilon^(2)). $

If payoff standard deviation is 12 currency units, $epsilon=0.05$, and $z=1.96$, the suggestion is about 221,277 paths. Retain the pilot's uncertainty and check approximation adequacy for rare/heavy-tail payoffs. A prespecified final count preserves the ordinary fixed-sample interval's interpretation. A rule that repeatedly inspects the width and stops when it looks small needs a suitable sequential guarantee.

=== Separate time bias from sampling noise

Let a discretized path scheme with step $h$ have mean price $V_(h)$ and payoff variance $v_(h)$. Expanding around that mean gives

$ E[(hat(V)_(N,h)-V)^(2)]
  =(V_(h)-V)^(2)+frac(v_(h),N). $

Write $hat(V)_(N,h)-V=(hat(V)_(N,h)-V_(h))+(V_(h)-V)$. On squaring and taking expectations, the mixed term is zero because $E[hat(V)_(N,h)-V_(h)]=0$; the first squared random term is the sample-mean variance $v_(h)/N$. The first term is squared discretization bias; the second is sampling variance. Increasing the path count reduces sampling variance; grid refinement addresses discretization bias. Market-model discrepancy is assessed separately from both numerical errors. Run a grid-refinement comparison with sampling uncertainty small enough to reveal the bias, while preserving the contract's *actual* monitoring grid. Replacing a discretely monitored barrier by a continuous barrier changes the contract, not merely numerical precision.

For constant-coefficient geometric Brownian motion and a European terminal payoff, Chapter 15 gives an exact terminal sampler:

$ S_(T)=S_(0)exp((r-sigma^(2)/2)T+sigma sqrt(T) Z). $

One normal draw per path supplies the exact terminal value, avoiding 250 time steps. For an Asian payoff, sample the actual observation dates and retain the sum. For a continuously monitored barrier, missing crossings between grid points requires a justified crossing correction or refinement. History-dependent volatility can also be simulated with a specified method and an account of its approximation.

=== Reduce variance before multiplying work

Suppose a correlated control $C$ has known mean $m_(C)$. The adjusted payoff $Z-b(C-m_(C))$ has the same mean for fixed $b$ and variance

$ Var(Z)-2b Cov(Z,C)+b^(2)Var(C). $

To expand the variance, center $Z$ and $C$ around their means and square the difference. The cross term is $-2b Cov(Z,C)$. Differentiating the resulting quadratic gives $-2Cov(Z,C)+2b Var(C)=0$. Differentiating in $b$ gives $b^*=Cov(Z,C)/Var(C)$ when $Var(C)>0$, with reduced variance

$ Var(Z)-frac(Cov(Z,C)^(2),Var(C)). $

For a no-dividend risk-neutral simulation, discounted terminal stock has known mean $S_(0)$ and can serve as a control for a call. Estimate $b$ on a separate pilot, freeze it, and evaluate independent main paths. Fitting $b$ on the same small sample changes finite-sample properties, so the fitted procedure's bias is assessed in its own right.

Paired draws $Z$ and $-Z$ are *antithetic*: they can lower variance when corresponding payoffs covary negatively. If the two payoff members have common variance $v$ and correlation $rho$, one pair average has variance $(v+v+2rho v)/4=v(1+rho)/2$. With $M$ independently generated pairs, the average variance is $v(1+rho)/(2M)$, compared with $v/(2M)$ for the same number of independent unpaired evaluations. Negative $rho$ is the gain; positive $rho$ is not. The independent units are the pair averages, not twice as many independent paths. Common random numbers can reduce the noise of differences between nearby inputs. These methods exploit structure in the numerical problem to improve precision on the same model target.

== Choose a Representation That Supports the Required Derivatives

=== Remove a redundant scale when the contract permits it

For a homogeneous model/payoff, scaling stock and strike by $a>0$ scales the payoff and price by $a$. Thus $V(a S,a K)=a V(S,K)$ and choosing $a=1/K$ gives

$ V(S,K,tau,dots.h)=K f(S/K,tau,dots.h). $

Moneyness $S/K$ is a dimensionless price-to-strike ratio. At fixed $K$, delta is $f_(s)$ and gamma is $f_(s s)/K$, with $s=S/K$. Explicitly, $partial_(S)[K f(S/K)]=K f_(s)/K=f_(s)$ and $partial_(S)^(2)[K f(S/K)]=f_(s s)/K$. This chain rule converts normalized-unit training derivatives to physical-unit Greeks. Fixed cash costs, fixed rebates, and nonhomogeneous contract features can invalidate the reduction.

Begin with a declared domain—for example $S/K in [0.7,1.3]$, $tau in [0.02,2]$ years, $sigma in [0.05,0.8]$, and $r in [-0.02,0.1]$ for a call benchmark. These are illustrative coverage choices, not market-wide bounds. Sample interior points, faces/corners, near-strike short maturities, and the economically important stress regions separately. The exact maturity payoff at $tau=0$ has a kink; evaluate it by its terminal rule rather than pretending a globally smooth network has classical gamma there.

A holdout point near training points checks interpolation. A held-out subregion, boundary strip, or distinct path state checks a different extrapolation/coverage claim. Report each. The final input gate routes contracts or states outside the confirmed domain away from surrogate use.

=== Small value errors can hide arbitrarily large Greek errors

Construct $hat(V)(x)=V(x)+epsilon sin(k x)$. The value error is at most $epsilon$, yet derivative errors have amplitudes $epsilon k$ and $epsilon k^(2)$ at first and second order. Taking large $k$ makes price plots look excellent while hedge quantities become wrong.

A piecewise-linear ReLU network also has zero classical second derivative inside each linear region. It may approximate a convex price in values while supplying zero gamma almost everywhere. When gamma is needed, a twice-differentiable representation makes it computable and explicit gamma tests assess its accuracy.

For price labels $V$ and Greek labels $g_(j)$, one justified training comparison is

$ J=E[((hat(V)-V)/s_(V))^(2)
      +sum_(j)lambda_(j) ((partial_(j)hat(V)-g_(j))/s_(j))^(2)]. $

The positive scales $s_(V),s_(j)$ convert heterogeneous units into comparable errors. Choose them from operational tolerances or an explicitly declared normalization, and select the nonnegative weights on development comparisons. If gamma is required, add a second-derivative term or a separate gamma acceptance gate. The word *Sobolev* refers to function spaces controlling functions and derivatives; here derivative supervision matches known slopes, unlike merely penalizing all slopes toward zero. Huge and Savine's differential-learning work provides an established value-and-derivative route whose performance is assessed on the particular label set.

Automatic differentiation supplies derivatives of the implemented function. Cash-flow and label checks connect that function and its derivatives to the intended contract. For a constant-volatility call, differentiate an individual discounted payoff path with respect to initial stock to obtain, outside the probability-zero exercise boundary,

$ g_(Delta)=exp(-r T)1_(S_(T)>K)frac(S_(T),S_(0)). $

For each draw write $S_(T)=S_(0)M$ with random multiplier $M>0$ independent of the input $S_(0)$. The discounted payoff is $exp(-r T)max(S_(0)M-K,0)$. Away from its kink, its derivative is $exp(-r T)M 1_(S_(0)M>K)$, giving the displayed label. The difference quotient is bounded by $exp(-r T)M$; this multiplier has finite expectation in the admitted lognormal model. That integrable domination and the probability-zero kink justify the first derivative passing through expectation. Under valid differentiation-under-expectation conditions, its average estimates delta. Differentiating that indicator naively again produces zero almost everywhere and misses the exercise-boundary contribution to gamma. The contradiction is concrete: the naive per-path second derivative is zero except at one threshold, whereas the analytic gamma from Chapter 15 is positive. As $S_(0)$ changes, new paths cross their exercise thresholds; their total boundary contribution survives averaging even though each fixed path is locally linear. Difference quotients of the indicator become arbitrarily large near a shrinking boundary interval, so the same integrable domination is not available. The second derivative cannot be interchanged with expectation by the same pathwise argument. Use analytic benchmark Greeks, a justified sensitivity estimator, or matched finite differences with step/error assessment instead.

Central price differences approximate delta by $(V(S+h)-V(S-h))/(2h)$ and gamma by $(V(S+h)-2V(S)+V(S-h))/h^(2)$. Taylor expansion around $S$ gives central delta $V_(S)+h^(2)V_(S S S)/6+O(h^(4))$ and central gamma $V_(S S)+h^(2)V_(S S S S)/12+O(h^(4))$ when the corresponding derivatives and remainder bounds exist locally. If independent price estimates each have variance $v/N$, central-delta noise variance is $v/(2N h^(2))$ and central-gamma noise variance is $6v/(N h^(4))$, because the squared coefficients are respectively $1+1$ and $1+4+1$. With smoothness, truncation shrinks as $h^(2)$; independent Monte Carlo noise is amplified by dividing by $h$ or $h^(2)$. Common random numbers help differences but do not certify their bias. Test several steps and independent replications before admitting derivative labels.

== The Equation, Boundary, and Shape Are Separate Constraints

For the no-dividend call benchmark, define the pricing residual

$ R_(hat(V))=hat(V)_(t)+frac(1,2)sigma^(2)S^(2)hat(V)_(S S)
               +r S hat(V)_(S)-r hat(V). $

A physics-informed training comparison can add normalized squared residuals, terminal-payoff errors, and boundary errors to the supervised value/Greek loss. Each component has its own domain, units, sample coverage, and weight. The zero function has zero residual for this homogeneous PDE but fails the call's positive terminal payoffs. A small equation residual alone is not a price solution.

No-arbitrage shape follows from cash flows as well. At fixed maturity, $max(S_(T)-K,0)$ is decreasing and convex in strike $K$. A positive discounted expectation preserves those inequalities. For a no-dividend call with deterministic rate and admissible replication,

$ max(S-K exp(-r tau),0)<=C<=S. $

The upper bound follows because the call payoff never exceeds the stock payoff; the lower bound follows from zero and stock-minus-discounted-strike comparisons. Its stock sensitivity is nonnegative under the benchmark. Strike convexity means the middle-strike price cannot exceed linear interpolation of the surrounding strike prices under matching contracts. These are cross-contract tests, not just a constraint on one output.

Positive activation cannot establish them. For example, $ln(1+exp(-S))$ is strictly positive but decreases with stock. It also cannot equal a zero boundary exactly. Likewise, “more maturity means higher price” needs the matching dividend/rate/exercise assumptions; it is not a universal constraint on all contracts.

Start with reliable supervised labels and explicit value/Greek/boundary/shape gates. A named numerical role motivates adding PDE residual training, followed by evaluation of its increment. Finite-grid penalties can find violations on their grid but do not prove global no-arbitrage. A structural parameterization can enforce some inequalities; identify which and assess what flexibility it removes.

== Assign Optimizers and Explanations Their Actual Jobs

Gradient clipping bounds a parameter-update gradient, not sensitivity to an input. For a network made of affine matrices $W_(j)$ and activations with Lipschitz constants $L_(j)$, repeated composition gives the input-sensitivity bound

$ norm(hat(V)(x)-hat(V)(y))
  <=(product_(j)L_(j)norm(W_(j))_("op"))norm(x-y). $

The operator norm is each matrix's largest stretch, introduced in Chapter 6. The bound concerns actual weights and activation slopes. Its tightness and physical-unit interpretation depend on input/output scaling. Gradient clipping supplies neither these weight bounds nor accurate Greeks.

Muon transforms matrix updates using an approximate orthogonalization operation. Applying an orthogonalized update $U$ as $W_("new")=W-eta U$ does not make $W_("new")$ orthogonal: multiplying its transpose by itself leaves $W^(T)W-eta(W^(T)U+U^(T)W)+eta^(2)U^(T)U$, not generally the identity. Optimizer geometry and function constraints are different operations. Chapter 7's step/noise reasoning and a validation comparison with a fixed budget assess the optimizer's fitting behavior; smoothness and no-arbitrage properties receive their own function-level checks.

An interpretable latent label or language explanation is also a hypothesis. Test an alleged “moneyness feature” by controlled input perturbation, ablation, Greeks, and contract constraints. Sparse bottlenecks can erase weak distributed risk contributions, as Chapter 5's shrinkage example warned. Explain the numerical construction and failure domains, and evaluate an explanatory label alongside independent model validation.

== A Concrete Surrogate Pilot and Its Adoption Gate

The following initial design makes the development order reproducible; training and evaluation remain to be carried out:

1. *Fix the valuation task.* State model/contract version, domain, price/delta/gamma tolerances, units, and fallback. Establish the closed-form/tree/grid reference and cash-flow fixtures first.
2. *Budget reference errors.* Separate sampling, time/observation discretization, and derivative-label error. For a teaching price tolerance of 0.01 currency units, allocate smaller declared budgets to the reference and approximation so reference noise cannot consume the entire allowance. Verify the allocation at stress points as well as in average errors.
3. *Build a bounded dataset.* As an initial workload, use 20,000 domain inputs for training, 2,000 development inputs, and 2,000 final inputs, with separately named boundary/stress suites. Measured coverage/error guides subsequent changes in these counts. Labels are from the same admitted model; paired noisy labels retain their standard errors and path lineage.
4. *Use a small smooth model.* Begin with two hidden layers of width 64 and tanh activations, normalized inputs, and a linear output for normalized price. Apply homogeneity only where justified. Use value/delta supervision, gamma supervision or a gamma gate, and separate shape checks. A linear output leaves positivity to the constraint checks; failed checks trigger rejection/fallback.
5. *Bound numerical fitting.* Begin with the declared Adam comparison at learning rate $10^(-3)$, batch 256, and a 200-epoch cap with development early stopping. These values are pilot settings, not information-theoretic optima. If fitting is unstable, distinguish step scale, noisy labels, bad units, and missing representation before widening the model. Freeze loss weights and stopping before final evaluation.
6. *Evaluate each consumer.* Report physical-unit errors by domain region, Greek order, boundary/shape violation, coverage, and matched hedge outcome. A small mean price error cannot pass a failed short-maturity gamma gate. Outside-domain requests or failed gates use the reference method.
7. *Assess adoption through complete-route gain.* Include oracle generation, training, refresh, validation, inference, and fallback costs. Preserve reproducibility and a tested fallback under model/input changes.

The required value, risk, and constraint tolerances define where the surrogate can replace the reference computation. When a simpler engine is already cheaper at those tolerances, it remains the appropriate choice.

=== Amortization determines whether speed pays

Let offline generation/training/maintenance cost be $C_(o)$, reference cost per request $C_(r)$, and checked surrogate cost per request $C_(s)<C_(r)$. For $N$ calls, adoption saves work when

$ C_(o)+N C_(s)<N C_(r),
  quad N>frac(C_(o),C_(r)-C_(s)). $

At illustrative costs $C_(o)=10,000$ seconds, $C_(r)=0.02$ seconds, and $C_(s)=0.0001$ seconds, the crossover is about 502,513 calls. If fraction $rho$ of requests requires the reference in addition to attempted surrogate inference, effective online cost is $C_(s)+rho C_(r)$; substitute it into the inequality. New model calibrations can require refresh and move the crossover again.

Throughput in a large batch is not latency of one request: overlapping many computations and dividing elapsed batch time by count does not tell a user how long one request waited. Benchmark identical hardware/resource budgets, products, coverage, error tolerances, and batch conditions. The supplied author's Thales account motivates these design questions, but an accessible, matched model card and reproducible benchmark are needed before adopting its claimed rates or universal superiority. That evidence remains open in the material considered here.

== Friction-Aware Hedging: Learn a Policy from Its Ledger and Risk

=== Construct terminal loss from the ledger

Suppose a desk sells a claim paying $H$ at $T$, receives initial capital $v_(0)$, and holds $q_(k)$ hedge units between dates $t_(k)$ and $t_(k+1)$. Let tildes denote quantities discounted to time zero by the declared cash account. A self-financing discounted terminal surplus is

$ E_(T)=v_(0)+sum_(k=0)^(m-1)q_(k) (tilde(S)_(k+1)-tilde(S)_(k))
              -C(q)-tilde(H). $

For proportional transaction cost rate $c$, one simple discounted cost is $C(q)=sum_(k)c tilde(S)_(k)abs(q_(k)-q_(k-1))$, with $q_(-1)=0$; state whether terminal liquidation is required and add it consistently. Chapter 11's ledger supplies the matching holding, financing, and settlement conventions.

Every $q_(k)$ uses only current/past information. Previous holdings belong to state because changing from 0.8 to 0.9 shares and from 0 to 0.9 incurs different cost. Contract state—running sum, hit status, remaining life—and feasible cash/margin also belong when relevant. A neural policy maps that admitted state to permitted quantities; quantity/exposure bounds remain independent controls.

Variance of terminal surplus alone ignores its mean: two policies can have the same variance but different systematic losses. Fix the premium and expected-outcome convention, or use a loss criterion that accounts for the needed downside. Neither the convexity of a risk measure nor a low training loss makes neural-policy optimization convex.

=== Construct a tail-sensitive objective

Let loss be $L=-E_(T)$ and let $alpha in (0,1)$ be a chosen tail level. For any threshold $z$, the quantity

$ z+frac(E[max(L-z,0)],1-alpha) $

charges the threshold plus scaled loss beyond it. For fixed $L$ away from $L=z$, increasing $z$ decreases $max(L-z,0)$ at slope one when $L>z$ and leaves it unchanged when $L<z$. This derivative is bounded by one, so differentiation can pass through expectation. For a continuous loss law, differentiation with respect to $z$ gives $1-Pr(L>z)/(1-alpha)$. A minimizing $z$ is therefore an $alpha$-quantile. At an atom the right derivative is $1-Pr(L>z)/(1-alpha)$, while the left derivative is $1-Pr(L>=z)/(1-alpha)$. A convex one-variable function is minimized when its left derivative is nonpositive and its right derivative nonnegative. At atoms, use left/right derivatives: $Pr(L>z)<=1-alpha<=Pr(L>=z)$. The minimum is *conditional value at risk* (CVaR), also called expected shortfall under the matching tail convention:

$ "CVaR"_(alpha) (L)=min_(z) [z+frac(E[max(L-z,0)],1-alpha)]. $

For a continuous law and a minimizing quantile with exactly $Pr(L>z)=1-alpha$, expand $E[(L-z)1_(L>z)]=E[L 1_(L>z)]-z(1-alpha)$. The $z$ terms cancel and the objective becomes the mean of the upper $(1-alpha)$ tail. For an atom, the threshold construction allocates the needed fraction of the threshold mass rather than including an oversized tail. With loss zero in 95% of cases and 20 in 5%, the objective equals $z+0.05(20-z)/0.05=20$ for every $z$ in $[0,20]$, so CVaR at 0.95 is 20. A constant loss of 1 also has mean 1, but CVaR is 1. The criterion distinguishes the rare severe tail from a uniform loss; it does not certify that a finite simulator contains every possible tail event.

If an extra premium $p$ shifts loss to $L-p$, put $y=z+p$ so $max(L-p-z,0)=max(L-y,0)$ and $z=y-p$. The objective is $y+E[max(L-y,0)]/(1-alpha)-p$, whose minimized value is the old CVaR minus $p$. This is the algebra behind the statement that substitution $z'=z+p$ shows $"CVaR"(L-p)="CVaR"(L)-p$. To define a risk-based indifference premium, compare optimized risk *with* the short claim to optimized risk *without* it on the same permitted market. If these are $R_(H)$ and $R_(0)$ before the extra premium, $p=R_(H)-R_(0)$ equalizes this criterion. It is a price under stated risk preferences and constraints, not automatically Chapter 15's unique replication price.

=== Use Discrete Delta as the First Hedge Comparison

Use the same initial premium, instruments, information, simulation law, trade dates, and costs for (i) no hedge, (ii) model delta at those discrete dates, (iii) a small friction-aware policy. A useful baseline also retains a prespecified no-trade band around the desired hedge to avoid tiny costly adjustments; its band is a development parameter, not evidence of optimality.

For a teaching policy, start with a two-layer width-32 smooth network consuming current normalized stock, time left, volatility/contract state, and previous holding. Clip/project the output into stated hedge limits. Train on complete development paths with costs and the selected terminal-loss objective, initially $alpha=0.95$ for CVaR. A minibatch of 256 paths has only about 13 observations in a 5% tail on average; check tail-estimation stability so the comparison can distinguish reliable improvement from noisy tail gradients. Reuse Chapter 7's bounded rate comparison and early stopping, then freeze the policy before final paths.

Simulate valuation under the admitted pricing law $Q$ where appropriate. Simulate risk under a declared physical law $P$ or stated stress/scenario law when that is the consumer. They need not coincide. Hold the policy fixed for stressed volatility, jumps, wider spreads, delayed rehedges, collateral impairment, and missing hedge availability. A policy that gains only by changing the premium or using future path state is not a better hedge.

The original deep-hedging work demonstrates a friction-aware learning framework with synthetic-market experiments. The transferable practice is to optimize an admissible policy for a stated risk and compare the complete hedging route. Its synthetic results address the stated settings; global optimization, market-model validity, and performance under other constraints remain separate questions. Adoption rests on independently supported residual-risk/net-cost improvement, tail coverage, and funding survival.

#principle[
  *Chapter conclusion:* computation learning is legitimate when it replaces a fixed expensive map within checked value/derivative/constraint tolerances; policy learning is legitimate when it improves a stated feasible hedging objective on complete held-out paths. Held-out value, risk, and full-route checks establish the role of numerical gradients, fast inference, and training loss in those claims.
]

== Closing the Book: Choose the Smallest Complete Problem That Pays Its Own Evidence Cost

The book's two lines now meet. Directional research retains the precision its action needs, represents state available at the time, and confirms a small predictive increment before spending more capacity. In allocation, remove unsupported mean bets and construct risk coverage. In strict replication, retain enough cash-flow structure to avoid forecasting altogether. In statistical/event arbitrage, forecast the actual uncertain completion and finance the route. In pricing and hedging, numerical values, derivatives, and path state are indispensable rather than unwanted detail.

#table(columns: (1.05fr, 1.45fr, 1.55fr),
  table.header([Consumer], [First selected construction], [Evidence required to upgrade]),
  [Directional trade], [Policy-aligned coarse probabilities, small explicit features, payoff-derived participation.], [A remaining representation gap and independent net increment.],
  [Relative stock selection], [Feasible future rank, same-date context, constrained benchmark-relative holdings.], [Useful cross-asset relations beyond the simple context baselines.],
  [Multi-asset allocation], [Economic exposure coverage and stabilized risk budgets.], [A confirmed tilt increment that preserves funding and risk limits.],
  [Arbitrage], [Executable replication, or a stateful calibrated convergence/event policy.], [Correct cash flows, completion, costs, and path survival.],
  [Numerical valuation], [Checked oracle, tolerance-aware labels, smooth surrogate only when needed.], [Value/Greek/constraint coverage and lifecycle cost advantage.],
  [Friction-aware hedge], [Discrete delta and cost-aware control, then a bounded stateful policy.], [Matched complete-path downside and cost improvement.],
)

The practical order is *define the economic decision → choose only necessary distinctions → preserve what was available → construct the relevant state and operations → measure and separate errors → admit upgrades on independent comparisons → carry the result through holdings, cash, and failure paths*. Capacity is spent where this route exposes a genuine missing relation.

The early chapters' decisive default remains: do not reconstruct future-price decimals when the directional action only needs a probability. The later chapters show its precise boundary: do reconstruct cash amounts and derivatives when contracts and hedges consume them. Decision sufficiency explains both choices: the target retains the distinctions its use requires. Numerical feedback helps an optimizer solve a stated problem; it cannot create absent market information. Structure can remove a need to predict; it cannot guarantee that institutions, custody, or financing will honor the assumed structure.

These seventeen chapters complete the methodological lecture. Their constructed examples and pilot settings provide inspectable first experiments, not certified profitable strategies. A later empirical companion would need admitted historical data, contract/rule versions, a frozen research protocol, and independently checked results. A later skill should preserve the reasoning and failure boundaries, with these teaching thresholds and machine-specific tools kept in their illustrative scope.

*Final self-check:* A price surrogate passes average value error but fails gamma near maturity: what happens? A binary model has 60% accuracy but loses after asymmetric payoffs: what changes? A neutral basis trade cannot move collateral in time: is it safe? Answers: use the reference where its risk gate fails; repair participation/payoff calibration rather than request exact-price digits; and no—its funding path must be changed or the opportunity rejected.

#block(breakable: true)[
#set text(size: 9pt)
#set par(leading: 0.5em, spacing: 0.35em)
#heading(level: 2, numbering: none)[References and Further Reading]
- Brian Huge and Antoine Savine. #link("https://arxiv.org/abs/2005.02347")[_Differential Machine Learning_]. 2020, version 4. Value-and-derivative supervised approximation and reference implementations.
- Maziar Raissi, Paris Perdikaris, and George Em Karniadakis. #link("https://arxiv.org/abs/1711.10561")[_Physics Informed Deep Learning (Part I)_]. 2017. PDE-informed approximation; a pricing application still needs its own terminal, boundary, and numerical contract.
- Hans Bühler, Lukas Gonon, Josef Teichmann, and Ben Wood. #link("https://arxiv.org/abs/1802.03042")[_Deep Hedging_]. 2018 preprint. Friction-aware risk optimization; numerical demonstrations are scoped to their stated synthetic settings.
- R. Tyrrell Rockafellar and Stanislav Uryasev. #link("https://doi.org/10.21314/JOR.2000.038")[_Optimization of Conditional Value-at-Risk_]. Journal of Risk 2(3), 21–41, 2000. Tail-risk threshold construction.
- Keller Jordan and contributors. #link("https://github.com/KellerJordan/Muon")[_Muon_], reference implementation. Update geometry is distinct from weight constraints and function-level guarantees.
]
