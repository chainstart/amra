# Mechanism falsification

## M786Q-02: `epsilon K` divergence alone does not preserve the stated tail

Take `epsilon=c/sqrt(K)` with a fixed small `c>0`.  Then `epsilon K` tends
to infinity but `epsilon^2 K=c^2`.  The shore discrepancy is greater than
`K-s-1`, while there are only `s+1` left vertices.  Keeping every decrement
within `O(1/epsilon)` supplies only `O(K)` total decrement capacity, with a
constant proportional to the frozen tail allowance.  The internal vertices
have only `O(epsilon K)` nonnegative padding reserve.  For sufficiently small
`c`, the specific `s=floor(epsilon K/4)` host cannot simultaneously absorb
the discrepancy, keep all exponents nonnegative, and retain the declared
`O(1/epsilon)` tail.  The uniform proof therefore needs a lower reserve such
as `epsilon^2 K -> infinity`; the weaker route is killed, not promoted as a
universal theorem.

## M786Q-03: the tail constant must grow when `epsilon` tends to zero

Equation `Delta>K-(s+1)` forces some left decrement to exceed

`(K-s-1)/(s+1)`.

For `s` of order `epsilon K`, this is of order `1/epsilon`.  Hence no fixed
base-`b` tail exponent can contain this construction for a sequence
`epsilon_K -> 0`.

## M786Q-04: square root is a hard barrier for the path rough parts

An internal path vertex is divisible by its two distinct incident edge
primes.  If both exceed `N^(1/2+eta)`, their product exceeds
`N^(1+2eta)>N`.  Multiplication by a padding power cannot reduce it.  This
path host cannot avoid all controlled primes beyond the square-root scale.

## M786Q-07: no density-free expectation charge

For a growing initial set of primes, the density of integers avoiding every
queried prime is `prod_p(1-1/p)`, which tends to zero.  The complete zero
transcript can then be deleted at `o(N)` cost.  The event
`zero leaf is deleted` no longer forces a positive-proportion deletion, so
the claimed expectation bound has no denominator bounded below by `cN`.
This kills the density-free charging mechanism; it does not assert that the
dense-query classifier is a transversal.

## M786Q-08: the current host cannot answer zero at the padding prime

The unequal shore sizes require nonconstant positive `b`-valuations to
balance the two products.  U.1 and its parameterized extension therefore do
not lie in the zero `b`-valuation transcript.  The padding prime must be
omitted from the controlled zero branch for this host.

## M786Q-09: per-integer programs destroy the common transcript

If the program may depend on the input label, it can encode a prescribed
integer and delete a chosen vertex of the displayed path.  There is no one
finite prime set whose zero transcript contains every path vertex.  Such a
model is an exact-label rule in disguise, not a uniform valuation-query
classifier.

## M786Q-10: global alteration repairs one path at unit cost

After the first-stage tree retains the constructed relation, a global repair
step that inspects missed supports can delete one of its vertices.  The
`delta N-t` zero-leaf charge applies only when the complete transcript is
deleted; it gives no lower bound for this one-vertex repair.

## M786Q-11: fresh per-input coins do not condition to one uniform tree

Conditioning on all independent coins indexed by input integers produces a
different deterministic program for each integer, not one tree applied
uniformly.  The result reduces to the killed per-integer comparator M786Q-09
and is outside the shared-seed theorem.

## M786Q-12: a transversal allows a seedwise witness edge

For each realized seed the deletion set is fixed.  It is a transversal only
if it meets every edge of `H_N`.  To prove failure one may therefore choose
any missed edge after fixing that set.  The arithmetic path may legitimately
depend on the seedwise zero transcript; it is not required to be chosen
before sampling.

## Survivors

* `M786Q-01`: the moving-parameter geometric budget survives with
  `epsilon_K^2 K -> infinity` and tail exponent `D_K+1`.
* `M786Q-05`: the deterministic adaptive tree reduces exactly to its finite
  zero transcript, whose positive-density population cannot be deleted at
  `o(N)` cost.
* `M786Q-06`: conditioning on a shared seed preserves one uniform tree and
  yields an exact expectation bound without independence between vertices.
