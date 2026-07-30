# Independent audit: rank-seven symbol and seventh long band

Date: 2026-07-30

Audited files:

* `ORDINARY_RANK_SEVEN_AND_SEVENTH_BAND_THEOREM.md`
* `verify_ordinary_rank_seven_and_seventh_band.py`
* `test_verify_ordinary_rank_seven_and_seventh_band.py`

Independent files:

* `independent_verify_ordinary_rank_seven_and_seventh_band.py`
* `test_independent_verify_ordinary_rank_seven_and_seventh_band.py`

## 0. Verdict

\[
\boxed{\text{PASS}}
\]

All claims requested for audit pass:

1. the exact degree-\(21\) polynomial for \(\beta_{d,7}\);
2. four exact depth holdouts not used in interpolation;
3. negativity of \(\beta_{d,7}\) from 22 positive shifted
   coefficients;
4. the strict normalized inequality
   \(a_{d,6}^2>a_{d,5}a_{d,7}\);
5. positivity and the \(C=3\) bound
   \(0<a_{d,7}<(3d^2)^7\);
6. the exact degree-\(20\) formula and full-domain positivity of
   \(\gamma_{d,6}\);
7. the seven forced roots of the seventh Newton row; and
8. correct unification of the otherwise distinct SymPy depth symbols.

No mathematical or implementation error was found in the theorem or
the author's verifier.

## 1. Independence boundary

The independent verifier does **not** import
`verify_ordinary_rank_seven_and_seventh_band.py`, does not import its
test, and does not use a stored rank-seven symbol to generate the
fixed-depth data.

The common, previously audited axiom layer is limited to:

* the all-rank theorem
  \(\deg_d\beta_{d,7}\le21\);
* the primitive exact finite-profile value
  `exact_ordinary_value(page_count, depth)` from
  `independent_verify_all_fixed_rank_ordinary_symbol_algorithm.py`;
* the already audited lower symbols
  \(\beta_{d,0},\ldots,\beta_{d,6}\).

Above that common layer, all reconstruction is new:

* the independent verifier calls the primitive exact value directly;
  it does **not** call `exact_ordinary_polynomial`;
* for each fixed depth, it rebuilds the monic ordinary polynomial by
  the defining Lagrange products and uses two page-count holdouts;
* it uses a different set of depth interpolation/holdout nodes from
  the author;
* it independently rebuilds signed Stirling rows, the
  ordinary-to-Newton triangle, and the long-recurrence triangle.

Thus this is not a comparison of two scripts reading the same stored
rank-seven coefficient table.  The only shared data generator is the
audited finite-profile source below the rank-seven theorem.

## 2. Independent rank-seven reconstruction

For each depth \(d\), the audit evaluates the exact finite-profile
formula at \(d+1\) page counts.  Given exact points
\((k_i,y_i)\), it constructs
\[
\boxed{
 P_d(k)=
 \sum_i y_i
 \prod_{j\ne i}\frac{k-k_j}{k_i-k_j}
}
\tag{1}
\]
over \(\mathbb Q[k]\), without calling SymPy's project-level ordinary
polynomial helper.  It verifies that \(P_d\) is monic of degree \(d\)
and checks two further page counts not used in (1).  It then extracts
\([k^{d-7}]P_d(k)\).

The 22 depth nodes used to interpolate \(\beta_{d,7}\) are
\[
 d=8,9,\ldots,29.
\tag{2}
\]
The four unused exact checks are
\[
\boxed{d=7,30,31,32.}
\tag{3}
\]
In particular, the first admissible depth is a holdout rather than an
interpolation node.

The resulting polynomial has exact degree 21 and equals
\[
\beta_{d,7}
=-\frac{P_7(d)}{2189632665771048960000},
\tag{4}
\]
with every one of the 22 coefficients of \(P_7\) agreeing with
equation (2) of the theorem.  The denominator in (4) is reduced.

After \(d=u+7\), the descending coefficient row of \(P_7\) is
\[
\begin{aligned}
(&30217328900,\ 5030218959150,\ 406937727496300,\\
&21062344231120500,\ 776610943210176360,\\
&21570208638735074175,\ 466465370655512663864,\\
&8020542960905087173440,\ 111153258122616106542808,\\
&1252342399879799258311692,\ 11526856540340618885659392,\\
&86814123123061472086793988,\ 534236507954722431911624924,\\
&2673695554818903265509573231,\\
&10791865937155927068806752204,\\
&34680170012028856038934611984,\\
&87059049275261964003182635248,\\
&166030226917232351743952788752,\\
&230636749356582953558492787840,\\
&218105728764319777804791660288,\\
&124124939578259721102715176960,\\
&31548840545575689309388800000).
\end{aligned}
\tag{5}
\]
All entries are positive.  The payload hash is
`06b4ba0bb503578bc318b953afc8ebe8a0dc1116048c80440850b0aae261ff9d`.
This proves \(\beta_{d,7}<0\) for every \(d\ge7\).

## 3. Depth-symbol mismatch audit

