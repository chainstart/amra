# Representation-rich cross cells

Date: 2026-07-30

## Purpose

`GRAM_RECTANGLE_MOMENT.md` reduces the unresolved branch to a visited
product-fibre distance cell
\[
 \xi=(p,t)
\]
with more than
\[
 V_0=L^{1/3-4\eta-o(1)} \tag{1}
\]
actual point-pair representations.  This note determines the exact
one-cell geometry and asks whether such richness forces parameter-line
expansion or the common-anchor network.

It does neither at one-cell level.  A cell is a ruled translation variety:
for each radius block in the product matching there are at most two fixed
difference vectors, and every representation is an arbitrary translate of
one of them.  Every admissible multiplicity profile up to height-set
capacity is realizable over the reals inside one product fibre.  In
particular, \(V_0\ll U\) at the current hub scale, so the representations
may occupy different blocks with no repeated ruling and no common anchor.

There is also an exact global counting barrier.  If the point-conditioned
moment is below its target, Cauchy forces at least
\[
 E\gtrsim L^{3-3\eta-o(1)} \tag{2}
\]
distinct cross point-pair edges.  The graph is bipartite between
\(O(Um)\) hub-coordinate vertices and \(O(Lm)\) partner-coordinate
vertices.  If it is \(C_4\)-free, Kővári--Sós--Turán gives
\(E\lesssim UL^2\).  Consequently failure of the target forces either a
coordinate rectangle or \(U\gtrsim L^{1-3\eta}\).  At
\(\eta=1/30\), the latter exactly equals the existing hub upper bound
\(L^{5/6+2\eta}=L^{9/10}\); there is no power surplus.  A coordinate
rectangle is still insufficient unless its four cell labels have additional
equality or reuse.

No global real construction simultaneously realizing all these rich cells
and small \(M\) was found.  The missing input is now precise: different
cells reuse the same height sets, so their signed translation labels must
sum to zero around every coordinate cycle.  This cross-cell cocycle is not
visible in the one-cell fan, the value-level Gram energy or ordinary graph
density.

No unconditional exponent improvement is claimed.

## 1. Exact one-cell parameterization

Let
\[
 \rho_j=Tq^j,\qquad q\geq2,
\]
and fix a product exponent \(p\).  A radius block in the fibre is
\[
 (i,j),\qquad i+j=p.
\]
Put
\[
 K=\rho_i\rho_j=T^2q^p,\qquad
 C_{ij}=(\rho_i-\rho_j)^2.
\]
An actual height pair \((a,z)\in Z_i\times Z_j\) represents the cell
\((p,t)\) exactly when
\[
 C_{ij}+(a-z)^2=t. \tag{3}
\]
Hence the block is inactive if \(t<C_{ij}\), and otherwise
\[
 a-z=\epsilon\,\delta_{ij}(t),\qquad
 \delta_{ij}(t)=\sqrt{t-C_{ij}},\quad
 \epsilon\in\{+1,-1\}. \tag{4}
\]

For a fixed sign, all representations have the form
\[
 (a,z)=(A,A-\epsilon\delta_{ij}(t)). \tag{5}
\]
The free parameter \(A\) is a vertical translation.  Thus one cell is a
disjoint union of at most two translation rulings per active radius block.

The semialgebraic geometry is equally explicit.  Put
\[
 X=\frac{\rho_i+\rho_j}{2},\qquad
 H=\frac{\rho_i-\rho_j}{2},\qquad D=a-z.
\]
Then
\[
 X^2-H^2=K,\qquad 4H^2+D^2=t. \tag{6}
\]
The first equation is the fixed-product hyperbola and the second puts the
difference vector \((2H,D)\) on the circle of radius \(\sqrt t\).
For every intersection direction, the segment midpoint
\[
 \left(X,\frac{a+z}{2}\right)
\]
moves freely on a vertical line.  The endpoints themselves need not be
concyclic; the common circle is in difference-vector space.

## 2. Sharp one-cell fan inequalities

Let \(B=B(\xi)\) be the number of active radius blocks, and write
\[
 r_{i,\epsilon}
=|\{(a,z):a-z=\epsilon\delta_{i,p-i}(t)\}|.
\]
Then
\[
 V=\sum_{i,\epsilon}r_{i,\epsilon}. \tag{7}
\]
There are at most \(2B\) nonzero terms, so
\[
\begin{aligned}
 {\cal F}(\xi)
 :=\sum_{i,\epsilon}r_{i,\epsilon}^2
 &\geq\frac{V^2}{2B},\\
 \mu(\xi):=\max_{i,\epsilon}r_{i,\epsilon}
 &\geq\frac{V}{2B}. \tag{8}
\end{aligned}
\]
Both inequalities are sharp up to rounding by distributing the
representations evenly among the rulings.

