# Independent audit of the critical square-root bottom window

Date: 2026-07-30

Audited file: `CRITICAL_SQRT_BOTTOM_WINDOW_THEOREM.md`

## Verdict

\[
\boxed{\text{PASS}}
\]

The fixed-constant conclusion
\[
a_{k,q_0+r}>0
\quad\text{for}\quad
k\ge9\cdot2^{58},
\qquad
r\le\left\lfloor2^{-28}\sqrt{k}\right\rfloor
\]
is a valid consequence of the already audited heat remainder and Newton
prefix estimate (39) in `GROWING_DEPTH_ATTACK.md`.

The critical function
\[
e^{-e^{-2}R^2/N}
\]
is also correct for the alternating leading-term model.  The manuscript
properly does not claim it for the exact coefficient because the current
determinant remainder stays \(O(2^{48}R^2/N)\).

## 1. Constant audit

For either parity,
\[
N=q_0+4+r\ge k/2,
\qquad
R+1\le2r+3.
\]
At the proposed boundary,
\[
2r\le2^{-27}\sqrt{k}.
\]
The threshold \(k\ge9\cdot2^{58}\) is equivalent to
\[
\sqrt{k}\ge3\cdot2^{29},
\]
and hence
\[
3\le2^{-29}\sqrt{k}.
\]
Therefore
\[
R+1\le5\cdot2^{-29}\sqrt{k}.
\]
Squaring with the full constant retained gives
\[
2^{52}(R+1)^2
\le\frac{25}{64}k
<\frac{k}{2}
\le N.
\]
No parity endpoint or floor error is hidden in this calculation.

## 2. Remainder and alternating-prefix audit

Put \(x=(R+1)^2/N\).  The previous inequality gives
\[
x\le2^{-52}.
\]
The first term of (39), which includes the uniform determinant
remainder, is therefore at most \(1/2\).

For the earlier Newton terms, the exact binomial coefficient and main
ratio satisfy
\[
\binom{N-4}{\ell}
\frac{M(R-2\ell,N-\ell)}{M(R,N)}
\le
\frac{(R^2/N)^\ell}{\ell!}.
\]
The determinant error condition makes each exact earlier determinant at
most twice its main term in magnitude.  Thus extending the finite
support to infinity gives the valid absolute bound
\[
2(e^{R^2/N}-1).
\]
Since \(R^2/N\le x\),
\[
2(e^{R^2/N}-1)
\le\frac{2x}{1-x}
\le\frac{2^{-51}}{1-2^{-52}}.
\]
Adding this to \(1/2\) remains strictly below one.  This verifies
positivity without relying on cancellation signs among the earlier
terms.

## 3. Critical main-term scaling audit

For fixed \(\ell\), direct division of the two main terms gives
\[
\begin{aligned}
&\binom{N-4}{\ell}
\frac{M(R-2\ell,N-\ell)}{M(R,N)}\\
&\quad=
\binom{N-4}{\ell}
\frac{R-2\ell}{R}
\frac{R!}{(R-2\ell)!}
N^{-2\ell}
\left(1-\frac{\ell}{N}\right)^{2N-2\ell-8}.
\end{aligned}
\]
If \(R^2/N\to\lambda\), this tends to
\[
\frac{(\lambda e^{-2})^\ell}{\ell!}.
\]
The same main-ratio inequality supplies the summable dominating
sequence \((\lambda+1)^\ell/\ell!\).  Dominated convergence therefore
justifies summing the alternating limits and yields
\[
\exp(-\lambda e^{-2}).
\]
With \(r/\sqrt{k}\to\tau\),
\(\lambda=R^2/N\to8\tau^2\), confirming
\[
\exp(-8e^{-2}\tau^2).
\]

## 4. Exact remaining obstruction

Dividing the determinant remainder (7) by its leading term gives
\[
2^{48}\frac{(R+1)^3}{RN}.
\]
When \(R^2/N\to\lambda>0\) and \(R\to\infty\), this majorant tends to
\[
2^{48}\lambda.
\]
It does not vanish.  Consequently the proof cannot exchange exact
determinants for their leading terms at general critical \(\lambda\).
The theorem's distinction between the proved small fixed window and the
unproved exact scaling limit is necessary and correct.

## 5. Verification

The new verifier checks the boundary inequalities using exact integers
and rational numbers.  It also compares exact finite main-term sums with
their stable logarithmic evaluation and tests the critical scaling
samples.  Combined with the original heat verifier and the independent
growing-depth audit:

```text
14 passed in 57.52s
```

The finite samples support the formulas but are not used to prove the
uniform window or the dominated-convergence limit.
