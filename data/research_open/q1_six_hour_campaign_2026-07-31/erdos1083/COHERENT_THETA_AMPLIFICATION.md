# Erdős #1083: coherent theta amplification from long path energy

Date: 2026-08-01

## 0. Result

The shared-endpoint path argument can be iterated far enough to force
a genuinely network-level coherent chart.

Using length-80 simple paths in the fixed nonzero-difference graph,
one first obtains a family of

\[
 t^{199/18+o(1)}
\]

paths having the same two endpoint rows, the same source label at
both endpoints, and the same complete orientation word.

Relative to one reference path, either a positive proportion of this
family gives nontrivial homogeneous height relations on at most 158
rows, or a positive proportion has one common internal-defect vector.
In the zero-defect subcase, four exact midpoint refinements produce

\[
 \boxed{t^{1/72+o(1)}}
\]

distinct internally coherent length-five paths with the same two
lifted endpoints and the same orientation word.

Those length-five paths satisfy a second dichotomy.  Either:

1. one fixed internal lifted row lies on
   \(t^{1/144+o(1)}\) paths; or
2. there are \(t^{1/144+o(1)}\) pairwise internally
   vertex-disjoint coherent length-five paths between the same lifted
   endpoints.

The second alternative is a coherent theta graph with a
power-growing number of arms.  Every pair of arms is a simple
coherent cycle of length ten, and all internal rows lie on the four
fixed parabolic potential levels dictated by one orientation word.

This is still conditional on the common defect vector being zero.
The nonzero common-defect branch remains a precise obstruction rather
than being silently discarded.

**Subsequent strengthening.**  `DEFECT_TRANSITION_TRICHOTOMY.md`
removes this zero-defect restriction.  Transition misalignment forces
a noncoherent cycle; transition alignment gives fixed coherent gaps,
which sharpen the theta-or-hub exponent from \(1/144\) to \(1/20\).

## 1. The length-80 path bundle

Retain the notation and the permanently selected labelled
undirected graph from `SHARED_ENDPOINT_PATH_ENERGY.md`:

\[
 n\le t^{13/18+o(1)},
 \qquad
 m=t^{8/9+o(1)},
 \qquad
 S=t^{7/9+o(1)}.
\tag{1.1}
\]

The pruned simple-path lemma with \(L=80\) gives two ordered rows
\(u,v\) joined by

\[
 t^{L/6-13/18+o(1)}
 =t^{227/18+o(1)}
\tag{1.2}
\]

oriented simple paths of length 80.  There are \(S^2\) endpoint
source-label pairs and only \(2^{80}\) complete orientation words.
After fixing both, the surviving family \(\mathcal P_0\) has

\[
 |\mathcal P_0|
 =t^{227/18-14/9+o(1)}
 =\boxed{t^{199/18+o(1)}}.
\tag{1.3}
\]

For any \(P,Q\in\mathcal P_0\), the exact path subtraction is

\[
 \sum_w z_w\bigl(D_P(w)-D_Q(w)\bigr)=0.
\tag{1.4}
\]

Its support has size at most \(2(80-1)=158\).  Fix \(Q\).  Either at
least half the paths have \(D_P\ne D_Q\), giving a nontrivial
homogeneous bounded-support relation through (1.4), or at least half
satisfy

\[
 D_P=D_Q.
\tag{1.5}
\]

If the common vector in (1.5) is nonzero, every path contains its
fixed support of at most 79 defect rows.  This is the explicit
nonzero-defect obstruction.

The rest of this note treats the zero-defect subcase

