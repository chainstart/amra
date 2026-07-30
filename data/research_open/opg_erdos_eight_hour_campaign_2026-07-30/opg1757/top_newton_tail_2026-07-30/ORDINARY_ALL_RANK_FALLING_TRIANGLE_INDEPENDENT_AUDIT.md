# Independent audit: all-rank falling triangle

Date: 2026-07-30

## 0. Verdict

\[
\boxed{\text{PASS}}
\]

`ORDINARY_ALL_RANK_FALLING_TRIANGLE_COROLLARY.md` correctly derives
the exact degree, leading sign, forced product, and residual degree
of every fixed falling-triangle column from the all-rank ordinary
symbol theorem.

## 1. Triangular identity

The coefficient of \(n^{d-\ell}\) in the ordinary expansion is
\[
\sum_{r=0}^{\ell}
P_r(d)\binom{d-r}{\ell-r}2^{\ell-r}.
\]
The coefficient of the same power in
\((n)_{\underline{d-j}}\) is
\[
s(d-j,d-\ell)=s_{\ell-j}(d-j).
\]
Isolating the \(j=\ell\) term gives equation (8) with the stated
sign.  Thus the polynomial extension \(\mathfrak h_\ell(d)\) is
well-defined recursively.

Since \(\deg s_m(n)=2m\), induction gives
\[
\deg\mathfrak h_\ell\le3\ell.
\]
The only possible degree-\(3\ell\) contribution is \(P_\ell(d)\):
all other first-sum terms have degree at most \(3\ell-2\), and all
second-sum terms have degree at most \(3\ell-1\).  Therefore
\[
[d^{3\ell}]\mathfrak h_\ell
=[d^{3\ell}]P_\ell\ne0.
\]
This proves both exact degree \(3\ell\) and leading sign
\((-1)^\ell\).

## 2. Forced roots and quotient

For \(j\le d\le2j-1\), the falling degree \(d-j\) is strictly below
\(\lceil d/2\rceil\), the forced order at the origin of the Poisson
transform.  Hence \(h_{d,j}=0\).

There is no illicit use of a polynomial extension here: every
ordinary symbol in the triangular formula has \(r\le j\le d\), so
\(P_r(d)=\beta_{d,r}\) is in its proved range.  The \(j\) distinct
integer roots are exactly
\[
j,j+1,\ldots,2j-1.
\]
Their monic product has degree \(j\).  Division of the exact
degree-\(3j\) polynomial therefore leaves an exact degree-\(2j\)
residual with the same leading coefficient and sign.

## 3. Long-band boundary factor

In the long-recurrence triangle, taking leading coefficients gives
the degree bound \(3q+2\).  At \(d=2q\), both
\(\mathfrak h_{q+1}\) terms are in their forced-root interval.  For
the summand indexed by \(i<q\), setting \(j=q-i\) gives
\[
\mathfrak h_j(d-1-2i)=\mathfrak h_j(2j-1)=0.
\]
Thus \(\mathfrak g_q(2q)=0\) for \(q\ge1\), proving the boundary
factor.  This argument proves neither exact degree nor positivity of
\(\mathfrak g_q\); the corollary correctly avoids those claims.

## 4. Finite verifier scope

`verify_all_rank_falling_triangle_corollary.py` reproduces the exact
available columns and bands.  Those finite values audit indexing and
shifts only.  The arbitrary-rank result follows from the triangular
degree separation and forced-zero argument above.
