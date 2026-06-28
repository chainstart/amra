# WOWII198a bad-pivot extremal round 002 iteration 3

Current first blocker between
`terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` and
`conjecture198a` remains the retained-suffix bad-pivot package.

External source policy: open research.  No web or literature source was used in
this iteration.  Sources relied on were the local context bundle, the local math
tools report, existing local proof notes, the target Lean file, and local
Python/Lean verifier output.

Tool checks:
- The configured Lean verifier was run before editing and failed only at the
  two residual containment branches inside
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`:
  `hpair_measure_min` is still being used where Lean needs membership in
  `(((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`.
- A transient exact Python graph search over the current extremal-helper shape
  completed all graphs on four and five vertices with zero satisfying instances,
  then was interrupted in the six-vertex range because it was not finishing
  quickly enough.  This produced no counterexample.
- Re-ran the existing durable search
  `proof_notes/wowii198a_suffix_retention_round003_countermodel_search.py`.
  Output:
  `no countermodel in shaped six-vertex search`
  and
  `no countermodel in 2000 random six-vertex graphs`.

Lean assessment:
- The target declaration is present and has the requested extremal-helper
  statement.
- The body of
  `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` still
  delegates to the older arbitrary-pivot theorem
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- The older theorem is not repairable by local containment: prior support-order
  probes and the current proof shape show that an arbitrary residual vertex in
  the left or right replacement side need not already be in the old common
  support with `x` erased.
- Existing checked helpers
  `mem_erase_common_without_x_or_not_common_triple` and
  `mem_erase_common_without_x_or_not_common_triple_left` can classify each
  residual vertex, but the proof still lacks the theorem-level step converting
  the non-common alternative into either:
  1. contradiction by first/last bad-pivot extremality, or
  2. common-card nonincrease plus strict support-length descent, then
     contradiction via
     `false_of_weighted_min_and_commonCard_le_supportLength_lt`.

Next Lean target:
- Replace the wrapper body of
  `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` with a
  real finite bad-set selection on `rs`.
- Use `exists_last_mem_support_forall_mem_dropUntil_imp_eq` for left-prefix bad
  pivots and `exists_first_mem_support_forall_mem_takeUntil_imp_eq` for
  right-suffix bad pivots.
- Prove the residual non-common branch as an extremal contradiction or as the
  weighted support-length descent packaged by the existing weighted-minimality
  helper.
