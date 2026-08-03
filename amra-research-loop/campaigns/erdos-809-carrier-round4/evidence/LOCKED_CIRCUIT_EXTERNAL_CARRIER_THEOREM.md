# Locked-circuit external-carrier theorem

## Statement

Let `G` be a fixed graph with B-shore `B`, let `e={b,c}` be a zero-shore
missing B-edge, and let `T` be `d` defect demands whose outer endpoint set is
exactly `{b,c}`.  Give every demand its full canonical-reserve neighbourhood.
Then every choice of root in its two-point outer support has the same unordered
base `e`, hence every demand has the identical neighbourhood `K(e)`.  Writing
`k=|K(e)|`,

```text
nu(C_G[T,K(e)]) = min(d,k),
delta(C_G[T,K(e)]) = max(0,d-k).
```

Any process composed only of root reversal, alternating rematching along
existing reserve arcs, unions/intersections of demand cuts, or random sampling
of existing arcs preserves this rank and deficiency.  If `d>k`, every
saturating augmentation by actual carriers must contain at least `d-k`
distinct missing B-edges outside `K(e)` and graph-proved legal arcs to them;
the complete augmented incidence graph must still pass every Hall cut.

## Proof

The only two possible roots are `b` and `c`.  In either case the only defect
base pair is the unordered pair `{b,c}=e`.  Canonical reserve determinism says
that `K(e)` depends on `G` and `e`, not on the colour or orientation.  Thus the
carrier incidence graph is the complete bipartite graph from the `d` demands
to the same `k` right vertices.

Its matching rank is `min(d,k)`: no matching can use more than either shore,
and pairing any `min(d,k)` demands with distinct reserve edges attains the
bound.  Therefore its Hall deficiency is `d-min(d,k)=max(0,d-k)`.

Root reversals do not change `e`; alternating paths only change a matching
inside the same incidence graph; uncrossing changes which demand subsets are
named but no neighbourhood; and sampling deletes or selects existing arcs.
None can increase rank.  Finally, a saturated matching for `d>k` uses `d`
distinct right vertices, so at least `d-k` of them lie outside `K(e)`.  Their
mere existence is not sufficient: legality and all augmented Hall inequalities
remain necessary.  This also explains why universal dummies prove only a
comparison min--max statement.

## Consequence for the two survivors

For `M809R4-04`, an actual absorber capable of repairing a locked circuit must
output an edge outside `K(e)` and include the original-graph C7/ownership
certificate licensing that new arc.  A catalogue of rotations, A diagonals,
or multiple witnesses whose outputs remain in `K(e)` has absorber rank at most
`k` regardless of its size.

For `M809R4-10`, a nibble over the original reserve arcs cannot contract the
locked deficiency.  The condition “the graph has many missing B-edges” is not
the relevant antecedent; it must be strengthened to graph-derived legal
neighbourhood expansion beyond each locked `K(e)`, plus a deterministic
all-cut cleanup.  This is still conditional and has not been established in
the hard public branches.

## Exact realization and scope

`graph_realizable_carrier_falsification.py` realizes the theorem with
`d=4`, `k=2` in the exact 14-vertex threshold graph, verifies all C7 and
`L4(2)` conditions, checks all 16 root states, and obtains rank two and
deficiency two.  No Lean is used.

The theorem is an exact negative interface lemma.  It does not construct an
external carrier, close the outer-A gate, or alter the public `1/8` term.

