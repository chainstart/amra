# A near-Dirac theorem for rainbow \(C_7\) colourings

## 1. Main result

Call two edges \(C_7\)-compatible if a copy of \(C_7\) contains both.

**Theorem A.**  Let \(G_n\) be a sequence of \(n\)-vertex graphs such that
\[
e(G_n)>\lfloor n^2/4\rfloor,\qquad
\delta(G_n)\ge n/2-o(n).
\]
If the edges of \(G_n\) are coloured so that every copy of \(C_7\) is
rainbow, then the number of colours is at least
\[
n^2/8-o(n^2).
\]

The proof is independent of bounded computation.  It uses the R004
near-complete-split theorem, and proves the three other structural branches
needed to remove R004's split hypothesis.

## 2. Robust exact-four-path property

Write \(L_4(2)\) for the following property:

> for every \(T\subseteq V(G)\) with \(|T|\le2\), every two distinct
> vertices of \(G-T\) are joined in \(G-T\) by a simple path of exactly
> four edges.

We first handle graphs satisfying \(L_4(2)\).

### Lemma 2.1: edge distance zero or one

For edges \(xy,zw\), put
\[
d_E(xy,zw)=\min\{d(x,z),d(x,w),d(y,z),d(y,w)\}.
\]

If \(G\) satisfies \(L_4(2)\) and \(\delta(G)\ge3\), any two distinct
edges with \(d_E\le1\) are \(C_7\)-compatible.

For adjacent edges \(xy,xz\), choose
\[
u\in N(y)\setminus\{x,z\}
\]
and an exact four-edge \(u\)-to-\(z\) path in \(G-\{x,y\}\).  Together
with \(xy,yu,zx\), it is a seven-cycle.

For disjoint edges \(xy,zw\) with, say, \(xz\in E(G)\), take an exact
four-edge \(y\)-to-\(w\) path in \(G-\{x,z\}\).  Adding
\(xy,xz,zw\) again gives a seven-cycle.  The other endpoint orientations
are symmetric.

Thus two edges of the same colour have edge distance at least two.

### Lemma 2.2: three same-colour edges force distance two

Assume also \(3\delta(G)>n\).  Any colour class with at least three edges
contains two edges at edge distance exactly two.

Indeed, if three such edges were pairwise at edge distance at least three,
the sets
\[
D(xy)=N(x)\cup N(y)
\]
would be pairwise disjoint.  Each has size at least \(\delta(G)>n/3\),
which is impossible.  Lemma 2.1 excludes distances zero and one.

### Lemma 2.3: a distance-two pair gives a no-three-step certificate

Let same-colour edges \(xy,zw\) have edge distance two, and choose a
shortest endpoint path
\[
x-a-z.
\]
The edges are disjoint, and no endpoint of one is adjacent to an endpoint
of the other.  In particular
\[
x,a,z,y,w
\]
are distinct and \(yw\notin E(G)\).

If \(G-\{x,a,z\}\) contained a simple three-edge path from \(y\) to \(w\),
that path together with
\[
y-x-a-z-w
\]
would be a simple seven-cycle containing both same-colour edges.  Hence no
such path exists.

This checks both possible degeneracies: adjacent specified edges were
already excluded by Lemma 2.1, and adjacency of the two outer endpoints
would itself make their edge distance one.

## 3. The no-three-step dichotomy

We restate the exact R003 neighbourhood lemma.  Let \(u,v\) be nonadjacent,
\(S\cap\{u,v\}=\varnothing\), \(|S|=s\), and suppose \(G-S\) has no
three-edge \(u\)-to-\(v\) path.  Put
\[
P=N(u)\setminus S,\quad Q=N(v)\setminus S,\quad
R=P\cap Q,
\]
\[
W=(P\cup Q)\setminus R,\qquad Z=V\setminus(P\cup Q).
\]
Any distinct \(p\in P,q\in Q\) are nonadjacent.

There are two branches.

### Branch I: \(R\ne\varnothing\)

Then \(R\) is independent, there are no \(R\)--\(W\) edges, and
\[
|R|\ge3\delta-n-2s,\qquad
|W|\le2n-4\delta+2s.                                          \tag{17}
\]
If \(\delta=n/2-o(n)\) and \(s=3\), this gives a half-sized independent
set \(R\), while every \(r\in R\) has all but \(o(n)\) vertices of its
complement as neighbours.  The hypotheses of the audited R004
near-complete-split theorem hold.  It produces
\[
n^2/8-o(n^2)
\]
pairwise \(C_7\)-compatible edges.

### Branch II: \(R=\varnothing\)

