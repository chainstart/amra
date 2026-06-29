## 2026-06-28 left-prefix not-alt descent iteration 6

Current first blocker:
- The requested stage theorem
  `terminal_set_fan_left_suffix_retention_left_prefix_not_alt_commonCard_descent`
  is closed in the live Lean file.  The `hy_suffix` branch constructs the
  later-return witness and routes it through
  `terminal_set_cross_swap_commonCard_lt_of_later_return`.
- The configured verifier still fails downstream in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, in the
  old-right-suffix branch at
  `AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean:6401:14`.

External sources relied on:
- None.  This iteration used only local Lean files, local proof notes, local
  mathlib source, and the configured Lean verifier.
- The prompt-specified run-artifact directory was not present in this
  workspace.  Attempts to read both `context_bundle.md` and
  `math_tools_report.md` at that path returned `No such file or directory`.

Diagnosis:
- The failing branch has a vertex `y` with
  `y ∈ (rs.takeUntil z hzrs).support` and
  `y ∈ (pair.1 : G.Walk v s).support`, while `y` is not an old common vertex
  distinct from `x`.
- The current proof selected `z` using `exists_last_bad_pivot_on_rs`.  That
  controls residual bad vertices in `rs.dropUntil z`, which is exactly what the
  left-prefix branch needs, but it does not control bad vertices in
  `rs.takeUntil z`.
- The checked helper
  `terminal_set_fan_left_suffix_retention_right_suffix_residual_bad_false_of_altRight`
  is the correct local contradiction only when the prefix residual vertex is
  known to lie in `altRight`.  The current branch does not provide that fact.
- Therefore replacing `exact hpair_measure_min` with another direct use of
  weighted minimality is not type-correct.  The right-suffix branch needs a
  first-bad-pivot package from `exists_first_bad_pivot_on_rs`, plus a non-alt
  fallback using `not_mem_left_suffix_fallback_of_not_left_prefix`.

Next Lean target:
- Prove a right-suffix prefix-residual fallback lemma:
  for a first bad pivot `z` on `rs`, if a prefix residual `y` is old-left-only,
  split on `y ∈ altRight`.  The alt subcase should call
  `terminal_set_fan_left_suffix_retention_right_suffix_residual_bad_false_of_altRight`.
  The non-alt subcase should build
  `fallbackLeft = ((rs.takeUntil y hy_rs).append
    ((pair.1 : G.Walk v s).dropUntil y hy_left)).toPath`,
  pair it with `altRight`, prove erased-common containment with `x` removed,
  and contradict weighted minimality through the existing common-card descent
  machinery.

Main-chain impact:
- This closes `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- That feeds `terminal_set_fan_left_suffix_retention_alt_intersections_control`,
  then `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, the
  splice descent chain, the two-fan theorem, Chvatal-Erdos traceability, and
  finally `conjecture198a`.
