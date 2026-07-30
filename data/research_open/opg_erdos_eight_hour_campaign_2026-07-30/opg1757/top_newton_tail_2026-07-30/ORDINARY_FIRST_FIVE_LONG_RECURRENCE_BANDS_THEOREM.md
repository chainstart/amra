# OPG-1757: the first five all-depth long-recurrence bands

Date: 2026-07-30

## 0. Result

Let \(P_d(k)=b_{k,d}\) be the monic degree-\(d\) ordinary symbol and
define its Poisson--Newton transform by
\[
A_d(z)=e^{-z}\sum_{n\ge0}P_d(n+2)\frac{z^n}{n!},
\qquad
A_d(x^2)=x^dH_d(x).
\tag{1}
\]
The monic parity polynomials \(H_d\) have a unique same-parity
connection expansion
\[
\boxed{
xH_d(x)-H_{d+1}(x)
=
\sum_{q=0}^{\lfloor(d-1)/2\rfloor}
\gamma_{d,q}H_{d-1-2q}(x).
}
\tag{2}
\]
The finite certificate through \(d=50\) found every coefficient in
(2) positive.  The first five bands can now be proved positive for
all depths.

### Theorem 1 (five positive recurrence bands)

For \(0\le q\le4\) and every \(d\ge2q+1\),
\[
\boxed{\gamma_{d,q}>0.}
\tag{3}
\]
Explicitly,
\[
\gamma_{d,0}
=\frac{(d+1)(11d+43)}6,
\tag{4}
\]
\[
\gamma_{d,1}
=\frac{d-2}{432}
\left(
341d^4+3269d^3+10852d^2+15838d+11094
\right),
\tag{5}
\]
\[
\begin{aligned}
\gamma_{d,2}
=\frac{d-4}{933120}\bigl(&
371585d^7+3038100d^6+6227486d^5-2746356d^4\\
&-12009655d^3+7914888d^2+37057752d+36634680
\bigr),
\end{aligned}
\tag{6}
\]
\[
\begin{aligned}
\gamma_{d,3}
=\frac{d-6}{2351462400}\bigl(&
477026935d^{10}+373655975d^9-13198014515d^8\\
&-2356653705d^7+116744157150d^6+348820236d^5\\
&-321203446846d^4-58621959506d^3\\
&+534175684124d^2+708834254088d-180164960640
\bigr),
\end{aligned}
\tag{7}
\]
and
\[
\begin{aligned}
\gamma_{d,4}
=\frac{d-8}{84652646400}\bigl(&
8756143850d^{13}-110386703260d^{12}
+169932034915d^{11}\\
&+2946121856418d^{10}-11807084667619d^9
-13369462591602d^8\\
&+122184475184308d^7-78467819453648d^6
-324534244911847d^5\\
&+252862845724584d^4+483781271752093d^3
+76417691692068d^2\\
&-1176624827988660d+229574732844240
\bigr).
\end{aligned}
\tag{8}
\]

These are unbounded statements in \(d\).  They do not prove that all
bands \(q\) in (2) are positive and, by themselves, do not prove
real-rootedness of \(H_d\).

## 1. A triangular coefficient identity

Write
\[
P_d(k)=\sum_{r=0}^{d}\beta_{d,r}k^{d-r},
\qquad \beta_{d,0}=1,
\tag{9}
\]
and
\[
H_d(x)=\sum_{j=0}^{\lfloor d/2\rfloor}
h_{d,j}x^{d-2j},
\qquad h_{d,0}=1.
\tag{10}
\]
Let
\[
s_m(n)=s(n,n-m)
\tag{11}
\]
be a near-diagonal signed Stirling number of the first kind.  It is
the polynomial determined by
\[
s_0(n)=1,\qquad
s_m(n+1)=s_m(n)-n\,s_{m-1}(n),
\qquad s_m(0)=0\quad(m\ge1).
\tag{12}
\]

### Lemma 2 (ordinary-to-Newton triangle)

For \(\ell\ge0\), put
\[
M_{d,\ell}
=
\sum_{r=0}^{\ell}
\beta_{d,r}
\binom{d-r}{\ell-r}2^{\ell-r}.
\tag{13}
\]
Then
\[
\boxed{
h_{d,\ell}
=
M_{d,\ell}
-
\sum_{j=0}^{\ell-1}
h_{d,j}s_{\ell-j}(d-j).
}
\tag{14}
\]

#### Proof

Newton's formula and (1) give
\[
P_d(n+2)
=\sum_j h_{d,j}(n)_{\underline{d-j}}.
\tag{15}
\]
The coefficient of \(n^{d-\ell}\) on the left is exactly (13).
The same coefficient in
\((n)_{\underline{d-j}}\) is
\[
s(d-j,d-\ell)=s_{\ell-j}(d-j).
\]
Separating the \(j=\ell\) term proves (14). \(\square\)

