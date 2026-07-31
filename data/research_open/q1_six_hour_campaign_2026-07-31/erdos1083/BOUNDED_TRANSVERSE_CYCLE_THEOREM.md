# Erdős #1083: a bounded transverse cycle on one nonzero tangent difference

Date: 2026-08-01

## 0. Result

The fixed nonzero-difference transverse graph obtained in the
previous theorem is dense enough to contain a cycle of length at most
ten.

Summing its edge equations around the cycle cancels every quadratic
height term.  One obtains one of two exact bounded configurations:

1. a nontrivial affine relation among at most ten heights, with
   coefficients in \(X-X\) and right side an integer multiple of the
   one fixed nonzero difference \(\delta\); or
2. a coherent labelled cycle in which every vertex uses one source
   value and the quantities \(z^2+2\rho zx\) perform a closed
   \(\pm\delta\) arithmetic walk of length at most ten.

This supplies the bounded labelled cycle sought in the diffuse side
of the earlier block-vs-diffuse target.  It does not yet prove that
the cycle is geometrically nondegenerate enough to contradict the
few-distance hypothesis.

## 1. A finite graph lemma

### Lemma 1 (ten-cycle criterion)

Let \(G\) be a simple undirected graph on \(n\) vertices with \(m\)
edges.  Put

\[
 d_0=\frac{m}{n}.
\]

If

\[
 (d_0-1)^5>n,
\tag{1.1}
\]

then \(G\) contains a cycle of length at most ten.

The same conclusion holds for a directed simple graph with \(M\)
ordered edges if

\[
 \left(\frac{M}{2n}-1\right)^5>n.
\tag{1.2}
\]

Here opposite orientations on one unordered pair are allowed.

#### Proof

The undirected graph has average degree \(2m/n=2d_0\).  Repeatedly
delete vertices of degree below \(d_0\).  This cannot delete every
vertex, because each deletion removes fewer than \(d_0\) edges and
the original graph has \(nd_0\) edges.  Thus a nonempty subgraph has
minimum degree at least \(d_0\).

If this subgraph had girth greater than ten, a breadth-first search
to depth five from any vertex would have no collision: two distinct
nonbacktracking paths of total length at most ten reaching the same
vertex would create a cycle of length at most ten.  The search tree
would therefore contain at least

\[
 1+d_0\sum_{j=0}^{4}(d_0-1)^j
 >(d_0-1)^5
\]

vertices, contradicting (1.1).

A directed simple graph with \(M\) ordered edges gives an underlying
simple graph with at least \(M/2\) edges, because each unordered pair
supports at most two orientations.  Apply the first part.  \(\square\)

## 2. The fixed-difference graph

Use the exact-block setup of
TRANSVERSE_NONZERO_DIFFERENCE_THEOREM.md.  That theorem gives one
nonzero \(\delta\) and a directed graph \(\vec G_\delta\) whose
vertices are rows and whose ordered edges \((i,j)\) have:

\[
 W_i\cap W_j=\{0\},
\tag{2.1}
\]

