# Erdős #809 — second directed attack on the two Case-1 obstructions

Date: 2026-07-30

Status:
`EXACT_23_LINKAGE_REDUCTION_AND_FIXED_S_BOTTLENECK__ORIGINAL_OPEN`

## 1. Outcome

This attack does **not** prove Erdős #809 and does not prove the fixed-\(s\)
colour bound
\[
\left(\frac18+\frac{s}{2}+\frac{s^2}{2}-o(1)\right)n^2.
\]

It does produce a sharper endpoint for the next attack:

1. the distance-two and distance-three profiles are exactly the two sides
   of one vertex-disjoint \((2,3)\)-path-linkage obstruction;
2. the required colour theorem is reduced to an exact **total linkage
   defect** estimate, strictly weaker than proving that every pair of good
   edges is compatible;
3. the fixed-\(s\) errors in the inherited two-block and split lemmas are
   quantified, and the natural “use only the two dense interiors” route is
   proved incapable of reaching the BCM target beyond
   \[
   s_*=\frac{1-\sqrt{4/5}}2
      =0.052786404500042\ldots;
   \]
4. a finite guard independently verifies the new linkage equivalence and
   both obstruction implications.

The main remaining task is no longer “find another \(C_7\) template” in
the abstract.  It is to show that a Case-1 colouring cannot support
\(\Theta(n^2)\) repeated good edges whose endpoint pairs all fail the
\((2,3)\)-linkage.

## 2. Frozen Case-1 contract

Write
\[
e(G)=\left(\frac14+s^2+o(1)\right)n^2,\qquad 0<s\le\frac12,
\]
and retain the BCM Case-1 consequences
\[
\delta(G)\ge(1/2-s-o(1))n,
\]
the robust exact-four-path property \(L_4(2)\), and a set
\[
A\subseteq V(G),\qquad |A|\ge(1/2+s-o(1))n,
\]
whose vertices have pairwise graph distance at most three.  An edge is
good if it has an endpoint in \(A\).

The number of good edges is at least
\[
\begin{split}
|E_{\rm good}|
&\ge e(G)-\binom{n-|A|}{2}\\
&\ge
\left(\frac18+\frac{s}{2}+\frac{s^2}{2}-o(1)\right)n^2.
\end{split}                                                   \tag{1}
\]

The original BCM proof for \(k\ge4\) proves that all good edges have
different colours.  For \(C_7\), the only failure occurs when the selected
endpoints of two good edges are at distance two or three.

## 3. Exact \((2,3)\)-linkage characterization

Let \(xy\) and \(zw\) be two disjoint edges, and assume that there is no
edge between \(\{x,y\}\) and \(\{z,w\}\).  This is precisely the situation
for two same-colour edges after applying \(L_4(2)\).

### Lemma 1 (exact endpoint linkage)

The edges \(xy,zw\) lie on a common \(C_7\) if and only if one of the two
endpoint pairings
\[
\{(x,z),(y,w)\},\qquad \{(x,w),(y,z)\}
\]
admits two vertex-disjoint paths whose lengths are two and three, in
either order.

### Proof

If a \(C_7\) contains the two specified edges, delete those edges from the
cycle.  What remains is a pair of vertex-disjoint paths joining one of the
two displayed endpoint pairings.  Their lengths sum to five.  The
no-cross-edge hypothesis makes both lengths at least two, so they are two
and three.

Conversely, the union of such two paths and the specified edges is a
simple seven-cycle.  All seven vertices are distinct because the two
paths are vertex-disjoint.  This proves the lemma.

This elementary equivalence is the correct common language for both
inherited obstructions.

## 4. The two profiles are the two linkage defects

Let same-colour good edges be oriented as \(xy,zw\), with \(x,z\in A\),
and choose their closest endpoints.  The \(L_4(2)\) argument makes the two
edges an induced matching, while the diameter-three property of \(A\)
makes the closest-endpoint distance two or three.

### 4.1 Inner distance two

Let
\[
x-a-z
\]
be a shortest inner path.  By Lemma 1, incompatibility implies that
\(G-\{x,a,z\}\) has no simple three-edge \(y\)-to-\(w\) path.

