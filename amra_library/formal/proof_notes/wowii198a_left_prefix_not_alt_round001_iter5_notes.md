## 2026-06-28 left-prefix not-alt descent iteration-5

Current first blocker:
- The requested theorem
  `terminal_set_fan_left_suffix_retention_left_prefix_not_alt_commonCard_descent`
  remains closed: its `hy_suffix` branch now uses the later-return witness
  through `terminal_set_cross_swap_commonCard_lt_of_later_return`.
- The configured verifier still fails downstream in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, at the stale
  right-suffix branch proof term:
  `Wowii198aLeftmost.lean:6401:14`.

External sources relied on:
- None. The prompt allowed open research, but this iteration used only local
  Lean files, local proof notes, and the configured Lean verifier.
- The requested run-artifact context files were not present at the supplied
  path under this workspace. Attempts to read both `context_bundle.md` and
  `math_tools_report.md` returned `No such file or directory`.

Verifier command:
- `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`

Verifier result:
- Failed with:
  `AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean:6401:14: error: Type mismatch`
- Lean expected `False`, but the proof term is still
  `hpair_measure_min`, whose type is weighted minimality:
  `∀ pair', terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair'`.

Diagnosis:
- The current `bad_pivot_descent` proof selects a last bad pivot on `rs`.
  That is the right extremal choice for the old-left-only branch, where the
  later residual lies in `rs.dropUntil z`.
- The failing branch is the symmetric old-right-only branch.  Its splice
  introduces a local obligation for a vertex in `rs.takeUntil z` that is
  old-left-only.  A last bad pivot gives no control over such prefix vertices.
- The exact replacement is not another direct use of weighted minimality.
  This branch needs either:
  1. a first-bad-pivot version of the right-suffix splice argument using
     `exists_first_bad_pivot_on_rs`, or
  2. a proved fallback lemma for the prefix old-left-only residual.  In the
     non-alt subcase this should use
     `not_mem_left_suffix_fallback_of_not_left_prefix` to build the candidate
     fallback `rs.takeUntil y ++ oldLeft.dropUntil y` and then apply weighted
     minimality only after proving the resulting strict common-card descent.

How this plugs into the main chain:
- Closing this right-suffix residual branch proves
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- That is consumed by
  `terminal_set_fan_left_suffix_retention_alt_intersections_control`, then by
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, then the
  splice descent chain, the two-fan theorem, the Chvatal-Erdos traceability
  reduction, and finally `conjecture198a`.

Next target:
- Prove a right-suffix first-bad-pivot residual fallback lemma, rather than
  continuing to use the last-bad-pivot formulation in the prefix branch.
