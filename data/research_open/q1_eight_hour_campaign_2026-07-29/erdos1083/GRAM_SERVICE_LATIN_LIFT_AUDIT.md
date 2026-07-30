# Gram-service lift audit for the Latin obstruction

Date: 2026-07-30

## Purpose and conclusion

The Latin/transversal construction in
`WEIGHTED_LABELLED_C4_DICHOTOMY.md` is a genuine real representation graph:
it has the endpoint capacities, shared height sets, geometric
squared-distance cell labels and exact KST edge count, while remaining
\(C_4\)-free.  It was not shown that its edges can arise as the two cross
edges of the required Gram services.

This note restores that missing pairing.  Two cross edges can belong to one
service only when:

1. their radius blocks lie on the same radius diagonal
   \(u-y=x-v\);
2. their signed cross shifts \(\lambda,\mu\) and their partner-height
   difference \(\theta\) satisfy one explicit linearized
   difference-of-squares equation.

For distinct original blocks, \(\lambda+\mu\ne0\), and \(\theta\) is
uniquely determined.  Hence one fixed pair of signed cross-cell/radius
types supports at most \(m\) services.  This cap is sharp by a real
two-block translation fan.

The unshifted AP-Latin construction from the preceding round has no
nontrivial service at all.  Its same-product radial gaps are larger than
the entire range of its vertical squared differences.  Thus that explicit
Latin graph does **not** lift to the original service problem.

This does not yet exclude all Latin-type lifts.  Independent translations
of the radius-class height sets can compensate radial gaps without changing
their internal AP energy or the two-cell-per-block property.  The new
global consistency condition is that the uniquely prescribed partner and
hub shifts must be coboundaries on the two endpoint projection graphs.
A complete family would need average cross-edge service degree
\(L^{2/5}\) at \(\eta=1/30\).  No contradiction or positive power surplus
from those coupled cocycles is proved here.

No unconditional distance-exponent improvement is claimed.

## 1. Full service and its two cross edges

Write
\[
\begin{aligned}
 P&=(\rho_u,a), & N&=(\rho_v,z),\\
 P'&=(\rho_x,c),& N'&=(\rho_y,d).
\end{aligned}
\]
A service satisfies
\[
 u+v=x+y,\qquad
 C_{uv}+(a-z)^2=C_{xy}+(c-d)^2,              \tag{1}
\]
where
\[
 C_{ij}=(\rho_i-\rho_j)^2.
\]
Its two cross edges are
\[
 e_-=(P,N'),\qquad e_+=(P',N).               \tag{2}
\]
Give them their actual signed vertical shifts
\[
 \lambda=a-d,\qquad \mu=c-z,                 \tag{3}
\]
and put
\[
 \theta=d-z.                                 \tag{4}
\]
Then the two original vertical differences are
\[
 a-z=\lambda+\theta,\qquad
 c-d=\mu-\theta.                             \tag{5}
\]

The original product equality in (1) is equivalent to
\[
 \boxed{\quad u-y=x-v.\quad}                 \tag{6}
\]
Thus cross edges cannot be paired arbitrarily: their radius blocks
\((u,y)\) and \((x,v)\) must lie on one common diagonal
\[
 \kappa=u-y=x-v.
\]
If their cross product indices are
\[
 p_-=u+y,\qquad p_+=x+v,
\]
then
\[
 p_-\equiv p_+\pmod2,\qquad
 u+v=x+y=\frac{p_-+p_+}{2}.                  \tag{7}
\]
Moreover \((p_-,p_+,\kappa)\) recovers all four radius indices.

## 2. The service-pair equation

Substitution of (5) into (1) gives
\[
 C_{uv}-C_{xy}+\lambda^2-\mu^2
 +2\theta(\lambda+\mu)=0.                    \tag{8}
\]

### Lemma 1 (unique partner shift)

Suppose the two original radius blocks \((u,v)\) and \((x,y)\) are
distinct and have geometric radii.  Then a service necessarily has
\[
 \lambda+\mu\ne0
\]
and
\[
 \boxed{\quad
 \theta
 =
 \frac{C_{xy}-C_{uv}-\lambda^2+\mu^2}
      {2(\lambda+\mu)}.
 \quad}                                      \tag{9}
\]

### Proof

Equation (9) follows from (8) when the denominator is nonzero.  If
\(\lambda+\mu=0\), the two squared vertical terms in (1) are equal for
every \(\theta\), so (1) requires \(C_{uv}=C_{xy}\).  The blocks have the
same product index by (1).  For geometric radii, product and radial offset
determine the unordered radius pair:
\[
 (\rho_i+\rho_j)^2=C_{ij}+4\rho_i\rho_j.
\]
Thus equality of offsets makes the two blocks identical, contrary to the
hypothesis. \(\square\)

