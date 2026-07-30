# OPG-1757: the top six base-four Newton layers

Date: 2026-07-30

## 0. Result

Keep the normalization
\[
c_k(s)=\frac{(k-2)!}{2}C_k(s)
=\sum_{q=0}^{2k-4}a_{k,q}\binom{s-4}{q},
\qquad k\ge2.
\]
Put
\[
m=2k-4,\qquad
p_{k,d}:=\frac{a_{k,m-d}}{(m-d)!}.
\]
The symbol \(p_{k,d}\) is used only when \(m-d\ge0\).

### Theorem

The top six normalized Newton coefficients are
\[
\boxed{p_{k,0}=1,}                                   \tag{1}
\]
\[
\boxed{p_{k,1}=2(k-2)(k+2),}                        \tag{2}
\]
\[
\boxed{
p_{k,2}
=\frac{k-2}{6}
\left(12k^3+8k^2-71k-171\right),
}                                                     \tag{3}
\]
\[
\boxed{
p_{k,3}
=\frac{(k-3)(k-2)}3
\left(4k^4+4k^3-25k^2-135k-214\right),
}                                                     \tag{4}
\]
\[
\boxed{
\begin{aligned}
p_{k,4}
={}&\frac{(k-4)(k-3)(k-2)}{360}\\
&\times
\left(
240k^5+240k^4-1240k^3-12384k^2
-40481k-55515
\right),
\end{aligned}
}                                                     \tag{5}
\]
\[
\boxed{
\begin{aligned}
p_{k,5}
={}&\frac{(k-4)(k-3)(k-2)}{180}\\
&\times
\left(
48k^7-208k^6-280k^5-2424k^4-333k^3\\
&\hspace{42mm}
+33943k^2+163804k+273030
\right).
\end{aligned}
}                                                     \tag{6}
\]

Consequently every existing coefficient in this six-layer tail is
nonnegative.  More precisely:

- \(p_{k,0}>0\) for \(k\ge2\);
- \(p_{k,1},p_{k,2}>0\) whenever their layers exist;
- \(p_{k,3}>0\) for \(k\ge4\);
- \(p_{4,4}=0\), which lies below the already proved active support,
  while \(p_{k,4}>0\) for \(k\ge5\);
- \(p_{k,5}>0\) for \(k\ge5\).

Thus the top six layers complement the growing positive window at the
bottom of the Newton support.  They do not control the intervening
linear-width middle.

## 1. Exact profile formula

Let \(\Phi_h(x)\), \(h=0,1,2\), be the weighted complete-graph forest
polynomial obtained after contracting a prescribed matching of size
\(h\).  Write
\[
U_{h,j}(s)=[x^j]\Phi_h(x).
\]
The rooted-tree/Lagrange formula proved in the preceding campaign is
\[
U_{0,j}(s)
=(s)_{\underline j}D(s,s-j,j),                      \tag{7}
\]
\[
U_{1,j}(s)
=(s-2)_{\underline j}D(s,s-2-j,j),                  \tag{8}
\]
\[
\begin{aligned}
U_{2,j}(s)
={}&(s-4)_{\underline j}D(s,s-4-j,j)\\
&+4(s-4)_{\underline{j-1}}E(s,s-3-j,j-1),           \tag{9}
\end{aligned}
\]
where
\[
E(s,c,j)=
\sum_{r=0}^{j}
\frac{(-1)^r(c)_{\underline r}s^{j-r}}
{2^r r!(j-r)!},
\qquad
D(s,c,j)=E(s,c,j)-E(s,c,j-1).                       \tag{10}
\]
Every formula here is a finite polynomial identity.

The determinant extraction is
\[
c_k(s)
=\frac{k!}{2k(k-1)}
\sum_{j=0}^{k}
\left(
U_{1,j}(s)U_{1,k-j}(s)
-U_{0,j}(s)U_{2,k-j}(s)
\right).                                             \tag{11}
\]

## 2. A finite-defect coefficient lemma

Normalize the top of each profile by
\[
U_{h,j}(s)
=\frac1{2^j j!}
\sum_{\ell\ge0}R_{\ell,h}(j)s^{2j-\ell},
\qquad R_{0,h}(j)=1.                                \tag{12}
\]

### Lemma 1

For fixed \(\ell\), \(R_{\ell,h}(j)\) is a polynomial in \(j\) of
degree at most \(\ell\).  For \(0\le\ell\le9\), direct extraction
from (7)--(10), followed by (11), gives
\[
\begin{aligned}
c_k(s)={}&s^{2k-4}
+(k-2)s^{2k-5}\\
&+(k-2)(k-21)s^{2k-6}\\
&+\frac{(k-3)(k-2)(2k-109)}2s^{2k-7}\\
&+\frac{(k-3)(k-2)(6k^2-661k+4240)}6s^{2k-8}\\
&+\frac{(k-4)(k-3)(k-2)(3k^2-554k+6961)}3
s^{2k-9}\\
&+O_k(s^{2k-10}).                                    \tag{13}
\end{aligned}
\]

### Proof of the degree assertion

