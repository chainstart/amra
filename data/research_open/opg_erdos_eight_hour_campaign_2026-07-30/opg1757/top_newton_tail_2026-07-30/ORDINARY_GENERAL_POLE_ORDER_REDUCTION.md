# OPG-1757: reduction for the general \(3r+1\) pole-order pattern

Date: 2026-07-30

## 0. Status

The computations through \(r=6\) show
\[
B_r(t)=\frac{t^rQ_r(t)}{c_r(1-t)^{3r+1}},
\qquad \deg Q_r=3r.
\tag{1}
\]
This note isolates a short sufficient condition for (1) at every
fixed rank.  One part of that condition follows from the existing
saddle recurrence; the remaining four-order determinant cancellation
has been verified through profile rank seven but is not yet proved
uniformly.  Accordingly, this note is a proof reduction and research
target, not a claimed all-\(r\) theorem.

## 1. Profile pole filtration

The recurrence strongly suggests, and direct symbolic verification in
each computed fixed rank gives,
\[
F_{h,j}(z)
=\sqrt{1-2z}\,
\frac{p_{h,j}(z)}{(1-2z)^{3j}},
\qquad
\deg p_{h,j}\le3j
\quad(h=0,1,2).
\tag{2}
\]
The assertion is exact for every \(0\le j\le8\).  The factor
\((1-2z)^{-3j}\) comes from the saddle variance and the phase/Gamma
recurrences; all apparent poles at \(z=0,1\) cancel in the normalized
profile.  This filtration is compatible with addition,
multiplication, differentiation, and the exceptional \(h=2\) term,
so a formal induction on (10)--(17) of the all-fixed-rank theorem is
the natural route to a general proof of (2).

## 2. The only missing cancellation

Define \(G_j\) as in the all-fixed-rank theorem.  The sufficient
determinant-jet statement is
\[
\boxed{
\partial_x^mG_j(\tfrac12,t)
\in
\frac{\mathbb Q[t]}{(1-t)^{3j+m-5}},
\qquad
\partial_x^mG_j(\tfrac12,t)=O(t^{j+1})
\quad(t\to\infty),
}
\tag{3}
\]
for every relevant even \(m\).  A negative exponent on the right is
interpreted as a zero or polynomial factor.

The naive bound from (2) has pole order \(3j+m-1\).  Thus (3) is
exactly a four-order cancellation in the determinant
\[
F_1F_1-F_0F_2.
\]
For the Laurent expansion
\[
\frac{F_{h,j}(z)}{\sqrt{1-2z}}
\]
at \(1-2z=0\), the leading coefficient is independent of \(h\), the
next coefficient vanishes, and the first \(h\)-dependent coefficient
is affine in \(h\).  These four leading jet relations explain the
observed cancellation, including the exceptional correction in
\(F_2\).  They have been checked exactly through \(j=8\).  What
remains is to derive them
uniformly from the amplitude and Bernoulli recurrences.

## 3. Why (3) proves the \(3r+1\) upper bounds

Assume (3).  In a term of \(H_n\), the central moment restriction is
\[
m\le2(n-j).
\]
Therefore its pole order is at most
\[
3j+m-5
\le3j+2(n-j)-5
=2n+j-5
\le3n-5.
\tag{4}
\]
Consequently,
\[
H_n(t)\in
\frac{\mathbb Q[t]}{(1-t)^{3n-5}},
\qquad
H_n(t)=O(t^{n+1}).
\tag{5}
\]
Since
\[
B_r(t)=\frac1{2t^4}\sum_{n=2}^{r+2}H_n(t),
\]
equation (5) gives
\[
B_r(t)\in\frac{\mathbb Q[t]}{(1-t)^{3r+1}},
\qquad
B_r(t)=O(t^{r-1}).
\tag{6}
\]
The all-fixed-rank theorem already proves that the Taylor
coefficients below \(t^r\) vanish.  Write the numerator over the
common denominator in (6) as \(t^rQ_r(t)\).  The growth at infinity
then yields
\[
\deg(t^rQ_r)-(3r+1)\le r-1,
\]
and hence
\[
\boxed{\deg Q_r\le3r.}
\tag{7}
\]
Thus the uniform determinant-jet cancellation (3) proves the
pole-order and degree *upper bounds* behind (1).

Exact equality in (1) additionally requires two nonvanishing facts:

1. the leading \((1-t)^{-(3r+1)}\) coefficient of \(H_{r+2}\) is
   nonzero; and
2. the leading \(t^{r-1}\) coefficient at infinity is nonzero.

Both hold for \(0\le r\le6\).  They should be kept separate from the
filtration theorem, since upper bounds alone do not rule out an
exceptional cancellation at a later rank.

## 4. Next proof target

The most economical next step is not another large interpolation.
It is a symbolic Laurent-jet recurrence retaining only the first four
coefficients in \(w=1-2z\), with the shift \(a\) in the main amplitude
left symbolic.  If that recurrence proves the three jet relations in
Section 2 and shows that the exceptional profile supplies precisely
the required quadratic correction at \(h=2\), then (3)--(7) become an
all-rank structural theorem.
