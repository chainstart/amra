# The seventh active base-four Newton layer is positive for every \(k\)

Date: 2026-07-30

## 1. Theorem and new determinant layers

Let
\[
c_k(s)=\frac{(k-2)!}{2}C_k(s)
=\sum_q a_{k,q}\binom{s-4}{q},
\qquad
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor.
\]

### Theorem

For every parameter for which the seventh active layer exists,
\[
\boxed{a_{k,q_0+6}>0\qquad(k\ge6).}                 \tag{1}
\]

Define
\[
\begin{aligned}
P_{15}(x)={}&x^{18}+87x^{17}+3800x^{16}+105360x^{15}
+1891421x^{14}+17289777x^{13}\\
&-118116085x^{12}-6505709265x^{11}-86775284431x^{10}
-38284278087x^9\\
&+14371618346075x^8+155474888000475x^7
-622230464754476x^6\\
&-21941798038092942x^5-34808916839991345x^4
+1685933108025287175x^3\\
&+3008726132139045000x^2-82118619319287127500x\\
&+197196338202113250000,
\end{aligned}
\]
\[
\begin{aligned}
P_{16}(x)={}&x^{20}+91x^{19}+4172x^{18}+121628x^{17}
+2284643x^{16}+20698691x^{15}\\
&-230561653x^{14}-11319430447x^{13}-162404702239x^{12}
-80646884461x^{11}\\
&+34321800795503x^{10}+457838031840137x^9
-1167527280504428x^8\\
&-82905605421055196x^7-398108708754400437x^6
+8161447984576101657x^5\\
&+64714964045818304358x^4-630805618098807641100x^3\\
&-3720646386150579275400x^2+41502191820112083060000x\\
&-86322277727720274240000.
\end{aligned}
\]

Direct substitution in the original finite Liu--Chow sums gives
\[
\boxed{
\mathcal C_{15}(n)=
\frac{(n-4)_{\underline6}}{119750400}
P_{15}(n)n^{2n-32},
}                                                     \tag{2}
\]
\[
\boxed{
\mathcal C_{16}(n)=
\frac{(n-4)_{\underline6}}{1556755200}
P_{16}(n)n^{2n-34}.
}                                                     \tag{3}
\]
Both are exact symbolic identities.

## 2. Seven-point Newton formulas

For odd \(k\), put \(n=(k+17)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+6}
={}&\frac{(k-2)!}{2}(n-4)_{\underline6}\Bigl[
\frac{P_{15}(n)}{119750400}n^{2n-32}\\
&-\frac{P_{13}(n-1)}{907200}(n-1)^{2n-30}
+\frac{P_{11}(n-2)}{20160}(n-2)^{2n-28}\\
&-\frac{P_9(n-3)}{1080}(n-3)^{2n-26}
+\frac{P_7(n-4)}{144}(n-4)^{2n-24}\\
&-\frac{P_5(n-5)}{60}(n-5)^{2n-22}
+\frac1{180}(n-6)^{2n-20}
\Bigr].
\end{aligned}}                                      \tag{4}
\]

For even \(k\), put \(n=(k+18)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+6}
={}&\frac{(k-2)!}{2}(n-4)_{\underline6}\Bigl[
\frac{P_{16}(n)}{1556755200}n^{2n-34}\\
&-\frac{P_{14}(n-1)}{9979200}(n-1)^{2n-32}
+\frac{P_{12}(n-2)}{181440}(n-2)^{2n-30}\\
&-\frac{P_{10}(n-3)}{7560}(n-3)^{2n-28}
+\frac{P_8(n-4)}{720}(n-4)^{2n-26}\\
&-\frac{Q_6(n-5)}{180}(n-5)^{2n-24}\\
&+\frac{n^2-8n-12}{180}(n-6)^{2n-22}
\Bigr].
\end{aligned}}                                      \tag{5}
\]
The last translation in (5) is
\[
(n-6)^2+4(n-6)-24=n^2-8n-12.                       \tag{6}
\]
Formula (4) also retains the exact factor \(2\) in
\(\mathcal C_5(x)=2(x-4)P_5(x)x^{2x-12}\); this is why its sixth term
has denominator \(60\), not \(240\).

## 3. Infinite odd range

For the first pair of (4), set \(E=2n-32\).  For \(n\ge22\),
\[
\left(1-\frac1n\right)^E
\le\frac{n-1}{3n-33},                               \tag{7}
\]
by reciprocal Bernoulli.  Since \(P_{13}(n-1)>0\), it suffices that
\[
G_{o,1}(n):=(3n-33)P_{15}(n)
-132(n-1)^3P_{13}(n-1)>0.                           \tag{8}
\]
At \(n=m+22\), the coefficients of \(G_{o,1}\) are
\[
\begin{aligned}
{}&3,1350,287973,38695542,3670725939,261057032244,\\
&14424621805476,633084639245850,22368228612820068,\\
&640748595550282626,14908699695311214840,\\
&280923707642817251262,4252181864268931311921,\\
&50974165110470401077240,473285576627030981052471,\\
&3288221068663928327100816,16174123610451830396817909,\\
&51082294110475819089522030,84052889176494601309791240,\\
&34436142487296252970850880.
\end{aligned}
\]
All are strictly positive.