The first five rows obtained from (14) factor as
\[
h_{d,1}
=-\frac{(d-1)(22d^2+151d+258)}{36},
\tag{16}
\]
\[
h_{d,2}
=\frac{(d-3)(d-2)
(286d^4+3392d^3+16445d^2+37213d+28668)}
{5184},
\tag{17}
\]
\[
\begin{aligned}
h_{d,3}
=-\frac{(d-5)(d-4)(d-3)}{83980800}\bigl(&
158450d^6+2236425d^5+15204170d^4\\
&+60657945d^3+141977342d^2\\
&+179753064d+45900864
\bigr).
\end{aligned}
\tag{18}
\]
The verifier records the longer \(h_{d,4},h_{d,5}\) identities
exactly.  Their forced zero factors are respectively
\[
\prod_{i=4}^{7}(d-i),
\qquad
\prod_{i=5}^{9}(d-i).
\tag{19}
\]
In the displayed factorization of \(h_{d,5}\), an additional minus
sign is pulled out so that the residual polynomial has positive
leading coefficient; that sign is not forced by the zeros.

## 2. Extraction of the recurrence bands

Comparing the coefficient of \(x^{d-1-2q}\) in (2) gives the
triangular recurrence
\[
\boxed{
\gamma_{d,q}
=h_{d,q+1}-h_{d+1,q+1}
-
\sum_{i=0}^{q-1}
\gamma_{d,i}h_{d-1-2i,q-i}.
}
\tag{20}
\]
Consequently \(\gamma_{d,q}\) uses only
\(\beta_{d,0},\ldots,\beta_{d,q+1}\).  Substituting the five
all-depth ordinary symbols already proved in:

- `ORDINARY_SUBLEADING_SYMBOL_THEOREM.md`;
- `ORDINARY_SECOND_SUBLEADING_SYMBOL_THEOREM.md`;
- `ALL_FIXED_RANK_ORDINARY_SYMBOL_ALGORITHM_THEOREM.md`;
- `ORDINARY_RANK_FOUR_SYMBOL_AND_NEWTON_THEOREM.md`; and
- `ORDINARY_RANK_FIVE_SYMBOL_AND_NEWTON_THEOREM.md`

into (14) and then (20) gives (4)--(8) by rational polynomial
arithmetic.  Thus no finite-depth interpolation enters this theorem.

## 3. Positivity certificates

For \(0\le q\le4\), define
\[
G_q(u)=D_q\,\gamma_{u+2q+1,q},
\tag{21}
\]
where
\[
(D_0,D_1,D_2,D_3,D_4)
=(6,432,933120,2351462400,84652646400).
\]
In descending order, the coefficient rows of \(G_q(u)\) are:
\[
\begin{array}{c|l}
q&[u^{\deg G_q}],\ldots,[u^0]\\ \hline
0&(11,\ 76,\ 108)\\
1&(341,\ 7702,\ 66048,\ 264728,\ 478201,\ 272160)\\
2&(371585,\ 16415160,\ 308496186,\ 3210365280,\\
&\quad 20131519269,\ 77281233888,\ 174977309920,\\
&\quad 208073083272,\ 93163400640)\\
3&(477026935,\ 34242568360,\ 1095952245010,\\
&\quad20614299021540,\ 252733231377030,\\
&\quad2115575618035236,\ 12298260858849350,\\
&\quad49422867136982780,\ 133635727915784255,\\
&\quad228954688032719124,\ 219108232011563820,\\
&\quad84782271117519360)\\
4&(8756143850,\ 922838271040,\ 44483567054325,\\
&\quad1298815018474078,\ 25637894919557219,\\
&\quad361521910469412770,\ 3750276830942731564,\\
&\quad29023617823992094316,\ 168012343916699257497,\\
&\quad721802363144853581354,\ 2255963150681039380081,\\
&\quad4943594263014222847546,\ 7109960867607398147784,\\
&\quad5904275325992272716336,\ 2061346070200345125120).
\end{array}
\tag{22}
\]
Every entry is strictly positive.  For \(d\ge2q+1\), put
\(u=d-(2q+1)\ge0\); equations (21)--(22) prove (3).

## 4. Meaning and remaining target

Equation (2) is not a Favard three-term recurrence: the
\(\gamma_{d,q}\) with \(q\ge1\) are genuinely nonzero.  The theorem
nevertheless shows that the observed positive lower-parity expansion
is not a low-depth accident in its first five bands.

An all-band proof would reduce to showing
\[
\gamma_{d,q}>0
\qquad
(d\ge2q+1,\ q\ge0)
\tag{23}
\]
from the exact bivariate forest determinant.  Positivity in (23)
alone still needs a compatibility/interlacing lemma before it can
imply real-rootedness.  The two logically separate open steps are
therefore:

1. extend the band theorem uniformly in \(q\); and
2. prove that the resulting long recurrence preserves the required
   common interlacing.

## 5. Verification

`verify_ordinary_first_five_long_recurrence_bands.py` independently
implements (12)--(14) and (20) from the five printed
\(\beta\)-polynomials.  It checks:

- all five rational identities (4)--(8);
- the exact shifted coefficient rows (22);
- positivity on the complete unbounded ranges; and
- the first numerical recurrence values.

The script does not use the finite \(d\le50\) recurrence certificate.
