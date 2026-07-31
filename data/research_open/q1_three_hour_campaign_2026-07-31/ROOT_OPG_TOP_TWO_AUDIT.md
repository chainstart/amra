# Root audit: the endpoint top-two law

Date: 2026-07-31

Status:
`Q_LE_5_ENDPOINT_PATTERN_CERTIFIED__ALL_EXCESS_TOP_TWO_THEOREM_PROVED`

## 1. Exact finite statement

Write the normalized endpoint from the fixed-deficit reduction as
\[
Q_{h,e,c}(s)
=\frac{H_{h,e,c}}
{2^h s^{s-h-2c-e}}.
\]
For every one of the 84 displayed endpoint polynomials occurring through
deficit \(q=5\), exact coefficient extraction gives
\[
\deg Q_{h,e,c}=D_{e,c}:=2c+2e-2,
\]
and
\[
\boxed{
[s^{D_{e,c}}]Q_{h,e,c}
=
\frac{1}
{2^{c+e-1}(c-1)!\,e!}.
}
\tag{1}
\]
The leading coefficient is independent of \(h\).  If it is denoted by
\(A_{e,c}\), the next coefficient is
\[
\boxed{
\frac{[s^{D_{e,c}-1}]Q_{h,e,c}}{A_{e,c}}
=
\frac{(15-4e)(c-1)-e(4e+5)}3
-h(c+2e-1).
}
\tag{2}
\]
Equation (2) is omitted in the single constant case \(e=0,c=1\).

All 84 polynomials have now passed their endpoint certificates, including
the 21 new \(q=5\) entries in the 924-value Abel audit.  More importantly,
`OPG_ENDPOINT_TOP_TWO_THEOREM.md` proves (1)--(2) for arbitrary \(e,c\)
using the rooted-hypertree EGF, binary-edge factorial moments, and marked
Abel leading terms.  The finite table is a regression audit rather than
the source of the general quantifier.

## 2. All-deficit consequence

The endpoint theorem supplies (1)--(2) as leading Laurent coefficients
for every \(e,c\); full endpoint polynomiality is not required.  In one
summand of the fixed-deficit master formula put
\[
A=(e,c),\qquad B=(f,d),\qquad
c+d+e+f=q+3-\ell .
\]
The product degree before the Rayleigh subtraction is
\[
(2c+2e-2)+(2d+2f-2)+2\ell=2q+2.
\]
Its leading term cancels because (1) is independent of \(h\).

For the next coefficient, put
\[
\kappa_{e,c}=c+2e-1.
\]
After the leading cancellation, the ordered pair \((A,B)\) contributes a
multiple of
\[
A_{e,c}A_{f,d}(\kappa_{f,d}-\kappa_{e,c}).
\tag{3}
\]
The falling-factor contribution is the same on both sides, since
\[
(1+c+e)+(1+d+f)
=(c+e)+(2+d+f).
\]
The master sum also contains the transposed pair \((B,A)\), whose
contribution is the negative of (3).  Hence the degree \(2q+1\) cancels
under this involution.  Since the denominator-aware theorem already makes
\(R_{q,r}=s^rC_{q,r}\) a polynomial,
\[
\deg R_{q,r}\le2q+r
\]
for every offset \(r\).

The executable audit checks the top-two identity in all 84 certified
formulas, checks the rooted/unrooted EGF against 119 primitive endpoints,
and checks the involution algebra through \(q=30\).  These finite loops are
regression guards for the displayed proofs, not the source of their
all-\(q\) quantifiers.

## 3. Remaining theorem

Endpoint polynomiality remains open: the Abel lemma gives a rational
function with a controlled power of \(s\) in the denominator.  Thus the
new theorem improves the cleared-numerator degree, but it does not prove
denominator cancellation or positivity at arbitrary deficit.

Run:

```text
python3 root_verify_opg_top_two.py
```
