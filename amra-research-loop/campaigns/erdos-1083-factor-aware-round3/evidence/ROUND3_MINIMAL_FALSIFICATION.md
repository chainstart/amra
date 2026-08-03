# Round 3 minimal falsification

## Exact typed quotient family

Normalize Laurent associates and list the irreducible factor occurrences of
`B` as `H_1,...,H_D`.  The polynomial

`Q(y)=product_nu ((1-y_nu)+y_nu H_nu)`

is a legal family in the Boolean parameters `y_nu`: every normalized divisor
quotient is a specialization at a `0/1` vector.  This repairs the round-two
type error.  It does not give low complexity.  The family has coordinate
degree one but total degree `D` and realizes all `2^D` products for independent
formal factors.  Therefore multilinearity alone supplies neither row
compression nor scalar-copy rigidity.  This kills `M1083R3-03` as stated,
while retaining the representation as a valid host for additional structure.

## Lambda interpolation is not automatic rigidity

For `K` distinct scalar nodes, a coefficient sequence that is zero at the
first `K-1` nodes and one at the last has nonzero finite difference of order
`K-1`.  Its interpolating polynomial has minimum degree `K-1`.  Exact checks
for `2<=K<=8` reproduce this boundary.  Hence a family `Q(T)` can always be
manufactured by interpolation, but the existence statement is vacuous unless
the exact-block hypotheses prove sublinear degree/pole complexity.  They do
not currently do so.  This kills `M1083R3-04` and the automatic-rank part of
`M1083R3-06`; it is not an actual exact-block counterexample.

## Incidence and exponent firewall

The frozen exponents give

`K=5/9, S=7/9, U=5/6, q=13/18`.

The reciprocal defining-cell domain has exponent `K+S=4/3`, but all of these
labels already lie in the same common spectrum `V`, whose exponent is
`S+U=29/18`.  Thus the row index cannot be multiplied into the defining-cell
label count.  This kills `M1083R3-07`.

The complete one-copy native capacity is

`K+S+U+q=26/9<3`.

It cannot be an exponent improvement even under perfect injectivity.  A
second source index would raise the formal tuple capacity to

`K+2S+U+q=11/3`,

but it is not a point-pair domain: the geometry has one common set of `S`
source points and `qU` target points, and one source--target pair carries only
one `X` index.  The actual capacities are

`sources to all targets: S+q+U=7/3`,

`selected chart targets to all targets: K+U+q+U=53/18<3`,

and

`all target--target pairs: 2(q+U)=28/9`.

Thus a genuine all-target-pair theorem must prove maximum fibre, or an
energy-equivalent average fibre, below `t^(1/9-epsilon)` to exceed
`t^(3+epsilon)`.  It must also transfer information from the selected `K`
chart rows to the unselected rows, because all pair domains involving only
the selected chart targets have exponent below three.

The same-sign width formula does give `K-1` genuine pinned target--target
squared-distance labels by fixing an extreme width, but this retains only
exponent `5/9`.

## Mechanism verdicts

- `M1083R3-01` survives only as a factor-moment route that uses the legal
  Boolean quotient family and proves information beyond subset recovery and
  width.
- `M1083R3-08` is killed as formulated: its `KS^2Uq` domain is not a set of
  actual point pairs.  The repaired M10 target is an all-target-pair theorem
  with fibre exponent below `1/9-epsilon` plus propagation beyond the selected
  chart rows.
- `M1083R3-02`, `03`, `04`, `05`, `06`, `07`, `08`, `09`, `10`, `11`, and `12`
  fail their stated first tests through inherited exact negative evidence,
  the interpolation/Boolean tests, the common-spectrum firewall, missing
  incidence domains, unhandled degeneracies, or distributed-defect arrays.

The verifier ran under a 5 GiB / 1800 second guard and used no Lean process.
No public exponent changed.
