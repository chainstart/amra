# OPG-1757: an explicit one-eighth top window

Date: 2026-07-30

## 0. Result

Retain
\[
c_k(s)=\sum_{q=0}^{2k-4}a_{k,q}\binom{s-4}{q}
      =\sum_{j\ge0}b_{k,j}s^{2k-4-j},
\qquad m=2k-4,
\]
and put
\[
p_{k,d}=\frac{a_{k,m-d}}{(m-d)!},
\qquad T_{n,r}={n\brace n-r}_4.
\]

### Theorem 1 (quantitative polynomial top window)

Uniformly for integers
\[
0\le d\le k^{1/8},
\]
one has
\[
\boxed{
p_{k,d}=T_{m,d}(1+o(1))>0.
}                                                     \tag{1}
\]
In particular, for all sufficiently large \(k\),
\[
\boxed{
a_{k,2k-4-d}>0
\qquad(0\le d\le k^{1/8}).
}                                                     \tag{2}
\]

This makes the absolute exponent in
`POLYNOMIAL_TOP_WINDOW_THEOREM.md` explicit.  The exponent \(1/8\)
is not claimed to be optimal.

The proof also gives a completely effective, deliberately enormous
threshold:
\[
\boxed{
k\ge 2^{2584}
\quad\Longrightarrow\quad
a_{k,2k-4-d}>0
\quad(0\le d\le\lfloor k^{1/8}\rfloor).
}                                                     \tag{2a}
\]
No computational verification below this threshold is being inferred
from (2a).

## 1. Coefficient norms with explicit constants

For a multivariate polynomial \(F\), let \(\|F\|_1\) be the sum of the
absolute values of its coefficients.  The exact profile notation is
that of `NEAR_LOGARITHMIC_TOP_WINDOW_THEOREM.md`:
\[
U_{h,r}(s)=\frac1{2^rr!}
\sum_{\ell\ge0}R_{\ell,h}(r)s^{2r-\ell},
\qquad h=0,1,2.                                    \tag{3}
\]

### Lemma 2 (explicit profile ledger)

For every \(\ell\ge1\) and \(h\in\{0,1,2\}\),
\[
\boxed{
\|R_{\ell,h}\|_1
\le
\left(2^{16}(\ell+1)^5\right)^\ell.
}                                                     \tag{4}
\]

### Proof

For \(0\le\beta\le5\), define
\[
P_{\beta,u}(t,r)
=[s^{t-u}](s-\beta-r)_{\underline t}.
\]
As in the earlier proof,
\[
P_{\beta,u}
=(-1)^u e_u(\beta+r,\ldots,\beta+r+t-1).           \tag{5}
\]
We retain every constant in its power-sum expansion.

Let
\[
F_v(t)=\sum_{a=0}^{t-1}a^v.
\]
Faulhaber's formula and
\(\lvert B_q\rvert\le4q!\) give, for \(v\ge1\),
\[
\begin{aligned}
\|F_v\|_1
&\le
\frac4{v+1}\sum_{q=0}^{v}\binom{v+1}{q}q!\\
&=
4v!\sum_{p=1}^{v+1}\frac1{p!}
<8v!.                                               \tag{6}
\end{aligned}
\]
The polynomial \((\beta+r+a)^v\) has coefficient norm
\((\beta+2)^v\le7^v\).  Replacing each power of \(a\) by (6) therefore
shows that the power sum
\[
S_v=\sum_{a=0}^{t-1}(\beta+r+a)^v
\]
satisfies
\[
\|S_v\|_1\le8\,7^v v!\le(56v)^v.                  \tag{7}
\]

Newton's partition formula is
\[
e_u=\sum_{\lambda\vdash u}
\frac{(-1)^{u-\ell(\lambda)}}{z_\lambda}
\prod_iS_{\lambda_i}.
\]
There are at most \(2^u\) partitions, \(z_\lambda\ge1\), and
\(\sum_i\lambda_i=u\).  Hence, for \(u\ge1\),
\[
\boxed{
\|P_{\beta,u}\|_1\le(112u)^u.
}                                                     \tag{8}
\]
The same estimate applies to the loss-\(u\) coefficient of
\((s-\alpha)_{\underline r}\).

