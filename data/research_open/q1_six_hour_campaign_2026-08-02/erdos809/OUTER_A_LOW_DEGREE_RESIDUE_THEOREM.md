# Erdős #809 — exact low-degree localization of the outer-`A` residue

Date: 2026-08-02

Status: `PROVED__PENDING_INDEPENDENT_CROSS_AUDIT`

## 1. Setup

Retain the maximum-degree partition `A=N[v]`, `B=V(G)\setminus A`.
For every colour `gamma`, let

\[
 t_\gamma=
 |\{\text{its good }A\text{--}B\text{ edges}\}|,
 \qquad
 a_\gamma=
 |\{\text{its edges internal to }A\}|.
\]

Then

\[
 D_A=\sum_\gamma(t_\gamma+a_\gamma-1)_+,
 \qquad
 D_B=\sum_\gamma(t_\gamma-1)_+,
 \qquad
 R_A=D_A-D_B.
\tag{1}
\]

Fix an integer `q>=2`.  Define

\[
 A_{<q}=\{a\in A:d_B(a)<q\},\qquad
 B_{<q}=\{b\in B:d_B(b)<q\}.
\tag{2}
\]

Let `N_{<q}` be the number of colours represented on good edges that
contain no good edge admitting an outer endpoint of `B`-degree at least
`q`.  Equivalently, these are the nonempty good colour classes wholly
contained in the low edge set defined below.

The inherited rich-outer compatibility theorem says that if

\[
 M_B<\binom{q-1}{2},
\tag{3}
\]

then all good edges admitting an orientation whose outer endpoint has
`B`-degree at least `q` are pairwise contained in a common `C_7`.

## 2. Exact residue theorem

### Theorem 2.1 (exact low-degree localization)

Under (3), every rainbow-`C_7` colouring satisfies

\[
 \boxed{
 D_A=e(G[A_{<q}])+e(A,B_{<q})-N_{<q}.
 }
\tag{4}
\]

Therefore

\[
 \boxed{
 R_A=e(G[A_{<q}])+e(A,B_{<q})-N_{<q}-D_B.
 }
\tag{5}
\]

Consequently,

\[
 \boxed{
 e(G[A_{<q}])+e(A,B_{<q})-N_{<q}\le D_B+S_m
 \quad\Longrightarrow\quad R_A\le S_m.
 }
\tag{6}
\]

If (6) and any certificate for `D_B<=M_B` hold simultaneously, then

\[
 D_A=R_A+D_B\le S_m+M_B,
\]

which closes the exact maximum-witness defect budget.

#### Proof

Call a good edge **high** if it admits the orientation in the inherited
rich-outer theorem, and **low** otherwise.  Under (3), every two high
edges lie on a common `C_7`; hence a rainbow-`C_7` colouring places at
most one high edge in each colour class.

For a colour containing `t_gamma+a_gamma` good edges, let `h_gamma` be
its number of high good edges.  We have `h_gamma in {0,1}`.  If
`h_gamma=1`, its contribution to `D_A` equals its number of low good
edges.  If `h_gamma=0`, that contribution is one less than its positive
number of low good edges.  Summing this exact colourwise identity gives

\[
 D_A=|E_{\rm low}|-N_{<q}.
\tag{7}
\]

An internal `A`-edge is low exactly when both endpoints lie in
`A_{<q}`.  An `A`--`B` edge has its forced outer endpoint in `B`, so it
is low exactly when that endpoint lies in `B_{<q}`.  Therefore

\[
 |E_{\rm low}|=e(G[A_{<q}])+e(A,B_{<q}),
\]

which proves (4).  Equations (5)--(6) and the final implication follow by
substitution.  QED.

### Corollary 2.2 (canonical unconditional threshold)

Set

\[
 q_*(M_B)=
 2+\left\lfloor\frac{1+\sqrt{1+8M_B}}2\right\rfloor.
\tag{8}
\]

Then `M_B<binom(q_*-1,2)` by the definition of the positive root, so
(4)--(5) hold for every maximum-degree instance at this canonical
threshold.  Thus the formerly separate residue has the unconditional
exact normal form

\[
 \boxed{
 R_A=
 e(G[A_{<q_*}])+e(A,B_{<q_*})-N_{<q_*}-D_B.
 }
\tag{9}
\]

This is a reduction, not a claim that the right side is at most `S_m`.

## 3. Relation to the earlier rich-edge count

The inherited direct closure condition counted high edges and required
at least `Phi(n,e)` of them.  Equations (4)--(5) are the exact
residue-level form of the same compatibility fact.  The colour credit
`N_{<q}` is essential: in the three-clique-chain stress model all good
edges are low for the natural threshold, but almost all irrelevant
edges have fresh colours and cancel through `N_{<q}`.  The identity can
be composed with any global reserve, matching, or opposite-star
certificate for `D_B`.

## 4. Scope firewall

The theorem localizes `R_A`; it does not prove (6) for every full BCM
instance.  In particular, the low-degree sets can be large when `M_B`
is quadratic.  Other witness branches are untouched.  Erdős #809
remains open.
