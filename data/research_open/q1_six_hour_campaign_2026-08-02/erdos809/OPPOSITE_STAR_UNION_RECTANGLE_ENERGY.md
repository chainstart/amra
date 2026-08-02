# Erdős #809 — union-host rectangle removes synchronization loss

Date: 2026-08-02

Status: PROVED__INDEPENDENTLY_CROSS_AUDITED

## 1. Setup

Use the maximum-degree partition

\[
 A=N[v],\qquad B=V(G)\setminus A,
\]

and let \(b\in B\) be the centre of an opposite-type active zero-star
with leaf set \(L\subset B\), \(|L|=\ell\).  Put

\[
 P=N(b),\qquad U=\bigcup_{c\in L}N(c),
\]

and write

\[
 X=A\cap P=N_A(b),\qquad Y=A\cap U.
\tag{1}
\]

For each leaf, let \(\Gamma_c\) be the set of active colours shared at
the outer endpoints \(b,c\), set

\[
 h_c=|\Gamma_c|,\qquad H=\sum_{c\in L}h_c,\qquad
 h_{\max}=\max_{c\in L}h_c,
\tag{2}
\]

and let \(\alpha=\alpha(G[L])\).

## 2. The union-host rectangle

### Theorem 2.1

The sets \(X,Y\) are disjoint and anticomplete.  Moreover,

\[
 |Y|\ge\max_{c\in L}d_A(c)\ge h_{\max}.
\tag{3}
\]

Consequently,

\[
 \boxed{M_A\ge d_A(b)\max_{c\in L}d_A(c).}
\tag{4}
\]

#### Proof

For every opposite zero-shore pair \(bc\), its neighbourhoods
\(P=N(b)\) and \(N(c)\) are disjoint and anticomplete.  Taking the union
over all leaves gives

\[
 P\cap U=\varnothing,\qquad E(P,U)=\varnothing.
\tag{5}
\]

Intersecting with \(A\) proves that \(X,Y\) are disjoint and
anticomplete, so all \(|X||Y|\) pairs between them are missing edges
inside \(A\).  Also \(N_A(c)\subseteq Y\) for every leaf.  This proves
(3)--(4).  Finally, every colour in \(\Gamma_c\) uses a distinct edge
from \(c\) to an inner endpoint in \(A\), hence \(d_A(c)\ge h_c\).
\(\square\)

The point is that \(Y\) is the whole union coordinate, not the common
intersection of the leaf neighbourhoods.  Therefore (4) loses nothing
when the synchronization defect is large.

## 3. Colour-support compression inside the rectangle

For a centre colour \(\gamma\), its leaf support

\[
 L_\gamma=\{c\in L:\gamma\in\Gamma_c\}
\]

is independent in \(G[L]\): same-colour edges form an induced
matching, so their outer endpoints are pairwise nonadjacent.  Hence
\(|L_\gamma|\le\alpha\).  Counting the \(H\) leaf--colour incidences
shows

\[
 \left|\bigcup_{c\in L}\Gamma_c\right|
 \ge\left\lceil\frac H\alpha\right\rceil.
\tag{6}
\]

Distinct colours at \(b\) use distinct incident \(A\)-edges, and thus

\[
 d_A(b)\ge\left\lceil\frac H\alpha\right\rceil.
\tag{7}
\]

Together with Theorem 2.1 and
\(h_{\max}\ge\lceil H/\ell\rceil\), this proves:

### Corollary 3.1 (defect-free union energy)

\[
 \boxed{
 M_A\ge
 \left\lceil\frac H\alpha\right\rceil h_{\max}
 \ge
 \left\lceil\frac H\alpha\right\rceil
 \left\lceil\frac H\ell\right\rceil.
 }
\tag{8}
\]

This holds for every synchronization defect \(A_L\).  It strictly
strengthens the earlier common-intersection estimate whenever that
estimate loses coordinates through \(A_L\).

## 4. Eliminate \(\alpha\) under reserve failure

Every pair in an independent subset of \(L\) is a missing \(B\)-edge
incident with an active zero-shore leaf, hence belongs to the actual
global reserve \(\mathcal Q\).  In the hard reserve branch

\[
 |\mathcal Q|\le D_B-1
\tag{9}
\]

one necessarily has \(D_B\ge1\), and

\[
 a_B:=
 \left\lfloor
 \frac{1+\sqrt{1+8(D_B-1)}}2
 \right\rfloor,
 \qquad
 a_*:=\min\{\ell,a_B\}
\tag{10}
\]

satisfies \(\alpha\le a_*\).  Therefore:

### Corollary 4.1 (reserve-branch quadratic energy)

\[
 \boxed{
 M_A\ge
 \left\lceil\frac H{a_*}\right\rceil h_{\max}
 \ge
 \left\lceil\frac H{a_*}\right\rceil
 \left\lceil\frac H\ell\right\rceil.
 }
\tag{11}
\]

In particular,

\[
 \boxed{H\le\left\lfloor\sqrt{a_*\ell M_A}\right\rfloor.}
\tag{12}
\]

If this is the star selected from a maximal repeated-zero matching of
size \(f\), the inherited concentration inequality

\[
 \frac{E_0}{4f}\le H-\ell
\]

gives the closed cap

\[
 \boxed{
 E_0\le
 4f\left(
 \left\lfloor\sqrt{a_*\ell M_A}\right\rfloor-\ell
 \right).
 }
\tag{13}
\]

A negative right-hand side means that this selected opposite-star
branch is impossible.

## 5. Stronger transfer to the \(B\)-budget

Put

\[
 x_0=\left\lceil\frac H{a_*}\right\rceil,\qquad
 y_0=\left\lceil\frac H\ell\right\rceil,\qquad
 g=|A|-\delta(G)-1.
\tag{14}
\]

Applying the rectangle-to-budget theorem directly to the union
rectangle \(X\times Y\) yields

\[
 \boxed{
 M_B\ge
 x_0(y_0-g)_+ +y_0(x_0-g)_+-M_A+L_m.
 }
\tag{15}
\]

Unlike the earlier common-intersection transfer, neither (11) nor
(15) degenerates when \(A_L\) is large.

## 6. Sharpness and scope firewall

For the inherited balanced three-clique-chain construction and a
one-leaf opposite star, \(|X|=|Y|=h_1=k\) and \(M_A=k^2\).
Thus (4) and (8) are exact even under the full BCM and rainbow-\(C_7\)
contract.

The theorem closes a synchronization-loss defect in the opposite-star
energy ledger.  It does not by itself prove that (13) contradicts all
global parameter choices, control the canonical low-degree outer
residue, remove the same-star alternative, or treat the other BCM
witness branches.  Maximum-degree Case 1 and Erdős #809 remain open.
