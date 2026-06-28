# WOWII198a suffix retention round 003 iteration 6 notes

Target:
`terminal_set_fan_left_suffix_retention_alt_intersections_control`.

Current first blocker:
the suffix-retention package needed by
`terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, then
`terminal_set_fan_splice_descent_left_of_hsep`, the mirrored right splice,
`terminal_set_two_fan_of_no_small_endpoint_separator`, the longest-path
missed-vertex contradiction, and `conjecture198a`.

External sources:
none.  Only local Lean/mathlib source files and local proof-lab artifacts were
used.

Tool checks:

- Ran the required Lean verifier:
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.
  It fails at the two known bad branches inside
  `terminal_set_fan_left_suffix_retention_alt_intersections_control`, and at
  the two downstream splice wrappers that still use `hdirect` as strict
  descent.
- Ran a small Python finite route check for a hand-built obstruction where the
  bad old-left-prefix vertex exists but weighted minimality fails because a
  zero-common alternate pair is available.  This confirms weighted minimality is
  doing essential work.
- Ran an exhaustive optional-edge search over 36 fixed small path-shape
  families enforcing the target hypotheses, including weighted minimality of
  the old pair.  No counterexample was found.
- Started a broader randomized search over eight-vertex shapes, then stopped it
  after 60 seconds without a result; no conclusion was drawn from that partial
  run.

Lean route assessment:

- The left-prefix bad branch has local facts
  `z ∈ rs.support`, `z ∈ (pair.1).takeUntil x`, `z ∉ pair.2.support`, and
  `z ∉ (rs.takeUntil w).support`.
  The natural descent candidate is the left replacement
  `(pair.1.takeUntil z).append (rs.dropUntil z)`, converted by `toPath`.
  To finish, one must prove its erased common support with `pair.2` is contained
  in the old erased common support with `x` removed, or else prove equal common
  card and smaller weighted measure.
- The old-right-suffix bad branch has local facts
  `z ∈ rs.support`, `z ∈ pair.2.dropUntil x`, and `z ∉ pair.1.support`.
  The same missing package must control the first/last later crossing; `hfirst`
  alone only says such vertices are not before `w` on `rs`.

Next theorem-level package:
prove a dedicated bad-pivot weighted-descent lemma for these two cases.  It
should explicitly choose the first bad later pivot on `rs.dropUntil w` and show
that the corresponding prefix/suffix splice either strictly lowers
`terminalPathPairCommonCard` or preserves common card while shortening
`terminalPathPairSupportLength`, contradicting `hpair_measure_min`.
