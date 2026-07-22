# Round 8 geometry/group-theory workflow report

Date: 2026-07-22 (Asia/Hong_Kong)

Problems: #325, #827, #934, #1083.

Strict verdict: **NO ORIGINAL CLOSURE / NO Q2 STOPPING RESULT**.  The strongest
positive outcome is a new \(O(t)\) near-reflection stability theorem and stable
coaxiality criterion for #1083.  The other three investigations either expose
an exact obstruction to the former route or isolate a structural lemma still
missing a global counting step.

## #325 — pointwise quartic coercivity is false

The Hadamard-coordinate identities and chamber split from the old route are
correct.  Its intended last step is not: the hard chamber contains the exact
equal-biquadrate ray

\[
158^4+59^4=134^4+133^4.
\]

For \((158T+1,59T;134T,133T)\), the relevant coordinates are exactly

\[
u=1-50T,\quad h=1+98T,\quad v=1+316T-7200T^2,
\]
\[
s=1+632T+149784T^2+15777248T^3.
\]

Consequently the desired uniform bounds
\(|u|=O(|s|^{1/4})\) and \(|v|=O(|s|^{1/2})\) both fail.  This does not refute
the Erdős problem; it refutes only a pointwise shifted-fibre proof.  The next
credible route is an *averaged* signature sum, separating a tube around the
quartic zero cone from a transverse determinant-method region.  No such
average estimate was proved this round.

Classification: `EXACT_ROUTE_REJECTION / ORIGINAL OPEN / NO Q2`.

## #827 — antipodal triples destroy the naive hypergraph route

The window and joint-deletion identities are valid but saturate unless one
obtains a genuine additive-energy saving.  A proposed (K_{2,2,2})-free
semialgebraic shortcut is exactly false: whenever the complex numbers
\(a^2,b^2,c^2\) are collinear, all eight triangles selecting one point from
each antipodal pair \(\{\pm a\},\{\pm b\},\{\pm c\}\) have the same circumradius.
The rational general-position configuration

\[
\pm(1,0),\qquad \pm(1,1),\qquad \pm(2,3)
\]

has no three collinear and no four cocircular, yet all eight transversal
triangles have \(R^2=25/2\).  A viable redesign must quotient antipodal signs
before using inverse additive theory and mixed-derivative positivity.  That
inverse theorem is still missing.

Classification: `EXACT_GEOMETRIC_OBSTRUCTION / ORIGINAL OPEN / NO Q2`.

## #934 — useful two-sided structure; quasirandom gain is vacuous