Next apply the exact binomial moment
\[
\sum_{t=0}^{r}\binom rt2^{r-t}(-1)^t
(t)_{\underline v}
=(-1)^v(r)_{\underline v}.                         \tag{9}
\]
In a monomial \(t^ar^b\) of \(P_{\beta,u}\), one has \(a\le2u\).
The conversion of \(t^a\) into falling powers has coefficient sum
the Bell number \(B_a\le a^a\), while
\[
\|(r)_{\underline v}\|_1=v!\le a^a.
\]
Thus the complete moment conversion costs at most
\[
a^{2a}\le(2u)^{4u}.
\]
If \(M_{\beta,u}(r)\) denotes the normalized Lagrange coefficient at
loss \(u\), equations (8)--(9) give
\[
\boxed{
\|M_{\beta,u}\|_1
\le(1792u^5)^u
\le(2^{11}u^5)^u.
}                                                     \tag{10}
\]

The normalized consecutive difference at loss \(u\) is
\[
M_{\beta,u}(r)-2rM_{\beta+1,u-1}(r).
\]
Using (10), including the case \(u=1\) separately, gives the convenient
uniform majorant
\[
\left\|
M_{\beta,u}-2rM_{\beta+1,u-1}
\right\|_1
\le
\left(2^{14}(u+1)^5\right)^u.                      \tag{11}
\]
For the first summand, its ratio to the right side is at most
\(8^{-u}\).  For \(u\ge2\), the second summand divided by the right
side is at most
\[
2\,
\frac{(2^{11}u^5)^{u-1}}
     {(2^{14}u^5)^u}
=2^{-3u-10}u^{-5}.
\]
At \(u=1\) that summand is simply \(2r\).  These estimates are
strictly stronger than (11).

Convolving (11) with the outer falling product costs \(\ell+1\)
summands.  Since \(\ell+1\le2^\ell\), the three main profiles are
bounded by
\[
\left(2^{15}(\ell+1)^5\right)^\ell.                \tag{12}
\]
For the exceptional \(h=2\) term, the substitutions \(r\mapsto r-1\)
multiply the two coefficient norms by at most \(2^{2u}\) and
\(2^{2v}\), respectively.  Its remaining factor is \(8r\), and its
two losses add to \(\ell-2\).  Its norm is therefore at most
\[
8(\ell-1)
\left(2^{13}(\ell+1)^5\right)^{\ell-2}
\qquad(\ell\ge2).                                  \tag{12a}
\]
This is at most the right side of (12).  Finally, adding the main and
exceptional terms costs at most a factor \(2\le2^\ell\), giving (4).
\(\square\)

## 2. An explicit ordinary-coefficient bound

### Lemma 3

Set
\[
\boxed{A=2^{320}.}                                  \tag{13}
\]
Whenever \(j\ge1\) and \(k\ge2(j+5)\),
\[
\boxed{
|b_{k,j}|\le A^j j^{6j}k^j.
}                                                     \tag{14}
\]

### Proof

Put \(L=j+4\).  Before division by \(2k(k-1)\), the exact
binomially averaged determinant coefficient is
\[
\mathbb E\sum_{\ell=0}^{L}
\left(
R_{\ell,1}(J)R_{L-\ell,1}(k-J)
-R_{\ell,0}(J)R_{L-\ell,2}(k-J)
\right),                                            \tag{15}
\]
where \(J\sim{\rm Bin}(k,\tfrac12)\).  Lemma 2 and
\(2(L+1)\le4^L\) give the kernel norm
\[
\left(2^{18}(L+1)^5\right)^L.                      \tag{16}
\]

For a monomial \(J^a(k-J)^b\), convert both powers to falling powers.
The two Bell-number costs have product at most \(L^L\), and
\[
\mathbb E\!\left[
(J)_{\underline u}(k-J)_{\underline v}
\right]
=\frac{(k)_{\underline{u+v}}}{2^{u+v}}.            \tag{17}
\]
Keep the result in the falling-power basis in \(k\).  The marked
degree cancellation below implies that the coefficients of
\((k)_{\underline L}\) and \((k)_{\underline{L-1}}\) vanish, because
this basis is monic and degree-triangular.  No conversion back to
ordinary powers is needed.  The coefficient norm in the remaining
falling basis is therefore at most
\[
\left(2^{18}(L+1)^6\right)^L.                      \tag{18}
\]

