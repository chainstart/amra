# Erdős #1083: nonzero-defect transition trichotomy and short theta extraction

Date: 2026-08-01

## 0. Verdict

The nonzero common-defect branch of the shared-endpoint path theorem
can be reduced without assuming that the defect vanishes.

From the length-80 fixed-endpoint bundle, one of the following holds:

1. **homogeneous-relation branch:** a power-large family of path
   differences gives nontrivial homogeneous height relations on at
   most 158 rows;
2. **transition-misalignment branch:** a path pair contains a
   noncoherent simple cycle of length at most 160, hence a bounded
   affine height relation; or
3. **aligned-defect network branch:** there is either a fixed lifted
   row used by \(t^{1/20+o(1)}\) internally coherent short paths, or
   a coherent theta graph with \(t^{1/20+o(1)}\) pairwise internally
   vertex-disjoint arms, each of length at most six.

Thus direct subtraction does **not** always turn a common nonzero
defect into a relation: the defect can live on a shared labelled
spine while paths differ by coherent detours.  But this is now the
only exception, and the coherent detours amplify to a much stronger
\(t^{1/20}\) short theta-or-hub conclusion.

This theorem also supersedes the weaker conditional
\(t^{1/144}\) conclusion in `COHERENT_THETA_AMPLIFICATION.md`.

## 1. Starting bundle and defect vectors

Use the length-80 family \(\mathcal P\) from
`COHERENT_THETA_AMPLIFICATION.md`.  Its paths have:

- the same ordered endpoint rows \(u,v\);
- the same endpoint source labels \(x_u,x_v\);
- the same complete orientation word
  \((\sigma_1,\ldots,\sigma_{80})\); and
- cardinality

  \[
  |\mathcal P|=t^{199/18+o(1)}.
  \tag{1.1}
  \]

For a path \(P\), its internal-defect vector is

\[
 D_P(w)=x_{P,\mathrm{out}}(w)-x_{P,\mathrm{in}}(w),
\tag{1.2}
\]

with value zero off the internal rows of \(P\).  The two endpoint
labels are kept separately and were fixed before this vector was
defined.  For any \(P,Q\in\mathcal P\), exact path subtraction gives

\[
 \sum_wz_w(D_P(w)-D_Q(w))=0.
\tag{1.3}
\]

Fix one reference path \(Q\).  If at least half the paths have
\(D_P\ne D_Q\), then (1.3) is a nontrivial homogeneous relation on at
most

\[
 2(80-1)=158
\]

rows for every such path.  This is the first branch.

Otherwise, after losing a factor at most two, assume

\[
 D_P=D_Q=:D
 \qquad(P\in\mathcal P_1),
\tag{1.4}
\]

where \(|\mathcal P_1|=t^{199/18+o(1)}\).  The vector \(D\) may be
zero or nonzero.  Its support \(R_D\) has size at most 79.  Because
defects are internal by definition, every row in \(R_D\) is an
internal row of every path in \(\mathcal P_1\).

## 2. When equal defects force a noncoherent cycle

At a defect row \(w\in R_D\), write

\[
 b_P(w)=x_{P,\mathrm{in}}(w),
 \qquad
 a_P(w)=x_{P,\mathrm{out}}(w),
\]

so

\[
 a_P(w)-b_P(w)=D(w)=:d_w\ne0.
\tag{2.1}
\]

### Lemma 1 (transition alignment or noncoherent cycle)

Let \(P,Q\in\mathcal P_1\).  If for some \(w\in R_D\),

\[
 (b_P(w),a_P(w))\ne(b_Q(w),a_Q(w)),
\tag{2.2}
\]

then the edge-occurrence union of \(P\) and \(Q\) contains a
noncoherent simple cycle of length at most 160.

#### Proof

Traverse \(P\) from \(u\) to \(v\) and then \(Q\) backwards.  This is
a closed edge-occurrence trail of length at most 160.  Decompose its
Eulerian edge-occurrence multigraph into simple cycles, allowing
coherent two-edge backtracks coming from repeated copies of one graph
edge.

The word "edge-occurrence" is essential: \(P\) and \(Q\) may share an
undirected edge, possibly traversed in opposite directions.  Both
occurrences are retained until the multigraph decomposition.  An
immediate reversal or a two-edge doubled-edge circuit uses the same
permanently selected incidence label at each endpoint, so it is
coherent and may be erased.  Erasing all such pieces cannot remove the
label-pairing obstruction below; if that obstruction occurs, a
genuine noncoherent simple cycle with at least three vertices remains.

If every resulting nontrivial cycle were coherent, the incident
half-edge labels at every row could be paired into equal-label pairs.
At \(w\), the four relevant labels are

\[
 b_P,\quad b_P+d_w,\quad b_Q,\quad b_Q+d_w.
\tag{2.3}
\]

Because \(d_w\ne0\), this multiset can be partitioned into two equal
pairs only when

\[
 b_P=b_Q,
 \qquad b_P+d_w=b_Q+d_w.
\tag{2.4}
\]

Indeed, the only alternative pairing would require simultaneously
\(b_P=b_Q+d_w\) and \(b_P+d_w=b_Q\), which gives \(2d_w=0\), impossible
over the reals.  Common edge occurrences simply remove an already
equal pair and lead to the same conclusion.

Thus (2.2) prevents an all-coherent cycle decomposition.  Some
simple cycle is noncoherent.  A doubled copy of one edge has identical
endpoint labels and is coherent, so the noncoherent cycle is a genuine
cycle and has length at most 160. \(\square\)

