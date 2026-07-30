# Independent audit of the first five ordinary long-recurrence bands

Date: 2026-07-30

## 0. Verdict

\[
\boxed{\text{PASS}}
\]

All five formulas in
`ORDINARY_FIRST_FIVE_LONG_RECURRENCE_BANDS_THEOREM.md` have been
independently recomputed from the six previously proved ordinary
symbols
\[
\beta_{d,0},\ldots,\beta_{d,5}.
\]
The independent derivation uses:

1. exact polynomial antidifferences for the near-diagonal signed
   Stirling numbers;
2. the ordinary-power to falling-factorial triangle; and
3. coefficient comparison in the long recurrence.

It does not import or call the author's verifier.

The five \(\gamma_{d,q}\) formulas, their applicability ranges, and
every coefficient of the positive-shift certificates are correct.
There is no formula error.

The only wording qualification concerns the phrase “forced factors”
for \(h_{d,4},h_{d,5}\).  Parity forces the roots and hence the unsigned
products
\[
\prod_{i=4}^7(d-i),
\qquad
\prod_{i=5}^9(d-i).
\]
The displayed minus sign in the \(h_{d,5}\) factorization is also
correct, but it is an explicit sign normalization making the remaining
factor have positive leading coefficient; a polynomial factor itself
is only defined up to a nonzero scalar.

## 1. Independent near-diagonal Stirling construction

Let
\[
s_m(n)=s(n,n-m).
\]
Starting with \(s_0(n)=1\), the verifier constructs every next row by
the exact antidifference
\[
\boxed{
s_m(n)
=-\sum_{k=0}^{n-1}k\,s_{m-1}(k).
}
\tag{1}
\]
This gives \(s_m(0)=0\) and directly verifies
\[
s_m(n+1)-s_m(n)=-n\,s_{m-1}(n).
\]
No interpolation in \(n\) is used.

Only \(s_0,\ldots,s_5\) are needed.  Their degrees grow as expected,
and the first row is
\[
s_1(n)=-\frac{n(n-1)}2.
\]

## 2. Ordinary-to-falling triangle

Write
\[
P_d(k)=\sum_{r=0}^d\beta_{d,r}k^{d-r}.
\]
After replacing \(k\) by \(n+2\), the coefficient of \(n^{d-\ell}\)
in the ordinary expansion is
\[
\boxed{
M_{d,\ell}
=\sum_{r=0}^{\ell}
\beta_{d,r}
\binom{d-r}{\ell-r}2^{\ell-r}.
}
\tag{2}
\]
Indeed, the term with rank \(r\) contributes
\[
\beta_{d,r}\binom{d-r}{d-\ell}2^{\ell-r}.
\]

On the falling-factorial side,
\[
P_d(n+2)
=\sum_jh_{d,j}(n)_{\underline{d-j}},
\]
and the same ordinary coefficient is
\[
\sum_{j=0}^{\ell}
h_{d,j}s_{\ell-j}(d-j).
\]
Since \(s_0=1\), isolating the last term gives exactly
\[
\boxed{
h_{d,\ell}
=M_{d,\ell}
-\sum_{j=0}^{\ell-1}
h_{d,j}s_{\ell-j}(d-j).
}
\tag{3}
\]

Substitution of the printed \(\beta\)-polynomials reproduces the
printed \(h_{d,1},h_{d,2},h_{d,3}\) identities exactly.

## 3. Long-recurrence coefficient index

The left side
\[
xH_d-H_{d+1}
\]
has coefficient
\[
h_{d,q+1}-h_{d+1,q+1}
\]
at \(x^{d-1-2q}\).

