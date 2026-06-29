# wowii198a right-suffix prefix package, round 001 iteration 1

Verifier command:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

Current first blocker:

- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, right-not-left
  bad pivot branch.
- The two stale local lines are still the prefix residual subcases where the
  goal is `False` but the term is only weighted minimality:
  `hpair_measure_min : ∀ pair', terminalPathPairWeightedMeasure pair ≤ ...`.

Required context read:

- `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_suffix_prefix_residual_package_20260628_focused/wowii198a-right-suffix-prefix-package/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-right-suffix-prefix-residual-bad-false/context_bundle.md`
- `/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_suffix_prefix_residual_package_20260628_focused/wowii198a-right-suffix-prefix-package/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-right-suffix-prefix-residual-bad-false/math_tools_report.md`

External web/literature sources:

- None.

Tool check:

I ran a Python support-order sanity check for the known obstruction pattern:

```text
oldLeft  = v, y, x, s
oldRight = v, w, x, z, t
rs       = v, w, y, z, s
```

Output:

```text
old common: ['x']
spliceR: ['v', 'w', 'y', 'z', 't'] common with oldLeft: ['y']
leftBridge: ['v', 'w', 'x', 's']
rightBridge: ['v', 'y', 'z', 't']
bridge common: []
```

Interpretation:

- The current `spliceRight = rs.takeUntil z ++ oldRight.dropUntil z` can merely
  replace old common vertex `x` by the prefix residual vertex `y`; it does not
  prove strict common-card descent by itself.
- The two-sided bridge suggested by the prior notes remains the right next
  target:

```text
left'  = oldRight.takeUntil x ++ oldLeft.dropUntil x
right' = oldLeft.takeUntil y ++ rs[y..z] ++ oldRight.dropUntil z
```

Lean status:

- No Lean theorem/proof edit was kept in this iteration; the missing proof is a
  genuine descent construction, not a local simplification.
- The exact next Lean target is a checked bridge lemma proving common-card
  descent (or common-card nonincrease plus strict support-length descent) for
  the two-sided replacement above.
