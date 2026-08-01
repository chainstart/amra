# Erdős #1083: a network-scale bounded-cycle dichotomy

Date: 2026-08-01

## 0. Verdict

The fixed-nonzero-difference transverse graph does not merely contain
one cycle of length at most ten.  At the frozen endpoint it contains

\[
 t^{8/9+o(1)}
\]

pairwise edge-disjoint simple cycles of length at most ten.

Consequently one of the following network-scale alternatives holds:

1. there are \(t^{8/9+o(1)}\) edge-disjoint short cycles producing
   nontrivial bounded-support height relations with coefficients in
   \(X-X\); or
2. there are \(t^{8/9+o(1)}\) edge-disjoint coherent short cycles,
   and one of the 36 coherent orientation signatures occurs on
   \(t^{8/9+o(1)}\) of them.

This upgrades the earlier one-cycle lemma to the repeated-cycle input
required by the coherent-cycle classification.  It still does not by
itself close #1083: the cycles are edge-disjoint, not necessarily
vertex-disjoint, and their source labels and additive base potentials
may vary.

## 1. A girth-five-level extremal bound

### Lemma 1 (elementary Moore bound)

Let \(H\) be a simple graph on \(n\) vertices with no cycle of length
at most ten.  Then

\[
 e(H)\le n\bigl(n^{1/5}+1\bigr).
\tag{1.1}
\]

#### Proof

Write \(d=2e(H)/n\) for the average degree.  Iteratively delete a
vertex of degree less than \(d/2\).  The process cannot delete every
vertex: if it did, the total number of edges deleted would be strictly
less than

\[
 n\frac d2=e(H),
\]

