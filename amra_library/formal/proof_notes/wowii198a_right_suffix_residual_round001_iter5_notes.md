# wowii198a right-suffix residual, round 001 iteration 5

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

Tool checks:
- Re-ran `python3 proof_notes/wowii198a_suffix_retention_round003_countermodel_search.py`.
- Output:
  `no countermodel in shaped six-vertex search`
  and
  `no countermodel in 2000 random six-vertex graphs`.

Current first blocker:
- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, in the
  right-not-left bad pivot branch.
- The local order obstruction remains:
  `w` is the first right-only old-path hit on `rs`, then a local `y` lies in
  `rs.takeUntil z` and on old-left only, and the selected last bad pivot `z`
  lies on old-right only.

Lean progress:
- In the `hy_alt_local` branch, Lean now checks the explicit derivation that
  `y ≠ x`, `y ∉ oldRight.support`, and therefore
  `y ∈ oldLeft.takeUntil x` via
  `mem_left_takeUntil_of_left_not_right_and_mem_altRight`.
- In the non-alt/non-left-prefix branch, Lean now checks the fallback-left
  setup:
  `fallbackLeft = ((rs.takeUntil y hy_rs).append (oldLeft.dropUntil y)).toPath`
  and
  `x ∉ fallbackLeft.support`, using
  `not_mem_left_suffix_fallback_of_not_left_prefix`.

Remaining verifier diagnostics:
- `AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean:6486:16`:
  `hpair_measure_min` has weighted-minimality type but `False` is expected.
- `AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean:6551:18`:
  same type mismatch.

Next target:
- Prove the right-suffix prefix-residual descent package.
- For the alt branch, the checked local state is now the sharper target:
  `y ∈ rs.takeUntil z`, `y ∈ oldLeft.takeUntil x`, `y ∉ oldRight`, and `y`
  is a bad `altRight` vertex. This needs a first-bad-pivot or two-sided
  bridge descent, not direct weighted minimality.
- For the fallback branch, continue from the checked fact
  `x ∉ fallbackLeft.support` and prove common-card descent, or common-card
  nonincrease plus strict support-length descent, before applying weighted
  minimality.
