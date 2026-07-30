# OPG-1757: a growing positive window at the top of every Newton row

Date: 2026-07-30

## 0. Result

Keep
\[
c_k(s)=\sum_{q=0}^{2k-4}a_{k,q}\binom{s-4}{q},
\qquad
m=2k-4,
\qquad
p_{k,d}=\frac{a_{k,m-d}}{(m-d)!}.
\]

### Theorem 1

Let \(d=d(k)\) be a nonnegative integer satisfying
\[
(d+5)^2\log(d+5)=o(\log k).                         \tag{1}
\]
Then
\[
\boxed{p_{k,d}>0}
\]
for all sufficiently large \(k\).  More precisely, if
\[
T_{n,r}:=[(s-4)_{\underline{n-r}}]\,s^n
\]
denotes the indicated base-four falling-factorial coefficient, then
\[
\boxed{p_{k,d}=T_{m,d}\bigl(1+o(1)\bigr)}           \tag{2}
\]
uniformly under (1).

In particular,
\[
\boxed{
a_{k,\,2k-4-d}>0
\quad\text{for every}\quad
0\le d\le(\log k)^{1/3}
}
                                                            \tag{3}
\]
once \(k\) is sufficiently large.

Thus the top positive region is genuinely unbounded.  The exponent
\(1/3\) is not optimized; it is a clean consequence of deliberately
coarse coefficient-norm estimates.  This theorem still leaves a
linear-width middle and therefore is not a proof of all Newton
coefficients.

## 1. Uniform coefficient bound for the ordinary power tail

Write
\[
c_k(s)=\sum_{j\ge0}b_{k,j}s^{m-j}.                  \tag{4}
\]
The fixed-top-depth theorem proved, for each fixed \(j\),
\(b_{k,j}=O_j(k^j)\).  We need a version that records how the hidden
constant grows with \(j\).

### Lemma 2 (effective marked finite-loss bound)

There is an absolute constant \(C>0\) such that, whenever
\(k\ge2(j+5)\),
\[
\boxed{
|b_{k,j}|
\le
\exp\!\left(
C(j+5)^2\log(j+5)
\right)k^j.
}                                                     \tag{5}
\]
More precisely, the profile symbols in (6) satisfy
\[
\boxed{
\deg_r[h^v]R_{\ell,h}(r)\le\ell-v,\qquad
\|R_{\ell,h}\|_1
\le
\exp\!\left(C(\ell+1)^2\log(\ell+2)\right)
}                                                     \tag{5a}
\]
for \(h=0,1,2\).  In the norm bound, \(h\) is specialized to one of
these three values and \(\|\cdot\|_1\) is the coefficient norm in
\(r\).  In the degree statement, \([h^v]\) refers to the general
prescribed-matching profile with symbolic matching size \(h\); the
three specializations used by the determinant are \(h=0,1,2\).

### Proof

We give the complete coefficient bookkeeping because only a uniform
bound in \(\ell\), not an optimized constant, can justify a growing
window.

For \(h=0,1,2\), normalize the forest profiles as
\[
U_{h,r}(s)
=\frac1{2^r r!}
\sum_{\ell\ge0}R_{\ell,h}(r)s^{2r-\ell}.            \tag{6}
\]
The exact rooted-tree/Lagrange formulas express every \(U_{h,r}\) as
a sum of at most two terms built from
\[
(s-\alpha)_{\underline r},\qquad
E(s,s-\beta-r,r):=
\sum_{t=0}^{r}
\frac{(-1)^t(s-\beta-r)_{\underline t}s^{r-t}}
     {2^t t!(r-t)!},                                \tag{7}
\]
and the difference of two consecutive copies of the second
expression.  Here \(\alpha,\beta\in\{0,2,3,4\}\).

We first record the bivariate estimate that is needed when both the
length and the initial point of a falling product vary.  For
\(0\le\beta\le5\), put
\[
P_{\beta,u}(t,r)
:=[s^{t-u}](s-\beta-r)_{\underline t}.
\]
Then
\[
\deg_{t,r}P_{\beta,u}\le2u,\qquad
\|P_{\beta,u}\|_{\mathbb Q[t,r],1}
\le
\exp\!\bigl(C_0(u+1)^2\log(u+2)\bigr).              \tag{8}
\]
Indeed,
\[
P_{\beta,u}(t,r)
=(-1)^u e_u(\beta+r,\ldots,\beta+r+t-1).
\]
Newton's identities express this in the power sums
\(\sum_{a=0}^{t-1}(\beta+r+a)^v\), \(v\le u\).
The binomial theorem, Faulhaber's formula, and the standard bound
\(|B_m|\le4m!/(2\pi)^m\) give coefficient norm
\(\exp(O(u\log(u+2)))\) for each power sum.  The partition expansion
in Newton's identities has at most \(\exp(O(u\log(u+2)))\) terms.
Their products are absorbed by the deliberately larger right side of
(8).  The same estimate covers
\([s^{r-u}](s-\alpha)_{\underline r}\).

