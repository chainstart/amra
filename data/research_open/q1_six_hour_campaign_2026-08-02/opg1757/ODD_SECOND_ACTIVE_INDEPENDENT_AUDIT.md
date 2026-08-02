# Odd-deficit second-active base-four Newton theorem

Date: 2026-08-02

Status: **PROVED; INDEPENDENT AUDIT PASSED**.

## 1. Statement

Write

\[
N_{q,j}(z)=\sum_{r=0}^{2q}\Delta_s^jC_{q,r}(4)z^r.
\]

For every (m\ge0), every coefficient of the second active Newton row
at odd deficit is strictly positive:

\[
\boxed{
[z^r]N_{2m+1,m+1}(z)>0
\qquad(0\le r\le4m+2).
}
\tag{1}
\]

Equivalently,

\[
\Delta_s^{m+1}C_{2m+1,r}(4)>0
\]

for every natural-support offset.  This promotes the previous exact
proof candidate after an independent reconstruction of its normalization,
positive kernel, four exceptional top coefficients, and bases.

## 2. Independent normalization

If (p=2s-5-q), the generating polynomial of a normalized (B_p) row
is

\[
\sum_r C_{q,r}(s)z^r
=\frac{s^{2s-2}}{p!z^{2p}}B_p(s,z/s).
\tag{2}
\]

Indeed, the coefficient of (z^r) on the right is

\[
\frac{[\beta^{2p+r}]B_p}{p!}
s^{2s-2-(2p+r)}
=\frac{[\beta^{2p+r}]B_p}{p!s^{2s-8-2q+r}}.
\]

For odd (q=2m+1), the boundary factor makes the second active row

\[
N_{q,m+1}(z)=
\sum_r\{C_{q,r}(m+5)-(m+1)C_{q,r}(m+4)\}z^r.
\tag{3}
\]

Set (s=m+5\), so (q=2s-9), and assume first (s\ge6).  Formula
(2) identifies the two terms in (3) with (B_4(s)) and (B_2(s-1)).
The exact fixed-page formulas are

\[
B_2(u,\beta)=4\beta^4(1+2\beta)^{2u-6}
(1+u\beta)^{2u-8},
\]

\[
B_4(s,\beta)=24\beta^4(1+s\beta)^{2s-12}L_s(\beta).
\]

Writing (L_s=\beta^4P_s) and dividing the common
((1+z)^{2s-12}) gives

\[
H_s(z):=\frac{N_{2s-9,s-4}(z)}{(1+z)^{2s-12}}
=A_s(z)-Q_s(z),
\tag{4}
\]

where, with (n=s-5\ge1) and (M=2n=2s-10),

\[
A_s=s^MP_s(z/s),
\qquad
Q_s=2(s-4)(s-1+2z)^{M+2}(1+z)^2.
\tag{5}
\]

Thus no untracked factorial, (s)-power, or common ((1+z))-factor is
present in the comparison.

## 3. Transport identity and the non-top range

The proved (B_4) recurrence is

\[
P_{s+1}=(1+4\beta)^2P_s+D_s^*,
\qquad D_s^*\ge_{\rm coeff}0.
\tag{6}
\]

Put

\[
\mathcal D_s(z)=(s+1)^{M+2}D_s^*(z/(s+1))
\]

and (b_{s,k}=[\beta^k](1+4\beta)^2P_s\).  Homogenization gives the
exact coefficient identity

\[
[z^k]\{A_{s+1}-(s+4z)^2A_s\}
=[z^k]\mathcal D_s+
\{(s+1)^{M+2-k}-s^{M+2-k}\}b_{s,k}.
\tag{7}
\]

Both terms are nonnegative for (0\le k\le M+2).  Only the four top
degrees (M+3,\ldots,M+6) escape this monotonic-power argument.

## 4. Fixed positive kernel dominates the moving boundary

The positive decomposition behind (6), after division by (\beta^4),
contains

\[
(1+2\beta)^M\,2\sum_{j=0}^6i_j(n)\beta^j
\]

and its (r=3) term

\[
\binom{M+2}{3}\beta(1+2\beta)^{M-1}
\sum_{j=0}^6\{q_j(n)+7d_j(n)\}\beta^j.
\]

All omitted terms are coefficientwise nonnegative.  Define

\[
\begin{aligned}
U&=n+6+2z,&V&=n+5+2z,\\
J_i&=\sum_{j=0}^6i_j(n)(n+6)^{2-j}z^j,&
J_a&=\sum_{j=0}^6(q_j+7d_j)(n+6)^{2-j}z^j.
\end{aligned}
\]

Then

\[
\mathcal D_s\ge_{\rm coeff}
U^{M-1}\left\{2UJ_i+\binom{M+2}{3}zJ_a\right\}.
\tag{8}
\]

Direct collection, with no interpolation in (n), gives the fixed
kernel

