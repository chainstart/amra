# Signed differences and a genuine mod-seven lifting barrier

Date: 2026-07-29

## Purpose

`CYCLE_LIFTING_PARITY_BARRIER.md` exhibits a two-colour obstruction to
lifting four large squared-difference overlaps to one quadruple of height
points.  This note tests whether parity is exceptional.

It is not.  There is an exact mod-seven obstruction in which every selected
edge has density \(2/7\), every selected squared value has average
representation multiplicity \(m\), and yet there is no transversal point
cycle.  The construction also embeds into genuine same-product shifted
correlations.

On the positive side, Fourier analysis gives a precise character obstruction
when a four-set zero-sum count is substantially below random, and a fixed
finite quotient that is coherent across a sufficiently dense active network
can be eliminated by a \(K_{2,t}\) argument.  The missing input is therefore
not arithmetic removal itself: it is a **uniform bounded-order character
model, with compatible coordinates at shared radius vertices**.

## 1. The signed-difference formulation

For a selected squared value \(r>0\), a representation
\[
 (x-y)^2=r
\]
is equivalent to
\[
 x-y=\sigma\sqrt r,\qquad \sigma\in\{-1,1\}. \tag{1}
\]
On a cyclic sequence of four height points, orient the differences as
\[
 d_{01}=z_0-z_1,\quad d_{12}=z_1-z_2,\quad
 d_{23}=z_2-z_3,\quad d_{30}=z_3-z_0.
\]
They necessarily satisfy
\[
 d_{01}+d_{12}+d_{23}+d_{30}=0. \tag{2}
\]
Conversely, four signed differences satisfying (2), together with one
starting height and membership in the four height sets, give a transversal
cycle.  Thus the local obstruction is a zero-sum obstruction, with the
important extra constraints that every difference set is symmetric and the
four partial sums must land in the prescribed height sets.

## 2. An exact mod-seven obstruction

Let \(m=7n\), and put
\[
 Z_0=Z_1=Z_2=Z_3=\{0,1,\ldots,m-1\}.
\]
For \(a\in\{1,2,3\}\), define
\[
 A_a(m)=\{d^2:1\leq d<m,\ d\equiv a\text{ or }-a\pmod7\}. \tag{3}
\]
Select \(A_1,A_1,A_1,A_2\) on the cycle edges \(01,12,23,30\).

### Theorem 1 (genuine seven-colour squared-difference obstruction)

For the selections above:

1. every selected value occurs in the relevant squared-difference set;
2. every representation graph has exactly \(2m^2/7\) ordered edges;
3. every selected value set has exactly \(2m/7\) values;
4. the average representation multiplicity per selected value is exactly
   \(m\); and
5. there is no transversal point \(4\)-cycle.

### Proof

Every residue class modulo seven contains exactly \(n\) members of
\(\{0,\ldots,7n-1\}\).  For one fixed nonzero residue \(c\), there are
\(7n^2=m^2/7\) ordered pairs \((x,y)\) with \(x-y\equiv c\pmod7\).
The two residues \(a,-a\) are distinct, giving \(2m^2/7\) representations.

Among the positive integers \(1,\ldots,7n-1\), each nonzero residue occurs
exactly \(n\) times.  Squaring is injective on positive integers, so (3) has
\(2n=2m/7\) elements.  Their quotient gives average multiplicity \(m\).

If a transversal cycle existed, reducing (2) modulo seven would give
\[
 \epsilon_1+\epsilon_2+\epsilon_3+2\epsilon_4=0\pmod7,
 \qquad \epsilon_i\in\{-1,1\}. \tag{4}
\]
The left side is one of
\[
 -5,-3,-1,1,3,5,
\]
none of which is zero modulo seven.  This is impossible. \(\square\)

This is genuinely finer than parity: all four allowed difference classes
are nonzero modulo seven, and the obstruction distinguishes the symmetric
classes \(\{\pm1\}\) and \(\{\pm2\}\).

## 3. Realization inside shifted block correlations

Use the same geometric radii and disjoint same-sum partner pairs as in the
parity construction:
\[
 (0,7),(7,1),(1,16),(16,0) \tag{5}
\]
for the cycle, and
\[
 (3,4),(2,6),(8,9),(5,11) \tag{6}
\]
for the external pairs.  For \(C_{uv}=(2^u-2^v)^2\), each cycle pair and its
external partner have the same index sum, while
\[
 \Delta_e=C_{\rm cycle,e}-C_{\rm external,e}>0. \tag{7}
\]

