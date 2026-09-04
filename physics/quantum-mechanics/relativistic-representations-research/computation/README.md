# Relativistic field computation workbench

This directory contains the executable part of the representation-to-observable
research graph. Conceptual derivations live in `../nodes/`; this package retains
only operations reused across nodes and compact behavioral certificates.

## Environment and verification

The project uses uv-managed CPython 3.13 with two direct mathematical
dependencies: SymPy for exact algebra and SciPy for numerical integration.

```powershell
uv sync --locked
uv run --locked python -m unittest discover -s tests
```

`uv.lock` fixes transitive versions. `.venv`, bytecode, raw traces, and generated
plots are never research artifacts.

## Ownership

- `fieldcalc.rewrite`: bounded semantic word rules, budgets, and refusals;
- `fieldcalc.exact`: exact-domain rank/kernel certificates;
- `fieldcalc.grammar`: operations generated from carrier laws and resources;
- `fieldcalc.residual`: obstruction-driven exact repair and cost verdicts;
- `fieldcalc.models`: admitted benchmark parameters and departure factors;
- `fieldcalc.measures`: one visible measure with bound/open transforms and errors.

A tool may be imported by a test; a tool never imports a test. A probe is deleted
after its conclusion is promoted. A retained certificate checks a semantic law,
not stdout text or a private helper call.

## Flow

```text
carrier/model request
  -> typed admission
  -> project semantic grammar or measure construction
  -> SymPy exact solve or SciPy value/error transform
  -> generated object or structured refusal
  -> certificate consumed by a surviving node
```

The package is private research infrastructure. It does not promise a public API,
arbitrary tensor algebra, carrier-global discovery, or a generic spectral solver.
