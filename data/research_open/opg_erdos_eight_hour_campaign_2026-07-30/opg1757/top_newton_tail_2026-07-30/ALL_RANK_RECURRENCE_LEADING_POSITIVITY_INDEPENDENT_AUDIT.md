# Independent audit: all-rank recurrence-leading positivity

Date: 2026-07-30

Audited target:
`ORDINARY_ALL_RANK_RECURRENCE_LEADING_POSITIVITY_THEOREM.md`

## 0. Verdict

**PASS.**  I found no sign, normalization, zero-counting, canonical-
product, annulus, or finite/analytic indexing gap.

The proof genuinely upgrades the finite observation to
\[
G_q=[d^{3q+2}]\mathfrak g_q(d)>0
\qquad(q\ge0).
\]
The exact finite verifier also passes.  The argument proves positivity
only of the leading coefficient of each fixed long-recurrence band,
and the theorem correctly makes no claim that the complete band is
positive at every admissible depth.

## 1. Coefficient majorant

The ratios
\[
\frac{p_{r+1}}{p_r}
=\frac{6(r-\frac16)(r+\frac16)}{r+1}<6r
\]
give
\[
p_r\le6^{r-2}(r-1)!.
\]
Also
\[
q_r=(6r-7)p_{r-1}\le6^{r-1}(r-1)!.
\]
For \(n\ge2\),
\[
\begin{aligned}
[z^n]Q^2
&\le6^{n-2}
\sum_{i=1}^{n-1}(i-1)!(n-i-1)!\\
&\le6^{n-2}(n-1)!,
\end{aligned}
\]
because each factorial product is at most \((n-2)!\) and there are
\(n-1\) terms.  Independently,
\[
6(n-1)p_{n-1}\le6^{n-2}(n-1)!.
\]
Thus the two bounds add to
\[
S_n\le2\cdot6^{n-2}(n-1)!.
\]
After \(n=r+2\) and division by \(2(3r)!\), this is exactly
\[
\lambda_r\le\frac{6^r(r+1)!}{(3r)!}.
\]
The factor two is therefore accounted for correctly.

The comparisons
\[
(3r)!\ge(r!)^3,\qquad r+1\le2^r
\]
give
\[
\lambda_r\le\frac{12^r}{(r!)^2}.
\]
Finally,
\[
\frac1{(r!)^2}\le\frac{4^r}{(2r)!}
\]
is equivalent to the central-binomial bound.  Hence
\[
M_H(x)\le\cosh(2\sqrt{12x})\le e^{2\sqrt{12x}},
\]
which proves finite order at most \(1/2\).

## 2. Rouché constants and the real zero

At \(R=21/10\), the geometric-tail ratio beginning at \(r=4\) is
\[
\frac{6R(4+2)}{13\cdot14\cdot15}=\frac9{325}.
\]
Direct exact recomputation gives
\[
\lambda_2R^2+\lambda_3R^3+
\frac{b_4R^4}{1-9/325}
=\frac{14448059591}{54058752000},
\]
and
\[
\frac{11R}{18}-1-\text{tail}
=\frac{868586809}{54058752000}>0.
\]
Thus the strict Rouché inequality holds everywhere on \(|z|=R\);
in particular, \(H\) has no boundary zero and exactly one zero,
counted with multiplicity, in the disk.

The analogous exact upper bound at \(2\) is
\[
H(2)\le-\frac{11562637}{1023096096}<0.
\]
Since \(H(0)=1\), there is a positive real zero in \((0,2)\).  It
must be the unique disk zero.  It is simple because the total
multiplicity in the disk is one.  Also
\[
H(-x)=\sum_{r\ge0}\lambda_rx^r>0
\]
excludes negative real zeros.  Every other zero therefore satisfies
\(|\rho_k|>21/10\), with strict inequality.

## 3. Hadamard product and reciprocal power sums

The maximum-modulus estimate gives order at most \(1/2<1\).
Since \(H(0)=1\), Hadamard factorization has neither a power of \(z\)
nor a nonconstant exponential factor:
\[
H(z)=\prod_k(1-z/\rho_k).
\]
The exponent of convergence of the zeros is below one, so
\(\sum_k|\rho_k|^{-1}<\infty\).  Therefore termwise logarithmic
differentiation near the origin is justified and yields
\[
-3zH'(z)/H(z)
=3\sum_{n\ge1}\left(\sum_k\rho_k^{-n}\right)z^n.
\]
Complex zeros cause no sign assumption here; they are controlled in
absolute value and occur in conjugate pairs.

## 4. Jensen and annulus estimate

Jensen at radius \(2s\), with a limiting radius if a zero lies on the
circle, gives
\[
N(s)\log2\le\log M_H(2s)\le2\sqrt{24s}.
\]
The inequalities \(\log2>2/3\) and \(\sqrt{24}<5\) imply
\[
N(s)<15\sqrt s.
\]

For the annulus
\[
R2^j<|\rho_k|\le R2^{j+1},
\]
the number of zeros is overbounded by
\[
N(R2^{j+1})<15\sqrt{2R}\,2^{j/2}.
\]
Consequently, for \(n\ge2\),
\[
\sum_{k\ne1}|\rho_k|^{-n}
<
\frac{15\sqrt{2R}}{1-2^{-(n-1/2)}}R^{-n}.
\]
The printed constant \(63\) is safely valid.  For example,
\(\sqrt{2R}=\sqrt{21/5}<21/10\) and
\(2^{-3/2}<3/8\), so the prefactor is already below
\[
\frac{15(21/10)}{1-3/8}
=\frac{252}{5}<63.
\]

The positive zero satisfies \(\rho<2\), while
\[
\left(\frac{R}{2}\right)^{100}
=\left(\frac{21}{20}\right)^{100}
>\frac{403809}{6400}>63.
\]
Thus, for all \(n\ge100\),
\[
\sum_k\rho_k^{-n}
\ge\rho^{-n}-\sum_{k\ne1}|\rho_k|^{-n}
>2^{-n}-63R^{-n}>0.
\]

## 5. Finite/analytic interface

The coefficient of \(z^n\) in the logarithmic derivative is
\(G_{n-1}\).  Hence the analytic argument covers
\[
n\ge100\quad\Longleftrightarrow\quad q=n-1\ge99.
\]
The exact verifier covers \(0\le q\le98\).  The two ranges are
adjacent and exhaustive; there is no missing \(q=99\) or duplicated
assumption.

I reran:

```bash
python3 verify_all_rank_recurrence_leading_positivity.py
pytest -q test_verify_all_rank_recurrence_leading_positivity.py
```

Both pass.  As a separate implementation, the newly added
`verify_long_recurrence_leading_log_derivative.py` derives the
second-order recurrence for \((-1)^jL_j\) and checks the first 120
logarithmic coefficients by exact rational arithmetic.

## 6. Minor presentation note

Between equations (7) and (10), it may help a reader to state
explicitly that the convolution bound and the \(p_{n-1}\) bound each
contribute \(6^{n-2}(n-1)!\), and that their sum is cancelled by the
factor \(2\) in
\(\lambda_r=S_{r+2}/(2(3r)!)\).  The printed value of \(b_r\) is
already correct; this is only an exposition suggestion.
