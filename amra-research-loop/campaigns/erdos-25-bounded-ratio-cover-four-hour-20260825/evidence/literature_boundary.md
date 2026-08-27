# Literature boundary checked in this round

The search was restricted to primary journal or paper pages.  It did not find
a theorem matching the infinite least-representative question

    union_j (r_j mod d_j),  r_j<d_j<=C r_j,

with both sequences increasing.  Novelty therefore remains
`priority_uncertain`; absence from this narrow search is not a novelty claim.

The closest directly relevant finite result found was:

- Shoni Gilboa and Rom Pinchasi, *On the Union of Arithmetic Progressions*,
  SIAM Journal on Discrete Mathematics 28 (2014), 1062--1073,
  DOI `10.1137/130941122`.
  https://doi.org/10.1137/130941122
  Open manuscript: https://arxiv.org/abs/1310.4348

Its published abstract states that the union of `n` finite arithmetic
progressions, with pairwise distinct differences and each of length `n`, has
at least `c(epsilon)n^(2-epsilon)` elements; it also treats asymmetric
parameters.  This is relevant to the collision side because the bounded-ratio
family has distinct differences.

The open manuscript gives an asymmetric lower bound of the shape

    min(c(epsilon) n^(1-epsilon) ell, ell^2/2)

for `n` progressions of length `ell`, and proves the related gcd estimate

    sum_{i<j} gcd(d_i,d_j)/d_j <= c(epsilon)n^(1+epsilon).

These results validate the idea that large echo collision has a scale cost.
However, they do not directly give the missing logarithmic tail estimate.
Truncating `n` bounded-ratio progressions to `ell=n` echoes can push the union
out to scale about `n C R` when their targets are near `R`; after harmonic
weighting, the bound loses a factor `n^epsilon`.  It therefore gives an
almost-packing inequality, not the scale-uniform or summable estimate required
by the closure contract.

The Davenport--Erdos multiples theorem remains the primary dependency for the
affine and finite-offset results:

- H. Davenport and P. Erdos, *On Sequences of Positive Integers*, Acta
  Arithmetica 2 (1936), 147--151.
  https://doi.org/10.4064/aa-2-1-147-151
