# wowii198a right-prefix wide residual round 001 iteration 4

Verifier command run from `/home/biostar/work/projects/amra/amra_library/formal`:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

Result: failed, with the expected two proof holes only.

Current first blocker:
- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, right-not-left
  bad pivot branch.
- The live errors are at:
  - `Wowii198aLeftmost.lean:6866:16`
  - `Wowii198aLeftmost.lean:6931:18`
- Both are still stale uses of `hpair_measure_min` where Lean expects `False`.

Lean progress this iteration:
- Added `mem_takeUntil_or_mem_dropUntil_of_mem_support`, a generic order
  dichotomy for vertices on a walk relative to a selected pivot.
- Added a second-pivot package in the local context of the failing branch:
  after an old-left-only prefix obstruction `y` and the old-right-only suffix
  pivot `z`, select the first noncommon old residual `a` on
  `rs.dropUntil y`.
- Recorded:
  - `ha_exclusive`: `a` is strictly old-left-only or strictly old-right-only.
  - `ha_right_position`: if `a` is old-right-only, then it is either before
    `x` on the old right path or in the old-right suffix after `x`.
  - `hz_tail_after_a_of_ne`: unless `a = z`, the old right suffix pivot `z`
    lies after `a` inside `rs.dropUntil y`.

Route correction:
- The two remaining holes are not local syntax or containment issues.
- The previous last-bad-pivot route is structurally insufficient for the
  right-not-left branch: the last-bad extremality controls
  `rs.dropUntil z`, but the bad obstruction lies in `rs.takeUntil z`.
- The next useful theorem should be a two-pivot or weighted-fallback bridge:
  from an old-left-only obstruction `y` before a right-only suffix pivot `z`,
  use the next residual `a` after `y` to either:
  - produce a right-path bypass around `x` between right-only pivots, or
  - prove a common-card nonincrease plus strict support-length decrease,
    contradicting `hpair_measure_min`.

Do not spend the next iteration on:
- Reworking only the `spliceRight` containment proof with the same last pivot.
- Reusing the right-only first-wide-residual helper directly; its firstness is
  global on `rs.takeUntil a`, while the available firstness here is relative to
  `rs.dropUntil y`.

Finite model sanity check:
- In the representative graph
  `oldLeft = v,y,x,s`, `oldRight = v,w,a,x,z,t`,
  `rs = v,w,y,a,z,s`, the lower pair is
  `oldLeft` together with the right bypass `v,w,a,z,t`.
- This supports the right-only-prefix/right-only-suffix bypass direction, but
  the formal theorem still needs a guard excluding extra old-left residuals in
  the `rs` segment between the two right-only pivots.