Equivalently, form the shored graph whose possible edges are
\[
pq,\qquad
p\in N(y),\quad q\in N(w),\quad p\ne q.
\]
Every such edge is the middle edge of a three-edge \(y\)-to-\(w\) path.
The set \(\{x,a,z\}\) is a vertex cover of this shored path graph.  Thus
the first obstruction is exactly
\[
\tau_3(y,w)\le3,                                               \tag{2}
\]
where \(\tau_3\) is the minimum number of internal vertices hitting every
simple length-three path between the two endpoints.

After deleting the cover, the inherited \(P,Q,R,W,Z\) dichotomy follows:

- if \(R=(N(y)\setminus S)\cap(N(w)\setminus S)=\varnothing\), then
  \(P=N(y)\setminus S\) and \(Q=N(w)\setminus S\) are anticomplete,
  \[
  |P|,|Q|\ge(1/2-s-o(1))n,\qquad |Z|\le(2s+o(1))n;
  \]
- if \(R\ne\varnothing\), then \(R\) is independent and anticomplete to
  \(W\), with
  \[
  |R|\ge(1/2-3s-o(1))n,\qquad |W|\le(4s+o(1))n.
  \]

### 4.2 Inner distance three

Let
\[
x-a-b-z
\]
be a shortest inner path.  Because three is the minimum distance between
the two specified edges, the outer endpoints also have distance at least
three.  Consequently
\[
N(y)\cap N(w)=\varnothing.                                    \tag{3}
\]