The corresponding hub-height difference is also fixed:
\[
 c-a=\mu-\lambda-\theta.                     \tag{10}
\]
Therefore a paired signed cross-cell type prescribes simultaneous
translations on both endpoint sides.

### Corollary 2 (sharp multiplicity cap)

Fix the four radius blocks and the two signed cross shifts
\(\lambda,\mu\).  At most \(m\) actual services use this paired type.

### Proof

Lemma 1 fixes \(\theta\).  The partner endpoints must satisfy
\[
 d-z=\theta.
\]
There are at most \(m\) such ordered pairs because \(d\) determines \(z\)
and each partner height set has size at most \(m\).  Equations (3) then
determine \(a\) and \(c\). \(\square\)

This is stronger than multiplying marginal cell representations: it keeps
the endpoint gluing and the diagonal radius condition.  It is still only a
linear cap, and Section 5 shows it is exact.

## 3. A diameter forbidden pattern

Let all height coordinates under consideration lie in a real interval of
diameter \(H\).  Then every vertical squared difference lies in
\([0,H^2]\).  Consequently two distinct same-product radius blocks cannot
form a service when
\[
 |C_{uv}-C_{xy}|>H^2.                        \tag{11}
\]
This is a forbidden block pair, independent of how its point pairs are
selected.

For geometric radii \(\rho_j=B^j\), the gap is explicit.  Suppose
\[
 x=u+\Delta,\qquad v=y+\Delta,\qquad
 \Delta\ge1.
\]
Then \(u+v=x+y\), and direct cancellation gives
\[
\begin{aligned}
 C_{u,v}-C_{x,y}
 &=(B^{v}-B^u)^2-(B^y-B^x)^2\\
 &=(B^{2\Delta}-1)(B^{2y}-B^{2u}).           \tag{12}
\end{aligned}
\]
When partner indices lie strictly above hub indices, (12) is positive and
rapidly increasing.  Combining (11)--(12) gives an exact obstruction,
not merely an asymptotic heuristic.

The hypothesis in (11) is global height diameter.  The original problem
does not bound that diameter: translating different radius classes far
apart can invalidate (11).  Thus the forbidden pattern kills the explicit
unshifted Latin model but not all translated variants.

## 4. The unshifted Latin model does not lift

Recall the prime-field graph
\[
\begin{aligned}
 H&=\{(s,x):0\le s<U,\ x\in\mathbb F_q\},\\
 N&=\{(p,b):p,b\in\mathbb F_q\},\\
 (s,x)&\sim(p,b)
 \quad\Longleftrightarrow\quad
 x=ps+b\pmod q.
\end{aligned}                                \tag{13}
\]
Embed every field element as its representative in
\(\{0,\ldots,q-1\}\), and give every radius class exactly that real height
set.  Put the partner radius indices at \(K+p\), with \(K=q+2\), and use
\(\rho_j=B^j\), \(B=10q\).

Take cross edges from distinct radius blocks which satisfy the necessary
diagonal condition (6).  After ordering their hub indices, their original
radius blocks have the form
\[
 (u,y+\Delta),\qquad(u+\Delta,y),
\]
where \(\Delta\ge1\) and \(y\ge K\).  Their radial gap is (12).  Every
height lies in an interval of diameter \(q-1\), whereas
\[
 (B^{2\Delta}-1)(B^{2y}-B^{2u})>(q-1)^2.     \tag{14}
\]
Equation (11) excludes the service.

### Theorem 3 (failure of the unshifted Latin lift)

The real Latin representation graph (13), with the radii and heights just
specified, contains no cross-edge pair arising from two distinct blocks of
one service.  Its only possible service pairings are same-block diagonal
self-collisions, which are not part of the selected cross-block overlap
mass.

For \(q=7,U=4\), exhaustive verification finds

```text
196 Latin cross edges,
32 nontrivial same-diagonal radius-block pairs,
1568 candidate cross-edge pairs,
0 Gram services.
```

Thus the previous Latin construction is a valid obstruction to the
coordinate-graph interface but not a counterexample to the full original
service family.

## 5. A two-block Latin strip does lift

The failure above is not local.  Fix any nontrivial radius parallelogram
\[
 u-y=x-v
\]
and any signed shifts \(\lambda,\mu\) with
\(\lambda+\mu\ne0\).  Let \(\theta\) be (9).  For arbitrary distinct
translations \(A_j\), put
\[
\begin{aligned}
 z_j&=A_j,& d_j&=A_j+\theta,\\
 a_j&=A_j+\theta+\lambda,&
 c_j&=A_j+\mu.
\end{aligned}                                \tag{15}
\]
Every quadruple is a service, and all first cross edges use one fixed cell
while all second cross edges use another.  With \(m\) translations this
gives exactly \(m\) services and uses \(m\) heights in each radius class.

Combinatorially, each cross block is a perfect matching of two \(m\)-sets,
so this is a two-block Latin strip.  It proves Corollary 2 sharp and shows
that any global anti-Latin result must use competition among many strips
sharing the same height sets.  A proof that merely excludes one radius
parallelogram is impossible.

