# #679: exact stopping-line recombination of the high-conductor ANOVA tail

Date: 2026-07-22

This is an exact algebraic reduction of the round-8 tail.  It removes the
spurious entropy coming from conductor sets that have already crossed the
cutoff.  It does not by itself prove the required interval bound.

## Identity

Order the selected primes as \(p_1,\ldots,p_M\), and write

\[
 W_i(n)=m_i+d_i(n),\qquad
 F_S(n)=\prod_{i\notin S}m_i\prod_{i\in S}d_i(n).
\]

For \(A\subseteq[j-1]\), put \(c(A)=\prod_{i\in A}p_i\).  The high-conductor
tail

\[
 R_D(n)=\sum_{\prod_{i\in S}p_i>D}F_S(n)
\]

has the exact stopping-line representation

\[
 \boxed{
 R_D(n)=\sum_{j=1}^{M}d_j(n)
 \prod_{i>j}W_i(n)
 \sum_{\substack{A\subseteq[j-1]\\c(A)\le D<c(A)p_j}}
 \prod_{i\in A}d_i(n)
 \prod_{\substack{i<j\\i\notin A}}m_i .
 }                                                       \tag{1}
\]

Indeed, every high set \(S\) has a unique first index \(j\) at which its
running conductor exceeds \(D\).  Fixing this crossing and summing freely
over membership after \(j\) replaces every later \(m_i/d_i\) pair by
\(m_i+d_i=W_i\).  Thus (1) is a partition, not an estimate.

If the primes are ordered decreasingly, every conductor at the crossing
satisfies

\[
 D<c(A)p_j\le Dz=X^{\kappa+o(1)}<X                  \tag{2}
\]

for fixed \(\kappa<1\).  Hence all *frontier coefficients* in (1) lie below
the interval length even though the freely recombined suffix has enormous
joint modulus.  This is sharper than summing all \(2^M\) high sets
separately.

## What remains after recombination

The suffix \(\prod_{i>j}W_i(n)\) is positive and at most one, but simply
discarding it on positive frontier terms loses precisely the accumulated
zero-mode saving.  Taking absolute values in the inner frontier likewise
restores a large subset entropy.  Thus the unresolved analytic object is a
bilinear correlation

\[
 \sum_{n\in I}
 \bigl(\text{low-conductor crossing polynomial at }n\bigr)
 \prod_{i>j}W_i(n),                                    \tag{3}
\]

not an isolated full-conductor Fourier layer.  A continuation must exploit
the mean-zero sign of \(d_j\), or conditionally transfer the positive suffix,
rather than replace that suffix by one.

## Finite audit

`verify_stopping_line.py` checks (1) for
\(H=2\), \(t=0.7\), \(Q=3\cdot5\cdot7\cdot11\cdot13=15015\), four cutoffs,
both increasing and decreasing prime order, and every residue modulo \(Q\).
The maximum identity error is \(2.220\times10^{-16}\).  The interval-tail
sign changes with the cutoff in the same test, confirming that an unsigned
monotonicity claim would be invalid.

Strict status: **exact reduction / bilinear suffix correlation open**.
