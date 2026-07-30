# OPG-1757: an all-fixed-rank ordinary-symbol algorithm

Date: 2026-07-30

## 0. Result

Write
\[
c_k(s)=\sum_{d\ge0}b_{k,d}s^{2k-4-d},
\qquad
b_{k,d}=\sum_{r=0}^{d}\beta_{d,r}k^{d-r}.
\tag{1}
\]
The preceding leading, first-subleading, and second-subleading
theorems give \(\beta_{d,0},\beta_{d,1},\beta_{d,2}\) explicitly.
They are instances of one finite algorithm at every fixed rank.

### Theorem 1 (all-fixed-rank symbol algorithm)

For every fixed \(R\ge0\), there is a finite symbolic recurrence,
starting directly from the exact Lagrange profiles, which computes
generating functions
\[
\boxed{
B_r(t):=\sum_{d\ge r}\beta_{d,r}t^d
\qquad(0\le r\le R).
}
\tag{2}
\]
The recurrence:

1. performs no interpolation in the loss or depth;
2. uses phase derivatives only through order \(2R+6\);
3. uses Bernoulli polynomials only through index \(R+3\); and
4. proves all depths \(d\ge r\) simultaneously.

More precisely, if \(H_n(t)\) is defined by the profile and central
binomial recurrences below, then
\[
\boxed{
B_r(t)
=\frac1{2t^4}\sum_{n=2}^{r+2}H_n(t).
}
\tag{3}
\]
For \(r=0,1,2\), formula (3) reproduces the three proved symbols.

The theorem is an algorithm at each fixed rank; it is not a uniform
bound as \(R\to\infty\).  In particular, it does not prove the open
weighted full-symbol estimate needed for a \(k^{1/3}\) top window.

## 1. Profiles to arbitrary fixed inverse-\(s\) rank

For \(h=0,1,2\), retain the exact profiles
\[
\begin{aligned}
U_{0,j}(s)&=(s)_{\underline j}D(s,s-j,j),\\
U_{1,j}(s)&=(s-2)_{\underline j}D(s,s-2-j,j),\\
U_{2,j}(s)&=(s-4)_{\underline j}D(s,s-4-j,j)
+4(s-4)_{\underline{j-1}}E(s,s-3-j,j-1),
\end{aligned}
\tag{4}
\]
and normalize, with \(j=xs\),
\[
\Phi_h(s,x)=\frac{2^jj!}{s^{2j}}U_{h,j}(s).
\tag{5}
\]

### Lemma 2 (fixed-rank profile recurrence)

For every fixed \(M\ge0\),
\[
\boxed{
\Phi_h(s,x)
=\sum_{r=0}^{M}F_{h,r}(x)s^{-r}
+O_{\rm formal}(s^{-M-1}),
}
\tag{6}
\]
where all \(F_{h,r}(x)\) are computed by the following finite
recurrences.

Put
\[
\phi_x(y)
=y+(1-x)\log(1-y/2)-x\log y,
\qquad y_0=2x,
\tag{7}
\]
\[
\phi_q
=\phi_x^{(q)}(2x)
=\frac{(q-1)!}{2^q}
\left(-(1-x)^{1-q}+(-1)^qx^{1-q}\right),
\tag{8}
\]
and \(\sigma=-\phi_2^{-1}\).  Define
\[
{\cal M}(z^{2a})=(2a-1)!!\,\sigma^a,
\qquad {\cal M}(z^{2a+1})=0.
\tag{9}
\]
Let \(E_0(z)=1\), and for \(n\ge1\) set
\[
\boxed{
nE_n(z)
=\sum_{p=1}^{n}
p\,\frac{\phi_{p+2}}{(p+2)!}
z^{p+2}E_{n-p}(z).
}
\tag{10}
\]
For an amplitude \(g\), put
\[
I_r(g)
=\sum_{m=0}^{2r}
\frac{g^{(m)}(2x)}{m!}
{\cal M}\!\left(z^mE_{2r-m}(z)\right).
\tag{11}
\]

