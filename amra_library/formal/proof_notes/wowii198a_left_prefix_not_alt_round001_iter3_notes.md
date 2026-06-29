## 2026-06-28 left-prefix not-alt descent iteration-3

External sources relied on:
- None. The prompt allowed open research, but this iteration used only the
  local Lean workspace, local mathlib files under `.lake`, the configured Lean
  verifier, and prompt-supplied context. The requested artifact directory
  `artifacts/open_problem_screening/latest/.../round-001-terminal-set-fan-left-suffix-retention-left-prefix-not-alt-commoncard-descent`
  is not present in this workspace.

Verifier command:
- `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`

Progress:
- Proved the requested target
  `terminal_set_fan_left_suffix_retention_left_prefix_not_alt_commonCard_descent`.
- Added `dropUntil_start_eq_self` for normalizing a `dropUntil` at a walk's
  start vertex with an arbitrary proof of start membership.
- Added
  `terminal_set_cross_swap_commonCard_lt_of_later_return`. This uses the
  later-return witness
  `r ∈ ((right.dropUntil x).dropUntil y).support ∩ (left.takeUntil x).support`
  to build the two cross-splices at `x`. The swapped-left path omits the old
  common vertex `r`, and the four raw support-overlap cases show every new
  common vertex is old common, so the erased common-card strictly descends.

Remaining verifier blocker:
- `Wowii198aLeftmost.lean:6372:14`: in the parent
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, the old
  right-suffix branch still has the stale line `exact hpair_measure_min` where
  Lean needs `False`.
- Local branch shape: current pivot `z` is a right-suffix bad pivot; the
  blocking vertex `y` lies in `rs.takeUntil z`, is on the old left path, and
  fails the old-common-without-`x` triple. This is the prefix-bad obstruction
  noted in the prior iteration.

Next target:
- Replace the right-suffix branch's last-bad-pivot handling with a first-bad
  pivot route, using `exists_first_bad_pivot_on_rs`, or add the symmetric
  right-suffix residual false lemma that turns the prefix bad vertex into an
  actual common-card descent before applying weighted minimality.
