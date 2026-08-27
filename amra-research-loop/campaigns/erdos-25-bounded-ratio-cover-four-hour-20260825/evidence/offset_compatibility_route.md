# Offset compatibility and the near-extremizer inverse route

Write

    s_j=d_j-r_j.

Then the progression is the residue class `-s_j (mod d_j)`.  Two full classes
intersect if and only if the generalized CRT compatibility condition holds:

    gcd(d_i,d_j) divides s_i-s_j.

When it holds, the intersection has period `lcm(d_i,d_j)` and density

    gcd(d_i,d_j)/(d_i d_j).

Thus every affine fixed-offset family has maximal phase compatibility, while
genuinely varying offsets delete precisely those gcd-weighted intersections
for which the offset difference is incompatible.

The order constraints add another exact relation.  Since

    r_(j+1)-r_j = (d_(j+1)-d_j) - (s_(j+1)-s_j) > 0,

one has

    s_(j+1)-s_j < d_(j+1)-d_j.

In a consecutive-modulus annulus, offsets must therefore be nonincreasing.
A large upward reset in the offset consumes at least the same additive gap in
the moduli.  Dense target blocks and repeated non-affine resets cannot be
chosen independently.

## Decisive inverse lemma now suggested

The multiplication-table obstruction proves that no constant one-generation
packing theorem is possible, even for target-irredundant `C<2` batches.  Its
small union comes from a fixed offset and hence lies in the already-convergent
affine family.  The natural replacement is an inverse statement:

> If a target-irredundant fixed-`C` batch has multiplication-table-scale small
> first-echo union, then all but a quantitatively controlled remainder of its
> gcd intersection weight is supported on finitely or summably many compatible
> offset/affine charts.

If proved with a summable remainder, the affine echo theorem handles the
structured part and the finite almost-packing bound handles the remainder.
This would yield the missing cellwise tightness-or-saturation alternative.

For `n` progressions truncated to `ell` terms, the relevant weighted quantity
is

    W = sum_{i<j, compatible} gcd(d_i,d_j)/max(d_i,d_j).

Each compatible pair intersects in at most
`1+ell*gcd(d_i,d_j)/max(d_i,d_j)` points.  The Dawson--Sankoff second-moment
bound therefore turns an upper bound for `W` into a lower bound for the finite
union.  Pairs with gcd one contribute only the baseline order `n`; the
multiplication-table loss is supported by excess high-gcd compatible weight.
An inverse lemma may consequently be stated as rigidity of near-maximal `W`,
which is more precise than rigidity of raw pair compatibility.

The formal 2700-second search tests the easiest falsification models: moduli in
dense arithmetic annuli with gaps `1,2,3,4,6,8`; monotone, staircase, sawtooth,
and bounded-walk offsets satisfying `Delta s < Delta d`; at least `sqrt(N)`
distinct offsets; no integer affine chart `d=cr+b` with `1<=c<=16` containing
more than half the batch; and exact target irredundancy.  (The sampled modulus
gaps are at most eight, so a majority chart must have slope at most sixteen.)
It records both union size
and the fraction/gcd weight of CRT-compatible pairs.
Finite failure to find a counterexample is not a proof of the inverse lemma.
