# OPG-1757: the rank-four ordinary symbol and third Newton inequality

Date: 2026-07-30

## 0. Result

Write
\[
b_{k,d}=\sum_{r=0}^{d}\beta_{d,r}k^{d-r},
\qquad
a_{d,r}=\frac{(-1)^r\beta_{d,r}}{\binom dr}.
\tag{1}
\]

### Theorem 1 (rank-four symbol)

For every \(d\ge4\),
\[
\boxed{\beta_{d,4}=\frac{P_4(d)}{169305292800},}
\tag{2}
\]
where
\[
\begin{aligned}
P_4(d)={}&
5672590d^{12}+111345780d^{11}+940800098d^{10}
+1247424360d^9\\
&-19928038791d^8-49386060432d^7
+332001672380d^6\\
&+627890141256d^5-5187992393129d^4
-5254056336228d^3\\
&+25894282085892d^2+59075314211664d
-31756394113920.
\end{aligned}
\tag{3}
\]
Equivalently,
\[
\boxed{
\sum_{d\ge4}\beta_{d,4}t^d
=
\frac{t^4Q_4(t)}{155520(1-t)^{13}},
}
\tag{4}
\]
with
\[
\begin{aligned}
Q_4(t)={}&
69010973t^{12}-808314420t^{11}+4268197710t^{10}\\
&-13359121428t^9+27385842717t^8-38351424456t^7\\
&+37307986992t^6-25675484328t^5+13629418560t^4\\
&-6085860480t^3+1956966480t^2+1499316480t
+659404800.
\end{aligned}
\tag{5}
\]

### Theorem 2 (third normalized Newton inequality)

For every \(d\ge4\),
\[
\boxed{
\beta_{d,4}>0,
\qquad
a_{d,3}^2>a_{d,2}a_{d,4}.
}
\tag{6}
\]
Together with `ORDINARY_INITIAL_NEWTON_CHAIN_THEOREM.md`, this proves
that
\[
a_{d,0},a_{d,1},a_{d,2},a_{d,3},a_{d,4}
\]
form a strictly positive, strictly log-concave prefix.  In particular,
\[
\boxed{
|\beta_{d,4}|
\le\binom d4(3d^2)^4.
}
\tag{7}
\]

These are all-depth theorems.  The finite interpolation values used
when the formula was first guessed are not part of the proof.

## 1. Exact profile-rank-six derivation

Use the all-fixed-rank recurrence in
`ALL_FIXED_RANK_ORDINARY_SYMBOL_ALGORITHM_THEOREM.md`.  To compute
\(\beta_{d,4}\), it requires profile ranks through six and determinant
kernels \(G_2,\ldots,G_6\).

The exact central-binomial rank-six ledger is
\[
\begin{aligned}
H_6={}&G_6(\tfrac12)
+\frac18G_5''(\tfrac12)
+\frac1{128}G_4^{(4)}(\tfrac12)\\
&-\frac1{192}G_3^{(4)}(\tfrac12)
+\frac1{3072}G_3^{(6)}(\tfrac12)\\
&-\frac1{1536}G_2^{(6)}(\tfrac12)
+\frac1{98304}G_2^{(8)}(\tfrac12).
\end{aligned}
\tag{8}
\]
The arguments \(t\) have been suppressed.  The coefficients in (8)
come directly from the exact binomial central moments, not a Gaussian
approximation.

The symbolic saddle/Gamma recurrence through profile rank six,
followed by the determinant convolution and (8), gives the rational
identity
\[
\boxed{
H_6(t)
=
\frac{t^7R_6(t)}{77760(1-t)^{13}},
}
\tag{9}
\]
where
\[
\begin{aligned}
R_6(t)={}&
69010973t^{13}-828131676t^{12}+4500844542t^{11}\\
&-14591534844t^{10}+31260693837t^9-46346440896t^8\\
&+48607255008t^7-36796779360t^6+21341475216t^5\\
&-10053253440t^4+3647118960t^3+984234240t^2\\
&+650592000t+50855040.
\end{aligned}
\tag{10}
\]
All operations are rational-function identities in the symbolic loss
variable \(t\); there is no finite-loss interpolation.

