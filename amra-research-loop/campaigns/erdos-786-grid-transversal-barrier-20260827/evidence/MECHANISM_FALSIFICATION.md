# Mechanism falsification: grid-atlas lower bounds

## M786G-01: coloured grids pass the algebra tests

Let `r=d-1` and let `P_1,...,P_r` be disjoint prime pools.  In row `i`
choose distinct primes `p_(i,1),...,p_(i,d)`.  Define

\[
 R_i=\prod_{j=1}^d p_{i,j},\qquad
 C_j=\prod_{i=1}^{r}p_{i,j}.
\]

Every cell prime occurs once in the product of the rows and once in the
product of the columns, hence `prod_i R_i=prod_j C_j`; the shore sizes are
`d-1` and `d`.  Row-pool signatures and injectivity within each row make all
`2d-1` integers distinct.

For arbitrary signed coefficients `a_i,c_j` in `{-1,0,1}`, a subproduct
equality gives `a_i+c_j=0` from the valuation at `p_(i,j)`.  Connectivity of
`K_(d-1,d)` forces all `a_i` to one common value and all `c_j` to its
negative.  Thus the only signed relations are zero and the two orientations
of the full relation.  Support minimality passes, including the stronger
arbitrary-sign test rather than only original-shore subproducts.

## M786G-02: an uncoloured pool loses row identity

If every row samples from one common pool, a fixed `d`-subset product can be
generated in any row.  The row-product universes are no longer disjoint, and
one deleted row product contributes to several row events.  The coefficient
`|D_row|/binom(m,d)` in the frozen inequality is therefore not the same.
An uncoloured atlas may merit a different analysis, but the claim that it
preserves the coloured counting and unique row identities is false.

## M786G-03: connectivity does not replace private cell labels

The valuation proof uses one equation `a_i+c_j=0` for every graph edge.  If
a prime labels several edges, its valuation gives only the sum of those
equations.  At the extreme, labelling every edge of `K_(2,3)` by one prime
makes the two row values equal to each other and the three column values
equal to each other, violating the distinct-Finset requirement before
minimality is considered.  Connectivity alone is insufficient.

## M786G-04: exact first-moment inequality survives

Choose every row as a uniformly random ordered injection of length `d`,
independently between row pools.  A fixed column is uniform on the Cartesian
column universe of size `m^(d-1)`.  The unordered set in row `i` is uniform
among `binom(m,d)` subsets.

Write `D_col` and `D_row` for the deleted vertices in the two disjoint
universes.  If `D` hits every grid, the event that the random grid meets `D`
has probability one.  The union bound, with no independence assumption,
gives

\[
 1\le {d|D_{\rm col}|\over m^{d-1}}
       +{|D_{\rm row}|\over {m\choose d}}.             \tag{F.1}
\]

Consequently

\[
 |D|\ge \min\left\{{m^{d-1}\over d},{m\choose d}\right\}.       \tag{F.2}
\]

Deleting all `m^(d-1)` possible column products hits every grid, so the
finite lower bound is sharp on the logarithmic scale whenever the first
term controls.

## M786G-05: grid columns are not independent

Within one row, the `d` cell primes are sampled without replacement.  Once
a prime appears in one column it cannot appear in another column of that
row.  Column products are therefore dependent.  The proof of (F.1) survives
because it uses only exact marginals and a union bound.

## M786G-07: fixed dimension loses a power

For fixed `d`, even an ideal pool size of order `N^(1/d)/log N` gives
`m^(d-1)=N^(1-1/d)` times logarithmic factors.  Its loss from `log N` is
`log N/d`, which dominates `sqrt(log N log log N)`.  A moving dimension is
essential for the frozen target.

## M786G-08: the growing-dimensional balance survives symbolically

Let `L=log N`, `ell=log L`, and
`d=floor(sqrt(L/ell))`.  Put `x=N^(1/d)`.  The prime-supply calculation in
M786G-10 gives

\[
 \log m={L\over d}-\log(2L)+o(1).                    \tag{F.3}
\]

Moreover `log m=(1+o(1))sqrt(L ell)`, while
`(d-1)log d=(1/2+o(1))sqrt(L ell)`.  Hence
`m>=d^(d-1)` for all sufficiently large `N`, and

