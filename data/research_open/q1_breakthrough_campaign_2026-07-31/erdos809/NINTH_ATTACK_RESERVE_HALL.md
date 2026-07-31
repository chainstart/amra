# Erdős #809 — ninth attack: reserve-Hall charging

Date: 2026-07-31

Status: `EXACT_RESERVE_HALL_DICHOTOMY_PROVED__UNIVERSAL_EXPANSION_OPEN`

## 1. Why this is a different attack

The previous zero-shore estimates tried to show that the raw local
congestion is small.  That target is false: the three-clique-chain
family has quadratic congestion although its exact colour defect is
fully paid by the missing edges of the outside block.

This note does not try to make congestion small.  It lets a congested
zero-shore pair spend *other* missing edges forced by its two outside
neighbourhoods.  The resulting question is an exact system-of-distinct-
representatives problem.  It absorbs the known full-contract
counterfamilies and gives a sharp certificate for any genuinely hard
sequence.

## 2. Frozen centered setup

Retain the maximum-degree branch of the preceding attacks.  Thus

\[
A=N[v],\qquad B=V(G)\setminus A,
\]

every copy of \(C_7\) is rainbow, and \(G\) has the robust exact-four-
path property \(L_4(2)\).  Orient the relevant good edges from an inner
endpoint in \(A\) to an outer endpoint in \(B\).

For a colour \(\gamma\), let \(Y_\gamma\subseteq B\) be its set of
outer endpoints and put \(t_\gamma=|Y_\gamma|\).  Same-colour edges form
an induced matching, so \(Y_\gamma\) is an independent set in \(G[B]\).
For every colour with \(t_\gamma\ge1\), choose one root
\(r_\gamma\in Y_\gamma\).  Colours with \(t_\gamma=0\) contribute no
token.  The \(t_\gamma-1\) objects

\[
(\gamma,b),\qquad b\in Y_\gamma\setminus\{r_\gamma\},       \tag{1}
\]

are called the **defect tokens** of \(\gamma\).  Their number is exactly

\[
D_B=\sum_\gamma(t_\gamma-1)_+.                              \tag{2}
\]

The base pair of the token is the missing edge
\(e(\gamma,b)=\{r_\gamma,b\}\) of \(G[B]\).

For a missing pair \(e=\{b,c\}\subseteq B\), its shore graph consists
of the middle edges of simple paths \(b-p-q-c\).  Call \(e\) a
zero-shore pair when that graph is empty.

## 3. The reserve forced by a zero shore

For a zero-shore pair \(e=\{b,c\}\), define

\[
\mathcal K(e)
=\bigl\{f\in\overline E(G[B]):f\cap\{b,c\}\ne\varnothing\bigr\}
\cup
\bigl\{\{p,q\}:p\in N_B(b),\ q\in N_B(c),\ p\ne q\bigr\}. \tag{3}
\]

### Lemma 3.1 (reserve validity)

Every member of \(\mathcal K(e)\) is a missing edge of \(G[B]\).

#### Proof

Every member of the first set in (3) is explicitly required to be
missing; in particular this set contains the base pair \(e\).  If distinct
\(p\in N_B(b)\) and \(q\in N_B(c)\) were adjacent, then

\[
b-p-q-c
\]

would be a simple three-edge shore path.  This contradicts the
zero-shore assumption.  \(\square\)

Thus a token based at a highly congested pair is not restricted to
charging that pair itself.  It may charge any still unused member of
the whole reserve (3).

### Lemma 3.2 (exact local reserve lower bound)

Write \(\overline d_B(b)=|B|-1-d_B(b)\).  Then every zero-shore pair
\(e=\{b,c\}\) satisfies

\[
\boxed{
|\mathcal K(e)|
\ge
\overline d_B(b)+\overline d_B(c)-1
+\binom{\min\{d_B(b),d_B(c)\}}2.}                          \tag{3a}
\]

#### Proof

The missing stars at \(b\) and \(c\) have respectively
\(\overline d_B(b)\) and \(\overline d_B(c)\) edges and intersect
exactly in \(bc\), giving the first three terms.  If the two
neighbourhood sizes are \(a\le b\) and their intersection has size
\(r\), the number of distinct unordered cross pairs is

\[
ab-r-\binom r2
=ab-\frac{r(r+1)}2
\ge\binom a2.
\]

This is minimized over all admissible \(a,b,r\) when the two sets
coincide at the smaller size.  None of these pairs touches \(b\) or
\(c\), because \(bc\) is missing, so this rectangle is disjoint from
the two stars.  Lemma 3.1 completes the proof. \(\square\)

