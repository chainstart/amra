# Independent raw audit of the fifth active Newton layer

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS}}
\]

The formulas, denominators, boundary values, positivity certificates,
and quantified ranges in `FIFTH_ACTIVE_NEWTON_THEOREM.md` were
recomputed from the original finite Liu--Chow sums.  The audit did not
import the fifth-layer verifier or reuse its stored intermediate
component polynomials.  No mathematical or transcription error was
found.

## 1. Independent source calculation

Write \((x)_{\underline m}=x(x-1)\cdots(x-m+1)\).  For \(c\ge1\), the
audit starts from
\[
W_{0,c}(n)=
\sum_{j=0}^{c-1}
\frac{(-1)^j(c+j)(n-1)_{\underline{c+j-1}}
 n^{\,n-c-j-1}}
{2^j j!(c-j-1)!},
\]
and, for a prescribed adjacent edge pair,
\[
D_c(n)=
\sum_{j=0}^{c-1}
\frac{(-1)^j(c+j+2)(n-3)_{\underline{c+j-1}}
 n^{\,n-c-j-3}}
{2^j j!(c-j-1)!}.
\]
It then reconstructs
\[
W_{1,c}=\frac{2(n-c)}{n(n-1)}W_{0,c},
\]
\[
W_{2,c}=
\frac{\binom{n-c}{2}W_{0,c}
-\frac{n(n-1)(n-2)}2D_c}
{\frac{n(n-1)(n-2)(n-3)}8},
\]
and finally
\[
\mathcal C_t(n)=
\sum_{c=1}^{t-1}
\left(W_{1,c}W_{1,t-c}-W_{0,c}W_{2,t-c}\right).
\]
Thus the determinant layers are obtained directly from the source
counts rather than from previously factored \(P_t\)'s.

Exact symbolic cancellation gives
\[
\mathcal C_{11}(n)=
\frac{(n-4)(n-5)(n-6)(n-7)}{10080}
P_{11}(n)n^{2n-24},
\]
\[
\mathcal C_{12}(n)=
\frac{(n-4)(n-5)(n-6)(n-7)}{90720}
P_{12}(n)n^{2n-26}.
\]
In particular, the two sensitive denominators are independently
confirmed as
\[
\boxed{10080\quad\text{and}\quad90720}.
\]

## 2. Initial-value audit

The depth-four Newton inversion was rerun using the raw
\(\mathcal C_t\)'s.  It gives every residual value used in the human
proof:
\[
\begin{array}{c|r}
k&a_{k,q_0+4}\\ \hline
5&5040\\
6&1095840\\
7&388668240\\
8&102879564480\\
9&21371783388480\\
10&8611754056375680\\
12&922909252139380800000
\end{array}
\]
All are positive.

## 3. Quantifier and certificate audit

For odd \(k\), \(n=(k+13)/2\).  The first-pair certificate and the
auxiliary sign \(P_9(n-1)>0\) apply for \(n\ge12\).  The second-pair
certificate and \(P_5(n-3)>0\) apply for \(n\ge10\).  The unpaired
last term is positive there.  Therefore the only values not covered
by the stable first pair are exactly
\[
n=9,10,11\quad\Longleftrightarrow\quad k=5,7,9.
\]

For even \(k\), \(n=(k+14)/2\).  With \(E=2n-26\),
\[
\left(1-\frac1n\right)^E
\le \frac1{1+E/n}
=\frac n{3n-26}
\]
is valid for \(n\ge14\): it is the reciprocal of Bernoulli's
inequality for \((1-1/n)^{-E}\).  Its denominator is positive on this
range.  The strengthened first-pair polynomial is coefficientwise
positive after \(n=m+14\), and the needed \(P_{10}(n-1)\) sign is
valid there.  The second pair applies for \(n\ge11\), while
\(n^2-4n-24>0\) for \(n\ge10\).  Hence the exact residual set is
\[
n=10,11,12,13\quad\Longleftrightarrow\quad k=6,8,10,12.
\]

The audit independently expands and checks all eight polynomial
certificates:

- both odd adjacent gaps;
- the auxiliary \(P_9\) and \(P_5\) signs;
- both even adjacent gaps; and
- the auxiliary \(P_{10}\) and \(Q_6\) signs.

Every shifted coefficient is a strictly positive integer.  The
claimed ranges cover all and only the admissible parameters, so there
is no boundary or quantifier gap.

## 4. Reproduction

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/sixth_layer_2026-07-30
pytest -q test_verify_sixth_active_newton.py
python3 verify_sixth_active_newton.py
```