Temporarily ignore acyclicity.  After the prescribed matching of size
\(h\) is fixed, the number of ways to choose the remaining \(j\)
edges is
\(\binom{\binom{s}{2}-h}{j}\).  In its normalization by
\(s^{2j}/(2^j j!)\), the coefficient of \(s^{-\ell}\) has degree at
most \(\ell\) in \(j\): a term which is \(r\) places below the top of
the falling factorial in the edge count loses \(2r\) powers of \(s\)
and has degree at most \(2r\) in \(j\), while choosing \(t\) copies
of the linear term in \(\binom{s}{2}\) loses another \(t\) powers and
has degree at most \(t\), with \(2r+t=\ell\).

It remains to impose acyclicity.  Apply inclusion--exclusion over
cycles in the chosen graph together with the prescribed matching.
A union of selected cycles that uses \(e\) nonprescribed edges and
\(v\) nonfixed vertices has \(v\le e\).  Its leading loss in the
\(s\)-degree is
\[
\delta=2e-v\ge e.
\]
After the normalization in (12), choosing those \(e\) edges
contributes a factor of degree at most \(e\) in \(j\).  If this core
contributes to the layer \(\ell\), the remaining edge-binomial
expansion loses \(\ell-\delta\) powers and has degree at most
\(\ell-\delta\).  Hence the total degree in \(j\) is at most
\[
e+\ell-\delta\le\ell.
\]
Moreover \(e\le\delta\le\ell\), so only finitely many cycle-union
types occur at a fixed layer.  This proves the polynomial assertion.
The same argument covers \(h=1,2\): the marked matching is fixed, and
any cyclic core involving marked endpoints still satisfies
\(v\le e\) when only nonfixed vertices and nonprescribed edges are
counted.

For completeness, (13) can also be checked without this species
description.  Expand the finite products in (7)--(10).  For each
\(\ell\le9\), both the extracted expression and the recorded
\(R_{\ell,h}(j)\) are polynomials of degree at most \(\ell\);
equality at \(j=0,\ldots,\ell\) proves the identity.  The verifier
also checks the redundant points \(j=\ell+1,\ldots,2\ell+2\).
Substitution
in (11) uses
\[
\frac1{2^k j!(k-j)!}
=\frac1{k!}\frac{\binom kj}{2^k}                    \tag{14}
\]
and the exact binomial falling-moment identity
\[
\mathbb E(J)_{\underline r}
=\frac{(k)_{\underline r}}{2^r},
\qquad J\sim{\rm Bin}(k,\tfrac12).                  \tag{15}
\]
Equations (14)--(15) reduce every coefficient to the six displayed
polynomials in (13).  No numerical fit in \(k\) is used.

The companion verifier records all \(R_{\ell,h}\), checks more points
than the degree bound requires, performs the binomial-moment
convolution symbolically, and independently recomputes exact Newton
rows.

## 3. Conversion from powers to the base-four Newton tail

Write
\[
c_k(s)=\sum_{d\ge0}b_{k,d}s^{m-d}.
\]
Equation (13) gives \(b_{k,0},\ldots,b_{k,5}\).
On the other hand,
\[
c_k(s)=\sum_{d\ge0}
p_{k,d}(s-4)_{\underline{m-d}}.                     \tag{16}
\]
The coefficient of \(s^{r-e}\) in
\((s-4)_{\underline r}\) is
\((-1)^e e_e(4,5,\ldots,r+3)\).  Therefore (16) is a
triangular system:
\[
p_{k,d}
=b_{k,d}
-\sum_{e=0}^{d-1}
p_{k,e}
[s^{m-d}](s-4)_{\underline{m-e}}.                  \tag{17}
\]
Newton's identities for the elementary symmetric functions in (17)
give exactly (1)--(6).

The calculation is worth recording because the ordinary power
coefficients in (13) are often negative.  For example,
\((k-2)(k-21)\) changes sign, whereas the corresponding base-four
Newton coefficient (3) is positive.  The positivity is genuinely
adapted to the four marked endpoints; it is not ordinary monomial
coefficient positivity.

## 4. Positivity

Formula (3) is positive from \(k=3\) onward because, with \(k=x+3\),
\[
12k^3+8k^2-71k-171
=12x^3+116x^2+301x+12.
\]
For (4), put \(k=x+4\):
\[
4k^4+4k^3-25k^2-135k-214
=4x^4+68x^3+407x^2+881x+126.
\]
For (5), putting \(k=x+5\) gives
\[
240x^5+6240x^4+63560x^3+305016x^2
+612679x+177480.
\]
Every coefficient in these three shifted polynomials is positive.

For the final bracket in (6), \(k=x+5\) gives
\[
\begin{aligned}
{}&48x^7+1472x^6+18680x^5+122576x^4\\
&\quad+411187x^3+515348x^2-258741x+9000.
\end{aligned}
\]
It is positive at \(x=0\).  For \(x\ge1\),
\[
515348x^2-258741x
=x(515348x-258741)>0,
\]
and all remaining terms are nonnegative.  This proves every stated
sign.

## 5. Scope

This theorem proves six all-\(k\) layers at the top end.  Together with
the bottom theorem it now gives:

- every active depth \(0,\ldots,6\) at the lower end;
- every depth \(r=o(\sqrt k)\) at the lower end, asymptotically; and
- six layers at the upper end.

It still does not prove all coefficients \(a_{k,q}\), the entire
complete-split \(\alpha^2\) layer, or OPG-1757 for arbitrary graphs.
