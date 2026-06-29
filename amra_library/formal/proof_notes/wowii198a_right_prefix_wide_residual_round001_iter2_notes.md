# wowii198a right-prefix wide residual round 001 iteration 2

Verifier command run from `/home/biostar/work/projects/amra/amra_library/formal`:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

Result: failed.

External sources relied on:
- None from web or literature.
- Local artifact sources read:
  `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_prefix_wide_residual_20260628_focused/wowii198a-right-prefix-wide-residual/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-right-prefix-wide-residual-descent/context_bundle.md`
  and
  `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_prefix_wide_residual_20260628_focused/wowii198a-right-prefix-wide-residual/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-right-prefix-wide-residual-descent/math_tools_report.md`.

Current first blocker:
- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, right-not-left
  bad pivot branch.
- The two live Lean errors are now:
  - `Wowii198aLeftmost.lean:6678:16`
  - `Wowii198aLeftmost.lean:6743:18`
- Both still use `hpair_measure_min` where Lean expects `False`.

Lean progress this iteration:
- Added
  `terminal_set_fan_left_suffix_retention_right_only_first_wide_residual_descent`.
- This helper proves the right-only first-wide-residual splice descent directly:
  if the splice pivot is right-only, lies in the old-right suffix after `x`,
  and is first for the broadened old-residual set on `rs`, then
  `((oldLeft), rs.takeUntil z ++ oldRight.dropUntil z)` has strictly smaller
  common-card.
- The containment proof uses
  `false_of_first_noncommon_old_residual_and_left_prefix` for left-only
  prefix intersections instead of treating weighted minimality as `False`.

Why the verifier still fails:
- The active failing theorem still selects the last bad pivot in
  `rs ∩ altRight`, not the first wide residual.
- The new helper applies only after the right branch is refactored to choose a
  suitable first-wide/right-suffix pivot before constructing `spliceRight`.

Next target:
- Refactor the right-not-left branch of
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` so it selects a
  first wide residual before the current `spliceRight` construction.
- The remaining hard split is the old-left-only first-wide case; the
  right-only-after-`x` case now has a compiled descent helper.
