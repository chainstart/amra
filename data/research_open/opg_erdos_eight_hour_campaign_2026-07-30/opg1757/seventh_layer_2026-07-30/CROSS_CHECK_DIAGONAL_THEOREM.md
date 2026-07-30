# Cross-check with the all-orders diagonal component theorem

Date: 2026-07-30

## Result

\[
\boxed{\text{The two normalizations agree exactly.}}
\]

The diagonal theorem writes \(R=t-2\) and
\[
\Delta_R(1/n)
=\frac{R!\mathcal C_{R+2}(n)}{n^{2n-6}}
=\frac{4R}{n^2}+\frac{16R(R-1)}{n^3}+O_R(n^{-4}).
\]
Therefore
\[
\mathcal C_t(n)
=\frac4{(t-3)!}n^{2n-8}
+\frac{16}{(t-4)!}n^{2n-9}
+O_t(n^{2n-10}).                                   \tag{1}
\]
The relative second term in (1) is \(4(t-3)/n\).

On the component-layer side,
\[
\mathcal C_{2r+3}
=(n-4)_{\underline r}A_r(n)n^{2n-4r-8},
\quad
\mathcal C_{2r+4}
=(n-4)_{\underline r}B_r(n)n^{2n-4r-10}.
\]
Since
\[
(n-4)_{\underline r}
=n^r\left(1-\frac{r(r+7)}{2n}+O_r(n^{-2})\right),
\]
equation (1) gives
\[
A_r(n)=\frac4{(2r)!}\left(
n^{3r}+\frac{r(r+23)}2n^{3r-1}+O_r(n^{3r-2})
\right),
\]
\[
B_r(n)=\frac4{(2r+1)!}\left(
n^{3r+2}+\frac{r^2+23r+8}{2}n^{3r+1}
+O_r(n^{3r})
\right).
\]
These are precisely the leading-two-coefficient lemma.

At the new \(r=6\) layer this predicts
\[
[n^{18}]A_6=\frac4{12!}=\frac1{119750400},
\qquad
\frac{[n^{17}]A_6}{[n^{18}]A_6}=87,
\]
\[
[n^{20}]B_6=\frac4{13!}=\frac1{1556755200},
\qquad
\frac{[n^{19}]B_6}{[n^{20}]B_6}=91.
\]
The independently computed \(P_{15}\) and \(P_{16}\) have monic
second coefficients \(87\) and \(91\), and exactly these denominators.

## Corrected sign in equation (14)

The verifier also expands the corrected identity directly:
\[
\begin{aligned}
\left(\frac1u-a\right)\log(1+uY)-Y
={}&-u\left(aY+\frac{Y^2}{2}\right)\\
&+u^2\left(\frac{aY^2}{2}+\frac{Y^3}{3}\right)\\
&-u^3\left(\frac{aY^3}{3}+\frac{Y^4}{4}\right)\\
&+u^4\left(\frac{aY^4}{4}+\frac{Y^5}{5}\right)
+O(u^5).
\end{aligned}
\]
Thus the alternating signs in the corrected diagonal equation (14)
agree with the finite-product expansion used here.  No sign mismatch
remains.

This cross-check uses exact symbolic identities.  The finite
order-\(r=6\) comparison audits the normalization; it is not the proof
of the diagonal theorem's all-orders claim.