For a signed Gamma list
\({\cal A}=\{(\epsilon_i,z_i,c_i)\}\), define
\[
\gamma_n({\cal A})
=
\frac{(-1)^{n+1}}{n(n+1)}
\sum_i\epsilon_i\frac{B_{n+1}(c_i)}{z_i^n},
\tag{12}
\]
\[
\Gamma_0({\cal A})=1,\qquad
r\Gamma_r({\cal A})
=\sum_{n=1}^{r}
n\gamma_n({\cal A})\Gamma_{r-n}({\cal A}),
\tag{13}
\]
and
\[
C_r(g,{\cal A})
=\sum_{a=0}^{r}
\Gamma_a({\cal A})\frac{I_{r-a}(g)}{I_0(g)}.
\tag{14}
\]

For \(a\in\{0,2,4\}\), use
\[
g_a(y)=\frac{1-y}{y}(1-y/2)^{-a},
\qquad
{\cal A}_a
=\{(1,x,1),(1,1,1-a),(-1,1-x,1-a)\}.
\tag{15}
\]
For the exceptional term use
\[
g_*(y)=(1-y/2)^{-3},
\qquad
{\cal A}_*
=\{(1,x,1),(1,1,-3),(-1,1-x,-2)\}.
\tag{16}
\]
Then
\[
\begin{aligned}
F_{0,r}&=\sqrt{1-2x}\,C_r(g_0,{\cal A}_0),\\
F_{1,r}&=\sqrt{1-2x}\,C_r(g_2,{\cal A}_2),\\
F_{2,0}&=\sqrt{1-2x},\\
F_{2,r}&=\sqrt{1-2x}\,C_r(g_4,{\cal A}_4)
+\frac{8x}{\sqrt{1-2x}}C_{r-1}(g_*,{\cal A}_*)
\quad(r\ge1).
\end{aligned}
\tag{17}
\]

### Proof

Cauchy's formula applied to (4) gives the exact main and exceptional
integrals displayed in
`ORDINARY_SUBLEADING_SYMBOL_THEOREM.md`.  On the circle
\(|y|=2x\), for rational \(0<x<1/2\), the unique contributing saddle
is \(y=2x\); the stationary point \(y=1\) lies outside.  Expanding the
phase with \(s^{-1/2}\) as local parameter gives (10), and Gaussian
integration gives (11).  Stirling's expansion for each Gamma factor
gives (12), while exponentiating its logarithm gives (13).  Their
product is (14).

To compute through \(s^{-M}\), the main profiles need
\(E_0,\ldots,E_{2M}\), hence phase derivatives through \(2M+2\),
and Gamma corrections through \(M\).  The exceptional profile has an
external factor \(s^{-1}\), producing the shift \(C_{r-1}\) in (17).
Thus every requested rank uses finitely many operations.

The local saddle remainder is uniform on compact subsets of
\(0<x<1/2\).  The resulting coefficients are algebraic-rational
functions of \(x\); analytic continuation to a neighbourhood of
\(x=0\) identifies their Taylor coefficients.  Since the coefficient
of \(x^{\ell-r}\) in \(F_{h,r}\) is exactly the subdegree
\([j^{\ell-r}]R_{\ell,h}(j)\), equation (6) proves all losses at once.
\(\square\)

## 2. Determinant ranks

Introduce a loss marker \(t\) and put
\[
{\cal F}_h(x;t,k)
=\sum_{r\ge0}\frac{t^r}{k^r}F_{h,r}(tx).
\tag{18}
\]
Define the rank-\(n\) determinant kernel by the finite convolution
\[
\boxed{
G_n(x,t)
=t^n\sum_{a+b=n}
\left(
F_{1,a}(tx)F_{1,b}(t(1-x))
-F_{0,a}(tx)F_{2,b}(t(1-x))
\right).
}
\tag{19}
\]
Here \(F_{h,0}(z)=\sqrt{1-2z}\).  Directly,
\[
G_0=0,
\qquad
G_1(1-x,t)=-G_1(x,t).
\tag{20}
\]
The second identity and the exact symmetry of
\({\rm Bin}(k,\tfrac12)\) imply that the entire expectation of \(G_1\)
vanishes, not merely its first few Taylor terms.

