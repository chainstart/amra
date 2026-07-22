# Erdős #679: dyadic reduced-conductor/Farey attempt for the small-tilt window

Date: 2026-07-22 (Asia/Hong_Kong)

Status: rigorous attempted transfer with an explicit failure boundary.
Typical conductors are harmless, but an energy-only Farey/Cauchy treatment
is destroyed by the Rényi-\(1/2\) mass of extreme conductors.  Exact ANOVA
recombination shows that this explosion is only a method loss (the actual
full-conductor layer is tiny).  A successful continuation must control the
signed high-ANOVA tail by retaining local phases or alternating physical-space
structure.

## 1. Reduced-fraction decomposition

For every \(h\bmod Q\), put

\[
 C(h)={Q\over\gcd(h,Q)}.
\]

If \(C(h)=c\), write \(h=(Q/c)u\), \((u,c)=1\).  The interval error is

\[
 {\cal E}(A,N)
 =\sum_{\substack{c\mid Q\\c>1}}
   \sum_{u\bmod c}^{*}
   b_{c,u}\,e(uA/c)\,G_N(u/c),                         \tag{1}
\]

where

\[
 b_{c,u}=\widehat W(Qu/c),\qquad
 G_N(u/c)=\sum_{m=1}^{N}e(um/c).
\]

The exact conductor energy law is

\[
 \sum_{u\bmod c}^{*}|b_{c,u}|^2
 =M_2\,\mathbb P_2(C(h)=c).                            \tag{2}
\]

## 2. What direct Farey large sieve gives

For a dyadic block \(C<c\le2C\), the reduced fractions \(u/c\) have spacing
at least \(1/(4C^2)\).  The large sieve applied to the \(N\)-term interval
sequence gives

\[
 \sum_{\substack{C<c\le2C\\c\mid Q}}
 \sum_{u\bmod c}^{*}|G_N(u/c)|^2
 \ll (N+C^2)N.                                         \tag{3}
\]

Cauchy with (2) therefore gives the blockwise relative estimate

\[
 { |{\cal E}_C| \over N\mu}
 \ll
 \left({M_2\over\mu^2}\right)^{1/2}
 \mathbb P_2(C<C(h)\le2C)^{1/2}
 \left(1+{C^2\over N}\right)^{1/2}.                    \tag{4}
\]

For \(C\le\sqrt N\), exact cancellation of complete \(c\)-periods is
stronger.  It gives

\[
 \sum_{u\bmod c}^{*}|G_N(u/c)|^2\le c^2,               \tag{5}
\]

and hence, after summing the denominators in a block,

\[
 { |{\cal E}_C| \over N\mu}
 \ll
 \left({M_2\over\mu^2}\right)^{1/2}
 {C^{3/2}\over N}
 \mathbb P_2(C<C(h)\le2C)^{1/2}.                       \tag{6}
\]

For the small-tilt parameters,
\(M_2/\mu^2\le(\log X)^{O_C(1)}\), and almost all energy is on
\(C(h)=X^{o(1)}\).  Thus (6) makes every typical-conductor block
\(X^{-1+o(1)}\), even after summing the \(X^{o(1)}\) relevant blocks.
The typical part is not the obstruction.

## 3. Extreme-conductor obstruction to energy-only Cauchy

Consider the single full-conductor layer \(c=Q\).  Its energy probability is

\[
 P_Q:=\mathbb P_2(C(h)=Q)=\prod_{p\mid Q}\beta_p.       \tag{7}
\]

The exact interval Parseval bound for this one layer is

\[
 \sum_{u\bmod Q}^{*}|G_N(u/Q)|^2\le QN.
\]

Consequently energy-only Cauchy contains the factor

\[
 \left({M_2\over\mu^2}\right)^{1/2}
 \left({QP_Q\over N}\right)^{1/2}.                     \tag{8}
\]

In the small-tilt window \(Ha^2=C_0^2\), where the fixed tilt constant is
written \(C_0>1\) to avoid confusion with conductor notation.  For every
prime well above \(H\),

\[
 p\beta_p=C_0^2\{1+o(1)\}.
\]

Therefore

\[
 \log(QP_Q)
 =\sum_{H<p\le z}\log(p\beta_p)
 =(2\log C_0+o(1))\pi(z).                              \tag{9}
\]

Since \(C_0>1\), (9) tends to \(+\infty\) on the enormous scale
\(\pi(z)\asymp z/\log z\).  Thus even the single layer \(c=Q\) makes
(8) useless.  This is not caused by the total energy probability \(P_Q\),
which is tiny; it is caused by taking its square root and multiplying by
the full interval Fourier norm.

More generally, conductor-by-conductor Cauchy is controlled by a
Rényi-\(1/2\) sum such as

