# two target round 001: WOWII198a and WOWII16

Verifier commands run from `/home/biostar/work/projects/amra/amra_library/formal`:

```bash
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean
```

Current result:
- `WOWII198a`: still fails with exactly the two expected stale
  `hpair_measure_min` holes in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- `WOWII16`: passes Lean with only existing unnecessary-`simpa` linter
  warnings.

## WOWII198a target

The active obstruction is the right-not-left branch of the last bad pivot
argument.  The pivot `z` is old-right-only and lies in the old right suffix
after `x`; the splice

```lean
rs.takeUntil z ++ oldRight.dropUntil z
```

removes `x`, but `rs.takeUntil z` can contain an old-left-only obstruction
`y`, which creates a new common vertex against the unchanged old left path.

The next theorem to prove is a double-pivot bridge:

- assume `y` is old-left-only and occurs before the right-only suffix pivot
  `z` on `rs`;
- choose the next noncommon old residual `a` after `y`;
- prove either a strict common-card descent by a cross-swap/right-bypass, or a
  common-card nonincrease plus strict support-length decrease contradicting
  `hpair_measure_min`.

New Lean support added this round:

```lean
private lemma mem_support_toPath_append_three_subset
private lemma mem_support_toPath_right_bypass_subset
private lemma not_mem_right_bypass_of_takeUntil_dropUntil_around
private lemma terminal_set_fan_right_bypass_commonCard_lt_of_segment_left_guard
private lemma exists_segment_left_only_of_not_segment_left_guard
private lemma mem_support_toPath_left_rs_right_bridge_subset
private lemma not_mem_left_rs_right_bridge_of_prefix_suffix
```

These decompose support membership of a `toPath` built from three appended
segments, and prove that the candidate bypass avoids `x` when its first pivot is
before `x` on the old right path and its last pivot is after `x`.  They are
intended for right-bypass candidates of the form

```lean
oldRight.takeUntil a ++ rs_segment(a,z) ++ oldRight.dropUntil z
```

The guarded descent lemma now proves strict common-card decrease once every old
left vertex in the middle `rs[a,z]` segment is already old-right.  Therefore the
remaining missing ingredient is not the bypass construction; it is the prefix
extremal/guard theorem excluding additional old-left-only vertices in that
middle segment, or replacing the route with a two-sided bridge that avoids such
vertices.

Round update:
- The guard-failure case is now explicitly extractable as an old-left-only
  witness in the middle segment.
- The first two-sided bridge tools are checked:
  `left.takeUntil y ++ rs[y,z] ++ right.dropUntil z` has a clean support
  decomposition, and omits `x` when `y` is before `x` on the old left path and
  `z` is after `x` on the old right path.
- Inside the live branch, the right-prefix-entry plus segment-guard case now has
  a local contradiction package `hright_prefix_guard_false`; the remaining work
  is to prove the guard or route the extracted guard-failure witness through a
  two-sided common-card descent.

The important route correction is that the existing last-bad-pivot extremality
controls `rs.dropUntil z`, but the live obstruction lies in `rs.takeUntil z`.
Purely iterating the current local containment proof will not solve the branch.

Round update, next 4h attack:
- Added and checked a guarded two-sided bridge descent:
  `terminal_set_fan_two_sided_bridge_commonCard_lt_of_middle_guard`.
  It packages the common-card decrease for
  `oldRight.takeUntil x ++ oldLeft.dropUntil x` paired with
  `oldLeft.takeUntil y ++ rs[y,z] ++ oldRight.dropUntil z`, provided the
  middle segment creates no non-old-common intersection with the swapped left
  path.
- Added checked order tools:
  `not_mem_cross_swap_left_of_left_prefix_not_right`,
  `not_mem_dropUntil_of_after_on_isPath`, and
  `two_sided_middle_guard_of_first_noncommon_not_swap`.
  These isolate the exact obstruction: if the first noncommon old residual
  after `y` is not itself on the swapped left path, then the middle guard
  follows from firstness.
- In the live `hy_alt_local` branch, the subcase where the selected residual
  `a` is old-right-only and lies in the old-right suffix after `x` now closes
  by the two-sided bridge.  The subcase where `a` is old-right-only, lies before
  `x`, and satisfies the segment left-guard also closes by the existing
  right-bypass descent.
- The first stale `hpair_measure_min` now represents only the hard complement:
  either `a` is left-only/on the left side, or `a` is old-right-prefix with a
  left-guard failure in `rs[a,z]`.  This is a real mathematical obstruction,
  not a missing support-decomposition lemma.
- The second stale `hpair_measure_min` remains the not-alt/not-left-prefix
  fallback-left branch.  It likely needs an analogous first-residual/fallback
  guard statement; direct common-card containment can be spoiled by old-right
  prefix vertices such as `w`.

Next concrete Lean target:
- Prove a guard-failure descent for the old-right-prefix `a` case: from a
  left-only witness in `rs[a,z]`, either derive a two-sided bridge with a later
  left pivot, or prove a fallback pair with common-card nonincrease and strict
  support-length decrease.
- In parallel, formulate the symmetric fallback-left guard for the second
  stale branch.  Do not attempt the naive two-sided bridge without explicitly
  controlling the first noncommon residual on the middle segment.

## WOWII16 target

Do not pursue the unrestricted fixed-color safe-pool refinement.  The file now
contains C6 refutations showing that route is false.

The next useful target is the exact compatible selector:

```lean
central_deficit_exists_diametral_safe_candidate_data_disjoint_selector
```

or a compatibility-restricted refinement/dichotomy strong enough to imply

```lean
centralDeficitExistsDiametralSafeCandidateDataDisjoint
```

The relevant existing positive endpoint is the C6-compatible witness theorem
near the end of `Wowii16CentralCore.lean`, while the unrestricted variants are
documented as refuted.

## Round update, current 4h attack

Verifier results:
- `WOWII198a` still fails, but the active failure set has been reduced and
  sharpened to three stale `hpair_measure_min` placeholders in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`:
  1. `a` is old-left-only and lies in the old-left prefix before `x`;
  2. in the old-right-prefix guard-failure branch, the first extracted
     old-left-only witness `b` lies in the old-left prefix before `x`;
  3. the non-alt/non-left-prefix fallback-left branch remains open.
- `WOWII16` passes Lean with only the existing unnecessary-`simpa` warnings.

Lean progress:
- Fixed the malformed `by_cases` branch around the left-bypass guard, replacing
  the fragile `exact match ...` structure with a normal `rcases` proof.
- Added checked left-bypass tools:
  `not_mem_left_bypass_of_prefix_suffix` and
  `terminal_set_fan_left_bypass_commonCard_lt_of_segment_right_guard`.
  These prove strict common-card descent for
  `oldLeft.takeUntil y ++ rs[y,a] ++ oldLeft.dropUntil a` when `y` is before
  `x` on oldLeft, `a` is after `x` on oldLeft, and the middle segment has no
  new old-right-only intersections.
- Used that tool in the live proof to close the old-left-only / old-left-suffix
  residual case.
- Closed the left-bypass guard-failure right-suffix witness `c` case by proving
  a segment-left guard from the firstness of `b`, then invoking the existing
  `terminal_set_fan_right_bypass_commonCard_lt_of_segment_left_guard`.

Route assessment:
- The remaining `a` and `b` prefix cases do not delete `x` under the available
  bridge candidates, so they are not local containment failures.  They require
  a real first-bad/extremal core for the right-only retained-suffix branch, or a
  weighted fallback theorem that can exploit support-length decrease without a
  strict common-card drop.
- The next target should be a right-only retained-suffix first-bad core, using
  `exists_first_bad_pivot_on_rs` before entering the right-only branch, instead
  of trying to squeeze prefix information from the current last-bad pivot.

## Round update, first-bad support package

Verifier result:
- `WOWII198a` still fails at exactly three stale `hpair_measure_min` sites,
  now shifted to lines 8180, 8276, and 8523 in
  `Wowii198aLeftmost.lean`.

New checked Lean support:
- `mem_takeUntil_of_mem_dropUntil_ne_on_isPath`
- `mem_takeUntil_of_mem_dropUntil_takeUntil_ne_on_isPath`
- `not_mem_altRight_of_first_bad_right_only_prefix_left_only`
- `not_mem_altRight_of_first_bad_right_only_before_pivot_left_only`
- `terminal_set_fan_first_bad_right_only_fallback_left_alt_commonCard_lt`

Meaning:
- If a right-only bad pivot `z` is chosen by `exists_first_bad_pivot_on_rs`,
  then any old-left-only vertex before `z` on `rs` cannot also lie on
  `altRight`.  This directly kills the `hy_alt_local` prefix obstruction that
  currently produces the `a` and `b` prefix branches under the last-bad proof.
- The non-alt/non-left-prefix fallback is now packaged: under the same
  first-bad right-only hypothesis, the pair
  `rs.takeUntil y ++ oldLeft.dropUntil y` versus
  `oldLeft.takeUntil x ++ oldRight.dropUntil x` has strictly smaller
  common-cardinality.

Next integration target:
- Refactor the right-only retained-suffix part of
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` so that this
  branch uses a first-bad pivot (or an auxiliary first-bad core) instead of the
  current last-bad pivot.  Once `hfirst_bad` is available in that branch, the
  three remaining stale placeholders should be replaced by:
  1. immediate contradiction via
     `not_mem_altRight_of_first_bad_right_only_prefix_left_only` for the
     `hy_alt_local` path, eliminating both `a` and `b` prefix subcases;
  2. `terminal_set_fan_first_bad_right_only_fallback_left_alt_commonCard_lt`
     for the non-alt/non-left-prefix fallback-left branch.

## Round update, filtered-residual selector integration

Lean progress:
- Added `two_sided_middle_guard_of_first_noncommon_not_left_prefix_not_swap`.
  This is the existing two-sided middle guard with the firstness hypothesis
  restricted to non-left-prefix residuals.  The proof shows any swap-path
  counterexample that is not already old-common is automatically outside
  `oldLeft.takeUntil x`.
- Added `exists_first_noncommon_old_residual_not_left_prefix_on_rs_dropUntil`.
  It selects the first noncommon old residual after `y` among vertices that are
  not in `oldLeft.takeUntil x`.
- Integrated this selector into
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.  The selected
  residual `a` now carries `ha_not_left_prefix`, and all later firstness calls
  pass the extra non-left-prefix proof.

Verifier result:
- `WOWII198a` now fails at exactly two stale placeholders instead of three:
  1. the old-right-prefix guard-failure witness `b` may still lie in
     `oldLeft.takeUntil x`;
  2. the non-alt/non-left-prefix fallback-left branch remains open.
- The previous `a` old-left-prefix branch is closed by
  `False.elim (ha_not_left_prefix ha_prefix_x)`.

Strategic assessment:
- The filtered selector route is validated and should remain part of the
  final proof.  It removes harmless old-left-prefix residuals from the main
  pivot choice without weakening the already-closed right-suffix and
  left-suffix branches.
- The remaining `b` prefix case is not the same problem: right-bypass removes
  old common `x` but can add `b` as a new common vertex, so strict common-card
  descent is not immediate.  A weighted proof would need a real support-length
  decrease theorem for the bypass path, which is not currently available.
- The fallback-left branch matches the shape of
  `terminal_set_fan_first_bad_right_only_fallback_left_alt_commonCard_lt`, but
  the live branch is still driven by a last-bad pivot.  This confirms the next
  structural target: introduce a first-bad/right-only core for the retained
  suffix branch, or prove a local first-bad property strong enough to reuse the
  fallback theorem.

## Round update, first-bad/right-only splice core

Lean progress:
- Added `terminal_set_fan_first_bad_right_only_splice_commonCard_lt`.
  This proves the retained-suffix right-only splice descent under the correct
  first-bad hypothesis:
  `spliceRight = rs.takeUntil z ++ oldRight.dropUntil z`, where `z` is
  old-right-only, lies in `oldRight.dropUntil x`, and is the first bad
  `rs ∩ altRight` vertex.
- The proof body uses the two intended escape routes for old-left-only
  prefix-side obstructions:
  1. if the obstruction is in `altRight`, first-bad extremality forces it to be
     `z`, contradicting `z ∉ oldLeft`;
  2. if it is not in `altRight`, the existing later-return cross-swap or
     `terminal_set_fan_first_bad_right_only_fallback_left_alt_commonCard_lt`
     gives a lower common-card pair, contradicting weighted minimality inside
     the containment proof.
- Updated `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent`
  so it first selects `exists_first_bad_pivot_on_rs`; when that pivot is
  right-only, it now routes directly to the new splice core. The left-only
  first-bad case still delegates to the old bad-pivot theorem.

Verifier result:
- `WOWII198a` still fails at exactly the two old placeholders inside
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`. No new Lean
  errors were introduced by the first-bad/right-only core.

Next target:
- Move the same first-bad split into
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` itself, before it
  selects the last bad pivot. The right-only first-bad branch can now be closed
  by the checked splice core. The remaining left-only first-bad branch needs a
  symmetric bridge/last-bad handoff, rather than continuing through the stale
  arbitrary last-bad right-only proof.

## Round update, first-bad-left / last-bad-right bridge handoff

Lean progress:
- Moved the first-bad split into
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
  The first-bad right-only branch now exits through
  `terminal_set_fan_first_bad_right_only_splice_commonCard_lt`; the remaining
  proof state is therefore the intended first-bad-left / last-bad-right case.
- Added `first_bad_left_prefix_package`, proving that a left-side first bad
  pivot is old-left-only, lies in `oldLeft.takeUntil x`, and is after the
  original first crossing `w`.
- Added `later_bad_after_first_bad_on_isPath`, giving the ordering
  `z ∈ rs.dropUntil zFirst` and `zFirst ∈ rs.takeUntil z` for the later
  last-bad right-only pivot.
- Instantiated
  `terminal_set_fan_two_sided_bridge_commonCard_lt_of_middle_guard` at
  `y = zFirst` and `z = lastBad`. This typechecks: if the global middle guard
  holds, weighted minimality is contradicted immediately. Therefore the live
  branch now carries the negation of exactly the right global bridge guard.
- Added the checked order utility
  `mem_dropUntil_takeUntil_of_mem_dropUntil_of_mem_takeUntil_on_isPath`, for
  converting `a <= b <= z` on a simple walk into membership in
  `(dropUntil a).takeUntil z`.

Verifier result:
- `WOWII198a` fails at exactly two genuine proof holes:
  1. after a right-prefix guard failure, the first left-only witness `b` may
     still lie in `oldLeft.takeUntil x`;
  2. the non-alt / non-left-prefix fallback-left branch still has only
     `x ∉ fallbackLeft`, not the required common-card descent.
- No mechanical errors or warnings remain from the first-bad handoff and
  global bridge instantiation.

Strategic assessment:
- The route is now correctly aimed at the main theorem: first-bad-left plus
  last-bad-right reduces to a global two-sided bridge guard, and the positive
  guard case is closed.
- The old local splice proof is no longer the right driver for the negative
  guard case. The remaining work should introduce a selector for the first
  global bridge-guard counterexample in
  `(rs.dropUntil zFirst).takeUntil z`, then split that witness by membership
  in `oldRight.takeUntil x` versus `oldLeft.dropUntil x`.
- The `b ∈ oldLeft.takeUntil x` subcase should not be patched locally: the
  usual bypass path preserves `x` and may add `b` as a new common vertex, so
  strict common-card descent is not available from the current construction.

Next target:
- Replace the remaining old `y/a/b` local search inside the last-bad-right
  branch with a global bridge-failure selector:
  first choose a non-common witness in
  `swapLeft ∩ ((rs.dropUntil zFirst).takeUntil z)`, then handle the
  right-prefix witness by right-bypass and the left-suffix witness by
  left-bypass/fallback. This is the next structural theorem needed for
  `WOWII198a`.

## Round update, checked global bridge-failure selector

Lean progress:
- Added `exists_first_bridge_guard_counterexample`.
  From failure of the global bridge guard it selects the first non-common
  witness in
  `swapLeft ∩ ((rs.dropUntil zFirst).takeUntil z)`, with a firstness property
  on that middle segment.
- Added `bridge_guard_counterexample_side`.
  Any such non-common witness in `swapLeft` is classified as exactly one of:
  old-right-only in `oldRight.takeUntil x`, or old-left-only in
  `oldLeft.dropUntil x`.
- Wired the selector into the live first-bad-left / last-bad-right branch.
  The branch now has a concrete `qBridge`, its middle-segment membership,
  its non-common firstness, and its side classification.
- Derived the strict ordering facts for `qBridge` in the live branch:
  `qBridge` is after `zFirst`, before `z`, not equal to either endpoint, and
  lies in `rs.takeUntil z`.

Verifier result:
- `WOWII198a` still fails at the same two old placeholders, now shifted by the
  new checked code. The selector and all `qBridge` ordering facts typecheck.

Strategic assessment:
- The negative global bridge case is now formalized enough to be the next
  driver. The old local `y/a/b` splice search should not be extended further;
  it is solving a different, weaker selection problem and reintroduces the
  `b ∈ oldLeft.takeUntil x` obstruction.
- The next proof step is to create a stage theorem with `qBridge` as the
  primary pivot. Its two top branches should be the classifier output:
  right-prefix-only `qBridge` handled by a right-bypass guard, and
  left-suffix-only `qBridge` handled by a left-bypass/fallback guard.

## Round update, qBridge-stage positive guards and next-witness selectors

Lean progress:
- Added `terminal_set_fan_bridge_right_prefix_stage_commonCard_lt`.
  If `qBridge` is old-right-only in `oldRight.takeUntil x` and the segment
  from `qBridge` to the last bad right-suffix pivot `z` has the expected
  left-guard, then the existing right-bypass construction gives strict
  common-card descent.
- Added `terminal_set_fan_bridge_left_suffix_stage_commonCard_lt`.
  If `qBridge` is old-left-only in `oldLeft.dropUntil x` and the segment from
  `zFirst` to `qBridge` has the expected right-guard, then the existing
  left-bypass construction gives strict common-card descent.
- Added the symmetric selector
  `exists_first_segment_right_only_of_not_segment_right_guard`, dual to the
  existing first left-only selector.
