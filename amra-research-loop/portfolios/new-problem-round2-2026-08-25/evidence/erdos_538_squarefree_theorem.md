# Erdős #538: an exact rank-two theorem on squarefree support

## Scope

Fix a finite set of primes \(P\), put \(w_p=1/p\), and restrict \(A\) to
squarefree integers whose prime factors lie in \(P\).  We impose the \(r=2\)
condition from problem #538: every integer \(m\) has at most two ordered
representations \(m=pa\), where \(p\) is prime and \(a\in A\).

This note solves only the optimisation of the rank-two part

\[
 A_2=\{pq\in A:p,q\in P,\ p\ne q\}.
\]

It does not solve the unrestricted problem, in which prime powers and all
ranks may occur.

## Theorem

Among all admissible choices of \(A_2\),

\[
 \max \sum_{pq\in A_2}\frac1{pq}
 =\max_{X\subseteq P}
 \left(\sum_{p\in X}\frac1p\right)
 \left(\sum_{q\in P\setminus X}\frac1q\right).
\]

In particular, an optimum is obtained by taking exactly the products \(pq\)
that cross one bipartition \(X\sqcup(P\setminus X)\).

## Proof

Associate to \(A_2\) the graph \(G\) on vertex set \(P\), with edge \(pq\)
exactly when \(pq\in A_2\).  If \(p,q,r\) span a triangle, then
\(m=pqr\) has the three representations

\[
 p(qr)=q(pr)=r(pq),
\]

contrary to the representation bound.  Conversely, if \(G\) is
triangle-free, every squarefree \(m\) supported on \(P\) has at most two such
representations: a representation from \(A_2\) is possible only when \(m\)
has exactly three prime factors, and the representations are precisely the
edges induced by those three vertices.  If \(m\) contains a repeated prime,
then deleting one prime factor can produce a squarefree rank-two integer in at
most one way.  Primes outside \(P\) likewise contribute at most one possible
deletion.  Hence admissibility of \(A_2\) is exactly triangle-freeness of
\(G\).

The objective is the product-weighted edge sum

\[
 W(G)=\sum_{pq\in E(G)}w_pw_q.
\]

It remains to show that some complete bipartite graph has weight at least
\(W(G)\).  We give the weighted Zykov symmetrisation argument.  Two
nonadjacent vertices are twins when they have the same open neighbourhood.
Work with the current twin classes.  If distinct nonadjacent classes \(C,D\)
have neighbourhood-weight sums

\[
 d(C)=\sum_{x\in N(C)}w_x,\qquad
 d(D)=\sum_{x\in N(D)}w_x,
\]

replace every vertex in \(C\) by a twin of \(D\) when \(d(D)\ge d(C)\);
otherwise replace \(D\) by twins of \(C\).  In the first case the change in
edge weight is

\[
 \left(\sum_{x\in C}w_x\right)(d(D)-d(C))\ge0,
\]

and the other case is symmetric.  The operation preserves
triangle-freeness because the neighbourhood of every vertex in a
triangle-free graph is independent.  It merges two twin classes and does not
split any other twin class, so the process terminates.

At termination every pair of distinct twin classes is adjacent; the graph is
complete multipartite.  Triangle-freeness permits at most two nonempty
parts.  Thus the final graph is complete bipartite and has not decreased
\(W\).  For sides \(X\) and \(P\setminus X\), its weight is exactly the
product in the displayed formula.  Taking the best \(X\) proves the theorem.

## Replay and adversarial checks

`work/verify_538_squarefree.py` exhausts every graph through six prime
vertices, checks triangle-freeness, compares the exact rational optimum with
every bipartition, and replays exponent vectors in \(\{0,1,2\}\) with an
extra outside prime.  The replay is supporting evidence; the proof above is
the universal justification.

The key scope boundary is that ranks are independent only inside the stated
squarefree restriction.  This note makes no local inequality for arbitrary
prime powers, which was the unsupported step in the previous candidate
route.
