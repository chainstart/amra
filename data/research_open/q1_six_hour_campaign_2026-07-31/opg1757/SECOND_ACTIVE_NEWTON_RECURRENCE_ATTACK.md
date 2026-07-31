# OPG-1757: second active Newton recurrence attack

Date: 2026-08-01
Status: **ODD RECURRENCE HAS AN EXACT PROOF CANDIDATE PENDING INDEPENDENT
AUDIT; EVEN RECURRENCE AND THE FULL NEWTON CLAIM REMAIN CONJECTURAL**

Let

\[
 N_{q,j}(z)=\sum_{r=0}^{2q}\Delta^j C_{q,r}(4)z^r,
 \qquad m=\lfloor q/2\rfloor.
\]

The boundary factor makes the second active row exactly

\[
 N_{q,m+1}(z)
 =\sum_r\{C_{q,r}(5+m)-(m+1)C_{q,r}(4+m)\}z^r.
\tag{1}
\]

For odd \(q=2m+1\), (1) is a normalized coefficientwise comparison of
\(B_4\) at \(s=m+5\) against \(B_2\) at \(s=m+4\).  For even
\(q=2m\), it compares \(B_5\) against \(B_3\).  Thus all four inputs
already have exact all-\(s\) formulas, but their separate positivity does
not determine the sign of (1).

Put, for \(s\ge6\),

\[
 G_s^{\rm o}(z)=N_{2s-9,s-4}(z),
 \qquad
 H_s^{\rm o}(z)=\frac{G_s^{\rm o}(z)}{(1+z)^{2s-12}},
\tag{2}
\]

and

\[
 G_s^{\rm e}(z)=N_{2s-10,s-4}(z),
 \qquad
 H_s^{\rm e}(z)=
 \frac{G_s^{\rm e}(z)}{(1+z)^{\max(0,2s-14)}}.
\tag{3}
\]

The divisibilities in (2)--(3) follow directly from the common
\((1+s\beta)\)-powers in the exact \(B_2,\ldots,B_5\) formulas.

The promising universal target is

\[
\boxed{
 H_{s+1}^{\rm o}(z)-(s+4z)^2H_s^{\rm o}(z)>_{\rm coeff}0,
}
\tag{4}
\]

\[
\boxed{
 H_{s+1}^{\rm e}(z)-(s+5z)^2H_s^{\rm e}(z)>_{\rm coeff}0.
}
\tag{5}
\]

If (4)--(5) are proved, the positive base rows at \(s=6\) inductively
prove every second active Newton coefficient for every deficit.  The
transport factors \(s+4z\) and \(s+5z\) are not fitted arbitrary bases:
they are the homogenized versions of the \((1+4\beta)^2\) and
\((1+5\beta)^2\) transports in the already proved coefficientwise
recurrences for \(B_4\) and \(B_5\).  The missing step is to carry those
old recurrence decompositions through the changing normalization
\(\beta=z/s\) and the subtracted \(B_2/B_3\) boundary term.

Exact evidence:

- all 1,023 coefficients of (1) through \(q=31\) are strictly positive;
- all 616 coefficients in the two recurrence remainders (4)--(5) for
  \(s=6,\ldots,19\) are strictly positive;
- no zero or negative coefficient occurs.

`verify_second_active_newton_probe.py` reproduces these counts.  They are
finite evidence and do not prove (4)--(5).  A proof should adapt the
finite positive-kernel decompositions in `B4_UNIFORM_POSITIVITY.md` and
`B5_UNIFORM_POSITIVITY_ATTEMPT.md`; interpolation in \(s\) would not close
the growing-degree tail and is not an acceptable substitute.

## 2. Exact odd-parity reduction to a fixed positive kernel

The following is no longer a finite extrapolation.  It is an exact proof
candidate for (4), isolated here for independent audit.  The analogous
even statement (5) is **not** proved.

Write

\[
 n=s-5\ge1,\qquad m=2n=2s-10,
 \qquad P_s(\beta)=L_s(\beta)/\beta^4.
\]

The exact odd comparison is

\[
 H_s^{\rm o}(z)=A_s(z)-Q_s(z),
\]

where

\[
 A_s=s^mP_s(z/s),\qquad
 Q_s=2(s-4)(s-1+2z)^{m+2}(1+z)^2.
\tag{6}
\]

Let

\[
 P_{s+1}=(1+4\beta)^2P_s+D_s^*.
\]

The proved \(B_4\) recurrence says \(D_s^*\ge_{\rm coeff}0\).  Put

\[
 \mathcal D_s(z)=(s+1)^{m+2}D_s^*(z/(s+1)).
\]

If \(b_{s,k}=[\beta^k](1+4\beta)^2P_s\), then the exact coefficient
identity is

\[
 [z^k]\{A_{s+1}-(s+4z)^2A_s\}
 = [z^k]\mathcal D_s+
 \{(s+1)^{m+2-k}-s^{m+2-k}\}b_{s,k}.
\tag{7}
\]

Consequently the second term in (7) is nonnegative for
\(0\le k\le m+2\).  It remains to dominate the new boundary term

\[
 Q_{s+1}=2(s-3)(s+2z)^{m+4}(1+z)^2.
\tag{8}
\]

The positive-kernel decomposition in the existing \(B_4\) proof gives