- In the live first-bad-left / last-bad-right branch, derived
  `hqBridge_stage_witness`: after splitting on `qBridge_side`, either
  the right-prefix stage produces a first left-only witness between
  `qBridge` and `z`, or the left-suffix stage produces a first right-only
  witness between `zFirst` and `qBridge`.

Verifier result:
- `WOWII198a` still fails only at the two old stale `hpair_measure_min`
  placeholders in the legacy `y/a/b` proof body. The new qBridge-stage
  wrappers, symmetric selector, and `hqBridge_stage_witness` all typecheck.

Strategic assessment:
- The qBridge route is now formalized through the next-witness selection
  point. The remaining work is no longer to invent the selector; it is to
  replace the old spliceRight common-subset proof body with a case split on
  `hqBridge_stage_witness`.
- A tempting shortcut in the left-suffix side would be to claim any
  right-prefix witness before `qBridge` is a global bridge-guard
  counterexample. That is not currently justified: membership in
  `oldRight.takeUntil x` does not automatically imply survival in
  `swapLeft.toPath`. The next theorem must either prove that survival lemma
  under right-only hypotheses or handle the bypass deletion as a separate
  descent.

## Round update, qBridge-stage obstruction compression

Lean progress:
- Added
  `terminal_set_fan_right_prefix_stage_left_suffix_witness_commonCard_lt`.
  This closes the right-prefix `qBridge` stage whenever its first left-only
  witness lies in `oldLeft.dropUntil x`; the proof uses the existing
  left-bypass-alt guard, and if that guard fails, a right-bypass descent.
- Added common-card symmetry and the symmetric cross-swap later-return wrapper:
  `terminalPathPairCommonCard_swap` and
  `terminal_set_cross_swap_commonCard_lt_of_later_left_return`.
- Added
  `terminal_set_fan_left_suffix_stage_right_suffix_witness_commonCard_lt` and
  `terminal_set_fan_left_suffix_stage_right_prefix_witness_commonCard_lt`.
  Together these eliminate the entire left-suffix `qBridge` stage under
  `hno_lower`: right-suffix witnesses give a two-sided bridge descent, while
  right-prefix witnesses either violate `hfirst_bridge_bad` by surviving in
  `swapLeft`, or give the symmetric cross-swap descent when deleted by
  `toPath`.
- Added
  `terminal_set_cross_swap_commonCard_lt_of_left_prefix_absent_altRight`, then
  derived the live local conclusions
  `hqBridge_right_prefix_front_obstruction` and
  `hqBridge_right_prefix_front_alt_obstruction`.

Current compressed obstruction:
- In the live first-bad-left / last-bad-right branch, all qBridge-stage cases
  now reduce to one front-front configuration:
  `qBridge` is old-right-only in `oldRight.takeUntil x`; the first left-only
  witness `b` between `qBridge` and `z` is in `oldLeft.takeUntil x`; and `b`
  also survives in `altRight.toPath`.
- If that `b` were absent from `altRight`, the new cross-swap wrapper would
  already contradict `hno_lower`.

Verifier result:
- `WOWII198a` still fails only at the two old stale `hpair_measure_min`
  placeholders in the legacy `y/a/b` proof body. The new obstruction
  compression lemmas and live local conclusions all typecheck.

Next target:
- Stop extending the legacy local `y/a/b` search. Replace the `spliceRight`
  prefix-common-subset proof with the compressed qBridge front-front
  obstruction.
- The next missing mathematical lemma should target the surviving front-front
  obstruction directly: from a right-prefix-only `qBridge` and a first
  left-prefix-only `b` that survives in `altRight`, prove either a strict
  common-card descent or a finite extremal contradiction with the choice of
  `z` as last bad / `qBridge` as first bridge bad.

## Round update, front-front successor extraction

Lean progress:
- Added the live local package `hqBridge_front_alt_order_package`.
  It refines the compressed front-front obstruction with explicit order facts:
  the witness `b` is in `rs`, lies strictly after `qBridge` and before `z`,
  satisfies `qBridge ∈ rs.takeUntil b`, and remains left-prefix-only while
  surviving in `altRight`.
- Added `hqBridge_front_next_bridge_package`.
  Using `b` as the new left endpoint, the two-sided bridge guard on the
  segment `b..z` cannot hold, because
  `terminal_set_fan_two_sided_bridge_commonCard_lt_of_middle_guard` would
  contradict `hno_lower`. Therefore a first new bridge counterexample
  `qNext` exists on `b..z`.
- Added `hqBridge_front_next_bridge_side_package`.
  It proves `b ∉ swapLeft`, hence `qNext ≠ b`, and classifies `qNext` by
  `bridge_guard_counterexample_side`.
- Added `hqBridge_front_next_stage_witness`.
  If `qNext` is right-prefix-only, the chain has advanced to a later
  right-prefix witness. If `qNext` is left-suffix-only, the positive
  left-bypass guard on `b..qNext` would give strict descent, so a first
  right-only witness is selected on that smaller segment.

Verifier result:
- `WOWII198a` still fails only at the two old legacy `hpair_measure_min`
  placeholders. The new successor-extraction and next-stage witness packages
  typecheck.

Strategic assessment:
- The remaining obstruction is now an explicitly advancing alternating chain
  along `rs`: right-prefix `qBridge`, left-prefix `b`, then either a later
  right-prefix bridge counterexample or a right-only witness produced before a
  left-suffix bridge counterexample.
- The next useful theorem should package this as a finite-progress/extremal
  contradiction: every unresolved front-front state produces a strictly later
  unresolved state before `z`, while `z` is the last bad pivot.

## Round update, qNext left-suffix eliminated

Lean progress:
- Added the live local package `hqBridge_front_next_right_prefix_package`.
  It strengthens the previous `qNext` stage: the left-suffix case for
  `qNext` is now impossible under `hno_lower`.
- The proof uses the first right-only witness produced on `b..qNext`.
  If that witness is in `oldRight.takeUntil x`, then
  `terminal_set_fan_left_suffix_stage_right_prefix_witness_commonCard_lt`
  gives a strict common-card descent. If it is in `oldRight.dropUntil x`, then
  `terminal_set_fan_left_suffix_stage_right_suffix_witness_commonCard_lt`
  gives the descent. Both contradict weighted minimality.

Verifier result:
- `WOWII198a` still fails only at the two old legacy `hpair_measure_min`
  placeholders. The new right-prefix-only successor package typechecks.
- `WOWII16` passes, with only the existing unnecessary-`simpa` warnings.

Strategic assessment:
- The surviving front-front obstruction has been tightened further:
  any unresolved right-prefix/front state now produces a strictly later
  right-prefix-only bridge counterexample. The left-suffix escape has been
  closed.
- The next formal target is to lift this local package into a reusable
  successor lemma for an arbitrary right-prefix/front state, then choose the
  last such state on `rs.takeUntil z`. The successor will contradict maximality.

## Round update, prefix-extremal closure

Lean progress:
- Replaced the old `spliceRight` prefix-common-subset search inside
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` with a genuine
  prefix-extremal argument.
- Defined the local finite set `S` of right-prefix/front bridge
  counterexamples on `rs.takeUntil z`.
- Proved a local successor principle:
  every `q ∈ S` has a strictly later `qNext ∈ S` in `rs.dropUntil q`.
  The proof reuses the two-sided bridge guard, the first left-only witness,
  the cross-swap absent-alt descent, and the left-suffix elimination package.
- Applied `exists_last_mem_support_forall_mem_dropUntil_imp_eq` to choose the
  last element of `S`; the successor gives a later element of `S`, contradicting
  maximality.
- This removes both stale `hpair_measure_min` placeholders from the legacy
  proof body.

Verifier result:
- `WOWII198a` now passes with `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.
- The temporary proof-check probes were removed, so the file verifies without
  proof debug output.

Next target:
- Poll/confirm the parallel WOWII16 verification.
- If committing, include the proof notes with the Lean change. The mathematical
  next cleanup would be to extract the local successor principle into a named
  private lemma, but it is no longer blocking the main theorem.

## Round update, two-fan wrapper restart

Lean progress:
- Re-opened the frozen `terminal_set_fan_splice_descent_left_of_hsep`
  wrapper long enough to verify that the only active failure is still the old
  strict common-card descent placeholder for the explicit `spliceRight` pair.
- Added checked symmetry infrastructure:
  `terminalPathPairSupportLength_swap`,
  `terminalPathPairWeightedMeasure_swap`, and
  `terminal_set_fan_right_first_crossing_uncrossing_commonCard_lt`.
- The new right-side theorem derives the mirrored first-crossing uncrossing
  statement by swapping the path pair, applying
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, then
  swapping the resulting pair back through
  `terminalPathPairCommonCard_swap`.

Verifier result:
- `WOWII198a` still passes with `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Remaining blocker:
- The full arbitrary-intersection left splice wrapper cannot yet be reactivated.
  The active checked theorem needs a crossing `w` that is both
  right-path-only and first among the old left/right support union on `rs`.
  The wrapper currently starts from an arbitrary new right-path intersection;
  if an earlier old-left/common support vertex occurs on `rs`, the old
  `spliceRight` containment proof is not valid. The next target is the bridge:
  either promote the arbitrary right intersection to a right-only union-first
  crossing, or prove that the earlier left/common first hit gives a separate
  weighted-minimality descent.

## Round update, refined two-fan residual

Lean progress:
- Added the checked union-first entry points
  `terminal_set_fan_splice_descent_left_of_hsep_of_union_first_right` and
  `terminal_set_fan_splice_descent_right_of_hsep_of_union_first_left`.
  These turn a first hit of the old-support union on the opposite old path
  into the existing first-crossing uncrossing descent.
- Added left/right arbitrary-splice reductions:
  `terminal_set_fan_splice_descent_left_reduction_of_not_direct` and
  `terminal_set_fan_splice_descent_right_reduction_of_not_direct`.
  If direct replacement does not lower common-cardinality, then either the
  union-first hit is on the opposite old path and already descends, or it is
  on the replaced old path and leaves a precise residual.
- Closed the prefix half of that residual with
  `terminal_set_fan_union_first_left_prefix_commonCard_lt` and its right-side
  mirror `terminal_set_fan_union_first_right_prefix_commonCard_lt`.
  If the old common vertex `x` lies before the union-first hit `w` on the old
  replaced path, replacing the corresponding prefix removes `x` and gives
  strict common-card descent.
- Added refined wrappers
  `terminal_set_fan_splice_descent_left_reduction_or_left_after`,
  `terminal_set_fan_splice_descent_right_reduction_or_right_after`, and the
  `..._of_hsep_or_union_first_..._residual` wrappers.  The surviving residual
  now states that `x` is not in `oldPath.takeUntil w`.
- Added position-normalization lemmas
  `terminal_set_fan_left_after_residual_w_prefix_x` and
  `terminal_set_fan_right_after_residual_w_prefix_x`, so the residual can be
  read positively as: the union-first hit `w` lies on the old replaced path
  before the old common vertex `x`, and a later replacement-path vertex is
  opposite-path-only.

Verifier result:
- `WOWII198a` passes with `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Current true blocker:
- The full two-fan splice wrapper is no longer blocked by arbitrary witness
  selection or by the case `x ∈ oldPath.takeUntil w`.  The remaining case is
  narrower and structural:
  `rs` first meets the old-support union at a vertex `w` on the replaced old
  path before `x`; later it meets the opposite old path at a vertex that is
  not on the replaced old path.  The next target is a cross-splice descent for
  exactly this ordered configuration, or a proof that weighted minimality plus
  the singleton-avoidance separator rules it out.

## Round update, finite wrapper reduced to bridge obstruction

Lean progress:
- Added residual predicates
  `terminalSetFanLeftOrderedSpliceResidual` and
  `terminalSetFanRightOrderedSpliceResidual`.
- Added the active finite-wrapper stage theorem
  `terminal_set_two_fan_or_ordered_splice_residual_of_no_small_endpoint_separator`.
  It proves that the finite two-fan/min-cut package now reduces to either an
  actual two-fan or one of the refined ordered splice residuals for a
  weighted-minimal terminal path pair.
- Added cross-splice guard theorems
  `terminal_set_fan_left_ordered_residual_bridge_commonCard_lt` and
  `terminal_set_fan_right_ordered_residual_bridge_commonCard_lt`.
  These feed the ordered residual directly into the existing two-sided bridge
  machinery: if the later opposite-only vertex lies after `x` on the opposite
  old path and the bridge middle guard holds, strict common-card descent
  follows.
- Added reduction theorems
  `terminal_set_fan_splice_descent_left_reduction_or_bridge_obstruction` and
  `terminal_set_fan_splice_descent_right_reduction_or_bridge_obstruction`.
  Thus the remaining ordered residual is split into two explicit obstructions:
  the later opposite-only vertex is not in the opposite old suffix after `x`,
  or the bridge middle guard fails.

Verifier result:
- `WOWII198a` passes with `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Next target:
- Attack the two bridge obstructions.  The guard-failure branch should produce
  a first bridge counterexample using the existing
  `exists_first_bridge_guard_counterexample`/successor machinery.  The
  suffix-failure branch should be converted into the symmetric prefix case on
  the opposite old path, or ruled out by a cross-swap descent.

## Round update, bridge obstruction split

Lean progress:
- Added the checked finite-wrapper theorem
  `terminal_set_two_fan_or_bridge_prefix_obstruction_of_no_small_endpoint_separator`.
  The no-small-endpoint-separator package now yields either an actual two-fan
  or a weighted-minimal terminal pair carrying a left/right
  `terminalSetFan...BridgePrefixObstruction`.
- Split that prefix obstruction into explicit front and first-guard cases:
  `terminalSetFanLeftBridgeFrontObstruction`,
  `terminalSetFanRightBridgeFrontObstruction`,
  `terminalSetFanLeftBridgeFirstGuardObstruction`, and
  `terminalSetFanRightBridgeFirstGuardObstruction`.
- Added the checked conversion lemmas
  `terminalSetFanLeftBridgePrefixObstruction.to_front_or_first_guard` and
  `terminalSetFanRightBridgePrefixObstruction.to_front_or_first_guard`.
  The guard-failure branch is no longer a raw negated universal: it now carries
  the first bad bridge vertex produced by
  `exists_first_bridge_guard_counterexample`, plus its old-path side
  decomposition from `bridge_guard_counterexample_side`.
- Strengthened the guard branch so it retains the necessary opposite-suffix
  fact for the terminal vertex `y`.  This was essential: the later bridge
  stage lemmas need `y` on the suffix side, and the weaker prefix-obstruction
  packaging would have lost that information.
- Added the checked finite-wrapper refinement
  `terminal_set_two_fan_or_bridge_front_or_first_guard_obstruction_of_no_small_endpoint_separator`.
- Added the checked local descent
  `terminal_set_fan_left_first_guard_left_suffix_commonCard_lt`: in the left
  first-guard case, if the first bad bridge vertex `q` lies on the old left
  suffix after `x`, then the existing bridge stage machinery already gives a
  strict common-card descent.

Verifier result:
- `WOWII198a` passes cleanly with `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Current true blocker:
- The final two-fan theorem is still not restored.  The remaining obstruction
  is now strictly narrower: for a weighted-minimal pair, one must eliminate
  either the opposite-prefix/front case (`y` lies before `x` on the opposite
  old path) or the explicit first-guard-bad vertex case.  On the left side,
  the `q`-on-left-suffix alternative of the first-guard case is now eliminated;
  the corresponding live branch is `q` on the old right prefix.  The next
  useful attack is to prove the symmetric right-side suffix elimination and
  then target the remaining front/right-prefix configurations with a
  cross-swap/front-pivot descent.

## Round update, first-guard suffix branches removed

Lean progress:
- Added the checked symmetric descent
  `terminal_set_fan_right_first_guard_right_suffix_commonCard_lt` by swapping
  the path pair and applying
  `terminal_set_fan_left_first_guard_left_suffix_commonCard_lt`.
- Added reduced first-guard obstruction predicates:
  `terminalSetFanLeftBridgeFirstGuardRightPrefixObstruction` and
  `terminalSetFanRightBridgeFirstGuardLeftPrefixObstruction`.
  These retain only the first-guard side alternatives not yet eliminated by
  strict common-card descent.
- Added weighted-minimality conversion lemmas
  `terminalSetFanLeftBridgeFirstGuardObstruction.to_right_prefix_of_weighted_min`
  and
  `terminalSetFanRightBridgeFirstGuardObstruction.to_left_prefix_of_weighted_min`.
  The eliminated suffix side would create a lower common-card path pair, which
  contradicts `terminalPathPairWeightedMeasure` minimality.
- Added the checked finite-wrapper refinement
  `terminal_set_two_fan_or_bridge_front_or_reduced_first_guard_obstruction_of_no_small_endpoint_separator`.
  The finite no-small-endpoint-separator package now reduces to an actual
  two-fan or one of four explicit remaining obstructions: left/right front, or
  left/right reduced first-guard prefix.