The finite-profile module defines a symbol printed as `d`.  The new
audit deliberately defines its triangle variable as
`depth`, with integer assumptions:
\[
 D_{\rm profile}=\operatorname{Symbol}(\texttt{"d"}),
 \qquad
 D_{\rm audit}=\operatorname{Symbol}(\texttt{"depth"},
 \texttt{integer=True}).
\tag{6}
\]
The verifier asserts that these are unequal objects.  Every imported
lower-rank polynomial function is called with
\(D_{\rm audit}\) explicitly, and it checks that
\(D_{\rm profile}\) is absent from the free-symbol set of all eight
\(\beta\)-polynomials before either triangle is formed.

The author's verifier uses a different but valid remedy: it explicitly
substitutes its triangle module's symbol by the profile symbol.  Both
routes leave exactly one depth variable.  No hidden bivariate
polynomial occurs.

## 4. Sixth normalized Newton inequality and \(C=3\)

The audit independently forms
\[
 a_{d,r}=\frac{(-1)^r\beta_{d,r}}{\binom dr}.
\]
Exact cancellation of
\[
 a_{d,6}^2-a_{d,5}a_{d,7}
\]
gives the same reduced denominator
\[
\begin{aligned}
162188424826230242096971776000000\,d^2(d-6)(d-5)^2
(d-4)^2(d-3)^2(d-2)^2(d-1)^2.
\end{aligned}
\tag{7}
\]
It is positive for \(d\ge7\).  After \(d=u+7\), the reduced numerator
has 38 strictly positive coefficients.  The independent full-list
hash is
`3279d8dd6f05921e1a9f5673693ca1821f755243a83d9740f1a226eb05be561c`,
identical to the author's payload.

Likewise,
\[
(3d^2)^7-a_{d,7}
\]
has reduced denominator
\[
434450925748224000\,d(d-6)(d-5)(d-4)(d-3)(d-2)(d-1),
\tag{8}
\]
positive on \(d\ge7\), and its shifted numerator has 22 strictly
positive coefficients.  Its full-list hash is
`e88a1cb1d3a7ecfe6a54a7ada885733606a072303643dade1e0c669deba05375`.
Together with (5), this proves
\[
0<a_{d,7}<(3d^2)^7.
\tag{9}
\]

The JSON emitted by the independent verifier records all 38 and all
22 coefficients explicitly, not only their hashes.

## 5. Independent Stirling, Newton, and recurrence triangles

The signed Stirling rows are rebuilt from exact Faulhaber power sums
and Newton's elementary-symmetric identities:
\[
p_j(n)=\sum_{a=0}^{n-1}a^j,
\qquad
m e_m(n)
=\sum_{j=1}^m(-1)^{j-1}e_{m-j}(n)p_j(n),
\qquad
s_m(n)=(-1)^me_m(n).
\tag{10}
\]
The implementation additionally verifies
\[
s_m(n+1)-s_m(n)=-n\,s_{m-1}(n)
\qquad(1\le m\le7).
\tag{11}
\]

It then solves, independently,
\[
h_{d,\ell}
=
\sum_{r=0}^{\ell}
\beta_{d,r}\binom{d-r}{\ell-r}2^{\ell-r}
-
\sum_{j=0}^{\ell-1}
h_{d,j}s_{\ell-j}(d-j)
\tag{12}
\]
through \(\ell=7\), followed by
\[
\gamma_{d,q}
=h_{d,q+1}-h_{d+1,q+1}
-
\sum_{i=0}^{q-1}
\gamma_{d,i}h_{d-1-2i,q-i}
\tag{13}
\]
through \(q=6\).  No author's \(\gamma\)-formula is supplied to this
calculation.

At the first depth \(d=13\), the six lower calls in (13) are
\[
(12,6),(10,5),(8,4),(6,3),(4,2),(2,1),
\tag{14}
\]
where each pair is `(depth,row)`.  Every depth is exactly twice its
row, so the boundary indexing is correct.

## 6. Seventh-band result

The independently derived \(\gamma_{d,6}\) has:

* exact degree \(20\);
* reduced denominator
  \[
  121646259209502720000;
  \]
* numerator divisible by \(d-12\);
* the same 21 coefficients after \(d=u+13\) as equation (6) of the
  theorem;
* all 21 shifted coefficients strictly positive.

The full shifted payload has SHA256
`f3602984001b3f92b587cde44fad311d5210f66aee0fc31af7dca1a6310dbac3`,
matching the theorem.  The boundary value is
\[
\boxed{
\gamma_{13,6}
=\frac{5764882926530737865899}{120960}>0.
}
\tag{15}
\]
Therefore
\[
\gamma_{d,6}>0\qquad(d\ge13)
\tag{16}
\]
on the entire admissible range.

The seventh Newton row factors by
\[
\prod_{r=7}^{13}(d-r).
\tag{17}
\]
The residual denominator is
\[
2189632665771048960000,
\]
and exact gcd with (17) is one.  Thus the seven forced integer roots
\(7,\ldots,13\) are simple and are not cancellation artifacts.

## 7. Reproduction

Independent audit:

```bash
python3 independent_verify_ordinary_rank_seven_and_seventh_band.py
pytest -q test_independent_verify_ordinary_rank_seven_and_seventh_band.py
```

The independent test suite checks the defining Lagrange implementation,
all four depth holdouts, symbol separation, every requested exact
payload, and an AST audit proving that the author's verifier is not an
import dependency.

The conclusion relies on the all-rank degree-\(21\) bound and the
previously audited finite-profile generator as stated in Section 1.
It does not establish rank eight, the eighth long band, all-band
positivity, or OPG-1757.
