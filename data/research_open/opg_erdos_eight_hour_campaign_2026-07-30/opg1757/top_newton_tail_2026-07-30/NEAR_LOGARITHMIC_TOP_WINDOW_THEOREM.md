# OPG-1757: a near-logarithmic positive top window

Date: 2026-07-30

## 0. Result

Write
\[
c_k(s)=\sum_{q=0}^{2k-4}a_{k,q}\binom{s-4}{q},
\qquad
m=2k-4,
\qquad
p_{k,d}=\frac{a_{k,m-d}}{(m-d)!}.
\]
Also let
\[
T_{n,r}=[(s-4)_{\underline{n-r}}]s^n
       ={n\brace n-r}_4>0 .
\]

### Theorem 1

Uniformly for every integer \(d=d(k)\ge0\) such that
\[
\boxed{(d+5)\log(d+5)=o(\log k),}                  \tag{1}
\]
one has
\[
\boxed{
p_{k,d}=T_{m,d}(1+o(1))>0.
}                                                    \tag{2}
\]
In particular, all the coefficients
\[
\boxed{
a_{k,\,2k-4-d}>0
\quad\text{for}\quad
0\le d\le
\frac{\log k}{(\log\log k)^2}
}                                                    \tag{3}
\]
are positive for sufficiently large \(k\).

This improves the earlier condition
\(d^2\log d=o(\log k)\).  It still does not reach the
linear-width middle of the Newton row.

## 1. Sharpened uniform profile estimate

Normalize the prescribed-matching profiles by
\[
U_{h,r}(s)
=\frac1{2^rr!}\sum_{\ell\ge0}
 R_{\ell,h}(r)s^{2r-\ell},
\qquad h=0,1,2.
\]

### Lemma 2

There is an absolute constant \(C\) such that
\[
\boxed{
\|R_{\ell,h}\|_1
\le \exp\!\bigl(C(\ell+1)\log(\ell+2)\bigr)
}                                                    \tag{4}
\]
for \(h=0,1,2\).  Together with the marked degree estimate
\[
\deg_r[h^v]R_{\ell,h}(r)\le\ell-v,                 \tag{5}
\]
this implies, whenever \(k\ge2(j+5)\),
\[
\boxed{
|b_{k,j}|
\le
\exp\!\bigl(C(j+5)\log(j+5)\bigr)k^j,
\qquad
c_k(s)=\sum_{j\ge0}b_{k,j}s^{m-j}.
}                                                    \tag{6}
\]

### Proof

Only the coefficient-norm ledger needs improvement; all finite
Lagrange identities and the marked cancellation are unchanged.
For \(0\le\beta\le5\), put
\[
P_{\beta,u}(t,r)
=[s^{t-u}](s-\beta-r)_{\underline t}
=(-1)^u e_u(\beta+r,\ldots,\beta+r+t-1).           \tag{7}
\]
Newton's partition formula is
\[
e_u
=\sum_{\lambda\vdash u}
\frac{(-1)^{u-\ell(\lambda)}}{z_\lambda}
\prod_{i=1}^{\ell(\lambda)}S_{\lambda_i},
\qquad
S_v=\sum_{a=0}^{t-1}(\beta+r+a)^v,                 \tag{8}
\]
where \(z_\lambda\ge1\).

The binomial theorem and Faulhaber's formula, with
\(|B_q|\le4q!/(2\pi)^q\), give one absolute \(c\) such that
\[
\|S_v\|_1
\le\exp\!\bigl(c(v+1)\log(v+2)\bigr).              \tag{9}
\]
The point missed by the earlier coarse estimate is that the costs of
the factors in one partition add.  Since every part
\(\lambda_i\ge1\),
\[
\begin{aligned}
\sum_i(\lambda_i+1)\log(\lambda_i+2)
&\le
2\sum_i\lambda_i\log(u+2)\\
&=2u\log(u+2).                                     \tag{10}
\end{aligned}
\]
The number of partitions is
\(p(u)=\exp(O(\sqrt u))\), and the factors \(1/z_\lambda\)
can only reduce the coefficient norm.  Equations (8)--(10) therefore
give the sharper bivariate bound
\[
\boxed{
\|P_{\beta,u}\|_1
\le\exp\!\bigl(C_0(u+1)\log(u+2)\bigr).
}                                                    \tag{11}
\]
The same bound applies to
\([s^{r-u}](s-\alpha)_{\underline r}\).