Verifier result:
- `WOWII198a` passes cleanly with `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Current true blocker:
- The full `terminal_set_two_fan_of_no_small_endpoint_separator` chain is still
  not restored.  The remaining nontrivial cases are now front/prefix cases:
  `y` is before `x` on the opposite old path, or the first guard-bad vertex is
  before `x` on the opposite old path.  The next target should be a
  front-pivot/cross-swap descent that handles those prefix configurations
  directly, rather than expanding the already-closed suffix branches.

## Round update, reduced first-guard branches removed

Lean progress:
- Added the checked finite-wrapper refinement
  `terminal_set_two_fan_or_bridge_front_obstruction_of_no_small_endpoint_separator`.
  It combines the previous
  `...front_or_reduced_first_guard_obstruction...` theorem with the strict
  common-card descents for the two reduced first-guard prefix branches.
- Added the checked common-card contradiction wrappers
  `terminalSetFanLeftBridgeFirstGuardRightPrefixObstruction.commonCard_lt`
  and
  `terminalSetFanRightBridgeFirstGuardLeftPrefixObstruction.commonCard_lt`.
  The underlying left proof is
  `terminal_set_fan_left_reduced_first_guard_right_prefix_commonCard_lt`.
  Its key finite argument is a successor construction inside the finite set of
  right-prefix bad vertices before the suffix endpoint `y`; weighted
  minimality forbids the produced strict common-card descent.
- Added checked prefix-core extraction lemmas
  `terminalSetFanLeftBridgeFrontObstruction.to_prefix_core` and
  `terminalSetFanRightBridgeFrontObstruction.to_prefix_core`.
  These make the remaining obstruction explicit: on the left side, `w` lies
  on the old left path before `x`, `y` lies on the old right path before `x`,
  `rs` avoids `x`, and the bridge segment from `w` to `y` is protected by the
  union-first condition.  The right side is the symmetric statement.
- Added first-front normal forms
  `terminalSetFanLeftBridgeFrontFirstObstruction`,
  `terminalSetFanRightBridgeFrontFirstObstruction`, and checked conversions
  `.to_first` from the raw front obstructions.  The front vertex `y` can now
  be chosen as the first opposite-prefix-only vertex on the replacement tail
  after `w`, so future front-pivot work can use a genuine firstness
  hypothesis rather than an arbitrary `y`.
- Added the checked wrapper
  `terminal_set_two_fan_or_bridge_front_first_obstruction_of_no_small_endpoint_separator`.
  The finite package now reduces directly to an actual two-fan or a left/right
  first-front obstruction.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Current true blocker:
- The active finite theorem now reduces to:
  actual two-fan, or a weighted-minimal pair with a left/right pure
  `terminalSetFan...BridgeFrontFirstObstruction`.
- This is a different shape from the suffix and first-guard cases already
  solved.  It is a double-prefix bridge: left front is `oldLeft`-prefix
  `w < x`, `rs[w,y]`, and `oldRight`-prefix `y < x`.  The available
  two-sided bridge lemmas require a suffix endpoint after `x`, so another
  local iteration of those lemmas is unlikely to solve it.
- Next target: prove a front-pivot/cross-swap descent for the double-prefix
  bridge in the first-front normal form, probably using either common-card
  nonincrease plus strict support length decrease, or a modified minimality
  choice that selects the first common vertex `x` rather than an arbitrary
  common vertex from the finite intersection.

## Round update, global-first front split

Lean progress:
- Added the checked global-first normal forms
  `terminalSetFanLeftBridgeFrontGlobalFirstObstruction` and
  `terminalSetFanRightBridgeFrontGlobalFirstObstruction`, with conversions
  from the first-front normal forms.  The opposite-prefix-only front vertex
  `y` is now first on the whole replacement prefix up to `y`, not merely first
  after the old-side vertex `w`.
- Added the checked finite wrapper
  `terminal_set_two_fan_or_bridge_front_global_first_obstruction_of_no_small_endpoint_separator`.
  The active finite package now reduces to an actual two-fan or one of the
  two global-first front obstructions.
- Added the support-order helper
  `eq_of_mem_takeUntil_of_mem_dropUntil_on_isPath`, used to collapse a vertex
  that lies on both sides of a `takeUntil`/`dropUntil` split of a simple path.
- Added the checked post-front-return splitters
  `terminalSetFanLeftBridgeFrontGlobalFirstObstruction.post_left_prefix_return_dichotomy`
  and
  `terminalSetFanRightBridgeFrontGlobalFirstObstruction.post_right_prefix_return_dichotomy`.
  These isolate the next real front obstruction: after `y`, either there is no
  prefix-only return to the original same-side prefix, or there is a first such
  return point on the replacement path.
- Added the checked middle-front splitters
  `terminalSetFanLeftBridgeFrontGlobalFirstObstruction.middle_left_prefix_return_dichotomy`
  and
  `terminalSetFanRightBridgeFrontGlobalFirstObstruction.middle_right_prefix_return_dichotomy`.
  These cover the previously unisolated gap inside the bridge interval
  `w..y`: even before post-`y` returns, a same-side prefix-only point between
  `w` and `y` can be a new common point for the natural front reroute.  The
  new split either rules out such a point or chooses the first one.
- Added the checked clean-branch support facts
  `no_left_prefix_only_except_front_of_no_middle_no_post` and
  `no_right_prefix_only_except_front_of_no_middle_no_post`, plus the direct
  commonness corollaries
  `left_prefix_mem_rs_ne_front_is_common_of_no_middle_no_post` and
  `right_prefix_mem_rt_ne_front_is_common_of_no_middle_no_post`.  These prove
  that once both middle and post-`y` same-side prefix-only returns are ruled
  out, any same-side old-prefix point of the replacement path is either the
  front point `w` or already an old common point.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Current true blocker:
- The full `terminal_set_two_fan_of_no_small_endpoint_separator` chain is
  still not restored.
- The no-return front reroute candidate should next prove a common-card
  nonincrease statement only after both middle and post-`y` same-side
  prefix-only returns are excluded.  Without the middle split, the candidate
  can still introduce a new prefix-only common point before `y`.
- The new clean-branch support facts should be used in that common-card
  nonincrease proof to account for all same-side old-prefix intersections:
  only `w` is a possible inserted non-old-common point from this source.
- The two return branches should next be attacked by successor/last-element
  arguments: one on the finite set of middle `w..y` prefix-only returns, and
  one on the finite set of post-`y` prefix-only returns, analogous to the
  earlier right-prefix front successor argument used in the reduced
  first-guard proof.

## Round update, clean front count boundary

Lean progress:
- Added checked prefix-half containment lemmas
  `left_clean_altRight_left_prefix_common_or_front` and
  `right_clean_altLeft_right_prefix_common_or_front`.  These package the
  previous clean-branch facts in the exact form needed by the natural front
  reroutes: on the left side, an `rs` point hitting
  `oldLeft.takeUntil x` is either the front point `w` or an old common point;
  the right side is symmetric.
- Added checked conditional common-card nonincrease lemmas
  `terminal_set_fan_left_front_clean_alt_commonCard_le_of_no_right_suffix_only`
  and
  `terminal_set_fan_right_front_clean_alt_commonCard_le_of_no_left_suffix_only`.
  After middle and post same-side prefix-only returns are excluded, the front
  reroute has `commonCard <=` the old pair provided there is no new
  opposite-suffix-only hit (`oldRight.dropUntil x` for the left case, and
  `oldLeft.dropUntil x` for the right case).  The only allowed new point in
  the count is the front point `w`, while the old common point `x` is erased.
- Added checked first-return selectors
  `first_right_suffix_only_on_rs_or_none` and
  `first_left_suffix_only_on_rt_or_none`.  These split the remaining clean
  branch into the above no-suffix-only case or a first opposite-suffix-only
  return on the replacement path.
- Added checked tail-location lemmas
  `left_front_right_suffix_only_mem_tail` and
  `right_front_left_suffix_only_mem_tail`.  A suffix-only return cannot occur
  before the front point `w`; the union-first property would force it to equal
  `w`, contradicting its opposite-only condition.  Thus the next bridge can
  legitimately use the segment from `w` to the first suffix-only return.
- Added checked guarded suffix-return descents
  `terminal_set_fan_left_front_suffix_return_commonCard_lt_of_middle_guard`
  and
  `terminal_set_fan_right_front_suffix_return_commonCard_lt_of_middle_guard`.
  These show that a first opposite-suffix-only return immediately yields a
  strict common-card descent if the `w..z` bridge segment has no non-old-common
  intersection with the cross-swap path.
- Added checked guard/counterexample splitters
  `terminal_set_fan_left_front_suffix_return_guard_or_first_counterexample`
  and
  `terminal_set_fan_right_front_suffix_return_guard_or_first_counterexample`.
  Failure of the bridge guard now produces the first non-old-common point on
  `w..z`, together with its side: opposite-prefix-only or same-side-suffix-only.
- Added checked post-front location facts
  `left_front_right_prefix_counterexample_ne_front_mem_post` and
  `right_front_left_prefix_counterexample_ne_front_mem_post`.  If a guard
  counterexample is opposite-prefix-only and not equal to the original front
  point `y`, it lies after `y`; future work can handle it as a post-front
  return rather than reopening the clean middle segment.
- Added checked `q = y` front-counterexample splitters
  `terminal_set_fan_left_front_at_front_counterexample_guard_or_first_left_suffix`
  and
  `terminal_set_fan_right_front_at_front_counterexample_guard_or_first_right_suffix`.
  These first prove that the opposite-suffix return `z` is after the original
  front point `y`.  Then they close the branch by a right/left bypass if the
  segment `y..z` has no same-side-only intersections; otherwise they extract
  the first same-side suffix-only witness on that segment.
- Added checked same-side witness side splitters
  `terminal_set_fan_left_front_same_side_witness_suffix_or_prefix_obstruction`
  and
  `terminal_set_fan_right_front_same_side_witness_suffix_or_prefix_obstruction`.
  If the extracted same-side-only witness lies in the old same-side suffix
  after `x`, the existing suffix-stage descent closes it; otherwise the
  witness is packaged as a same-side prefix-only obstruction.
- Added checked combined `q = y` wrappers
  `terminal_set_fan_left_front_at_front_counterexample_descent_or_prefix_obstruction`
  and
  `terminal_set_fan_right_front_at_front_counterexample_descent_or_prefix_obstruction`.
  The whole `q = y` branch now returns either a strict common-card descent or a
  first same-side prefix-only obstruction on the segment after `y`.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Current true blocker:
- Same-side prefix-only returns are no longer the clean-branch blocker; they
  are isolated and counted.
- The real remaining front obstruction is now sharper: an opposite-suffix-only
  return, e.g. left front has some first `z` on `rs` with
  `z ∈ oldRight.dropUntil x` and `z ∉ oldLeft`.
- The next proof target should use this first suffix-only return to build a
  strict descent.  The plausible route is a two-sided bridge from the front
  point `w` to this suffix point `z`, with a finite guard/successor argument
  for any bridge counterexample lying in `oldLeft.dropUntil x`.
- After the guarded descent wrapper, the next unresolved branch is narrower:
  the first `w..z` guard counterexample is either the original opposite-prefix
  front point `y`, a later post-`y` opposite-prefix-only return, or a
  same-side-suffix-only point.  The next round should attack these by a
  successor/firstness argument on the finite counterexample set, mirroring the
  earlier reduced first-guard proof.
- With the combined `q = y` wrapper, the same-side suffix-after-`x` subcase is
  closed.  The remaining hard cases are now a first same-side prefix-only
  obstruction after `y`, or a later post-`y` opposite-prefix-only return.  Both
  have firstness data and should be routed through a successor/guard-failure
  descent rather than by raw containment.

## Round update, front suffix residual theorem layer

Lean progress:
- Repaired the active `WOWII198a` file after a local indentation regression and
  reconfirmed that the full two-fan wrapper declarations remain inside a frozen
  block comment.  The active theorem frontier is still the front/global-first
  obstruction line, not the full theorem.
- Added the checked right mirror
  `terminal_set_fan_right_front_suffix_return_descent_or_post_prefix_or_same_prefix`.
  Together with the left lemma, the first opposite-suffix return is now
  decomposed symmetrically.
- Added checked residual wrappers
  `terminalSetFanLeftBridgeFrontSuffixResidual` and
  `terminalSetFanRightBridgeFrontSuffixResidual`.
- Added checked reductions
  `terminalSetFanLeftBridgeFrontGlobalFirstObstruction.descent_or_suffix_residual`
  and
  `terminalSetFanRightBridgeFrontGlobalFirstObstruction.descent_or_suffix_residual`.
- Added the active theorem-layer reduction
  `terminal_set_two_fan_or_bridge_front_suffix_residual_of_no_small_endpoint_separator`.
  It upgrades the live theorem from "fan or front/global-first obstruction" to
  "fan or front suffix residual", using weighted minimality to rule out the
  strict common-card descent branch.
- Added reusable finite-set counting bridges
  `card_lt_of_subset_insert_erase_mem_of_inserted_mem`,
  `common_support_erase_card_lt_of_subset_insert_erase_common_of_inserted_common`,
  and
  `terminalPathPairCommonCard_lt_of_subset_insert_erase_common_of_inserted_common`.
  These are for the clean branch where the inserted front point is already an
  old common point.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The route is still viable, but the previous "no opposite-suffix return"
  branch cannot be closed from `commonCard <=` alone.  If the front point `w`
  is already an old common point, the new counting bridge should upgrade this
  to strict `commonCard <`.  If `w` is old same-side-only, equality can occur:
  the new pair deletes old common `x` and inserts `w`.
- Therefore the next proof target should split the clean no-suffix residual by
  whether `w` is already common.  Close the common-`w` branch with the new
  strict insert/erase counting lemma.  Treat the same-side-only `w` branch as
  the genuine extremal obstruction; it likely needs either a strengthened
  measure/leftmost choice or a successor argument showing that such an equal
  replacement cannot persist.

## Round update, common-front clean branch

Lean progress:
- Activated the honest left/right splice wrappers
  `terminal_set_fan_splice_descent_left_of_hsep_or_bridge_prefix_obstruction`
  and
  `terminal_set_fan_splice_descent_right_of_hsep_or_bridge_prefix_obstruction`.
  These restore the splice layer up to the bridge-prefix obstruction, without
  pretending that the arbitrary-intersection splice wrapper is done.
- Added the finite theorem-layer residual wrapper
  `finite_two_fan_to_pair_or_bridge_front_suffix_residual_of_terminal_set_no_small_endpoint_separator`.
  The live finite chain now reaches the same honest front-suffix residual as the
  terminal-set theorem layer.
- Added strict clean-branch lemmas
  `terminal_set_fan_left_front_clean_alt_commonCard_lt_of_no_right_suffix_only_of_front_common`
  and
  `terminal_set_fan_right_front_clean_alt_commonCard_lt_of_no_left_suffix_only_of_front_common`.
  They upgrade the old clean `<=` result to strict `<` when the inserted front
  point `w` is already an old common point.
- Added unbundled left post/middle prefix-return dichotomies and the combined
  `terminal_set_fan_left_no_right_suffix_common_front_descent_or_left_prefix_obstruction`.
  Its right mirror,
  `terminal_set_fan_right_no_left_suffix_common_front_descent_or_right_prefix_obstruction`,
  is proved by swapping the pair.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The clean no-suffix branch is now split correctly.  If `w` is common and there
  is no same-side prefix return in the middle or post segment, the branch gives
  a strict common-card descent.  Therefore a minimal counterexample can only keep
  this branch by exposing a same-side prefix obstruction, or by making `w`
  same-side-only.
- The active main theorem is still not complete.  The full
  `terminal_set_two_fan_of_no_small_endpoint_separator` and finite full wrapper
  remain frozen in the block comment.  The live chain reaches
  `terminal_set_two_fan_or_bridge_front_suffix_residual_of_no_small_endpoint_separator`
  and its finite residual wrapper.
- Next target: replace the broad front-suffix residual by a sharper residual
  that records the new split explicitly: no-suffix with same-side-only `w`,
  post same-side prefix obstruction, middle same-side prefix obstruction, or the
  existing opposite post/suffix residual branches.  After that, attack the
  same-side-only `w` case with a leftmost or successor argument.

## Round update, theorem-layer sharp suffix residual

Lean progress:
- Added checked sharp residuals
  `terminalSetFanLeftBridgeFrontSharpSuffixResidual` and
  `terminalSetFanRightBridgeFrontSharpSuffixResidual`.
  These refine the broad front-suffix residual by replacing the old no-suffix
  branch with an explicit split:
  same-side-only front point `w`, post same-side prefix obstruction, middle
  same-side prefix obstruction, or one of the existing opposite post/suffix
  residual branches.
- Proved the checked conversions
  `terminalSetFanLeftBridgeFrontSuffixResidual.to_sharp_of_weighted_min` and
  `terminalSetFanRightBridgeFrontSuffixResidual.to_sharp_of_weighted_min`.
  The proof uses weighted minimality to eliminate the strict descent produced by
  the common-front clean branch.
- Added the active theorem-layer wrapper
  `terminal_set_two_fan_or_bridge_front_sharp_suffix_residual_of_no_small_endpoint_separator`
  and the finite wrapper
  `finite_two_fan_to_pair_or_bridge_front_sharp_suffix_residual_of_terminal_set_no_small_endpoint_separator`.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The current active theorem frontier is sharper than the previous broad
  front-suffix residual.  The no-suffix/common-front clean escape is no longer
  hidden inside the residual; it has been discharged into strict descent under
  minimality.
- The full theorem is still not restored.  The remaining genuine branches are:
  same-side-only `w`, post same-side prefix obstruction, middle same-side prefix
  obstruction, opposite post-prefix residual, and opposite suffix/same-prefix
  residual.
- Next target: attack the same-side-only `w` branch first.  It is the equality
  case left by the strict insert/erase argument and likely needs a leftmost
  choice or successor argument showing that replacing old common `x` by
  same-side-only `w` cannot persist in a minimal counterexample.

## Round update, clean same-side suffix residual

Lean progress:
- Added checked local splitters
  `terminal_set_fan_left_same_side_no_right_suffix_clean_or_left_prefix_obstruction`
  and
  `terminal_set_fan_right_same_side_no_left_suffix_clean_or_right_prefix_obstruction`.
  They split the same-side-only/no-suffix branch into either a genuinely clean
  equality branch, a post same-side prefix obstruction, or a middle same-side
  prefix obstruction.
- Added checked clean residuals
  `terminalSetFanLeftBridgeFrontCleanSuffixResidual` and
  `terminalSetFanRightBridgeFrontCleanSuffixResidual`, with branch helpers
  `terminalSetFanLeftBridgeFrontCleanSuffixBranch` and
  `terminalSetFanRightBridgeFrontCleanSuffixBranch`.
- Proved checked conversions
  `terminalSetFanLeftBridgeFrontSharpSuffixResidual.to_clean` and
  `terminalSetFanRightBridgeFrontSharpSuffixResidual.to_clean`.
- Added the active theorem-layer wrapper
  `terminal_set_two_fan_or_bridge_front_clean_suffix_residual_of_no_small_endpoint_separator`
  and the finite wrapper
  `finite_two_fan_to_pair_or_bridge_front_clean_suffix_residual_of_terminal_set_no_small_endpoint_separator`.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The same-side-only residual is now normalized.  It no longer hides middle or
  post same-side prefix obstructions inside the first branch.
- The true equality branch is now:
  `w` is same-side-only, there is no opposite suffix-only return on the
  replacement path, and there are no same-side prefix-only returns either in the
  middle segment `w..y` or after `y`.
- Next target: attack this clean equality branch directly.  The plausible route
  is a support-length/leftmost argument: the common-card replacement can only be
  equality by replacing old common `x` with same-side-only `w`; the proof should
  now show that this violates weighted minimality or can be advanced to a later
  same-side clean witness, contradicting maximality.

## Round update, length-guarded clean equality branch

Lean progress:
- Added checked support-length nondecrease lemmas
  `terminal_set_fan_left_front_clean_alt_supportLength_ge_of_weighted_min` and
  `terminal_set_fan_right_front_clean_alt_supportLength_ge_of_weighted_min`.
  They say that in the fully clean no-suffix branch, the splice replacement
  cannot have smaller support length under weighted minimality, because the
  clean common-card estimate is already `<=`.
- Added checked length-guarded residuals
  `terminalSetFanLeftBridgeFrontLengthGuardedCleanSuffixResidual` and
  `terminalSetFanRightBridgeFrontLengthGuardedCleanSuffixResidual`.
  These preserve the clean residual data and additionally record the support
  length lower bound for the only branch where equality can still hide.
- Proved checked conversions
  `terminalSetFanLeftBridgeFrontCleanSuffixResidual.to_length_guarded_of_weighted_min`
  and
  `terminalSetFanRightBridgeFrontCleanSuffixResidual.to_length_guarded_of_weighted_min`.
- Added theorem-layer wrappers
  `terminal_set_two_fan_or_bridge_front_length_guarded_clean_suffix_residual_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_bridge_front_length_guarded_clean_suffix_residual_of_terminal_set_no_small_endpoint_separator`.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The active frontier is now sharper: any remaining fully clean equality branch
  must be common-card nonincreasing and support-length nondecreasing.  Therefore
  the next proof cannot merely show that the replacement is no worse; it must
  prove an actual support-length decrease, or derive a new later clean witness
  and close it by a leftmost/maximality principle.
- The full `terminal_set_two_fan_of_no_small_endpoint_separator` and finite full
  wrapper remain frozen in the block comment.  The live chain currently reaches
  the length-guarded clean residual wrapper, not the final two-fan theorem.
- Next target: formalize the support accounting for the clean equality branch.
  The promising claim is that, with no opposite suffix-only return and no
  same-side prefix-only return in the middle or post segment, the replacement
  path's support is contained in old support with old common `x` removed and
  same-side-only `w` inserted; if this containment is strict on support length,
  weighted minimality closes the branch.

## Round update, support-length accounting scaffold

Lean progress:
- Added generic support-length/cardinality bridges:
  `walk_support_length_le_of_toFinset_subset`,
  `walk_support_length_le_of_toFinset_subset_insert_erase_mem`,
  `walk_support_length_lt_of_toFinset_subset_erase_mem`, and
  `walk_support_length_lt_of_toFinset_subset_insert_erase_inserted_mem`.
  These turn Finset containment statements for path supports into `support.length`
  inequalities.
- Added pair-level support-length bridges:
  `terminalPathPairSupportLength_le_of_component_toFinset_subset`,
  `terminalPathPairSupportLength_lt_of_left_erase_right_subset`,
  `terminalPathPairSupportLength_lt_of_left_insert_erase_inserted_right_subset`,
  `terminalPathPairSupportLength_lt_of_left_subset_right_erase`, and
  `terminalPathPairSupportLength_lt_of_left_subset_right_insert_erase_inserted`.
- Added checked left/right omission lemmas
  `terminal_set_fan_left_front_clean_altRight_omits_right_prefix_only` and
  `terminal_set_fan_right_front_clean_altLeft_omits_left_prefix_only`.
  They isolate the fact that the prefix-only opposite point `y` is genuinely
  removed from the swapped path.
- Added checked prefix-cover support estimates
  `terminal_set_fan_left_front_altRight_supportLength_le_of_left_prefix_common_or_front`
  and
  `terminal_set_fan_right_front_altLeft_supportLength_le_of_right_prefix_common_or_front`.
  These prove that the swapped path is no longer than the old opposite path
  provided every imported old-prefix vertex is either the front point `w` or is
  already on the old opposite path.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The support-length route is now more precise but also exposes a real missing
  hypothesis.  The current clean residual controls vertices that lie on both
  `rs` and the swapped path; it does not control arbitrary vertices imported
  from `(pair.1).takeUntil x` into `altRight` (or symmetrically from
  `(pair.2).takeUntil x` into `altLeft`).  Those imported prefix vertices are
  exactly what the new prefix-cover lemmas require.
- Therefore the current attack can solve the branch only after one of two
  additional moves:
  1. add a genuine selection/minimality principle implying the needed prefix
     cover, or
  2. split the residual again and record prefix-cover failure as a new explicit
     obstruction, then prove that obstruction descends by a separate splice.
- Next target: do not keep iterating inside the already-clean residual.  First
  decide which global choice is available in the theorem layer.  If no
  leftmost/prefix-minimal choice is present, introduce a new prefix-cover-failure
  residual and route the proof through that obstruction explicitly.

## Round update, prefix-cover split frontier

Lean progress:
- Confirmed from the active theorem layer that `pair` is selected only by
  `terminalPathPairWeightedMeasure`; there is no current prefix/leftmost
  minimality principle for the imported prefix vertices, and no shortest choice
  for the separator path `rs`/`rt`.
- Added checked split predicates
  `terminalSetFanLeftBridgeFrontPrefixCoverSplit` and
  `terminalSetFanRightBridgeFrontPrefixCoverSplit`.  Each records either the
  needed prefix-cover condition or an explicit imported prefix-only witness.
- Added checked residuals
  `terminalSetFanLeftBridgeFrontPrefixSplitLengthGuardedCleanSuffixResidual`
  and
  `terminalSetFanRightBridgeFrontPrefixSplitLengthGuardedCleanSuffixResidual`.
  These keep all length-guarded clean residual data and add the prefix-cover
  split at the actual witness `w`.
- Proved checked conversions
  `terminalSetFanLeftBridgeFrontLengthGuardedCleanSuffixResidual.to_prefix_split`
  and
  `terminalSetFanRightBridgeFrontLengthGuardedCleanSuffixResidual.to_prefix_split`.
- Added theorem-layer and finite wrappers:
  `terminal_set_two_fan_or_bridge_front_prefix_split_length_guarded_clean_suffix_residual_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_bridge_front_prefix_split_length_guarded_clean_suffix_residual_of_terminal_set_no_small_endpoint_separator`.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The active frontier now explicitly distinguishes the two cases inside the
  clean equality branch:
  1. prefix-cover holds, so the newly added support estimate can be applied to
     the swapped path; the remaining missing comparison is then about the
     replacement separator path `rs`/`rt` versus the old same-side path.
  2. prefix-cover fails, giving an explicit old-prefix, same-side-only witness
     not on the opposite old path.  This is now a named obstruction, not a
     hidden informal gap.
- Since the theorem layer currently has no prefix-minimal or shortest
  separator-path choice, the next honest target is to attack the prefix-cover
  failure obstruction as a separate splice/uncrossing case, or to intentionally
  strengthen the theorem-layer choice with an additional lexicographic
  minimization and then rethread the wrappers.

## Round update, prefix-cover length consequence

Lean progress:
- Added checked consequences for the prefix-cover branch:
  `terminal_set_fan_left_front_clean_prefix_cover_rs_supportLength_ge_of_weighted_min`
  and
  `terminal_set_fan_right_front_clean_prefix_cover_rt_supportLength_ge_of_weighted_min`.
  In the fully clean branch, if prefix-cover holds, then weighted minimality
  plus the swapped-path support estimate imply that the replacement separator
  path is at least as long as the old same-side path:
  `(pair.1).support.length <= rs.support.length` on the left and
  `(pair.2).support.length <= rt.support.length` on the right.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The prefix-cover case no longer fails because of the swapped path: that part
  is controlled.  The remaining obstruction is now specifically that `rs` or
  `rt` may be as long as, or longer than, the old same-side path.  Without a
  shortest separator-path choice, this cannot be contradicted by the current
  theorem-layer minimality.
- The live fork is therefore:
  1. prefix-cover fails: attack the explicit imported-prefix-only obstruction;
  2. prefix-cover holds: add a shortest/lexicographic separator-path choice, or
     derive a separate structural contradiction forcing `rs/rt` to be shorter.

## Round update, cover-length guarded prefix-split frontier

Lean progress:
- Added residual wrappers
  `terminalSetFanLeftBridgeFrontCoverLengthGuardedPrefixSplitResidual` and
  `terminalSetFanRightBridgeFrontCoverLengthGuardedPrefixSplitResidual`.
  They keep the prefix-split residual and add a universal guard: whenever the
  clean no-suffix branch and prefix-cover hypotheses hold, the separator path
  length lower bound follows.
- Proved checked conversions
  `terminalSetFanLeftBridgeFrontPrefixSplitLengthGuardedCleanSuffixResidual.to_cover_length_guarded_of_weighted_min`
  and
  `terminalSetFanRightBridgeFrontPrefixSplitLengthGuardedCleanSuffixResidual.to_cover_length_guarded_of_weighted_min`.
- Added theorem-layer and finite wrappers:
  `terminal_set_two_fan_or_bridge_front_cover_length_guarded_prefix_split_residual_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_bridge_front_cover_length_guarded_prefix_split_residual_of_terminal_set_no_small_endpoint_separator`.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The theorem frontier now carries the cover-branch length consequence directly,
  instead of leaving it as an external lemma.  The remaining cover branch is
  precisely: prefix-cover holds, all clean no-suffix conditions hold, and yet
  the separator path is not shorter than the original same-side path.
- This confirms the next serious proof choice.  Either strengthen the initial
  selection to choose shortest separator replacements, or attack the explicit
  prefix-cover-failure witness first; the current weighted pair minimality alone
  is not enough to close the cover-length branch.

## Round update, first-prefix-absent obstruction

Lean progress:
- Added first-witness normalizations for the prefix-cover split:
  `terminalSetFanLeftBridgeFrontPrefixCoverSplit.to_first` and
  `terminalSetFanRightBridgeFrontPrefixCoverSplit.to_first`.  If prefix-cover
  fails, the witness can now be chosen first along the corresponding old
  prefix, not merely as an arbitrary imported prefix-only point.
- Added checked sufficient-cover lemmas:
  `left_clean_prefix_cover_of_left_prefix_subset_rs` and
  `right_clean_prefix_cover_of_right_prefix_subset_rt`.  In the clean branch,
  if the old prefix is contained in the replacement path support, then the
  needed prefix-cover follows from the existing clean/front machinery.
- Added checked obstruction splits:
  `left_clean_prefix_cover_or_first_prefix_absent_of_no_middle_no_post` and
  `right_clean_prefix_cover_or_first_prefix_absent_of_no_middle_no_post`.
  These prove that, under the clean no-middle/no-post hypotheses, failure of
  prefix-cover forces a first prefix-only witness that is also absent from the
  replacement path `rs`/`rt`.
- Lifted the result into the theorem frontier with residual guards:
  `terminalSetFanLeftBridgeFrontCoverLengthAbsentGuardedPrefixSplitResidual`,
  `terminalSetFanRightBridgeFrontCoverLengthAbsentGuardedPrefixSplitResidual`,
  and the wrappers
  `terminal_set_two_fan_or_bridge_front_cover_length_absent_guarded_prefix_split_residual_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_bridge_front_cover_length_absent_guarded_prefix_split_residual_of_terminal_set_no_small_endpoint_separator`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The active theorem frontier now confirms that the existing first-guard/front
  machinery is already strong enough for prefix-only witnesses that lie on the
  replacement path.  Therefore the remaining prefix-cover failure is sharper
  than before: the bad witness is an old-prefix same-side-only point that the
  replacement path completely misses.
- That obstruction cannot be removed by the current local `rs`/`rt` first-guard
  lemmas, because those lemmas require membership in the replacement path.
  The next useful target is therefore one of:
  1. prove a new rerouting/descent using the replacement-absent prefix witness;
  2. strengthen the theorem-layer choice so separator replacements are selected
     to minimize this absent-prefix defect;
  3. add a shortest/lexicographic separator-path choice, which would also be
     needed for the separate cover-length branch.

## Round update, exchange-guarded prefix obstruction

Lean progress:
- Added weighted-minimal exchange splits
  `left_clean_prefix_cover_or_first_prefix_exchange_of_weighted_min` and
  `right_clean_prefix_cover_or_first_prefix_exchange_of_weighted_min`.
  They refine the previous absent-alt obstruction: if prefix-cover fails, the
  first bad same-side prefix point is absent from the replacement path but
  retained by the swapped path, while the current opposite-prefix crossing `y`
  is omitted by that same swapped path.
- Added residual guards
  `terminalSetFanLeftBridgeFrontPrefixExchangeGuard` and
  `terminalSetFanRightBridgeFrontPrefixExchangeGuard`, plus the guarded
  residual wrappers
  `terminalSetFanLeftBridgeFrontCoverLengthExchangeGuardedPrefixSplitResidual`
  and
  `terminalSetFanRightBridgeFrontCoverLengthExchangeGuardedPrefixSplitResidual`.
- Lifted the theorem frontier and finite wrapper to:
  `terminal_set_two_fan_or_bridge_front_cover_length_exchange_guarded_prefix_split_residual_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_bridge_front_cover_length_exchange_guarded_prefix_split_residual_of_terminal_set_no_small_endpoint_separator`.
- Added clean-branch support-length tradeoff lemmas
  `terminal_set_fan_left_front_clean_rs_supportLength_ge_or_altRight_supportLength_lt_of_weighted_min`
  and
  `terminal_set_fan_right_front_clean_rt_supportLength_ge_or_altLeft_supportLength_lt_of_weighted_min`.
  These state that if the replacement path does not satisfy the desired length
  lower bound, then the swapped path must strictly inflate on the opposite side.
- Lifted that tradeoff into the theorem frontier via
  `terminalSetFanLeftBridgeFrontCleanLengthTradeoffGuard`,
  `terminalSetFanRightBridgeFrontCleanLengthTradeoffGuard`,
  `terminalSetFanLeftBridgeFrontCoverLengthExchangeTradeoffGuardedPrefixSplitResidual`,
  `terminalSetFanRightBridgeFrontCoverLengthExchangeTradeoffGuardedPrefixSplitResidual`,
  and the theorem/finite wrappers
  `terminal_set_two_fan_or_bridge_front_cover_length_exchange_tradeoff_guarded_prefix_split_residual_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_bridge_front_cover_length_exchange_tradeoff_guarded_prefix_split_residual_of_terminal_set_no_small_endpoint_separator`.
- Added no-inflation closure lemmas
  `terminal_set_fan_left_front_clean_rs_supportLength_ge_of_altRight_no_inflation`
  and
  `terminal_set_fan_right_front_clean_rt_supportLength_ge_of_altLeft_no_inflation`.
  These make the next needed choice principle explicit: if the swapped path can
  be shown not to inflate, then the replacement path length lower bound follows
  without needing prefix-cover directly.
- Added the sharper local trichotomy
  `left_clean_prefix_cover_or_length_or_exchange_alt_inflation_of_weighted_min`
  and
  `right_clean_prefix_cover_or_length_or_exchange_alt_inflation_of_weighted_min`.
  In a clean branch, either prefix-cover holds, the replacement path is already
  long enough, or there is a concrete exchange witness and strict
  `altRight`/`altLeft` support inflation.
- Added the final length-failure compression
  `left_clean_length_failure_exchange_alt_inflation_of_weighted_min`
  and
  `right_clean_length_failure_exchange_alt_inflation_of_weighted_min`.
  If the desired replacement length lower bound fails, prefix-cover is
  impossible and the only remaining case is the explicit exchange+inflation
  witness.
- Lifted that final compression into theorem-level residuals:
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard`,
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard`,
  `terminalSetFanLeftBridgeFrontCoverLengthFailureExchangeInflationGuardedPrefixSplitResidual`,
  `terminalSetFanRightBridgeFrontCoverLengthFailureExchangeInflationGuardedPrefixSplitResidual`,
  and theorem/finite wrappers
  `terminal_set_two_fan_or_bridge_front_cover_length_failure_exchange_inflation_guarded_prefix_split_residual_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_bridge_front_cover_length_failure_exchange_inflation_guarded_prefix_split_residual_of_terminal_set_no_small_endpoint_separator`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The residual is now structurally explicit.  In the clean no-middle/no-post
  branch, prefix-cover failure is not an arbitrary defect: it is a z/y exchange.
  The old same-side-only prefix point `z` moves from the old side into the
  swapped path and is absent from `rs`/`rt`; the opposite-prefix crossing `y`
  is on `rs`/`rt` but is omitted from the swapped path.
- This explains why the current weighted measure can stall.  The exchange can
  remove the old common vertex `x` and add the front vertex `w`, while swapping
  one side-only support vertex for another.  Common-card and total-support
  comparisons may therefore tie.
- The support-length tradeoff isolates the separate length obstacle: either the
  replacement path is already long enough for the cover branch, or all failure
  is paid for by strict inflation of `altRight`/`altLeft`.  The exchange guard
  shows the concrete source of that inflation/tie.
- The newest combined residual is the strongest current theorem frontier:
  cover-length guard + exchange guard + clean length tradeoff.  It reduces the
  length part of the obstruction to a precise no-alt-inflation/tie-breaker
  problem.
- The length-failure residual is now sharper still: once the replacement path
  is too short, the branch is forced into explicit exchange+alt-inflation.
  This isolates the next proof obligation to a replacement-level shortest or
  lexicographic choice that forbids strict inflation of the swapped path.
- The next non-local target should be a strengthened choice principle:
  shortest replacement path, or lexicographic minimization of the z/y exchange
  defect after minimizing `(commonCard, supportLength)`.  A purely local
  repetition of first-guard lemmas is unlikely to close this residual.

## Round update, support-minimal replacement choice

Lean progress:
- Added the replacement-path choice interface
  `terminalReplacementPathSupportLengthMinimal` and
  `exists_support_length_minimal_path_avoiding`.  From any path avoiding a
  forbidden vertex `x`, the finite path space now yields a path to the same
  endpoint with minimal support length among all paths avoiding `x`.
- Added support-minimal ordered-splice residuals:
  `terminalSetFanLeftSupportMinimalOrderedSpliceResidual` and
  `terminalSetFanRightSupportMinimalOrderedSpliceResidual`, plus coercion
  lemmas back to the old ordered residuals.
- Strengthened the main ordered-splice theorem to choose the separator
  replacement path minimally in the endpoint branch:
  `terminal_set_two_fan_or_support_minimal_ordered_splice_residual_of_no_small_endpoint_separator`.
  The proof still starts from the singleton separator witness, but before
  entering the residual branch it reselects a support-minimal avoiding path to
  the chosen endpoint.
- Added support-minimal bridge-prefix residuals:
  `terminalSetFanLeftSupportMinimalBridgePrefixObstruction` and
  `terminalSetFanRightSupportMinimalBridgePrefixObstruction`, with conversions
  back to the old bridge-prefix obstructions.
- Lifted support minimality through the ordered-splice to bridge-prefix step via
  `terminalSetFanLeftSupportMinimalOrderedSpliceResidual.to_support_minimal_bridge_prefix_obstruction`
  and the right-hand analogue.
- Added theorem/finite wrappers:
  `terminal_set_two_fan_or_support_minimal_bridge_prefix_obstruction_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_support_minimal_bridge_prefix_obstruction_of_terminal_set_no_small_endpoint_separator`.
- Added support-minimal bridge-front residuals:
  `terminalSetFanLeftSupportMinimalBridgeFrontObstruction` and
  `terminalSetFanRightSupportMinimalBridgeFrontObstruction`, with conversions
  back to the old bridge-front obstructions.
- Lifted support minimality one step further through the bridge-prefix
  dichotomy:
  `terminalSetFanLeftSupportMinimalBridgePrefixObstruction.to_support_minimal_front_or_first_guard`
  and the right-hand analogue.  The direct front branch now keeps the
  support-minimal replacement path; the first-guard branch currently falls
  back to the existing non-minimal first-guard obstruction.
- Added theorem/finite wrappers for this stronger split:
  `terminal_set_two_fan_or_support_minimal_bridge_front_or_first_guard_obstruction_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_support_minimal_bridge_front_or_first_guard_obstruction_of_terminal_set_no_small_endpoint_separator`.
- Added support-minimal first-front residuals:
  `terminalSetFanLeftSupportMinimalBridgeFrontFirstObstruction` and
  `terminalSetFanRightSupportMinimalBridgeFrontFirstObstruction`, with
  conversions back to the old first-front obstructions.
- Proved
  `terminalSetFanLeftSupportMinimalBridgeFrontObstruction.to_support_minimal_first`
  and the right-hand analogue.  This repeats the existing finite first-witness
  selection while preserving the support-minimal replacement path.
- Added theorem/finite wrappers upgrading the theorem frontier to
  `terminal_set_two_fan_or_support_minimal_bridge_front_first_or_first_guard_obstruction_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_support_minimal_bridge_front_first_or_first_guard_obstruction_of_terminal_set_no_small_endpoint_separator`.
- Added support-minimal global-first residuals:
  `terminalSetFanLeftSupportMinimalBridgeFrontGlobalFirstObstruction` and
  `terminalSetFanRightSupportMinimalBridgeFrontGlobalFirstObstruction`, with
  conversions back to the old global-first obstructions.
- Proved
  `terminalSetFanLeftSupportMinimalBridgeFrontFirstObstruction.to_support_minimal_global_first`
  and the right-hand analogue, preserving support-minimality through the local
  first-to-global-first normalization.
- Added theorem/finite wrappers upgrading the theorem frontier again to
  `terminal_set_two_fan_or_support_minimal_bridge_front_global_first_or_first_guard_obstruction_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_support_minimal_bridge_front_global_first_or_first_guard_obstruction_of_terminal_set_no_small_endpoint_separator`.
- Added support-minimal suffix residuals:
  `terminalSetFanLeftSupportMinimalBridgeFrontSuffixResidual` and
  `terminalSetFanRightSupportMinimalBridgeFrontSuffixResidual`, with
  conversions back to the old suffix residuals.
- Proved
  `terminalSetFanLeftSupportMinimalBridgeFrontGlobalFirstObstruction.descent_or_support_minimal_suffix_residual`
  and the right-hand analogue.  These preserve the shortest replacement path
  through the suffix-return split.
- Added theorem/finite wrappers upgrading the public theorem frontier to
  `terminal_set_two_fan_or_support_minimal_bridge_front_suffix_residual_of_no_small_endpoint_separator`
  and
  `finite_two_fan_to_pair_or_support_minimal_bridge_front_suffix_residual_of_terminal_set_no_small_endpoint_separator`.
  In this theorem, the separate first-guard side is eliminated by the existing
  weighted-minimal common-card descent argument, so the residual branch now
  carries a support-minimal replacement path directly into suffix residual.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This is the first theorem-level strengthening that changes how the
  replacement path is selected, instead of only classifying the final residual.
  The current strongest support-minimal frontier reaches suffix residual.  The
  separate first-guard side is no longer present in that theorem; it is removed
  by the existing common-card descent contradiction.
- The support-minimal choice does not by itself contradict the length-failure
  branch: the original same-side path contains `x`, so it is not a valid
  competitor in the class of paths avoiding `x`.
- Therefore the next useful target is not another local wrapper.  The proof
  needs one of two concrete bridges:
  1. continue from support-minimal suffix residual into the sharp/clean,
     length-guarded, and exchange+inflation layers; or
  2. build, from the explicit z/y exchange witness, a new path to the same
     endpoint that still avoids `x` and is shorter than the support-minimal
     replacement path, giving a contradiction.
- The second target is the sharper mathematical attack, but the first may be
  needed as infrastructure so that the local exchange witness and the global
  shortestness hypothesis appear in the same Lean context.

## Round update, support-minimal path reaches length-failure frontier

Lean progress:
- Propagated the support-minimal replacement path past the previous suffix
  frontier:
  `terminalSetFanLeftSupportMinimalBridgeFrontSharpSuffixResidual` and the
  right-hand analogue, plus projections back to the old sharp residuals.
- Proved
  `terminalSetFanLeftSupportMinimalBridgeFrontSuffixResidual.to_sharp_of_weighted_min`
  and the right-hand analogue, reusing the old suffix-to-sharp descent proof
  while preserving the same shortest replacement path.
- Added support-minimal clean, length-guarded clean, prefix-split
  length-guarded clean, and cover-length guarded prefix-split residuals, each
  with projections back to the old residuals and theorem/finite wrappers.
- Added the strongest support-minimal theorem-layer endpoint:
  `terminal_set_two_fan_or_support_minimal_bridge_front_cover_length_failure_exchange_inflation_guarded_prefix_split_residual_of_no_small_endpoint_separator`
  and its finite wrapper.  This matches the previous strongest old frontier,
  but the residual branch now also carries a shortest replacement path avoiding
  `x`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This is meaningful progress: the global shortest-replacement choice and the
  local exchange/length-failure witness are now present in the same theorem
  branch.
- It still does not prove the original theorem.  The remaining obstruction is
  the length-failure guard itself: if the replacement path is shorter than the
  old side, the current theorem only forces a prefix exchange witness and
  strict alt-path inflation.  It does not yet construct a shorter path to the
  same endpoint avoiding `x`.
- The next target should be a real contradiction lemma for the support-minimal
  final residual.  In the left case, destruct the residual to get the shortest
  `rs`; under `¬ oldLeft.support.length ≤ rs.support.length`, use the guard's
  prefix witness `z ∉ rs.support` and alt-right inflation to build either:
  1. a path from `v` to `s` avoiding `x` with support length `< rs.support.length`,
     contradicting `terminalReplacementPathSupportLengthMinimal`; or
  2. a direct no-alt-inflation/common-card descent contradiction showing that
     the length-failure premise cannot occur.
- Do not spend the next round on more theorem wrappers unless they directly
  feed that contradiction; the useful infrastructure target is now reached.

## Round update, secondary minimality reaches final residual

Lean progress:
- Added a generic two-stage choice lemma:
  `exists_minimal_terminal_path_pair_weighted_measure_then`.  It first chooses
  a globally `terminalPathPairWeightedMeasure`-minimal terminal path pair, then
  chooses it minimal for an arbitrary secondary `Nat`-valued defect among all
  weighted-minimal pairs.
- Added transparent abbreviations for the carried hypotheses:
  `terminalPathPairWeightedMeasureMinimal` and
  `terminalPathPairSecondaryMinimalAfterWeighted`.
- Factored the ordered-splice core after the initial pair choice into
  `terminal_set_two_fan_or_support_minimal_ordered_splice_residual_of_weighted_min_pair`.
  This lets later pair-choice variants reuse the same support-minimal
  ordered-splice proof without copying the initial endpoint selection.
- Added the secondary-minimal theorem-layer entry point:
  `terminal_set_two_fan_or_secondary_minimal_support_minimal_ordered_splice_residual_of_no_small_endpoint_separator`.
- Propagated the same arbitrary secondary-minimality hypothesis through the
  support-minimal chain:
  bridge-prefix, bridge-front/first-guard, first-front, global-first, suffix,
  sharp suffix, clean suffix, length-guarded clean suffix, prefix-split,
  cover-length guarded prefix-split, and finally
  `terminal_set_two_fan_or_secondary_minimal_support_minimal_bridge_front_cover_length_failure_exchange_inflation_guarded_prefix_split_residual_of_no_small_endpoint_separator`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The final support-minimal residual can now be reached while carrying an
  arbitrary secondary minimization principle on the original weighted-minimal
  pair.  This is the right global-choice infrastructure for attacking the
  remaining exchange/length-failure obstruction.
- A direct contradiction using bare left/right support length as the secondary
  measure is still not immediate.  In the left length-failure case the
  replacement path `rs` is shorter than the old left path, but the forced
  swapped right path `altRight` is strictly longer than the old right path.
  If the swapped pair has larger old weighted measure, secondary minimality
  among weighted-minimal pairs cannot compare against it.  The right case is
  symmetric.
- Therefore the next real mathematical target is narrower than "thread more
  wrappers": prove that the final z/y exchange witness either
  1. can be converted into a weighted-minimal comparison pair with a strictly
     smaller exchange defect, contradicting the new secondary-minimality; or
  2. produces a shorter same-endpoint path avoiding `x`, contradicting
     `terminalReplacementPathSupportLengthMinimal`.
- The likely secondary should measure an exchange/frontier defect tied to the
  first bad prefix witness, not merely total support length or one component's
  support length.

## Round update, prefix-only secondary residual

Lean progress:
- Added concrete prefix-only defect measures:
  `terminalPathPairLeftPrefixOnlyDefect`,
  `terminalPathPairRightPrefixOnlyDefect`, and
  `terminalPathPairPrefixOnlyDefect`.  They count one-sided prefix vertices
  before a common vertex, left plus right for the combined measure.
- Proved positivity lemmas
  `terminalPathPairLeftPrefixOnlyDefect_pos_of_prefix_only` and
  `terminalPathPairRightPrefixOnlyDefect_pos_of_prefix_only`.
- Connected the final length-failure exchange guards to those concrete defects
  with
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.left_prefix_only_defect_pos`
  and
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.right_prefix_only_defect_pos`.
  Thus the final residual now carries a positive, named prefix-only defect
  rather than only an informal z/y obstruction.
- Instantiated the arbitrary secondary-minimal final theorem with the new
  measure, yielding
  `terminal_set_two_fan_or_prefix_only_minimal_support_minimal_bridge_front_cover_length_failure_exchange_inflation_guarded_prefix_split_residual_of_no_small_endpoint_separator`
  and the finite wrapper
  `finite_two_fan_to_pair_or_prefix_only_minimal_support_minimal_bridge_front_cover_length_failure_exchange_inflation_guarded_prefix_split_residual_of_terminal_set_no_small_endpoint_separator`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This still does not prove the original theorem.  The active
  `terminal_set_two_fan_of_no_small_endpoint_separator` and full finite wrapper
  remain frozen in block comments, so the passing file should not be read as a
  completed two-fan proof.
- The route is nevertheless more precise than before.  The theorem frontier now
  chooses the original terminal pair minimal for weighted measure and then for a
  concrete prefix-only defect; the final residual forces that same concrete
  defect to be positive.
- The next contradiction target is exact: from the prefix-only-minimal final
  residual, prove that the left/right final guard either
  1. constructs a weighted-minimal comparison pair with strictly smaller
     `terminalPathPairPrefixOnlyDefect`; or
  2. constructs a shorter same-endpoint replacement path avoiding `x`,
     contradicting `terminalReplacementPathSupportLengthMinimal`.
- Until one of these two contradiction lemmas exists, the proof is on the right
  main route but remains one substantial mathematical step short of activating
  the original two-fan theorem.

## Round update, prefix-only defect bridge lemmas

Lean progress:
- Added component/combined defect bookkeeping:
  `terminalPathPairLeftPrefixOnlyDefect_eq_zero_of_prefix_only_defect_eq_zero`,
  `terminalPathPairRightPrefixOnlyDefect_eq_zero_of_prefix_only_defect_eq_zero`,
  `terminalPathPairPrefixOnlyDefect_pos_of_left_prefix_only`, and
  `terminalPathPairPrefixOnlyDefect_pos_of_right_prefix_only`.
- Upgraded the final left/right length-failure exchange guards from side-only
  positivity to positivity of the actual secondary measure:
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.prefix_only_defect_pos`
  and
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.prefix_only_defect_pos`.
- Added zero-defect cover bridges:
  `terminalSetFanLeftBridgeFrontPrefixCover_of_prefix_only_defect_eq_zero`,
  `terminalSetFanRightBridgeFrontPrefixCover_of_prefix_only_defect_eq_zero`,
  and the corresponding
  `terminalSetFanLeftBridgeFrontPrefixCoverSplit.of_prefix_only_defect_eq_zero`
  / `terminalSetFanRightBridgeFrontPrefixCoverSplit.of_prefix_only_defect_eq_zero`.
  These say that if the combined prefix-only defect is zero, then the prefix
  cover split is forced into its cover branch.
- Added the direct zero-defect length-failure blockers
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.length_ge_of_prefix_only_defect_eq_zero`
  and
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.length_ge_of_prefix_only_defect_eq_zero`.
  Under the local final-guard hypotheses, a zero combined defect now rules out
  the corresponding left/right support-length failure immediately.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This closes a real interface gap: the secondary measure used by the theorem
  frontier is now connected both to the final exchange guard and to the
  prefix-cover branch needed by the existing alt-path support-length lemmas.
- It still does not provide the strict descent required by secondary
  minimality.  The remaining hard lemma is now more concrete: in the positive
  defect case forced by length failure, construct a weighted-minimal comparison
  pair with strictly smaller `terminalPathPairPrefixOnlyDefect`, or construct a
  shorter same-endpoint path avoiding `x`.
- The next local target should be an alt-pair defect comparison lemma.  In the
  left case, use the guard witness `z` with
  `z ∈ altRight.support` and `y ∉ altRight.support` to prove that replacing
  the right component by `altRight` removes the selected left-prefix defect; the
  missing condition is a weighted-measure tie/minimality proof for that
  comparison pair.

## Round update, alt-pair defect descent interface

Lean progress:
- Named the finite sets underlying the prefix-only defects:
  `terminalPathPairLeftPrefixOnlyDefectSet` and
  `terminalPathPairRightPrefixOnlyDefectSet`, with membership and card bridge
  lemmas.
- Added generic strict descent tools:
  `terminalPathPairLeftPrefixOnlyDefect_lt_of_defectSet_subset_erase`,
  `terminalPathPairRightPrefixOnlyDefect_lt_of_defectSet_subset_erase`,
  `terminalPathPairPrefixOnlyDefect_lt_of_left_defectSet_subset_erase_right_defectSet_subset`,
  and
  `terminalPathPairPrefixOnlyDefect_lt_of_left_defectSet_subset_right_defectSet_subset_erase`.
  These reduce strict secondary descent to a finite-set inclusion into an
  erased old defect set.
- Proved the concrete exchange-witness absorption lemmas
  `terminalPathPairLeftPrefixOnlyDefectSet_mem_and_absent_after_altRight` and
  `terminalPathPairRightPrefixOnlyDefectSet_mem_and_absent_after_altLeft`.
  The final exchange witness is an old side defect and is no longer a side
  defect after replacing the opposite component by the corresponding alt path.
- Lifted that fact through the final guards:
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.left_defect_witness_removed_after_altRight`
  and
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.right_defect_witness_removed_after_altLeft`.
- Added conditional descent interfaces
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.prefix_only_defect_lt_after_altRight_of_defectSet_subsets`
  and
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.prefix_only_defect_lt_after_altLeft_of_defectSet_subsets`.
  Once the remaining defect-set subset facts are supplied, the alt pair has
  strictly smaller `terminalPathPairPrefixOnlyDefect`.
- Added the secondary-minimal contradiction interfaces
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.false_of_secondary_minimal_altRight_subsets`
  and
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.false_of_secondary_minimal_altLeft_subsets`.
  These turn strict alt-pair defect descent plus alt-pair weighted-minimality
  into contradiction with the secondary-minimal choice.
- Added `terminalPathPairWeightedMeasureMinimal_of_measure_le`: an alt pair
  inherits weighted minimality from the original pair as soon as its weighted
  measure is not larger than the original pair's weighted measure.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The remaining positive-defect obstruction is no longer diffuse.  To close the
  current final residual by secondary minimality, it is enough to prove for the
  left alt pair `(oldLeft, altRight)`:
  1. `terminalPathPairWeightedMeasure (oldLeft, altRight) ≤
     terminalPathPairWeightedMeasure pair`;
  2. the new left defect set is contained in the old left defect set with the
     absorbed witness erased;
  3. the new right defect set is contained in the old right defect set.
  The right case is symmetric with `(altLeft, oldRight)`.
- The hard work has therefore shifted from theorem wrapping to two concrete
  path-order/support-set subset proofs plus one weighted-measure nonincrease
  proof for the alt pair.  Until those are proved, the original two-fan theorem
  remains inactive.

## Round update, replacement alt-pair correction

Lean progress:
- Added the generic weighted-measure nonincrease lemma
  `terminalPathPairWeightedMeasure_le_of_commonCard_le_supportLength_le`.
  This converts common-card nonincrease plus support-length nonincrease into
  weighted-measure nonincrease.
- Added clean replacement-pair weighted-measure wrappers:
  `terminal_set_fan_left_front_clean_alt_weightedMeasure_le_of_supportLength_le`
  and
  `terminal_set_fan_right_front_clean_alt_weightedMeasure_le_of_supportLength_le`.
  These use the existing clean alt common-card controls for the actual
  replacement pairs `(rs, altRight)` and `(altLeft, rt)`.
- Added generic absence lemmas
  `not_mem_terminalPathPairLeftPrefixOnlyDefectSet_of_mem_right` and
  `not_mem_terminalPathPairRightPrefixOnlyDefectSet_of_mem_left`.
  They formalize the simple reason an absorbed exchange witness cannot remain a
  side defect after it appears on the opposite component.
- Lifted the final exchange witness to the replacement pairs:
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.left_defect_witness_removed_after_replacement_altRight`
  and
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.right_defect_witness_removed_after_replacement_altLeft`.
- Added replacement-pair descent and contradiction interfaces:
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.prefix_only_defect_lt_after_replacement_altRight_of_defectSet_subsets`,
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.prefix_only_defect_lt_after_replacement_altLeft_of_defectSet_subsets`,
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.false_of_secondary_minimal_replacement_altRight_measure_le_subsets`,
  and
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.false_of_secondary_minimal_replacement_altLeft_measure_le_subsets`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This corrects the previous alt-pair target.  The pair `(oldLeft, altRight)`
  is too strong as a weighted-measure comparison target because `altRight`
  imports old-left prefix vertices and may increase common-card.  The route
  supported by the existing proof infrastructure is the replacement pair
  `(rs, altRight)` in the left case, and `(altLeft, rt)` in the right case.
- The next exact tasks are therefore:
  1. prove replacement-pair weighted-measure nonincrease, likely by proving
     replacement-pair support-length nonincrease and using the new wrapper;
  2. prove the replacement-pair left/right defect-set subset conditions needed
     by the new secondary-minimal contradiction interfaces.
- The original two-fan theorem and finite wrapper remain inactive until those
  conditions close the final residual.

## Round update, replacement common-front classification

Lean progress:
- Added reusable replacement-pair common-vertex classifiers:
  `terminal_set_fan_left_front_clean_alt_common_or_front` and
  `terminal_set_fan_right_front_clean_alt_common_or_front`.
  In the left case, any non-apex common vertex of `rs` and `altRight` is either
  the front vertex `w` or an old common vertex of the original pair distinct
  from `x`; the right case is symmetric.
- Added the corresponding finite-set subset wrappers:
  `terminal_set_fan_left_front_clean_alt_common_subset_insert_erase` and
  `terminal_set_fan_right_front_clean_alt_common_subset_insert_erase`.
  These expose the exact subset relation that was previously buried inside the
  common-card nonincrease proofs.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This does not close the final residual yet, but it removes duplicated local
  reasoning from the next target.  A future defect-set subset proof can now
  start by classifying its new common witness through these lemmas, instead of
  redoing the `altRight`/`altLeft` append-support split and suffix-only
  exclusion.
- The remaining concrete tasks are still:
  1. prove replacement-pair support-length or weighted-measure nonincrease;
  2. prove replacement-pair defect-set subset, using the new common-front
     classification as the first reduction.

## Round update, replacement defect-set route diagnosis

Lean progress:
- Added the small path-start helpers
  `takeUntil_start_eq_nil` and `eq_start_of_mem_takeUntil_start`.
  These remove the spurious `c = v` branch when a prefix-only defect witness
  is unpacked at the replacement pair.
- Added replacement-pair defect-witness classifiers:
  `terminal_set_fan_left_front_clean_alt_leftPrefixOnlyDefect_witness_common_or_front`
  and
  `terminal_set_fan_right_front_clean_alt_rightPrefixOnlyDefect_witness_common_or_front`.
  In the left case, any new left prefix-only defect of `(rs, altRight)` has a
  common witness `c` on `rs ∩ altRight`, and that witness is either the front
  `w` or an old common vertex of the original pair distinct from `x`; the right
  case is symmetric.
- Added front-prefix diagnostic lemmas:
  `terminal_set_fan_left_front_prefix_absent_altRight_not_old_support` and
  `terminal_set_fan_right_front_prefix_absent_altLeft_not_old_support`.
  These formalize the key obstruction: a prefix vertex before the front `w`
  that is absent from the replacement alt path is not in either old terminal
  path, provided `w` is retained by the alt path.
- Added generic support-exclusion bridges
  `not_mem_terminalPathPairLeftPrefixOnlyDefectSet_of_not_mem_left` and
  `not_mem_terminalPathPairRightPrefixOnlyDefectSet_of_not_mem_right`, then
  lifted the front-prefix diagnosis to old-defect exclusion via
  `terminal_set_fan_left_front_prefix_absent_altRight_not_old_leftPrefixOnlyDefect`
  and
  `terminal_set_fan_right_front_prefix_absent_altLeft_not_old_rightPrefixOnlyDefect`.
  This makes the subset obstruction explicit at the defect-set level.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The replacement defect-set subset route is not a viable main closure as
  stated.  The new front-prefix diagnostic shows why: `(rs, altRight)` can
  create prefix-only defects from genuinely new vertices before `w`; these
  vertices are outside both old supports and, by the new lifted lemmas, are
  not old prefix-only defects.  This is a mathematical obstruction, not a Lean
  bookkeeping issue.
- Therefore the conditional secondary-minimal interfaces based on full
  defect-set subset/erase remain useful as diagnostics, but they should not be
  treated as the next main proof target.
- The active theorem frontier remains the residual theorem
  `terminal_set_two_fan_or_prefix_only_minimal_support_minimal_bridge_front_cover_length_failure_exchange_inflation_guarded_prefix_split_residual_of_no_small_endpoint_separator`
  and its finite wrapper.  The direct
  `terminal_set_two_fan_of_no_small_endpoint_separator` / full terminal-set
  wrapper are still only present in the frozen sketch block, not active Lean
  declarations.
- The next main attack should close the final residual by a route that accounts
  for the new front-prefix vertices, likely by deriving a common-card descent
  or a weighted/support-length contradiction from the exchange-inflation guard
  itself, rather than by forcing replacement defect-set subset.

## Round update, suffix-retention wide residual interface

Lean progress:
- Added stronger weighted-minimal contradiction wrappers for the existing
  first-crossing union-first descents:
  `terminal_set_fan_splice_descent_left_of_hsep_of_union_first_right_false_of_weighted_min`
  and
  `terminal_set_fan_splice_descent_right_of_hsep_of_union_first_left_false_of_weighted_min`.
  These show that an opposite-only front with the residual `hfirst_union`
  property is already impossible under weighted minimality.
- Added the right-hand symmetric wide residual descent
  `terminal_set_fan_right_suffix_retention_left_prefix_wide_residual_descent`,
  by swapping the already-active left-hand lemma.  This closes the previous
  left/right asymmetry near the splice-descent tail.
- Added `..._of_union_first` wrappers on both sides:
  `terminal_set_fan_left_suffix_retention_right_prefix_wide_residual_descent_of_union_first`
  and
  `terminal_set_fan_right_suffix_retention_left_prefix_wide_residual_descent_of_union_first`.
  These convert the residual-layer `hfirst_union` field directly into the
  `z = w ∨ z ∉ takeUntil w` form needed by the uncrossing descent.
- Added weighted-minimal contradiction interfaces:
  `terminal_set_fan_left_suffix_retention_right_prefix_wide_residual_false_of_weighted_min`
  and
  `terminal_set_fan_right_suffix_retention_left_prefix_wide_residual_false_of_weighted_min`.
  Thus an opposite-front retained branch with a further noncommon old residual
  point is now a checked contradiction under weighted minimality.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This is real progress, but it is not the final residual closure.  The new
  interfaces eliminate the opposite-front branch and, a fortiori, the
  opposite-front wide-residual subcase.  The strongest theorem-level frontier
  is still the prefix-only-minimal support-minimal
  cover-length-failure/exchange-inflation guarded prefix-split residual.
- The main unresolved branch remains the same-side front branch carried by the
  support-minimal final residual.  The next target should be a contradiction
  for that actual witness: combine the support-minimal replacement path,
  the cover-length guard, and the exchange-inflation guard without requiring
  full replacement defect-set subset.

## Round update, final residual prefix-defect narrowing

Lean progress:
- Added prefix-cover failure interfaces:
  `terminalSetFanLeftBridgeFrontPrefixCoverSplit.prefix_only_defect_pos_of_not_cover`
  and
  `terminalSetFanRightBridgeFrontPrefixCoverSplit.prefix_only_defect_pos_of_not_cover`.
  Thus failure of the same-side prefix-cover condition is now formally recorded
  as a positive side prefix-only defect of the original pair.
- Added clean prefix-cover length-failure contradictions for the final support
  minimal residual:
  `terminalSetFanLeftSupportMinimalBridgeFrontCoverLengthFailureExchangeInflationGuardedPrefixSplitResidual.false_of_clean_prefix_cover_length_failure`
  and the right analogue.  In the clean branch, prefix-cover plus side-length
  failure is now impossible.
- Added final-residual split interfaces:
  `terminalSetFanLeftSupportMinimalBridgeFrontCoverLengthFailureExchangeInflationGuardedPrefixSplitResidual.length_ge_or_prefix_only_defect_pos_of_prefix_split`
  and the right analogue.  These expose the usable dichotomy: under the clean
  no-suffix/no-post/no-middle hypotheses, the actual replacement side is not
  shorter, or the weighted-minimal pair has positive total prefix-only defect.
- Added inverse witness extractors for positive prefix-only defect:
  `terminalPathPairLeftPrefixOnlyDefect_pos_cases`,
  `terminalPathPairRightPrefixOnlyDefect_pos_cases`, and
  `terminalPathPairPrefixOnlyDefect_pos_cases`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The active theorem frontier is still the prefix-only-minimal support-minimal
  cover-length-failure/exchange-inflation guarded prefix-split residual and its
  finite wrapper; the original two-fan theorem is not yet active.
- The route has narrowed.  The prefix-cover branch no longer hides a length
  failure; the prefix-cover failure branch now gives a concrete prefix-only
  defect witness.  The remaining mathematical gap is to turn that concrete
  positive prefix-only defect into a secondary-minimal contradiction, most
  likely by reusing the singleton-separator/first-guard machinery with the
  defect witness as the point to avoid.
- The previous full replacement defect-set subset route remains a diagnostic
  dead end: replacement paths can introduce genuinely new prefix-only defects.

## Round update, absent-first defect frontier

Lean progress:
- Added first-witness extractors for positive prefix-only defect:
  `terminalPathPairLeftPrefixOnlyDefect_pos_first_cases`,
  `terminalPathPairRightPrefixOnlyDefect_pos_first_cases`, and
  `terminalPathPairPrefixOnlyDefect_pos_first_cases`.  A positive defect can
  now be normalized to an earliest bad prefix point on the left or right path.
- Added support-minimal final residuals carrying the absent guard in addition
  to the existing length-failure/exchange-inflation guard:
  `terminalSetFanLeftSupportMinimalBridgeFrontCoverLengthAbsentFailureExchangeInflationGuardedPrefixSplitResidual`
  and the right analogue.
- Added theorem-level strengthened frontiers:
  `terminal_set_two_fan_or_prefix_only_minimal_support_minimal_bridge_front_cover_length_absent_failure_exchange_inflation_guarded_prefix_split_residual_of_no_small_endpoint_separator`
  and its finite wrapper.  The active main-chain residual now preserves the
  absent-prefix guard rather than dropping back to the weaker final residual.
- Added clean-branch dichotomy interfaces:
  `terminalSetFanLeftSupportMinimalBridgeFrontCoverLengthAbsentFailureExchangeInflationGuardedPrefixSplitResidual.length_ge_or_first_prefix_absent`
  and the right analogue.  In the clean branch, either the replacement side is
  not shorter, or there is an earliest prefix defect point absent from the
  replacement path.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The original two-fan theorem is still not active.  The strongest active
  theorem-level frontier is now the prefix-only-minimal, support-minimal,
  cover-length/absent/failure-exchange-inflation guarded prefix-split residual.
- This is a genuine strengthening of the main route: the unresolved clean
  length-failure branch now yields a specific earliest defect point which is
  also absent from the support-minimal replacement path.  That is the right
  shape for the next secondary-minimal contradiction attempt.
- Next target: use the absent earliest defect `z` to prove that the replacement
  pair eliminates one old side defect without creating an earlier same-side
  defect, or else extract a first-guard/commonCard descent.  The route should
  stay local to this earliest-defect witness and avoid the already-failed full
  defect-set subset claim.

## Round update, replacement front-subset obstruction

Lean progress:
- Added direct secondary-minimal contradiction interfaces for the absent-alt
  replacement pair:
  `terminalPathPairSecondaryMinimal_false_after_replacement_altRight_of_absent_alt_measure_le_defectSet_subsets`
  and the right analogue.  These consume the original pair's weighted
  minimality plus a measure nonincrease for the replacement pair, rather than
  requiring the replacement pair to be pre-proved weighted-minimal.
- Added front-new-defect witnesses for replacement pairs:
  `terminal_set_fan_left_front_absent_mem_replacement_altRight_leftPrefixOnlyDefectSet`
  and
  `terminal_set_fan_right_front_absent_mem_replacement_altLeft_rightPrefixOnlyDefectSet`.
  A vertex on the replacement front segment that is absent from the cross-swap
  alt path is now formally a new prefix-only defect.
- Added the corresponding obstruction lemmas:
  `terminal_set_fan_left_front_absent_forbidden_by_replacement_left_defectSet_subset`
  / `_subset_erase` and the right analogues.  These show that the replacement
  defect-set subset assumptions are not harmless: they forbid any front vertex
  of `rs.takeUntil w` (or `rt.takeUntil w`) from being absent from the alt path.
- Strengthened that to front-trivial consequences:
  `terminal_set_fan_left_front_eq_start_or_front_of_replacement_left_defectSet_subset_erase`
  and the right analogue.  Under the current erase-subset assumption, every
  vertex on the clean replacement front is forced to be `v` or `w`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The original two-fan theorem is still not closed.  This round clarifies why:
  the full replacement defect-set subset route is stronger than it first
  looked, because the replacement front naturally creates fresh prefix-only
  defects unless that front is already covered by the alt path.
- The current route is still plausible, but the next missing mathematical fact
  is sharper than before.  It is not enough to say "replacement decreases the
  defect count"; one must prove either
  1. the replacement front is trivial (`takeUntil w` contains only `v,w`) and
     then use support-minimality/uncrossing, or
  2. a nontrivial front vertex yields a commonCard/support-length descent before
     the secondary-minimal defect argument is applied.
- Next target: prove a support-minimal contradiction from the newly formalized
  front-trivial condition, or prove that any nontrivial front vertex gives a
  first-guard/commonCard descent.  This is now the real local gap in the
  absent-first branch.

## Round update, weighted-minimal front-trivial compression

Lean progress:
- Added weighted-minimal bridge wrappers:
  `terminal_set_fan_left_front_eq_start_or_front_of_weighted_min_replacement_left_defectSet_subset_erase`
  and the right analogue.  These remove the standalone `w ∈ altRight/altLeft`
  prerequisite by deriving it from the real residual hypothesis
  `w ∈ old-prefix-to-x` plus weighted minimality.
- Added nontrivial-front obstruction wrappers:
  `terminal_set_fan_left_front_nontrivial_forbidden_by_weighted_min_replacement_left_defectSet_subset_erase`
  and the right analogue.  If the replacement front has any vertex other than
  `v` or `w`, the same-side erase-subset hypothesis is impossible.
- Added support-length compression:
  `terminal_set_fan_left_front_support_length_le_two_of_weighted_min_replacement_left_defectSet_subset_erase`
  / `_eq_two_...` and right analogues.  In the genuine residual case
  `w ≠ v`, the erase-subset route forces `(rs.takeUntil w).support.length = 2`
  (or symmetrically `(rt.takeUntil w).support.length = 2`).
- Added adjacency compression:
  `terminal_set_fan_left_front_adj_of_weighted_min_replacement_left_defectSet_subset_erase`
  and the right analogue.  The remaining direct-front special case is now
  formally an actual graph edge `G.Adj v w`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The previous hope "front-trivial directly contradicts support minimality" is
  too optimistic: a direct `v-w` replacement front can be support-minimal.
  This round therefore converts the gap into a precise remaining special case.
- The active branch is now: either a nontrivial replacement front blocks the
  defect-set erase-subset route immediately, or the replacement front is exactly
  a two-vertex `v,w` prefix and hence an edge `G.Adj v w`.  The remaining proof
  should target this direct-edge case, likely by combining the old-prefix
  position `w < x`, the first opposite-side hit `y`, and the no-middle/no-post
  guards to extract a splice or support-length contradiction.
- Next target: formalize the direct-front case as its own residual/obstruction
  lemma, rather than continuing to strengthen the generic defect-set subset
  interface.

## Round update, direct-edge old-prefix compression

Lean progress:
- Added a component-subset commonCard monotonicity helper:
  `terminalPathPairCommonCard_le_of_component_toFinset_subset`.
- Proved the direct-edge shortcut obstruction:
  `terminal_set_fan_left_direct_edge_old_prefix_nontrivial_false_of_weighted_min`
  and the right analogue.  If `G.Adj v w` and the weighted-minimal old path
  from `v` to `w` has any prefix vertex other than `v,w`, replacing the old
  prefix by the edge `v-w` gives commonCard nonincrease and support-length
  strict decrease, contradicting weighted minimality.
- Packaged this as old-prefix compression:
  `terminal_set_fan_left_direct_edge_old_prefix_eq_start_or_front_of_weighted_min`,
  `terminal_set_fan_left_direct_edge_old_prefix_support_length_eq_two_of_weighted_min`,
  and right analogues.
- Connected it back to the previous replacement-front direct-edge branch:
  `terminal_set_fan_left_front_old_prefix_support_length_eq_two_of_weighted_min_replacement_left_defectSet_subset_erase`
  and the right analogue.  Under the same replacement defect erase-subset
  assumptions, both the replacement front and the original old prefix to `w`
  are now formally two-vertex prefixes.
- Added tail-location utilities:
  `terminal_set_fan_left_direct_edge_old_support_nontrivial_mem_dropUntil_front_of_weighted_min`
  and right analogue.  Any old-path vertex distinct from `v,w` must lie after
  `w` once the direct edge `v-w` is available.
- Added residual-level localization:
  `terminalSetFanLeftSupportMinimalBridgeFrontCoverLengthAbsentFailureExchangeInflationGuardedPrefixSplitResidual.first_prefix_absent_after_front_of_length_failure_direct_edge`
  and the right analogue.  In the length-failure residual plus direct-edge
  case, the first absent prefix witness is now located in the old path tail
  after `w`, while retaining the alt-membership and first-prefix data.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This is real progress on the direct-edge special case, but it still does not
  close the original theorem.  The current residual interface still does not
  directly provide the replacement defect erase-subset assumptions; those are
  conditional branches produced by secondary-minimality arguments.
- The remaining obstruction is now sharper: after the direct-edge compression,
  the bad witness is no longer on the front before `w`; it is an old-path tail
  vertex after `w`, absent from both the replacement path `rs/rt` and the
  opposite old path, but present in the cross-swap alt path.
- The next target should be a bridge from this old-tail absent witness to one
  of the existing replacement-tail guards (`no_middle`, `no_post`,
  `no_suffix_only`) or to a new splice/commonCard descent.  The present tools
  mostly handle bad vertices already lying on `rs.dropUntil w`/`rt.dropUntil w`;
  the new witness lies on the old path tail and is explicitly not in `rs/rt`.

## Round update, direct-edge witness between front and common

Lean progress:
- Strengthened the direct-edge tail localization from "after `w`" to the exact
  old-path segment between the direct front `w` and common vertex `x`:
  `terminal_set_fan_left_direct_edge_old_prefix_nontrivial_mem_between_front_and_common_of_weighted_min`
  and the right analogue.
- Lifted that localization to the length-failure residual exchange witness:
  `...first_prefix_exchange_between_front_and_common_of_length_failure_direct_edge`
  on both sides.  The witness now carries
  `z ∈ (old.dropUntil w).takeUntil x`, plus the previous `alt` membership,
  `y ∉ alt`, and first-prefix data.
- Added stronger inflation-preserving wrappers:
  `...first_prefix_exchange_inflation_between_front_and_common_of_length_failure_direct_edge`
  on both sides.  These preserve the original length-failure guard's alt-path
  support-length inflation while adding the between-front/common localization.
- Connected the same localized witness to the replacement-alt defect-set
  language:
  `...left_defect_witness_removed_between_front_and_common_after_replacement_altRight_of_direct_edge`
  and the right analogue.  The erased prefix-only defect witness is now not
  just known to be removed by the replacement-alt pair; it is known to lie in
  the old segment from `w` to `x`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This did not close the theorem.  It sharpens the direct-edge branch into a
  much more structured residual, but the remaining missing step is still a
  cross-path bridge: the bad witness is on the original path segment
  `(old.dropUntil w).takeUntil x`, while the existing `no_middle`/`no_post`
  guards act on the replacement path tail `rs.dropUntil w` / `rt.dropUntil w`.
- The alt-path support-length fact points in the wrong direction for a weighted
  descent by itself: it certifies inflation, not a smaller weighted measure.
  Therefore the next real target is commonCard control or a splice descent,
  not another support-length wrapper.
- Next target: prove a bridge lemma converting the localized old-segment
  defect witness plus `z ∉ rs/rt` into either a replacement-tail witness
  forbidden by `no_middle`/`no_post`, or a direct commonCard descent via a
  cross-swap/fallback splice.

## Round update, old-segment obstruction package

Lean progress:
- Added the direct-edge old-segment obstruction wrappers:
  `terminalSetFanLeftSupportMinimalBridgeFrontCoverLengthAbsentFailureExchangeInflationGuardedPrefixSplitResidual.old_segment_obstruction_of_length_failure_direct_edge`
  and the right analogue.
- These wrap the existing between-front/common witness with the extra
  opposite-suffix exclusion:
  on the left branch, the same residual gives
  `y ∉ (oldRight.dropUntil x).support`; on the right branch,
  `y ∉ (oldLeft.dropUntil x).support`.

Meaning:
- The tempting later-return route is now formally ruled out in the direct-edge
  length-failure branch.  The opposite-side point `y` lies before `x` on the
  old opposite path, is absent from the cross-swap alt path, and is not a
  suffix point after `x`.
- The current branch is therefore genuinely an old-segment obstruction:
  the removed defect witness `z` is between `w` and `x` on the old path,
  is absent from the replacement path `rs/rt`, and survives in the cross-swap
  alt path.  It cannot be passed directly to the existing replacement-tail
  guards.

Strategic status:
- The direct-edge shortcut route is exhausted for the prefix before `w`: the
  existing weighted-minimality lemmas already prove that old prefix has only
  `{v,w}`.  The remaining `z` is after `w`, so another shortcut of the
  `v-w` prefix will not close the branch.
- The two viable next targets are unchanged but sharper:
  1. prove defect-set monotonicity / erase-subset for the replacement-alt
     pair, or
  2. build a new splice/commonCard descent that uses the old segment
     `(old.dropUntil w).takeUntil x` directly.

## Round update, opposite defect-source split

Lean progress:
- Added the replacement-alt opposite defect source classifiers:
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_source_common_or_front`
  and
  `terminal_set_fan_right_front_clean_alt_leftPrefixOnlyDefect_source_common_or_front`.
