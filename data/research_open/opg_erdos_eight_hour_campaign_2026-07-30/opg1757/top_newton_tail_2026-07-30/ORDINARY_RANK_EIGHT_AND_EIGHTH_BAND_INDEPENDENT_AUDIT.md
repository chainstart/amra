# Independent rank-eight symbol and eighth-band certificate

Date: 2026-07-30

Verifier:
`independent_verify_ordinary_rank_eight_and_eighth_band.py`

## 0. Outcome

\[
\boxed{\text{PASS}}
\]

Before any author rank-eight verifier or coefficient table appeared,
the independent exact finite-profile route produced:

\[
\boxed{
\beta_{d,8}
=\frac{P_8(d)}{16395969401293614612480000}
\qquad(d\ge8),
}
\tag{1}
\]
where \(P_8\) has exact degree 24 and
\(P_8(u+8)\) has 25 strictly positive coefficients.  Hence
\(\beta_{d,8}>0\) throughout its admissible range.

With
\[
a_{d,r}=\frac{(-1)^r\beta_{d,r}}{\binom dr},
\]
the same reconstruction proves
\[
\boxed{
a_{d,7}^2>a_{d,6}a_{d,8},
\qquad
0<a_{d,8}<(3d^2)^8
\qquad(d\ge8).
}
\tag{2}
\]

Finally, the independently rebuilt ordinary-to-falling and
long-recurrence triangles give
\[
\boxed{
\gamma_{d,7}>0\qquad(d\ge15).
}
\tag{3}
\]

## 1. Independence and uniqueness

No author rank-eight verifier, author rank-eight test, or stored author
rank-eight coefficient list is imported.  At the time of this
calculation no such file was present.

The common audited axiom layer is:

1. the all-rank bound
   \[
   \deg_d\beta_{d,8}\le3\cdot8=24;
   \]
2. the primitive finite-profile value
   `exact_ordinary_value(page_count, depth)`;
3. the independently audited lower symbols
   \(\beta_{d,0},\ldots,\beta_{d,7}\).

For each fixed depth, the verifier reconstructs the monic ordinary
polynomial directly from \(d+1\) primitive values using the defining
Lagrange products.  It does not call `exact_ordinary_polynomial`.
Two additional page counts check every reconstructed fixed-depth
polynomial before its \(k^{d-8}\) coefficient is extracted.

The 25 depth nodes used for the degree-\(24\) interpolation are
\[
\boxed{d=9,10,\ldots,33.}
\tag{4}
\]
The four exact values excluded from interpolation are
\[
\boxed{d=8,34,35,36.}
\tag{5}
\]
All four agree, including the first admissible depth.

The profile source uses `Symbol("d")`; this verifier deliberately uses
`Symbol("rank8_depth", integer=True)` and asserts both that the symbols
are unequal and that the profile symbol is absent from every
lower-rank polynomial entering the triangles.

## 2. Exact rank-eight polynomial

In descending powers, the numerator in (1) is
\[
\begin{aligned}
P_8(d)={}&
889430541350d^{24}
+14622142134600d^{23}
+548021093858420d^{22}\\
&-2856959481810720d^{21}
+28701596207603462d^{20}
-1423489168742166240d^{19}\\
&+12861217758561559244d^{18}
-82998625358866417200d^{17}\\
&+922977463212725257961d^{16}
-8177441437699868025120d^{15}\\
&+42938933142825418811336d^{14}
-76677846419551695275328d^{13}\\
&-511184340302410319000404d^{12}
+3899371073189547912083712d^{11}\\
&-37899401549116356635663992d^{10}
+491762300999382375736137936d^9\\
&-3768699654323965134722976313d^8
+18306948644611241354070999096d^7\\
&-76768891977718913728168749960d^6
+337541647224593255540675147712d^5\\
&-1258527065761592686759918183056d^4\\
&+3449860233699583645836821626752d^3\\
&-7267027629287109649368128456448d^2\\
&+11300732071776760453999392614400d\\
&-9638644787509862596194526003200.
\end{aligned}
\tag{6}
\]

After \(d=u+8\), all 25 coefficients are positive.  Their SHA256 is
`fc42182bba415d93e3fc8ccece107311ab457b775be06240e9990ae2a017607d`.
The verifier JSON records the full coefficient list.

## 3. Seventh normalized Newton inequality and \(C=3\)

Exact cancellation gives the denominator of
\(a_{d,7}^2-a_{d,6}a_{d,8}\) as
\[
\begin{aligned}
&17176032226397484747055763030016000000\,
d^2(d-7)(d-6)^2(d-5)^2\\
&\hspace{25mm}\cdot(d-4)^2(d-3)^2(d-2)^2(d-1)^2.
\end{aligned}
\tag{7}
\]
It is positive for \(d\ge8\).  The reduced numerator after
\(d=u+8\) has 44 strictly positive coefficients, with SHA256
`3beb8729bdbb110c7694c3da5b56b4f38cce48bfa23ffe90b9976df45b5bf2c3`.

