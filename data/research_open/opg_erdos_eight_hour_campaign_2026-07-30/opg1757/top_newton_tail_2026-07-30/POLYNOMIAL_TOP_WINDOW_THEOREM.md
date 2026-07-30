# OPG-1757: a fixed-power positive top window

Date: 2026-07-30

## 0. Result

Let
\[
c_k(s)=\sum_{q=0}^{2k-4}a_{k,q}\binom{s-4}{q},
\qquad
m=2k-4,
\qquad
p_{k,d}=\frac{a_{k,m-d}}{(m-d)!}.
\]

### Theorem 1

There exists an absolute constant \(\eta>0\) such that, uniformly for
integers
\[
0\le d\le k^\eta,
\]
\[
\boxed{
p_{k,d}
=T_{m,d}(1+o(1))>0,
\qquad
T_{n,r}:={n\brace n-r}_4.
}                                                     \tag{1}
\]
Equivalently, for all sufficiently large \(k\),
\[
\boxed{
a_{k,\,2k-4-d}>0
\quad(0\le d\le k^\eta).
}                                                     \tag{2}
\]

This changes the top positive region from a polylogarithmic window to
a genuine fixed-power window.  The exponent \(\eta\) is absolute but
is not optimized: its value comes from deliberately nonnumerical
coefficient-norm constants.

## 1. A sharp ratio for near-diagonal \(4\)-Stirling numbers

### Lemma 2

If \(0\le j\le d\le n/4\), then
\[
\boxed{
\frac{T_{n-j,d-j}}{T_{n,d}}
\le
\exp\!\left(\frac{6d^2}{n}\right)
\left(\frac{2d}{n^2}\right)^j.
}                                                     \tag{3}
\]

### Proof

The lower bound obtained by making \(d\) disjoint pairs from the
\(n\) ordinary elements is
\[
T_{n,d}
\ge\frac{(n)_{\underline{2d}}}{2^d d!}.             \tag{4}
\]
For the upper bound, replace every nonsingleton block by the star from
its least element.  A partition of \(n-j+4\) elements with block
deficit \(d-j\) injects into a \((d-j)\)-edge graph.  Hence
\[
T_{n-j,d-j}
\le
\frac{(n-j+4)^{2(d-j)}}
{2^{d-j}(d-j)!}.                                    \tag{5}
\]
Dividing (5) by (4) gives
\[
\frac{T_{n-j,d-j}}{T_{n,d}}
\le
2^j(d)_{\underline j}
\frac{(n-j+4)^{2(d-j)}}{(n)_{\underline{2d}}}.
                                                            \tag{6}
\]

Since \(2d\le n/2\), the elementary inequality
\(\log(1-x)\ge-2x\) for \(0\le x\le1/2\) gives
\[
\begin{aligned}
(n)_{\underline{2d}}
&=n^{2d}\prod_{r=0}^{2d-1}\left(1-\frac rn\right)\\
&\ge
n^{2d}
\exp\!\left(-\frac2n\sum_{r=0}^{2d-1}r\right)
\ge n^{2d}\exp\!\left(-\frac{4d^2}{n}\right).
\end{aligned}                                      \tag{7}
\]
For \(j\ge1\), also
\[
(n-j+4)^{2(d-j)}
\le n^{2(d-j)}
\left(1+\frac{(4-j)_+}{n}\right)^{2(d-j)}
\le n^{2(d-j)}
\exp\!\left(
\frac{2(d-j)(4-j)_+}{n}
\right).
\tag{8}
\]
For \(d\ge2\) and \(1\le j\le d\),
\[
4d^2+2(d-j)(4-j)_+\le6d^2.
\]
(The only smallest case, \(d=2,j=1\), reads \(22\le24\);
for \(d\ge3\), the added term is at most \(6d\le2d^2\).)
Thus the exponential factors in (7)--(8) are at most
\(\exp(6d^2/n)\).  When \(j=0\), the ratio on the left of (3) is
exactly one, so (3) is immediate; the cases \(d=0,1\) are likewise
immediate.  Finally
\((d)_{\underline j}\le d^j\), proving (3).
\(\square\)

The essential feature is that (3) has no factor exponential in \(d\)
outside the harmless \(\exp(O(d^2/n))\).

## 2. Uniform ordinary-power coefficients

The sharpened profile estimate proved in
`NEAR_LOGARITHMIC_TOP_WINDOW_THEOREM.md` supplies an absolute
constant \(C_0\) such that, for \(k\ge2(j+5)\),
\[
|b_{k,j}|
\le
\exp\!\bigl(C_0(j+5)\log(j+5)\bigr)k^j,
\qquad
c_k(s)=\sum_{j\ge0}b_{k,j}s^{m-j}.                 \tag{9}
\]
Consequently there is another absolute constant \(A\ge1\) such that
for every \(j\ge1\),
\[
\boxed{
|b_{k,j}|\le A^j j^{Aj}k^j.
}                                                     \tag{10}
\]
Indeed, enlarge \(A\) once to cover \(1\le j\le5\); for \(j\ge6\),
\((j+5)\log(j+5)\le3j\log j\), and (10) follows after another
absolute enlargement.

## 3. Proof of Theorem 1

The exact monomial-to-Newton identity is
\[
p_{k,d}
=\sum_{j=0}^d b_{k,j}T_{m-j,d-j},                 \tag{11}
\]
and \(b_{k,0}=1\).  Take \(n=m=2k-4\).  For \(d\le m/4\), Lemma 2
and (10) imply
\[
\begin{aligned}
\left|\frac{p_{k,d}}{T_{m,d}}-1\right|
&\le
\exp\!\left(\frac{6d^2}{m}\right)
\sum_{j=1}^d
A^j j^{Aj}k^j
\left(\frac{2d}{m^2}\right)^j\\
&\le
\exp\!\left(\frac{6d^2}{m}\right)
\sum_{j=1}^d
\left(\frac{2A\,d^{A+1}}{k}\right)^j,              \tag{12}
\end{aligned}
\]
after increasing \(A\) by an absolute factor and using \(m\ge k\).

Choose
\[
\boxed{
0<\eta<
\min\left\{\frac12,\frac1{A+1}\right\}.
}                                                     \tag{13}
\]
Uniformly for \(d\le k^\eta\),
\[
\frac{d^2}{m}=o(1),
\qquad
\theta_k:=\frac{2A\,d^{A+1}}k=o(1).
\]
For large \(k\), \(\theta_k<1/2\), and (12) yields
\[
\left|\frac{p_{k,d}}{T_{m,d}}-1\right|
\le(1+o(1))\frac{\theta_k}{1-\theta_k}
=o(1).                                               \tag{14}
\]
Since \(T_{m,d}>0\), equations (1)--(2) follow.
\(\square\)

## 4. Scope and significance

The theorem proves a growing algebraic window of width \(k^\eta\) at
the high-degree boundary of every complete-split Newton row.  It
strictly contains every polylogarithmic window and includes the nine
exact layers as finite boundary checks.

It does not reach the linear-width middle and therefore does not prove
the complete-split case of OPG-1757, much less the conjecture for all
graphs.  Its publication value depends on novelty relative to existing
near-diagonal generalized-Stirling and forest-Rayleigh literature; that
comparison is recorded separately.
