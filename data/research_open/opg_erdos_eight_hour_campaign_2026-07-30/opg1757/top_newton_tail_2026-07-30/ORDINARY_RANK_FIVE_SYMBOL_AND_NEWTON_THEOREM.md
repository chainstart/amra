# OPG-1757: the rank-five ordinary symbol and fourth Newton inequality

Date: 2026-07-30

## 0. Result

Write
\[
b_{k,d}=\sum_{r=0}^{d}\beta_{d,r}k^{d-r},
\qquad
a_{d,r}=\frac{(-1)^r\beta_{d,r}}{\binom dr}.
\tag{1}
\]

### Theorem 1 (rank-five symbol)

For every \(d\ge5\),
\[
\boxed{\beta_{d,5}=\frac{P_5(d)}{42664933785600},}
\tag{2}
\]
where
\[
\begin{aligned}
P_5(d)={}&-15479380d^{15}-325941210d^{14}
-3742393522d^{13}-6592418448d^{12}\\
&+111326408900d^{11}+573131680737d^{10}
-2606390331587d^9\\
&-10630453797180d^8+79178201476618d^7
+110117646980439d^6\\
&-1139766102529649d^5-2901603595595082d^4\\
&+14532178406634252d^3+4464839765897784d^2\\
&+14350329772954848d-57046347650960640.
\end{aligned}
\tag{3}
\]
Equivalently,
\[
\boxed{
\sum_{d\ge5}\beta_{d,5}t^d
=-\frac{t^5Q_5(t)}{6531840(1-t)^{16}},
}
\tag{4}
\]
with
\[
\begin{aligned}
Q_5(t)={}&9543257389t^{15}-140250399969t^{14}
+951749798832t^{13}\\
&-3945460303470t^{12}+11135319369237t^{11}
-22571194746933t^{10}\\
&+33805605333654t^9-38027667126492t^8
+32629922959320t^7\\
&-21910689192672t^6+12053146354704t^5
-4690002325680t^4\\
&+1006414204320t^3+1035063126720t^2
+1393726461120t+363745105920.
\end{aligned}
\tag{5}
\]

### Theorem 2 (fourth normalized Newton inequality)

For every \(d\ge5\),
\[
\boxed{
\beta_{d,5}<0,
\qquad
a_{d,4}^2>a_{d,3}a_{d,5}.
}
\tag{6}
\]
Together with the rank-three and rank-four theorems, this proves that
\[
a_{d,0},a_{d,1},a_{d,2},a_{d,3},a_{d,4},a_{d,5}
\]
form a strictly positive, strictly log-concave prefix.  In particular,
\[
\boxed{
|\beta_{d,5}|
<\binom d5(3d^2)^5.
}
\tag{7}
\]

These are all-depth theorems.  The finite values that first suggested
(2) are redundant audits and are not used to promote an interpolation
to an infinite statement.

## 1. Exact profile-rank-seven derivation

The all-fixed-rank recurrence requires profile ranks through seven and
determinant kernels \(G_2,\ldots,G_7\).  The exact central-binomial
rank-seven ledger is
\[
\begin{aligned}
H_7={}&G_7(\tfrac12)+\frac18G_6''(\tfrac12)
+\frac1{128}G_5^{(4)}(\tfrac12)\\
&-\frac1{192}G_4^{(4)}(\tfrac12)
+\frac1{3072}G_4^{(6)}(\tfrac12)\\
&-\frac1{1536}G_3^{(6)}(\tfrac12)
+\frac1{98304}G_3^{(8)}(\tfrac12)\\
&+\frac1{2880}G_2^{(6)}(\tfrac12)
-\frac1{24576}G_2^{(8)}(\tfrac12)
+\frac1{3932160}G_2^{(10)}(\tfrac12).
\end{aligned}
\tag{8}
\]
The arguments \(t\) are suppressed.  Every coefficient in (8) is an
exact coefficient of a normalized central binomial moment.

The symbolic saddle/Gamma recurrence and determinant convolution give
\[
\boxed{
H_7(t)=-\frac{t^8R_7(t)}{3265920(1-t)^{16}},
}
\tag{9}
\]
where
\[
\begin{aligned}
R_7(t)={}&9543257389t^{16}-143148860835t^{15}
+994394387070t^{14}\\
&-4235267606808t^{13}+12338941458459t^{12}
-25976391558075t^{11}\\
&+40729494946896t^{10}-48438581343930t^9
+44391584537658t^8\\
&-32029801985664t^7+18828105712416t^6
-8334690418656t^5\\
&+2529274688640t^4+694098084960t^3
+1370090181600t^2\\
&+343631393280t+27695001600.
\end{aligned}
\tag{10}
\]
This is a rational-function identity in \(t\), with no evaluation or
interpolation in \(t\).

