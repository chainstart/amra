# Survivor deepening: near-square-root paths and adaptive query trees

## Theorem Q.1 (moving near-square-root rough path)

Let `b` be a prime.  For each `K`, let `0<epsilon_K<1/2` and put

\[
N=b^K,\qquad
u_K=\left\lceil(1/2-\epsilon_K)K\right\rceil,
\qquad
s_K=\left\lfloor\epsilon_K K/4\right\rfloor,
\]

and

\[
D_K=\left\lceil 8/\epsilon_K+1\right\rceil.
\]

Assume `epsilon_K^2 K -> infinity`.  For all sufficiently large `K`, and
for every finite set `P_K` of primes different from `b` and smaller than
`b^(u_K)`, there are `2s_K+1` distinct `P_K`-coprime integers in

\[
(N/b^{D_K+1},N]
\]

which form a support-minimal equal-product relation with shore sizes
`s_K+1` and `s_K`.  Outside the padding prime `b`, their prime-incidence
graph is an increasingly prime-labelled path, all edge primes exceed
`b^(u_K)`, and every vertex has rough degree one or two.

For fixed `epsilon>0`, the tail factor is constant and
`b^(u_K)>=N^(1/2-epsilon)`.  Thus the relation avoids every prescribed prime
below `N^(1/2-epsilon)`.  When `epsilon_K` tends to zero subject to the stated
condition, the observation cutoff approaches the square-root scale and the
tail exponent is `O(1/epsilon_K)`.

### Proof

Suppress the subscript `K`.  Starting above `b^u`, recursively choose
distinct primes

\[
b^u<p_1<2b^u,\qquad p_{i-1}<p_i<2p_{i-1}
\quad(2\le i\le2s)
\]

by Bertrand's postulate.  Since `2<=b`,

\[
p_i<2^i b^u\le b^{u+i}.                            \tag{1}
\]

Label the edges of `v_0,...,v_(2s)` in order by the `p_i`, and let `q_i`
be the product of labels incident with `v_i`.  The `q_i` are pairwise
distinct and coprime to `b P_K`, while (1) gives

\[
q_i<b^{2u+4s}
\le b^{(1-\epsilon)K+2}.                           \tag{2}
\]

The products of the `q_i` over the even and odd vertices both equal
`prod_i p_i`.

Let `c_i=ceil(log_b q_i)` and `e_i^0=K-c_i`.  No `q_i` is a power of `b`,
so

\[
N/b<b^{e_i^0}q_i<N,
\qquad e_i^0\ge\epsilon K-2.                       \tag{3}
\]

For the even shore `L` and odd shore `R`, define

\[
\Delta=\sum_{i\in L}e_i^0-\sum_{i\in R}e_i^0.
\]

Equality of the two rough-part products and the strict ceiling errors give

\[
K-(s+1)<\Delta<K+s.                                \tag{4}
\]

This is positive for all sufficiently large `K`.  Distribute the integer
`Delta` as evenly as possible among the `s+1` left exponents.  Since
`s=floor(epsilon K/4)>=epsilon K/8` eventually,

\[
\max_i d_i
\le\left\lceil\frac{\Delta}{s+1}\right\rceil
\le\left\lceil8/\epsilon+1\right\rceil=D.          \tag{5}
\]

The hypothesis `epsilon^2 K -> infinity` and (3) imply
`epsilon K-2-D>=0` eventually.  Decrease the left exponents by the `d_i`
and leave the right exponents unchanged.  Their sums now agree, giving an
equal-product relation; (3)--(5) put every vertex above `N/b^(D+1)`.

Removing the `b`-part recovers the pairwise distinct `q_i`, so all padded
integers are distinct.  In a signed subrelation, valuation at `p_i` gives
`z_(i-1)+z_i=0`.  Connectivity forces `z_i=(-1)^i z_0`, so either every
coefficient is zero or the full bipartition relation is used.  The support
is minimal.

## Theorem Q.2 (deterministic zero-transcript dichotomy)

