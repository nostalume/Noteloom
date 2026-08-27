#import "../lib.typ": *

#show: mine.with(
  title: "Review of Electronic Tech",
  eq-numbering: "(1.1)",
  eq-chapterwise: true,
)

#let non(content) = $overline(content)$
#let xor = $plus.o$
#let nxor = $dot.o$

= Analog

== BJT

The _Bipolar Junction Transistor_, with NPN structure, is n: emitter, p: base, n: collector. But there concentration level is different, which is from high to small. Thus it can't be interchanged. That's when base and emitter has a slightly positive voltage greater than threshold, the current, by charge carriers from emitter where they are minority carrier(form n to p) diffuse into collector. It means the base must be thin enough less than diffusion length and the voltage from collector to base is higher enough to maintains the current. If such current is maintained, it should be propotional to the perturbation of base current and unrelated to collector voltage if such current is already fully established.

$
  beta I_B + (beta+1) I_(C O)= I_C
$

Such stability factor between established collector current and the base current is given above. However, there's also a leakage current due to quantum tunnel effect from emitter to collector also. So we denote here as $I_(C O)$ with a factor $I_E = (beta+1) I_B$. It's proportional to temperature and inverse proportional to thickness of base. The problem is when a base current run in the transistor will cause heat. Therefore cause the final collector current instablely increase with out curb, which is called thermal-runaway.

$
  S(I_(C O)) = (d I_C)/(d I_(C O)) \
  1 - beta (d I_B)/(d I_C) = (beta + 1) 1/S(I_(C O)) \
  S_(I_(C O)) = (beta + 1)/(1-beta (d I_B)/(d I_C))
$

== MOSFET

A _MOSFET_ is for a n/p typed semiconductor, equipped with a metal-oxide plate as a capacitor. For a p doped semiconductor, we use the metal-oxide to provide a positive voltage, that's, poshu the doped charge away from its surrounded area, induce a relative negative charge region. We call such induced region as _charge inversion layer_, and the threshold voltage as $V_(T N\/P)$. Then we take two n doped terminal in two side of the semiconductor, as source and drain. The oxide-metal plate is, the gate. When we apply a drain voltage. If $V_(G S) < V_(T N)$, there's no current. If $V_(G S) > V_(T N)$, we can apply $V_(D S)$ to drive current, and initially, following Ohm law until the voltage is too higher even attracting the n doped area of gate area until depletion, a.k.a saturation. Thus we can declare that the saturation current only proportional to $V_(G S) - V_(T N)$ for the inversion layer thickness.

It's more stable that doesn't rely on diffusion current and thus less dependent on temperature.

$
  I_D &= K_n (V_(G S) - V_(T N))^2 \
  &= I_(D S S) ((V_(G S))/(V_(T N)) - 1)^2
$

So if we, are given the expression of $V_(G S)$, we should find the intersection point of above relation and $V_(G S)$.


= Digital

== Numerical Code

- BCD(8421) code: 4-bit code, each represents: 8421.
- Excess 3 code: 8421 code + 3.

== Boolean

$
	non(A+B) = non(A) dot non(B) \
$

You should notice that, because turn every element should be same as turn each:
$
	non(non(A B)) = non(non(A) + non(B)) = non(non(A)) dot non(non(B))
$

It's often used to turn OR device into NAND:

$
	(A+C)B + D+E &= non(non(A+C))dot non(non(B)) + non(non(D+E)) 
	&= non(non(A) dot non(C)) dot non(non(B)) + non(non(D) dot non(E))
$

And XOR:
$
	non(A xor B) = A nxor B = A B + non(A) dot non(B) \
	non(A xor B) = non(A non(B) + non(A) B) = non(A non(B)) dot non(non(A)B) = (non(A)+ B)(A+non(B)) = A nxor B
$

Karnaugh Map is rather to identify minimal or maximal term. What is minimal/maximal term? If we choose the range of variables and we intersects them, we yield a minimal term $A B C...$, if we union them, we yield a maximal term $A + B + C...$. It said that every logic results as $f(A,B,...)$.

Suppose a selection function, which is minimal term:
$A B non(C) D$, it can only becomes $1$ when $1101$. Thus, as a finite function $f$, it has $2^n$ terms corresponding to $2^n$ selection to construct all function. $f(1,1,0,1) = 1 ->^"only if" A B non(C) D = 1 ->^"only if" "term"(A B non(C) D) "exists"$ indicating the term doesn't exist.

$
  f(A,B,C,D) = A B C D + non(A) B C D + (non(A) non(B) C D = 0) +...
$

For only minimal terms that equal to $1$, else all is 0 to construct a function. Reversely, we can have $(A+B+C+D)(non(A)+B+C+D) ...$ can construct another form which the term only exist if it's $0$, otherwise $f(1,1,0,1) = 0 ->^"only if" (non(A) + non(B) + C +non(D)) = 0 ->^"only if" "term"((non(A) + non(B) + C +non(D)) "exists"$. Notice it's reverse because we need the maximal term equal zero, so only if the specific selection maximal term equal zero, which means it must exist.

Then Karnaugh map said that we can list all possibilities and use merge operation like $A + non(A) = 1$ for adjoin terms or $A dot non(A) = 0$. We seek the maximal $2^n$ block to cover $1$ for minimal terms or $0$ in maximal terms(notice it should be reversed!) and yielding the final results.

== Adder 

