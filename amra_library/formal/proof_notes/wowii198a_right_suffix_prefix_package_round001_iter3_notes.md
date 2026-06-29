# wowii198a right-suffix prefix package, round 001 iteration 3

Verifier command run from `/home/biostar/work/projects/amra/amra_library/formal`:

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

Current first blocker:
- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, right-not-left
  bad pivot branch.
- The two live Lean errors remain:
  - `Wowii198aLeftmost.lean:6486:16`
  - `Wowii198aLeftmost.lean:6551:18`
- Both use `hpair_measure_min` where Lean expects `False`.

Additional finite-order probe:

```text
oldLeft  = v, y, x, s
oldRight = v, w, a, x, z, t
rs       = v, w, y, a, z, s
```

This satisfies the currently tracked right-suffix prefix-bad shape:
- `x ∉ rs`;
- `w` is the first old-path intersection on `rs`;
- `z` is right-not-left and lies in the old-right suffix after `x`;
- `y ∈ rs.takeUntil z`, `y ∈ oldLeft`, and `y` is not old-common;
- the current last-bad control over `rs.dropUntil z` still sees only `z`
  among bad vertices in `rs ∩ altRight`.

Output of the probe:

```text
altRight ['v', 'y', 'x', 'z', 't']
bad rs ∩ altRight vertices ['y', 'z']
old common non-apex ['x']
bridge_left ['v', 'w', 'a', 'x', 's']
bridge_right ['v', 'y', 'a', 'z', 't']
bridge common non-apex ['a']
new bridge common outside old common ['a']
```

Interpretation:
- The previously suggested two-sided bridge
  `oldRight.takeUntil x ++ oldLeft.dropUntil x` and
  `oldLeft.takeUntil y ++ rs[y..z] ++ oldRight.dropUntil z`
  is not sufficient under the current hypotheses alone.
- The segment `rs[y..z]` may carry an old-right-only vertex before `x`
  (`a` above), creating a new bridge common vertex outside the old common set.
- The next target should therefore strengthen the extremal choice to control
  all one-sided old-path intersections on the prefix segment, or use a
  different descent pair that avoids the uncontrolled `rs[y..z]` segment.

Next target:
- Prove a broadened prefix-residual extremal lemma whose bad set includes
  old-left-only and old-right-only vertices in `rs.takeUntil z`, not only
  vertices already surviving in `altRight`.  Then use it to replace the two
  stale `hpair_measure_min` branches with a genuine lower-pair contradiction.
