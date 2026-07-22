# Erdős #679: adversarial QA of conductor truncation and multiband stress test

Date: 2026-07-22 (Asia/Hong_Kong)

Verdict: **PASS_INTERNAL_STRICT_PARTIAL**.  The theorem in
conductor_truncation_transfer.md correctly transfers the collision-free
CRT weight to an arbitrary interval when the squarefree prime-prefix modulus
is the first one exceeding the interval length.  It does not close #679,
because its zero-frequency exponent is \(o(\log X)\).

## 1. First-overrun modulus

Let \(z\) be the first selected prime for which

\[
 Q(z)=\prod_{H<p\le z}p>N.
\]

If \(z^{-}\) is the preceding selected prime, then
\(Q(z)/z=Q(z^-)\le N\).  Hence

\[
 1<{Q\over N}\le z.                                    \tag{1}
\]

The PNT gives

\[
 \log Q=\vartheta(z)-\vartheta(H).
\]

Because \(H=(\log X)^{o(1)}=o(\log X)\) and \(N\asymp X\), a test endpoint
\(2\log N\) already gives product logarithm greater than \(\log N\).
Thus \(z\ll\log X\).  Conversely,

\[
 \log Q=\log N+O(\log z)
\]

by minimality, and the PNT then gives \(z=(1+o(1))\log N\).  Therefore the
proof uses the valid uniform bound

\[
 {Q\over N}\ll\log X,                                  \tag{2}
\]

not an unstated assertion \(Q/N=1+o(1)\).

## 2. Fourier and interval Parseval normalisations

For

\[
 \widehat W(h)=Q^{-1}\sum_{a\bmod Q}W(a)e(-ha/Q),
\]

Fourier inversion and Parseval are

\[
 W(a)=\sum_{h\bmod Q}\widehat W(h)e(ha/Q),\qquad
 \sum_h|\widehat W(h)|^2={1\over Q}\sum_aW(a)^2=M_2.   \tag{3}
\]

There is no missing \(Q\) in (3).

For an interval \({\cal I}\) of \(N<Q\) consecutive integers, its residues
modulo \(Q\) are distinct even if the interval wraps through zero.  Hence,
with \(G_N(h)=\sum_{a\in{\cal I}}e(ha/Q)\),

\[
 \sum_{h\bmod Q}|G_N(h)|^2=QN.                         \tag{4}
\]

This verifies the normalisation in the high-conductor Cauchy step.

If \(C(h)=c\), then \(h=(Q/c)u\), \((u,c)=1\), so the character has period
\(c\).  Complete periods cancel for \(c>1\).  The remaining \(r=N\bmod c\)
terms can start at any residue; translation changes only a unit phase.
Parseval modulo \(c\) gives

\[
 \sum_{u\bmod c}\left|\sum_{v<r}e(uv/c)\right|^2=cr\le c^2. \tag{5}
\]

Restricting to primitive \(u\), and summing over divisors \(c\le D\), is
therefore at most

\[
 \sum_{\substack{c\mid Q\\c\le D}}c^2\le\sum_{c\le D}c^2\le D^3. \tag{6}
\]

The zero character is the unique \(c=1\) term and is explicitly excluded.
Thus neither wraparound nor a “length plus one” endpoint loss is hidden in
the low-conductor estimate.

## 3. Conductor energy law

The exact local quantities are

\[
 m_p=1-{H(1-t)\over p},\qquad
 v_p={H(1-t)^2\over p}(1-H/p),
\]

\[
 m_p^2+v_p=1-{H(1-t^2)\over p}.
\]

The CRT frequency has \(p\) in its reduced conductor exactly when its
local frequency is nonzero.  After normalising squared Fourier
coefficients by \(M_2\), these choices are independent Bernoulli variables
with

\[
 \beta_p={v_p\over m_p^2+v_p}.                         \tag{7}
\]

For \(p>H\) and \(t\ge1/2\), the denominator in (7) is at least
\(t^2\ge1/4\), so \(\beta_p\le4H/p\).  Therefore, for fixed
\(0<\theta<1\),

\[
 \begin{aligned}
 \mathbb E_2 C^\theta
 &=\prod_p(1-\beta_p+\beta_pp^\theta)\\
 &\le\exp\!\left(\sum_p\beta_pp^\theta\right)
 \le\exp\{O_\theta(Hz^\theta)\}
 =\exp\{o(\log X)\}.                                   \tag{8}
 \end{aligned}
\]

The last equality follows from
\(H=(\log X)^{o(1)}\), \(z\ll\log X\), and \(\theta<1\).  Markov gives

\[
 \mathbb P_2(C>X^\eta)\le X^{-\theta\eta+o(1)}.         \tag{9}
\]

This probability is with respect to *Fourier energy*, not uniform
frequency count; the proof uses exactly the former.

The variance ratio also has the required upper, not merely lower, bound:

\[
 \log{M_2\over\mu^2}
 \le O\!\left(H\sum_{H<p\le z}{1\over p}\right)
 =(\log X)^{o(1)}=o(\log X).                            \tag{10}
\]

Hence \(M_2/\mu^2=X^{o(1)}\).

## 4. Recombination of low and high conductors

For \(D=X^\eta\), equations (3), (6), and (10) give relative low error

\[
 {M_2^{1/2}D^{3/2}\over N\mu}
 =X^{-1+3\eta/2+o(1)}.                                 \tag{11}
\]

