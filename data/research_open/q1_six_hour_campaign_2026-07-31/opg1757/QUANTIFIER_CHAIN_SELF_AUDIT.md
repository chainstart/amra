# OPG-1757 polynomial-window quantifier-chain self-audit

Date: 2026-08-01
Status: **SELF-AUDIT PASSED; THEOREM STILL PENDING INDEPENDENT CROSS-AUDIT**

This note audits only the chain from the normalized coefficient bound to
the root threshold and then to the simultaneous deficit window.  It does
not replace an independent audit of the endpoint filtration or profile
EGF.

## 1. Exact domain and normalization

Fix integers

\[
 q\ge1,\qquad 0\le r\le2q,
\]

and an integer \(s\) in the inherited stable range \(s\ge6q+4\).  Put

\[
 n=2s-5-q,
 \qquad
 C_{q,r}(s)=
 \frac{[\beta^{2n+r}]B_n(s,\beta)}
 {n!s^{2s-8-2q+r}}.
\tag{A1}
\]

The two factors in the denominator of (A1) are strictly positive.  The
stable range also gives \(n\ge0\), so positivity of \(C_{q,r}(s)\) is
equivalent to positivity of the original coefficient.  The exact master
formula has already cancelled the ordered-chain \(n!\), its selected
\(\lambda\)-power is exactly \(s^{2s-8-2q+r}\), and the remaining
profile weight is

\[
 \frac{4}{\ell!}\binom{q+1-\ell}{r-2\ell-e-f}.
\tag{A2}
\]

Thus no normalization factor is reintroduced in the tail bound.

## 2. Coefficient bound and all endpoint cases

Write

\[
 C_{q,r}(s)=L_{q,r}s^{2q}
 +\sum_{k=1}^{2q}c_{q,r,k}s^{2q-k},
 \qquad
 L_{q,r}=\frac4{q!}[z^r](1+2z+2z^2)^q>0.
\tag{A3}
\]

The apparent master degree is \(2q+2\); hence the coefficient indexed by
actual loss \(k\) is at apparent loss \(K=k+2\), including the boundary
values \(k=1\) and \(k=2q\).  The product-loss estimate and exact
absolute-profile mass give

\[
 \frac{|c_{q,r,k}|}{L_{q,r}}
 \le10q[256(k+3)]^{20(k+2)}q^{2(k+2)}.
\tag{A4}
\]

The ratio \(10q\) is valid for every \(0\le r\le2q\).  At \(r=0\),
negative adjacent-coefficient indices are zero; at \(r=2q\), the
word-increment comparison still has a legal increment for the source
layers \(2q-1\) and \(2q-2\).  Natural support gives \(\ell\le q\), so
all falling orders and all four endpoint shifts in (A4) are in their
stated domains.

## 3. Constant chain, with smallest integers checked

For every integer \(q\ge1\) and \(1\le k\le2q\),

\[
 k+2\le3k,\qquad k+3\le4k\le8q.
\tag{A5}
\]

Both first inequalities are equalities at the smallest value \(k=1\);
the last is an equality only when \(k=2q\).  Therefore

\[
 [256(k+3)]^{20(k+2)}
 \le(2048q)^{60k},
\tag{A6}
\]

while

\[
 q^{2(k+2)}\le(2048q)^{6k},
 \qquad
 10q<(2048q)^k.
\tag{A7}
\]

All bases are positive and at least one, so increasing the exponents in
(A6)--(A7) preserves the inequalities.  Multiplication yields

\[
 \frac{|c_{q,r,k}|}{L_{q,r}}
 <(2048q)^{67k}
 \le\{(4096q)^{67}\}^{k}.
\tag{A8}
\]

No asymptotic notation or fixed-\(q\) constant occurs in (A4)--(A8).
The executable integer check covers \(q=1,\ldots,60\) and every stated
\(k\); the displayed inequalities prove the unrestricted range.

## 4. Root threshold, including equality

Set \(X_q=(4096q)^{67}\).  If \(s\ge2X_q\), then \(s>0\) and
\(X_q/s\le1/2\).  Equations (A3) and (A8) imply

\[
 \frac{C_{q,r}(s)}{L_{q,r}s^{2q}}
 \ge1-\sum_{k=1}^{2q}(X_q/s)^k
 \ge1-\sum_{k=1}^{2q}2^{-k}
 =2^{-2q}>0.
\tag{A9}
\]

Thus the non-strict hypothesis \(s\ge2X_q\) gives a strict conclusion,
even at equality.  Also, for \(q\ge1\),

\[
 2(4096q)^{67}\ge8192q>6q+4,
\tag{A10}
\]

so the root threshold automatically places (A1) in the exact stable
range.

## 5. Simultaneous polynomial window

Let \(s\ge4\) be an integer and let \(q\) be an integer satisfying

\[
 0\le q\le s^{1/67}/8192.
\tag{A11}
\]

If \(q=0\), the separately normalized identity \(C_{0,0}=4\) applies.
If \(q\ge1\), raising the nonnegative inequality in (A11) to the
67th power gives

\[
 2(4096q)^{67}
 \le2\left(\frac{4096}{8192}\right)^{67}s
 =2^{-66}s<s.
\tag{A12}
\]

Hence (A9) applies to every such \(q\), and to every integer
\(0\le r\le2q\), simultaneously.  Equality in (A11) causes no endpoint
problem because (A12) is still strict for \(q\ge1\).

## 6. Self-audit verdict

The integer endpoints, \(q=0\) exception, \(q=1\) and \(k=1\) minima,
strict versus non-strict inequalities, stable-range absorption, and all
normalization factors pass this audit.  The status remains PENDING until
a different agent independently reconstructs the all-order endpoint
interface, profile EGF, apparent-loss shift, and constant chain.
