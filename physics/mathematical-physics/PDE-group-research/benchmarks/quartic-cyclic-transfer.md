# Quartic oscillator: group detection before cyclic approximation

## Purpose and spine binding

This probe removes the quadratic-closure resource from the previous oscillator
bench while retaining one survival observable. It tests the composition

```text
PDE coefficients
  -> detected finite symmetry and representation block
  -> observable-cyclic recurrence inside that block
  -> exact no-gain or controlled-truncation verdict.
```

The upstream objects are the decision engine, the cyclic calculus, and its
[exact finite implementation](../computation/README.md). The invariant target is
the ground-preparation survival amplitude. The finite Galerkin model is the
current horizon; convergence back to the continuum PDE is explicitly outside the
supported result.

## 1. The PDE constructs its first group

Consider

```text
H_g=-d^2/dx^2+x^2+g x^4,             g>0.                           (1)
```

The coefficient involution `x -> -x` constructs the pullback
`(Rf)(x)=f(-x)`. Evaluating both routes on a smooth core gives

```text
R d^2/dx^2 = d^2/dx^2 R,
R x^(2k) = x^(2k) R,
[R,H_g]=0,                            R^2=I.                         (2)
```

Thus the PDE itself supplies a representation of `Z_2`, not a guessed
spectrum-generating group. Its two irreducibles construct the even and odd
projectors `(I+R)/2` and `(I-R)/2`. The even ground preparation makes the odd
block exactly invisible to the requested amplitude.

This is already a bilateral step: coefficient invariance generates a commuting
operator algebra, its relation `R^2=I` integrates to `Z_2`, and the group
representation returns the parity decomposition of the PDE. It does not solve the
dynamics within either block.

## 2. A structurally generated finite action

Use the unnormalized Hermite carrier

```text
e_n(x)=H_n(x) exp(-x^2/2),
<e_n,e_m>/sqrt(pi)=2^n n! delta_(nm).                               (3)
```

The two operator rules

```text
(-d^2/dx^2+x^2)e_n=(2n+1)e_n,
x e_n=(1/2)e_(n+1)+n e_(n-1)                                      (4)
```

generate the entire finite model. Four applications of the second rule construct
`x^4`; no quadrature, eigenfunction table, or component-wise quartic formula is an
input. Let `V_N=span{e_0,e_2,...,e_(2N-2)}` and define

```text
H_(g,N)=P_(V_N) H_g P_(V_N).                                       (5)
```

The projection makes (5) a finite Galerkin problem, not an invariant subspace of
the continuum quartic operator. The diagonal metric in (3) exactly certifies
`H_(g,N)^T G=G H_(g,N)`.

The reproducible adapter is
[quartic_galerkin.py](../computation/quartic_galerkin.py). Its generator uses
(4), passes the matrix and physical metric to the same cyclic reducer used by the
earlier tests, and prints the missing continuum certificate before any result.

## 3. Exact transfer returns no cyclic dimension gain

For the exact rational input

```text
g=1/10,        N=6,        psi=e_0,                                 (6)
```

the constructor terminates at cyclic degree `r=6`, verifies recurrence and moment
recovery through degree `11`, and returns

```text
ExactCyclicReduction: ambient 6 -> cyclic 6,
dimension verdict: exact_no_dimension_gain.                         (7)
```

The harmonic limit `g=0` instead terminates at `r=1` with relative minimal
polynomial `lambda-1`; this is the regression check. At nonzero coupling (6), the
ground preparation reaches the entire tested even Galerkin block. Therefore the
exact cyclic route does not compress beyond the `Z_2` representation reduction on
this input.

This negative result is useful. It prevents the tridiagonal recurrence from being
advertised as a universal simplification. The exact coefficients also grow
rapidly—for example the beginning is

```text
alpha_0=43/40,    c_1=3/50,    alpha_1=171/20, ...                  (8)
```

and later exact rationals are semantically less readable than the two generative
rules (4). Human compression therefore selects the parity action and Hermite
operator grammar, not the full six-step coefficient list.

## 4. Budget truncation is a different arrow

Stopping the same recurrence at `m=2` yields boundary coefficient

```text
c_2=927/64.                                                         (9)
```

For `|t|<=1/100`, the cyclic Duhamel certificate computes

```text
|C_(g,N)(t)-C_(g,N,2)(t)|^2
  <= t^2 c_2
  <= 927/640000
  < (1/10)^2.                                                       (10)
```

The executable consequently returns `ControlledCyclicReduction` for tolerance
`1/10`. It also states that the four excluded Galerkin directions are **not**
invisible. Equation (10) is a controlled approximation inside (5), whereas (7)
is an exact visibility statement; the decision engine must not merge them.

No bound in this node compares `C_(g,N)` with the continuum survival amplitude of
(1). Until a Galerkin convergence estimate is supplied, (10) is not a certified
PDE observable error.

## 5. Whole-route verdict

For this finite transfer:

| Route | Constructed object | Verdict |
| --- | --- | --- |
| coefficient symmetry | `R`, `R^2=I`, even/odd irreps | exact, human-simple, reusable |
| exact cyclic inside even block | length-six recurrence | correct but no dimension gain |
| two-step cyclic | two coefficients plus boundary arrow | controlled only for the declared finite model and time |
| continuum quartic PDE | full survival amplitude | still open; Galerkin error unpaid |

The result changes the global selector:

```text
detect and use the finite symmetry first;
run the cyclic probe inside the prepared representation block;
retain it exactly only when r<N;
otherwise use a budgeted recurrence only with an observable error certificate.
```

This is broader than the quadratic bench because no finite oscillator ladder
closure is used. It is narrower than a PDE solver because the analytic passage
`H_(g,N) -> H_g` and the bounded Lie/factor refusal remain open.

## 6. Reproduction

From the repository root:

```powershell
python physics\mathematical-physics\PDE-group-research\computation\quartic_galerkin.py `
  --levels 6 --coupling 1/10

python physics\mathematical-physics\PDE-group-research\computation\quartic_galerkin.py `
  --levels 6 --coupling 1/10 --budget 2 `
  --time-horizon 1/100 --tolerance 1/10
```

Persistent tests reconstruct (4)--(10), the exact no-gain result, the harmonic
limit, and the truncation/invisibility distinction.
