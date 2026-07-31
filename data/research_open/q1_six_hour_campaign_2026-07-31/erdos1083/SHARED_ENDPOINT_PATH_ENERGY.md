# Erdős #1083: shared-endpoint path energy in the fixed-difference graph

Date: 2026-08-01

## 0. Verdict

The fixed-difference transverse graph forces a substantially stronger
shared-endpoint object than the edge-disjoint short-cycle theorem.
There are two rows \(u,v\) joined by

\[
 t^{16/9+o(1)}
\]

distinct simple paths of length fifteen.  After fixing the source
label at each endpoint and the signed orientation sum, a bundle of

\[
 \boxed{t^{2/9+o(1)}}
\]

paths remains.

Subtracting any two path identities in this bundle cancels both
quadratic endpoint terms, both endpoint source terms, and the
fixed-\(\delta\) right-hand side.  It gives either:

- a nontrivial homogeneous height relation supported on at most 28
  internal rows, with coefficients in
  \((X-X)-(X-X)\); or
- identical internal-defect vectors for the two paths.

Thus a fixed reference path yields a rigorous dichotomy: many sparse
homogeneous height relations, or a \(t^{2/9+o(1)}\)-scale bundle with
one common defect vector.  If that vector is zero, every path in the
bundle is internally coherent.  If it is nonzero, all paths pass
through its bounded set of defect rows and are coherent away from
those rows.

This is not yet a contradiction, but it is the first result that
simultaneously fixes two endpoint rows and their source labels on a
power-growing family of paths.

## 1. The labelled simple graph

Start with the fixed nonzero difference \(\delta\) directed graph from
`TRANSVERSE_NONZERO_DIFFERENCE_THEOREM.md`.  For a fixed ordered
transverse row pair and fixed \(\delta\), the source-label pair is
unique.  Hence this is a simple directed graph at the row-pair level.

Forget orientations and merge opposite directed edges.  The resulting
simple graph \(H\) has

\[
 n\le q=t^{13/18+o(1)},
 \qquad
 m=t^{8/9+o(1)}.
\tag{1.1}
\]

For each undirected edge, permanently choose one directed edge above
it and one coincidence record witnessing that edge.  At each endpoint
\(w\) of an edge \(e\), denote the record's source label by

\[
 \alpha_e(w)\in X.
\]

Also retain the chosen direction of \(e\).  Nothing below assumes that
the projection from full records is injective: one witness is simply
selected once and for all.

## 2. A lower bound for simple paths

### Lemma 1 (pruned simple-path count)

Let \(H\) be a simple graph with \(n\) vertices and \(m\) edges, and
put

\[
 a=\frac{m}{2n}.
\]

If \(a>L\), then the number of oriented simple paths of length \(L\)
in \(H\) is at least

\[
 m\prod_{j=1}^{L-1}(a-j).
\tag{2.1}
\]

#### Proof

