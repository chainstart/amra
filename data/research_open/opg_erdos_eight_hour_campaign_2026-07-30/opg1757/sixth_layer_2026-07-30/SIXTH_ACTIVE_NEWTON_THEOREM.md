# The sixth active base-four Newton layer is positive for every \(k\)

Date: 2026-07-30

## 1. Theorem

Write
\[
c_k(s)=\frac{(k-2)!}{2}C_k(s)
=\sum_q a_{k,q}\binom{s-4}{q},
\qquad
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor.
\]

### Theorem

For every \(k\ge5\),
\[
\boxed{a_{k,q_0+5}>0.}                              \tag{1}
\]
For \(k\le4\), this layer lies beyond the degree \(2k-4\).

Define
\[
\begin{aligned}
P_{13}(x)={}&x^{15}+70x^{14}+2405x^{13}+50045x^{12}
+593631x^{11}+1071225x^{10}\\
&-94449035x^9-1549919255x^8-5168791531x^7
+141697195355x^6\\
&+1627621385085x^5-3660582507525x^4
-131552143027686x^3\\
&+13386402798885x^2+5444743454388450x
-14171594774337000,
\end{aligned}
\]
and
\[
\begin{aligned}
P_{14}(x)={}&x^{17}+74x^{16}+2701x^{15}+59855x^{14}
+747256x^{13}+629309x^{12}\\
&-168601994x^{11}-3022692475x^{10}-12400886366x^9
+352146822071x^8\\
&+5386103546704x^7-2201028418405x^6
-610742061754071x^5\\
&-2210374509140079x^4+42588028344796389x^3\\
&+134015359118765310x^2-2135313543686815800x\\
&+4656619107268128000.
\end{aligned}
\]

For odd \(k\), put \(n=(k+15)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+5}
={}&\frac{(k-2)!}{2}(n-4)(n-5)(n-6)(n-7)(n-8)\\
&\times\Bigl[
\frac{P_{13}(n)}{907200}n^{2n-28}
-\frac{P_{11}(n-1)}{10080}(n-1)^{2n-26}\\
&\qquad+\frac{P_9(n-2)}{360}(n-2)^{2n-24}
-\frac{P_7(n-3)}{36}(n-3)^{2n-22}\\
&\qquad+\frac{P_5(n-4)}{12}(n-4)^{2n-20}
-\frac1{30}(n-5)^{2n-18}
\Bigr].
\end{aligned}}                                      \tag{2}
\]

For even \(k\), put \(n=(k+16)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+5}
={}&\frac{(k-2)!}{2}(n-4)(n-5)(n-6)(n-7)(n-8)\\
&\times\Bigl[
\frac{P_{14}(n)}{9979200}n^{2n-30}
-\frac{P_{12}(n-1)}{90720}(n-1)^{2n-28}\\
&\qquad+\frac{P_{10}(n-2)}{2520}(n-2)^{2n-26}
-\frac{P_8(n-3)}{180}(n-3)^{2n-24}\\
&\qquad+\frac{Q_6(n-4)}{36}(n-4)^{2n-22}\\
&\qquad-\frac{n^2-6n-19}{30}(n-5)^{2n-20}
\Bigr].
\end{aligned}}                                      \tag{3}
\]

The polynomials with indices at most twelve are exactly those defined
in the preceding active-layer theorems.

## 2. Raw component-total calculation

Starting afresh from the finite Liu--Chow \(W_{0,c}\) and adjacent-pair
sums, and then applying the two exact edge-orbit identities, gives
\[
\boxed{
\mathcal C_{13}(n)=
\frac{(n-4)(n-5)(n-6)(n-7)(n-8)}{907200}
P_{13}(n)n^{2n-28},
}                                                     \tag{4}
\]
\[
\boxed{
\mathcal C_{14}(n)=
\frac{(n-4)(n-5)(n-6)(n-7)(n-8)}{9979200}
P_{14}(n)n^{2n-30}.
}                                                     \tag{5}
\]
These are symbolic identities, not fitted formulas.  The same raw
calculation independently reproduces \(\mathcal C_{11}\) and
\(\mathcal C_{12}\), including denominators \(10080\) and \(90720\).

At depth five the component totals are
\[
13,11,9,7,5,3
\]
for odd \(k\), and
\[
14,12,10,8,6,4
\]
for even \(k\).  Substitution into the six-point Newton difference and
use of
\[
\binom{n-4}{\ell}(n-\ell-4)_{\underline{5-\ell}}
=\frac{(n-4)_{\underline5}}{\ell!}
\]
give (2)--(3).  The sign-sensitive last even translation is
\[
(n-5)^2+4(n-5)-24=n^2-6n-19.                       \tag{6}
\]

## 3. Odd-\(k\) positivity

