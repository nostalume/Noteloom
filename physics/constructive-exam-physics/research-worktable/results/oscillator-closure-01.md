# Oscillator observable-closure result 01

## Result

An exact rational constructor now generates the smallest subspace reached by
repeated adjoint action on a requested linear observable. It returns reduced
second-order equations or the first independent observable exceeding the declared
exam budget.

## Evidence

Canonical command:

```text
python -m unittest discover -s tests -v
```

The fresh development run passed seven tests:

- scalar center-of-mass closure for a four-coordinate reciprocal ring;
- transfer to irregular reciprocal couplings;
- transfer to unequal masses using the mass-weighted observable;
- construction of a two-coordinate closure for two visible restoring scales;
- refusal when broken common frequency exceeds a one-coordinate budget;
- refusal of the zero observable;
- rejection of a noninteger equation budget.

For the four-coordinate ring the generated cost record is:

```text
full unknowns:      4
retained unknowns:  1
law actions:        1
```

For the two-frequency case, the constructor generates two observables and the
reduced operator

```text
R = [[ 0, 1],
     [-4, 5]].
```

The test evaluates the full and reduced acceleration of the same requested
observable on the same state and obtains exact rational equality.

## Unexpected diagnostic

The first irregular-coupling fixture failed to close because one diagonal entry
violated the common-frequency construction. The tool expanded to four variables
instead of accepting the case by its description. Correcting the physical input
restored scalar closure. This is evidence that the operation consumes the actual
dynamics, not the test label.

## Supported claim

Within finite rational second-order linear systems, the probe constructs an exact
observable closure and a useful failure witness. It reduces the number of live
quantities relative to a componentwise full-state route when the generated
dimension `r` is smaller than `N`.

## Unsupported claim

No advantage over an expert center-of-mass derivation has been established. No
human timing, error, retention, or blind-transfer study has been performed. The
current result supports a mathematical generator and a candidate exam worksheet,
not improved examination performance.
