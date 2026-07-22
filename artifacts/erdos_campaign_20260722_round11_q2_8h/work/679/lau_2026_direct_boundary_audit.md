# #679: Lau 2026 direct boundary and conditional-negative audit

Date: 2026-07-22

Primary source: [Cheuk Fung (Joshua) Lau, *On the Number of Prime Factors
of Consecutive Integers*, arXiv:2604.15042v2](https://arxiv.org/abs/2604.15042).
The arXiv submission history gives v1 on 2026-04-16 and v2 on
2026-06-24. The current TeX source and rendered paper were both checked.
The extracted v2 main.tex checked in this audit has SHA-256
50c31fc1861c480a67073bfe3f9cf9a95c0a04c7b4e058eec1b94223b8be17f2.

## 1. Unconditional theorem

Theorem 1.1 proves that there is a constant \(C>0\) and infinitely many
positive integers \(n\) such that

\[
 \omega(n+k)\le\Omega(n+k)\le C\log k
\]

for every integer \(k\ge2\). More directly for #679, Theorem 1.3 proves
the minus-shift version: for infinitely many positive \(n\),

\[
 \omega(n-k)\le\Omega(n-k)\le C\log k
 \qquad(1<k<n).
\]

This is a substantial improvement on Tao--Teräväinen's \(O(k)\) bound.
It does not close #679: the first target is
\((1+\varepsilon)\log k/\log\log k\), so the proved result is weaker by a
factor of order \(\log\log k\). Lau states this comparison explicitly.

## 2. What is conditional rather than proved

Lau conjectures that the \(C\log k\) order is optimal up to a constant.
For the minus shifts, that conjecture predicts that every sufficiently
large \(n\) has some \(k<n\) with roughly \(\log k\) distinct prime
factors, which would imply a negative answer to the first part of #679.

Section 7 gives a second, short-interval density conjecture and proves a
conditional theorem from it: for some fixed \(\delta>0\), every sufficiently
large \(n\) would have a \(1\ll k<n\) satisfying

\[
 \omega(n-k)>(1+\delta){\log k\over\log\log k}.
\]

Neither premise is proved in the paper. Consequently the section title
“Conditional Falsity” must not be read as an unconditional disproof.

More precisely, the sufficient conjecture asks for constants
\(1\le d<C_0\) such that every sufficiently large terminal interval
\((x-(\log(x/2))^d,x]\) contains an \(m\) with
\(\omega(m)\ge C_0\log_2m/\log_3m\). This gives a concrete alternative
interface to the Fourier-tail route, but it remains conjectural.

## 3. Interface with the present attempt

The new theorem supplies the closest known unconditional scale and makes
the present negative-direction moment attack mathematically well aligned
with the author's random-model prediction. It does not bound the exact
ultra-high-conductor signed aggregate isolated in this round. Conversely,
our low-conductor reduction does not improve Lau's pointwise
\(C\log k\) theorem to the #679 constant-one logarithmic-over-loglog
threshold.

There is an exact scale match behind the two approaches. Our block length
\(H=(\log X)^2\) corresponds to Lau's fixed-power exponent \(d=2\).
For shifts \(k\asymp H\), a #679 candidate permits only
\[
 (2+o_\varepsilon(1))(1+\varepsilon)
 {\log_2X\over\log_3X}
\]
distinct prime factors per shifted integer. Thus a theorem forcing, in
every relevant \(H\)-block, one integer with
\(\omega>C_0\log_2X/\log_3X\) for a fixed
\(C_0>2(1+\varepsilon)\) would immediately rule out the candidate. The
\(d=2\) specialization of Lau's short-interval template supplies precisely
this kind of assertion; Lau's stated weak conjecture only asks for some
pair \(1\le d<C_0\), so the specialization remains an additional
unproved target. The present Fourier analysis instead reduces its failure
to the ultra-high-conductor signed tail.

Strict status: **unconditional \(C\log k\) partial result; conditional
evidence for a negative answer; no proof or disproof of #679**.
