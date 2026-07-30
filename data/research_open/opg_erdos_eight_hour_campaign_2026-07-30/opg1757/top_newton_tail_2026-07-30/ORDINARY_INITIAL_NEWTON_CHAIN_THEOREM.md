# OPG-1757: a proved initial Newton chain for ordinary symbols

Date: 2026-07-30

## 0. Result

Write
\[
b_{k,d}
=\sum_{r=0}^{d}\beta_{d,r}k^{d-r},
\qquad
a_{d,r}
=\frac{(-1)^r\beta_{d,r}}{\binom dr}.
\tag{1}
\]
The real-rootedness conjecture would imply that the entire row
\((a_{d,r})_{r=0}^d\) is positive and log-concave.  The first
nontrivial part of this conclusion can be proved unconditionally.

### Theorem 1 (initial normalized Newton chain)

For every \(d\ge3\),
\[
\boxed{
a_{d,0},a_{d,1},a_{d,2},a_{d,3}>0,
}
\tag{2}
\]
and
\[
\boxed{
a_{d,1}^2>a_{d,0}a_{d,2},
\qquad
a_{d,2}^2>a_{d,1}a_{d,3}.
}
\tag{3}
\]
The first inequality also holds for \(d=2\).

Consequently, for every admissible \(d\) and \(0\le r\le3\),
\[
\boxed{
|\beta_{d,r}|
\le
\binom dr(3d^2)^r.
}
\tag{4}
\]

This is an all-depth theorem, not finite evidence.  It proves the
weighted \(C=3\) estimate through rank three but does not control
ranks \(r\ge4\).

## 1. Positivity

The proved all-depth symbol formulas give
\[
e_1:=-\beta_{d,1}
=\frac{
22d^3+147d^2+161d-258
}{36},
\tag{5}
\]
\[
e_2:=\beta_{d,2}
=\frac{
286d^6+3546d^5+12721d^4-7812d^3
-86231d^2+40338d+209160
}{5184},
\tag{6}
\]
and
\[
\begin{aligned}
e_3:=-\beta_{d,3}
=\frac1{83980800}\bigl(&
158450d^9+2651625d^8+15805020d^7+6658380d^6\\
&-213815208d^5-151402725d^4+2063879770d^3\\
&+1562087520d^2-10631426832d-6142443840
\bigr).
\end{aligned}
\tag{7}
\]

Put \(x=d-1,d-2,d-3\), respectively.  The numerators of
(5)--(7) become
\[
22x^3+213x^2+521x+72,
\tag{8}
\]
\[
\begin{aligned}
286x^6+6978x^5+65341x^4+281556x^3
+524521x^2+347334x+217728,
\end{aligned}
\tag{9}
\]
and
\[
\begin{aligned}
158450x^9+6929775x^8+130781820x^7
+1366137900x^6\\
{}+8519582112x^5+32362130205x^4
+75192592450x^3\\
{}+109574155800x^2+97629278688x
+27461721600.
\end{aligned}
\tag{10}
\]
Every coefficient is positive.  Therefore \(e_r>0\) for
\(d\ge r\), \(1\le r\le3\), proving (2).

## 2. Exact Newton differences

Since
\[
a_{d,0}=1,\qquad
a_{d,1}=\frac{e_1}{d},\qquad
a_{d,2}=\frac{e_2}{\binom d2},\qquad
a_{d,3}=\frac{e_3}{\binom d3},
\]
exact simplification gives
\[
a_{d,1}^2-a_{d,2}
=
\frac{P_1(d)}
{2592d^2(d-1)},
\tag{11}
\]
where, after \(d=x+2\),
\[
\begin{aligned}
P_1(x+2)
={}&682x^7+17970x^6+190081x^5+1035960x^4\\
&+3092125x^3+4935066x^2+3813828x+935712,
\end{aligned}
\tag{12}
\]
and
\[
a_{d,2}^2-a_{d,1}a_{d,3}
=
\frac{P_2(d)}
{503884800d^2(d-2)(d-1)^2}.
\tag{13}
\]
After \(d=x+3\),
\[
\begin{aligned}
P_2(x+3)={}&
2648800x^{13}+165015200x^{12}+4584250535x^{11}\\
&+75076014295x^{10}+806001912771x^9
+5959501846077x^8\\
&+31001080123301x^7+113806907340373x^6\\
&+291209310185401x^5+504249957626123x^4\\
&+560412147187224x^3+368724645480492x^2\\
&+139206175492608x+38683739980800.
\end{aligned}
\tag{14}
\]
All coefficients and denominators are positive for the claimed
ranges.  This proves (3).

## 3. Rank-three weighted consequence

Equations (2)--(3) imply
\[
a_{d,2}<a_{d,1}^2,
\qquad
a_{d,3}<\frac{a_{d,2}^2}{a_{d,1}}
<a_{d,1}^3.
\tag{15}
\]
The exact first defect also satisfies
\[
e_1\le3d^3.
\tag{16}
\]
Indeed,
\[
36(3d^3-e_1)
=86d^3-147d^2-161d+258,
\]
which equals \(36\) at \(d=1,2\), and its forward difference is
\[
6(43d^2-6d-37)>0\qquad(d\ge2).
\]
Thus \(a_{d,1}=e_1/d\le3d^2\).  Combining this with (15) proves
(4).

## 4. A weaker sufficient target than real-rootedness

Positive real-rootedness of \(b_{k,d}\) is sufficient but not
necessary for the weighted \(C=3\) theorem.  It is enough to prove,
for every \(d\), that
\[
a_{d,r}>0,\qquad
a_{d,r}^2\ge a_{d,r-1}a_{d,r+1}
\quad(1\le r<d).
\tag{17}
\]
Indeed the ratios \(a_{d,r}/a_{d,r-1}\) would then be nonincreasing,
so
\[
a_{d,r}\le a_{d,1}^r\le(3d^2)^r.
\tag{18}
\]
Equation (17) therefore implies the full weighted symbol estimate
without a PF sequence, a stable-polynomial representation, or a proof
that all zeros are real.

Theorem 1 proves exactly the first two instances of (17).  The next
minimal theorem-level target is
\[
a_{d,3}^2\ge a_{d,2}a_{d,4},
\tag{19}
\]
which requires the all-depth rank-four ordinary symbol.

## 5. Relation to finite root evidence

Exact Sturm calculations currently show positive simple zeros through
substantial finite depth, including after removal of the forced factor
\[
\prod_{j=2}^{\lfloor(d+3)/2\rfloor}(k-j).
\]
They remain finite evidence.  The natural even and odd quotient
sequences fail the scalar Favard three-term recurrence already at
degrees six and seven, so no orthogonal-polynomial proof follows from
the observed interlacing without an additional transformation.

The theorem above is independent of that finite root search: it uses
only the three all-depth symbol identities.
