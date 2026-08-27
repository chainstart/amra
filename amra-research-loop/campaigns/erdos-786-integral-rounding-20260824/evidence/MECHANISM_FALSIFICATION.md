# Mechanism falsification

The exact replay is

```text
python3 evidence/verify_integral_rounding_kills.py
```

with SHA-256

```text
4eddf2345972162e722ad95f2bcde01982f2fc109bb679d835315faa48e0b0ad
```

It returns `PASS`.  Its loops instantiate symbolic families; the universal
kills below come from the proofs, not from cutoff extrapolation.

## M786I-01 killed: every `o(N)` hard lower-tail threshold fails

Write `N=2^K`.  Deleting `n<=N^(1-delta_K)` has relative cost
`N^(-delta_K)=2^(-K delta_K)`, so it is `o(N)` precisely in the useful regime
`K delta_K -> infinity`.  Theorem IR.1 applies to this moving sequence and,
for every sufficiently large `K`, embeds a support-minimal bad relation
entirely in the retained strict tail.  This kills the full quantified claim,
not only constant thresholds.

## M786I-02 killed: finite nested coarea thresholds collapse

The sets `{w_N>=t_i}` are nested, so their finite union is `{w_N>=min t_i}`.
If its size is `o(N)`, the minimum threshold satisfies the same moving-tail
condition as M786I-01 and is defeated by IR.1.  This does not kill a coarea
rule whose choices also depend on prime-incidence rank.

## M786I-03 killed: independent rounding cannot cover almost surely

Suppose independent probabilities obey
`q_N(n)<=g_N w_N(n)` with `g_N=o(log N)`, the scale required for the promoted
mass to have expected cost `o(N)`.  On powers `N=2^K`, put
`eta_K=1/(2 max(1,g_N))`.  Then `K eta_K -> infinity`; IR.1 supplies a bad
edge all of whose weights are below `eta_K`, hence every `q_N(n)<1/2` on
that edge.  Independence gives the edge a strictly positive probability
`prod_(n in E)(1-q_N(n))` of being completely missed.  Thus the sample is
not a transversal with probability one.  Randomized alteration remains a
different mechanism.

## M786I-04 killed: one arbitrary representative per disjoint edge

The three arithmetic bad supports

```text
{2,3,6}, {5,6,30}, {2,5,10}
```

are pairwise intersecting and have no common vertex.  The first alone is a
maximal vertex-disjoint edge family.  Choosing its representative `3` misses
both other edges.  Maximality of a disjoint packing guarantees that the
**union** of its edges is a transversal, not that one arbitrary point per
packed edge is.

## M786I-07 killed: residue-free largest-prime triangularity

In `2*3=6`, the largest active prime `3` sees one term on each shore, so the
top-fibre cardinalities balance.  Stripping that prime leaves cofactors `1`
and `2`; the latter contributes to the lower prime `2`.  Therefore lower
valuation equations are not triangular in fibre cardinality unless the
cofactor residue is retained.  This is the smallest exact counterexample to
the claimed elimination.

## M786I-08 killed: no single active-degree layer has mass one

This failure has an all-parameter finite-cylinder proof.  Choose finite prime
blocks `P_m` whose least prime tends to infinity and whose reciprocal mass
`lambda_m=sum_(p in P_m)1/p` tends to infinity; this is possible by divergence
of the prime reciprocal series.  On residues modulo `prod_(p in P_m)p^2`,
the indicators

```text
X_p = 1_{nu_p(n)=1}
```

are independent Bernoulli variables of parameters
`q_p=(p-1)/p^2`.  Their variance is asymptotic to `lambda_m`.  Fourier
inversion and

\[
|E e^{itX}|^2
=\prod_p(1-4q_p(1-q_p)\sin^2(t/2))
\le \exp(-4\sigma_m^2\sin^2(t/2))
\]

give `sup_k P(sum X_p=k)=O(1/sqrt(lambda_m))=o(1)`.  Meanwhile the zero layer
has probability at most `exp(-sum q_p)=o(1)`, and the total square-exponent
exception is `O(sum_(p>=min P_m)1/p^2)=o(1)`.  Thus conditioning on a
nonempty squarefree active set cannot make any single active-degree stratum
dense.  The fact that a fixed stratum is admissible is insufficient.

## M786I-09 killed: adjacent active degrees already contain bad circuits

For every `s>=1`, label `K_(s+1,s)` edges by active primes.  Left vertex
integers have active degree `s`, right vertices degree `s+1`, and the two
shore products agree with cardinalities `s+1` and `s`.  Hence the union of
the adjacent degree strata `s,s+1` is not certified by total incidence.
This leaves open a selection using the full incidence pattern rather than
only degrees.

## M786I-10 killed: global rank cannot bound the transversal

On the one-prime universe

\[
\{2^1,2^2,\ldots,2^{6r}\},
\]

the exponent matrix has rank one.  For `0<=j<r`, the supports with exponents

\[
\{3j+1,\;3j+2,\;6j+3\}
\]

are pairwise vertex-disjoint and bad because
`(3j+1)+(3j+2)=6j+3`.  Every transversal therefore has at least `r`
vertices.  No universal `C*rank` bound exists.  Since this universe itself is
sparse in `[N]`, the family does not refute a weight-compatible **local**
rank/coarea theorem.

## M786I-11 killed: a fixed valuation cylinder is not coherent protection

Fix any finite controlled prime set.  Choose the padding prime and all path
edge primes outside it in the IR.1 construction.  Every constructed integer
then has the same zero valuation signature on the controlled primes, while
the full support is a minimal bad relation.  Thus admitting the entire
zero-signature cylinder is invalid.  A growing-state profinite rule with a
proved stabilization theorem is materially different and remains inside
M786I-12.

## Survivors

### M786I-05: arithmetic resampling/alteration

This survives only with an explicit witness compression on the rough,
long-circuit hypergraph.  Neither per-edge probability nor a generic LLL
dependency count is accepted.  The target is an all-`N` charged repair of
cost `O(log log N) sum w_N` or any `o(log N)` multiple.

### M786I-06: largest-prime ownership with residue state

The residue-free form is killed by M786I-07, but a rule carrying lower-prime
cofactors has not been refuted.  It must prove that one integer receives only
`o(log N)` total charge over every prime scale after the smooth exception is
removed.

### M786I-12: recursive token balance and coherence

This is the exact-state version of prime peeling.  It keeps balanced top-
fibre token counts together with their cofactor products and is the only
survivor that could stabilize across cutoffs.  Its decisive missing theorem
is a bounded potential preventing the residue state from reproducing the
original circuit at every lower level.

These three targets are all-parameter and non-equivalent as mechanisms:
failure-event compression, deterministic owner congestion, and recursive
state potential.  None is currently proved.
