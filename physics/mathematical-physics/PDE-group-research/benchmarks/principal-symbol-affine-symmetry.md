# Principal-symbol affine symmetry probe

## Target and discriminator

`E-G22-01` tests `C_G22_v0`: either a constant nondegenerate scalar principal
symbol constructs the complete finite affine base candidate space before the
full-operator test, or seed discovery still requires a supplied group or
polynomial-vector-field enumeration. The candidate is frozen across all cases;
only the defect map changes with the operator coefficients.

## Inputs and operation

The maintained checker extracts `G`, constructs translations and `A=G S_ab`,
adds the canonical real `u(n)` basis, lowers every `[D,L_v-J]` exactly, and uses
one defect-kernel/ideal/quotient compilation. It never receives a group name,
expected generator, or preparation-derived direction.

The bench family contains:

- the free scalar Laplacian in two dimensions;
- the same free operator in a nonorthogonal coordinate metric
  `G=[[2,1],[1,1]]`;
- the anisotropic scalar oscillator `-Delta+x^2+2y^2`;
- the radial coupled operator `-Delta I_3+x x^T`;
- the existing public G20 polynomial fixture, evaluated independently by both
  routes; and
- the degenerate symbol `-partial_y^2` as a refusal control.

## Exact result

```text
operator                         base / all candidates  kernel  visible / ambiguity
free scalar, G=I                 3 / 4                  4       3 / 1
free scalar, non-diagonal G      3 / 4                  4       3 / 1
anisotropic scalar oscillator    3 / 4                  1       0 / 1
radial 3x3 matrix PDE            6 / 15                 4       3 / 1
public G20 fixture               3 / 12                 2       1 / 1
degenerate second-order symbol   --                     --      typed refusal
```

For the radial matrix PDE, the exact residual target has 75 coordinates and the
generic compiler performs 3629 bracket/ideal checks. Its quotient table is the
three-dimensional rotation table, recognized only after construction. On the
public fixture, the G22 visible direction and the G20 residual-derived direction
have joint rank one. The anisotropic potential removes every visible affine
motion while retaining scalar `iI`; this shows lower coefficients filter rather
than enlarge the symbol candidate space.

## Reproduction and evidence right

From `computation/`:

```powershell
uv run python -m unittest check_affine_symbol_symmetry.py
```

All four exact checks pass under the locked CPython 3.14 / SymPy 1.14 environment.
The checker consumes production commutator and defect-compiler operations, but no
production route imports the checker.

```text
id: E-G22-01
target: C_G22_v0 principal-symbol affine symmetry construction
kind: deductive completeness witness plus maintained exact computation
result: intrinsic finite candidate algebra, exact full kernel and quotient,
        G20 coincidence, lower-order elimination, degenerate-symbol refusal
permitted consequence: promote G22 in the stated constant-scalar/constant-lift class
boundary: no variable or matrix symbol completeness, variable internal lift,
          public schema, global integration, domain flow, spectrum, or cost leverage
```

Retention: **promote** the constructor, compact result table, coincidence witness,
and refusal boundary; drop transient residual matrices.
