# OPG-1757: exact third-active Newton reduction

Date: 2026-08-02

Status: **EXACT ALL-PARAMETER REDUCTION; UNIVERSAL SIGN OPEN**.

## 1. Target and forward-difference collapse

Write

\[
 N_{q,j}(z)=\sum_{r=0}^{2q}\Delta_s^jC_{q,r}(4)z^r,
 \qquad m=\lfloor q/2\rfloor .
\]

The next open row after the audited parity-free second-active theorem is
\(j=m+2\).  The boundary factor annihilates the first \(m\) values, so
the forward difference collapses exactly to three terms:

\[
\boxed{
N_{q,m+2}(z)
=C_q(m+6,z)-(m+2)C_q(m+5,z)
 +\binom{m+2}{2}C_q(m+4,z).}
\tag{1}
\]

Here

\[
C_q(t,z)=\frac{t^{2t-2}}{p!\,z^{2p}}B_p(t,z/t),
\qquad p=2t-5-q.
\tag{2}
\]

Consequently (1) is the \(B_6/B_4/B_2\) comparison when \(q\) is odd
and the \(B_7/B_5/B_3\) comparison when \(q\) is even.  No later
\(B_p\) formula is needed.

## 2. Stable odd formula

Let \(q=2m+1\), \(s=m+6\), and \(s\ge8\).  Write

\[
B_6(s,\beta)
=60\beta^4\lambda_s^{2s-16}F_s^{(6)}(\beta),
\qquad F_s^{(6)}=\beta^8P_s^{(6)},
\]

\[
B_4(s-1,\beta)
=24\beta^4\lambda_{s-1}^{2s-14}F_{s-1}^{(4)}(\beta),
\qquad F_{s-1}^{(4)}=\beta^4P_{s-1}^{(4)}.
\]

Direct substitution in (1)--(2) gives the exact factorization

\[
N_{2m+1,m+2}(z)=(1+z)^{2s-16}H_s^{\rm o}(z),
\tag{3}
\]

\[
\boxed{
\begin{aligned}
H_s^{\rm o}(z)={}&
\frac1{12}s^{2s-14}P_s^{(6)}(z/s)\\
&-(s-4)(s-1)^{2s-12}(1+z)^2
 P_{s-1}^{(4)}(z/(s-1))\\
&+(s-4)(s-5)(s-2+2z)^{2s-10}(1+z)^4.
\end{aligned}}
\tag{4}
\]

The factor in (3) is maximal for every \(s\ge8\), and the natural
support gives \(\deg H_s^{\rm o}\le2s-6\).

## 3. Stable even formula

Let \(q=2m\), \(s=m+6\), and \(s\ge9\).  Put

\[
F_s^{(7)}=\beta^{10}P_s^{(7)},\qquad
F_{s-1}^{(5)}=\beta^6P_{s-1}^{(5)},\qquad
J_{s-2}^{(3)}=\beta^2P_{s-2}^{(3)}
\]

in the stable \(B_7,B_5,B_3\) formulas.  Then

\[
N_{2m,m+2}(z)=(1+z)^{2s-18}H_s^{\rm e}(z),
\tag{5}
\]

\[
\boxed{
\begin{aligned}
H_s^{\rm e}(z)={}&
\frac1{60}s^{2s-16}P_s^{(7)}(z/s)\\
&-\frac{s-4}{3}(s-1)^{2s-14}(1+z)^2
 P_{s-1}^{(5)}(z/(s-1))\\
&+(s-4)(s-5)(s-2)^{2s-12}(1+z)^4
 P_{s-2}^{(3)}(z/(s-2)).
\end{aligned}}
\tag{6}
\]

The factor in (5) is maximal for every \(s\ge9\), and the natural
support gives \(\deg H_s^{\rm e}\le2s-6\).

## 4. Maximal-factor certificate

The maximality assertions are all-parameter statements, not finite
observations.  Direct substitution in the two fixed kernels gives

