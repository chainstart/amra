# wowii198a right-suffix residual, round 001 iteration 4

Verifier command run from `/home/biostar/work/projects/amra/amra_library/formal`:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

Result: failed.

External sources relied on:
- None from web or literature.
- Local artifact sources read:
  `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_suffix_residual_20260628_focused_2h/wowii198a-right-suffix-prefix-residual/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-bad-pivot-descent/context_bundle.md`
  and
  `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_suffix_residual_20260628_focused_2h/wowii198a-right-suffix-prefix-residual/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-bad-pivot-descent/math_tools_report.md`.

Current first blocker:
- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, in the
  right-not-left bad pivot branch.
- The two remaining stale branches are still:
  - a prefix offender `y ∈ rs.takeUntil z` with `y ∈ oldLeft`, not old-common,
    and `y ∈ altRight.support`;
  - the non-alt fallback branch where `y ∉ oldLeft.takeUntil x`.

Lean progress:
- Added the checked helper
  `mem_left_takeUntil_of_left_not_right_and_mem_altRight`.
- It proves that a vertex surviving in
  `((oldLeft.takeUntil x).append (oldRight.dropUntil x)).toPath.support`
  and known not to lie on `oldRight.support` must have come from
  `oldLeft.takeUntil x`, not from the old-right suffix.
- This isolates the `hy_alt` branch: after deriving `y ∉ oldRight` from
  `hy_new_bad`, `hy_left`, and `y ≠ x`, the remaining gap is not support
  localization but a true descent construction for an earlier bad prefix
  vertex.

Verifier diagnostics after the edit:
- `AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean:6470:16`:
  `hpair_measure_min` has weighted-minimality type but `False` is expected.
- `AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean:6519:18`:
  same type mismatch.

Next target:
- Prove a right-suffix prefix-residual descent package.  The package must
  build a lower pair, not invoke weighted minimality directly.
- For the `hy_alt` branch, use the new support helper to reduce to
  `y ∈ oldLeft.takeUntil x`, then either use a first-bad pivot package for
  prefix bad vertices or construct the two-sided bridge descent.
- For the non-alt branch, use
  `not_mem_left_suffix_fallback_of_not_left_prefix` to make
  `rs.takeUntil y ++ oldLeft.dropUntil y` omit `x`, then prove common-card
  descent or common-card nonincrease plus strict support-length descent.
