# OPG-1757: the all-orders subleading ordinary-power symbol

Date: 2026-07-30

## 0. Result

Write
\[
c_k(s)=\sum_{d\ge0}b_{k,d}s^{2k-4-d}.
\]
The leading-symbol theorem gives
\([k^d]b_{k,d}=1\).  The next coefficient also has a closed form.

### Theorem 1

For every \(d\ge1\),
\[
\boxed{
\begin{aligned}
b_{k,d}
={}&k^d
-\frac{
22d^3+147d^2+161d-258
}{36}\,k^{d-1}\\
&+O_d(k^{d-2}).
\end{aligned}
}                                                     \tag{1}
\]
Equivalently,
\[
\boxed{
\sum_{d\ge1}[k^{d-1}]b_{k,d}\,z^d
=-\frac{
z(43z^3-123z^2+90z+12)
}{6(1-z)^4}.
}                                                     \tag{2}
\]

The cubic scale in (1) explains the observed largest positive roots of
the first ordinary-power perturbation polynomials.  The theorem alone
does not bound all lower symbols and therefore does not prove the
conjectural uniform root bound \(O(d^3)\).

## 1. Four profile symbols

For \(h=0,1,2\), write
\[
R_{\ell,h}(j)
=A_\ell j^\ell
+P_{h,\ell}j^{\ell-1}
+Q_{h,\ell}j^{\ell-2}
+S_{h,\ell}j^{\ell-3}
+O_\ell(j^{\ell-4}).                                \tag{3}
\]
Unavailable powers are zero.  Define
\[
\begin{aligned}
A(z)&=\sum_{\ell\ge0}A_\ell z^\ell,\\
P_h(z)&=\sum_{\ell\ge1}P_{h,\ell}z^{\ell-1},\\
Q_h(z)&=\sum_{\ell\ge2}Q_{h,\ell}z^{\ell-2},\\
S_h(z)&=\sum_{\ell\ge3}S_{h,\ell}z^{\ell-3}.
\end{aligned}                                      \tag{4}
\]

### Lemma 2 (profile resummation through three subdegrees)

Put \(w=1-2z\).  Then
\[
A(z)=\sqrt w,                                       \tag{5}
\]
\[
\begin{aligned}
P_0(z)&=-\frac{z(4z^2-3)}{6w^{5/2}},\\
P_1(z)&=-\frac{z(52z^2-48z+9)}{6w^{5/2}},\\
P_2(z)&=-\frac{z(100z^2-96z+21)}{6w^{5/2}},
\end{aligned}                                      \tag{6}
\]
\[
\begin{aligned}
Q_0(z)
&=\frac{z(16z^5-24z^3+153z-144)}{72w^{11/2}},\\
Q_1(z)
&=\frac{z^2(5008z^4-11904z^3+10152z^2-3168z+81)}
{72w^{11/2}},\\
Q_2(z)
&=\frac{z(5392z^5-14592z^4+13416z^3-4032z^2-279z+144)}
{72w^{11/2}},
\end{aligned}                                      \tag{7}
\]
and
\[
\begin{aligned}
S_0(z)
={}&\frac{z}{6480w^{17/2}}
\bigl(
8896z^8-41472z^7+83664z^6-79488z^5\\
&\hspace{26mm}
+11556z^4+116640z^3-183465z^2+3240z+80460
\bigr),\\
S_1(z)
={}&-\frac{z}{6480w^{17/2}}
\bigl(
3596864z^8-13932288z^7+22711536z^6\\
&\hspace{13mm}
-19498752z^5+8751564z^4-2032560z^3\\
&\hspace{40mm}
+884925z^2-502200z+36180
\bigr),\\
S_2(z)
={}&\frac{z}{6480w^{17/2}}
\bigl(
32886976z^8-111992832z^7+157083984z^6\\
&\hspace{13mm}
-116581248z^5+49790916z^4-12121920z^3\\
&\hspace{40mm}
+474255z^2+793800z-126900
\bigr).
\end{aligned}                                      \tag{8}
\]

### Proof