\[
K_n(z)=2UJ_i+\binom{M+2}{3}zJ_a
-2(n+2)V^5(1+z)^2.
\tag{9}
\]

After positive denominators are cleared, its eight coefficients have
the following numerators:

\[
\begin{array}{c|l}
0&2n^6+90n^5+1490n^4+12034n^3+50202n^2+100266n+69148\\
1&16n^6+816n^5+14756n^4+126252n^3+544632n^2+1107600n+784416\\
2&10n^6+590n^5+18662n^4+194134n^3+870618n^2+1795722n+1299852\\
3&380n^5+11164n^4+174104n^3+813212n^2+1680980n+1230264\\
4&96n^6+3944n^5+110688n^4+1095188n^3+3920448n^2+6659084n+4321764\\
5&928n^6+33784n^5+609624n^4+4110328n^3+11606408n^2+16402864n+9385416\\
6&96n^7+3944n^6+155316n^5+1827772n^4+8828448n^3+19795488n^2+23216256n+11598912\\
7&336n^7+22888n^6+367344n^5+2534136n^4+8623808n^3+15050816n^2+14403328n+6206976.
\end{array}
\tag{10}
\]

The denominators in rows (0,1,2,3) are respectively (1,3,3,3);
those in rows (4,5,6,7) are
(3(n+6),3(n+6)^2,3(n+6)^3,3(n+6)^4).  Hence (K_n>_{\rm coeff}0)
for every (n\ge1).

Because (U=V+1), equations (8)--(10) imply

\[
\mathcal D_s
\ge_{\rm coeff}2(n+2)U^{M-1}V^5(1+z)^2
\ge_{\rm coeff}2(n+2)V^{M+4}(1+z)^2
=Q_{s+1}.
\tag{11}
\]

The positive term ((s+4z)^2Q_s) in the boundary transport may be
dropped.  Combining (7) and (11) proves

\[
[z^k]\{H_{s+1}-(s+4z)^2H_s\}>0
\quad(0\le k\le M+2).
\tag{12}
\]

## 5. Four exceptional top degrees

Independent reverse-coefficient extraction from the three terms defining
(L_s) gives, from the highest degree downward, the four remaining
coefficients (T_0,T_1,T_2,T_3):

\[
T_0=4^n(96n-128)+756\,9^n,
\]

\[
\begin{aligned}
T_1={}&16^n(1024n+1024)
+4^n(96n^3+352n^2-384n-2496)\\
&+9^n(504n^2+2592n+7344),
\end{aligned}
\]

\[
\begin{aligned}
T_2={}&16^n(512n^3+3584n^2+12672n+12160)\\
&+4^n(48n^5+392n^4+600n^3-3488n^2-14728n-17064)\\
&+9^n(168n^4+1644n^3+7860n^2+20604n+28332),
\end{aligned}
\]

\[
\begin{aligned}
3T_3={}&16^n(384n^5+4800n^4+30464n^3+113280n^2+236992n+196224)\\
&+4^n(48n^7+584n^6+2040n^5-3888n^4-51856n^3\\
&\hspace{35mm}-170648n^2-264488n-168240)\\
&+9^n(112n^6+1560n^5+10016n^4+38648n^3\\
&\hspace{35mm}+95904n^2+149872n+125304).
\end{aligned}
\tag{13}
\]

For (T_t), the only possibly negative summand is the displayed
(4^n)-polynomial.  After shifting (n=x+t+2), every monomial
coefficient in that polynomial is positive.  Therefore (T_t>0) for
(n\ge t+2).  The ten omitted boundary cases

\[
6676,\ 117000,\ 1947088,\ 853360,\ 23016212,\ 551714560,
\ 3493752,\ 150983432,\ 5256031416,\ 162813496168
\]

are all positive.  This proves the four top coefficients universally.
The independent verifier derives (13) from reverse coefficient
convolution before checking these positivity certificates; it does not
merely re-enter the claimed (T_t)'s.

Together with (12),

\[
\boxed{H_{s+1}-(s+4z)^2H_s>_{\rm coeff}0\qquad(s\ge6).}
\tag{14}
\]

## 6. Bases and induction

The two required natural-support bases are

\[
H_5=52+64z+28z^2,
\]

obtained directly from the three exact (q=1) layer polynomials, and

\[
H_6=14132+50328z+76976z^2+65104z^3+32256z^4
+8912z^5+1076z^6.
\]

The first covers (m=0).  Starting from (H_6), recurrence (14) and
the positive transport factor ((s+4z)^2) prove (H_s>_{\rm coeff}0)
for every (s\ge6).  Restoring the positive common
((1+z)^{2s-12}) proves (1).

## 7. Remaining boundary

This theorem proves only the odd-deficit second active row.  The even
second active row, the third and later active rows, and the full
base-four Newton conjecture remain open.
