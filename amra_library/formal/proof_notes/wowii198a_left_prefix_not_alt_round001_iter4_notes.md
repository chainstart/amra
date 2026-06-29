## 2026-06-28 left-prefix not-alt descent iteration-4

Current first blocker:
- The requested theorem
  `terminal_set_fan_left_suffix_retention_left_prefix_not_alt_commonCard_descent`
  remains closed from iteration 3.
- The verifier still fails in the downstream parent theorem
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, now at
  `Wowii198aLeftmost.lean:6401:14` after this iteration's helper insertion.

External sources relied on:
- None. The prompt allowed open research, but this iteration used only the
  local Lean workspace, local proof notes, local mathlib/Lean source, and the
  configured Lean verifier.
- The requested artifact files
  `artifacts/open_problem_screening/latest/.../context_bundle.md` and
  `artifacts/open_problem_screening/latest/.../math_tools_report.md` are not
  present in this workspace; I attempted to read them before editing and the
  shell reported `No such file or directory`.

Lean progress:
- Added checked support helper
  `not_mem_left_suffix_fallback_of_not_left_prefix`.
- The helper proves that the symmetric fallback left path
  `rs.takeUntil y ++ oldLeft.dropUntil y` omits `x`, provided `y` is not in
  `oldLeft.takeUntil x`, `x ∉ rs.support`, and the old left path is simple.
- This is the first reusable support fact needed for the right-suffix residual
  fallback branch, where the stale proof currently has a prefix vertex on
  `rs` that is old-left-only.

Verifier command:
- `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`

Verifier result:
- Failed at the pre-existing downstream blocker:
  `AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean:6401:14: error: Type mismatch`
  where `hpair_measure_min` has weighted-minimality type but Lean needs
  `False`.

Next target:
- Prove the symmetric right-suffix residual fallback lemma.  It should handle
  a vertex `y ∈ rs.takeUntil z` that is old-left-only in the right-suffix
  branch, split on whether `y` is retained in `altRight`, and in the non-alt
  case use the new fallback-omits-`x` helper as the support-length/common-card
  descent route before applying weighted minimality.
