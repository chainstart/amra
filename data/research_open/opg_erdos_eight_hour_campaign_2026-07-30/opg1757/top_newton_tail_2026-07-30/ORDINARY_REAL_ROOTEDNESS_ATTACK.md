# OPG-1757: ordinary-polynomial real-rootedness attack

Date: 2026-07-30

## 0. Status

Write
\[
b_{k,d}
=k^d-\beta^-_{d,1}k^{d-1}
+\beta^+_{d,2}k^{d-2}-\cdots.
\]
Exact reconstruction currently supports:

> **Conjecture.** For every \(d\ge1\), the polynomial
> \(k\mapsto b_{k,d}\) has \(d\) positive real zeros.

This is not yet proved.  It would, however, close the desired weighted
symbol bound with the sharp small integer \(C=3\).

## 1. Conditional route to \(C=3\)

### Proposition 1

If \(b_{k,d}\) has \(d\) nonnegative real zeros for every \(d\), then
\[
\boxed{
|[k^{d-r}]b_{k,d}|
\le\binom dr(3d^2)^r
\qquad(0\le r\le d).
}
\tag{1}
\]

### Proof

Write the roots as \(\lambda_1,\ldots,\lambda_d\ge0\).  Then
\[
b_{k,d}=\prod_{i=1}^{d}(k-\lambda_i),
\qquad
|[k^{d-r}]b_{k,d}|=e_r(\lambda_1,\ldots,\lambda_d).
\]
Maclaurin's inequality gives
\[
\left(\frac{e_r}{\binom dr}\right)^{1/r}
\le\frac{e_1}{d}.                                  \tag{2}
\]
The proved first-subleading symbol says
\[
e_1
=\frac{22d^3+147d^2+161d-258}{36}.                \tag{3}
\]
Moreover
\[
3d^3-e_1
=\frac{
86d^3-147d^2-161d+258
}{36}>0.                                           \tag{4}
\]
The numerator in (4) equals \(36\) at \(d=1,2\), and its forward
difference is
\[
6(43d^2-6d-37),
\]
which is positive for \(d\ge2\).  Thus \(e_1/d\le3d^2\), and (1)
follows from (2).
\(\square\)

As already explained in the explicit-window attack, (1) gives
\[
|b_{k,j}|
\le k^j\left(1+\frac{3j^2}{k}\right)^j
\le k^j e^{3j^3/k}.                                \tag{5}
\]
Combining (5) with the audited near-diagonal \(4\)-Stirling ratio
would prove the complete-split positive top window
\[
d\le k^{1/3}.
\]
Thus real-rootedness is not merely descriptive; it is a sufficient
publication-level bridge to the cubic scale.

## 2. Exact evidence

The independent verifier reconstructs every \(b_{k,d}\) directly from
the finite Lagrange profiles.  It uses \(d+1\) interpolation values and
two unused values of \(k\), then applies exact Sturm root counts.

Through \(d=40\), it verifies:

1. \(\deg_k b_{k,d}=d\);
2. all \(d+1\) coefficients are nonzero and have sign \((-1)^r\);
3. \(\gcd(b_{k,d},\partial_k b_{k,d})=1\);
4. the exact number of roots in \((0,\infty)\) is \(d\);
5. every coefficient satisfies the candidate \(C=3\) bound.

There are forced boundary roots
\[
\boxed{
2,3,\ldots,\left\lfloor\frac{d+3}{2}\right\rfloor.
}
\tag{6}
\]
Indeed \(b_{k,d}\) is the coefficient at loss \(d\) from degree
\(2k-4\), so it vanishes when \(d>2k-4\).  The experiment confirms
that all roots in (6) are simple.

The range \(1\le d\le40\) contains 40 exact Sturm counts, 860 strict
coefficient-sign checks, 860 weighted-\(C=3\) checks, and 420
forced-boundary-root checks.  These finite Sturm checks do not prove
the conjecture for arbitrary \(d\).

## 3. Failure of the most obvious three-term recurrence

Remove the forced roots and make the even subsequence monic:
\[
Q_n(k)
=
\frac{b_{k,2n}}
{\prod_{a=2}^{n+1}(k-a)}.
\]
The first terms are
\[
Q_1=k-21,
\]
\[
Q_2=k^2-\frac{661}{6}k+\frac{2120}{3},
\]
\[
Q_3
=k^3-\frac{869}{3}k^2
+\frac{182471}{24}k-\frac{283665}{8}.
\]
If these were a monic orthogonal-polynomial sequence, one would have
\[
Q_3=(k-a)Q_2-bQ_1.
\]
Matching the two highest available coefficients forces
\[
a=\frac{359}{2},
\qquad
b=\frac{103029}{8}.
\]
But exact subtraction gives
\[
\boxed{
(k-a)Q_2-Q_3-bQ_1=\frac{2148751}{12}\ne0.
}
\tag{7}
\]
The odd residual subsequence fails analogously, with residual
\[
\frac{55578361}{48}.
\]
Therefore the standard Favard three-term route is unavailable in this
normalization.

## 4. Failure of the naive totally-nonnegative Hessenberg route

Every monic basis has a multiplication recurrence
\[
k b_{k,d}
=b_{k,d+1}+\sum_{j=0}^{d}h_{d,j}b_{k,j}.
\tag{8}
\]
The computed \(h_{d,j}\) are positive through the tested range, but
entrywise positivity is insufficient.  In the leading multiplication
matrix, the minor with rows \((1,2)\) and columns \((2,3)\) is
\[
\det
\begin{pmatrix}
603&41889\\
73/2&13963/6
\end{pmatrix}
=\boxed{-125667}.
\tag{9}
\]
Thus this natural Hessenberg matrix is not totally nonnegative, and
oscillatory-matrix theory cannot be invoked directly.

The coefficient-triangle production matrix also contains negative
entries; its first obstruction is \(-92/21\).  A proof through total
positivity would therefore need a different basis, factorization, or
planar-network representation.

## 5. Smallest useful missing structure

By the Aissen--Schoenberg--Whitney theorem, positive real-rootedness of
\(b_{k,d}\) is equivalent to the coefficient row
\[
\left(
(-1)^r[k^{d-r}]b_{k,d}
\right)_{r=0}^{d}
\]
being a finite PF sequence.  Consequently the most targeted remaining
lemma is:

> Construct, for every \(d\), a planar network or stable multivariate
> polynomial whose one-variable specialization has the above
> coefficient row.

A weaker but still sufficient target is an inductive
real-root-preserving operator taking the pair of residual even/odd
polynomials at depth \(d\) to depth \(d+2\).  The failures in
(7)--(9) show that this operator cannot be the naive scalar
three-term recurrence or the current multiplication Hessenberg
matrix.

Reproduce the full finite search with
```bash
python3 independent_verify_ordinary_real_rootedness_attack.py \
  --maximum-depth 40
```
