# OPG-1757: an all-orders diagonal component theorem

Date: 2026-07-30

## 0. Status and purpose

This note proves an exact all-orders structural statement for the
component determinant underlying the base-four Newton coefficients.  It
is stronger than computing any fixed active layer:

> the coefficient of \(n^{-d}\), after convolution at total component
> excess \(R\), is a polynomial in \(R\) of degree at most \(d-1\), and
> its leading coefficient is positive and explicit for every \(d\ge2\).

The theorem explains and resums the two previously proved fixed-\(t\)
terms.  It does **not** by itself give a uniform error bound when
\(R=R(n)\), so it is not yet a proof of all Newton coefficients or even
of a numerical range \(R\le c n\).  That remaining analytic step is
stated precisely in Section 7.

## 1. Exact normalized component series

Put
\[
g_r=\frac1{2^r r!},\qquad u=\frac1n,\qquad c=r+1.
\]
For the ordinary forest count \(W_{0,c}\), the adjacent-pair count
\(A_c\), and the one- and two-forced-edge counts \(W_{1,c},W_{2,c}\),
define normalized formal series by
\[
\frac{W_{0,r+1}}{n^{n-2}}=g_rF_{0,r}(u),\qquad
\frac{A_{r+1}}{n^{n-4}}=g_rF_{A,r}(u),
\]
\[
\frac{W_{1,r+1}}{n^{n-3}}=g_rF_{1,r}(u),\qquad
\frac{W_{2,r+1}}{n^{n-4}}=g_rF_{2,r}(u).
\]
The finite Liu--Chow formulas give the exact product expressions
\[
F_{0,r}(u)=\frac1{g_r}\sum_{j=0}^{r}
\frac{(-1)^j(r+1+j)}{2^j j!(r-j)!}
\prod_{h=1}^{r+j}(1-hu),                            \tag{1}
\]
\[
F_{A,r}(u)=\frac1{g_r}\sum_{j=0}^{r}
\frac{(-1)^j(r+3+j)}{2^j j!(r-j)!}
\prod_{h=3}^{r+j+2}(1-hu).                          \tag{2}
\]
The two edge-orbit identities become
\[
F_{1,r}
=2\left(1-\frac{ru}{1-u}\right)F_{0,r},             \tag{3}
\]
\[
\begin{aligned}
F_{2,r}={}&
4\frac{(1-(r+1)u)(1-(r+2)u)}
{(1-u)(1-2u)(1-3u)}F_{0,r}\\
&-\frac{4u}{1-3u}F_{A,r}.                           \tag{4}
\end{aligned}
\]
Equations (1)--(4) are identities, not asymptotic approximations.

## 2. Exact binomial representation of the determinant

Let
\[
\mathcal C_{R+2}(n)
=\sum_{r=0}^{R}
\left(
W_{1,r+1}W_{1,R-r+1}
-W_{0,r+1}W_{2,R-r+1}
\right).
\]
Since
\[
R!g_rg_{R-r}=2^{-R}\binom Rr,
\]
we have, in the stable range \(n\ge R+4\),
\[
\boxed{
\Delta_R(u):=
\frac{R!\,\mathcal C_{R+2}(n)}{n^{2n-6}}
=\mathbb E\!\left[
F_{1,X}(u)F_{1,R-X}(u)
-F_{0,X}(u)F_{2,R-X}(u)
\right],
}                                                     \tag{5}
\]
where \(X\sim{\rm Bin}(R,\tfrac12)\).  Formula (5) is an
ordinary finite binomial average; no probabilistic approximation is
being used.

Write
\[
\Delta_R(u)=\sum_{d\ge0}P_d(R)u^d.                  \tag{6}
\]

## 3. The all-orders theorem

### Theorem

