# OPG-1757: every fixed top Newton depth is eventually positive

Date: 2026-07-30

## 0. Result

Use the normalization
\[
c_k(s)=\frac{(k-2)!}{2}C_k(s)
      =\sum_{q=0}^{2k-4}a_{k,q}\binom{s-4}{q},
\qquad k\ge2,
\]
and put
\[
m=2k-4,\qquad
p_{k,d}:=\frac{a_{k,m-d}}{(m-d)!}.
\]
Here \(d\) is the depth measured downwards from the highest Newton
coefficient.

### Theorem 1

For every fixed integer \(d\ge0\),
\[
\boxed{
p_{k,d}
=\frac{2^d}{d!}k^{2d}
+O_d(k^{2d-1})
}
\qquad(k\longrightarrow\infty).                    \tag{1}
\]
Consequently, for each fixed \(d\), there is \(k_0(d)\) such that
\[
\boxed{a_{k,\,2k-4-d}>0\qquad(k\ge k_0(d)).}        \tag{2}
\]

This is an all-depth statement: \(d\) is arbitrary, although fixed
before \(k\) tends to infinity.  The companion exact theorem gives
the stronger all-\(k\) sign result for \(0\le d\le5\).  Neither result
controls a top depth growing proportionally to \(k\), so the
linear-width middle of the Newton row remains open.

## 1. Forest profiles at a fixed loss from the top

Let
\[
U_{h,j}(s)=[x^j]\Phi_h(x),\qquad h=0,1,2,
\]
where \(\Phi_h\) is the complete-graph forest polynomial after a
prescribed matching of size \(h\) is contracted and its forced edge
factors are deleted.  Equivalently, \(U_{h,j}(s)\) counts forests of
\(K_s\) that contain the prescribed matching and have \(j+h\) edges.

Write
\[
U_{h,j}(s)
=\frac1{2^j j!}
\sum_{\ell\ge0}R_{\ell,h}(j)s^{2j-\ell}.            \tag{3}
\]

### Lemma 2 (marked finite-loss lemma)

For each fixed \(\ell\), \(R_{\ell,h}(j)\) is a polynomial in \(j\)
and the matching size \(h\), of total degree at most \(\ell\).
In particular,
\[
\deg_j [h^r]R_{\ell,h}(j)\le \ell-r.                \tag{4}
\]

### Proof

First count all \(j\)-subsets of the nonprescribed edges, without the
forest constraint.  Their number is
\[
\binom{\binom{s}{2}-h}{j}.                          \tag{5}
\]
Expand the falling factorial in the upper argument of (5).  A term
\(r\) places below its top has lost \(2r\) powers of \(s\) and,
after multiplication by \(2^j j!\), has degree at most \(2r\) in
\(j\).  Choosing \(t\) linear terms from
\(\binom{s}{2}=(s^2-s)/2\) loses another \(t\) powers of \(s\) and
has degree at most \(t\).  Thus the coefficient at total loss
\(\ell=2r+t\) has degree at most \(\ell\).  Choosing a factor
\(-h\) instead loses two powers of \(s\) and adds one degree in each
of \(j\) and \(h\), so its total degree is again no larger than its
loss.

Now impose acyclicity by inclusion--exclusion over cycles in the
chosen edge set together with the fixed matching.  Suppose a union
of selected cycles uses \(e\) nonprescribed edges, touches \(u\)
marked matching pairs, and uses \(v\) nonfixed vertices.  Each
cyclic component has at least as many edges as vertices.  A touched
matching pair contributes at least one fixed endpoint, or two fixed
endpoints together with one prescribed edge.  Removing all fixed
data from this inequality gives
\[
v\le e-u.
\]
The leading loss of this core from the \(s^{2j}\) scale is therefore
\[
\delta=2e-v\ge e+u.                                 \tag{6}
\]
Choosing the \(e\) occupied edge slots contributes degree at most
\(e\) in \(j\), while choosing the touched matching pairs contributes
degree at most \(u\) in \(h\).  If the core reaches loss \(\ell\),
the remaining edge-binomial expansion has loss
\(\ell-\delta\) and total degree at most \(\ell-\delta\).  Its total
degree in \(j,h\) is at most
\[
e+u+\ell-\delta\le\ell.                             \tag{7}
\]
Also \(e+u\le\delta\le\ell\), so only finitely many cycle-union types
can contribute to a fixed loss.  The embedding polynomial of a fixed
core is \((s-O(h))_{\underline v}\); its lower terms spend additional
loss but add no more degree than that loss.  Summing the core types
proves the lemma.
\(\square\)

This proof includes cycles that use one or both prescribed matching
edges.  For example, after a fixed edge is removed from such a cycle,
the remaining path has one fewer nonfixed vertex than nonprescribed
edges, so (6) only becomes stronger.

## 2. Degree bound for the ordinary power tail

Write
\[
c_k(s)=\sum_{d\ge0}b_{k,d}s^{m-d}.                  \tag{8}
\]
The exact determinant formula is
\[
c_k(s)
=\frac{k!}{2k(k-1)}
\sum_{j=0}^{k}
\left(
U_{1,j}(s)U_{1,k-j}(s)
-U_{0,j}(s)U_{2,k-j}(s)
\right).                                             \tag{9}
\]
Because
\[
\frac1{2^j j!\,2^{k-j}(k-j)!}
=\frac1{k!}\frac{\binom{k}{j}}{2^k},                \tag{10}
\]
the coefficient at total profile loss \(L\) in (9) is
\[
\frac1{2k(k-1)}
\mathbb E\!\left[
\sum_{\ell=0}^{L}
\left\{
R_{\ell,1}(J)R_{L-\ell,1}(k-J)
-R_{\ell,0}(J)R_{L-\ell,2}(k-J)
\right\}
\right],                                             \tag{11}
\]
where \(J\sim{\rm Bin}(k,\tfrac12)\).

