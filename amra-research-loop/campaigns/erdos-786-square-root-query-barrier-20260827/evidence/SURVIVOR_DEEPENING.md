# Survivor deepening: a constant-factor square-root query barrier

## Theorem S.1 (square-root-scale support-minimal paths)

Fix a prime `b` and an integer `A>=4`.  For every sufficiently large `K`,
put

\[
N=b^K,\qquad h=\lfloor K/2\rfloor,\qquad
X=b^{h-A},\qquad s=\lfloor K/4\rfloor.
\]

For every finite set `P_K` of primes different from `b` and smaller than
`X`, there are `2s+1` distinct `P_K`-coprime integers in

\[
(N/b^6,N]
\]

which form a support-minimal equal-product relation with shore sizes `s+1`
and `s`.  Outside the padding prime `b`, the prime-incidence graph is a path
whose edge labels all lie in `(X,2X)`.

Thus a fixed-width relation avoids every prescribed prime below a fixed
multiplicative distance from `sqrt(N)`: for even `K`,
`X=sqrt(N)/b^A`, and for odd `K`, `X=sqrt(N)/b^(A+1/2)`.

### Proof

The prime number theorem gives

\[
\pi(2X)-\pi(X)\sim X/\log X.                       \tag{1}
\]

For fixed `b,A`, the quantity `X` grows exponentially in `K`, so the right
side of (1) dominates `K`.  Hence `(X,2X)` contains at least `2s` primes for
all sufficiently large `K`.  Choose distinct labels
`p_1<...<p_(2s)` from this interval and put them in order on the edges of
the path `v_0,...,v_(2s)`.

Let `q_i` be the product of the labels incident with `v_i`.  The `q_i` are
pairwise distinct, avoid `b P_K`, and the products over the even and odd
path vertices both equal `prod_i p_i`.  Moreover

\[
q_i<(2X)^2=4b^{2h-2A}\le b^{K-2A+2}.              \tag{2}
\]

Let `c_i=ceil(log_b q_i)` and `e_i^0=K-c_i`.  Since no `q_i` is a power of
`b`,

\[
N/b<b^{e_i^0}q_i<N,
\qquad e_i^0\ge2A-2.                               \tag{3}
\]

For the even shore `L` and odd shore `R`, define

\[
\Delta=\sum_{i\in L}e_i^0-\sum_{i\in R}e_i^0.
\]

As in the predecessor path proof, equality of the two rough-part products
and the strict ceiling errors give

\[
K-(s+1)<\Delta<K+s.                                \tag{4}
\]

Write `K=4s+r`, `0<=r<=3`.  Distribute the positive integer `Delta` as
evenly as possible among the `s+1` left exponents.  Since

\[
\Delta<5s+r<5(s+1),
\]

every decrement is at most five.  Equation (3) and `A>=4` give

\[
e_i^0-d_i\ge2A-7\ge1.                              \tag{5}
\]

After the decrements, the two total padding exponents agree.  The padded
products are equal, and every value remains above `N/b^6` by (3).

Removing the `b`-part recovers the pairwise distinct `q_i`.  In a signed
subrelation, valuation at edge label `p_i` gives
`z_(i-1)+z_i=0`; path connectivity forces the zero vector or the full
alternating bipartition vector.  The displayed relation is support-minimal.

## Theorem S.2 (deterministic square-root query dichotomy)

Let `0<=t<N/b^6`, and apply one finite rooted exact-prime-valuation decision
tree `T` uniformly to every integer in `(t,N]`.  Suppose the branch reached
by answering zero to every query terminates, omits `b`, and queries only
primes below `X`.  Let `P(T)` be its queried-prime set and

\[
Z(T)=|\{1\le n\le N:\nu_p(n)=0\text{ for every }p\in P(T)\}|.
\]

Let `D(T)` consist of `[1,t]` and all inputs classified `delete`.  Then

\[
D(T)\text{ is not a transversal},
\quad\text{or}\quad |D(T)|\ge Z(T)-t.              \tag{6}
\]

If the zero leaf is deleted, all but at most `t` members of its population
are deleted, giving the second conclusion.  If it is retained, Theorem S.1
with `P_K=P(T)` supplies a bad path above `t`; every vertex follows that
zero branch and is retained, giving the first conclusion.  Queries away
from the zero branch may use arbitrary primes and arbitrary adaptive logic.

## Theorem S.3 (shared-seed randomized square-root query bound)

Let a shared random seed `omega` select a deterministic tree `T_omega`
satisfying S.2, and apply that one tree uniformly to every input.  Put

\[
L=\operatorname*{ess\,inf}_\omega Z(T_\omega),
\qquad \mu=\mathbb E_\omega|D(T_\omega)|.
\]

If `L>t`, then

\[
\Pr_\omega(D(T_\omega)\text{ is a transversal of }H_N)
\le\frac{\mu}{L-t}.                                \tag{7}
\]

Indeed, every successful seed must label its zero leaf deleted, and then
`|D(T_omega)|>=Z(T_omega)-t>=L-t`.  Taking expectations of the resulting
pointwise indicator inequality proves (7).  No independence between the
decisions for different integers is used.

If every zero branch satisfies

\[
\sum_{p\in P(T_\omega)}1/p\le1-\delta,
\]

the union bound gives `L>=delta N`.  Consequently, for fixed `b,A,delta`,
threshold `t=o(N)`, and expected deletion `mu=o(N)`, the probability of
producing a transversal tends to zero.

## Proposition S.4 (exact square-root limitation of the path host)

No degree-two edge-prime path of the above form can have all edge labels
strictly greater than `sqrt(N)` while keeping every vertex at most `N`.
Every internal vertex contains the product of two incident labels, which
would already exceed `N` before padding.

Thus S.1 reaches the geometric boundary of this host up to a fixed factor
depending only on `b,A`.

## Evidence classification and gaps

* S.1--S.4: `proved` at author level.  The only analytic dependency beyond
  the predecessor proof is the standard dyadic-interval consequence (1) of
  the prime number theorem.
* Exact finite replays verify arithmetic identities and small-support
  minimality but do not supply the all-parameter prime count.
* Uniform deterministic adaptive trees and arbitrary shared-seed mixtures
  are covered; off-zero branches are unrestricted.
* Exact labels, nonuniform per-integer programs, fresh private per-input
  query randomness, nonterminating zero branches, observation of the padding
  prime on the zero branch, and global post-classification alteration remain
  outside scope.
* The result gives no full transversal bound, no `o(N)` construction, no
  infinite density-one set, and no solution of Erdős 786.
* Independent reconstruction, source verification for (1), and novelty
  comparison remain mandatory before promotion.