A full adder, should record the two bit as "addee", and one bit for "carry-out". First, we evaluate "addee" first, when both are $0$ or $1$, it's $0$, if one of it is $1$, we has $1$ as output, so it's $a xor b$. Then consider carry-out, if the output and carry-out is both $0$ or $1$, we has $0$, if one of them is $1$, we has $1$ as final output. So it's $C_"in" xor (a xor b)$. Then, what's the new carry-out from the adder machine? It's only possible when the addee or carry-out, two of them or three of them is $1$ to create a new carry-out. So we has $(a+b)(a+C_"in")(b+C_"in") = a b + C_"in" (a + b) $, three of them is $1$ is already in the term.

#image("assets/4-bit-adder.png")

To chain series of adders form a higher bits adder.

== Latches

The flip-flop is the most simple _memory_ state circuit. Given a input $S$ and $R$ as set or rest, and current state $Q$. Initially, we could design a no input connection circuit that $A ->^("neg") B ->^("neg") A$ will immediately fall into a certain state. However, there's no input to nudge it.

$
  Q_(n+1) = f(S,R,Q) \
$

We know $S$ must set no matter previous is, and $R$ must reset no matter previous is, then if no input, it should be $Q_n$ to retain state:

$
  Q_(n+1) &= S non(R) + non(S) dot non(R) Q \ 
  &= non(R) (S + non(S) Q) \
  &= non(R) (S + Q) \
  &= S non(R) + non(R) Q
$

It use three different gate, we try to simplify using lesser:

$
  non(R)(non(non(S+Q))) = non(R)(non(non(S) dot non(Q)))
$

Or:

$
  non(non(non(R)(S + Q))) = non(R + non(S + Q))
$

Using OR gate too.

However, if $S = R = 1$, we see $Q_(n+1) = 0$! We aren't luck, this indicates it's not robust that we should forbid such state.

#align(center)[#image("assets/latches.png", width: 80%)]

From the first latch, we see:
$
  non(non(S + Q) + R) = non( non(S) non(Q) + R) = non(R) (non(non(S+Q))) = non(R)(S + Q) = Q'
$
And the third latch:
$
  non(non(non(S) non(Q)) dot non(R)) = non(Q) \
  non(non(S) non(Q)) dot non(R) = Q
$

That's the deduction of simple latches. In digital circuit, time or frequency is important because such square waves can order different speed gate into a standard sequential logic. It's important to share a global clock for each state process machine. How to take effect, we know it should be $1$ in square wave pulse to allowing others pass, so we add a AND gate in front of each input $S$ and $R$.

#image("assets/clock-latch.png")
#footnote[It use NAND is due to previous shown _reverse_ input design].

Now, if we only need a single data input, control all bit by its input $0$ or $1$, $R = non(D), S = D$ indeed, and we remove the violated state! Reversely, we can construct $T$-latch which reverse $Q$ state!

#image("assets/D-latch.png")

we leave a forceful input $non(S)$ or $non(R)$ to allowing asynchronous operation. Now we try to learn how to read this sequential diagram, in the period $"R" = 0$, D can only trigger the bit when it's high and CLK is high too. Finally, we see R = 1 suddenly make Q = 0.

The underneath problem is if D changes when CLK = 1, /* the response of Q would be depended on the response delay, especially on the edge of CLK transition. */ In data transmission, it indicates a unacceptable change of state in only one clock time, causing confusion. So we want a design only triggered on up or down of CLK, to identify the presumed state from $D$ present.#footnote[There's also ambuguity exist if $D$ is on the CLK transition collide with D transition. But already reduced too much.]

#align(center,image("assets/pulse-latch.png",height: 20%))

It first store the change tendency on the first latch, and then apply it's tendency on the second latch which is output only when CLK is down, and we can reverse the design to acquire a output only when CLK is high.

Another way to reduce input state violation problem is to take the output into input as a Three input AND gate. We see if $S = R = 1, Q = 1, non(Q) = 0$, the real $R' = R dot non(Q) = 0$  and $S' = S dot Q = 1$, so retain its state, reversely, when $Q = 0, non(Q) = 1$, $R' = 1, S' = 0$, which is same. However, it also forbid the original operation too. When $S = 1, S' = S Q = 0$. Then, we can let $S' = S non(Q), R = R Q$, which is reasonable that only triggered when they are in their case. But when $S = R =1$, it reverse $S' = non(Q), R' = Q, Q_(n+1) = non(Q) (non(Q) + Q) = non(Q)$. Reverse original state. We call the new $S = J$, $R = K$ as JK-latch.

Now given a JK-latch, the new state transition is: 
$
	Q' &= non(R') (S' + Q) = non(K Q)(J non(Q) + Q) \
	&= (non(K) + non(Q))(J + Q) \
	&= J non(Q) + non(K) Q
$

The third line is that $(J + Q)$ has complement $non(Q)$ only, and $(non(K) + non(Q))$ has complement $Q$ only. The above declares that $Q' = 1$ if $J = 1$ to reverse into $non(Q)$#footnote[Or only set if $Q = 0$.] state as above suggests, or $K = 0$ to keep $Q$ state.

In practise, we often use edge triggered JK or D-latch.

Flip-flop can be connected as series, but in order to keep synchronous logic, we should use CLK, when the before is ready, it gonna to trigger the next. However, in order to avoid previous mentioned state changed in one CLK period problem, we use edge triggered flip-flop. 

#image("assets/counter.png")

Here $Q' = D = non(Q)$ only when the previous CLK = $"Q"^(n-1)$ is falling. That's, only when previous $"Q"^(n-1)$ finishes its state period, the next state triggered, and switch between $Q <-> non(Q)$ in previous one's full period. It means, to construct a counter, we should let next state contains previous one's $2$ switched state period to completely encompass counts, suggesting to trigger the next one when previous one falling and until one falling, a.k.a completely finishes it works. Therefore, the current one gonna trigger next next one etc...

The self reference of $D = non(Q)$ isn't necessary, we can based on the state store to construct more complicated state transition circuit.

