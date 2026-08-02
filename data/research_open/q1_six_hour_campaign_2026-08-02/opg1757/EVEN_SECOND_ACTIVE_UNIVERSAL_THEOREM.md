# OPG-1757: universal even second-active Newton positivity

Date: 2026-08-02

Status: **PROVED**

## 1. Theorem

Let

\[
N_{q,j}(z)=\sum_{r=0}^{2q}\Delta_s^j C_{q,r}(4)z^r,
\qquad m=\lfloor q/2\rfloor.
\]

> **Even second-active theorem.**  For every even deficit \(q=2m\)
> with \(m\ge1\),
> \[
> [z^r]N_{2m,m+1}(z)>0
> \qquad(0\le r\le4m).
> \tag{1}
> \]

Together with the independently audited odd theorem, this gives the
parity-free corollary

\[
\boxed{
\Delta_s^{\lfloor q/2\rfloor+1}C_{q,r}(4)>0
\quad(q\ge1,\ 0\le r\le2q).}
\tag{2}
\]

This proves the second active base-four Newton row for every deficit.  It
does not prove the third and later active rows, the full base-four Newton
conjecture, or the original arbitrary-host OPG-1757 statement.

## 2. Stable even row and the comparison lemma

Put \(s=m+5\).  The case \(s=6\), corresponding to \(q=2\), is the
direct positive boundary

\[
972+2480z+2760z^2+1504z^3+348z^4.
\tag{3}
\]

Assume henceforth that \(s\ge7\).  Use
\(u_j=1+j\beta\), \(\lambda_s=1+s\beta\), and write

\[
\begin{aligned}
A_s&=u_5^{2s-12}K_s^{(5)},\\
B_s&=\lambda_s^2u_4^{2s-10}K_s^{(4)},\\
C_s&=\lambda_s^4u_3^{2s-8}K_s^{(3)},\\
D_s&=\lambda_s^6u_2^{2s-6},\\
F_s&=A_s-3B_s+3C_s-D_s,
\end{aligned}
\tag{4}
\]

\[
J_s=u_3^{2s-8}K_s^{(3)}-\lambda_s^2u_2^{2s-6}.
\tag{5}
\]

The reduced row \(H_s(z)\), defined exactly in
`EVEN_SECOND_ACTIVE_PARTIAL_THEOREM.md`, has degree \(2s-6\).  That file
proved two facts which will be used here:

1. its six highest coefficients are positive for every \(s\ge7\);
2. for \(d\le2s-12\), positivity follows from
   \([\beta^d]\mathcal K_s>0\), where

\[
\mathcal K_s(\beta)
=\frac{F_s(\beta)}{3\beta^6}
-2(s-4)(s-1)^2\lambda_{s-1}^2
 \frac{J_{s-1}(\beta)}{\beta^2}.
\tag{6}
\]

Indeed, with \(N=2s-12-d\ge0\), exact homogenization gives

\[
\begin{aligned}
[z^d]H_s={}&s^N[\beta^d]\mathcal K_s\\
&+2(s-4)(s-1)^2G_d(s)
 \{s^N-(s-1)^N\},
\end{aligned}
\tag{7}
\]

where
\(G_d(s)=[\beta^d]\lambda_{s-1}^2J_{s-1}/\beta^2\ge0\) by the
proved \(B_3\) theorem.  Thus it remains only to prove

\[
\mathcal K_s>_{\rm coeff}0\qquad(s\ge7).
\tag{8}
\]

## 3. A positive part and the hard remainder

Set

\[
T_s=6(s-4)(s-1)^2\beta^4\lambda_{s-1}^2J_{s-1}
\tag{9}
\]

and

\[
M_s=3\beta^6\mathcal K_s=F_s-T_s.
\tag{10}
\]

Split

\[
M_s=Y_s+P_s,
\qquad
Y_s=A_s-3B_s-T_s,
\qquad
P_s=3C_s-D_s.
\tag{11}
\]

The second summand is coefficientwise nonnegative without any estimate:

\[
P_s=\lambda_s^4
\left(2u_3^{2s-8}K_s^{(3)}+J_s\right)
\ge_{\rm coeff}0.
\tag{12}
\]

The point of the split is that \(Y_s\), unlike \(M_s\) itself, has a
four-layer positive recurrence.

## 4. Four-layer recurrence for \(Y_s\)

Let \(L=2s-10\), and define the following four fixed-degree polynomials:

\[
\begin{aligned}
E_{5,s}={}&K_{s+1}^{(5)}-K_s^{(5)},\\
E_{4,s}={}&3\left(
u_5^2\lambda_s^2K_s^{(4)}
-u_4^2\lambda_{s+1}^2K_{s+1}^{(4)}\right),
\end{aligned}
\tag{13}
\]

\[
\begin{aligned}
E_{3,s}={}&-6(s-3)s^2\beta^4\lambda_s^2u_3^2K_s^{(3)}\\
&+6(s-4)(s-1)^2\beta^4u_5^2
 \lambda_{s-1}^2K_{s-1}^{(3)},\\
E_{2,s}={}&6(s-3)s^2\beta^4\lambda_s^4u_2^4\\
&-6(s-4)(s-1)^2\beta^4u_5^2
 \lambda_{s-1}^4u_2^2.
\end{aligned}
\tag{14}
\]

Direct subtraction of (11) gives the exact identity

\[
Y_{s+1}-u_5^2Y_s
=u_5^LE_{5,s}+u_4^LE_{4,s}
 +u_3^LE_{3,s}+u_2^LE_{2,s}.
\tag{15}
\]

Expand \(u_5=u_2+3\beta\), \(u_4=u_2+2\beta\), and
\(u_3=u_2+\beta\), and put