The first two polynomials vanish:
\[
P_0(R)=P_1(R)=0.
\]
For every \(d\ge2\), \(P_d(R)\) is a polynomial in \(R\) of degree
exactly \(d-1\), with
\[
\boxed{
[R^{d-1}]P_d(R)=\frac23d(d^2-1)>0.
}                                                     \tag{7}
\]
Equivalently, the complete generating function of the highest-degree
terms is
\[
\boxed{
\sum_{d\ge2}[R^{d-1}]P_d(R)\,\alpha^d
=\frac{4\alpha^2}{(1-\alpha)^4}.
}                                                     \tag{8}
\]

The first exact polynomials are
\[
\begin{aligned}
P_2(R)&=4R,\\
P_3(R)&=16R(R-1),\\
P_4(R)&=8R(R-1)(5R-22),\\
P_5(R)&=10R(R-1)(R-2)(8R-85),\\
P_6(R)&=\frac{10}{3}R(R-1)(R-2)
\bigl(42R^2-977R+3093\bigr).
\end{aligned}                                        \tag{9}
\]

Consequently the fixed-\(R\) determinant begins
\[
\Delta_R(1/n)
=\frac{4R}{n^2}
+\frac{16R(R-1)}{n^3}
+O_R(n^{-4}),                                        \tag{10}
\]
which is exactly
\[
\mathcal C_t(n)
=\frac4{(t-3)!}n^{2n-8}
+\frac{16}{(t-4)!}n^{2n-9}
+O_t(n^{2n-10})
\]
after \(t=R+2\) is restored.

## 4. Heat-operator proof of the degree bound

Introduce a formal Gaussian functional by
\[
\mathbb E_z e^{sY}=\exp\left(zs-\frac z2s^2\right). \tag{11}
\]
Expanding the finite products in (1)--(2), or equivalently applying
the heat operator
\(\exp(zwD-\tfrac z2w^2D^2)\), gives
\[
\sum_{r\ge0}g_rF_{0,r}(u)z^r
=\mathbb E_z\!\left[
(1+Y)(1+uY)^{1/u-2}
\right],                                             \tag{12}
\]
\[
\sum_{r\ge0}g_rF_{A,r}(u)z^r
=\mathbb E_z\!\left[
(3+Y)(1+uY)^{1/u-4}
\right].                                             \tag{13}
\]
These are formal power-series identities, so the apparent exponent
\(1/u\) is interpreted through
\[
(1+uY)^{1/u-a}
=e^Y\exp\left(
-u\left(aY+\frac{Y^2}{2}\right)
+u^2\left(\frac{aY^2}{2}+\frac{Y^3}{3}\right)
-u^3\left(\frac{aY^3}{3}+\frac{Y^4}{4}\right)
+\cdots
\right).                                             \tag{14}
\]

After tilting (11) by \(e^Y\),
\[
\frac{\mathbb E_z(e^Ye^{sY})}{e^{z/2}}
=e^{-zs^2/2}.                                        \tag{15}
\]
Thus odd tilted moments vanish and
\[
\mathbb E_z(e^YY^{2m})
=e^{z/2}(-1)^m(2m-1)!!\,z^m.                        \tag{16}
\]
The coefficient of \(u^d\) in (14) has \(Y\)-degree at most \(2d\).
Equations (12)--(16) therefore show that
\([u^d]F_{i,r}(u)\) is a polynomial in \(r\) of degree at most \(d\)
for \(i=0,A,1,2\).  Applying the binomial moments in (5) first gives
\(\deg P_d\le d\).

The degree-\(d\) part cancels.  The next section computes that
cancellation and the surviving degree-\((d-1)\) part simultaneously.

## 5. Leading and subleading component symbols

