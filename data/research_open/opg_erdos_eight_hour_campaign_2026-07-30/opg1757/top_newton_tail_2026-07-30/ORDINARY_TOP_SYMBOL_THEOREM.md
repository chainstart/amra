# OPG-1757: an all-orders ordinary-power top symbol

Date: 2026-07-30

## 0. Result

Let
\[
c_k(s)=\sum_{d\ge0}b_{k,d}s^{2k-4-d}.
\]

### Theorem 1

For every fixed \(d\ge0\), \(b_{k,d}\) is eventually a polynomial in
\(k\) of degree exactly \(d\), and
\[
\boxed{
b_{k,d}=k^d+O_d(k^{d-1}).
}                                                     \tag{1}
\]
Equivalently, the generating function of all leading ordinary-power
symbols is
\[
\boxed{
\sum_{d\ge0}[k^d]b_{k,d}\,z^d=\frac1{1-z}.
}                                                     \tag{2}
\]

The first terms are
\[
\begin{aligned}
b_{k,0}&=1,\\
b_{k,1}&=k-2,\\
b_{k,2}&=(k-2)(k-21),\\
b_{k,3}&=\frac{(k-3)(k-2)(2k-109)}2,\\
b_{k,4}&=\frac{(k-3)(k-2)(6k^2-661k+4240)}6,\\
b_{k,5}&=\frac{(k-4)(k-3)(k-2)(3k^2-554k+6961)}3.
\end{aligned}                                        \tag{3}
\]

This theorem sharpens the degree estimate used in the fixed
top-Newton-depth proof.  It does not assert that the \(b_{k,d}\) are
positive: the lower coefficients in (3) already change sign.  The
positive object is the base-four Newton tail after triangular
conversion.

## 1. Three marked profile symbols

Normalize the prescribed-matching profiles by
\[
U_{h,j}(s)
=\frac1{2^j j!}
\sum_{\ell\ge0}R_{\ell,h}(j)s^{2j-\ell},
\qquad h=0,1,2.                                     \tag{4}
\]
The marked finite-loss lemma gives
\[
\deg_j[h^r]R_{\ell,h}(j)\le\ell-r.                  \tag{5}
\]
Define the three highest marked symbols by
\[
A_\ell=[j^\ell]R_{\ell,0}(j),                       \tag{6}
\]
\[
B_\ell=[j^{\ell-1}]
\left(R_{\ell,1}(j)-R_{\ell,0}(j)\right),           \tag{7}
\]
\[
C_\ell=\frac12[j^{\ell-2}]
\left(R_{\ell,2}(j)-2R_{\ell,1}(j)+R_{\ell,0}(j)\right).
                                                            \tag{8}
\]
Thus \(B_\ell\) is the coefficient of \(h j^{\ell-1}\), and
\(C_\ell\) is the coefficient of \(h^2j^{\ell-2}\).

### Lemma 2 (exact symbol resummation)

The three generating functions are
\[
\boxed{
A(x):=\sum_{\ell\ge0}A_\ell x^\ell
=\sqrt{1-2x},
}                                                     \tag{9}
\]
\[
\boxed{
B(x):=\sum_{\ell\ge1}B_\ell x^{\ell-1}
=-\frac{2x}{\sqrt{1-2x}},
}                                                     \tag{10}
\]
\[
\boxed{
C(x):=\sum_{\ell\ge2}C_\ell x^{\ell-2}
=-\frac{2x^2}{(1-2x)^{3/2}}.
}                                                     \tag{11}
\]

### Proof

The exact Lagrange profiles are
\[
U_{0,j}(s)
=(s)_{\underline j}D(s,s-j,j),                     \tag{12}
\]
\[
U_{1,j}(s)
=(s-2)_{\underline j}D(s,s-2-j,j),                 \tag{13}
\]
\[
\begin{aligned}
U_{2,j}(s)
={}&(s-4)_{\underline j}D(s,s-4-j,j)\\
&+4(s-4)_{\underline{j-1}}E(s,s-3-j,j-1),
\end{aligned}                                        \tag{14}
\]
where
\[
E(s,c,j)=
\sum_{r=0}^{j}
\frac{(-1)^r(c)_{\underline r}s^{j-r}}
     {2^r r!(j-r)!},
\qquad
D(s,c,j)=E(s,c,j)-E(s,c,j-1).                       \tag{15}
\]