This is the zero-codegree form of the same linkage failure: the inner
length-three path has no disjoint outer length-two partner.  Here
\[
P=N(y),\quad Q=N(w)
\]
are disjoint, each has size at least \((1/2-s-o(1))n\), and their
complement has size at most \((2s+o(1))n.  Unlike the distance-two
empty-intersection branch, (3) alone does **not** forbid \(P\)--\(Q\)
edges.

## 5. The minimal sufficient new lemma

For each colour \(\gamma\), let
\[
M_\gamma=E_{\rm good}\cap\{\text{edges of colour }\gamma\}.
\]
Since every \(C_7\) is rainbow, every \(M_\gamma\) is an induced matching
with no \((2,3)\)-linkage between any two of its edges.

The exact identity
\[
|E_{\rm good}|-
|\{\gamma:M_\gamma\ne\varnothing\}|
=\sum_\gamma (|M_\gamma|-1)_+                                \tag{4}
\]
shows that the following is sufficient.

### Linkage-defect lemma

Under the frozen Case-1 contract,
\[
\boxed{\quad
\sum_\gamma (|M_\gamma|-1)_+=o(n^2).
\quad}                                                        \tag{LD}
\]

Indeed, (1), (4), and (LD) give the desired BCM lower bound.

This is the minimum useful target in two senses.

1. It permits \(o(n^2)\) exceptional repeated good edges; proving pairwise
   compatibility of *all* good edges is unnecessarily strong.
2. Every summand on the left can be rooted at one edge of its colour.
   Each extra edge then supplies either a cover certificate (2) or a
   zero-codegree certificate (3).  Thus no third obstruction profile is
   missing.

A proof of (LD) may therefore be organized as a charging theorem:
charge every non-root edge of every repeated good colour to a low
length-three-path-cover pair or a zero-codegree pair, and prove that the
total charge is \(o(n^2)\).  What is still absent is the bounded-congestion
mechanism for that charge.

## 6. Why the inherited fixed-\(s\) estimates do not close (LD)

When \(s=o(1)\), all exceptional blocks above are \(o(n)\), which is why
the near-Dirac theorem closes.  For fixed \(s\), they have linear size:

- the empty-intersection branch may have a \(2sn\)-vertex separator;
- its two large interiors may each miss \(\Theta(sn)\) neighbours per
  vertex;
- the split branch may have a \(4sn\)-vertex bad block and each independent
  column may miss \(\Theta(sn)\) crossing edges;
- the zero-codegree branch permits a \(2sn\)-vertex complement and places
  no direct restriction on \(E(P,Q)\).

These are not lower-order errors and cannot be hidden in \(o(n^2)\).

There is also a precise numerical barrier.  In the empty-intersection
branch, even make the optimistic extra assumption that every edge of
\(G[P]\cup G[Q]\) receives a globally distinct colour.  From
\[
|P|+|Q|\ge(1-2s-o(1))n,\qquad
\delta(G[P]),\delta(G[Q])\ge(1/2-3s-o(1))n
\]
one obtains only
\[
L(s)n^2,\qquad
L(s)=\frac{(1-2s)(1/2-3s)}2.                                 \tag{5}
\]
The target is
\[
T(s)=\frac18+\frac{s}{2}+\frac{s^2}{2}.
\]
Their difference is
\[
L(s)-T(s)=\frac18-\frac52s+\frac52s^2.
\]
It becomes negative at
\[
s_*=\frac{1-\sqrt{4/5}}2=0.052786404500042\ldots.             \tag{6}
\]

Thus any full fixed-\(s\) argument must convert edges incident with the
linear separator/bad block into colours; the two interiors alone cannot
work beyond (6), even under an unrealistically favourable no-colour-reuse
assumption.

For \(0<s<s_*\), (5) identifies a possible restricted milestone, but two
nontrivial facts are still missing: global colour separation between the
two interiors, and compatibility templates robust to the separator.  No
claim for this interval is made.

## 7. Attempted countermodel search

The finite guard samples arbitrary labelled graphs on seven through nine
vertices and compares:

- brute-force membership of two induced edges in a common \(C_7\);
- existence of the vertex-disjoint \((2,3)\)-linkage in Lemma 1.

It also checks every sampled non-linked distance-two orientation against
the three-vertex-cover certificate and every sampled distance-three
orientation against zero outer codegree.

The run

```text
python3 verify_809_case1_second.py
```

returned:

```text
random graphs:                         240
induced edge pairs:                    684
linked / C7-compatible pairs:          361
unlinked pairs:                        323
distance-two certificates checked:    530
distance-three certificates checked:   84
normalized crossover: 0.05278640450004207
all guards: PASS
```

No finite result is extrapolated.  The search found many graphs realizing
each local obstruction, so neither (2) nor (3) is contradictory by itself.
It did not find or claim an asymptotic counterexample satisfying the full
Case-1 density, minimum-degree, diameter, and colouring contract.

## 8. Recommended next attack

The highest-value next step is a **bounded-congestion defect charging
lemma** for (LD), retaining the BCM set \(A\) rather than discarding it
after producing one certificate.

The proposed order is:

1. orient each repeated good edge towards an endpoint in \(A\), root each
   non-singleton colour, and record its outer pair;
2. split charges into \(\tau_3\le3\) and codegree-zero types;
3. in the \(\tau_3\le3\) type, use the complete coverage constraint
   \[
   (A\cap P)\times(A\cap Q)
   \subseteq
   \{\text{\(P\)-to-\(Q\) paths of length two or three
   containing a vertex of \(Z\)}\}
   \]
   forced by the diameter-three property of \(A\).  The possible part
   patterns are \(PZQ,PPZQ,PZZQ,PZQQ\);
4. in the codegree-zero type, charge to disjoint-neighbourhood pairs and
   exploit \(d(y)+d(w)\le n\);
5. prove that no vertex, missing adjacency, or separator incidence can
   absorb more than \(O_s(1)\) or \(o(n)\) non-root edges after the colour
   classes' induced-matching constraint is imposed.

Step 5 is the exact current bottleneck.  Without bounded congestion, the
linear \(2sn\) and \(4sn\) blocks can absorb \(\Theta(n^2)\) candidate
charges, and all existing estimates stop at that scale.

## 9. Claim boundary

- Exact \(C_7\) / \((2,3)\)-linkage equivalence: **proved**.
- Distance-two and distance-three unification: **proved**.
- Fixed-\(s\) internal-block barrier (6): **proved**.
- Linkage-defect lemma (LD): **open**.
- Fixed-\(s\) BCM Case 1: **open**.
- Erdős #809: **open**.

Primary comparison:
Matija Bucić, Kaizhe Chen and Jie Ma,
*On a maximal anti-Ramsey conjecture of Burr, Erdős, Graham, and Sós*,
arXiv:2603.18952v1.  Their theorem covers \(k\ge4\); the present note does
not alter that published boundary.
