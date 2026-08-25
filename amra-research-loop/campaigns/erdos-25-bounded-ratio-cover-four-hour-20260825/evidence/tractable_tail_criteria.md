# Exact tractable tails inside the bounded-ratio problem

Let

    U = union_j {r_j + h d_j : h >= 0},

where `r_j` and `d_j` are strictly increasing and

    0 < r_j < d_j <= C r_j

for one fixed `C`.

The results below are author-verified natural proofs.  They do not settle the
general bounded-ratio problem and have not been independently reconstructed.

## 1. Summable reciprocal moduli

If

    sum_j 1/d_j < infinity,

then `U` has natural density, and hence logarithmic density.

Indeed `1/r_j <= C/d_j`, so `sum_j 1/r_j` also converges.  Let `U_N` be the
finite periodic union of the first `N` progressions.  For `x >= 1`, the number
of points contributed by the tail is at most

    x sum_{j>N} 1/d_j + #{j>N : r_j <= x}.

Convergence of `sum 1/r_j` implies

    #{j : r_j <= x} / x -> 0.

Consequently the upper natural density of `U minus U_N` is at most
`sum_{j>N} 1/d_j`, which tends to zero.  The periodic densities of `U_N`
therefore form a Cauchy approximation to the natural density of `U`.

This isolates the hard regime: every counterexample must have
`sum_j 1/d_j = infinity`.

## 2. Pairwise-coprime moduli

If the `d_j` are pairwise coprime, `U` has natural density without any
assumption on the reciprocal sum.

For a finite subfamily, CRT independence gives complement density

    product_{j<=N} (1 - 1/d_j).

If `sum 1/d_j` diverges, these products tend to zero, so finite subunions force
the lower natural density of `U` to be one.  If the sum converges, the first
lemma applies.  Thus the density is one in the divergent case and exists by
periodic approximation in the convergent case.

More generally, suppose the graph joining `i` and `j` when
`gcd(d_i,d_j)>1` has finite chromatic number.  Each colour class has pairwise
coprime moduli.  If one colour has a divergent reciprocal sum, its union has
density one.  Otherwise the total reciprocal sum converges and the first
lemma applies.  Hence `U` again has natural density.

Therefore any counterexample must simultaneously have divergent reciprocal
sum and an infinite-chromatic gcd-dependency graph.  Pairwise target
isolation is far too weak; unbounded higher-order arithmetic dependence is
necessary.

### Why a linear target-charge potential is false

Take every prime `p` and set

    d_p = p,    r_p = p-1.

This already has `d_p <= 2 r_p` (apart from the harmless first term).  The
target `p-1` is not in any earlier class `-1 (mod q)`, since that would require
`q|p`.  Nevertheless

    sum_p 1/(p-1) = infinity,

whereas the eventual union has density at most one; in fact it is all positive
integers because `n+1` has a prime divisor.  Thus no inequality of the form

    sum of uncovered target charges <= K(C) * total periodic density loss

can hold.  The correct potential, if one exists, must allow a component to
saturate, for example through conditional entropy or negative logarithm of
the surviving fraction.  This example refutes the proposed linear packing
mechanisms but supports the saturation side of a possible dichotomy.

## 3. Finite offsets and summable affine charts

Writing `s_j=d_j-r_j`, a fixed offset `s` gives

    n in {r_j+h d_j}  iff  d_j divides n+s.

It is a translate of a set of multiples and has logarithmic density by the
Davenport--Erdos theorem.  The upper-log finite-periodic approximation from
the preceding campaign is stable under finite unions, so the conclusion holds
whenever the offsets take only finitely many values.

The same diagonal argument covers countably many affine charts if, for every
`epsilon>0`, finite periodic subfamilies can be chosen in the charts so that
the sum of their upper-log remainder bounds is below `epsilon`, and the union
of all omitted charts has upper logarithmic density below `epsilon`.  This is
a useful exact criterion, not a proof that arbitrary bounded-ratio families
admit such a decomposition.

## Remaining hard core

A counterexample, if one exists, must have all of the following:

1. divergent `sum 1/d_j`;
2. infinitely complex gcd dependence (not finite-colourable into coprime
   families);
3. infinitely many genuinely non-affine offset/slope charts with a
   nonsummable upper-log remainder;
4. recurrent intermediate coverage rather than convergence to saturation.

These necessities materially narrow the computational search, but they do not
provide the missing universal tail estimate.
