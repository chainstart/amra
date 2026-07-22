# #679: finite signed-majorant minimax probe

Date: 2026-07-22

The LP in `minimax_majorant_probe.py` minimizes the complete-product-space
mean of a signed multilinear polynomial supported on conductor
\(c(S)\le D\), subject to pointwise majorization of
\(W(x)=\prod_p(1-ax_p)\) on the entire Boolean activation cube.

For \(H=5\), \(a=0.2\), and ten primes \(11,\ldots,43\), the optimum/true-
mean ratios at \(D=1,100,1000,10000,100000,Q\) are respectively

\[
 1.612845, 1.181429, 1.029079, 1.003376, 1.000692, 1.
\]

Thus the finite model decisively rejects a blanket claim that every
**signed**, non-SOS low-conductor majorant must have a large loss.  It is
consistent with the possibility of an adaptive conductor-weighted minimax
majorant.  Conversely, this ten-variable calculation says nothing about the
round-8 asymptotic regime, where \(aHL\asymp\log X\) and the conductor budget
is highly nonuniform across prime scales.

An additional symmetric-binomial exploratory LP showed good accuracy at
small \(a\lambda\), but became severely ill-conditioned once
\(a\lambda\) reached \(40\)--\(200\); HiGHS then returned negative objectives
or “unbounded” statuses incompatible with a genuine majorant problem.  Those
large-parameter outputs are explicitly discarded and are not evidence.

Strict use of the computation: it keeps the non-SOS minimax route alive and
prevents overclaiming the Christoffel/SOS barrier.  No asymptotic inequality
is inferred.

## Abstract-Bonferroni literature boundary

A targeted search found the abstract-tube/improved-Bonferroni literature
(Naiman--Wynn and subsequent work of Dohmen, and the independent-complex
formulas of Attali--Edelsbrunner).  Their savings exploit topological or
emptiness structure in the Venn diagram.  Here every Boolean activation
pattern is realized: for each prime choose one of its \(H\) active residues
or one inactive residue, then apply CRT.  Therefore no missing Venn cell or
contractible-intersection certificate is available for a direct invocation
of those theorems.  A useful result would have to exploit the *weighted
conductor cost*, not merely the incidence complex.