Equations (2)--(4), (9)--(10) give relative high error

\[
 \left({M_2\over\mu^2}\right)^{1/2}
 \left({Q\over N}\right)^{1/2}
 \mathbb P_2(C>D)^{1/2}
 =X^{-\theta\eta/2+o(1)}.                              \tag{12}
\]

Taking \(\eta=1/2,\theta=3/4\) makes (11) and (12)
\(X^{-1/4+o(1)}\) and \(X^{-3/16+o(1)}\), respectively.
All estimates are uniform in the starting point of \({\cal I}\).

The finite script verify_conductor_ledger.py independently reconstructs
the complete DFT for \(H=2\), \(Q=3\cdot5\cdot7=105\), checks every
conductor-energy product, and checks Fourier inversion on a translated
60-point interval.  Its output is recorded in
verify_conductor_ledger.out.

## 5. Critical-parameter interface

In the round-5 construction,

\[
 \log H={U\over1+\varepsilon}
 (V+\log V-c_\varepsilon),\qquad
 U=\log_3X,\quad V=\log_4X.
\]

Thus \(\log H=o(\log_2X)\), or equivalently
\(H=(\log X)^{o(1)}\).

For all but \(o(H)\) shifts \(k_j=K+j\), one has
\(\log k_j=\log H+o(\log H)\).  The integer thresholds consequently have
average

\[
 {1\over H}\sum_{j<H}r(k_j)
 ={UA\over D}\{1+o(1)\}.
\]

Since \(L=U-D+o(1)\) and
\((A/D)\{U/(U-D)\}\to1\), the critical Chernoff parameter

\[
 t=\rho={\sum_jr(k_j)\over HL}
\]

tends to one.  In particular \(t\ge1/2\) for all sufficiently large
\(X\), as required by the transfer theorem.

## 6. Multiband attempt and a strict disjoint-band barrier

Consider any collection of collision-free bands indexed by \(b\).  Band
\(b\) uses \(H_b\) shifts, a parameter \(t_b\), and a prime set
\({\cal P}_b\) with \(p>H_b\).  Assume the prime sets are pairwise disjoint,
so their zero-mode exponents and Fourier conductor budgets add.  Take
\(t_b=R_b/(H_bL_b)\), the usual Chernoff saddle for the band's aggregate
threshold \(R_b\), and put

\[
 a_b=1-t_b,\qquad
 L_b=\sum_{p\in{\cal P}_b}{1\over p},
\]

\[
 E_{\rm zero}=\sum_bH_bL_bI(t_b),\qquad
 B_C=\sum_bH_ba_b^2
       \sum_{p\in{\cal P}_b}{\log p\over p}.            \tag{13}
\]

If \(B_C=O(\log X)\), then

\[
 \boxed{E_{\rm zero}=o(\log X).}                        \tag{14}
\]

Indeed \(I(t)\le4(1-t)^2\).  Split the distinct selected primes at
\(Y=(\log X)^{1/2}\).  For \(p\le Y\), the condition \(H_b<p\) makes each
summand \(H_ba_b^2/p<1\), so their total is at most
\(O(\pi(Y))=o(\log X)\).  For \(p>Y\),

\[
 \sum_{b}\sum_{\substack{p\in{\cal P}_b\\p>Y}}
 {H_ba_b^2\over p}
 \le {B_C\over\log Y}
 =O\!\left({\log X\over\log\log X}\right).
\]

This proves (14).  Thus simply stacking disjoint collision-free bands
cannot make the zero mode strong enough while their energy-typical
conductors remain in the \(X^{O(1)}\) transfer budget.

The only apparent Fourier escape inside this framework is to reuse primes
across correlated coordinate groups.  Such groups must be merged into the
exact local factor

\[
 A_p(0)=1-{1\over p}\sum_j(1-t_j),\qquad
 \sum_{\xi\ne0}|A_p(\xi)|^2
 ={1\over p}\sum_j(1-t_j)^2
  -{1\over p^2}\left(\sum_j(1-t_j)\right)^2.           \tag{15}
\]

Whether a correlated choice can obtain a \(\log X\)-sized lower-tail
exponent while keeping the energy in transferable conductors reduces to a
new local entropy-versus-energy inequality for (15).  No such favourable
choice was found.  Reusing a prime also does not create new reciprocal
prime mass, so treating repeated appearances as independent would be
invalid.

## 7. Increment and literature boundary

Relative to round 7, the new increment is precise:

* round 7 derived (7), proposed grouping by conductor, and proved that raw
  undifferentiated \(L^2\) loses;
* round 8 proves the polynomial conductor tail (9), the short-period
  low-conductor bound (6), and the actual interval asymptotic after the
  first modulus overrun.

A targeted arXiv search found general weighted-large-sieve/Parseval work,
including Olivier Ramaré,
[*The weighted large sieve through Parseval*](https://arxiv.org/abs/2605.29470),
but no source in that search stating this specific Bernoulli
reduced-conductor transfer for the #679 CRT weight.  This is not an
exhaustive priority search, and no literature-novelty claim is certified.

Strict final status: the new transfer theorem passes internal mathematics
QA and is campaign-new.  The critical saddle parameters still meet the
zero-mode boundary proved above.  The separate large-band/small-tilt note
escapes that boundary, but its enormous full modulus introduces a new
unresolved interval-transfer problem.  Erdős #679 therefore remains open.