## 4. Exact Hall dichotomy

Let \(\mathcal T_+\) be the tokens whose base pair has a nonempty shore,
and let \(\mathcal T_0\) be the zero-shore tokens.  The fixed-pair theorem
from `FOURTH_ATTACK.md` implies that the base pairs of tokens in
\(\mathcal T_+\) are all distinct.  Charge those tokens to their base
pairs and denote the resulting set of already used missing edges by
\(C_+\).

Build a bipartite graph \(\mathfrak H\) with left side \(\mathcal T_0\),
right side

\[
\overline E(G[B])\setminus C_+,
\]

and join a token \(\tau\) to all edges in

\[
\mathcal K(e(\tau))\setminus C_+.                           \tag{4}
\]

### Theorem 4.1 (reserve-Hall closure)

Exactly one of the following holds.

1. The graph \(\mathfrak H\) has a matching saturating
   \(\mathcal T_0\).  Then
   \[
   \boxed{D_B\le M_B}.                                      \tag{5}
   \]
2. There is a set \(\mathcal S\subseteq\mathcal T_0\) such that
   \[
   \boxed{
   \left|
   \bigcup_{\tau\in\mathcal S}
   \bigl(\mathcal K(e(\tau))\setminus C_+\bigr)
   \right|<|\mathcal S|.}                                  \tag{6}
   \]

#### Proof

This is Hall's theorem, followed by Lemma 3.1.  In the first case the
nonempty-shore tokens use the pairwise distinct edges in \(C_+\), and
the matching assigns pairwise distinct edges outside \(C_+\) to all
zero-shore tokens.  Hence all \(D_B\) tokens inject into the \(M_B\)
missing edges of \(G[B]\), proving (5).  If no saturating matching
exists, Hall's theorem gives precisely (6).  \(\square\)

Tokens with the same base pair have identical candidate sets.  Hence
(6) can equivalently be compressed to a family \(\mathcal F\) of
zero-shore pairs with token multiplicities \(a_e\):

\[
\sum_{e\in\mathcal F}a_e
>
\left|
\left(\bigcup_{e\in\mathcal F}\mathcal K(e)\right)
\setminus C_+
\right|.                                                    \tag{7}
\]

This is the first exact obstruction in the attack that is conditioned
on failure of the *true* missing-edge budget rather than failure of a
loose moment bound.

### Corollary 4.2 (maximum-witness closure interface)

If every repeated good colour is outer-\(B\) supported and the first
alternative of Theorem 4.1 holds, then \(R_A=0\), \(D_A=D_B\le M_B\),
and therefore

\[
D_A\le M_B+S_m.
\]

The maximum-degree BCM branch closes in this regime.

More generally, the same conclusion holds whenever

\[
R_A\le S_m
\]

and the reserve matching exists.

### Corollary 4.3 (one-shot high-reserve closure)

Let \(Z=|\mathcal T_0|\).  If every zero-shore base pair \(bc\) obeys

\[
\overline d_B(b)+\overline d_B(c)-1
+\binom{\min\{d_B(b),d_B(c)\}}2
\ge Z+|C_+|,                                                \tag{7a}
\]

then the reserve matching exists.

Indeed, after deleting \(C_+\), every nonempty candidate set still has
at least \(Z\) elements by Lemma 3.2.  The union of the candidate sets
of any \(z\le Z\) tokens consequently has size at least \(Z\ge z\),
so Hall's condition holds.

Unlike the earlier per-pair congestion cutoff, (7a) spends both
missing stars and the forced neighbourhood rectangle.  Its failure
forces every genuinely active obstruction into the simultaneous
low-reserve/concentrated-overlap regime targeted by (7).

### Corollary 4.4 (two simultaneous consequences of genuine hardness)

Suppose Hall fails and choose a deficient token set \(\mathcal S\) as
in (6).  Let \(W\subseteq B\) be the set of endpoints of its base pairs
and put \(T=|\mathcal S|\).  Then

\[
\left|
\{f\in\overline E(G[B]):f\cap W\ne\varnothing\}
\right|
<T+|C_+|,                                                   \tag{7b}
\]

and

\[
\left|
\bigcup_{bc\in e(\mathcal S)}
N_B(b)\widehat\times N_B(c)
\right|
<T+|C_+|.                                                   \tag{7c}
\]

Indeed, both sets on the left are contained in
\(\bigcup_{\tau\in\mathcal S}\mathcal K(e(\tau))\).  Restoring the
at most \(|C_+|\) already charged edges to (6) proves the two bounds.