Use the exact finite profiles
\[
\begin{aligned}
U_{0,j}(s)&=(s)_{\underline j}D(s,s-j,j),\\
U_{1,j}(s)&=(s-2)_{\underline j}D(s,s-2-j,j),\\
U_{2,j}(s)&=(s-4)_{\underline j}D(s,s-4-j,j)
+4(s-4)_{\underline{j-1}}E(s,s-3-j,j-1),
\end{aligned}                                      \tag{9}
\]
where
\[
E(s,c,j)=
\sum_{r=0}^j
\frac{(-1)^r(c)_{\underline r}s^{j-r}}
{2^rr!(j-r)!},
\qquad D(s,c,j)=E(s,c,j)-E(s,c,j-1).               \tag{10}
\]
We now give a parameterized all-orders extraction; this avoids
inferring an infinite identity from finitely many losses.  Normalize
by \(2^jj!/s^{2j}\), set \(j=xs\), and put
\[
\Phi_h(s,x):=\frac{2^jj!}{s^{2j}}U_{h,j}(s).
\]
Equation (3) gives the coefficientwise formal identity
\[
\boxed{
\Phi_h(s,x)
=A(x)+\frac{P_h(x)}s+\frac{Q_h(x)}{s^2}
+\frac{S_h(x)}{s^3}+O_{\rm formal}(s^{-4}).
}                                                     \tag{11}
\]
Indeed, a term
\([j^{\ell-r}]R_{\ell,h}(j)s^{-\ell}\), after \(j=xs\),
is exactly
\([j^{\ell-r}]R_{\ell,h}(j)x^{\ell-r}s^{-r}\).
Thus an identity in the symbolic variable \(x\) proves all losses at
once.

For completeness, here is a finite symbolic saddle certificate for
the four coefficients in (11).  Cauchy's formula rewrites the main
term with shift \(a\in\{0,2,4\}\) as
\[
\begin{aligned}
\Phi_a^{\rm main}(s,x)
={}&
\frac{
2^{xs}\Gamma(xs+1)\Gamma(s-a+1)
}{
s^{2xs}\Gamma(s-a-xs+1)
}\\
&\times\frac1{2\pi i}\oint
g_a(y)e^{s\phi_x(y)}\,dy,                           \tag{11a}\\
g_a(y)&:=\frac{1-y}{y}(1-y/2)^{-a},\\
\phi_x(y)&:=y+(1-x)\log(1-y/2)-x\log y.
\end{aligned}
\]
The exceptional term in \(U_{2,j}\) is
\[
\begin{aligned}
\Phi^{\rm ex}(s,x)
={}&
\frac{
4\,2^{xs}\Gamma(xs+1)\Gamma(s-3)
}{
s^{2xs}\Gamma(s-xs-2)
}\\
&\times\frac1{2\pi i}\oint
g_*(y)e^{s\phi_x(y)}\,dy,                           \tag{11b}\\
g_*(y)&:=(1-y/2)^{-3}.
\end{aligned}
\]
These are exact coefficient integrals obtained directly from
(9)--(10).