Every cross block produced by the low--low hub orientation has a hub
endpoint.  Since blocks in one product fibre form a matching,
\[
 B\leq U. \tag{9}
\]
Consequently
\[
 {\cal F}(\xi)\geq\frac{V^2}{2U},\qquad
 \mu(\xi)\geq\frac{V}{2U}. \tag{10}
\]

At the smallest permitted hub scale,
\[
 U\geq L^{2/3-\eta/2-o(1)},
\]
while the rich-cell threshold is (1).  Their ratio is
\[
 \frac{V_0}{U}
\leq L^{-1/3-7\eta/2+o(1)}. \tag{11}
\]
Thus (10) does not even force two representations on one signed ruling.
The cell can place one representation in each of \(V_0\) different hub
blocks.  Neither a translation fan nor a repeated numerical anchor follows.

## 3. One-cell universality over the reals

### Theorem 1

Fix one geometric product fibre, one \(t\) larger than the radial offsets
of \(B\) matching blocks, and nonnegative integers
\[
 r_{i,+}+r_{i,-}\leq m.
\]
There are real height sets of size at most \(m\) on the \(2B\) radius
classes for which the cell \((p,t)\) has at least the prescribed signed
multiplicities.  The translation parameters may be chosen generically so
that no numerical height is shared between different radius classes.

### Proof

For every block \(ij\) and sign \(\epsilon\), choose
\(r_{i,\epsilon}\) generic real parameters \(A_{i,\epsilon,k}\).  Put
\[
 A_{i,\epsilon,k}\in Z_i,\qquad
 A_{i,\epsilon,k}-\epsilon\sqrt{t-C_{ij}}\in Z_j. \tag{12}
\]
The product-fibre blocks form a matching, so no radius class receives
prescriptions from another block.  Each receives at most \(m\) coordinates.
There are only finitely many unwanted coordinate coincidences and unwanted
opposite-sign representations; generic choices avoid them.  Pad every set
to size \(m\).  Equation (3) verifies all desired representations.
\(\square\)

The theorem is a strict real barrier to every one-cell argument.  It
preserves the exact geometric radii, point coordinates and Gram identities.
It can realize the completely dispersed profile \(r_{i,+}=1\) on \(V\)
blocks, or one vertical-translation fan of size \(V\), whenever the relevant
capacity allows.

## 4. Why the established rich-plane counts do not absorb a fan

A signed ruling of multiplicity \(\mu\) consists of \(\mu\) congruent,
parallel segments translated in height.  Their midpoints have distinct
heights, hence their perpendicular bisectors are parallel distinct lines in
the axial plane, or parallel distinct reflection planes after restoring the
angular coordinates.  They do not give one \(\mu\)-rich plane.

Conversely, a common midpoint height would give a common perpendicular
bisector, but within one signed ruling the map
\[
 A\longmapsto A-\epsilon\delta
\]
is injective and the midpoint height is
\(A-\epsilon\delta/2\).  Distinct representations therefore have distinct
midpoints.  The current rich-plane incidence bound cannot charge
\(\mu\) to one plane.

The dispersed branch is even weaker: it uses different radius blocks,
different difference directions and, by Theorem 1, disjoint numerical
height ranges.  A large \(B\) merely says that many hub endpoints occur in
one product matching; it gives \(B\leq U\), already present in the hub
capacity count.

Thus neither term of the fan dichotomy (8) reconnects to the inherited
rich-plane or common-anchor theorem at threshold (1).

## 5. Cross-cell representation graph and the exact \(C_4\) threshold

Let
\[
 {\cal V}=\{(i,a):a\in Z_i\},\qquad
 |{\cal V}|=N=\Theta(Lm)=\Theta(L^2).
\]
Join two coordinate vertices by their unique cell label
\[
 (i+j,C_{ij}+(a-z)^2). \tag{13}
\]
Restrict to cells visited by cross edges of the represented services.  For
such a collection \({\cal C}\), the number of distinct representation
edges is
\[
 E({\cal C})=\sum_{\xi\in{\cal C}}\nu(\xi). \tag{14}
\]

Let \(c(e)\) be the number of service-cross occurrences completed through
one actual edge \(e\).  The point-conditioned moment and total occurrence
mass are
\[
\mathcal R_{\rm pt}=\sum_e c(e)^2,\qquad
\sum_e c(e)=2S. \tag{15}
\]
Therefore
\[
\mathcal R_{\rm pt}\geq\frac{4S^2}{E}. \tag{16}
\]
If the target
\[
\mathcal R_{\rm pt}\gtrsim L^{11/3+\eta-o(1)}
\]
fails, (16) forces
\[
\begin{aligned}
 E
 &\gtrsim
 L^{2(10/3-\eta)-(11/3+\eta)-o(1)}\\
 &=L^{3-3\eta-o(1)}. \tag{17}
\end{aligned}
\]

