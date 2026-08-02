# Erdős #809 — dense leaf core gives a direct colour exit

Date: 2026-08-02

Status: `PROVED__PENDING_INDEPENDENT_CROSS_AUDIT`

## 1. The cleaning theorem

Let `L subset B` be the leaf set of an active zero-shore star, of
either neighbourhood type, and put `ell=|L|`.  Every missing edge of
`G[B]` incident with `L` belongs to the global reserve union
`mathcal Q`.  In particular,

\[
 M(G[L])\le|\mathcal Q|.
\tag{1}
\]

### Theorem 1.1 (exact dense-leaf cleaning)

Suppose `|mathcal Q|<=q`.  For every integer `d>=0`, `G[L]` has an
induced subgraph `H` with

\[
 \boxed{
 h:=|V(H)|\ge
 h_0:=\ell-\left\lfloor\frac{2q}{d+1}\right\rfloor,
 }
\tag{2}
\]

\[
 \boxed{\delta(H)\ge h-1-d,}
\tag{3}
\]

and

\[
 \boxed{e(H)\ge\binom h2-q\ge\binom{h_0}2-q.}
\tag{4}
\]

#### Proof

Delete every leaf whose missing degree inside `G[L]` exceeds `d`.
Each deleted vertex has missing degree at least `d+1`, while the sum of
all missing degrees is `2M(G[L])<=2q`.  This proves (2).  A retained
vertex has at most `d` nonneighbours in `L`, hence at most `d`
nonneighbours in the induced subgraph `H`, proving (3).  Finally
`M(H)<=M(G[L])<=q`, which gives (4).  QED.

## 2. Direct `C_7`-colour exit

The inherited dense-subgraph compatibility lemma states that every two
edges of a graph `J` lie on a common `C_7` whenever

\[
 2\delta(J)-|V(J)|\ge5.
\tag{5}
\]

By (2)--(3), condition

\[
 \boxed{h_0\ge2d+7}
\tag{6}
\]

implies (5) for `H`.  Every edge of `H` must then receive a distinct
colour in any rainbow-`C_7` colouring.  Therefore:

### Corollary 2.1 (finite colour closure)

If some integer `d>=0` satisfies

\[
 h_0=\ell-\left\lfloor\frac{2q}{d+1}\right\rfloor\ge2d+7
\tag{7}
\]

and

\[
 \boxed{\binom{h_0}2-q\ge\Phi(n,e),}
\tag{8}
\]

then the graph already uses at least `Phi(n,e)` colours.  The desired
maximum-witness colour bound closes directly, without charging `D_A`.

Under global reserve failure one may take `q=D_B-1`.  Consequently any
hard maximum-witness obstruction must violate (7)--(8) for every
integer `d>=0`.  This is an explicit optimized scalar restriction on
the number of leaves of every selected star.

## 3. Asymptotic reading

If `q=o(ell^2)`, choosing `d` on the order of `sqrt(q)` deletes only
`O(sqrt(q))` leaves and leaves missing degree `O(sqrt(q))`.  Thus a
linear leaf set becomes an almost-complete pairwise-`C_7`-compatible
edge core.  Whether its edge count reaches `Phi(n,e)` depends on the
actual leaf density; no universal closure is asserted.

## 4. Scope firewall

The theorem is strongest when `D_B` is small compared with `ell^2`.
The selected opposite star may have few leaves but high multiplicity,
or `D_B` may itself be quadratic, making (8) unavailable.  The theorem
does not control the outer-`A` residue in those cases.  Erdős #809
remains open.