- These handle the exact subset side that was previously opaque.  On the left
  replacement branch, any right-prefix defect of the alt pair is now known to
  be absent from `rs`, to have its common witness either at `w` or at an old
  common vertex different from `x`, and to come from one of exactly two
  cross-swap sources:
  `oldLeft.takeUntil x` or `oldRight.dropUntil x`.  The right branch is
  symmetric.
- Added the subset reduction wrappers:
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefectSet_subset_of_source_cases`
  and
  `terminal_set_fan_right_front_clean_alt_leftPrefixOnlyDefectSet_subset_of_source_cases`.
  These reduce the global opposite defect-set subset obligation to two local
  source obligations: the old-prefix source and the old-suffix source.
- Added the subset-branch source exclusion lemmas:
  `terminal_set_fan_left_altRight_old_left_prefix_source_forbidden_by_right_defectSet_subset`
  and
  `terminal_set_fan_right_altLeft_old_right_prefix_source_forbidden_by_left_defectSet_subset`.
  These show that, once the opposite defect-set subset is assumed, the
  old-prefix source is impossible because such a vertex lies on the original
  same-side support.
- Packaged this as the suffix-only consequences:
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_suffix_source_of_subset`
  and
  `terminal_set_fan_right_front_clean_alt_leftPrefixOnlyDefect_suffix_source_of_subset`.
  Thus in the secondary-minimality subset branch, every opposite alt defect
  must come from `oldRight.dropUntil x` / `oldLeft.dropUntil x`.
