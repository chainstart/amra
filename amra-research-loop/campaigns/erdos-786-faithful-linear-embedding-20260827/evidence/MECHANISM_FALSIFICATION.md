# Mechanism tests for the faithful linear-hypergraph embedding

## Retained facts

- `M786F-01`: For
  \(r=\lceil\log_2(D+1)\rceil+1\), the number
  \(2^{r-1}-1\) of unordered nontrivial bipartitions is at least \(D\).
  The prime and bit budgets are separated explicitly in
  `FAITHFUL_LINEAR_EMBEDDING.md`.
- `M786F-04`: One private prime row per auxiliary path edge forces every
  rational valuation-kernel vector to alternate.  The complete kernel is
  one-dimensional and its primitive integral generator has coefficients
  \(\pm1\).
- `M786F-06`: The footprint case analysis uses exactly one host condition:
  a two-point set belongs to at most one edge.  This is linearity.
- `M786F-08`: Replacing an edge-private selected vertex by any shared vertex
  of the same nonempty host edge proves the reverse transversal inequality.
- `M786F-09`: Equations (4)--(9) of `FAITHFUL_LINEAR_EMBEDDING.md` give an
  explicit decrement vector, its sum, its maximum, and the exact two-adic
  exponent identity.

## Killed mechanisms

- `M786F-02`: With two primes and complementary exponent pairs
  \((a,T-a)\), \(D\) distinct codes require an exponent interval containing
  at least \(D\) integers.  The point product then has exponent sum at least
  \(D-1\), rather than the logarithmic number of coordinates supplied by
  subset bipartitions.  This does not satisfy the same uniform bit budget.
- `M786F-03`: Reusing a prime block at two different host vertices makes
  their shared raw products equal.  Multiplication by the same scale rule
  preserves that collision; varying the scale would destroy the common
  point label used across incident edges.
- `M786F-05`: Petrović--Thoma--Vladoiu encode integer-matrix toric data by
  hypergraph incidence matrices.  Their theorem does not assign distinct
  positive integers in a fixed interval to the hypergraph vertices, create
  unequal-cardinality equal products, or assert preservation of the host's
  transversal and matching numbers.  It is an algebraic comparator, not a
  substitute for the present arithmetic construction.
- `M786F-07`: A graph intersection representation retains only whether two
  representing sets meet.  It does not identify which multiple edges share
  one common host vertex, and therefore does not determine hypergraph
  transversals or a valuation circuit on each represented edge.
- `M786F-10`: When \(m\le K\), the discrepancy upper bound
  \(\Delta<K+3m\) no longer implies a constant decrement per private vertex.
  Adding padding primes does not reduce the required total exponent change
  or the size of the fixed odd parts.  No uniform fixed-band proof follows
  under the frozen hypotheses.
- `M786F-11`: If two distinct host edges contain the same pair \(\{x,y\}\),
  an internal private vertex on each edge can have the same two-block
  footprint.  The linearity step that made this footprint edge-identifying
  is then false.
- `M786F-12`: The edge-intersection graph records only nonempty pairwise
  intersections.  Three edges meeting at one common host vertex have
  transversal number one, whereas three edges with three distinct pairwise
  intersection vertices have transversal number two; both edge-intersection
  graphs are triangles.
- `M786F-13`: Cloning every vertex separately inside each short edge creates
  only edge-private vertices and does not increase the number of shared host
  vertices.  Declaring clones shared across several incident edges changes
  intersection multiplicities and can violate linearity.  Thus cloning does
  not remove the scale hypothesis while preserving all frozen invariants.

The eight killed mechanisms are evidenced mathematical failures, not merely
unused alternatives.  The retained mechanisms combine into the theorem in
`FAITHFUL_LINEAR_EMBEDDING.md`.
