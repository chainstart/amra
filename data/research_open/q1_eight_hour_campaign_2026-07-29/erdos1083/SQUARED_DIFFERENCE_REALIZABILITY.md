# Squared-difference realizability: local universality and cross-product constraints

Date: 2026-07-29

## Purpose

`NETWORK_INVERSE_AUDIT.md` leaves one precise gap: its Hadamard block
barrier uses arbitrary nonnegative sets rather than sets of the form
\[
 (Z_u-Z_v)^2.
\]
This note determines what realizability does and does not add.

The outcome has two sides.

1. Inside one fixed radius-product fibre, the radius pairs form a matching.
   There is essentially no compatibility between different blocks.  A
   three-block Hadamard gadget is exactly realizable even with two heights at
   every radius.
2. Compatibility first appears when blocks from different products form a
   triangle on the original radius indices.  Every such triangle supports
   many triples on an explicit degenerate-triangle algebraic surface.

Thus a successful inverse theorem must couple different product fibres.

## 1. One product fibre is a matching

For geometric radii indexed by integers, a fixed product exponent \(p\)
contains the unordered pairs
\[
 (u,p-u),\qquad u\leq p-u.
\]
Except for a possible central loop \(u=p/2\), these pairs are vertex-disjoint.
Consequently, the height sets used by distinct noncentral blocks in one
product fibre are independent variables.

### Proposition 1 (local universality with a singleton endpoint)

Let \(Y_1,\ldots,Y_t\) be arbitrary finite sets of nonnegative reals assigned
to distinct noncentral pairs in one product fibre.  They can be realized
exactly as
\[
 Y_e=(Z_u-Z_v)^2.
\]

### Proof

For each matching edge \(e=(u,v)\), independently set
\[
 Z_v=\{0\},\qquad
 Z_u=\{\sqrt y:y\in Y_e\}.
\]
Then \((Z_u-Z_v)^2=Y_e\).  No height set is reused by another edge in the
same fibre. \(\square\)

This already proves that no within-fibre compatibility identity can hold
without cardinality or cross-product hypotheses.

## 2. Exact equal-cardinality Hadamard gadget

The singleton in Proposition 1 is not the whole obstruction.

### Lemma 2.1 (every positive two-value set)

For every \(0<r<s\), there are two two-point real sets \(A,B\) such that
\[
 (A-B)^2=\{r,s\}.
\]

### Proof

Put
\[
 \alpha=\frac{\sqrt s+\sqrt r}{2},\qquad
 \beta=\frac{\sqrt s-\sqrt r}{2},
\]
and take
\[
 A=\{-\alpha,\alpha\},\qquad B=\{-\beta,\beta\}.
\]
The four differences have absolute values
\(\alpha-\beta=\sqrt r\) and \(\alpha+\beta=\sqrt s\). \(\square\)

### Proposition 2 (a realizable three-block Hadamard fibre)

Take \(q=2,T=1\) and product exponent \(p=5\).  Its three radius pairs and
radial offsets are
\[
\begin{array}{c|c}
(u,v)&C_{uv}=(2^u-2^v)^2\\ \hline
(0,5)&961\\
(1,4)&196\\
(2,3)&16.
\end{array}
\]
There are two-point height sets at all six radii such that the three shifted
blocks are
\[
 \{1000,1001\},\qquad
 \{1000,1002\},\qquad
 \{1000,1003\}. \tag{1}
\]
Thus every pair of blocks intersects in one value, every symmetric
difference has size two, and their union has size four.

### Proof

For each edge \(e\), prescribe
\[
 Y_e=\{1000-C_e,\ 1000+j_e-C_e\},
\]
where \(j_e=1,2,3\) for the three rows.  All six prescribed numbers are
positive.  Lemma 2.1 realizes each \(Y_e\) by two two-point height sets.
The three radius pairs are disjoint, so the realizations can be assigned
independently.  Adding \(C_e\) gives (1). \(\square\)

