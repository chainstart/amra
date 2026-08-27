# Mechanism falsification

## M786S-02: Bertrand does not count a fixed dyadic reservoir

Bertrand's postulate asserts at least one prime in `(x,2x)`.  Reapplying it
moves to a new interval and does not produce `K/2` primes inside the original
`(X,2X)`.  The reservoir requires a quantitative prime-counting input such
as `pi(2X)-pi(X)~X/log X`.

## M786S-03: `A=3` fails the frozen worst-case budget

The dyadic rough-part estimate guarantees only `2A-2=4` initial padding
units when `A=3`, whereas even balancing may require five decrements at one
left vertex.  Nonnegativity is not uniformly certified.  This kills the
stated worst-case proof; it does not assert that every individual `A=3`
instance fails.

## M786S-05: two super-square-root labels exceed `N`

An internal path vertex is divisible by two distinct incident labels.  If
both are greater than `sqrt(N)`, their product is already greater than `N`,
and multiplicative padding cannot reduce it.

## M786S-06: disconnection creates a proper bad component

Every connected component of the edge-prime incidence graph has equal
products on its induced shores.  If the full disconnected relation has
nonzero cardinality difference, at least one component has nonzero
difference and is a proper bad subrelation.  Support minimality forces
connectedness.

## M786S-08: off-zero query primes are irrelevant

An integer answering zero throughout never visits a nonzero branch.  A prime
of arbitrary size may be placed only on such a branch without changing the
zero transcript or the relation embedded in it.  Only zero-branch primes
need lie below `X`.

## M786S-09: `o(N)` cost is not small relative to an `o(N)` zero population

The exact bound is `E|D|/(L-t)`.  When `L=o(N)`, an expected deletion cost
may be `o(N)` yet much larger than `L`; the ratio then gives no vanishing
success probability.  Positive density is needed for the simple `o(N)`
corollary.

## M786S-10: one global repair hits one witness path

Once a missed path is exposed, a global alteration may delete one of its
vertices.  The zero-transcript charge does not make that one repair cost a
positive fraction of `N`.

## M786S-11: private coins condition to nonuniform programs

Conditioning on random coins indexed separately by the input leaves a
different deterministic program for each integer, not one uniform tree.
There is no common zero transcript to which the path theorem can be applied.

## M786S-12: finite prime counts do not supply an asymptotic theorem

Checking finitely many intervals cannot establish that every sufficiently
large exponential `X` contains the required number of primes.  The universal
claim depends on the named prime-interval theorem, while computation is only
a replay guard.

## Survivors

* `M786S-01`: prime interval abundance supplies all path labels within one
  fixed dyadic interval.
* `M786S-04`: `A>=4` gives reserve `2A-2>=6`, exceeding the maximum decrement
  five.
* `M786S-07`: the prior zero-transcript dichotomy and expectation charge lift
  unchanged to the stronger square-root-scale cutoff.
