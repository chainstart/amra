# Stretched-exponential equal-defect cluster theorem

## Statement

Let \(H_N\) be the hypergraph on \(\{2,\ldots,N\}\) whose edges are the
supports of equal-product relations between two disjoint finite sets of
distinct integers with unequal cardinalities.  For every sufficiently large
integer \(N\), there is a family \(\mathcal F_N\subseteq H_N\) with the
following properties.

1. Every vertex in every member of \(\mathcal F_N\) lies in
   \((N/64,N]\).
2. Every member is support-minimal after cancellation of overlap.
3. All relations have normalized cardinality defect \(-1\).
4. Every two distinct supports meet in exactly one integer.
5. The matching and transversal numbers satisfy
   \[
      \nu(\mathcal F_N)=1,
      \qquad
      \tau(\mathcal F_N)>2^{\sqrt{\log_2N}/200}.
   \]

In fact, \(\tau(\mathcal F_N)=q+1\) for a prime
\(q>2^{\lfloor\sqrt K/100\rfloor}\), where
\(K=\lfloor\log_2N\rfloor\).

## 1. Quantitative incidence host and prime allocation

Put \(K=\lfloor\log_2N\rfloor\), \(N_0=2^K\), and
\[
 Q=2^{\lfloor\sqrt K/100\rfloor}.
\]
For all large \(K\), Bertrand's postulate supplies a prime
\(Q<q<2Q\), and \(q>K\).  Let \(P\) and \(\mathcal L\) be the points and
lines of the projective plane of order \(q\).  Thus
\[
 |P|=|\mathcal L|=q^2+q+1,
 \qquad m:=q+1,
\]
every line has \(m\) points, every point lies on \(m\) lines, and any two
lines meet in exactly one point.

Set
\[
 r=\lceil\log_2(q+2)\rceil+1.
\]
There are \(2^{r-1}-1\ge q+1\) unordered nontrivial bipartitions of an
\(r\)-element set.  The prime number theorem gives, for all large \(q\),
\[
 \pi(q^6)-1>(q^2+q+1)r.
\]
Choose that many distinct odd primes below \(q^6\), and split them into
pairwise disjoint \(r\)-element blocks \(Q_x\), one for each \(x\in P\).

For every point \(x\), inject the \(q+1\) lines through \(x\) into the
unordered nontrivial bipartitions of \(Q_x\).  For an incident pair
\((x,L)\), orient the assigned bipartition arbitrarily and write
\[
 Q_x=Q^-_{x,L}\mathbin{\dot\cup}Q^+_{x,L},\qquad
 A_{x,L}=\prod_{p\in Q^-_{x,L}}p,\qquad
 B_{x,L}=\prod_{p\in Q^+_{x,L}}p.
\]
Then
\[
 a_x=A_{x,L}B_{x,L}=\prod_{p\in Q_x}p
\]
is independent of \(L\).  Distinct unordered partitions ensure that all
factors used at one point are distinct, and every factor has a nonempty
prime support disjoint from that of its partner.

Write \(\ell=\log_2q\).  For large \(q\), \(r\le\ell+3\), so
\[
 \log_2a_x\le 6r\ell\le6(\ell+3)\ell.             \tag{1}
\]
Every raw private value below uses factors from at most two point blocks and
therefore has logarithm at most \(12(\ell+3)\ell\).  Since
\[
 \ell<\frac{\sqrt K}{100}+1,
\]
the latter bound is less than \(K/4\) for all sufficiently large \(K\).
This leaves a fixed positive fraction of the \(K\)-bit host for padding.

## 2. One minimal relation per projective line

Fix a line \(L=\{x_1,\ldots,x_m\}\), in any order.  Form a path on
\(2m+1\) vertices whose consecutive edge labels are
\[
 A_{x_1,L},B_{x_1,L},A_{x_2,L},B_{x_2,L},\ldots,
 A_{x_m,L},B_{x_m,L}.                              \tag{2}
\]
The \(m\) odd path vertices have raw values \(a_{x_i}\).  The \(m+1\)
even path vertices have raw values
\[
 b_0=A_{x_1,L},\quad
 b_i=B_{x_i,L}A_{x_{i+1},L}\ (1\le i<m),\quad
 b_m=B_{x_m,L}.                                    \tag{3}
\]
Each edge label in (2) contains a prime occurring in no other edge label on
this line.  Also,
\[
 \prod_{i=1}^{m}a_{x_i}=\prod_{j=0}^{m}b_j.        \tag{4}
\]

