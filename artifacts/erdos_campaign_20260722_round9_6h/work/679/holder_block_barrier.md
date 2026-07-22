# #679: a strict Hölder barrier for blockwise first-overrun transfer

Date: 2026-07-22

This note tests a natural attempt to avoid the enormous joint CRT modulus:
split the selected primes into disjoint blocks, transfer each block separately,
and recombine the block weights by generalized Hölder.  The result below
shows that this architecture retains only an \(o(\log X)\) zero-mode exponent
in the round-8 large-band scale.  It is a method barrier, not a statement
about the original problem.

## Setup

Put

\[
 H=(L_1/L_2)^2\{1+o(1)\},\qquad
 a=1-t={C\over\sqrt H},qquad C>1.
\]

Partition primes above \(H\) into blocks \({\cal P}_b\), each having

\[
 \sum_{p\in{\cal P}_b}\log p\le A L_1                  \tag{1}
\]

for a fixed \(A\).  This includes first-overrun blocks whose individual CRT
moduli are \(X^{O(1)}\).  Let

\[
 W_b(n)=t^{T_b(n)},qquad
 \mu_b(q)=\prod_{p\in{\cal P}_b}
 \left(1-{H(1-t^q)\over p}\right).
\]

Assume, even optimistically, that every moment needed below transfers with
only \(X^{o(1)}\) loss.  Generalized Hölder with \(q_b\ge1\) and
\(\sum_bq_b^{-1}=1\) would give an effective zero-mode exponent

\[
 G_{\rm H}:=\sum_b{-\log\mu_b(q_b)\over q_b}.           \tag{2}
\]

## The cap imposed by Hölder

Write \(y_b=q_b^{-1}\).  For \(x=H/p\in(0,1)\), convexity in
\(u\in[0,1]\) gives

\[
 -\log(1-xu)\le u\{-\log(1-x)\}.
\]

Also \(1-t^{q_b}\le\min(q_ba,1)\).  Therefore

\[
 {1\over q_b}
 \left[-\log\left(1-{H(1-t^{q_b})\over p}\right)\right]
 \le \min(a,y_b)\left[-\log(1-H/p)\right].             \tag{3}
\]

Put

\[
 J_b=\sum_{p\in{\cal P}_b}-\log(1-H/p).
\]

Since \(0\le\min(a,y_b)\le a\) and
\(\sum_b\min(a,y_b)\le1\), the linear-programming maximum of the right side
of (3) spends mass \(a\) on at most \(m=\lceil1/a\rceil\) blocks with the
largest \(J_b\).  The ratio
\(-\log(1-H/p)/\log p\) decreases away from \(H\), so (1) and rearrangement
bound their total by the initial prime segment \((H,Y]\) with

\[
 \vartheta(Y)-\vartheta(H)\ll mL_1.
\]

Here \(m\asymp\sqrt H\asymp L_1/L_2\), hence the PNT gives
\(Y\ll H L_2\).  On \(H<p\le2H\), comparison with all integers gives

\[
 \sum_{H<p\le2H}-\log(1-H/p)
 \le\sum_{r=1}^{H}\log{H+r\over r}
 =\log{(2H)!\over(H!)^2}=O(H).                         \tag{4}
\]

For \(2H<p\le H L_2\), use
\(-\log(1-H/p)\le2H/p\) and Mertens to obtain \(O(H)\) again.  Combining
(2)--(4),

\[
 \boxed{
 G_{\rm H}\ll aH={C}\sqrt H
       \asymp {C L_1\over L_2}=o(L_1).
 }                                                       \tag{5}
\]

The candidate-threshold factor \(t^{-R}\) can only subtract from this gain.
Thus no proof that treats \(X^{O(1)}\)-modulus prime blocks separately and
recombines only their scalar interval means by generalized Hölder can reach
the \(>(1+o(1))\log X\) exponent required to empty an \(X\)-interval.

## Scope

Equation (5) does not exclude a phase-sensitive bilinear recombination,
conditioning between blocks, or a signed stopping-line argument.  It only
rules out the tempting black-box composition

\[
 \text{individual block transfer}+\text{generalized Hölder}.
\]
