# Independent proof audit: outside-stable saturated-\(K_4\) repair

Date: 2026-07-30

## Claim checked

In the saturated simple-\(K_4\) deficit class, each source colour restricts
to a spanning tree \(T\) on the four terminals.  Replacing that restriction
by any of the repair trees \(T'\), while leaving every edge incident with an
outside vertex unchanged, preserves acyclicity.  The four listed repair
targets also determine their sources uniquely.

This is a local lemma only.  It is not the missing injection on all negative
forest pairs.

## Acyclicity

Let \(H\) be all same-colour edges having at least one outside endpoint.  It
contains no terminal--terminal edge.  Suppose \(T\cup H\) is a forest.

If one component of \(H\) contained distinct terminals \(u,v\), its unique
\(H\)-path from \(u\) to \(v\), together with the unique \(T\)-path from
\(u\) to \(v\), would form a cycle.  Therefore every component of \(H\)
contains at most one terminal.

Contract every component of \(H\).  The four terminals remain in four
distinct contracted vertices.  Since \(T'\) is a tree on those terminals,
its three edges join distinct contracted components and cannot form a cycle.
Thus \(T'\cup H\) is a forest.  The argument is colour-by-colour and does not
depend on the number or shape of outside components.

The proof uses an essential scope condition: the source terminal restriction
is exactly the local spanning tree.  It would not justify a replacement if
additional same-colour terminal--terminal edges were hidden in \(H\).
The saturated-\(K_4\) class satisfies this condition because every terminal
edge copy is explicitly included in the local restriction.

## Inverse

The repair uses two cross-edge perfect matchings.  For each matching:

- one target has the simple \(K_4\) union and its red terminal tree identifies
  the matching;
- the other target has exactly that matching doubled.

These four terminal multiplicity patterns are distinct.  The first kind
recovers the source missing the smaller matching edge, the second the source
missing the larger matching edge.  Since outside edges are fixed, equality
of two targets forces equality of their complete sources.

## Boundary

The proof establishes injectivity inside this four-object repair domain.  It
does not show that its images are disjoint from direct-move, fundamental-cycle
or future subdivision-repair images.  The verifier's five-vertex search
correctly identifies the next uncovered fixed-union deficit as a
series-subdivision of a terminal edge of \(K_4\), with 12 negative and 10
positive colourings.

Audit verdict:

> The outside-stability and local inverse arguments are valid.  The
> manuscript must retain the explicit qualifier “saturated simple-\(K_4\)
> local class”; general coefficient positivity remains open.
