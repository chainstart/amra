# Labelled-C4 algebra and the multiplicity barrier

Date: 2026-07-30

## Purpose

The preceding cross-cell argument reaches a bipartite coordinate graph at
the exact \(C_4\)-free threshold when \(\eta=1/30\).  This note freezes the
four radius-pair labels around a coordinate rectangle, eliminates the signed
square roots from its cocycle, and tests whether the resulting algebraic
constraint supplies the missing labelled-\(C_4\) surplus.

The elimination is explicit.  If the first three adjusted cell values are
fixed, the fourth has at most four choices.  Equivalently, the four values
lie on a quartic hypersurface.  This is a rigorous low-degree
label-completion lemma.

It does not close the campaign.  At \(\eta=1/30\), the resulting
\(O(M^3)\) label-quadruple bound is larger than the trivial point-rectangle
capacity by \(L^{3/10+o(1)}\), while the preceding edge count has zero power
surplus over Kővári--Sós--Turán.  Moreover a shared arithmetic progression
of height coordinates produces \(m^4\) point rectangles although there are
only \(O(m^3)\) compatible label quadruples.  Representation multiplicity
and the capacity of the shared \(Z_i\)'s therefore cannot be discarded.

The construction identifies the structured obstruction: equal opposite
labels contain vertical parallelograms, and their multiplicity is the
additive energy of the height set.  A useful next theorem must either gain
beyond quartic completion or show that near-saturation forces
additive/translation structure which expands another part of the distance
set.

No unconditional distance-exponent improvement is claimed.

## 1. Frozen labels and signed cocycle

Take two hub-coordinate vertices with heights \(a,c\), and two partner
vertices with heights \(z,d\).  Freeze the four radius pairs on the edges,
with radial offsets \(C_{01},C_{21},C_{23},C_{03}\).  For the four full
cell values put
\[
\begin{aligned}
 A&=t_{01}-C_{01}=(a-z)^2,\\
 B&=t_{21}-C_{21}=(c-z)^2,\\
 C&=t_{23}-C_{23}=(c-d)^2,\\
 D&=t_{03}-C_{03}=(a-d)^2.                 \tag{1}
\end{aligned}
\]
The actual signed roots
\[
 x=a-z,\quad y=c-z,\quad w=c-d,\quad v=a-d
\]
obey
\[
 x-y+w-v=0.                                 \tag{2}
\]

### Lemma 1 (four-choice completion)

For fixed nonnegative \(A,B,C\), every compatible \(D\) belongs to
\[
 \left\{
   \bigl(\epsilon_1\sqrt A-\epsilon_2\sqrt B
                  +\epsilon_3\sqrt C\bigr)^2:
   \epsilon_1,\epsilon_2,\epsilon_3\in\{\pm1\}
 \right\}.                                  \tag{3}
\]
This set has at most four distinct members.

### Proof

Equation (2) gives \(v=x-y+w\), which proves (3).  Simultaneously reversing
all three signs negates the expression without changing its square.  The
eight sign patterns therefore form at most four pairs.  On a fixed actual
sign branch the fourth value is unique. \(\square\)

The bound four is sharp: \(A=1,B=4,C=9\) gives
\[
 D\in\{0,4,16,36\}.                          \tag{4}
\]

## 2. Continuous squaring and the explicit quartic

Define
\[
 X=A+B-C-D
\]
and
\[
 F(A,B,C,D)
 =
 \left(4CD-X^2-4AB\right)^2-16X^2AB.         \tag{5}
\]

### Lemma 2 (radical elimination)

For nonnegative \(A,B,C,D\), a signed square-root relation
\[
 \epsilon_1\sqrt A+\epsilon_2\sqrt B+
 \epsilon_3\sqrt C+\epsilon_4\sqrt D=0       \tag{6}
\]
exists if and only if \(F(A,B,C,D)=0\).  In particular every coordinate
rectangle satisfies (5).  For fixed \(A,B,C\), equation (5) is a nonzero
polynomial of degree four in \(D\).

### Proof

After moving two terms to each side and squaring once, choose signs
\(\sigma,\tau\in\{\pm1\}\) so that
\[
 X=2\bigl(\sigma\sqrt{CD}-\tau\sqrt{AB}\bigr).
\]
Isolating one radical and squaring again gives (5).

Conversely, (5) implies
\[
 4CD=\left(X\pm2\sqrt{AB}\right)^2
\]
for one choice of sign.  Taking a square root and choosing the remaining
sign recovers a two-against-two relation of the form (6).  Degenerate zero
radicals cause sign branches to merge but do not affect the equivalence.
Finally, \(X\) is linear in \(D\), and the leading \(D^4\) coefficient of
\(F\) is one, so it is never identically zero in \(D\). \(\square\)

For example, \((a,c,z,d)=(0,5,2,9)\) gives
\[
 (A,B,C,D)=(4,9,16,81)
\]
and \(F=0\).  The unrelated tuple \((1,2,3,4)\) gives \(F=64\).
Continuous squaring remembers the union of all sign branches rather than
the actual branch of a point representation.

## 3. Degenerate label patterns

The four-choice statement includes lower-dimensional cases which must not
be treated as generic.

