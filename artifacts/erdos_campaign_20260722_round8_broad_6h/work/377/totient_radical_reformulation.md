# Erdős #377: a totient-radical reformulation and route autopsy

Date: 2026-07-22 (Asia/Hong_Kong)

Status: exact equivalent reformulation and a different proof interface.  No
uniform lower bound at the required scale is proved, so the original problem
remains open.

## 1. Exact statement and old-route audit

Put

\[
 B_n=\binom{2n}{n},\qquad
 S(n)=\sum_{\substack{p\le n\\p\nmid B_n}}{1\over p}.
\]

The following parts of the previous work survive audit.

* Kummer's theorem gives the exact criterion: an odd prime \(p\) is absent
  from \(B_n\) if and only if every base-\(p\) digit of \(n\) is at most
  \((p-1)/2\).
* The contribution of \(p>n^\alpha\) is \(O_\alpha(1)\) by Mertens, so the
  small-prime core is decisive.
* The round-7 discrete overlap and gap-moment ledgers are correct local
  lemmas.
* The ordinary second-derivative two-term estimate has a growing term whose
  aggregate ratio is \(\gg R/K\) on every surviving off-diagonal cell.  This
  is a proved barrier to that particular shortcut, not to Type II in
  general.

Two failures must remain explicitly separated from these correct results.

1. In an earlier high-prime interval argument, the Brun--Titchmarsh
   denominator was evaluated at the location of the interval instead of
   its much shorter length.  That inference was genuinely invalid; the
   high-prime \(O(1)\) bound survives only through the simpler Mertens
   argument.
2. A proposed pointwise \(O(j^{-2})\) bound for each digit-depth layer is
   false.  For fixed odd \(p\),
   \(n=(p^{j+1}-1)/2\) makes all \(j+1\) digits equal to
   \((p-1)/2\), so the layer contains a fixed contribution \(1/p\) for
   arbitrarily large \(j\).

Thus the old proof chain contains local results and two correctly identified
method failures, but no proof of the pointwise reciprocal-prime bound.

## 2. Exact prefix form of Kummer's condition

Write the base-\(p\) digits of \(n\) as \(d_0,d_1,\ldots\).  For every
\(a\ge1\), let \(r_a=n\bmod p^a\).  Then

\[
 p\nmid B_n
 \quad\Longleftrightarrow\quad
 r_a\le {p^a-1\over2}\quad\hbox{for every }a\ge1.       \tag{1}
\]

The forward implication follows by summing the digit bounds:

\[
 r_a\le {p-1\over2}(1+p+\cdots+p^{a-1})
 ={p^a-1\over2}.
\]

Conversely, if \(d_j\ge(p+1)/2\), then

\[
 r_{j+1}\ge {p+1\over2}p^j>{p^{j+1}-1\over2},
\]

contradicting (1).  Equivalently,

\[
 p\nmid B_n
 \quad\Longleftrightarrow\quad
 \left\{{n\over p^a}\right\}< {1\over2}
 \quad(1\le a\le\lfloor\log_p n\rfloor+1).             \tag{2}
\]

Formula (2) is the exact all-level entropy condition.  Any finite truncation
alone has a zero-class obstruction: for prescribed depths \(J_p\) and a
finite prime set \({\cal P}\), every multiple of

\[
 Q=\prod_{p\in{\cal P}}p^{J_p}
\]

passes all tests with \(a\le J_p\).  Hence a pointwise proof must couple the
tested depth to the full height of \(n\), or use information other than
independent finite CRT densities.

## 3. New paradigm: the small-prime radical of the central binomial

Let

\[
 P_n=\prod_{p\le n}p,
\qquad
 R_n=\operatorname{rad}\gcd(B_n,P_n)
     =\prod_{\substack{p\le n\\p\mid B_n}}p.            \tag{3}
\]

Then the original problem is exactly equivalent to the lower bound

\[
 \boxed{{R_n\over\varphi(R_n)}\gg\log n
        \quad\hbox{uniformly in }n.}                    \tag{4}
\]

Since \(R_n\mid P_n\), the reverse inequality

\[
 {R_n\over\varphi(R_n)}
 \le {P_n\over\varphi(P_n)}
 \sim e^\gamma\log n                                   \tag{5}
\]

is automatic.  Thus (4) says that the distinct prime support of \(B_n\)
below \(n\) is asymptotically maximal in the totient sense, up to an
absolute constant.

### Proof of equivalence

Euler products give

\[
 \log {P_n/\varphi(P_n)\over R_n/\varphi(R_n)}
 =\sum_{\substack{p\le n\\p\nmid B_n}}
   -\log(1-1/p).                                       \tag{6}
\]

Uniformly over every subset of primes,

\[
 \sum_p\left|-\log(1-1/p)-{1\over p}\right|
 \ll\sum_p{1\over p^2}<\infty.
\]

Therefore

\[
 \boxed{
 S(n)=
 \log {P_n/\varphi(P_n)\over R_n/\varphi(R_n)}+O(1).
 }                                                       \tag{7}
\]

Mertens' product theorem gives
\(P_n/\varphi(P_n)\sim e^\gamma\log n\).  Equations
(6)--(7) prove both directions of the equivalence between \(S(n)=O(1)\)
and (4).

## 4. Why this is genuinely different from the short-window ledger

The Type-I/II route tries to obtain cancellation after Fourier-expanding
selected digit conditions as \(p\) varies.  Equations (3)--(7) instead ask
for a multiplicative-support theorem about one integer \(B_n\): its
small-prime radical must contain enough reciprocal-prime mass to make its
totient ratio comparable with that of the full primorial.

A possible proof could therefore come from a lower-bound sieve for
\(\operatorname{rad}(B_n)\) weighted by
\(-\log(1-1/p)\), or from a product identity which shows that the missing
Euler factors have bounded product.  Such an argument would bypass the
short Type-II phase cells entirely.

## 5. Stress test: magnitude alone cannot prove the radical bound

The estimate

\[
 \log B_n=2n\log2+O(\log n)
\]

does not imply (4).  An integer of comparable size can be a power of 2 and
have \(R/\varphi(R)=2\), or can be supported mostly on large primes and have
a bounded totient ratio.  Even an exponential lower bound for
\(\operatorname{rad}(B_n)\) would not by itself force the inclusion of
small reciprocal-weight primes.  The proof must use the *location* of the
prime divisors, not only the size of \(B_n\) or its radical.

Likewise, the fact that every missing prime makes \(B_n\) invertible modulo
\(p\) provides no common divisibility relation among the missing primes.
Fermat congruences \(B_n^{p-1}\equiv1\pmod p\) have varying exponents and
do not combine into a suitably small fixed auxiliary integer.

## 6. A precise next theorem

The reformulation reduces #377 to the following standalone target:

> There is an absolute \(c>0\) such that, for every \(n\ge3\),
> \[
> \prod_{\substack{p\le n\\p\mid\binom{2n}{n}}}
> (1-1/p)^{-1}\ge c\log n.
> \]

It is enough to prove the same estimate using only \(p\le n^{1/3}\), since
the omitted range changes the logarithm of the product by \(O(1)\).
This weighted radical target keeps all digit depths at once and avoids the
false layer-by-layer supremum.

No lower-bound sieve or product identity establishing this theorem was
found in the present round.  Accordingly the new route is an exact,
potentially reusable equivalence, not a closure or a publishable main
theorem by itself.