\[
 \sum_{c\mid Q}c^s\sqrt{\mathbb P_2(C=c)}
 =
 \prod_{p\mid Q}
 \left(\sqrt{1-\beta_p}+p^s\sqrt{\beta_p}\right),      \tag{10}
\]

and (10) is dominated by extreme subsets, not by the geometric-mean
conductor in the energy distribution.  Hence an \(L^2\) energy tail or
Markov bound for \(C(h)\) cannot, by itself, prove the desired interval
asymptotic.

## 4. Pointwise coefficient information that Cauchy discards

For a full-conductor frequency the exact local coefficient is

\[
 A_p(\xi)
 =-{a\over p}e(-\xi K/p)
   {1-e(-\xi H/p)\over1-e(-\xi/p)}.                    \tag{11}
\]

Its phase contains both the translated block \(K\) and the local geometric
sum.  Equations (7)--(10) retain only
\(\sum_{\xi\ne0}|A_p(\xi)|^2\), discarding all of this information.
The failure of (8) therefore proves a barrier only for energy-only
blockwise Cauchy/Farey arguments.

There is an exact physical-space form of the discarded cancellation.  For
a conductor \(c=\prod_{p\in S}p\), let \(F_S(n)\) be the sum of all Fourier
terms whose reduced conductor is exactly \(c\).  Local Fourier inversion
gives the ANOVA identity

\[
 \boxed{
 F_S(n)=
 \prod_{p\notin S}m_p
 \prod_{p\in S}\{W_p(n)-m_p\}.
 }                                                       \tag{12}
\]

At a selected residue,

\[
 |W_p(n)-m_p|=a(1-H/p)<a,
\]

and at every other residue,

\[
 |W_p(n)-m_p|=Ha/p<a.
\]

Thus

\[
 |F_S(n)|\le
 \left(\prod_{p\notin S}m_p\right)a^{|S|}
 \le a^{|S|}.                                         \tag{13}
\]

In particular, for the full-conductor layer \(S={\cal P}\),

\[
 \left|\sum_{n\in I}F_{\cal P}(n)\right|
 \le Na^{\pi(z)-\pi(H)},                               \tag{14}
\]

which is astronomically small.  So the very layer that makes
energy-Cauchy expression (8) explode is harmless once its local phases are
recombined exactly.  This confirms that (8) is a method loss, not evidence
that the interval asymptotic is false.

Formula (12) does not yet control the sum over all conductor subsets:
using (13) absolutely introduces the enormous binomial entropy of choosing
\(S\).  A successful hybrid must use Farey/period cancellation for the
low-cardinality subsets and (12), with more of its active/inactive
structure retained, for the high-cardinality tail.

### Conductor/degree-cutoff stress test

Let \(M=\pi(z)-\pi(H)\).  If \(|S|=r\), then
\(c=\prod_{p\in S}p\le z^r\).  Therefore every degree

\[
 r\le R=\lfloor\kappa L_2\rfloor
\]

has \(c\le X^\kappa\).  For any fixed \(\kappa<2/3\), the complete-period
bound (6), summed up to \(X^\kappa\), gives a power saving after the
polylogarithmic variance loss.  In fact this controls **every** layer with
\(c(S)\le X^\kappa\), including some layers of degree larger than
\(\kappa L_2\); the degree cutoff is only a convenient guaranteed
subcollection.

However, (13) alone bounds the absolute high-degree tail only by

\[
 \sum_{r>R}\binom Mr a^r.                              \tag{15}
\]

Here

\[
 \log M=(1+o(1))\log z={L_1\over L_2}\{1+o(1)\},
 \qquad
 -\log a=L_2-L_3+O_C(1),
\]

so \(aM\) is vastly larger than every power of \(\log X\).  Since
\(R=O(L_2)\ll aM\), expression (15) is enormous.  Hence the factor
\(a^{|S|}\) does **not** absorb combinatorial entropy at the largest degree
that period/Farey estimates control.

This remains true after restricting to genuinely high conductors.  Fix
\(\delta>0\), take
\(r=\lceil(\kappa+\delta)L_2\rceil\), and choose all \(r\) primes from
\((z/2,z]\).  Every such set has

\[
 \log c(S)\ge r\log(z/2)>\kappa L_1
\]

for large \(X\), whereas the corresponding (13)-based combinatorial upper
sum is at least

\[
 \binom{\pi(z)-\pi(z/2)}r a^r
 \ge X^{\kappa+\delta+o(1)}.                            \tag{15b}
\]

Here the final estimate follows from
\(\log\{\pi(z)-\pi(z/2)\}=(1+o(1))L_1/L_2\), while
\(-\log a\) and \(\log r\) are only \(O(L_2)\).  Thus merely replacing the
degree cutoff by the sharper conductor cutoff does not rescue absolute use
of (13).

