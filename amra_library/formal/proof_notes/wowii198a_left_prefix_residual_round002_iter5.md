# WOWII198a left-prefix residual round 002 iteration 5

Current first blocker:
- `terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false`.
- This helper feeds `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent`,
  then `terminal_set_fan_left_suffix_retention_bad_pivot_descent`,
  `terminal_set_fan_left_suffix_retention_alt_intersections_control`,
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, the splice
  descent chain, the two-fan theorem, Chvatal-Erdos traceability, and finally
  `conjecture198a`.

External sources relied on:
- None from web or literature search.
- Local sources read: the supplied `context_bundle.md`, supplied
  `math_tools_report.md`, existing local proof notes, local mathlib grep
  results for `Walk.toPath`, `takeUntil`, `dropUntil`, and the configured Lean
  verifier output.

Tool check:
- Ran a bounded Python union-path search for small configurations satisfying
  the weighted-minimality condition and bad-pivot hypotheses. The exhaustive
  search did not return within 60 seconds and was interrupted, so it is
  inconclusive and is not used as proof evidence.

Lean progress:
- Added checked pair-level wrapper
  `terminalPathPairCommonCard_le_of_subset_insert_erase_common`, packaging the
  existing finite-set lemma
  `common_support_erase_card_le_of_subset_insert_erase_common` at the
  `terminalPathPairCommonCard` level.
- Added checked pair-level wrapper
  `terminalPathPairSupportLength_lt_of_same_left_right_lt`, reducing a
  same-left support-length descent to the changed right path's strict support
  length inequality.

Verifier result:
- The required verifier still fails.
- The new wrappers compile cleanly; the only Lean errors remain the three
  residual `False` branches where `hpair_measure_min` is still used directly.

Next target:
- Prove the concrete fallback facts needed by the wrappers for the constructed
  `fallbackPair`: the common-support subset into
  `insert y (((oldCommon.erase v).erase x))`, and a strict support-length
  descent for the selected secondary splice.
