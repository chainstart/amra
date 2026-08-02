# Erdős #809 — exact three-budget conservation for an opposite star

Date: 2026-08-02

Status: PROVED__INDEPENDENTLY_CROSS_AUDITED

## 1. Setup

Retain an opposite-type active zero-star with centre \(b\in B\),
leaf set \(L\subset B\), \(|L|=\ell\), and union host

\[
 U=\bigcup_{c\in L}N(c).
\]

Put

\[
 S=L\cap U,\qquad T=L\setminus U,\qquad
 s=|S|,\qquad t=|T|=\ell-s,
\tag{1}
\]

and let

\[
 A_L=\sum_{c\in L}|U\setminus N(c)|.
\tag{2}
\]

Inside the union host, separate

\[
 Y=A\cap U,\qquad Z_B=(U\cap B)\setminus L
\tag{3}
\]

and define the two external incidence deficits

\[
\begin{aligned}
 E_A&=\sum_{c\in L}|Y\setminus N(c)|,\\
 E_B&=\sum_{c\in L}|Z_B\setminus N(c)|.
\end{aligned}
\tag{4}
\]

Finally, write

\[
 \mu=M(G[L])=\binom\ell2-e(G[L]).
\tag{5}
\]

## 2. Exact conservation identity

### Theorem 2.1

\[
 \boxed{
 A_L+\ell(t-1)=2\mu+E_A+E_B.
 }
\tag{6}
\]

#### Proof

The leaf vertices in \(U\) are exactly \(S\), while
\(U\setminus L=Y\mathbin{\dot\cup}Z_B\).  Therefore the exact
leaf-deficit identity is

\[
 A_L=\ell s-2e(G[L])+E_A+E_B.
\]

Substitute \(s=\ell-t\) and
\(2e(G[L])=\ell(\ell-1)-2\mu\).  The result simplifies to (6).
\(\square\)

Identity (6) is a literal conservation law: total synchronization
defect is distributed among missing leaf pairs, missing external
\(B\)-incidences, and missing \(A\)-incidences, with the isolated-leaf
correction \(\ell(t-1)\).

## 3. The actual reserve pays the \(B\)-side terms

Every missing pair inside \(L\) belongs to the actual global reserve
\(\mathcal Q\).  The same is true for every missing pair counted by
\(E_B\), because it is a missing \(B\)-edge incident with an active
zero-shore leaf.  The two families are disjoint, so

\[
 \boxed{|\mathcal Q|\ge\mu+E_B.}
\tag{7}
\]

Combining (6)--(7) gives:

### Corollary 3.1 (reserve versus \(A\)-incidence deficit)

\[
\boxed{
 |\mathcal Q|
 +\min\left\{|\mathcal Q|,\binom\ell2\right\}
 +E_A
 \ge A_L+\ell(t-1).
 }
\tag{8}
\]

Equivalently, with

\[
 \eta=
 \max\left\{
 0,\,
 A_L+\ell(t-1)-|\mathcal Q|
 -\min\left\{|\mathcal Q|,\binom\ell2\right\}
 \right\},
\tag{9}
\]

one has

\[
 \boxed{E_A\ge\eta.}
\tag{10}
\]

Indeed, (7) gives \(\mu+E_B\le|\mathcal Q|\), while
\(\mu\le\binom\ell2\).  Therefore

\[
 2\mu+E_B=(\mu+E_B)+\mu
 \le
 |\mathcal Q|+
 \min\left\{|\mathcal Q|,\binom\ell2\right\}.
\]

Substitution in (6) proves (8).  This is sharper than the valid but
coarser bound with \(2|\mathcal Q|\), and is the optimal elimination
using only (6)--(7) and \(0\le\mu\le\binom\ell2\).

Thus synchronization defect not paid by the true \(B\)-reserve must
reappear as a literal missing-incidence deficit on the \(A\)-part of
the union host.

## 4. Unpaid defect enlarges the union rectangle

Since \(N_A(c)\subseteq Y\) for every leaf,