## 3. Central-binomial recurrence

Let
\[
J\sim{\rm Bin}(k,\tfrac12),
\qquad
\delta=J/k-\tfrac12.
\]
For even \(m\), define the exact rational constants
\[
\mu_{m,q}:=[k^{-q}]\mathbb E\delta^m,
\tag{21}
\]
and put \(\mu_{0,0}=1\).  Odd central moments vanish.  The binomial
moments, and hence every \(\mu_{m,q}\), are computed explicitly by
\[
\boxed{
\mathbb E\delta^m
=
\frac1{k^m}
\sum_{u=0}^{m}
\binom mu\left(-\frac k2\right)^{m-u}
\sum_{v=0}^{u}
{u\brace v}\frac{(k)_{\underline v}}{2^v}.
}
\tag{21a}
\]
This follows from
\(\mathbb E J^u=\sum_v{u\brace v}(k)_{\underline v}/2^v\)
and is a finite rational algorithm with no unstated cumulant
convention.  Moreover
\[
\mu_{m,q}=0\qquad(m>2q).
\tag{22}
\]
In particular, \(\mu_{0,q}=0\) for every \(q>0\).

For \(n\ge2\), define
\[
\boxed{
H_n(t)
=
\sum_{a=2}^{n}
\ \sum_{\substack{0\le m\le2(n-a)\\m\ {\rm even}}}
\frac{\mu_{m,n-a}}{m!}
\partial_x^mG_a(\tfrac12,t).
}
\tag{23}
\]
The convention for \(n=a\) uses only \(m=0\) and
\(\mu_{0,0}=1\).

Taylor's formula, applied coefficientwise in \(t\), gives
\[
\boxed{
\mathbb E\!\left[
{\cal F}_1(J/k;t,k){\cal F}_1(1-J/k;t,k)
-{\cal F}_0(J/k;t,k){\cal F}_2(1-J/k;t,k)
\right]
=
\sum_{n\ge2}k^{-n}H_n(t).
}
\tag{24}
\]
For any fixed coefficient of \(t\), the Taylor series is finite, so
(24) is a formal coefficient identity and requires no uniform
summation over the depth.

The first terms are
\[
\begin{aligned}
H_2={}&G_2(\tfrac12,t),\\
H_3={}&G_3(\tfrac12,t)+\tfrac18G_2''(\tfrac12,t),\\
H_4={}&G_4(\tfrac12,t)+\tfrac18G_3''(\tfrac12,t)
+\tfrac1{128}G_2^{(4)}(\tfrac12,t).
\end{aligned}
\tag{25}
\]
At the next rank the two distinct contributions from
\(\mathbb E\delta^4=3/(16k^2)-1/(8k^3)\) must both be retained:
\[
\boxed{
\begin{aligned}
H_5={}&G_5(\tfrac12,t)+\tfrac18G_4''(\tfrac12,t)
+\tfrac1{128}G_3^{(4)}(\tfrac12,t)\\
&-\tfrac1{192}G_2^{(4)}(\tfrac12,t)
+\tfrac1{3072}G_2^{(6)}(\tfrac12,t).
\end{aligned}
}
\tag{25a}
\]
The formulas for \(H_2,H_3,H_4\) are exactly the kernels used in the
first two explicit symbol theorems; (25a) is the new rank-three check.

## 4. Proof of the symbol formula