\[
 {m\choose d}\ge (m/d)^d\ge m^{d-1}/d.             \tag{F.4}
\]

Using (F.2)--(F.4),

\[
\begin{aligned}
 \log\tau(H_N)
 &\ge (d-1)\log m-\log d\\
 &=L-{L\over d}-(d-1)\log(2L)+o(d)-\log d\\
 &=L-(2+o(1))\sqrt{L\ell}.                          \tag{F.5}
\end{aligned}
\]

All row products lie in `((x/2)^d,x^d]` and all column products in
`((x/2)^(d-1),x^(d-1)]`.  Therefore every grid vertex lies in

\[
 \left(N^{1-1/d}/2^{d-1},N\right]
 =\left(N\exp(-(1+o(1))\sqrt{L\ell}),N\right].       \tag{F.6}
\]

The full column universe gives the reverse grid-specific estimate with the
same logarithmic asymptotic, so the constant `2` is exact for this atlas.

## M786G-09: the column term does not always control

For `m=d=3`, `binom(3,3)=1`, whereas `m^(d-1)/d=3`.  Thus the row term in
(F.2) controls.  The optimized regime separately proves `m>=d^(d-1)`; the
shortcut for all `m>=d` is false.

## M786G-10: prime supply survives

Since `d` is asymptotic to `sqrt(L/ell)`,
`x=exp(L/d)` tends to infinity.  The prime number theorem gives

\[
 \pi(x)-\pi(x/2)=(1+o(1)){x\over2\log x}.
\]

Partition these primes among `d-1` rows and discard a remainder.  The common
pool size is

\[
 m=(1+o(1)){x\over2(d-1)\log x}
  =(1+o(1)){x\over2L},                               \tag{F.7}
\]

because `d log x=L` and `(d-1)/d` tends to one.  The floor is negligible
since `x/L` tends to infinity.  This proves (F.3).

## M786G-11: Bertrand does not supply a dense pool

Bertrand's postulate guarantees a prime between `y` and `2y`; it does not
give asymptotic order `x/log x` primes inside the single frozen interval
`(x/2,x]`.  Repeated expanding intervals also violate the common height
budget.  The optimized proof genuinely uses a prime-counting theorem.

## M786G-12: arbitrary global repair is charged

All selected cell primes exceed `x/2`.  Hence every grid vertex has zero
valuation at every prime below `x/2`.  If a uniform valuation-query
classifier retains its terminating all-zero transcript, it retains the
entire grid atlas.  Any arbitrary second-stage repair that makes the final
set a transversal must itself hit every grid and therefore obey (F.2).

More generally, (F.5) is already a lower bound for the complete `H_N`.
Thus every deterministic transversal, and every successful realization of
an arbitrary randomized deletion procedure, has at least

\[
 T_N=N\exp(-(2+o(1))\sqrt{L\ell})
\]

deleted vertices.  For a random output `D`, the exact finite form gives
`Pr(D is a transversal)<=E|D|/T_(N,d,m)` with
`T_(N,d,m)=min(m^(d-1)/d,binom(m,d))`.

## M786G-13: the bound does not exclude all sublinear repair

The threshold `T_N` is `o(N)`.  In particular

\[
 {N/\log N\over T_N}
 =\exp((2+o(1))\sqrt{L\ell}-\log L)\longrightarrow\infty.
\]

Thus an allowed `o(N)` budget such as `N/log N` is much larger than the
proved obstruction.  A lower bound cannot supply the missing `o(N)` upper
bound or settle the infinite density problem.

## M786G-14: proof shape does not establish priority or tier

Correctness, novelty, and venue significance are distinct gates.  The grid
argument reuses a standard complete-bipartite incidence identity and a
first-moment cover bound; no priority conclusion follows from the improved
exponent alone.  Independent reconstruction and a scoped primary-source
literature audit remain mandatory before any publication-tier assessment.

## Finite replay

`verify_grid_transversal.py` exhausts the `d=m=3` grid atlas, checks every
deletion subset, replays the exact marginal identities at `d=3,m=4`, checks
signed support minimality on `K_(2,3)`, records the binomial counterexample,
and guards the height inequalities.  It is a finite check only and is not
used to infer (F.5).
