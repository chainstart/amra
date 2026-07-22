# Erdős #686: an exact Mahler-coefficient reduction for the high Cartier layer

Date: 2026-07-22 (Asia/Hong_Kong)

Status: all-parameter algebraic reduction and four uniform endpoint checks;
not the missing uniform Cartier theorem.

## 1. Exact formula

Put

\[
 H_m(v)=\prod_{j=1}^{2m}\left(1-\binom j2v\right)^{1/2}
       =\sum_{k\geq0}h_kv^k
\]

and retain the transferred polynomial

\[
 C_m(z)=[v^m]\frac{H_m(v)}{1-zv}
       =\sum_{k=0}^m h_{m-k}z^k.
\]

For `0<=r<=m`, its `r`-th Mahler coefficient is

\[
 \boxed{
 \Delta^r C_m(0)
 =r!\,[v^{m-r}]\frac{H_m(v)}
 {(1-v)(1-2v)\cdots(1-rv)}.}                    \tag{1}
\]

(For `r=0`, the empty denominator is one.)  Indeed,

\[
 \Delta^r z^k\big|_{z=0}=r!\,S(k,r)
\]

and the ordinary generating function for Stirling numbers is

\[
 \sum_{k\ge r}r!S(k,r)v^k
 =\frac{r!v^r}{\prod_{j=1}^r(1-jv)}.
\]

Multiplying by `H_m(v)` and extracting `[v^m]` proves (1).  Thus the
all-integer valuation claim

\[
 v_2(C_m(z))=T(m)\qquad(z\in\mathbb Z)
\]

is equivalent to the constant coefficient having valuation exactly `T(m)`
and every expression in (1) with `r>=1` having valuation at least `T(m)+1`.
This is an exact divided-power formulation; it avoids the false demand that
the ordinary monomial coefficients be individually integral after
normalisation.

## 2. The last four Mahler coefficients are never the obstruction

Formula (1) immediately gives

\[
 \Delta^m C_m(0)=m!.
\]

Since

\[
 [v]H_m(v)=-\frac12\binom{2m+1}{3},
\]

the next coefficient is

\[
\begin{aligned}
 \Delta^{m-1}C_m(0)
 &=(m-1)!\left\{-\frac12\binom{2m+1}{3}
                   +\sum_{j=1}^{m-1}j\right\}\\
 &=-\frac{m!(4m^2-3m+2)}6.                       \tag{2}
\end{aligned}
\]

In the first unresolved uniform family `m=4s` (`s` odd), the second factor
in (2) has 2-adic valuation one, so both endpoint Mahler coefficients have
valuation `v_2(m!)`.  Writing `s_2(s)` for the binary digit sum,

\[
\begin{aligned}
 v_2(m!)-T(m)
 &=\{m-s_2(s)\}-\{m-3s+s_2(s)\}\\
 &=3s-2s_2(s)\ge1.
\end{aligned}
\]

Consequently `r=m-1,m` satisfy the required strict extra divisibility for
every odd `s`, without any finite scan.  The unresolved part is precisely
the constant valuation together with the middle band `1<=r<=m-2`.

One more coefficient can be removed uniformly.  Expanding (1) through
degree two gives

\[
 \Delta^{m-2}C_m(0)
 ={(m-2)!m\over360}
 \left(80m^5-264m^4+365m^3-360m^2+230m-96\right). \tag{3}
\]

If `4|m`, the polynomial in parentheses is divisible by eight.  Since
`v_2(360)=3` and `m-1` is odd, (3) has valuation at least

\[
 v_2((m-2)!)+v_2(m)=v_2(m!).
\]

It therefore also has valuation at least `T(m)+1` in the family `m=4s`,
`s` odd.

The degree-three expansion is longer but still explicit:

\[
 \Delta^{m-3}C_m(0)=-{(m-3)!m\over45360}P(m),              \tag{4}
\]

where

\[
\begin{aligned}
P(m)={}&2240m^8-17136m^7+53652m^6-98721m^5\\
 &+137886m^4-137844m^3+108388m^2-60984m+21024.
\end{aligned}
\]

For `4|m`, every displayed summand is divisible by 32.  As
`v_2(45360)=4` and `v_2((m-2)(m-1))=1`, (4) again has valuation at least
`v_2(m!)`, hence at least `T(m)+1`.  After these endpoint calculations, the
genuinely unresolved band is `1<=r<=m-4` (together with the exact constant
valuation at `r=0`).

## 3. Boundary

This reduction explains why the ordinary monomial basis loses powers of two
while the Mahler basis can still work, and removes four endpoint families from
the induction.  It does not control the middle band and therefore neither
proves the conjectured valuation formula nor closes Erdős #686.