although every edge would be deleted exactly once.  Thus a nonempty
subgraph \(H'\) remains with minimum degree at least \(d/2\).

If \(d/2<2\), (1.1) is immediate.  Otherwise perform breadth-first
search from any vertex of \(H'\) through depth five.  No vertex can
occur twice in this search tree, because two root paths of length at
most five would create a cycle of length at most ten.  If
\(d_0=\delta(H')\), the tree contains at least

\[
 1+d_0\sum_{j=0}^{4}(d_0-1)^j
 >(d_0-1)^5
 \ge (d/2-1)^5
\]

vertices.  Hence \(d\le2(n^{1/5}+1)\), and

\[
 e(H)=\frac{nd}{2}\le n(n^{1/5}+1).
\]

This proves the lemma. \(\square\)

## 2. Edge-disjoint short-cycle extraction

### Theorem 2 (quantitative extraction)

Let \(H\) be any simple graph with \(n\) vertices and \(m\) edges.
Then \(H\) contains at least

\[
 \boxed{
 \frac{m-n(n^{1/5}+1)}{10}}
\tag{2.1}
\]

pairwise edge-disjoint simple cycles of length at most ten whenever
the numerator is positive.

#### Proof

As long as the current graph contains a cycle of length at most ten,
choose one such cycle and delete all of its edges.  The chosen cycles
are pairwise edge-disjoint.  The terminal graph has girth greater than
ten, so Lemma 1 leaves at most \(n(n^{1/5}+1)\) edges.  At least

\[
 m-n(n^{1/5}+1)
\]

edges were therefore deleted.  Each chosen cycle deletes at most ten
edges, proving (2.1). \(\square\)

No regularity, expansion, or uniform degree assumption is used here.
In particular, concentration of the original fixed-difference edges
on a small set of high-degree rows does not invalidate the theorem.

## 3. Application to the fixed-difference transverse graph

Use the fixed nonzero difference \(\delta\) supplied by
`TRANSVERSE_NONZERO_DIFFERENCE_THEOREM.md`.  Let \(D_\delta\) be its
directed row graph.  Its endpoint parameters are

\[
 |E(D_\delta)|=M=t^{8/9+o(1)},
 \qquad
 |V(D_\delta)|\le q=t^{13/18+o(1)}.
\tag{3.1}
\]

Forget orientations and merge a possible pair of opposite directed
edges.  The resulting simple graph \(H_\delta\) has

\[
 m\ge M/2=t^{8/9+o(1)}
\tag{3.2}
\]

edges.  Lemma 1's terminal-edge scale is

\[
 q^{6/5}+q
 =t^{13/15+o(1)}+t^{13/18+o(1)}.
\tag{3.3}
\]

The leading exponent has a strict gap:

\[
 \frac89-\frac{13}{15}
 =\frac1{45}>0.
\tag{3.4}
\]

Therefore (2.1) gives

\[
 \boxed{
 C_\delta=t^{8/9+o(1)}}
\tag{3.5}
\]

pairwise edge-disjoint cycles of lengths between three and ten.

The factor \(1/2\) in (3.2), the factor \(1/10\) in (2.1), and every
fixed constant absorbed above are harmless.  Equation (3.4) is the
power saving that prevents the high-girth residual graph from
absorbing a positive proportion of the fixed-difference edges.

## 4. Lifting every undirected cycle back to records

For each edge of an extracted undirected cycle, choose one directed
edge of \(D_\delta\) lying above it, and then choose one coincidence
record witnessing that directed edge.  This choice is legitimate even
if both orientations exist or several tangent pairs project to the
same source-label tuple.

Traverse the cycle in either direction.  Put \(\sigma_k=+1\) when the
chosen directed edge agrees with the traversal and \(\sigma_k=-1\)
otherwise.  If \(a_k\) and \(b_k\) are respectively the labels supplied
at vertex \(k\) by its outgoing and incoming cycle edges, summing the
edge equations gives

\[
 2\rho\sum_k z_k(a_k-b_k)
 =\delta\sum_k\sigma_k.
\tag{4.1}
\]

The \(z_k^2\) terms telescope exactly.  The projection multiplicity
issue found in the legacy proof causes no loss here: only one witness
record is selected for each graph edge, and no injectivity of the map
from records to projected tuples is asserted.

Each cycle now has exactly the dichotomy from
`BOUNDED_TRANSVERSE_CYCLE_THEOREM.md`:

- **noncoherent:** some \(a_k-b_k\ne0\), producing a nontrivial height
  relation supported on at most ten rows;
- **coherent:** every \(a_k=b_k\), forcing
  \(\sum_k\sigma_k=0\) because \(\delta\ne0\), and hence giving the
  bounded arithmetic-potential walk.

At least half of the \(C_\delta\) extracted cycles lie in one branch.
If the coherent branch is the large one, its cycles have lengths
\(4,6,8,10\), and the exhaustive classification in
`COHERENT_CYCLE_CLASSIFICATION_AND_MODEL.md` has only 36 cycle-symmetry
types.  One fixed type therefore occurs at least

\[
 \frac{C_\delta}{72}=t^{8/9+o(1)}
\tag{4.2}
\]

times.

This proves the network-scale dichotomy stated in Section 0.

## 5. What has and has not been gained

The new result supplies exactly the previously missing
\(t^{\Omega(1)}\)-many-cycle input.  It is materially stronger than
the average-degree conclusion:

- the cycles use disjoint graph edges;
- all cycles use the same nonzero tangent difference \(\delta\);
- every cycle has uniformly bounded length;
- in the coherent-heavy branch one normalized sign pattern repeats
  on the full \(t^{8/9+o(1)}\) scale.

The remaining obstruction is now sharply localized.  Edge-disjoint
cycles may share rows, while their source labels \(x\in X\) and base
potential \(F_1\) can change.  A closing lemma must exploit that all
these local charts arise from the same exact row partitions.  Plausible
next targets are:

1. a sunflower or dependent-random-choice extraction giving many
   cycles with controlled row intersections;
2. an energy bound for repeated triples
   \((z,x,F(z,x))\) across one coherent signature;
3. a cycle-space sum that cancels shared edges and produces a shorter
   noncoherent relation; or
4. a proof that a coherent-heavy fixed-difference graph contains a
   large commensurate-height subgraph, contradicting transverse-edge
   status.

No one of these closing statements is claimed here.
