# Independent audit of Newton top depths \(6,7,8\)

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS}}
\]

The Newton coefficients at top depths \(d=6,7,8\) were recomputed
from the finite Lagrange/profile definitions.  No fitted coefficient
from a theorem statement, summary, or existing top-tail verifier was
used as input.

For each depth:

- the degree bound \(\deg_k p_{k,d}\le2d\) is proved independently
  from the profile cancellation and triangular Newton conversion;
- \(2d+1\) exact values determine the polynomial;
- four further exact \(k\)-values, not used in interpolation, agree;
- exact factorization and an integer-interval positivity certificate
  are checked symbolically.

The three polynomials have degrees exactly \(12,14,16\), with leading
coefficients
\[
\frac4{45},\qquad \frac8{315},\qquad \frac2{315},
\]
respectively.  These are precisely \(2^d/d!\).

## 1. Independent source computation

Put \(z=s^{-1}\).  The verifier constructs the normalized falling
product
\[
F_{\alpha,r}(z)
=\prod_{a=0}^{r-1}\left(1-(\alpha+a)z\right)
\]
and the normalized finite Lagrange sum
\[
E_{\beta,r}(z)
=\sum_{t=0}^{r}
\binom rt2^{r-t}(-1)^t
\prod_{a=0}^{t-1}
\left(1-(\beta+r+a)z\right).
\]
These are exactly
\[
F_{\alpha,r}(z)
=s^{-r}(s-\alpha)_{\underline r},
\]
\[
E_{\beta,r}(z)
=\frac{2^rr!}{s^r}
E(s,s-\beta-r,r).
\]

Only coefficients through \(z^{12}\) are retained.  This is exact,
because depth \(d\) uses total profile loss \(L=d+4\), and the largest
requested depth is eight.

The normalized consecutive difference is generated as
\[
D_{\beta,r}(z)
=E_{\beta,r}(z)-2rzE_{\beta+1,r-1}(z).
\]
The three profile series are then
\[
G_{0,r}=F_{0,r}D_{0,r},
\qquad
G_{1,r}=F_{2,r}D_{2,r},
\]
\[
G_{2,r}
=F_{4,r}D_{4,r}
+8rz^2F_{4,r-1}E_{4,r-1}.
\]
Thus
\[
G_{h,r}(z)=\sum_{\ell=0}^{12}R_{\ell,h}(r)z^\ell
+O(z^{13})
\]
is obtained directly from the source profiles, including the shifted
consecutive term and the exceptional \(h=2\) contribution.

For \(L=j+4\), the ordinary top coefficient is evaluated by the exact
binomial determinant average
\[
b_{k,j}
=\frac1{2k(k-1)2^k}
\sum_{r=0}^k\binom kr
\sum_{\ell=0}^{L}
\left(
R_{\ell,1}(r)R_{L-\ell,1}(k-r)
-
R_{\ell,0}(r)R_{L-\ell,2}(k-r)
\right).
\]

Finally, the verifier independently generates the base-four Stirling
coefficients from
\[
{n\brace q}_4
=(q+4){n-1\brace q}_4+{n-1\brace q-1}_4
\]
and uses
\[
p_{k,d}
=\sum_{j=0}^d
b_{k,j}{\,2k-4-j\brace 2k-4-d\,}_4.
\]
All arithmetic before interpolation is integral or rational and
exact.

## 2. Why \(2d+1\) values suffice

At ordinary depth \(j\), total profile loss is \(L=j+4\).
The marked profile lemma and the two determinant cancellations give:

1. the degree-\(L\) kernel cancels pointwise;
2. the degree-\((L-1)\) kernel is antisymmetric and has zero binomial
   expectation;
3. the mixed falling-moment identity makes the averaged numerator a
   polynomial \(Q_L(k)\) of degree at most \(L-2=j+2\).

The division is polynomial, rather than merely a rational
large-\(k\) estimate.  At \(k=0\), all three zero-edge profiles equal
one and their positive-loss symbols vanish, so \(Q_L(0)=0\).  At
\(k=1\), the binomial convolution reduces to
\[
2G_{1,1}-G_{0,1}-G_{2,1}.
\]
The exact one-edge profiles are
\[
G_{0,1}=1-z,\qquad
G_{1,1}=1-z-2z^2,\qquad
G_{2,1}=1-z-4z^2,
\]
and hence this expression vanishes identically.  Thus
\[
k(k-1)\mid Q_L(k).
\]
After division by \(2k(k-1)\),
   \[
   \deg_k b_{k,j}\le j.
   \]

For fixed \(r\), the near-diagonal coefficient
\[
T_{n,r}={n\brace n-r}_4
\]
is a polynomial in \(n\) of degree at most \(2r\).  This follows
either from the deficit-\(r\) partition interpretation or inductively
from the displayed \(4\)-Stirling recurrence.

The \(j\)-th summand in
\[
p_{k,d}
=\sum_{j=0}^d b_{k,j}T_{2k-4-j,d-j}
\]
therefore has \(k\)-degree at most
\[
j+2(d-j)=2d-j\le2d.
\]
Hence
\[
\boxed{\deg_kp_{k,d}\le2d.}
\]

It is consequently legitimate—not merely heuristic—to recover
\(p_{k,d}\) from \(2d+1\) exact values.  The verifier additionally
checks four spare values beyond the interpolation range.

## 3. Exact depth-six polynomial

