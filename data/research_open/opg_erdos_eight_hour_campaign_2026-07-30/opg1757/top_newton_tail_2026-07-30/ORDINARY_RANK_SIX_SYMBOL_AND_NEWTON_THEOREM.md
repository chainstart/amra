# OPG-1757: the rank-six ordinary symbol and fifth Newton inequality

Date: 2026-07-30

## 0. Result

Write
\[
b_{k,d}=\sum_{r=0}^{d}\beta_{d,r}k^{d-r},
\qquad
a_{d,r}=\frac{(-1)^r\beta_{d,r}}{\binom dr}.
\tag{1}
\]

### Theorem 1 (rank-six symbol)

For every \(d\ge6\),
\[
\boxed{\beta_{d,6}=\frac{P_6(d)}{2764687709306880000},}
\tag{2}
\]
where
\[
\begin{aligned}
P_6(d)={}&7301929250d^{18}+153379721250d^{17}
+2431268137725d^{16}\\
&+2874784928400d^{15}-80975845704300d^{14}
-935374628777400d^{13}\\
&+3592457053926440d^{12}+19939081990290120d^{11}\\
&-117051403660829448d^{10}-390355621772659110d^9\\
&+3565087697695904835d^8+15186099809099153160d^7\\
&-139123168520225939854d^6+129786516909791432460d^5\\
&+43553643530874118200d^4+3926765129917260384720d^3\\
&-11165053968083036288448d^2
+13833562112789217292800d\\
&-18754809088236550963200.
\end{aligned}
\tag{3}
\]
Equivalently,
\[
\boxed{
B_6(t):=\sum_{d\ge6}\beta_{d,6}t^d
=\frac{t^6Q_6(t)}{1175731200(1-t)^{19}},
}
\tag{4}
\]
where
\[
\begin{aligned}
Q_6(t)={}&5468059639079t^{18}-96707287173402t^{17}
+801767610507177t^{16}\\
&-4134187624467924t^{15}+14830405816091625t^{14}
-39221892759811734t^{13}\\
&+79082500484277927t^{12}-124083480256039152t^{11}\\
&+153583463986914384t^{10}-151678254909239820t^9\\
&+121207591660577760t^8-78908761803359520t^7\\
&+41937232067473680t^6-13707502253383680t^5\\
&+4613598230169600t^4+1516898143656000t^3\\
&+8047513105228800t^2+5084915163955200t\\
&+1000541372544000.
\end{aligned}
\tag{5}
\]

### Theorem 2 (fifth normalized Newton inequality)

For every \(d\ge6\),
\[
\boxed{
\beta_{d,6}>0,
\qquad
a_{d,5}^2>a_{d,4}a_{d,6}.
}
\tag{6}
\]
Thus the normalized symbols through rank six form a strictly positive,
strictly log-concave prefix.  In particular,
\[
\boxed{
|\beta_{d,6}|<\binom d6(3d^2)^6.
}
\tag{7}
\]
Finite-depth reconstruction is only a redundant audit; the proof is
the exact profile-rank-eight rational identity below.

## 1. Profile-rank-eight derivation

The exact central-binomial ledger is
\[
\begin{aligned}
H_8={}&G_8+\tfrac18G_7''+\tfrac1{128}G_6^{(4)}
-\tfrac1{192}G_5^{(4)}+\tfrac1{3072}G_5^{(6)}\\
&-\tfrac1{1536}G_4^{(6)}+\tfrac1{98304}G_4^{(8)}
+\tfrac1{2880}G_3^{(6)}\\
&-\tfrac1{24576}G_3^{(8)}
+\tfrac1{3932160}G_3^{(10)}\\
&+\tfrac7{122880}G_2^{(8)}
-\tfrac1{589824}G_2^{(10)}
+\tfrac1{188743680}G_2^{(12)}.
\end{aligned}
\tag{8}
\]
Every kernel and derivative in (8) is evaluated at \(x=1/2\).
The coefficients come from exact central binomial moments.

