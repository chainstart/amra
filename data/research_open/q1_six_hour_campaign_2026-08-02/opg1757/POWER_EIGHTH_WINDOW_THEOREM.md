# OPG-1757 layer theorem: an explicit eighth-root deficit window

Date: 2026-08-02

Status: **PROVED**.

## 1. Theorem

For the complete-split pooled, disjoint-core, alpha-squared layer, let

\[
C_{q,r}(s)=
\frac{[\beta^{2(2s-5-q)+r}]B_{2s-5-q}(s,\beta)}
{(2s-5-q)!s^{2s-8-2q+r}}.
\]

For every integer (q\ge1), every (0\le r\le2q), and every integer

\[
\boxed{s\ge2(2^{23}q)^8,}
\tag{1}
\]

one has (C_{q,r}(s)>0).  Consequently, for every integer (s\ge4),
all natural-support coefficients in this layer are strictly positive
simultaneously whenever

\[
\boxed{0\le q\le\frac{s^{1/8}}{2^{24}}.}
\tag{2}
\]

This improves the independently audited exponent (1/67) to (1/8).
No finite-(q) extrapolation is used.

## 2. Sharpened endpoint loss lemma

Use the relative endpoint expansion

\[
Q_{h,e,\rho+1}(s)=
\frac{s^{2(e+\rho)}}{2^{e+\rho}\rho!e!}
\left(1+\sum_{k\ge1}q_{h,k}(e,\rho)s^{-k}\right).
\tag{3}
\]

The all-order filtration gives
(\deg q_{h,k}\le2k).  The exact endpoint norm, evaluated on
(e+\rho\le2k), gives the node bound

\[
B_k=15(2k+1)2^{4k}(2k)!(4k+4)^{4k}.
\tag{4}
\]

For (k\ge1),

\[
B_k\le45k\,2^{18k}k^{6k},
\tag{5}
\]

using (2k+1\le3k), ((2k)!\le(2k)^{2k}), and
(4k+4\le8k).

Bivariate Newton interpolation has at most ((2k+1)^2\le9k^2)
terms.  Mixed differences cost at most (2^{2k}), and
((q+1)^{2k}\le(2q)^{2k}).  Thus every actual master-profile value
satisfies

\[
|q_{h,k}(e,\rho)|
\le405\,2^{22k}k^{6k+3}q^{2k}.
\tag{6}
\]

Since (405\le2^{9k}), (k^3\le2^{3k}), and (k\le k+1),

\[
\boxed{
|q_{h,k}(e,\rho)|
\le W_k(q):=[64(k+1)]^{6k}q^{2k}.
}
\tag{7}
\]

This holds for all (h=0,1,2), (k\ge1), and
(0\le e,\rho\le q+1).  Put (W_0=1).

Every loss-(i) coefficient of each pooled falling factor is at most
((5q^2)^i\le W_i(q)), so (7) controls all four relative factors in a
master product.

## 3. Four-factor convolution

At total apparent loss (K\), a fixed product has at most
(\binom{K+3}{3}\le4^K) weak compositions.  For each composition,

\[
\prod_{\nu=1}^4 W_{i_\nu}(q)
\le[64(K+1)]^{6K}q^{2K}.
\]

Absorbing (4^K) by doubling the base gives

\[
\boxed{
U_K(q):=[128(K+1)]^{6K}q^{2K}.
}
\tag{8}
\]

The independent profile-EGF audit proves that the total absolute
baseline mass is at most (10q) times the positive leading symbol.
Since actual loss (k) is apparent loss (K=k+2),

\[
\frac{|[s^{2q-k}]C_{q,r}|}{[s^{2q}]C_{q,r}}
\le10q[128(k+3)]^{6(k+2)}q^{2(k+2)}.
\tag{9}
\]

## 4. Eighth-power geometric majorant

Let (1\le k\le2q).  Since (k+3\le4k), (9) is at most

\[
R_{q,k}:=10\,2^{54k+108}q^{2k+5}k^{6k+12}.
\tag{10}
\]

Also (q\ge k/2), and (6k-5>0).  Dividing (10) by (q^{8k}) gives

\[
\begin{aligned}
\frac{R_{q,k}}{q^{8k}}
&\le10\,2^{54k+108}k^{6k+12}
\left(\frac2k\right)^{6k-5}\\
&=10\,2^{60k+103}k^{17}\\
&\le2^{184k}=(2^{23})^{8k}.
\end{aligned}
\tag{11}
\]

The final inequality uses (10\le2^{4k}), (k\le2^k), and
(2^{103}\le2^{103k}).  Therefore

\[
\boxed{
\frac{|[s^{2q-k}]C_{q,r}|}{[s^{2q}]C_{q,r}}
\le\{(2^{23}q)^8\}^{k}.
}
\tag{12}
\]

With (X_q=(2^{23}q)^8), condition (1) yields

\[
\frac{C_{q,r}(s)}{[s^{2q}]C_{q,r}s^{2q}}
\ge1-\sum_{k=1}^{2q}(X_q/s)^k
\ge2^{-2q}>0.
\]

The threshold is far inside the exact stable range (s\ge6q+4).
Under (2),

\[
2(2^{23}q)^8\le2(2^{-1})^8s=s/128<s,
\]

so (1) applies simultaneously to all such deficits.  At (q=0), use
(C_{0,0}=4).

## 5. Method boundary

The exponent eight is the natural limit of this particular absolute
interpolation ledger: endpoint node heights contribute (k^{6k}), and
profile evaluation contributes (q^{2k}).  This is a statement about
the present proof method, not an optimality theorem for the actual
coefficients.  Full Newton positivity could still remove the large-(s)
threshold entirely.
