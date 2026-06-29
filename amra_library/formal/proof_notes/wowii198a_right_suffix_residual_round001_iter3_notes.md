# wowii198a right-suffix residual, round 001 iteration 3

Verifier command run from `/home/biostar/work/projects/amra/amra_library/formal`:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

External sources: none used. The prompt-supplied local artifact context and
`math_tools_report.md` were read from:

```text
/home/biostar/work/projects/amra/artifacts/open_problem_screening/latest/wowii198a_right_suffix_residual_20260628_focused_2h/wowii198a-right-suffix-prefix-residual/lean_formalizer/round-001-terminal-set-fan-left-suffix-retention-bad-pivot-descent/
```

Selected blocker:

- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, right-not-left
  bad pivot branch.
- Local failing subcase: a prefix vertex `y` lies in `rs.takeUntil z`, lies in
  old-left, is not old common, and would be introduced into the spliced right
  path.

Tool check:

- Ran a finite sequence-order probe modeling simple old-left, old-right, and
  replacement `rs` supports with the endpoint constraint that `rs` ends at the
  same terminal as old-left while omitting `x`.
- The probe found an admissible support-order pattern:

```text
oldLeft  = v, y, x, s
oldRight = v, w, x, z, t
rs       = v, w, y, z, s
altRight = v, y, x, z, t
spliceR  = v, w, y, z, t
```

  In this pattern, the current splice-right containment does not give strict
  common-card descent: old common-card is `1` via `x`, while the spliced pair
  still has common-card `1` via `y`.
- A graph-level check on the corresponding edge set still has a different
  zero-common pair, so this is not evidence against the theorem. It is evidence
  against closing the current branch by applying weighted minimality to the
  existing `spliceRight` pair without a new descent construction.

Conclusion:

- No Lean proof change was kept this iteration. Replacing the stale
  `hpair_measure_min` lines remains invalid.
- The next useful construction is a two-sided bridge descent for the
  surviving-prefix branch. The sequence witness suggests the shape:

```text
left'  = oldRight.takeUntil x ++ oldLeft.dropUntil x
right' = oldLeft.takeUntil y ++ rs segment y..z ++ oldRight.dropUntil z
```

  with both sides loop-erased by `toPath`. This avoids merely trading `x` for
  `y` in the common set.

Remaining Lean blockers:

- `Wowii198aLeftmost.lean:6448:16`: surviving-prefix branch
  `y ∈ altRight.support`; needs the two-sided bridge descent or stronger
  first-bad control on the prefix segment.
- `Wowii198aLeftmost.lean:6497:18`: non-alt, non-left-prefix branch; the
  existing fallback-left path can omit `x`, but a common-card or weighted
  descent still needs to control new old-right intersections from the `rs`
  prefix.

Next target:

Prove a right-suffix prefix-residual bridge lemma for a left-only `y` before a
right-only bad pivot `z`, using `oldLeft.takeUntil y`, the `rs` segment from
`y` to `z`, and `oldRight.dropUntil z` for the new right path, paired with the
existing cross-swap left path at `x`.