In the normalized index-two Cayley model, with
\(U=AA^{-1}\), \(V=A^{-1}A\), \(C=K\setminus U\), and
\(D'=K\setminus V\), the defect relation yields the strict dual containments

\[
A^{-1}CA\subseteq V,\qquad AD'A^{-1}\subseteq U,
\]

and hence \(AD'\cap CA=\varnothing\).  Thus adjoining a translate on either
side can double \(A\) without enlarging the associated one-sided difference
set.  This is a genuine no-growth structure, but a stabilizer/energy theorem
is still needed to turn it into a numerical improvement.

A tempting Babai--Nikolov--Pyber mixing calculation was independently
rejected rather than promoted.  Although it formally gives \(rc\le N^2/D\)
and the hypothesis \(D\ge11r\) would beat \(253/225\), the hypothesis is empty
in the target range: the regular representation and the existing
\(N<2r^2\) bound force

\[
D\le\sqrt{N-1}<\sqrt2\,r.
\]

Classification: `RIGOROUS_COMPONENT + VACUOUS_ROUTE_REJECTION / NO Q2`.

## #1083 — \(O(t)\) near-reflection stability and stable coaxiality

Let \(P\subset\mathbb R^3\) have \(n\) points and \(t\) nonzero distances, and
write \(e_\pi=|\{p\in P:s_\pi(p)\notin P\}|\).  The round proves the following
chain of statements.

1. If \(T\) is a nonzero translation, an infinite-order rotation, or a
   rotation of order \(m>2t+1\), then
   \[
   n\le(e_T+1)(t+1).
   \]
2. For two different reflection planes, either their product is a rotation
   of order at most \(2t+1\), or
   \[
   n\le(e_\pi+e_\sigma+1)(t+1).
   \]
3. Put \(\mathcal R_E=\{\pi:e_\pi\le E\}\).  If
   \((2E+1)(t+1)<n\), the KKPR rational-angle classification first gives at
   most 15 planes or a perpendicular configuration.  In the latter branch,
   projective normal directions lie on \(\mathbb R/\mathbb Z\), and every
   pairwise difference has denominator at most \(M=2t+1\).  Each cyclically
   adjacent gap is therefore at least \(1/M\); since the gaps sum to one,
   there are at most \(M\) in-plane directions.  Including the single possible
   perpendicular exception gives the uniform sharp-scale bound
   \[
   \boxed{|\mathcal R_E|\le\max\{15,2t+2\}.}
   \]
   若退化分支的 \(M\) 个面内方向取到上限，则所有间隙都等于 \(1/M\)，
   方向集恰是一个循环子群的陪集，即精确二面群方向。
   正奇数 \(M\)-边形嵌入 \(\mathbb R^3\) 时有 \(t=(M-1)/2\) 种距离、
   \(M\) 张竖直镜面及承载平面本身，故实际达到 \(M+1=2t+2\) 的等号。
4. For three pairwise nonparallel affine reflection lines in the perpendicular
   two-dimensional quotient, \(r_1r_2r_3\) is a pure reflection **if and only
   if** the three lines are concurrent.  Otherwise it is a nontrivial glide
   reflection and its square is a nonzero translation.  Hence under
   \((6E+1)(t+1)<n\), every plane in the common-direction subfamily shares one
   affine axis (apart from the possible KKPR exceptional plane).
5. A product rotation of order \(m\) has at least
   \(n-(e_\pi+e_\sigma)(m-1)\) points in complete rotation orbits.

The \(O(t)\) count corrects this round's preliminary \(O(t^2)\) Farey bound:
the latter used only differences from one base direction and discarded the
pairwise constraint.  An earlier \(O(t^4)\) spherical-polynomial estimate is
also correct but fully superseded.  The exact remaining bottleneck is to
connect the extreme small-defect, near-dihedral layer to the medium-defect
reflection energy responsible for the \(3/5\) critical spectrum.  Thus the
result is a potentially useful new structural theorem, not yet a Q2 main
theorem and not an improvement of the official distance exponent.

External input used transparently: Kedlaya--Kolpakov--Poonen--Rubinstein,
*Space vectors forming rational angles*, arXiv:2011.14232, Theorem 1.2,
<https://arxiv.org/abs/2011.14232>.

Classification:
`RIGOROUS_O(t)_STABILITY + STABLE_COAXIALITY / ORIGINAL OPEN / NO Q2`.

## Workflow ranking and boundary

1. Strongest new positive result: #1083 \(O(t)\) near-reflection theorem and
   the length-six stable-coaxiality mechanism.
2. Strongest route correction: #325's exact quartic-cone obstruction.
3. Clean geometric obstruction: #827's general-position antipodal radius cube.
4. Useful algebraic component: #934's two-sided no-growth inclusions; the
   proposed quasirandom numerical gain was correctly rejected as vacuous.

All universal statements are proved in the accompanying Markdown files;
exact scripts audit constants, algebraic identities, and finite examples.
No finite computation is promoted to an infinite theorem.  None of the four
original Erdős questions is claimed closed, and no result meets the stipulated
SCI-Q2 stopping gate without a new exponent/order or a broader application.

Budget accounting: unified interval 08:52:14--10:22:14; 5,400 active seconds
charged across #325 (900), #827 (900), #934 (1,500), and #1083 (2,100).
Files were frozen after the boundary at 10:22:24 (Asia/Hong_Kong).