The determinant cancels identically at losses \(L=0,1,2,3\); its
degree in \(s\) is \(2k-4\).  Hence \(b_{k,d}\) is (11) with
\(L=d+4\).

There are two further degrees of cancellation.  Lemma 2 lets us
separate the two highest degrees in the variable \(j\):
\[
R_{\ell,h}(j)
=A_\ell(j)+C_\ell(j)+hB_\ell(j)
+O_{\deg_j}(\ell-2),                                \tag{12}
\]
where \(A_\ell\) is homogeneous of \(j\)-degree \(\ell\);
\(C_\ell\) and \(B_\ell\) have \(j\)-degree at most \(\ell-1\);
and \(A_\ell,C_\ell\) are independent of \(h\).  Terms involving
\(h^2\) have \(j\)-degree at most \(\ell-2\).  All terms of
\((J,k-J)\)-degree \(L\) in (11) are therefore independent of \(h\)
and cancel pointwise.  The independent \(C\)-terms at degree
\(L-1\) cancel pointwise as well.  What remains at that degree is
\[
\sum_{\ell=0}^{L}
\left(
B_\ell(J)A_{L-\ell}(k-J)
-A_\ell(J)B_{L-\ell}(k-J)
\right).                                             \tag{13}
\]
Its expectation is zero: interchange
\(\ell\leftrightarrow L-\ell\) and use the symmetry
\(J\overset d=k-J\).  Thus the numerator of (11) has degree at most
\(L-2=d+2\) in \(k\).  The required mixed binomial falling moments
are
\[
\mathbb E\!\left[
(J)_{\underline a}(k-J)_{\underline b}
\right]
=\frac{(k)_{\underline{a+b}}}{2^{a+b}},             \tag{14}
\]
obtained by choosing \(a\) successes and \(b\) failures from the
same \(k\) independent fair trials.  (The marginal formula is the
case \(b=0\).)  Consequently the expectation in (11) preserves the
stated degree bound, and division by \(2k(k-1)\) gives
\[
b_{k,d}=O_d(k^d).                                   \tag{15}
\]

This sharper estimate agrees with the exact beginning
\[
b_{k,0}=1,\quad b_{k,1}=k-2,\quad
b_{k,2}=(k-2)(k-21).                                \tag{16}
\]
In particular \(b_{k,d}=O_d(k^{2d-1})\) for every fixed \(d\ge1\),
which is the weaker form needed below.

## 3. Triangular conversion to the base-four Newton basis

For integers \(q,r\ge0\), put
\[
E_r(q):=e_r(4,5,\ldots,q+3),
\]
the elementary symmetric function of degree \(r\) in the consecutive
roots.  For fixed \(r\) and \(q=2k+O(1)\),
\[
\boxed{
E_r(q)
=\frac{2^r}{r!}k^{2r}+O_r(k^{2r-1}).
}                                                     \tag{17}
\]
Indeed,
\[
\sum_{\nu=4}^{q+3}\nu
=\frac{q(q+7)}2
=2k^2+O(k),                                         \tag{18}
\]
and Newton's identities show that the unique contribution of degree
\(2r\) to \(E_r\) is \(1/r!\) times the \(r\)-th power of (18).
Every term involving a power sum of order at least two has degree at
most \(2r-1\) in \(k\).

Since
\[
(s-4)_{\underline q}
=\sum_{r=0}^{q}(-1)^rE_r(q)s^{q-r},                 \tag{19}
\]
comparison of the coefficient of \(s^{m-d}\) gives the triangular
identity
\[
b_{k,d}
=\sum_{i=0}^{d}
p_{k,i}(-1)^{d-i}E_{d-i}(m-i).                      \tag{20}
\]

We prove (1) by induction on \(d\).  The case \(d=0\) is
\(p_{k,0}=b_{k,0}=1\).  Suppose the result holds below \(d\).
Equations (15), (17), and (20) give
\[
\begin{aligned}
p_{k,d}
&=-\sum_{i=0}^{d-1}
(-1)^{d-i}
\frac{2^i}{i!}\frac{2^{d-i}}{(d-i)!}k^{2d}
+O_d(k^{2d-1})\\
&=-2^d
\sum_{i=0}^{d-1}
\frac{(-1)^{d-i}}{i!(d-i)!}k^{2d}
+O_d(k^{2d-1}).
\end{aligned}                                       \tag{21}
\]
The full alternating sum from \(i=0\) to \(d\) is zero.  Therefore
the truncated sum equals \(-1/d!\), and (21) becomes
\[
p_{k,d}
=\frac{2^d}{d!}k^{2d}+O_d(k^{2d-1}).
\]
This proves Theorem 1. \(\square\)

## 4. What this closes and what remains

The Newton support now has two rigorous asymptotic positive regimes:

1. from its first active coefficient, every depth
   \(r=o(\sqrt{k})\) is positive by the growing-depth theorem;
2. from its highest coefficient, every fixed depth \(d\) is positive
   by Theorem 1.

The first regime grows with \(k\), whereas the second is currently
fixed-depth only.  A proof of OPG-1757 still needs either a uniform
argument through the intervening middle, a top window with growing
depth that meets the lower window, or a global injection/Hall
inequality.
