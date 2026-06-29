# wowii198a right-suffix prefix package, round 001 iteration 2

Verifier command:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

Result: failed.

External sources relied on:
- None from web or literature.
- Local artifact sources read:
  `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_suffix_prefix_residual_package_20260628_focused/wowii198a-right-suffix-prefix-package/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-right-suffix-prefix-residual-bad-false/context_bundle.md`
  and
  `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_suffix_prefix_residual_package_20260628_focused/wowii198a-right-suffix-prefix-package/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-right-suffix-prefix-residual-bad-false/math_tools_report.md`.
- The prompt-relative artifact path under `formal/artifacts/...` does not exist; the actual artifact path is one project level above `formal/`.

Current first blocker:
- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, right-not-left
  bad pivot branch.
- The only Lean errors remain:
  - `Wowii198aLeftmost.lean:6486:16`
  - `Wowii198aLeftmost.lean:6551:18`
- Both sites try to close a `False` goal with
  `hpair_measure_min : ∀ pair', terminalPathPairWeightedMeasure pair ≤ ...`.

Tool check:

I reran a small ordered-support probe for the shaped obstruction:

```text
oldLeft  = v, y, x, s
oldRight = v, w, x, z, t
rs       = v, w, y, z, s
```

Output:

```text
old common ['x']
spliceRight common ['y'] ['v', 'w', 'y', 'z', 't']
fallbackLeft common with oldRight ['w', 'x'] ['v', 'w', 'y', 'x', 's']
bridge common [] ['v', 'w', 'x', 's'] ['v', 'y', 'z', 't']
```

Interpretation:
- The existing `spliceRight` containment can trade old common vertex `x` for
  prefix residual `y`, so it does not give strict common-card descent.
- The simple fallback-left route is not enough in the shaped obstruction; it
  can retain `x` or introduce earlier old-right intersections.
- The next useful Lean target is still the two-sided bridge:
  `left' = oldRight.takeUntil x ++ oldLeft.dropUntil x` and
  `right' = oldLeft.takeUntil y ++ rs[y..z] ++ oldRight.dropUntil z`.

Next target:
- Prove a bridge common-card descent lemma for the local right-not-left prefix
  residual branch, then replace both stale `hpair_measure_min` sites with that
  lower-pair contradiction.
