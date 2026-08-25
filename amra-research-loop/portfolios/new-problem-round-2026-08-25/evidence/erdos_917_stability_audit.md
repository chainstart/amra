# Erdős #917 — stability-route audit for the \(k=6\) case

## Exact edge-witness lemma

If \(G\) is 6-chromatic and deleting every edge lowers its chromatic number,
then for every edge \(uv\) there is a 5-colouring of \(G-uv\), and in every
such 5-colouring \(u\) and \(v\) receive the same colour. Otherwise that
colouring would also be a 5-colouring of \(G\).

Equivalently, for each edge there is a partition into five sets such that all
edges other than \(uv\) go between parts and \(uv\) is the only edge internal
to its part. This is exact but the partition depends on the chosen edge.

## Why an unannotated regularity reduction loses criticality

Let

\[
G_m=C_{2m+1}\vee C_{2m+1}
\]

be the join of two disjoint odd cycles. Then

\[
|V(G_m)|=4m+2,\qquad
|E(G_m)|=(2m+1)^2+2(2m+1)=4m^2+8m+3.
\]

The chromatic number of a join is additive, so \(\chi(G_m)=3+3=6\).
Every internal cycle edge is critical because deleting it turns that cycle
into a bipartite path, reducing the join chromatic number to \(2+3=5\).
For a cross edge \(uv\), colour each odd cycle so that its specified endpoint
is the sole vertex using a third colour; use disjoint two-colour palettes on
the remaining paths and share the third colour between \(u\) and \(v\). This
is a 5-colouring of \(G_m-uv\). Hence every edge is critical.

But deleting only the \(4m+2=o(|V|^2)\) cycle edges leaves the balanced complete
bipartite graph \(K_{2m+1,2m+1}\). Any ordinary dense reduced graph that ignores
an \(o(n^2)\) set of edges therefore sees only a bipartite skeleton, while the
discarded sparse edges carry all four additional units of chromatic demand.

Consequently the proposed step “apply regularity, then enumerate finite
critical colouring patterns of the reduced graph” is not faithful: the
unannotated reduced graph need not retain either 6-chromaticity or edge
criticality. The Dirac extremisers already witness the loss.

## Required replacement bridge

A viable stability theorem must keep a sparse chromatic annotation on each
dense part. The target shape suggested by the extremiser is:

1. a dense skeleton asymptotically close to a balanced complete bipartite
   graph;
2. each side contains a sparse 3-critical core;
3. almost all cross edges form the join, with an edge-by-edge witness rule.

Without a theorem producing this annotated sparse–dense decomposition, a
finite reduced-graph classification cannot close \(f_6(n)\sim n^2/4\).

Decision: `proposed_regular_reduction_killed`; the public problem remains open,
and the annotated bipartite-skeleton theorem is the sole retained route.
