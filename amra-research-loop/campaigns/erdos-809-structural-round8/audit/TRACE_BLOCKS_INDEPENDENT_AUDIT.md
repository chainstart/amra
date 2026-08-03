# Independent audit: locked-assignment trace blocks

Auditor: root, independent of the author traversal.

The author enumerates cycles by extending paths from a repeated-colour edge.
This audit instead enumerates every seven-vertex subset and every canonical
undirected Hamilton cycle on it, filters the 68,508 cycles present in the
locked graph, and only then asks whether a repeated-colour pair is contained.

The independent enumeration obtains 93 distinct deletion traces: 21
singletons and 72 triples.  The singleton set equals exactly

```text
R x (P union U union W)  union  P x Q  union  U x W  union  K2(W),
```

whose disjoint block sizes are 12, 4, 4 and 1.  Of the triples, 60 contain
three forced edges and 12 contain two.  The five block signatures and their
multiplicities are independently reproduced as 32, 24, 8, 4 and 4.

Every transversal must contain all 21 forced edges because each occurs as a
singleton trace.  Those 21 edges meet all 93 traces, so the transversal
number is exactly 21.  The theorem and the statement match pass.

The result is only about the locked 16-vertex assignment.  It supplies no
reduction forcing these blocks in arbitrary hard graphs and does not change
the public asymptotic constant.  Priority is not checked.
