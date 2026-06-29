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
- The temporary `#check` lines were removed, so the file verifies without proof
  debug output.

Next target:
- Poll/confirm the parallel WOWII16 verification.
- If committing, include the proof notes with the Lean change. The mathematical
  next cleanup would be to extract the local successor principle into a named
  private lemma, but it is no longer blocking the main theorem.
