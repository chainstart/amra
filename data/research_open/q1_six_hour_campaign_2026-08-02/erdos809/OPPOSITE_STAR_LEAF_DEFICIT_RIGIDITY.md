# Erdős #809 — exact leaf-deficit rigidity in an opposite star

Date: 2026-08-02

Status: `PROVED__PENDING_INDEPENDENT_CROSS_AUDIT`

## 1. Setup

Retain

\[
 U=\bigcup_{c\in L}N(c),\qquad
 R=(V(G)\setminus N(b))\setminus U,
\]

for an opposite active zero-star with `|L|=ell`.  Put

\[
 S=L\cap U,\quad T=L\cap R,
 \quad s=|S|,\quad t=|T|=\ell-s,
\]

and

\[
 A_L=\sum_{c\in L}|U\setminus N(c)|.
\tag{1}
\]

The set `T` is the isolated-vertex set of `G[L]`; `S` is precisely its
nonisolated-vertex set.

## 2. Exact decomposition

### Theorem 2.1 (leaf-deficit identity)

Let `Z=U\setminus L` and define the external synchronization defect

\[
 E_Z=\sum_{c\in L}|Z\setminus N(c)|.
\tag{2}
\]

Then

\[
 \boxed{
 A_L=\ell s-2e(G[L])+E_Z.
 }
\tag{3}
\]

Consequently,

\[
 \boxed{A_L\ge s(\ell-s+1)=s(t+1).}
\tag{4}
\]

#### Proof

The leaf vertices lying in `U` are exactly `S`.  For every `c in L`,
the two disjoint parts of its deficit are therefore

\[
 |U\setminus N(c)|
 =|S\setminus N_L(c)|+|Z\setminus N(c)|.
\]

Summing the first term over all leaves gives

\[
 \sum_{c\in L}(s-d_L(c))=\ell s-2e(G[L]),
\]

which proves (3).  All edges of `G[L]` lie inside `S`, so
`e(G[L])<=binom(s,2)`; discard `E_Z>=0` in (3) to obtain (4).  QED.

## 3. The sharp integer phase transition

If `s>0`, then

\[
 s(\ell-s+1)-\ell=(s-1)(\ell-s)\ge0.
\]

(The formal case `s=1` cannot actually occur, because a nonisolated
induced subgraph has at least two vertices.)  Hence:

### Corollary 3.1 (subcritical defects force an independent star)

\[
 \boxed{
 A_L<\ell\quad\Longrightarrow\quad E(G[L])=\varnothing.
 }
\tag{5}
\]

Every one of the `binom(ell,2)` leaf pairs is then a missing `B`-edge
incident with an active zero-shore endpoint, so

\[
 \boxed{|\mathcal Q|\ge\binom\ell2.}
\tag{6}
\]

### Corollary 3.2 (critical nonempty endpoint is rigid)

If `A_L=ell` and `G[L]` contains an edge, then equality must hold at
every step of (4).  Thus

\[
 \boxed{
 S=L,\qquad G[L]=K_\ell,\qquad E_Z=0,
 }
\tag{7}
\]

and, for every leaf,

\[
 \boxed{N(c)=U\setminus\{c\}.}
\tag{8}
\]

Indeed, equality in `(s-1)(ell-s)>=0`, together with `s>=2`, forces
`s=ell`; equality in (3)--(4) forces all `binom(ell,2)` leaf edges and
zero external defect.  Simplicity then gives (8).

Thus `A_L=ell` has only two qualitative possibilities: the leaf graph
is empty, or the nonempty endpoint is the completely rigid clique
system (7)--(8).  Intermediate leaf supports require `A_L>ell`.

### Corollary 3.3 (square-root reserve/dense-leaf dichotomy)

Put

\[
 a=A_L,\qquad q_a=\lfloor\sqrt a\rfloor.
\]

At least one of the following holds:

1. `s<=q_a`, and the actual global reserve satisfies
   \[
   \boxed{
   |\mathcal Q|\ge
   \binom\ell2-\binom{q_a}2;
   }
   \tag{9}
   \]
2. `t<=q_a-1`, so `s>=ell-q_a+1`, and the leaf graph satisfies
   \[
   \boxed{
   2e(G[L])\ge
   \ell(\ell-q_a+1)-a.
   }
   \tag{10}
   \]

Indeed, if both `s>=q_a+1` and `t+1>=q_a+1`, then (4) gives
`a>q_a^2`, a contradiction.  In the first outcome, all leaf edges lie
inside `S`, so at most `binom(q_a,2)` leaf pairs are present and all
the others belong to the actual reserve.  In the second, (3) gives

\[
 2e(G[L])=\ell s+E_Z-a\ge\ell s-a,
\]

and the displayed lower bound follows.  Thus every intermediate
opposite star must choose between a nearly complete reserve on its
leaves and a quantitatively dense leaf core.

## 4. Scope firewall

The clique endpoint may still occur in an abstract/full-contract hard
configuration; this note does not yet turn it into a compatible-edge
family or a contradiction.  For `A_L>ell`, many support sizes remain.
The theorem sharpens the first synchronization-defect gate but does not
solve maximum-degree Case 1 or Erdős #809.
