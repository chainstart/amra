# wowii198a right-prefix wide residual round 001 iteration 3

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
  - `Wowii198aLeftmost.lean:6706:16`
  - `Wowii198aLeftmost.lean:6771:18`
- Both still use `hpair_measure_min` where Lean expects `False`.

Lean progress this iteration:
- Added `noncommon_old_residual_exclusive_side`.
- This packages the immediate consequence of `x ∉ rs.support`: any selected
  wide residual on `rs` that lies on an old path and is not an old common
  vertex distinct from `x` is strictly one-sided, either old-left-only or
  old-right-only.
- Updated
  `terminal_set_fan_left_suffix_retention_right_prefix_wide_residual_descent`
  so it actually applies `exists_first_noncommon_old_residual_on_rs` and
  records the exclusive-side split before falling through to the existing
  first-crossing descent route.

Why the verifier still fails:
- The old `terminal_set_fan_left_suffix_retention_bad_pivot_descent` proof is
  still compiled before the stage theorem can be accepted.
- Its right-not-left branch still uses the last `rs ∩ altRight` bad pivot.
  The prefix-side obstruction is a vertex `y ∈ rs.takeUntil z` that is
  old-left-only.  The last-bad extremality gives no control over this prefix
  vertex.

Next target:
- Replace the right-not-left branch of
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` with the
  first-wide-residual split.
- The already compiled right-only-after-`x` helper handles one subcase; the
  next missing proof is the old-left-only first-wide residual descent, plus
  any old-right-only-before-`x` prefix-control case exposed by the split.
