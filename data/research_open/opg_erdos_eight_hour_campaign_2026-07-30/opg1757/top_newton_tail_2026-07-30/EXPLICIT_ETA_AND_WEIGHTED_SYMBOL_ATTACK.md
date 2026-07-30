# OPG-1757: explicit-eta ledger and the remaining cubic-window lemma

Date: 2026-07-30

## 0. Status

Two conclusions must be kept separate.

1. **PROVED:** the existing polynomial-window argument can be made
   completely quantitative and gives the explicit exponent
   \[
   \boxed{\eta=1/8}.
   \]
   The proof is in `EXPLICIT_POLYNOMIAL_TOP_WINDOW_THEOREM.md`.
2. **OPEN:** the desired cubic-scale window \(d\ll k^{1/3}\) would
   follow from a rank-sensitive full-symbol bound.  Exact experiments
   strongly support such a bound with \(C=3\), but no all-rank proof is
   presently available.

## 1. Where the explicit \(1/8\) comes from

The complete loss ledger is:
\[
\begin{array}{c|c}
\text{operation}&\text{coefficient-norm cost}\\ \hline
\text{Faulhaber power sum }S_v&(56v)^v\\
\text{Newton partition for }e_u&(112u)^u\\
t^a\to(t)_{\underline q}\to(r)_{\underline q}
&(2u)^{4u}\\
\text{normalized Lagrange coefficient}
&(2^{11}u^5)^u\\
\text{difference and profile convolution}
&(2^{16}(\ell+1)^5)^\ell\\
\text{two ordinary-to-falling binomial moments}
&L^L\\
\text{retain the falling basis after degree cancellation}
&1.
\end{array}
\]
Thus the determinant at \(L=j+4\) has the explicit bound
\[
|b_{k,j}|
\le
\left(2^{18}(j+5)^6\right)^{j+4}k^j.
\tag{1}
\]
Absorbing the fixed offset \(4\) gives
\[
|b_{k,j}|\le2^{320j}j^{6j}k^j.
\tag{2}
\]
The \(4\)-Stirling ratio contributes one further power of \(d\), so
the relative tail is geometric with ratio
\[
\theta=\frac{2^{321}d^7}{k}.
\]
Any \(\eta<1/7\) follows from this ledger; \(1/8\) is the stated
round exponent.

## 2. The exact missing lemma for a cubic window

Write the eventual polynomial as
\[
b_{k,d}=\sum_{r=0}^{d}\beta_{d,r}k^{d-r},
\qquad \beta_{d,0}=1.
\]
The sufficient target is:

### Weighted full-symbol lemma (open)

There is an absolute \(C\) such that, for all \(d\ge1\) and
\(0\le r\le d\),
\[
\boxed{
|\beta_{d,r}|
\le\binom dr(Cd^2)^r.
}
\tag{3}
\]

If (3) holds, then for \(k>Cd^2\),
\[
\left|\frac{b_{k,d}}{k^d}-1\right|
\le
\left(1+\frac{Cd^2}{k}\right)^d-1
\le
\exp(Cd^3/k)-1.                                    \tag{4}
\]
Inserted termwise in the triangular \(4\)-Stirling conversion, the
same rank weighting gives positivity throughout every window
\(d=o(k^{1/3})\), and with a fixed safety constant can give
\(d\le c\,k^{1/3}\).

The already proved first-subleading formula implies the necessary
asymptotic restriction
\[
C\ge\lim_{d\to\infty}
\frac{|\beta_{d,1}|}{d^3}
=\frac{11}{18}.
\tag{5}
\]
At the small depth \(d=2\), it forces the stronger global restriction
\[
C\ge\frac{23}{8}=2.875.                            \tag{6}
\]
Thus \(C=3\) is the first natural integer candidate.

## 3. Exact growth experiment

The companion verifier reconstructs \(b_{k,d}\) from the original
finite Lagrange profiles, interpolates the complete polynomial, and
uses two unused values of \(k\) at every depth.  Through \(d=40\), all
\[
\sum_{d=1}^{40}d=820
\]
nonleading symbols satisfy (3) with \(C=3\).  The largest normalized
ratio to its proposed right side is
\[
\boxed{\frac{23}{24}}
\]
at \((d,r)=(2,1)\).  For each \(1\le d\le40\), the rank requiring the
largest value of \(C\) is \(r=1\); the required value decreases from
\(2.875\) at \(d=2\) toward the proved limit \(11/18\).

This is finite evidence only.  It is not a proof of (3).

## 4. Smallest structural gap

For
\[
F_{h,r}(z)
=\sum_{\ell\ge r}
[j^{\ell-r}]R_{\ell,h}(j)\,z^{\ell-r},
\]
the proved ranks \(r=0,1,2,3\) have singular denominators following
the pattern
\[
(1-2z)^{-(6r-1)/2}.
\]
The saddle/Gamma recurrence now proves these fixed ranks without
finite-loss interpolation.  What is missing is a bound uniform in
the rank:
\[
\boxed{
[z^n]F_{h,r}(z)
\ \text{has size at most}\
\frac{C_0^r}{r!}(n+r)^{3r+O(1)}2^n
}
\tag{7}
\]
with the same type of estimate for the finite marked differences
entering the determinant.

Equation (7), propagated through the binomial central-moment
recurrence, is the minimal analytic input expected to imply (3).
The factorial \(1/r!\) is essential: a bound merely of the form
\((C_0d^3)^r\) loses the binomial weighting and does not by itself
close the sharp cubic window.

## 5. Next attack

The most economical next proof attempt is:

1. write the all-rank saddle correction as a bivariate majorant in
   the inverse-\(s\) rank and \(z\);
2. prove that the phase-polynomial recurrence is stable under the
   weight \(r!C^{-r}(1-2z)^{3r}\);
3. prove the analogous Bernoulli/Gamma exponential bound;
4. carry the weighted norm through the three marked profiles and the
   binomial central moments;
5. compare the resulting determinant bound directly with (3).

Until Step 4 is closed, \(C=3\) and an exponent \(1/3\) remain
conjectural.

The reported experiment is reproduced by
```bash
python3 verify_explicit_polynomial_top_window.py \
  --maximum-depth 40 --maximum-profile-loss 24
```
