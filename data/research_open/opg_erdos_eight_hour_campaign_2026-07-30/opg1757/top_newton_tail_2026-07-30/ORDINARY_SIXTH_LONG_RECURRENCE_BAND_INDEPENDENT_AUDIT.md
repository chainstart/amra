# Independent audit of the sixth ordinary long-recurrence band

Date: 2026-07-30

Audited file:
`ORDINARY_SIXTH_LONG_RECURRENCE_BAND_THEOREM.md`

Independent certificate:
`independent_verify_ordinary_sixth_long_recurrence_band.py`

## 0. Verdict

\[
\boxed{\text{PASS}}
\]

The \(q=5\) recurrence band was independently reconstructed from the
printed ordinary symbols
\(\beta_{d,0},\ldots,\beta_{d,5}\) and the previously audited
`rank_six_polynomial`.  The audit does not call or import
`verify_ordinary_sixth_long_recurrence_band.py`.

The following items agree exactly with the theorem:

* the reduced denominator \(15359376162816000\);
* all 17 coefficients of \(R_5(d)\);
* all 18 positive coefficients after the shift \(d=u+11\);
* the boundary value
  \[
  \gamma_{11,5}
  =\frac{3316778722205903687}{120960};
  \]
* the six simple forced roots
  \[
  d=6,7,8,9,10,11
  \]
  of the polynomial continuation of \(h_{d,6}\).

No formula, denominator, indexing, or admissible-range error was
found.

## 1. A genuinely separate signed-Stirling reconstruction

The author's sixth-band verifier was not inspected or imported as a
computational dependency.  The new verifier also avoids the
antidifference implementation used in the earlier five-band
independent audit.

Put
\[
 p_a(n)=\sum_{j=0}^{n-1}j^a
\]
and let \(e_m(n)\) be the \(m\)-th elementary symmetric polynomial in
\(0,1,\ldots,n-1\).  Newton's identities give
\[
\boxed{
 m e_m(n)
 =
 \sum_{a=1}^m(-1)^{a-1}e_{m-a}(n)p_a(n),
 \qquad e_0(n)=1.
}
\tag{1}
\]
The exact Faulhaber polynomials \(p_a(n)\) are generated symbolically.
Since
\[
 (x)_{\underline n}
 =\prod_{j=0}^{n-1}(x-j),
\]
the near-diagonal signed Stirling rows are then
\[
\boxed{
 s_m(n)=s(n,n-m)=(-1)^m e_m(n).
}
\tag{2}
\]

As independent consistency checks, the verifier proves symbolically
for every \(1\le m\le6\) that
\[
 s_m(n+1)-s_m(n)=-n\,s_{m-1}(n),
 \qquad s_m(0)=0,
\tag{3}
\]
and its test compares every row through \(m=6\), at depths
\(6\le n\le12\), against direct coefficient extraction from
\(\prod_{j=0}^{n-1}(x-j)\).

## 2. Independent ordinary-to-Newton triangle

For fixed loss \(\ell\), the coefficient of \(n^{d-\ell}\) in
\(P_d(n+2)\) is rebuilt as
\[
 M_{d,\ell}
 =
 \sum_{r=0}^{\ell}
 \beta_{d,r}
 \frac{\prod_{a=0}^{\ell-r-1}(d-r-a)}
 {(\ell-r)!}
 2^{\ell-r}.
\tag{4}
\]
This uses an explicit polynomial product rather than a retained
symbolic binomial node.

On the falling-factorial side the same coefficient is
\[
 \sum_{j=0}^{\ell}
 h_{d,j}s_{\ell-j}(d-j).
\]
Solving the lower-triangular system gives
\[
\boxed{
 h_{d,\ell}
 =
 M_{d,\ell}
 -
 \sum_{j=0}^{\ell-1}
 h_{d,j}s_{\ell-j}(d-j),
 \qquad0\le\ell\le6.
}
\tag{5}
\]
All arithmetic in (4)--(5) is exact over \(\mathbb Q[d]\).

## 3. Independent long-recurrence triangle

