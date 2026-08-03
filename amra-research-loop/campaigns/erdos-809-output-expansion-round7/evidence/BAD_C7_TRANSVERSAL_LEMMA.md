# Bad-C7 trace transversal lemma

## General lemma

Let `G+` be a fixed graph before old-edge deletions, let `D` be the set of
admissible old edges, and let `P` be a fixed collection of repeated-colour
edge pairs.  Let `C(P)` be the simple C7s in `G+` containing both edges of at
least one pair in `P`.  Define the trace hypergraph

```text
H = { E(C) intersect D : C in C(P) }.
```

For every `S subset D`, the graph `G+-S` is C7-safe for all pairs in `P` if
and only if `S` is a transversal of `H`.

Proof.  Deleting edges creates no cycle.  A bad C7 from `G+` survives in
`G+-S` exactly when none of its admissible edges is deleted, equivalently
when `S` is disjoint from its trace.  Hence no bad C7 survives exactly when
`S` meets every trace.  This argument is independent of the size of `S`.

Two consequences are used by the search.

1. If `H` contains the empty trace, no admissible deletion set of any size
   can repair that configuration.  This is an absolute protected-cycle
   obstruction, not merely a lower bound of three or four.
2. Suppose `H` has no empty trace and `|D| >= d`.  If no `d`-element subset
   is a transversal, then the transversal number satisfies `tau(H)>d`.
   Indeed, any transversal with fewer than `d` elements could be extended
   inside `D` to a `d`-element transversal.

The bit-mask implementation is exactly this lemma: one bit represents one
fixed-size subset of `D`; a cycle mask contains precisely the subsets meeting
its trace; intersection over the cycle masks is precisely the set of
fixed-size transversals.

## Finite applications

In the reproduced two-deletion domain, 3,860 of 3,876 assignments have an
empty trace.  The other sixteen have no two-element transversal, so their
transversal number is at least three.

In the new three-deletion domain, 968 of 969 assignments have an empty trace.
The unique unprotected assignment omits `bu,bw,uw`.  Its exact deduplicated
trace hypergraph has 93 traces: twenty-one singleton traces and seventy-two
three-edge traces.  The singleton traces force twenty-one distinct deletion
edges, and those twenty-one edges hit all remaining traces.  Therefore its
transversal number is exactly 21, not merely at least four.

The general lemma is a graph-theoretic equivalence, but these numerical
applications remain finite statements about the locked graph.  They do not
imply that arbitrary hard graphs have protected cycles or large transversal
number, and they do not change the public `1/8` question.