For \(i=0,1,2\), write
\[
[u^d]F_{i,r}(u)=\ell_{i,d}r^d+m_{i,d}r^{d-1}
+O_d(r^{d-2}).
\]
The centered Wick rule (16), followed by summation of the binomial
series, gives
\[
L_0(x):=\sum_{d\ge0}\ell_{0,d}x^d
=(1-2x)^{-5/2},                                      \tag{17}
\]
\[
L_1(x)=2(1-x)(1-2x)^{-5/2},\qquad
L_2(x)=4(1-x)^2(1-2x)^{-5/2}.                        \tag{18}
\]
The next symbols are
\[
M_0(x)=
\frac{x^2(-47/2+24x-2x^2/3)}{(1-2x)^{11/2}},         \tag{19}
\]
\[
M_1(x)=
\frac{x^2(-49+107x-220x^2/3+52x^3/3)}
{(1-2x)^{11/2}},                                     \tag{20}
\]
\[
M_2(x)=
\frac{x^2(-114+428x-2018x^2/3+1648x^3/3-584x^4/3)}
{(1-2x)^{11/2}}.                                     \tag{21}
\]
Here \(M_i(x)=\sum_{d\ge0}m_{i,d}x^d\).
Equations (17)--(21) follow by retaining respectively the highest and
next-highest powers of \(z\) in (12)--(16); (3)--(4) then give the
one- and two-edge formulas.  This is a finite algebraic extraction at
each coefficient, while the rational functions simply resum it.

## 6. Extraction of the universal leading coefficient

Put \(X=R/2+Z\), so
\[
\mathbb EZ=0,\qquad \mathbb EZ^2=R/4.
\]
To extract the degree-\((d-1)\) terms of all \(P_d\) at once, substitute
\(u=\alpha/R\) into (5) and retain order \(R^{-1}\).

The degree-\(d\) contribution vanishes because at the binomial centre
\[
L_1(\alpha/2)^2
=L_0(\alpha/2)L_2(\alpha/2).                         \tag{22}
\]
There are two order-\(R^{-1}\) contributions.

First, (19)--(21) give
\[
4M_1L_1-2(M_0L_2+L_0M_2)
=\frac{2\alpha^2(2\alpha-3)}{(\alpha-1)^5},          \tag{23}
\]
where every function on the left is evaluated at \(\alpha/2\).

Second, the binomial variance applied to
\[
h(v)=L_1(\alpha/2+v)L_1(\alpha/2-v)
-L_0(\alpha/2+v)L_2(\alpha/2-v)
\]
contributes
\[
\frac{\alpha^2}{8}h''(0)
=\frac{2\alpha^2}{(\alpha-1)^5}.                    \tag{24}
\]
Adding (23) and (24) yields
\[
\lim_{R\to\infty}^{\rm coefficientwise}
R\Delta_R(\alpha/R)
=\frac{4\alpha^2}{(1-\alpha)^4}.                    \tag{25}
\]
Because this is a coefficientwise identity between polynomials in
\(R\), (25) proves both \(\deg P_d\le d-1\) and (7):
\[
4[\alpha^{d-2}](1-\alpha)^{-4}
=4\binom{d+1}{3}
=\frac23d(d^2-1).
\]
The quantity is nonzero for \(d\ge2\), so the degree is exactly
\(d-1\).

## 7. The remaining uniform-positivity lemma

Theorem (7) is an exact statement for every order \(d\), but a
coefficientwise diagonal limit is not automatically a numerical
asymptotic when \(R\) itself grows with \(n\).  A sufficient next lemma
would be the following.

> **Uniform remainder target.**  Find absolute \(c,C>0\) such that for
> \(0\le R\le cn\),
> \[
> \left|
> \Delta_R(1/n)
> -\frac{4R/n^2}{(1-R/n)^4}
> \right|
> \le C\frac{R}{n^2}\,\varepsilon_{n,R},
> \qquad \varepsilon_{n,R}<1.
> \]

Even a version only for \(R=o(n^\eta)\), with an explicit
\(\eta>0\), would upgrade fixed-depth positivity to a genuinely growing
Newton window.  Proving such a bound requires uniform control of the
lower-degree parts of \(P_d\), not additional fixed-layer
factorizations.

## 8. Verification

`verify_diagonal_component_theorem.py` independently reconstructs
(1)--(4), checks the component degree bounds and the rational leading
and subleading symbols through order ten, and verifies (7) and the
exact polynomials (9) through order seven.  These finite checks audit
the algebra; the all-\(d\) statement rests on the heat-operator/Wick
proof above.
