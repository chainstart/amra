# Universal outside-stability of a forest replacement

Date: 2026-07-30

## Statement

Let \(B\) be a finite set of boundary vertices.  Let \(F\) and \(F'\) be
local forests whose local internal vertices are disjoint from every external
graph except at \(B\); local and external edge sets are disjoint.  Write
\(\pi_B(F)\) for the partition of \(B\) induced by connectivity in \(F\).

Call the replacement \(F\mapsto F'\) **universally outside-stable** if, for
every external forest \(H\) meeting the local graphs only in \(B\),
\[
 F\cup H\text{ is a forest}
 \quad\Longrightarrow\quad
 F'\cup H\text{ is a forest}.                         \tag{1}
\]

Then
\[
\boxed{
 F\mapsto F'\text{ satisfies (1)}
 \iff
 \pi_B(F')\text{ refines }\pi_B(F).
}                                                       \tag{2}
\]

Here refinement means that every pair of boundary vertices connected in
\(F'\) is already connected in \(F\).  The statement assumes, as part of
the local replacement contract, that \(F'\) itself is a forest; this is also
forced by (1) by taking \(H\) empty.

For a pair of coloured forests, a local replacement is universally
outside-stable **for per-colour acyclicity** exactly when (2) holds
separately in each colour, provided the admissible external edge sets are
disjoint from both the source and target local edge sets.  If the coloured
objects are additionally required to have disjoint underlying edge
supports, preservation of that cross-colour condition is a separate local
support contract; it is not detected by the two boundary partitions.

## Proof

For two forests \(X,Y\) meeting only in boundary vertices, form the bipartite
component-incidence multigraph \(I(X,Y)\).  Its left vertices are the
components of \(X\), its right vertices are the components of \(Y\), and
each shared boundary vertex contributes one incidence edge between its two
components.  Alternating paths inside components show
\[
 X\cup Y\text{ is a forest}
 \iff
 I(X,Y)\text{ is a forest}.                            \tag{3}
\]
Parallel incidence edges count as a two-cycle, exactly corresponding to an
\(X\)-path and a \(Y\)-path with the same two endpoints.

The edge-disjointness assumption is essential for this formulation.  If
the same underlying edge were allowed in both \(X\) and \(Y\), it would
give two incidences after contraction but only one edge in the ordinary
set-theoretic union.  In an application where an external context is
required to be disjoint only from the source, a target that introduces an
externally occupied edge must therefore be rejected separately before
applying the partition criterion.

Suppose \(\pi_B(F')\) refines \(\pi_B(F)\).  In the incidence graph, passing
from \(I(F,H)\) to \(I(F',H)\) only splits left component vertices and
redistributes their incident boundary edges.  Splitting vertices cannot
create a cycle.  Thus (3) gives (1).

Conversely, suppose \(u,v\in B\) are connected in \(F'\) but not in \(F\).
Let \(H\) be a new two-edge path \(u-w-v\), with \(w\) external.  It joins
two different \(F\)-components, so \(F\cup H\) is a forest.  The unique
\(F'\)-path from \(u\) to \(v\), together with \(u-w-v\), is a cycle.
Hence (1) fails.  This proves (2). \(\square\)

## Consequences for the OPG injection

1. Preserving the boundary component partition is sufficient but stronger
   than necessary; one-way safety permits the target partition to split
   source components.
2. If both a replacement and its local inverse must be universally
   outside-stable for the same class of admissible edge-disjoint contexts,
   the two boundary partitions must be equal.
3. Any fixed local rule that merges two source boundary components in either
   colour necessarily has an external cycle witness of the two-edge-path
   form used above.  Adding more finite \(q\)-layers cannot repair that
   defect.
4. The saturated-\(K_4\) tree replacement is outside-stable because both
   source and target induce the one-block partition on the four terminals.
5. The finite \(q=2,k=7\) completion violates refinement in the red colour.
   Its displayed \(q=3\) triangle \(01,06,16\) is a concrete instance of
   the necessity construction.

Therefore a uniform completion must do one of two things:

- restrict every context-free local move to component-refining replacements,
  with equality whenever a context-free local inverse is required; or
- read and encode the actual external component partition, so that a move
  which is unsafe universally is used only in compatible states.

This characterization does not itself construct the missing injection or
prove Hall expansion.  It is a general obstruction and a design contract
for the next round.  It is an elementary component-incidence lemma; no
independent novelty claim is made for it without a dedicated search of
forest gluing and graphic-matroid exchange literature.

The human proof is independently pressure-tested for
\(|B|=1,\ldots,4\) on every ordered pair of boundary-only local forests
(at \(|B|=4\), 38 forests and \(38^2=1444\) ordered pairs).  For each pair,
the verifier enumerates every edge-disjoint external forest on
\(B\cup\{w\}\), where \(w\) is one new vertex.  This finite audit does not
enumerate local internal vertices or contexts with more than one external
vertex; the general sufficiency direction is supplied by the incidence-graph
proof.  The audit nevertheless represents every boundary partition through
four vertices and contains every two-edge necessity witness \(u-w-v\):

```bash
python3 verify_outside_stability_characterization.py
pytest -q test_verify_outside_stability_characterization.py
```
