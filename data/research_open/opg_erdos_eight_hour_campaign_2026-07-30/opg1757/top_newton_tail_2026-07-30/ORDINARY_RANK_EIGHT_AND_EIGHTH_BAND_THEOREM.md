# OPG-1757: rank-eight ordinary symbol and eighth long band

Date: 2026-07-30

## 0. Result

For every \(d\ge8\),
\[
\boxed{
\beta_{d,8}=\frac{P_8(d)}
{16395969401293614612480000}>0,
}
\tag{1}
\]
where
\[
\begin{aligned}
P_8(d)={}&889430541350d^{24}+14622142134600d^{23}
+548021093858420d^{22}\\
&-2856959481810720d^{21}+28701596207603462d^{20}
-1423489168742166240d^{19}\\
&+12861217758561559244d^{18}
-82998625358866417200d^{17}
+922977463212725257961d^{16}\\
&-8177441437699868025120d^{15}
+42938933142825418811336d^{14}
-76677846419551695275328d^{13}\\
&-511184340302410319000404d^{12}
+3899371073189547912083712d^{11}\\
&-37899401549116356635663992d^{10}
+491762300999382375736137936d^9\\
&-3768699654323965134722976313d^8
+18306948644611241354070999096d^7\\
&-76768891977718913728168749960d^6
+337541647224593255540675147712d^5\\
&-1258527065761592686759918183056d^4
+3449860233699583645836821626752d^3\\
&-7267027629287109649368128456448d^2
+11300732071776760453999392614400d\\
&-9638644787509862596194526003200.
\end{aligned}
\tag{2}
\]
All 25 coefficients of \(P_8(u+8)\) are strictly positive.

With
\[
a_{d,r}=\frac{(-1)^r\beta_{d,r}}{\binom dr},
\]
the next normalized Newton inequality and weighted-symbol bound hold:
\[
\boxed{
a_{d,7}^2>a_{d,6}a_{d,8},
\qquad
0<a_{d,8}<(3d^2)^8
\qquad(d\ge8).
}
\tag{3}
\]
Thus strict normalized log-concavity and the uniform \(C=3\) bound
now hold through rank eight.

The eighth long-recurrence band is positive on its complete
admissible range:
\[
\boxed{
\gamma_{d,7}>0\qquad(d\ge15).
}
\tag{4}
\]
More precisely,
\[
\gamma_{d,7}
=\frac{R_7(d-15)}{113860898620094545920000},
\tag{5}
\]
where the coefficients of \(R_7(u)\), in descending powers, are
\[
\begin{aligned}
(&1561601241389666024275,
378257654066055578742200,\\
&43399151014977476474715960,
3137341234190203371435584480,\\
&160345102804655406389036745460,
6162432321193972015605848689540,\\
&184930471488563387807542380122350,
4441537634902915859699052686640620,\\
&86810758260458031410774898153155334,
1396506238942381836020155538489736680,\\
&18627223852830009296590007747380961716,
206892528211131527712409474560588414712,\\
&1916590565131653997450556325484105603348,
14795096556097939423935444403243192448948,\\
&94848423278978965804367181698045318803998,
501854322963927159548511227603583584664956,\\
&2170848974618952759804845680663967943292447,
7571820422883198432491827526054561127879784,\\
&20880363921400777632652337367622449796361496,
44244355779537170896799258677444794474104832,\\
&69010100928202046265813651364774426539617136,
73917818536575003240583435087381568243730048,\\
&47854944406348979688454154428638998068366080,
13762189506637017969286097171436879613132800).
\end{aligned}
\tag{6}
\]
All 24 integers in (6) are positive.

## 1. Rank-eight reconstruction

`ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md` proves before this
calculation that \(\deg_d\beta_{d,8}\le24\).  Therefore 25 exact
values uniquely determine the symbol.

For each \(d=8,\ldots,36\), the verifier independently rebuilds the
fixed-depth ordinary polynomial using
`exact_ordinary_polynomial(d)` and extracts its
\(k^{d-8}\) coefficient.  The values at
\[
d=8,\ldots,32
\]
alone determine (1)--(2).  The values at
\[
d=33,34,35,36
\]
are excluded from interpolation and all agree exactly with (1).
The degree bound is a proved input, not an empirical conclusion from
the sampled values.

The source and triangle modules use two printed \(d\) symbols with
different SymPy assumptions.  Every lower symbol is explicitly
substituted from `TRIANGLE_D` to the independent `D` before the
triangles are evaluated.

## 2. Positivity certificates

The verifier reduces
\[
a_{d,7}^2-a_{d,6}a_{d,8}
\]
and expands its numerator at \(d=u+8\).  All 44 resulting
coefficients are printed in the JSON certificate and strictly
positive.  Its payload SHA256 is
`3beb8729bdbb110c7694c3da5b56b4f38cce48bfa23ffe90b9976df45b5bf2c3`.

Likewise, the reduced numerator of
\[
(3d^2)^8-a_{d,8}
\]
has 25 strictly positive coefficients after \(d=u+8\), all included
in the certificate.  Its SHA256 is
`cc81f974a0d321000b5ed3a69a9e040a95240db41da897937573ccfe37826b87`.
The corresponding reduced denominators are factored and printed so
their positivity on \(d\ge8\) is directly checkable.

## 3. Exact eighth-band derivation

The exact ordinary-to-falling triangle reconstructs
\(\mathfrak h_0,\ldots,\mathfrak h_8\), and the long-recurrence
triangle then reconstructs
\(\gamma_{d,0},\ldots,\gamma_{d,7}\).  The eighth falling row has all
forced roots
\[
8,9,\ldots,15,
\]
and the numerator of \(\gamma_{d,7}\) has the expected factor
\(d-14\).  It has exact degree \(23\).  Shifting the first
admissible depth gives (5)--(6), and
\[
\gamma_{15,7}
=\frac{2631644430366587366723616427}{21772800}>0.
\]

No floating-point calculation or empirical degree inference is used.

## 4. Scope and reproduction

This proves the eighth full-domain positive long-recurrence band,
not coefficientwise positivity of every band at arbitrary rank.

```bash
python3 verify_ordinary_rank_eight_and_eighth_band.py
pytest -q test_verify_ordinary_rank_eight_and_eighth_band.py
```

The shifted eighth-band coefficient payload has SHA256
`433f384ada20eaa4a9ea9869d8057e98a51ff2f6d3f0f195a2e55530badae019`.