1. If one of \(A,B,C,D\) is zero, an edge has equal endpoint heights and
   several sign branches merge.
2. An adjacent equality such as \(A=B\) says
   \(|a-z|=|c-z|\).  Either \(a=c\), collapsing the hub coordinates, or
   \[
   2z=a+c,                                   \tag{7}
   \]
   so the partner is their vertical midpoint.  Similarly for \(C=D\).
3. An opposite equality such as \(A=C\), on the compatible equal-sign
   branch, gives
   \[
   a-z=c-d,\qquad a+d=c+z.                   \tag{8}
   \]
   This is a vertical parallelogram.  Similarly for \(B=D\); other sign
   choices give midpoint/reflection variants.
4. Multiple pair equalities lower the effective label dimension but may
   increase point multiplicity.  They must be charged through height-set
   energy, not discarded as a negligible algebraic locus.

Thus the generic case has four nonzero, nonpaired adjusted values and at
most four algebraic completions.  The paired case exposes the additive
structure that can saturate the point count.

## 4. A sharp shared-height obstruction

Fix four radius classes and put the same height set
\[
 Z=\{0,1,\ldots,m-1\}
\]
on all four.  Retain every edge between the relevant pairs of classes.
Every \((a,c,z,d)\in Z^4\) is then a point-level labelled \(C_4\), and (2)
holds identically.  There are exactly
\[
 m^4.                                                     \tag{9}
\]
Every adjusted edge label belongs to
\[
 \{0^2,1^2,\ldots,(m-1)^2\},
\]
so there are only \(m\) adjusted labels per frozen edge class.  Lemma 1
gives at most
\[
 4m^3                                                     \tag{10}
\]
distinct compatible label quadruples, while their representation
multiplicities lift the point count to (9).

The vertical-parallelogram subfamily (8) has cardinality
\[
\begin{aligned}
 E_+(Z)
 &=|\{(a,d,c,z)\in Z^4:a+d=c+z\}|\\
 &=\sum_s r_{Z+Z}(s)^2
   =\frac{2m^3+m}{3}.                                    \tag{11}
\end{aligned}
\]
Arithmetic progressions sharply realize the translation/additive-energy
obstruction while respecting the shared height capacity \(|Z|=m\).

This is a real obstruction inside four frozen radius blocks.  It is not by
itself a construction with small global cell universe \(M\), because other
radius pairs and product fibres may add many geometric cell labels.  Its
valid conclusion is local: a label-only \(O(M^3)\) count cannot replace
representation bookkeeping.

## 5. Exact \(\eta=1/30\) ledger

The established cell-universe bound is
\[
 M\leq L^{8/3+\eta+o(1)}.
\]
Lemma 1 gives the coarse compatible-label bound
\[
 O(M^3)=L^{8+3\eta+o(1)}.                              \tag{12}
\]
At \(\eta=1/30\), this is \(L^{81/10+o(1)}\).

The two hub coordinate classes have capacity
\[
 n_H\leq UL,\qquad U\leq L^{5/6+2\eta+o(1)},
\]
and the partner side has \(n_N\leq L^2\).  Even the trivial ordered
point-rectangle capacity is
\[
 n_H^2n_N^2
 \leq L^{\,2(11/6+2\eta)+4+o(1)}
 =L^{23/3+4\eta+o(1)}.                                 \tag{13}
\]
At \(\eta=1/30\), this is \(L^{78/10+o(1)}\).  Thus (12) is worse than
the trivial point capacity by
\[
 L^{1/3-\eta+o(1)}=L^{3/10+o(1)}.                       \tag{14}
\]

There is no compensating rectangle surplus.  Failure of the desired point
moment forces
\[
 E\gtrsim L^{3-3\eta-o(1)}=L^{29/10-o(1)}
\]
cross point-pair edges.  The \(C_4\)-free KST threshold is
\[
 UL^2\leq L^{17/6+2\eta+o(1)}=L^{29/10+o(1)}.
\]
The edge surplus exponent \(1/6-5\eta\) is exactly zero at
\(\eta=1/30\), so KST supersaturation forces no power-sized rectangle
family from the current lower bound.

## 6. Result and remaining gap

The rigorous gain is:

> After freezing four radius-pair labels, the signed cell cocycle is
> equivalent to the explicit quartic (5), and any three nonnegative
> adjusted cell values admit at most four fourth values.

This gives conclusion (A) only at the distinct-label level.  It falls short
at point level because \(O(M^3)\) exceeds total point-rectangle capacity by
\(L^{3/10+o(1)}\), and because one compatible label quadruple may have high
representation multiplicity.  The shared-AP model has \(m^4\) point
rectangles on \(O(m^3)\) label quadruples.

Conclusion (B) is realized locally: the complete shared-height model
produces many labelled \(C_4\)'s, and its equal-opposite-label portion is
governed by \(E_+(Z)\).  The strong geometry is vertical
translation/parallelogram structure.

A viable next lemma must retain both representation multiplicities of the
four cell labels and the common constraint \(|Z_i|\leq m\) across all
incident cells.  Promising formulations are a weighted quartic-energy
inequality with a structured additive-energy alternative, or a stability
theorem for near-KST coordinate graphs whose edge colours satisfy (5).
