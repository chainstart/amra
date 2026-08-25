# Round 4: reserve-relative coherent recourse

## Scope and verdict

This note treats only `M786G-11`.  It gives an all-parameter finite-to-infinite
interface, but it does **not** construct the reserve or prove the local recourse
estimate required by that interface.  Thus the positive result below is a
conditional bridge, not a proof of either `tau(H_N)=o(N)` or the original
infinite assertion.

There are also two exact negative conclusions.

1. The current wording of `M786G-11`, which concludes that the admitted limit
   has density one, is refuted by `MC.1` itself.  No density-one admissible set
   exists.
2. A summable bound only on the **total** number of old-prefix changes at scale
   `k` does not imply pointwise stabilization or a zero-density permanent
   revision reserve.  Spatially local prefix control is indispensable.

The repaired interface is epsilon-dependent.  It first allocates a permanent
reserve of actual density `beta<epsilon`, then asks for summable recourse only
in the residual hypergraph not already hit by that reserve.

## CR.0: MC.1 refutes the density-one formulation

Let `A` be an admissible set and `D=N\A`.  If `A` contains three distinct
integers `a,b,c`, take `P={a,b}` and `Q={c}`.  If `ab=c`, these shores already
give a forbidden unequal-cardinality relation.  Otherwise `MC.1` gives

\[
 \overline d(D)\ \geq\ {1\over 2\max(ab,c)}>0.             \tag{CR.0}
\]

Consequently an admissible set with density one contains at most two integers,
which is impossible for a density-one set.  Therefore a coherent construction
for the public epsilon-statement must retain a positive (although arbitrarily
small) deletion density.  A zero-density revision reserve may be added to that
positive baseline reserve, but cannot replace it.

This does not refute the public problem: the baseline density and the finite
initial segment it deletes may depend on `epsilon`.

## CR.1: prefix-Carleson recourse theorem

Write

\[
 X_k=\{2,3,\ldots,2^k\},\qquad H_k=H_{2^k}.
\]

Fix `epsilon>0`.  Suppose the following data are given.

1. **Permanent baseline reserve.**  `B subseteq N` contains `1` and has a
   natural density `d(B)=beta` with `0<beta<epsilon`.  It is not assumed to be
   a transversal.  (Putting `1` in `B` enforces the campaign's exceptional-
   element convention and does not affect its density.)
2. **Finite residual transversals.**  `T_k subseteq X_k\B` meets every edge of
   `H_k` that is disjoint from `B`, and

   \[
       a_k:={|T_k|\over 2^k}\longrightarrow0.              \tag{CR.1}
   \]

   Notice that `tau(H_k)=o(2^k)` supplies this item for every fixed `B`: if
   `U_k` is a full transversal, then `U_k\B` meets every edge disjoint from
   `B` and has no larger size.
3. **Reserve-relative prefix-Carleson recourse.**  Put

   \[
   C_k=\bigl(T_{k+1}\triangle T_k\bigr)\cap X_k.           \tag{CR.2}
   \]

   There are numbers `rho_k>=0` such that

   \[
   \sum_{k\geq1}\rho_k<\infty,
   \qquad
   |C_k\cap X_j|\leq \rho_k2^j
   \quad(1\leq j\leq k).                                  \tag{CR.3}
   \]

Here the symmetric difference in (CR.2) explicitly permits both deleting a
previously admitted old seed and re-admitting a previously deleted one.
Condition (CR.3), unlike an endpoint-only estimate, measures where the changes
occur inside every old dyadic prefix.

Then there is an explicit coherent deletion set `D` meeting every finite bad
support such that

\[
 d(D)=\beta,
 \qquad d(N\setminus D)=1-\beta>1-\epsilon.                \tag{CR.4}
\]

### Construction

Put `X_0=emptyset` and permanently delete

\[
 S=\bigcup_{k\geq1}\bigl(T_k\cap(X_k\setminus X_{k-1})\bigr),
 \qquad
 R=\bigcup_{k\geq1}C_k,
 \qquad
 D=B\cup S\cup R.                                         \tag{CR.5}
\]

This is a stagewise recourse rule.  On first exposing a dyadic block, retain
its current residual deletions in `S`.  Whenever any old residual decision is
changed in either direction, put that integer permanently in the revision
reserve `R`.  No limit-membership oracle and no nested choice are used.

### Every finite residual transversal is retained

For every `m`,

\[
                         T_m\subseteq S\cup R.             \tag{CR.6}
\]

Indeed, take `n in T_m` and let `e` be its first dyadic level.  If `n in T_e`,
then `n in S`.  Otherwise there is a first `ell`, `e<=ell<m`, at which its
membership changes from absent in `T_ell` to present in `T_{ell+1}`; then
`n in C_ell subseteq R`.  This argument also shows why re-admissions cause no
problem: the construction deliberately overpays every revised integer once
and never removes it from `D`.

Let `E` be any finite bad support and choose `m` with `E subseteq X_m`.  If
`E` meets `B`, then it meets `D`.  Otherwise `T_m` meets `E`, and (CR.6) again
shows that `D` meets `E`.  Hence `D` is an infinite transversal.

### Entry cost is zero density

At a dyadic endpoint,

\[
 { |S\cap X_m|\over2^m}
 \leq \sum_{k\leq m}a_k2^{k-m}\longrightarrow0.           \tag{CR.7}
\]