\[
\boxed{
\begin{aligned}
p_{k,6}
={}&\frac{(k-5)(k-4)(k-3)(k-2)}{45360}\,Q_6(k),\\
Q_6(k)
={}&4032k^8-24192k^7+9072k^6-319760k^5\\
&-296716k^4+3115760k^3+29380477k^2\\
&+103674567k+153772290.
\end{aligned}}
\]

The interpolation used the 13 values \(5\le k\le17\).  The unused
values at \(k=18,19,20,21\) agree exactly.

Its degree is 12 and
\[
[k^{12}]p_{k,6}=\frac4{45}=\frac{2^6}{6!}.
\]

For \(x=k-6\),
\[
\begin{aligned}
Q_6(x+6)
={}&4032x^8+169344x^7+3057264x^6+30488752x^5\\
&+177900884x^4+578481488x^3+823870525x^2\\
&+16300131x+58786560.
\end{aligned}
\]
Every coefficient is positive.  The active Newton index
\(2k-4-6\) first becomes nonnegative at \(k=5\).  Therefore
\[
\boxed{
p_{5,6}=0,\qquad p_{k,6}>0\quad(k\ge6).
}
\]
The first positive value is
\[
p_{6,6}=31104.
\]

## 4. Exact depth-seven polynomial

\[
\boxed{
\begin{aligned}
p_{k,7}
={}&\frac{(k-6)(k-5)(k-4)(k-3)(k-2)}{22680}\,
Q_7(k),\\
Q_7(k)
={}&576k^9-4608k^8+9744k^7-75488k^6\\
&-66724k^5+254944k^4+6661499k^3\\
&+37990606k^2+117200435k+160178004.
\end{aligned}}
\]

The interpolation used the 15 values \(6\le k\le20\).  The unused
values at \(k=21,22,23,24\) agree exactly.

Its degree is 14 and
\[
[k^{14}]p_{k,7}=\frac8{315}=\frac{2^7}{7!}.
\]

For \(x=k-7\),
\[
\begin{aligned}
Q_7(x+7)
={}&576x^9+31680x^8+767760x^7+10675504x^6\\
&+92533868x^5+504730916x^4+1637411011x^3\\
&+2641830621x^2+1114952148x+440695080.
\end{aligned}
\]
Every coefficient is positive.  The active range begins at \(k=6\),
and hence
\[
\boxed{
p_{6,7}=0,\qquad p_{k,7}>0\quad(k\ge7).
}
\]
The first positive value is
\[
p_{7,7}=2331720.
\]

## 5. Exact depth-eight polynomial

\[
\boxed{
\begin{aligned}
p_{k,8}
={}&\frac{(k-6)(k-5)(k-4)(k-3)(k-2)}{5443200}\,
Q_8(k),\\
Q_8(k)
={}&34560k^{11}-599040k^{10}+3893760k^9\\
&-17736960k^8+55219360k^7-15634240k^6\\
&+657272176k^5+682878800k^4-9060987065k^3\\
&-88234978600k^2-335731520391k\\
&-533577731400.
\end{aligned}}
\]

The interpolation used the 17 values \(6\le k\le22\).  The unused
values at \(k=23,24,25,26\) agree exactly.

Its degree is 16 and
\[
[k^{16}]p_{k,8}=\frac2{315}=\frac{2^8}{8!}.
\]

For \(x=k-8\),
\[
\begin{aligned}
Q_8(x+8)
={}&34560x^{11}+2442240x^{10}+77621760x^9\\
&+1457007360x^8+17800320160x^7+146682082240x^6\\
&+814106974576x^5+2932689703120x^4\\
&+6300148093255x^3+6999364090240x^2\\
&+4163497996089x+1222490102400.
\end{aligned}
\]
Every coefficient is positive, proving \(Q_8(k)>0\) for \(k\ge8\).
The remaining active value below this shift satisfies
\[
Q_8(7)=7054387200>0.
\]
Since the active range begins at \(k=6\),
\[
\boxed{
p_{6,8}=0,\qquad p_{k,8}>0\quad(k\ge7).
}
\]
The first positive value is
\[
p_{7,8}=155520.
\]

## 6. Verification scope

The independent verifier is
`independent_verify_top_nine.py`.  It:

- imports no existing OPG verifier;
- stores no target fitted polynomial as a computational input;
- generates every value from truncated finite products and Lagrange
  sums;
- uses respectively 13, 15, and 17 fitting points;
- verifies four additional points at each depth;
- checks exact degree and the leading coefficient \(2^d/d!\);
- factors each interpolant exactly;
- proves the active-range signs from positive shifted coefficients,
  with the single separate check \(Q_8(7)>0\).

The companion test
`test_independent_verify_top_nine.py` records the resulting exact
factorizations and positivity boundaries as regression data.  Those
expected expressions are used only after the independent computation,
not to generate or fit it.

## 7. Conclusion

The independent computation certifies three new exact layers beyond
the previously audited top six:
\[
\begin{array}{c|c|c|c}
d&\deg p_{k,d}&\text{first active }k&
\text{sign on the active range}\\ \hline
6&12&5&p_{5,6}=0,\ p_{k,6}>0\ (k\ge6)\\
7&14&6&p_{6,7}=0,\ p_{k,7}>0\ (k\ge7)\\
8&16&6&p_{6,8}=0,\ p_{k,8}>0\ (k\ge7)
\end{array}
\]

No discrepancy was found in the degree, factorization, leading
coefficient, or active-interval sign.
