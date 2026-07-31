# Maximum-cut core/hub theorem for the near-bipartite branch

## 1. The theorem

Two edges are called \(C_7\)-compatible if a copy of \(C_7\) contains
both of them.

**Theorem 2 (near-bipartite branch).**  Let \(G_n\) be an \(n\)-vertex
graph sequence satisfying
\[
e(G_n)>\lfloor n^2/4\rfloor,\qquad
\delta(G_n)\ge n/2-o(n).
\]
Suppose that \(G_n\) has edit distance \(o(n^2)\) from a complete
bipartite graph with two balanced parts.  Then \(G_n\) contains
\[
n^2/8-o(n^2)
\]
pairwise \(C_7\)-compatible edges.

Consequently every edge-colouring in which every \(C_7\) is rainbow uses
at least \(n^2/8-o(n^2)\) colours.

This strengthens the R004 core/hub theorem at one precise point: neither
side of the starting partition is required to be independent.

## 2. Maximum-cut normalisation

Choose a maximum cut \(V=A\sqcup B\), and write \(a=|A|,b=|B|\).
The assumed near-bipartite partition already has
\(n^2/4-o(n^2)\) crossing edges.  Hence the maximum cut does too.  Since
\[
e(A,B)\le ab\le n^2/4,
\]
we have
\[
a,b=n/2+o(n),\qquad ab-e(A,B)=o(n^2).                          \tag{11}
\]

Local optimality of a maximum cut gives, for every vertex \(v\),
\[
d_{\rm cross}(v)\ge d_{\rm internal}(v).                       \tag{12}
\]
Indeed, otherwise moving \(v\) to the other part would increase the cut.
Thus
\[
d_{\rm cross}(v)\ge d(v)/2\ge n/4-o(n).                        \tag{13}
\]

Because \(e(G)>\lfloor n^2/4\rfloor\ge ab\), the graph has an internal
edge in this maximum-cut partition.  Interchanging \(A,B\) if necessary,
fix
\[
pq\in E(A).
\]

## 3. Three-scale cleaning

Let \(\epsilon=\epsilon_n=o(1)\) dominate

- \((ab-e(A,B))/n^2\);
- \(|a-b|/n\);
- \((n/2-\delta(G))_+/n\);
- \(1/n\).

Put
\[
\rho=\epsilon^{1/2},\qquad \tau=\epsilon^{1/4}.
\]
Call a vertex cross-good if it misses at most \(\rho n\) vertices in the
opposite part.  Equation (11) shows that only \(O(\rho n)=o(n)\) vertices
are cross-bad.

Write
\[
h_p=d_A(p),\qquad h_q=d_A(q),\qquad
I=N_B(p)\cap N_B(q).
\]
By (13), each of \(p,q\) has a cross-good neighbour in \(B\); fix anchors
\[
s_p\in N_B(p),\qquad s_q\in N_B(q).
\]

Let
\[
P_0=(N_A(p)\setminus\{q\})\cap A_{\rm good}\cap N_A(s_p),
\]
\[
Q_0=(N_A(q)\setminus\{p\})\cap A_{\rm good}\cap N_A(s_q).
\]
If \(|P_0|<\tau n\), put \(P=\varnothing\); otherwise put \(P=P_0\).
Define \(Q\) similarly.  Also set
\[
I_0=I\cap B_{\rm good},
\]
and discard \(I_0\) if \(|I_0|<\tau n\).

Since the bad sets and the anchor-column defects have size \(o(n)\),
\[
|P\cup Q|\ge\max(h_p,h_q)-o(n),                               \tag{14}
\]
where a discarded subthreshold hub contributes only \(o(n)\) to the
right-hand error.  Further,
\[
\begin{split}
|I_0|
&\ge d_B(p)+d_B(q)-b-o(n)\\
&\ge2\delta(G)-b-h_p-h_q-o(n)\\
&\ge\max\{0,b-h_p-h_q\}-o(n).                                 \tag{15}
\end{split}
\]

## 4. The compatible family

Put \(U=P\cup Q\).  The hub rectangle is
\[
\mathcal H=E(U,B_{\rm good})
\setminus\{xs_p:x\in P\}
\setminus\{xs_q:x\in Q\}.
\]
The core rectangle is
\[
\mathcal K=
E\bigl(A_{\rm good}\setminus(U\cup\{p,q\}),I_0\bigr).
\]
Let
\[
\mathcal F=\mathcal H\cup\mathcal K.
\]

