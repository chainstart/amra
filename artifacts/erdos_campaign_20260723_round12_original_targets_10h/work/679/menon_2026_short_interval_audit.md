# #679: audit of Menon's July 2026 short-interval bounds

Date: 2026-07-23

The official TeX of Siddarth Menon, *Improved bounds for multiplicative
functions in almost all short intervals*, arXiv:2607.15574v1 (submitted
2026-07-17), was checked because it postdates the earlier #679 rounds.
It does not bridge the remaining growing-level gap.

Menon's general theorem controls mean-square short averages of an
arbitrary **1-bounded multiplicative function** by a pretentious-distance
term plus

\[
 { (\log_2 h)^2\over(\log h)^2}
 +{1\over(\log X)^{1-o(1)}}.
\]

The indicator \(1_{\omega(n)=r}\) is not multiplicative.  Recovering it
by a saddle-point coefficient extraction from \(z^{\omega(n)}\) at the
high levels relevant to the optimized far interface requires

\[
 z\asymp {r\over\log_2X}\gg1,
\]

because there

\[
 r\asymp_\varepsilon
 (\log_2X)^{D_0}(\log_3X)^{D_0-1},
 \qquad D_0={1+\varepsilon\over\varepsilon}>1.
\]

Thus the needed multiplicative tilt is not 1-bounded and lies outside the
theorem.  Unit-circle Fourier inversion does not reproduce the positive
saddle-point large-deviation estimate, and the theorem's additive error is
also much larger than the ultra-rare exact-level density in this regime.

Accordingly Menon's new result improves cancellation for Liouville and
other bounded multiplicative functions, but supplies neither a local law
for \(\omega=r\) with \(r\gg\log_2X\) nor a weighted far-tail estimate
under Lau's sieve measure.  It changes no closure assessment and leaves
the gap between Goudout's fixed-multiple range and the critical far cutoff
open.

Primary source: https://arxiv.org/abs/2607.15574 (Theorems 1.1--1.3 in
the official v1 TeX).
