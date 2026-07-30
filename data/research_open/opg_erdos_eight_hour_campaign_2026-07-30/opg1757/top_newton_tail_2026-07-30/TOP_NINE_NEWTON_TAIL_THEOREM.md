# OPG-1757: nine exact layers at the top Newton boundary

Date: 2026-07-30

## 0. Result

Retain
\[
c_k(s)=\sum_{q=0}^{2k-4}a_{k,q}\binom{s-4}{q},
\qquad
m=2k-4,
\qquad
p_{k,d}=\frac{a_{k,m-d}}{(m-d)!}.
\]
The top-six theorem gives \(p_{k,d}\) for \(0\le d\le5\).

### Theorem

The next three normalized Newton coefficients are
\[
\boxed{
\begin{aligned}
p_{k,6}
={}&\frac{(k-5)(k-4)(k-3)(k-2)}{45360}\\
&\times\bigl(
4032k^8-24192k^7+9072k^6-319760k^5-296716k^4\\
&\hspace{19mm}
+3115760k^3+29380477k^2+103674567k+153772290
\bigr),
\end{aligned}}                                      \tag{1}
\]
\[
\boxed{
\begin{aligned}
p_{k,7}
={}&\frac{(k-6)(k-5)(k-4)(k-3)(k-2)}{22680}\\
&\times\bigl(
576k^9-4608k^8+9744k^7-75488k^6-66724k^5\\
&\hspace{20mm}
+254944k^4+6661499k^3+37990606k^2\\
&\hspace{20mm}
+117200435k+160178004
\bigr),
\end{aligned}}                                      \tag{2}
\]
and
\[
\boxed{
\begin{aligned}
p_{k,8}
={}&\frac{(k-6)(k-5)(k-4)(k-3)(k-2)}{5443200}\\
&\times\bigl(
34560k^{11}-599040k^{10}+3893760k^9-17736960k^8\\
&\hspace{13mm}
+55219360k^7-15634240k^6+657272176k^5\\
&\hspace{13mm}
+682878800k^4-9060987065k^3-88234978600k^2\\
&\hspace{13mm}
-335731520391k-533577731400
\bigr).
\end{aligned}}                                      \tag{3}
\]

Every existing coefficient in depths \(0,\ldots,8\) is nonnegative,
and every coefficient in the active support is positive.  At the new
depths this says
\[
p_{k,6}>0\ (k\ge6),\qquad
p_{k,7}>0\ (k\ge7),\qquad
p_{k,8}>0\ (k\ge7).
\]
The boundary zeros \(p_{5,6}=p_{6,7}=p_{6,8}=0\) lie strictly below
the known first-support index \(\lfloor(k-2)/2\rfloor\).

## 1. Why finitely many values prove the identities

The finite-loss profile lemma writes
\[
U_{h,j}(s)
=\frac1{2^j j!}\sum_{\ell\ge0}R_{\ell,h}(j)s^{2j-\ell},
\qquad
\deg_j R_{\ell,h}\le\ell.
\]
In the determinant for \(c_k(s)\), binomial symmetrization converts
every monomial in \(j,k-j\) to an exact mixed falling moment.  It
follows that, for a fixed ordinary-power loss \(d\),
\[
\deg_k b_{k,d}\le d,
\qquad
c_k(s)=\sum_{d\ge0}b_{k,d}s^{m-d}.                 \tag{4}
\]
The Newton conversion is triangular:
\[
p_{k,d}
=b_{k,d}
-\sum_{e<d}p_{k,e}
[s^{m-d}](s-4)_{\underline{m-e}}.                 \tag{5}
\]
The coefficient in (5) is, up to sign, the elementary symmetric
polynomial of degree \(d-e\) in
\(4,5,\ldots,m-e+3\).  Newton's identities and Faulhaber's formula
show that it is a polynomial in \(m=2k-4\) of degree at most
\(2(d-e)\).  Induction in (5) therefore gives
\[
\boxed{\deg_k p_{k,d}\le2d.}                       \tag{6}
\]
This holds on the whole range \(m-d\ge0\); falling factorials make
the unavailable lower terms vanish at the boundary.

For each \(d=6,7,8\), the companion verifier does not assume
(1)--(3).  It evaluates the exact finite Lagrange profiles
\[
\begin{aligned}
U_{0,j}(s)&=(s)_{\underline j}D(s,s-j,j),\\
U_{1,j}(s)&=(s-2)_{\underline j}D(s,s-2-j,j),\\
U_{2,j}(s)&=(s-4)_{\underline j}D(s,s-4-j,j)
+4(s-4)_{\underline{j-1}}E(s,s-3-j,j-1),
\end{aligned}
\]
forms the determinant, and takes exact base-four forward
differences.  It reconstructs \(p_{k,d}\) from \(2d+1\) distinct
integer values.  Bound (6) makes that reconstruction a proof of a
polynomial identity.  It then checks later \(k\)-values that were not
used for reconstruction and checks the low boundary separately.
All arithmetic is rational or integral.

## 2. Positivity

Let the bracket in (1) be \(Q_6(k)\).  With \(k=x+6\),
\[
\begin{aligned}
Q_6(x+6)={}&4032x^8+169344x^7+3057264x^6
+30488752x^5\\
&+177900884x^4+578481488x^3+823870525x^2\\
&+16300131x+58786560.
\end{aligned}
\]
Every coefficient is positive.

For the bracket \(Q_7\) in (2), put \(k=x+7\):
\[
\begin{aligned}
Q_7(x+7)={}&576x^9+31680x^8+767760x^7
+10675504x^6\\
&+92533868x^5+504730916x^4+1637411011x^3\\
&+2641830621x^2+1114952148x+440695080.
\end{aligned}
\]
Again every coefficient is positive.

For the bracket \(Q_8\) in (3), the same shift gives
\[
\begin{aligned}
Q_8(x+7)={}&34560x^{11}+2062080x^{10}+55100160x^9
+862609920x^8\\
&+8656980640x^7+56852723040x^6+235409656336x^5\\
&+532086497280x^4+324469036615x^3
-581477383605x^2\\
&+638518398174x+7054387200.
\end{aligned}
\]
All terms outside the cubic-to-linear block are positive.  The
remaining block equals
\[
x\left(
324469036615x^2-581477383605x+638518398174
\right).
\]
Its quadratic has positive leading coefficient and discriminant
\[
-490601850421766697768015<0.
\]
It is therefore positive for \(x>0\), while the constant term handles
\(x=0\).  This proves all three sign assertions.

Finally, the leading coefficients in (1)--(3) are
\[
\frac4{45},\quad\frac8{315},\quad\frac2{315},
\]
respectively.  They equal \(2^d/d!\) for \(d=6,7,8\), providing an
independent consistency check against the fixed-top-depth theorem.

## 3. Scope

This establishes the entire top boundary through depth eight, for all
parameters, not merely for a finite range of \(k\).  Combined with
the growing top-window theorem it is a useful exact certificate and
a check on its asymptotic constants.  It still leaves the
linear-width middle of the Newton row open and therefore does not by
itself prove OPG-1757.

Reproduce with
```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/top_newton_tail_2026-07-30
pytest -q test_verify_top_nine_newton_tail.py
python3 verify_top_nine_newton_tail.py
```
