## 2026-06-27 bad-pivot extremal iteration 6

Current first blocker:
- `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` is still
  blocked by the earlier active theorem
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- The Lean file fails at the two residual containment branches where
  `hpair_measure_min` is used at a membership goal in
  `(((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`.

External sources relied on:
- None from web or literature search.
- Local context read: supplied `context_bundle.md`, supplied
  `math_tools_report.md`, current Lean source, and local mathlib grep output
  for `Walk.takeUntil` / `Walk.dropUntil` APIs.

Tool checks:
- Ran the configured verifier:
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.
  Result: failed at lines 4895 and 4982 with the same membership-type mismatch.
- Ran an exhaustive Python sanity check for the theorem's path-level shape on
  all labelled simple graphs with 2, 3, and 4 vertices, plus the first 1023
  five-vertex graph masks. The encoding required the selected pair to minimize
  the weighted measure among all simple `v-s` / `v-t` path pairs in the graph.
  Result: no counterexample found in that bounded sample. This is route
  evidence only, not a proof.
- Started a broader exhaustive search through six vertices and interrupted it
  as too slow; that interrupted run is not used as evidence.

Lean assessment:
- The current target helper
  `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` is only a
  wrapper around `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, so
  it cannot bypass the bad arbitrary-pivot containment proof.
- Existing checked helpers `exists_last_bad_pivot_on_rs` and
  `exists_first_bad_pivot_on_rs` can choose an extremal bad pivot, but the two
  residual branches also need the weighted-minimality fallback for residual
  vertices that are not immediately shown to lie in the alternate-right support.

Next Lean target:
- Prove a real extremal core before the arbitrary-`z` theorem, using
  `exists_last_bad_pivot_on_rs` / `exists_first_bad_pivot_on_rs` and a weighted
  fallback lemma for the non-alt residual vertices. Then make both
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` and
  `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` call that
  core.