Every cross edge has one hub-coordinate endpoint.  Thus the two sides of
the graph have sizes
\[
 n_H\leq Um=O(UL),\qquad n_N\leq Lm=O(L^2). \tag{18}
\]
If the graph contains no \(K_{2,2}\), count pairs of hub neighbours at each
partner vertex to obtain
\[
 E\leq n_H\sqrt{n_N}+n_N
\lesssim UL^2+L^2. \tag{19}
\]
Combining (17)--(19), failure of the point moment in the \(C_4\)-free branch
requires
\[
 U\gtrsim L^{1-3\eta-o(1)}. \tag{20}
\]
The established hub upper bound is
\[
 U\lesssim L^{5/6+2\eta+o(1)}. \tag{21}
\]
The exponent surplus in (20) over (21) is
\[
 \frac16-5\eta. \tag{22}
\]
It is positive for \(\eta<1/30\), zero at the campaign endpoint
\(\eta=1/30\), and negative beyond it.

Hence at \(\eta=1/30\), a failed point moment with no coordinate rectangle
forces simultaneous saturation:
\[
 E=L^{29/10+o(1)},\qquad U=L^{9/10+o(1)}, \tag{23}
\]
as well as near equality in the bipartite \(C_4\)-free bound.  This is much
more rigid than one rich cell, but it has no power margin.

If a \(K_{2,2}\) occurs, its two hub points and two partner points satisfy
the exact signed cocycle and Gram rectangle.  However, the four edges may
carry four unrelated cells.  A coloured rectangle does not put either
partner on the perpendicular bisector of the two hub points unless the two
incident distance labels agree.  Thus an arbitrary coordinate rectangle
does not yet produce a rich reflection plane or a common anchor.

Any successful endpoint argument must therefore use numeric cell labels
and real order, not only representation degrees or uncoloured
\(C_4\) supersaturation.

## 6. The missing cross-cell cocycle

Orient a representation edge from \((i,a)\) to \((j,z)\) and attach its
signed displacement
\[
 \lambda_e=a-z
=\epsilon_e\sqrt{t_e-C_{ij}}. \tag{24}
\]
For every coordinate cycle
\[
 v_0v_1\cdots v_{\ell-1}v_0
\]
one necessarily has
\[
 \sum_{r=0}^{\ell-1}\lambda_{v_rv_{r+1}}=0. \tag{25}
\]
The first nontrivial rectangle is
\[
 \lambda_{01}-\lambda_{21}
+\lambda_{23}-\lambda_{03}=0. \tag{26}
\]
Squaring and combining (26) with the radial offsets recovers the vertical
part of the Gram rectangle.

Inside one product fibre the radius blocks form a matching, so Theorem 1
creates no cross-block coordinate cycle and (25) is vacuous.  Across many
cells, the same \(Z_i\) is reused and (18) couples their independently
chosen square roots.  This is exactly what the Latin anchor tensor and the
one-cell fan omit.

A sufficient next theorem would be a **labelled-cycle surplus**:

> A representation graph with the edge mass forced by (17), the geometric
> labels (24), and all shared height sets either has
> \(M>L^{8/3+\eta}\), or contains
> \(L^{1/3+2\eta-o(1)}\) more zero-sum labelled rectangles than the
> unlabelled extremal bound predicts.

No such theorem is proved here.

## 7. Status of a global barrier

Theorem 1 gives a genuine real realization of every individual rich cell.
The vertical-translation fan from the previous round gives a genuine real
service family with quadratic cell energy and only linear
point-conditioned energy.  The graph ledger (17)--(23) shows that failure
of the target forces either a coordinate rectangle or simultaneous
near-extremality of the hub and \(C_4\)-free capacities.

However, these pieces cannot simply be pasted together: a radius class
appears in many product fibres and must keep one \(m\)-point set \(Z_i\).
Pasting independent one-cell constructions violates the cycle equations
(25).  No global real point set with simultaneously

1. \(M\leq L^{8/3+\eta}\);
2. the required overlap service mass;
3. many cells above (1); and
4. all shared height sets

was found.  Such a construction would address the central unresolved
consistency problem, not merely this audit.

Therefore the representation-rich branch remains open, but its missing
ingredient is narrowed from “Gram geometry” to the labelled cross-cell
cocycle (25).  One-cell fan bounds, rich-plane incidence, common-anchor
extraction and unlabelled DRC are quantitatively insufficient.

No unconditional exponent or publication claim is made.

## 8. Verification

`verify_representation_rich_cross_cell.py` checks the ruled-cell
parameterization, fan-energy inequalities, an algebraic one-cell
multiplicity certificate for geometric radii, and every exponent in the
hub/C4 ledger.