The general symbol formula has the fixed shift \(t^{-4}\):
\[
B_5(t)=\frac1{2t^4}\sum_{n=2}^{7}H_n(t)
=B_4(t)+\frac{H_7(t)}{2t^4}.
\tag{11}
\]
Substitution of the already certified \(B_4\) and (9) gives (4)
exactly.  In particular, the shift in (11) is \(t^{-4}\), not
\(t^{-5}\).

Applying the Euler operator \(\mathcal D=t\,d/dt\) gives
\[
\frac1{42664933785600}
P_5(\mathcal D)\frac{t^5}{1-t}=B_5(t).
\tag{12}
\]
Coefficient extraction proves (2) for every \(d\ge5\).

## 2. Sign of the fifth symbol

Put \(d=x+5\).  The coefficients of \(-P_5(x+5)\), in descending
order, are
\[
\begin{aligned}
(&15479380,\ 1486894710,\ 67191650722,\ 1871753987628,\\
&35618057183380,\ 487153250874213,\ 4924255190645987,\\
&37353795240626970,\ 214095975249271382,\\
&926530002338077431,\ 2998723160852584529,\\
&7103132608484505432,\ 11851571303245313388,\\
&13084600004741630736,\ 8521014920490726912,\\
&2375924832652492800).
\end{aligned}
\tag{13}
\]
They are all strictly positive.  Thus
\(-\beta_{d,5}>0\) for every \(d\ge5\).

## 3. The fourth Newton difference

Use the proved formulas
\[
e_3=-\beta_{d,3},\qquad e_4=\beta_{d,4},
\qquad e_5=-\beta_{d,5},
\qquad a_{d,r}=e_r/\binom dr.
\]
Exact simplification gives
\[
a_{d,4}^2-a_{d,3}a_{d,5}
=\frac{N_4(d)}
{49764378767523840000d^2(d-4)(d-3)^2(d-2)^2(d-1)^2}.
\tag{14}
\]
The coefficients of \(N_4(x+5)\), in descending order, are
\[
\begin{aligned}
(&7651199698100,\ 1237597045030500,\ 94907771803546940,\\
&4594900400676079620,\ 157717485063727942304,\\
&4084767615821780052564,\ 82928579453402767481894,\\
&1353260502620725367851602,\ 18056644655159041540107269,\\
&199354648423578446786849781,\ 1836098256945079163653427660,\\
&14183945530910985502271055300,\\
&92203515210061708968995954246,\\
&505118222304834396807784612122,\\
&2331798821082257123412182761130,\\
&9055575888165319080275786127750,\\
&29482963966013532619263960643625,\\
&80015568674364057265657330701057,\\
&179423601505917551756876533742544,\\
&328007283129199861070367839699592,\\
&479260695484669918874657832496656,\\
&543622277324877682678540428085776,\\
&458648156396417487832548475708032,\\
&269748979372545468173123013294336,\\
&99131996581763541208925051289600,\\
&17623654313236332691052298240000).
\end{aligned}
\tag{15}
\]
All 26 coefficients and the denominator in (14) are positive for
\(x\ge0\).  This proves (6).

Strict normalized log-concavity through rank five makes the successive
ratios \(a_{d,r}/a_{d,r-1}\), \(1\le r\le5\), strictly decreasing.
Each is at most \(a_{d,1}\).  Hence
\[
a_{d,5}<a_{d,1}^5\le(3d^2)^5,
\]
which proves (7).  The verifier also checks (7) directly by a
positive-shift numerator certificate.

## 4. Verification

`independent_verify_ordinary_rank_five_symbol.py` has two modes.

The fast mode verifies:

- the Euler identity (12);
- the sign certificate (13);
- the exact Newton difference (14)--(15);
- the rank-five \(C=3\) consequence; and
- independent exact ordinary polynomials at depths \(5,\ldots,12\).

The full symbolic mode recomputes profiles through rank seven, all
determinant kernels needed by (8), \(H_7\), and (11).  It computes only
central rank seven and reuses the already certified \(B_4\), avoiding
six unnecessary lower-rank expansions:

```bash
python3 independent_verify_ordinary_rank_five_symbol.py \
  --full-symbolic
pytest -q test_independent_verify_ordinary_rank_five_symbol.py
```

On the reference run the complete raw rank-seven calculation used
about 193 MB maximum resident memory.  The full recurrence is the
logical all-depth certificate; finite checks alone are not.