All auxiliary choices below are possible: a retained pool has size at
least \(\tau n\), while each good row or column excludes at most
\(\rho n=o(\tau n)\) candidates.  A bounded number of already used
vertices is also avoided.

The following table gives a simple seven-cycle for every type of pair.
Symbols are interpreted in the row in which they occur: a hub row lies in
\(A\), a core/hub column lies in \(B\), and \(c\) is always an auxiliary
\(A\)-vertex.

| specified pair | subcase | seven-cycle |
|---|---|---|
| core \(a_1z_1,a_2z_2\) | different rows/columns | \(p,q,z_1,a_1,x,a_2,z_2,p\) |
| core/core | same row \(a\) | \(p,q,z_1,a,z_2,c,x,p\) |
| core/core | same column \(z\) | \(p,q,x,a_1,z,a_2,y,p\) |
| same \(p\)-hub \(x_1y_1,x_2y_2\) | different rows/columns | \(p,x_1,y_1,c,y_2,x_2,s_p,p\) |
| same \(p\)-hub | same row \(x\) | \(p,x',y_1,x,y_2,c,s_p,p\) |
| same \(p\)-hub | same column \(y\) | \(p,x_1,y,x_2,z,c,s_p,p\) |
| \(p\)-hub \(xy\), \(q\)-hub \(tz\) | \(y\ne z\) | \(p,x,y,c,z,t,q,p\) |
| two hubs | \(y=z\) | \(q,t,y,x,r,c,s_q,q\) |
| core \(az\), \(p\)-hub \(xy\) | \(z\ne y\) | \(p,x,y,c,t,a,z,p\) |
| core/hub | \(z=y\) | \(p,x,z,a,t,c,s,p\) |

Here the selectors have the following meanings.

- In the first row, \(x\) is a common good column of \(a_1,a_2\).
- In the same-core-row case, \(x\in I_0\) is spare and \(c\) sees the
  two required good columns.
- In the same-core-column case, distinct \(x,y\in I_0\) see the
  corresponding good rows.
- In the same-hub-row case, \(x'\) is a spare retained hub row; this is
  exactly why subthreshold hubs were discarded.
- Every \(c\) is chosen as a common neighbour of two good columns.
- In the last row, \(s\in I_0\) and \(t\) is a spare neighbour of the
  core row.

The \(q\)-hub cases are symmetric.  If a row belongs to both \(P,Q\), pair
classification assigns both relevant edges to the same hub first.  The
ten rows exhaust equal-row, equal-column, and disjoint possibilities.
Thus all edges of \(\mathcal F\) receive different colours in a
rainbow-\(C_7\) colouring.

## 5. Count

Set
\[
u=|U|,\qquad k=|I_0|.
\]
Goodness and the anchor deletions give
\[
|\mathcal F|\ge ub+(a-u)k-o(n^2).                              \tag{16}
\]
Let
\[
x=\max(h_p,h_q),\qquad y=\min(h_p,h_q).
\]
Equations (14)--(15), together with \(a=b+o(n)\), reduce the worst case
of (16) to
\[
xb+(b-x)\max(0,b-x-y).
\]

If \(x+y\ge b\), then \(x\ge b/2\), so the first term is at least
\(b^2/2\).  If \(x+y\le b\), then \(y\le x\), and for \(x\le b/2\),
\[
\begin{split}
xb+(b-x)(b-x-y)
&\ge xb+(b-x)(b-2x)\\
&=b^2/2+2(x-b/2)^2\\
&\ge b^2/2.
\end{split}
\]
For \(x\ge b/2\), the hub term again suffices.  Hence
\[
|\mathcal F|\ge b^2/2-o(n^2)=n^2/8-o(n^2),
\]
proving Theorem 2.

## 6. Why maximum cut is essential

Without (12), a vertex could replace almost all of its crossing edges by
an internal fan.  Such a graph need not have an anchor for the displayed
hub templates in the original partition.  Maximum-cut normalisation gives
every vertex linear crossing degree and makes the three-scale cleaning
uniform.  This is the precise repair of the one-defective-row obstruction
found in R002.