For the \(C=3\) gap
\[
(3d^2)^8-a_{d,8},
\]
the reduced denominator is
\[
406646066500337664000\,
d(d-7)(d-6)(d-5)(d-4)(d-3)(d-2)(d-1).
\tag{8}
\]
Its shifted numerator has 25 strictly positive coefficients, with
SHA256
`cc81f974a0d321000b5ed3a69a9e040a95240db41da897937573ccfe37826b87`.
Positivity of \(a_{d,8}\) follows separately from (1) and the positive
shift of \(P_8\).

## 4. Independent eighth long band

The signed Stirling rows through loss eight are generated from exact
Faulhaber power sums and Newton's elementary-symmetric identities.
The verifier then independently solves
\[
h_{d,\ell}
=
\sum_{r=0}^{\ell}
\beta_{d,r}\binom{d-r}{\ell-r}2^{\ell-r}
-
\sum_{j=0}^{\ell-1}
h_{d,j}s_{\ell-j}(d-j)
\tag{9}
\]
through \(\ell=8\), followed by
\[
\gamma_{d,q}
=h_{d,q+1}-h_{d+1,q+1}
-
\sum_{i=0}^{q-1}
\gamma_{d,i}h_{d-1-2i,q-i}
\tag{10}
\]
through \(q=7\).

The result has exact degree 23 and reduced denominator
\[
C_8=113860898620094545920000.
\tag{11}
\]
Writing
\[
\gamma_{d,7}=\frac{R_7(d-15)}{C_8},
\tag{12}
\]
the descending coefficient row of \(R_7\) is
\[
\begin{aligned}
(&1561601241389666024275,\
378257654066055578742200,\\
&43399151014977476474715960,\
3137341234190203371435584480,\\
&160345102804655406389036745460,\
6162432321193972015605848689540,\\
&184930471488563387807542380122350,\\
&4441537634902915859699052686640620,\\
&86810758260458031410774898153155334,\\
&1396506238942381836020155538489736680,\\
&18627223852830009296590007747380961716,\\
&206892528211131527712409474560588414712,\\
&1916590565131653997450556325484105603348,\\
&14795096556097939423935444403243192448948,\\
&94848423278978965804367181698045318803998,\\
&501854322963927159548511227603583584664956,\\
&2170848974618952759804845680663967943292447,\\
&7571820422883198432491827526054561127879784,\\
&20880363921400777632652337367622449796361496,\\
&44244355779537170896799258677444794474104832,\\
&69010100928202046265813651364774426539617136,\\
&73917818536575003240583435087381568243730048,\\
&47854944406348979688454154428638998068366080,\\
&13762189506637017969286097171436879613132800).
\end{aligned}
\tag{13}
\]
All 24 coefficients are positive.  Their SHA256 is
`433f384ada20eaa4a9ea9869d8057e98a51ff2f6d3f0f195a2e55530badae019`.
The first value is
\[
\boxed{
\gamma_{15,7}
=\frac{2631644430366587366723616427}{21772800}>0.
}
\tag{14}
\]
The unshifted numerator is divisible by \(d-14\), as required at the
band boundary.

The eighth Newton row contains
\[
\prod_{r=8}^{15}(d-r).
\tag{15}
\]
The residual polynomial has degree 16, denominator equal to the
rank-eight denominator in (1), and gcd one with (15).  Hence all eight
forced roots are simple.

At \(d=15\), the lower recurrence calls are
\[
(14,7),(12,6),(10,5),(8,4),(6,3),(4,2),(2,1),
\tag{16}
\]
again exactly on the legal parity boundary.

## 5. Post-discovery comparison with the author certificate

The author theorem and verifier appeared only after the independent
formula and all four hashes above had been reported.  The subsequent
comparison found exact agreement in:

* all 25 coefficients of \(P_8\) and its denominator;
* the 25 shifted rank-eight coefficients;
* the 44 normalized-Newton coefficients and denominator;
* the 25 \(C=3\) coefficients and denominator;
* all 24 shifted eighth-band coefficients and denominator;
* \(\gamma_{15,7}\), the factor \(d-14\), and the forced roots.

The two reconstructions use different nodes and different fixed-depth
interfaces.  The author uses depths \(8,\ldots,32\) with holdouts
\(33,\ldots,36\) and calls `exact_ordinary_polynomial`.  This audit
uses depths \(9,\ldots,33\), holds out \(8,34,35,36\), and directly
rebuilds each fixed-depth polynomial from the lower-level primitive.
The AST test confirms that the author rank-eight verifier is not an
import dependency.

## 6. Reproduction

```bash
python3 independent_verify_ordinary_rank_eight_and_eighth_band.py
pytest -q test_independent_verify_ordinary_rank_eight_and_eighth_band.py
```

Combined author and independent tests:

```bash
pytest -q \
  test_verify_ordinary_rank_eight_and_eighth_band.py \
  test_independent_verify_ordinary_rank_eight_and_eighth_band.py
```

Result:

```text
5 passed in 42.22s
```

The certificate is conditional only on the explicitly listed common
axiom layer in Section 1.  It makes no rank-nine or all-band claim.
