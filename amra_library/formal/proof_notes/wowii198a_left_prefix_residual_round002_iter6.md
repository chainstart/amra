# WOWII198a left-prefix residual round 002 iteration 6

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
  `math_tools_report.md`, local mathlib files for `SimpleGraph.Walk`
  `takeUntil`, `dropUntil`, `toPath`, and the configured Lean verifier output.

Tool check:
- Ran a bounded Python sanity check on a seven-vertex graph with paths
  `left = v-z-x-s`, `right = v-w-y-x-t`, and `rs = v-w-z-y-s`.
- The skeleton satisfies the order/residual assumptions
  `hfirst`, `hret`, `z ∈ left.takeUntil x`, `z ∉ rs.takeUntil w`,
  `y ∈ rs.dropUntil z`, `y ∈ right`, `y` is not an old common non-`x`, and
  `y ∉ altRight`.
- The selected pair is not weighted-minimal in that graph: a lower pair
  `v-w-y-s` with `v-z-x-t` has common-card `0`. This does not disprove the
  Lean helper, but it shows the one-sided fallback pair is probably the wrong
  repair; the residual branch likely needs a two-sided replacement pair.

Lean progress:
- Added checked order lemma `mem_dropUntil_of_not_mem_dropUntil`, proving that
  for vertices on a walk, if `y` is not in the suffix from `x`, then `x` is in
  the suffix from `y`. This compiles and is intended to support the residual
  branch proof that `hy_alt = false` puts `x` after `y` on the old right path.

Verifier result:
- The required verifier still fails.
- The only Lean errors remain the three residual `False` branches where
  `hpair_measure_min` is used directly.

Next target:
- Replace the one-sided fallback in
  `terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false` with
  a two-sided replacement pair: left path from the old-right prefix to `y`
  followed by `rs.dropUntil y`, and right path `altRight`. Prove its common
  support is contained in the old common support with `x` erased, then
  contradict weighted minimality via the existing common-card descent route.
