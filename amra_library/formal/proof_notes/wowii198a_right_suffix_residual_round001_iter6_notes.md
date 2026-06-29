# wowii198a right-suffix residual, round 001 iteration 6

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
- The live Lean file still has two checked local setup blocks followed by stale
  `hpair_measure_min` terms where the goal is `False`.

Verifier diagnostics:
- `AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean:6486:16`:
  `hpair_measure_min` has weighted-minimality type but `False` is expected.
- `AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean:6551:18`:
  same type mismatch.

Useful facts already checked in the local branch:
- In the alt subcase, Lean has:
  `y ≠ x`, `y ∉ (pair.2 : G.Walk v t).support`, and
  `y ∈ ((pair.1 : G.Walk v s).takeUntil x hx_left).support`.
- In the fallback subcase, Lean has:
  `fallbackLeft =
    (((rs.takeUntil y hy_rs).append
      ((pair.1 : G.Walk v s).dropUntil y hy_left_walk)).toPath)` and
  `x ∉ (fallbackLeft : G.Walk v s).support`, via
  `not_mem_left_suffix_fallback_of_not_left_prefix`.

Reason direct extremality did not close:
- The current proof chooses `z` using `exists_last_bad_pivot_on_rs`.  This
  controls residual bad vertices in `rs.dropUntil z`, which is correct for the
  left-prefix branch.
- The failing right-not-left branch introduces old-left-only vertices from
  `rs.takeUntil z`.  Last-bad control gives no prefix exclusion.
- The artifact context confirms that simply replacing this with
  `exists_first_bad_pivot_on_rs` is not enough, because the local prefix vertex
  is not always known to lie in `altRight.support`; if it lies after `x` on
  old-left, it is not in the raw left prefix of `altRight`.

Next target:
- Prove a dedicated right-suffix prefix-residual descent package.  It should
  either:
  1. choose an extremal set broad enough to include the old-left-only prefix
     residuals, then use the existing
     `terminal_set_fan_left_suffix_retention_right_suffix_residual_bad_false_of_altRight`
     in the surviving-alt subcase; or
  2. abandon the current `spliceRight` containment and build a different lower
     pair from `fallbackLeft`, proving common-card descent or common-card
     nonincrease plus strict support-length descent before applying
     `hpair_measure_min`.

