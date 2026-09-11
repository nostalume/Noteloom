# Polynomial lift Lie-closure probe

## Target and alternatives

`E-G21-01` tests `C_G21_v0`: several exact local lift pairs may already be closed,
generate a finite extension, fail their common-operator identity, or continue
beyond a finite budget. Closure is computed over constant real scalars; rational
function-field span is deliberately not accepted as finite Lie closure.

## Inputs and operation

The positive transfer uses the three-dimensional matrix Schrödinger operator

```text
D=-Delta I_3+x x^T
```

with two coordinate-free skew matrices acting simultaneously on base coordinates
and the carrier. No `SO(3)` name or third generator is supplied. Exact bracket
closure generates the third rotation pair. A supplied scalar `iI` seed tests that
pure internal symmetry is retained as ambiguity rather than counted as visible.

The adversarial second-order control uses `D=-partial_y^2` and the exact symmetries
`x^2 partial_x`, `x^3 partial_x`. Their brackets generate unbounded polynomial
degree. A separate broken rotation omits the forced internal action and must fail
before closure.

A finite-type control solves the flat Killing equations for every three-component
polynomial vector field of total degree at most two. Its exact kernel has dimension
six—three translations and three metric-skew linear fields—and every quadratic
coefficient vanishes. This checks the internally derived `d(d+1)/2` candidate
bound without supplying the six generators.

## Result

```text
radial matrix PDE:
  seed dimension             3 (two visible, one internal)
  generated dimension        4
  visible quotient dimension 3
  ambiguity ideal dimension  1
  bracket evaluations        6
  quotient checks            ideal, antisymmetry, Jacobi: exact

degenerate second-order PDE:
  dimension budget           5
  independent dimension      5 before the next escaping bracket
  result                     unresolved within budget

broken internal lift:
  result                     SeedNotFullOperatorSymmetry

nondegenerate scalar principal symbol:
  quadratic ansatz unknowns  30
  exact Killing kernel        6
  surviving quadratic terms  0
```

The degree formula
`[x^m partial_x,x^n partial_x]=(n-m)x^(m+n-1) partial_x` proves that the second
case is genuinely infinite-dimensional; the budget result is not treated as that
proof.

## Reproduction and evidence right

From `computation/`:

```powershell
uv run python -m unittest check_polynomial_lift_lie_closure.py
```

The four exact checks pass under the locked CPython 3.14 / SymPy 1.14
environment. The checker reuses the production polynomial commutator evaluator without
being imported by production.

```text
id: E-G21-01
target: C_G21_v0 constant-scalar closure and ambiguity quotient
kind: deductive identities plus maintained exact computation
result: finite generated so(3) quotient; affine Killing bound; invalid-seed refusal;
        unbounded-growth control
permitted consequence: freeze G21 closure and the constant nondegenerate-symbol gate
boundary: no production constructor, completeness criterion, integration, domain flow,
          group uniqueness, or complete-route leverage
```

Retention: **promote** the contract, positive table, and unbounded-growth boundary;
drop transient coefficient matrices.
