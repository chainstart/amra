# Leading-two-coefficient lemma for the general component layers

Date: 2026-07-30

## Lemma

Use the normalization
\[
\mathcal C_{2r+3}(n)
=(n-4)_{\underline r}A_r(n)n^{2n-4r-8},
\]
\[
\mathcal C_{2r+4}(n)
=(n-4)_{\underline r}B_r(n)n^{2n-4r-10}.
\]
Then
\[
\boxed{
A_r(n)=\frac4{(2r)!}
\left(n^{3r}+\frac{r(r+23)}2n^{3r-1}
+O_r(n^{3r-2})\right),
}
\]
and
\[
\boxed{
B_r(n)=\frac4{(2r+1)!}
\left(n^{3r+2}
+\frac{r^2+23r+8}{2}n^{3r+1}
+O_r(n^{3r})\right).
}
\]
Thus the monic normalization of \(A_r\) has a positive second
coefficient for \(r\ge1\) (the formal value is zero at \(r=0\)), and
that of \(B_r\) has a positive second coefficient for every \(r\ge0\).

This is an all-\(r\) algebraic statement, not a pattern inferred by
interpolation.

## Proof

Put \(u=1/n\), \(\rho=c-1\), and
\[
g_\rho=\frac1{2^\rho\rho!}.
\]
Expanding the finite Liu--Chow products through \(u^3\), and evaluating
the remaining finite binomial moments from
\((1+z)^\rho\), gives
\[
[u^3]\frac{W_{0,c}}{g_\rho n^{n-2}}
=\frac72\rho(\rho-1)(15\rho-52),
\]
\[
[u^3]\frac{D_c}{g_\rho n^{n-4}}
=\frac12\rho(\rho-1)(175\rho-1304).
\]
The exact edge-orbit identities then give
\[
[u^3]\frac{W_{1,c}}{g_\rho n^{n-3}}
=2\rho(\rho-1)(35\rho-181),
\]
\[
[u^3]\frac{W_{2,c}}{g_\rho n^{n-4}}
=2\rho(\rho-1)(45\rho-368).
\]
These identities follow from elementary symmetric sums in the finite
products; no numerical fitting is used.

In a symmetrized determinant summand put
\[
R=\rho+\sigma,\qquad \delta=\rho-\sigma.
\]
The resulting \(u^3\) coefficient is
\[
-2\left(5R\delta^2+4\delta^2-13R^2+4R\right).
\]
Under the weights
\(\binom R\rho/2^R\), one has
\(\mathbb E(\delta^2)=R\).  Therefore its weighted mean is
\[
16R(R-1).
\]
Together with the already exact \(u^2\) term this proves, for every
fixed \(t\ge3\),
\[
\mathcal C_t(n)
=\frac4{(t-3)!}n^{2n-8}
\left(1+\frac{4(t-3)}n+O_t(n^{-2})\right).       \tag{1}
\]

Finally,
\[
(n-4)_{\underline r}
=n^r\left(1-\frac{S_r}{n}+O_r(n^{-2})\right),
\qquad
S_r=\sum_{j=4}^{r+3}j=\frac{r(r+7)}2.
\]
For \(t=2r+3\), comparison with (1) says that the second monic
coefficient of \(A_r\) is
\[
S_r+4(t-3)=\frac{r(r+23)}2.
\]
For \(t=2r+4\), the corresponding coefficient of \(B_r\) is
\[
S_r+4(t-3)=\frac{r^2+23r+8}{2}.
\]
This proves the lemma.

## Scope

The lemma strengthens “positive leading coefficient” to two exact
leading coefficients.  It supports uniform adjacent-gap estimates,
but it does **not** prove that every shifted coefficient of \(A_r\) or
\(B_r\) is positive.  That stronger sign-regularity question remains
open.
