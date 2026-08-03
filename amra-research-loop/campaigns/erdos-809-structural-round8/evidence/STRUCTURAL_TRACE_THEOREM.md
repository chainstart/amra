# Locked-assignment structural trace theorem

Put `R={r1,r2}`, `P={x1,x2}`, `Q={x3,x4}`, `U={y1,y2}` and
`W={y3,y4}`.  In the unique unprotected round-7 assignment (the one
omitting `bu,bw,uw`), let `H` be the hypergraph of intersections of bad
rainbow-`C7`s with the 32 admissible old edges.

Exact reconstruction gives 93 distinct traces: 21 singletons and 72 triples.
The set `F` of singleton edges has the exact disjoint block formula

```text
F = R x (P union U union W)  union  P x Q  union  U x W  union  K2(W),
```

with respective sizes 12, 4, 4 and 1.  Of the 72 triple traces, twelve meet
`F` in two edges and sixty lie wholly in `F`.  Their five block-signature
types and multiplicities are recorded in `TRACE_BLOCK_CERTIFICATE.json`.

Consequently every transversal of `H` contains all of `F` (because every
edge of `F` occurs as a singleton trace), while `F` itself meets every trace.
Thus `tau(H)=|F|=21`.  This explains the round-7 number by a block
certificate and proves immediately that a three-old-edge repair is
impossible in this assignment.

## Scope

This is an exact finite theorem for one locked 16-vertex assignment.  It does
not show that the five blocks, singleton traces, or transversal lower bound
occur in arbitrary hard graphs.  It does not improve the public `1/8`
constant.  The unresolved route is a quantified reduction that forces an
analogous block kernel in every relevant hard branch.
