# OPG-1757: the sixth all-depth long-recurrence band

Date: 2026-07-30

## 0. Result

Use the notation of
`ORDINARY_FIRST_FIVE_LONG_RECURRENCE_BANDS_THEOREM.md`:
\[
xH_d(x)-H_{d+1}(x)
=
\sum_{q=0}^{\lfloor(d-1)/2\rfloor}
\gamma_{d,q}H_{d-1-2q}(x).
\tag{1}
\]
The rank-six ordinary-symbol theorem closes one more complete band.

### Theorem (sixth positive recurrence band)

For every \(d\ge11\),
\[
\boxed{\gamma_{d,5}>0.}
\tag{2}
\]
More precisely,
\[
\boxed{
\gamma_{d,5}
=
\frac{d-10}{15359376162816000}R_5(d),
}
\tag{3}
\]
where
\[
\begin{aligned}
R_5(d)={}&
810123093896375d^{16}
-25921081431700875d^{15}\\
&+313490671217497970d^{14}
-1492874651122299900d^{13}\\
&-1887303336152228890d^{12}
+49625869946758088130d^{11}\\
&-167524355872717489604d^{10}
-106706576731710308472d^9\\
&+1816293817555406107219d^8
-3108681098587146424959d^7\\
&-2327663884048779946070d^6
+9529661544865824480588d^5\\
&-493471326045590983080d^4
-8190583449886689443856d^3\\
&-15710022013283259194016d^2
+29745938852108657679744d\\
&-5169307325421355490304.
\end{aligned}
\tag{4}
\]
Together with the preceding five-band theorem, this proves
\[
\boxed{
\gamma_{d,q}>0
\quad
(0\le q\le5,\ d\ge2q+1).
}
\tag{5}
\]
This is an all-depth statement.  It is not inferred from the finite
\(d\le50\) recurrence table.

## 1. Exact derivation

Write
\[
P_d(k)=\sum_{r=0}^d\beta_{d,r}k^{d-r},
\qquad
H_d(x)=\sum_jh_{d,j}x^{d-2j}.
\tag{6}
\]
The ordinary-to-Newton triangle is
\[
h_{d,\ell}
=
\sum_{r=0}^{\ell}
\beta_{d,r}\binom{d-r}{\ell-r}2^{\ell-r}
-
\sum_{j=0}^{\ell-1}
h_{d,j}s_{\ell-j}(d-j),
\tag{7}
\]
where \(s_m(n)=s(n,n-m)\) is obtained from the signed Stirling
recurrence.  The long-recurrence triangle is
\[
\gamma_{d,q}
=h_{d,q+1}-h_{d+1,q+1}
-
\sum_{i=0}^{q-1}
\gamma_{d,i}h_{d-1-2i,q-i}.
\tag{8}
\]
Thus \(\gamma_{d,5}\) uses exactly
\(\beta_{d,0},\ldots,\beta_{d,6}\).  The first six symbols are
all-depth polynomial identities; in particular,
`ORDINARY_RANK_SIX_SYMBOL_AND_NEWTON_THEOREM.md` supplies
\(\beta_{d,6}\).  Substitution into (7), followed by (8), simplifies
to (3)--(4).

As an internal boundary check, the same computation gives
\[
\prod_{m=6}^{11}(d-m)\mid h_{d,6},
\tag{9}
\]
as required by the independently proved all-rank falling-triangle
theorem.

## 2. Positivity certificate

Put \(d=u+11\).  After multiplying (3) by its positive denominator,
the numerator has the following coefficients in descending powers of
\(u\):
\[
\begin{aligned}
(&810123093896375,\ 117470706187957500,\\
&7916160141456279720,\ 329090197951577059200,\\
&9446873816558259471810,\ 198583558207712884868760,\\
&3162912470191756651508636,\\
&38951480639440722082621584,\\
&375079850835431480188544199,\\
&2836468344865020127987279932,\\
&16817548301644562228270567652,\\
&77567404341593653627142341584,\\
&274129824219295871333741310776,\\
&723941511230071673766897349008,\\
&1371903306568738801868891133792,\\
&1742598030043436615873060144832,\\
&1304914777582506924209367824640,\\
&421161144536910289212100915200).
\end{aligned}
\tag{10}
\]
All eighteen coefficients are strictly positive.  Since \(u\ge0\)
on the complete admissible range \(d\ge11\), equation (10) proves
(2).  The first admissible value is
\[
\gamma_{11,5}
=\frac{3316778722205903687}{120960}>0.
\tag{11}
\]

## 3. Verification and claim boundary

`verify_ordinary_sixth_long_recurrence_band.py` independently rebuilds
the signed Stirling rows, the ordinary-to-Newton rows
\(h_{d,0},\ldots,h_{d,6}\), and all six recurrence bands.  It checks:

- exact agreement with the previously reconstructed first five bands;
- the factorization (3)--(4);
- all eighteen shifted coefficients in (10);
- the first admissible value (11); and
- the six forced roots of \(h_{d,6}\).

Run:

```bash
python3 verify_ordinary_sixth_long_recurrence_band.py
pytest -q test_verify_ordinary_sixth_long_recurrence_band.py
```

The theorem proves the sixth band on its whole unbounded depth range.
It does not prove positivity for \(q\ge6\), common interlacing of the
\(H_d\), the complete-split middle Newton region, or OPG-1757.