The second pair is positive for \(n\ge14\), since its common-base
exponent is nonnegative and
\[
G_{o,2}(n):=3P_{11}(n-2)
-56P_9(n-3)(n-3)^2>0.                               \tag{9}
\]
At \(n=m+9\), its coefficients are
\[
\begin{aligned}
{}&3,358,20427,731206,18006615,313592354,3818601153,\\
&30974205662,151336714005,373156571046,473030855553,\\
&462474270522,51870192696.
\end{aligned}
\]

The third pair is positive for \(n\ge12\), because
\[
G_{o,3}(n):=5P_7(n-4)
-12P_5(n-5)(n-5)^2>0,                               \tag{10}
\]
whose coefficients after \(n=m+9\) are
\[
5,263,5761,63241,318511,408401,46938.
\]
The auxiliary signs \(P_{13}(n-1),P_9(n-3),P_5(n-5)>0\) follow from
their positive expansions after shifts \(9,11,7\), respectively.
The last term in (4) is positive.  Hence every term pair is positive
for \(n\ge22\).

## 4. Infinite even range

For the first pair in (5), put \(E=2n-34\).  For \(n\ge26\),
\[
\left(1-\frac1n\right)^E
\le\frac{n-1}{3n-35}.                               \tag{11}
\]
It reduces the first pair to
\[
G_{e,1}(n):=(3n-35)P_{16}(n)
-156(n-1)^3P_{14}(n-1)>0.                           \tag{12}
\]
At \(n=m+26\), its coefficients are
\[
\begin{aligned}
{}&3,1720,469427,81095582,9945913397,920547523078,\\
&66716604797228,3877023937490326,183462735777181328,\\
&7138370444025791542,229590088784158973676,\\
&6113352063104101847070,134494529047797323051377,\\
&2430722685126572403776174,35726808646990476636653341,\\
&420423132179828212652111644,3869042694416308480368096063,\\
&26865226768650717718086954516,132873767875060610221949005448,\\
&422244122987457003552029735868,685267024045360411738991332152,\\
&213051947425072218963792452160.
\end{aligned}
\]

The second pair is positive for \(n\ge15\), because
\[
G_{e,2}(n):=P_{12}(n-2)
-24P_{10}(n-3)(n-3)^2>0.                            \tag{13}
\]
At \(n=m+10\), its coefficients are
\[
\begin{aligned}
{}&1,146,10241,456010,14277705,327639270,5560596319,\\
&68801688950,598246879619,3437000092814,12062342741723,\\
&25602284772170,34217571635104,21774762392328,5270137679520.
\end{aligned}
\]

The third pair is positive for \(n\ge13\), because
\[
G_{e,3}(n):=P_8(n-4)
-4Q_6(n-5)(n-5)^2>0,                                \tag{14}
\]
and its coefficients at \(n=m+10\) are
\[
1,73,2343,41807,429479,2343541,5280646,4236064,1212180.
\]
The auxiliary signs \(P_{14}(n-1),P_{10}(n-3),Q_6(n-5)>0\) follow
from shifts \(9,12,8\).  Finally,
\[
n^2-8n-12>0\qquad(n\ge12).
\]
Thus all terms in (5) are positive in pairs, plus the final positive
term, for every \(n\ge26\).

## 5. Exact closure of the residual ranges

The odd stable proof leaves exactly \(12\le n\le21\), or
\(k=7,9,\ldots,25\):
\[
\begin{array}{c|r}
7&129024000\\
9&38466105189120\\
11&8459995287334752000\\
13&2057634945868538561817600\\
15&629013092157326490510651955200\\
17&252902104918288632975645944603136000\\
19&135348119377829575229021244569109135360000\\
21&96199130980722253989938072808952931562455040000\\
23&90040892954791322663935009017638461713607966064640000\\
25&109772406518111164968414347516075482376452480344698388480000
\end{array}
\]

The even stable proof leaves exactly \(12\le n\le25\), or
\(k=6,8,\ldots,32\):
\[
\begin{array}{c|r}
6&40320\\
8&56384294400\\
10&19172585464704000\\
12&5588121248292596428800\\
14&1840898547634306585990118400\\
16&755656377559846704218640358195200\\
18&400885200400329152324178964122673152000\\
20&277750473779994027112715979465152548577280000\\
22&250969416726626124614385322827257976884593950720000\\
24&293723920454657044846124904241982585080107921372610560000\\
26&441147474656488554818915934918954526505848409795275134074880000\\
28&841661100888739666797729646999468711983328248818691755627249664000000\\
30&2018953119324318711635469624199863166244074241113792840348866938142720000000\\
32&6028234524723186002881797176873713285862791239328168109189458928525723566080000000
\end{array}
\]
Every entry is positive.  These 24 values are the complete finite
complement of the two proved infinite ranges, so (1) follows.

## 6. Verification boundary

The human proof uses six exact shifted-polynomial certificates, six
auxiliary sign certificates, two reciprocal Bernoulli inequalities,
and the complete finite residual set.  A regression through \(k=100\)
is included only to catch transcription errors.

The verifier independently:

- reconstructs (2)--(3) from the raw Liu--Chow sums;
- compares (4)--(5) with direct seven-point Newton inversion for
  \(6\le k\le35\);
- checks every coefficient certificate exactly;
- checks all residual values; and
- cross-checks the corrected diagonal component theorem.

Reproduction:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/seventh_layer_2026-07-30
pytest -q test_verify_seventh_active_newton.py
python3 verify_seventh_active_newton.py
```