\[
 E_A
 =\sum_{c\in L}\bigl(|Y|-d_A(c)\bigr)
 =\ell|Y|-\sum_{c\in L}d_A(c).
\tag{11}
\]

Every active colour at \(c\) uses a distinct \(A\)-edge, so
\(\sum_c d_A(c)\ge H:=\sum_c h_c\).  Hence

\[
 \boxed{
 |Y|\ge
 \left\lceil\frac{H+\eta}{\ell}\right\rceil.
 }
\tag{12}
\]

Let \(\alpha=\alpha(G[L])\).  The independent colour-support theorem
gives

\[
 d_A(b)\ge\left\lceil\frac H\alpha\right\rceil.
\tag{13}
\]

The sets \(N_A(b)\) and \(Y\) form the union-host anticomplete
rectangle, proving:

### Theorem 4.1 (three-budget energy inequality)

\[
 \boxed{
 M_A\ge
 \left\lceil\frac H\alpha\right\rceil
 \left\lceil\frac{H+\eta}{\ell}\right\rceil.
 }
\tag{14}
\]

This strengthens the synchronization-free union bound.  If defect is
not paid by \(\mathcal Q\), it increases the second side of the
missing-\(A\) rectangle rather than causing a coordinate loss.

## 5. Closed reserve-branch form

Under global reserve failure,

\[
 |\mathcal Q|\le D_B-1,
\tag{15}
\]

define

\[
\begin{aligned}
 a_B&=
 \left\lfloor
 \frac{1+\sqrt{1+8(D_B-1)}}2
 \right\rfloor,\\
 a_*&=\min\{\ell,a_B\},\\
 \eta_B&=
 \max\left\{
 0,\,
 A_L+\ell(t-1)-(D_B-1)
 -\min\left\{D_B-1,\binom\ell2\right\}
 \right\}.
\end{aligned}
\tag{16}
\]

Then \(\alpha\le a_*\), \(\eta\ge\eta_B\), and

\[
 \boxed{
 M_A\ge
 \left\lceil\frac H{a_*}\right\rceil
 \left\lceil\frac{H+\eta_B}{\ell}\right\rceil.
 }
\tag{17}
\]

In particular,

\[
 H(H+\eta_B)\le a_*\ell M_A,
\]

so

\[
 \boxed{
 H\le
 \left\lfloor
 \frac{\sqrt{\eta_B^2+4a_*\ell M_A}-\eta_B}{2}
 \right\rfloor.
 }
\tag{18}
\]

For a star selected from a maximal repeated-zero matching of size
\(f\), the inherited inequality \(E_0/(4f)\le H-\ell\) gives

\[
 \boxed{
 E_0\le4f\left(
 \left\lfloor
 \frac{\sqrt{\eta_B^2+4a_*\ell M_A}-\eta_B}{2}
 \right\rfloor-\ell
 \right).
 }
\tag{19}
\]

The rectangle-to-budget theorem also strengthens to

\[
\boxed{
 M_B\ge
 x_0(y_0-g)_+ +y_0(x_0-g)_+-M_A+L_m,
}
\tag{20}
\]

where

\[
 x_0=\left\lceil\frac H{a_*}\right\rceil,\qquad
 y_0=\left\lceil\frac{H+\eta_B}{\ell}\right\rceil.
\tag{21}
\]

## 6. Boundary and scope

- For the one-leaf three-clique-chain equality model,
  \(t=1\), \(A_L=\eta_B=0\), and (17) reduces to the sharp
  \(M_A=h_1^2\) rectangle.
- At the rigid clique endpoint, \(t=0\), \(A_L=\ell\), and the
  correction \(A_L+\ell(t-1)\) vanishes exactly.
- When the reserve already pays all of (8), \(\eta_B=0\) and (17)
  reduces to the independently audited union-host theorem.

The conservation law strengthens every opposite-star parameter
regime, but it does not prove that the resulting scalar system is
empty.  Same-star obstructions, the canonical outer-low residue, and
other BCM witness branches remain.  Maximum-degree Case 1 and
Erdős #809 are open.
