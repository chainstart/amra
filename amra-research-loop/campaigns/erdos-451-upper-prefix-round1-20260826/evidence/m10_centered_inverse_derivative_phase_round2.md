# M10 round 2: centered inverse-derivative phase diagnostic

Date: 2026-08-27

Status: **finite evidence compatible with marginal square-root cancellation;
not a distribution theorem and not a bound for the high-support A-shell.**

## 1. Exact identities retained

For a dyadic block with offsets `d_1,...,d_q`, put

\[
 F(X)=\prod_i(X-d_i),\qquad p_i=k+d_i,qquad P=\prod_i p_i.
\]

The local phase is not an arbitrary unit.  It obeys

\[
 F'(d_i)=\prod_{j\ne i}(d_i-d_j)
       \equiv(-1)^{q-1}{P\over p_i}\pmod {p_i}.              \tag{1}
\]

There are two useful global identities:

\[
 \prod_iF'(d_i)=(-1)^{q(q-1)/2}
                    \prod_{i<j}(d_i-d_j)^2,                 \tag{2}
\]

and the CRT lift of the vector `(F'(d_i) mod p_i)_i` is

\[
 (-1)^{q-1}\sum_i{P\over p_i}\pmod P.                       \tag{3}
\]

Equation (2) is the discriminant identity.  Equation (3) follows because
all cofactors except `P/p_i` vanish modulo `p_i`.  They show genuine global
dependence, but neither controls the centered representative separately in
each changing modulus.

There is also an exact recursion.  Adding a new offset `d_*` changes the old
phases by

\[
 F_{new}'(d_i)=F_{old}'(d_i)(d_i-d_*),qquad
 F_{new}'(d_*)=\prod_i(d_*-d_i).                              \tag{4}
\]

Thus any theorem should use a multiplicative product-of-differences process,
not independent random residues.

## 2. Guarded finite scan

The script

```text
work/m10_round1/centered_derivative_phase_scan.py
```

formed every actual-prime dyadic block of rank at least 12 for
`k=200,229,...,4985`.  It measured the centered residues

\[
 {\langle F'(d_i)\rangle_{p_i}\over p_i},\qquad
 {\langle F'(d_i)^{-1}\rangle_{p_i}\over p_i},               \tag{5}
\]

adjacent-offset correlation, inverse-residue star discrepancy, and the
largest of the first 16 normalized exponential sums.  There were 741
systems, with ranks from 12 through 230.

Authoritative command:

```text
/home/biostar/work/projects/openmath/bin/openmath-memory-guard -- \
  /usr/bin/time -v python3 \
  amra-research-loop/campaigns/erdos-451-upper-prefix-round1-20260826/work/m10_round1/centered_derivative_phase_scan.py \
  --min-k 200 --max-k 5000 --step 29 --min-rank 12 --frequencies 16
```

Guard unit `openmath-task-20260827-003136-352755.scope` exited zero in
`0.48s`, maximum RSS `15200 KiB`, zero swap.

## 3. Quantitative outcome

For a uniform point of `[-1/2,1/2]`, the reference mean absolute value and
mean square are `1/4` and `1/12`.  Across all 741 blocks the derivative
statistics were

\[
 0.2507518\quad\hbox{and}\quad0.0835836,                     \tag{6}
\]

and the inverse-derivative statistics were

\[
 0.2492591\quad\hbox{and}\quad0.0829566.                     \tag{7}
\]

For the 182 blocks of rank at least 100, these became respectively

\[
 (0.2500942,0.0832347),\qquad(0.2477376,0.0821584).           \tag{8}
\]

The fractions with centered absolute value at most `0.01,0.05,0.10` were,
for inverse derivatives in the rank-at-least-100 stratum,

\[
               0.02066,\quad0.10139,\quad0.20281,            \tag{9}
\]

close to the uniform benchmarks `0.02,0.10,0.20`.  Mean adjacent correlation
was `-0.01610` for derivatives and `-0.00737` for inverses.  The first-16
frequency maximum, multiplied by `sqrt(q)`, had mean `1.7993` and maximum
`2.7539`.  This is compatible with square-root-sized marginal Fourier
coefficients after taking a maximum over 16 frequencies.  It is not proof of
such a bound.

No systematic smallness was visible at high rank.  The extreme small means
and large discrepancies came principally from ranks 12--20.  Conversely,
the exact dependence (2)--(4) means the finite uniform-looking marginals
cannot be promoted to independence.

## 4. Round-3 implication

The scan does not kill the signed inverse-derivative route.  It modestly
supports deepening it, but only at the correct joint statistic.  Marginal
equidistribution of (5) is insufficient for the endpoint problem, whose
actual residual is a weighted simultaneous correlation of the shape

\[
 \sum_{|A|\le X}\prod_i
 W_i\!\left(\left\langle
        (-1)^{q-1}A/F'(d_i)\right\rangle_{p_i}\right),       \tag{10}
\]

with coordinate weights inherited from (43).  A Round-3 theorem or kill
test should therefore retain the recursion (4) inside (10), and seek
square-root cancellation averaged over `A` and a positive proportion of
the block coordinates.  Treating the phases as independent because of
(6)--(9) would be unjustified.