and a unique source pair \((x_{ij},x'_{ij})\in X^2\) satisfying

\[
 z_i^2-z_j^2
 +2\rho(z_ix_{ij}-z_jx'_{ij})
 =\delta.
\tag{2.2}
\]

At the frozen endpoint,

\[
 |V(\vec G_\delta)|
 \le q=t^{13/18+o(1)}
\tag{2.3}
\]

and

\[
 |E(\vec G_\delta)|
 \ge t^{8/9+o(1)}.
\tag{2.4}
\]

The underlying average-degree scale is therefore

\[
 \frac{|E|}{q}=t^{1/6+o(1)}.
\tag{2.5}
\]

Its fifth power has exponent \(5/6\), strictly greater than the
vertex exponent \(13/18\), with margin

\[
 \frac56-\frac{13}{18}=\frac19.
\tag{2.6}
\]

Hence Lemma 1 applies for sufficiently large \(t\).

### Theorem 2 (bounded transverse cycle)

The transverse-heavy branch contains a simple undirected cycle

\[
 v_1v_2\cdots v_\ell v_1,
\qquad 3\le\ell\le10,
\tag{2.7}
\]

such that every cycle edge is represented by an ordered transverse
edge satisfying (2.2) with the same nonzero \(\delta\).

## 3. Exact cycle identity

Choose one of the available directed records for each undirected
cycle edge.  Traverse the cycle from \(v_k\) to \(v_{k+1}\), with
indices modulo \(\ell\).  Let

\[
 \sigma_k=
 \begin{cases}
 +1,&\text{if the chosen record points from }v_k\text{ to }v_{k+1},\\
 -1,&\text{if it points from }v_{k+1}\text{ to }v_k.
 \end{cases}
\tag{3.1}
\]

Let \(a_k\in X\) be the source label attached to \(v_k\) on the
outgoing traversed edge \(v_kv_{k+1}\), and let \(b_k\in X\) be the
source label attached to \(v_k\) on the incoming traversed edge
\(v_{k-1}v_k\).

Orienting every edge equation along the traversal and summing
cancels the quadratic terms:

\[
 \sum_{k=1}^{\ell}(z_{v_k}^2-z_{v_{k+1}}^2)=0.
\]

What remains is the exact identity

\[
 \boxed{
 2\rho\sum_{k=1}^{\ell}z_{v_k}(a_k-b_k)
 =\delta\sum_{k=1}^{\ell}\sigma_k.}
\tag{3.2}
\]

Every coefficient \(a_k-b_k\) lies in \(X-X\), and

\[
 \sum_k\sigma_k\in\{-\ell,-\ell+2,\ldots,\ell-2,\ell\}.
\]

### Corollary 3 (bounded cycle dichotomy)

One of the following holds.

1. **Noncoherent affine relation.**  Some \(a_k-b_k\ne0\), and (3.2)
   is a nontrivial relation among at most ten distinct heights.  If
   the cycle length is odd, this branch is automatic, because
   \(\sum_k\sigma_k\) is odd and cannot vanish.
2. **Coherent arithmetic-potential cycle.**  For every \(k\),

   \[
   a_k=b_k=:x_k,
   \tag{3.3}
   \]

   and necessarily

   \[
   \sum_k\sigma_k=0.
   \tag{3.4}
   \]

   Define

   \[
   F_k=z_{v_k}^2+2\rho z_{v_k}x_k.
   \tag{3.5}
   \]

   Along every traversed edge,

   \[
   F_k-F_{k+1}=\sigma_k\delta.
   \tag{3.6}
   \]

   Hence all \(F_k\)'s lie in an arithmetic progression of at most
   eleven positions and common nonzero step \(\delta\), and they form
   a closed \(\pm\delta\) walk.

#### Proof

If all coefficients in (3.2) vanish, its left side is zero.  Since
\(\delta\ne0\), the sign sum must vanish, giving (3.3)--(3.4).
Substituting the coherent endpoint labels into each oriented edge
equation gives (3.6).  Otherwise (3.2) is the first branch.  On an
odd cycle, a sum of \(\ell\) signs cannot be zero.  \(\square\)

## 4. Why this is a key node but not closure

The theorem turns a global \(t^{19/9}\) tangent-overlap surplus into
an \(O(1)\)-size exact algebraic object.  It avoids:

- zero tangent difference;
- rationally nontransverse edges;
- repeated source-pair ambiguity on an edge; and
- unbounded cycle length.

What remains is a finite classification problem.

- In branch 1, one must show that the coefficient pattern in (3.2)
  is sufficiently nondegenerate to pin several heights or force a
  ruled affine chart.
- In branch 2, one must show that the coherent arithmetic potential
  (3.5)--(3.6), together with pairwise transverse adjacent spaces,
  cannot recur with the critical mass, or else extract a
  distance-expanding subsystem.

The present theorem guarantees one bounded cycle, not a positive
power of vertex-disjoint cycles.  It therefore does not yet yield an
exponent improvement for #1083.