Let \(N_L(k)\) denote the binomially averaged determinant numerator at
total profile loss \(L\), before division by \(2k(k-1)\).  Equation
(24) gives, for every fixed \(L\),
\[
N_L(k)
=\sum_{n\ge2}k^{L-n}[t^L]H_n(t).
\tag{26}
\]
Since
\[
\frac1{2k(k-1)}
=\frac1{2k^2}\sum_{q\ge0}k^{-q},
\tag{27}
\]
put \(L=d+4\).  The coefficient of \(k^{d-r}\) receives exactly the
terms with
\[
n+q=r+2.
\]
Therefore
\[
\beta_{d,r}
=\frac12[t^{d+4}]
\sum_{n=2}^{r+2}H_n(t),
\tag{28}
\]
which is equivalent to (3).  The coefficients of \(t^d\) with
\(d<r\) on its right side vanish: equivalently, they would be
coefficients of \(k^{d-r}\) with negative exponent in the polynomial
\(b_{k,d}\).  Thus the lower limit \(d\ge r\) in (2) introduces no
additional truncation operator.  For each fixed \(R\), computing
\(B_0,\ldots,B_R\) needs profiles only through rank \(M=R+2\).
Lemma 2 then uses phase derivatives through
\(2M+2=2R+6\) and Gamma corrections through \(M\), whose largest
Bernoulli-polynomial index is \(M+1=R+3\).  These are upper bounds for
that fixed \(R\), not estimates uniform as \(R\to\infty\).  This proves
Theorem 1. \(\square\)

## 5. Verified instances and the remaining uniform problem

The recurrence gives:
\[
B_0(t)=\frac{t^0}{1-t}= \frac1{1-t},
\]
after the \(t^{-4}\) shift in (3), so \(\beta_{d,0}=1\).  It also
reproduces
\[
\beta_{d,1}
=-\frac{22d^3+147d^2+161d-258}{36},
\]
and
\[
\beta_{d,2}
=
\frac{
286d^6+3546d^5+12721d^4-7812d^3
-86231d^2+40338d+209160
}{5184}.
\]

The next rank is also an explicit theorem-level consequence.  The
central recurrence gives
\[
\begin{aligned}
H_5(t)
=-\frac{t^6}{3240(1-t)^{10}}\bigl(&
825719t^{10}-7431471t^9+29112669t^8\\
&-64490751t^7+87663474t^6-74537550t^5\\
&+40641750t^4-17199000t^3+8377560t^2\\
&+1202040t+272160\bigr).
\end{aligned}
\tag{29}
\]
Consequently
\[
\boxed{
B_3(t)
=-\frac{t^3}{6480(1-t)^{10}}\bigl(
825719t^9-7216461t^8+27224019t^7
-57304971t^6
+72322254t^5-54697140t^4
+25024140t^3-9849600t^2
+5989680t+2118960
\bigr).
}
\tag{30}
\]
Equivalently, for every \(d\ge3\),
\[
\boxed{
\begin{aligned}
\beta_{d,3}
=-\frac1{83980800}\bigl(&
158450d^9+2651625d^8+15805020d^7+6658380d^6\\
&-213815208d^5-151402725d^4+2063879770d^3\\
&+1562087520d^2-10631426832d-6142443840
\bigr).
\end{aligned}
}
\tag{31}
\]
The independent rank-five implementation verifies (29)--(31) as
rational generating-function identities and compares (31) with exact
finite Lagrange reconstructions of \(b_{k,d}\), using two unused
interpolation values at every tested depth.

The symbolic implementations through profile rank four and the
independent exact Lagrange reconstructions are:

- `verify_ordinary_subleading_saddle_certificate.py`;
- `verify_ordinary_second_subleading_all_orders.py`;
- `independent_verify_ordinary_second_subleading_all_orders.py`.

The theorem proves computability for every fixed rank \(R\).  It does
not control the constants uniformly in \(R\).  The outstanding
publication-level strengthening remains
\[
|\beta_{d,r}|
\le\binom dr(Cd^2)^r
\]
with one absolute \(C\), which would reach the natural cubic scale.