- Added the forward proof interface for the subset goal:
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefectSet_subset_of_no_prefix_source_and_suffix_source`
  and
  `terminal_set_fan_right_front_clean_alt_leftPrefixOnlyDefectSet_subset_of_no_prefix_source_and_suffix_source`.
  This is the right next interface: to prove the opposite subset, it is enough
  to rule out the old-prefix source and recover the old-suffix source as an
  original opposite defect.
- Connected that interface back to the secondary-minimality contradiction:
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.false_of_secondary_minimal_replacement_altRight_measure_le_source_cases`
  and
  `terminalSetFanRightBridgeFrontLengthFailureExchangeInflationGuard.false_of_secondary_minimal_replacement_altLeft_measure_le_source_cases`.
  These wrappers replace the previous black-box opposite defect-set subset
  hypothesis by the two local source obligations while reusing the verified
  `false_of_secondary_minimal_*_subsets` contradiction.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This confirms that the current approach is not blocked by an unstructured
  Finset subset.  The missing monotonicity has been localized to path-order
  facts about the sources created by the cross-swap alt path.
- It also clarifies the secondary-minimality branch: if the opposite subset is
  assumed, the old-prefix source is already impossible.  The remaining local
  obligation is the old-suffix source, namely showing that any alt opposite
  defect sourced from `oldRight.dropUntil x` / `oldLeft.dropUntil x` is already
  an original opposite defect, or else extracting a splice/commonCard descent.