\[
 \beta^4D_s^*=(1+2\beta)^mI_s+
 \sum_{r=3}^{m+2}\binom{m+2}{r}
 \beta^r(1+2\beta)^{m+2-r}A_{s,r},
\]

where

\[
 I_s=2\beta^4\sum_{j=0}^6i_j(n)\beta^j,
 \qquad
 A_{s,3}=\beta^2\sum_{j=0}^6\{q_j(n)+7d_j(n)\}\beta^j.
\]

All omitted \(r\ge4\) summands are coefficientwise nonnegative.  Define

\[
 \begin{aligned}
 U&=n+6+2z=s+1+2z, &V&=n+5+2z=s+2z,\\
 J_i&=\sum_{j=0}^6i_j(n)(n+6)^{2-j}z^j,&
 J_a&=\sum_{j=0}^6(q_j+7d_j)(n+6)^{2-j}z^j.
 \end{aligned}
\]

Keeping only the \(I_s\) and \(r=3\) pieces therefore yields

\[
 \mathcal D_s\ge_{\rm coeff}
 U^{m-1}\left\{2UJ_i+\binom{m+2}{3}zJ_a\right\}.
\tag{9}
\]

The crucial finite identity is

\[
 K_n(z):=2UJ_i+\binom{m+2}{3}zJ_a
 -2(n+2)V^5(1+z)^2>_{\rm coeff}0.
\tag{10}
\]

Indeed, its eight coefficients, after harmless positive denominators,
are as follows:

\[
\begin{array}{c|c|c}
k&\text{numerator of }[z^k]K_n&\text{denominator}\\ \hline
0&2n^6+90n^5+1490n^4+12034n^3+50202n^2+100266n+69148&1\\
1&16n^6+816n^5+14756n^4+126252n^3+544632n^2+1107600n+784416&3\\
2&10n^6+590n^5+18662n^4+194134n^3+870618n^2+1795722n+1299852&3\\
3&380n^5+11164n^4+174104n^3+813212n^2+1680980n+1230264&3\\
4&96n^6+3944n^5+110688n^4+1095188n^3+3920448n^2+6659084n+4321764&3(n+6)\\
5&928n^6+33784n^5+609624n^4+4110328n^3+11606408n^2+16402864n+9385416&3(n+6)^2\\
6&96n^7+3944n^6+155316n^5+1827772n^4+8828448n^3+19795488n^2+23216256n+11598912&3(n+6)^3\\
7&336n^7+22888n^6+367344n^5+2534136n^4+8623808n^3+15050816n^2+14403328n+6206976&3(n+6)^4.
\end{array}
\]

Thus (10), \(U=V+1\), and (9) imply

\[
 \mathcal D_s\ge_{\rm coeff}
 2(n+2)U^{m-1}V^5(1+z)^2
 \ge_{\rm coeff}Q_{s+1}.
\tag{11}
\]

Combining (7) and (11) proves every coefficient of (4) through degree
\(m+2\).  The exponent difference in (7) is negative only in the four
remaining degrees.  Direct extraction from the top four terms of the
three-exponential formula for \(L_s\) gives, from highest degree downward,

\[
\begin{aligned}
T_0={}&4^n(96n-128)+756\,9^n,\\
T_1={}&16^n(1024n+1024)
 +4^n(96n^3+352n^2-384n-2496)\\
&+9^n(504n^2+2592n+7344),\\
T_2={}&16^n(512n^3+3584n^2+12672n+12160)\\
&+4^n(48n^5+392n^4+600n^3-3488n^2-14728n-17064)\\
&+9^n(168n^4+1644n^3+7860n^2+20604n+28332),\\
T_3={}&\frac{16^n}{3}(384n^5+4800n^4+30464n^3+113280n^2+236992n+196224)\\
&+\frac{4^n}{3}(48n^7+584n^6+2040n^5-3888n^4-51856n^3-170648n^2-264488n-168240)\\
&+\frac{9^n}{3}(112n^6+1560n^5+10016n^4+38648n^3+95904n^2+149872n+125304).
\end{aligned}
\tag{12}
\]

For \(T_t\), the possibly negative \(4^n\)-polynomial is nonnegative
once \(n\ge t+2\): after shifting \(n=x+t+2\), every displayed
polynomial coefficient is positive.  The remaining finite values are

\[
\begin{array}{c|rrrr}
t\backslash n&1&2&3&4\\\hline
0&6676&&&\\
1&117000&1947088&&\\
2&853360&23016212&551714560&\\
3&3493752&150983432&5256031416&162813496168.
\end{array}
\]

Hence all four quantities in (12) are strictly positive.  This closes
(4), subject only to independent verification of the transcription and
normalization above.  The positive bases

\[
H_5^{\rm o}=52+64z+28z^2,
\]

\[
H_6^{\rm o}=14132+50328z+76976z^2+65104z^3
+32256z^4+8912z^5+1076z^6
\]

then imply the **odd-parity second-active theorem candidate**

\[
 \gamma_{2m+1,r,m+1}>0\qquad(m\ge0,\ 0\le r\le4m+2).
\tag{13}
\]

Equation (13) is marked **PENDING INDEPENDENT AUDIT**, not promoted from
finite evidence.  In particular, it does not establish the even parity,
the third active row, or the complete conjecture (1) in
`BASE4_NEWTON_GLOBAL_ATTACK.md`.
