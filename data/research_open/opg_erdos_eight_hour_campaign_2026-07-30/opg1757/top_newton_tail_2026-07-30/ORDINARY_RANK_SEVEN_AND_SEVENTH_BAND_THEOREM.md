# OPG-1757: rank-seven ordinary symbol and seventh long band

Date: 2026-07-30

## 0. Result

The seventh ordinary symbol is the exact degree-\(21\) polynomial
\[
\boxed{
\beta_{d,7}=-\frac{P_7(d)}
{2189632665771048960000}
\qquad(d\ge7),
}
\tag{1}
\]
where, in descending powers,
\[
\begin{aligned}
P_7(d)={}&
30217328900d^{21}
+588271610850d^{20}
+13643387596300d^{19}\\
&-13878287091900d^{18}
-206865593275440d^{17}
-13510109661967215d^{16}\\
&+72376793545393304d^{15}
+23072778779075520d^{14}
+639389903532886168d^{13}\\
&-17666060968351929996d^{12}
+84496255105723314960d^{11}\\
&+489445758683198578404d^{10}
-5864687888148553029676d^9\\
&+15666213093792343586097d^8
-42538398347646927587972d^7\\
&+643254880572068718227472d^6
-3764530202112123124432752d^5\\
&+10480876675598477563463664d^4
-26911510436413086105307392d^3\\
&+76861878762263173992232704d^2
-137796321367666244115302400d\\
&+129244798226101901724057600.
\end{aligned}
\tag{2}
\]
After \(d=u+7\), all 22 coefficients of \(P_7(u+7)\) are
strictly positive.  Hence \(\beta_{d,7}<0\) throughout its
admissible range.

Write, as before,
\[
a_{d,r}=\frac{(-1)^r\beta_{d,r}}{\binom dr}.
\]
The rank-seven symbol also closes the next normalized Newton
inequality and extends the uniform symbol bound:
\[
\boxed{
a_{d,6}^2>a_{d,5}a_{d,7},
\qquad
0<a_{d,7}<(3d^2)^7
\qquad(d\ge7).
}
\tag{3}
\]
Together with the preceding ranks, this proves strict normalized
log-concavity and the \(C=3\) weighted-symbol bound through rank
seven.

More importantly, the seventh long-recurrence band satisfies
\[
\boxed{
\gamma_{d,6}>0\qquad(d\ge13).
}
\tag{4}
\]
It has exact degree \(20\), denominator
\[
C_7=121646259209502720000,
\]
and
\[
\boxed{
\gamma_{d,6}=\frac{R_6(d-13)}{C_7},
}
\tag{5}
\]
where the coefficients of \(R_6(u)\), in descending powers, are
\[
\begin{aligned}
(&3271787244462017050,
623648042617358143000,\\
&55856875934329452263050,
3124374449017856908566000,\\
&122355759286004351589595575,
3564341289917374275903469920,\\
&80099132802493969498884814000,
1421058904493630987185394627680,\\
&20200960399253804993196252363940,
232183805877904273159570354721976,\\
&2167537096961864786157429994245990,
16446364861467480300030466642161360,\\
&101115582702312578695739865178530355,
500203837038278678128508374054816528,\\
&1967490179042233169037740486691569800,
6042615980557589009769445887708502560,\\
&14099566784784874077474835182924882480,
23963972915208111433458538784014037376,\\
&27687602384655981572175962384529653760,
19132079682860615978089318293170457600,\\
&5797589639494004327761299341549568000).
\end{aligned}
\tag{6}
\]
Every integer in (6) is positive, proving (4) directly.

## 1. Strict reconstruction of the rank-seven symbol

`ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md` proves independently
that \(\beta_{d,7}\) is a polynomial in \(d\) of degree at most
\(3\cdot7=21\) on \(d\ge7\).  It is therefore uniquely determined by
22 exact values.