- For a direct proof of the subset, the next target is now exact:
  prove `no_prefix_source` for the alt opposite defect, then prove the
  old-suffix source recovery lemma.  If order along the cross-swap
  `alt.takeUntil c` cannot be transported back to the original old suffix
  `takeUntil c`, that failure is the next precise splice obstruction.
- The theorem-level finite fan wrappers remain in the residual/or form; the
  full arbitrary-intersection splice wrappers are still frozen route sketches.
  Therefore the next effective move is not another finite wrapper, but closing
  these two source obligations inside the length-failure residual branch.

## Round update, suffix-source obstruction interface

Lean progress:
- Added the small order-witness constructors
  `terminalPathPairLeftPrefixOnlyDefectSet_mem_of_order_witness` and
  `terminalPathPairRightPrefixOnlyDefectSet_mem_of_order_witness`.
  These package the trivial but repeatedly needed step: once an old common
  witness `c` is known and `z` lies in the old path prefix up to `c`, the
  corresponding original prefix-only defect follows immediately.
- Added the suffix-source decomposition wrappers
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_suffix_source_decomposition`
  and
  `terminal_set_fan_right_front_clean_alt_leftPrefixOnlyDefect_suffix_source_decomposition`.
  For an opposite alt defect sourced from the old suffix, the wrapper now
  proves a four-way split:
  1. it is already an original opposite defect;
  2. it is an omitted old common vertex on the same-side old path;
  3. the alt prefix witness is the front vertex `w`;
  4. the witness is an old common vertex but the order transport from
     `alt.takeUntil c` back to the old path `takeUntil c` fails.
- Added the no-obstruction recovery wrappers
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_suffix_source_recovery_of_no_obstructions`
  and the right analogue.  These turn the four-way split into the exact
  old-suffix recovery obligation needed by the previous `source_cases`
  interface, provided the three genuine obstruction classes are ruled out.
