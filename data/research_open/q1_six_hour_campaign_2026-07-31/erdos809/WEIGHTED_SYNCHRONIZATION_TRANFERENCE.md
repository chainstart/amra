# Erdős #809 — weighted two-energy synchronization

Date: 2026-08-01

Status: PROVED__WEIGHTED_MATCHING_MASS_FORCES_GLOBAL_RESERVE_ENERGY

## 1. Outcome

The unweighted synchronization theorem controls the number of
vertex-disjoint active zero-shore pairs.  The colour-rectangle theorem
controls their multiplicities through missing edges in \(A\).  These
two mechanisms can be composed without losing a power.

Retain the maximum-degree witness
\[
 A=N[v],\qquad B=V(G)\setminus A,\qquad m=|A|,
\]
and let
\[
 F=\{e_i=\{b_i,c_i\}:1\le i\le f\}
\tag{1}
\]
be a nonempty matching of active zero-shore pairs in \(B\).  Let \(h_i\)
be the number of colours using \(e_i\), and put
\[
 H_F=\sum_{i=1}^f h_i.
\tag{2}
\]
Write
\[
 d_0=\binom{\delta(G)}2,\qquad
 \overline M=\binom n2-e(G),
\tag{3}
\]
let \(M_A\) be the number of missing edges in \(G[A]\), and let
\(\mathcal Q\) be the global reserve union in \(B\).

### Theorem 1.1 (weighted synchronization transference)

If \(\delta(G)\ge2\), then
\[
 \boxed{
 d_0^2 H_F^2
 \le
 \overline M^{\,2} M_A|\mathcal Q|.
 }
\tag{4}
\]
Equivalently, with \(\alpha=d_0/\overline M\),
\[
 \boxed{
 |\mathcal Q|
 \ge
 \frac{\alpha^2H_F^2}{M_A}.
 }
\tag{5}
\]
Here \(M_A>0\) automatically because a nonempty active zero-shore pair
has at least one colour and its two \(A\)-coordinates form a missing
edge.

Together with the earlier one-coordinate and unweighted bounds, every
such matching satisfies the exact three-energy inequality
\[
 \boxed{
 |\mathcal Q|
 \ge
 \max\left\{
 \frac{4H_F^2}{m^2},\
 \frac{d_0^2H_F^2}{\overline M^{\,2}M_A},\
 \frac{d_0f^2}{2\overline M-d_0}
 \right\}.
 }
\tag{6}
\]

The new middle term is useful precisely when the matching carries
large colour mass but the missing-\(A\) budget is not large enough to
hide that mass through overlapping colour rectangles.

## 2. Proof

For every \(i\), set
\[
 P_i=N(b_i),\qquad Q_i=N(c_i),
\]
and let \(\mathcal C_i\) be the set of distinct unordered pairs with one
endpoint in \(P_i\) and one in \(Q_i\).  The zero-shore condition and
the overlapping-neighbourhood count give
\[
 \mathcal C_i\subseteq\overline E(G),
 \qquad
 |\mathcal C_i|\ge d_0.
\tag{7}
\]

For a missing edge \(z\in\overline E(G)\), define its weighted support
\[
 \mu_h(z)=\sum_{i:z\in\mathcal C_i}h_i.
\tag{8}
\]
Double counting yields
\[
 \sum_{z\in\overline E(G)}\mu_h(z)
 =\sum_i h_i|\mathcal C_i|
 \ge d_0H_F.
\tag{9}
\]
Hence some missing anchor \(z=xy\) has
\[
 \mu_h(xy)\ge\frac{d_0H_F}{\overline M}
 =\alpha H_F.
\tag{10}
\]

Let \(I=\{i:xy\in\mathcal C_i\}\) and \(k=|I|\).  Orient every supported
base pair so that
\[
 x\in N(b_i),\qquad y\in N(c_i).
\]
As in the unweighted synchronization theorem, the matching endpoints
then span a \(k\)-by-\(k\) missing rectangle in \(B\), contained in
\(\mathcal Q\).  Therefore
\[
 k\le\sqrt{|\mathcal Q|}.
\tag{11}
\]

The colour rectangle attached to \(e_i\) has side length \(h_i\).
The two-anchor transference theorem gives
\[
 \sum_{i=1}^fh_i^2
 \le M_A\sqrt{|\mathcal Q|}.
\tag{12}
\]
Apply Cauchy--Schwarz only on the anchor support \(I\):
\[
 \begin{aligned}
 \alpha^2H_F^2
 &\le \mu_h(xy)^2\\
 &=\left(\sum_{i\in I}h_i\right)^2\\
 &\le k\sum_{i\in I}h_i^2\\
 &\le \sqrt{|\mathcal Q|}
       M_A\sqrt{|\mathcal Q|}\\
 &=M_A|\mathcal Q|.
 \end{aligned}
\tag{13}
\]
This is (4)--(5).

The first term in (6) is the one-coordinate inequality
\(2H_F\le m\sqrt{|\mathcal Q|}\).  The third is the exact iterated
unweighted synchronization bound.  Taking their maximum proves (6).
\(\square\)

## 3. Exact obstruction consequences

If the global reserve test fails, then
\[
 |\mathcal Q|\le D_B-1.
\tag{14}
\]
Every weighted active zero-shore matching therefore obeys
\[
 \boxed{
 H_F
 \le
 \min\left\{
 \frac m2\sqrt{D_B-1},\
 \frac{\overline M}{d_0}
 \sqrt{M_A(D_B-1)}
 \right\},
 }
\tag{15}
\]
as well as
\[
 f\le
 \sqrt{\frac{(D_B-1)(2\overline M-d_0)}{d_0}}.
\tag{16}
\]

Thus any matching whose captured colour mass violates either term in
(15) closes the entire \(B\)-reserve defect budget.  This is a
quantifier-safe sufficient exit: it applies to one explicitly produced
matching and does not assume that total repeated-zero mass is evenly
distributed.

At the fixed-\(s\) scale
\[
 e(G)=\left(\frac14+s^2+o(1)\right)n^2,\qquad
 \delta(G)\ge\left(\frac12-s-o(1)\right)n,
\]
one has
\[
 \alpha=\frac{1-2s}{2(1+2s)}+o(1).
\tag{17}
\]
If
\[
 H_F=(\eta+o(1))n^2,\quad
 M_A=(a+o(1))n^2,\quad
 |\mathcal Q|=(q+o(1))n^2,
\]
then (5) becomes
\[
 \boxed{
 q\ge
 \frac{(1-2s)^2}{4(1+2s)^2}\,
 \frac{\eta^2}{a}.
 }
\tag{18}
\]
This gives an explicit macroscopic reserve cost for any matching that
captures quadratic zero-pair multiplicity.

## 4. Scope firewall

The theorem is an exact all-parameter composition of two proved
mechanisms.  It does not assert that the repeated-zero graph always has
a matching with \(H_F=\Omega(n^2)\).  A weighted star can carry
quadratic total multiplicity while every matching captures only one
star edge.  Such concentration is the remaining alignment branch, not
a counterexample to (4).

Consequently, (4) closes the heavy-matching alternative but does not
by itself control the concentrated-star alternative, the outer-\(A\)
residue \(R_A\), the maximum-degree branch, or Erdős #809.
