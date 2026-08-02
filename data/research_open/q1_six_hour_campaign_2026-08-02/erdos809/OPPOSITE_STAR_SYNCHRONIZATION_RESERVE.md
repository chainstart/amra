# Erdős #809 — synchronization forces actual reserve

Date: 2026-08-02

Status: `PROVED__PENDING_INDEPENDENT_CROSS_AUDIT`

## 1. Setup

Retain the opposite-star setup and notation of
`OPPOSITE_STAR_COMMON_HOST_DICHOTOMY.md`.  Thus

\[
 P=N(b),\quad C=V(G)\setminus P,\quad
 Q_c=N(c),\quad U=\bigcup_{c\in L}Q_c,\quad R=C\setminus U,
\]

where `L` is a set of `ell` opposite-type active zero-shore leaves in
the maximum-degree set `B`.  Put

\[
 r=|R|,\qquad
 A_L=\sum_{c\in L}|U\setminus Q_c|
     =\sum_{c\in L}(\rho_c-r)=R_L-\ell r.
\tag{1}
\]

Let `mathcal Q` be the inherited global reserve union.  Its defining
property needed below is that every missing `B`-edge incident with an
active zero-shore endpoint belongs to `mathcal Q`.

## 2. Exact bridge

### Theorem 2.1 (synchronization--reserve bridge)

Let

\[
 T=L\cap R,\qquad t=|T|.
\tag{2}
\]

Then `T` is exactly the set of isolated vertices of `G[L]`, and

\[
 \boxed{\ell-t\le A_L.}
\tag{3}
\]

Moreover,

\[
 \boxed{
 |\mathcal Q|
 \ge \binom\ell2-\binom{\ell-t}{2}
 \ge \binom\ell2-\binom{\min\{\ell,A_L\}}2.
 }
\tag{4}
\]

Consequently, under the inherited global reserve obstruction
`|mathcal Q| <= D_B-1`,

\[
 \boxed{
 \binom\ell2-
 \binom{\min\{\ell,R_L-\ell r\}}2
 \le D_B-1.
 }
\tag{5}
\]

Thus a large opposite star cannot have both synchronized leaf
neighbourhoods (`A_L` small) and a small actual reserve.  In the perfect
synchronization endpoint `A_L=0`, all leaves are mutually nonadjacent and

\[
 |\mathcal Q|\ge\binom\ell2.
\tag{6}
\]

#### Proof

By definition, a leaf `c` lies in `R=C\setminus U` precisely when it is
not adjacent to any member of `L`.  Hence `T` is the isolated-vertex set
of `G[L]`.

Every nonisolated leaf `c` belongs to `U`; simplicity gives
`c notin Q_c=N(c)`, so this vertex contributes one distinct incidence to
`U\setminus Q_c`.  Summing these incidences over the `ell-t`
nonisolated leaves proves (3).

Every pair in `binom(L,2)` with at least one endpoint in `T` is missing.
There are exactly

\[
 \binom\ell2-\binom{\ell-t}{2}
\]

such pairs.  They are missing `B`-edges incident with active zero-shore
endpoints and therefore belong to `mathcal Q`.  This proves the first
inequality in (4).  Equation (3) gives
`ell-t <= min{ell,A_L}`; monotonicity of `binom(x,2)` for nonnegative
integers proves the second.  Substitution of (1) and the reserve
obstruction gives (5).  Equation (6) is the case `A_L=0`.  QED.

## 3. What this repairs

The common-host theorem alone left its synchronized endpoint detached
from the actual reserve budget.  Theorem 2.1 supplies that missing exact
interface: synchronization forces isolated active leaves, and isolated
active leaves spend genuine reserve pairs quadratically.

It does not yet show that `ell` is large enough relative to `D_B`, nor
does it control the intermediate common-residual regime or the separate
outer-`A` residual.  Erdős #809 and maximum-degree Case 1 remain open.
