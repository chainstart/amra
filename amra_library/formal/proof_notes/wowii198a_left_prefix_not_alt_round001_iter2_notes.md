## 2026-06-28 left-prefix not-alt descent iteration-2

External sources relied on:
- None.  I used the local Lean file, local mathlib sources, the configured
  Lean verifier, and the prompt-supplied context.  The artifact path named in
  the prompt was not present under this workspace.

Verifier baseline:
- Command:
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`
- Result: failed with the same two diagnostics:
  `Wowii198aLeftmost.lean:5422:4`, where the `hy_suffix` branch returns the
  later-return witness instead of a common-card descent pair; and
  `Wowii198aLeftmost.lean:6188:14`, where `hpair_measure_min` is used where
  `False` is needed.

Proof analysis:
- In the `hy_suffix` branch, the non-suffix fallback pair
  `((right.takeUntil y).append (rs.dropUntil y), altRight)` is still the
  natural construction.  Since `y` is after `x` on the old right path, `x`
  remains on the fallback-left side; the strict common-card containment must
  instead prove `x ∉ altRight.support`.
- The available witness
  `r ∈ ((right.dropUntil x).dropUntil y).support`,
  `r ≠ y`, and `r ∈ (left.takeUntil x).support` is exactly the ordered
  loop-erasure certificate: a left-prefix vertex reappears in the right suffix
  after `y`, so `toPath` should bypass the segment containing `x` and `y`.
- The next helper should be a narrow ordered bypass-erasure lemma for this
  shape, not a broad replacement of `Walk.bypass`:
  from `r ∈ (left.takeUntil x).support` and
  `r ∈ ((right.dropUntil x).dropUntil y).support` with `y` after `x`, prove
  `x ∉ (((left.takeUntil x).append (right.dropUntil x)).toPath).support`.
  With that fact, the existing non-suffix containment proof can be reused by
  deriving `a ≠ x` from the `altRight` side.
- The downstream stale old-right-suffix branch at line 6188 is a separate
  pivot-choice issue: the branch has a prefix-side residual bad vertex, so it
  should be routed through `exists_first_bad_pivot_on_rs` rather than the
  current last-bad-pivot-only local argument.

Main chain:
- Closing the ordered bypass-erasure helper plugs directly into
  `terminal_set_fan_left_suffix_retention_left_prefix_not_alt_commonCard_descent`.
- That closes the residual false lemma, then
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`,
  `terminal_set_fan_left_suffix_retention_alt_intersections_control`,
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`,
  the splice descent chain, the two-fan theorem, Chvatal-Erdos traceability,
  and finally `conjecture198a`.
