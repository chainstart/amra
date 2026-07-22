# Erdős #679: internal constants and quantifiers QA for the small-tilt window

Date: 2026-07-22 (Asia/Hong_Kong)

Verdict: **PASS_ZERO_MODE_ONLY / TRANSFER_OPEN**.

## 1. Scale separation

With \(L_i=\log_iX\),

\[
 \log H=2L_2-2L_3+o(1),\qquad
 \log z=L_1/L_2.
\]

Hence \(H<z<X\) for all sufficiently large \(X\), and the selected shifts
are distinct modulo every selected prime.  Also
\(a=C/\sqrt H=o(1)\), so \(t=1-a\in(1/2,1)\).

Mertens is applied only after fixing \(\varepsilon,K,C\):

\[
 \sum_{H<p\le z}{1\over p}
 =\log\log z-\log\log H+o(1)
 =L_2-2L_3-\log2+o(1).
\]

No uniformity in a moving \(C\) or \(\varepsilon\) is claimed.

## 2. Threshold and strict inequality

The integer threshold

\[
 r(k)=\left\lceil(1+\varepsilon)
 {\log k\over\log\log k}\right\rceil-1
\]

is exactly equivalent to the strict candidate inequality.  Uniformly for
\(K\le k<K+H\),

\[
 r(k)\le
 {(2+o(1))(1+\varepsilon)L_2\over L_3}.
\]

The ceiling contributes at most one and is absorbed in the displayed
\(o(1)\) relative error.

If all coordinate conditions hold, then
\(\sum_j\nu_j\le R=\sum_jr(k_j)\).  Since \(0<t<1\),

\[
 W=t^{\sum_j\nu_j}\ge t^R,
\]

so \(1_{\rm good}\le t^{-R}W\).  The direction of the Markov inequality is
correct.

## 3. Constant ledger

Let \(G=-\log(t^{-R}\mu)\).  The exact inequalities used are

\[
 -\log(1-Ha/p)\ge Ha/p,\qquad
 -\log(1-a)=a+O(a^2).
\]

They give

\[
 {G\over L_1}
 \ge
 C\left(1-{2L_3+O(1)\over L_2}\right)
 -{(2+o(1))C(1+\varepsilon)\over L_3}
 -o(1)
 =C-o(1).                                               \tag{1}
\]

For any fixed \(C>1\), choose a fixed margin
\(\delta<(C-1)/2\).  Equation (1) gives

\[
 t^{-R}\mu\le X^{-1-\delta}
\]

for all sufficiently large \(X\).  Thus, if the interval transfer
\(\sum_IW=(1+o(1))N\mu\) were proved for \(N\asymp X\), the number of
original candidates in that interval would be at most

\[
 t^{-R}\sum_IW\le X^{-\delta+o(1)}<1.
\]

As an integer, it would be zero.

## 4. Original quantifiers

The argument is valid separately for every fixed
\(\varepsilon>0\) and every fixed lower threshold \(K>e^e\).  The tested
shifts \(K,\ldots,K+H-1\) form only a subset of the shifts required in the
original candidate definition, so every original candidate is counted by
the band-good set.  Proving the transfer uniformly on each dyadic interval
\([X,2X]\) would therefore show that, for the fixed
\((\varepsilon,K)\), only finitely many candidates exist.

Since this holds for every fixed \(K\), it would negate the first question
under its standard “threshold depends only on \(\varepsilon\)” reading.
The current note does not make that conclusion because the transfer is
open.

## 5. Energy and full-modulus boundary

The variance calculation uses the exact local identity and yields

\[
 \log(M_2/\mu^2)=O(C^2L_2).
\]

The expected log conductor is \(O(C^2L_1/L_2)\), but this is only a
geometric-mean statement.  The full modulus satisfies

\[
 \log Q=X^{1/L_2+o(1)}.
\]

The separate Farey audit shows that energy-only Cauchy on the full
conductor contains

\[
 QP_Q=\prod_p(p\beta_p)
 =\exp\{(2\log C+o(1))\pi(z)\},
\]

which diverges for the necessary \(C>1\).  The later exact ANOVA inversion
also shows that the *actual* full-conductor layer is at most \(Na^M\), hence
tiny.  Thus this divergence is a genuine failure of the energy-only
inference, not a genuine obstruction from that layer.  What remains open is
the signed combination of all high ANOVA layers; it cannot be erased merely
by quoting the small expected log conductor.

Strict QA conclusion: constants, ceilings, inequality directions, and
original quantifiers in the zero-mode theorem pass.  No interval asymptotic
or even the weaker one-sided \(N\mu X^{o(1)}\) upper bound, original-problem
closure, independent external QA, or literature novelty is certified.