Give one endpoint of each external pair a height set containing
\[
 \{\sqrt{\Delta_e+a}:a\in A_e\}
\]
and the other a height set containing zero, then pad both to \(m\) distinct
real heights.  Because \(|A_e|=2m/7<m\), this is possible independently on
the eight distinct external indices.  The two shifted blocks then share
every value in \(C_{\rm cycle,e}+A_e\).

Hence every one of the four genuine correlations has size
\[
 r=\frac{2m}{7}, \tag{8}
\]
while Theorem 1 still prevents a point-level lift on the original cycle.

## 4. Complete exponent ledger

In the balanced regime of `CORRELATION_K4_JOINT_AUDIT.md`,
\[
 m\asymp L,\qquad F\asymp Lm\asymp L^2.
\]
The mod-seven gadget has, on every cycle edge,
\[
 |A_e|=\frac{2m}{7}=\Theta(L),\qquad
 |{\cal R}_e|=\frac{2m^2}{7}=\Theta(L^2),\qquad
 \lambda_e=\frac{|{\cal R}_e|}{|A_e|}=m=\Theta(L). \tag{9}
\]
Thus:

- the shifted overlap exceeds the dichotomy scale
  \(L^{5/6-\eta}\) by \(L^{1/6+\eta}\);
- the representation graph has constant density \(2/7\);
- the average representation multiplicity has the maximum possible order;
- nevertheless the transversal cycle count is exactly zero.

Consequently the strong-pair branch cannot be closed by any lemma using only
overlap size, edge density, or average representation multiplicity.  As in
the parity example, padding the external height sets leaves other product
fibres uncontrolled, so this is not a global small-line-count example.

## 5. What Fourier analysis and arithmetic removal actually give

Let \(G\) be a finite abelian group, let \(B_1,\ldots,B_4\subseteq G\) have
densities \(\alpha_i\), and use normalized Fourier coefficients
\[
 \widehat{1_{B_i}}(\chi)
   =\mathbb E_{x\in G}1_{B_i}(x)\overline{\chi(x)}.
\]
Let
\[
 \tau=\mathbb E_{x_1,x_2,x_3\in G}
 1_{B_1}(x_1)1_{B_2}(x_2)1_{B_3}(x_3)
 1_{B_4}(-x_1-x_2-x_3). \tag{10}
\]

### Lemma 2 (quantitative character obstruction)

If
\[
 \tau\leq(1-\kappa)\alpha_1\alpha_2\alpha_3\alpha_4,
\]
then
\[
 \max_{i,\ \chi\ne1}|\widehat{1_{B_i}}(\chi)|
 \geq
 \sqrt{\kappa}\,
 \max_{\{i,j\}}
 \left(\alpha_i\alpha_j
       \sqrt{\alpha_k\alpha_l}\right)^{1/2}, \tag{11}
\]
where \(\{k,l\}\) is the complementary pair.  In particular, if every
\(\alpha_i\geq\delta\), the right side is at least
\[
 \sqrt{\kappa}\,\delta^{3/2}. \tag{12}
\]

If \(|G|=q\), there is moreover one common nontrivial character satisfying
\[
 \prod_{i=1}^4|\widehat{1_{B_i}}(\chi)|
 \geq
 \frac{\kappa\alpha_1\alpha_2\alpha_3\alpha_4}{q-1}. \tag{13}
\]

### Proof

Fourier inversion expresses (10) as the trivial-character contribution
\(\prod_i\alpha_i\) plus a sum, over nontrivial characters, of products of
the four Fourier coefficients (with harmless conjugations).  The
nontrivial sum therefore has absolute mass at least
\(\kappa\prod_i\alpha_i\).

Put \(\rho=\max_{i,\chi\ne1}|\widehat{1_{B_i}}(\chi)|\).  For any chosen
pair \(\{i,j\}\), bound its two coefficients pointwise by \(\rho^2\), and
apply Cauchy--Schwarz and Parseval to the complementary pair:
\[
 \kappa\prod_s\alpha_s
 \leq \rho^2\sqrt{\alpha_k\alpha_l}.
\]
This is (11), and (12) follows.  If there are only \(q-1\) nontrivial
characters, one summand has magnitude at least the average, proving
(13). \(\square\)

Lemma 2 is a useful inverse statement, but it is weaker than the needed
network theorem:

