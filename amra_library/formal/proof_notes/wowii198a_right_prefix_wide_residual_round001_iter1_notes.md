# wowii198a right-prefix wide residual round 001 iteration 1

Verifier command run from `/home/biostar/work/projects/amra/amra_library/formal`:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

External sources relied on:
- None from web or literature.
- Local artifact sources read:
  `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_prefix_wide_residual_20260628_focused/wowii198a-right-prefix-wide-residual/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-right-prefix-wide-residual-descent/context_bundle.md`
  and
  `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_prefix_wide_residual_20260628_focused/wowii198a-right-prefix-wide-residual/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-right-prefix-wide-residual-descent/math_tools_report.md`.

Current first blocker:
- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, right-not-left bad pivot branch.
- The two live Lean errors are at `Wowii198aLeftmost.lean:6582:16` and `Wowii198aLeftmost.lean:6647:18`.
- Both use `hpair_measure_min` where Lean expects `False`.

Finite-order probe run this iteration:

```text
oldLeft  = v, y, x, s
oldRight = v, w, a, x, z, t
rs       = v, w, y, a, z, s
```

Edges were the undirected union of the three displayed walks. Exhaustive simple-path enumeration found 24 `v-s` paths and 20 `v-t` paths. The old pair has one non-apex common vertex `{x}`. The minimum non-apex common-card over all path pairs is 0, witnessed by:

```text
left  = v, y, x, s
right = v, w, a, z, t
```

This does not falsify the wide-residual theorem, but it confirms the descent is not the stale right-prefix splice at the last `altRight` bad pivot. The first wide residual is `y`; later residuals such as `a` and `z` are not first-wide-residual choices.
