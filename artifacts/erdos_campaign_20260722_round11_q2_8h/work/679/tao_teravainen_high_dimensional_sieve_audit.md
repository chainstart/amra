# #679: Tao--Teräväinen high-dimensional sieve audit

Date: 2026-07-22

Primary source:
[Tao--Teräväinen, *Quantitative correlations and some problems on prime
factors of consecutive integers*, arXiv:2512.01739v2](https://arxiv.org/abs/2512.01739).
The arXiv record is v2, updated 2026-04-25.
The submission history gives v1 on 2025-12-01 and v2 on 2026-04-25;
the current TeX source was checked in addition to the rendered text.
The extracted v2 main2.tex checked in this audit has SHA-256
66eb00d6506974a42db872c26f6e4673eed0a4d5ab68b552c86a38d2f1bc3292.

## 1. What the paper proves

Their Theorem 1.1 closes Erdős #248: there is an absolute \(C>0\) and
infinitely many positive integers \(n\) such that

\[
 \omega(n+k)\le\Omega(n+k)\le Ck
\]

for every positive integer \(k\).

For the difficult initial range they construct a probability measure on
\([x,2x]\) from a product of smooth one-dimensional Selberg sieves. The
simultaneous shift dimension is

\[
 K=\left\lfloor {1\over C_0}\log_2x\right\rfloor,
\]

and the prime cutoff for the \(k\)-th form is roughly
\(R_k=x^{1/100^k}\). They compute bounded-order correlations, principally
second and fourth moments, with enough uniformity for this slowly growing
dimension.

## 2. The paper explicitly identifies #679 as out of range

Remark 1.2 states the #679 question in the form

\[
 \omega(n-k)<(1+\varepsilon){\log k\over\log_2k}
\]

for all sufficiently large \(k<n\), and says that it appears to be beyond
the capability of their methods. This is direct primary-source evidence,
not an inference from the title or abstract.

The same v2 remark has a footnote pointing to Lau's later
\(O(\log k)\) refinement. Thus this audit does not treat the older
\(O(k)\) theorem as the current best partial bound; the Lau comparison is
recorded separately in lau_2026_direct_boundary_audit.md.

## 3. Why its proved theorem does not fill the present tail

There are three quantitative differences.

1. The proved upper bound \(Ck\) is much weaker than
   \((1+\varepsilon)\log k/\log_2k\).
2. The simultaneously engineered range has dimension
   \(O(\log_2X)\). The present deterministic contradiction block has
   \(H=(\log X)^2\) shifts and needs a lower-tail saving on the scale
   \(HL\asymp(\log X)^2\log_2X\).
3. Their sieve is designed to construct some \(n\in[x,2x]\) under a
   positive probability measure. The unresolved #679 object here is an
   upper bound for a signed ultra-high-conductor aggregate at every
   self-consistent dyadic scale. Neither their theorem nor their stated
   moment calculations assert such a bound.

The paper is nevertheless the closest checked high-dimensional sieve
comparison and a natural source for any future attempt to replace the
Fourier-tail route. Its own Remark 1.2 confirms that no #679 closure can
be imported from the current version.

Strict status: **direct recent-method applicability audit; #248 closed in
the source, #679 explicitly left beyond the method, and no #679 theorem is
claimed here**.