In the term
\[
\gamma_{d,i}H_{d-1-2i},
\]
the required coefficient has internal row
\[
j=q-i,
\]
because
\[
d-1-2i-2j=d-1-2q.
\]
The \(i=q\) term has \(j=0\) and coefficient one.  Isolating it gives
\[
\boxed{
\gamma_{d,q}
=h_{d,q+1}-h_{d+1,q+1}
-\sum_{i=0}^{q-1}
\gamma_{d,i}h_{d-1-2i,q-i}.
}
\tag{4}
\]
Thus neither \(q-i\) nor the depth \(d-1-2i\) is shifted incorrectly.

At the minimum depth
\[
d=2q+1,
\]
every lower call satisfies
\[
d-1-2i=2(q-i),
\]
which is precisely the lowest depth supporting row \(q-i\).  For
\(q=0,\ldots,4\), the minimum depths are
\[
1,3,5,7,9.
\]
All \(\beta_{n,r}\) used in these calls lie inside their proved range
\(n\ge r\).

## 4. Recomputed bands

Applying (3)--(4) to the six printed \(\beta\)-polynomials reproduces
all five displayed identities:
\[
\gamma_{d,0},\ldots,\gamma_{d,4}.
\]
Symbolic subtraction of each independently derived polynomial from
the corresponding printed formula is identically zero.

At their minimum depths the five values are respectively
\[
18,\qquad
630,\qquad
\frac{399363}{4},\qquad
\frac{721102503}{20},\qquad
\frac{11688306931609}{480},
\]
all positive.

## 5. Positive-shift certificates

For every band, set
\[
u=d-(2q+1)\ge0
\]
and multiply by the printed positive denominator \(D_q\).  Exact
expansion gives coefficient-row lengths
\[
3,\ 6,\ 9,\ 12,\ 15.
\]
Every coefficient is strictly positive, and all rows agree
entry-for-entry with equation (22) of the theorem.

Therefore
\[
D_q\gamma_{u+2q+1,q}>0
\qquad(u\ge0),
\]
which proves the claimed unbounded range.  The shift is by
\(2q+1\), not \(2q\); this agrees with the first depth at which the
band occurs in the parity expansion.

## 6. The \(h_{d,4}\) and \(h_{d,5}\) factors

The row \(h_{d,4}\) is algebraically available from the rank-four
symbol for \(d\ge4\), but parity permits row four only for \(d\ge8\).
Consequently
\[
h_{4,4}=h_{5,4}=h_{6,4}=h_{7,4}=0,
\]
and its polynomial continuation must contain
\[
\prod_{i=4}^7(d-i).
\]
Independent division is exact.  The remaining numerator has degree
eight and positive leading coefficient.

Similarly, the rank-five formula is available for \(d\ge5\), while
row five is absent through \(d=9\).  Hence
\[
h_{d,5}=0
\qquad(d=5,6,7,8,9),
\]
and exact division gives
\[
h_{d,5}
=-\left(\prod_{i=5}^9(d-i)\right)Q_5(d),
\]
where \(Q_5\) has degree ten and positive leading coefficient after
clearing its positive constant denominator.

Thus both factorizations in equation (19) are correct.  Strictly
speaking, the roots force the products; the choice to place a minus
sign outside the second product is verified normalization rather than
additional root information.

## 7. Claim status

### Verified

* the Newton/falling-factorial triangular identity;
* all printed \(h_{d,1},h_{d,2},h_{d,3}\) formulas;
* all five \(\gamma_{d,q}\) formulas;
* the recurrence indices and full applicability ranges;
* every positive shifted coefficient;
* the \(h_{d,4}\) and \(h_{d,5}\) roots and sign-normalized factors.

### Not implied

* positivity of bands \(q\ge5\);
* positivity of the entire long recurrence;
* real-rootedness or common interlacing of the \(H_d\).

## 8. Verification

Run:

```bash
pytest -q test_independent_verify_ordinary_first_five_long_recurrence_bands.py
python3 independent_verify_ordinary_first_five_long_recurrence_bands.py
```

The independent implementation imports nothing from
`verify_ordinary_first_five_long_recurrence_bands.py`.
