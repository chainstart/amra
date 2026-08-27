# Obstruction analysis: the missing scale is constant multiplicative width

## Frozen predecessor gap

The predecessor path construction starts from a connected path on `2s+1`
vertices, labels its edges by distinct primes, and pads its vertex-products by
powers of one prime `b`.  Connectivity gives support minimality.  The sole
quantitative loss occurs when the earlier proof requires `s=o(K)` in order to
make every edge-prime product `b^o(K)`.  That condition is sufficient for a
moving power tail, but stronger than necessary for a fixed multiplicative
tail.

The useful budget has three parts.  For `N=b^K`, put
`m=floor(K/16)` and attempt `s=m`.

1. Start all edge primes above `y=b^m`.  Repeated Bertrand intervals place
   the `2m`-th prime below `2^(2m)b^m`.  Since `b>=2`, the product at a path
   vertex is below `b^(6m)`.
2. Rounding each path product upward to the next power of `b` leaves an
   initial padding exponent at least `K-6m`.
3. Equal path-shore products imply that the discrepancy between the two
   padding-exponent sums is less than `K+m`.  Distributing it over the
   `m+1` vertices of the larger shore costs at most 18 exponent units per
   vertex.

For large `m`, the remaining exponent is nonnegative and the padded values
are all greater than `N/b^19`.  This is the precise candidate calculation to
prove or kill.  The constant 19 is intentionally not optimized.

## Why a broad local-rule theorem is not currently justified

A rule seeing the exact integer label, all prime factors, or an adaptive
largest-prime residue can distinguish every member of the path.  One
minimal relation then says nothing about the size of the union of owners over
all relations.  Extending the no-go conclusion to every such rule would
therefore require a global transversal lower bound, which is not available.

There is, however, a natural exact class with an indistinguishability cell.
Freeze a set `P_K` of controlled primes, omit the padding prime `b`, and let
the rule see only the vector `(nu_p(n))_(p in P_K)` above a lower cutoff.  If

`sum_(p in P_K) 1/p <= 1-delta`,

then at least `delta N-O(1)` integers up to `N` have the all-zero signature,
by the union bound.  An `o(N)` union of complete signature fibres cannot
delete that fibre.  A path whose edge primes lie above every member of
`P_K` and whose padding uses `b` lies entirely in the retained zero fibre.

This observation model includes a lower threshold, any finite union of
nested lower thresholds, and sparse controlled prime valuations.  It does
not include adaptive rough-prime ownership, full factorization, arbitrary
congruence predicates, or residue-aware recursive rounding.

## Exact consequence sought

The campaign can promote only if the constant-width construction is proved
for all sufficiently large `K` and the valuation-cylinder corollary follows
with all quantifiers frozen.  A finite instance, another `N^(1-eta)` tail,
or an informal statement about all local algorithms is non-success.
