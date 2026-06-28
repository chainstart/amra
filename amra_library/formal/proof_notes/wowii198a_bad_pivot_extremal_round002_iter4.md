# WOWII198a bad-pivot extremal round 002 iteration 4

External source policy: open research.  No web or literature source was used.
Sources relied on were the supplied local context bundle, the supplied local
math tools report, existing local proof notes, the target Lean file, the local
Python finite-search script, and local Lean verifier output.

Current first blocker:
`terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` still
depends on the retained-suffix bad-pivot package.  The older arbitrary-pivot
lemma `terminal_set_fan_left_suffix_retention_bad_pivot_descent` still fails in
the two residual containment branches.

Tool checks:
- Required Lean verifier:
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`
  failed only at the residual membership terms now located at lines 4881 and
  4968.  In both places `hpair_measure_min` has weighted-minimality type while
  Lean expects membership in
  `(((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`.
- Re-ran `proof_notes/wowii198a_suffix_retention_round003_countermodel_search.py`.
  Output: `no countermodel in shaped six-vertex search` and
  `no countermodel in 2000 random six-vertex graphs`.

Lean progress:
- Added checked finite bad-set selection helpers:
  `exists_last_bad_pivot_on_rs` and `exists_first_bad_pivot_on_rs`.
- These helpers turn the existential bad-pivot witness for the current
  extremal target into a last or first bad pivot on `rs`, with the corresponding
  `dropUntil` or `takeUntil` extremality property.
- The helpers typecheck under the required verifier.  They do not yet replace
  the body of `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent`,
  so the verifier still reaches the old arbitrary-pivot residual branches.

Next target:
- Refactor `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent`
  to use `exists_last_bad_pivot_on_rs` for the old-left-prefix bad branch and
  `exists_first_bad_pivot_on_rs` for the old-right-suffix bad branch.
- Then refactor `terminal_set_fan_left_suffix_retention_bad_pivot_descent` into
  a corollary of the extremal helper instead of proving erased-common
  containment for an arbitrary bad pivot.