\[
 D_P=0
 \qquad(P\in\mathcal P_0'),
\tag{1.6}
\]

where \(|\mathcal P_0'|=t^{199/18+o(1)}\).  Every path in
\(\mathcal P_0'\) is internally coherent.

## 2. One midpoint refinement

### Lemma 1 (coherent midpoint refinement)

Let \(\mathcal P\) be \(N\) distinct internally coherent paths of a
common even length \(L\), with:

- the same lifted endpoints \((u,x_u),(v,x_v)\); and
- the same complete orientation word.

Then there is a family of at least

\[
 \boxed{(N/n)^{1/2}}
\tag{2.1}
\]

distinct internally coherent paths of length \(L/2\), again with the
same lifted endpoints and orientation word.

#### Proof

Write

\[
 F(w,x)=z_w^2+2\rho z_wx.
\]

Coherence and the fixed orientation word determine the potential at
the midpoint exactly:

\[
 F(v_{L/2},x_{L/2})
 =F(u,x_u)-\delta\sum_{r=1}^{L/2}\sigma_r.
\tag{2.2}
\]

For each fixed row \(w\), its nonzero height \(z_w\) makes (2.2)
linear in the source label, so at most one \(x\in X\) can occur.
There are at most \(n\) lifted midpoint choices.  Pigeonholing gives
a subfamily of at least \(N/n\) full paths through one common lifted
midpoint.

Let \(A\) be the number of distinct first halves and \(B\) the number
of distinct second halves in this subfamily.  A full path is
determined by its ordered pair of halves, so

\[
 AB\ge N/n.
\]

At least one of \(A,B\) is at least \((N/n)^{1/2}\).  Keep one
representative of every distinct half on that side.  Coherence,
lifted endpoints, and the relevant orientation subword are inherited.
This proves (2.1). \(\square\)

The lemma uses the row bound \(n\), not the weaker \(2S\) quadratic
root bound; it therefore does not require globally distinct height
values.

## 3. Four refinements: 80 to 5

Write \(b_r\) for the base-\(t\) exponent of the family after \(r\)
refinements.  Since \(n=t^{13/18+o(1)}\), Lemma 1 gives

\[
 b_{r+1}=\frac12\left(b_r-\frac{13}{18}\right).
\tag{3.1}
\]

Starting from \(b_0=199/18\), the exact ledger is:

| refinement | path length | family exponent |
|---:|---:|---:|
| 0 | 80 | \(199/18\) |
| 1 | 40 | \(31/6\) |
| 2 | 20 | \(20/9\) |
| 3 | 10 | \(3/4\) |
| 4 | 5 | \(1/72\) |

Indeed,

\[
 \frac12\left(\frac34-\frac{13}{18}\right)
 =\frac1{72}>0.
\tag{3.2}
\]

Thus there are two fixed lifted rows joined by

\[
 K=t^{1/72+o(1)}
\tag{3.3}
\]

distinct coherent simple paths of length five, all carrying one
fixed five-sign orientation word.

The length five endpoint is close to optimal for this midpoint
scheme.  Iterating toward length four would leave the limiting
exponent

\[
 \frac46-\frac{13}{18}=-\frac1{18},
\]

whereas length five leaves \(1/9\) before the finite initial
endpoint-label cost is accounted for.

## 4. Theta-or-hub extraction

### Theorem 2 (coherent theta-or-hub)

From the \(K\) paths in (3.3), one can extract one of:

1. one fixed internal lifted row lying on at least
   \(K^{1/2}/4\) paths; or
2. at least \(K^{1/2}/4\) paths whose interiors are pairwise
   vertex-disjoint.

In endpoint notation, both lower bounds are

\[
 t^{1/144+o(1)}.
\tag{4.1}
\]

#### Proof

If some internal row occurs on at least \(K^{1/2}\) paths, one of the
four internal positions contains it on at least \(K^{1/2}/4\) paths.
The potential at that position is fixed by the common orientation
word, so the source label on the row is unique.  This is the first
alternative.

Otherwise every internal row occurs on fewer than \(K^{1/2}\) paths.
Greedily choose a path and discard every remaining path sharing one
of its four internal rows.  Each choice discards fewer than
\(4K^{1/2}\) paths, so at least \(K^{1/2}/4\) paths are selected.  Their
interiors are pairwise vertex-disjoint. \(\square\)

In the second branch, every two selected paths have only their two
endpoints in common.  Their union is therefore a simple cycle of
length ten.  Internal coherence and the common endpoint source
labels make this cycle coherent.  The two copies of the same
orientation word are traversed in opposite directions, so its sign
sum is zero.

Moreover, at internal position \(r\in\{1,2,3,4\}\), all selected
lifted vertices satisfy the one fixed equation

\[
 z^2+2\rho zx
 =F(u,x_u)-\delta\sum_{j=1}^{r}\sigma_j.
\tag{4.2}
\]

Thus the theta graph contains \(t^{1/144+o(1)}\) distinct rows on each
of four prescribed parabolic potential levels (with possible equality
between levels if the sign walk revisits a position).

## 5. Exact scope

What is now proved in the zero-defect branch is stronger than merely
having many uncoordinated cycles:

- both endpoint rows and their source labels are fixed;
- every arm is simple, coherent, and has the same orientation word;
- either an internal lifted row is highly reused, or the arms have
  disjoint interiors;
- the theta branch gives a power-growing bounded-level potential
  chart on distinct rows.

What is not proved is that either outcome already exceeds the common
distance budget.  The next exact-block input must control tangent or
distance-label reuse along the common lifted endpoint and the four
fixed potential levels.  The common nonzero-defect branch in (1.5)
also remains open; it should be attacked by fixing the order of its
at most 79 mandatory defect rows and applying the same midpoint
argument on the coherent gaps.
