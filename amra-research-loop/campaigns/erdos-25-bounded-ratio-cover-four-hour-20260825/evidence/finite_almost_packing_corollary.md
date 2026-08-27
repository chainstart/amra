# Finite almost-packing corollary from Gilboa--Pinchasi

This is an author-verified corollary of the published finite union theorem in
Shoni Gilboa and Rom Pinchasi, *On the Union of Arithmetic Progressions*, SIAM
J. Discrete Math. 28 (2014), 1062--1073, DOI `10.1137/130941122`; open
manuscript `arXiv:1310.4348`.

## Corollary

Fix `C>=1` and `epsilon>0`.  Take any `n` of the bounded-ratio progressions

    P_j = {r_j+h d_j:h>=0}

whose targets all lie in `[R,2R]`.  The differences are pairwise distinct and
`d_j<=2CR`.  Let `P_j(ell)` contain its first `ell>=2` terms.  The asymmetric
Gilboa--Pinchasi theorem gives

    |union_j P_j(ell)|
      >= c(epsilon) min(n^(1-epsilon) ell, ell^2/2).

Every term in these truncations is at most

    2R + (ell-1)2CR <= 4 C ell R.

Consequently their harmonic mass satisfies

    sum_{m in union_j P_j(ell)} 1/m
      >= c'(epsilon)/C * min(n^(1-epsilon),ell)/R.

In particular, with `ell=n`, the first `n` echoes carry at least

    c'(epsilon) n^(1-epsilon)/(C R)

harmonic mass, whereas the targets themselves carry between `n/(2R)` and
`n/R`.  Thus distinct differences prevent arbitrary collision at only an
`n^epsilon` loss.

## Why this does not close the infinite problem

A block with nonvanishing target harmonic mass may have `n` comparable to
`R`.  The proved lower bound can then be smaller than the target mass by
`R^epsilon`, and its echoes extend to scale `O(CR^2)`.  For every fixed
`epsilon`, this loss tends to infinity; the published theorem also gives
constructions showing that an epsilon-free quadratic union bound is false.

The remaining possible upgrade is not to discard the result, but to determine
whether its explicit constant dependence, repeated echo generations, and the
logarithmic scale ledger together turn the subpolynomial collision loss into a
summable tail.  That is mechanism `M25Q-15`; it remains conditional rather than
proved.

## The epsilon loss already occurs inside the exact bounded-ratio class

For `2<=d<=N`, take

    r_d=d-1,    P_d={d-1,2d-1,...,Nd-1}.

The targets and differences strictly increase and `r_d<d<=2r_d`.  Their
finite union is exactly the `N` by `N` multiplication-table set (up to deleting
the first row and translating by `-1`):

    union_d P_d = {q d-1:1<=q<=N, 2<=d<=N}.

The number of distinct multiplication-table products is `o(N^2)`.  Hence a
constant quadratic packing theorem is false even with the monotone targets and
`C=2` required here; the epsilon loss is not merely caused by arbitrary AP
starting points.

The displayed family is not target-irredundant when all `2<=d<=N` are used,
but an annular restriction repairs this completely.  Take only

    N<d<=2N,    r_d=d-1,

and again truncate every progression to its first `N` terms.  No earlier
target is covered: for the common residue `-1`, this would require one distinct
integer in `(N,2N]` to divide another, which is impossible.  The truncated
union

    {q d-1:1<=q<=N, N<d<=2N}

is a subset of the `2N` by `2N` multiplication table, so it still has
`o(N^2)` elements.  Thus a constant quadratic finite packing bound is false
even for target-irredundant batches in one target scale.  A successful theorem
really must exploit later saturation or repeated generations, not a stronger
one-generation incidence estimate.

At infinite depth the same model saturates: the prime subfamily
`p-1 (mod p)` covers every positive integer.  This is the cleanest demonstration
that finite near-packing loss and eventual component saturation must be treated
together rather than as rival explanations.

The multiplication-table result is part of Kevin Ford, *The distribution of
integers with a divisor in a given interval*, Annals of Mathematics 168 (2008),
367--433, DOI `10.4007/annals.2008.168.367`.
