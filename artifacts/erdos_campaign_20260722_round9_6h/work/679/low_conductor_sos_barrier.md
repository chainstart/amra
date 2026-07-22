# #679: a Christoffel/SOS barrier for low-conductor majorants

Date: 2026-07-22

This note tests the most direct minimax repair of the round-8 tail: truncate a
square root of the weight to low ANOVA conductors and square it (or use a sum
of such squares) to obtain a pointwise nonnegative majorant.  Such a majorant
cannot have a sufficiently small zero mode.

## Product-space evaluation kernel

On the full CRT product space let \(X_p\) be the indicator of the selected
\(H\)-residue block modulo \(p\).  Then the \(X_p\) are independent with

\[
 q_p={H\over p},qquad
 \chi_S(X)=\prod_{p\in S}{X_p-q_p\over\sqrt{q_p(1-q_p)}}
\]

an orthonormal ANOVA basis.  Let \({\cal V}(D_0)\) be the span of \(\chi_S\)
with \(c(S)=\prod_{p\in S}p\le D_0\).  At the all-inactive point
\(x^{(0)}=(0)_p\), its evaluation kernel is

\[
 K(D_0)=\sum_{c(S)\le D_0}|\chi_S(x^{(0)})|^2
 =\sum_{c(S)\le D_0}\prod_{p\in S}{H\over p-H}.         \tag{1}
\]

For every \(P\in{\cal V}(D_0)\), Cauchy in the orthonormal basis gives the
sharp Christoffel inequality

\[
 |P(x^{(0)})|^2\le K(D_0)\,\mathbb E_Q|P|^2.           \tag{2}
\]

The kernel has the elementary uniform bound

\[
 K(D_0)le\sum_{d\le D_0}d< D_0^2.                    \tag{3}
\]

Indeed \(H/(p-H)\le p\) for every integer prime \(p>H\), so the summand
indexed by \(S\) is at most \(c(S)\); distinct \(S\) give distinct squarefree
integers.

## Consequence for sum-of-squares majorants

Suppose

\[
 M(X)=\sum_{\ell}|P_\ell(X)|^2,qquad
 P_\ell\in{\cal V}(D_0),                               \tag{4}
\]

pointwise majorizes the round-8 weight

\[
 W(X)=\prod_p(1-aX_p).
\]

At \(x^{(0)}\), \(W=1\), hence
\(\sum_\ell|P_\ell(x^{(0)})|^2\ge1\).  Summing (2) and using (3) gives

\[
 \boxed{\mathbb E_Q M\ge K(D_0)^{-1}>D_0^{-2}.}        \tag{5}
\]

Products of two ANOVA monomials of conductors at most \(D_0\) have conductor
at most \(D_0^2\).  Thus, to keep the majorant (4) inside the already
transferable range \(X^\kappa\), one must take
\(D_0\le X^{\kappa/2}\).  Equation (5) then forces

\[
 \mathbb E_QM\ge X^{-\kappa}.                           \tag{6}
\]

But the required main term is
\(\mu X^{o(1)}=X^{-C+o(1)}\), with \(C>1\) and
\(\kappa<2/3\).  Therefore (6) is polynomially too large.

## Strict scope

This rules out:

1. square a low-conductor truncation of \(\sqrt W\);
2. any finite or countable sum-of-squares majorant whose square roots have
   conductor at most \(X^{\kappa/2}\);
3. the corresponding Christoffel/minimax optimization, regardless of how its
   coefficients are chosen.

It does **not** rule out a signed low-conductor majorant that is nonnegative
only on the CRT cube but has no low-degree SOS representation, nor a bilinear
majorant using the high-conductor suffix in the stopping identity.  Hence it
is a strict architecture barrier, not closure of #679.
