# High multiplicative-energy radii: a thin-slab theorem

Date: 2026-07-29

## Purpose

`AFFINE_COPY_REDUCTION_AND_BARRIER.md` reduces the all-circle-pairs route to
the number \(M\) of distinct parameters
\[
 A_{ij}=(\rho_i-\rho_j)^2+(z_i-z_j)^2,\qquad
 B_{ij}=2\rho_i\rho_j.
\]
Low multiplicative energy of the radii already gives a useful lower bound for
\(M\).  This note proves a complementary high-energy special case: geometric
progression radii and completely arbitrary height sets lying in a common
thin slab.

Two complementary structured theorems are proved.  The first allows arbitrary
and unequal height sets in a common thin slab.  The second removes the slab
condition completely when every radius carries the same arbitrary height
set.  Neither covers fully independent, widely spread height sets.

## Theorem 1 (geometric radii in a thin slab)

Let the distinct radii be
\[
 \rho_u=Tq^u,\qquad 0\leq u<L,
\]
where \(q\geq2\) is an integer and \(T>0\).  On radius \(\rho_u\), let
\(Z_u\subset\mathbb R\) be an arbitrary finite height set of size \(n_u\).
Suppose that all the height sets lie in one interval of length \(H<T\).
Put
\[
 F=\sum_{u=0}^{L-1}n_u.
\]
Then the number \(M\) of distinct parameter pairs \((A_{ij},B_{ij})\),
including pairs of circles at the same radius, satisfies
\[
 M\geq \frac{L+1}{4}F. \tag{1}
\]

In particular, if \(L\asymp F^{1/2}\), then
\[
 M\gg F^{3/2}. \tag{2}
\]

### Proof

Fix a pair of radius indices \(u\leq v\).  Its product parameter is
\[
 B_{uv}=2T^2q^{u+v},
\]
and its radial offset is
\[
 C_{uv}=T^2(q^u-q^v)^2.
\]
The parameter intercepts contributed by this radius pair form
\[
 C_{uv}+(Z_u-Z_v)^2. \tag{3}
\]

For a fixed product exponent \(p=u+v\), different unordered pairs
\(\{u,v\}\) have different radial offsets.  Indeed, the positive product
\(q^{u+v}\) and the value \((q^u-q^v)^2\) determine
\[
 (q^u+q^v)^2=(q^u-q^v)^2+4q^{u+v},
\]
and hence determine the unordered pair \(\{q^u,q^v\}\).  Since the unscaled
offsets are distinct integers, two such offsets differ by at least \(1\).
Consequently their scaled offsets differ by at least \(T^2\).

All squared height differences lie in \([0,H^2]\).  The assumption \(H<T\)
therefore makes the intervals
\[
 [C_{uv},C_{uv}+H^2]
\]
disjoint for different radius pairs with the same product parameter.
Thus the sets in (3) have no cross-pair collisions at a fixed \(B\).

For arbitrary finite real sets \(U,V\),
\[
 |(U-V)^2|\geq \frac12\max\{|U|,|V|\}. \tag{4}
\]
To see this, fix one member of \(V\).  The \(|U|\) resulting differences are
distinct, and squaring is at most two-to-one; interchange \(U,V\) for the
other bound.

It follows from the disjoint blocks and (4) that
\[
 M\geq\frac12\sum_{0\leq u\leq v<L}\max\{n_u,n_v\}.
\]
Using \(\max\{a,b\}\geq(a+b)/2\),
\[
\begin{aligned}
 M
 &\geq\frac14\sum_{u\leq v}(n_u+n_v)\\
 &=\frac{L+1}{4}\sum_un_u
 =\frac{L+1}{4}F.
\end{aligned}
\]
This proves (1), and (2) is immediate. \(\square\)

## Theorem 2 (identical arbitrary height sets, no slab condition)

Keep the geometric radii
\[
 \rho_u=Tq^u,\qquad 0\leq u<L,\quad q\geq2.
\]
Suppose now that every radius carries exactly the same arbitrary \(m\)-point
height set \(Z\subset\mathbb R\).  There is no restriction on the diameter or
additive structure of \(Z\).  Then
\[
 M\gg
 \sum_p\frac{t_p^2m}{t_p+m}, \tag{5}
\]
where
\[
 t_p=|\{(u,v):0\leq u\leq v<L,\ u+v=p\}|.
\]
In particular, if \(m\geq cL\) for a fixed \(c>0\), then
\[
 M\gg_c L^3\asymp_c F^{3/2}. \tag{6}
\]

### Lemma 2.1 (Sidon radial offsets)

For each fixed \(p\), the set
\[
 C_p=\{T^2(q^u-q^v)^2:u\leq v,\ u+v=p\}
\]
has all its positive differences distinct.

### Proof

Write \(x=(v-u)/2\).  Apart from the common positive factor \(T^2q^p\),
the offsets are
\[
 a_x=(q^x-q^{-x})^2=4\sinh^2(x\log q),
\]
where the admissible \(x\)'s form an arithmetic progression of step one.
For \(x>0\),
\[
 \sinh((x+1)\log q)>q\sinh(x\log q),
\]
and the same growth conclusion is immediate from \(a_0=0\).  Hence
\[
 a_{x+1}>q^2a_x\geq4a_x.
\]
The consecutive gaps \(g_x=a_{x+1}-a_x\) are therefore superincreasing:
each \(g_x\) is larger than the sum of all preceding gaps.  If two positive
differences of the \(a_x\)'s were equal, they would give two equal sums of
consecutive gaps.  Comparing the largest gap and cancelling successively
forces the two intervals, and hence the two differences, to be identical.
\(\square\)