The verifier uses
\[
 (u,y,x,v)=(0,5,1,6),\qquad
 (\lambda,\mu)=(1,2),\qquad B=2
\]
and obtains \(\theta=-511\); every exact rational identity holds.

## 6. Paired-service cocycles

Treat every service as a directed edge from its first partner coordinate
\((v,z)\) to its second partner coordinate \((y,d)\).  Lemma 1 labels it
by the forced displacement
\[
 \theta=d-z.
\]
On every cycle in this partner-coordinate projection,
\[
 \sum_{\rm cycle}\pm\theta=0.                \tag{16}
\]
The same service gives a directed edge between its hub coordinates with
forced displacement
\[
 \psi=c-a=\mu-\lambda-\theta,
\]
and every hub-coordinate cycle satisfies
\[
 \sum_{\rm cycle}\pm\psi=0.                  \tag{17}
\]

Equations (16)--(17) are simultaneous coboundary conditions.  They are
strictly stronger than:

* the unpaired Latin cross graph;
* the four-edge labelled-\(C_4\) quartic;
* the marginal multiplicities of the two cross cells.

For example, two proposed services using the same ordered partner pair but
having different values from formula (9) are immediately forbidden.
Likewise for their hub pair and (10).  More generally, a cycle whose
formula-derived labels have nonzero signed sum cannot be realized by shared
height sets.

These conditions are automatic after actual service points have been
chosen.  Their potential value is during reconstruction: a proposed
Latin-type pairing must solve both large coboundary systems at once.

## 7. Exact \(\eta=1/30\) ledger

The service and failed-point-moment scales are
\[
 S=L^{10/3-\eta-o(1)},\qquad
 E=L^{3-3\eta-o(1)}.
\]
At \(\eta=1/30\),
\[
 S=L^{33/10-o(1)},\qquad E=L^{29/10-o(1)}.   \tag{18}
\]
A hypothetical Latin lift must therefore use each distinct cross edge in
an average of
\[
 \frac{2S}{E}=L^{2/5-o(1)}                   \tag{19}
\]
services, up to the harmless factor two.  Equivalently, its
service-compatibility graph on cross edges must have average degree
\(L^{2/5-o(1)}\).

This is exactly the zero-surplus point-moment scale:
\[
 \frac{S^2}{E}
 =
 L^{37/10-o(1)}
 =
 L^{11/3+\eta-o(1)}.                         \tag{20}
\]
Thus even a fully lifted near-Latin configuration would saturate, rather
than violate by a power, the desired point-conditioned moment.

Corollary 2 says that the \(S\) services require at least
\[
 S/m=L^{23/10-o(1)}                         \tag{21}
\]
distinct paired signed-cell/radius types.  The number of available pairs
of radius blocks on common diagonals is
\[
 O(LU^2)=L^{14/5+o(1)}.                      \tag{22}
\]
There remains capacity
\[
 L^{14/5-23/10}=L^{1/2}.                    \tag{23}
\]
Hence the new diagonal and multiplicity conditions alone give no counting
contradiction.

Projecting the \(S\) services to partner and hub coordinates gives average
degrees, with multiplicity, of
\[
 S/L^2=L^{13/10-o(1)},\qquad
 S/(UL)=L^{7/5-o(1)},                        \tag{24}
\]
respectively.  Many cycles are unavoidable in these projections, but the
translation fan shows that locally their labels can remain coherent.
What is missing is a bound showing that both cocycles (16)--(17) cannot
remain coherent across the required number of radius diagonals without
expanding \(M\) or producing the anchor-reuse moment.

## 8. Strongest conclusion and precise gap

This round proves a genuinely new global consistency layer:

> A service family is a paired cross-edge graph confined to radius
> diagonals; each paired signed type fixes both a partner displacement and
> a hub displacement, and those labels must be simultaneous coboundaries.

It excludes the exact unshifted real Latin obstruction of the previous
round.  The exclusion has no \(L^\delta\) consequence because:

1. arbitrary class translations can overcome the radial-diameter
   obstruction;
2. one translated two-block strip attains the sharp \(m\)-service
   multiplicity;
3. the available same-diagonal block-pair capacity exceeds the required
   paired-type count by \(L^{1/2}\);
4. exact saturation already places the point moment at, not above, its
   target exponent.

The remaining candidate counterexample is therefore precise: a
**translated Latin service design** with \(L^{33/10-o(1)}\) compatible
edge pairs, \(L^{29/10+o(1)}\) distinct cross edges, average compatibility
degree \(L^{2/5-o(1)}\), and simultaneous partner/hub coboundaries from
(9)--(10).  Constructing it would invalidate the present endpoint route.
Proving it impossible with a power saving would supply the missing
anti-transversal theorem.
