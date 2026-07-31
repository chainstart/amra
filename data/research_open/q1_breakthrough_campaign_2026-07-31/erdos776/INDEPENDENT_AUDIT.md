# Independent audit — Erdős #776 breakthrough package

Date: 2026-07-31

Verdict: **PASS for every statement labelled PROVED; the universal
rank-42/rank-248 gate and Erdős #776 remain open.**

The audit independently reconstructed the two Pascal peels, the
\(53\mapsto109\mapsto221\) constants, the tail-complement index at rank
42, diagonal-surplus persistence, the first-carry parameters, the
one-borrow normal form, and the cancellation of the separated high
Macaulay block. It also checked the patched boundary details:

- the first capacity comparison in (4.3) is non-strict at \(r=2\);
- Lemma 4.1 is scoped to \(c\ge0\);
- the \(x_3,\ldots,x_6\) and \(y_3,\ldots,y_6\) low tails have explicit
  nonnegative binomial lower bounds.

Independent exact stress tests found:

- 29,328 agreements between global \(\Gamma\) and local \(\gamma\) for
  \(225\le M\le10000\);
- minimum rank-three separation margin 223;
- 83,252 valid persistence transitions for \(67\le M\le5000\);
- no failure in 2,297 endpoint/random samples from the first 59 carry
  strips.

These computations audit, but do not prove, the remaining all-strip
inequality

\[
y_6\ge S_5(x_5).
\]

A final signed-lift argument subsequently proved
\(\delta_3,\delta_4,\delta_5\ge0\) on every strip and the exact right
endpoint formula
\(\gamma_5(L,L)=\binom{L-14}{2}+2L-144>0\). It localizes the still-open
gate to the stronger rank-six carry bound \(\delta_5\ge T+1\).

That fixed rank-five inequality is the exact open gate. Finite checks
through \(M=10000\) and finitely many carry strips must not be extrapolated
to it. Thus the package is a genuine symbolic reduction beyond finite
scanning, but not a solution of Erdős #776.