To extract the diagonal symbols, multiply (12)--(14) by
\(2^j j!/s^{2j}\), put \(j=xs\), and expand formally in \(s^{-1}\).
Only finite products are involved at every requested power.  The
summation in (15) is reduced by
\[
\sum_{r=0}^{j}
\binom jr2^{j-r}(-1)^r(r)_{\underline v}
=(-1)^v(j)_{\underline v}.                         \tag{16}
\]
The constant, first marked, and second marked diagonal terms are
\[
\lim_{s\to\infty}
\frac{2^j j!}{s^{2j}}U_{h,j}(s)
=A(x),                                               \tag{17}
\]
\[
\lim_{s\to\infty}
s\left[
\frac{2^j j!}{s^{2j}}U_{1,j}(s)
-\frac{2^j j!}{s^{2j}}U_{0,j}(s)
\right]
=B(x),                                               \tag{18}
\]
\[
\begin{aligned}
\lim_{s\to\infty}\frac{s^2}{2}
\left[
\frac{2^j j!}{s^{2j}}U_{2,j}(s)
-2\frac{2^j j!}{s^{2j}}U_{1,j}(s)
+\frac{2^j j!}{s^{2j}}U_{0,j}(s)
\right]
=C(x).                                               \tag{19}
\end{aligned}
\]
Direct logarithmic expansion of the falling products in
(12)--(15) gives
\[
A(x)=\sqrt{1-2x}.                                   \tag{20}
\]
Coefficientwise, the same calculation is the recurrence
\[
A_0=1,\qquad
(\ell+1)A_{\ell+1}=(2\ell-1)A_\ell
\quad(\ell\ge0),                                    \tag{20a}
\]
obtained by applying (16) to the highest homogeneous part at loss
\(\ell+1\).  Equation (20a) is equivalent to
\((1-2x)A'(x)+A(x)=0\) and fixes the branch in (20).
There is also a short check of the first marked term.  Edge
transitivity gives the exact identity
\[
U_{1,j}(s)
=\frac{j+1}{\binom{s}{2}}U_{0,j+1}(s).
                                                            \tag{21}
\]
After normalization, (21) becomes
\[
\frac{2^j j!}{s^{2j}}U_{1,j}(s)
=\frac1{1-s^{-1}}
\frac{2^{j+1}(j+1)!}{s^{2j+2}}U_{0,j+1}(s).
                                                            \tag{22}
\]
Taking the coefficient of \(s^{-1}\) with \(j=xs\) yields
\[
B(x)=A(x)+A'(x)
=-\frac{2x}{\sqrt{1-2x}}.                           \tag{23}
\]
For completeness, here is the all-orders coefficient identity behind
the second marked term.  Write
\[
 {\cal P}_h(s,x)
 =\frac{2^j j!}{s^{2j}}U_{h,j}(s),\qquad j=xs,
 \qquad \varepsilon=s^{-1}.
\]
Substitute (12)--(15), expand each finite falling product through
\(\varepsilon^2\), and collect the coefficient of a fixed power
\(x^{\ell-2}\).  Every summand containing the Lagrange index \(r\)
is a linear combination of \((r)_{\underline v}\), so (16) applies
coefficientwise and leaves
\[
\begin{aligned}
[x^{\ell-2}\varepsilon^2]\,
 \bigl({\cal P}_2-2{\cal P}_1+{\cal P}_0\bigr)
 &=4(\ell-2)(\ell-3)A_{\ell-2}
 \qquad(\ell\ge2).                                  \tag{23a}
\end{aligned}
\]
Equivalently, as an identity of formal series,
\[
 {\cal P}_2-2{\cal P}_1+{\cal P}_0
 =4x^2A''(x)\varepsilon^2+O_{\rm formal}(\varepsilon^3).
                                                            \tag{23b}
\]
Notice that (23a) is an identity for every \(\ell\), rather than a
finite-order computer check: for a fixed coefficient only finitely
many factors from (12)--(15) enter, and (16) evaluates their complete
sum.  Comparing (23b) with the normalization \(s^2/2\) in (19) gives
\[
 C_\ell=2(\ell-2)(\ell-3)A_{\ell-2}
 \quad(\ell\ge2),                                   \tag{23c}
\]
where the right side is zero for \(\ell=2,3\).  Hence
\[
C(x)=2x^2A''(x)
=-\frac{2x^2}{(1-2x)^{3/2}}.                       \tag{24}
\]
All three calculations are identities of formal power series around
\(x=0\).  The companion verifier performs the same extraction
coefficientwise, without using an analytic limit.
\(\square\)

As a consistency check,
\[
\begin{aligned}
A(x)&=1-x-\tfrac12x^2-\tfrac12x^3-\tfrac58x^4-\cdots,\\
B(x)&=-2x-2x^2-3x^3-5x^4-\cdots,\\
C(x)&=-2x^2-6x^3-15x^4-\cdots,
\end{aligned}
\]
which reproduces every recorded profile symbol.

## 2. Determinant extraction

The exact determinant formula is
\[
c_k(s)
=\frac{k!}{2k(k-1)}
\sum_{j=0}^{k}
\left(
U_{1,j}(s)U_{1,k-j}(s)
-U_{0,j}(s)U_{2,k-j}(s)
\right).                                             \tag{25}
\]
At total profile loss \(L=d+4\), use
\[
\frac1{2^j j!\,2^{k-j}(k-j)!}
=\frac1{k!}\frac{\binom kj}{2^k}.                   \tag{26}
\]
The marked degree lemma shows that the numerator after binomial
averaging has degree at most \(L-2\) in \(k\).  We now extract that
highest surviving degree.

All profile terms independent of \(h\) cancel.  Terms linear in \(h\)
at \(j\)-degree \(\ell-1\) form an antisymmetric convolution and have
zero binomial expectation.  To make the next degree completely
explicit, write
\[
\begin{aligned}
R_{\ell,h}(j)
={}&A_\ell j^\ell
 +(P_\ell+hB_\ell)j^{\ell-1}\\
 &+(Q_\ell+hD_\ell+h^2C_\ell)j^{\ell-2}
 +O_\ell(j^{\ell-3}).                               \tag{26a}
\end{aligned}
\]
For \(r=L-\ell\), the degree-\((L-2)\) part of
\[
R_{\ell,1}(J)R_{r,1}(k-J)
-R_{\ell,0}(J)R_{r,2}(k-J)
\]
has coefficient ledger
\[
B_\ell B_r
 +(D_\ell A_r-A_\ell D_r)
 +(B_\ell P_r-P_\ell B_r)
 +(C_\ell A_r-3A_\ell C_r),                         \tag{26b}
\]
with the corresponding powers of \(J\) and \(k-J\).  Summing over
\(\ell\), the \(DA-AD\) and \(BP-PB\) convolutions vanish by the
involution
\[
(\ell,J)\longleftrightarrow(r,k-J).
\]
The same involution changes the expectation of
\(C_\ell A_r-3A_\ell C_r\) into that of
\(-2A_\ell C_r\).  Thus, after binomial symmetrization (not
pointwise), the complete surviving contribution is \(BB-2AC\):
\[
\sum_{\ell=0}^{L}
\left(
B_\ell B_{L-\ell}
\mathbb E\!\left[
J^{\ell-1}(k-J)^{L-\ell-1}
\right]_{\rm lead}
-2A_\ell C_{L-\ell}
\mathbb E\!\left[
J^\ell(k-J)^{L-\ell-2}
\right]_{\rm lead}
\right),                                             \tag{27}
\]
with a term understood as zero when one of its exponents is negative.
Since
\[
\mathbb E[J^a(k-J)^b]
=2^{-a-b}k^{a+b}+O_{a,b}(k^{a+b-1}),                \tag{28}
\]
the generating function of the degree-\((L-2)\) numerator symbols is
\[
\begin{aligned}
B(z/2)^2-2A(z/2)C(z/2)
&=\frac{z^2}{1-z}+\frac{z^2}{1-z}\\
&=\frac{2z^2}{1-z}.                                 \tag{29}
\end{aligned}
\]
Thus the leading coefficient of the numerator is \(2\) at every
loss \(L\ge4\).  Division by \(2k(k-1)\) in (25) gives
\[
[k^{L-4}]b_{k,L-4}=1.
\]
Taking \(L=d+4\) proves (1)--(2). \(\square\)

## 3. Consequences

Combining (1) with the base-four triangular conversion recovers
\[
p_{k,d}
=\frac{2^d}{d!}k^{2d}+O_d(k^{2d-1})
\]
for every fixed top Newton depth \(d\).  The new information is that
the entire ordinary-power perturbation has a universal leading symbol,
not merely a degree bound.

This exact resummation also identifies the right route to a wider
growing top window: one should bound the lower symbols uniformly
around the singularity \(x=1/2\), rather than estimate every
finite-loss coefficient independently.
