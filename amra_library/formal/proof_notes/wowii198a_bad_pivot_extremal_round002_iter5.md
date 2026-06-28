# WOWII198a bad-pivot extremal round 002 iteration 5

External source policy: OPEN RESEARCH.  No web or literature source was used in
this iteration.  Sources relied on were the supplied local `context_bundle.md`,
the supplied local `math_tools_report.md`, existing local proof notes, the
target Lean file, the configured Lean verifier, and the local Python finite
search script.

Current first blocker:
- `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent`, feeding
  `terminal_set_fan_left_suffix_retention_alt_intersections_control`, then
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, the splice
  descent chain, the two-fan theorem, Chvatal-Erdos traceability, and
  `conjecture198a`.

Verifier/tool checks:
- Ran the required verifier command:
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.
  It still fails only at the two residual membership branches inside the older
  arbitrary-pivot lemma, where `hpair_measure_min` is used as membership in the
  old erased common-support set with `x` removed.
- Reran `proof_notes/wowii198a_suffix_retention_round003_countermodel_search.py`.
  Output: `no countermodel in shaped six-vertex search` and
  `no countermodel in 2000 random six-vertex graphs`.
- Searched the local mathlib checkout for a reverse support theorem for
  `Walk.toPath`.  The available theorem is only
  `Walk.support_toPath_subset`, so residual vertices from a raw append support
  cannot automatically be fed back into a bad set defined using
  `altRight.toPath.support`.

Lean route assessment:
- The existing one-splice containment proof is still the wrong local target.
  In the left residual branch, a vertex `y` from `rs.dropUntil z` can meet the
  old right path before `x`; it need not be in the old common support, and it
  need not lie in `altRight.toPath.support`.
- The next useful theorem-level helper should handle this residual branch by a
  weighted descent, not by erased-common containment for the one-splice pair.
  The candidate pair is the two-splice pair:
  left path `oldLeft.takeUntil z ++ rs.dropUntil z`, right path
  `oldLeft.takeUntil x ++ oldRight.dropUntil x`.
  This replaces the old common vertex `x` by the bad pivot `z`; the cardinal
  part should be proved by a finite-set bound of the form
  `newCommon ⊆ insert z (oldCommon.erase x)`, and the strict weighted decrease
  should come from support-length descent.
- The symmetric right residual branch needs the analogous two-splice weighted
  descent package.

No trusted assumptions, theorem weakening, or forbidden proof tokens were
introduced.
