# Obstruction analysis: the missing quantity is joint repair cost

## The predecessor loss

The audited edge-prime construction assigns a distinct prime to every edge
of one `K_(s+1,s)`.  It proves that long, squarefree, support-minimal bad
relations survive all bounded-length shortcuts.  Its transversal number is
one.  Consequently it does not obstruct a global alteration: after the
relation is exposed, delete any one of its vertices.

Making many prime-disjoint copies is safe but wasteful.  A copy with shore
degrees `d-1` and `d` consumes `d(d-1)` fresh primes, so prime supply bounds
the number of copies.  More importantly, it discards the combinatorial
reuse of the same row pools.

## The retained information

Use `d-1` disjoint prime pools `P_i`, each of size `m`.  A grid independently
chooses an ordered sample of `d` distinct primes from every row pool.  The
possible column products then form a Cartesian product of size
`m^(d-1)`, even though the total number of cell labels is only `(d-1)m`.
Every grid supplies one bad relation, and a deletion must hit all grids at
once.

For a fixed deletion set, a uniformly random grid has exact marginals:

* each one of its `d` column products is uniform among the `m^(d-1)`
  possible column products;
* row `i` is uniform among the `binom(m,d)` possible row products in that
  pool.

No independence between columns or rows is claimed.  A union bound alone
shows that if

\[
 {d|D_{\rm col}|\over m^{d-1}}+
 {|D_{\rm row}|\over {m\choose d}}<1,
\]

then some grid avoids the deletion set.  Thus a transversal satisfies the
reverse inequality.  This is the precise information discarded by a
one-circuit or disjoint-packing analysis.

## Height versus dimension

Take all cell primes at most `x=N^(1/d)`.  Row products have `d` factors
and column products have `d-1`, so all vertices are at most `N`.  The prime
number theorem supplies pool size approximately `x/(2 log N)` after a
dyadic prime interval is divided among the `d-1` rows.  The leading lower
bound therefore has logarithm

\[
 (d-1)\bigl({\log N\over d}-\log(2\log N)+o(1)\bigr)-\log d.
\]

Its loss from `log N` is
`log N/d+d log log N` to first order.  Freezing `d` loses a power of `N`;
taking `d` too large loses too many factors of `log N`.  Balancing the two
terms requires `d` asymptotic to
`sqrt(log N/log log N)` and predicts the constant `2` in the target.

## Remaining checks

The calculation is not yet a theorem until the following are proved:

1. integer distinctness and support minimality for every grid;
2. the exact finite transversal inequality;
3. the binomial-term comparison in the growing-dimensional regime;
4. prime supply and integer rounding uniformly for all large `N`;
5. the high-tail and arbitrary-repair corollaries;
6. a scope proof separating this lower bound from the unresolved `o(N)`
   upper bound.
