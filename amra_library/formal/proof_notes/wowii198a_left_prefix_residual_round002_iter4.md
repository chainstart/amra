# WOWII198a left-prefix residual round 002 iteration 4

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
  results for `Walk.toPath`, `takeUntil`, and `dropUntil`, and the configured
  Lean verifier output.

Lean progress:
- In the hard branch of
  `terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false`,
  derived the fallback facts:
  `y ∈ rs.support`, `y ≠ x`, `y ∉ pair.1.support`, and
  `y ∉ (rs.takeUntil w hw_rs).support`.
- Constructed the intended fallback right path
  `((rs.takeUntil y hy_rs).append ((pair.2 : G.Walk v t).dropUntil y hy_right)).toPath`
  and the corresponding `fallbackPair`.

Verifier result:
- The required verifier still fails.
- The first error is now the final weighted contradiction line in the fallback
  branch, after the derived facts and `fallbackPair` construction have
  typechecked.
- The two older arbitrary-pivot branches still fail at the same residual
  `hpair_measure_min : False` stubs.

Next target:
- Prove the weighted fallback for `fallbackPair`: common-card nonincrease and
  strict support-length descent, then call
  `false_of_weighted_min_and_commonCard_le_supportLength_lt`.
