# The fifth active base-four Newton layer is positive for every \(k\)

Date: 2026-07-30

## 1. Theorem and closed forms

Use
\[
c_k(s)=\frac{(k-2)!}{2}C_k(s)
=\sum_q a_{k,q}\binom{s-4}{q},
\qquad
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor.
\]

### Theorem

For every \(k\ge5\),
\[
\boxed{a_{k,q_0+4}>0.}                               \tag{1}
\]
For \(k\le4\), this fifth active layer lies beyond the degree
\(2k-4\).

Let \(P_5,Q_6,P_7,P_8,P_9,P_{10}\) have the definitions in the earlier
exact layers, and define
\[
\begin{aligned}
P_{11}(x)={}&x^{12}+54x^{11}+1377x^{10}+19446x^9
+107701x^8\\
&-1254774x^7-27736029x^6-128979594x^5\\
&+1411682095x^4+15230717502x^3\\
&-33712195581x^2-584682858630x\\
&+1716330092400,
\end{aligned}
\]
\[
\begin{aligned}
P_{12}(x)={}&x^{14}+58x^{13}+1601x^{12}+24578x^{11}
+141681x^{10}\\
&-2309634x^9-56550089x^8-341453834x^7\\
&+3612221555x^6+61253397878x^5
+3728325315x^4\\
&-4265925973902x^3-4604924521080x^2\\
&+173451580124400x-404699171184000.
\end{aligned}
\]

For odd \(k\), put \(n=(k+13)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+4}
={}&\frac{(k-2)!}{2}(n-4)(n-5)(n-6)(n-7)\\
&\times\Bigl[
\frac{P_{11}(n)}{10080}n^{2n-24}
-\frac{P_9(n-1)}{180}(n-1)^{2n-22}\\
&\qquad+\frac{P_7(n-2)}{12}(n-2)^{2n-20}
-\frac{P_5(n-3)}3(n-3)^{2n-18}\\
&\qquad+\frac16(n-4)^{2n-16}
\Bigr].
\end{aligned}}                                       \tag{2}
\]

For even \(k\), put \(n=(k+14)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+4}
={}&\frac{(k-2)!}{2}(n-4)(n-5)(n-6)(n-7)\\
&\times\Bigl[
\frac{P_{12}(n)}{90720}n^{2n-26}
-\frac{P_{10}(n-1)}{1260}(n-1)^{2n-24}\\
&\qquad+\frac{P_8(n-2)}{60}(n-2)^{2n-22}
-\frac{Q_6(n-3)}9(n-3)^{2n-20}\\
&\qquad+\frac{n^2-4n-24}{6}(n-4)^{2n-18}
\Bigr].
\end{aligned}}                                       \tag{3}
\]

## 2. New component-total layers

The common finite Lagrange formulas for \(W_{0,c}\) and the adjacent
pair count \(A_c\), followed by the two edge-orbit identities, give
\[
\boxed{
\mathcal C_{11}(n)
=\frac{(n-4)(n-5)(n-6)(n-7)}{10080}
P_{11}(n)n^{2n-24},
}                                                       \tag{4}
\]
\[
\boxed{
\mathcal C_{12}(n)
=\frac{(n-4)(n-5)(n-6)(n-7)}{90720}
P_{12}(n)n^{2n-26}.
}                                                       \tag{5}
\]
After the common factors are removed, these are exact polynomial
identities of degrees twelve and fourteen.

## 3. Five-point Newton difference

Let \(n_0=q_0+4\) and \(n=n_0+4\).  Newton inversion gives
\[
\begin{aligned}
a_{k,q_0+4}
=\frac{(k-2)!}{2}\Bigl[
&C_k(n)-(n-4)C_k(n-1)\\
&+\binom{n-4}{2}C_k(n-2)\\
&-\binom{n-4}{3}C_k(n-3)\\
&+\binom{n-4}{4}C_k(n-4)
\Bigr].                                               \tag{6}
\end{aligned}
\]
For odd \(k\), the component totals are \(11,9,7,5,3\), giving (2).
For even \(k\), they are \(12,10,8,6,4\), giving (3).  In the final
even term the translated quadratic is
\[
(n-4)^2+4(n-4)-24=n^2-4n-24.                        \tag{7}
\]

