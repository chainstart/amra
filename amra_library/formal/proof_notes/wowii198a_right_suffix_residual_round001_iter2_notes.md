# wowii198a right-suffix residual, round 001 iteration 2

Verifier command run from `/home/biostar/work/projects/amra/amra_library/formal`:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

Result after this iteration: failed.

External sources: none used.

Context/artifact note: the prompt-required artifact files
`artifacts/open_problem_screening/latest/wowii198a_right_suffix_residual_20260628_focused_2h/wowii198a-right-suffix-prefix-residual/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-bad-pivot-descent/context_bundle.md`
and `math_tools_report.md` were not present relative to the Lean workspace.

Work performed:

- Confirmed the only live Lean diagnostics are the two stale `hpair_measure_min`
  uses in `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- Probed replacing `exists_last_bad_pivot_on_rs` by
  `exists_first_bad_pivot_on_rs`. This is not a viable global replacement:
  it removes the `hlast_bad` control needed by the left-suffix residual branch
  and does not by itself close the right-suffix residual branch.
- Restored the last-pivot selection. The net Lean blocker is unchanged.

Remaining Lean blockers:

- `Wowii198aLeftmost.lean:6448:16`: the local right-suffix prefix offender
  survives in `altRight`; last-pivot control does not rule out an earlier bad
  vertex in `rs.takeUntil z`.
- `Wowii198aLeftmost.lean:6497:18`: the local offender is not in `altRight`
  and is not in `oldLeft.takeUntil x`; the intended
  `not_mem_left_suffix_fallback_of_not_left_prefix` fallback still needs a
  proved common-card or weighted-measure descent.

Next target:

Add a right-suffix residual descent lemma that combines first-side control for
bad vertices before `z` with last-side control for bad vertices after `z`, or
prove an induction on the number of bad `rs ∩ altRight` vertices so the
surviving-prefix case can recurse to a smaller bad set.