For the finite sum in (7), multiply by \(2^r r!/s^r\) and use the
falling-factorial moment identity
\[
\sum_{t=0}^{r}
\binom rt2^{r-t}(-1)^t(t)_{\underline v}
=(-1)^v(r)_{\underline v}.                         \tag{9}
\]
At loss \(u\), (8) is a polynomial in \(t,r\) of degree at most
\(2u\).  Convert the \(t\)-powers to falling factorials, apply (9),
and convert the resulting falling powers of \(r\) back to ordinary
powers.  Both changes use Stirling numbers of order at most \(2u\),
each bounded by \((2u)^{2u}\).  Hence the normalized \(E\)-profile at
loss \(u\) has coefficient norm bounded by the right side of (8)
after increasing \(C_0\).

The consecutive difference has the exact normalized form
\[
\widehat D_{\beta,r}(s)
=\widehat E_{\beta,r}(s)
-\frac{2r}{s}\widehat E_{\beta+1,r-1}(s),
\qquad
\widehat E_{\beta,r}(s):=\frac{2^r r!}{s^r}
E(s,s-\beta-r,r).                                  \tag{9a}
\]
The shift \(\beta\mapsto\beta+1\) is necessary because the second
copy has degree \(r-1\) but retains the same component parameter.
Thus the difference introduces only one factor \(2r\), one bounded
shift of \(\beta\), and one unit of loss.
The exceptional term in the \(h=2\) profile has the exact normalized
form
\[
\frac{2^r r!}{s^{2r}}\,
4(s-4)_{\underline{r-1}}
E(s,s-3-r,r-1)
=\frac{8r}{s^2}\,
\widehat F_{4,r-1}(s)\widehat E_{4,r-1}(s),         \tag{9b}
\]
where
\(\widehat F_{4,r-1}=s^{-(r-1)}(s-4)_{\underline{r-1}}\);
both hatted factors are of the type already bounded.  The exceptional
term begins at loss two, as required.

Finally convolve the outer falling product with (9a), and include
(9b).  At total loss \(\ell\), there are at most \(O(\ell^2)\)
truncated convolution terms.  Products and sums of the bounds (8),
including the factors \(2r\) and \(8r\), give
\[
\|R_{\ell,h}\|_1
\le
\exp\!\bigl(C_1(\ell+1)^2\log(\ell+2)\bigr),         \tag{10}
\]
with one absolute \(C_1\) for all three profiles.

The stronger degree part of (5a) follows from the marked
cycle-inclusion--exclusion lemma: a core touching \(v\) prescribed
matching pairs spends at least \(v\) units of its loss on those
marks.  Equivalently,
\[
\deg_r\!\left(R_{\ell,1}-R_{\ell,0}\right)\le\ell-1,
\qquad
\deg_r\!\left(R_{\ell,2}-2R_{\ell,1}+R_{\ell,0}\right)
\le\ell-2.                                         \tag{10a}
\]
Finite differences multiply the coefficient norm in (10) by at most
four.  This proves the full effective marked bound (5a).

The coefficient \(b_{k,j}\) is the total profile-loss \(L=j+4\)
term in
\[
\frac1{2k(k-1)}
\mathbb E\!\left[
\sum_{\ell=0}^{L}
\bigl(
R_{\ell,1}(J)R_{L-\ell,1}(k-J)
-R_{\ell,0}(J)R_{L-\ell,2}(k-J)
\bigr)
\right],                                             \tag{11}
\]
where \(J\sim{\rm Bin}(k,\tfrac12)\).
Power-to-falling conversion followed by the mixed moment identity
\[
\mathbb E\!\left[
(J)_{\underline a}(k-J)_{\underline b}
\right]
=\frac{(k)_{\underline{a+b}}}{2^{a+b}}              \tag{12}
\]
multiplies the coefficient norm in (10) by at most another
\(\exp(C_2L^2\log(L+2))\).