This is the smallest Hadamard design from `NETWORK_INVERSE_AUDIT.md`
(\(U=4,k=2,t=3\)), now with exact squared-difference realizability and equal
height multiplicity.  It is a local obstruction, not a global counterexample:
the same six height sets also determine blocks in all the other product
fibres.

## 3. The first genuine compatibility: triangles across products

Let \(A,B,C\subset\mathbb R\), and put
\[
 Y_{AB}=(A-B)^2,\quad
 Y_{BC}=(B-C)^2,\quad
 Y_{AC}=(A-C)^2.
\]
Define the degenerate-triangle polynomial
\[
 \Phi(a,b,c)=(c-a-b)^2-4ab. \tag{2}
\]

### Theorem 3 (representation-level triangle compatibility)

Every point triple \((x,y,z)\in A\times B\times C\) produces
\[
 a=(x-y)^2,\quad b=(y-z)^2,\quad c=(x-z)^2
\]
satisfying
\[
 \Phi(a,b,c)=0. \tag{3}
\]
Let
\[
 R_{AB}=\max_a|\{(x,y)\in A\times B:(x-y)^2=a\}|,
\]
and define \(R_{BC},R_{AC}\) similarly.  If
\[
 R=\min\{R_{AB},R_{BC},R_{AC}\},
\]
then the Cartesian product
\[
 Y_{AB}\times Y_{BC}\times Y_{AC}
\]
contains at least
\[
 \frac{|A||B||C|}{2R} \tag{4}
\]
distinct triples on the surface \(\Phi=0\).

In particular, if all three sets have size \(m\), then \(R\leq2m\), so there
are at least
\[
 \frac{m^2}{4} \tag{5}
\]
distinct compatible squared-value triples.

### Proof

Write \(d_1=x-y\), \(d_2=y-z\).  Then \(x-z=d_1+d_2\), and direct expansion
gives
\[
 ((d_1+d_2)^2-d_1^2-d_2^2)^2
 =4d_1^2d_2^2,
\]
which is (3).

There are \(|A||B||C|\) point triples.  Fix one squared-value triple
\((a,b,c)\), and use an edge attaining \(R\), say \(AB\).  There are at most
\(R\) choices for \((x,y)\) with squared difference \(a\).  For each such
\(y\), the equation \((y-z)^2=b\) has at most two real solutions \(z\).
Thus at most \(2R\) point triples map to one value triple, proving (4).

Finally, for fixed \(x\in A\) and \(a\geq0\), the equation
\((x-y)^2=a\) has at most two real solutions \(y\).  Hence
\(R_{AB}\leq2\min\{|A|,|B|\}\), and similarly for the other pairs.  This
proves (5). \(\square\)

### Interpretation

An arbitrary three-set system can avoid the surface \(\Phi=0\) completely.
Actual height sets cannot: every triangle of radius indices contributes
\(\gg m^2\) compatible triples in the balanced case.  This is strictly
stronger information than block intersections or an abstract correlation
graph.

The signs behind (3) also obey a cocycle:
\[
 \epsilon_{AB}\sqrt a+\epsilon_{BC}\sqrt b
 =\epsilon_{AC}\sqrt c
\]
for signs arising from the same point triple.  A future inverse argument
must retain these representation-level signs; set-level squaring discards
them.

## 4. What this resolves and what remains

Proposition 2 rules out a purely local strategy: even equal-cardinality,
exact squared-difference realizability does not prevent a maximally
correlated three-block fibre.

Theorem 3 identifies the minimum cross-product constraint.  To close the
global branch, one must combine:

1. the many significant within-product correlations extracted in
   `NETWORK_INVERSE_AUDIT.md`;
2. the \(\gg m^2\) compatible value triples on \(\Phi=0\) for each triangle
   of radius indices; and
3. consistency of the square-root signs around cycles.

No estimate combining these three inputs at the \(F^{3/2-o(1)}\) threshold
has yet been proved.

## 5. Verification

`verify_squared_difference_realizability.py` checks the exact \(p=5\)
Hadamard gadget, the polynomial identity, representation multiplicities, and
the support lower bound (4) on finite integer examples.
