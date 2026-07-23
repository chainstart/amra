# #679: density cost of splicing the far theorem to a near-shift sieve

Date: 2026-07-23

The unconditional far-shift theorem holds for almost every *uniformly*
chosen integer.  This note quantifies when it transfers to another
probability measure and why a black-box transfer to the usual single
primorial progression is unavailable.  It is a method audit, not a no-go
result for a weighted Hardy--Ramanujan theorem tailored to that measure.

## 1. A bounded-density splice lemma

Let \({\cal I}_X=[X,2X]\cap\mathbb Z\), let \(U_X\) be its uniform
probability measure, and let \({\mathbb P}_X\) be any other probability
measure on \({\cal I}_X\).  Define its maximal density ratio by

\[
 M_X=\max_{n\in{\cal I}_X}
 {\mathbb P_X(n)\over U_X(n)}\asymp
 X\max_{n\in{\cal I}_X}\mathbb P_X(n).             \tag{1}
\]

For the far-bad event \({\cal E}_{\rm far}\) in (7) of
`hardy_ramanujan_far_shift_reduction.md`, one immediately has

\[
 \mathbb P_X({\cal E}_{\rm far})
 \le M_X U_X({\cal E}_{\rm far})
 \ll_\varepsilon {M_X\over\log X}
 K_X^{-\varepsilon/4}.                              \tag{2}
\]

Here and below we use the convenient specialization
\(D_\varepsilon=2(1+\varepsilon)/\varepsilon\), for which the general
far theorem has \(\eta_D=\varepsilon/2\).  The same discussion works with
any \(D>(1+\varepsilon)/\varepsilon\) after replacing
\(\varepsilon/4\) by \(\eta_D/2\).

In particular, the uniform far result transfers whenever, for example,

\[
 \log M_X\le {\varepsilon\over8}\log K_X.           \tag{3}
\]

This is a sufficient condition only; failure of (3) does not imply that
far bad shifts are common under \(\mathbb P_X\).

## 2. Cost of one primorial progression

Suppose a near-shift construction is supported on one residue class modulo
\(W\le X\).  That class contains at most \(X/W+1\) points in
\({\cal I}_X\).  Every probability measure supported there therefore has

\[
 M_X\gg \min(W,X).                                  \tag{4}
\]

The standard device that makes all small-prime factors of \(n-k\)
inherited from \(k\) imposes

\[
 W=\prod_{p\le w}p
\]

(or an even larger prime-power modulus).  If it is required uniformly for
all \(k\le K\), the simple collision-free implementation takes \(w\ge K\).
The prime number theorem then gives

\[
 \log M_X\ge(1+o(1))K.                              \tag{5}
\]

There are in fact two distinct obstructions at the far cutoff

\[
 K_X=\exp\{(\log_2X)^{D_\varepsilon}\}.
\]

First, \(K_X\gg\log X\).  Taking \(w\ge K_X\) would give
\(W=\exp\{(1+o(1))w\}>2X\), so the zero residue class would contain no
positive integer in \([X,2X]\).  A single feasible primorial progression
cannot inherit all small primes throughout the entire growing near range.

Second, even the much smaller primorial moduli actually used to engineer
only the initial shifts are too concentrated for the black-box comparison
(2).  For example, any \(w=(\log X)^c\) with fixed \(c>0\) gives

\[
 \log M_X\ge(1+o(1))(\log X)^c,
\]

which is eventually much larger than the available far saving

\[
 {\varepsilon\over4}\log K_X
 ={\varepsilon\over4}(\log_2X)^{D_\varepsilon}.     \tag{6}
\]

Thus (2) becomes vacuous by an enormous margin for such a measure.  The
issue persists even for \(\omega\), where fourth powers in Lau's
small-prime modulus could be removed: it is the cost of restricting to a
single primorial class, not only the prime powers, that defeats this
black-box density comparison.

## 3. Surviving route

The far theorem can still be spliced if one proves its large-deviation
bound **inside the actual weighted near-shift measure**, exploiting the
arithmetic of the weight rather than its maximal density ratio.  A second
possibility is a near construction spread over sufficiently many residue
classes that (3) holds.  Neither statement is presently proved.

Consequently the new far-shift estimate genuinely narrows the target but
does not combine automatically with Lau's product sieve.  This audit rules
out only the simplest absolute-continuity/cardinality splice and makes no
claim that a tailored weighted argument is impossible.
