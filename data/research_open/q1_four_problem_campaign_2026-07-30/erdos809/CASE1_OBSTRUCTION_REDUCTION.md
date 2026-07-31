# Exact reduction of the remaining BCM \(C_7\) Case 1

## 1. Setup

Let \(G\) be an \(n\)-vertex graph in which every \(C_7\) is rainbow.
Assume:

1. \(G\) has \(L_4(2)\): after deleting any two vertices, every remaining
   pair is joined by a simple path of exactly four edges;
2. \(A\subseteq V(G)\) has pairwise graph distance at most three.

Call an edge **good** if at least one endpoint lies in \(A\).

These are exactly the two structural outputs available at the point where
the BCM26 Case-1 construction fails for \(k=3\).

## 2. Reduction theorem

**Proposition 3.**  At least one of the following conclusions holds.

1. Every good edge has a different colour.
2. There are same-colour good edges \(xy,zw\), a shortest endpoint path
   \(x-a-z\), and outer endpoints \(y,w\), such that
   \(G-\{x,a,z\}\) has no three-edge \(y\)-to-\(w\) path.
3. There are same-colour good edges \(xy,zw\), a shortest endpoint path
   \(x-a-b-z\), and outer endpoints \(y,w\), such that
   \[
   N(y)\cap N(w)=\varnothing.                                  \tag{28}
   \]

In alternatives 2 and 3 all displayed vertices are distinct.

## 3. Proof

If conclusion 1 fails, take same-colour good edges \(xy,zw\).  By the
exact-four-path argument in Lemma 2.1 of `NEAR_DIRAC_C7_THEOREM.md`, their
edge distance is at least two.

Each good edge has an endpoint in \(A\).  Since any two vertices of \(A\)
are at distance at most three,
\[
d_E(xy,zw)\le3.
\]
Thus the edge distance is exactly two or three.

If it is two, choose a shortest endpoint path \(x-a-z\).  A three-edge
path from \(y\) to \(w\) avoiding \(x,a,z\) would splice with
\[
y-x-a-z-w
\]
to form a seven-cycle containing both same-colour edges.  This is
alternative 2.

If the edge distance is three, choose a shortest path \(x-a-b-z\).
The outer endpoints \(y,w\) also have distance at least three; otherwise
the edge distance of the specified edges would be at most two.  Hence
they have no common neighbour, proving (28) and alternative 3.

This proves the proposition.

## 4. Exact colour count in the non-obstruction branch

BCM Lemma 3.1 supplies
\[
|A|\ge
\frac n2+\sqrt{e-\frac{n^2}{4}+\frac n2}
>
\frac n2+\sqrt{e-\frac{n^2}{4}}.
\]
Consequently the number of good edges is more than
\[
\begin{split}
e-\frac12\left(\frac n2-\sqrt{e-\frac{n^2}{4}}\right)^2
&=
\frac e2+\frac n2\sqrt{e-\frac{n^2}{4}}.                       \tag{29}
\end{split}
\]
Therefore conclusion 1 gives the entire BCM target before its
\(o(n^2)\) allowance.

The remaining Case 1 is now reduced to alternatives 2 and 3 only.

## 5. Parameterized shape of the two obstructions

Write
\[
s=\sqrt{\frac e{n^2}-\frac14},\qquad
\delta(G)\ge(1/2-s-o(1))n.
\]

### Alternative 2

The R003 no-three-step lemma gives:

- an empty-intersection branch with disjoint sets
  \(P,Q\), no \(P\)--\(Q\) edges,
  \[
  |P|,|Q|\ge(1/2-s-o(1))n,
  \]
  and at most \((2s+o(1))n\) leftover vertices;
- or a nonempty-intersection branch with an independent set
  \[
  |R|\ge(1/2-3s-o(1))n
  \]
  anticomplete to all but at most \((4s+o(1))n\) vertices of
  \(P\cup Q\).

### Alternative 3

The disjoint neighbourhoods
\[
P=N(y),\qquad Q=N(w)
\]
both have size at least \((1/2-s-o(1))n\), and their complement has at
most \((2s+o(1))n\) vertices.

These descriptions are exact reductions, not colour lower bounds.  When
\(s=o(1)\), the near-Dirac theorem closes them.  For fixed \(s>0\), the
leftover block is linear and is precisely the unresolved Case-1 mass.

## 6. Unique next lemma

A complete solution through this route would follow from the following
parameterized statement:

> Under either obstruction profile above, a rainbow-\(C_7\) colouring
> uses at least
> \[
> \left(\frac18+\frac s2+\frac{s^2}{2}-o(1)\right)n^2
> \]
> colours.

The target equals the number of edges in the larger clique of the
unbalanced two-clique extremizer.  No such parameterized lemma is claimed
in this campaign.