For completeness, given `delta>0`, choose `K` with `a_k<delta` for `k>=K`.
The finitely many terms below `K` vanish after division by `2^m`, while the
remaining geometric sum is at most `2delta`.

### Permanent revision reserve has zero upper density

Using (CR.3),

\[
 { |R\cap X_m|\over2^m}
 \leq
 \sum_{k<m}\rho_k2^{k-m}+\sum_{k\geq m}\rho_k
 \longrightarrow0.                                      \tag{CR.8}
\]

The first term is the convolution of an `ell^1` sequence with the backwards
geometric kernel and tends to zero; the second is its tail.  Thus
`overline d(R)=0`.  More precisely, the full permanent reserve `B union R`
has actual density `beta` and hence upper density exactly `beta`.

### Dyadic endpoints imply the full natural-density limit

Let `Z=S union R`.  Equations (CR.7)--(CR.8) give
`|Z cap X_m|/2^m -> 0`.  If `2^m<=x<2^(m+1)`, then

\[
 { |Z\cap[1,x]|\over x}
 \leq 2,{ |Z\cap[1,2^{m+1}]|\over2^{m+1}}\longrightarrow0.  \tag{CR.9}
\]

Therefore `Z` has natural density zero at all integer endpoints, not merely
along the dyadic subsequence.  Since `D triangle B subseteq Z` and `B` has
natural density `beta`, (CR.4) follows.

## CR.2: exact failure of endpoint-only summable recourse

The total-change premise currently written in `M786G-11` is insufficient even
as an abstract stabilization lemma.  For every `k>=1`, let

\[
 C_k=\{2,3,\ldots,2^{\lfloor k/2\rfloor}\},
 \qquad
 \eta_k=2^{-\lceil k/2\rceil}.                             \tag{CR.10}
\]

Then

\[
 |C_k|\leq \eta_k2^k,
 \qquad \sum_{k\geq1}\eta_k=2.                            \tag{CR.11}
\]

Starting with the empty decision set and toggling precisely `C_k` at step
`k`, every stage has only `O(2^{k/2})=o(2^k)` deleted decisions.  Nevertheless
every fixed integer at least `2` lies in all sufficiently late `C_k`, so its
decision changes infinitely often and

\[
 \bigcup_k C_k=\{2,3,\ldots\},                             \tag{CR.12}
\]

which has density one.  This example is not asserted to consist of
transversals of the Erdős 786 hypergraph; its exact scope is to refute the
logical inference from (CR.11) alone to stabilization or a sparse permanent
reserve.  It violates (CR.3) maximally on prefixes much shorter than scale
`k`.

## Compatibility with multiplier completion MC.1

The reserve-relative formulation does not evade `MC.1`.  Let disjoint
unequal-size seeds `P,Q` with products `X!=Y` lie outside `B`.

- If `B` meets every sufficiently late completion
  `P union {tY}`, `Q union {tX}`, those edges are absent from the residual
  hypergraph and their positive-density cost is correctly paid by the
  baseline density `beta`.
- Otherwise every completion avoiding `B` remains a residual edge and must be
  met by `T_k`.  A later deletion or re-admission of an old member of `P union Q`
  is included in `C_k` and is charged by (CR.3).  If many arbitrary old seeds
  are forced at badly separated scales, then the prefix-Carleson estimate
  fails; this is exactly the unresolved arithmetic content, not an omitted
  step in the theorem.

In particular, deleting an old seed is allowed.  The theorem quantifies its
cost in every lower prefix, and the permanent reserve produced from all such
changes has the density asserted in (CR.8).  It does not rely on the false
guard-only claim killed by `MC.1`.

## Strictness, non-circularity, and remaining gap

The hypothesis is structurally weaker than nested finite transversals:
`C_k` may be nonempty at every scale and may contain changes in both
directions.  It is also weaker than assuming an infinite zero-density
transversal of the full hypergraph: `B` need not hit even one edge, and the
zero-density construction `S union R` is required to cover only the residual
edges disjoint from `B`.  The conclusion has deletion density `beta>0`, as
`MC.1` requires, rather than the impossible density-zero conclusion.

The local condition is finite and adjacent-scale: for a proposed explicit
`B,T_k,T_{k+1}`, (CR.3) can be checked on finite prefixes.  It does not state
that an optimal cluster hitting set exists and does not encode a pre-existing
infinite transversal.

What remains open is decisive: for every `epsilon`, construct an explicit
`B` of some density `beta<epsilon` and residual finite transversals satisfying
(CR.3), or prove that no such data can exist.  Finite `tau(H_N)=o(N)` alone
only supplies the individual `T_k`; it supplies no recourse control.  Thus
`CR.1` repairs the logical finite-to-infinite interface but does not close
`M786G-11` or change the status of Erdős 786.

To prevent the baseline from encoding a pre-existing solution, the exact
successor `M786G-13` freezes it to the explicit periodic set

\[
B_Q=\{1\}\cup\{n:Q\mid n\},\qquad Q\ge2.                 \tag{CR.13}
\]

It has density `1/Q` and is specified independently of all bad relations.
The remaining claim is that the `B_Q`-disjoint residual hypergraphs admit
`o(2^k)` transversals satisfying (CR.3).  Proving this for every `Q` would,
by CR.1, give admissible sets of density `1-1/Q` and hence the public
epsilon-statement.  No such prefix-Carleson estimate is proved here.
