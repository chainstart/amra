# Erdős #809: corrected \(A\)-oriented obstruction taxonomy

Date: 2026-07-31

## 1. Audit verdict

The sentence in the previous `CASE1_SECOND_ATTACK.md` that simultaneously
orients two good edges \(xy,zw\) with \(x,z\in A\) and chooses \(x,z\) as
their closest endpoints is not justified. The endpoint pair of minimum
distance need not be the pair lying in \(A\).

The linkage-defect identity itself is unaffected, but the proposed charging
taxonomy must be corrected before it can be used in a proof. A first attempted
repair—take an arbitrary shortest path between the \(A\)-endpoints—also has
a gap: a length-three \(A\)-geodesic may run through one of the two outer
edge endpoints. The final correction below records this as a third, small
transversal profile.

## 2. Frozen hypotheses

Assume:

1. \(G\) has \(L_4(2)\): after deleting any set of at most two vertices,
   every two remaining vertices have a simple exact four-edge path;
2. \(\delta(G)\ge3\);
3. \(A\subseteq V(G)\) has pairwise graph distance at most three;
4. every \(C_7\) is rainbow.

Let \(xy\) and \(zw\) be distinct same-colour good edges. Choose the
orientation so that
\[
x,z\in A.
\]

The standard exact-four-path lemma implies that distinct same-colour edges
have edge distance at least two. In particular they are disjoint, no endpoint
of one is adjacent to an endpoint of the other, and \(x\ne z\).

## 3. Corrected trichotomy

### Proposition

At least one of the following three certificates applies.

1. There is a shortest path \(x-a-z\), and the three-vertex set
   \(\{x,a,z\}\) meets every simple three-edge path from \(y\) to \(w\).
2. There is a shortest path \(x-a-b-z\) whose internal vertices avoid
   \(\{y,w\}\), and
   \[
   N(y)\cap N(w)\subseteq\{a,b\}.
   \]
   In particular,
   \[
   |N(y)\cap N(w)|\le2.
   \]
3. The pair \(\{y,w\}\) meets every simple three-edge path from \(x\) to
   \(z\). In particular the \(A\)-endpoint pair has a length-three-path
   transversal of size two.

### Proof

Because \(x,z\in A\), their distance is at most three. It cannot be zero.
It also cannot be one, since then the two specified edges would have edge
distance at most one and the exact-four-path lemma would put them on a common
\(C_7\). Hence \(d(x,z)\in\{2,3\}\).

If \(d(x,z)=2\), fix a shortest path \(x-a-z\). A simple three-edge
\(y\)-to-\(w\) path avoiding \(\{x,a,z\}\), together with
\[
y-x-a-z-w,
\]
would be a simple seven-cycle containing both same-colour edges. Such a path
cannot exist, proving the first alternative.

Now suppose \(d(x,z)=3\). If every length-three \(x\)-to-\(z\) path
meets \(\{y,w\}\), the third certificate holds. Otherwise choose one such
path \(x-a-b-z\) with \(\{a,b\}\cap\{y,w\}=\varnothing\). Suppose
\[
c\in N(y)\cap N(w)\setminus\{a,b\}.
\]
The same-colour edge-distance lemma excludes \(c=x\) and \(c=z\): either
choice would be a cross edge between the two specified edges. Thus
\(y-c-w\) and \(x-a-b-z\) are vertex-disjoint paths of lengths two and
three. Their union with \(xy\) and \(zw\) is a \(C_7\), a contradiction.
Therefore every common neighbour of \(y,w\) lies in \(\{a,b\}\). This proves
the second certificate. \(\square\)

## 4. Why the old simultaneous orientation is genuinely unsafe

At the purely local level, take vertices
\[
\{x,y,z,w,a,b\}
\]
and edges
\[
xy,\ zw,\ xa,\ ab,\ bz,\ ya,\ yb,\ aw,\ bw.
\]
For \(A=\{x,z\}\), the \(A\)-endpoints have distance three along the clean
path \(x-a-b-z\), while the non-\(A\) endpoints have distance two along
\(y-a-w\), and their common neighbourhood is exactly \(\{a,b\}\).
The specified edges form an induced pair and there is no seven-cycle
because the graph has only six vertices.

This example is not an asymptotic counterexample and does not satisfy the
full dense \(L_4(2)\) contract. Its purpose is narrower: goodness plus
diameter three alone does not permit the closest endpoints to be chosen in
\(A\). Any global proof using that simultaneous choice needs an additional
argument.

## 5. Consequence for the linkage-defect programme

For every non-root edge of a repeated good colour, orient both it and its
root towards \(A\). It now supplies one of three valid certificates:

1. an outer endpoint pair whose length-three paths have a transversal of
   size three; or
2. an outer endpoint pair of codegree at most two; or
3. an \(A\)-endpoint pair whose length-three paths have a transversal of
   size two.

Thus no proliferation into four endpoint-orientation cases is necessary,
but the earlier two-profile charging plan was incomplete. In the clean
distance-three profile, codegree \(O(1)\) replaces codegree zero. Its
asymptotic neighbourhood geometry is unchanged:
\[
|N(y)\cup N(w)|
\ge 2\delta(G)-2,
\]
so under \(\delta(G)\ge(1/2-s-o(1))n\), all but at most
\((2s+o(1))n\) vertices still lie in the two nearly disjoint
neighbourhoods.

The remaining publication-level step is a bounded-congestion theorem for
the three corrected certificate classes. No such total bound is claimed
here.

## 6. Claim boundary

- Simultaneous “closest and in \(A\)” orientation: **not justified**.
- Unqualified two-profile \(A\)-oriented repair: **false as stated**, because
  an \(A\)-geodesic may use \(y\) or \(w\) internally.
- Corrected \(A\)-oriented three-certificate proposition: **proved**.
- Replacement of zero codegree by codegree at most two: **proved and sharp
  in the clean-geodesic profile**.
- Total linkage-defect estimate: **open**.
- Erdős #809: **open**.
