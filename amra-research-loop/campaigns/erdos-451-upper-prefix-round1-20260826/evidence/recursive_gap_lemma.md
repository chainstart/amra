# A proved recursive CRT covering-radius inequality

This note gives a genuine gap inequality.  It is much weaker than the open
density-scale gap lemma in `survivor_deepening.md`, but it makes the recursive
CRT loss exact.

## Definitions

For a nonempty periodic set `A subset Z` define its forward covering radius

\[
W(A)=\max_{x\in\mathbb Z}\min\{t\ge0:x+t\in A\}.
\]

Thus the largest distance between consecutive cyclic representatives is
`W(A)+1` (with the harmless convention change at adjacent representatives).

Let `q_1,...,q_m` be pairwise coprime.  For each `i`, let
`A_i subset Z/q_i Z` be any nonempty allowed set of size `d_i`.  Put

\[
A=\{n\in\mathbb Z:n\bmod q_i\in A_i\text{ for every }i\}.
\]

## The recursive lemma

> **Lemma.**  For every ordering `sigma` of the coordinates,
> \[
> W(A)\le
> \sum_{j=1}^{m}(q_{\sigma(j)}-d_{\sigma(j)})
>       \prod_{\ell<j}q_{\sigma(\ell)}.                 \tag{1}
> \]
> Consequently the minimum of the right side over all orderings is also an
> upper bound.

**Proof.**  The one-coordinate assertion is immediate: a subset of a cycle of
length `q` whose complement has `q-d` points cannot contain a missing run
longer than `q-d`.

Suppose a collection of processed coordinates has product modulus `Q`,
solution set `B`, and covering radius `W(B)`.  Add a coprime modulus `q` with
allowed set `I` of size `d`.  Given an arbitrary starting integer `x`, choose
`b in B` with

\[
x\le b\le x+W(B).
\]

Every `b+tQ` remains in `B`.  Since `gcd(Q,q)=1`, as `t` runs modulo `q` the
residues `b+tQ mod q` run through the entire `q`-cycle.  The set of acceptable
values of `t` has cardinality `d`, so from `t=0` one meets it after at most
`q-d` forward steps.  Hence

\[
W(B\cap\{n:n\bmod q\in I\})
\le W(B)+Q(q-d).                                        \tag{2}
\]

Iterating (2) proves (1).  Notice that the proof works for arbitrary local
allowed subsets, not only intervals. `square`

For two adjacent coordinates `a,b`, with complement sizes `c_a,c_b`, the two
possible contributions are `c_a+a c_b` and `c_b+b c_a`.  The first ordering is
no worse exactly when

\[
\frac{a-1}{c_a}\le\frac{b-1}{c_b}.                     \tag{3}
\]

Thus sorting by `(q_i-1)/(q_i-d_i)` minimizes the right side of (1), by the
standard adjacent-swap argument.

## Exact implication for Erdős 451

For the 451 allowed sets, `q_i=p_i`, `d_i=p_i-k`, so every complement size is
exactly `k`.  The optimal order in (3) is increasing prime order.  Write

\[
k<p_1<\cdots<p_m<2k,
\qquad Q_j=\prod_{i=1}^{j}p_i,
\qquad P_k=Q_m.
\]

Then

\[
W(\mathcal A_k)\le k\sum_{j=0}^{m-1}Q_j.               \tag{4}
\]

Because every `p_i>=k+1`,

\[
\sum_{j=0}^{m-1}Q_j
<Q_{m-1}\sum_{r\ge0}(k+1)^{-r}
=Q_{m-1}\frac{k+1}{k}.
\]

Therefore

\[
W(\mathcal A_k)<(k+1)\frac{P_k}{p_m},                  \tag{5}
\]

and, by starting the covering-radius search at `2k+1`, the desired successor
satisfies the unconditional bound

\[
n_k\le 2k+1+W(\mathcal A_k)
<2k+1+(k+1)\frac{P_k}{p_m}.                             \tag{6}
\]

By the prime number theorem `p_m=(2-o(1))k` and
`log P_k=(1+o(1))k`, so (6) is

\[
n_k\le (\tfrac12+o(1))P_k=\exp((1+o(1))k).             \tag{7}
\]

This improves the trivial representative `P_k` by an asymptotic factor two,
but does **not** change its exponential scale and does not prove Erdős's
`exp(o(k))` upper conjecture.

## Exact obstruction exposed

The induction pays `Q(q-d)` at each new coordinate because it keeps only one
seed `b` from the previous CRT box.  At the final step this is
approximately `P_k/2`.  A successful recursion must use many previous seeds
simultaneously and prove that their residues modulo the new prime hit the
allowed interval after `exp(O(m log log k))` rather than `Theta(p)` steps.
Neither density nor the current additive-energy calculation supplies that
pointwise multi-seed assertion.

## A proved multi-seed/Cauchy--Davenport refinement, and why it stalls

The preceding loss is not merely an artefact of selecting one seed.  Let `B`
be a nonempty set modulo `Q`, let `N_B=|B|`, and add a prime modulus `p` with
allowed set `I` of size `d`.  In every half-open interval `[x,x+Q)` there are
exactly `N_B` representatives of `B`.  Let `R_x` be their residues modulo `p`.
One residue modulo `p` occurs at most `ceil(Q/p)` times in an interval of
length `Q`, hence

\[
r_x:=|R_x|\ge
\left\lceil\frac{N_B}{\lceil Q/p\rceil}\right\rceil.    \tag{8}
\]

For `0<=T<p`, Cauchy--Davenport in `Z/pZ` gives

\[
|R_x+\{0,Q,2Q,\ldots,TQ\}|
\ge\min(p,r_x+T).                                       \tag{9}
\]

Since the complement of `I` has `p-d` elements, (9) must meet `I` once
`r_x+T>p-d`.  Therefore, with

\[
r=\left\lceil\frac{N_B}{\lceil Q/p\rceil}\right\rceil,
\qquad T=\max(0,p-d-r+1),
\]

one obtains the valid multi-seed bound

\[
W(B\cap I)\le (T+1)Q-1.                                \tag{10}
\]

For a processed 451 block of density `D_B=N_B/Q`, (8) supplies only
`r approximately pD_B`.  After more than `O(log k)` half-density coordinates,
`pD_B<1`, and the integral lower bound collapses to `r=1`; then (10) again
pays essentially `Q(p-d)=Qk`.  Cauchy--Davenport uses all previous seeds but
still cannot see the exponentially rare box once its projection lower bound
has fallen below one point per residue.  A successful Ruzsa/expansion route
must prove much stronger, position-specific structure of `R_x` than its
cardinality alone.
