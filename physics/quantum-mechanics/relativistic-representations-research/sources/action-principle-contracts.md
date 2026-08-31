# Action-Principle Contracts

Status: primary-source packet for `N4c`; historical action claims are bounded here,
while adjoint identities and equivalence maps must be reconstructed internally

## `AP-01` — Constrained bosonic action

- Source: C. Fronsdal,
  [Massless fields with integer spin](https://doi.org/10.1103/PhysRevD.18.3624),
  _Physical Review D_ 18 (1978), 3624--3629.
- Contract: a symmetric rank-`s` potential with vanishing double trace and a
  traceless rank-`s-1` gauge parameter admits a local quadratic gauge-invariant
  action. Its equation is the trace-reversed Fronsdal equation and transmits the
  massless spin-`s` sector.
- Source consequence: coupling to a source does not require its full divergence to
  vanish; the traceless projection of the divergence must vanish.
- Internal obligation: construct the trace-reversal map from the invariant fiber
  pairing, prove formal self-adjointness, derive the projected Noether identity,
  and prove equivalence with N4a's equation on the constrained carrier.
- Boundary: the paper does not make the action unique from Poincare symmetry alone
  and does not supply an interacting completion.

## `AP-02` — Constrained fermionic action

- Source: J. Fang and C. Fronsdal,
  [Massless fields with half-integral spin](https://doi.org/10.1103/PhysRevD.18.3630),
  _Physical Review D_ 18 (1978), 3630--3633.
- Contract: a symmetric rank-`n` spinor-tensor with vanishing triple gamma trace and
  a gamma-traceless rank-`n-1` gauge parameter admits a local quadratic
  gauge-invariant action for spin `n+1/2`.
- Source consequence: the source condition is a projected divergence condition,
  matched to the constrained gauge parameter rather than ordinary unconstrained
  conservation.
- Internal completion: N4i chooses the invariant complex Dirac--Fischer pairing,
  constructs the gamma/metric trace-reversal map, proves its formal adjoint
  identity, and compares its Euler equation with N4b's symbol complex.
- Remaining obligation: select a Majorana or other real Grassmann form and its
  sign convention before claiming a real action.
- Boundary: Majorana reality, positivity, normalization, gauge fixing,
  quantization, and interaction are additional data.

## `AP-03` — Why unconstrained actions are a different presentation

- Source: D. Francia and A. Sagnotti,
  [Minimal Local Lagrangians for Higher-Spin Geometry](https://arxiv.org/abs/hep-th/0507144),
  _Physics Letters B_ 624 (2005), 93--104.
- Contract: removing the Fronsdal/Fang--Fronsdal trace constraints while retaining
  locality and an action requires additional compensator and multiplier fields in
  the minimal construction: ranks `s-3,s-4` for bosons and `n-2,n-3` for fermions.
- Research use: this is not evidence that N4a/N4b are incomplete as constrained
  free systems. It identifies a distinct off-shell design choice and its auxiliary
  cost.
- Boundary: equivalence must be tested through local maps, eliminated auxiliary
  equations, and source exchange; equality of free helicity fibers is insufficient.

## `AP-04` — Current exchange distinguishes equation presentations

- Source: D. Francia, J. Mourad, and A. Sagnotti,
  [Current Exchanges and Unconstrained Higher Spins](https://arxiv.org/abs/hep-th/0701163).
- Contract: constrained and minimal unconstrained local formulations can be matched
  in free current exchange, whereas a gauge-invariant nonlocal equation is not
  selected uniquely by its vacuum solution space; the Bianchi identity and source
  coupling distinguish the proper Lagrangian representative.
- Research use: N4c must audit equation equivalence at three different strengths:
  physical quotient, local off-shell Euler complex, and source-response kernel.
- Boundary: this contract does not establish an interacting equivalence.
