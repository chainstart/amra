# Exact one-sum/block reduction for forest Rayleigh differences

Status: **PROVED STRUCTURAL REDUCTION; NOVELTY NOT CLAIMED**.

Suppose `G=G1 union G2`, the edge sets are disjoint, and the vertex sets
intersect in at most one vertex.  Every cycle of `G` lies entirely in one
side.  Therefore an edge set is a forest of `G` exactly when its restrictions
to both sides are forests, and

\[
F_G(\mathbf x)=F_{G_1}(\mathbf x)F_{G_2}(\mathbf x).
\tag{1}
\]

For marked edges in different sides, (1) makes the two inclusion indicators
independent and the Rayleigh difference is zero.  If both marked edges lie in
`G1`, direct differentiation gives

\[
\Delta_G(e,f)=F_{G_2}^2\Delta_{G_1}(e,f).
\tag{2}
\]

Iterating over the block-cut tree proves:

1. edge negative correlation for a graph is equivalent to the property on
   each nontrivial 2-connected block;
2. any counterexample has a counterexample block containing both marked
   edges;
3. a minimal counterexample may be assumed 2-connected, after deleting
   irrelevant isolated vertices and one-edge blocks.

The algebraic kernels of (1)--(2) are checked in
`opg_one_sum_block_probe.lean`.  Combined with the explicit cycle-block
calculation in `CACTUS_WEIGHTED_THEOREM.md`, this proves the weighted theorem
for all cactus graphs.

This is a genuine arbitrary-host simplification but not the campaign's
required arbitrary-host closure: general 2-connected blocks remain.