For the first pair in (2), put \(E=2n-28\).  When \(n\ge16\),
\[
\left(1-\frac1n\right)^E
\le\frac{n-1}{3n-29}.                              \tag{7}
\]
Indeed,
\[
\left(1-\frac1n\right)^{-E}
=\left(1+\frac1{n-1}\right)^E
\ge1+\frac{E}{n-1}
=\frac{3n-29}{n-1}.
\]
Since \(P_{11}(n-1)>0\), (7) reduces the desired first-pair
inequality to
\[
(3n-29)P_{13}(n)-90(n-1)^3P_{11}(n-1)>0.           \tag{8}
\]
After \(n=m+16\), the coefficients of (8), from highest degree to
constant term, are
\[
\begin{aligned}
{}&3,859,115675,9717610,569361868,24627762136,\\
&811490053906,20705161071070,411487903208542,\\
&6351422992608136,75280685663825112,\\
&670900703649554616,4345106989436839047,\\
&19351033699312031579,53734068443614713647,\\
&75313923210636142634,24628498850290684440.
\end{aligned}
\]
They are all positive.  The auxiliary \(P_{11}\) sign follows, for
example, from its positive-coefficient expansion after \(x=v+8\).

For \(n\ge12\), the second pair is positive because its common-base
exponent \(2n-24\) is nonnegative and
\[
P_9(n-2)-10P_7(n-3)(n-3)^2>0.                      \tag{9}
\]
After \(n=m+10\), the coefficients in (9) are
\[
1,101,4657,127052,2215286,24838162,171249983,
659978609,1268884197,958465280.
\]
The sign \(P_7(n-3)>0\) follows from the positive expansion of
\(P_7(v+6)\).

For \(n\ge10\), the last pair is positive because
\[
5P_5(n-4)-2(n-5)^2>0,                              \tag{10}
\]
whose coefficients after \(n=m+10\) are
\[
5,148,1340,2665.
\]
Thus all three pairs are positive for \(n\ge16\).

The exact remaining values \(n=10,\ldots,15\), corresponding to
\(k=5,7,\ldots,15\), are
\[
\begin{array}{c|r}
k&a_{k,q_0+5}\\ \hline
5&720\\
7&288691200\\
9&35530741814400\\
11&4372223151942455040\\
13&686476515794775028646400\\
15&148236140800840446847164672000
\end{array}
\]
and are all positive.

## 4. Even-\(k\) positivity

For the first pair in (3), put \(E=2n-30\).  When \(n\ge19\),
\[
\left(1-\frac1n\right)^E
\le\frac{n-1}{3n-31}.                              \tag{11}
\]
As above, this is the reciprocal Bernoulli bound.  Since
\(P_{12}(n-1)>0\), it suffices that
\[
(3n-31)P_{14}(n)-110(n-1)^3P_{12}(n-1)>0.          \tag{12}
\]
At \(n=m+19\), its coefficients are
\[
\begin{aligned}
{}&3,1107,193161,21169348,1631997253,93906191285,\\
&4174840923923,146396418456759,4096201455639975,\\
&91882486202741773,1650348979286780831,\\
&23573056064563636455,264242035049475407466,\\
&2275628853615782107582,14569979903467258582780,\\
&65838862978158802015183,192011978155455155242008,\\
&301634695986262673074308,151205665437678276784800.
\end{aligned}
\]
Every coefficient is positive; \(P_{12}(n-1)>0\) follows from the
positive expansion of \(P_{12}(v+8)\).

For \(n\ge13\), the second pair is positive because \(2n-26\ge0\) and
\[
P_{10}(n-2)-14P_8(n-3)(n-3)^2>0.                   \tag{13}
\]
At \(n=m+11\), the coefficients in (13) are
\[
\begin{aligned}
{}&1,128,7622,276715,6725831,112974316,1307452749,\\
&10121652288,49784863002,146285921447,232905724939,\\
&154117981710.
\end{aligned}
\]
The needed \(P_8(n-3)>0\) follows from \(P_8(v+6)\).

For \(n\ge11\), the third pair is positive.  Here
\(n^2-6n-19>0\), the common-base exponent is nonnegative, and
\[
5Q_6(n-4)-6(n^2-6n-19)(n-5)^2>0.                  \tag{14}
\]
After \(n=m+11\), the coefficients in (14) are
\[
5,249,4782,41611,145552,167699.
\]
Thus all three pairs are positive for \(n\ge19\).

The exact residual values \(n=11,\ldots,18\), corresponding to
\(k=6,8,\ldots,20\), are
\[
\begin{array}{c|r}
k&a_{k,q_0+5}\\ \hline
6&322560\\
8&94624871040\\
10&15571237995694080\\
12&2730672303823816531200\\
14&606851536299200279176320000\\
16&181036425392118892912101411225600\\
18&73501592937716326740283702977417216000\\
20&40469104973014172139529610745337065996288000
\end{array}
\]
and are all positive.  This completes the proof of (1) for every
admissible \(k\).

## 5. Formal verification boundary

The human proof consists of six infinite-range shifted-coefficient
certificates, four auxiliary polynomial signs, two reciprocal
Bernoulli inequalities, and fourteen exact residual values.  The
finite regression through \(k=100\) is only a transcription check and
is not used to infer general positivity.

The companion verifier additionally:

- rebuilds \(\mathcal C_{11},\ldots,\mathcal C_{14}\) from the raw
  Liu--Chow sums;
- checks the fifth-layer independent audit;
- compares (2)--(3) with direct Newton inversion for \(5\le k\le22\);
- checks every displayed coefficient certificate exactly; and
- verifies the leading-two-coefficient lemma's symbolic identities.

Reproduction:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/sixth_layer_2026-07-30
pytest -q test_verify_sixth_active_newton.py
python3 verify_sixth_active_newton.py
```
