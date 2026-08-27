# Survivor deepening: constant-width rough paths

## Theorem U.1 (constant-width support-minimal path)

Let `b` be a prime, let `K>=32`, put

\[
N=b^K,\qquad m=\lfloor K/16\rfloor,\qquad y=b^m.
\]

Let `P_K` be any finite set of primes different from `b` and smaller than
`y`.  There are `2m+1` distinct integers in

\[
(N/b^{18},N]
\]

which are all coprime to every prime in `P_K` and which support an
equal-product relation with shore sizes `m+1` and `m`.  The relation is
support-minimal.  After the padding prime `b` is omitted, its prime-incidence
graph is a path, every edge prime is greater than `y` and occurs
squarefreely, and every vertex has non-`b` prime degree one or two.

### Proof

Choose consecutive edge primes `p_1,...,p_(2m)` recursively with

\[
b^m<p_1<2b^m,\qquad p_{i-1}<p_i<2p_{i-1};
\]

Bertrand's postulate supplies every choice.  Since `2<=b`,

\[
p_i<2^i b^m\le b^{m+i}\le b^{3m}.                 \tag{1}
\]

Label the edges of the path `v_0,...,v_(2m)` in order by these primes and
let `q_i` be the product of the labels incident with `v_i`.  The `q_i` are
pairwise distinct, are coprime to `b` and to every member of `P_K`, and

\[
q_i<b^{6m}.                                        \tag{2}
\]

The even and odd path vertices have sizes `m+1` and `m`, and both shore
products of the `q_i` equal `prod_i p_i`.

For each vertex let `c_i` be the unique integer satisfying

\[
b^{c_i-1}<q_i<b^{c_i}.
\]

The inequalities are strict because `q_i` is not a power of `b`; (2) gives
`c_i<=6m`.  Put `e_i^0=K-c_i`.  The initially padded values satisfy

\[
N/b<b^{e_i^0}q_i<N.                                \tag{3}
\]

Let `L` be the even vertices and `R` the odd vertices, and define

\[
\Delta=\sum_{i\in L}e_i^0-\sum_{i\in R}e_i^0.
\]

Writing `c_i=log_b(q_i)+epsilon_i`, with `0<epsilon_i<1`, and using equality
of the two `q`-products gives

\[
K-(m+1)<\Delta<K+m.                                \tag{4}
\]

Thus `Delta` is a positive integer.  Distribute `Delta` unit decrements as
evenly as possible among the `m+1` exponents on `L`.  Every decrement `d_i`
satisfies

\[
d_i\le\left\lceil\frac{\Delta}{m+1}\right\rceil
\le17,                                             \tag{5}
\]

because `K=16m+r`, `0<=r<=15`, and `Delta<17m+r`.
Moreover

\[
e_i^0-d_i\ge K-6m-17=10m+r-17\ge0                 \tag{6}
\]

for `m>=2`.  Decrease the left exponents by these `d_i` and leave the right
exponents unchanged.  The total padding exponents now agree on the two
shores, so their padded products are equal.  Equations (3)--(5) place every
left value above `N/b^18`, and every right value above `N/b`.

Distinctness follows because removing the `b`-part recovers the pairwise
distinct `q_i`.  Finally, in any signed subrelation let `z_i` be the
coefficient of the vertex `v_i`.  The valuation equation at `p_i` is
`z_(i-1)+z_i=0`.  Path connectivity forces
`z_i=(-1)^i z_0`; hence either every coefficient is zero or the full path is
used with its bipartition signs.  No proper nonempty subrelation exists.
This proves the theorem.

## Theorem U.2 (sparse valuation-cylinder no-go theorem)

Fix a prime `b` and `delta>0`.  For every `K`, let `P_K` be a finite set of
primes such that

\[
b\notin P_K,\qquad \max P_K<b^{\lfloor K/16\rfloor},\qquad
\sum_{p\in P_K}\frac1p\le1-\delta.                \tag{7}
\]

Let `t_K=o(b^K)`.  Above `t_K`, suppose a deletion rule is a union of
complete fibres of

\[
\sigma_K(n)=(\nu_p(n))_{p\in P_K}.                 \tag{8}
\]

If the total deletion set has size `o(b^K)`, then for every sufficiently
large `K` it misses an entire support-minimal bad relation.  In particular,
no such rule is a transversal of the complete bad-relation hypergraph for
all sufficiently large `N`.

### Proof

Among the integers at most `N=b^K`, at most

\[
\sum_{p\in P_K}\lfloor N/p\rfloor
\le N\sum_{p\in P_K}1/p\le(1-\delta)N
\]

are divisible by a controlled prime.  The zero-signature fibre therefore
has at least `delta N` members.  If that complete fibre were selected above
the threshold, the deletion set would contain at least `delta N-t_K`
integers and would not be `o(N)`.  Hence the zero fibre is retained for all
sufficiently large `K`.

Theorem U.1 supplies a bad relation whose vertices all have zero signature
and exceed `N/b^18`.  Since `t_K=o(N)`, they also exceed `t_K` eventually.
The deletion rule misses all of them.

Finite unions of nested lower thresholds collapse to their largest cutoff
and are included.  The theorem does not include adaptive largest-prime
inspection, dense controlled-prime sets whose zero fibre has density zero,
or an arbitrary exceptional deletion outside complete fibres.

## Corollary U.3 (unaltered independent proportional rounding)

Let

\[
w_N(n)=\frac{\log(N/n)}{\log N}.
\]

At `N=b^K`, independently delete each integer `n` with probability
`q_K(n)<=g_K w_N(n)`, where `g_K=o(K)` (equivalently
`g_K=o(log N)`).  For every sufficiently large `K`, the unaltered sample is
not a transversal almost surely.

Indeed, every vertex from Theorem U.1 has `w_N(n)<18/K`, so its deletion
probability is strictly less than one eventually.  Independence gives a
strictly positive probability that all finitely many path vertices survive.
On that event the displayed bad relation is missed.  This does not refute a
subsequent dependent alteration or repair step.

## Evidence classification and remaining gaps

* U.1: `proved` by the all-parameter natural proof above; finite exact replay
  is provided separately and is not used for universal extrapolation.
* U.2 and U.3: `proved` as direct corollaries with frozen hypotheses.
* A theorem for arbitrary local, adaptive, or residue-aware rounding:
  `open` and explicitly outside the observation model.
* Any nontrivial lower bound on `tau(H_N)`: not implied; one displayed edge
  has hitting number one.
* `tau(H_N)=o(N)`, the infinite density construction, and Erdős 786: open.
* Novelty and publication priority: unchecked pending independent audit and
  literature comparison.
