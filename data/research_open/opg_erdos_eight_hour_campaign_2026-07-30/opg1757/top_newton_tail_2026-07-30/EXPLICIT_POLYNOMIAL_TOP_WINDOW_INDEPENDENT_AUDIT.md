# OPG-1757 explicit one-eighth top window: independent audit

Date: 2026-07-30

## Verdict

\[
\boxed{\mathrm{PASS}}
\]

The exponent \(\eta=1/8\) and the effective threshold
\(k\ge2^{2584}\) are supported by the displayed estimates.  No
constant failure was found.

The theorem required one expository repair: its degree-cancellation
reference was ambiguous.  It now points explicitly to
`FIXED_TOP_DEPTH_ASYMPTOTIC_THEOREM.md`, Lemma 2 and equations
(12)--(14).  The effective-threshold paragraph now also derives its two
side conditions instead of only asserting them.  Neither change alters
the theorem or its constants.

The independent verifier imports no existing OPG verifier.  It rebuilds
the finite Lagrange profiles, determinant numerator, ordinary
polynomials, and shifted \(4\)-Stirling numbers from their definitions.

## 1. Faulhaber and Newton norms

Faulhaber's formula gives
\[
\|F_v\|_1
\le4v!\sum_{p=1}^{v+1}\frac1{p!}<8v!.
\]
After expanding \((\beta+r+a)^v\), the replacement of \(a^q\) by
\(F_q(t)\) costs at most \(8v!\), while the univariate expansion has
norm at most \(7^v\).  Thus
\[
\|S_v\|_1\le8\,7^vv!\le(56v)^v.
\]
Newton's recurrence, equivalently the displayed partition formula,
then gives
\[
\|P_{\beta,u}\|_1\le2^u(56u)^u=(112u)^u.
\]
The independent program checks the exact Faulhaber identities through
\(v=8\), and independently constructs the Newton polynomials for all
\(0\le\beta\le5\), \(1\le u\le5\).

## 2. Moment conversion

For a monomial \(t^ar^b\),
\[
t^a=\sum_v {a\brace v}(t)_{\underline v}.
\]
The Stirling coefficient sum is the Bell number and is at most \(a^a\).
After the exact signed-binomial moment, expansion of
\((r)_{\underline v}\) costs \(v!\le a^a\).  Since \(a\le2u\), the
total conversion factor is at most \((2u)^{4u}\).  Consequently
\[
(112u)^u(2u)^{4u}=(1792u^5)^u
\le(2^{11}u^5)^u.
\]
Thirty independently transformed polynomials agree exactly with the
raw finite Lagrange sums.

## 3. Main and exceptional profiles

The normalized main profile is the convolution of an outer falling
factor with
\[
M_{\beta,u}-2rM_{\beta+1,u-1}.
\]
The two ratios used in the theorem are respectively at most
\(8^{-u}\) and \(2^{-3u-10}u^{-5}\); the \(u=1\) second term is exactly
\(2r\).  Hence the difference bound is valid.

For the exceptional term, substituting \(r-1\) multiplies the norm of a
degree-\(2u\) polynomial by at most \(2^{2u}\).  Its two losses total
\(\ell-2\), there are \(\ell-1\) convolution positions, and the
remaining factor is \(8r\).  This yields exactly
\[
8(\ell-1)
\left(2^{13}(\ell+1)^5\right)^{\ell-2}.
\]
Direct exact profile reconstructions through the audited loss satisfy
both this exceptional bound and the final
\((2^{16}(\ell+1)^5)^\ell\) bound.

## 4. Determinant and division

At total loss \(L\), the \(2(L+1)\) determinant summands are absorbed
by \(4^L\), changing the profile base from \(2^{16}\) to \(2^{18}\).
The two input power-to-falling conversions together cost at most
\(L^L\).  Keeping the output in the falling-power basis avoids any
second \(L^L\) conversion.  Thus the averaged numerator's
falling-basis norm is bounded by
\[
\left(2^{18}(L+1)^6\right)^L.
\]

The cited marked-degree lemma cancels degree \(L\) pointwise.  Its
mark-linear degree-\(L-1\) convolution is antisymmetric under
\((J,\ell)\leftrightarrow(k-J,L-\ell)\), so the averaged numerator has
degree at most \(L-2\).  This is the exact result proved in the newly
explicit citation, not an assumption about the expected leading term.

For \(L=j+4\), evaluation and division give
\[
\frac{k^{j+2}}{2k(k-1)}
=k^j\frac{k}{2(k-1)}
\le k^j\qquad(k\ge2).
\]
Independent exact determinant numerators exhibit the stated two-degree
cancellation and divide with zero remainder by \(2k(k-1)\).

## 5. Fixed-offset absorption

For all \(j\ge1\),
\[
\begin{aligned}
\left(2^{18}(j+5)^6\right)^{j+4}
&=2^{18j+72}j^{6j+24}(1+5/j)^{6j+24}\\
&\le2^{90j}j^{6j}\,2^{13j}\,2^{217j}\\
&=2^{320j}j^{6j}.
\end{aligned}
\]
Here \(j^{24}\le2^{13j}\), while
\((1+5/j)^{6j+24}\le e^{150}<2^{217}\le2^{217j}\).
Therefore \(A=2^{320}\) is valid uniformly; no small/large-\(j\)
gap remains.

## 6. Window and effective threshold

With \(d\le k^{1/8}\),
\[
\frac{d^2}{m}\le k^{-3/4},\qquad
\frac{2Ad^7}{k}\le2Ak^{-1/8}.
\]
This gives a uniformly vanishing geometric tail and proves
\(\eta=1/8\).

At \(k_0=2^{2584}\),
\[
k_0^{1/8}=2^{323},
\qquad
2A k_0^{-1/8}
=2^{1+320-323}
=\frac14.
\]
Moreover \(k^{1/8}\le k/4\) for \(k\ge16\), so
\[
d\le m/4,\qquad 2(d+5)\le k
\]
at the stated threshold.  Finally
\[
e^{6k^{-3/4}}<2
\]
there, and the relative error is strictly below
\[
2\frac{1/4}{1-1/4}=\frac23<1.
\]
Thus the effective positivity claim, including all side conditions, is
valid.

## Verification

```bash
python3 independent_verify_explicit_polynomial_top_window.py
pytest -q test_independent_verify_explicit_polynomial_top_window.py
```
