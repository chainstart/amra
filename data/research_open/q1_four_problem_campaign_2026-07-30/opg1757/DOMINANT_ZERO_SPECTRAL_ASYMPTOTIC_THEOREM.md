# OPG-1757: dominant-zero spectral asymptotics of the long-recurrence layer

Date: 2026-07-30

## 1. Theorem

Let
\[
H(z)=\sum_{j\ge0}L_jz^j
\]
be the highest-degree falling-triangle series, and let
\[
\sum_{q\ge0}G_qz^{q+1}=-3z\frac{H'(z)}{H(z)}.
\tag{1}
\]
The inherited all-rank theorem proved that \(H\) is entire of order at
most \(1/2\), that it has one zero \(\rho\) in \(|z|<21/10\), and that
all other zeros \(\rho_\nu\) satisfy \(|\rho_\nu|>21/10\).

The new quantitative form is:
\[
\boxed{
\frac{1961}{1000}<\rho<\frac{1962}{1000},
}
\tag{2}
\]
and, for every \(n\ge2\),
\[
\boxed{
\left|
\frac{G_{n-1}}{3\rho^{-n}}-1
\right|
<
63\left(\frac{327}{350}\right)^n.
}
\tag{3}
\]
Consequently
\[
\boxed{
\lim_{q\to\infty}\frac{G_{q+1}}{G_q}=\rho^{-1},
\qquad
\lim_{q\to\infty}G_q^{1/(q+1)}=\rho^{-1}.
}
\tag{4}
\]
The relative error in (3) is below \(1,1/2,1/10,1/100\) from
\(n=61,72,95,129\), respectively.

## 2. Rational localization of the first zero

Write \(L_j=(-1)^j\lambda_j\), \(\lambda_j>0\).  The coefficient
recurrence proved in the hypergeometric/Airy analysis gives
\[
\frac{\lambda_{r+1}}{\lambda_r}<\frac1{r^2}\qquad(r\ge1).
\tag{5}
\]
At \(x\le1962/1000<2\), the terms therefore decrease from the first
tail onward; the exceptional first ratio is directly
\[
\frac{\lambda_2x}{\lambda_1}
\le\frac{13}{144}\frac{1962}{1000}<1.
\]
Alternating-series bounds now give
\[
\sum_{j=0}^{5}L_j(1961/1000)^j
=
\frac{7457293263738952482833}
{304749527040000000000000000}>0,
\tag{6}
\]
while
\[
\sum_{j=0}^{4}L_j(1962/1000)^j
=-\frac{8765678187043}{23040000000000000}<0.
\tag{7}
\]
The odd partial sum in (6) is a lower bound and the even partial sum in
(7) is an upper bound.  Hence \(H(1961/1000)>0>H(1962/1000)\).
Uniqueness in the earlier Rouché disk proves (2).

## 3. Spectral expansion

Order below one and \(H(0)=1\) give the genus-zero product
\[
H(z)=\prod_\nu(1-z/\rho_\nu).
\]
Logarithmic differentiation of (1) yields
\[
G_{n-1}=3\sum_\nu\rho_\nu^{-n}.
\tag{8}
\]
The inherited Jensen annulus estimate is
\[
\sum_{\rho_\nu\ne\rho}|\rho_\nu|^{-n}
<63(21/10)^{-n}.
\tag{9}
\]
Divide (8) by \(3\rho^{-n}\).  Equations (2) and (9) give
\[
\left|
\frac{G_{n-1}}{3\rho^{-n}}-1
\right|
<
63\left(\frac{\rho}{21/10}\right)^n
<
63\left(\frac{1962/1000}{21/10}\right)^n,
\]
and the last ratio is exactly \(327/350\).  This proves (3), and (4)
follows immediately.

## 4. Meaning and limit

The Airy/\({}_2F_0\) highest layer therefore has a single dominant
spectral scale: asymptotically, the full leading long-band sequence is
geometric with base \(\rho^{-1}\), with an explicit exponential error.
This strengthens the earlier sign theorem, but controls only the
highest power of the depth polynomial \(\mathfrak g_q(d)\).  It does
not prove \(\gamma_{d,q}>0\) at every admissible pair.