### Proof of Theorem 2

Put
\[
 Y=(Z-Z)^2,\qquad y=|Y|.
\]
Fixing the smallest member of \(Z\) gives \(y\geq m\).  At product exponent
\(p\), the set of intercepts is exactly \(C_p+Y\).

Let \(E(C_p,Y)\) be the additive energy counting
\(c+y_1=c'+y_2\).  The diagonal \(c=c'\) contributes \(t_py\).
By Lemma 2.1, every nonzero difference \(c-c'\) has at most one ordered
representation, so all off-diagonal solutions together contribute at most
\(y^2\).  Therefore
\[
 E(C_p,Y)\leq t_py+y^2.
\]
Cauchy--Schwarz gives
\[
 |C_p+Y|
 \geq\frac{(t_py)^2}{t_py+y^2}
 =\frac{t_p^2y}{t_p+y}
 \geq\frac{t_p^2m}{t_p+m}. \tag{7}
\]
Different \(p\)'s have different product parameters \(B\), so these counts
add and prove (5).

If \(m\geq cL\), then \(t_p\leq(L+1)/2=O_c(m)\), and (7) is
\(\gg_c t_p^2\).  For a positive proportion of the \(2L-1\) product
exponents, \(t_p\gg L\); hence
\[
 \sum_pt_p^2\gg L^3.
\]
This proves (6). \(\square\)

The proof actually gives a reusable criterion.  For an arbitrary radius set
\(R\), define at each product \(p\)
\[
 C_p=\{(\rho-\sigma)^2:\rho,\sigma\in R,\ \rho\leq\sigma,\ \rho\sigma=p\}.
\]
If every \(C_p\) has distinct positive differences and every radius carries
the same \(m\)-point height set, then (5) holds with \(t_p=|C_p|\).
The geometric progression with ratio \(q\geq2\) is one concrete
high-multiplicative-energy family satisfying this Sidon-offset criterion.

## Corollary 3 (conditional exponent gain)

Suppose the synchronized-circle extraction in the critical branch has
\[
 S=N^{2/5-o(1)},\qquad F=N^{3/5-o(1)},\qquad
 L=F^{1/2-o(1)},
\]
and satisfies either the hypotheses of Theorem 1 or the balanced case of
Theorem 2.
Then the all-pairs Szemerédi--Trotter bound gives
\[
 D\gg\sqrt{SM}
 \gg N^{13/20-o(1)}.
\]

This is a \(1/20\) gain inside either stated structured subcase.  The inherited
argument currently produces neither a common thin slab nor identical height
sets, so the corollary does not improve the unconditional exponent.

## Why the arbitrary-height case remains open

When the total height span is at least \(T\), blocks
\[
 C_{uv}+(Z_u-Z_v)^2
\]
belonging to distinct radius pairs with the same product can overlap.
Counting one block at a time then gives only \(M\gg F\).  The missing
statement must show one of the following:

1. many radial-offset blocks remain sufficiently separated;
2. extensive overlap forces a large squared height-difference set;
3. the overlap equations
   \[
   (z-w)^2-(z'-w')^2=C_{u'v'}-C_{uv}
   \]
   have energy below the \(F^{8/3}\) threshold; or
4. the resulting height structure yields an independent distance expansion.

Theorems 1 and 2 establish that the high multiplicative energy of a geometric
radius progression is not itself an obstruction.  The unresolved part is the
interaction of independently varying, widely spread height sets with
radial-offset collisions.

### Conjectural target, not a theorem

For geometric radii \(\rho_u=Tq^u\), \(q\geq2\), and arbitrary nonempty
finite height sets \(Z_u\), the computations and the two theorems suggest
\[
 M\geq \frac{FL}{F^{o(1)}}. \tag{8}
\]
In the balanced regime \(L\asymp F^{1/2}\), this is
\(M\geq F^{3/2-o(1)}\).  No proof of (8) is currently known.  A valid proof
must control simultaneous overlap among the independently varying sets
\[
 T^2(q^u-q^v)^2+(Z_u-Z_v)^2
\]
for all pairs with the same sum \(u+v\).  Pairwise sumset estimates alone do
not provide that control.

`HIGH_ENERGY_OVERLAP_STABILITY.md` gives the exact elementary second-order
version of this target: a factor-\(K\) loss in \(M\) forces a factor-\(K\)
excess of shifted cross-correlation among these blocks.  It stops short of
the translate/reflection inverse theorem.

## Exact search status

`verify_geometric_radius_high_energy.py` performs three kinds of exact integer
checks.

- It verifies Theorem 1 on exhaustive small thin-slab instances.
- It verifies the Sidon-offset lemma and Theorem 2 on exact small instances.
- Outside the slab hypothesis, it exhaustively searches small independent
  height sets for radii \(1,2,4,\ldots\).

For the searched cases, the smallest values were attained when all radius
classes used the same arithmetic progression of heights.  No configuration
with anomalously small \(M/F^{3/2}\) was found.  This is finite experimental
evidence only; it neither proves the arbitrary-height conjecture nor rules
out a larger counterexample.
