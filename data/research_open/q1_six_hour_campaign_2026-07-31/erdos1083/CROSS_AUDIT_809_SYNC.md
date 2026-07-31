# Cross-audit of Erdős #809 matching synchronization

Audit window: 2026-08-01 01:30--02:20 HKT

Audited, without modifying either source file:

- `erdos809/LINEAR_MATCHING_SYNCHRONIZATION.md`
  (`d111a4860cce0581e2219fb752535dfc16d672e7bcc2b634c81178493e6ddc87`);
- `erdos809/MATCHING_RECTANGLE_TRANSFERENCE.md`
  (`4889f0da89fe0eb632f9a6fef6a93cf178e86a92de30b018eb2edc570a471487`).

## Verdict

**PASS on the substantive theorems and on every requested proof
interface.**  I found no counterexample to the synchronization,
rectangle-transference, common-host, or iterated quadratic-reserve
claims.

Before publication, two local scope hypotheses should be made
explicit and one verifier description should be corrected:

1. displayed inequality (18) needs \(\delta\ge2\), since it divides by
   \(\binom\delta2\);
2. Theorem 3.1's assertion \(0<\alpha\le1\) needs a nonempty
   zero-shore matching (the \(f=0\) case should be separated);
3. the rectangle verifier fixes one global endpoint orientation,
   whereas the proof reorients each pair separately for each anchor.
   This does not affect the universal proof, but the verifier does not
   literally materialize the anchor-dependent forced union it claims
   to model.

These are scope/verification edits, not failures of the nonempty,
\(\delta\ge2\) results used in the campaign.

## 1. Overlapping-neighbourhood count: PASS

For one zero pair \(bc\), put \(P=N(b)\), \(Q=N(c)\), and
\(r=|P\cap Q|\).  The unordered cross-pair count is exactly

\[
 |\mathcal C|=|P||Q|-r-\binom r2.
\]

The term \(-r\) removes loops \((x,x)\), and the term
\(-\binom r2\) removes the second ordering of a pair wholly inside
\(P\cap Q\).  If \(p=|P|\le q=|Q|\), the expression decreases with
\(r\le p\), and at \(r=p\) equals

\[
 pq-\frac{p(p+1)}2
 =\binom p2+p(q-p)
 \ge\binom p2.
\]

Every counted pair \(xy\) is missing.  If it were an edge,
\(b-x-y-c\) would be a simple three-edge path.  The possible
coincidences \(x=c\) and \(y=b\) would themselves make \(bc\) an edge,
so no hidden nonsimple walk is used.

The incidence average therefore really gives an anchor missing edge
of multiplicity at least

\[
 \left\lceil
 f\binom\delta2/\overline M
 \right\rceil.
\]

## 2. An anchor cannot be a supported endpoint: PASS

After orienting a supported pair so that
\(x\in N(b_i)\), \(y\in N(c_i)\):

- \(x=b_i\) or \(y=c_i\) would require a loop;
- \(x=c_i\) or \(y=b_i\) would require the missing edge
  \(b_ic_i\).

This covers both initial orientations.  Hence no supported index is
lost, and the ceiling in the main bound is retained exactly.

For distinct supported indices, an edge \(b_jc_i\) would create the
simple path

\[
 b_i-x-b_j-c_i.
\]

Matching endpoints are all distinct and the anchor is not one of
them, so this proves the entire \(U\times V\) rectangle missing,
including off-diagonal pairs.

## 3. One- and two-anchor rectangle transference: PASS

For a common \(A\)-coordinate \(a\), orient each matching pair
independently so that \(a\in X_i\).  Then \(a b_i\) and \(a b_j\) are
edges.  If \(b_jc_i\) were an edge, the same simple three-path
\(b_i-a-b_j-c_i\) would contradict the zero-shore condition.

The matching hypothesis makes all endpoint vertices distinct, so the
resulting rectangle has exactly \(r(a)^2\) distinct unordered
\(B\)-edges.  Activity places each missing edge in the global reserve
union.  Thus

