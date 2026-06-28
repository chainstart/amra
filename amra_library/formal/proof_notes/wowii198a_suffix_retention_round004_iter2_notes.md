## 2026-06-27 terminal-set suffix-retention bad-pivot iteration-2

External sources relied on:
- None.  I used only the supplied context bundle, supplied math tools report,
  local workspace/mathlib source, the configured Lean verifier, and a local
  Python finite-model sanity check.

Lean work:
- Updated the target declaration binder from `∀ z` to `∀ y` in `hfirst`, so
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` matches the
  requested source declaration text.
- Wired `terminal_set_fan_left_suffix_retention_alt_intersections_control`
  through `terminal_set_fan_left_suffix_retention_bad_pivot_descent` by
  contradiction against `not_terminalPathPairCommonCard_lt_of_weighted_min`.
  This removes the independent bad-intersection open exits in the control
  lemma once the bad-pivot descent lemma is proved.

Tool check:
- Ran the configured verifier after the edit.  The control-lemma errors at the
  old bad-intersection branches disappeared.  Remaining target errors are the
  two unproved descent witnesses in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- Ran a bounded Python path-list search over small labelled graphs for a model
  satisfying weighted minimality, `hfirst`, `hdirect`, suffix retention, and a
  bad `z ∈ rs.support ∩ altRight.support`.  Exhaustive search through five
  vertices and randomized search on six through eight vertices found no
  counterexample.  This supports the bad-pivot route but does not replace the
  Lean proof.

Remaining formal blocker:
- The first missing Lean package is still the two-branch descent inside
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`: choose an
  order-extremal bad pivot on `rs`, build the secondary splice, and prove
  erased common-support containment or a weighted-measure contradiction.