The general symbol formula now yields
\[
B_4(t)
=\frac1{2t^4}\sum_{n=2}^{6}H_n(t).
\tag{11}
\]
Substituting the previously proved \(H_2,\ldots,H_5\) and (9)
simplifies exactly to (4)--(5).

Finally, applying the Euler operator
\(\mathcal D=t\,d/dt\) to \(t^4/(1-t)\) shows that the right side of
(4) equals
\[
\frac1{169305292800}
P_4(\mathcal D)\frac{t^4}{1-t}.
\tag{12}
\]
Coefficient extraction proves (2) for every \(d\ge4\).

## 2. Positivity of the fourth symbol

Put \(d=x+4\).  The numerator in (3) becomes
\[
\begin{aligned}
P_4(x+4)={}&
5672590x^{12}+383630100x^{11}+11830269458x^{10}\\
&+216733781880x^9+2596997350329x^8
+21263785247376x^7\\
&+121450423661756x^6+487902290197224x^5\\
&+1375537364691511x^4+2661970848928524x^3\\
&+3302274805667316x^2+2273243721353136x\\
&+717854441472000.
\end{aligned}
\tag{13}
\]
Every coefficient is positive, proving \(\beta_{d,4}>0\).

## 3. The third Newton difference

Use the proved formulas for
\[
e_2=\beta_{d,2},\qquad
e_3=-\beta_{d,3},\qquad
e_4=\beta_{d,4},
\]
and
\[
a_{d,r}=e_r/\binom dr.
\]
Exact simplification gives
\[
a_{d,3}^2-a_{d,2}a_{d,4}
=
\frac{N_3(d)}
{1371372871680000d^2(d-3)(d-2)^2(d-1)^2}.
\tag{14}
\]
After \(d=x+4\), the coefficients of \(N_3(x+4)\), in descending
order, are
\[
\begin{aligned}
(&54067762000,\ 5810377016500,\ 289638866979525,\\
&8903905795452675,\ 189164615281077750,\\
&2948091878218321050,\ 34901746977006261385,\\
&320605868529267491380,\ 2314074253976124664263,\\
&13210919944847952061038,\ 59784760493297808636630,\\
&214210520420341401251625,\ 605451963779233153705999,\\
&1342509840636633198201364,\ 2318691434453416880051760,\\
&3084679203056865803765520,\ 3083735149936893218156688,\\
&2176060189375149048070848,\ 932354656857985560192000,\\
&163237963290215546880000).
\end{aligned}
\tag{15}
\]
They are all strictly positive, as is the denominator for \(d\ge4\).
This proves (6).

The three strict Newton inequalities say that the successive ratios
\[
\frac{a_{d,2}}{a_{d,1}},\qquad
\frac{a_{d,3}}{a_{d,2}},\qquad
\frac{a_{d,4}}{a_{d,3}}
\]
are strictly decreasing and each is smaller than
\(a_{d,1}/a_{d,0}=a_{d,1}\).  Multiplying the four successive-ratio
bounds gives
\[
a_{d,4}<a_{d,1}^4.
\]
Since \(a_{d,1}\le3d^2\), equation (7) follows.

## 4. Verification

`independent_verify_ordinary_rank_four_symbol.py` has two modes.

The fast mode verifies:

- the Euler-operator identity (12);
- positivity (13);
- the exact Newton difference (14)--(15);
- the rank-four \(C=3\) consequence; and
- independent exact ordinary polynomials at unused finite depths.

The full symbolic mode additionally recomputes profile rank six,
\(G_2,\ldots,G_6\), \(H_6\), and (11) from the audited recurrences:

```bash
python3 independent_verify_ordinary_rank_four_symbol.py \
  --full-symbolic
pytest -q test_independent_verify_ordinary_rank_four_symbol.py
```

The full mode is intentionally slower.  It is the logical certificate
for the all-depth statement; the finite exact checks are only redundant
audits.