Iteratively delete vertices of current degree less than \(a\).  Fewer
than \(an=m/2\) edges are deleted, so the remaining nonempty graph
\(H'\) has

\[
 e(H')>m/2,
 \qquad \delta(H')\ge a.
\]

There are more than \(m\) choices for the first oriented edge.  Having
chosen distinct vertices \(v_0,\ldots,v_r\), at most \(r\) previously
used vertices are forbidden neighbours of \(v_r\).  There are at
least \(a-r\) choices for \(v_{r+1}\).  Multiplication for
\(r=1,\ldots,L-1\) proves (2.1). \(\square\)

### Corollary 2 (fifteen-step endpoint concentration)

Take \(L=15\).  Since

\[
 \frac mn=t^{1/6+o(1)},
\]

the condition \(a>15\) holds for sufficiently large \(t\).  Dividing
(2.1) by the at most \(n^2\) ordered endpoint pairs, some ordered pair
\((u,v)\) is joined by at least

\[
 \frac{m}{n^2}
 \prod_{j=1}^{14}\left(\frac{m}{2n}-j\right)
 =t^{16/9+o(1)}
\tag{2.2}
\]

oriented simple paths of length fifteen.  The exponent calculation is

\[
 \frac89+14\left(\frac89-\frac{13}{18}\right)
 -2\left(\frac{13}{18}\right)
 =\frac{16}{9}.
\tag{2.3}
\]

## 3. Exact path identity

Let

\[
 P=(v_0=u,v_1,\ldots,v_L=v)
\]

be one of the oriented simple paths, traversed from \(u\) to \(v\).
Let \(e_r=v_{r-1}v_r\).  Put \(\sigma_r=+1\) if the permanently
chosen direction of \(e_r\) agrees with the traversal, and
\(\sigma_r=-1\) otherwise.

The chosen record on \(e_r\) gives

\[
 z_{v_{r-1}}^2-z_{v_r}^2
 +2\rho\left(
 z_{v_{r-1}}\alpha_{e_r}(v_{r-1})
 -z_{v_r}\alpha_{e_r}(v_r)
 \right)
 =\sigma_r\delta.
\tag{3.1}
\]

Define the endpoint labels

\[
 x_P=\alpha_{e_1}(u),
 \qquad y_P=\alpha_{e_L}(v),
\tag{3.2}
\]

the orientation sum

\[
 s_P=\sum_{r=1}^{L}\sigma_r,
\tag{3.3}
\]

and the internal-defect vector, indexed by rows, by

\[
 D_P(w)=
 \begin{cases}
 \alpha_{e_{r+1}}(w)-\alpha_{e_r}(w),
   &w=v_r,\ 1\le r<L,\\
 0,&\text{otherwise}.
 \end{cases}
\tag{3.4}
\]

Because the path is simple, this is unambiguous and has support at
most \(L-1\).  Summing (3.1) telescopes the quadratic terms and gives
the exact identity

\[
 \boxed{
 z_u^2-z_v^2
 +2\rho\left(
 z_u x_P-z_v y_P+
 \sum_w z_wD_P(w)
 \right)
 =s_P\delta.}
\tag{3.5}
\]

The path is internally coherent exactly when \(D_P=0\).

## 4. Endpoint-label energy and homogeneous relations

For \(L=15\), the pair \((x_P,y_P)\) has at most \(S^2\) possible
values and \(s_P\) has only 16 possible values:

\[
 -15,-13,\ldots,13,15.
\]

Pigeonholing the paths from (2.2) gives a bundle \(\mathcal P\) with
the same \((u,v,x_P,y_P,s_P)\) and

\[
 |\mathcal P|
 \ge\frac{t^{16/9+o(1)}}{16S^2}
 =t^{2/9+o(1)},
\tag{4.1}
\]

because \(S=t^{7/9}\).

For \(P,Q\in\mathcal P\), subtract (3.5).  Every endpoint and
right-hand term cancels:

\[
 \boxed{
 \sum_w z_w\bigl(D_P(w)-D_Q(w)\bigr)=0.}
\tag{4.2}
\]

The support has size at most

\[
 2(L-1)=28,
\]

and each coefficient belongs to

\[
 (X-X)-(X-X).
\]

If \(D_P\ne D_Q\), (4.2) is a nontrivial homogeneous bounded-support
height relation.  If \(D_P=D_Q\), the subtraction is the zero
identity.

Fix any \(Q\in\mathcal P\).  Either at least half the other paths have
\(D_P\ne D_Q\), furnishing that many bounded relation witnesses, or
at least half have

\[
 D_P=D_Q.
\tag{4.3}
\]

In the second branch a \(t^{2/9+o(1)}\)-scale shared-endpoint bundle
has one common defect vector.  Two important subcases are immediate:

1. **zero defect:** all paths are internally coherent and lift to the
   same endpoint pair \((u,x_P),(v,y_P)\) in the row--source graph;
2. **nonzero defect:** every path contains the fixed support of
   \(D_Q\), consisting of at most fourteen rows, and is internally
   coherent away from that support.

The last assertion follows directly from (3.4): a nonzero coordinate
of the common vector must be realized at that same row on every path.

## 5. Significance and remaining gap

The exponent \(2/9\) is a real gain, not a constant-size extraction.
Length five only gives \(t^{1/9}\) paths between shared endpoints,
which is below the \(S^2\) endpoint-label capacity.  Length fifteen is
the first odd length in this scheme with a comfortable endpoint-label
surplus:

\[
 \underbrace{16/9}_{\text{path multiplicity}}
 -\underbrace{14/9}_{S^2}
 =\frac29.
\]

What remains is to convert one branch into a distance-budget
contradiction.  In the relation-heavy branch, distinctness or rank of
the sparse coefficient vectors is not yet controlled.  In the
common-defect branch, the many paths can still share internal rows and
edges.  The next useful lemma should therefore bound the number of
simple paths with fixed endpoints and fixed defect vector using the
exact tangent partitions, or prove that such a bundle forces many
distinct common-spectrum labels.
