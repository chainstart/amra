# Obstruction analysis for the distinct-factor variant

## Exact relation model

For `n>=1`, write

\[
 v(n)=(\nu_p(n))_{p\ {m prime}}
\]

with finite support.  After cancelling the intersection of two Finsets,
the target property is exactly

\[
 \sum_{n\in A}c_n v(n)=0,\quad c_n\in\{-1,0,1\}
 \quad\Longrightarrow\quad
 \sum_{n\in A}c_n=0.                              \tag{1}
\]

The restriction on coefficients is not cosmetic.  If repetitions were
allowed, arbitrary integer coefficients would occur.  For a finite set of
vectors, the repeated-factor property is equivalent to the existence of a
rational linear functional `L` on their span satisfying `L(v(n))=1` for
every admitted `n`: the assignment is well-defined exactly when every
integer kernel relation has coefficient sum zero.

That equivalence is false for (1).  The set `{2,4}` is admissible for Finset
products--its four subset products are `1,2,4,8`--but

\[
 2v(2)-v(4)=0,
 \qquad 2-1\ne0.                                   \tag{2}
\]

Thus no additive functional is one on both elements.  Any use of the
totally additive-function obstruction for the repetitions-allowed problem
is a variant mismatch.

## Ceiling of the one-additive-level construction

For a finite prime set `P`, put

\[
 f_P(n)=\sum_{p\in P}\nu_p(n),\qquad A_P=\{n:f_P(n)=1\}.
\]

Since `f_P` is totally additive and equals one on `A_P`, this construction
has the desired property even with repetitions.  Its natural density is

\[
 d(A_P)=\prod_{p\in P}\left(1-\frac1p\right)
          \sum_{p\in P}\frac1p.                    \tag{3}
\]

Writing `lambda=sum 1/p`, the product is at most `e^(-lambda)`, so

\[
 d(A_P)\le \lambda e^{-\lambda}\le e^{-1}.         \tag{4}
\]

This recovers the scale of the local Selfridge construction and proves that
adding more selected primes to the same exact-one mechanism cannot approach
density one.  Several additive coordinates do not repair the loss unless a
new high-probability family of codewords is proved to satisfy the exact
unbalanced-relation condition.

## What a high-tail cutoff proves

Fix an integer `L>=2` and set

\[
 I_{N,L}=\{n\le N:n>N^{1-1/L}\}.
\]

If disjoint subsets `S,T` of `I_(N,L)` have equal product and
`max(|S|,|T|)<=L`, then their sizes are equal.  Indeed, if `r=|S|>|T|=s`,
then

\[
 \prod S>N^{r(1-1/L)}\ge N^{r-1}\ge N^s\ge\prod T,
\]

a contradiction.  Consequently choosing `L=L(N)=o(log N)` gives a set of
size `N-o(N)` which defeats every bad relation of length at most `L(N)`.

This is a genuine finite near-density-one theorem, but it is a bounded-length
variant only and is non-success under the closure contract.

## Arbitrarily long minimal squarefree obstructions

The high-tail argument cannot be completed by asserting that every bad
relation contains a bounded bad subrelation.  Fix `s>=2`.  Label the edges
of the complete bipartite graph `K_(s+1,s)` by distinct primes `p_(ij)`, and
put

\[
 a_i=\prod_{j=1}^{s}p_{ij}\quad(1\le i\le s+1),
 \qquad
 b_j=\prod_{i=1}^{s+1}p_{ij}\quad(1\le j\le s).
                                                               \tag{5}
\]

All these integers are squarefree and distinct, and

\[
 \prod_{i=1}^{s+1}a_i=\prod_{j=1}^{s}b_j.           \tag{6}

This is an unbalanced `s+1` versus `s` relation.  It is minimal among these
`2s+1` elements.  If a subproduct of the `a_i` equals a subproduct of the
`b_j`, then unique occurrence of `p_(ij)` says that the membership indicator
of `a_i` equals that of `b_j` for every edge.  Connectivity forces all
indicators equal, hence the subrelation is either empty or (6).

Taking the edge primes in one interval `[P,2P]` and letting `P` grow places
the `a_i` at exponent scale `P^s` and the `b_j` at scale `P^(s+1)`.  If
`N=max_j b_j`, then

\[
 \frac{\log a_i}{\log N}\longrightarrow\frac{s}{s+1}.
\]

Therefore, for every fixed `L<s+1` and sufficiently large `P`, the complete
minimal relation lies inside `I_(N,L)`.  Prime-exponent `0/1` structure,
squarefreeness, and a high-tail cutoff do not bound circuit length.

## Auxiliary-element amplification loss

A common linear dilation cannot turn a repeated unbalanced relation into a
distinct unbalanced one.  Replacing every factor by `q_i x` multiplies the
two products by `x^r` and `x^s`; if `r!=s`, homogeneity destroys equality.
More elaborate polarization, such as

\[
 (2x)(2y)=4xy,                                      \tag{7}
\]

uses a nonlinear auxiliary element `xy`.  Natural density near one does not
force membership on a prescribed sparse polynomial image; it may be removed
at zero density.  Any viable amplification must state an all-scale supply
lemma for its auxiliary elements, not merely a formal identity.

The bipartite construction (5) is the exact positive use of auxiliary
primes: it distinctifies edge occurrences, but it produces sparse bad
circuits rather than a density obstruction.

## Finite SAT/ILP boundary

For a fixed `N`, enumerate every pair of disjoint subsets `S,T subset [N]`
with equal product and unequal cardinality, and retain inclusion-minimal
supports `H=S union T`.  Then the maximum admissible set is exactly the
zero-one ILP

\[
 \max\sum_{n=2}^N x_n,
 \qquad
 \sum_{n\in H}x_n\le |H|-1\quad(H\text{ minimal bad}).       \tag{8}
\]

This is a complete finite reduction, not a completeness reduction to all
`N`.  The relation hypergraph grows with `N`, and independently optimal
solutions are neither nested nor protected against cross-block relations.

## Other exact bottlenecks

* A private-prime certificate can certify at most one admitted integer per
  prime, hence at most `pi(N)=o(N)` integers in `[N]`.  Large-prime fibres
  must reuse labels and require a new within-fibre theorem.
* Projecting exponent vectors to `Omega(n)`, residue classes, or finitely
  many scalar additive statistics can only give necessary equations.  It
  discards which primes balance which factors and cannot certify (1) without
  a proved lifting theorem.
* The infinite assertion implies the finite one by truncation.  Concatenating
  unrelated finite optimizers does not prove a natural-density set because
  new relations may use elements from several blocks.
* Finite optima, bounded factor length, bounded prime dimension, or density
  along selected endpoints are not promotion conditions.

## Required new information

The most promising positive interface is a hereditary admission or deletion
lemma which removes `o(N)` vertices from the full minimal-relation hypergraph,
not merely from its bounded-length part.  A second possible interface is an
ordered peeling theorem for largest-prime fibres which proves that every
minimal unbalanced circuit exposes a cheaply removable endpoint.  Both must
control the long squarefree circuits (5).  A negative resolution would need
a supersaturation theorem showing that every `1-o(1)` subset contains one
such circuit; the existence of isolated sparse circuits is insufficient.