\[
 r(a)^2\le|\mathcal Q|
\]

with no requirement that orientations be consistent for different
anchors.

For a common missing \(A\)-pair \(aa'\), every supporting colour
rectangle can likewise be oriented with \(a\in X_i\),
\(a'\in Y_i\).  Applying the one-anchor lemma to \(a\) proves
\(\mu_F(aa')^2\le|\mathcal Q|\).  The double counts

\[
 \sum_a r(a)=2\sum_i h_i,
 \qquad
 \sum_{z\in\overline E(G[A])}\mu_F(z)=\sum_i h_i^2
\]

are exact because \(X_i\cap Y_i=\varnothing\) and one rectangle has
exactly \(h_i^2\) distinct unordered cross edges.  The two displayed
capacity inequalities follow.

## 4. Batch rectangles are genuinely edge-disjoint: PASS

At an iteration of Theorem 3.1, one removes the selected matching
pairs, not merely their current orientation.  Since the original
matching has pairwise disjoint endpoint sets, two different batches
use disjoint vertex sets.  Every edge of a batch rectangle has both
endpoints in that batch's endpoint set.  Hence rectangles from
different batches cannot share an unordered edge.

The next round's anchor is allowed to be an old endpoint, but anchors
are not rectangle vertices unless they belong to the current matching
batch; this does not change edge-disjointness.  Every batch rectangle
still lies in the same global \(\mathcal Q\).

## 5. The potential coefficient \(\alpha/(2-\alpha)\): PASS

For a nonempty zero-shore matching and \(\delta\ge2\), one zero pair's
neighbourhood rectangle already gives

\[
 \overline M\ge\binom\delta2,
\]

so \(0<\alpha\le1\).  A synchronized batch of size at least
\(\lceil\alpha r\rceil\) may be trimmed to exactly

\[
 t=\lceil\alpha r\rceil.
\]

Put \(c=\alpha/(2-\alpha)\), so
\((1+c)\alpha=2c\), and write
\(t=\alpha r+\varepsilon\), \(0\le\varepsilon<1\).  Direct expansion
gives

\[
 t^2+c(r-t)^2-cr^2
 =2cr\varepsilon+(1+c)\varepsilon^2\ge0.
\]

The matching size strictly falls because \(1\le t\le r\); telescoping
ends at zero and yields

\[
 \sum_jt_j^2\ge\frac{\alpha}{2-\alpha}f^2.
\]

Together with batch edge-disjointness, this proves the reserve bound.
The closed form

\[
 \frac{\alpha}{2-\alpha}
 =\frac{d_0}{2\overline M-d_0}
\]

and the quadratic solution (23c) are algebraically correct.  At fixed
\(s\), substitution gives

\[
 \alpha=\frac{1-2s}{2(1+2s)}+o(1),
 \qquad
 c_\alpha=\frac{1-2s}{3+10s}+o(1),
\]

also as claimed.

## 6. Common complementary hosts: PASS

The anchors give \(U\subseteq N(x)\), \(V\subseteq N(y)\).  If
\(z\in N(v_i)\cap N(x)\), then

\[
 u_i-x-z-v_i
\]

is simple: \(z=x\) is excluded by open neighbourhoods,
\(z=u_i\) would make \(u_iv_i\) an edge, and the anchor is not a
matching endpoint.  Thus \(N(v_i)\cap N(x)=\varnothing\), symmetrically
for \(u_i,y\).

Consequently \(N(v)\subseteq C_x=V(G)\setminus N(x)\), and the exact
deficit is

\[
 |C_x\setminus N(v)|=n-d(x)-d(v)\le n-2\delta.
\]

The anchored missing-energy count is also exact.  For
\(r_x=|V\cap N(x)|\), the number of distinct unordered pairs between
the anticomplete sets is

\[
 t d_x-r_x-\binom{r_x}{2}.
\]

The constraints \(d_x\ge\max\{\delta,t\}\) and
\(r_x\le\min\{t,d_x-t\}\) follow from the disjoint subset
\(U\subseteq N(x)\setminus V\).  The displayed minimization is
monotone in the asserted directions, including the boundary
\(d_x=2t\).

## 7. Counterexample search and finite evidence

I independently enumerated every labelled simple graph on
\(n=2,3,4,5,6\) vertices and every nonempty matching of missing pairs
having no simple three-edge endpoint path.  This covered:

| \(n\) | graphs | graphs with a zero pair | zero-pair matchings checked |
|---:|---:|---:|---:|
| 2 | 2 | 1 | 1 |
| 3 | 8 | 7 | 12 |
| 4 | 64 | 45 | 198 |
| 5 | 1,024 | 581 | 4,645 |
| 6 | 32,768 | 15,725 | 173,295 |

For every matching I checked the exact \(\mathcal C_i\) formula,
anchor multiplicity, endpoint exclusion, full anticomplete rectangle,
both common-host containments, and the \(n-2\delta\) deficits.  No
counterexample occurred.

The repository's eight targeted unit tests pass.  The two standalone
verifiers also pass, including 3,969 exhaustive set pairs, 438,155
host-cut parameter tuples, 2,000 random neighbourhood systems, 5,000
greedy recurrences, 5,000 closed-form parameter pairs, and 2,000
random colour-rectangle systems.

## 8. Required local fixes and verifier caveat

### 8.1 Equation (18) needs \(\delta\ge2\)

As written, (18) divides by \(\binom\delta2\) before the later
\(\delta\ge2\) hypothesis.  For example, the four-vertex graph with
edges \(02,13\) has minimum degree one and \(01\) is a zero-shore
missing pair, but the denominator in (18) is zero.  Add
\(\delta\ge2\) to the statement of (18), or leave the
\(\delta\le1\) case outside that corollary.

### 8.2 Theorem 3.1 needs a nonempty matching

The inference \(\alpha\le1\) uses the neighbourhood rectangle of at
least one zero pair.  Without that existence hypothesis it is false:
in \(K_5\) with one edge removed,
\(\delta=3\), \(\overline M=1\), and
\(\binom\delta2/\overline M=3\), while there is no zero-shore pair.
State Theorem 3.1 for \(f>0\), and handle \(f=0\) separately as the
trivial reserve inequality.

The structural alternative in MATCHING_RECTANGLE_TRANSFERENCE.md
likewise has a harmless empty-family corner: if \(F=\varnothing\) and
\(M_A=0\), its strict first inequality and its second outcome both
fail.  The intended nonempty active matching automatically has
\(M_A>0\).

### 8.3 Orientation in the finite rectangle verifier

The proof correctly reorients pair \(i\) separately for each anchor.
The verifier's `forced_q`, however, always inserts
`((0,i),(1,j))`.  These need not be the actual anchor-dependent
endpoints.  A two-rectangle example is

\[
 X_1=\{0\},\ Y_1=\{1\},
 \qquad
 X_2=\{0,1\},\ Y_2=\{2,3\}.
\]

The verifier's fixed-orientation union has four edges, while the union
obtained by orienting at anchors 0 and 1 has six.  The per-anchor
inequality remains valid, and the universal proof never unions these
rectangles, so no theorem changes.  For a literal materialization
guard, store the side of each coordinate occurrence and orient the
corresponding \(B\)-endpoint before inserting its forced edges.

There is also a numbering typo after (23c): “Thus (26)” should refer
to (23c).

## Final classification

**PASS with the stated local scope and verifier corrections.**  The
central synchronization theorem, common-host conclusion,
one-/two-anchor transference, batch edge-disjointness, and
\(\alpha/(2-\alpha)\) potential argument are mathematically sound.
The remaining #809 gap is genuinely downstream: turning the aligned
anticomplete/common-host structure into the final BCM distance/cycle
budget, not repairing these two synchronization proofs.