First take rational \(0<x<1/2\) and let \(s\) run through multiples of
its denominator, so that \(j=xs\) is integral.  In (11a)--(11b) choose
the Cauchy circle \(|y|=2x\).  On \(y=2xe^{i\theta}\), the real part of
the phase has its unique maximum at \(\theta=0\): indeed, apart from
the positive factor \(x\sin\theta\), its derivative on
\(0<\theta<\pi\) is
\[
-2+\frac{1-x}{1-2x\cos\theta+x^2}<0.
\]
Thus the contributing saddle is \(y_0=2x\); the other solution
\(y=1\) of \(\phi_x'(y)=0\) lies outside the circle.  Standard local
steepest-descent deformation at \(2x\) is consequently valid, and its
remainder is uniform when \(x\) ranges over a compact subinterval of
\((0,1/2)\).  The following recurrences write out that saddle
expansion so that every coefficient is auditable.  Put
\[
\phi_r:=\phi_x^{(r)}(2x)
=\frac{(r-1)!}{2^r}
\left(
-(1-x)^{1-r}+(-1)^rx^{1-r}
\right),                                           \tag{11c}
\]
\[
\sigma:=-\phi_2^{-1}.
\]
Define the Gaussian functional
\[
{\cal M}(q^{2m})=(2m-1)!!\,\sigma^m,
\qquad
{\cal M}(q^{2m+1})=0.
\]
Let \(E_0(q)=1\), and, for \(1\le n\le6\), define
\[
\boxed{
nE_n(q)
=\sum_{p=1}^{n}
p\,\frac{\phi_{p+2}}{(p+2)!}\,
q^{p+2}E_{n-p}(q).
}                                                     \tag{11d}
\]
This is exactly the coefficient recurrence for
\[
\exp\!\left(
\sum_{p\ge1}
\frac{\phi_{p+2}}{(p+2)!}q^{p+2}\varepsilon^p
\right).
\]
For an amplitude \(g\), put
\[
B_r(g)
:=
\sum_{m=0}^{2r}
\frac{g^{(m)}(2x)}{m!}
{\cal M}\!\left(q^mE_{2r-m}(q)\right),
\qquad 0\le r\le3.                                 \tag{11e}
\]

The Gamma factors are equally explicit.  For a signed list
\({\cal A}=\{(\epsilon_i,z_i,c_i)\}\), define
\[
\gamma_n({\cal A})
:=
\frac{(-1)^{n+1}}{n(n+1)}
\sum_i
\epsilon_i\frac{B_{n+1}(c_i)}{z_i^n},
\qquad 1\le n\le3,                                \tag{11f}
\]
where \(B_n(c)\) is the Bernoulli polynomial.  Let
\[
\Gamma_0({\cal A})=1,\qquad
r\Gamma_r({\cal A})
=\sum_{n=1}^{r}
n\gamma_n({\cal A})\Gamma_{r-n}({\cal A}).         \tag{11g}
\]
This is the exponential of the correction terms in
\[
\begin{aligned}
\log\Gamma(sz+c)
={}&sz(\log s+\log z-1)
+(c-\tfrac12)(\log s+\log z)\\
&+\tfrac12\log(2\pi)
+\sum_{n=1}^{3}
\frac{(-1)^{n+1}B_{n+1}(c)}
{n(n+1)(sz)^n}
+O(s^{-4}).                                       \tag{11h}
\end{aligned}
\]
Finally set
\[
C_r(g,{\cal A})
:=
\sum_{i=0}^{r}
\Gamma_i({\cal A})
\frac{B_{r-i}(g)}{B_0(g)}.                         \tag{11i}
\]

For the three main profiles use
\[
{\cal A}_a
=\{(1,x,1),(1,1,1-a),(-1,1-x,1-a)\},
\]
and for the exceptional profile use
\[
{\cal A}_*
=\{(1,x,1),(1,1,-3),(-1,1-x,-2)\}.
\]
The saddle and Gamma leading terms cancel exactly, leaving
\[
\boxed{
\Phi_a^{\rm main}(s,x)
=\sqrt{1-2x}
\sum_{r=0}^{3}
C_r(g_a,{\cal A}_a)s^{-r}
+O(s^{-4}),
}                                                     \tag{11j}
\]
and
\[
\boxed{
\Phi^{\rm ex}(s,x)
=\frac{8x}{s\sqrt{1-2x}}
\sum_{r=0}^{2}
C_r(g_*,{\cal A}_*)s^{-r}
+O(s^{-4}).
}                                                     \tag{11k}
\]

To evaluate the finite recurrences (11d)--(11i), no differentiation
of large products is needed.  If
\[
f_0=\frac1{2x}-1,\qquad
f_q=\frac{(-1)^q}{(2x)^{q+1}}\quad(q\ge1),
\]
then
\[
\frac{g_a^{(m)}(2x)}{m!}
=
\sum_{q=0}^{m}
f_q
\frac{(a)_{m-q}}
{(m-q)!\,2^{m-q}}
(1-x)^{-a-m+q},                                   \tag{11l}
\]
while
\[
\frac{g_*^{(m)}(2x)}{m!}
=
\frac{(3)_m}{m!\,2^m}(1-x)^{-3-m}.                \tag{11m}
\]
Substitution of (11c), (11l), and (11m) into the finite recurrences
(11d)--(11i), followed by
\[
\Phi_0=\Phi_0^{\rm main},\quad
\Phi_1=\Phi_2^{\rm main},\quad
\Phi_2=\Phi_4^{\rm main}+\Phi^{\rm ex},
\]
gives exactly (5)--(8).  The companion
`verify_ordinary_subleading_saddle_certificate.py` performs these
twelve rational-function identities in the symbolic variable \(x\);
it contains no finite-loss interpolation.

The asymptotic identities were obtained first for rational
\(0<x<1/2\), a dense set.  Their coefficients are rational functions
of \(x\) and \(\sqrt{1-2x}\), so analytic continuation gives the same
identities throughout \(0<x<1/2\).  Both sides have analytic
continuations to a neighbourhood of \(x=0\); their Taylor expansions
there prove every coefficient in (4).  This completes the all-orders
resummation.
\(\square\)

## 2. Binomial central expansion of the determinant

Let \(J\sim{\rm Bin}(k,\tfrac12)\), put \(x=J/k\), and introduce a
loss marker \(t\).  Equations (3)--(4) give the formal profile
\[
\begin{aligned}
\mathcal F_h(x;t,k)
={}&A(tx)+\frac tkP_h(tx)+\frac{t^2}{k^2}Q_h(tx)\\
&+\frac{t^3}{k^3}S_h(tx)+O_{\rm formal}(k^{-4}).
\end{aligned}                                      \tag{12}
\]
For \(u=tx\), \(v=t(1-x)\), define
\[
\begin{aligned}
G_2(x,t)=t^2\{&
(Q_1(u)-Q_0(u))A(v)
+A(u)(Q_1(v)-Q_2(v))\\
&+P_1(u)P_1(v)-P_0(u)P_2(v)\},                    \tag{13}
\end{aligned}
\]
and
\[
\begin{aligned}
G_3(x,t)=t^3\{&
(S_1(u)-S_0(u))A(v)
+A(u)(S_1(v)-S_2(v))\\
&+P_1(u)Q_1(v)+Q_1(u)P_1(v)\\
&-P_0(u)Q_2(v)-Q_0(u)P_2(v)\}.                    \tag{14}
\end{aligned}
\]
The order-\(k^0\) determinant cancels pointwise.  The order-\(k^{-1}\)
term is antisymmetric under \(x\leftrightarrow1-x\), so its binomial
expectation is exactly zero.  Since
\[
\mathbb E(x-\tfrac12)^2=\frac1{4k},
\]
the next two expected terms are
\[
H_2(t)=G_2(\tfrac12,t),                             \tag{15}
\]
\[
H_3(t)=G_3(\tfrac12,t)
+\frac18\partial_x^2G_2(\tfrac12,t).               \tag{16}
\]
Substitution of (5)--(8) simplifies to
\[
\boxed{
H_2(t)=\frac{2t^4}{1-t},
}                                                     \tag{17}
\]
\[
\boxed{
H_3(t)=
-\frac{t^4(43t^4-129t^3+108t^2-6t+6)}
{3(1-t)^4}.
}                                                     \tag{18}
\]

Let \(N_L(k)\) denote the binomially averaged numerator at total
profile loss \(L\), before division by \(2k(k-1)\).  Equations
(12)--(18) give, coefficientwise,
\[
N_L(k)
=k^{L-2}[t^L]H_2(t)
+k^{L-3}[t^L]H_3(t)
+O_L(k^{L-4}).                                      \tag{19}
\]
For \(L\ge5\),
\[
[t^L]H_2=2,
\qquad
[t^L]H_3
=-\frac{22L^3-117L^2+41L+78}{18}.                 \tag{20}
\]

## 3. Completion of the proof

Put \(L=d+4\).  Since
\[
\frac1{2k(k-1)}
=\frac1{2k^2}\left(1+\frac1k+O(k^{-2})\right),
\]
equations (19)--(20) give
\[
\begin{aligned}
[k^{d-1}]b_{k,d}
&=1+\frac12[t^{d+4}]H_3(t)\\
&=-\frac{22d^3+147d^2+161d-258}{36}.
\end{aligned}
\]
This proves (1).  Summing the standard series for
\(\sum d^rz^d\), \(0\le r\le3\), gives (2).
\(\square\)

## 4. Consequence and open strengthening

The first nine exact polynomials have largest real root of cubic scale,
consistent with (1).  A useful next theorem would be the weighted
symbol bound
\[
|[k^{d-r}]b_{k,d}|
\le\binom dr(Cd^2)^r.
\]
It would imply \(b_{k,d}>0\) for \(k>C'd^3\), and because every
\(4\)-Stirling coefficient is positive, would yield an explicit
top window \(d\ll k^{1/3}\).  The present theorem proves the \(r=1\)
case exactly but does not establish the all-\(r\) inequality.
