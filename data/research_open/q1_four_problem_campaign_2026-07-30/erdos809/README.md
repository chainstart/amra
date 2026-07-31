# Erdős #809 — 2026-07-30 Q1 campaign

This directory contains the #809 line of the four-problem campaign.  It is a
read-only continuation of

- `artifacts/erdos_master_rotation/R002/core_809_592/`;
- `artifacts/erdos_master_rotation/R002/qa_809/`;
- `artifacts/erdos_master_rotation/R003/core_809_592/809/`;
- `artifacts/erdos_master_rotation/R004/core_809_592/809/`.

## Outcome

The original problem is **not closed**.  The low-minimum-degree part of the
Bucić--Chen--Ma high-density Case 1 remains open.

The new rigorous milestone is an unbounded near-Dirac theorem:

> Let \(G_n\) be an \(n\)-vertex graph sequence with
> \[
> e(G_n)>\lfloor n^2/4\rfloor,\qquad
> \delta(G_n)\ge n/2-o(n).
> \]
> Every edge-colouring of \(G_n\) in which every \(C_7\) is rainbow uses at
> least
> \[
> n^2/8-o(n^2)
> \]
> colours.

This removes all additional structural hypotheses from the R004
near-complete-split theorem.  Its two new structural ingredients are:

1. a closure theorem for the near-two-clique branch of the R003 no-three-step
   obstruction;
2. a four-path-obstruction stability lemma: failure of a simple path of
   exactly four edges between one pair forces edit distance \(o(n^2)\) from
   either two balanced cliques or a balanced complete bipartite graph.

The near-bipartite output is closed by a maximum-cut version of the R004
core/hub construction; the near-two-clique output is closed by a dense
seven-cycle embedding lemma.

In `BCM_CASE2_INTERFACE.md`, the theorem is put into uniform
\(\varepsilon\)-\(\eta\) form and closes the full BCM-style \(k=3\)
Case-2 induction step after choosing the density cutoff sufficiently below
the target error.  The only remaining bottleneck in that route is Case 1.

## Files

- `FOUR_PATH_OBSTRUCTION_STABILITY.md`: quantified stability lemma and proof.
- `MAXCUT_CORE_HUB_THEOREM.md`: near-bipartite colour lower bound without an
  independent-side assumption.
- `NEAR_DIRAC_C7_THEOREM.md`: complete proof of the new near-Dirac theorem.
- `BCM_CASE2_INTERFACE.md`: rigorous insertion into the BCM-style Case-2
  induction step.
- `CASE1_OBSTRUCTION_REDUCTION.md`: exact reduction of the sole remaining
  Case 1 to distance-two/no-three-step and distance-three/disjoint-
  neighbourhood profiles.
- `verify_809_near_dirac.py`: independent finite guards.
- `test_809_near_dirac.py`: executable regression tests.
- `VERIFICATION.md`: commands, counts, and guard boundaries.
- `CLAIM_LEDGER.md`: proved/open/conditional claims.
- `FINAL_REPORT.md`: campaign-level assessment and next bottleneck.

## Claim boundary

Finite computation is used only to check displayed templates and exact
finite inequalities.  It is not used to extrapolate an asymptotic claim.
The new theorem does not imply Erdős #809 because the BCM26 induction can
enter a regime
\[
\delta(G)\approx n/2-\sqrt{e(G)-n^2/4},
\]
whose deficit from \(n/2\) can be linear in \(n\).
