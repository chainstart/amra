# Final report — Erdős #809 line

## Executive result

The original \(C_7\) instance of Erdős #809 remains open.  This campaign
nevertheless upgrades the inherited one-branch R004 result to a global
theorem throughout the near-Dirac regime:

\[
\boxed{
e(G)>\lfloor n^2/4\rfloor,\quad
\delta(G)\ge n/2-o(n)
\quad\Longrightarrow\quad
\chi_{\mathrm{rainbow}\ C_7}(G)\ge n^2/8-o(n^2).
}
\]

Here the left-hand colouring parameter means the minimum number of colours
in an edge-colouring of \(G\) in which every \(C_7\) is rainbow.

## What changed relative to R004

R004 proved the bound only when a near-half independent set with an almost
complete crossing graph was already supplied.  The new proof removes that
input.

1. If robust exact-four paths exist, a colour used three times produces a
   distance-two pair and hence a no-three-step certificate.
2. The nonempty-common-neighbourhood output is the R004 split branch.
3. The empty-common-neighbourhood output is now closed by two internally
   near-complete half-blocks.
4. If robust exact-four paths fail, a new stability lemma proves that the
   entire graph is close to two balanced cliques or to a balanced complete
   bipartite graph.
5. The clique output is closed by dense \(C_7\) embedding; the bipartite
   output is closed by a generalized maximum-cut core/hub construction.

This is a genuine unbounded theorem, not a finite search observation.

Writing Theorem A in uniform \(\varepsilon\)-\(\eta\) form also closes the
complete BCM-style \(k=3\) Case-2 induction step: choose the Case-2 density
cutoff \(\kappa^2\) below the near-Dirac modulus and below the target
induction error.  The exact comparison is recorded in
`BCM_CASE2_INTERFACE.md`.

## Red-team result

The most fragile implication was:

> failure of an exact-four-edge path \(\Rightarrow\) near two-clique or
> near complete-bipartite structure.

It was written with explicit quantifiers and error
\[
O((N-2\delta(H)+1)N).
\]
The proof needs the adjacency-symmetry product bound
\[
|X\cap U|\,|X\cap W|\le O(N-2\delta+1)|X|,
\]
which rules out a linear mixture of the two neighbourhood orientations.
Without this step, the dichotomy would not follow.

The second fragile implication, from a same-colour distance-two pair to a
no-three-step certificate, explicitly excludes shared endpoints and
outer-endpoint adjacency before splicing the seven-cycle.

No logical break was found in these audits.  The finite guard suite passed:

- 33,864 labelled graphs through order six;
- 212,888 exact-four-path obstruction profiles;
- 728 actual distance-two/three-path \(C_7\) splices;
- all 496 core/hub family pairs in a model whose nominal second side is
  deliberately non-independent;
- all 80,601 rational optimization profiles at denominator 400.

## Why this is not yet a proof of #809

BCM26's full-range induction can enter its high-density Case 1 with
\[
\delta(G)\approx
\frac n2-\sqrt{e(G)-n^2/4}.
\]
When \(e(G)-n^2/4=\Theta(n^2)\), the deficit is linear.  Theorem A requires
an \(o(n)\) deficit.  Neither the exact-four-path stability lemma nor the
near-two-clique closure bridges that linear gap.

Thus the unique main mathematical target in the BCM route is now:

> **Parameterized Case-1 stability.**  For
> \(s=\sqrt{e/n^2-1/4}\), control rainbow-\(C_7\) colour classes under
> \(\delta\ge(1/2-s+o(1))n\) strongly enough to produce
> \[
> \left(\frac18+\frac s2+\frac{s^2}{2}-o(1)\right)n^2
> \]
> colours.

That expression is the edge count of the larger clique in the extremal
two-clique construction and equals the BCM target.

`CASE1_OBSTRUCTION_REDUCTION.md` further shows that this target only has
to be proved in two exact profiles: a distance-two same-colour pair with a
no-three-step outer certificate, or a distance-three same-colour pair whose
outer endpoints have disjoint neighbourhoods.  If neither profile occurs,
all BCM good edges have different colours and the full target follows
immediately.

## Publication assessment

The present package is substantially stronger than the previous proof
seed and may support a serious stability note after novelty clearance.
It is not yet safe to call it a Q1-ready paper:

- the closest authors have already announced an unspecified \(k=3\)
  Case-2 stability argument;
- quantitative constants have not been inserted into their induction;
- no exhaustive citation-chain or expert proof audit has been completed;
- the headline Erdős problem remains open.

For a credible Q1-level outcome, the preferred route is to solve the
parameterized Case-1 target above.  A second route is to establish that the
exact-four-path obstruction stability theorem is independently novel and
broad enough to matter outside #809, then strengthen it to a quantitative
prescribed-path stability theorem.

## Second-attack addendum

The fixed-\(s\) Case 1 was attacked after the midpoint red team.  It remains
open, but the two obstruction profiles now have one exact common form.
For two induced edges, membership in a common \(C_7\) is equivalent to one
endpoint pairing supporting vertex-disjoint paths of lengths two and three.

If \(M_\gamma\) is the set of BCM good edges with colour \(\gamma\), the
remaining colour loss is exactly
\[
\sum_\gamma (|M_\gamma|-1)_+.
\]
Thus the minimum sufficient closure lemma is
\[
\sum_\gamma (|M_\gamma|-1)_+=o(n^2).
\]
The missing ingredient is bounded-congestion charging of every non-root
same-colour edge to its length-three-path-cover or zero-codegree
certificate.  The inherited two-interior estimate cannot be enough for
general fixed \(s\): even with favourable global colour separation it falls
below the BCM target when
\[
s>\frac{1-\sqrt{4/5}}2.
\]

See `CASE1_SECOND_ATTACK.md` and `verify_809_case1_second.py`.  This addendum
does not change the claim boundary: Erdős #809 remains open.

## Repository boundary

Only files inside
`data/research_open/q1_four_problem_campaign_2026-07-30/erdos809/`
were created or modified.  No commit or push was performed.
