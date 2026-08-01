# Erdős #1083: path-energy exponent and multiplicity red team

Date: 2026-08-01

## 0. Verdict

The four path-energy exponents and their multiplicity interfaces pass
independent line-by-line recomputation:

\[
 15\longmapsto\frac29,
 \qquad
 80\longmapsto\frac{199}{18},
 \qquad
 80\to40\to20\to10\to5
 \longmapsto\frac1{72},
 \qquad
 \text{hub/packing}\longmapsto\frac1{144}.
\]

The full orientation-word pigeonhole costs only the fixed constant
\(2^{80}\).  Each midpoint fibre has at most \(q\) lifted row--source
choices, not \(qS\).  Every counted path is simple, so a path never
repeats a row or edge.  Different paths may overlap; the final
hub/packing dichotomy explicitly accounts for that multiplicity.

## 1. Primitive graph scales

The fixed-\(\delta\) directed graph has

\[
 M\ge t^{8/9+o(1)}
\]

ordered edges.  A fixed ordered transverse row pair and fixed
\(\delta\) has at most one source pair, so there are no parallel
directed edges at the row-pair level.  Forgetting direction merges at
most the two opposite orientations and leaves a simple graph with

\[
 m\ge M/2=t^{8/9+o(1)},
 \qquad
 n\le q=t^{13/18+o(1)}.
\tag{1.1}
\]

Thus the degree exponent is

\[
 \frac89-\frac{13}{18}=\frac16.
\tag{1.2}
\]

Minimum-degree pruning at threshold \(m/(2n)\) deletes fewer than
\(m/2\) edges.  In the remaining graph, extending an already simple
path at step \(r\) forbids at most \(r\) previous vertices.  Hence the
factor

\[
 \prod_{r=1}^{L-1}\left(\frac{m}{2n}-r\right)
\]

counts simple paths, not arbitrary walks.  Since \(L\) is fixed and
\(m/n=t^{1/6+o(1)}\to\infty\), every subtracted integer \(r\) is
asymptotically harmless.

## 2. The length-15 ledger

After division by the at most \(n^2\) ordered endpoint pairs, the
shared-endpoint path exponent is

\[
 \frac89+14\cdot\frac16
 -2\cdot\frac{13}{18}
 =\frac{16}{9}.
\tag{2.1}
\]

Fixing two endpoint source labels costs

\[
 S^2=t^{14/9+o(1)}.
\]

The signed orientation sum of a length-15 path has only 16 values.
Therefore the fixed endpoint-label and orientation-sum bundle has

\[
 \frac{16}{9}-\frac{14}{9}
 =\boxed{\frac29}.
\tag{2.2}
\]

No factor of \(U\), \(R\), or the full record multiplicity enters this
projection: one witness record was permanently selected for each
simple graph edge.

## 3. The length-80 ledger

For length 80, the shared-endpoint exponent is

\[
 \frac89+79\cdot\frac16
 -2\cdot\frac{13}{18}
 =\frac{227}{18}.
\tag{3.1}
\]

Fixing the two endpoint source labels subtracts \(14/9=28/18\),
leaving

\[
 \frac{227}{18}-\frac{28}{18}
 =\boxed{\frac{199}{18}}.
\tag{3.2}
\]

A complete orientation word is an element of \(\{-1,+1\}^{80}\).
There are exactly \(2^{80}\) such words.  Because 80 is an absolute
constant independent of \(t\), this pigeonhole changes only the
implicit multiplicative constant and contributes no \(t\)-exponent.

## 4. Midpoint fibre and recurrence

For an internally coherent path with fixed lifted start
\((u,x_u)\) and fixed orientation word, the midpoint potential is
fixed:

\[
 z_w^2+2\rho z_wx
 =z_u^2+2\rho z_ux_u
 -\delta\sum_{r\le L/2}\sigma_r.
\tag{4.1}
\]

For one fixed row \(w\), the height \(z_w\ne0\) and \(\rho\ne0\), so
(4.1) determines at most one real \(x\), hence at most one member of
\(X\).  The midpoint fibre therefore has size at most the number of
rows,

\[
 n\le q=t^{13/18+o(1)},
\]

not \(qS\).  This remains true even if two different rows have the
same numerical height.

After fixing a midpoint, a distinct full path determines a distinct
ordered pair (first half, second half).  If there are \(N/q\) full
paths, each ordered half-path pair determines at most one full path
by concatenation.  Therefore the two half-family sizes \(A,B\)
satisfy \(AB\ge N/q\), so one has size at least
\((N/q)^{1/2}\).  Thus the exponent recurrence is

\[
 b_{r+1}=\frac12\left(b_r-\frac{13}{18}\right).
\tag{4.2}
\]

Starting with \(b_0=199/18\), exact arithmetic gives

\[
 \frac{199}{18}
 \longmapsto\frac{31}{6}
 \longmapsto\frac{20}{9}
 \longmapsto\frac34
 \longmapsto\boxed{\frac1{72}}.
\tag{4.3}
\]

At every stage the retained object is a half of a simple path.  It is
therefore still simple and inherits fixed lifted endpoints and one
fixed orientation subword.  Across the family, different paths may
share rows or edges; no disjointness is assumed here.

## 5. Hub/packing multiplicity

Let \(K=t^{1/72+o(1)}\) be the number of distinct coherent simple
length-five paths with fixed lifted endpoints.  Each path has four
internal rows.

- If one internal row lies on at least \(K^{1/2}\) paths, one of four
  fixed positions contains it on at least \(K^{1/2}/4\) paths.  The
  position potential fixes its source label, giving a lifted-row hub.
- Otherwise every internal row lies on fewer than \(K^{1/2}\) paths.
  Greedy selection of one path discards fewer than \(4K^{1/2}\)
  paths, so at least \(K^{1/2}/4\) paths with pairwise disjoint
  interiors remain.

In both cases the exponent is

\[
 \boxed{\frac12\cdot\frac1{72}=\frac1{144}}.
\tag{5.1}
\]

The constants \(1/4\) do not change the exponent.  In the packing
branch, internal vertex-disjointness also prevents any shared
internal edge; sharing endpoints is intended.

## 6. Firewall

This audit validates the counting and fibre claims only.  The
length-80 amplification enters the coherent conclusion after a
common-defect-vector dichotomy.  It does not assert that the common
defect vector must vanish, and it does not turn the resulting theta
graph into a global few-distance contradiction without an additional
tangent/distance-label argument.

By definition, a path defect is recorded only at a path's internal
rows: the two endpoint labels are kept separately and fixed before
path subtraction.  Hence every row in the support of a nonzero common
defect vector is an internal row of every path in that common-defect
family.  No endpoint is silently included in that support.
