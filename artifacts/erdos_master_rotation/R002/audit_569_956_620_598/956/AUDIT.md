# Erdős Problem #956 — independent evidence audit

## Verdict

`verified_closed`

The fixed public note *Unit distances between disjoint convex translates*
(27 April 2026) contains a self-contained lower-bound construction which
survived the checks below.  Together with the published Erdős–Pach upper
bound already built into the official problem record, it proves

\[
h(n)=\Theta(n^{4/3}).
\]

The lower proof is a public note, not a peer-reviewed paper.  The associated
Lean file compiles, but it is **not** a formal proof of this result: it proves
only numerical estimates and a few coordinate inequalities, without defining
the convex body, disjoint translates, set-distance, or \(h(n)\).

## Source and attribution audit

Valtr's 2005 manuscript proves that one fixed strictly convex norm admits
\(\Theta(n^{4/3})\) unit distances.  It reformulates this as
\(\Theta(n^{4/3})\) touching pairs among translates of the norm ball, but
explicitly allows the translates to overlap.  Therefore that manuscript alone
does not meet #956's pairwise-disjoint hypothesis.

Valtr's abstract in *Oberwolfach Report 17/2005*, pp. 985–986, separately
defines \(t_2(n)\) using **pairwise disjoint translates** and announces
\(t_2(n)=\Theta(n^{4/3})\), with centrally symmetric translates.  The abstract
says only that the talk outlines a construction; it contains no proof.

The 2026 note appropriately identifies its counting mechanism as Valtr's
parabolic-grid mechanism and supplies the missing written conversion: replace
the norm ball by a very small difference body whose Euclidean unit parallel
boundary contains the required parabolic arc.  This attribution is consistent
with both fixed Valtr sources.

## Difference-body reduction

For compact convex \(C\), let \(D=C-C\).  Direct substitution gives

\[
\delta(C+x,C+y)=\operatorname{dist}(y-x,D)
\]

and

\[
(C+x)\cap(C+y)=\varnothing\quad\Longleftrightarrow\quad y-x\notin D.
\]

Conversely, if \(D\) is centrally symmetric, compact and convex, then
\(C=D/2\) satisfies

\[
C-C=(D-D)/2=(D+D)/2=D.
\]

The equivalences include boundary contact, so the later strict spacing
inequalities really do prove pairwise disjointness rather than merely
interior-disjointness.

## The small convex body and exact unit offset

For \(0<W\leq1\), put \(\eta=W^4\) and

\[
\gamma(t)=(t,1+\eta-t^2/2),\qquad
\nu(t)=\frac{(t,1)}{\sqrt{1+t^2}},\qquad
p(t)=\gamma(t)-\nu(t)
\]

for \(0\leq t\leq W\), and let

\[
D_W=\operatorname{conv}\{\pm p(t):0\leq t\leq W\}.
\]

The three points \(p(0),-p(0),p(W)\) are non-collinear, so \(D_W\) is a
genuine centrally symmetric compact convex body.  The elementary reciprocal
square-root bounds in Lemma 1 give

\[
0\leq p_x(t)\leq W^3/2,\qquad 0\leq p_y(t)\leq W^4,
\]

and hence

\[
D_W\subset[-W^3/2,W^3/2]\times[-W^4,W^4].
\]

For Lemma 2, the displayed algebra was independently expanded.  Writing
\(r_u=\sqrt{1+u^2}\), it is exactly true that

\[
\langle p(t)-p(s),\nu(t)\rangle
=\frac{(s-t)^2}{2r_t}
-\left(1-\frac{1+st}{r_sr_t}\right),
\]

while

\[
1-\frac{1+st}{r_sr_t}
=\frac{(s-t)^2}{r_sr_t(r_sr_t+1+st)}.
\]

Since \(r_s(r_sr_t+1+st)\geq2\), \(p(t)\) maximizes the
\(\nu(t)\)-support functional over all \(p(s)\).  Both coordinates of
\(p(s)\) and \(\nu(t)\) are nonnegative, so the negative generators
\(-p(s)\) also lie in the same supporting half-plane.  Finally
\(\|\nu(t)\|_2=1\) and \(\gamma(t)-p(t)=\nu(t)\).  Therefore

\[
\operatorname{dist}(\gamma(t),D_W)=1
\]

for every \(0\leq t\leq W\), not merely at the sampled parameters.

## Pairwise-disjoint translates

Fix \(0<\alpha\leq1/10\) and integer \(k\geq2\), and set

\[
W=\alpha/k,\quad
a=\alpha/k^2,\quad
b=\alpha^2/(2k^4),\quad
\eta=\alpha^4/k^4.
\]

The two grids are

