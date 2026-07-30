# Triangle and \(K_4\) compatibility: group-like saturation and the sign obstruction

Date: 2026-07-29

## Purpose

`SQUARED_DIFFERENCE_REALIZABILITY.md` identifies the triangle surface
\[
 (c-a-b)^2=4ab
\]
as the first constraint coupling different radius-product fibres.  This note
tests whether that surface, or the additional consistency from four radius
vertices, supplies a usable incidence gain.

The result is mixed.

- Four vertices impose a genuine sign-consistency polynomial not implied by
  the four triangle equations.
- Both the triangle and \(K_4\) varieties are additively parameterized and
  saturate their natural quadratic and cubic counts.  Compatibility alone
  therefore gives no exponent gain.  It must be combined with the
  high-correlation information from `HIGH_ENERGY_OVERLAP_STABILITY.md`.

No Elekes--Szabó theorem is invoked; the exceptional group-like behaviour is
proved directly by explicit parameterizations.

## 1. The triangle surface is additively group-like

Put
\[
 \Phi(a,b,c)=(c-a-b)^2-4ab.
\]
The surface \(\Phi=0\) has the parameterization
\[
 a=x^2,\qquad b=y^2,\qquad c=(x+y)^2. \tag{1}
\]
It also has the branch \(c=(x-y)^2\), corresponding to the other square-root
sign.

### Proposition 1 (quadratic saturation)

For every \(n\), there are sets \(A,B,C\) of sizes \(n,n,2n-1\) for which
\[
 |\{(a,b,c)\in A\times B\times C:\Phi(a,b,c)=0\}|\geq n^2.
\]

### Proof

Take
\[
 A=B=\{1^2,\ldots,n^2\},\qquad
 C=\{2^2,3^2,\ldots,(2n)^2\}.
\]
Every ordered pair \(1\leq x,y\leq n\) gives the distinct triple
\((x^2,y^2,(x+y)^2)\). \(\square\)

Thus a generic point--surface incidence estimate cannot improve the
quadratic scale on this particular surface.  It is exactly an additive-group
surface after adjoining square roots.

## 2. Four triangles do not ensure one-dimensional consistency

Let \(a_{ij}\) denote a proposed squared distance on the edge \(ij\) of
\(K_4\), with vertices \(0,1,2,3\).  Anchor at vertex \(0\) and define
\[
 g_{ij}=\frac{a_{0i}+a_{0j}-a_{ij}}2,
 \qquad 1\leq i<j\leq3. \tag{2}
\]
For actual real heights \(x_0,x_1,x_2,x_3\),
\[
 g_{ij}=(x_i-x_0)(x_j-x_0). \tag{3}
\]

The triangle equation on \(\{0,i,j\}\) says only
\[
 g_{ij}^2=a_{0i}a_{0j}. \tag{4}
\]
It determines the absolute value of \(g_{ij}\), but not a globally coherent
choice of its sign.

### Theorem 2 (\(K_4\) sign-cocycle identity)

Every squared-distance six-tuple from four real points satisfies
\[
\begin{aligned}
 &(a_{01}+a_{02}-a_{12})
  (a_{01}+a_{03}-a_{13})
  (a_{02}+a_{03}-a_{23})\\
 &\hspace{45mm}=8a_{01}a_{02}a_{03}. \tag{5}
\end{aligned}
\]
Equivalently,
\[
 g_{12}g_{13}g_{23}=a_{01}a_{02}a_{03}. \tag{6}
\]

Conversely, if \(a_{01},a_{02},a_{03}>0\), the three anchored triangle
conditions (4) together with (6) are sufficient for the six values to be
squared distances of four real points.

### Proof

Equation (3) gives
\[
\begin{aligned}
 g_{12}g_{13}g_{23}
 &=(x_1-x_0)^2(x_2-x_0)^2(x_3-x_0)^2\\
 &=a_{01}a_{02}a_{03}.
\end{aligned}
\]
Multiplying by \(2^3\) gives (5).

For the converse, put
\[
 t_1=\sqrt{a_{01}},\qquad
 t_2=g_{12}/t_1,\qquad
 t_3=g_{13}/t_1.
\]
The triangle identities give \(t_i^2=a_{0i}\).  Using (6) and
\(g_{23}^2=a_{02}a_{03}\) gives \(t_2t_3=g_{23}\).  Hence, for all
\(1\leq i<j\leq3\),
\[
 a_{ij}=a_{0i}+a_{0j}-2g_{ij}=(t_i-t_j)^2.
\]
The points \(0,t_1,t_2,t_3\) realize the six values. \(\square\)

### Proposition 3 (smallest triangle-only obstruction)

