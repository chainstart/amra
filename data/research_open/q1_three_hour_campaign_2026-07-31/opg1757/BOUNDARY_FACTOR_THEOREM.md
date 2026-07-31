# Boundary-factor theorem for every fixed deficit

Date: 2026-07-31

## 1. Statement

Fix an integer \(q\ge0\), put
\[
n=2s-5-q,
\]
and for \(0\le r\le2q\) use the normalization from
`FIXED_DEFICIT_FINITE_REDUCTION.md`:
\[
C_{q,r}(s)
=
\frac{[\beta^{2n+r}]B_n}
{n!\,s^{2s-8-2q+r}}
=\frac{R_{q,r}(s)}{s^r},
\qquad
\deg R_{q,r}\le2q+r+2.
\tag{1}
\]
Here (1) initially denotes the actual pooled coefficient whenever
\(n\ge0\), and its unique rational continuation supplied by the finite
hyperforest reduction elsewhere.

Define
\[
t_q=\left\lfloor\frac{q+6}{2}\right\rfloor,
\qquad
F_q(s)=\prod_{j=4}^{t_q}(s-j),
\tag{2}
\]
with an empty product equal to one.  Then
\[
\boxed{
F_q(s)\mid R_{q,r}(s)
\quad\text{in }\mathbb Q[s]
\quad
(0\le r\le2q).
}
\tag{3}
\]

This is a boundary factor, not a positivity theorem.

## 2. Why negative depth can be used safely

The point requiring care is that \(B_n\) is not a combinatorial pooled
layer for \(n<0\).  We do not assign a negative factorial or assert the
existence of such a layer.

Instead start from the factorial-free right-hand side of the exact master
formula
\[
\begin{aligned}
\frac{[\beta^{2n+r}]B_n}{n!}
={}&
\sum_{\ell=0}^{\lfloor r/2\rfloor}\frac1{\ell!}
\sum_{\substack{e+f+a=r-2\ell\\0\le a\le q+1-\ell}}
\binom{q+1-\ell}{a}s^a\\
&\quad\times[x^{n-\ell}]
\left(
\mathcal H_{1,e}^{(\ell)}\mathcal H_{1,f}^{(\ell)}
-
\mathcal H_{0,e}^{(\ell)}\mathcal H_{2,f}^{(\ell)}
\right).
\end{aligned}
\tag{4}
\]
For \(n\ge0\), (4) is the proved pooled identity.  For \(n<0\), define
only the right-hand side, with the standard formal-series convention
\[
[x^m]G(x)=0\qquad(m<0).
\tag{5}
\]
Every \(n-\ell\) in (4) is negative, so this continuation is exactly zero.

The denominator-aware Abel proof is coefficient-preserving.  It expands
each fixed incidence type into falling factorials in the number of unit
slots; unavailable types vanish rather than introduce exceptional small
values.  Consequently the finite rational expression derived from (4)
is valid at every integer \(s\ge4\), including the values for which
\(n<0\).  Equivalently, it agrees with (4) for infinitely many stable
\(s\), and the coefficient-preserving falling-factorial extension fixes
its evaluations at the smaller integer profiles.  No value of
\((-1)!\), \((-2)!\), or a negative-depth \(B_n\) is used.

Multiplication by the nonzero normalization powers of \(s\) therefore
gives
\[
R_{q,r}(s)=0
\qquad
\text{whenever }s\ge4\text{ and }2s-5-q<0.
\tag{6}
\]

## 3. The \(B_0\) and \(B_1\) endpoints

The already proved exact pooled support theorem says
\[
B_0=B_1=0.
\tag{7}
\]
At the largest integer \(t_q\) in (2),
\[
2t_q-5-q
=
\begin{cases}
1,&q\text{ even},\\
0,&q\text{ odd}.
\end{cases}
\tag{8}
\]
Every smaller integer \(s\ge4\) gives negative depth, except for any
intermediate \(0\) or \(1\) case already covered by (7).  Combining
(6)--(8) yields
\[
R_{q,r}(j)=0
\qquad(4\le j\le t_q).
\tag{9}
\]
The roots in (9) are distinct, proving (3).

## 4. Reduced certificate count

Put
\[
m_q=\deg F_q
=
\max\left(
0,\left\lfloor\frac{q+6}{2}\right\rfloor-3
\right).
\tag{10}
\]
After writing \(R_{q,r}=F_q\widetilde R_{q,r}\),
\[
\deg\widetilde R_{q,r}
\le2q+r+2-m_q.
\tag{11}
\]
Thus a proposed coefficient formula needs only
\[
\boxed{
2q+r+3-m_q
}
\tag{12}
\]
non-boundary exact values, rather than \(2q+r+3\).

Examples:

- \(q=2,3\): \(F_q=s-4\);
- \(q=4,5\): \(F_q=(s-4)(s-5)\);
- \(q=5\): the eleven offsets require \(11+r\) values each, or
  \(176\) values in total.

The factor explains the boundary zeros already observed in the
\(q=2,3,4\) formulas and is used in the \(q=5\) independent certificate.
These counts use the original degree bound.  The later endpoint top-two
theorem sharpens it by two.  In particular, at \(q=6\),
\(F_6=(s-4)(s-5)(s-6)\) and only \(10+r\) values are required per offset,
or 208 over all thirteen offsets; `SEVENTH_ATTACK_Q6.md` executes exactly
that sharp certificate.

## 5. Scope

Equation (3) holds for every fixed \(q\), but it gives only forced roots.
It does not imply that the quotient \(\widetilde R_{q,r}\) is positive,
that the denominator \(s^r\) cancels, or that arbitrary-host OPG-1757
holds.