The saddle/Gamma and determinant recurrences through profile rank
eight give
\[
\boxed{
H_8(t)=\frac{t^9R_8(t)}{587865600(1-t)^{19}},
}
\tag{9}
\]
where
\[
\begin{aligned}
R_8(t)={}&5468059639079t^{19}-98425073503422t^{18}
+832166041491657t^{17}\\
&-4386391163231004t^{16}+16131986564398785t^{15}
-43895988773511894t^{14}\\
&+91460251525777407t^{13}-149080189693453272t^{12}\\
&+192876273599662584t^{11}-200404423224844200t^{10}\\
&+169391623321654920t^9-117375238792050480t^8\\
&+66995289814356720t^7-26873881152249600t^6\\
&+9672918137406720t^5+437297380128000t^4\\
&+8356871743516800t^3+4715036594956800t^2\\
&+1054989778348800t+65474119065600.
\end{aligned}
\tag{10}
\]
There is no interpolation in \(t\).  The fixed symbol shift gives
\[
B_6(t)=B_5(t)+\frac{H_8(t)}{2t^4},
\tag{11}
\]
which simplifies exactly to (4)--(5).  Finally,
\[
\frac1{2764687709306880000}
P_6(t\,d/dt)\frac{t^6}{1-t}=B_6(t),
\tag{12}
\]
so coefficient extraction proves (2) for every \(d\ge6\).

The raw rank-eight computation took approximately 14.4 minutes and
306 MB maximum resident memory on the reference run.

## 2. Sign certificate

Put \(d=x+6\).  The coefficients of \(P_6(x+6)\), in descending
order, are
\[
\begin{aligned}
(&7301929250,\ 941988080250,\ 58295026014225,\\
&2274232483278000,\ 62166945552503700,\ 1256801560135493400,\\
&19387240707676218440,\ 232564705814811472200,\\
&2194101148604030264712,\ 16373287079887463406810,\\
&96732631652867719661535,\ 450655573220183287596600,\\
&1639890235840779094207826,\ 4585140827734156411144500,\\
&9599799660931504120721400,\ 14455833747745470425636400,\\
&14644537342940330377883712,\ 8814813642957150399767040,\\
&2352735417181608345600000).
\end{aligned}
\tag{13}
\]
All are positive, proving \(\beta_{d,6}>0\).

## 3. Fifth Newton difference

Exact simplification gives
\[
a_{d,5}^2-a_{d,4}a_{d,6}
=\frac{N_5(d)}
{189614226555170036121600000d^2(d-5)(d-4)^2
(d-3)^2(d-2)^2(d-1)^2}.
\tag{14}
\]
The coefficients of \(N_5(x+6)\), in descending order, are
\[
\begin{aligned}
(&69470851866797500,\ 15638686808048727500,\\
&1692438135779771455250,\ 117306562346582019239500,\\
&5851834216795713308922900,\ 223791964873779292529260050,\\
&6823335626558847150723998925,\ 170284383227143719884716498650,\\
&3543529604972697083086850895150,\\
&62321669381152809660915474230310,\\
&935661128541476206044715258720113,\\
&12080941593776278809900483961347066,\\
&134887210113497901348986554175465574,\\
&1307523243567608522065994855650934658,\\
&11033435449602666615161953576791213567,\\
&81181560419480148027891270378549171438,\\
&521151040644113432983876665044064700806,\\
&2918040341560935433833863197742596700166,\\
&14232487586826040962564851320599581343401,\\
&60327734886632935387320413983563697305010,\\
&221446563463978453483623659383672150844278,\\
&700487035848819771968695613389982184073844,\\
&1896893576954585071094524805622644776083720,\\
&4359378890317639941043598299719425121649152,\\
&8406518819280013617620094471956224868635680,\\
&13401358136171686622386460317752288897210432,\\
&17313104751569579975489428166667141828753024,\\
&17632385148390493450758615685750967578589184,\\
&13593845681578539482922041987218835418458112,\\
&7432427914770282547887341185706846147543040,\\
&2553222645752405666419761930693103583232000,\\
&409444594484139709293271197438443520000000).
\end{aligned}
\tag{15}
\]
All 32 coefficients and the denominator in (14) are positive for
\(d\ge6\), proving (6).  The successive-ratio argument from the
preceding Newton theorems gives
\[
a_{d,6}<a_{d,1}^6\le(3d^2)^6,
\]
and hence (7).

## 4. Verification

The fast mode of
`independent_verify_ordinary_rank_six_symbol.py` verifies the Euler
identity, sign, fifth Newton difference, direct \(C=3\) gap, and exact
ordinary polynomials at depths \(6,\ldots,12\).  The full mode
recomputes profile rank eight, 27 profile-filtration/endpoint-jet
checks, \(H_8\), and \(B_6\):

```bash
python3 independent_verify_ordinary_rank_six_symbol.py \
  --full-symbolic
pytest -q test_independent_verify_ordinary_rank_six_symbol.py
```