## 4. Odd-\(k\) positivity

The finite cases below the stable first-pair range are
\[
a_{5,5}=5040,\quad
a_{7,6}=388668240,\quad
a_{9,7}=21371783388480.                              \tag{8}
\]

For \(n\ge12\), the first two terms in (2) are positive because
\[
P_{11}(n)-56P_9(n-1)(n-1)^2>0,                      \tag{9}
\]
and \(P_9(n-1)>0\).  Both statements have positive-coefficient
certificates: after writing \(n=m+9\), the coefficients of (9) are
\[
\begin{aligned}
1,106,4957,135134,2451349,33872006,411660943,\\
4359531734,32895057599,141149572602,\\
311334687567,371880318914,197744294160,
\end{aligned}
\]
while \(P_9(v+11)\) also has all coefficients positive.

For \(n\ge10\), the next pair is positive because
\[
P_7(n-2)-4P_5(n-3)(n-3)^2>0.                        \tag{10}
\]
At \(n=m+9\), its coefficients are
\[
1,63,1671,23061,163873,503445,517648.
\]
Here \(P_5(n-3)>0\), certified by the positive expansion of
\(P_5(v+7)\).  The last term in (2) is positive.  The remaining
\(n=9,10,11\) are exactly (8).

## 5. Even-\(k\) positivity

The exact small cases are
\[
\begin{aligned}
a_{6,6}&=1095840,\\
a_{8,7}&=102879564480,\\
a_{10,8}&=8611754056375680,\\
a_{12,9}&=922909252139380800000.
\end{aligned}                                        \tag{11}
\]

For \(n\ge14\), put \(E=2n-26\).  The elementary inequality
\[
\left(1-\frac1n\right)^E
\le\frac1{1+E/n}
=\frac{n}{3n-26}                                    \tag{12}
\]
follows from Bernoulli's inequality applied to
\((1-1/n)^{-E}\).  Hence the first pair in (3) is bounded below by a
positive multiple of
\[
(3n-26)P_{12}(n)-72nP_{10}(n-1)(n-1)^2.             \tag{13}
\]
At \(n=m+14\), every coefficient of (13) is positive; the exact list
from highest degree to constant term is
\[
\begin{aligned}
{}&3,706,77771,5312054,251057071,8669285070,\\
&224967667317,4441292985970,66745347511373,\\
&756360735004742,6335898473374553,\\
&37973787855046886,154507276638216884,\\
&389413900763108272,502056354127992768,\\
&180273391055724960.
\end{aligned}
\]
The needed \(P_{10}(n-1)>0\) follows
from the positive expansion of \(P_{10}(v+12)\).

For \(n\ge11\), the second pair is positive because
\[
3P_8(n-2)-20Q_6(n-3)(n-3)^2>0.                      \tag{14}
\]
At \(n=m+10\), its coefficients are
\[
3,259,9911,215485,2829083,22009407,
93758260,197341756,160015540.
\]
Also \(Q_6(n-3)>0\), from the positive expansion of \(Q_6(v+8)\).
Finally \(n^2-4n-24>0\) for \(n\ge10\).  The four residual values
\(n=10,11,12,13\) are exactly (11).

Thus (1) holds for every parameter for which the fifth layer exists.

## 6. Formal finite closure

The proof uses no positivity scan:

- four explicit positive-coefficient gap certificates cover the
  infinite ranges;
- four auxiliary positive-coefficient certificates justify the signs
  used in the ratio bounds; and
- seven exact values close the complete residual interval.

The companion verifier reconstructs (4)--(5), checks every certificate,
recomputes exact Newton differences for \(5\le k\le14\), and performs a
transcription regression through \(k=100\).  None of those finite
regressions is a premise of the human proof.

Reproduction:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/fifth_layer_2026-07-30
pytest -q test_verify_fifth_active_newton.py
python3 verify_fifth_active_newton.py
```