- Added the secondary-minimality bridge wrappers
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.false_of_secondary_minimal_replacement_altRight_measure_le_source_obstructions`
  and the right analogue.  The high-level contradiction now needs:
  `no_prefix_source`, same-side overlap exclusion, front-witness exclusion,
  and old-common order transport; it no longer needs an opaque
  `suffix_source` assumption.
- Added the front-common exclusion wrappers
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_no_front_source_of_weighted_min_of_front_common`
  and the right analogue.  If the front witness `w` is already an old common
  vertex of the original pair, the existing front-common commonCard descent
  contradicts weighted minimality.  Thus the front-witness obstruction is
  closed in the old-common subcase.
- Added the high-level front-common source-obstruction wrappers
  `terminalSetFanLeftBridgeFrontLengthFailureExchangeInflationGuard.false_of_secondary_minimal_replacement_altRight_measure_le_source_obstructions_front_common`
  and the right analogue.  These feed the old-common front-witness exclusion
  directly into the secondary-minimality contradiction, so that in the
  old-common-front subcase the remaining explicit assumptions are only the
  same-side overlap exclusion and old-common order transport.
- Added direct front-common contradictions
  `terminal_set_fan_left_front_common_false_of_weighted_min` and the right
  analogue.  In the old-common-front subcase the replacement pair itself has
  strictly smaller common-cardinality, so this case does not depend on suffix
  source bookkeeping.
- Added the bypass/drop order bridge
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_suffix_order_of_no_overlap`
  and the right analogue.  Once same-side overlap is excluded, order transport
  from `alt.takeUntil c` back to the original old suffix is automatic.
- Added the reduced suffix-source recovery wrappers
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_suffix_source_recovery_of_no_overlap`
  and the right analogue, plus the secondary-minimality wrappers
  `...measure_le_overlap_front_obstructions`.  The explicit `horder`
  assumption is no longer needed at the high level.
- Added front-not-opposite exclusions
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_no_front_source_of_no_overlap_of_front_not_right`
  and the right analogue, then packaged them as
  `...suffix_source_recovery_of_no_overlap_front_not_right` / right-not-left.
  Thus a front-source obstruction can survive only when the front vertex is on
  the opposite old path but is not old common.

Verifier result:
- `WOWII198a` passes cleanly with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.
- Hygiene checks: no `sorry`/`admit`/`#check`/`conflict` in the touched Lean
  file and no tab characters.

Strategic status:
- The current route is still coherent.  The previous large defect-subset
  problem has now been converted into a small number of mathematically
  meaningful residuals, not an unstructured Lean engineering problem.
- Order transport is closed under no-overlap.  It should no longer be treated
  as an independent blocker.
- The remaining suffix-source target is now sharply localized:
  1. prove the same-side overlap exclusion, or turn overlap into a
     commonCard/splice descent;
  2. handle the opposite-only front case (`w` old-right-only in the left
     branch, old-left-only in the right branch), or show that the existing
     first-union/front hypotheses rule it out.
- The separate `no_prefix_source` obligation in the secondary-minimality
  wrapper remains outside this suffix-source reduction.
- If any of these residuals cannot be proved locally, that failure should be
  escalated to the splice/commonCard descent layer rather than patched by
  adding more residual hypotheses.

## Round update, omitted-common overlap closure

Lean progress:
- Added the strict counting helper
  `card_lt_of_subset_insert_erase_erase_mem`.  It covers the exact case needed
  when the new common set is contained in an inserted singleton plus the old
  common set with two known old common vertices removed.
- Added omitted-common strict common-card descents:
  `terminal_set_fan_left_front_clean_alt_commonCard_lt_of_no_right_suffix_only_of_omitted_common`
  and the right analogue.  These strengthen the earlier front-common descent:
  if an additional old common vertex `zOmit` is absent from the replacement
  separator path and `zOmit ≠ x`, then the cross-swap replacement has strictly
  smaller common-cardinality.
- Added same-side overlap exclusions:
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_no_overlap_of_weighted_min_and_no_prefix_source`
  and the right analogue.  The proof splits on `z = x`: the equality case is
  exactly the existing `no_prefix_source` obstruction, while `z ≠ x` is ruled
  out by the omitted-common strict descent plus weighted minimality.
- Added high-level secondary-minimality wrappers that no longer require an
  explicit `hno_overlap` hypothesis:
  `...false_of_secondary_minimal_replacement_altRight_measure_le_front_obstructions`,
  `...false_of_secondary_minimal_replacement_altRight_measure_le_front_not_right`,
  and the two right-side analogues.  In these branches, same-side overlap is
  generated internally from weighted minimality, `x ≠ v`, and `no_prefix_source`.
- Added prefix-source reductions
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_prefix_source_eq_x_or_not_right_of_weighted_min`
  and the right analogue.  Thus a prefix-source obstruction cannot be a
  non-`x` old common vertex: if such a point exists, the same omitted-common
  descent contradicts weighted minimality.  The remaining prefix-source
  subcases are now only `z = x` and old same-side-only prefix points.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- Same-side overlap is no longer a real residual obstruction once the branch
  has weighted minimality, `x ≠ v`, and `no_prefix_source`.
- Front-not-opposite is also closed at the secondary-minimality wrapper level:
  the old `hno_overlap` premise has been eliminated from those wrappers.
- The suffix-source route is still on the right track.  It has reduced the
  problem to two genuine main-chain tasks rather than local bookkeeping:
  1. prove or discharge the reduced `no_prefix_source` cases (`z = x` and
     old same-side-only prefix points);
  2. handle the opposite-only front case (`w` lies on the opposite old path but
     is not old common), likely by a first-union/order argument or by extracting
     a splice/common-card descent.

## Round update, reduced-prefix lifted to front wrappers

Lean progress:
- Added reduced-prefix no-prefix-source wrappers:
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_no_prefix_source_of_reduced_prefix_obstructions`
  and the right analogue.  Full `no_prefix_source` is now formally reduced to
  exactly two subgoals: exclude the `z = x` prefix-defect case, and exclude an
  old same-side-only prefix point.
- Lifted that reduction to the high-level secondary-minimality contradiction
  wrappers:
  `...measure_le_front_not_right_of_reduced_prefix_obstructions`,
  `...measure_le_front_not_left_of_reduced_prefix_obstructions`,
  `...measure_le_front_obstructions_of_reduced_prefix_obstructions`, and the
  `...source_obstructions_front_common_of_reduced_prefix_obstructions`
  wrappers.  These wrappers derive full `no_prefix_source` internally and then
  reuse the existing front/no-overlap/common-front contradictions.
- Verified that common-front can now bypass explicit `hno_overlap`: common-front
  gives `hno_front`, and reduced-prefix gives the full prefix/no-overlap route.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This round moved the reduced-prefix obstruction from a local lemma to the
  relevant high-level contradiction interfaces.  The remaining proof debt is no
  longer hidden in `hno_prefix_source`.
- The `z = x` case is genuine: in the left branch, for example, the replacement
  left path is `rs` and the hypotheses include `x ∉ rs.support`, while
  `altRight` still contains `x`.  So `x` can naturally become a new
  right-prefix-only defect unless the witness geometry is ruled out.
- Existing `source_common_or_front` lemmas already classify the witness for any
  such defect as either the front vertex `w` or an old common vertex.  The next
  honest target is to specialize that classification to `z = x` and prove a
  front/common descent, not to add more opaque residual hypotheses.
- The old same-side-only prefix-point residual is also real: existing suffix
  recovery/decomposition lemmas act on opposite-suffix sources, while this
  obstruction lies on the old same-side prefix before `x`.  It needs a separate
  front-prefix or first-witness descent.
- The bottom full finite two-fan/splice theorem block is still frozen/commented.
  Active progress remains on the residual/wrapper chain above it.

## Round update, `z = x` source witness split

Lean progress:
- Added the `z = x` source-witness classifiers
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_x_source_front_or_common`
  and the right analogue.  If `x` itself is the new opposite-prefix-only
  defect in the replacement pair, then its defect witness is now formally
  classified as either the front vertex `w` or an old common vertex `c ≠ x`.
