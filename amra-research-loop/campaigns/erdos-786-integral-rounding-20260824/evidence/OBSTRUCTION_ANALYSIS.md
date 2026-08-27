# Obstruction analysis for integral rounding

## The inherited gap is exactly integrality

The predecessor theorem supplies a feasible fractional cover of mass
`(1+o(1))N/log N`.  It does not choose a vertex.  Any black-box rounding loss
of order `log N` spends `O(N)`, and the bad-support hypergraph has neither a
bounded edge size nor a proved polynomial edge/dependency count.  Therefore
ordinary set-cover and union-bound statements do not cross the finite target.

The arithmetic information discarded by the LP is overlap: the same prime
valuation constrains many circuits, and the same integer participates in
many prime fibres.  A successful rule must use this incidence jointly.

## Exact new obstruction: minimal circuits in every power-thin tail

The unpadded edge-prime circuits from the predecessor have different
magnitude scales on their two shores.  Nonuniform padding removes that
apparent protection.

### Theorem IR.1 (moving thin-tail obstruction)

Let `(eta_K)` be any positive sequence such that `K eta_K -> infinity`.
For every sufficiently large `K`, with `N=2^K`, there exist
distinct integers

\[
a_1,\ldots,a_{s+1},b_1,\ldots,b_s\in(N^{1-\eta},N]
\]

such that

\[
\prod_{i=1}^{s+1}a_i=\prod_{j=1}^{s}b_j,             \tag{1}
\]

and (1) is support-minimal among these `2s+1` integers.  The parameter `s`
may depend on `K` and can be chosen of order `1/eta_K`.

### Proof

Put `theta_K=min(eta_K,1)` and choose `s=ceil(4/theta_K)`.  Label the `2s` edges of the odd path
`P_(2s+1)` by distinct **odd** primes.  Its bipartition has shore sizes
`s+1` and `s`.  Let `q_x` be
the product of the incident edge primes at a graph vertex `x`.  Then the
`q_x` are distinct odd integers, their products over the two shores agree,
and their unique edge-prime equations make the displayed unbalanced
relation support-minimal.

Repeated use of Bertrand's postulate bounds the `2s`-th chosen prime by
`2^(O(s))`.  Since path degrees are at most two, this gives
`max_x log_2 q_x=O(s)=o(K)` because `K theta_K -> infinity`.  Thus, for all
sufficiently large `K`, the following exponents are nonnegative.  Put
`N=2^K`.
For each vertex set

\[
c_x=\lceil\log_2q_x\rceil,\qquad e_x^{(0)}=K-c_x.
\]

Then

\[
N/2<2^{e_x^{(0)}}q_x\le N.                           \tag{2}
\]

If `L,R` are the shores of sizes `s+1,s`, respectively, let

\[
\Delta=\sum_{x\in L}e_x^{(0)}-\sum_{x\in R}e_x^{(0)}.
\]

Because `prod_L q_x=prod_R q_x`, writing each ceiling as its logarithm plus
an error in `[0,1)` gives

\[
K-(s+1)<\Delta<K+s.                                  \tag{3}
\]

Thus `Delta>0` once `K>s+1`, which follows from `K eta_K -> infinity`.
Distribute `Delta` unit decrements among the
`s+1` left exponents as evenly as possible: choose nonnegative integers
`d_x` with `sum_L d_x=Delta` and

\[
d_x\le\left\lceil\frac{\Delta}{s+1}\right\rceil
\le\frac K{s+1}+2.                                   \tag{4}
\]

Since `s=o(K)` and `max c_x=o(K)`, all
`e_x=e_x^(0)-d_x` are nonnegative for sufficiently large `K`.  Leave
the right exponents unchanged.  Equation (3) now gives
`sum_L e_x=sum_R e_x`, so setting

\[
a_x=2^{e_x}q_x\ (x\in L),\qquad b_x=2^{e_x^{(0)}}q_x\ (x\in R)
\]

preserves (1).  From (2)--(4), every padded value exceeds

\[
N/2^{K/(s+1)+3}=N^{1-1/(s+1)-3/K}.                  \tag{5}
\]

Here `1/(s+1)<=theta_K/4<=eta_K/4`, while `3/K<eta_K/2` eventually.  This proves the
moving thin-tail claim.

Distinctness holds because the odd parts `q_x` are distinct.  In any signed
subrelation, the valuation at an odd edge prime gives `c_x+c_y=0`; graph
connectivity forces either the zero vector or the full bipartition vector.
Adding the prime `2` therefore creates no proper subrelation.  QED.

### Exact consequence

Deleting the lower tail `n<=N^(1-eta_K)` costs `o(N)` exactly when
`N^(-eta_K)=2^(-K eta_K)->0`.  The theorem therefore defeats every such
`o(N)` hard threshold, including a finite union of nested thresholds.
Minimal circuit length is not bounded in the residual tail.  The theorem does **not** refute the
largest-prime/smooth-core route: the construction deliberately concentrates
mass in the common prime `2` and can lie in the smooth exceptional core.

## Why the largest-prime route is not yet a proof

After deleting `y`-smooth integers and integers divisible by `p^2` for some
`p>y`, every remaining integer has a nonempty squarefree set of active primes
above `y`.  A product equality balances the incidence count at every active
prime.  It does not follow that it balances the number of integer-vertices:
the vertices are hyperedges of varying active-prime cardinality.  Choosing a
single owner prime for each integer also does not make non-owner incidences
disappear.  A valid peeling proof must bound this cross-fibre load rather
than assert private labels.

## Why coherence is separate

A cutoff-dependent random seed, ILP optimum, or prime threshold can change
the status of every fixed integer infinitely often.  Even stabilization of
individual decisions is insufficient without a zero-upper-density deletion
bound.  Furthermore admissible blocks do not concatenate: `2*3=6` already
crosses the admissible blocks `{2,3}` and `{6}`.

The representations in the next phase must therefore retain either full
prime-incidence ownership, arithmetic dependency under resampling, a
rank/coarea load, or a genuinely coherent profinite state.