The marked degree lemma and the antisymmetric binomial cancellation,
proved in `FIXED_TOP_DEPTH_ASYMPTOTIC_THEOREM.md`, Lemma 2 and
equations (12)--(14), lower its degree from \(L\) to at most \(L-2\).
Dividing by \(2k(k-1)\), and using
\(k/[2(k-1)]\le1\) for \(k\ge2\), yields
\[
|b_{k,j}|
\le
\left(2^{18}(j+5)^6\right)^{j+4}k^j.               \tag{19}
\]

It remains only to put (19) in a per-\(j\) form.  For every \(j\ge1\),
\[
\begin{aligned}
\left(2^{18}(j+5)^6\right)^{j+4}
={}&2^{18j+72}j^{6j+24}(1+5/j)^{6j+24}\\
\le{}&2^{90j}\,j^{6j}\,2^{13j}\,2^{217j}\\
={}&2^{320j}j^{6j}.                                \tag{20}
\end{aligned}
\]
Here \(j^{24}\le2^{13j}\), since
\(\log j/j\le1/e<13\log2/24\), and
\[
(1+5/j)^{6j+24}
\le e^{30+120/j}\le e^{150}<2^{217}\le2^{217j}.
\]
This proves (14).
\(\square\)

## 3. Proof of Theorem 1

The exact triangular conversion is
\[
p_{k,d}=\sum_{j=0}^{d}b_{k,j}T_{m-j,d-j},          \tag{21}
\]
and \(b_{k,0}=1\).  The audited \(4\)-Stirling ratio is
\[
\frac{T_{m-j,d-j}}{T_{m,d}}
\le
\exp(6d^2/m)
\left(\frac{2d}{m^2}\right)^j
\qquad(0\le j\le d\le m/4).                        \tag{22}
\]
For \(k\ge4\), \(m\ge k\).  Lemma 3 and \(j\le d\) therefore give
\[
\left|
\frac{p_{k,d}}{T_{m,d}}-1
\right|
\le
\exp(6d^2/m)
\sum_{j=1}^{d}
\left(\frac{2A\,d^7}{k}\right)^j.                  \tag{23}
\]

If \(d\le k^{1/8}\), then, uniformly,
\[
\frac{d^2}{m}\le k^{-3/4},
\qquad
\theta_k:=\frac{2Ad^7}{k}\le2Ak^{-1/8}=o(1).       \tag{24}
\]
Also \(d\le m/4\) and \(k\ge2(d+5)\) for all sufficiently large \(k\).
Consequently
\[
\sup_{0\le d\le k^{1/8}}
\left|
\frac{p_{k,d}}{T_{m,d}}-1
\right|
\le
e^{6k^{-3/4}}\frac{2Ak^{-1/8}}{1-2Ak^{-1/8}}
=o(1).                                               \tag{25}
\]
Since \(T_{m,d}>0\), (1)--(2) follow.

For the effective claim, if \(k\ge2^{2584}\), then
\[
2Ak^{-1/8}
\le
2\cdot2^{320}\cdot2^{-323}
=\frac14.
\]
The same threshold is larger than \(256\), so
\[
6k^{-3/4}\le\frac{6}{64}<\frac12
\quad\text{and hence}\quad
e^{6k^{-3/4}}<2.
\]
The right side of (25) is therefore strictly smaller than
\[
2\frac{1/4}{1-1/4}=\frac23<1.
\]
The elementary side conditions also hold.  Indeed, for \(k\ge16\),
\(k^{1/8}\le k/4\); hence
\[
d\le k/4\le(k-2)/2=m/4
\]
and, since the effective threshold is larger than \(20\),
\[
2(d+5)\le k/2+10\le k.
\]
Hence the leading positive term dominates absolutely, proving (2a).
\(\square\)

## 4. Boundary of the result

The proved exponent is \(1/8\), not \(1/3\).  The all-\(d\)
first-subleading symbol
\[
[k^{d-1}]b_{k,d}
=-\frac{22d^3+147d^2+161d-258}{36}
\]
shows that cubic scale is the natural target.  Reaching it requires a
rank-sensitive estimate that replaces the \(j^{6j}\) loss in (14) by
the weighted full-symbol control discussed in
`EXPLICIT_ETA_AND_WEIGHTED_SYMBOL_ATTACK.md`.
