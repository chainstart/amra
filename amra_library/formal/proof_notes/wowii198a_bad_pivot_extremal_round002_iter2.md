# WOWII198a bad-pivot extremal round 002 iteration note

Current first blocker between the stage theorem
`terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` and
`conjecture198a` is still the retained-suffix bad-pivot package.  The build
fails before downstream first-crossing work, inside
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.

External sources relied on:
- None from web or literature.
- Local run context was read from the supplied `context_bundle.md` and
  `math_tools_report.md`.

Verifier:
- Ran
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.
- Lean still reports exactly two errors: the left residual branch and the
  right residual branch both use `hpair_measure_min` where membership in the
  old erased common-support set with `x` removed is required.

Tool check:
- Started a Python/NetworkX bounded search for concrete counterexamples to the
  exact extremal-target hypothesis shape, including weighted minimality of the
  old terminal path pair.  The search did not return within about one minute
  and was interrupted, so it is inconclusive and is not used as evidence.

Lean assessment:
- The newly declared
  `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` currently
  only unwraps the existential bad witness and delegates to the older
  arbitrary-pivot theorem.
- The older theorem is still proving residual containment for the arbitrary
  bad pivot.  In the left-prefix branch, the unresolved case has
  `y ∈ rs.dropUntil z` and `y ∈ oldRight`; in the right-suffix branch, the
  unresolved case has `y ∈ rs.takeUntil z` and `y ∈ oldLeft`.  The current
  hypotheses do not provide the missing old-side membership needed by
  `common_support_erase_card_lt_of_subset_erase_common`.

Next required theorem-level move:
- Replace the body of the extremal helper with a real finite bad-set selection.
  It needs either:
  1. a proved last/first bad-pivot containment lemma strong enough to show the
     residual `rs`-side vertices are already old common vertices distinct from
     `x`, or
  2. a proved support-length descent lemma for the secondary splice, used with
     `false_of_weighted_min_and_commonCard_le_supportLength_lt`.

No trusted assumptions, theorem weakening, or forbidden proof tokens were
introduced in this iteration.