Applying Lemma 1 path by path gives another dichotomy.  Either a
positive proportion of \(\mathcal P_1\) supplies a noncoherent cycle
witness, or a subfamily

\[
 |\mathcal P_2|=t^{199/18+o(1)}
\tag{2.5}
\]

has the same ordered transition pair

\[
 (b(w),a(w))
\tag{2.6}
\]

at every defect row \(w\in R_D\).

### Why direct subtraction alone is insufficient

The aligned case is real.  Two paths may share a defective initial
spine, use the same incoming and outgoing labels at its defect row,
and then take two different internally coherent branches with the
same lifted endpoint.  Their path defects are the same nonzero
vector, while their symmetric difference is a coherent cycle.  Thus
"common nonzero defect" does not itself imply a noncoherent relation;
transition misalignment is the exact missing condition.

## 3. Fixed defect spine and coherent gaps

Work in the aligned family \(\mathcal P_2\).  Each simple path contains
the fixed set \(R_D\).  Pigeonhole the order and the positions of
these at most 79 rows along the length-80 path.  The number of choices
depends only on 80, so the family still has exponent \(199/18\).

Cut every path immediately before and after each defect transition.
This produces \(r+1\) coherent gap paths, where

\[
 r=|R_D|\le79.
\]

Their lengths \(\ell_1,\ldots,\ell_{r+1}\) are fixed positive
integers satisfying

\[
 \sum_j\ell_j=80.
\tag{3.1}
\]

Every gap has fixed lifted endpoints:

- the global endpoint label is fixed at \(u\) or \(v\); and
- at a defect row, the incoming label \(b(w)\) and outgoing label
  \(a(w)\) are fixed by (2.6).

Let \(A_j\) be the number of distinct gap paths in position \(j\).
Each ordered tuple of gap paths determines at most one full path by
concatenation with the fixed defect transitions.  Hence

\[
 \prod_jA_j\ge t^{199/18+o(1)}.
\tag{3.2}
\]

By (3.1), some gap of length \(\ell\) satisfies

\[
 A\ge
 t^{(199/1440)\ell+o(1)}.
\tag{3.3}
\]

It cannot have \(\ell=1\), because a simple graph has at most one
edge between fixed endpoint rows.  Thus

\[
 2\le\ell\le80.
\]

## 4. Compressing one coherent gap to length at most six

Put

\[
 s=\left\lceil\frac\ell6\right\rceil.
\]

Choose \(s-1\) checkpoint positions that divide the gap into \(s\)
segments of length at most six.  Coherence, fixed lifted endpoints,
and the fixed orientation subword determine the potential at every
checkpoint.  For a fixed row, that potential determines at most one
source label.  Thus each checkpoint has at most

\[
 q=t^{13/18+o(1)}
\]

lifted choices.

Every gap is a contiguous subpath of an original simple length-80
path.  Every checkpoint segment is therefore itself a simple path:
it repeats neither a row nor an edge.  Pigeonholing across different
paths permits cross-path overlap but does not change this individual
simple-path property.

After fixing all checkpoints, at least

\[
 t^{(199/1440)\ell-(s-1)13/18+o(1)}
\]

full gap paths remain.  Each ordered segment tuple determines at most
one full gap path, so one of the \(s\) segments has at least

\[
 t^{g(\ell)+o(1)},
 \qquad
 g(\ell)=
 \frac{(199/1440)\ell-(s-1)13/18}{s},
\tag{4.1}
\]

distinct realizations between fixed lifted endpoints.

The lower bound is uniformly positive.  For fixed \(s\), (4.1) is
increasing in \(\ell\), so its minimum occurs at
\(\ell=6s-5\).  For \(2\le s\le14\), this minimum is

\[
 \frac{154s+45}{1440s},
\]

which decreases with \(s\).  The global minimum on
\(2\le\ell\le80\) is at \((\ell,s)=(79,14)\):

\[
 g(79)=\frac{2201}{20160}>\frac1{10}.
\tag{4.2}
\]

The case \(s=1\), \(2\le\ell\le6\), is larger still.  Therefore the
aligned common-defect branch contains

\[
 \boxed{t^{1/10+o(1)}}
\tag{4.3}

distinct internally coherent paths, all of one length between two
and six, with the same lifted endpoints and orientation word.

## 5. Unconditional short theta-or-hub conclusion

Let \(K=t^{1/10+o(1)}\) be the path family in (4.3).  Every path has
at most five internal rows.  Apply the same incidence packing as in
the earlier theta theorem:

- if one internal row lies on at least \(K^{1/2}\) paths, fix one of
  its at most five positions; its potential fixes the source label;
- otherwise greedily select at least \(K^{1/2}/5\) paths with
  pairwise disjoint interiors.

This proves the aligned-defect alternative stated in Section 0:

\[
 \boxed{t^{1/20+o(1)}}
\tag{5.1}

arms in either a lifted-row hub or an internally vertex-disjoint
coherent theta graph.  In the theta branch, every pair of arms forms
a simple coherent cycle of length at most twelve.  At each internal
position, all arms lie on the one parabolic potential level fixed by
the common orientation word.

## 6. Remaining boundary

The nonzero common-defect obstruction is no longer an unanalysed
exception.  It either exposes a bounded noncoherent cycle or yields a
power-growing short coherent theta/hub with fixed lifted endpoints.

The final missing step is now a tangent/distance-label theorem for
that short network.  Its arms can still use distinct endpoint tangent
records, and the exponent \(1/20\) remains below the tangent-set size
\(U=t^{5/6}\).  No unsupported claim that the distance budget is
already exceeded is made here.