Put \(c_x=\lceil\log_2a_x\rceil\) and use the same padded point integer
on every line through \(x\):
\[
 u_x=2^{K-c_x-2}a_x.
\]
Equation (1) makes the exponent nonnegative, and
\[
 N_0/8<u_x\le N_0/4.                               \tag{5}
\]

For (3), set \(d_j=\lceil\log_2b_j\rceil\), and initially put
\(v_j^{(0)}=2^{K-d_j}b_j\).  These values lie in \((N_0/2,N_0]\).
Since (4) holds, the ceiling discrepancy
\[
 C_L=\sum_{j=0}^{m}d_j-\sum_{i=1}^{m}c_{x_i}
\]
satisfies
\[
 -m<C_L<m+1.                                       \tag{6}
\]
The even-shore power of two must be decreased by
\[
 \Delta_L=K-C_L+2m.                                \tag{7}
\]
For large \(K\), \(q>K\), and hence
\[
 0<\Delta_L<K+3m<4(m+1).                           \tag{8}
\]
Distribute exactly \(\Delta_L\) integer decrements among the \(m+1\)
even vertices as evenly as possible.  Every decrement \(t_j\) is at most
four.  The bit bound following (1) ensures \(K-d_j-t_j\ge0\).  Define
\[
 v_j=2^{K-d_j-t_j}b_j.
\]
Equations (4) and (7) now give
\[
 \prod_{i=1}^{m}u_{x_i}=\prod_{j=0}^{m}v_j,         \tag{9}
\]
and
\[
 N_0/32<v_j\le N_0.                                \tag{10}
\]
The two shores in (9) have sizes \(m\) and \(m+1\), so the normalized
defect, oriented from the shared shore to the private shore, is \(-1\).

## 3. Distinctness and support minimality

The odd-prime support of \(u_x\) is the complete point block \(Q_x\).
A private endpoint uses a proper nonempty subset of one point block, and an
internal private vertex uses proper subsets of two different point blocks.
The blocks are globally disjoint.  At a fixed point, distinct incident lines
use distinct unordered bipartitions; two different points determine a unique
projective line.  These observations show that all private values are
globally distinct, no private value equals a shared value, and two line
supports meet only in the shared integer belonging to their unique
projective intersection point.

For support minimality, consider a cancelled subrelation on one line and let
\(\varepsilon_z\in\{-1,0,1\}\) be its coefficient at path vertex \(z\).
The valuation at a private prime on a path edge \(zz'\) gives
\[
 \varepsilon_z+\varepsilon_{z'}=0.
\]
Connectivity forces either every coefficient to vanish or the full
alternating path vector, up to sign.  Thus (9) has no proper equal-product
subrelation and is a support-minimal edge of \(H_{N_0}\).

## 4. Exact packing and transversal numbers

Let \(\mathcal F_K\) consist of the relation supports obtained from all
projective lines.  Any two meet in exactly one shared point integer, so
\(\nu(\mathcal F_K)=1\).

A private integer lies on one support, while a shared point integer lies on
exactly \(q+1\) supports.  A set of at most \(q\) arithmetic vertices, of
which \(s\) are shared, hits at most
\[
 s(q+1)+(q-s)=q(s+1)\le q^2+q<q^2+q+1
\]
line supports.  Hence \(\tau(\mathcal F_K)\ge q+1\).  Conversely, the
\(q+1\) shared point integers on any fixed projective line meet every line
support.  Therefore
\[
 \tau(\mathcal F_K)=q+1>2^{\lfloor\sqrt K/100\rfloor}. \tag{11}
\]

## 5. Every sufficiently large cutoff

For the original integer \(N\), we have \(N_0\le N<2N_0\).  Thus
\[
 (N_0/32,N_0]\subset(N/64,N],
\]
and the same family is a subfamily of \(H_N\).  Also, for all sufficiently
large \(K\),
\[
 \left\lfloor\frac{\sqrt K}{100}\right\rfloor
 >\frac{\sqrt{\log_2N}}{200}.                       \tag{12}
\]
Combining (11) and (12) proves the theorem for every sufficiently large
integer \(N\).

## Scope

This theorem strengthens the quantitative blocking number of the predecessor
equal-defect cluster while preserving its arithmetic and intersection
properties.  It is a lower-bound construction for a special subfamily.  It
does not give an upper bound on \(\tau(H_N)\), prove \(\tau(H_N)=o(N)\), or
construct an infinite density-one admissible set.