- Added the `no_x` reducers
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_no_x_source_of_front_common_obstructions`
  and the right analogue.  These replace the abstract assumption
  `∀ z, z ∈ altDefect → z = x → False` by two concrete witness exclusions:
  no front witness `x ∈ alt.takeUntil w`, and no old-common witness
  `x ∈ alt.takeUntil c`.
- Added full no-prefix-source wrappers
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_no_prefix_source_of_x_source_front_common_obstructions`
  and the right analogue.  These combine the new `z = x` witness split with
  the previous reduced-prefix wrapper; the remaining no-prefix-source debt is
  now exactly:
  1. front-witness exclusion for `x`;
  2. old-common-witness exclusion for `x`;
  3. old same-side-only prefix-source exclusion.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This improves the main route because `hno_x` has been split into geometric
  witness cases that match the existing front/common-front descent vocabulary.
- The front-witness subcase for `x` appears to overlap the previously hard
  opposite-only front branch: if the witness is `w`, then the next target is to
  show either `w` is not on the opposite old suffix, or extract the same
  front/opposite splice descent already isolated as a residual.
- The old-common-witness subcase should be attacked by an order/common-card
  descent: `x` is omitted from the separator path, while some old common
  witness `c ≠ x` is retained and lies after `x` on the replacement path.
- The old same-side-only prefix-source subcase remains separate from this
  `z = x` split and still needs a first-prefix/front-prefix descent.

## Round update, `x` front-source closed in front-not-opposite branch

Lean progress:
- Added the generic endpoint append/drop bridge
  `mem_dropUntil_append_right_of_pivot_endpoint_ne`.  If the pivot is the
  endpoint of a path-like left append segment, then any non-pivot vertex seen
  after the pivot in the appended walk comes from the right segment.
- Used this to prove
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_no_x_front_source_of_front_not_right`
  and the right analogue.  In the left branch, if
  `altRight = oldLeft.takeUntil x ++ oldRight.dropUntil x` and
  `w ∉ oldRight.support`, then `x ∈ altRight.takeUntil w` is impossible.
  The symmetric statement closes the right branch under `w ∉ oldLeft.support`.
- Added local no-prefix-source wrappers
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_no_prefix_source_of_front_not_right_common_obstructions`
  and
  `terminal_set_fan_right_front_clean_alt_leftPrefixOnlyDefect_no_prefix_source_of_front_not_left_common_obstructions`.
  In the front-not-opposite branches, full `no_prefix_source` now needs only:
  old-common `x` witness exclusion and old same-side-only prefix exclusion.
- Lifted the same reduction to the high-level secondary-minimality wrappers:
  `...measure_le_front_not_right_of_x_source_common_obstructions` and
  `...measure_le_front_not_left_of_x_source_common_obstructions`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This closes one real `z = x` source branch.  The front witness for `x` is no
  longer a residual in the easy front-not-opposite case; the proof debt moved
  strictly toward the genuinely hard opposite/front and old-common cases.
- The next exact targets are:
  1. old-common `x` witness exclusion: rule out
     `x ∈ alt.takeUntil c` for old common `c ≠ x`, likely by common-card or
     order descent;
  2. old same-side-only prefix-source exclusion: rule out a same-side-only
     point before `x`, likely by first-prefix/front-prefix descent;
  3. opposite-only front case: when the front vertex lies on the opposite old
     path but is not old common, extract a splice/common-card descent or show
     it contradicts the first-union/front hypotheses.
- The bottom full finite two-fan/splice theorem block is still frozen.  Active
  theorem-level progress remains in the residual/wrapper chain until these
  source bridges are connected to the final finite wrapper.

## Round update, old-common `x` witness narrowed to a double-suffix residual

Lean progress:
- Added the left/right residual-shape lemmas
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_old_common_x_witness_suffix_residual_of_front_not_right`
  and
  `terminal_set_fan_right_front_clean_alt_leftPrefixOnlyDefect_old_common_x_witness_suffix_residual_of_front_not_left`.
  In the left branch, if an old-common vertex `c` witnesses
  `x ∈ altRight.takeUntil c` while the front is not on the old right path,
  then `c` is forced into both `rs.dropUntil w` and
  `oldRight.dropUntil x`.  The right branch is the symmetric statement.
- Added local no-prefix-source reducers
  `terminal_set_fan_left_front_clean_alt_rightPrefixOnlyDefect_no_prefix_source_of_front_not_right_suffix_common_obstructions`
  and
  `terminal_set_fan_right_front_clean_alt_leftPrefixOnlyDefect_no_prefix_source_of_front_not_left_suffix_common_obstructions`.
  These replace the broad old-common witness exclusion by a smaller
  double-suffix residual exclusion.
- Lifted this reduction to the high-level secondary-minimality wrappers:
  `...measure_le_front_not_right_of_suffix_common_obstructions` and
  `...measure_le_front_not_left_of_suffix_common_obstructions`.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The old-common branch is not closed, but it is now structurally smaller.
  The remaining left residual is:
  `c ∈ rs.dropUntil w`, `c ∈ oldLeft.support`,
  `c ∈ oldRight.dropUntil x`, and `c ≠ x`; the right residual is symmetric.
- This residual is not contradicted by the existing middle/post/suffix-only
  guards, because those guards only eliminate same-side-only or suffix-only
  vertices.  It likely needs a new order/common-card or secondary-minimality
  argument that treats a retained old-common vertex after the front.
- The old same-side-only prefix-source branch remains separate.  Existing
  prefix-cover and length-failure machinery already targets it, so the next
  productive step is to connect that machinery to the current
  `hno_same_only` assumptions, while separately designing the new
  double-suffix old-common descent.

## Round update, suffix-common residual lifted to support-minimal theorem layer

Lean progress:
- Added support-minimal theorem-layer residual-shape lemmas:
  `terminalSetFanLeftSupportMinimalBridgeFrontCoverLengthFailureExchangeInflationGuardedPrefixSplitResidual.suffix_common_or_same_only_of_secondary_minimal_replacement_altRight_measure_le_front_not_right`
  and
  `terminalSetFanRightSupportMinimalBridgeFrontCoverLengthFailureExchangeInflationGuardedPrefixSplitResidual.suffix_common_or_same_only_of_secondary_minimal_replacement_altLeft_measure_le_front_not_left`.
- These lemmas convert the previous negative high-level wrappers into positive
  residual alternatives.  In the left front-not-right branch, a
  measure-non-increasing replacement plus secondary minimality now forces:
  either a double-suffix old-common witness
  `c ∈ rs.dropUntil w`, `c ∈ oldLeft.support`,
  `c ∈ oldRight.dropUntil x`, `c ≠ x`; or an old-left prefix-only source
  for the new right defect.  The right branch is symmetric.
- This is the first direct bridge from the recent suffix-common narrowing into
  the active `SupportMinimal...CoverLengthFailureExchangeInflation...`
  residual layer.  It does not close the residual, but it makes the next
  obstruction explicit at theorem-layer granularity.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.
- `git diff --check` passes, and
  `rg -n "\b(sorry|admit)\b|#check|conflict"
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`
  has no matches.

Strategic status:
- The current route still looks structurally correct: every new lemma is
  pushing the residual toward explicit witnesses at the same level as the
  theorem-chain output, not merely adding local rewriting.
- The remaining proof debt in this branch is now sharply split:
  1. eliminate the double-suffix old-common witness by an order/common-card
     descent or by showing it violates support-minimal replacement order;
  2. eliminate the same-side prefix-only source using the existing
     prefix-cover/length-failure machinery, likely by deriving the relevant
     `hno_same_only` contradiction from the first-prefix absent/exchange
     lemmas;
  3. after both are closed, promote the support-minimal residual split back
     into the active finite wrapper and only then reopen the frozen final
     two-fan/splice block.

## Round update, double-suffix residual normalized to non-apex old-common

Lean progress:
- Added local normalization lemmas
  `terminal_set_fan_left_suffix_common_residual_old_common_ne_apex` and
  `terminal_set_fan_right_suffix_common_residual_old_common_ne_apex`.
  They show that the double-suffix residual witness is an actual old-common
  vertex on both original paths and is distinct from both `v` and `x`.
- Added the reusable disjunction post-processors
  `terminal_set_fan_left_suffix_common_residual_old_common_ne_apex_or_same`
  and
  `terminal_set_fan_right_suffix_common_residual_old_common_ne_apex_or_same`.
  These turn any existing
  `double-suffix old-common witness ∨ same-side prefix-only source` split into
  a stronger
  `non-apex old-common suffix witness ∨ same-side prefix-only source` split.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This deliberately does not assume that the old-common witness survives in
  the replacement `toPath`; that would require a separate survival hypothesis.
  The useful gain is narrower and safer: the remaining old-common obstruction
  is now a genuine non-apex shared vertex in the old fan, behind `x` on the
  opposite old path and behind `w` on the replacement path.
- Next target: connect this normalized witness to the weighted/secondary
  minimality comparison.  The likely contradiction is not a local suffix-only
  obstruction, but a common-card/order descent: either the replacement retains
  enough old common vertices to violate secondary minimality, or the missing
  common vertex creates the same-side prefix-only source already exposed by the
  current residual split.

## Round update, weighted-minimal survival for suffix residuals

Lean progress:
- Added `right_suffix_mem_altRight_of_weighted_min` and
  `left_suffix_mem_altLeft_of_weighted_min`.  Under weighted minimality of the
  original path pair, every vertex in the old opposite suffix after `x`
  survives in the corresponding replacement `toPath`.
- Added residual post-processors
  `terminal_set_fan_left_suffix_common_residual_old_common_survives_or_same_of_weighted_min`
  and
  `terminal_set_fan_right_suffix_common_residual_old_common_survives_or_same_of_weighted_min`.
  These strengthen the previous
  `double-suffix old-common witness ∨ same-side prefix-only source` split to a
  split where the old-common witness is non-apex, old-common on both original
  paths, behind `x` on the opposite old path, behind `w` on the replacement
  path, and present in the new `alt` path.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This is a real route correction, not just local cleanup.  Earlier we could
  not safely assert that the double-suffix witness survived through
  `toPath`.  The new survival lemmas prove exactly the missing conditional:
  survival follows from weighted minimality, because failure of survival gives
  a cross-swap common-card descent.
- Remaining proof debt: use the surviving non-apex old-common witness inside
  the secondary-minimality/prefix-defect comparison, or show it forces the
  exposed same-side prefix-only source.  The residual is now at the right
  semantic level for that argument.

## Round update, support-minimal residual shape consumes survival

Lean progress:
- Added concrete support-minimal-output wrappers
  `terminal_set_fan_left_support_minimal_suffix_common_or_same_only_survives_of_weighted_min`
  and
  `terminal_set_fan_right_support_minimal_suffix_common_or_same_only_survives_of_weighted_min`.
- These wrappers consume the theorem-layer
  `suffix_common_or_same_only` output shape and return the same split with the
  suffix-common branch strengthened by old-common membership, non-apex
  distinctness, opposite-suffix membership, replacement-tail membership, and
  `alt` survival.

Verifier result:
- `WOWII198a` passes with
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The active residual is now ready to be consumed at the support-minimal layer:
  one branch is an explicit surviving old-common witness; the other is an
  explicit same-side prefix-only source.
- Next useful target is no longer survival.  It is to close one of these two
  exposed branches, preferably by deriving a strict prefix-defect decrease from
  the same-side source or by showing the surviving old-common witness imposes
  such a source.

## Round update, surviving old-common residual split sharpened

Lean progress:
- Added theorem-layer surviving residual wrappers
  `...suffix_common_or_same_only_survives_of_secondary_minimal_replacement_altRight_measure_le_front_not_right`
  and the right-side `altLeft` analogue.  The old-common residual now carries
  old-common membership on both original paths, opposite-suffix membership,
  replacement-tail membership, non-apex distinctness, and survival in the
  replacement `alt` path.
- Added `...false_of_secondary_minimal_replacement_..._of_surviving_suffix_common_obstructions`
  wrappers.  These expose the exact two remaining obstruction predicates:
  a surviving suffix old-common witness and the same-side prefix-only source.
- Added order-splitting lemmas
  `right_suffix_common_x_before_or_left_prefix_of_weighted_min` and
  `left_suffix_common_x_before_or_right_prefix_of_weighted_min`.  Under
  weighted minimality, a surviving old opposite-suffix common vertex is either
  after `x` in the replacement path, or it is also present in the old same-side
  prefix.
- Added post-processors
  `terminal_set_fan_left_surviving_suffix_common_order_or_left_prefix_or_same_of_weighted_min`
  and the right analogue.  They refine the residual to three branches:
  ordered surviving old-common, cross-prefix surviving old-common, or
  same-side prefix-only source.  The cross-prefix branch explicitly records
  the negated order fact `x ∉ alt.takeUntil c`, so it is exactly the bypass
  obstruction rather than just a loose membership overlap.

Verifier result:
- `WOWII198a` passes with
  `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- This confirms the current route is still structurally sound, but the old
  common branch is not automatically contradictory.  The real remaining hard
  case is now smaller: a vertex that is simultaneously in the old same-side
  prefix before `x` and the old opposite-side suffix after `x`, while also
  surviving in the replacement path.
- Next target: use the ordered branch with the existing
  `old_common_x_witness_suffix_residual` / front-not-right machinery, and
  separately attack the cross-prefix branch as the genuine bypass obstruction.

## Round update, theorem layer exposes the cross-prefix obstruction

Lean progress:
- Added theorem-layer wrappers
  `...false_of_secondary_minimal_replacement_altRight_measure_le_front_not_right_of_surviving_order_or_left_prefix_obstructions`
  and
  `...false_of_secondary_minimal_replacement_altLeft_measure_le_front_not_left_of_surviving_order_or_right_prefix_obstructions`.
- These consume the surviving residual theorem and immediately post-process it
  through the weighted-minimality order split.  The resulting false criterion
  now has three explicit obstruction predicates: ordered surviving old-common,
  cross-prefix surviving old-common, and same-side prefix-only source.

Verifier result:
- `WOWII198a` passes with
  `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The ordered and same-side-source cases are now directly pluggable into
  existing front-clean / prefix-defect machinery.  The remaining non-mechanical
  proof obligation is the cross-prefix branch:
  a surviving common vertex lies before `x` on the old same-side path and after
  `x` on the old opposite-side path, while `x` is not before it in the
  replacement path.
- This is the right next attack point.  Proving that cross-prefix predicate
  false, or turning it into a strict secondary-measure descent, should close
  the main residual split.

## Round update, cross-prefix obstruction eliminated

Lean progress:
- Added local weighted-minimality contradictions
  `right_suffix_left_prefix_common_false_of_weighted_min` and
  `left_suffix_right_prefix_common_false_of_weighted_min`.
- These instantiate the existing cross-swap common-card descent at `y = x`.
  A vertex `c ≠ x` cannot be both in the old opposite-side suffix after `x`
  and in the old same-side prefix before `x`; otherwise a swapped pair has
  strictly smaller `terminalPathPairCommonCard`, contradicting weighted
  minimality.
- Added two-way post-processors
  `terminal_set_fan_left_surviving_suffix_common_order_or_same_of_weighted_min`
  and the right analogue.  The previous three-way split is now reduced to:
  ordered surviving old-common, or same-side prefix-only source.
- Added theorem-layer wrappers
  `...false_of_secondary_minimal_replacement_altRight_measure_le_front_not_right_of_surviving_order_obstructions`
  and
  `...false_of_secondary_minimal_replacement_altLeft_measure_le_front_not_left_of_surviving_order_obstructions`.
  The theorem layer no longer requires a separate cross-prefix obstruction
  hypothesis.

Verifier result:
- `WOWII198a` passes with
  `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The cross-prefix branch is closed.  This is a genuine simplification of the
  main WOWII198a residual, not just a restatement.
- Remaining hard branches:
  1. ordered surviving old-common: an old common vertex survives after the
     replacement pivot, with `x` before it on the replacement path;
  2. same-side prefix-only source: the replacement creates or preserves a
     prefix-only defect source on the same side.
- Next target: connect the ordered surviving old-common branch to the existing
  front-clean / prefix-defect descent machinery, and separately check whether
  the same-side source already gives the strict secondary-measure decrease
  required by `terminalPathPairSecondaryMinimalAfterWeighted`.

## Round update, ordered old-common sharpened to double suffix

Lean progress:
- Added
  `right_suffix_common_left_suffix_of_weighted_min` and
  `left_suffix_common_right_suffix_of_weighted_min`.
- These use the just-closed cross-prefix obstruction to show that an old
  common vertex on the opposite-side suffix cannot lie in the same-side prefix.
  Therefore it must lie in the same-side suffix after `x`.
- Added two post-processors
  `terminal_set_fan_left_surviving_suffix_common_double_suffix_order_or_same_of_weighted_min`
  and the right analogue.  The surviving residual is now narrowed to:
  a double-suffix ordered old-common vertex, or the same-side prefix-only
  source.

Verifier result:
- `WOWII198a` passes with
  `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- The old-common branch is smaller than before: the remaining common witness
  is after `x` on both original paths and after `x` in the replacement path.
  This rules out all “one side before `x`, one side after `x`” configurations.
- Next mechanical lift: expose this double-suffix ordered branch at the
  theorem-layer wrappers, replacing the current ordered-only obstruction
  predicate.  After that, the real mathematical split is double-suffix common
  versus prefix-absent/same-side source.

## Round update, double-suffix obstruction exposed at theorem layer

Lean progress:
- Added theorem-layer wrappers
  `...false_of_secondary_minimal_replacement_altRight_measure_le_front_not_right_of_surviving_double_suffix_order_obstructions`
  and
  `...false_of_secondary_minimal_replacement_altLeft_measure_le_front_not_left_of_surviving_double_suffix_order_obstructions`.
- These are thin lifts over the previous ordered-obstruction wrappers.  They
  derive the missing same-side suffix membership with
  `right_suffix_common_left_suffix_of_weighted_min` / the right analogue, so
  callers no longer need to rule out a merely one-sided ordered common point.

Verifier result:
- `WOWII198a` passes with
  `lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Strategic status:
- Current theorem-layer residual is now exactly:
  double-suffix ordered old-common, or same-side prefix-only source.
- The next nontrivial attack should decide which of these is convertible to
  the existing prefix-absent guarded branch.  The same-side source already has
  the shape of a prefix-absent witness; the double-suffix common branch likely
  needs a separate common-suffix descent or separator argument.
