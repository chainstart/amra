# Round 4: three global-potential falsifications

This note works in the distinct-Finset variant.  It does not claim a lower
bound for the full transversal number.  It tests only `M786G-08`,
`M786G-09`, and `M786G-10` against support-minimal relations that retain all
prime-occurrence information.

## 1. A graph-product minimality lemma

Let `G=(U,V,E)` be a finite connected bipartite graph.  Give every edge `e`
an odd label `b_e>1`, with the labels pairwise coprime, and put

\[
q_x=\prod_{e\ni x}b_e.
\]

Then

\[
\prod_{u\in U}q_u=\prod_{v\in V}q_v=\prod_{e\in E}b_e.       \tag{GP.1}
\]

Assume every `b_e` contains a prime absent from every other edge label.  In
any subrelation, the valuation at that private prime equates the two endpoint
indicators of `e`.  Connectedness therefore makes all indicators equal.
Consequently, if `|U|!=|V|`, the two vertex shores form a support-minimal bad
relation.

This relation can be placed in a fixed top band.  Take `N=2^K`, write
`c_x=ceil(log_2 q_x)`, and initially multiply `q_x` by `2^(K-c_x)`.  If
`|U|=|V|+1`, the excess two-adic exponent on `U` is

\[
\Delta=K-\left(\sum_{u\in U}c_u-\sum_{v\in V}c_v\right).    \tag{GP.2}
\]

Because the unpadded odd products agree, the parenthesis in (GP.2) is a
difference of ceiling errors and has absolute value less than `|U|+|V|`.
For a graph with `Theta(K)` vertices and all `q_x<N^(1/2)`, `Delta>0` and
can be distributed on `U` with `O(1)` decrement at each vertex.  All padded
terms then lie in `(N/2^C,N]` for an absolute `C`.  Odd-prime supports make
the terms distinct.

## 2. Narrow-scale paths kill M786G-08

Choose an odd path on `2s+1` vertices with `s=floor(K/8)`.  Its bipartition
sizes are `s+1` and `s`.  There are more than `2s` primes in one dyadic
interval `[P,2P)` for a suitable `P=N^(1/L)` and fixed sufficiently large
`L`, once `K` is large.  Label the path edges by distinct increasing primes
from this one interval and apply (GP.2).

Largest-prime stripping propagates through all `2s=Theta(K)` edges: the
private-prime equations leave no proper bad subrelation at which propagation
can terminate.  Yet every active prime lies in one dyadic scale.

Therefore a prime-scale coarea potential faces an exact dichotomy.  If one
unit of potential pays every successive residue transfer, its initial value
on this path is at least `2s=Theta(log N)`, contradicting the claimed
`O(log log N)` initial mass.  If multiplicity inside a scale is normalized so
the initial value is `O(log log N)`, stripping the largest prime and moving to
the adjacent prime in the same scale need not decrease the scale boundary at
all.  It cannot pay every transition.  This refutes `M786G-08` as frozen; it
does not refute a potential retaining the complete within-scale incidence
component.

## 3. Private branching kills M786G-09

Start with an odd path and attach a pendant path of length two to each of
`Theta(K)` distinct vertices on its larger shore.  Each attachment adds one
vertex to each shore, so the final bounded-degree tree still satisfies
`|U|=|V|+1`.  Label all edges by distinct private primes from one narrow
scale and apply (GP.2).

Order the private primes so that the pendant arms are processed from their
outer edges inward.  Every split exposes a signed cofactor state containing
a private prime that occurs in no state exposed by another arm.  Thus all
exposed nontrivial states have multiplicity one, there are `Theta(K)` genuine
splits, and no later identical-state merge occurs.

Hence a convex energy depending on multiplicities of *identical* signed
cofactor states cannot amortize every split against a later merge.  It either
pays `Theta(K)=Theta(log N)` initial energy or leaves an unpaid split.  This
refutes `M786G-09`; a potential able to compare nonidentical states through a
new global invariant remains possible.

## 4. Large occurrence cycle rank kills M786G-10

Return to the odd path, but label each edge by a product of `d` private odd
primes, with all these primes distinct over all edges.  The graph-product
relation is still support-minimal.  Each endpoint term has at least `d`
prime occurrences.  Ignoring additional two-adic occurrence edges, every
full occurrence matching contains `d` parallel edges above each path edge.
For `m=2s+1` support vertices its cycle rank is

\[
\beta=d(m-1)-m+1=(d-1)(m-1).                               \tag{GP.3}
\]

Take `d` tending slowly to infinity while keeping every odd vertex product
below `N^(1/2)`; for example `d=floor(K/(20 log K))` with private primes of
polynomial size in `K`.  The padding above remains valid.

Despite (GP.3), support minimality says that no nonempty proper subset of the
integer vertices is a bad relation.  The parallel occurrence cycles are
valuation identities internal to the *same* minimal circuit; they do not
supply independent bad circuits, circuit eliminations, or shared repair
vertices.  Thus full-occurrence cycle rank alone cannot certify that one
repair is reusable for `Omega(d)` fractional units.  This refutes
`M786G-10` as stated.  RR.3 remains valid as a complexity theorem, but an
additional projection from occurrence cycles to distinct support repairs is
indispensable.

## 5. Scope

The three results are all-parameter mechanism no-gos, not finite
extrapolations.  They leave `M786G-11` and `M786G-12` open, and they do not
prove or disprove `tau(H_N)=o(N)` or the coherent infinite density-one
statement.