1. in a growing group, the cancellation may be spread over many characters;
2. (11) forces a large coefficient in at least one of the four sets, not a
   bounded-order common character with compatible phases in all four;
3. different active edges may select different characters;
4. a character on a difference set does not by itself give compatible
   character coordinates on all shared height sets.

The arithmetic removal lemma for one linear equation says that
\(o(|G|^3)\) zero-sum quadruples can be destroyed by deleting \(o(|G|)\)
elements from the four sets.  It does not classify the resulting
zero-sum-free sets as cosets or bounded-order character level sets.
Therefore invoking removal alone leaves precisely the structural step that
the geometry needs.  No BSG conclusion follows merely from a deficit of
four-set zero sums; BSG would additionally require a high-energy/small
sumset hypothesis.

## 6. A fixed finite quotient is globally repairable

Suppose now that every active edge \(uv\) has an exact common
\(\mathbb Z/q\mathbb Z\) coordinate and contains all point pairs whose
coordinate difference lies in one symmetric colour
\(\{\pm a_{uv}\}\).  For odd \(q\), there are
\[
 h=(q-1)/2
\]
possible nonzero symmetric colours.

### Theorem 3 (bounded-quotient network repair)

If the active radius graph contains \(K_{2,h^2+1}\), then some radius
\(4\)-cycle has a transversal point cycle.  If every coordinate class at
every vertex has at least \(\alpha m\) points, that cycle supports at least
\((\alpha m)^4\) transversal point cycles.

### Proof

Write the two-vertex side as \(u,v\).  Each vertex \(w\) on the other side
has the ordered colour pair
\[
 (a_{uw},a_{vw})\in\{1,\ldots,h\}^2.
\]
Among \(h^2+1\) vertices, two, say \(w,w'\), have the same ordered pair.
On the cycle \(u,w,v,w'\), choose opposite signs on the two edges with the
first colour and opposite signs on the two edges with the second colour.
Their signed sum is zero modulo \(q\).  Choosing a starting coordinate then
determines compatible coordinates around the cycle.  The class-size
hypothesis supplies the stated point choices. \(\square\)

A \(K_{2,t}\)-free graph on \(L\) vertices has
\[
 O(\sqrt t\,L^{3/2}+tL)
\]
edges, by counting pairs of neighbours.  Hence a fixed \(q\), common across
the network, is excluded once the active-edge count has a fixed-power excess
over \(L^{3/2}\).

For the special mod-seven single-colour model, one can sharpen
\(K_{2,10}\) to \(K_{2,3}\).  A four-edge colour multiset from
\(\{1,2,3\}\) fails to have a signed zero modulo seven exactly when it is
one of
\[
 1112,\qquad2223,\qquad3331. \tag{14}
\]
If two columns of a \(2\times3\) colour matrix form a bad multiset, one
column is monochromatic in the repeated colour and the other has that colour
and its successor in (14).  Requiring the same with a third column makes
the last two columns have two copies of each of two colours, which has an
immediate signed zero.  Thus not all three \(4\)-cycles can be frustrated.

## 7. Exact remaining input

The current high-correlation machinery can rule out a **fixed, coherent**
finite quotient in the diffuse-network branch, but it cannot establish that
model.  It also gives no network density at all in the strong-pair branch.

A sufficient next lemma would be:

> From many shifted squared-difference correlations of size
> \(r\), extract a fixed \(q=O(1)\), a common coordinate
> \(\phi_u:Z_u\to\mathbb Z/q\mathbb Z\) on every vertex of a subgraph with
> \(\gg L^{3/2+\epsilon}\) edges, and one symmetric colour per retained
> edge containing \(\gg r\) selected representations.

Theorem 3 would then produce a cycle-consistent lift.  Fourier deficit and
arithmetic removal do not currently supply the common bounded order, the
vertex-wise coordinate compatibility, or the required retention across
many edges.  These three requirements are one synchronization input, and
they are the exact obstruction left by this audit.

## 8. Verification

`verify_signed_difference_finite_quotient.py` checks the exact mod-seven
counts, absence of transversal cycles, the shifted-correlation realization,
the classification (14), and the \(K_{2,3}\) repair over all \(3^6\)
edge-colourings.

For arithmetic removal over finite abelian groups, see D. Král', O. Serra
and L. Vena, *On the Removal Lemma for Linear Systems over Abelian Groups*,
arXiv:1106.4243, which includes the single-equation setting used here.