Here
\[
|P|,|Q|\ge\delta-s=n/2-o(n),\qquad
|Z|\le n-2\delta+2s=o(n),                                     \tag{18}
\]
and there are no \(P\)--\(Q\) edges.  For \(p\in P\),
\[
d_{G[P]}(p)\ge\delta-|Z|=|P|-o(n),                             \tag{19}
\]
and the same holds for \(Q\).

We use the following elementary dense-cycle fact.

**Lemma 3.1.**  If \(J_m\) is an \(m\)-vertex graph with
\(\delta(J_m)=m-o(m)\), then every two distinct edges of \(J_m\) are
\(C_7\)-compatible for sufficiently large \(m\).

For disjoint edges \(ab,cd\), choose successively
\[
r\in N(b)\cap N(c),\quad s\in N(d),\quad
t\in N(s)\cap N(a),
\]
avoiding previously used vertices.  All candidate pools have
\(m-o(m)\) elements.  Then
\[
a,b,r,c,d,s,t,a
\]
is the required cycle.

For adjacent edges \(ab,ac\), choose distinct
\[
r\in N(c),\quad s\in N(r),\quad w\in N(b),
\quad t\in N(s)\cap N(w),
\]
again avoiding the bounded used set.  Then
\[
b,a,c,r,s,t,w,b
\]
is the required cycle.

By (18)--(19), Lemma 3.1 applies to \(G[P]\), and
\[
e(G[P])\ge\frac{|P|(\delta-|Z|)}2=n^2/8-o(n^2).                \tag{20}
\]
Thus Branch II also supplies the required compatible family.  This is the
new closure of the near-two-clique branch left open after R004.

## 4. Completion when \(L_4(2)\) holds

If every colour class has size at most two, then the number of colours is
at least
\[
e(G)/2>n^2/8-O(1).
\]

Otherwise a class has at least three edges.  Lemmas 2.1--2.3 give a
no-three-step certificate with \(s=3\).  Branch I is closed by the R004
split theorem and Branch II by (20).  Therefore Theorem A holds whenever
\(L_4(2)\) holds.

## 5. What if \(L_4(2)\) fails?

There are \(T\), \(|T|\le2\), and \(u,v\in V(G-T)\) for which \(G-T\)
has no simple exact-four-edge \(u\)-to-\(v\) path.  Put \(H=G-T\).
Then
\[
|V(H)|=n-O(1),\qquad
\delta(H)\ge |V(H)|/2-o(n).
\]

Apply the independently proved
`FOUR_PATH_OBSTRUCTION_STABILITY.md`.  Adding back \(T\) changes only
\(O(n)\) potential adjacencies.  Hence \(G\) is \(o(n^2)\)-close to one
of:

1. the union of two balanced cliques;
2. a balanced complete bipartite graph.

### 5.1 Near two cliques

Let the two parts be \(U,W\).  The total number of missing clique edges is
\(o(n^2)\).  Delete from \(U\) vertices missing more than \(\rho n\)
internal neighbours, where \(\rho\to0\) sufficiently slowly.  The
remaining \(U'\) has
\[
|U'|=n/2-o(n),\qquad
\delta(G[U'])=|U'|-o(n).
\]
Lemma 3.1 makes every two edges of \(G[U']\) compatible, while
\[
e(G[U'])=n^2/8-o(n^2).
\]

### 5.2 Near complete bipartite

This is exactly Theorem 2 in `MAXCUT_CORE_HUB_THEOREM.md`.  Maximum-cut
normalisation supplies a balanced, almost complete crossing graph and a
linear crossing anchor at every vertex.  The core/hub family has
\[
n^2/8-o(n^2)
\]
pairwise compatible edges.

Thus Theorem A also holds when \(L_4(2)\) fails.  The proof is complete.

## 6. Relation to Erdős #809 and BCM26

Bucić--Chen--Ma prove, for \(k\ge4\),
\[
f(n,e,C_{2k+1})
=\frac e2+\frac n2\sqrt{e-\frac{n^2}{4}}+o(n^2)
\]
through strong induction over the full range \(e>n^2/4\).  They state that
their \(k=3\) Case 2 can be handled by a more involved stability argument,
while Case 1 remains the main bottleneck.

Theorem A supplies a self-contained stability theorem for the
near-minimum-degree regime and strictly extends the prior local
near-complete-split lemma.  It does **not** close their Case 1.  In that
case the induction only forces approximately
\[
\delta(G)\ge
\frac n2-\sqrt{e(G)-n^2/4}+o(n),
\]
and the square-root term can be a positive linear fraction of \(n\).
Theorem A requires that deficit to be \(o(n)\).

Therefore:

- `near-Dirac theorem proved`: yes;
- `BCM-style Case-2 induction step closed`: yes, after choosing its density
  cutoff through the uniform modulus; see `BCM_CASE2_INTERFACE.md`;
- `general BCM Case 1 closed`: no;
- `Erdős #809 closed`: no.
