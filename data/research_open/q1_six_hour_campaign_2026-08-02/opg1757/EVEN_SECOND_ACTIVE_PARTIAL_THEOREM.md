# OPG-1757: even second-active row — two infinite boundary bands

Date: 2026-08-02

Status: **THE TWO BOUNDARY BANDS BELOW ARE PROVED; THE FORMER OPEN
MIDDLE IS NOW CLOSED IN `EVEN_SECOND_ACTIVE_UNIVERSAL_THEOREM.md`**

## 1. Exact row and the result

Put \(u_j=1+j\beta\), \(\lambda_s=1+s\beta\), and

\[
\begin{aligned}
F_s={}&u_5^{2s-12}K_s^{(5)}
-3\lambda_s^2u_4^{2s-10}K_s^{(4)}\\
&+3\lambda_s^4u_3^{2s-8}K_s^{(3)}
-\lambda_s^6u_2^{2s-6},
\end{aligned}
\tag{1}
\]

\[
J_s=u_3^{2s-8}K_s^{(3)}-\lambda_s^2u_2^{2s-6}.
\tag{2}
\]

The three fixed kernels \(K^{(3)},K^{(4)},K^{(5)}\) are reproduced in
`verify_even_second_active_partial.py`.  For \(s\ge7\), the reduced even
second-active row is exactly

\[
\begin{aligned}
H_s(z)={}&\frac{s^{2s-12}}3
 \left(\frac{F_s(\beta)}{\beta^6}\right)_{\beta=z/s}\\
&-2(s-4)(s-1)^{2s-10}(1+z)^2
 \left(\frac{J_{s-1}(\beta)}{\beta^2}\right)_{
 \beta=z/(s-1)}.
\end{aligned}
\tag{3}
\]

It has degree \(2s-6\).  Multiplying it by the already removed positive
factor \((1+z)^{2s-14}\) recovers
\(N_{2s-10,s-4}(z)\), so coefficientwise positivity of \(H_s\) implies
positivity of the corresponding Newton row.

> **Partial even-row theorem.**  For every integer \(s\ge7\):
>
> 1. \([z^d]H_s(z)>0\) whenever
>    \(0\le d\le\min(30,2s-12)\);
> 2. \([z^{2s-6-t}]H_s(z)>0\) for \(0\le t\le5\).

The two intervals meet for \(7\le s\le21\).  Together with the direct
boundary

\[
H_6(z)=972+2480z+2760z^2+1504z^3+348z^4,
\tag{4}
\]

this proves the complete even second-active rows for even deficits
\(2\le q\le32\).  This last range statement is finite in \(q\); the two
boundary-band statements are uniform in \(s\).

## 2. The bulk comparison kernel

Write

\[
A_d(s)=\frac13[\beta^{d+6}]F_s,
\qquad
G_d(s)=[\beta^d]\lambda_{s-1}^2\frac{J_{s-1}}{\beta^2},
\tag{5}
\]

and \(N=2s-12-d\).  Direct coefficient extraction from (3) gives

\[
[z^d]H_s
=A_d(s)s^N-2(s-4)G_d(s)(s-1)^{N+2}.
\tag{6}
\]

The \(B_3\) theorem gives \(G_d(s)\ge0\).  Define the comparison kernel

\[
\boxed{
\mathcal K_s(\beta)
=\frac{F_s(\beta)}{3\beta^6}
-2(s-4)(s-1)^2\lambda_{s-1}^2
 \frac{J_{s-1}(\beta)}{\beta^2}.}
\tag{7}
\]

If \(d\le2s-12\), then \(N\ge0\), and (6) becomes

\[
\begin{aligned}
[z^d]H_s={}&s^N[\beta^d]\mathcal K_s\\
&+2(s-4)(s-1)^2G_d(s)
 \{s^N-(s-1)^N\}.
\end{aligned}
\tag{8}
\]

Thus strict positivity of \([\beta^d]\mathcal K_s\) is sufficient for
the bulk coefficient.  Notice that this is an exact implication, not an
asymptotic comparison.

For a fixed \(d\), let

\[
\sigma_d=\max\left(7,\left\lceil\frac{d+6}{2}\right\rceil\right).
\tag{9}
\]

Using

\[
 [\beta^k](1+a\beta)^M
 =a^k\binom Mk,
\tag{10}
\]

in (1), (2), and (7), the verifier expands

\[
[\beta^d]\mathcal K_{\sigma_d+x}
=\sum_{j=0}^{d+6}p_{d,j}x^j.
\tag{11}
\]

For every \(0\le d\le30\), all 682 rational numbers \(p_{d,j}\)
are strictly positive.  Equation (11) therefore proves
\([\beta^d]\mathcal K_s>0\) for every integer \(s\ge\sigma_d\).
The row only invokes this assertion when
\(s\ge\lceil(d+12)/2\rceil\), which is a stronger lower bound and hence
a subset of the proved domain, so (8) proves the first band.  Six direct
values of \(s\) and all 31 columns give 186 independent
full-convolution transcription checks.

## 3. The last six coefficients

Let \(n=s-7\ge0\).  Reverse extraction from the four exponentials in
(1) and the two in (2) gives, for each \(0\le t\le5\),

\[
[z^{2s-6-t}]H_s
=25^nP_{t,25}(n)+16^nP_{t,16}(n)
 +9^nP_{t,9}(n)+4^nP_{t,4}(n).
\tag{12}
\]