Fix parameters for which Theorem Q.1 holds, and choose an integer
`0<=t<N/b^(D+1)`.  Let one finite rooted decision tree be applied uniformly
to every integer `n` in `(t,N]`.  Each internal node queries the exact value
of `nu_p(n)` for a prime `p`; subsequent queries may depend on all previous
answers.  Leaves are labelled `retain` or `delete`.

Assume the branch obtained by answering zero at every query terminates, does
not query `b`, and queries only primes below `b^u`.  Let `P(T)` be its set of
queried primes and let

\[
Z(T)=|\{1\le n\le N:\nu_p(n)=0\text{ for every }p\in P(T)\}|.
\]

Let `D(T)` contain `[1,t]` and every `n>t` classified `delete`.  Then exactly
one of the following conclusions is forced:

1. `D(T)` is not a transversal of the bad-relation hypergraph `H_N`; or
2. `|D(T)|>=Z(T)-t`.

### Proof

Every integer counted by `Z(T)` follows the all-zero branch.  If its leaf is
labelled `delete`, at least `Z(T)-t` such integers lie above the threshold
and are deleted, giving conclusion 2.

If the leaf is labelled `retain`, apply Theorem Q.1 with `P_K=P(T)`.  Every
vertex of the resulting relation exceeds `t` and is coprime to every prime
on the zero branch.  Hence every vertex follows that branch and is retained.
The whole bad support is missed, giving conclusion 1.

The tree may be arbitrarily complicated away from the zero branch; none of
those queries enter the proof.

## Theorem Q.3 (shared-seed randomized success bound)

Let a random seed `omega` choose a deterministic tree `T_omega` satisfying
the hypotheses of Q.2, and apply that one tree uniformly to every input
integer.  Define

\[
L=\inf_\omega Z(T_\omega),\qquad
\mu=\mathbb E_\omega|D(T_\omega)|,
\]

where the infimum may be replaced by an essential infimum.  If `L>t`, then

\[
\Pr_\omega(D(T_\omega)\text{ is a transversal of }H_N)
\le \frac{\mu}{L-t}.                               \tag{6}
\]

No independence between the decisions for different integers is assumed.

### Proof

For a fixed seed, a transversal cannot occur when the zero leaf is labelled
`retain`, by Q.2.  Thus success implies zero-leaf deletion, which in turn
implies `|D(T_omega)|>=Z(T_omega)-t>=L-t`.  Pointwise,

\[
1_{\{D(T_\omega)\text{ transversal}\}}
\le\frac{|D(T_\omega)|}{L-t}.
\]

Taking expectations proves (6).  The missed path is allowed to depend on
`omega`, because each realized deletion set must meet every edge of `H_N`.

## Corollary Q.4 (positive-density zero branches)

If every seedwise zero branch satisfies

\[
\sum_{p\in P(T_\omega)}\frac1p\le1-\delta
\]

for one `delta>0`, the union bound gives `Z(T_omega)>=delta N`, and therefore

\[
\Pr(D(T_\omega)\text{ transversal})
\le\frac{\mu}{\delta N-t}.                         \tag{7}
\]

For fixed `epsilon`, if `t=o(N)` and `mu=o(N)`, the success probability tends
to zero.  The deterministic theorem is recovered by using a point-mass seed.

## Exact scope and remaining gaps

* Q.1--Q.4: `proved` by the all-parameter natural proofs above; exact finite
  replay is separate supporting evidence.
* The result covers adaptive exact-valuation queries and arbitrary shared
  randomness, including correlations between vertex decisions induced by
  the seed.
* It does not cover exact-label access, a different program or fresh private
  seed for each integer, the padding prime on the zero branch, queries beyond
  the geometric cutoff, nonterminating zero paths, or global alteration
  based on already classified integers or discovered bad supports.
* The square-root boundary is exact for this path host: two incident rough
  primes above `sqrt(N)` already produce a vertex greater than `N`.
* No lower or upper bound for the full `tau(H_N)`, no density-one admissible
  set, and no solution of Erdős 786 is claimed.
* Independent reconstruction and literature novelty comparison have not yet
  been performed.
