# Exact-four-path obstruction stability

## 1. Statement with quantified error

All paths in this note are simple.  For graphs \(F_1,F_2\) on the same
vertex set, write
\[
d_\triangle(F_1,F_2)=|E(F_1)\triangle E(F_2)|.
\]

**Lemma 1 (four-path obstruction stability).**  Let \(H\) be a graph on
\(N\) vertices with minimum degree \(d\), and suppose that two distinct
vertices \(u,v\) are not joined by a path of exactly four edges.  Assume
\[
3d>N+6.
\]
Put
\[
t=N-2d,\qquad \Theta=t+4.
\]
Then there is a partition \(V(H)=U\sqcup W\), with
\[
d\le |U|\le N-d+2,
\]
such that, provided
\[
N\ge100(t+10),
\]
one of
\[
d_\triangle(H,K_U\cup K_W)=O((|t|+1)N)                         \tag{1}
\]
or
\[
d_\triangle(H,K_{U,W})=O((|t|+1)N)                            \tag{2}
\]
holds.  (The obstruction itself implies \(t\ge-2\).)  The implicit
constant is absolute.

Consequently, if \(d=N/2-o(N)\), then \(U,W=(1/2+o(1))N\) and \(H\) is
\(o(N^2)\)-close either to the union of two balanced cliques or to a
balanced complete bipartite graph.

The hypothesis is existential in the obstructed pair.  In particular, if a
graph \(G\) fails the property

> after deleting every set of at most two vertices, every remaining pair is
> joined by a path of exactly four edges,

then apply Lemma 1 to the one induced subgraph and the one pair witnessing
failure.  No common partition for all deletion sets is asserted or needed.

## 2. Adding the endpoint edge is safe

If \(uv\notin E(H)\), add it.  A simple four-edge \(u\)-to-\(v\) path in
\(H+uv\) cannot use the new edge: using \(uv\) as its first or last edge
would repeat an endpoint, and it cannot occur internally without repeating
one of \(u,v\).  Thus adding \(uv\) creates no forbidden path.  It also does
not decrease the minimum degree.  We henceforth assume \(uv\in E(H)\).

Set
\[
A=N(u)\cap N(v),
\]
\[
X=N(u)\setminus(A\cup\{v\}),\qquad
Y=N(v)\setminus(A\cup\{u\}),
\]
and let
\[
Z=V(H)\setminus(A\cup X\cup Y\cup\{u,v\}).
\]

The absence of a four-edge \(u\)-to-\(v\) path gives the exact property

\[
\tag{P}
\text{if }a\in A\cup X,\ b\in A\cup Y,\ a\ne b,\text{ then }
N(a)\cap N(b)\subseteq\{u,v\}.
\]

Indeed, any common neighbour \(c\notin\{u,v\}\) would give the simple path
\(u,a,c,b,v\).

## 3. The common neighbourhood has constant size

We first prove
\[
|A|\le2.                                                       \tag{3}
\]
If \(a,b,c\) were three distinct vertices of \(A\), property (P) would give
\[
|N(a)\cap N(b)|,\ |N(a)\cap N(c)|,\ |N(b)\cap N(c)|\le2.
\]
Hence
\[
|N(a)\cup N(b)|\ge2d-2
\]
and
\[
\begin{split}
d(c)
&\le |V\setminus(N(a)\cup N(b))|
   +|N(c)\cap N(a)|+|N(c)\cap N(b)|\\
&\le N-(2d-2)+4=N-2d+6.
\end{split}
\]
Since \(d(c)\ge d\), this implies \(3d\le N+6\), contrary to the
hypothesis.

It follows that
\[
|X|,|Y|\ge d-3,\qquad
|Z|=N-d(u)-d(v)+|A|\le N-2d+2=t+2.                            \tag{4}
\]

## 4. Two complementary neighbourhood types

For every \(x\in X,y\in Y\), property (P) and the degree lower bound give
\[
|N(x)\cap N(y)|\le2,
\]
\[
|V\setminus(N(x)\cup N(y))|
\le N-d(x)-d(y)+2\le t+2.
\]
Therefore
\[
\left|N(x)\triangle\bigl(V\setminus N(y)\bigr)\right|
\le t+4=\Theta.                                                \tag{5}
\]

Fix \(x_0\in X\), \(y_0\in Y\), and define
\[
U=N(x_0),\qquad W=V\setminus U.
\]
Equation (5), used twice, yields
\[
|N(x)\triangle U|\le2\Theta\quad(x\in X),                      \tag{6}
\]
\[
|N(y)\triangle W|\le\Theta\quad(y\in Y).                       \tag{7}
\]
Moreover,
\[
d\le |U|=d(x_0)\le N-d+2,                                     \tag{8}
\]
where the upper bound follows from
\(|N(x_0)\cap N(y_0)|\le2\) and \(d(y_0)\ge d\).

Thus \(X\)-vertices have the common neighbourhood type \(U\), while
\(Y\)-vertices have the complementary type \(W\).

## 5. Symmetry forces one of two global models

Write \(X_U=X\cap U\), \(X_W=X\cap W\).  From (6),
\[
e(X_U,X_W)\le2\Theta|X_U|
\]
and, looking from the \(X_W\) side,
\[
e(X_U,X_W)\ge |X_U||X_W|-2\Theta|X_W|.
\]
Consequently
\[
|X_U||X_W|\le2\Theta|X|.                                      \tag{9}
\]
The smaller of \(X_U,X_W\) therefore has size at most \(4\Theta\).
The same argument using (7) shows that the smaller of
\(Y\cap U,Y\cap W\) has size at most \(2\Theta\).

Since \(X,Y\) each have size \(N/2-o(N)\), while (8) makes \(U,W\)
balanced, the two majority orientations must be complementary once
\(\Theta=o(N)\):

- either almost all of \(X\) lies in \(U\) and almost all of \(Y\) lies
  in \(W\);
- or almost all of \(X\) lies in \(W\) and almost all of \(Y\) lies in
  \(U\).

For completeness, the first forbidden alternative, in which both majorities
lie in \(U\), would imply
\[
|U|\ge |X|+|Y|-6\Theta\ge2d-6-6\Theta,
\]
contradicting \(|U|\le N-d+2\) for \(d=N/2-o(N)\).  The alternative in
which both lie in \(W\) is identical.

Let \(E_0\) consist of \(A,Z,u,v\) and the two minority type classes.
Equations (3), (4), and (9) give
\[
|E_0|=O(|t|+1).                                                \tag{10}
\]

In the first majority orientation, every vertex of \(U\setminus E_0\)
has neighbourhood \(U\) up to \(O(|t|+1)\) errors, and every vertex of
\(W\setminus E_0\) has neighbourhood \(W\) up to the same error.  Summing
these errors and then allowing all edges incident with \(E_0\) proves (1).

In the second orientation, regular vertices in \(U\) have neighbourhood
close to \(W\), and regular vertices in \(W\) have neighbourhood close to
\(U\).  The same count proves (2).

This proves Lemma 1.

## 6. Red-team boundaries

1. The conclusion concerns failure for one specified pair.  It does not
   claim a canonical partition valid for every pair.
2. “Length four” means exactly four edges, not distance at most four.
3. The proof uses adjacency symmetry in (9).  Merely observing that the
   \(X\)-neighbourhoods are similar is not enough without that step.
4. The result is asymptotically useful only when \(N-2d=o(N)\).  It does
   not handle the BCM26 Case-1 range in which \(N/2-d\) is a positive
   linear fraction of \(N\).