This is a symbolic identity: choosing a coefficient a fixed distance
from the top replaces every large binomial coefficient by one with fixed
lower argument.  The four polynomials in (12) are constructed directly
by `top_row_components`; 24 comparisons with full expansions of (3)
guard the reverse indexing.

The \(25\)-base polynomial has strictly positive monomial coefficients.
Let \(Q_t(n)\) be the sum of the absolute values of every negative
monomial in the three lower-base polynomials.  Since
\(4^n,9^n\le16^n\),

\[
[z^{2s-6-t}]H_s
\ge 25^nP_{t,25}(n)-16^nQ_t(n).
\tag{13}
\]

Both \(P_{t,25}\) and \(Q_t\) have positive coefficients.  Set

\[
R_t(n)=25P_{t,25}(n+1)Q_t(n)
 -16Q_t(n+1)P_{t,25}(n).
\tag{14}
\]

The exact certificates are:

| \(t\) | \(\deg P_{t,25}\) | \(\deg Q_t\) | shift \(n_0\) | initial lower-bound gap | smallest coefficient of \(R_t(x+n_0)\) |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 1 | 0 | \(57946/3\) | \(455625000\) |
| 1 | 2 | 3 | 0 | \(453832/3\) | \(121500000\) |
| 2 | 4 | 5 | 0 | \(565510/3\) | \(8100000\) |
| 3 | 6 | 7 | 1 | \(628789160/3\) | \(240000\) |
| 4 | 8 | 9 | 1 | \(1307680274/9\) | \(4000\) |
| 5 | 10 | 11 | 2 | \(7595068744186/45\) | \(128/3\) |

All 72 coefficients in the shifted polynomials in the last column are
nonnegative.  Hence the ratio

\[
\frac{25^nP_{t,25}(n)}{16^nQ_t(n)}
\tag{15}
\]

is nondecreasing from \(n_0\), while the initial gap is positive.  This
proves (13) for \(n\ge n_0\).  The four omitted values are, exactly,

\[
\begin{array}{c|c|r}
t&n&[z^{2s-6-t}]H_s\\ \hline
3&0&2714480\\
4&0&4852512\\
5&0&5756112\\
5&1&1785283448
\end{array}
\tag{16}
\]

and are positive.  This proves the second band.

## 4. Why a fixed number of \(u_2\)-layers cannot prove the kernel recurrence

Finite data suggest the stronger recurrence

\[
\mathcal K_{s+1}-u_5^2\mathcal K_s>_{\rm coeff}0.
\tag{17}
\]

It is positive in the exact scan through \(s=35\), but it remains
unproved.  The following calculation rules out one tempting proof
strategy.

Let \(M_s=3\beta^6\mathcal K_s\), \(L=2s-10\).  Exact subtraction gives

\[
M_{s+1}-u_5^2M_s
=u_5^LA_{5,s}+u_4^LA_{4,s}+u_3^LA_{3,s}+u_2^LA_{2,s},
\tag{18}
\]

where the four fixed-degree polynomials \(A_{j,s}\) are printed by
`recurrence_layer_data`.  Expanding the first three bases around \(u_2\)
sets

\[
L_{s,r}=3^rA_{5,s}+2^rA_{4,s}+A_{3,s}.
\tag{19}
\]

If the first \(R\) layers are merged, the required initial kernel is

\[
I_{s,R}=u_2^RA_{2,s}
 +\sum_{r=0}^{R-1}\binom Lr\beta^ru_2^{R-r}L_{s,r}.
\tag{20}
\]

For every fixed \(R\ge6\), its coefficient at degree \(R+3\) has

\[
[\beta^{R+3}]I_{s,R}
=-\frac{3\,2^R(R+5)}{(R-1)!}s^{R+2}+O_R(s^{R+1}).
\tag{21}
\]

Indeed, only \(r=R-1\) and \(r=R-2\) contribute to the leading power.
After removing their binomial factors, the two leading coefficients are
respectively \(-36\) and \(-12\); the next three offsets vanish, and all
later offsets have \(s\)-degree below \(R+2\).  Therefore

\[
-36\frac{2^{R-1}}{(R-1)!}
-12\frac{2^{R-2}}{(R-2)!}
=-\frac{3\,2^R(R+5)}{(R-1)!}.
\]

Thus \(I_{s,R}\) eventually has a negative coefficient for every fixed
\(R\).  This does **not** refute (17): it proves only that no fixed-depth
version of this \(u_2\)-layer merge can establish it.  A successful proof
must use a depth growing with \(s\), a different comparison, or a direct
two-parameter inequality.

## 5. Exact verification and the former open middle

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_even_second_active_partial.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_even_second_active_partial.py
PYTHONDONTWRITEBYTECODE=1 python3 even_second_active_workbench.py \
  --maximum-s 35
```

The proof verifier checks 682 positive shifted monomials, 210 independent
direct/reverse convolution values, 72 ratio-certificate monomials, four
exceptional top values, and the universal leading-term obstruction.
The workbench additionally finds no negative coefficient among 1,073
comparison-kernel coefficients, 1,064 kernel-recurrence coefficients,
1,064 first-transport coefficients, and 1,053 second-transport
coefficients through \(s=35\).  Those four scans are **FINITE evidence**.

Before the universal tail proof, the uncovered interval was

\[
31\le d\le2s-12.
\tag{22}
\]

The direct recurrence (17) and the two transport recurrences remain
unproved, but they are no longer needed: the \(Y_s+P_s\) split in
`EVEN_SECOND_ACTIVE_UNIVERSAL_THEOREM.md` closes this interval by a
different four-layer recurrence.  The full base-four Newton conjecture
still remains open.