Thus a counterexample to the exact charge cannot merely have large
zero-shore multiplicity.  The endpoint set of the deficient tokens must
simultaneously expose too few missing-star edges **and** make all forced
outside-neighbourhood rectangles overlap into a set smaller than the
token mass.  This is a concrete two-sided synchronization certificate,
not a heuristic moment condition.

## 5. Why the old counterfamily is now paid correctly

In the balanced three-clique-chain family of `EIGHTH_ATTACK.md`, write

\[
B=U\sqcup W,\qquad |U|=|W|=k.
\]

There are \(k\) repeated tokens on each matched zero pair
\(e_i=\{u_i,w_i\}\).  The old local charge tried to put all \(k\) tokens
on the single edge \(e_i\).  The new reserve is

\[
\mathcal K(e_i)
=U\times W.                                                 \tag{8}
\]

Indeed, its incident-edge part supplies row \(i\) and column \(i\),
while its neighbourhood rectangle supplies every entry outside that
row and column.  Thus every token sees the full \(k^2\)-edge missing
bipartite block \(U\times W\).  For every \(k\ge3\), the token--reserve
graph has a perfect matching of size \(k^2\).  Thus Theorem 4.1 gives

\[
D_B=k^2=M_B
\]

without asking the false condition \(E_0=o(n^2)\).  The verifier checks
this for \(3\le k\le30\).

The same mechanism pays the three-hub family of `SIXTH_ATTACK.md`.
There \(|U|=u\), \(|W|=w\le u\), every one of the \(w\) matched
zero pairs carries \(u+3\) tokens, and the two hubs outside \(A\) are
isolated in \(G[B]\).  All candidate sets contain the common
\(uw\)-edge block \(U\times W\); the candidate set of group \(i\) also
contains its four distinct missing hub incidences.  If a token set
meets \(g\le w\) groups, its candidate union has at least \(uw+4g\)
edges, whereas it has at most \((u+3)g\) tokens.  The difference is

\[
uw+4g-(u+3)g=u(w-g)+g\ge0.
\]

Hall's condition therefore holds for every parameter in that family.
Its large local rectangle overlap is irrelevant because the outside
missing block and the hub incidences supply a global system of distinct
representatives.  The verifier regression-tests 117 instances in
addition to this symbolic inequality.

## 6. The bold remaining theorem

The route now has one non-incremental target.

> **Reserve expansion conjecture.**  Under the full fixed-\(s\)
> maximum-degree Case-1 contract, one can choose the roots
> \(r_\gamma\) so that either the reserve-Hall matching exists, or the
> Hall-deficient family (7) forces an asymptotically complete
> \((1/2+s)n\)-vertex core.

Either outcome closes the maximum-degree branch: the first by
Corollary 4.2 and the second by the compatible-core theorem already
proved in `SECOND_ATTACK.md`.

The key point is that (7) is much stronger than quadratic raw
congestion.  Every pair in \(\mathcal F\) brings the whole missing
rectangle

\[
N_B(b)\ \widehat\times\ N_B(c)
\]

into the union on the right.  Hall failure therefore says that many
weighted zero pairs have not only large overlap in their \(A\)-side
colour rectangles, but also abnormally concentrated and overlapping
outside-neighbourhood rectangles.  That is the synchronization input
which the previous moment estimates lacked.

## 7. Computational falsification boundary

The accompanying verifier checks the exact Hall matching on the
balanced chain and the validity of every reserve edge.  A separate
finite falsifier examined:

- 1,000 random/block-structured full-contract centered graphs on
  9--12 vertices; and
- all 93 qualifying equal three-vertex blow-ups of four-vertex
  templates,

and found no instance in which the chromatic defect of the centered
\(A\)--\(B\) compatibility graph exceeded \(M_B\).

This is evidence for the reserve-expansion conjecture, not a proof.
The finite search is especially unable to certify the asymptotic
aligned-core alternative.

## 8. Claim boundary

- Reserve validity (Lemma 3.1): **PROVED**.
- Exact reserve-Hall dichotomy (Theorem 4.1): **PROVED**.
- Closure whenever the reserve matching exists and \(R_A\le S_m\):
  **PROVED**.
- Exact closure of the previous three-clique-chain obstruction by a
  reserve matching: **PROVED / FINITELY REGRESSION-TESTED**.
- Universal reserve expansion or aligned-core alternative: **OPEN**.
- Maximum-degree Case 1 and Erdős #809: **OPEN / NOT CLAIMED**.
