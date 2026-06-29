# wowii198a right-suffix residual, round 001 iteration 1

Verifier command run from `/home/biostar/work/projects/amra/amra_library/formal`:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

Result after this iteration: failed.

External sources: none used.

Context/artifact note: the prompt-required artifact directory
`artifacts/open_problem_screening/latest/wowii198a_right_suffix_residual_20260628_focused_2h/wowii198a-right-suffix-prefix-residual/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-bad-pivot-descent`
was not present relative to the Lean workspace, and `find .. -path '*round-001-terminal-set-fan-left-suffix-retention-bad-pivot-descent*' -type d`
returned no matches.

Progress:

- Added `not_isPath_append_of_not_mem_toPath_append_left`, symmetric to the existing right-side append/toPath obstruction.
- Added `exists_left_prefix_right_suffix_tail_of_not_mem_left_alt`, exposing a right-suffix tail return when a left-prefix vertex disappears from `altRight.toPath`.
- Used that helper in `terminal_set_fan_left_suffix_retention_bad_pivot_descent` to close the subcase where the local bad vertex is in `oldLeft.takeUntil x` and absent from `altRight`; this now routes through `terminal_set_cross_swap_commonCard_lt_of_later_return` and contradicts `hno_lower`.

Remaining Lean blockers:

- `Wowii198aLeftmost.lean:6448:16`: `hpair_measure_min` is still used where `False` is required in the subcase where the local prefix vertex survives in `altRight`.
- `Wowii198aLeftmost.lean:6497:18`: `hpair_measure_min` is still used where `False` is required in the fallback subcase where the local prefix vertex is not in `oldLeft.takeUntil x`.

Next target:

Prove the missing right-suffix residual false/descent lemma for those two local branches. The first branch likely needs an extremality argument that does not rely only on the current last-bad pivot. The second branch should use
`not_mem_left_suffix_fallback_of_not_left_prefix` to build the fallback-left path and then prove either a strict common-card descent or a common-card nonincrease plus strict support-length decrease.