The six ordinary edge lengths
\[
 d_{01}=d_{02}=d_{13}=d_{23}=1,\qquad
 d_{03}=d_{12}=2 \tag{7}
\]
make every one of the four triangles degenerate, so their squares satisfy
all four triangle equations.  Nevertheless, they are not distances of four
points on a line and violate (5).

### Proof

Every triangle has edge lengths \(1,1,2\).  If four line points realized
(7), place vertex \(0\) at zero.  Vertices \(1,2\) must both lie at distance
one from zero and at distance two from one another, so they occupy \(-1,1\).
Vertex \(3\) must be at distance two from zero, but neither choice \(-2,2\)
is at distance one from both \(-1\) and \(1\).

Algebraically, the three anchored Gram entries are
\[
 g_{12}=-1,\qquad g_{13}=g_{23}=2.
\]
Their product is \(-4\), whereas
\(a_{01}a_{02}a_{03}=4\), contradicting (6). \(\square\)

This four-cycle metric is the minimum sign-cocycle obstruction: triangle
compatibility fixes edge-length magnitudes, while (5) enforces parity of the
three anchored signs.

## 3. \(K_4\) compatibility is also group-like

Once signs are retained, a valid six-tuple is parameterized by three signed
differences from an anchor:
\[
 t_i=x_i-x_0,\qquad
 a_{0i}=t_i^2,\qquad
 a_{ij}=(t_i-t_j)^2. \tag{8}
\]

### Theorem 4 (support lower bound and sharp cubic scale)

Let \(Z_0,Z_1,Z_2,Z_3\subset\mathbb R\) have \(m\) elements each.  The six
squared-difference sets contain at least
\[
 \frac{m^3}{8} \tag{9}
\]
distinct compatible \(K_4\) six-tuples arising from point quadruples.
This cubic order is sharp up to constants.

### Proof

There are \(m^4\) point quadruples.  Fix one compatible six-tuple.  The edge
value \(a_{01}\) has at most \(2m\) ordered representations
\((x_0,x_1)\).  For each fixed \(x_0\), the equations
\((x_0-x_2)^2=a_{02}\) and \((x_0-x_3)^2=a_{03}\) give at most two choices
each.  Hence one six-tuple has at most \(8m\) point representations, proving
(9).

For sharpness, take all four sets equal to
\(\{1,\ldots,m\}\).  Translation of a point quadruple does not change its
six squared differences.  The tuple is determined by the three signed
differences \(x_i-x_0\), each lying in an interval of \(2m-1\) integers.
Thus there are at most \((2m-1)^3=O(m^3)\) six-tuples. \(\square\)

Likewise, the triangle lower bound \(m^2/4\) from
`SQUARED_DIFFERENCE_REALIZABILITY.md` is sharp up to constants for common
arithmetic progressions.

## 4. Exact exponent ledger

In the balanced geometric-radius regime,
\[
 L\asymp m\asymp F^{1/2}.
\]
Summing the representation-level support bounds over labelled radius
subsets gives:

\[
\begin{array}{c|c|c|c}
\text{configuration}&\text{index choices}&\text{support per choice}
 &\text{raw labelled total}\\ \hline
\text{triangle}&\Theta(L^3)&\Omega(m^2)&\Omega(L^3m^2)=\Omega(L^5)\\
K_4&\Theta(L^4)&\Omega(m^3)&\Omega(L^4m^3)=\Omega(L^7).
\end{array}
\]

These totals do not contradict a small parameter-line count.  The edge-value
vertices are labelled by their radius pair and product parameter; different
triangles and \(K_4\)'s may reuse the same local value patterns without being
identified as the same hypergraph vertices.  Moreover, the additive
parameterizations (1) and (8) attain exactly the quadratic and cubic support
orders.

At the original critical scale \(L\asymp m\asymp N^{3/10}\), the raw totals
are \(N^{3/2}\) and \(N^{21/10}\), respectively, but their matching
group-like capacities have the same exponents.  Hence neither count yields a
fixed-power saving.

## 5. Remaining combined target

The new \(K_4\) identity eliminates triangle-only sign assignments such as
(7), but compatibility by itself is saturated.  A successful next lemma must
use both:

1. small shifted unions inside many product fibres, which force the
   correlation mass from `HIGH_ENERGY_OVERLAP_STABILITY.md`; and
2. the sign-consistent parameterization (8) across \(K_4\)'s sharing original
   radius vertices.

Equivalently, it must prove that Hadamard-like diffuse overlap cannot be
maintained simultaneously with the rank-one anchored Gram identities (4)
and (6) on a positive-density family of original-radius \(K_4\)'s.

No such combined correlation--cocycle inequality is proved here.

## 6. Verification

`verify_triangle_k4_compatibility.py` checks the surface parameterization,
the obstruction (7), the Gram identity, the support lower bound, and
quadratic/cubic saturation on exact integer examples.
