# Mechanism falsification

## M786U-02: half-logarithmic scaling is not certified by Bertrand alone

For `s=floor(K/2)`, iterating Bertrand over `2s` edge primes gives only a
largest-prime bound of order `2^(2s)` before the starting scale is included.
For `b=2`, a product of two incident edge primes may therefore consume about
`4s`, which is about `2K`, base-2 exponent units.  The claimed `b^4` tail
does not follow from this route.  A sharper prime-distribution input might
revive a different theorem, but it is not part of this mechanism.

## M786U-03: the padding prime cannot have one common valuation

If every one of the `m+1` left vertices and `m` right vertices had the same
positive or zero `b`-valuation `e`, equality of products at `b` would give
`(m+1)e=me`, hence `e=0`.  Nontrivial common `b`-padding is therefore
incompatible with unequal shore sizes.

## M786U-04: positive regularity forces equal shore sizes

In a `d`-regular bipartite graph with positive `d` and parts of sizes `r,s`,
counting edges from both parts gives `dr=ds`, hence `r=s`.  A regular
edge-prime host cannot simultaneously provide positive local degree and the
required cardinality imbalance.

## M786U-05: the padding prime must be outside the zero signature

The fixed-width construction uses powers of `b` whose exponents vary across
vertices to compensate for the one-vertex shore imbalance.  Its vertices
therefore do not lie in the zero `b`-valuation fibre.  The controlled set in
the zero-signature theorem must omit `b`.

## M786U-06: dense growing prime sets have a vanishing zero fibre

For the first `r` primes other than `b`, the natural density of integers
avoiding every controlled prime is the finite product
`prod_p(1-1/p)`.  As `r` grows this product tends to zero (equivalently, by
Euler's divergence of the reciprocal prime sum).  Choosing `r=r(K)` slowly
enough makes the finite counting error negligible, so deleting the entire
zero fibre can itself cost `o(N)`.  A quantitative positive-density
hypothesis, such as `sum 1/p <= 1-delta`, is essential.

## M786U-08: one edge does not refute adaptive global owners

An adaptive rule that sees the complete displayed relation can select one
distinguished vertex and hit that edge.  The construction supplies no
packing or overlap theorem forcing distinct owners across many edges.
Consequently it cannot refute arbitrary residue-aware or globally adaptive
rounding.

## M786U-10: support size is not a transversal lower bound

A hypergraph containing only the displayed path support as one edge has
transversal number one, regardless of whether the edge contains
`Theta(log N)` vertices.  A lower bound for `tau(H_N)` would require a
family with a separately proved hitting number; it does not follow from
support minimality.

## Retained mechanisms

* `M786U-01`: the conservative `s=floor(K/16)` exponent budget survives all
  boundary checks and is sent to full symbolic proof.
* `M786U-07`: the reciprocal-sum hypothesis supplies the positive-density
  zero fibre missing from the overbroad growing-prime claim.
* `M786U-09`: on a fixed-width edge every log-defect weight is `O(1/K)`, so
  affordable independent deletion leaves the whole finite edge with
  strictly positive probability; alteration remains outside the claim.