For clarity, write modulo \(r\)-degree at most \(\ell-2\)
\[
R_{\ell,h}(r)
=A_\ell(r)+C_\ell(r)+hB_\ell(r)
+O_{\deg_r}(\ell-2),                                \tag{12a}
\]
where \(A_\ell\) has degree \(\ell\), while \(C_\ell,B_\ell\)
have degree at most \(\ell-1\), and \(A_\ell,C_\ell\) are
independent of \(h\).  The degree-\(L\) part of the numerator in
(11) is \(A_\ell A_{L-\ell}-A_\ell A_{L-\ell}\) and cancels
pointwise.  The independent \(C\)-terms at degree \(L-1\) also cancel
pointwise.  The remaining degree-\((L-1)\) kernel is
\[
\sum_{\ell=0}^{L}
\left(
B_\ell(J)A_{L-\ell}(k-J)
-A_\ell(J)B_{L-\ell}(k-J)
\right).                                             \tag{12b}
\]
It is antisymmetric under
\[
J\longleftrightarrow k-J,\qquad
\ell\longleftrightarrow L-\ell,
\]
and hence has binomial expectation zero.  The remaining numerator has degree
at most \(L-2=j+2\) in \(k\), with coefficient norm at most
\(\exp(C_3L^2\log(L+2))\).  Dividing by \(2k(k-1)\), and enlarging
the absolute constant to cover \(k\ge2(j+5)\), proves (5).
\(\square\)

The intentionally generous square in the exponent absorbs all basis
conversions, truncation convolutions, and the two exceptional
profiles.  No constant in Lemma 2 depends on \(j\) or \(k\).

## 2. Positive comparison coefficients

Put \(x=s-4\).  The identity
\[
(x+4)^n
=\sum_{q=0}^{n}
{n\brace q}_{4}(x)_{\underline q}                  \tag{13}
\]
defines the \(4\)-Stirling numbers of the second kind.  Hence
\[
T_{n,r}={n\brace n-r}_{4}>0.                        \tag{14}
\]
Combinatorially, this counts partitions of \(n+4\) elements into
\(n-r+4\) blocks in which four distinguished elements lie in
different blocks.

### Lemma 3 (two crude Stirling bounds)

If \(n\ge4r\), then
\[
\boxed{
\frac{n^{2r}}{8^r r!}
\le T_{n,r}
\le\frac{(n+4)^{2r}}{2^r r!}.
}                                                     \tag{15}
\]

### Proof

For the lower bound, pair \(2r\) of the \(n\) ordinary elements into
\(r\) disjoint pairs and leave every other element singleton.  These
are admissible \(4\)-Stirling partitions, so
\[
T_{n,r}\ge\frac{(n)_{\underline{2r}}}{2^r r!}
\ge\frac{n^{2r}}{8^r r!},
\]
where \(n\ge4r\) gives
\((n)_{\underline{2r}}\ge(n/2)^{2r}\).

For the upper bound, forget the restriction on the four distinguished
elements.  Canonically join every nonsingleton block to its smallest
element.  A partition with block deficit \(r\) is thereby injected
into an \(r\)-edge graph on \(n+4\) vertices.  Thus
\[
T_{n,r}
\le\binom{\binom{n+4}{2}}r
\le\frac{(n+4)^{2r}}{2^r r!}.
\]
\(\square\)

## 3. Dominance of the monic term

Linearity of (13) gives the exact identity
\[
\boxed{
p_{k,d}
=\sum_{j=0}^{d}b_{k,j}T_{m-j,d-j}.
}                                                     \tag{16}
\]
The term \(j=0\) is \(T_{m,d}\), because \(b_{k,0}=1\).

Assume \(m\ge4d\), which follows from (1) for large \(k\).  Lemma 3,
\(m\ge k\), and \(m-j+4\le2k\) give, for \(1\le j\le d\),
\[
\frac{T_{m-j,d-j}}{T_{m,d}}
\le
16^d\,\frac{(d)_{\underline j}}{k^{2j}}
\le
16^d\left(\frac d{k^2}\right)^j.                   \tag{17}
\]
Combining (5), (16), and (17), and increasing \(C\) once, yields
\[
\begin{aligned}
\left|\frac{p_{k,d}}{T_{m,d}}-1\right|
&\le
16^d\sum_{j=1}^{d}
\exp\!\left(C(j+5)^2\log(j+5)\right)
\left(\frac d k\right)^j\\
&\le
16^d d\,
\exp\!\left(C(d+5)^2\log(d+5)\right)\frac d k.
\end{aligned}                                       \tag{18}
\]
Under (1), the logarithm of the last expression tends to
\(-\infty\).  Therefore the relative error in (2) is \(o(1)\), and
the positivity of \(T_{m,d}\) proves Theorem 1.

Finally, \(d\le(\log k)^{1/3}\) implies
\[
(d+5)^2\log(d+5)
=O\!\left((\log k)^{2/3}\log\log k\right)
=o(\log k),
\]
which proves (3).

## 4. Scope

Together with the lower-support theorem, the proved positive regimes
are now
\[
\begin{array}{c|c}
\text{location in the Newton row}&\text{proved positive window}\\ \hline
\text{first active coefficient}&r=o(\sqrt{k})\\
\text{highest coefficient}&d\le(\log k)^{1/3}
\end{array}
\]
The top exponent can be improved by tightening Lemma 2, but no
sublinear estimate of this kind reaches the unresolved middle.