In the normalized Lagrange sum, the loss-\(u\) polynomial in the
summation index has degree at most \(2u\).  Both changes
\[
t^a\longleftrightarrow(t)_{\underline v},
\qquad
(r)_{\underline v}\longleftrightarrow r^q
\]
use Stirling numbers of order at most \(2u\), bounded by
\((2u)^{2u}\).  Their combined norm cost is
\(\exp(O(u\log(u+2)))\), still within (11).  The exact identity
\[
\sum_{t=0}^r
\binom rt2^{r-t}(-1)^t(t)_{\underline v}
=(-1)^v(r)_{\underline v}                          \tag{12}
\]
then removes the summation index without further loss.

The normalized consecutive difference contributes only a factor
\(2r\) and one unit of loss.  The exceptional \(h=2\) term contributes
only \(8r\), two units of loss, and a product of two already bounded
profiles.  At total loss \(\ell\), every convolution has losses
\(u_1+\cdots+u_q=\ell+O(1)\), with \(q\le3\), and hence
\[
\sum_i(u_i+1)\log(u_i+2)
=O((\ell+1)\log(\ell+2)).                           \tag{13}
\]
There are only \(O(\ell^2)\) such terms.  This proves (4).

For completeness, at total determinant loss \(L=j+4\), the exact
binomial form is
\[
\frac1{2k(k-1)}
\mathbb E\sum_{\ell=0}^L
\left(
R_{\ell,1}(J)R_{L-\ell,1}(k-J)
-R_{\ell,0}(J)R_{L-\ell,2}(k-J)
\right).                                            \tag{14}
\]
The degree-\(L\) terms cancel pointwise.  At degree \(L-1\), the
mark-independent terms cancel pointwise and the remaining
mark-linear convolution is antisymmetric under
\((J,\ell)\leftrightarrow(k-J,L-\ell)\).  Thus the averaged numerator
has degree at most \(L-2=j+2\).

Ordinary-to-falling conversion and
\[
\mathbb E\bigl[(J)_{\underline a}
(k-J)_{\underline b}\bigr]
=\frac{(k)_{\underline{a+b}}}{2^{a+b}}             \tag{15}
\]
cost only \(\exp(O(L\log L))\).  Evaluating the resulting polynomial
at \(k\), then dividing by \(2k(k-1)\), proves (6).
\(\square\)

## 2. Dominance of the positive monic contribution

The exact triangular identity is
\[
p_{k,d}
=\sum_{j=0}^d b_{k,j}T_{m-j,d-j}.                 \tag{16}
\]
For \(m\ge4d\), the elementary \(4\)-Stirling estimates give
\[
\frac{T_{m-j,d-j}}{T_{m,d}}
\le16^d\frac{(d)_{\underline j}}{k^{2j}}
\le16^d\left(\frac d{k^2}\right)^j.               \tag{17}
\]
Using (6), for \(1\le j\le d\),
\[
\begin{aligned}
\left|\frac{p_{k,d}}{T_{m,d}}-1\right|
&\le16^d
\sum_{j=1}^d
\exp\!\bigl(C(j+5)\log(j+5)\bigr)
\left(\frac dk\right)^j\\
&\le
16^d d\,
\exp\!\bigl(C(d+5)\log(d+5)\bigr)\frac dk.         \tag{18}
\end{aligned}
\]
The logarithm of the last expression is
\[
-\log k+O(d\log(d+5)),
\]
which tends to \(-\infty\) under (1).  This proves (2).

Finally, if
\[
d\le\frac{\log k}{(\log\log k)^2},
\]
then
\[
d\log(d+5)
=O\!\left(\frac{\log k}{\log\log k}\right)
=o(\log k),
\]
which proves (3).

## 3. Claim boundary

The result is an all-parameter asymptotic theorem for a growing,
near-logarithmic top window.  Its proof is human and the finite
companion audit checks the exact norm-bookkeeping inequalities and
the downstream \(4\)-Stirling ratios.  It is not a positivity theorem
for the unresolved middle, nor a proof of OPG-1757 for all graphs.