\[
R_{s,r}=3^rE_{5,s}+2^rE_{4,s}+E_{3,s}.
\tag{16}
\]

Merging exactly the first four binomial layers yields

\[
\boxed{
Y_{s+1}-u_5^2Y_s
=u_2^{L-4}I_s
+\sum_{r=4}^{L}\binom Lr\beta^ru_2^{L-r}R_{s,r},}
\tag{17}
\]

where

\[
I_s=u_2^4E_{2,s}
 +\sum_{r=0}^{3}\binom Lr\beta^ru_2^{4-r}R_{s,r}.
\tag{18}
\]

Let \(n=s-8\ge0\).  Exact expansion gives the following finite positive
certificate:

| fixed polynomial | nonzero positive monomials after \(s=n+8\) |
|---|---:|
| \(E_{5,s}\) | 36 |
| \(R_{s,4}=81E_{5,s}+16E_{4,s}+E_{3,s}\) | 59 |
| \(81E_{5,s}+8E_{4,s}\) | 52 |
| \(I_s\) | 112 |

Every listed monomial coefficient is strictly positive.  These are
fixed-degree identities, not interpolation over finitely many \(s\).

They also control every omitted layer.  For \(r\ge4\),

\[
\begin{aligned}
R_{s,r+1}-R_{s,r}
&=2^r\left(E_{4,s}+2(3/2)^rE_{5,s}\right)\\
&\ge_{\rm coeff}\frac{2^r}{8}
 \left(8E_{4,s}+81E_{5,s}\right)
\ge_{\rm coeff}0.
\end{aligned}
\tag{19}
\]

Since \(R_{s,4}\ge0\), all \(R_{s,r}\ge0\) for \(r\ge4\).  Equations
(17)--(19) therefore prove the universal recurrence

\[
\boxed{Y_{s+1}-u_5^2Y_s\ge_{\rm coeff}0\qquad(s\ge8).}
\tag{20}
\]

## 5. Tail induction

The two degrees just below the inductive tail have direct all-\(s\)
certificates.  For \(n=s-8\ge0\),

\[
[\beta^{14}]Y_s
=\frac{(n+2)(n+3)(n+4)(2n+3)}{681080400}P_{14}(n),
\tag{21}
\]

\[
[\beta^{15}]Y_s
=\frac{(n+1)(n+2)(n+3)(n+4)(2n+3)}{5108103000}P_{15}(n),
\tag{22}
\]

where

\[
\begin{aligned}
P_{14}(n)={}&12131007040n^{10}+2805027309728n^9
+164301451878720n^8\\
&+4044058250927352n^7+51645515707001160n^6
+397698300009358992n^5\\
&+1962912613323137765n^4+6283732244134867438n^3\\
&+12652260244623945405n^2+14576845307765180580n\\
&+7328964643179379200,
\end{aligned}
\tag{23}
\]

\[
\begin{aligned}
P_{15}(n)={}&297415107392n^{10}+35283444198112n^9
+1649736263073792n^8\\
&+37667583655665432n^7+470069337982462008n^6
+3618894188027596548n^5\\
&+18054555547697989393n^4+58785509859798324878n^3\\
&+120834656727835957335n^2+142446196312092933750n\\
&+73398486015170316000.
\end{aligned}
\tag{24}
\]

All coefficients displayed in (23)--(24) are positive.  The needed base
values are

\[
[\beta^{14}]Y_7=6462889978,
\tag{25}
\]

\[
\bigl([\beta^{14}]Y_8,[\beta^{15}]Y_8,[\beta^{16}]Y_8\bigr)
=(774777037056,1034570170784,600055653616).
\tag{26}
\]

Let \(Q_s=Y_{s+1}-u_5^2Y_s\ge0\).  For \(d\ge16\), (20) says

\[
[\beta^d]Y_{s+1}
=[\beta^d]Y_s+10[\beta^{d-1}]Y_s
 +25[\beta^{d-2}]Y_s+[\beta^d]Q_s.
\tag{27}
\]

Equations (21)--(22) supply the two lower entries in (27), while (26)
starts the induction.  Hence

\[
[\beta^d]Y_s>0
\qquad(s\ge8,\ d\ge14\text{ on the support}).
\tag{28}
\]

Equation (25) handles \(s=7\).

## 6. Completion of the row

For beta degrees \(6\le d\le13\), the low-column certificate in
`EVEN_SECOND_ACTIVE_PARTIAL_THEOREM.md` gives directly

\[
[\beta^d]M_s>0.
\tag{29}
\]

It consists of 84 positive shifted monomials and 48 independent direct
convolution checks.  For \(d\ge14\), equations (11), (12), and (28) give
the same conclusion.  Since \(M_s\) is divisible by \(3\beta^6\), this
proves (8) on its complete support.

Equation (7) now proves every coefficient through degree \(2s-12\).
The six reverse coefficients already proved in the boundary-band lemma
are precisely degrees \(2s-11,\ldots,2s-6\).  These two ranges partition
the support of \(H_s\), so \(H_s>_{\rm coeff}0\) for all \(s\ge7\).
Together with (3), theorem (1) follows.

## 7. Verification and scope firewall

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_even_second_active_universal.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_even_second_active_universal.py \
  test_even_second_active_partial.py
```

The first verifier checks all 259 monomials in the four recurrence
certificates, the 31 boundary-polynomial monomials, four exact bases, 105
direct recurrence coefficients, the low comparison columns, and the six
reverse columns.  The direct checks guard transcription only; the
unbounded conclusion is the algebraic induction (17)--(28).

The new theorem settles exactly one Newton order,
\(j=\lfloor q/2\rfloor+1\).  The global claim that every active
\(\gamma_{q,r,j}\) is positive remains open, as does the passage from the
complete-split coefficient model to arbitrary graphs in OPG-1757.