\[
L=\{(ra,sb):0\leq r\leq k,\ 0\leq s\leq k^2\},
\]

\[
U=\{(ra,1+\eta+sb):0\leq r\leq k,\ 0\leq s\leq k^2\}.
\]

Within either grid, every nonzero difference has a coordinate of magnitude
at least \(a>W^3/2\) or \(b>\eta\).  Between the grids, the vertical
coordinate has magnitude at least

\[
1+\eta-k^2b
=1+\eta-W^2/2
\geq1-\alpha^2/2>\eta.
\]

Thus no nonzero difference of \(X_k=L\cup U\) belongs to \(D_W\).  Taking
\(C=D_W/2\), the difference-body criterion proves that all
\((C+x)_{x\in X_k}\) are pairwise disjoint.  The argument uses the same
single compact convex \(C\) for the whole \(n_k\)-point configuration.

## Unit-distance pairs and count

For each \(1\leq i\leq k\), \(t_i=ia\) lies in \((0,W]\) and

\[
\gamma(t_i)=(ia,1+\eta-i^2b).
\]

For every

\[
0\leq r\leq k-i,\qquad i^2\leq s\leq k^2,
\]

the lower-grid point \((ra,sb)\) and upper-grid point
\(((r+i)a,1+\eta+(s-i^2)b)\) have precisely this difference.  The pairs are
distinct, and Lemma 2 plus the difference-body identity makes their set
distance exactly one.  Their number is

\[
M_k=\sum_{i=1}^{k}(k+1-i)(k^2+1-i^2)
=\frac5{12}k^4+\frac16k^3+\frac1{12}k^2+\frac13k.
\]

Meanwhile

\[
n_k=|X_k|=2(k+1)(k^2+1)=2k^3+O(k^2).
\]

Consequently \(M_k\geq c_1n_k^{4/3}\) for a fixed \(c_1>0\) and all
sufficiently large \(k\).

## Every sufficiently large \(n\)

The construction is not restricted to the subsequence \(n_k\).  Given large
\(n\), choose the maximal \(k\) with \(n_k\leq n\).  If

\[
\|v\|>\sup_{d\in D_W}\|d\|+\sup_{x\in X_k}\|x\|,
\]

then points \(v,2v,\ldots,(n-n_k)v\) have every mutual and old-to-new
difference outside \(D_W\).  Adding their translates preserves pairwise
disjointness and cannot remove an old unit-distance pair.  Since
\(n_{k+1}/n_k\to1\), a smaller absolute constant gives

\[
h(n)\geq c_0n^{4/3}
\]

for **all** sufficiently large integers \(n\).  Combining this with the
Erdős–Pach \(O(n^{4/3})\) bound yields the asserted \(\Theta\)-order.  In
particular, for every fixed \(c<1/3\),
\(c_0n^{4/3}>n^{1+c}\) once \(n\) is large enough.

## Lean artifact boundary

The downloaded file `erdos956.lean` was checked with:

- Lean `4.27.0`, commit
  `db93fe1608548721853390a10cd40580fe7d22ae`;
- mathlib commit
  `a3a10db0e9d66acbebf76c5e6a135066525ac900`;
- command `lake env lean erdos956.lean`.

It exits successfully, with linter warnings only, and contains no `sorry`,
`admit`, or added axiom.  What it actually proves is:

- the polynomial closed form for \(M(k)\);
- numerical lower bounds comparing \(M(k)\) and `gridSize k`;
- coordinate bounds for the individual offset point \(p(t)\);
- \(\|\nu(t)\|^2=1\);
- two scalar spacing inequalities;
- an eventual numerical inequality
  \(C\,\mathrm{gridSize}(k)^{4/3}\leq M(k)\).

It does **not** define \(D_W\) as a convex hull, \(C=D_W/2\), the grids as
point sets, translations, compactness, convexity, Euclidean set-distance,
pairwise disjointness, or \(h(n)\).  It omits the supporting-hyperplane proof
that \(\operatorname{dist}(\gamma(t),D_W)=1\), the realization and
distinctness of the counted pairs, the padding argument from \(n_k\) to all
large \(n\), and the Erdős–Pach upper bound.  The theorem named
`erdos_956_lower_bound` is only about the two numerical sequences
`gridSize` and `M`; it has no hypothesis or conclusion connecting either
sequence to a convex-translate configuration.

Accordingly:

- Lean file compiles: **yes**;
- Lean file formally proves #956: **no**;
- handwritten note supplies the closure proof: **yes**.

## Timing

- Start: `2026-07-23T19:59:46+08:00`
- End: `2026-07-23T20:07:19+08:00`
- Active agent time: `453 s = 0.125833 agent-hours`
- Budget ceiling: `1 agent-hour`
