# Survivor deepening: rough paths, universal residues, and cycle surplus

## Decisive all-parameter obstruction package

### RR.1 (rough ordered-path circuit theorem)

For every pair of integers `L>=3` and `s>=L`, there are arbitrarily large
`N=2^K` and a support-minimal bad relation on `2s+1` distinct integers such
that:

1. all integers lie in the strict high tail `(N^(1-1/L),N]`;
2. for `y=N^(1/L)`, every integer has one or two prime divisors above `y`,
   all with exponent one;
3. the active-prime incidence graph is the tree path `P_(2s+1)`;
4. its edge primes can be strictly ordered along the path, so successive
   largest-prime residue transfers traverse all `2s` edges.

The proof is the construction in `evidence/OBSTRUCTION_ANALYSIS.md`: label a
path by distinct primes above `y`, then use balanced nonuniform powers of two
to place all vertex-products near `N`.  The exponent-capacity inequality is

\[
1-\frac2L-\frac1{s+1}>0,
\]

and unique edge-prime equations give signed support minimality.

### RR.2 (universal largest-prime residue extension)

For disjoint sets `A,B` of `r,s>=1` distinct primes with `r!=s`, choose a
prime `p>max(A union B)` and put `X=prod A`, `Y=prod B`.  Then

\[
A\cup\{pY\}\quad\text{and}\quad B\cup\{pX\}         \tag{1}
\]

are the shores of a support-minimal bad relation.  The top `p`-fibre has one
term per shore, but stripping `p` transfers the coprime residue `Y/X`, whose
numerator and denominator prime-support sizes `s,r` are arbitrary.  The
incidence graph is a connected double-star tree, proving minimality.

Together RR.1--RR.2 close the following frozen local claims:

* bounded support or bounded radius from fixed `L` and active degree;
* safety of active-incidence forests or positive active cycle rank;
* bounded recursive depth from fixed `L` and active degree;
* bounded residue complexity from the top-fibre cardinality;
* splitting of the global relation from coprime exposed cofactors;
* strict token-count descent at every top-prime peel;
* no-reserve future safety of finite lower-prime decisions.

They do not lower-bound `tau(H_N)`: one vertex hits either displayed circuit.

## New exact positive host: the full prime-occurrence graph

The active graph loses the small-prime residue.  Retaining **all** prime
occurrences gives a different exact representation.

Let `S,T` be disjoint shores of an equal-product relation.  For each prime
`p`, make `nu_p(n)` occurrence stubs at every term `n`.  Equality of products
lets us match the `p`-stubs on `S` bijectively to the `p`-stubs on `T`.
Doing this for every prime produces a bipartite multigraph `G` on `S union T`
whose edges are labelled by matched prime occurrences.  Its vertex degree is

\[
\deg_G(n)=\Omega(n).                                 \tag{2}
\]

Every connected component `C` has equal products on its two induced shores:
for each prime, its matched occurrence edges stay inside `C` and give equal
valuation totals.  Therefore, if the original bad support is inclusion-
minimal, `G` must be connected.  Otherwise the sum of the component
cardinality differences is nonzero, so one proper component is already bad.

### Lemma RR.3 (cycle-surplus bound)

Suppose the minimal bad support has shores `r>s`, every term satisfies
`Omega(n)>=d`, and `v=r+s` is its support size.  For any occurrence matching,
the connected multigraph above has `e=sum_(n in S)Omega(n)` edges and cycle
rank

\[
\begin{aligned}
\beta(G)&=e-v+1\\
&\ge dr-(r+s)+1\\
&\ge \left(\frac d2-1\right)v+\frac d2+1.           \tag{3}
\end{aligned}
\]

This is an exact all-parameter inequality.  By the standard
Turán--Kubilius estimate, for
`d_N=floor((1/2)log log N)` the integers with `Omega(n)<d_N` are `o(N)`.
Thus, after one legitimate zero-density deletion, every remaining minimal
bad event has cycle surplus linear in its support with coefficient tending
to infinity.

RR.3 does not itself round the LP.  It shows that the zero-cycle obstruction
RR.1 is caused by discarding the small-prime occurrences (especially the
padding prime), and it supplies a strictly richer common host for the three
survivors.

## M786R-04: full-component arithmetic alteration

The surviving claim is the existence of an explicit dependent alteration
on the full occurrence components such that

\[
|D_N|\le g(N)\sum_{n=2}^Nw_N(n)+o(N),
\qquad g(N)=o(\log N).                               \tag{4}
\]

RR.3 supplies many independent cycle edges inside each event after deleting
low-`Omega` integers.  The missing theorem is a **cluster compression** that
turns this internal surplus into simultaneous event repairs while charging a
shared vertex only `o(log N)` times.  Counting cycles separately is invalid
because one bad support may contain exponentially many cycle bases and
different supports may reuse them.

## M786R-08: global residue-aware owner flow

For every minimal bad support, build its full occurrence graph and expose the
largest active prime together with the exact cofactor ratio.  The target is a
noncircular owner map `owner(E) in E` satisfying

\[
\bigl|\{owner(E):E\text{ minimal bad}\}\bigr|
\le g(N)\sum_nw_N(n)+o(N),
\qquad g(N)=o(\log N).                               \tag{5}
\]

RR.1--RR.2 disallow a load proof based only on local degree, top fibre size,
coprimality, or peel depth.  RR.3 suggests a possible global flow through
cycle surplus, but no owner definition and no inequality (5) have been
proved.

## M786R-12: global recursive potential and coherent reserve

The precise finite target is a potential `Phi(G,R)` of the full occurrence
graph `G` and its signed residue state `R` such that a global prime-scale
transition either chooses a paid owner or decreases `Phi`, and the total
paid load telescopes to the right side of (4).

For the equally mandatory infinite target, the same rule must be compatible
under growing cutoffs/prime prefixes.  RR.2 proves that future primes can
complete any two lower prime products into a bad double star.  Hence the rule
needs either:

* a summable revision probability/budget for every fixed integer; or
* a reserved deletion set of zero upper density that intercepts every future
  completion.

It must then prove both pointwise stabilization and zero upper density of
all deletions, which gives an actual natural-density limit.  No such
potential or reserve theorem is proved here.

## Checkpoint classification

* RR.1, RR.2, and elementary RR.3: `proved`, all parameters.
* The `o(N)` low-`Omega` deletion used with RR.3: `proved` from the standard
  Turán--Kubilius theorem, not from computation.
* M786R-04, M786R-08, M786R-12: `conditional/open` at (4), (5), and the
  stated potential/reserve interfaces.
* `tau(H_N)=o(N)`: open.
* The coherent infinite natural-density assertion: open.
* Original distinct-Finset Erdős #786: open.

This author campaign remains at `survivor_deepening`.  RR.1--RR.2 are the
decisive scoped countermechanism package offered for non-author audit; there
is no self-audit, promotion, or freeze decision here.
