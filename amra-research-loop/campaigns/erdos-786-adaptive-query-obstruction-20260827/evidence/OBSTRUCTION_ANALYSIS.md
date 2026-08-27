# Obstruction analysis: only the zero query branch must be controlled

## Geometry lost by the fixed `1/16` parameter

In U.1, edge primes start above `b^m` and a path of `2m` edges is used.  The
same calculation has two independent parameters.  Let

`u=floor((1/2-epsilon)K)` and `s=floor(epsilon K/4)`.

Starting above `b^u` and iterating Bertrand over `2s` edges keeps every edge
prime below `b^(u+2s)` and every path vertex rough part below
`b^(2u+4s)<=b^((1-epsilon)K)`.  Initial padding therefore retains at least
`epsilon K` base-`b` exponent units.  The shore-sum discrepancy is still
less than `K+s`; distributing it over `s+1` vertices costs at most
`O(1/epsilon)` per vertex.  The exact surviving condition is
`epsilon^2 K -> infinity`.

For fixed `epsilon`, this predicts a fixed multiplicative tail while the
construction avoids every declared prime below `N^(1/2-epsilon)`, a much
larger observation range than `N^(1/16)`.

## Adaptive trees reduce to one seedwise branch

Fix a deterministic exact-valuation decision tree and repeatedly answer
zero.  The resulting finite root-to-leaf path queries a set `P` of primes.
Every integer coprime to `P` follows this path, even if all nonzero branches
query unrelated or much larger primes.  Thus only `P`, not the union of all
tree queries, must be avoided by the arithmetic relation.

If `sum_(p in P)1/p <= 1-delta`, at least `delta N` integers up to `N` are
coprime to `P`.  Labelling the zero leaf deleted therefore costs at least
`delta N-t` above a lower threshold `t`.  An `o(N)` deterministic classifier
must retain that leaf.  A path relation avoiding `P` then witnesses failure.

## Shared randomness yields an expectation bound

Now draw a seed and let it select the full deterministic tree.  The missed
relation may depend on the seed; this is legitimate because a transversal
must meet every bad support.  Seedwise, success implies that the zero leaf is
labelled deleted.  If `X` is the deletion-set size, then

`X >= (delta N-t) 1_{zero leaf deleted}`.

Taking expectations gives the candidate exact inequality

`Pr(output is a transversal) <= E X/(delta N-t)`.

No independence between integer decisions is used.  The argument does not
cover global alteration because one uniform per-integer tree is essential.

## Required adversarial checks

The proposed theorem must fail closed when the zero branch does not
terminate, queries the padding prime, reaches primes above the geometric
cutoff, or has a zero cell of size `o(N)`.  It must also reject trees that
read the exact integer label or change their query program after observing
decisions made for other integers.  Those models can target individual path
vertices and are not consequences of one seedwise leaf.