At band \(q\), coefficient comparison at
\(x^{d-1-2q}\) gives
\[
\boxed{
 \gamma_{d,q}
 =
 h_{d,q+1}-h_{d+1,q+1}
 -
 \sum_{i=0}^{q-1}
 \gamma_{d,i}h_{d-1-2i,q-i}.
}
\tag{6}
\]
The verifier starts with an empty band list and derives
\(\gamma_{d,0},\ldots,\gamma_{d,5}\) successively; no previously
printed \(\gamma\)-formula is fed into the triangle.

At the boundary \(d=11,q=5\), the five lower calls in (6) are
\[
\begin{array}{c|ccccc}
i&0&1&2&3&4\\ \hline
\text{depth }d-1-2i&10&8&6&4&2\\
\text{row }q-i&5&4&3&2&1.
\end{array}
\tag{7}
\]
Every depth is exactly twice its row.  Thus all lower calls are on
their legal parity boundary, and there is no hidden off-by-one
evaluation.

## 4. Reconstructed \(q=5\) identity

The independently derived expression reduces to
\[
\gamma_{d,5}
=
\frac{d-10}{15359376162816000}R_5(d),
\tag{8}
\]
where the descending coefficient row of \(R_5\) is
\[
\begin{aligned}
(&810123093896375,
-25921081431700875,
313490671217497970,\\
&-1492874651122299900,
-1887303336152228890,
49625869946758088130,\\
&-167524355872717489604,
-106706576731710308472,
1816293817555406107219,\\
&-3108681098587146424959,
-2327663884048779946070,
9529661544865824480588,\\
&-493471326045590983080,
-8190583449886689443856,
-15710022013283259194016,\\
&29745938852108657679744,
-5169307325421355490304).
\end{aligned}
\tag{9}
\]
This agrees entry-for-entry with equation (4) of the theorem.
The denominator in (8) is the actual reduced denominator returned by
exact cancellation, not merely a valid common multiple.

Substitution of \(d=11\) in the independently derived rational
polynomial gives
\[
\boxed{
\gamma_{11,5}
=\frac{3316778722205903687}{120960}>0,
}
\tag{10}
\]
again in lowest terms.

## 5. Shifted positivity certificate

Multiplying \(\gamma_{u+11,5}\) by the denominator in (8) gives a
degree-17 polynomial whose descending coefficient row is
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
\tag{11}
\]
All 18 entries are strictly positive.  Since \(u=d-11\ge0\) on the
complete admissible range, this independently proves
\[
\gamma_{d,5}>0\qquad(d\ge11).
\tag{12}
\]

## 6. Exact \(h_{d,6}\) root audit

The independently reconstructed sixth Newton row factors as
\[
\boxed{
 h_{d,6}
 =
 \frac{\prod_{a=6}^{11}(d-a)}
 {2764687709306880000}\,Q_6(d),
}
\tag{13}
\]
where \(Q_6\) has descending coefficient row
\[
\begin{aligned}
(&7301929250,\ 24246201000,\ 347369332975,\\
&1635376219575,\ 9364980819900,\ 38121852131550,\\
&70749064934065,\ 468983371831485,\\
&-1333242190430338,\ 4415752376305302,\\
&-26513888651983548,\ 33346612662549552,\\
&-124792620885722880).
\end{aligned}
\tag{14}
\]
The residual polynomial has degree 12 and positive leading
coefficient.  Exact polynomial gcd gives
\[
\gcd\!\left(Q_6(d),\prod_{a=6}^{11}(d-a)\right)=1,
\]
so the six displayed forced roots are simple; none has been introduced
by a cancellation artifact.

## 7. Reproduction

Run:

```bash
python3 independent_verify_ordinary_sixth_long_recurrence_band.py
pytest -q test_independent_verify_ordinary_sixth_long_recurrence_band.py
```

Result:

```text
status: PASS
3 passed
```

The logical input boundary is the already audited all-depth identity
for `rank_six_polynomial` together with the five previously proved
lower-rank ordinary symbols.  No claim for \(q\ge6\), global
interlacing, or OPG-1757 is inferred from this audit.