For each
\[
d=7,8,\ldots,32,
\]
the verifier calls
`exact_ordinary_polynomial(d)` from
`independent_verify_all_fixed_rank_ordinary_symbol_algorithm.py`.
That routine does not read a stored rank-seven symbol.  It rebuilds
the fixed-depth ordinary polynomial from the normalized finite
Lagrange/falling profiles and exact binomial averaging.  The
coefficient of \(k^{d-7}\) is, by the ordinary-symbol definition,
\(\beta_{d,7}\).

The values at
\[
d=7,\ldots,28
\tag{7}
\]
interpolate uniquely to (1)--(2).  The four further exact values at
\[
d=29,30,31,32
\tag{8}
\]
are held out from interpolation and agree identically.  Thus (1) is
an all-depth consequence of the proved degree bound and exact source
formula, not an extrapolation based only on empirical degree.

There are two SymPy symbols printed as \(d\) in the source modules
but carrying different assumptions.  The verifier explicitly
substitutes the triangle module's symbol into the independent
ordinary-profile symbol before any polynomial operation.  This
prevents a hidden second free variable from entering the result.

For (3), the verifier forms \(a_{d,5},a_{d,6},a_{d,7}\) exactly and
reduces
\[
a_{d,6}^2-a_{d,5}a_{d,7}.
\]
Its denominator is
\[
\begin{aligned}
&162188424826230242096971776000000\,d^2(d-6)(d-5)^2\\
&\hspace{25mm}\cdot(d-4)^2(d-3)^2(d-2)^2(d-1)^2,
\end{aligned}
\tag{9}
\]
which is positive for \(d\ge7\).  Its reduced numerator has 38
coefficients after \(d=u+7\), all printed in the JSON certificate
and all strictly positive.  Similarly, the reduced numerator of
\[
(3d^2)^7-a_{d,7}
\]
has 22 strictly positive shifted coefficients.  The certificate
records the complete coefficient lists, not only their hashes.

## 2. Exact triangular derivation of the seventh band

Starting from
\[
\beta_{d,0},\ldots,\beta_{d,7},
\]
the verifier applies the exact ordinary-to-falling triangle to
reconstruct
\[
\mathfrak h_0(d),\ldots,\mathfrak h_7(d).
\]
It then applies the exact long-recurrence triangle successively to
obtain
\[
\gamma_{d,0},\ldots,\gamma_{d,6}.
\]
No numerical root finding or floating-point evaluation occurs.

The seventh falling row has the independently expected forced roots
\[
7,8,\ldots,13.
\tag{10}
\]
The final numerator is divisible by \(d-12\), in agreement with the
all-rank boundary factor, and has exact degree \(20\).  Shifting the
first admissible depth \(d=13\) gives (5)--(6).  In particular,
\[
\gamma_{13,6}
=\frac{5764882926530737865899}{120960}>0.
\tag{11}
\]

## 3. Scope

This proves the seventh full-domain positive long-recurrence band.
It does not prove coefficientwise positivity of every band at every
admissible depth; the all-rank theorem currently proves positive
leading coefficients and eventual positivity.

The optional direct profile route
\[
\operatorname{profile\_functions}(9)
\longrightarrow H_9
\longrightarrow B_7=B_6+\frac{H_9}{2t^4}
\]
is a redundant second certificate, not a logical premise of the
finite-interpolation proof above.

A resource-controlled attempt at that redundant route was stopped
after 25 minutes 56 seconds while still factoring a rank-nine
Gaussian moment inside `profile_functions(9)`.  It used less than
95 MB resident memory but had not yet produced \(H_9\).  Accordingly
this note makes no direct \(H_9\) or \(B_7\) symbolic-recurrence
claim; the proved statements rest on the degree theorem, exact source
values, holdouts, and exact triangles described above.

## 4. Reproduction

```bash
python3 verify_ordinary_rank_seven_and_seventh_band.py
pytest -q test_verify_ordinary_rank_seven_and_seventh_band.py
```

The shifted seventh-band coefficient payload has SHA256
`f3602984001b3f92b587cde44fad311d5210f66aee0fc31af7dca1a6310dbac3`.
