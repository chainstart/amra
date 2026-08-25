# Local entropy route and its exact missing lemma

This note separates a false linear packing idea from the strongest surviving
positive route.  Nothing here is an all-sequence proof.

## Finite-stage bookkeeping

Let `B_i` be the finite periodic union after the first `i` classes and let

    s_i = density(N minus B_i),
    e_i = density(B_i minus B_(i-1)).

Whenever `s_(i-1)>0`, define the conditional hazard

    p_i = e_i / s_(i-1).

These quantities satisfy the exact identities

    s_i = s_(i-1) (1-p_i),
    -log(s_i/s_0) = sum_{k<=i} -log(1-p_k).

Thus if a fixed periodic cell retains a positive limiting fraction, its total
conditional hazard is summable.  Conversely, divergent conditional entropy
is compatible with convergence because it can simply saturate that cell.  The
prime family `p-1 (mod p)` is the clean comparator: target charge diverges and
the unique active component saturates completely.

## Why global entropy is still insufficient

The classes may all lie in one coarse cell `a (mod g)`.  Global survivor
density then stays at least `1-1/g` even if that cell saturates, so a global
positive lower bound does not make the hazards summable.  Entropy must be
computed relative to the smallest persistent cell carrying the new classes.

After quotienting such a cell, one obtains another least-representative
progression system.  The bounded-ratio constant changes by a finite factor,
but the same obstruction can recur.  Therefore a proof needs a tree of
conditional cells, not one global scalar potential.

## Candidate decisive lemma

For fixed `C`, seek the following uniform alternative on every persistent
periodic cell `V`:

> For every `epsilon>0`, a finite stage can be chosen so that either the
> remaining classes meeting `V` have upper logarithmic mass at most
> `epsilon*density(V)`, or the finite-stage uncovered part of `V` has density
> at most `epsilon*density(V)`.

The second alternative is finite-stage saturation and is uniformly visible
to logarithmic averages because it is periodic.  The first is precisely the
tail tightness needed for a Cauchy approximation.  Applying the alternative
on finitely many cells of a finite periodic partition would prove existence of
the logarithmic density.

## Current gap

Neither monotonicity of `r_j,d_j`, the bounded first-echo delay
`r_j+d_j <= (C+1)r_j`, nor pairwise gcd estimates currently proves this
cellwise alternative.  Infinite-chromatic gcd dependence can concentrate the
classes without presenting a single common divisor, so a naive common-factor
recursion is incomplete.  The guarded search therefore measures both recent
signed cycles and attacked-cell capacity utilisation; it cannot certify the
lemma from finite data.

## Exact obstruction to a collision-multiplicity proof

The first echo is bounded by `(C+1)r_j`, but later echoes can have arbitrarily
large multiplicity even for `C=2` and even when every target is new.

Fix `H>=2`, let `L=lcm(1,...,2H)`, and for each integer
`k` with `H<k<=2H` put

    d_k = L/k,    r_k = d_k-1.

Order these pairs by decreasing `k`.  Then both `d_k` and `r_k` strictly
increase and `r_k<d_k<=2r_k`.  No earlier progression contains a later target:
for the common residue `-1`, that would require an earlier `d` to divide the
later `d`, equivalently the later `k` to divide the earlier `k`; two distinct
integers in `(H,2H]` cannot have that divisibility relation.

Nevertheless every one of the `H` progressions contains the common point

    L-1 = r_k + (k-1)d_k.

Thus neither bounded echo delay nor target irredundancy bounds global echo
collision multiplicity.  A successful positive proof must charge such a
collision as overlap/saturation, not try to inject all later echoes into
distinct integers.