There is a sharper pointwise description of the same entropy.  Let
\(T(n)\) be the number of primes for which
\(n\bmod p\in{\cal K}\).  At an inactive prime,

\[
 m_p+|W_p(n)-m_p|=1,
\]

whereas at an active prime

\[
 m_p+|W_p(n)-m_p|
 =1+a-{2aH\over p}\le1+a.
\]

Consequently

\[
 \sum_{S\subseteq{\cal P}}|F_S(n)|
 =\prod_{p\in{\cal P}}\{m_p+|W_p(n)-m_p|\}
 \le(1+a)^{T(n)}.                                      \tag{15a}
\]

This is much smaller than \((1+a)^M\), but it still does not close the
argument: on the natural scale \(T(n)\asymp HL\), its logarithm is
\(aT(n)\asymp aHL\asymp\log X\).  Equivalently, the absolute ANOVA degree
distribution lives around degree \(\asymp\log X\), not around the
period-controllable cutoff \(O(L_2)\).  No uniform bound on \(T(n)\) strong
enough to reverse this mismatch is available (and unusually large
\(T(n)\) is precisely the event being excluded).

The original inclusion--exclusion expansion (17 below) has alternating
signs and admits Bonferroni upper truncation, but its natural exponential
parameter is

\[
 aHL=(C_0+o(1))\log X.
\]

An even truncation must therefore have degree comparable with \(\log X\)
before it approximates the small exponential \(e^{-aHL}\); degree
\(O(L_2)\) gives a huge upper polynomial.  Such a truncation has moduli far
beyond the interval length.  This closes the two simplest hybrid variants.

The clean missing estimate for a full interval asymptotic can now be stated
without ambiguity.  For some fixed \(\kappa<2/3\), it is enough to prove the
**signed** high-ANOVA tail bound

\[
 \boxed{
 \left|
 \sum_{n\in I}
 \sum_{\substack{S\subseteq{\cal P}\\c(S)>X^\kappa}}
 F_S(n)
 \right|
 =o(N\mu),
 }                                                       \tag{16}
\]

Neither absolute use of (13) nor Bonferroni truncation proves (16).  The
conductor condition is deliberately weaker than a degree condition:
although \(c(S)>X^\kappa\) forces \(|S|>\kappa L_2\), the converse need not
hold.  Thus all period-controllable high-degree layers have already been
removed before (16).

For the negative direction of the original #679 question, (16) is stronger
than necessary.  The zero-mode argument has a fixed exponent margin
\(C_0-1>0\).  Consequently it would already suffice to prove the one-sided
bound

\[
 \sum_{n\in I}
 \sum_{\substack{S\subseteq{\cal P}\\c(S)>X^\kappa}}
 F_S(n)
 \le N\mu X^{o(1)},                                    \tag{16a}
\]

because the controllable low conductors then give
\(\sum_IW\le N\mu X^{o(1)}\), and the candidate count is
\(X^{1-C_0+o(1)}<1\).  Thus the sharp proof target for closing the problem is
the one-sided signed estimate (16a); cancellation to \(o(N\mu)\) is the
stronger target needed for an asymptotic formula.

The physical-space expansion has the same warning in a different form:

\[
 W(n)=\prod_{p\in{\cal P}}(1-a\,1_{n\bmod p\in{\cal K}})
 =\sum_{S\subseteq{\cal P}}(-a)^{|S|}
   \prod_{p\in S}1_{n\bmod p\in{\cal K}}.              \tag{17}
\]

Absolute summation of the CRT remainder in (17) loses
\((aH)^{|S|}=(C_0\sqrt H)^{|S|}\), so it also fails.  Any usable
physical-space continuation must preserve alternating signs, for example
through a high-dimensional fundamental lemma with an error uniform at the
small tilt.

## 5. Exact remaining target

The route is now sharply localised.  One must prove cancellation in (1)
which is stronger than (4) on the extreme-conductor layers, using at least
one of:

1. the phases in the product (11), equivalently the ANOVA factors (12);
2. cancellation between adjacent conductor layers;
3. an alternating, rather than absolute, truncation of (12);
4. a weighted large sieve whose norm is adapted to the actual local
   Dirichlet kernels, not merely their \(L^2\) energy.

No such estimate was completed in this round.  In particular, the
geometric-mean conductor statement must not be cited as if it implied
interval transfer; equations (8)--(10) give a concrete counter-pressure to
that inference.

Strict conclusion: direct dyadic conductor splitting handles the typical
energy, but standard Farey large sieve plus Cauchy does not close the
small-tilt window.  The one-sided signed tail estimate (16a) is the weakest
currently isolated sufficient step for the negative direction in this new
#679 route; its truth is presently unproved.