\[
K_s^{(6)}(-1/s)=
\frac{(s-7)(s-6)(s-5)^2(s-4)^2(s-3)(s-2)}{s^8}>0
\quad(s\ge8),
\tag{7}
\]

\[
K_s^{(7)}(-1/s)=
\frac{(s-8)(s-7)(s-6)^2(s-5)^2(s-4)^2(s-3)(s-2)}
{s^{10}}>0
\quad(s\ge9).
\tag{8}
\]

At \(z=-1\), the second and third terms of both (4) and (6) vanish.
In the first term, every summand of \(F_s^{(6)}\), respectively
\(F_s^{(7)}\), except its leading kernel term contains a positive power
of \(\lambda_s=1+s\beta\) and also vanishes.  Hence

\[
H_s^{\rm o}(-1)=\frac1{12}(s-6)^{2s-14}
(s-7)(s-6)(s-5)^2(s-4)^2(s-3)(s-2)>0,
\tag{9}
\]

\[
H_s^{\rm e}(-1)=\frac1{60}(s-7)^{2s-16}
(s-8)(s-7)(s-6)^2(s-5)^2(s-4)^2(s-3)(s-2)>0.
\tag{10}
\]

Thus neither reduced polynomial has another \(1+z\) factor.  The
workbench checks (7)--(8) as exact symbolic identities.

## 5. Exact positive bases

The two odd pre-stable rows \(N_{1,2},N_{3,3}\) and the stable base
\(H_8^{\rm o}\), respectively, have coefficient vectors

\[
(8,16,16),
\]

\[
(24044,94336,170092,175968,109396,38752,6196),
\]

\[
\begin{aligned}
(&14207112,88847152,257302408,454890592,543963464,\\
 &459988784,278846744,119841856,35017744,6296512,530304).
\end{aligned}
\tag{11}
\]

The two even pre-stable rows \(N_{2,3},N_{4,4}\) and the stable base
\(H_9^{\rm e}\), respectively, have coefficient vectors

\[
(360,1184,1872,1392,464),
\]

\[
(741044,3941792,9854608,14916288,14852376,9939424,
4370752,1159072,143076),
\]

\[
\begin{aligned}
(&577839736,4411248016,15850877164,35459528480,\\
 &55004522340,62337009504,52951321624,33998782656,\\
 &16397772960,5802781200,1432657948,221972128,16350372).
\end{aligned}
\tag{12}
\]

Every entry is positive.  Thus no unproved base case remains.

## 6. The first open gate

Exact falsification suggests the two clean transports

\[
\boxed{
H_{s+1}^{\rm o}-(s+6z)^2H_s^{\rm o}>_{\rm coeff}0
\quad(s\ge8),}
\tag{13}
\]

\[
\boxed{
H_{s+1}^{\rm e}-(s+7z)^2H_s^{\rm e}>_{\rm coeff}0
\quad(s\ge9).}
\tag{14}
\]

If (13) and (14) are proved, their positive initial rows plus the finitely
many pre-stable rows prove the third-active theorem for every deficit.
At present (13)--(14) are conjectures, not promoted claims.  They are the
first sharply isolated open gate.

The exact workbench checks:

- both stable identities coefficient by coefficient through \(m=100\);
- 20,503 odd and 20,300 even original row coefficients through \(m=100\);
- 10,780 odd and 10,767 even transport coefficients;
- maximal \((1+z)\)-multiplicities on the same range.

No zero or negative row coefficient and no zero or negative transport
coefficient occurs.  These counts are finite route selection only.

## 7. Firewall

Equations (1)--(6) are exact all-parameter identities derived from the
already proved fixed-page formulas.  Equations (7)--(10) certify the
factor multiplicities.  The signs in (13)--(14) remain open.
Nothing here proves a third-active row, the full base-four Newton
conjecture, or the original arbitrary-host OPG-1757 statement.

The reproducible source is third_active_workbench.py; its focused tests
are in test_third_active_workbench.py.
